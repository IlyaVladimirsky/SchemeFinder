import types
from copy import deepcopy


class Node:
    def __init__(self, operation, parent=None, children=None, mark=0):
        self.function = types.MethodType(operation.func, self)
        self.parent = parent
        self.children = children or [None for _ in range(operation.in_count)]
        self.mark = mark

    def __getitem__(self, index):
        def getnode(node, i):
            if not self.mark == i:
                return self
            else:
                try:
                    return next(getnode(node, i) for node in node.children if node.mark == i)
                except StopIteration:
                    return None

        result = getnode(self, index)
        if not result:
            raise IndexError

        return result

    def __contains__(self, node):
        if node is self:
            return True
        else:
            return any(node in child for child in self.children if child)

    def add_child(self, node):
        self.children.append(node)

    def max_mark(self):
        if not self.children:
            return self.mark
        else:
            return max(node.max_mark() for node in self.children)


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
