"""Graph implementation"""

from typing import Iterable, Dict, Tuple
from abc import ABC, abstractmethod
from connections.core.identifier import Identifier, generate_identifier
from connections.core.nodes import Nodes
from connections.core.edges import Edges
from connections.exceptions.cant_delete_basic_elements import (
    CanNotDeleteBasicElementsInGraphException)
from connections.exceptions.object_already_exists import (
    NodeAlreadyExistsException,
    EdgeAlreadyExistsException)
from connections.exceptions.validation import (
    WrongTypeOfNodesException,
    WrongTypeOfNodeIdentifierException,
    WrongTypeOfNodeAttributesException,
    WrongTypeOfEdgesException,
    WrongTypeOfCoupleException,
    WrongLengthOfCoupleException,
    WrongTypeOfNodeIdentifierInCoupleException,
    WrongTypeOfMultipleEdgesException,
    WrongLengthOfMultipleEdgesException,
    WrongTypeOfEdgeIdentifierException,
    WrongTypeOfEdgeAttributesException,
    DuplicationInEdgeIdentifiersException)


class Graph(ABC):
    """Graph implementation"""

    def __init__(self, nodes: Nodes = None, edges: Edges = None):
        self.nodes = nodes
        self.edges = edges

        self.calc_degree()
        self.calc_neighbors()

    def __repr__(self):
        return str(self.__class__)

    @property
    def nodes(self):
        """Nodes getter"""
        return self.__nodes

    @nodes.setter
    def nodes(self, new_nodes: Nodes):
        """Nodes setter"""
        self.__nodes = {}
        self._nodes_validation(new_nodes)

    @nodes.deleter
    def nodes(self):
        """Nodes deleter"""
        raise CanNotDeleteBasicElementsInGraphException('nodes')

    def _nodes_validation(self, nodes) -> Nodes:
        """Validation function for nodes"""

        def check_node_identifier_type() -> None:
            """Checks that type of node identifier is Identifier"""
            if not all(isinstance(identifier, Identifier) for identifier in nodes):
                raise WrongTypeOfNodeIdentifierException()

        def check_node_attributes_type() -> None:
            """Checks that type of node attributes is Dict"""
            if not all(isinstance(attrs, Dict) for attrs in nodes.values()):
                raise WrongTypeOfNodeAttributesException()

        if nodes is None:
            return

        if isinstance(nodes, Dict):
            check_node_identifier_type()
            check_node_attributes_type()
            for identifier, attributes in nodes.items():
                self.add_node(identifier=identifier, **attributes)
        elif isinstance(nodes, Iterable):
            check_node_identifier_type()
            for identifier in nodes:
                self.add_node(identifier=identifier, replace=True)
        else:
            raise WrongTypeOfNodesException()

    @property
    def edges(self):
        """Edges getter"""
        return self.__edges

    @edges.setter
    def edges(self, new_edges: Edges):
        """Edges setter"""
        self.__edges = {}
        self._edges_validation(new_edges)

    @edges.deleter
    def edges(self):
        """Edges deleter"""
        raise CanNotDeleteBasicElementsInGraphException('edges')

    def _edges_validation(self, edges) -> Edges:
        """Validation function for directed edges"""

        def check_couple_type() -> None:
            """Checks that type of couple is Tuple"""
            if not all(isinstance(couple, Tuple) for couple in edges):
                raise WrongTypeOfCoupleException()

        def check_couple_len() -> None:
            """Checks that length of couple == 2"""
            if not all(len(couple) == 2 for couple in edges):
                raise WrongLengthOfCoupleException()

        def check_node_identifier_type() -> None:
            """Checks that type of node identifier in couple is Identifier"""
            if not all(
                    isinstance(node_l, Identifier) and isinstance(node_r, Identifier)
                    for (node_l, node_r) in edges):
                raise WrongTypeOfNodeIdentifierInCoupleException()

        def check_multiples_type() -> None:
            """Checks that type of multiple edges is Dict"""
            if not all(isinstance(multiples, Dict) for multiples in edges.values()):
                raise WrongTypeOfMultipleEdgesException()

        def check_multiples_len() -> None:
            """Checks that length of multiple edges more than 0"""
            if not all(len(multiples) > 0 for multiples in edges.values()):
                raise WrongLengthOfMultipleEdgesException()

        def check_edge_identifier_type():
            """Checks that type of edge identifier is Identifier"""
            for multiples in edges.values():
                if not all(
                        isinstance(edge_identifier, Identifier)
                        for edge_identifier in multiples.keys()):
                    raise WrongTypeOfEdgeIdentifierException()

        def check_edge_attributes_type():
            """Checks that type of edge attributes is Dict"""
            for multiples in edges.values():
                if not all(
                        isinstance(edge_attributes, Dict)
                        for edge_attributes in multiples.values()):
                    raise WrongTypeOfEdgeAttributesException()

        if edges is None:
            return

        if isinstance(edges, Dict):
            check_couple_type()
            check_couple_len()
            check_node_identifier_type()
            check_multiples_type()
            check_multiples_len()
            check_edge_identifier_type()
            check_edge_attributes_type()
            for (node_l, node_r), multiples in edges.items():
                if len(multiples) == 0:
                    self.add_edge(
                        node_l=node_l, node_r=node_r,
                        add_non_existent_incident_nodes=True,
                        recalculate_calculated_attributes=False)
                else:
                    for identifier, attributes in multiples.items():
                        try:
                            self.add_edge(
                                node_l=node_l, node_r=node_r, identifier=identifier,
                                add_non_existent_incident_nodes=True,
                                recalculate_calculated_attributes=False, **attributes)
                        except EdgeAlreadyExistsException as exc:
                            raise DuplicationInEdgeIdentifiersException(
                                node_l=node_l, node_r=node_r) from exc
        elif isinstance(edges, Iterable):
            check_couple_type()
            check_couple_len()
            check_node_identifier_type()
            for (node_l, node_r) in edges:
                self.add_edge(
                    node_l=node_l, node_r=node_r,
                    add_non_existent_incident_nodes=True,
                    recalculate_calculated_attributes=False)
        else:
            raise WrongTypeOfEdgesException()

    def __eq__(self, other):
        return type(self) is type(other) and \
            self.nodes == other.nodes and \
            self.edges == other.edges

    def __len__(self):
        """Returns the number of nodes in the graph"""
        return len(self.nodes)

    def add_node(
        self, identifier: Identifier = None, replace: bool = False,
        **attributes) -> Identifier:
        """Adds node to the graph

        Parameters
        ----------
        identifier, optional
            Node identifier
                - None (default): assigned an automatically generated identifier (UUID)
                - ...: assigned selected identifier
        replace, optional
            Replace existing node
                - False (default): raise NodeAlreadyExistsException if node exists
                - True: replace existing node by new
        attributes, optional
            Node attributes, calculated attributes added automatically with None values

        Returns
        -------
            Node identifier
        """

        # validate identifier
        if identifier is None:
            identifier = generate_identifier()
        else:
            if not isinstance(identifier, Identifier):
                raise WrongTypeOfNodeIdentifierException()

        # actions if (node exists)
        if self.nodes.get(identifier) is not None:
            if replace is False:
                raise NodeAlreadyExistsException()
            if replace is True:
                attributes['degree'] = self.nodes[identifier].get('degree')
                attributes['neighbors'] = self.nodes[identifier].get('neighbors')
        # actions if (node not exists)
        self.nodes[identifier] = attributes

        return identifier

    def del_node(
            self, identifier: Identifier,
            recalculate_calculated_attributes: bool = True) -> None:
        """Removes node from the graph

        Parameters
        ----------
        identifier
            Node identifier
        recalculate_calculated_attributes, optional
            Recalculate nodes attributes, that calculated by functions: calc_degree, calc_neighbors
                - True (deafult): recalculate calculated nodes attributes (worst performance)
                    * use it when removing a small number of nodes
                - False: do nothing (best performance)
                    * use it when removing a large number of nodes,
                      then recalculate calculated attributes
        """

        # delete incident edges
        incident_edges = [
            couple for couple in self.edges.keys()
            if identifier in couple]
        for couple in incident_edges:
            self.del_edge(*couple, recalculate_calculated_attributes=False)

        # delete node
        del self.nodes[identifier]

        # recalculate calculated attributes
        if recalculate_calculated_attributes is True:
            self.calc_degree()
            self.calc_neighbors()

    def clear_nodes(self) -> None:
        """Removes all nodes from the graph"""
        self.nodes = {}

    @abstractmethod
    def _couple_representation(
            self, couple: Tuple[Identifier, Identifier]
            ) -> Tuple[Identifier, Identifier]:
        """Couple representation for different graph types"""

    def add_edge(
            self, node_l: Identifier, node_r: Identifier,
            identifier: Identifier = None, replace: bool = False,
            add_non_existent_incident_nodes: bool = True,
            recalculate_calculated_attributes: bool = True,
            **attributes) -> Identifier:
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
        recalculate_calculated_attributes, optional
            Recalculate nodes attributes, that calculated by functions: calc_degree, calc_neighbors
                - True (deafult): recalculate calculated nodes attributes (worst performance)
                    * use it when adding a small number of edges
                - False: do nothing (best performance)
                    * use it when adding a large number of edges,
                      then recalculate calculated attributes

        Returns
        -------
            Edge identifier
        """
        # couple representation
        couple = self._couple_representation((node_l, node_r))

        # validate identifier
        if identifier is None:
            identifier = generate_identifier()

        # actions if (edge exists) and (replace is True)
        if self.edges.get(couple) is not None and \
                self.edges.get(couple).get(identifier) is not None:
            if replace is False:
                raise EdgeAlreadyExistsException()
        # actions if (edge not exists) or (edge exists and replace is True)
        self.edges[couple] = self.edges.get(couple) or {}
        self.edges[couple][identifier] = attributes

        # add non-existent incident nodes
        if add_non_existent_incident_nodes is True:
            try:
                self.add_node(node_l, replace=False)
            except NodeAlreadyExistsException:
                pass
            try:
                self.add_node(node_r, replace=False)
            except NodeAlreadyExistsException:
                pass

        # recalculate calculated values
        if recalculate_calculated_attributes is True:
            self.calc_degree()
            self.calc_neighbors()

        return identifier

    def del_edge(
            self, node_l: Identifier, node_r: Identifier,
            identifier: Identifier = None,
            recalculate_calculated_attributes: bool = True) -> None:
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
        recalculate_calculated_attributes, optional
            Recalculate nodes attributes, that calculated by functions: calc_degree, calc_neighbors
                - True (deafult): recalculate calculated nodes attributes (worst performance)
                    * use it when removing a small number of edges
                - False: do nothing (best performance)
                    * use it when removing a large number of edges,
                      then recalculate calculated attributes
        """

        # couple representation
        couple = self._couple_representation((node_l, node_r))

        # delete edges
        if identifier is None:
            del self.edges[couple]
        else:
            del self.edges[couple][identifier]

        # clear calculated attributes
        if recalculate_calculated_attributes is True:
            self.calc_degree()
            self.calc_neighbors()

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

        # intersection of selected nodes and existing nodes
        selected_nodes = set(selected_nodes) & set(self.nodes.keys())

        # initialise subgraph
        subgraph = self.__class__()

        def _condition(fullmatch, node_l, node_r):
            if fullmatch is True:
                return (node_l in selected_nodes) and (node_r in selected_nodes)
            return (node_l in selected_nodes) or (node_r in selected_nodes)

        # fill subgraph by nodes and edges
        for (node_l, node_r), multiples in self.edges.items():
            if _condition(fullmatch, node_l, node_r):
                for edge_identifier, edge_attributes in multiples.items():
                    subgraph.add_edge(
                        node_l=node_l, node_r=node_r, identifier=edge_identifier,
                        add_non_existent_incident_nodes=False,
                        recalculate_calculated_attributes=False, **edge_attributes)
                    try:
                        subgraph.add_node(
                            identifier=node_l, replace=False,
                            recalculate_calculated_attributes=False, **self.nodes[node_l])
                    except NodeAlreadyExistsException:
                        pass
                    try:
                        subgraph.add_node(
                            identifier=node_r, replace=False,
                            recalculate_calculated_attributes=False, **self.nodes[node_r])
                    except NodeAlreadyExistsException:
                        pass

        # recalculate calculated attributes
        subgraph.calc_degree()
        subgraph.calc_neighbors()

        return subgraph

    def calc_degree(self):
        """Calculate degree for each node in graph"""
        for node in self.nodes.keys():
            self.nodes[node]['degree'] = 0

        for (node_l, node_r), multiples in self.edges.items():
            self.nodes[node_l]['degree'] += len(multiples)
            self.nodes[node_r]['degree'] += len(multiples)

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

    def _is_complete(self):
        """Checks that graph is complete"""
        edges_lenght = len({
            (node_l, node_r) for (node_l, node_r) in self.edges.keys()
            if node_l != node_r})
        max_edges_legth = (len(self.nodes) * (len(self.nodes) - 1)) / 2
        return edges_lenght == max_edges_legth

    def _is_connected(self):
        """Checks that graph is conncted"""
        return NotImplemented

    def _is_pseudo(self):
        """Checks that graph is pseudograph"""
        return any(self.find_loops())

    def _is_multi(self):
        """Checks that graph is multigraph"""
        return any(len(multiples) > 1 for multiples in self.edges.values())

    def describe(self):
        """Returns information about graph"""
        self.calc_degree()
        self.calc_neighbors()
        return {
            'type': self.__class__,
            'number_of_nodes': len(self.nodes),
            'number_of_edges': len(self.edges),
            'multi_graph': self._is_multi(),
            'pseudo_graph': self._is_pseudo(),
            'connected_graph': self._is_connected(),
            'complete_graph': self._is_complete(),
        }
