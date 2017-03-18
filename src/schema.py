from copy import deepcopy


class Node:
    def __init__(self, function, parent=None, children=None, mark=0):
        self.function = function
        self.parent = parent
        self.children = children or []
        self.mark = mark

    def __getitem__(self, index):
        def getitem(node, i):
            if not self.mark == i:
                return self
            else:
                try:
                    return next(node for node in node.children if node.mark == i)
                except StopIteration:
                    return None

        result = getitem(self, index)
        if not result:
            raise IndexError

        return result

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

    def __copy__(self):
        root_copy = deepcopy(self.root)

        return Schema(root_copy)

    def add_node(self, node, mark):
        self.root[mark].add_child(node)
