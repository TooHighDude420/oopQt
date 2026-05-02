# main imports
from enum import Enum, auto
from modules.dealer import Dealer
from modules.player import Player
from modules.deck import Deck
from modules.main_window import MainWindow
from modules.gamelogger import GameLogger
from modules.table import Table, actions, gamestate

# nicer console
from rich.console import Console

import time
import sys


running = True

# main_window = MainWindow()
# game_logger = GameLogger(players)
table = Table(0, 3)
console = Console(color_system='truecolor')

# delay for clearing text
CLEAR_DELAY = 2

bust_list: list[str] = []

save_guard = 0

# will be added to game window later
while (running):
        match table.get_gamestate():
            case gamestate.GAME_START:
                # ask dealer to shuffle
                feedback = table.get_dealer().shuffle_deck(console, table.get_deck())
                console.print(f"{feedback[0]}, earned points: {feedback[1]}")
                time.sleep(CLEAR_DELAY)
                console.clear()

                if feedback[1] > 0:
                    table.set_gamestate(gamestate.ROUND_START)
            
            case gamestate.ROUND_START:
                dealer_coise = console.input("what to do next:\n\n1. Deal cards\n2. take bets\n")
                
                if int(dealer_coise) == 2:
                    console.clear()
                    console.print(f"[green]Good choise![/green] earned points: 1")
                    time.sleep(CLEAR_DELAY)
                    console.clear()

                    i = 0
                    
                    for player in table.get_players():
                        bet = player.det_bet()
                        player.set_bet(bet)

                        table.add_bet(bet)
                        console.print(f"Player{i + 1} betted:{bet}")

                        i += 1

                    time.sleep(CLEAR_DELAY)
                    console.clear()

                    done = False
                    cards_dealt = 0

                    while not done:
                        if (cards_dealt == table.get_player_count() * 2):
                            done = True
                            table.set_gamestate(gamestate.MAIN_LOOP)

                        else:
                            ii = 0

                            totals_dict: dict[str, int] = {}
                            totals_text = ""

                            correct_player, correct_player_num = table.get_active_player()

                            for player in table.get_players():
                                totals_dict[f"Player{ii + 1}"] = player.get_num_cards()
                                ii += 1

                            for key, val in totals_dict.items():
                                totals_text += f"{key}: {val} Cards\n"

                            console.print(totals_text)

                            deal_text = "\nwho do you give a card:\n"

                            for iii in range(table.get_player_count()):
                                deal_text += f"\n{iii + 1}. Player{iii + 1}"

                            deal_text += "\n"

                            dealer_coise = console.input(deal_text)

                            if int(dealer_coise) != correct_player_num + 1:
                                console.clear()
                                console.print(f"[red]Wrong choise![/red] you must deal the cards one by one Player{correct_player_num} must get a card, earned points: -1")
                                time.sleep(CLEAR_DELAY)
                                console.clear()
                            else:
                                console.clear()
                                console.print(f"[green]Good choise![/green] earned points: 1")
                                time.sleep(CLEAR_DELAY)
                                console.clear()
                                correct_player.hit(table.get_dealer().deal(table.get_deck()))
                                table.next_player()
                                cards_dealt += 1

                        # table.set_gamestate(gamestate.MAIN_LOOP)

                elif int(dealer_coise) == 1:
                    console.clear()
                    console.print(f"[red]Wrong choise![/red] first take the bets then deals the cards, earned points: -1")
                    time.sleep(CLEAR_DELAY)
                    console.clear()

            case gamestate.MAIN_LOOP:
                player, playernum = table.get_active_player()
                
                if player.allowed_play:
                    action = player.det_action()

                    console.print(f"Player{playernum + 1}'s turn\nPlayer{playernum + 1} chooses [bold]{action.lower()}[/bold]\n")
                    dealer_coise = console.input('what do you do?\n\n1. give card\n2. nothing\n')
                    console.clear()

                    match int(dealer_coise):
                        case 1:
                            if action == actions.HIT.name:
                                feedback = ("[green]Good choise![/green]", 1)
                                bust = table.next_move(actions.HIT)

                                if bust:
                                    bust_list.append(f"Player{playernum + 1}")
                                    table.next_player()

                            else:
                                feedback = ("[red]Wrong choise![/red] When someone [bold]stand[/bold]s you should [bold]do nothing[/bold]", -1)
                                table.next_move(actions.STAND)

                            console.print(f"{feedback[0]}, earned points: {feedback[1]}")
                            time.sleep(CLEAR_DELAY)
                            console.clear()

                        case 2:
                            if action == actions.STAND.name:
                                feedback = ("[green]Good choise![/green]", 1)
                                table.next_move(actions.STAND)

                            else:
                                feedback = ("[red]Wrong choise![/red] When someone [bold]hit[/bold]s you should [bold]give them a card[/bold]", -1)
                                bust = table.next_move(actions.HIT)

                                if bust:
                                    bust_list.append(f"Player{playernum + 1}")
                                    table.next_player()

                            console.print(f"{feedback[0]}, earned points: {feedback[1]}")
                            time.sleep(CLEAR_DELAY)
                            console.clear()
                
                elif f"Player{playernum + 1}" not in bust_list:
                    bust_list.append(f"Player{playernum + 1}")
                    table.next_player()
                
                elif f"Player{playernum + 1}" in bust_list:
                    table.next_player()

                if len(bust_list) >= table.get_player_count():
                    table.set_gamestate(gamestate.ROUND_END)

            case gamestate.ROUND_END:
                totals = {}
                
                for i in range(table.get_player_count()):
                    player, playernum = table.get_active_player()
                    totals[f"Player{playernum + 1}"] = player.get_total()
                    table.next_player()

                if len(totals.keys()) >= table.get_player_count():
                    totals_text = ""
                    
                    i = 1

                    for key, val in totals.items():
                        totals_text += f"{i}. {key}: {val} total card value\n"
                        i += 1

                    console.print(totals_text)
                    sys.exit()


