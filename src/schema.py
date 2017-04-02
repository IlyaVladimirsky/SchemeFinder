from copy import copy

import itertools

BOOL_COMBINATIONS = {}


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
    is_node = True

    def __init__(self, function, in_count, parent=None, children=None):
        self.function = function
        self.parent = parent
        self.children = children or [None for _ in range(in_count)]

    def __contains__(self, node):
        return any(node is n for n in self)

    def __copy__(self):
        return Node(
            function=self.function,
            in_count=-1,  # not needed as children passed
            parent=self.parent,
            children=[copy(chi) for chi in self.children]
        )

    def __iter__(self):
        for child_iter in (iter(child) for child in self.children if isinstance(child, Node)):
            for c in child_iter:
                yield c

        yield self

    def __str__(self):
        return \
            (self.function.__name__[0] + str(len(self.children))).join('(' + str(c) + ')' for c in self.children) \
            if self.function.__name__ != 'negation' \
            else '{' + str(self.children[0]) + '}'

    def __repr__(self):
        return str(self)

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
            if child.is_node:
                bool_args.append(child.calculate())
            else:
                bool_args.append(child.value)

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
        root_copy = copy(self.root)

        return Schema(root_copy)

    def __iter__(self):
        return iter(self.root)

    def __repr__(self):
        return str(self.root)

    def connect_vars(self, varset):
        # if self.free_wares_count != len(varset):
        #     raise WrongInputCountException

        varset = list(varset)
        for i, node in self.root.free_wires():
            node.children[i] = varset.pop(0)

    def calculate(self):
        return self.root.calculate()

    def get_derivatives(self, basis, boolvars):
        for base_node in basis:
            ins_count = len(base_node.children)
            varsets = BOOL_COMBINATIONS.get(
                str(ins_count),
                list(itertools.combinations(boolvars, ins_count))  # == var^ins
            )

            for i, node in self.root.free_wires():
                for varset in varsets:
                    previous = node.children[i]

                    node.children[i] = base_node
                    node.children[i].children = list(varset)

                    yield copy(self)

                    node.children[i] = previous
