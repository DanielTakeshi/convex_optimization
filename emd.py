import time, os, sys
import numpy as np
np.set_printoptions(suppress=False, linewidth=160, edgeitems=5)
import cvxpy as cvx


def _get_threshold(x):
    x = np.copy(np.array(x))
    thresh_inds = x < 0.001
    x[thresh_inds] = 0
    return x


def _report_results(prob, p_time, x):
    """Debugging, checking that result makes sense, etc.
    """
    print("\n\n  ========== PROB ==========\n{}".format(prob))
    print("\nstatus:        {}".format(prob.status))
    print("time (mins):   {:.5f}".format(p_time))
    print("optimal value: {:.5f}".format(prob.value))
    print("optimal soln:\n{}".format(x.value))

    sol_thresh = _get_threshold(x.value)
    print("optimal THRESHOLDED soln:\n{}".format(sol_thresh))
    print("sum of thresholded elements:  {:.3f}".format(np.sum(sol_thresh)))
    max_0    = np.max(sol_thresh, axis=0)
    max_1    = np.max(sol_thresh, axis=1)
    argmax_0 = np.argmax(sol_thresh, axis=0)
    argmax_1 = np.argmax(sol_thresh, axis=1)
    print("max_0:       {}".format(max_0))
    print("max_1:       {}".format(max_1))
    print("argmax_0:    {}".format(argmax_0))
    print("argmax_1:    {}".format(argmax_1))
    print("len(unique): {}".format( len(np.unique(argmax_0))) )
    print("len(unique): {}".format( len(np.unique(argmax_1))) )


def emd(nrows, c):
    """Keep nrows == ncols.
    """
    x = cvx.Variable((nrows,nrows), name='x')
    constraints = [x >= 0]
    for i in range(nrows):
        constraints.append( cvx.sum(x[i,:]) == 1 )
        constraints.append( cvx.sum(x[:,i]) == 1 )

    obj = cvx.Minimize( cvx.sum(cvx.multiply(x,c)) )
    prob = cvx.Problem(obj, constraints)

    p_time = time.time()
    prob.solve(verbose=True)
    p_time = (time.time() - p_time) / 60.0
    _report_results(prob, p_time, x)


if __name__ == "__main__":
    # Simple 2x2 case, to confirm that it's equal to what I did earlier.
    ## c = np.array([[1.0, 3.0], [3.0, 4.0]])
    ## emd(nrows=c.shape[0], c=c)

    # 10x10. Results look good since 10x10 is still easy.
    c = np.random.rand(10,10)
    emd(nrows=c.shape[0], c=c)

    # 100x100. Solver time: 0.008 mins. But num unique nodes ~96-98 ish.
    ## c = np.random.rand(100,100)
    ## emd(nrows=c.shape[0], c=c)

    # 500x500. Solver time: 0.409 mins. But num unique nodes ~450-470 ish.
    ## c = np.random.rand(500,500)
    ## emd(nrows=c.shape[0], c=c)
