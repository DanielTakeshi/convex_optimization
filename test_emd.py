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


def emd_two_solns():
    """If there's two solutions, we get fractional solutions.
    In practice, when scaling things up, this will not happen.
    """
    x = cvx.Variable((2,2), name='x')
    c = np.array([[1.0, 2.0],
                  [3.0, 4.0]])

    constraints = [
        x >= 0,                 # Elementwise, all x[i,j] >= 0
        cvx.sum(x[0,:]) == 1,   # x[0,0] + x[0,1] == 1,
        cvx.sum(x[1,:]) == 1,   # x[1,0] + x[1,1] == 1,
        cvx.sum(x[:,0]) == 1,   # x[0,0] + x[1,0] == 1,
        cvx.sum(x[:,1]) == 1,   # x[0,1] + x[1,1] == 1,
    ]

    obj = cvx.Minimize( cvx.sum(cvx.multiply(x,c)) )
    prob = cvx.Problem(obj, constraints)
    prob.solve()

    print("\n  ===== prob1: =====\n{}".format(prob))
    print("\nstatus: {}".format(prob.status))
    print("optimal value: {}".format(prob.value))
    print("optimal var:\n{}\n".format(x.value))

    # Just to confirm
    sol = x.value
    print(sol * c)
    print(np.sum(sol * c))


def emd_unique_soln():
    """Whew, unique _integral_ solution. :-)
    """
    x = cvx.Variable((2,2), name='x')
    c = np.array([[1.0, 3.0],
                  [3.0, 4.0]])

    constraints = [
        x >= 0,                 # Elementwise, all x[i,j] >= 0
        cvx.sum(x[0,:]) == 1,   # x[0,0] + x[0,1] == 1,
        cvx.sum(x[1,:]) == 1,   # x[1,0] + x[1,1] == 1,
        cvx.sum(x[:,0]) == 1,   # x[0,0] + x[1,0] == 1,
        cvx.sum(x[:,1]) == 1,   # x[0,1] + x[1,1] == 1,
    ]

    # --------------------------------------------------------------------------
    # Note: c*x if c and x are both 2x2 does not resolve to a scalar. 
    # EDIT: do NOT use * in cvxpy!! Use `multiply` for element-wise stuff.
    # http://www.cvxpy.org/tutorial/functions/index.html#elementwise-functions
    # https://github.com/cvxgrp/cvxpy/issues/496
    # https://github.com/cvxgrp/cvxpy/issues/80
    # --------------------------------------------------------------------------

    obj = cvx.Minimize( cvx.sum(cvx.multiply(x,c)) )
    prob = cvx.Problem(obj, constraints)
    prob.solve()

    print("\n  ===== prob1: =====\n{}".format(prob))
    print("\nstatus: {}".format(prob.status))
    print("optimal value: {}".format(prob.value))
    print("optimal var:\n{}\n".format(x.value))

    # Just to confirm
    sol = x.value
    print(sol * c)
    print(np.sum(sol * c))


if __name__ == "__main__":
    emd_two_solns()
    emd_unique_soln()
