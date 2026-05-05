from .card import Card, Suits, Values
from random import shuffle

class Deck():
    def __init__(self):
        self.__cards: list[Card] = [] 
        self.cards_left: int = 0

        for s in Suits:
            for v in Values:
                self.__cards.append(Card(s, v))

        self.cards_left = len(self.__cards)

    def shuffle_deck(self) -> None:
        shuffle(self.__cards)

    def hit(self) -> Card:
        selected = self.__cards.pop(0)
        self.cards_left = len(self.__cards)

        return selected
