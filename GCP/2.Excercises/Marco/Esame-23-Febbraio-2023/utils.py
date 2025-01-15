from uuid import uuid4
from datetime import datetime
from re import findall, DOTALL


def get_hashtags(msg: str) -> list:
    return findall('(#\w+)', msg, DOTALL)

def generate_id() -> str:
    return str(uuid4())

def generate_timestamp() -> str:
    return str(datetime.now().timestamp())
