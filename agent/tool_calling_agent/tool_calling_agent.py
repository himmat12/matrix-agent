import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOLS_SCHEMA, TOOLS_REGISTERY
from schema import TEXT_FORMAT, LLMResponse, INSTRUCTIONS
from enum import Enum
from typing import List, Dict, Any

# from utilities import create_message, get_parsed_conversation_history

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


MESSAGE = "message"
FUNCTION_CALL = "function_call"
REASONING = "reasoning"


def create_message(role: str, content: str) -> Dict[str, str]:
    """
    Generates a dictionary object for a message with `role` and `content` property.

    Args:
        role (str): Message role
        content (str): Message content

    Returns:
       Object (Dict[str, str]): A message dictionary object
    """

    return {"role": role, "content": content}


def get_parsed_conversation_history(conversation_history: List[Dict[str, Any]]):
    lines = []
    for message in conversation_history:
        lines.append(f"{message['role'].upper()}: {message['content']}\n")

    return "\n".join(lines)


def generate_response(user_input: str) -> LLMResponse:
    try:
        response = client.responses.create(
            model="gpt-5.4",
            input=user_input,
            instructions=INSTRUCTIONS,
            text=TEXT_FORMAT,
            tools=TOOLS_SCHEMA,
        )
        # print(response.output[0].type)
        # print()
        # print(response.output)
        # print()
        # print(response)

        items = [item.model_dump() for item in response.output]
        item_types = [item.type for item in response.output]

        messages = [
            item.model_dump()
            for item in response.output
            if item.type == MESSAGE
        ]

        function_calls = [
            item.model_dump()
            for item in response.output
            if item.type == FUNCTION_CALL
        ]

        reasoning = [
            item.model_dump()
            for item in response.output
            if item.type == REASONING
        ]

        llm_response = LLMResponse(
            type=(
                MESSAGE
                if messages
                else (
                    FUNCTION_CALL
                    if function_calls
                    else (
                        REASONING
                        if reasoning
                        else item_types[0] if item_types else "Unknown"
                    )
                )
            ),
            output={
                "output_text": response.output_text,
                "item_types": item_types,
                "messages": messages,
                "function_calls": function_calls,
                "reasoning": reasoning,
                "raw_items": items,
                "response_id": response.id,
            },
        )
        return llm_response

    except Exception as e:

        print(f"Error: {str(e)}")


conversation_history = []


def run_tool_calling_agent(user_input: str, max_steps: int = 8):
    message = create_message("user", user_input)
    conversation_history.append(message)

    conversation_context = get_parsed_conversation_history(conversation_history)

    for each_step in range(max_steps):
        llm_response = generate_response(conversation_context)

        if llm_response:
            if not llm_response.type == FUNCTION_CALL:
                return llm_response.output["output_text"]

            for function_call in llm_response.output["function_calls"]:
                function_name = function_call["name"]
                arguments = json.loads(function_call["arguments"])

                if function_name not in TOOLS_REGISTERY:
                    fnction_output = {"error": f"Unknown function: {function_name}"}
                else:
                    try:
                        funcation_result = TOOLS_REGISTERY[function_name](**arguments)
                        fnction_output = {
                            "ok": True,
                            "function_name": function_name,
                            "arguments": arguments,
                            "result": funcation_result,
                        }
                    except Exception as e:
                        fnction_output = {
                            "ok": False,
                            "function_name": function_name,
                            "arguments": arguments,
                            "error": str(e),
                        }

                function_output_text = json.dumps(fnction_output)

                print(
                    f"function call:\n{function_name} with parameters {arguments}\nfunction result:\n{fnction_output}\n\n"
                )

                conversation_history.append(
                    create_message("tool_call", function_output_text)
                )


def main():
    while True:
        user_input = input("Enter your prompt: ")

        if user_input.lower() == "exit" or user_input.lower() == "e":
            break

        if user_input.lower() == "history" or user_input.lower() == "h":
            print("\nRaw Conversation Data:\n")
            for entry in conversation_history:
                print(entry)
            continue

        print(run_tool_calling_agent(user_input))


if __name__ == "__main__":
    main()
