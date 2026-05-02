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
WRONG_DELAY = 4
GOOD_DELAY = 1

bust_list: list[str] = []
save_guard = 0

# will be added to game window later
while (running):
    match table.get_gamestate():
        case gamestate.GAME_START:
            # ask dealer to shuffle
            feedback = table.get_dealer().shuffle_deck(console, table.get_deck())
            console.print(f"{feedback[0]}, earned points: {feedback[1]}")
            
            if feedback[1] > 0:
                time.sleep(GOOD_DELAY)
                console.clear()
                table.set_gamestate(gamestate.ROUND_START)

            else:
                time.sleep(WRONG_DELAY)
                console.clear()
        
        case gamestate.ROUND_START:
            dealer_coise = console.input("what to do next:\n\n1. Deal cards\n2. take bets\n")
            
            if int(dealer_coise) == 2:
                console.clear()
                console.print(f"[green]Good choise![/green] earned points: 1")
                time.sleep(GOOD_DELAY)
                console.clear()

                i = 0
                
                for player in table.get_players():
                    bet = player.det_bet()
                    player.set_bet(bet)

                    table.add_bet(bet)
                    console.print(f"Player{i + 1} betted:{bet}")

                    i += 1

                time.sleep(WRONG_DELAY)
                console.clear()

                done = False
                cards_dealt = 0
                dealt_index = 1

                player_list: list[Player|Dealer] = [p for p in table.get_players()]
                player_list.append(table.get_dealer())

                max_cards = len(player_list) * 2

                while not done:
                    ii = 1

                    totals_dict: dict[str, int] = {}
                    totals_text = ""

                    for p in player_list:
                        if isinstance(p, Player):
                            totals_text += f"Player{ii}: {p.get_num_cards()}\n"
                        elif isinstance(p, Dealer):
                            totals_text += f"Dealer: {p.get_num_cards()}\n"

                        ii += 1

                    console.print(totals_text)

                    deal_text = "\nwho do you give a card:\n"

                    ii = 1

                    for player in player_list:
                        if isinstance(player, Player):
                            deal_text +=  f"\n{ii}. Player{ii}"
                        elif isinstance(player, Dealer):
                            deal_text +=  f"\n{ii}. Dealer"
                    
                        ii += 1

                    deal_text += f"\n{ii}. Done dealing cards\n"
                    dealer_coise = console.input(deal_text)

                    if int(dealer_coise) == dealt_index:
                        console.clear()
                        console.print(f"[green]Good choise![/green] earned points: 1")
                        time.sleep(GOOD_DELAY)
                        console.clear()

                        if dealt_index == len(player_list) + 1:
                            done = True
                        else:
                            player_list[dealt_index - 1].hit(table.get_dealer().deal(table.get_deck()))
                            dealt_index += 1
                            cards_dealt += 1
                            
                            if cards_dealt == max_cards:
                                dealt_index == len(player_list) + 1
                            elif dealt_index == len(player_list) + 1:
                                dealt_index = 1

                    else:
                        console.clear()
                        if dealt_index != len(player_list) + 1:
                            console.print(f"[red]Wrong choise![/red] you must deal the cards one by one in order {dealt_index} was the right choice, earned points: -1")
                            time.sleep(WRONG_DELAY)
                        else:
                            console.print(f"[red]Wrong choise![/red] everyone gets 2 cards, earned points: -1")
                            time.sleep(WRONG_DELAY)

                        console.clear()

                table.set_gamestate(gamestate.MAIN_LOOP)

            elif int(dealer_coise) == 1:
                console.clear()
                console.print(f"[red]Wrong choise![/red] first take the bets then deals the cards, earned points: -1")
                time.sleep(WRONG_DELAY)
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
                        
                        if feedback[1] > 0:
                            time.sleep(GOOD_DELAY)
                        else:
                            time.sleep(WRONG_DELAY)
            
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
                        
                        if feedback[1] > 0:
                            time.sleep(GOOD_DELAY)
                        else:
                            time.sleep(WRONG_DELAY)
                        
                        console.clear()
            
            elif f"Player{playernum + 1}" not in bust_list:
                bust_list.append(f"Player{playernum + 1}")
                table.next_player()
            
            elif f"Player{playernum + 1}" in bust_list:
                table.next_player()

            if len(bust_list) >= table.get_player_count():
                table.set_gamestate(gamestate.ROUND_END)

        case gamestate.ROUND_END:
            while table.get_dealer().hand.can_play:
                dealer_coise = console.input(f"Your turn!\ntotal:{table.get_dealer().hand.total}\n\n1. hit\n2. stand\n")
            
                match int(dealer_coise):
                    case 1:
                        feedback = table.get_dealer().hit(table.get_dealer().deal(table.get_deck()))
                        console.clear()
                        console.print(f"{feedback[0]}, earned points {feedback[1]}")
                        
                        if feedback[1] > 0:
                            time.sleep(GOOD_DELAY)
                        else:
                            time.sleep(WRONG_DELAY)

                        console.clear()

                    
                    case 2:
                        feedback = table.get_dealer().stand()
                        console.clear()
                        console.print(f"{feedback[0]}, earned points {feedback[1]}")
                        if feedback[1] > 0:
                            time.sleep(GOOD_DELAY)
                        else:
                            time.sleep(WRONG_DELAY)

                        console.clear()

            totals = {}
            
            for i in range(table.get_player_count()):
                player, playernum = table.get_active_player()
                totals[f"Player{playernum + 1}"] = [player.get_total(), player.get_bet()]
                table.next_player()

            totals["Dealer"] = table.get_dealer().hand.total

            if len(totals.keys()) >= table.get_player_count():
                totals_text = ""
                
                i = 1

                for key, val in totals.items():
                    if "Player" in key:
                        totals_text += f"{i}. {key}: {val[0]} total card value, ${val[1]} bet size\n"
                    else:
                        totals_text += f"{i}. {key}: {val} total card value\n"
            
                    i += 1

                console.print(totals_text)

                # todo add pay-out
                ## reipmplement gamelogger
                
                sys.exit()

