import json
import inspect
from datetime import datetime


class ObjectEncoder(json.JSONEncoder):
    """
    https://stackoverflow.com/a/35483750/3291194
    """
    def default(self, obj):
        if hasattr(obj, "to_json"):
            return self.default(obj.to_json())
        elif isinstance(obj, datetime):
            return obj.isoformat() + 'Z'
        elif hasattr(obj, "__dict__"):
            d = dict(
                (key, value)
                for key, value in inspect.getmembers(obj)
                if not key.startswith("__")
                and not inspect.isabstract(value)
                and not inspect.isbuiltin(value)
                and not inspect.isfunction(value)
                and not inspect.isgenerator(value)
                and not inspect.isgeneratorfunction(value)
                and not inspect.ismethod(value)
                and not inspect.ismethoddescriptor(value)
                and not inspect.isroutine(value)
            )
            return self.default(d)


def _encode_tuple_keys(obj):
    if isinstance(obj, list):
        return [_encode_tuple_keys(item) for item in obj]
    elif isinstance(obj, dict):
        obj = dict(
            (str(key), value) if not isinstance(key, (str, int, float, bool))
            else (key, value)
            for key, value in obj.items()
        )
    return obj


def json_serialize(obj):
    obj = _encode_tuple_keys(obj)
    return json.dumps(obj, cls=ObjectEncoder)
