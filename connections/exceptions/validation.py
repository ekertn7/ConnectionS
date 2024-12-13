"""Validation exceptions"""


class ValidationException(Exception):
    """Validation exception"""
    def __init__(self, prefix: str, message: str):
        super().__init__()
        self.__message = f'{prefix}: {message}'

    def __str__(self):
        return self.__message


class NodesValidationException(ValidationException):
    """Nodes validation exception"""
    def __init__(self, message: str):
        super().__init__(prefix='Nodes validation exception', message=message)


class EdgesValidationException(ValidationException):
    """Edges validation exception"""
    def __init__(self, message: str):
        super().__init__(prefix='Edges validation exception', message=message)


class WrongTypeOfNodeIdentifierException(NodesValidationException):
    """Wrong type of node identifier exception"""
    def __init__(self):
        super().__init__(message = (
            'Wrong type of node identifier! Node identifier type must be '
            'Identifier!'))


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
