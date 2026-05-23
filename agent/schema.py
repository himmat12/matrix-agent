TOOL_NAMES = [
    "getAgentLocation",
    "moveAgent",
    "moveUntilEdgeOrWallWithoutFallingFromEdge",
    None,
]

TOOLS_SCHEMA = [
    {
        "type": "function",
        "name": "getAgentLocation",
        "description": "Get the current location of the agent in the 10x10 matrix world.",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "moveAgent",
        "description": "Move the agent by one cell in the given direction if the move is valid. Returns true if the move succeeds, otherwise false.",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "enum": ["up", "down", "left", "right"],
                    "description": "The direction to move the agent by one step.",
                }
            },
            "required": ["direction"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "moveUntilEdgeOrWallWithoutFallingFromEdge",
        "description": "Move the agent continuously in the given direction until it reaches a wall or the edge of the world without falling off the map.",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "direction": {
                    "type": "string",
                    "enum": ["up", "down", "left", "right"],
                    "description": "The direction to keep moving the agent.",
                }
            },
            "required": ["direction"],
            "additionalProperties": False,
        },
    },
]

AGENT_INSTRUCTIONS = """
You are a helpful assistant who exists in a 2D grid world.
You can move around the grid by choosing tools when needed.

Always respond with a JSON object matching this structure:
{
  "plan": "A brief explanation of the next step.",
  "action": "Either 'tool_call' or 'final'.",
  "tool_name": "One of: getAgentLocation, moveAgent, moveUntilEdgeOrWallWithoutFallingFromEdge, or null.",
  "arguments": "An object of tool arguments if action is 'tool_call', otherwise null.",
  "message": "A user-facing response for this step."
}

Rules:
- If action is "final", tool_name must be null and arguments must be null.
- If action is "tool_call", tool_name must be a valid tool name and arguments must match that tool.
- Keep plan short and useful.
"""

AGENT_SCHEMA = {
    "type": "object",
    "properties": {
        "plan": {
            "type": "string",
            "description": "Brief explanation of the next step.",
        },
        "action": {
            "type": "string",
            "description": "The action you want to take, either 'tool_call' or 'final'.",
            "enum": ["tool_call", "final"],
        },
        "tool_name": {
            "type": ["string", "null"],
            "description": "Tool to call when action is tool_call, otherwise null.",
            "enum": TOOL_NAMES,
        },
        "arguments": {
            "type": ["object", "null"],
            "description": "Arguments for the tool call, otherwise null.",
            "additionalProperties": False,
        },
        "message": {
            "type": "string",
            "description": "User-facing response for this step. If action is final, this is the final answer.",
        },
    },
    "required": ["plan", "action", "tool_name", "arguments", "message"],
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
