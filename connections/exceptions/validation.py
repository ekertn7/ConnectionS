"""Validation exceptions"""


class ValidationException(Exception):
    """Validation exception"""
    def __init__(self, message: str):
        super().__init__()
        self.__message = message

    def __str__(self):
        return self.__message


class NodesValidationException(ValidationException):
    """Nodes validation exception"""


class EdgesValidationException(ValidationException):
    """Edges validation exception"""


class CanNotDeleteBasicElementsInGraphException(Exception):
    """Trying delete basic element exception"""
    def __init__(self, element: str):
        super().__init__()
        self.__message = (
            f'You can not delete basic elements in graph, like nodes or edges! '
            f'If you want to delete all {element}, use clear_{element} method '
            f'instead of del!')

    def __str__(self):
        return self.__message
