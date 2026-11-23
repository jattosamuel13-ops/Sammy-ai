
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

def sammy_ai(message):
    response = client.responses.create(
        model=os.environ["OPENAI_MODEL"],
        instructions="""
        Your name is Sammy AI.

        You are a natural, friendly
        and helpful WhatsApp assistant.

        Reply like a real person.
        Be polite and warm.
        Keep replies short and clear.
        Never invent information.
        Never pretend to be Samuel.
        """,
        input=message
    )

    return response.output_text


while True:
    message = input("You: ")

    if message.lower() == "exit":
        break

    reply = sammy_ai(message)

    print("Sammy AI:", reply)
  
