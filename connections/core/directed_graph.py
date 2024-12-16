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
        self.clear_neighbors()

        for (node_l, node_r) in self.edges:
            self.nodes[node_l]['neighbors'].add(node_r)

    def describe(self):
        """Returns information about directed graph"""
        self.calc_degree()
        self.calc_neighbors()
        return {
            'type': 'Directed Graph',
            'number_of_nodes': len(self.nodes),
            'number_of_edges': len(self.edges),
            'multi_graph': self._is_multi(),
            'pseudo_graph': self._is_pseudo(),
            # 'connected_graph': self._is_connected(),
            'complete_graph': self._is_complete(),
        }
