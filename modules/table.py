from .shoe import Shoe
from .dealer import Dealer
from .player import Player
from .deck import Deck

from enum import Enum, auto

class gamestate(Enum):
    GAME_START = 0
    ROUND_START = auto()
    MAIN_LOOP = auto()
    ROUND_END = auto()
    GAME_END = auto()

class actions(Enum):
    HIT = 1
    STAND = auto()

class Table:
    def __init__(self, shoe_size:int, amount_of_players:int) -> Table:
        self.__dealer: Dealer = Dealer()

        # list comprehension
        self.__players: list[Player] = [Player(500) for player in range(amount_of_players)]
        self.__gamestate: gamestate = gamestate.GAME_START
        self.__chips: int = 0
        self.__points: int = 0
        self.__active_player_index: int = 0
        self.__deck: Deck = Deck()

        # tmp_deck_list: list[Deck] = [Deck() for shoe in range(shoe_size)]
        
        # self.__shoe: Shoe = Shoe(tmp_deck_list)


    def get_gamestate(self) -> gamestate:
        return self.__gamestate
    
    def set_gamestate(self, new_state:gamestate):
        self.__gamestate = new_state
    
    def get_active_player(self) -> tuple[Player, int]:
        return (self.__players[self.__active_player_index], self.__active_player_index)
    
    def get_players(self) -> list[Player]:
        return self.__players
    
    def get_player_count(self) -> int:
        return len(self.__players)
    
    def get_dealer(self) -> Dealer:
        return self.__dealer
    
    def get_deck(self) -> Deck:
        return self.__deck

    def next_player(self) -> None:
        if self.__active_player_index == len(self.__players) -1:
            self.__active_player_index = 0
        else:
            self.__active_player_index += 1

    def add_bet(self, amount:int) -> None:
        self.__chips += amount

    def next_move(self, input: actions) -> None | bool:
        if input not in actions:
            raise ValueError("not a valid action")
        else:
            match input:
                case actions.HIT:
                    bust = self.get_active_player()[0].hit(self.__dealer.deal(self.__deck))

                    if bust:
                        return bust

                case actions.STAND:
                    self.get_active_player()[0].stand()
                    self.next_player()
