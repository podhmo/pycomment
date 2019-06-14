import typing as t
import contextlib
from collections import namedtuple
from io import StringIO
from . import SEP_MARKER

CaptureResult = namedtuple("CaptureResult", "comments, stdout")


def capture(code: str, *, g: t.Optional[t.IO] = None):
    o = StringIO()
    with contextlib.redirect_stdout(o):
        g = g or {"__name__": "exec"}
        exec(code, g)

    result_map = {}
    rest = []

    reading = False
    buf = None
    lineno = None

    lines = o.getvalue().splitlines()
    for line in lines:
        if reading:
            if line.endswith(SEP_MARKER):
                reading = False
                buf.append(line.rstrip(SEP_MARKER))
                result_map[lineno] = "\n".join(buf)
            else:
                buf.append(line)
        elif line.startswith(SEP_MARKER):
            reading = True
            lineno, line = line.lstrip(SEP_MARKER).split(":", 1)
            buf = [line]
            if line.endswith(SEP_MARKER):
                reading = False
                result_map[lineno] = buf[0].rstrip(SEP_MARKER)
        else:
            rest.append(line)
    return CaptureResult(comments=result_map, stdout=rest)
