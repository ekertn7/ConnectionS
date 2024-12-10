"""UndirectedGraph implementation"""
from connections.core.identifier import Identifier, generate_identifier
from connections.core.nodes import Nodes
from connections.core.edges import Edges
from connections.core.graph import Graph
from connections.exceptions.object_already_exists import (
    NodeAlreadyExistsException, EdgeAlreadyExistsException
)


class UndirectedGraph(Graph):
    """UndirectedGraph implementation

    Nodes representation
    --------------------

    Nodes representation is a dict with:
        - keys: node identifier
        - values: node attributes

    Nodes representation example:
        {
            'Elizabeth': {'age': 19, 'sex': False},
            'Sebastian': {'age': 21, 'sex': True},
        }

    Edges representation
    --------------------

    Edges representation is a dict with:
        - keys: a sorted tuple with two nodes identifier
        - values (same as in UndirectedGraph): a dict with:
            - keys: edge identifier
            - values: edge attributes

    Edges representation example:
        {
            ('Elizabeth', 'Sebastian'): {
                '46f893e': {'amount': 1400, 'date': '2024-03-08'},
                '206ij5s': {'amount': 2700, 'date': '2024-07-23'},
                '239af58': {'amount': 1900, 'date': '2024-04-16'},
            },
        }
    """
    def __init__(self, nodes: Nodes = None, edges: Edges = None):
        super().__init__(nodes=nodes, edges=edges)

    def add_edge(
            self, node_l: Identifier, node_r: Identifier,
            identifier: Identifier = None, replace: bool = False,
            add_non_existent_incident_nodes: bool = True,
            **kwargs) -> Identifier:
        """Adds an edge and its incident nodes to the graph

        Parameters
        ----------
        node_l
            Left node identifier
        node_r
            Right node identifier
        identifier, optional
            Edge identifier
                - None (default): an automatically generated identifier (UUID) is assigned
                - ...: selected identifier is assigned
        replace, optional
            Replace existing edge
                - False (default): raise EdgeAlreadyExistsException if edge exists
                - True: replace existing edge by new
        add_non_existent_incident_nodes, optional
            Add non-existent incident nodes
                - True (default): add non-existent incident nodes to the graph
                - False: do nothing

        Returns
        -------
            Edge identifier
        """
        edge = tuple(sorted((node_l, node_r)))
        if identifier is None:
            identifier = generate_identifier()

        if self.edges.get(edge) is None:
            self.edges[edge] = {identifier: kwargs}
        else:
            if replace is False and self.edges[edge].get(identifier) is not None:
                raise EdgeAlreadyExistsException()
            self.edges[edge][identifier] = kwargs

        if add_non_existent_incident_nodes is True:
            try:
                self.add_node(node_l, replace=False)
            except NodeAlreadyExistsException:
                pass
            try:
                self.add_node(node_r, replace=False)
            except NodeAlreadyExistsException:
                pass

        self.clear_degree()
        self.clear_neighbors()

        return identifier

    def del_edge(
            self, node_l: Identifier, node_r: Identifier,
            identifier: Identifier = None) -> None:
        """Removes an edge from the graph

        Parameters
        ----------
        node_l
            Left node identifier
        node_r
            Right node identifier
        identifier
            Edge identifier
                - None (default): removes all edges incident with left ant right nodes
                - ...: removes selected edge
        """
        edge = tuple(sorted((node_l, node_r)))

        if identifier is None:
            del self.edges[edge]
        else:
            del self.edges[edge][identifier]

        self.clear_degree()
        self.clear_neighbors()

    def calc_neighbors(self):
        """Find neighbors for each node in graph"""
        for node in self.nodes.keys():
            self.nodes[node]['neighbors'] = set()

        for (node_l, node_r) in self.edges:
            self.nodes[node_l]['neighbors'].add(node_r)
            self.nodes[node_r]['neighbors'].add(node_l)
