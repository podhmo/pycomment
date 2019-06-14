import typing as t
import sys
import re
from .langhelpers import PushBackIterator
from . import COMMENT_MARKER, STDOUT_HEADER_MARKER


def emit(
    rf: t.Iterable[str],
    *,
    result_map: t.Dict[str, t.List[str]],
    rest: t.List[str],
    out: t.IO = sys.stdout,
    _rx=re.compile(COMMENT_MARKER + ".*$"),
    _padding_rx=re.compile("^[ 	]*"),
) -> None:
    i = 0  # xxx
    itr = PushBackIterator(enumerate(rf, 1))
    for lineno, line in itr:
        if line.rstrip() == STDOUT_HEADER_MARKER:
            break

        m = _rx.search(line)
        k = str(lineno)
        if m is None or k not in result_map:
            print(line, end="", file=out)
        else:
            comments = result_map[k]
            if len(comments) == 1:
                print(line[: m.start()] + COMMENT_MARKER, comments[0], file=out)
            else:
                print(line[: m.start()] + COMMENT_MARKER, "multi-line..", file=out)
                padding = ""
                m = _padding_rx.match(line)
                if m is not None:
                    padding = m.group(0)

                for lineno, line in itr:
                    if not line.startswith("# "):
                        itr.pushback((lineno, line))
                        break
                    if line.startswith("# ..multi-line"):
                        break

                for comment in comments:
                    print(f"{padding}# {comment}", file=out)
                print(f"{padding}# ..multi-line", file=out)
            i += 1

    if rest:
        print(STDOUT_HEADER_MARKER, file=out)
        for line in rest:
            print("# >>", line, file=out)
