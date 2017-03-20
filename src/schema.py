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
    def __init__(self, operation, parent=None, children=None, mark=0):
        self.function = types.MethodType(operation.func, self)
        self.parent = parent
        self.children = children or [None for _ in range(operation.in_count)]
        self.mark = mark

    def __getitem__(self, index):
        def getnode(node, i):
            if node.mark == i:
                return node
            else:
                try:
                    return next(getnode(child, i) for child in node.children if isinstance(child, Node))
                except StopIteration:
                    return None

        result = getnode(self, index)

        if not result:
            raise IndexError

        return result

    def __contains__(self, node):
        return any(node == n for n in self)

    def __iter__(self):
        for child_iter in (iter(child) for child in self.children if isinstance(child, Node)):
            for c in child_iter:
                yield c

        yield self

    def add_child(self, node):
        if node in self:
            raise AlreadyContainsNodeException

        for i, e in enumerate(self.children):
            if not e:
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

    def max_mark(self):
        return max(n.mark for n in self)


class Schema:
    def __init__(self, node):
        self.root = node
        self.counter = node.max_mark() + 1

    def __contains__(self, node):
        return node in self.root

    def __copy__(self):
        root_copy = deepcopy(self.root)

        return Schema(root_copy)

    def __iter__(self):
        return iter(self.root)

    def add_node(self, parent_node, child_node):
        child_node.mark = self.counter
        self.counter += 1

        self.root[parent_node.mark].add_child(child_node)

    def free_wares_count(self):
        return sum(1 for node in self for child in node.children if not child)

    def connect_vars(self, bool_vars):
        if self.free_wares_count() != len(bool_vars):
            raise WrongInputCountException

        for node in self:
            for i, child in enumerate(node.children):
                if not isinstance(child, Node):
                    node.children[i] = bool_vars.pop(0)

    def calculate(self):
        return self.root.calculate()
