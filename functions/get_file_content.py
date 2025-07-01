from pathlib import Path
from google.genai import types

# Schema for 'get_file_content'
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a text file located within the working directory. Output is truncated to 10,000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file to read, from the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        # Always resolve the working directory first
        working_directory = Path(working_directory).resolve()

        # Combine file_path with working_directory before resolving
        file_path = (working_directory / file_path).resolve()
    except Exception as e:
        return f'Error: {e}'

    # SECURITY: check if file_path is within working_directory
    try:
        file_path.relative_to(working_directory)
    except ValueError:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Ensure it is a regular file
    if not file_path.is_file():
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # Read contents with truncation check
    try:
        content = file_path.read_text(encoding='utf-8')
        if len(content) > 10000:
            truncated = content[:10000]
            truncated += f'\n[...File "{file_path}" truncated at 10000 characters]'
            return truncated
        return content
    except Exception as e:
        return f'Error: {e}'

