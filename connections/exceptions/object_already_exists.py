"""Exception when an object already exists"""


class ObjectAlreadyExistsException(Exception):
    """Exception when an object already exists"""
    def __init__(self, obj_name: str):
        super().__init__()
        self.__message = (
            f'{obj_name.capitalize()} already exists! Please, change parameter '
            f'`replace` to true if you want to replace this {obj_name} by new!')

    def __str__(self):
        return self.__message


class NodeAlreadyExistsException(ObjectAlreadyExistsException):
    """Exception when node already exists"""
    def __init__(self):
        super().__init__('node')


class EdgeAlreadyExistsException(ObjectAlreadyExistsException):
    """Exception when edge already exists"""
    def __init__(self):
        super().__init__('edge')
