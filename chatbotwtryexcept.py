import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: No API key found. Check that your .env file exists and contains GEMINI_API_KEY.")
    exit()

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        #model="gemini-2.5-flash",
        model="gemini-2.5-flash-lite",
        contents="In one sentence, explain what an API is to a beginner."
    )
    print(response.text)

except errors.ServerError as e:
    print("Gemini's servers are busy right now (this happens under high demand). Try again in a moment.")
    print(f"(Technical detail: {e})")

except errors.APIError as e:
    print("Something went wrong with the API request. Check your key and model name.")
    print(f"(Technical detail: {e})")

except Exception as e:
    print("An unexpected error occurred.")
    print(f"(Technical detail: {e})")