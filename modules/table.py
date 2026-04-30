from modules.shoe import Shoe
from modules.dealer import Dealer
from modules.player import Player

from enum import Enum, auto

class gamestate(Enum):
    GAME_START = 0
    MAIN_LOOP = auto()
    GAME_END = auto()

class Table:
    def __init__(self, shoe_size:int, amount_of_players:int) -> Table:
        self.__shoe = Shoe()
        self.__dealer = Dealer()

        # list comprehension
        self.__players: list[Player] = [Player() for player in range(len(amount_of_players))]
        self.__gamestate = gamestate
        self.__chips = 0
        self.__points = 0
        self.__active_player_index = 0

    def next_move(input: str) -> None:
        pass