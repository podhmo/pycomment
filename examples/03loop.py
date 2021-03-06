for i in range(10):
    i  # => 9
    j = i * i
    j  # => 81
    for k in range(2):  # =>
        (k, j, i)  # => (1, 81, 9)

import itertools

itertools.combinations(
    [1, 2, 3, 4, 5], 2
).__class__  # => <class 'itertools.combinations'>
list(
    itertools.combinations([1, 2, 3, 4, 5], 3)
)  # => [(1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 3, 4), (1, 3, 5), (1, 4, 5), (2, 3, 4), (2, 3, 5), (2, 4, 5), (3, 4, 5)]

x = 1 - 10  # => -9
