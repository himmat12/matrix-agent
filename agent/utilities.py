from typing import List, Dict, Any


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
