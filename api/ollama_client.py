import os
import requests
import json
import logging
from typing import Any, Dict, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OllamaClient:
    """
    Client for interacting with local Ollama models.
    Designed to be compatible with adalflow's client interface.
    """
    
    def __init__(self, api_url: Optional[str] = None, default_model: Optional[str] = None):
        """
        Initialize the Ollama client.
        
        Args:
            api_url: The URL of the Ollama API. If None, will use OLLAMA_URL env var or default to http://localhost:11434
            default_model: The default model to use. If None, will use OLLAMA_MODEL env var or default to llama3
        """
        self.api_url = api_url or os.environ.get('OLLAMA_URL', 'http://localhost:11434')
        self.default_model = default_model or os.environ.get('OLLAMA_MODEL', 'llama3')
        
        # Ensure API URL ends with /api
        if not self.api_url.endswith('/api'):
            self.api_url = f"{self.api_url.rstrip('/')}/api"
            
        logger.info(f"Initialized Ollama client with URL: {self.api_url}, default model: {self.default_model}")
    
    def _make_request(self, endpoint: str, method: str = 'POST', data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a request to the Ollama API.
        
        Args:
            endpoint: The API endpoint to call
            method: The HTTP method to use
            data: The request data
            
        Returns:
            The JSON response from the API
        """
        url = f"{self.api_url}/{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method.upper() == 'POST':
                response = requests.post(url, json=data, headers=headers)
            elif method.upper() == 'GET':
                response = requests.get(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error making request to Ollama API: {e}")
            raise

    def create_embeddings(self, texts: List[str], model: Optional[str] = None, **kwargs) -> List[List[float]]:
        """
        Create embeddings for a list of texts. Compatible with adalflow's embedder interface.
        
        Args:
            texts: List of strings to embed
            model: Model to use for embeddings, falls back to default_model if not specified
            
        Returns:
            List of embeddings, where each embedding is a list of floats
        """
        model_name = model or self.default_model
        embeddings = []
        
        for text in texts:
            try:
                data = {
                    "model": model_name,
                    "prompt": text
                }
                response = self._make_request('embeddings', 'POST', data)
                embeddings.append(response.get('embedding', []))
            except Exception as e:
                logger.error(f"Error creating embedding: {e}")
                # Return a zero embedding as fallback (with dimensionality of 256)
                embeddings.append([0.0] * 256)
                
        return embeddings

    def generate_content(self, prompt: str, model: Optional[str] = None, stream: bool = False, **kwargs) -> Union[Dict[str, Any], Any]:
        """
        Generate content using the Ollama API. Compatible with Google's GenAI interface.
        
        Args:
            prompt: The prompt to generate content from
            model: The model to use for generation
            stream: Whether to stream the response
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            If stream is False, returns the generated text
            If stream is True, returns a generator that yields text chunks
        """
        model_name = model or self.default_model
        
        # Extract and format generation parameters from kwargs
        temperature = kwargs.get('temperature', 0.7)
        top_p = kwargs.get('top_p', 0.8)
        top_k = kwargs.get('top_k', 40)
        
        request_data = {
            "model": model_name,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k
            }
        }
        
        if stream:
            return self._stream_generate(request_data)
        else:
            return self._complete_generate(request_data)
    
    def _complete_generate(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a complete response (non-streaming).
        
        Args:
            request_data: The request data
            
        Returns:
            Response object with text attribute for compatibility
        """
        try:
            response = self._make_request('generate', 'POST', request_data)
            
            # Create a response object that mimics Google's GenAI interface
            class ResponseWrapper:
                def __init__(self, text):
                    self.text = text
                    self.response = response
                    
            return ResponseWrapper(response.get('response', ''))
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            raise
    
    def _stream_generate(self, request_data: Dict[str, Any]):
        """
        Stream response chunks.
        
        Args:
            request_data: The request data
            
        Returns:
            Generator that yields response chunks
        """
        url = f"{self.api_url}/generate"
        headers = {'Content-Type': 'application/json'}
        
        try:
            with requests.post(url, json=request_data, headers=headers, stream=True) as response:
                response.raise_for_status()
                
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk_data = json.loads(line.decode('utf-8'))
                            
                            # Create a chunk object that mimics Google's GenAI interface
                            class ChunkWrapper:
                                def __init__(self, text):
                                    self.text = text
                            
                            if 'response' in chunk_data:
                                yield ChunkWrapper(chunk_data['response'])
                            
                            # Stop if the model signals it's done
                            if chunk_data.get('done', False):
                                break
                                
                        except json.JSONDecodeError:
                            logger.warning(f"Failed to decode JSON from chunk: {line}")
                            continue
        except Exception as e:
            logger.error(f"Error streaming response: {e}")
            raise