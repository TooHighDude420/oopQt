from .hand import Hand
from .card import Card
from .deck import Deck

from rich.console import Console

class Dealer():
    def __init__(self):
        self.__hand: Hand = Hand()

    def hit(self, card: Card) -> tuple[str, int]:
        if self.__hand.get_total() > 17:
            return ("[red]Wrong choise![/red] if the dealer has 17 or higher they should stand", -1)
        else:
            self.__hand.hit(card)
            return ("[green]Good choise![/green]", 1)
            
    def stand(self) -> tuple[str, int]:
        if self.__hand.get_total() < 17:
            return ("[red]Wrong choise![/red] if the dealer has 16 or lower they should stand", -1)
        else:
            self.__hand.stand()
            return ("[green]Good choise![/green]", 1)

    def deal(self, deck:Deck) -> Card:
        return deck.hit()
    
    def get_num_cards(self) -> int:
        return self.__hand.get_num_cards()
    
    def get_total(self) -> int:
        return self.__hand.get_total()

    def shuffle_deck(self, shuffle: str, deck: Deck) -> tuple[str, int]:
        if shuffle not in ('y', 'n'):
            return ("enter y or n\n", 1)
        
        if shuffle == 'y':
            deck.shuffle_deck()
            return ("[green]Good choise![/green]", 1)
        else:
            return ("[red]Wrong choise![/red] at the start of the game the dealer must shuffle the cards", -1)

    def dealer_turn(self, input: int, deck: Deck) -> tuple[str, int]:
        match input:
            case 1:
                feedback = self.hit(self.deal(deck))

            case 2:
                feedback = self.stand()

            case _:
                return ("enter 1 or 2", 0)

        return feedback

    def det_winner(self, totals:dict[str, list[int, int]], input: int, sellist: list[str]) -> tuple[tuple[str, int], list[int]] | tuple[None, list[int]]:
        dealer_num = len(totals.keys())
        done_choise = dealer_num + 1
        
        if input == done_choise:
            if str(dealer_num) in sellist:
                if len(sellist) > 1:
                    feedback = ("[red]Wrong choise![/red] when the dealer wins, nobody else wins. earned points", -1)
                    sellist = []

                else:
                    if not totals["Dealer"] > 21:
                        truth = []

                        for key, val in totals.items():
                            if key != "Dealer":
                                if not val[0] > 21:
                                    if totals["Dealer"] >= val[0]:
                                        truth.append(True)
                                    else:
                                        truth.append(False)
                                else:
                                    truth.append(True)

                        if False in truth:
                            feedback = ("[red]Wrong choise![/red]someone has higher then dealer", -1)
                            sellist = []
                        else:
                            feedback = ("[green]Good choise![/green], earned points", 1)

                    else:
                        feedback = ("[red]Wrong choise![/red] dealer is bust", -1)
                        sellist = []

            else:
                truth = []

                for sel in sellist:
                    if totals[f"Player{sel}"][0] > totals["Dealer"] and totals[f"Player{sel}"][0] < 22:
                        truth.append(True)
                    else:
                        truth.append(False)

                if False in truth:
                    feedback = ("[red]Wrong choise![/red] you enterd a losing number. earned points", -1)
                    sellist = []
                else:
                    feedback = ("[green]Good choise![/green], earned points", 1)

        else:
            sellist.append(str(input))
            return (None, sellist)

        return (feedback, sellist)

    # todo add pay-out
    ## reipmplement gamelogger

    def reset():
        pass