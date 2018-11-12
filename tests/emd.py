import argparse, time, os, sys
import numpy as np
np.set_printoptions(precision=4, suppress=False, linewidth=160, edgeitems=5)
import cvxpy as cvx


def _get_threshold(x, thresh):
    """Filter out any values below some quantity.
    """
    x = np.copy(np.array(x))
    thresh_inds = x < thresh
    x[thresh_inds] = 0
    return x


def _report_results(prob, p_time, x, args):
    """Debugging, checking that result makes sense, etc.
    Note, `n=nrows`, or the number of nodes in each group.
    """
    print("\n\n  ========== PROB ==========\n")
    #print(prob)
    print("\nstatus:        {}".format(prob.status))
    print("time (mins):   {:.5f}".format(p_time))
    print("optimal value: {:.5f}".format(prob.value))
    print("optimal soln:\n{}".format(x.value))

    sol_thresh = _get_threshold(x.value, args.thresh)
    print("optimal THRESHOLDED soln:\n{}".format(sol_thresh)) # ideally, 0 means no edge, 1 means edge
    print("sum of thresholded elements:  {:.3f}".format(np.sum(sol_thresh))) # should be ~n
    max_0    = np.max(sol_thresh, axis=0)
    max_1    = np.max(sol_thresh, axis=1)
    argmax_0 = np.argmax(sol_thresh, axis=0)
    argmax_1 = np.argmax(sol_thresh, axis=1)
    print("max_0:         {}".format(max_0))
    print("max_1:         {}".format(max_1))
    #print("argmax_0:      {}".format(argmax_0))
    #print("argmax_1:      {}".format(argmax_1))
    print("len(unique_0): {}".format( len(np.unique(argmax_0))) ) # should be equal to n
    print("len(unique_1): {}".format( len(np.unique(argmax_1))) ) # should be equal to n


def emd(args, nrows, c):
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

    _report_results(prob, p_time, x, args)


if __name__ == "__main__":
    pp = argparse.ArgumentParser()
    pp.add_argument('--nrows', type=int, default=10)
    pp.add_argument('--max_iter', type=int, default=None)
    pp.add_argument('--thresh', type=float, default=0.01)
    args = pp.parse_args() 

    c = np.random.rand(args.nrows, args.nrows)
    emd(args, nrows=args.nrows, c=c)
