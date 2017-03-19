import unittest
from copy import copy, deepcopy

from src.bool_var import BoolVar
from src.operations import Operation
from src.schema import Node, Schema, WrongInputCountException


class TestSchema(unittest.TestCase):
    def setUp(self):
        conj = Operation('conjunction', 2)
        self.root = Node(conj)
        self.node_1 = Node(conj)
        self.node_2 = Node(conj)

        self.schema = Schema(self.root)
        self.schema.add_node(self.root, self.node_1)
        self.schema.add_node(self.root, self.node_2)

        self.x1 = BoolVar(1)
        self.x2 = BoolVar(2)
        self.x3 = BoolVar(3)

    def test_copy(self):
        schema_copy = copy(self.schema)

        self.assertTrue(self.root not in schema_copy)
        self.assertTrue(self.node_1 not in schema_copy)
        self.assertTrue(self.node_2 not in schema_copy)

    def test_free_wares(self):
        self.assertTrue(self.schema.free_wares_count() == 4)

    def test_connect_vars(self):
        with self.assertRaises(WrongInputCountException):
            self.schema.connect_vars([])

        copied_node = deepcopy(self.node_1)
        self.node_2.children[0] = copied_node

        self.schema.connect_vars([self.x1, self.x2, self.x3, self.x1, self.x2])

        self.assertTrue(self.node_1.children == [self.x1, self.x2])
        self.assertTrue(copied_node.children == [self.x3, self.x1])
        self.assertTrue(self.node_2.children[1] == self.x2)
