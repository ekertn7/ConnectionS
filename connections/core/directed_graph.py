"""DirectedGraph implementation"""

from typing import Tuple, Iterable, Dict, Set
from connections.core.identifier import Identifier, generate_identifier
from connections.core.nodes import Nodes
from connections.core.edges import Edges
from connections.core.graph import Graph
from connections.exceptions import (
    NodeAlreadyExistsException, EdgeAlreadyExistsException,
    EdgesValidationException)


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

    def _edges_validation(self, edges) -> Edges:
        """Validation function for directed edges"""

        def check_couple_type() -> None:
            """Checks that type of couple is Tuple"""
            if not all(isinstance(edge, Tuple) for edge in edges):
                raise Exception('WrongEdgesNodesTypeException')

        def check_couple_len() -> None:
            """Checks that length of couple == 2"""
            if not all(len(edge) == 2 for edge in edges):
                raise Exception('WrongEdgesKeyLengthException')

        def check_node_identifier_type() -> None:
            """Checks that type of node identifier in couple is Identifier"""
            if not all(
                    isinstance(node_l, Identifier) and isinstance(node_r, Identifier)
                    for (node_l, node_r) in edges):
                raise Exception('WrongEdgesKeyNodesIdentifierTypeException')

        def check_multiples_type() -> None:
            """Checks that type of multiple edges is Dict"""
            if not all(isinstance(values, Dict) for values in edges.values()):
                raise Exception('WrongEdgesValueTypeException')

        def check_edge_identifier_type():
            """Checks that type of edge identifier is Identifier"""
            for multiples in edges.values():
                if not all(
                        isinstance(edge_identifier, Identifier)
                        for edge_identifier in multiples.keys()):
                    raise Exception('WrongEdgeIdentifierTypeException')

        def check_edge_attributes_type():
            """Checks that type of edge attributes is Dict"""
            for multiples in edges.values():
                if not all(
                        isinstance(edge_attributes, Dict)
                        for edge_attributes in multiples.values()):
                    raise Exception('WrongEdgeAttributesTypeException')

        def add_non_existent_incident_nodes() -> None:
            new_nodes = {node_l for (node_l, _) in edges} | {node_r for (_, node_r) in edges}
            existent_nodes = set(self.nodes)
            non_existent_nodes = new_nodes - existent_nodes
            for identifier in non_existent_nodes:
                self.add_node(identifier=identifier, clear_calculated_values=False)

        if edges is None:
            return {}

        if isinstance(edges, Dict):
            check_couple_type()
            check_couple_len()
            check_node_identifier_type()
            check_multiples_type()
            check_edge_identifier_type()
            check_edge_attributes_type()
            add_non_existent_incident_nodes()
            return edges

        if isinstance(edges, Iterable):
            check_couple_type()
            check_couple_len()
            check_node_identifier_type()
            add_non_existent_incident_nodes()
            return {edge: {generate_identifier(): {}} for edge in edges}

        raise EdgesValidationException(
            'Wrong edges type! Edges type must be Dict or Iterable!')

    def add_edge(
            self, node_l: Identifier, node_r: Identifier,
            identifier: Identifier = None, replace: bool = False,
            add_non_existent_incident_nodes: bool = True,
            clear_calculated_nodes_values: bool = True,
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
                - True: replace existing edge by new
                - False (default): raise EdgeAlreadyExistsException if edge exists
        add_non_existent_incident_nodes, optional
            Add non-existent incident nodes
                - True (default): add non-existent incident nodes to the graph
                - False: do nothing
        clear_calculated_nodes_values, optional
            Clear nodes values, that calculated by functions: calc_degree, calc_neighbors
                - True (deafult): clear calculated nodes values (worst performance)
                    * use it when adding a small number of edges
                - False: do nothing (best performance)
                    * use it when adding a large number of edges,
                      then recalculate calculated values

        Returns
        -------
            Edge identifier
        """
        edge = (node_l, node_r)
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

        if clear_calculated_nodes_values is True:
            self.clear_degree()
            self.clear_neighbors()

        return identifier

    def del_edge(
            self, node_l: Identifier, node_r: Identifier,
            identifier: Identifier = None,
            clear_calculated_nodes_values: bool = True) -> None:
        """Removes an edge from the graph

        Parameters
        ----------
        node_l
            Left node identifier
        node_r
            Right node identifier
        identifier
            Edge identifier
                - None (default): removes all edges incident with source and target nodes
                - ...: removes selected edge
        clear_calculated_nodes_values, optional
            Clear nodes values, that calculated by functions: calc_degree, calc_neighbors
                - True (deafult): clear calculated nodes values (worst performance)
                    * use it when removing a small number of edges
                - False: do nothing (best performance)
                    * use it when removing a large number of edges,
                      then recalculate calculated values
        """
        edge = (node_l, node_r)

        if identifier is None:
            del self.edges[edge]
        else:
            del self.edges[edge][identifier]

        if clear_calculated_nodes_values is True:
            self.clear_degree()
            self.clear_neighbors()

    def calc_neighbors(self):
        """Finds neighbors for each node in graph"""
        for node in self.nodes.keys():
            self.nodes[node]['neighbors'] = set()

        for (node_l, node_r) in self.edges.keys():
            self.nodes[node_l]['neighbors'].add(node_r)
