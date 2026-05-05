from .hand import Hand
from .card import Card
from .deck import Deck

class Dealer():
    def __init__(self):
        self.hand: Hand = Hand()

    def hit(self, card: Card) -> tuple[str, int] | None:
        if self.hand.total > 17:
            return ("wrong choise!\n if the dealer has 17 or higher they should stand", -1)
        else:
            self.hand.hit(card)
            return ("Good choise", 1)
            

    def stand(self) -> tuple[str, int]:
        if self.hand.total < 17:
            return ("wrong choise!\n if the dealer has 16 or lower they should stand", -1)
        else:
            self.hand.stand()
            return ("Good choise", 1)

    def deal(self, deck:Deck) -> Card:
        return deck.hit()
    
<<<<<<< Updated upstream
=======
    def get_num_cards(self) -> int:
        return self.__hand.get_num_cards()
    
    def get_total(self) -> int:
        return self.__hand.get_total()

    def shuffle_deck(self, shuffle: str, deck: Deck) -> tuple[str, int]:
        if shuffle not in ('y', 'n'):
            return ("enter y or n\n", 1)
        
        if shuffle == 'y':
            deck.shuffle_deck()
            return ("[green]Good choice![/green]", 1)
        else:
            return ("[red]Wrong choice![/red] at the start of the game the dealer must shuffle the cards", -1)

    def dealer_turn(self, input: int, deck: Deck) -> tuple[str, int]:
        match input:
            case 1:
                feedback = self.hit(self.deal(deck))

            case 2:
                feedback = self.stand()

            case _:
                return ("enter 1 or 2", 0)

        return feedback

    def deal_cards_choise(self, input:int) -> tuple[str, int]:
        if input == 1:
            return (f"[red]Wrong choice![/red] first take the bets then deals the cards", -1)
        elif input == 2:
            return (f"[green]Good choice![/green]", 1)

    def give_cards(self, input: int, max_cards: int, done_choise:int, player_list:list[Player], deck: Deck) -> tuple[str, int] | None:
        if input == done_choise:
            if self.__dealt_cards == max_cards:
              feedback = (f"[green]Good choice![/green]", 1)

            else:
                feedback = (f"[red]Wrong choice![/red] everyone gets 2 cards", -1)
            
            return feedback
        
        elif self.__dealt_index != input:
            feedback = (f"[red]Wrong choice![/red] you must deal the cards one by one in order {self.__dealt_index} was the right choice", -1)
            
            return feedback

        else:
            player_list[self.__dealt_index - 1].hit(self.deal(deck))
            self.__dealt_index += 1
            self.__dealt_cards += 1
            
            if self.__dealt_cards == max_cards:
                self.__dealt_index == len(player_list) + 1
            elif self.__dealt_index == len(player_list) + 1:
                self.__dealt_index = 1

    def det_winner(self, totals:dict[str, list[int, int]], input: int, sellist: list[str]) -> tuple[tuple[str, int], list[int]] | tuple[None, list[int]]:
        dealer_num = len(totals.keys())
        done_choise = dealer_num + 1
        
        if input == done_choise:
            if str(dealer_num) in sellist:
                if len(sellist) > 1:
                    feedback = ("[red]Wrong choice![/red] when the dealer wins, nobody else wins. earned points", -1)
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
                            feedback = ("[red]Wrong choice![/red]someone has higher then dealer", -1)
                            sellist = []
                        else:
                            feedback = ("[green]Good choice![/green]", 1)

                    else:
                        feedback = ("[red]Wrong choice![/red] dealer is bust", -1)
                        sellist = []

            else:
                truth = []

                for key, val in totals.items():
                    if key != "Dealer":
                        if val[0] > totals["Dealer"] and val[0] < 22 or totals["Dealer"] > 21 and val[0] < 22:
                            index = key.replace("Player", "")
                            if index in sellist:
                                truth.append(True)
                            else:
                                truth.append(False)

                for sel in sellist:
                    if totals[f"Player{sel}"][0] > totals["Dealer"] and totals[f"Player{sel}"][0] < 22 or totals["Dealer"] > 21 and totals[f"Player{sel}"][0] < 22:
                        truth.append(True)
                    else:
                        truth.append(False)

                if False in truth:
                    feedback = ("[red]Wrong choice![/red] you enterd a losing number. earned points", -1)
                    sellist = []
                else:
                    feedback = ("[green]Good choice![/green], earned points", 1)

        else:
            sellist.append(str(input))
            return (None, sellist)

        return (feedback, sellist)

    def player_turn(self, input: int, action: str) -> tuple[str, int]:
        match input:
            case 1:
                if action == "HIT":
                    feedback = ("[green]Good choice![/green]", 1)

                else:
                    feedback = ("[red]Wrong choice![/red] When someone [bold]stand[/bold]s you should [bold]do nothing[/bold]", -1)

                return feedback

            case 2:
                if action == "STAND":
                    feedback = ("[green]Good choice![/green]", 1)

                else:
                    feedback = ("[red]Wrong choice![/red] When someone [bold]hit[/bold]s you should [bold]give them a card[/bold]", -1)

                return feedback

>>>>>>> Stashed changes
    def reset():
        pass