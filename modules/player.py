from .hand import Hand
from .card import Card

class Player():
    def __init__(self, chips:int):
        self.__hands:list[Hand] = []
        self.__hands.append(Hand())
        self.__chips:int = chips
        self.allowed_play:bool = True

    def hit(self, card: Card) -> None:
        self.__hands[0].hit(card)

        if self.__hands[0].total > 21:
            self.allowed_play = False

    def stand(self) -> None:
        self.__hands[0].stand()
        self.allowed_play = False

    def get_total(self) -> int:
        return self.__hands[0].total

    def place_bets(self, amount:int):
        return NotImplementedError("place_bet is not implemented")

    def reset(self):
        return NotImplementedError("reset is not implemented")