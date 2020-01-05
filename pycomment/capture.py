import typing as t
import contextlib
from collections import namedtuple
from io import StringIO
from . import SEP_MARKER

CaptureResult = namedtuple("CaptureResult", "comments, stdout")


def _exec_self(
    code: str, *, g: t.Optional[dict] = None, filename: t.Optional[str] = None,
) -> dict:
    g = g or {"__name__": "exec"}
    exec(code, g)
    return g


def _exec_in_tempfile(
    code: str, *, g: t.Optional[dict] = None, filename: t.Optional[str] = None,
) -> dict:
    import runpy
    import tempfile
    import os.path
    import sys

    with contextlib.ExitStack() as s:
        dirpath = None
        if filename is not None:
            dirpath = os.path.dirname(os.path.abspath(filename))
            sys.path.insert(0, dirpath)
            s.callback(lambda: sys.path.pop(0))
        with tempfile.NamedTemporaryFile("w+", suffix=".py", dir=dirpath) as f:
            print(code, file=f)
            f.seek(0)
            return runpy.run_path(f.name, init_globals=g)


def capture(
    code: str,
    *,
    g: t.Optional[dict] = None,
    filename: t.Optional[str] = None,
    _exec=_exec_in_tempfile,
):
    o = StringIO()
    with contextlib.redirect_stdout(o):
        g = _exec(code, g=g, filename=filename)

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
