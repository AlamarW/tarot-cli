from __future__ import annotations
import src.models as tarot
import src.builders as builders
import src.draws as draws

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
