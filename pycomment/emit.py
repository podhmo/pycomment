import typing as t
import sys
import re
from . import COMMENT_MARKER, STDOUT_HEADER_MARKER


def emit(
    rf: t.Iterable[str],
    *,
    result_map: t.Dict[str, str],
    rest: t.List[str],
    out: t.IO = sys.stdout
) -> None:
    i = 0  # xxx
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

    if rest:
        print(STDOUT_HEADER_MARKER, file=out)
        for line in rest:
            print("# >>", line, file=out)
