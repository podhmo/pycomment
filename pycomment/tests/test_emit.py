import unittest
import textwrap
from collections import namedtuple
from .testing import AssertDiffMixin


class Tests(unittest.TestCase, AssertDiffMixin):
    maxDiff = None

    def _callFUT(self, code: str, result_map, rest, out):
        from pycomment.emit import emit
        from io import StringIO

        return emit(StringIO(code), result_map=result_map, rest=rest, out=out)

    def test_it(self):
        from io import StringIO

        C = namedtuple("C", "msg, code, comments, stdout, want")
        cases = [
            C(
                msg="simplest",
                code=textwrap.dedent(
                    """
                    ["hello", "bye"][0] + " world"  # =>
                    """
                ).strip(),
                comments={"1": [repr("hello, world")]},
                stdout=[],
                want=textwrap.dedent(
                    """
                    ["hello", "bye"][0] + " world"  # => 'hello, world'
                    """
                ).strip(),
            ),
            # todo: stdout
            C(
                msg="multi-line",
                code=textwrap.dedent(
                    """
                    from pycomment.tests._fakearray import arange
                    arange(9).reshape((3, 3))  # =>
                    """
                ).strip(),
                comments={
                    "2": [
                        "array([[0, 1, 2],",
                        "       [3, 4, 5],",
                        "       [6, 7, 8]])",
                    ]
                },
                stdout=[],
                want=textwrap.dedent(
                    """
                    from pycomment.tests._fakearray import arange
                    arange(9).reshape((3, 3))  # => multi-line..
                    # array([[0, 1, 2],
                    #        [3, 4, 5],
                    #        [6, 7, 8]])
                    # ..multi-line
                    """
                ).strip(),
            ),
            C(
                msg="multi-line replace",
                code=textwrap.dedent(
                    """
                    from pycomment.tests._fakearray import arange
                    arange(9).reshape((3, 3))  # => multi-line..
                    # array([[0, 1, 2],
                    #        [3, 4, 5],
                    #        [6, 7, 8]])
                    # ..multi-line
                    """
                ).strip(),
                comments={
                    "2": [
                        "array([[0, 1, 2],",
                        "       [3, 4, 5],",
                        "       [6, 7, 8]])",
                    ]
                },
                stdout=[],
                want=textwrap.dedent(
                    """
                    from pycomment.tests._fakearray import arange
                    arange(9).reshape((3, 3))  # => multi-line..
                    # array([[0, 1, 2],
                    #        [3, 4, 5],
                    #        [6, 7, 8]])
                    # ..multi-line
                    """
                ).strip(),
            ),
            C(
                msg="multi-line with indent",
                code=textwrap.dedent(
                    """
                    def run():
                        from pycomment.tests._fakearray import arange
                        arange(9).reshape((3, 3))  # =>
                    run()
                    """
                ).strip(),
                comments={
                    "3": [
                        "array([[0, 1, 2],",
                        "       [3, 4, 5],",
                        "       [6, 7, 8]])",
                    ]
                },
                stdout=[],
                want=textwrap.dedent(
                    """
                    def run():
                        from pycomment.tests._fakearray import arange
                        arange(9).reshape((3, 3))  # => multi-line..
                        # array([[0, 1, 2],
                        #        [3, 4, 5],
                        #        [6, 7, 8]])
                        # ..multi-line
                    run()
                    """
                ).strip(),
            ),
        ]

        for c in cases:
            with self.subTest(msg=c.msg):
                o = StringIO()
                self._callFUT(c.code, c.comments, c.stdout, out=o)
                got = o.getvalue().strip()
                self.assertDiff(got, c.want, fromfile="got", tofile="want")
