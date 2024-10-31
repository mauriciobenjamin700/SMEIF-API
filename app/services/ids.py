from uuid import uuid4


def id_generate() -> str:
    """
    Generate a random ID
    """
    return str(uuid4())