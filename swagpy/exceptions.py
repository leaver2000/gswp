class Error(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(self.__doc__, *args)


class SingletonError(Error):
    """singleton type should not be instantiated"""
