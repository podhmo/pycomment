import contextlib
from collections import namedtuple
from io import StringIO
from . import SEP_MARKER

CaptureResult = namedtuple("CaptureResult", "comments, stdout")


def capture(code, *, o=None, g=None):
    o = o or StringIO()
    with contextlib.redirect_stdout(o):
        g = g or {"__name__": "exec"}
        exec(code, g)

    result_map = {}
    stdout_outputs = []
    for line in o.getvalue().splitlines():
        if line.startswith(SEP_MARKER) and line.endswith(SEP_MARKER):
            line = line.strip(SEP_MARKER)
            lineno, line = line.split(":", 1)
            result_map[lineno] = line
        else:
            stdout_outputs.append(line)
    return CaptureResult(comments=result_map, stdout=stdout_outputs)
