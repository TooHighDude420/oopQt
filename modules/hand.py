from .card import Card

class Hand():
    def __init__(self):
        self.can_play:bool = True
        self.__total:int = 0
        self.__cards: list[Card] = []
        self.__has_passed:bool = False

    def hit(self, card: Card) -> None:
        self.__add_to_total(card)
        self.__cards.append(card)

        if self.get_total() > 21:
            self.can_play = False
    
    def get_total(self) -> int:
        temp_total = self.__total

        for card in self.__cards:
            if card.get_value() == "ace" and temp_total > 21:
                temp_total -= 10

        return temp_total

    def __add_to_total(self, card: Card) -> None:
        if card.get_value() == "ace":
            self.__total += 11
        elif card.value > 10:
            self.__total += 10
        else:
            self.__total += card.value
    
    def stand(self) -> None:
        self.__has_passed = True
        self.can_play = False

    def get_passed(self) -> bool:
        return self.__has_passed

    def get_num_cards(self) -> int:
        return len(self.__cards)