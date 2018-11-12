# Testing Convex Optimization Code

Run `python emd_cvxopt.py` for testing the Earth Mover's Distance. Unfortunately it's not usable now
since I get a singular KKT matrix.

NOTE a key difference between numpy's `*` and cvxpy's `*`, when applied to a combination of
`nd.array`s and `cvx.Variable`s. The former is for element-wise products, the latter is actual
matrix multiplication, as one would use with `np.matrix` rather than `np.array`. Just be careful.


## CVXOPT

- `linprog_test.py`, initial exploratory tests.
- `emd_cvxopt.py`, initial EMD tests, not working.

## CVXPY

- `test_cvx.py`, initial exploratory tests.
- `test_emd.py`, initial EMD tests, working.
- `emd.py`, scaling up EMD tests. It's working, somewhat, but some solutions are not actual perfect
  matches. Keep this fixed, because I referenced it in [a Google Groups question][1]. Since I keep
  that fixed, for further tests involving this, go into the `tests/` directory.


[1]:https://groups.google.com/forum/#!topic/cvxpy/hS03fikOzl4
