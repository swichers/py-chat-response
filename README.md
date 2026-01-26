# LLM Chat Response

A lightweight, FastAPI-based microservice that generates intelligent chat responses using Google's Gemini 2.5 Flash Lite model. Designed for easy integration with Discord bots and other applications requiring conversational AI capabilities.

## Features

- **Gemini Integration**: Leverages Google's `gemini-2.5-flash-lite` (configurable) for fast and coherent text generation.
- **Context-Aware**: Processing handles user-provided context and system-level instructions to tailor responses.
- **Dynamic Context Management**: Create, list, and delete system contexts via REST API without requiring file system access.
- **RESTful API**: Simple endpoints for chat generation, context management, and health checks.

## Setup

### Prerequisites
- **Python**: Managed via `pyenv`
- **Dependency Management**: Uses `poetry`

### Installation

1.  **Set up Python version:**
    ```bash
    pyenv install 3.13
    pyenv local 3.13
    ```

2.  **Install dependencies:**
    ```bash
    poetry install
    ```

3.  **Configure Environment:**
    ```bash
    cp .env.example .env
    ```
    Edit `.env` and set:
    - `LLM_API_KEY`: Your Google Gemini API key
    - `LLM_MODEL`: (Optional) Model name, defaults to `gemini-2.5-flash-lite`

### Helper Tasks

This project uses `taskipy` to simplify common commands. Run these with `poetry run task <command>`.

- **Start Development Server**:
  ```bash
  poetry run task dev
  ```
  Runs the uvicorn server with hot-reload enabled on port 8001.

- **Build Docker Image**:
  ```bash
  poetry run task build
  ```

- **Run Docker Container**:
  ```bash
  poetry run task run
  ```
  Automatically passes your `.env` file variables to the container.

### Docker Compose

For easier deployment and development:

```bash
docker compose up -d
```

The `contexts/` folder is mounted as a volume, allowing dynamic context management without rebuilding.

## API Endpoints

The service provides the following REST API endpoints:

### Core Endpoints

- **`GET /health`** - Health check endpoint
- **`POST /api/v1/chat`** - Generate AI chat responses

### Context Management

- **`GET /api/v1/contexts`** - List all available contexts
- **`POST /api/v1/contexts`** - Create a new context
- **`DELETE /api/v1/contexts/{machine_name}`** - Delete a context

### Quick Start Examples

**Generate a chat response:**
```bash
http :8001/api/v1/chat text="What is the capital of France?"
```

**Create a custom context:**
```bash
http :8001/api/v1/contexts \
    name="Geography Teacher" \
    content="You are an enthusiastic geography teacher."
```

**Use a custom context:**
```bash
http :8001/api/v1/chat \
    text="Tell me about Paris" \
    system_context="geography_teacher"
```

## Documentation

The API documentation is available in OpenAPI format. To generate the latest `openapi.json` specification:

```bash
poetry run task generate-docs
```

The generated file will be located at `docs/openapi/openapi.json`.

Documentation is automatically deployed to GitHub Pages on every push to `main` (or manually triggered).
HTML documentation: `https://swichers.github.io/py-chat-response/`
- Inline docstrings in the source code

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_API_KEY` | Google Gemini API key (required) | - |
| `LLM_MODEL` | Gemini model to use | `gemini-2.5-flash-lite` |
