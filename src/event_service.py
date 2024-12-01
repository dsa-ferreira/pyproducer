import random
from src.utils.reflection import get_class_name

class EventServiceException(Exception):

    def __init__(self, msg):
        super().__init__(msg)

class EventService:

    def __init__(self, types: list):
        self.types = types
        self.is_last_dict = {}
        self.previous: dict[str, list] = {}
        self.current = None

    def is_last(self, event):
        event_check = self.is_last_dict.get(type(event).__name__)
        if event_check is not None:
            return event_check

        for tipe in self.types:
            if tipe != event:
                if tipe.dependencies and type(event).__name__ in tipe.dependencies:
                    return False
        return True

    def get_event_type(self):
        event = None
        while not event:
            index = random.randrange(0, len(self.types))
            ready = False
            evaluated = self.types[index]
            if not evaluated.dependencies:
                return evaluated

            for dep in evaluated.dependencies:
                if self.check_available(dep):
                    ready = True
                    self.pull(dep)
                    break
            event = self.types[index] if ready else None
        return event

    def push(self, event, payload):
        if self.is_last(event):
            return

        class_name = get_class_name(event)
        if self.previous.get(class_name) is None:
            self.previous[class_name] = []
        self.previous[class_name].append(payload)

    def check_available(self, class_name):
        class_list = self.previous.get(class_name)
        return class_list and len(class_list) > 0

    def pull(self, class_name):
        if not self.check_available(class_name):
            raise EventServiceException("Something went terribly wrong! (no dependency event available)")

        class_list: list = self.previous.get(class_name)
        self.current = class_list.pop()

    def get_attribute_from_curr(self, attribute_name):
        if self.current is None:
            raise EventServiceException("Something went terribly wrong! (no event pulled for use as dependency)")

        attribute = self.current.get(attribute_name)
        if attribute is None:
            raise EventServiceException(f"No attribute value available for {attribute_name}! Are you dependencies properly configured?")

        return attribute

    def clear_current(self):
        self.current = None
