import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import available_functions, call_function
from prompt import system_prompt
from constants import *

# Load environment and create Gemini client
def setup_client():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)

# Parse CLI arguments
def parse_args():
    arguments = sys.argv[1:]
    verbose = "--verbose" in arguments
    if verbose:
        arguments.remove("--verbose")
    if len(arguments) != 1:
        print("Usage: script.py <prompt> [--verbose]")
        sys.exit(1)
    return arguments[0], verbose

def handle_response(response, prompt, verbose):
    prompt_token_count = response.usage_metadata.prompt_token_count
    candidates_token_count = response.usage_metadata.candidates_token_count
    if response.function_calls:
        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose=verbose)
            if not function_call_result.parts or not function_call_result.parts[0].function_response:
                raise RuntimeError("Function call failed or returned malformed content")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_token_count}")
            print(f"Response tokens: {candidates_token_count}")
        print(response.text or "[No text response]")

def get_gemini_response(client, messages):
    return client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

def handle_agent_loop(client, prompt, verbose):
    messages = [types.Content(
        role="User",
        parts=[types.Part(text=prompt)]
        )
    ]
    for iter in range(MAX_ITER):
        response = get_gemini_response(client, messages)
        for candidate in response.candidates:
            messages.append(candidate.content)
        if response.function_calls:
            for function_call_part in response.function_calls:
                function_result = call_function(function_call_part, verbose=verbose)
                messages.append(function_result)
        else:
            print("Final response:")
            print(response.text or "[No text response]")
            break
def main():
    client = setup_client()
    user_prompt, verbose = parse_args()
    handle_agent_loop(client, user_prompt, verbose)
    # handle_response(response, user_prompt, verbose)

if __name__ == "__main__":
    main()
