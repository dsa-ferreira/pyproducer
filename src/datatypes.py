from datetime import datetime, timezone
from typing import Callable, Any, Dict
import re
import rstr
import random
import uuid

class NotDatatypeError(Exception):

    def __init__(self, field_name):
        super().__init__(f'field {field_name} does not extend the Datatype class')
        self.field_name = field_name

class Datatype:

    def apply(self) -> Any:
        raise Exception

class ConstDatatype(Datatype):

    def __init__(self, value: Any):
        self.value = value

    def apply(self) -> Any:
        return self.value


class UUIDDatatype(Datatype):

    def apply(self) -> str:
        return str(uuid.uuid4())

class StringDatatype(Datatype):

    def __init__(self, regex: str = r"[A-Za-z]{5}[0-9]{3}"):
        self.regex = re.compile(regex)

    def apply(self) -> str:
        return rstr.xeger(self.regex)


class NumericDatatype(Datatype):

    def __init__(self, min: int = 0, max: int = 1000000000, step: int = 1):
        self.min = min
        self.max = max
        self.step = step

    def apply(self) -> int:
        return random.randrange(self.min, self.max, self.step)


class ObjectDatatype(Datatype):

    def apply(self) -> Dict:
        final_object = {}
        for key, value  in vars(self).items():
            if not isinstance(value, Datatype):
                raise NotDatatypeError(key)
            final_object[key] = value.apply()

        return final_object

class CustomDatatype(Datatype):

    def __init__(self, callable: Callable):
        self.callable = callable

    def apply(self) -> Any:
        return self.callable()

class DatetimeDatatype(Datatype):

    def __init__(self, 
                 start: datetime = datetime(1970, 1, 1, tzinfo=timezone.utc), 
                 end: datetime = datetime(2114, 12, 31, tzinfo=timezone.utc), 
                 format: str = "%Y-%m-%d %H:%M:%S"):
        self.start = start
        self.end = end
        self.format = format

    def apply(self) -> str:
        start_timestamp = self.start.timestamp()
        end_timestamp = self.end.timestamp()

        random_timestamp = random.uniform(start_timestamp, end_timestamp)

        return datetime.fromtimestamp(random_timestamp).strftime(self.format)

class NullDatatype(Datatype):

    def apply(self) -> None:
        return None


