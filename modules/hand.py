from .card import Card

class Hand():
    def __init__(self):
        self.can_play:bool = True
        self.total:int = 0
        self.__cards: list[Card] = []
        self.__has_passed:bool = False

    def hit(self, card: Card) -> bool:
        self.total += card.value
        self.__cards.append(card)

        if self.total > 21:
            self.can_play = False
            return True

        return False 

    def stand(self) -> None:
        self.__has_passed = True
        self.can_play = False