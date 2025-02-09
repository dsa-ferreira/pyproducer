from datetime import datetime, timezone
from typing import Callable, Any, Dict
import re
import rstr
import random
import uuid

from src.event_service import EventService

class UnsupportedUUIDVersion(Exception):

    def __init__(self ):
        super().__init__(f'unsupported uuid version')

class NotDatatypeError(Exception):

    def __init__(self, field_name):
        super().__init__(f'field {field_name} does not extend the Datatype class')
        self.field_name = field_name

class Datatype:

    def apply(self, event_service: EventService) -> Any:
        raise Exception

class PrevDatatype(Datatype):

    def __init__(self, field_name: Any):
        self.field_name = field_name

    def apply(self, event_service: EventService) -> Any:
        return event_service.get_attribute_from_curr(self.field_name)

class IncreasingNumbericDatatype(Datatype):

    def __init__(self, field_name: Any, max = 1000000000, step: int = 1):
        self.field_name = field_name
        self.max = max
        self.step = step

    def apply(self, event_service: EventService) -> Any:
        prev_value = event_service.get_attribute_from_curr(self.field_name)
        if isinstance(prev_value, int) and not isinstance(prev_value, bool):
            return random.randrange(prev_value, self.max, self.step)
        raise Exception("Referenced field was not numeric")

class DecreasingNumbericDatatype(Datatype):

    def __init__(self, field_name: Any, min = 0, step: int = 1):
        self.field_name = field_name
        self.min = min
        self.step = step

    def apply(self, event_service: EventService) -> Any:
        prev_value = event_service.get_attribute_from_curr(self.field_name)
        if isinstance(prev_value, int) and not isinstance(prev_value, bool):
            return random.randrange(self.min, prev_value, self.step)
        raise Exception("Referenced field was not numeric")

class ConstDatatype(Datatype):

    def __init__(self, value: Any):
        self.value = value

    def apply(self, event_service: EventService) -> Any:
        return self.value


class UUIDDatatype(Datatype):

    def __init__(self, version: int = 4):
        self.version = version

    def apply(self, event_service: EventService) -> str:
        match self.version:
            case 1:
                return str(uuid.uuid1())
            case 4:
                return str(uuid.uuid4())
            case _:
                raise UnsupportedUUIDVersion()
class StringDatatype(Datatype):

    def __init__(self, regex: str = r"[A-Za-z]{5}[0-9]{3}"):
        self.regex = re.compile(regex)

    def apply(self, event_service: EventService) -> str:
        return rstr.xeger(self.regex)


class NumericDatatype(Datatype):

    def __init__(self, min: int = 0, max: int = 1000000000, step: int = 1):
        self.min = min
        self.max = max
        self.step = step

    def apply(self, event_service: EventService) -> int:
        return random.randrange(self.min, self.max, self.step)


class ObjectDatatype(Datatype):

    def apply(self, event_service: EventService) -> Dict:
        final_object = {}
        for key, value  in vars(self).items():
            if not isinstance(value, Datatype):
                raise NotDatatypeError(key)
            final_object[key] = value.apply(event_service)

        return final_object

class CustomDatatype(Datatype):

    def __init__(self, callable: Callable):
        self.callable = callable

    def apply(self, event_service: EventService) -> Any:
        return self.callable()

class DatetimeDatatype(Datatype):

    def __init__(self, 
                 start: datetime = datetime(1970, 1, 1, tzinfo=timezone.utc), 
                 end: datetime = datetime(2114, 12, 31, tzinfo=timezone.utc), 
                 format: str = "%Y-%m-%d %H:%M:%S"):
        self.start = start
        self.end = end
        self.format = format

    def apply(self, event_service: EventService) -> str:
        start_timestamp = self.start.timestamp()
        end_timestamp = self.end.timestamp()

        random_timestamp = random.uniform(start_timestamp, end_timestamp)

        return datetime.fromtimestamp(random_timestamp).strftime(self.format)

class NullDatatype(Datatype):

    def apply(self, event_service: EventService) -> None:
        return None


