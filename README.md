# pycomment ![Python package](https://github.com/podhmo/pycomment/workflows/Python%20package/badge.svg) [![PyPi version](https://img.shields.io/pypi/v/pycomment.svg)](https://pypi.python.org/pypi/pycomment) [![](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/download/releases/3.10.0/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)

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
