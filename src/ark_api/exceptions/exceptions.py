class ArkApiError(Exception):
    """
    Base exception
    """
    pass


class APIError(ArkApiError):
    """
    API Error
    """
    pass


class SecretUsed(ArkApiError):
    """
    Secret Used Error
    """
    pass
