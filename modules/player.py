from .hand import Hand
from .card import Card

class Player():
    def __init__(self, chips:int):
        self.__hands:list[Hand] = [Hand()]
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

<<<<<<< Updated upstream
    def place_bets(self, amount:int):
        return NotImplementedError("place_bet is not implemented")

    def reset(self):
=======
    def place_bets(self, amount:int) -> int:
            self.__chips -= amount
            return amount

    def det_bet(self) -> int:
        return random.randrange(self.__chips)
    
    def set_bet(self, amount: int) -> None:
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
>>>>>>> Stashed changes
        return NotImplementedError("reset is not implemented")