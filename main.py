import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import available_functions, call_function

# Hardcoded system prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Load environment and create Gemini client
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Parse CLI arguments
arguments = sys.argv[1:]
verbose_flag = False

if "--verbose" in arguments:
    verbose_flag = True
    arguments.remove("--verbose")

if len(arguments) != 1:
    print("Usage: script.py <prompt> [--verbose]")
    sys.exit(1)

user_prompt = arguments[0]
messages = [
    types.Content(role="User", parts=[types.Part(text=user_prompt)])
]

# Ask Gemini
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
    ),
)

# Usage metadata
prompt_token_count = response.usage_metadata.prompt_token_count
candidates_token_count = response.usage_metadata.candidates_token_count

# Response handling
if response.function_calls:
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose=verbose_flag)

        if not function_call_result.parts or not function_call_result.parts[0].function_response:
            raise RuntimeError("Function call failed or returned malformed content")

        if verbose_flag:
            print(f"-> {function_call_result.parts[0].function_response.response}")
else:
    if verbose_flag:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_token_count}")
        print(f"Response tokens: {candidates_token_count}")
    print(response.text or "[No text response]")
