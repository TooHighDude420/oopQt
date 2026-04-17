# main imports
from enum import Enum, auto
from modules.dealer import Dealer
from modules.player import Player
from modules.deck import Deck
from modules.main_window import MainWindow

# debug imports
import datetime

# ui widgets

class gamestate(Enum):
    GAME_START = 0
    MAIN_LOOP = auto()
    GAME_END = auto()

dealer = Dealer()
deck = Deck()
running = True

players = {
    "dealer": dealer,
    "player one": Player(1),
    "player two": Player(1),
    "player three": Player(1)
    }

main_window = MainWindow()

current_gamestate = gamestate.GAME_START

# will be added to game window later
while (running):
    match current_gamestate:
        case gamestate.GAME_START:
            print(f"[DEBUG][{datetime.datetime.now()}] showing main menu")
            deck.shuffle_deck()
            for i in range(2):
                for name, instance in players.items():
                    instance.hit(dealer.deal(deck))
            
            current_gamestate = gamestate.MAIN_LOOP
            
        case gamestate.MAIN_LOOP:
            for name, instance in players.items():
                    if instance.hand.can_play:
                        print(f"{name}'s turn\n\n")
                        print(f"Total: {instance.hand.total}\n\n")
                        print("1. hit")
                        print("2. fold\n")

                        choise = input(f"choose a action {name}:\n")

                        match int(choise):
                            case 1:
                                instance.hit(deck.hit())
                            case 2:
                                instance.stand()
                            case _:
                                print(f"choise not valid")
                    else:
                        print(f"{name} is bust or passed")

