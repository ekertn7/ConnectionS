"""Graph implementation"""

from typing import Iterable, Dict
from abc import ABC, abstractmethod
from connections.core.identifier import Identifier, generate_identifier
from connections.core.nodes import Nodes
from connections.core.edges import Edges
from connections.exceptions.object_already_exists import NodeAlreadyExistsException


class Graph(ABC):
    """Graph implementation"""

    def _nodes_validation(self, nodes) -> Nodes:
        """Validation function for nodes"""
        def _check_node_keys_type() -> bool:
            """Checks that type of 'Elizabeth' is Identifier"""
            if not all(isinstance(node, Identifier) for node in nodes):
                raise Exception()

        def _check_node_values_type() -> bool:
            """Checks that type of {'age': 19, 'sex': False} is dict"""
            if not all(isinstance(values, Dict) for values in nodes.values()):
                raise Exception()

        if isinstance(nodes, Dict):
            _check_node_keys_type()
            _check_node_values_type()
            for identifier, values in nodes.items():
                self.add_node(
                    identifier=identifier, replace=False,
                    clear_calculated_values=False, **values)
        if isinstance(nodes, Iterable):
            _check_node_keys_type()
            return {node: {} for node in nodes}
        raise TypeError()

    @property
    def nodes(self):
        """Nodes getter"""
        return self.__nodes

    @nodes.setter
    def nodes(self, new_nodes: Nodes):
        """Nodes setter"""
        self.__nodes = new_nodes

    @nodes.deleter
    def nodes(self):
        """Nodes deleter"""
        raise Exception('LOL')

    def __init__(self, nodes: Nodes = None, edges: Edges = None):
        self.__nodes = {}
        self._nodes_validation(nodes)
        self.__edges = edges or {}

        self.clear_degree()
        self.clear_neighbors()

    # @property
    # def edges(self):
    #     """Edges getter"""
    #     return self.__edges

    # @edges.setter
    # def edges(self, new_edges: Edges):
    #     """Edges setter"""
    #     for (node_l, node_r), edge in new_edges.items():
    #         for identifier, values in edge.items():
    #             print(node_l, node_r, identifier, values)
    #             self.add_edge(
    #                 node_l=node_l, node_r=node_r, identifier=identifier,
    #                 replace=False, add_non_existent_incident_nodes=True,
    #                 clear_calculated_nodes_values=False, **values)
    #     # self.__edges = new_edges

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
        clear_calculated_nodes_values, optional
            Clear nodes values, that calculated by functions: calc_degree, calc_neighbors
                - True (deafult): clear calculated nodes values (worst performance)
                    * use it when adding a small number of nodes
                - False: do nothing (best performance)
                    * use it when adding a large number of nodes,
                      then recalculate calculated values

        Returns
        -------
            Node identifier
        """
        if identifier is None:
            identifier = generate_identifier()
        else:
            if not isinstance(identifier, Identifier):
                raise TypeError()

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
        clear_calculated_nodes_values, optional
            Clear nodes values, that calculated by functions: calc_degree, calc_neighbors
                - True (deafult): clear calculated nodes values (worst performance)
                    * use it when removing a small number of nodes
                - False: do nothing (best performance)
                    * use it when removing a large number of nodes,
                      then recalculate calculated values
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

        if any(value.get('degree') is not None for value in subgraph.nodes.values()):
            subgraph.calc_degree()
        if any(value.get('neighbors') is not None for value in subgraph.nodes.values()):
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

    def is_complete(self):
        """Checks that graph is complete"""
        edges_lenght = len({
            (node_l, node_r) for (node_l, node_r) in self.edges.keys()
            if node_l != node_r})
        max_edges_legth = (len(self.nodes) * (len(self.nodes) - 1)) / 2
        return edges_lenght == max_edges_legth

    def is_connected(self):
        """Checks that graph is conncted"""
        return NotImplemented

    def describe(self):
        """Returns information about graph"""
        self.calc_degree()
        self.calc_neighbors()
        return {
            'type': self.__class__,
            'number_of_nodes': len(self.nodes),
            'number_of_edges': len(self.edges),
            'multi_graph': any(len(values) > 1 for values in self.edges.values()),
            'pseudo_graph': any(self.find_loops()),
            'connected_graph': self.is_connected(),
            'complete_graph': self.is_complete(),
        }
