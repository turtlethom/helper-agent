import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
    contents=messages
)

prompt_token_count = response.usage_metadata.prompt_token_count
candidates_token_count = response.usage_metadata.candidates_token_count

# Output
if verbose_flag:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_token_count}")
    print(f"Response tokens: {candidates_token_count}")
    print(response.text)
else:
    print(response.text)
