"""Type alias for edges"""

from typing import TypeAlias, Any, Dict, Tuple
from connections.core.identifier import Identifier


Edges: TypeAlias = Dict[
    Tuple[Identifier, Identifier],
    Dict[Identifier, Dict[str, Any]]
]
