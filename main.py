# main imports
from enum import Enum, auto
from modules.dealer import Dealer
from modules.player import Player
from modules.deck import Deck
from modules.main_window import MainWindow
from modules.gamelogger import GameLogger

import sys

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

# main_window = MainWindow()
game_logger = GameLogger(players)
current_gamestate = gamestate.GAME_START

temp_bust = {

}

# will be added to game window later
while (running):
    match current_gamestate:
        case gamestate.GAME_START:
            deck.shuffle_deck()

            for i in range(2):
                for name, instance in players.items():
                    instance.hit(dealer.deal(deck))
            
            current_gamestate = gamestate.MAIN_LOOP
            
        case gamestate.MAIN_LOOP:
            for name, instance in players.items():
                if isinstance(instance, Dealer):
                    if instance.hand.can_play:
                        print(f"{name}'s turn\n\n")
                        print(f"Total: {instance.hand.total}\n\n")
                        print("1. hit")
                        print("2. fold\n")

                        choise = input(f"choose a action {name}:\n")

                        match int(choise):
                            case 1:
                                feedback = instance.hit(deck.hit())
                                game_logger.log(name, "Hit", instance.hand.total, feedback[0], feedback[1])
                            case 2:
                                feedback = instance.stand()
                                game_logger.log(name, "Stand", instance.hand.total, feedback[0], feedback[1])
                            case _:
                                print(f"choise not valid")
                    else:
                        if name not in temp_bust:
                            temp_bust[name] = "bust"
                            game_logger.log(name, "is bust", instance.hand.total)
                            print(f"{name} is bust or passed")

                elif isinstance(instance, Player):
                    print(f"{name}'s turn\n\n")
                    print(f"Total: {instance.get_total()}\n\n")

                    if instance.allowed_play:
                        if not instance.get_total() > 19:
                            print(f"{name} chooses hit")
                            instance.hit(deck.hit())
                            game_logger.log(name, "Hit", instance.get_total())

                        else:
                            instance.stand()
                            game_logger.log(name, "Stand", instance.get_total())

                    else:
                        if name not in temp_bust:
                            temp_bust[name] = "bust"
                            game_logger.log(name, "is bust", instance.get_total())
                            print(f"{name} is bust or passed")

            if len(temp_bust) > 3:
                current_gamestate = gamestate.GAME_END
        
        case gamestate.GAME_END:
            game_logger.write_log()
            evaluation = game_logger.evaluate_current_session()
            
            total_points = evaluation["dealer_points"]
            
            if total_points > 0:
                good_bad = "Good job!"
            else:
                good_bad = "please try better next time"

            print(f"you earned {total_points} points, {good_bad}")
            
            for action in evaluation["dealer_actions"]:
                eval_item = "_____________\n"
                
                for key, val in action.items():
                    eval_item += f"{key}:{val}\n"

                print(eval_item)

            sys.exit()