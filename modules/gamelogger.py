import json
import datetime

from pathlib import Path
from typing import TYPE_CHECKING
from typing import TypedDict


# for type hinting
if TYPE_CHECKING:
    from .player import Player

class ActionLog(TypedDict):
    time:str
    player_name:str
    action:str

class LogContent(TypedDict):
    date: str
    action_log: list[ActionLog]

LOGS_DIR = Path(__file__).parent.parent / "logs"

class GameLogger:
    def cal_gameid(self) -> int:
        if not LOGS_DIR.exists():
            LOGS_DIR.mkdir(parents=True, exist_ok=True)
            id = 0
        elif LOGS_DIR.exists():
            id = 0
            
            for i in range(len(list(LOGS_DIR.iterdir()))):
                id = i
        
        return id

    def __init__(self, players: dict[str, Player]) -> None:
        # self.datetime = datetime()
        self.points:int = 0

        self.__game_id:int = self.cal_gameid()
        self.__players:dict[str, Player] = players
        self.__current_log = LOGS_DIR / f"session_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}.json"

        if not self.__current_log.exists():
            self.__log_content: LogContent = {
                "date": datetime.datetime.now().date().isoformat(),
                "action_log":[

                ]
            }

        else:
            with open(self.__current_log, mode='r') as log:
                self.__log_content = json.loads(log.read())

    def log(self, player_name:str, action:str, hand_value:int, feedback:str | None):
        self.__log_content["action_log"].append({
            "time":datetime.datetime.now().time().strftime("%H:%M:%S"),
            "player_name":player_name,
            "hand_value":hand_value,
            "feedback":feedback,
            "action":action
        })

    def write_log(self):
        if not self.__current_log.exists():
            with open(self.__current_log, mode='w') as log:
                log.write(json.dumps(self.__log_content))
        else:
            with open(self.__current_log, mode='r') as handle:
                current_fc = json.loads(handle.read())

            if current_fc is not self.__current_log:
                with open(self.__current_log, mode='w') as log:
                    log.write(json.dumps(self.__log_content))