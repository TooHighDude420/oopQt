from .hand import Hand
from .card import Card

class Player():
    def __init__(self):
        self.hand:Hand = Hand()

    def hit(self, card: Card) -> None:
        self.hand.hit(card)

    def stand(self) -> None:
        self.hand.stand()