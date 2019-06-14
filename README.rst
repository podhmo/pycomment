.. image:: https://travis-ci.org/podhmo/pycomment.svg?branch=master
    :target: https://travis-ci.org/podhmo/pycomment

pycomment
========================================

Inserting repr value on comment with marker (marker is `# =>`).
This is heavily inspired by xmpfilter of ruby's `rocodetools <https://github.com/rcodetools/rcodetools>`_

install
----------------------------------------

warning: in the future (not yet)

.. code-block:: console

  $ pip install pycomment


how to use
----------------------------------------


code.py

.. code-block:: python

  import sys

  print("stderr", file=sys.stderr)
  print("hello")
  1 + 2 + 3 + 3 + 4 + 5  # =>
  1 + 2 + 3 + 3 + 4 + 5  # =>
  print("bye")


.. code-block:: console

  $ pycomment --inplace code.py

.. code-block:: python

  import sys

  print("stderr", file=sys.stderr)
  print("hello")
  1 + 2 + 3 + 3 + 4 + 5  # => 18
  1 + 2 + 3 + 3 + 4 + 5  # => 18
  print("bye")


  # -- stdout --------------------
  # >> hello
  # >> bye

multi-line output

.. code:: python

  import numpy as np

  np.arange(9).reshape((3, 3))  # => multi-line..
  # array([[0, 1, 2],
  #        [3, 4, 5],
  #        [6, 7, 8]])
  # ..multi-line

