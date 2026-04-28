from .hand import Hand
from .card import Card
from .deck import Deck

class Dealer():
    def __init__(self):
        self.hand: Hand = Hand()

    def hit(self, card: Card) -> str | None:
        if self.hand.total > 17:
            return "wrong choise!\n if the dealer has 17 or higher they should stand"
        else:
            self.hand.hit(card)
            return "Good choise"
            

    def stand(self) -> None:
        if self.hand.total < 17:
            return "wrong choise!\n if the dealer has 16 or lower they should stand"
        else:
            self.hand.stand()
            return "Good choise"

    def deal(self, deck:Deck) -> Card:
        return deck.hit()
    
    def reset():
        pass