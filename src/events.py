from src.datatypes import Datatype

class EventValidationException(Exception):
    def __init__(self, msg):
        super().__init__(msg)

    

def event(cls):

    def apply(self):
        return self.payload.apply()

    if not getattr(cls, "payload", False):
        raise EventValidationException("No payload defined")
    if not isinstance(cls.payload, Datatype):
        raise EventValidationException("Payload is not a Datatype")
    if not getattr(cls, "topic", False):
        cls.topic = ""

    cls.apply = apply
    cls.is_event = True
    return cls
