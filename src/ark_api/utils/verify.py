def _verify(obj, class_name):
    _cls = obj.__class__
    while _cls is not object:
        if _cls.__name__ == class_name:
            return True
        _cls = _cls.__base__


def verify(obj, class_name, error_message=""):
    if not isinstance(obj, object):
        raise TypeError("obj must be object")
    if not isinstance(class_name, (str, list)):
        raise TypeError("class_name must be str or list")
    if not isinstance(error_message, str):
        raise TypeError("error_message must be str")
    if isinstance(class_name, str):
        if _verify(obj, class_name):
            return
    elif isinstance(class_name, list):
        for _class_name in class_name:
            if _verify(obj, _class_name):
                return
    if not error_message:
        error_message = (
            f"<{obj.__class__.__module__}.{obj.__class__.__qualname__}"
            f" object at {hex(id(obj))}> is not '{class_name}'"
        )
    raise TypeError(error_message)
