class ArkObject:
    def __init__(self, attributes):
        assert isinstance(attributes, dict)
        for key, value in attributes.items():
            if isinstance(value, dict):
                setattr(self, key, ArkObject(value))
            else:
                setattr(self, key, value)
