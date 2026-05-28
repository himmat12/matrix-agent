from pydantic import BaseModel
from typing import Dict, List, Any


class PropertiesObject(BaseModel):
    name: str
    type: str
    description: str


class Properties(BaseModel):
    plan: PropertiesObject
    message: PropertiesObject


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


planProperty = PropertiesObject(
    name="plan",
    type="string",
    description="A brief plan for next action.",
)
messageProperty = PropertiesObject(
    name="message",
    type="string",
    description="Response for user.",
)
properties = Properties(plan=planProperty, message=messageProperty)
schema = Schema(
    type="object",
    properties=properties,
    required=[planProperty.name, messageProperty.name],
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
