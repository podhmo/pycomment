import itertools
import typing as t

# stolen from pyramid
class reify:
    """cached property"""

    def __init__(self, wrapped):
        self.wrapped = wrapped
        try:
            self.__doc__ = wrapped.__doc__
        except:  # noqa
            pass

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val


class PushBackIterator:
    def __init__(self, itr) -> None:
        self.itr = iter(itr)

    def pushback(self, x: str) -> None:
        self.itr = itertools.chain([x], self.itr)

    def __next__(self) -> str:
        return next(self.itr)

    def __iter__(self) -> t.Iterator[str]:
        return self
