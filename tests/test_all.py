from __future__ import annotations
import src.models as tarot
import src.builders as builders
import src.draws as draws
import src.intent as intent
from datetime import datetime

import pytest


def test_build_minor_arcana():
    d = builders.build_minor_arcana()
    assert len(d) == 56


def test_build_major_arcana():
    d = builders.build_major_arcana()
    assert len(d) == 22


def test_build_full_deck():
    d = builders.build_full_deck()

    assert isinstance(d, tarot.Deck)
    assert len(d) == 78


def test_draw_card():
    d = builders.build_full_deck()

    c = d.draw_card()
    assert isinstance(c, tarot.MinorArcana) or isinstance(c, tarot.MajorArcana)


def test_read_minor_card():
    c = tarot.MinorArcana("Pentacles", 10)
    message = c.read_minor_card()
    assert message == "Ending of Practicality"


def test_read_minor_card_ace():
    c = tarot.MinorArcana("Pentacles", "Ace")
    message = c.read_minor_card()

    assert message == "New Beginnings in, or raw essence of Practicality"


def test_read_major_card():
    c = tarot.MajorArcana(0, "THE FOOL")
    message = c.read_major_card()

    assert message == "New beginnings and unlimited potential"


def test_draw_one():
    d = builders.build_full_deck()
    c_message = draws.draw_one(d)

    assert isinstance(c_message, dict)
    assert c_message["cards"]
    assert c_message["messages"]


def test_draw_w_input():
    d = builders.build_full_deck()
    inp = "draw one"
    draw_function = draws.process_draw(inp)
    message = draw_function(d)
    assert message["cards"]
    assert message["messages"]


def test_draw_past_present_future():
    d = builders.build_full_deck()
    inp = "past present future"
    draw_function = draws.process_draw(inp)
    message = draw_function(d)

    assert "Past" in message["spread"]
    assert "Present" in message["spread"]
    assert "Future" in message["spread"]


def test_draw_past_present_future_cards_are_different():
    d = builders.build_full_deck()
    inp = "past present future"
    draw_function = draws.process_draw(inp)
    message = draw_function(d, intent=123)

    past_card = message["cards"][0]
    present_card = message["cards"][1]
    future_card = message["cards"][2]

    assert past_card != present_card
    assert present_card != future_card
    assert past_card != future_card


def test_draw_with_prompt():
    d = builders.build_full_deck()
    inp = "draw one"
    prompt = "What is in store for today?"
    draw_function = draws.process_draw(inp)
    message = draw_function(d, intent=prompt)

    assert message["cards"]
    assert message["messages"]


def test_process_draw_invalid_input():
    with pytest.raises(ValueError):
        draws.process_draw("invalid spread")


def test_draw_one_with_int_intent():
    d = builders.build_full_deck()
    message = draws.draw_one(d, intent=42)

    assert message["cards"]
    assert message["messages"]


def test_draw_past_present_future_with_int_intent():
    d = builders.build_full_deck()
    message = draws.draw_past_present_future(d, intent=42)

    assert len(message["cards"]) == 3
    assert len(message["messages"]) == 3


def test_read_intent_with_datetime():
    dt = datetime(2024, 1, 1, 12, 0, 0, 123456)
    result = intent.read_intent(dt)
    assert result == 123456


def test_read_intent_with_unsupported_type():
    with pytest.raises(ValueError, match="Unsupported intent type"):
        intent.read_intent(42)


def test_draw_past_present_future_with_datetime_intent():
    d = builders.build_full_deck()
    dt = datetime(2024, 1, 1, 12, 0, 0, 123456)
    message = draws.draw_past_present_future(d, intent=dt)

    assert len(message["cards"]) == 3
    assert len(message["messages"]) == 3
    assert "Past" in message["spread"]
    assert "Present" in message["spread"]
    assert "Future" in message["spread"]


def test_draw_celtic_cross():
    d = builders.build_full_deck()
    inp = "celtic cross"
    draw_function = draws.process_draw(inp)
    message = draw_function(d, intent=42)

    # Celtic Cross has 10 positions
    assert len(message["cards"]) == 10
    assert len(message["messages"]) == 10
    assert len(message["spread"]) == 10

    # Verify the 10 Celtic Cross positions are present
    expected_positions = [
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
    ]

    for position in expected_positions:
        assert position in message["spread"]

    # All cards should be different (no duplicates in same reading)
    cards = message["cards"]
    unique_cards = set(cards)
    assert len(unique_cards) == 10, (
        f"Expected 10 unique cards, but got {len(unique_cards)} unique cards out of {len(cards)} total cards"
    )


def test_draw_celtic_cross_empty_deck():
    # Create a completely empty deck
    empty_deck = tarot.Deck([], [])
    
    inp = "celtic cross"
    draw_function = draws.process_draw(inp)
    
    # Should raise a ValueError immediately when trying to draw from empty deck
    with pytest.raises(ValueError):
        draw_function(empty_deck, intent=42)


def test_draw_celtic_cross_with_string_intent():
    # Test that string intents work correctly (deterministic results)
    d1 = builders.build_full_deck()
    d2 = builders.build_full_deck()
    
    inp = "celtic cross"
    draw_function = draws.process_draw(inp)
    prompt = "What path should I take in my career?"
    
    message1 = draw_function(d1, intent=prompt)
    message2 = draw_function(d2, intent=prompt)
    
    # Same prompt should give same cards (deterministic)
    assert message1["cards"] == message2["cards"]
    assert message1["messages"] == message2["messages"]


def test_draw_celtic_cross_with_datetime_intent():
    # Test that datetime intents work correctly
    d = builders.build_full_deck()
    dt = datetime(2024, 1, 1, 12, 0, 0, 123456)
    
    inp = "celtic cross"
    draw_function = draws.process_draw(inp)
    message = draw_function(d, intent=dt)
    
    assert len(message["cards"]) == 10
    assert len(message["messages"]) == 10
