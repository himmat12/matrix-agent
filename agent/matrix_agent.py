import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOLS_SCHEMA, TOOLS_REGISTERY
from schema import TEXT_FORMAT, INSTRUCTIONS

CONVERSATION = []


def run_tool(name: str, arguments: dict):
    if name not in TOOLS_REGISTERY:
        return {"ok": False, "error": f"Unknown tool: {name}"}
    try:
        result = TOOLS_REGISTERY[name](**arguments)
        return {"ok": True, "result": result}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def run_agent(user_input: str, max_steps: int = 12):
    input_items = CONVERSATION + [{"role": "user", "content": user_input}]

    for _ in range(max_steps):
        response = client.responses.create(
            model="gpt-5.4",
            input=input_items,
            instructions=INSTRUCTIONS,
            tools=TOOLS_SCHEMA,
            # text=TEXT_FORMAT,
            parallel_tool_calls=False,
        )

        response_items = [item.model_dump() for item in response.output]
        input_items.extend(response_items)
        CONVERSATION.extend(response_items)

        function_calls = [
            item for item in response.output if item.type == "function_call"
        ]
        if function_calls:
            for fc in function_calls:
                arguments = json.loads(fc.arguments)
                tool_output = run_tool(fc.name, arguments)

                output_item = {
                    "type": "function_call_output",
                    "call_id": fc.call_id,
                    "output": json.dumps(tool_output),
                }

                input_items.append(output_item)
                CONVERSATION.append(
                    {
                        "type": "function_call_output",
                        "call_id": fc.call_id,
                        "name": fc.name,
                        "arguments": arguments,
                        "output": tool_output,
                    }
                )
            continue

        final_text = response.output_text
        if final_text:
            CONVERSATION.append({"role": "assistant", "content": final_text})
            return final_text

        message_items = [item for item in response.output if item.type == "message"]
        if message_items:
            parts = []
            for msg in message_items:
                for content in msg.content:
                    if hasattr(content, "text") and content.text:
                        parts.append(content.text)
            final_text = "\n".join(parts)
            CONVERSATION.append({"role": "assistant", "content": final_text})
            return final_text

    return "Max agent steps reached without a final answer."

