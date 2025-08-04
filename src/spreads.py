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
        raise ValueError


def read_card(card: tarot.MajorArcana | tarot.MinorArcana) -> str:
    if isinstance(card, tarot.MajorArcana):
        return card.read_major_card()
    if isinstance(card, tarot.MinorArcana):
        return card.read_minor_card()


def draw_one(deck: tarot.Deck, intent: int | str | dt | None = None) -> dict:
    if intent is None:
        intent_seed = dt.now().microsecond
    elif isinstance(intent, (str, dt)):
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
    if intent is None:
        intent_seed = dt.now().microsecond
    elif isinstance(intent, (str, dt)):
        intent_seed = intent_module.read_intent(intent)
    else:
        intent_seed = intent
    
    card1 = deck.draw_card(intent=intent_seed)
    card2 = deck.draw_card(intent=intent_seed+1)
    card3 = deck.draw_card(intent=intent_seed+2)

    card1_message = read_card(card1)
    card2_message = read_card(card2)
    card3_message = read_card(card3)

    return {
        "spread": ("First", "Second", "Third"),
        "cards": (str(card1), str(card2), str(card3)),
        "messages": (card1_message, card2_message, card3_message),
    }

def draw_past_present_future(
    deck: tarot.Deck, intent: int | str | dt | None = None
) -> dict:
    if intent is None:
        intent_seed = dt.now().microsecond
    elif isinstance(intent, (str, dt)):
        intent_seed = intent_module.read_intent(intent)
    else:
        intent_seed = intent

    past = deck.draw_card(intent=intent_seed)
    present = deck.draw_card(intent=intent_seed + 1)
    future = deck.draw_card(intent=intent_seed + 2)

    past_message = read_card(past)
    present_message = read_card(present)
    future_message = read_card(future)

    return {
        "spread": ("Past", "Present", "Future"),
        "cards": (str(past), str(present), str(future)),
        "messages": (past_message, present_message, future_message),
    }


def draw_celtic_cross(deck: tarot.Deck, intent: int | str | dt | None = None) -> dict:
    if intent is None:
        intent_seed = dt.now().microsecond
    elif isinstance(intent, (str, dt)):
        intent_seed = intent_module.read_intent(intent)
    else:
        intent_seed = intent

    # Draw 10 cards for the Celtic Cross spread
    cards = []
    for i in range(10):
        card = deck.draw_card(intent=intent_seed + i)
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
