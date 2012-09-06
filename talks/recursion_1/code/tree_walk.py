#!/usr/bin/env python

"""
Recursive tree walk example.

Usage: tree_walk
"""

class Node(object):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

Tree = Node(value=7)
Tree.left = Node(value=3)
Tree.left.left = Node(value=2)
Tree.left.right = Node(value=5)
Tree.left.right.left = Node(value=4)
Tree.left.right.right = Node(value=6)
Tree.right = Node(value=8)
Tree.right.right = Node(value=9)


def walk_inorder(node):
    """Walk through a node in 'inorder' fashion."""

    if node:
        walk_inorder(node.left)
        print node.value,
        walk_inorder(node.right)

def walk_preorder(node):
    """Walk through a node in 'preorder' fashion."""

    if node:
        print node.value,
        walk_preorder(node.left)
        walk_preorder(node.right)

def walk_postorder(node):
    """Walk through a node in 'postorder' fashion."""

    if node:
        walk_postorder(node.left)
        walk_postorder(node.right)
        print node.value,


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 1:
        print __doc__
        sys.exit(10)

    print 'Tree:'
    print '  inorder:',
    walk_inorder(Tree)
    print

    print ' preorder:',
    walk_preorder(Tree)
    print

    print 'postorder:',
    walk_postorder(Tree)
    print

