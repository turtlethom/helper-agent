import os
import sys
from dotenv import load_dotenv
from google import genai

# Setting up Gemini Client
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
arguments = sys.argv

# Exit program if argument not provided
if len(arguments) != 2:
    sys.exit(1)
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=arguments[1]
)

prompt_token_count, candidates_token_count = response.usage_metadata.prompt_token_count, response.usage_metadata.candidates_token_count

# Output
print(response.text)
print(f"Prompt tokens: {prompt_token_count}")
print(f"Response tokens: {candidates_token_count}")
