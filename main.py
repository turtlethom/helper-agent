import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Hardcoded String
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Schema for 'get_files_info'
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
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
# Available functions for Gemini AI
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python,
        schema_write_file,
    ]
)
# Load API key and initialize Gemini client
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Parse command-line arguments
arguments = sys.argv[1:]  # Skip the script name
verbose_flag = False

# Check for verbose flag and remove it
if "--verbose" in arguments:
    verbose_flag = True
    arguments.remove("--verbose")

# Require exactly one remaining argument (the prompt)
if len(arguments) != 1:
    print("Usage: script.py <prompt> [--verbose]")
    sys.exit(1)

user_prompt = arguments[0]
messages = [
    types.Content(role="User", parts=[types.Part(text=user_prompt)])
]

# Generate content using Gemini
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    )
)

prompt_token_count = response.usage_metadata.prompt_token_count
candidates_token_count = response.usage_metadata.candidates_token_count

# Output
if response.function_calls:
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
    if verbose_flag:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")
    print(response.text or "[No text response]")
