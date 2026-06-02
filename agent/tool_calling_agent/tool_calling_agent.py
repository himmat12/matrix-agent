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
            item.model_dump() for item in response.output if item.type == MESSAGE
        ]

        function_calls = [
            item.model_dump() for item in response.output if item.type == FUNCTION_CALL
        ]

        reasoning = [
            item.model_dump() for item in response.output if item.type == REASONING
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


agent_state = {
    "latest_plan": None,
    "plans": [],
    "debug_traces": [],
    "conversation": [],
}

conversation_history = agent_state.get("conversation")


def call_model_with_tools(user_input_list: List[Dict[str, Any]]):
    return client.responses.create(
        model="gpt-5.4",
        input=user_input_list,
        instructions=INSTRUCTIONS,
        tools=TOOLS_SCHEMA,
    )


def call_model_final_answer(user_input_list: List[Dict[str, Any]]):
    response = client.responses.create(
        model="gpt-5.4",
        input=user_input_list,
        instructions=(
            "Produce the final answer for the user as structured JSON. "
            "Do not call any tools."
        ),
        text=TEXT_FORMAT,
    )

    message_items = [item for item in response.output if item.type == "message"]

    if not message_items:
        raise ValueError("No final message returned by model.")

    text = message_items[0].content[0].text
    return json.loads(text)


def run_agent(user_input: str, max_steps: int = 12):
    message = create_message("user", user_input)
    conversation_history.append(message)

    for each_step in range(max_steps):
        llm_response = call_model_with_tools(conversation_history)

        if not llm_response:
            return None

        function_calls = [
            item for item in llm_response.output if item.type == "function_call"
        ]

        message_items = [item for item in llm_response.output if item.type == "message"]

        if len(function_calls) > 0:
            for each_function_call in function_calls:
                tool_call_id = each_function_call.call_id
                tool_name = each_function_call.name
                arguments = json.loads(each_function_call.arguments)

                conversation_history.append(each_function_call.model_dump())

                if tool_name not in TOOLS_REGISTERY:
                    tool_output = {"error": f"Unknown tool: {tool_name}"}
                else:
                    try:
                        tool_call_result = TOOLS_REGISTERY[tool_name](**arguments)
                        tool_output = {
                            "ok": True,
                            "tool_name": tool_name,
                            "arguments": arguments,
                            "result": tool_call_result,
                        }
                    except Exception as e:
                        tool_output = {
                            "ok": False,
                            "tool_name": tool_name,
                            "arguments": arguments,
                            "error": str(e),
                        }

                    conversation_history.append(
                        {
                            "type": "function_call_output",
                            "call_id": tool_call_id,
                            "output": json.dumps(tool_output),
                        }
                    )
                    continue

        if message_items:
            assistant_text_parts = []
            for each_message_item in message_items:
                for each_content in each_message_item.content:
                    if hasattr(each_content, "text") and each_content.text:
                        assistant_text_parts.append(each_content.text)
            assistant_text = "\n".join(assistant_text_parts)

            final_json = call_model_final_answer(conversation_history)

            plan = final_json.get("plan", "")
            observation = final_json.get("observation", "")
            message = final_json.get("message", assistant_text)

            if plan:
                conversation_history.append(
                    create_message("assistant", f"[PLAN]:\n{plan}")
                )

            if assistant_text:
                conversation_history.append(create_message("assistant", assistant_text))

            if observation:
                conversation_history.append(
                    create_message("assistant", f"[OBSERVATION]:\n{observation}")
                )
            return message

        # with open("response.txt", "a", encoding="utf-8") as f:
        #     f.write(
        #         f"LLM RESPONSE - STEP {each_step}:\n{llm_response.model_dump_json(indent=2)}\n\n"
        #     )
        #     f.write(f"UPDATED CONVERSATION HISTORY:\n{conversation_history}\n\n")

        # if each_step == (max_steps - 1):
    return "Max agent steps reached without a final answer."


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

        # print(run_tool_calling_agent(user_input))

        try:
            print(f"\n[user]: {user_input}")
            assistant_message = run_agent(user_input)
            print(f"\n[assistant]: {assistant_message}")
            print()
            print()
            print(agent_state["conversation"])
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
