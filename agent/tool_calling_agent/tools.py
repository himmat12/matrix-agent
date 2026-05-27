import inspect
from docstring_parser import parse
from typing import Dict, Any, List

"""
Agent Tools: Arithmetic tool sets
"""


def add(x: float, y: float) -> float:
    """Adds two numbers and returns the sum.

    Args:
        x (float): first positional parameter number
        y (float): second positional parameter number

    Returns:
        float: A sum of `x` and `y`
    """
    return x + y


def subtract(x: float, y: float) -> float:
    """Subtracts two numbers and returns the difference.

    Args:
        x (float): first positional parameter number
        y (float): second positional parameter number

    Returns:
        float: A difference of `x` and `y`
    """
    return x - y


def multiply(x: float, y: float) -> float:
    """Multiply two numbers and returns the product.

    Args:
        x (float): first positional parameter number
        y (float): second positional parameter number

    Returns:
        float: A product of `x` and `y`
    """
    return x * y


def divide(x: float, y: float) -> float:
    """Divides two numbers and returns the quotient.

    Args:
        x (float): dividend number
        y (float): divisor number

    Returns:
        float: A quotient of `x` / `y`

    Raises:
        ValueError: If attempt to divide by zero.
    """
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y


def mod(x: float, y: float) -> float:
    """Modulo two numbers and returns the remainder.

    Args:
        x (float): dividend number
        y (float): divisor number

    Returns:
        float: A remainder of `x` modulo `y`

    Raises:
        ValueError: If attempt to modulo by zero.
    """
    if y == 0:
        raise ValueError("Cannot modulo by zero.")
    return x % y


def pi() -> float:
    """
    Value of Pi.
    Returns:
        float: the constant value of `pi` which is `3.141592653589793`
    """

    return 3.141592653589793


def get_x_percentage_of_y(x: float, y: float) -> float:
    """Calculate the `x` percentage of `y`.

    Args:
        x (float): percentage number, eg.: `10%`
        y (float): number of which percenage you want to calcuate, eg.: `100`

    Returns:
        float: A `x` percentage of `y`

    Examples:
        ```python
        percentage = get_x_percentage_of_y(x=10, y=100)
        percentage = 10
        # 10% of 100 is 10
        ```
    """
    return (x / 100.0) * y


TOOLS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
    "mod": mod,
    "pi": pi,
    "get_x_percentage_of_y": get_x_percentage_of_y,
}

"""
Utility functions: Tool schemas generation functions 
"""


def create_tool_schmea(
    func: Any,
    strict: bool = True,
    additional_properties: bool = False,
) -> Dict[str, Any]:
    """Extracts the metadata from the docstring and generates a OpenAI compatible tools schema.

    Args:
        func (Any): An object coud be `function` or `class`

    Returns:
        tool_schema (Dict[str, Any]): A tool schema dictionary fr OpenAI models.
    """
    tool_schema = {}
    required = []
    properties = {}

    sig = inspect.signature(func)
    doc_string = inspect.getdoc(func)
    parsed = parse(doc_string)

    if parsed:
        for parma in parsed.params:
            properties[parma.arg_name] = {
                "type": parma.type_name,
                "description": parma.description,
            }

        for name, parma in sig.parameters.items():
            is_required = parma.default is inspect.Parameter.empty
            if is_required:
                required.append(name)

        tool_schema["type"] = "function"
        tool_schema["name"] = func.__name__
        tool_schema["description"] = parsed.description
        tool_schema["strict"] = strict
        tool_schema["required"] = required
        tool_schema["properties"] = properties
        tool_schema["additionalProperties"] = additional_properties

    return tool_schema


def generate_tools_schema(tools: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Generates a list of tools schema compitable to OpenAI models.

    Returns:
        tool_schemas (Dict[str, Any]): A List of dictionary which is compitable with OpenAI models tool schema.
    """
    tool_schemas = []

    for tool in tools:
        tool_schema = create_tool_schmea(tools[tool])
        tool_schemas.append(tool_schema)

    return tool_schemas


TOOLS_SCHEMA = generate_tools_schema(TOOLS)
