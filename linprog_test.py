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

def test1():
    """Quick linear programming test:
    https://cvxopt.org/examples/tutorial/lp.html

    In canonical form:

    minimize_x:
        c*x --> [2, 1] * [x1, x2] = 2*x1 + x2

    subject to:
        - x1 + x2  <=  1
        - x1 - x2  <= -2
        - x2       <=  0
          x1 -2*x2 <=  4

    Thus, b^T = [1, -2, 0, 4], and

    A^T = [-1 -1  0  1]
          [ 1 -1 -1 -2]

    Note, annoyingly it seems like they follow the 'transpose' of numpy conventions,
    so `A` here is a (4,2) matrix, not a (2,4) as it would be in numpy. Though, the 
    conversion is seamless among them, so numpy(cvx_matrix) would be (4,2).

    WAIT ... actually in solvers.lp, the arguments are for (c,G,h,A,b), so despite
    their naming convention, we are actually dealing with G and h. In their notation,
    `Ax = b` is a constraint, NOT `Ax <= b` (i.e., it is _equality_). To handle
    inequality constraints, use `G` and `h` becasue their formalism assumes that we
    have an extra `s >= 0` term which makes the `Gx + s = h` constraint handle
    'inequalities'. These are component-wise vector inequalities, btw. Whew, easy.
    """
    print("\nstart test1()\n")
    A = matrix([ [-1.0, -1.0, 0.0, 1.0],
                 [1.0, -1.0, -1.0, -2.0] ])
    b = matrix([ 1.0, -2.0, 0.0, 4.0 ])
    c = matrix([ 2.0, 1.0 ])

    # Will print progress
    sol = solvers.lp(c,A,b)

    #print(A.size) # (4,2)
    #print(b.size) # (4,1)
    #print(c.size) # (2,1)
    # sol['x'])) = [0.5, 1.5]^T

    print("")
    for key in sol:
        print("sol[{}]: {}".format(key, sol[key]))
    print("\ndone test1()\n")


def test2():
    """Test graph matching. For this we use row-major (C-style) flattening, so:

    a = np.array([[1,2,3],[4,5,6]])
        [1 2 3
         4 5 6]

    a.flatten()
        [1 2 3 4 5 6]

    This is the default for numpy. Define `a` in numpy, then call `matrix(a)`.

    Easy perfect bipartite graph matching to start with, will figure out API.
    Follow convention of rows = index into node of set A (i.e., first set).
    So, cost matrix `c` has first row as cost of edges emanating out of nodes in A.
    When flattening, this means the first k elements are from the first node in A,
    where k = # of nodes in set A (and set B).
    """
    print("\nstart test2()\n")

    # Cost coefficients
    c = np.array([[1.0, 2.0],
                  [3.0, 4.0]])
    c = c.flatten()

    # Inequality constraints, Gx + s = h (s >= 0) or Gx <= h.
    G = -np.eye(4)

    h = np.array([[0.0, 0.0],
                  [0.0, 0.0]])
    h = h.flatten()

    # Equality constraints
    A = np.array([[1.0, 1.0, 0.0, 0.0],
                  [0.0, 0.0, 1.0, 1.0],
                  [1.0, 0.0, 1.0, 0.0],
                  [0.0, 1.0, 0.0, 1.0]]
    )
    print(np.linalg.inv(A))

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
    print("")
    for key in sol:
        print("sol[{}]: {}".format(key, sol[key]))

    print("\ndone test2()")


if __name__ == "__main__":
    test1()
    test2()
