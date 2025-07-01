import subprocess
from pathlib import Path
from google.genai import types

# Schema for 'run_python'
schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output. Only .py files are allowed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the Python file to execute. Must end in .py and reside in the working directory.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path):
    try:
        # Resolve working directory and target file path
        working_directory = Path(working_directory).resolve()
        target_path = (working_directory / file_path).resolve()
    except Exception as e:
        return f'Error: executing Python file: {e}'

    # Security: block execution outside working directory
    try:
        target_path.relative_to(working_directory)
    except ValueError:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # Check existence
    if not target_path.exists():
        return f'Error: File "{file_path}" not found.'

    # Check file extension
    if not target_path.name.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    # Run the file with subprocess
    try:
        result = subprocess.run(
            ["python3", str(target_path)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(working_directory)
        )

        output_lines = []

        if result.stdout:
            output_lines.append("STDOUT:\n" + result.stdout.strip())

        if result.stderr:
            output_lines.append("STDERR:\n" + result.stderr.strip())

        if result.returncode != 0:
            output_lines.append(f"Process exited with code {result.returncode}")

        if not output_lines:
            return "No output produced."

        return "\n".join(output_lines)

    except Exception as e:
        return f"Error: executing Python file: {e}"
