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
    hand_value:str
    feedback:str
    action:str

class LogContent(TypedDict):
    date: str
    dealer_points:int
    action_log: list[ActionLog]

class EvaluationActionContent(TypedDict):
    hand_value: int
    feedback: str | None
    action: str

class EvaluationContent(TypedDict):
    dealer_points: int
    dealer_actions: list[EvaluationActionContent]

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
                "dealer_points":0,
                "action_log":[

                ]
            }

        else:
            with open(self.__current_log, mode='r') as log:
                self.__log_content = json.loads(log.read())

    def log(self, player_name:str, action:str, hand_value:int, feedback:str | None = None, points: str | None = None) -> None:
        if points is not None:
            self.__log_content["dealer_points"] += points

        self.__log_content["action_log"].append({
            "time":datetime.datetime.now().time().strftime("%H:%M:%S"),
            "player_name":player_name,
            "hand_value":hand_value,
            "feedback":feedback,
            "action":action
        })

    def write_log(self) -> None:
        if not self.__current_log.exists():
            with open(self.__current_log, mode='w') as log:
                log.write(json.dumps(self.__log_content))
        else:
            with open(self.__current_log, mode='r') as handle:
                current_fc = json.loads(handle.read())

            if current_fc is not self.__current_log:
                with open(self.__current_log, mode='w') as log:
                    log.write(json.dumps(self.__log_content))

    def evaluate_current_session(self) -> EvaluationContent:
        tmpdict: EvaluationContent = {}

        tmpdict["dealer_points"] = self.__log_content["dealer_points"]
        tmpdict["dealer_actions"] = []

        for log_item in self.__log_content["action_log"]:
            if log_item["player_name"] == "dealer":
                reldict = {}
                
                for key, val in log_item.items():
                    if key != "player_name" and key != "time":
                        reldict[key] = val

                tmpdict["dealer_actions"].append(reldict)

        return tmpdict