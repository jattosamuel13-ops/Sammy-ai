
  
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

INSTRUCTIONS = """
Your name is Sammy AI.

You are a natural, friendly and helpful WhatsApp assistant.

Reply like a real person.
Be polite and warm.
Keep replies short and clear.
Never invent information.
Never pretend to be Samuel.
"""

class ChatMessage(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head><title>Sammy AI</title></head>
    <body style="font-family:Arial;text-align:center;padding:30px">
        <h1>Welcome to Sammy AI</h1>
        <p>Your personal AI assistant.</p>
        <form id="chat">
            <input id="message" placeholder="Talk to Sammy AI"
            required style="padding:12px;width:70%">
            <button style="padding:12px">Send</button>
        </form>
        <p id="reply"></p>
        <script>
        document.getElementById("chat").onsubmit = async (e) => {
            e.preventDefault();
            const message = document.getElementById("message");
            const reply = document.getElementById("reply");
            reply.innerText = "Sammy AI is thinking...";
            try {
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({message: message.value})
                });
                const data = await response.json();
                reply.innerText = data.reply || data.detail || "Something went wrong.";
            } catch (error) {
                reply.innerText = "Connection error. Try again.";
            }
        };
        </script>
    </body>
    </html>
    """

@app.post("/chat")
def chat(data: ChatMessage):
    response = client.responses.create(
        model=MODEL,
        instructions=INSTRUCTIONS,
        input=data.message
    )
    return {"reply": response.output_text}
    
