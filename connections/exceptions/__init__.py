"""Exceptions init"""

from . object_already_exists import (
    NodeAlreadyExistsException, EdgeAlreadyExistsException)
from . validation import (
    NodesValidationException, EdgesValidationException,
    CanNotDeleteBasicElementsInGraphException)
