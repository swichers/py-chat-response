# LLM Chat Response

A lightweight, FastAPI-based microservice that generates intelligent chat responses using Google's Gemini 2.5 Flash Lite model. Designed for easy integration with Discord bots and other applications requiring conversational AI capabilities.

## Features

- **Gemini Integration**: Leverages Google's `gemini-2.5-flash-lite` (configurable) for fast and coherent text generation.
- **Context-Aware**: processing handles user-provided context and system-level instructions to tailor responses.
- **Dynamic Context Management**: Create, list, and delete system contexts via REST API without requiring file system access.
- **RESTful API**: Simple endpoints for chat generation, context management, and health checks.

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
  Runs the container, listening on port 8001. This command automatically passes your `.env` file variables to the container. Ensure your `.env` file is properly configured before running.

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
- `context_name` (string, optional): Machine name of a saved context to use (e.g., "geography_teacher"). If specified, the context must exist or the request will return a 404 error. If not specified, the "default" context is used if available.

**Context Resolution Behavior**:
- If `context_name` is provided: The specified context **must exist** in the `contexts/` directory, otherwise a 404 error is returned.
- If `context_name` is **not** provided: The system attempts to use the `default` context. If no default context exists, the request proceeds without a system context (no error).

**Example Request (with named context):**

```bash
http :8001/api/v1/chat \
    text="What is the capital of France?" \
    context="User is asking geography questions." \
    context_name="geography_teacher"
```

**Example Request (using default context):**

```bash
http :8001/api/v1/chat \
    text="What is the capital of France?"
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

**Error Response (404 - Context Not Found):**
```json
{
    "detail": "Context 'geography_teacher' not found"
}
```

## Context Management API

The service provides endpoints to dynamically manage system contexts without requiring file system access. Contexts are stored as markdown files in the `contexts/` directory.

### List Available Contexts

**Endpoint**: `GET /api/v1/contexts`

Returns a list of all available context files.

**Example Request:**
```bash
http :8001/api/v1/contexts
```

**Example Response:**
```json
{
    "contexts": [
        {
            "machine_name": "system",
            "file_path": "contexts/system.md"
        },
        {
            "machine_name": "geography_teacher",
            "file_path": "contexts/geography_teacher.md"
        }
    ]
}
```

### Create a New Context

**Endpoint**: `POST /api/v1/contexts`

Creates a new context file. The context name is automatically normalized to lowercase with underscores replacing non-alphanumeric characters.

**Parameters**:
- `name` (string): Display name for the context (will be normalized).
- `content` (string): The context content/instructions.

**Example Request:**
```bash
http :8001/api/v1/contexts \
    name="Geography Teacher" \
    content="You are an enthusiastic geography teacher who loves to share interesting facts about places around the world."
```

**Example Response:**
```json
{
    "machine_name": "geography_teacher",
    "message": "Context 'geography_teacher' created successfully"
}
```

The context will be saved to `contexts/geography_teacher.md`.

**Name Normalization Examples**:
- `"System"` → `system`
- `"Geography Teacher"` → `geography_teacher`
- `"My Bot v2.0!"` → `my_bot_v2_0`

### Delete a Context

**Endpoint**: `DELETE /api/v1/contexts/{machine_name}`

Deletes a context file by its machine name.

**Example Request:**
```bash
http DELETE :8001/api/v1/contexts/geography_teacher
```

**Example Response:**
```json
{
    "message": "Context 'geography_teacher' deleted successfully"
}
```

**Error Response (404 - Not Found):**
```json
{
    "detail": "Context 'geography_teacher' not found"
}
```
