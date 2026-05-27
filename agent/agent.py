import os
import json
from typing import Any, Dict, List

import httpx
from dotenv import load_dotenv
from openai import OpenAI

from schema import TOOLS_SCHEMA
from world import TOOLS_REGISTRY, initialise_world, printWorld, matrix

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=20,
    base_url="https://api.openai.com/v1",
    default_headers={"Content-Type": "application/json"},
    http_client=httpx.Client(timeout=20),
    organization=os.getenv("ORGANIZATION_ID"),
    project=os.getenv("PROJECT_ID"),
)


AGENT_INSTRUCTIONS = """
You are a helpful assistant that exists in a 2D grid world.
You can answer normal questions directly, and you can use tools to inspect or move in the world when needed.

Behavior rules:
- Use tools when the user asks about your current location or asks you to move.
- Do not invent tools.
- If a tool result is enough to answer, answer clearly and briefly.
- Keep track of the ongoing task across tool calls.
""".strip()


FINAL_SCHEMA = {
    "type": "object",
    "properties": {
        "plan": {
            "type": "string",
            "description": "Brief explanation of how the final answer was produced.",
        },
        "message": {"type": "string", "description": "Final user-facing response."},
    },
    "required": ["plan", "message"],
    "additionalProperties": False,
}


FINAL_TEXT_FORMAT = {
    "format": {
        "type": "json_schema",
        "name": "final_answer",
        "strict": True,
        "schema": FINAL_SCHEMA,
    }
}


conversation_history: List[Dict[str, str]] = []


def create_message(role: str, content: str) -> Dict[str, str]:
    return {"role": role, "content": content}


def print_history() -> None:
    print("\nConversation History:\n")
    for entry in conversation_history:
        print(f"{entry['role'].capitalize()}: {entry['content']}\n")

    print("\nRaw Conversation Data:\n")
    for entry in conversation_history:
        print(entry)


def call_model_with_tools(
    input_items: List[Dict[str, Any]], previous_response_id: str | None = None
):
    return client.responses.create(
        model="gpt-5.4",
        input=input_items,
        instructions=AGENT_INSTRUCTIONS,
        tools=TOOLS_SCHEMA,
        previous_response_id=previous_response_id,
    )


def call_model_for_final_answer(
    input_items: List[Dict[str, Any]], previous_response_id: str | None = None
) -> Dict[str, Any]:
    response = client.responses.create(
        model="gpt-5.4",
        input=input_items,
        instructions=(
            "Produce the final answer for the user as structured JSON. "
            "Do not call any tools."
        ),
        text=FINAL_TEXT_FORMAT,
        previous_response_id=previous_response_id,
    )

    message_items = [item for item in response.output if item.type == "message"]
    if not message_items:
        raise ValueError("No final message returned by model.")

    text = message_items[0].content[0].text
    return json.loads(text)


def run_agent(user_input: str, max_steps: int = 8) -> str:
    conversation_history.append(create_message("user", user_input))

    previous_response_id = None

    for _ in range(max_steps):
        response = call_model_with_tools(
            conversation_history, previous_response_id=previous_response_id
        )
        previous_response_id = response.id

        function_calls = [
            item for item in response.output if item.type == "function_call"
        ]
        message_items = [item for item in response.output if item.type == "message"]

        if function_calls:
            input_items = []
            for call in function_calls:
                tool_name = call.name
                arguments = json.loads(call.arguments or "{}")

                if tool_name not in TOOLS_REGISTRY:
                    tool_output = {"error": f"Unknown tool: {tool_name}"}
                else:
                    try:
                        result = TOOLS_REGISTRY[tool_name](**arguments)
                        tool_output = {
                            "ok": True,
                            "tool_name": tool_name,
                            "arguments": arguments,
                            "result": result,
                        }
                    except Exception as e:
                        tool_output = {
                            "ok": False,
                            "tool_name": tool_name,
                            "arguments": arguments,
                            "error": str(e),
                        }

                tool_output_text = json.dumps(tool_output)
                print(f"[tool_call]: {tool_name}({arguments}) -> {tool_output_text}")
                conversation_history.append(
                    create_message("tool_call", tool_output_text)
                )

                input_items.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": tool_output_text,
                    }
                )
            continue

        if message_items:
            assistant_text_parts = []
            for item in message_items:
                for content in item.content:
                    if hasattr(content, "text") and content.text:
                        assistant_text_parts.append(content.text)
            assistant_text = "\n".join(assistant_text_parts).strip()

            final_json = call_model_for_final_answer(
                (
                    conversation_history.append(create_message("assistant", assistant_text))
                    if assistant_text
                    else conversation_history.append(create_message("user", user_input))
                ),
                previous_response_id=previous_response_id,
            )
            plan = final_json.get("plan", "")
            message = final_json.get("message", assistant_text)

            if plan:
                conversation_history.append(create_message("plan", plan))
            conversation_history.append(create_message("assistant", message))
            return message

        input_items = [{"role": "user", "content": user_input}]

    final_message = "Max agent steps reached without a final answer."
    conversation_history.append(create_message("assistant", final_message))
    return final_message


def main() -> None:
    initialise_world()

    while True:
        user_input = input("\nEnter a prompt (or 'exit' to quit): ").strip()

        if user_input.lower() == "exit":
            break

        if not user_input:
            print("Please enter a valid prompt.")
            continue

        if user_input.lower() == "history":
            print_history()
            continue

        print("\n[user]:", user_input)
        try:
            llm_message = run_agent(user_input)
            print("\n[assistant]:", llm_message)
            printWorld(matrix)
        except Exception as e:
            print(f"\n[error]: {e}")


if __name__ == "__main__":
    main()
