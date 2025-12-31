import re
from pathlib import Path
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ContextManager:
    """Manages system context files in the contexts directory."""

    def __init__(self, contexts_dir: str = "contexts"):
        self.contexts_dir = Path(contexts_dir)
        self.contexts_dir.mkdir(exist_ok=True)
        logger.info(f"Context manager initialized with directory: {self.contexts_dir}")

    @staticmethod
    def normalize_name(name: str) -> str:
        """
        Normalize a context name to a machine-friendly format.
        Converts to lowercase and replaces non-alphanumeric characters with underscores.

        Args:
            name: The original context name

        Returns:
            Normalized machine name (lowercase with underscores)
        """
        normalized = re.sub(r"[^a-z0-9]+", "_", name.lower())
        normalized = normalized.strip("_")
        return normalized

    def create_context(self, name: str, content: str) -> Dict[str, str]:
        """
        Create a new context file.

        Args:
            name: The display name for the context
            content: The context content to store

        Returns:
            Dictionary with machine_name and message

        Raises:
            ValueError: If name or content is empty
        """
        if not name or not name.strip():
            raise ValueError("Context name cannot be empty")

        if not content or not content.strip():
            raise ValueError("Context content cannot be empty")

        machine_name = self.normalize_name(name)

        if not machine_name:
            raise ValueError(
                "Context name must contain at least one alphanumeric character"
            )

        file_path = self.contexts_dir / f"{machine_name}.md"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"Created context '{machine_name}' at {file_path}")

        return {
            "machine_name": machine_name,
            "message": f"Context '{machine_name}' created successfully",
        }

    def list_contexts(self) -> List[Dict[str, str]]:
        """
        List all available context files.

        Returns:
            List of dictionaries containing machine_name and file_path for each context
        """
        contexts = []

        for file_path in self.contexts_dir.glob("*.md"):
            machine_name = file_path.stem
            contexts.append({"machine_name": machine_name, "file_path": str(file_path)})

        logger.info(f"Found {len(contexts)} contexts")
        return contexts

    def delete_context(self, machine_name: str) -> Dict[str, str]:
        """
        Delete a context file by its machine name.

        Args:
            machine_name: The machine name of the context to delete

        Returns:
            Dictionary with success message

        Raises:
            FileNotFoundError: If the context file doesn't exist
        """
        file_path = self.contexts_dir / f"{machine_name}.md"

        if not file_path.exists():
            raise FileNotFoundError(f"Context '{machine_name}' not found")

        file_path.unlink()
        logger.info(f"Deleted context '{machine_name}' from {file_path}")

        return {"message": f"Context '{machine_name}' deleted successfully"}

    def get_context_content(self, machine_name: str) -> Optional[str]:
        """
        Read the content of a context file.

        Args:
            machine_name: The machine name of the context to read

        Returns:
            The content of the context file, or None if not found
        """
        file_path = self.contexts_dir / f"{machine_name}.md"

        if not file_path.exists():
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
