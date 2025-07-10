from blib2to3.pgen2 import token
from blib2to3.pygram import python_symbols as syms
from blib2to3.pytree import Leaf, Node

# copy of lib2to3.fixer_util

def Assign(target, source):
    """Build an assignment statement"""
    if not isinstance(target, list):
        target = [target]
    if not isinstance(source, list):
        source.prefix = " "
        source = [source]

    return Node(syms.atom,
                target + [Leaf(token.EQUAL, "=", prefix=" ")] + source)
def Name(name, prefix=None):
    """Return a NAME leaf"""
    return Leaf(token.NAME, name, prefix=prefix)
def Newline():
    """A newline literal"""
    return Leaf(token.NEWLINE, "\n")

