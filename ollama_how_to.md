# Using DeepWiki with Ollama

This guide explains how to set up and use DeepWiki with a local Ollama server instead of cloud-based AI services like Google Gemini and OpenAI.

## Prerequisites

1. [Install Ollama](https://ollama.ai/download) on your system
2. Pull a model that you want to use (e.g., Llama 3)
3. Ensure Ollama is running on your machine

## Setup Instructions

### 1. Install Ollama

Follow the installation instructions on the [Ollama website](https://ollama.ai/download) for your operating system.

### 2. Pull a Model

Open a terminal and pull a model you want to use:

```bash
ollama pull llama3        # 8B parameter model (recommended)
# or
ollama pull gemma:7b      # Google's Gemma model
# or
ollama pull mistral       # Mistral model
```

You can see all available models at [Ollama Library](https://ollama.ai/library).

### 3. Start Ollama Server

Ensure the Ollama server is running:

```bash
# On most systems, it starts automatically after installation
# To check if it's running:
curl http://localhost:11434/api/version
```

### 4. Configure DeepWiki to Use Ollama

#### Option A: Using .env File

Create a `.env` file in the root directory of DeepWiki with:

```
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3
```

Replace `llama3` with whichever model you pulled.

#### Option B: Setting Environment Variables Directly

```bash
# Linux/macOS
export OLLAMA_URL=http://localhost:11434
export OLLAMA_MODEL=llama3

# Windows (Command Prompt)
set OLLAMA_URL=http://localhost:11434
set OLLAMA_MODEL=llama3

# Windows (PowerShell)
$env:OLLAMA_URL = "http://localhost:11434"
$env:OLLAMA_MODEL = "llama3"
```

### 5. Start DeepWiki

#### Using Docker Compose

```bash
# Make sure your .env file contains OLLAMA_URL and OLLAMA_MODEL
docker-compose up
```

**Note for Docker users**: When running Ollama on your host machine and DeepWiki in Docker, use `http://host.docker.internal:11434` as the OLLAMA_URL to allow the container to access the host's Ollama server.

#### Manual Setup

```bash
# Start the backend
python -m api.main

# In another terminal, start the frontend
npm run dev
```

## Usage

Once both the frontend and backend are running:

1. Open your browser to http://localhost:3000
2. Enter a GitHub repository URL (e.g., `https://github.com/vercel/next.js`)
3. Click "Generate Wiki"

DeepWiki will now use your local Ollama model for all AI operations, including:
- Embeddings for RAG (Retrieval Augmented Generation)
- Text generation for documentation and diagram creation

## Troubleshooting

### Connection Issues

If DeepWiki can't connect to Ollama, check:

1. **Ollama is Running**: Verify with `curl http://localhost:11434/api/version`
2. **Correct URL**: Ensure OLLAMA_URL is set correctly
3. **Docker Network Issues**: If using Docker, ensure you're using `host.docker.internal` instead of `localhost`

### Model Not Found

If you see errors about the model not being available:

1. Check the model name is correct in your configuration
2. Pull the model with `ollama pull <model_name>` 
3. List available models with `ollama list`

### Performance Issues

Local models may be slower than cloud APIs, especially on computers without a powerful GPU:

1. Try a smaller model like `llama3:8b` or `phi3:mini`
2. Ensure your computer has adequate RAM (8GB minimum, 16GB+ recommended)
3. If you have a GPU, ensure Ollama is configured to use it

## Recommended Models

For good performance on most consumer hardware:

| Model | Size | Quality | Speed | GPU Memory Required |
|-------|------|---------|-------|---------------------|
| llama3 | 8B | Good | Good | 8GB+ |
| gemma:7b | 7B | Good | Good | 8GB+ |
| phi3:mini | 3.8B | Moderate | Fast | 6GB+ |
| mistral | 7B | Good | Good | 8GB+ |
| neural-chat | 7B | Good | Good | 8GB+ |

For better performance on high-end hardware:

| Model | Size | Quality | Speed | GPU Memory Required |
|-------|------|---------|-------|---------------------|
| llama3:70b | 70B | Excellent | Slow | 40GB+ |
| gemma:27b | 27B | Very Good | Slow | 24GB+ |
| mixtral | 47B | Excellent | Slow | 32GB+ |

## Benefits of Using Ollama

- **Privacy**: All processing happens locally without data sent to cloud services
- **No API Keys**: No need for Google or OpenAI API keys
- **No Costs**: Free to use without API usage fees
- **No Rate Limits**: Not subject to API rate limiting
- **Offline Usage**: Works without an internet connection after initial repository cloning