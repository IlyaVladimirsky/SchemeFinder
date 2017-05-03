from copy import copy

import re

from src.bool_var import BoolVar
from src.operations import operations


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

    @classmethod
    def init(cls, node_str, boolvars):
        created_nodes = {}
        subnode_pattern = re.compile('(\(|{)x*\d(\)|})\w{3}(\(|{)x*\d(\)|})')
        subnode_counter = 0
        subnode_matches = list(subnode_pattern.finditer(node_str))

        while len(subnode_matches):
            for match in subnode_matches:
                subnode_str = match.group()

                func_pattern = re.compile('(\)|})(\w{3}(\(|{))+')
                str_op = func_pattern.search(subnode_str).group()[1:-1]
                operation = next(v for k, v in operations.items() if k.startswith(str_op[:3]))

                children = subnode_str.split(str_op)
                in_count = len(children)
                node = Node(operation, in_count)

                for j, c in enumerate(children):
                    var = re.search('x\d', c)
                    if var:
                        chi = next(x for x in boolvars if x == BoolVar(int(var.group()[1])))
                    else:
                        subnode_numb = str(re.search('\d', c).group())
                        chi = copy(created_nodes[subnode_numb])

                    node.children[j] = Node(operations['negation'], 1, children=[chi]) if c.startswith('{') else chi

                created_nodes[str(subnode_counter)] = node
                node_str = node_str.replace(subnode_str, str(subnode_counter))

                subnode_counter += 1

            subnode_matches = list(subnode_pattern.finditer(node_str))

        return node

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

    def __eq__(self, other):
        return self.function == other.function and len(self.children) == len(self.children)

    def __iter__(self):
        for child_iter in (iter(child) for child in self.children if isinstance(child, Node)):
            for c in child_iter:
                yield c

        yield self

    def __str__(self):
        return \
            (self.function.__name__[:3]) \
                .join(
                    '{' + str(self.children[0]) + '}'
                    if self.is_node and self.function.__name__ == 'negation'
                    else str(c) if c.is_node and c.function.__name__ == 'negation' else '(' + str(c) + ')'
                    for c in self.children
                )

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
    @classmethod
    def init(cls, str_schema, boolvars):
        return Schema(Node.init(str_schema, boolvars))

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

    def get_derivatives(self, basis):
        for base_node in basis:
            used_nodes = []

            for i, node in self.root.free_wires():
                if any(node is used for used in used_nodes):
                    continue

                node.children[i] = copy(base_node)
                derivative = copy(self)
                node.children[i] = None

                used_nodes.append(node)

                yield derivative
