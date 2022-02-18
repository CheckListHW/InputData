from typing import Any


def recursive_extraction(obj: [Any]) -> Any:
    if type(obj) in [str]:
        return obj
    try:
        obj_list = iter(obj)
        return [recursive_extraction(i) for i in obj_list]
    except TypeError as te:
        if hasattr(obj, 'get_as_dict'):
            return obj.get_as_dict()
        else:
            return obj
