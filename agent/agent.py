import os
from urllib import response
from dotenv import load_dotenv
import httpx
from typing import Any, Dict, List, Optional
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=10,
    base_url="https://api.openai.com/v1",
    default_headers={"Content-Type": "application/json"},
    default_query={"model": "gpt-5.4", "temperature": 0.7},
    http_client=httpx.Client(timeout=10),
    organization=os.getenv("ORGANIZATION_ID"),
    project=os.getenv("PROJECT_ID"),
)

TOOLS = []

def generate_text(prompt: str, max_tokens: int = 500) -> Any:
    """
    Generate text based on a given prompt using an external API.

    Args:
        prompt (str): The input prompt for text generation.
        max_tokens (int): The maximum number of tokens to generate.

    Returns:
        str: The generated text.
    """
    try:

        response = client.responses.create(
            input=prompt,
            model="gpt-5.4",
            instructions="You are a helpful assistant that generates text based on the given prompt.",
            tools=TOOLS,
        )

        data = response.model_dump_json(indent=2)
        return json.loads(data)["output"][0]["content"][0]["text"]
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""


conversation_history: List[Dict[str, str]] = []

while True:

    user_input = input("\nEnter a prompt (or 'exit' to quit): ")
    print("\n[user]:", user_input)
    if user_input.lower() == "exit":
        break

    if user_input.strip() == "":
        print("Please enter a valid prompt.")
        continue

    if user_input.lower() == "history":
        print("\nConversation History:\n")
        for entry in conversation_history:
            print(f"{entry['role'].capitalize()}: {entry['content']}\n")

        print("\nRaw Conversation Data:\n")
        for entry in conversation_history:
            print(entry)
        continue

    llm_response = generate_text(user_input)
    print("[assistant]:", llm_response)

    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": llm_response})
