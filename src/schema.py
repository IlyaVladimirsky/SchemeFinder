import types
from copy import deepcopy

from src.bool_var import BoolVar


class NodeException(Exception):
    pass


class ExcessChildException(NodeException):
    pass


class AlreadyContainsNodeException(NodeException):
    pass


class WrongCalculatedTypesException(NodeException):
    pass


class SchemaException(Exception):
    pass


class WrongInputCountException(SchemaException):
    pass


class Node:
    def __init__(self, operation, parent=None, children=None):
        self.function = types.MethodType(operation.func, self)
        self.parent = parent
        self.children = children or [None for _ in range(operation.in_count)]

    def __contains__(self, node):
        return any(node is n for n in self)

    def __iter__(self):
        for child_iter in (iter(child) for child in self.children if isinstance(child, Node)):
            for c in child_iter:
                yield c

        yield self

    def add_child(self, node):
        if node in self:
            raise AlreadyContainsNodeException

        for i, e in enumerate(self.children):
            if not isinstance(e, Node):
                self.children.pop(i)

                node.parent = self
                self.children.insert(i, node)

                return

        raise ExcessChildException

    def calculate(self):
        bool_args = []

        for child in self.children:
            if isinstance(child, Node):
                bool_args.append(child.calculate())
            elif isinstance(child, BoolVar):
                bool_args.append(child.value)
            else:
                raise WrongCalculatedTypesException

        return self.function(*bool_args)

    def free_wires(self):
        for node in self:
            for i, child in enumerate(node.children):
                if not isinstance(child, Node):
                    yield i, node


class Schema:
    @property
    def free_wares_count(self):
        return sum(1 for _, _ in self.root.free_wires())

    def __init__(self, node):
        self.root = node

    def __contains__(self, node):
        return node in self.root

    def __copy__(self):
        root_copy = deepcopy(self.root)

        return Schema(root_copy)

    def __iter__(self):
        return iter(self.root)

    def connect_vars(self, bool_vars):
        if self.free_wares_count != len(bool_vars):
            raise WrongInputCountException

        for i, node in self.root.free_wires():
            node.children[i] = bool_vars.pop(0)

    def calculate(self):
        return self.root.calculate()

    # def get_derivatives(self, basis):
    #     for base_node in basis:
    #         for node in self:
    #             for i, child in enumerate(node.children):
    #                 if not isinstance(child, Node):
    #                     node.children[i] = deepcopy(base_node)
    #                     derivative = copy(self)
    #                     node.children[i] = None
