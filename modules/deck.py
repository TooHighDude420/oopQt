from .card import Card, Suits, Values
from random import shuffle

class Deck():
    full_deck = []

    def __init__(self):
        for s in Suits:
            for v in Values:
                self.full_deck.append(Card(s, v))

    def shuffle_deck(self):
        shuffle(self.full_deck)
        
        for card in self.full_deck:
            print(str(card))