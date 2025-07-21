from datetime import datetime as dt


def read_intent(intent: str | dt) -> int | float:
    if isinstance(intent, dt):
        return int(dt.now().timestamp())
    if isinstance(intent, str):
        intent_seed = sum([ord(i) for i in intent.replace(" ", "")])
        return intent_seed
