"""Type alias and descriptor for nodes"""

from typing import TypeAlias, Any, Dict, Iterable
from connections.core.identifier import Identifier


Nodes: TypeAlias = Dict[Identifier, Any]


# class NodesDescriptor:
#     """Nodes descriptor"""

#     @staticmethod
#     def nodes_validation(nodes) -> Nodes:
#         """Validation function for nodes

#         Nodes representation is a dict with:
#             - keys: node identifier
#             - values: node attributes

#         Nodes representation example:
#             {
#                 'Elizabeth': {'age': 19, 'sex': False},
#                 'Sebastian': {'age': 21, 'sex': True},
#             }
#         """

#         def _check_node_keys_type() -> bool:
#             """Checks that type of 'Elizabeth' is Identifier"""
#             if not all(isinstance(node, Identifier) for node in nodes):
#                 raise Exception()

#         def _check_node_values_type() -> bool:
#             """Checks that type of {'age': 19, 'sex': False} is dict"""
#             if not all(isinstance(values, Dict) for values in nodes.values()):
#                 raise Exception()

#         if isinstance(nodes, Dict):
#             _check_node_keys_type()
#             _check_node_values_type()
#             return nodes
#         if isinstance(nodes, Iterable):
#             _check_node_keys_type()
#             return {node: {} for node in nodes}
#         raise TypeError()

#     def __set_name__(self, owner, name):
#         self._name = f'_{name}'

#     def __get__(self, instance, owner):
#         return getattr(instance, self._name)

#     def __set__(self, instance, value):
#         setattr(instance, self._name, self.nodes_validation(value))

#     def __delete__(self, instance) -> None:
#         raise Exception()
