import os
from urllib import response
from dotenv import load_dotenv
import httpx
from typing import Any, Dict, List, Optional
from openai import OpenAI
import json
from schema import AGENT_INSTRUCTIONS, TEXT_FORMAT, AGENT_SCHEMA
from pydantic import BaseModel

load_dotenv()


class Steps(BaseModel):
    thought: str
    action: str
    tool_name: Optional[str] = None
    arguments: Optional[Dict[str, Any]] = None
    message: str


class AgentResponse(BaseModel):
    thought: str
    action: str
    tool_name: Optional[str] = None
    arguments: Optional[Dict[str, Any]] = None
    message: str


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


def generate_text(prompt: str, max_tokens: int = 500) -> Dict[str, Any]:
    """
    Generate text based on a given prompt using an external API.

    Args:
        prompt (str): The input prompt for text generation.
        max_tokens (int): The maximum number of tokens to generate.

    Returns:
        Dict[str, Any]: The generated text as a JSON object.
    """
    try:

        response = client.responses.create(
            input=prompt,
            model="gpt-5.4",
            instructions=AGENT_INSTRUCTIONS,
            text=TEXT_FORMAT,
            tools=TOOLS,
        )

        json_string = response.output[0].content[0].model_dump_json(indent=2)
        return json.loads(json_string)

    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


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

    llm_response = json.loads(generate_text(user_input)["text"])
    print("[assistant]:", llm_response["final_answer"])

    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": llm_response})
