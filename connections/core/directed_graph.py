"""DirectedGraph implementation"""

from typing import Tuple
from connections.core.identifier import Identifier
from connections.core.nodes import Nodes
from connections.core.edges import Edges
from connections.core.graph import Graph


class DirectedGraph(Graph):

    """DirectedGraph implementation

    Nodes representation
    --------------------

    Nodes representation is a dict with:
        - node identifier
        - node attributes

    Nodes representation example:
        {
            'Elizabeth': {'age': 19, 'sex': False},
            'Sebastian': {'age': 21, 'sex': True},
        }

    Edges representation
    --------------------

    Edges representation is a dict with:
        - couple - a tuple with:
            - left node identifier
            - right node identifier
        - multiples (same as in UndirectedGraph) - a dict with:
            - edge identifier
            - edge attributes

    Edges representation example:
        {
            ('Sebastian', 'Elizabeth'): {
                '46f893e': {'amount': 1400, 'date': '2024-03-08'},
                '206ij5s': {'amount': 2700, 'date': '2024-07-23'},
            },
            ('Elizabeth', 'Sebastian'): {
                '239af58': {'amount': 1900, 'date': '2024-04-16'},
            },
        }
    """

    def __init__(self, nodes: Nodes = None, edges: Edges = None):
        super().__init__(nodes=nodes, edges=edges)

    def _couple_representation(
            self, couple: Tuple[Identifier, Identifier]
            ) -> Tuple[Identifier, Identifier]:
        """Couple representation for directed graph"""
        return couple

    def calc_neighbors(self):
        """Finds neighbors for each node in graph"""
        for node in self.nodes.keys():
            self.nodes[node]['neighbors'] = set()

        for (node_l, node_r) in self.edges.keys():
            self.nodes[node_l]['neighbors'].add(node_r)
