from copy import deepcopy


class Node:
    def __init__(self, function, parent=None, children=None, mark=0):
        self.function = function
        self.parent = parent
        self.children = children or []
        self.mark = mark

    def max_mark(self):
        if not self.children:
            return self.mark
        else:
            return max(node.max_mark() for node in self.children)


class Schema:
    def __init__(self, node):
        self.root = node
        self.counter = node.max_mark() + 1

    def __copy__(self):
        root_copy = deepcopy(self.root)

        return Schema(root_copy)
