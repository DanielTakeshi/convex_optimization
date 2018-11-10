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
    """
    pass


def test3():
    """Simple EMD?
    """
    pass


if __name__ == "__main__":
    test1()
    test2()
    test3()
