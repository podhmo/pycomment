import difflib

# don't show this module's infor,  on traceback, when test is failed.
__unittest = True


class AssertDiffMixin:  # with unittest.TestCase
    def assertDiff(self, first, second, *, msg=None, fromfile="first", tofile="second"):
        self.assertIsInstance(first, str, "First argument is not a string")
        self.assertIsInstance(second, str, "Second argument is not a string")

        msg = msg or "{} != {}".format(repr(first)[:40], repr(second)[:40])

        if first != second:
            # don't use difflib if the strings are too long
            if len(first) > self._diffThreshold or len(second) > self._diffThreshold:
                self._baseAssertEqual(first, second, msg)

            firstlines = first.splitlines(keepends=True)
            secondlines = second.splitlines(keepends=True)
            if not firstlines[-1].endswith("\n"):
                firstlines[-1] = firstlines[-1] + "\n"
            if not secondlines[-1].endswith("\n"):
                secondlines[-1] = secondlines[-1] + "\n"

            diff = "\n" + "".join(
                difflib.unified_diff(
                    firstlines, secondlines, fromfile=fromfile, tofile=tofile
                )
            )
            raise self.fail(self._formatMessage(diff, msg))
