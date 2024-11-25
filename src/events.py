
from src.datatypes import Datatype


class EventBase:

    def __init__(self, payload: Datatype, weight: int = 1):
        if payload is None:
            raise Exception
        self.payload = payload
        self.weight = weight

    def apply(self):
        return self.payload.apply()

