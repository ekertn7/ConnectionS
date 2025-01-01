"""Type alias for nodes"""

from typing import TypeAlias, Any
from connections.core.identifier import Identifier


Nodes: TypeAlias = dict[Identifier, Any]
