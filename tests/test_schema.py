import unittest
from copy import copy

from src.operations import Operation
from src.schema import Node, Schema


class TestSchema(unittest.TestCase):
    def setUp(self):
        conj = Operation('conjunction', 2)
        self.root = Node(conj)
        self.node_1 = Node(conj)
        self.node_2 = Node(conj)

        self.schema = Schema(self.root)
        self.schema.add_node(self.root, self.node_1)
        self.schema.add_node(self.root, self.node_2)

    def test_copy(self):
        schema_copy = copy(self.schema)

        self.assertTrue(self.root not in schema_copy)
        self.assertTrue(self.node_1 not in schema_copy)
        self.assertTrue(self.node_2 not in schema_copy)

    def test_free_wares(self):
        self.assertTrue(self.schema.free_wares_count() == 4)
