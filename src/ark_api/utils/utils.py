from ark_api.utils import SecretStr


def verify(obj, class_name, error_message):
    _cls = obj.__class__
    while _cls is not object:
        if _cls.__name__ == class_name:
            return
        _cls = _cls.__base__
    raise AssertionError(error_message)


def mask_secrets_from_dict(d):
    return {
        key: "*****"
        if isinstance(value, SecretStr) else value
        for key, value in d.items()
    }
