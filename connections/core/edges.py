"""Type alias and descriptors for edges"""

from typing import TypeAlias, Any, Dict, Tuple, Iterable
from connections.core.identifier import Identifier


Edges: TypeAlias = Dict[
    Tuple[Identifier, Identifier],
    Dict[Identifier, Dict[str, Any]]
]


class DirectedEdgesDescriptor:
    """Directed edges descriptor"""

    def __init__(self, nodes):
        self.nodes = nodes

    @staticmethod
    def directed_edges_validation(edges, nodes) -> Edges:
        """Validation function for directed edges

        Edges representation is a dict with:
            - keys: a tuple with two nodes identifier
            - values (same as in UndirectedGraph): a dict with:
                - keys: edge identifier
                - values: edge attributes

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

        def _check_edge_keys_type():
            """Checks that type of ('Sebastian', 'Elizabeth') is tuple"""
            return all(isinstance(edge, Tuple) for edge in edges)

        def _check_edge_keys_len():
            """Checks that len of ('Sebastian', 'Elizabeth') == 2"""
            return all(len(edge) == 2 for edge in edges)

        def _check_edge_keys_items_type():
            """Checks that type of 'Sebastian' is Identifier"""
            return all(
                isinstance(node_l, Identifier) and isinstance(node_r, Identifier)
                for (node_l, node_r) in edges)

        def _check_edge_keys_items_in_nodes(nodes):
            """Checks that 'Sebastian' and 'Elizabeth' in nodes"""
            return all(
                (node_l in nodes) and (node_r in nodes)
                for (node_l, node_r) in edges)

        def _check_edge_values_type():
            """Checks that type of edge values is dict"""
            return all(isinstance(values, Dict) for values in edges.values())

        def _check_edge_values_keys_type():
            """Checks that type os edge values keys is Identifier"""

        def _check_edge_values_values_type():
            """Checks that type os edge values values is dict"""

        if isinstance(edges, Dict):
            if _check_edge_keys_type() and _check_edge_keys_len() and \
                    _check_edge_keys_items_type() and \
                    _check_edge_values_type() and \
                    _check_edge_keys_items_in_nodes(nodes):
                return edges
            raise Exception()
        if isinstance(edges, Iterable):
            if _check_edge_keys_type() and _check_edge_keys_len() and \
                    _check_edge_keys_items_type():
                return {edge: {} for edge in edges}
            raise Exception()
        raise Exception()

    def __set_name__(self, owner, name):
        self._name = f'_{name}'

    def __get__(self, instance, owner):
        return getattr(instance, self._name)

    def __set__(self, instance, edges):
        setattr(instance, self._name, self.directed_edges_validation(edges, self.nodes))

    def __delete__(self, instance) -> None:
        raise Exception('HAHAHA!')


# class UndirectedEdgesDescriptor:
#     """Undirected edges descriptor"""

#     @staticmethod
#     def undirected_edges_validation(edges) -> Edges:
#         """Validation function for undirected edges

#         Edges representation is a dict with:
#             - keys: a sorted tuple with two nodes identifier
#             - values (same as in UndirectedGraph): a dict with:
#                 - keys: edge identifier
#                 - values: edge attributes

#         Edges representation example:
#             {
#                 ('Elizabeth', 'Sebastian'): {
#                     '46f893e': {'amount': 1400, 'date': '2024-03-08'},
#                     '206ij5s': {'amount': 2700, 'date': '2024-07-23'},
#                     '239af58': {'amount': 1900, 'date': '2024-04-16'},
#                 },
#             }
#         """

#     def __set_name__(self, owner, name):
#         self._name = f'_{name}'

#     def __get__(self, instance, owner):
#         return getattr(instance, self._name)

#     def __set__(self, instance, value):
#         setattr(instance, self._name, self.undirected_edges_validation(value))

#     def __delete__(self, instance) -> None:
#         raise Exception('HAHAHA!')
