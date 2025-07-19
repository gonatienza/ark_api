from .secret import SecretStr


def verify(obj, class_name, error_message=""):
    assert isinstance(obj, object), "obj must be object"
    assert isinstance(class_name, str), "class_name must be str"
    assert isinstance(error_message, str), "error_message must be str"
    _cls = obj.__class__
    while _cls is not object:
        if _cls.__name__ == class_name:
            return
        _cls = _cls.__base__
    if not error_message:
        error_message = (
            f"<{obj.__class__.__module__}.{obj.__class__.__qualname__}"
            f" object at {hex(id(obj))}> is not '{class_name}'"
        )
    raise AssertionError(error_message)


def mask_secrets_from_dict(d):
    assert isinstance(d, dict), "d must be dict"
    return {
        key: "*****"
        if isinstance(value, SecretStr) else value
        for key, value in d.items()
    }
