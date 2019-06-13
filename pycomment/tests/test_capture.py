import unittest
import textwrap
from collections import namedtuple
from pycomment.capture import CaptureResult


class Tests(unittest.TestCase):
    def _callFUT(self, code):
        from pycomment.capture import capture

        return capture(code)

    def test_it(self):
        C = namedtuple("C", "msg, code, comments, stdout")
        cases = [
            C(
                msg="oneline",
                code=textwrap.dedent(
                    """
                    _ = ["hello", "bye"][0] + " world"  # =>
                    print('ZZ\U000f0000ZZ1:', repr(_), 'ZZ\U000f0000ZZ', sep='')
                    """
                ).strip(),
                comments={"1": repr("hello world")},
                stdout=[],
            ),
            C(
                msg="oneline, stdout",
                code=textwrap.dedent(
                    """
                    print("hello, world")
                    """
                ).strip(),
                comments={},
                stdout=["hello, world"],
            ),
        ]
        for c in cases:
            with self.subTest(msg=c.msg):
                got = self._callFUT(c.code)
                self.assertDictEqual(got.comments, c.comments)
                self.assertEqual(got.stdout, c.stdout)
