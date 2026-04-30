from modules.deck import Deck

class Shoe:
    def __init__(self, decks: list[Deck]):
        self.__decks = decks

    def shuffle(self) -> None:
        return NotImplementedError("suffle for shoe not implemented")
    
    def draw(self) -> None:
        return NotImplementedError("draw for shoe not implemented")