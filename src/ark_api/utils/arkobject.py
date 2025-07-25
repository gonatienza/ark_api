from .utils import pythonify_attr


class ArkObject:
    def __init__(self, attributes):
        assert isinstance(attributes, (dict, list))
        if isinstance(attributes, dict):
            for key, value in attributes.items():
                _key = pythonify_attr(key)
                if isinstance(value, dict):
                    setattr(self, _key, ArkObject(value))
                else:
                    setattr(self, _key, value)
        elif isinstance(attributes, list):
            self.items = [
                ArkObject(item) if isinstance(item, (dict, list)) else item
                for item in attributes
            ]

    def __iter__(self):
        return iter(self.__dict__.items())
