pycomment
========================================

Inserting repr value on commen with marker (marker is `# =>`).
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
