import sys
import time

from .shoe import Shoe
from .dealer import Dealer
from .player import Player
from .deck import Deck

from enum import Enum, auto
from rich.console import Console
from modules.gamelogger import GameLogger

class gamestate(Enum):
    GAME_START = 0
    ROUND_START = auto()
    MAIN_LOOP = auto()
    ROUND_END = auto()
    GAME_END = auto()

# delay for clearing text
WRONG_DELAY = 4
GOOD_DELAY = 1

ACTIONS = [
    "HIT",
    "STAND"
]

class Table:
    def __init__(self, amount_of_players:int, console: Console) -> Table:
        self.__dealer: Dealer = Dealer()
        self.__console = console
        self.__gamelogger: GameLogger = GameLogger()
        self.__players: list[Player] = [Player(500) for player in range(amount_of_players)]
        self.__gamestate: gamestate = gamestate.GAME_START
        self.__chips: int = 0
        self.__possible_points: int = 0
        self.__active_player_index: int = 0
        self.__deck: Deck = Deck()
        self.__bust: int = 0
        self.__dealer_turn = True

    def get_gamestate(self) -> gamestate:
        return self.__gamestate

    def next_player(self) -> None:
        if self.__active_player_index == len(self.__players) -1:
            self.__active_player_index = 0
        else:
            self.__active_player_index += 1

    def next_move(self, input: str) -> None:
        if input not in ACTIONS:
            raise ValueError("not a valid action")
        else:
            player = self.__players[self.__active_player_index]

            match input:
                case "HIT":
                    player.hit(self.__dealer.deal(self.__deck))

                case "STAND":
                    player.stand()
                    self.next_player()

    def deal_cards_loop(self) -> None:
        done = False
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
            feedback = self.__dealer.give_cards(int(dealer_coise), max_cards, ii, player_list, self.__deck)

            if feedback:
                self.__console.clear()
                self.__console.print(f"{feedback[0]}, earned points: {feedback[1]}")

                if feedback[1] > 0:
                    time.sleep(GOOD_DELAY)
                    self.__console.clear()
                    done = True
                else:
                    time.sleep(WRONG_DELAY)
                    self.__console.clear()
            else:
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
        self.__gamelogger.log("Dealer", "shuffle", feedback[0], feedback[1])
        self.__console.print(f"{feedback[0]}, earned points: {feedback[1]}")
        
        if feedback[1] > 0:
            time.sleep(GOOD_DELAY)
            self.__console.clear()
            self.__possible_points += 1
            self.__gamestate = gamestate.ROUND_START

        else:
            time.sleep(WRONG_DELAY)
            self.__console.clear()

    def round_start(self, input: int) -> None:
        feedback = self.__dealer.deal_cards_choise(input)

        self.__console.clear()
        self.__console.print(f"{feedback[0]}, earned points: {feedback[1]}")
        self.__gamelogger.log("Dealer", "Deal cards choise",  feedback[0], feedback[1])

        if feedback[1] > 0:
            time.sleep(GOOD_DELAY)
            
            self.__console.clear()
            self.__possible_points += 1

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
            time.sleep(WRONG_DELAY)

    def main_loop(self) -> None:
        player, playernum = (self.__players[self.__active_player_index], self.__active_player_index)

        if self.__players[self.__active_player_index].allowed_play:
            action = player.det_action()
            self.__console.print(f"Player{playernum + 1}'s turn\nPlayer{playernum + 1} chooses [bold]{action.lower()}[/bold]\n")
            dealer_coise = self.__console.input('what do you do?\n\n1. give card\n2. nothing\n')
            self.__console.clear()

            feedback = self.__dealer.player_turn(int(dealer_coise), action, player)
            self.next_move(action)

            self.__console.print(f"{feedback[0]}, point earned {feedback[1]}")
            self.__gamelogger.log("Dealer", f"Player{playernum}'s turn",  feedback[0], feedback[1])

            if feedback[1] > 0:
                time.sleep(GOOD_DELAY)
                self.__possible_points += 1

            else:
                time.sleep(WRONG_DELAY)
                
            self.__console.clear()

            if not player.allowed_play:
                self.__bust += 1
        
        elif self.__bust >= len(self.__players):
            self.__gamestate = gamestate.ROUND_END

        else:
            self.next_player()
            
    def round_end(self) -> None:
        while self.__dealer_turn:
            dealer_coise = self.__console.input(f"Your turn!\ntotal:{self.__dealer.get_total()}\n\n1. hit\n2. stand\n")
            feedback = self.__dealer.dealer_turn(int(dealer_coise), self.__deck)

            if feedback:
                self.__console.clear()
                self.__console.print(f"{feedback[0]}, earned points {feedback[1]}")
                self.__gamelogger.log("Dealer", "Dealers turn", feedback[0], feedback[1])
                
                if feedback[1] > 0:
                    time.sleep(GOOD_DELAY)
                    self.__possible_points += 1
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
                self.__gamelogger.log("Dealer", "Dealers turn",  feedback[0], feedback[1])

                if feedback[1] > 0:
                    time.sleep(GOOD_DELAY)
                    self.__console.clear()
                    self.__possible_points += 1
                    done = True
                    self.__gamelogger.write_log()

                    self.__console.print(f"Your earned {self.__gamelogger.get_points()} points of possible {self.__possible_points}\n")
                    grade = self.__gamelogger.get_points() / self.__possible_points * 10
                    self.__console.print(f"your final grade:{grade}")

                    if grade > 6:
                        self.__console.print("good job!")
                        time.sleep(WRONG_DELAY)

                    else:
                        self.__console.print("try better next time")
                        time.sleep(WRONG_DELAY)
                        
                    sys.exit()
                    
                else:
                    time.sleep(WRONG_DELAY)
                    self.__console.clear()