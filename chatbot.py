import os
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: No API key found. Check that your .env file exists and contains GEMINI_API_KEY.")
    exit()

client = genai.Client(api_key=api_key)

chat = client.chats.create(
    model="gemini-2.5-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction="You are a patient SQL tutor for a data analyst learning to code. Explain concepts using gaming analogies where they fit. Keep answers short and encouraging."
    )
)

print("SQL Tutor Bot ready! Type your question, or type 'quit' to exit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Bot: Good session! See you next time.")
        break

    try:
        response = chat.send_message(user_input)
        print(f"Bot: {response.text}\n")

    except errors.ServerError as e:
        print("Bot: Servers are busy right now. Try again in a moment.\n")
        print(f"(Technical detail: {e})\n")

    except errors.APIError as e:
        print("Bot: Something went wrong with the request.\n")
        print(f"(Technical detail: {e})\n")

    except Exception as e:
        print("Bot: An unexpected error occurred.\n")
        print(f"(Technical detail: {e})\n")