from pathlib import Path
from google.genai import types

# Schema for 'write_file'
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates or overwrites a text file in the working directory with the provided content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the file to create or overwrite.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write into the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        # Resolve working_directory
        working_directory = Path(working_directory).resolve()

        # Join and resolve the full target path
        target_path = (working_directory / file_path).resolve()
    except Exception as e:
        return f'Error: {e}'

    # Sandbox check: prevent writing outside the working directory
    try:
        target_path.relative_to(working_directory)
    except ValueError:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        # Ensure parent directories exist
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Overwrite file with content
        target_path.write_text(content, encoding='utf-8')

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
