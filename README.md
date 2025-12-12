# LLM Chat Response

A lightweight, FastAPI-based microservice that generates intelligent chat responses using Google's Gemini 2.5 Flash Lite model. Designed for easy integration with Discord bots and other applications requiring conversational AI capabilities.

## Features

- **Gemini Integration**: Leverages Google's `gemini-2.5-flash-lite` (configurable) for fast and coherent text generation.
- **Context-Aware**: processing handles user-provided context and system-level instructions to tailor responses.
- **RESTful API**: Simple `POST` endpoint for chat generation and `GET` endpoint for health checks.

## Setup

### Prerequisites
- **Python**: Managed via `pyenv`
- **Dependency Management**: Uses `poetry`.

### Installation

1.  **Set up Python version:**
    If you have `pyenv` installed:
    ```bash
    pyenv install 3.13
    pyenv local 3.13
    ```

2.  **Install dependencies:**
    ```bash
    poetry install
    ```

3.  **Configure Environment:**
    Create a `.env` file from the example and add your Google Gemini API key.
    ```bash
    cp .env.example .env
    ```
    Edit `.env` and set `LLM_API_KEY` to your valid API key.

4.  **Configure System Context (Optional):**
    The service generates responses using a system context (persona/instructions). You can define a default context by creating a `system_context.md` file.
    ```bash
    cp system_context.md.example system_context.md
    ```
    Edit `system_context.md` to customize the default behavior of the chat bot.

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
  Builds the `py-chat-response` Docker image.

- **Run Docker Container**:
  ```bash
  poetry run task run
  ```
  Runs the container, listening on port 8001.

## API Usage

### Check Service Health

**Endpoint**: `GET /health`

Checks if the service is running and if CUDA is available.

**Example Request:**
```bash
http :8001/health
```

**Response**:
```json
{
    "status": "ok"
}
```

### Generate Chat Response

**Endpoint**: `POST /api/v1/chat`

Generates a response based on the provided text and context.

**Parameters**:
- `text` (string): The user's input message.
- `context` (string, optional): Context about the current conversation state or user intent.
- `system_context` (string, optional): High-level system instructions. Overrides the default context loaded from `system_context.md`.

**Example Request:**

```bash
http :8001/api/v1/chat \
    text="What is the capital of France?" \
    context="User is asking geography questions." \
    system_context="You are a helpful geography teacher."
```

**Example JSON Response:**

```json
{
    "output": [
        {
            "type": "message",
            "role": "assistant",
            "content": {
                "text": "The capital of France is Paris."
            }
        }
    ]
}
```
