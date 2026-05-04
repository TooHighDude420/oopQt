import sys
import time

from .shoe import Shoe
from .dealer import Dealer
from .player import Player
from .deck import Deck

from enum import Enum, auto
from rich.console import Console

class gamestate(Enum):
    GAME_START = 0
    ROUND_START = auto()
    MAIN_LOOP = auto()
    ROUND_END = auto()
    GAME_END = auto()

class actions(Enum):
    HIT = 1
    STAND = auto()

# delay for clearing text
WRONG_DELAY = 4
GOOD_DELAY = 1

class Table:
    def __init__(self, shoe_size:int, amount_of_players:int, console: Console) -> Table:
        self.__dealer: Dealer = Dealer()
        self.__console = console

        # list comprehension
        self.__players: list[Player] = [Player(500) for player in range(amount_of_players)]
        self.__gamestate: gamestate = gamestate.GAME_START
        self.__chips: int = 0
        self.__points: int = 0
        self.__active_player_index: int = 0
        self.__deck: Deck = Deck()
        self.__bust: int = 0
        self.__dealer_turn = True

        # tmp_deck_list: list[Deck] = [Deck() for shoe in range(shoe_size)]
        
        # self.__shoe: Shoe = Shoe(tmp_deck_list)

    def get_gamestate(self) -> gamestate:
        return self.__gamestate
    
    def set_gamestate(self, new_state:gamestate):
        self.__gamestate = new_state
    
    def get_active_player(self) -> tuple[Player, int]:
        return (self.__players[self.__active_player_index], self.__active_player_index)

    def get_player_count(self) -> int:
        return len(self.__players)
    
    def get_deck(self) -> Deck:
        return self.__deck

    def next_player(self) -> None:
        if self.__active_player_index == len(self.__players) -1:
            self.__active_player_index = 0
        else:
            self.__active_player_index += 1

    def next_move(self, input: actions) -> None:
        if input not in actions:
            raise ValueError("not a valid action")
        else:
            player = self.__players[self.__active_player_index]

            match input:
                case actions.HIT:
                    player.hit(self.__dealer.deal(self.__deck))

                case actions.STAND:
                    player.stand()
                    self.next_player()

    def deal_cards_loop(self) -> None:
        done = False
        cards_dealt = 0
        dealt_index = 1

        player_list: list[Player|Dealer] = [p for p in self.__players]
        player_list.append(self.__dealer)

        max_cards = len(player_list) * 2

        while not done:
            ii = 1

            totals_text = ""

            for p in player_list:
                if isinstance(p, Player):
                    totals_text += f"Player{ii}: {p.get_num_cards()}\n"
                elif isinstance(p, Dealer):
                    totals_text += f"Dealer: {p.get_num_cards()}\n"

                ii += 1

            self.__console.print(totals_text)

            deal_text = "\nwho do you give a card:\n"

            ii = 1

            for player in player_list:
                if isinstance(player, Player):
                    deal_text +=  f"\n{ii}. Player{ii}"
                elif isinstance(player, Dealer):
                    deal_text +=  f"\n{ii}. Dealer"
            
                ii += 1

            deal_text += f"\n{ii}. Done dealing cards\n"
            dealer_coise = self.__console.input(deal_text)

            if int(dealer_coise) == dealt_index:
                self.__console.clear()
                self.__console.print(f"[green]Good choise![/green] earned points: 1")
                time.sleep(GOOD_DELAY)
                self.__console.clear()

                if dealt_index == len(player_list) + 1:
                    done = True
                else:
                    player_list[dealt_index - 1].hit(self.__dealer.deal(self.__deck))
                    dealt_index += 1
                    cards_dealt += 1
                    
                    if cards_dealt == max_cards:
                        dealt_index == len(player_list) + 1
                    elif dealt_index == len(player_list) + 1:
                        dealt_index = 1

            else:
                self.__console.clear()
                if dealt_index != len(player_list) + 1:
                    self.__console.print(f"[red]Wrong choise![/red] you must deal the cards one by one in order {dealt_index} was the right choice, earned points: -1")
                    time.sleep(WRONG_DELAY)
                else:
                    self.__console.print(f"[red]Wrong choise![/red] everyone gets 2 cards, earned points: -1")
                    time.sleep(WRONG_DELAY)

                self.__console.clear()

    def get_totals(self) -> tuple[dict[str, int], str]:
        totals = {}

        self.__active_player_index = 0

        for i in range(len(self.__players)):
            player, playernum = (self.__players[self.__active_player_index], self.__active_player_index)
            totals[f"Player{playernum + 1}"] = [player.get_total(), player.get_bet()]
            self.next_player()

        totals["Dealer"] = self.__dealer.get_total()

        if len(totals.keys()) >= len(self.__players):
            totals_text = ""
            
            i = 1

            for key, val in totals.items():
                if "Player" in key:
                    totals_text += f"{i}. {key}: {val[0]} total card value, ${val[1]} bet size\n"
                else:
                    totals_text += f"{i}. {key}: {val} total card value\n"
        
                i += 1

            totals_text += f"{i}. done\n"

            return (totals, totals_text)

    def game_start(self, input: str) -> None:
        feedback = self.__dealer.shuffle_deck(input, self.__deck)
        self.__console.print(f"{feedback[0]}, earned points: {feedback[1]}")
        
        if feedback[1] > 0:
            time.sleep(GOOD_DELAY)
            self.__console.clear()
            self.__gamestate = gamestate.ROUND_START

        else:
            time.sleep(WRONG_DELAY)
            self.__console.clear()

    def round_start(self, input: int) -> None:
        if input == 1:
            self.__console.clear()
            self.__console.print(f"[red]Wrong choise![/red] first take the bets then deals the cards, earned points: -1")
            time.sleep(WRONG_DELAY)
            self.__console.clear()
        
        elif input == 2:
            self.__console.clear()
            self.__console.print(f"[green]Good choise![/green] earned points: 1")
            time.sleep(GOOD_DELAY)
            self.__console.clear()

            i = 1
            
            for player in self.__players:
                bet = player.det_bet()
                player.set_bet(bet)

                self.__chips += bet
                self.__console.print(f"Player{i} betted:{bet}")

                i += 1

            time.sleep(WRONG_DELAY)
            self.__console.clear()

            self.deal_cards_loop()
            self.__gamestate = gamestate.MAIN_LOOP

        else:
            self.__console.clear()
            self.__console.print(f"please enter 1 or 2")
            time.sleep(WRONG_DELAY)
            self.__console.clear()

    def main_loop(self) -> None:
        player, playernum = (self.__players[self.__active_player_index], self.__active_player_index)

        if self.__players[self.__active_player_index].allowed_play:
            action = player.det_action()
            self.__console.print(f"Player{playernum + 1}'s turn\nPlayer{playernum + 1} chooses [bold]{action.lower()}[/bold]\n")
            dealer_coise = self.__console.input('what do you do?\n\n1. give card\n2. nothing\n')
            self.__console.clear()

            match int(dealer_coise):
                case 1:
                    if action == actions.HIT.name:
                        feedback = ("[green]Good choise![/green]", 1)
                        self.next_move(actions.HIT)

                        if not player.allowed_play:
                            self.__bust += 1

                    else:
                        feedback = ("[red]Wrong choise![/red] When someone [bold]stand[/bold]s you should [bold]do nothing[/bold]", -1)
                        self.next_move(actions.STAND)
                        self.__bust += 1

                    self.__console.print(f"{feedback[0]}, earned points: {feedback[1]}")
                    
                    if feedback[1] > 0:
                        time.sleep(GOOD_DELAY)
                    else:
                        time.sleep(WRONG_DELAY)
        
                    self.__console.clear()

                case 2:
                    if action == actions.STAND.name:
                        feedback = ("[green]Good choise![/green]", 1)
                        self.next_move(actions.STAND)
                        self.__bust += 1

                    else:
                        feedback = ("[red]Wrong choise![/red] When someone [bold]hit[/bold]s you should [bold]give them a card[/bold]", -1)
                        self.next_move(actions.HIT)

                        if not player.allowed_play:
                            self.__bust += 1

                    self.__console.print(f"{feedback[0]}, earned points: {feedback[1]}")
                    
                    if feedback[1] > 0:
                        time.sleep(GOOD_DELAY)
                    else:
                        time.sleep(WRONG_DELAY)
                    
                    self.__console.clear()
        
        elif self.__bust >= len(self.__players):
            self.__gamestate = gamestate.ROUND_END

        else:
            self.next_player()
            
    def round_end(self) -> None:
        while self.__dealer_turn:
            dealer_coise = self.__console.input(f"Your turn!\ntotal:{self.__dealer.get_total()}\n\n1. hit\n2. stand\n")

            feedback = self.__dealer.dealer_turn(int(dealer_coise), self.__deck)

            self.__console.clear()
            self.__console.print(f"{feedback[0]}, earned points {feedback[1]}")
            
            if feedback[1] > 0:
                time.sleep(GOOD_DELAY)
                self.__dealer_turn = False
            else:
                time.sleep(WRONG_DELAY)

            self.__console.clear()

        totals, totals_text = self.get_totals()
        done = False
        sellist = []

        while not done:
            self.__console.print(totals_text)
            dealer_coise = self.__console.input(f"Who won? selected: {", ".join(sellist)}\n")
            self.__console.clear()

            feedback, sellist = self.__dealer.det_winner(totals, int(dealer_coise), sellist)

            if feedback:
                self.__console.print(f"{feedback[0]}, earned points {feedback[1]}")

                if feedback[1] > 0:
                    time.sleep(GOOD_DELAY)
                    done = True
                    sys.exit()
                    
                else:
                    time.sleep(WRONG_DELAY)
                    self.__console.clear()
                



