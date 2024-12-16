"""Exceptions init"""

from . object_already_exists import (
    NodeAlreadyExistsException,
    EdgeAlreadyExistsException)
from . cant_delete_basic_elements import (
    CanNotDeleteBasicElementsInGraphException)
from . validation import (
    WrongTypeOfNodesException,
    WrongTypeOfNodeIdentifierException,
    WrongTypeOfNodeAttributesException,
    WrongTypeOfEdgesException,
    WrongTypeOfCoupleException,
    WrongLengthOfCoupleException,
    WrongTypeOfNodeIdentifierInCoupleException,
    WrongTypeOfMultipleEdgesException,
    WrongLengthOfMultipleEdgesException,
    WrongTypeOfEdgeIdentifierException,
    WrongTypeOfEdgeAttributesException,
    DuplicationInEdgeIdentifiersException)
