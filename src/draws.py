from __future__ import annotations

import src.models as tarot
from typing import Callable


def process_draw(inp: str) -> Callable:
    action_dict = {
        "draw one": draw_one,
        "draw": draw_one,
        "past present future": draw_past_present_future,
    }
    if inp in action_dict:
        return action_dict[inp]
    else:
        raise ValueError


def read_card(card: tarot.MajorArcana | tarot.MinorArcana) -> dict:
    if isinstance(card, tarot.MajorArcana):
        return card.read_major_card()
    if isinstance(card, tarot.MinorArcana):
        return card.read_minor_card()


def draw_one(deck: tarot.Deck, intent: int) -> dict:
    card = deck.draw_card(intent=intent)
    message = read_card(card)

    return {
        "spread": ("Draw one",),
        "cards": (str(card),),
        "messages": (message,),
    }


def draw_past_present_future(deck: tarot.Deck, intent: int) -> dict:
    past = deck.draw_card(intent=intent)
    present = deck.draw_card(intent=intent)
    future = deck.draw_card(intent=intent)

    past_message = read_card(past)
    present_message = read_card(present)
    future_message = read_card(future)

    return {
        "spread": ("Past", "Present", "Future"),
        "cards": (str(past), str(present), str(future)),
        "messages": (past_message, present_message, future_message),
    }
