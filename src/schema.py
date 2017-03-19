import types
from copy import deepcopy


class NodeException(BaseException):
    pass


class ExcessChildException(NodeException):
    pass


class AlreadyContainsNodeException(NodeException):
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
                    return next(getnode(child, i) for child in node.children if child)
                except StopIteration:
                    return None

        result = getnode(self, index)

        if not result:
            raise IndexError

        return result

    def __contains__(self, node):
        return any(node == n for n in self)

    def __iter__(self):
        yield self

        for child_iter in (iter(child) for child in self.children if child):
            for c in child_iter:
                yield c

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

    def calculate_schema(self, input_array):
        if self.free_wares_count() != len(input_array):
            raise WrongInputCountException
