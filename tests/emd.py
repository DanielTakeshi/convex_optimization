import argparse, time, os, sys
import numpy as np
np.set_printoptions(precision=3, suppress=False, linewidth=160, edgeitems=5)
import cvxpy as cvx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')

# matplotlib
# ----------
titlesize = 33
xsize = 30
ysize = 30
ticksize = 25
legendsize = 25
# ----------

def _get_threshold(x, thresh):
    """Filter out any values below some quantity.
    """
    x = np.copy(x)
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
    print("time (mins):   {:.4f}".format(p_time))
    print("optimal value: {:.4f}".format(prob.value))
    print("optimal soln:\n{}".format(x.value))

    sol_matrix = np.array(x.value)
    sol_thresh = _get_threshold(sol_matrix, args.thresh)
    print("optimal THRESHOLDED soln:\n{}".format(sol_thresh)) # 0 means no edge, 1 means edge
    print("sum of thresholded elements:  {:.3f}".format(np.sum(sol_thresh))) # should be ~n
    max_0    = np.max(sol_thresh, axis=0)
    max_1    = np.max(sol_thresh, axis=1)
    argmax_0 = np.argmax(sol_thresh, axis=0)
    argmax_1 = np.argmax(sol_thresh, axis=1)
    print("max_0:         {}".format(max_0))
    print("max_1:         {}".format(max_1))
    #print("argmax_0:      {}".format(argmax_0))
    #print("argmax_1:      {}".format(argmax_1))
    k1 = len(np.unique(argmax_0))
    k2 = len(np.unique(argmax_1))
    print("len(unique_0): {}".format(k1)) # should be n
    print("len(unique_1): {}".format(k2)) # should be n

    # -------------------------------------------
    # Can also plot values in matrices, carefully
    # -------------------------------------------
    f_nrows = 1
    f_ncols = 2
    fig, ax = plt.subplots(f_nrows,f_ncols, squeeze=False, figsize=(11*f_ncols,8*f_nrows))
    title1 = "All (Non-Thresh). Unique: ({},{})".format(k1, k2)
    ax[0,0].set_title(title1, fontsize=titlesize)
    ax[0,0].set_xlabel("Index in Solution Matrix", fontsize=xsize)
    ax[0,0].plot(
        np.arange(sol_matrix.size),
        np.sort(sol_matrix.flatten()),
        label='All Values'
    )
    larger_vals    = np.sort(sol_matrix.flatten())[-2*args.nrows:]
    larger_vals_th = np.sort(sol_thresh.flatten())[-2*args.nrows:]
    title2 = "Only Larger Elements (c is {}x{})".format(args.nrows, args.nrows)
    ax[0,1].set_title(title2, fontsize=titlesize)
    ax[0,1].set_xlabel("Only Larger Elements", fontsize=xsize)
    ax[0,1].plot(
        np.arange(2*args.nrows),
        larger_vals,
        label='Large Values (min: {:.5f})'.format(larger_vals[0])
    )
    #ax[0,1].plot(
    #    np.arange(2*args.nrows),
    #    larger_vals_th,
    #    label='Thresholded'.format()
    #)
    for i in range(f_nrows):
        for j in range(f_ncols):
            leg = ax[i,j].legend(loc="best", ncol=1, prop={'size':legendsize})
            for legobj in leg.legendHandles:
                legobj.set_linewidth(4.0)
            ax[i,j].tick_params(axis='x', labelsize=ticksize)
            ax[i,j].tick_params(axis='y', labelsize=ticksize)
    plt.tight_layout()
    lastname = 'example.png'.format()
    figname = os.path.join('figs',lastname)
    plt.savefig(figname)
    print("Just saved:\n\t{}\n".format(figname))


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
    prob.solve(verbose=True,
               max_iter=args.max_iter,
               eps_abs=args.eps_abs,
               eps_rel=args.eps_rel)
    p_time = (time.time() - p_time) / 60.0

    _report_results(prob, p_time, x, args)


if __name__ == "__main__":
    pp = argparse.ArgumentParser()
    pp.add_argument('--nrows', type=int, default=10)
    pp.add_argument('--thresh', type=float, default=0.01)
    # For OSQP see: https://osqp.org/docs/interfaces/solver_settings.html
    pp.add_argument('--max_iter', type=int, default=4000)
    pp.add_argument('--eps_abs', type=float, default=1e-3)
    pp.add_argument('--eps_rel', type=float, default=1e-3)
    args = pp.parse_args() 

    c = np.random.rand(args.nrows, args.nrows)
    emd(args, nrows=args.nrows, c=c)
