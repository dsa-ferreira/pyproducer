
from src.datatypes import Datatype


class EventBase:

    def __init__(self, payload: Datatype, topic: str = "", weight: int = 1):
        self.payload = payload
        self.topic = topic
        self.weight = weight

    def apply(self):
        return self.payload.apply()

