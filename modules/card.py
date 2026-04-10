from enum import Enum, auto

class Suits(Enum):
    Hearts = 0
    Diamonds = auto()
    Clubs = auto()
    Spades = auto()

class Values(Enum):
    Ace = 1
    Two = auto()
    Three = auto()
    Four = auto()
    Five = auto()
    Six = auto()
    Seven = auto()
    Eight = auto()
    Nine = auto()
    Ten = auto()
    Jack = auto()
    Queen = auto()
    King = auto()

class Card:
    def __init__(self, suit:Suits, value:Values):
        self.__suit = suit.name
        self.__value = value
        self.value = value.value
        
    def __str__(self):
        return f"{self.__value.name} of {self.__suit}"