from __future__ import annotations
import random


class Deck:
    def __init__(
        self, major_arcana: list[MajorArcana], minor_arcana: list[MinorArcana]
    ) -> None:
        self.major_arcana = major_arcana
        self.minor_arcana = minor_arcana

    def __len__(self):
        return len(self.major_arcana) + len(self.minor_arcana)

    def draw_card(self, intent: int) -> MinorArcana | MajorArcana:
        random.seed(intent)
        deck = self.major_arcana + self.minor_arcana
        card = deck.pop(random.randrange(len(deck)))
        return card


class MajorArcana:
    def __init__(self, num: int, name: str) -> None:
        self.num = num
        self.name = name

    def __str__(self):
        return f"{self.num}. {self.name}"

    def read_major_card(self) -> str:
        major_arcana_lookup = {
            "THE FOOL": "New beginnings and unlimited potential",
            "THE MAGICIAN": "Personal power and manifestation ability",
            "THE HIGH PRIESTESS": "Intuition and inner wisdom",
            "THE EMPRESS": "Fertility, creativity, and nurturing abundance",
            "THE EMPEROR": "Authority, structure, and stable leadership",
            "THE HIEROPHANT": "Spiritual guidance and traditional wisdom",
            "THE LOVERS": "Love, relationships, and important choices",
            "THE CHARIOT": "Willpower and triumph through determination",
            "STRENGTH": "Inner strength and patient courage",
            "THE HERMIT": "Soul searching and inner guidance",
            "WHEEL OF FORTUNE": "Destiny, cycles, and changing fortune",
            "JUSTICE": "Fairness, truth, and karmic balance",
            "THE HANGED MAN": "Surrender and gaining new perspective",
            "DEATH": "Transformation and necessary endings",
            "TEMPERANCE": "Balance, moderation, and healing",
            "THE DEVIL": "Temptation and confronting limitations",
            "THE TOWER": "Sudden change and necessary disruption",
            "THE STAR": "Hope, inspiration, and renewal",
            "THE MOON": "Illusion, intuition, and subconscious wisdom",
            "THE SUN": "Joy, success, and enlightenment",
            "JUDGEMENT": "Rebirth and spiritual awakening",
            "THE WORLD": "Completion and fulfillment",
        }

        return f"{major_arcana_lookup[self.name]}"


class MinorArcana:
    def __init__(self, suit: str, val: int | str) -> None:
        self.suit = suit
        self.val = val

    def __str__(self):
        return f"{self.val} of {self.suit}"

    def read_minor_card(self) -> str:
        suit_meaning_lookup = {
            "Cups": "Emotion",
            "Pentacles": "Practicality",
            "Swords": "Intellect",
            "Wands": "Passion",
        }

        val_meaning_lookup = {
            "Ace": "New Beginnings in, or raw essence of",
            2: "Balance in",
            3: "New Union in",
            4: "Structure of",
            5: "Change in or stress from",
            6: "Seeking Stability in",
            7: "Needing Pause in",
            8: "Strength in",
            9: "Climax in",
            10: "Ending of",
            "Page": "Embodying curiosity in",
            "Knight": "Embodying action in",
            "Queen": "Embodying wisdom in",
            "King": "Embodying authority in",
        }

        return f"{val_meaning_lookup[self.val]} {suit_meaning_lookup[self.suit]}"
