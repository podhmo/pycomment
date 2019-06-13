import sys
from pycomment.transform import transform_file
from pycomment.capture import capture
from pycomment.emit import emit


def run(sourcefile, out=sys.stdout, g=None):
    code = str(transform_file(sourcefile))
    capture_result = capture(code, g=g)

    with open(sourcefile) as rf:
        emit(
            rf, result_map=capture_result.comments, rest=capture_result.stdout, out=out
        )


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


if __name__ == "__main__":
    main()
