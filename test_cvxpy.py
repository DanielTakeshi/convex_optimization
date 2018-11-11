"""Testing CVXPY (not CVXOPT, note the naming...).

Documentation of CVXOPT says:
> Modeling interfaces to the CVXOPT solvers are available in CVXPY and PICOS.

So, CVXPY must make it easier to call CVXOPT.
"""
import os
import sys
import numpy as np
np.set_printoptions(suppress=True)
import cvxpy as cvx
from cvxopt import matrix, solvers


def test1():
    # Create two scalar optimization variables.
    x = cvx.Variable()
    y = cvx.Variable()
    
    # Create two constraints.
    constraints = [x + y == 1,
                   x - y >= 1]
    
    # Form objective.
    obj = cvx.Minimize((x - y)**2)
    
    # Form and solve problem.
    prob = cvx.Problem(obj, constraints)
    prob.solve()  # Returns the optimal value.
    print("\n  prob1:\n{}".format(prob))
    print("status:",       prob.status)
    print("optimal value", prob.value)
    print("optimal var",   x.value, y.value)

    # New problem, but borrow old constraints
    prob2 = cvx.Problem(cvx.Maximize(x+y), prob.constraints)
    prob2.solve()
    print("\n  prob2:\n{}".format(prob2))
    print("status:",       prob2.status)
    print("optimal value", prob2.value)
    print("optimal var",   x.value, y.value)


def test2():
    """Simple linear program?

    Fortunately, docs say:

    > You can use your numeric library of choice to construct matrix and
    > vector constants. For instance, if x is a CVXPY Variable in the
    > expression A*x + b, A and b could be Numpy ndarrays, SciPy sparse
    > matrices, etc. A and b could even be different types.

    It gets the same solution as cvxopt.
    """
    x = cvx.Variable(2, name='x')
    c = np.array([2.0, 1.0])

    constraints = [
        -x[0]  + x[1] <=  1,
        -x[0]  - x[1] <= -2,
                -x[1] <=  0,
        x[0] - 2*x[1] <=  4,
    ]
    
    # I think c*x is the same as cvx.sum(c*x) despite differences in numpy semantics?
    obj = cvx.Minimize( c*x )
    prob = cvx.Problem(obj, constraints)
    prob.solve()

    print("\n  prob1:\n{}".format(prob))
    print("status:",       prob.status)
    print("optimal value", prob.value)
    print("optimal var",   x.value)


if __name__ == "__main__":
    #test1()
    test2()
