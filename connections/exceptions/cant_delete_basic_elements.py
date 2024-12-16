"""Can not delete basic elements in graph exception"""


class CanNotDeleteBasicElementsInGraphException(Exception):
    """Can not delete basic elements in graph exception"""
    def __init__(self, element: str):
        super().__init__()
        self.__message = (
            f'You can not delete basic elements in graph, like nodes or edges! '
            f'If you want to delete all {element}, use clear_{element} method '
            f'instead of del!')

    def __str__(self):
        return self.__message
