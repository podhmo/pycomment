import unittest
import textwrap
from collections import namedtuple


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
_ = ["hello", "bye"][0] + " world"  # => "hello world"
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
            C(
                msg="toplevels",
                code=textwrap.dedent(
                    """
import sys

print("stderr", file=sys.stderr)
print("hello")
_ = 1 + 2 + 3 + 3 + 4 + 5  # => 18
print('ZZ\U000f0000ZZ6:', repr(_), 'ZZ\U000f0000ZZ', sep='')
print('ZZ\U000f0000ZZ5:', repr(_), 'ZZ\U000f0000ZZ', sep='')
_ = _ = 1 + 2 + 3 + 3 + 4 + 5  # => 18
print('ZZ\U000f0000ZZ6:', repr(_), 'ZZ\U000f0000ZZ', sep='')
print("bye")
                    """
                ).strip(),
                comments={"5": "18", "6": "18"},
                stdout=["hello", "bye"],
            ),
            C(
                msg="inline function",
                code=textwrap.dedent(
                    """
def main():
    print("Hoi")
    _ = sum([10, 20, 30])  # => 60
    print('ZZ\U000f0000ZZ3:', repr(_), 'ZZ\U000f0000ZZ', sep='')


_ = 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1  # => 25
print('ZZ\U000f0000ZZ6:', repr(_), 'ZZ\U000f0000ZZ', sep='')

# yapf: disable
_ = (1 + 2
 + 3)  # => 6

# yapf: disable
print('ZZ\U000f0000ZZ10:', repr(_), 'ZZ\U000f0000ZZ', sep='')

# yapf: enable

main()
                    """
                ).strip(),
                comments={"3": "60", "6": "25", "10": "6"},
                stdout=["Hoi"],
            ),
            C(
                msg="loop",
                code=textwrap.dedent(
                    """
for i in range(10):
    _ = i  # => 9
    print('ZZ\U000f0000ZZ2:', repr(_), 'ZZ\U000f0000ZZ', sep='')
    j = i * i
    _ = j  # => 81
    print('ZZ\U000f0000ZZ4:', repr(_), 'ZZ\U000f0000ZZ', sep='')
    for k in range(2):  # =>
        _ = (k, j, i)  # => (1, 81, 9)
        print('ZZ\U000f0000ZZ6:', repr(_), 'ZZ\U000f0000ZZ', sep='')
_ = x = 1 - 10  # => -9
print('ZZ\U000f0000ZZ17:', repr(_), 'ZZ\U000f0000ZZ', sep='')
                    """
                ).strip(),
                comments={"2": "9", "4": "81", "6": "(1, 81, 9)", "17": "-9"},
                stdout=[],
            ),
        ]
        for c in cases:
            with self.subTest(msg=c.msg):
                got = self._callFUT(c.code)
                self.assertDictEqual(got.comments, c.comments)
                self.assertEqual(got.stdout, c.stdout)
