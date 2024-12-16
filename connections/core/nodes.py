"""Type alias for nodes"""

from typing import TypeAlias, Any, Dict
from connections.core.identifier import Identifier


Nodes: TypeAlias = Dict[Identifier, Any]
