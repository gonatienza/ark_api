class ArkApiError(Exception):
    """
    Base exception
    """
    pass


class ExpiredToken(ArkApiError):
    """
    Expired token
    """
    pass


class APIError(ArkApiError):
    """
    API Error
    """
    pass


class SecretUsed(Exception):
    """
    Secret Used Error
    """
    pass


class Unsupported(Exception):
    """
    Unsupported
    """
    pass
