from .card import Card

class Hand():
    def __init__(self):
        self.can_play = True
        self.total = 0
        self.__cards = []
        self.__has_passed = False

    