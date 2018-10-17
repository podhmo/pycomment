from pycomment.parse import (
    parse_string,
    PyTreeVisitor,
    type_repr,
)
from lib2to3.pgen2 import token
from lib2to3.fixer_util import Assign, Name, Newline

# utf8 's PUA(https://en.wikipedia.org/wiki/Private_Use_Areas)
SEP = "\U000F0000"

SEP_MARKER = "ZZ{}ZZ".format(SEP)
COMMENT_MARKER = "# =>"


def transform_string(source: str):
    t = parse_string(source)
    return transform(t)


def transform_file(fname: str):
    with open(fname) as rf:
        return transform_string(rf.read())


def transform(node):
    t = Transformer()
    t.transform(node)
    return node


class Transformer(PyTreeVisitor):
    marker = COMMENT_MARKER

    def visit_NEWLINE(self, node):
        if node.prefix.lstrip().startswith(self.marker):
            # MEMO: <expr> -> _ = <expr>
            target = node
            while True:
                parent = target.parent
                if parent is None:
                    return

                if type_repr(target.parent.type) == "simple_stmt":
                    break
                target = parent

            eol = target  # target is Leaf("\n]")
            target = eol.prev_sibling

            cloned = target.clone()
            cloned.parent = None

            assigned = Assign(Name("_"), cloned)
            assigned.prefix = target.prefix
            target.replace(assigned)

            # MEMO: adding print(SEP_MARKER, _, SEP_MARKER, sep="\n")
            this_stmt = eol.parent
            print_stmt = this_stmt.clone()
            print_stmt.children = []
            print_stmt.append_child(
                Name(
                    "print({ms!r}, repr(_), {me!r}, sep='')".format(
                        ms="{}{}:".format(SEP_MARKER, node.get_lineno()), me=SEP_MARKER
                    )
                )
            )

            print_stmt.prefix = assigned.prefix
            # xxx: for first line
            if not print_stmt.prefix:
                prev_line = assigned.parent.prev_sibling
                if prev_line is not None and prev_line.type == token.INDENT:
                    print_stmt.prefix = prev_line.value

            print_stmt.append_child(Newline())

            for i, stmt in enumerate(this_stmt.parent.children):
                if stmt == this_stmt:
                    this_stmt.parent.insert_child(i + 1, print_stmt)
                    break

    transform = PyTreeVisitor.visit
