import unittest
from copy import deepcopy, copy

from src.operations import Operation
from src.schema import Node, ExcessChildException, AlreadyContainsNodeException


class TestNode(unittest.TestCase):
    def setUp(self):
        conj = Operation('conjunction', 2)

        self.root = Node(conj)
        self.node_1 = Node(conj, parent=self.root, mark=1)
        self.node_2 = Node(conj, parent=self.root, mark=2)
        self.root.children = [self.node_1, self.node_2]

    def test_contains(self):
        self.assertTrue(self.root in self.root, 'root not in root')
        self.assertTrue(self.node_2 in self.root, 'node_2 not in root')

    def test_iter(self):
        self.node_2.children[0] = self.node_1
        self.assertTrue([self.node_1, self.node_1, self.node_2, self.root] == list(self.root))

    def test_indices(self):
        self.assertTrue(self.root[1] is self.node_1)

        with self.assertRaises(IndexError):
            self.root[-1], self.root[3]

    def test_add_child(self):
        with self.assertRaises(AlreadyContainsNodeException):
            self.root.add_child(self.node_1)

        with self.assertRaises(ExcessChildException):
            self.root.add_child(deepcopy(self.node_1))

        copied_node = deepcopy(self.node_2)
        self.node_1.add_child(copied_node)
        self.assertTrue(copied_node in self.node_1)
