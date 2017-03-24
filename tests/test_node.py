import unittest
from copy import deepcopy

from src.operations import Operation
from src.schema import Node, ExcessChildException, AlreadyContainsNodeException
from src.wire import Wire


class TestNode(unittest.TestCase):
    def setUp(self):
        conj = Operation('conjunction', 2)

        self.root = Node(conj)
        self.node_1 = Node(conj, parent=self.root)
        self.node_2 = Node(conj, parent=self.root)
        self.root.children = [self.node_1, self.node_2]

    def test_contains(self):
        self.assertTrue(self.root in self.root, 'root not in root')
        self.assertTrue(self.node_2 in self.root, 'node_2 not in root')

    def test_iter(self):
        self.node_2.children[0] = self.node_1
        self.assertTrue([self.node_1, self.node_1, self.node_2, self.root] == list(self.root))

    def test_indices(self):
        self.node_1.children[1] = Wire(value=True, label=5)

        self.assertTrue(self.root[5].value)
        self.assertIsNone(self.root[-1].value)

        with self.assertRaises(IndexError):
            self.root[-5]

    def test_add_child(self):
        with self.assertRaises(AlreadyContainsNodeException):
            self.root.add_child(self.node_1)

        with self.assertRaises(ExcessChildException):
            self.root.add_child(deepcopy(self.node_1))

        copied_node = deepcopy(self.node_2)
        self.node_1.add_child(copied_node)
        self.assertTrue(copied_node in self.node_1)

    def test_free_wires(self):
        self.assertTrue(all(not wire.value for wire in self.root.free_wires))
