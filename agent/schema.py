AGENT_INSTRUCTIONS = """
You are a helpful assistant James that generates text based on the given prompt. You can also call tools if needed. 
Always respond with a JSON object that adheres to the following schema:
{
    "thought": "Your thought process or reasoning behind the response.",
    "action": "The action you want to take, either 'tool_call' or 'final'.",
    "tool_name": "The name of the tool you want to call (if action is 'tool_call'), otherwise null.",
    "arguments": { ... } (if action is 'tool_call'), otherwise null.",
    "final_answer": "The final answer you want to convey to the user."
}
"""

AGENT_SCHEMA = {
    "type": "object",
    "properties": {
        "thought": {
            "type": "string",
            "description": "Your step-by-step thought process or reasoning explanation behind the response.",
        },
        "action": {
            "type": "string",
            "description": "The action you want to take, either 'tool_call' or 'final'.",
            "enum": ["tool_call", "final"],
        },
        "tool_name": {
            "type": ["string", "null"],
            "description": "The name of the tool you want to call (if action is 'tool_call'), otherwise null.",
        },
        "arguments": {
            "description": "The arguments for the tool call (if action is 'tool_call'), otherwise null.",
            "anyOf": [
                {
                    "type": "object",
                    "description": "Tool arguments: shape depends on tool_name",
                    "additionalProperties": False,
                },
                {"type": "null"},
            ],
        },
        "final_answer": {
            "type": "string",
            "description": "The final answer you want to convey to the user for this step.",
        },
    },
    "required": ["thought", "action", "tool_name", "arguments", "final_answer"],
    "additionalProperties": False,
}

TEXT_FORMAT = {
    "format": {
        "type": "json_schema",
        "name": "react_agent_step",
        "strict": True,
        "schema": AGENT_SCHEMA,
    }
}

text = {
    "format": {
        "type": "json_schema",
        "name": "math_response",
        "schema": {
            "type": "object",
            "properties": {
                "steps": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "explanation": {"type": "string"},
                            "output": {"type": "string"},
                        },
                        "required": ["explanation", "output"],
                        "additionalProperties": False,
                    },
                },
                "final_answer": {"type": "string"},
            },
            "required": ["steps", "final_answer"],
            "additionalProperties": False,
        },
        "strict": True,
    }
}
