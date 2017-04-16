import unittest
from copy import copy, deepcopy

from src.bool_var import BoolVar
from src.operations import Operation
from src.schema import Node, Schema, WrongInputCountException, WrongCalculatedTypesException


class TestSchema(unittest.TestCase):
    def setUp(self):
        self.conj = Operation('conjunction', 2)
        self.disj = Operation('disjunction', 2)
        self.neg = Operation('negation', 1)

        self.root = Node(self.conj.func, self.conj.in_count)
        self.node_1 = Node(self.conj.func, self.conj.in_count)
        self.node_2 = Node(self.conj.func, self.conj.in_count)

        self.schema = Schema(self.root)
        self.root.add_child(self.node_1)
        self.root.add_child(self.node_2)

        self.x1 = BoolVar(1)
        self.x2 = BoolVar(2)
        self.x3 = BoolVar(3)

    def test_copy(self):
        schema_copy = copy(self.schema)

        self.assertTrue(self.root not in schema_copy)
        self.assertTrue(self.node_1 not in schema_copy)
        self.assertTrue(self.node_2 not in schema_copy)

    def test_free_wares(self):
        self.assertTrue(self.schema.free_wares_count == 4)

    def test_connect_vars(self):
        # with self.assertRaises(WrongInputCountException):
        #     self.schema.connect_vars([])

        copied_node = deepcopy(self.node_1)
        self.node_2.children[0] = copied_node

        self.schema.connect_vars([self.x1, self.x2, self.x3, self.x1, self.x2])

        self.assertTrue(self.node_1.children == [self.x1, self.x2])
        self.assertTrue(copied_node.children == [self.x3, self.x1])
        self.assertTrue(self.node_2.children[1] == self.x2)

    def test_calculate(self):
        # with self.assertRaises(WrongCalculatedTypesException):
        #     self.schema.calculate()

        self.schema.connect_vars([self.x1, self.x2, self.x3, self.x1])

        self.x1.value, self.x2.value, self.x3.value = True, True, True
        self.assertTrue(self.schema.calculate())

        self.x1.value, self.x2.value, self.x3.value = True, True, False
        self.assertFalse(self.schema.calculate())

        self.x1.value, self.x2.value, self.x3.value = True, False, True
        self.assertFalse(self.schema.calculate())

    def test_derivatives(self):
        basis = [self.conj, self.disj]

        self.assertEqual(sum(1 for _ in self.schema.get_derivatives(basis)), 2)
