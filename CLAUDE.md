# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Run Commands
- Frontend: `npm run dev` (Next.js with Turbopack)
- Backend: `python -m api.main` (FastAPI server)
- Build: `npm run build` (Next.js build)
- Lint: `npm run lint` (ESLint with Next.js config)
- Test API: `python -m api.test_api <repo_url> <query> [file_path]`
- Docker: `docker-compose up` (runs both frontend and backend)

## Code Style Guidelines
- TypeScript: Use strict types, React functional components with hooks
- Python: Follow PEP 8 style guide, type annotations encouraged
- Imports: Group imports by type (React, third-party, internal)
- Error handling: Use try/catch blocks with specific error types
- Naming: camelCase for JS/TS variables/functions, PascalCase for components
- File structure: Components in src/components, pages in src/app
- Frontend styling: Tailwind CSS classes for styling
- API structure: FastAPI routes in api.py, data processing in data_pipeline.py
- Environment: Use .env file for API keys (see README for required keys)
- State management: React hooks (useState, useCallback, useMemo) for component state