from .hand import Hand
from .card import Card
from .deck import Deck

class Dealer():
    def __init__(self):
        self.hand: Hand = Hand()

    def hit(self, card: Card) -> None:
        self.hand.hit(card)

    def stand(self) -> None:
        self.hand.stand()

    def deal(self, deck:Deck) -> Card:
        return deck.hit()
    
    def reset():
        pass