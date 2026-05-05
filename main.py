# main imports
import time

from rich.console import Console
from modules.table import Table, gamestate

running = True
console = Console(color_system='truecolor')
table = Table(3, console)

while (running):
    match table.get_gamestate():
        case gamestate.GAME_START:
            shuffle = console.input("shuffle deck?, y/n\n")
            console.clear()            
            table.game_start(shuffle.lower())
        
        case gamestate.ROUND_START:
            try:
                dealer_coise = console.input("what to do next:\n\n1. Deal cards\n2. take bets\n")
                table.round_start(int(dealer_coise))
            except ValueError:
                console.print("please enter 1 or 2")
                time.sleep(2)
                console.clear()

        case gamestate.MAIN_LOOP:
            table.main_loop()

        case gamestate.ROUND_END:
            table.round_end()