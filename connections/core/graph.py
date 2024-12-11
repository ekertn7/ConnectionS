"""Graph implementation"""

from typing import Iterable
from abc import ABC, abstractmethod
from connections.core.identifier import Identifier, generate_identifier
from connections.core.nodes import Nodes
from connections.core.edges import Edges
from connections.exceptions.object_already_exists import NodeAlreadyExistsException


class Graph(ABC):
    """Graph implementation

    All graphs supports multi edges

    Nodes format
    ------------
    nodes = {
        'bc4f32b941': {'name': 'Alex', 'age': 19, 'sex': True},
        '9cbdbedb44': {'name': 'Bella', 'age': 20, 'sex': False},
        '488bc1b9c1': {'name': 'Clare', 'age': 18, 'sex': False},
    }

    Edges format
    ------------
    edges = {
        ('bc4f32b941', '9cbdbedb44'): {
            'ac89bf9b56': {'amount': 1400, 'date': '2024-02-12'},
            'c2484a9d76': {'amount': 2900, 'date': '2024-01-18'},
            '783b2810af': {'amount': 3400, 'date': '2024-03-05'},
        },
        ('bc4f32b941', '488bc1b9c1'): {
            '2c7dfd0a44': {'amount': 5300, 'date': '2024-03-16'},
            '347c595307': {'amount': 2200, 'date': '2024-02-19'},
        },
        ('488bc1b9c1', '9cbdbedb44'): {
            '0650ba3e6e': {'amount': 4100, 'date': '2024-02-24'},
        },
    }
    """
    def __init__(self, nodes: Nodes = None, edges: Edges = None):
        self.__nodes = nodes or {}
        self.__edges = edges or {}

        self.clear_degree()
        self.clear_neighbors()

    @property
    def nodes(self):
        """Nodes getter"""
        return self.__nodes

    @nodes.setter
    def nodes(self, new_nodes: Nodes):
        """Nodes setter"""
        self.__nodes = new_nodes

    @property
    def edges(self):
        """Edges getter"""
        return self.__edges

    @edges.setter
    def edges(self, new_edges: Edges):
        """Edges setter"""
        self.__edges = new_edges

    def __eq__(self, other):
        return type(self) is type(other) and \
            self.nodes == other.nodes and \
            self.edges == other.edges

    def __len__(self):
        """Returns the number of nodes in the graph"""
        return len(self.nodes)

    def add_node(
            self, identifier: Identifier = None, replace: bool = False,
            clear_calculated_values: bool = True, **kwargs) -> Identifier:
        """Adds node to the graph

        Parameters
        ----------
        identifier, optional
            Node identifier
                - None (default): an automatically generated identifier (UUID) is assigned
                - ...: selected identifier is assigned
        replace, optional
            Replace existing node
                - False (default): raise NodeAlreadyExistsException if node exists
                - True: replace existing node by new

        Returns
        -------
            Node identifier
        """
        if identifier is None:
            identifier = generate_identifier()

        if replace is False and self.nodes.get(identifier) is not None:
            raise NodeAlreadyExistsException()

        self.nodes[identifier] = kwargs

        if clear_calculated_values is True:
            self.clear_degree()
            self.clear_neighbors()

        return identifier

    def del_node(
            self, identifier: Identifier,
            clear_calculated_values: bool = True) -> None:
        """Removes node from the graph

        Parameters
        ----------
        identifier
            Node identifier
        """
        del self.nodes[identifier]

        if clear_calculated_values is True:
            self.clear_degree()
            self.clear_neighbors()

    def clear_nodes(self) -> None:
        """Removes all nodes from the graph"""
        self.nodes = {}

    @abstractmethod
    def add_edge(
            self, node_l: Identifier, node_r: Identifier,
            identifier: Identifier = None, replace: bool = False,
            add_non_existent_incident_nodes: bool = True,
            clear_calculated_nodes_values: bool = True,
            **kwargs) -> Identifier:
        """Adds an edge and its incident nodes to the graph"""

    @abstractmethod
    def del_edge(
            self, node_l: Identifier, node_r: Identifier,
            identifier: Identifier,
            clear_calculated_nodes_values: bool = True) -> None:
        """Removes an edge from the graph"""

    def clear_edges(self) -> None:
        """Removes all edges from the graph"""
        self.edges = {}

        self.clear_degree()
        self.clear_neighbors()

    def get_subgraph(
            self, selected_nodes: Iterable[Identifier], fullmatch: bool = True):
        """Returns subgraph with selected nodes

        Parameters
        ----------
        selected_nodes
            Iterable object with node identifiers
        fullmatch, optional
            Include nodes adjacent to nodes from selected nodes (but not in selected nodes)
                - True (default): include adjacent nodes
                - False: include nodes only from selected nodes

        Returns
        -------
            Subgraph
        """
        selected_nodes = set(selected_nodes) & set(self.nodes.keys())

        subgraph = self.__class__(
            nodes={node_id: self.nodes[node_id] for node_id in selected_nodes},
            edges=None,
        )

        def _condition(fullmatch, node_l, node_r):
            if fullmatch is True:
                return (node_l in selected_nodes) and (node_r in selected_nodes)
            return (node_l in selected_nodes) or (node_r in selected_nodes)

        for (node_l, node_r), edges in self.edges.items():
            if _condition(fullmatch, node_l, node_r):
                for edge_id, edge_kwargs in edges.items():
                    subgraph.add_edge(
                        node_l=node_l, node_r=node_r, identifier=edge_id,
                        add_non_existent_incident_nodes=False,
                        clear_calculated_nodes_values=False, **edge_kwargs)
                    subgraph.add_node(
                        identifier=node_l, replace=True, clear_calculated_values=False,
                        **self.nodes[node_l])
                    subgraph.add_node(
                        identifier=node_r, replace=True, clear_calculated_values=False,
                        **self.nodes[node_r])

        if any(True for value in subgraph.nodes.values() if value.get('degree') is not None):
            subgraph.calc_degree()
        if any(True for value in subgraph.nodes.values() if value.get('neighbors') is not None):
            subgraph.calc_neighbors()

        return subgraph

    def calc_degree(self):
        """Calculate degree for each node in graph"""
        for node in self.nodes.keys():
            self.nodes[node]['degree'] = 0

        for (node_l, node_r), edges in self.edges.items():
            self.nodes[node_l]['degree'] += len(edges)
            self.nodes[node_r]['degree'] += len(edges)

    def clear_degree(self):
        """Set degree value to None for each node in graph"""
        for node in self.nodes.keys():
            self.nodes[node]['degree'] = None

    @abstractmethod
    def calc_neighbors(self):
        """Finds neighbors for each node in graph"""

    def clear_neighbors(self):
        """Set neighbors value to None for each node in graph"""
        for node in self.nodes.keys():
            self.nodes[node]['neighbors'] = None

    def find_loops(self):
        """Finds loops in a graph (when an edge incident to one node)"""
        for (node_l, node_r) in self.edges.keys():
            if node_l == node_r:
                yield (node_l, node_r)

    def describe(self):
        """Returns information about graph"""
        self.calc_degree()
        self.calc_neighbors()
        return {
            'type': self.__class__,
            'multi_graph': any(True for values in self.edges.values() if len(values) > 1),
            'pseudo_graph': any(self.find_loops()),
            'complete_graph': (len(self.nodes) * (len(self.nodes) - 1)) / 2 == len(self.edges),
        }