# match current_gamestate:
#     case gamestate.GAME_START:
#         deck.shuffle_deck()

#         for i in range(2):
#             for name, instance in players.items():
#                 instance.hit(dealer.deal(deck))
        
#         current_gamestate = gamestate.MAIN_LOOP
        
#     case gamestate.MAIN_LOOP:
#         for name, instance in players.items():
#             if isinstance(instance, Dealer):
#                 if instance.hand.can_play:
#                     print(f"{name}'s turn\n\n")
#                     print(f"Total: {instance.hand.total}\n\n")
#                     print("1. hit")
#                     print("2. fold\n")

#                     choise = input(f"choose a action {name}:\n")

#                     match int(choise):
#                         case 1:
#                             feedback = instance.hit(deck.hit())
#                             game_logger.log(name, "Hit", instance.hand.total, feedback[0], feedback[1])
#                         case 2:
#                             feedback = instance.stand()
#                             game_logger.log(name, "Stand", instance.hand.total, feedback[0], feedback[1])
#                         case _:
#                             print(f"choise not valid")
#                 else:
#                     if name not in temp_bust:
#                         temp_bust[name] = "bust"
#                         game_logger.log(name, "is bust", instance.hand.total)
#                         print(f"{name} is bust or passed")

#             elif isinstance(instance, Player):
#                 print(f"{name}'s turn\n\n")
#                 print(f"Total: {instance.get_total()}\n\n")

#                 if instance.allowed_play:
#                     if not instance.get_total() > 19:
#                         print(f"{name} chooses hit")
#                         instance.hit(deck.hit())
#                         game_logger.log(name, "Hit", instance.get_total())

#                     else:
#                         instance.stand()
#                         game_logger.log(name, "Stand", instance.get_total())

#                 else:
#                     if name not in temp_bust:
#                         temp_bust[name] = "bust"
#                         game_logger.log(name, "is bust", instance.get_total())
#                         print(f"{name} is bust or passed")

#         if len(temp_bust) > 3:
#             current_gamestate = gamestate.GAME_END
    
#     case gamestate.GAME_END:
#         game_logger.write_log()
#         evaluation = game_logger.evaluate_current_session()
        
#         total_points = evaluation["dealer_points"]
        
#         if total_points > 0:
#             good_bad = "Good job!"
#         else:
#             good_bad = "please try better next time"

#         print(f"you earned {total_points} points, {good_bad}")
        
#         for action in evaluation["dealer_actions"]:
#             eval_item = "_____________\n"
            
#             for key, val in action.items():
#                 eval_item += f"{key}:{val}\n"

#             print(eval_item)

#         sys.exit()