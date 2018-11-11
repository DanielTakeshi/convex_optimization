"""Testing EMD.
"""
import time, os, sys
import numpy as np
np.set_printoptions(suppress=True)
import cvxpy as cvx


def emd_unique_soln():
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
    emd_unique_soln()
