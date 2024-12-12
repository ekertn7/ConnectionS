"""Type alias for nodes"""

from typing import TypeAlias, Any, Dict
from connections.core.identifier import Identifier


Nodes: TypeAlias = Dict[Identifier, Any]


# class NodesDescriptor:
#     """Nodes descriptor"""

#     # def __init__(self):
#     #     self.result = {}

#     # def add_node(self, identifier: Identifier, **kwargs):
#     #     """Adds node to result"""
#     #     self.result[identifier] = kwargs

#     def nodes_validation(self, nodes) -> Nodes:
#         """Validation function for nodes"""
#         def _check_node_keys_type() -> bool:
#             """Checks that type of 'Elizabeth' is Identifier"""
#             return all(isinstance(node, Identifier) for node in nodes)

#         def _check_node_values_type() -> bool:
#             """Checks that type of {'age': 19, 'sex': False} is dict"""
#             return all(isinstance(values, Dict) for values in nodes.values())

#         if isinstance(nodes, Dict):
#             if not _check_node_keys_type():
#                 raise TypeError()
#             if not _check_node_values_type():
#                 raise TypeError()
#             return nodes
#         if isinstance(nodes, Iterable):
#             if not _check_node_keys_type():
#                 raise TypeError()
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
