from datetime import datetime as dt


def read_intent(intent: str | dt) -> int:
    if isinstance(intent, dt):
        return intent.microsecond
    if isinstance(intent, str):
        intent_seed = sum([ord(i) for i in intent.replace(" ", "")])
        return intent_seed
    raise ValueError(f"Unsupported intent type: {type(intent)}")
