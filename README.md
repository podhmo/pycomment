[![Python application test with Pytest](https://github.com/podhmo/pycomment/actions/workflows/python-package/badge.svg)](https://github.com/podhmo/pycomment/actions)

# pycomment

Inserting repr value on comment with marker (marker is `# =>`). This is heavily inspired by xmpfilter of ruby's [rocodetools](https://github.com/rcodetools/rcodetools).

## install

```console
$ pip install pycomment
```

## how to use

`code.py`

```python
import sys

print("stderr", file=sys.stderr)
print("hello")
1 + 2 + 3 + 3 + 4 + 5  # =>
1 + 2 + 3 + 3 + 4 + 5  # =>
print("bye")
```

```console
$ pycomment --inplace code.py
```

```python
import sys

print("stderr", file=sys.stderr)
print("hello")
1 + 2 + 3 + 3 + 4 + 5  # => 18
1 + 2 + 3 + 3 + 4 + 5  # => 18
print("bye")


# -- stdout --------------------
# >> hello
# >> bye
```

### multi-line output

```python
import numpy as np

np.arange(9).reshape((3, 3))  # => multi-line..
# array([[0, 1, 2],
#        [3, 4, 5],
#        [6, 7, 8]])
# ..multi-line
```