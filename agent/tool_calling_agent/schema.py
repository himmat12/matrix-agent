from pydantic import BaseModel
from typing import Dict, List, Any


class PropertiesObject(BaseModel):
    name: str
    type: str
    description: str


class Properties(BaseModel):
    plan: PropertiesObject
    message: PropertiesObject
    observation: PropertiesObject


class Schema(BaseModel):
    type: str
    properties: Properties
    required: List[str]
    additionalProperties: bool


class Format(BaseModel):
    type: str
    name: str
    strict: bool
    schema: Schema


class LLMResponse(BaseModel):
    type: str
    output: Dict[str, Any]


observationProperty = PropertiesObject(
    name="observation",
    type="string",
    description="Brief explanation of how the final answer was produced and did it meet the user request.",
)

messageProperty = PropertiesObject(
    name="message",
    type="string",
    description="Final user-facing response.",
)

planProperty = PropertiesObject(
    name="plan",
    type="string",
    description="Short working memory summary for the next loop: what was done, what remains, and any constraints.",
)


properties = Properties(
    plan=planProperty,
    message=messageProperty,
    observation=observationProperty,
)

schema = Schema(
    type="object",
    properties=properties,
    required=[
        planProperty.name,
        messageProperty.name,
        observationProperty.name,
    ],
    additionalProperties=False,
)

format = Format(
    name="new_json_schema",
    type="json_schema",
    strict=True,
    schema=schema,
)

INSTRUCTIONS = """
You are a tool calling agent who will use available tools to help user queries.
When user requests some tasks you first evaluate the goal and use tools when necessary.
Tools can be used when possible if the specific tasks can be done with it.
""".strip()

TEXT_FORMAT = {"format": format.model_dump()}
