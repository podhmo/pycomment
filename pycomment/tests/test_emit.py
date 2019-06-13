import unittest
from collections import namedtuple


class Tests(unittest.TestCase):
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
                code="""["hello", "bye"][0] + " world"  # => """,
                comments={"1": repr("hello, world")},
                stdout=[],
                want="""["hello", "bye"][0] + " world"  # => 'hello, world'""".strip(),
            )
        ]

        for c in cases:
            with self.subTest(msg=c.msg):
                o = StringIO()
                self._callFUT(c.code, c.comments, c.stdout, out=o)
                got = o.getvalue().strip()
                self.assertEqual(got, c.want)
