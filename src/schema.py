import types
from copy import deepcopy


class NodeException(BaseException):
    pass


class ExcessChildException(NodeException):
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
        for i, e in enumerate(self.children):
            if not e:
                self.children.pop(i)
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

    def add_node(self, node, mark):
        self.root[mark].add_child(node)
