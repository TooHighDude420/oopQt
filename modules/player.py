from .hand import Hand
from .card import Card

import random

class Player():
    def __init__(self, chips:int):
        self.__hands:list[Hand] = []
        self.__hands.append(Hand())
        self.__chips:int = chips
        self.__current_bet: int
        self.allowed_play:bool = True

    def hit(self, card: Card) -> None:
        self.__hands[0].hit(card)

        if not self.__hands[0].can_play:
            self.allowed_play = False

    def stand(self) -> None:
        self.__hands[0].stand()
        self.allowed_play = False

    def get_total(self) -> int:
        return self.__hands[0].get_total()
    
    def get_num_cards(self) -> int:
        return self.__hands[0].get_num_cards()
    
    def update_chips(self, increment:int) -> None:
        self.__chips = max(0, self.__chips + increment)

    def place_bets(self, amount:int):
        if amount > self.__chips:
            return ValueError("bet can't be higher then held chips")
        else:
            self.__chips -= amount
            return amount

    def det_bet(self) -> int:
        return random.randrange(self.__chips)
    
    def set_bet(self, amount: int):
        self.__current_bet = amount

    def get_bet(self) -> int:
        return self.__current_bet

    def det_action(self) -> str:
        if self.__hands[0].get_total() >= 18:
            return 'STAND'
        else:
            return 'HIT'
        
    def get_passed(self) -> bool:
        return self.__hands[0].get_passed()

    def reset(self) -> None:
        return NotImplementedError("reset is not implemented")