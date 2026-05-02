from .hand import Hand
from .card import Card
from .deck import Deck

from rich.console import Console

class Dealer():
    def __init__(self):
        self.hand: Hand = Hand()

    def hit(self, card: Card) -> tuple[str, int]:
        if self.hand.total > 17:
            return ("[red]Wrong choise![/red] if the dealer has 17 or higher they should stand", -1)
        else:
            self.hand.hit(card)
            return ("[green]Good choise![/green]", 1)
            
    def stand(self) -> tuple[str, int]:
        if self.hand.total < 17:
            return ("[red]Wrong choise![/red] if the dealer has 16 or lower they should stand", -1)
        else:
            self.hand.stand()
            return ("[green]Good choise![/green]", 1)

    def deal(self, deck:Deck) -> Card:
        return deck.hit()
    
    def get_num_cards(self) -> int:
        return self.hand.get_num_cards()
    
    def shuffle_deck(self, console: Console, deck: Deck) -> tuple[str, int]:
        shuffle = console.input("shuffle deck?, y/n\n")
        console.clear()
        shuffle.lower()

        if shuffle not in ('y', 'n'):
            console.print("enter y or n\n")
            feedback = self.shuffle_deck(deck)
            return feedback
        
        if shuffle == 'y':
            deck.shuffle_deck()
            return ("[green]Good choise![/green]", 1)
        else:
            return ("[red]Wrong choise![/red] at the start of the game the dealer must shuffle the cards", -1)

    def reset():
        pass