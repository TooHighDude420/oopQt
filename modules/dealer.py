from .hand import Hand
from .card import Card
from .deck import Deck

class Dealer():
    def __init__(self):
        self.hand: Hand = Hand()

    def hit(self, card: Card) -> None:
        if self.hand.total > 17:
            print("wrong choise!\n if the dealer has 17 or higher he/she should stand")
        
        self.hand.hit(card)


    def stand(self) -> None:
        self.hand.stand()

    def deal(self, deck:Deck) -> Card:
        return deck.hit()
    
    def reset():
        pass