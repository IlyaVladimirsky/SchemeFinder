import unittest
from copy import deepcopy, copy

from src.bool_var import BoolVar
from src.operations import Operation
from src.schema import Node, ExcessChildException, AlreadyContainsNodeException


class TestNode(unittest.TestCase):
    def setUp(self):
        conj = Operation('conjunction', 2)

        self.root = Node(conj.func, conj.in_count)
        self.node_1 = Node(conj.func, conj.in_count, parent=self.root)
        self.node_2 = Node(conj.func, conj.in_count, parent=self.root)
        self.root.children = [self.node_1, self.node_2]

        self.x1 = BoolVar(1)
        self.x2 = BoolVar(2)
        self.x3 = BoolVar(3)

    def test_contains(self):
        self.assertTrue(self.root in self.root, 'root not in root')
        self.assertTrue(self.node_2 in self.root, 'node_2 not in root')

    def test_eq(self):
        self.assertTrue(self.root == self.node_1)

    def test_copy(self):
        self.node_1.children[0] = self.x1
        self.node_2.children[0] = self.x2
        self.node_2.children[1] = self.x3
        self.node_1.children[1] = self.node_2

        c = copy(self.node_1)

        self.assertIsNot(c, self.node_1)
        self.assertIsNot(c.children[1], self.node_2)
        self.assertIs(c.children[0], self.x1)
        self.assertIs(c.children[1].children[0], self.x2)
        self.assertIs(c.children[1].children[1], self.x3)

    def test_iter(self):
        self.node_2.children[0] = self.node_1
        self.assertTrue([self.node_1, self.node_1, self.node_2, self.root] == list(self.root))

    def test_add_child(self):
        with self.assertRaises(AlreadyContainsNodeException):
            self.root.add_child(self.node_1)

        with self.assertRaises(ExcessChildException):
            self.root.add_child(deepcopy(self.node_1))

        copied_node = deepcopy(self.node_2)
        self.node_1.add_child(copied_node)
        self.assertTrue(copied_node in self.node_1)

    def test_free_wires(self):
        self.assertEqual(sum(1 for i, node in self.root.free_wires()), 4)

        self.assertTrue(all(node in [self.node_1, self.node_2] for i, node in self.root.free_wires()))

    def test_create_node_from_str(self):
        created = Node.init('(x2)con2(((x1)con2(x2))con2({x2}con2(x3)))', [self.x1, self.x2, self.x3])

        self.assertEqual(str(created), '(x2)con2(((x1)con2(x2))con2({x2}con2(x3)))')
