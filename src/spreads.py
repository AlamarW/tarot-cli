from __future__ import annotations

import src.models as tarot
import src.intent as intent_module
from typing import Callable
from datetime import datetime as dt


def process_draw(inp: str) -> Callable:
    action_dict = {
        "draw one": draw_one,
        "draw": draw_one,
        "past present future": draw_past_present_future,
        "celtic cross": draw_celtic_cross,
        "draw three": draw_three,
    }
    if inp in action_dict:
        return action_dict[inp]
    else:
        raise ValueError(f"could not find {inp}")


def read_card(card: tarot.MajorArcana | tarot.MinorArcana) -> str:
    if isinstance(card, tarot.MajorArcana):
        return card.read_major_card()
    if isinstance(card, tarot.MinorArcana):
        return card.read_minor_card()


def draw_one(deck: tarot.Deck, intent: int | str | dt ) -> dict:
    if isinstance(intent, (str, dt)):
        intent_seed = intent_module.read_intent(intent)
    else:
        intent_seed = intent

    card = deck.draw_card(intent=intent_seed)
    message = read_card(card)

    return {
        "spread": ("Draw one",),
        "cards": (str(card),),
        "messages": (message,),
    }


def draw_three(
        deck: tarot.Deck, intent: int | str | dt | None = None
) -> dict:
    if isinstance(intent, (str, dt)):
        intent_seed = intent_module.read_intent(intent)
    else:
        intent_seed = intent

    cards = []
    for i in range(3):
        card = deck.draw_card(intent=intent_seed*dt.now().microsecond)
        cards.append(card)

    positions = (
        "First",
        "Second",
        "Third",
    )

    messages = tuple(read_card(card) for card in cards)
    card_strings = tuple(str(card) for card in cards)

    return {
        "spread": positions,
        "cards": card_strings,
        "messages": messages,
    }

def draw_past_present_future(
    deck: tarot.Deck, intent: int | str | dt = dt.now()
) -> dict:
    if isinstance(intent, (str, dt)):
        intent_seed = intent_module.read_intent(intent)
    else:
        intent_seed = intent
    cards = []
    for i in range(3):
        card = deck.draw_card(intent=intent_seed*dt.now().microsecond)
        cards.append(card)
    positions = (
            "Past",
            "Present",
            "Future",
    )

    messages = tuple(read_card(card) for card in cards)
    card_strings = tuple(str(card) for card in cards)

    return {
        "spread": positions,
        "cards": card_strings,
        "messages": messages,
    }


def draw_celtic_cross(deck: tarot.Deck, intent: int | str | dt) -> dict:
    if isinstance(intent, (str, dt)):
        intent_seed = intent_module.read_intent(intent)
    else:
        intent_seed = intent

    # Draw 10 cards for the Celtic Cross spread
    cards = []
    for i in range(10):
        card = deck.draw_card(intent=intent_seed*dt.now().microsecond)
        cards.append(card)

    # Celtic Cross positions in traditional order
    positions = (
        "Present Situation",
        "Cross/Challenge",
        "Distant Past/Foundation",
        "Recent Past",
        "Possible Outcome",
        "Immediate Future",
        "Your Approach",
        "External Influences",
        "Inner Feelings",
        "Final Outcome",
    )

    # Read each card
    messages = tuple(read_card(card) for card in cards)
    card_strings = tuple(str(card) for card in cards)

    return {
        "spread": positions,
        "cards": card_strings,
        "messages": messages,
    }
