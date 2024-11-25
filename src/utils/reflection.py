from src.events import EventBase
import importlib
import inspect

def find_event_models(module: str):
    return find_subclasses(EventBase, module)

def find_subclasses(base_class, module):
    module = importlib.import_module(module)
    subclasses = []
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, base_class) and obj is not base_class:
            subclasses.append(obj)
    return subclasses

