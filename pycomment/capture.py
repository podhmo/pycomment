import typing as t
import contextlib
from collections import namedtuple
from io import StringIO
from . import SEP_MARKER

CaptureResult = namedtuple("CaptureResult", "comments, stdout")


def _exec_self(code: str, *, g: t.Optional[dict] = None) -> None:
    g = g or {"__name__": "exec"}
    exec(code, g)


def _exec_in_tempfile(code: str, *, g: t.Optional[dict] = None) -> None:
    import runpy
    import tempfile

    with tempfile.NamedTemporaryFile("w+") as f:
        print(code, file=f)
        f.seek(0)
        runpy.run_path(f.name)


def capture(code: str, *, g: t.Optional[dict] = None, _exec=_exec_in_tempfile):
    o = StringIO()
    with contextlib.redirect_stdout(o):
        _exec(code, g=g)

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
                result_map[lineno] = buf
            else:
                buf.append(line)
        elif line.startswith(SEP_MARKER):
            reading = True
            lineno, line = line.lstrip(SEP_MARKER).split(":", 1)
            buf = [line.rstrip(SEP_MARKER)]
            if line.endswith(SEP_MARKER):
                reading = False
                result_map[lineno] = buf
        else:
            rest.append(line)
    return CaptureResult(comments=result_map, stdout=rest)
