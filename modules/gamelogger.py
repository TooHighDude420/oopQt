import json
import datetime

from pathlib import Path
from typing import TypedDict

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
    def __init__(self) -> None:
        self.__current_log: Path = LOGS_DIR / f"session_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}.json"

        if not self.__current_log.exists():
            self.__log_content: LogContent = {
                "date": datetime.datetime.now().date().isoformat(),
                "dealer_points":0,
                "action_log":[]
            }

        else:
            with open(self.__current_log, mode='r') as log:
                self.__log_content = json.loads(log.read())

    def get_points(self):
        return self.__log_content["dealer_points"]

    def log(self, player_name:str, action:str, feedback:str, points: int) -> None:
        if points is not None:
            self.__log_content["dealer_points"] += points

        self.__log_content["action_log"].append({
            "time":datetime.datetime.now().time().strftime("%H:%M:%S"),
            "player_name":player_name,
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