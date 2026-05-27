import os
from urllib import response
from dotenv import load_dotenv
import httpx
from typing import Any, Dict, List, Optional
from openai import OpenAI
import json
from schema import AGENT_INSTRUCTIONS, TEXT_FORMAT, AGENT_SCHEMA, TOOLS_SCHEMA
from pydantic import BaseModel
from world import (
    TOOLS_REGISTRY,
    setEmptyWorld,
    setBorderWorld,
    plantAgentInRandomLocation,
    printWorld,
    initialise_world,
    matrix,
)

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
        print (prompt)
        
        response = client.responses.create(
            input=prompt,
            model="gpt-5.4",
            instructions=AGENT_INSTRUCTIONS,
            text=TEXT_FORMAT,
            tools=TOOLS_SCHEMA,
        )

        # print(response)
        json_string = response.output[0].content[0]
        print(json_string)
        final_json = json.loads(json_string)
        print(final_json)
        return final_json
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}


conversation_history: List[Dict[str, str]] = []


def create_message(role: str, content: str) -> Dict[str, str]:
    return {"role": role, "content": content}


def get_parsed_conversation_history():
    lines = []

    for message in conversation_history:
        lines.append(f"{message['role'].upper()}: {message['content']}\n")

    return "\n".join(lines)


def run_agent(user_input: str, max_setps: int = 5):

    conversation_history.append(create_message("user", user_input))

    for i in range(max_setps):
        conversation_Context = get_parsed_conversation_history()
        llm_response = generate_text(conversation_Context)

        print(f"\n\nLLM RESPONSE: {llm_response}\n\n")

        if not isinstance(llm_response, dict):
            return "Model returned invalid response."

        plan = llm_response.get("plan", "")
        action = llm_response.get("action", "")
        tool_name = llm_response.get("tool_name", None)
        arguments = llm_response.get("arguments", None)
        message = llm_response.get("message", "")

        conversation_history.append(create_message("plan", plan))

        print(plan)
        print(action)
        print(tool_name)
        print(arguments)
        print(message)
        
        if action == "final":
            conversation_history.append(create_message("assistant", message))
            return message
        elif action == "tool_call":
            try:
                tool_call_result = TOOLS_REGISTRY[tool_name](**arguments)
                tool_call_response = f"Tool `{tool_name}` with arguments `{arguments}` returned: `{tool_call_result}`"
            except Exception as e:
                tool_call_response = (
                    f"Tool `{tool_name}` failed with an error:\n{str(e)}"
                )

            print(f"[tool_call]:", tool_call_response)
            conversation_history.append(create_message("tool_call", tool_call_response))
            continue
        else:
            unexpected_action_message = f"Unexpected action {action}"
            print(f"[action]: {unexpected_action_message}")
            conversation_history.append(create_message("[action]", unexpected_action_message))
            continue

    message = "Max agent steps reached without a final answer."
    conversation_history.append(create_message("action", message))
    return message


def main():

    initialise_world()

    while True:

        user_input = input("\nEnter a prompt (or 'exit' to quit): ")

        if user_input.lower() == "exit":
            break

        if user_input.strip() == "":
            print("Please enter a valid prompt.")
            continue

        if user_input.lower() == "history":
            print("\nConversation History:\n\n")
            for entry in conversation_history:
                print(f"{entry['role'].capitalize()}: {entry['content']}\n")

            print("\nRaw Conversation Data:\n")
            for entry in conversation_history:
                print(entry)
            continue

        print("\n[user]:", user_input)

        llm_message = run_agent(user_input)

        print("\n[assistant]:", llm_message)

        # printWorld(matrix)


if __name__ == "__main__":
    main()
