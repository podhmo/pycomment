import sys
from io import StringIO
from pycomment import transform_file, COMMENT_MARKER
from pycomment.capture import capture

STDOUT_HEADER_MARKER = "# -- stdout --------------------"


def run(sourcefile, out=sys.stdout, g=None):
    o = StringIO()
    code = str(transform_file(sourcefile))
    capture_result = capture(code, g=g, o=o)

    i = 0
    result_map = capture_result.comments

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
                print(line[: m.start()] + COMMENT_MARKER, result_map[k], file=out)
                i += 1

    if capture_result.stdout:
        print(STDOUT_HEADER_MARKER, file=out)
        for line in capture_result.stdout:
            print("# >>", line, file=out)


def main():
    import argparse
    import logging

    parser = argparse.ArgumentParser()
    parser.add_argument("sourcefile")
    parser.add_argument(
        "--logging", default="INFO", choices=list(logging._nameToLevel.keys())
    )
    parser.add_argument("-i", "--inplace", action="store_true")
    parser.add_argument("--show-code", action="store_true")
    parser.add_argument("--show-ast", action="store_true")

    args = parser.parse_args()

    logging.basicConfig(level=args.logging)

    if args.show_ast:
        from prestring.python.parse import dump_tree

        dump_tree(transform_file(args.sourcefile))
        return
    elif args.show_code:
        print(str(transform_file(args.sourcefile)))
        return
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
