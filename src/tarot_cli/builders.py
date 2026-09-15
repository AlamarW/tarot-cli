from .models import MinorArcana
from .models import MajorArcana
from .models import Deck


def build_minor_arcana() -> list[MinorArcana]:
    suits = ["Pentacles", "Swords", "Cups", "Wands"]
    vals = list(range(2, 11)) + (["Ace", "Page", "Knight", "Queen", "King"])
    partial_deck = []
    for suit in suits:
        for val in vals:
            partial_deck.append(MinorArcana(suit, val))

    return partial_deck


def build_major_arcana() -> list[MajorArcana]:
    vals = [
        "THE FOOL",
        "THE MAGICIAN",
        "THE HIGH PRIESTESS",
        "THE EMPRESS",
        "THE EMPEROR",
        "THE HIEROPHANT",
        "THE LOVERS",
        "THE CHARIOT",
        "STRENGTH",
        "THE HERMIT",
        "WHEEL OF FORTUNE",
        "JUSTICE",
        "THE HANGED MAN",
        "DEATH",
        "TEMPERANCE",
        "THE DEVIL",
        "THE TOWER",
        "THE STAR",
        "THE MOON",
        "THE SUN",
        "JUDGEMENT",
        "THE WORLD",
    ]
    partial_deck = []
    for i in range(len(vals)):
        partial_deck.append(MajorArcana(i, vals[i]))

    return partial_deck


def build_full_deck() -> Deck:
    minor_arcana = build_minor_arcana()
    major_arcana = build_major_arcana()

    return Deck(major_arcana=major_arcana, minor_arcana=minor_arcana)
