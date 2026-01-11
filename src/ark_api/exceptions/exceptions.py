class ArkApiError(Exception):
    """
    Base exception
    """
    pass


class ArkApiClientError(ArkApiError):
    """
    API Error
    """
    pass
