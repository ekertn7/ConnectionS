"""Type alias for edges"""

from typing import TypeAlias, Any
from connections.core.identifier import Identifier


Edges: TypeAlias = dict[
    tuple[Identifier, Identifier],
    dict[Identifier, dict[str, Any]]
]
