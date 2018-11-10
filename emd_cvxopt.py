"""Testing CVXOPT.

Look at this for docs:
    https://cvxopt.org/userguide/coneprog.html

Also this for linprog more specifically:
    https://cvxopt.org/userguide/coneprog.html#linear-programming
"""
import os
import sys
import numpy as np
np.set_printoptions(suppress=True)
from cvxopt import matrix, solvers


def earth_mover_distance():
    """Test (perfect) bipartite graph matching. Use row-major (C-style) flattening:

    a = np.array([[1,2,3],[4,5,6]])
        [1 2 3
         4 5 6]

    a.flatten()
        [1 2 3 4 5 6]

    This is the default for numpy. Define `a` in numpy, then call `matrix(a)`.

    Follow convention of rows = index into node of set A (i.e., first set).
    So, cost matrix `c` has first row as cost of edges emanating out of nodes in A.
    When flattening, this means the first k elements are from the first node in A,
    where k = # of nodes in set A (and set B).
    """
    # Cost coefficients
    c = np.array([[1.0, 2.0],
                  [3.0, 4.0]])
    c = c.flatten()

    # Inequality constraints, Gx + s = h (s >= 0) or Gx <= h.
    G = -np.eye(4)

    h = np.array([[0.0, 0.0],
                  [0.0, 0.0]])
    h = h.flatten()

    # Equality constraints, Ax = b.
    A = np.array([[1.0, 1.0, 0.0, 0.0],
                  [0.0, 0.0, 1.0, 1.0],
                  [1.0, 0.0, 1.0, 0.0],
                  [0.0, 1.0, 0.0, 1.0]]
    )

    b = np.array([[1.0, 1.0],
                  [1.0, 1.0]])
    b = b.flatten()

    # convert to matrix
    c = matrix(c)
    G = matrix(G)
    h = matrix(h)
    A = matrix(A)
    b = matrix(b)

    # Solve!
    sol = solvers.lp(c,G,h,A,b)


if __name__ == "__main__":
    earth_mover_distance()
