import json
import os
import sys

# Add the project root to the python path so we can import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


def generate_openapi():
    """Generates the OpenAPI JSON schema and saves it to docs/openapi/openapi.json"""
    openapi_data = app.openapi()

    # Ensure docs directory exists
    docs_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs"
    )
    # Ensure openapi directory exists
    openapi_dir = os.path.join(docs_dir, "openapi")
    os.makedirs(openapi_dir, exist_ok=True)

    output_path = os.path.join(openapi_dir, "openapi.json")

    with open(output_path, "w") as f:
        json.dump(openapi_data, f, indent=2)

    print(f"OpenAPI schema generated at: {output_path}")


if __name__ == "__main__":
    generate_openapi()
