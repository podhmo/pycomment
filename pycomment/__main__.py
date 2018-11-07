import sys
import contextlib
from io import StringIO
from pycomment import (
    transform_file,
    SEP_MARKER,
    COMMENT_MARKER,
)
STDOUT_HEADER_MARKER = "# -- stdout --------------------"


def run(sourcefile, out=sys.stdout, g=None):
    o = StringIO()
    with contextlib.redirect_stdout(o):
        code = str(transform_file(sourcefile))
        g = g or {}
        exec(code, g, g)

    result_map = {}
    stdout_outputs = []
    for line in o.getvalue().splitlines():
        if line.startswith(SEP_MARKER) and line.endswith(SEP_MARKER):
            line = line.strip(SEP_MARKER)
            lineno, line = line.split(":", 2)
            result_map[lineno] = line
        else:
            stdout_outputs.append(line)

    i = 0

    with open(sourcefile) as rf:
        import re
        rx = re.compile(COMMENT_MARKER + ".*$")
        for lineno, line in enumerate(rf, 1):
            if line.rstrip() == STDOUT_HEADER_MARKER:
                break

            m = rx.search(line)
            k = str(lineno)
            if m is None or k not in result_map:
                print(line, end="", file=out)
            else:
                print(line[:m.start()] + COMMENT_MARKER, result_map[k], file=out)
                i += 1

    if stdout_outputs:
        print(STDOUT_HEADER_MARKER, file=out)
        for line in stdout_outputs:
            print("# >>", line, file=out)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("sourcefile")
    parser.add_argument("--inplace", action="store_true")
    parser.add_argument("--show-only", action="store_true")

    args = parser.parse_args()

    if args.show_only:
        print(str(transform_file(args.sourcefile)))
        from prestring.python.parse import dump_tree
        dump_tree(transform_file(args.sourcefile))
    elif not args.inplace:
        run(args.sourcefile)
    else:
        import tempfile
        import os
        import shutil

        name = None
        try:
            with tempfile.NamedTemporaryFile("w", delete=False) as wf:
                name = wf.name
                run(args.sourcefile, out=wf)
            print("replace: {} -> {}".format(name, args.sourcefile), file=sys.stderr)
            shutil.move(name, args.sourcefile)
        except Exception:
            if os.path.exists(name):
                os.unlink(name)
            raise
