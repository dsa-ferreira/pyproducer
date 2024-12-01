import importlib
import inspect

def find_event_models(module_name: str):
    module = importlib.import_module(module_name)
    subclasses = []
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if getattr(obj, "is_event", False):
            subclasses.append(obj)
    return subclasses

def get_class_name(obj):
    return type(obj).__name__
