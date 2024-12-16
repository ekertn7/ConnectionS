"""Validation exceptions

- ValidationException
    - NodesValidationException
        - WrongTypeOfNodesException
        - WrongTypeOfNodeIdentifierException
        - WrongTypeOfNodeAttributesException

    - EdgesValidationException
        - WrongTypeOfEdgesException
        - WrongTypeOfCoupleException
        - WrongLengthOfCoupleException
        - WrongTypeOfNodeIdentifierInCoupleException
        - WrongTypeOfMultipleEdgesException
        - WrongLengthOfMultipleEdgesException
        - WrongTypeOfEdgeIdentifierException
        - WrongTypeOfEdgeAttributesException
        - DuplicationInEdgeIdentifiersException
"""


class ValidationException(Exception):
    """Validation exception"""
    def __init__(self, prefix: str, message: str):
        super().__init__()
        self.__message = f'{prefix} {message}'

    def __str__(self):
        return self.__message


class NodesValidationException(ValidationException):
    """Nodes validation exception"""
    def __init__(self, message: str):
        prefix = 'Nodes validation exception!'
        super().__init__(prefix=prefix, message=message)


class WrongTypeOfNodesException(NodesValidationException):
    """Wrong type of nodes exception"""
    def __init__(self):
        message = 'Wrong type of nodes: nodes type must be Dict or Iterable!'
        super().__init__(message=message)


class WrongTypeOfNodeIdentifierException(NodesValidationException):
    """Wrong type of node identifier exception"""
    def __init__(self):
        message = (
            'Wrong type of node identifier: node identifier type must be '
            'Identifier!')
        super().__init__(message=message)


class WrongTypeOfNodeAttributesException(NodesValidationException):
    """Wrong type of node attributes exception"""
    def __init__(self):
        message = (
            'Wrong type of node attributes: node attributes type must be Dict!')
        super().__init__(message=message)


class EdgesValidationException(ValidationException):
    """Edges validation exception"""
    def __init__(self, message: str):
        prefix = 'Edges validation exception!'
        super().__init__(prefix=prefix, message=message)


class WrongTypeOfEdgesException(EdgesValidationException):
    """Wrong type of edges exception"""
    def __init__(self):
        message = 'Wrong type of edges: edges type must be Dict or Iterable!'
        super().__init__(message=message)


class WrongTypeOfCoupleException(EdgesValidationException):
    """Wrong type of couple exception"""
    def __init__(self):
        message = 'Wrong type of couple: couple type must be Tuple!'
        super().__init__(message=message)


class WrongLengthOfCoupleException(EdgesValidationException):
    """Wrong length of couple exception"""
    def __init__(self):
        message = 'Wrong length of couple: couple length must be equal 2!'
        super().__init__(message=message)


class WrongTypeOfNodeIdentifierInCoupleException(EdgesValidationException):
    """Wrong type of node identifier in couple exception"""
    def __init__(self):
        message = (
            'Wrong type of node identifier: node identifier type must be '
            'Identifier!')
        super().__init__(message=message)


class WrongTypeOfMultipleEdgesException(EdgesValidationException):
    """Wrong type of multiple edges exception"""
    def __init__(self):
        message = (
            'Wrong type of multiple edges: multiple edges type must be Dict!')
        super().__init__(message=message)


class WrongLengthOfMultipleEdgesException(EdgesValidationException):
    """Wrong length of multiple edges exception"""
    def __init__(self):
        message = (
            'Wrong length of multiple edges! Multiple edges length must be '
            'more than 0!')
        super().__init__(message=message)


class WrongTypeOfEdgeIdentifierException(EdgesValidationException):
    """Wrong type of edge identifier exception"""
    def __init__(self):
        message = (
            'Wrong type of edge identifier: edge identifier type must be '
            'Identifier!')
        super().__init__(message=message)


class WrongTypeOfEdgeAttributesException(EdgesValidationException):
    """Wrong type of edge attributes exception"""
    def __init__(self):
        message = (
            'Wrong type of edge attributes: edge attributes type must be Dict!')
        super().__init__(message=message)


class DuplicationInEdgeIdentifiersException(EdgesValidationException):
    """Duplication in edge identifiers exception"""
    def __init__(self, node_l: str, node_r: str):
        message = (
            f'Duplication in edge identifiers incident to nodes '
            f'{node_l} and {node_r}! Please, resolve conflict and try again!')
        super().__init__(message=message)
