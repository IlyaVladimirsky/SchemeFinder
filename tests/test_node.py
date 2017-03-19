import unittest

from src.operations import Operation
from src.schema import Node


class TestNode(unittest.TestCase):
    def test_contains(self):
        conj = Operation('conjunction', 2)
        root = Node(conj)
        node_1 = Node(conj, parent=root)
        node_2 = Node(conj, parent=root)
        root.children = [node_1, node_2]

        self.assertTrue(root in root, 'node_2 not in root')
        self.assertTrue(node_2 in root, 'node_2 not in root')
