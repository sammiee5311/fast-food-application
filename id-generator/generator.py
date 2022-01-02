import uuid


def generate_id() -> str:
    _uuid = uuid.uuid4()

    return _uuid.hex
