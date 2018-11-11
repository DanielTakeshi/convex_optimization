# Testing Convex Optimization Code

Run `python emd_cvxopt.py` for testing the Earth Mover's Distance. Unfortunately it's not usable now
since I get a singular KKT matrix.

NOTE a key difference between numpy's `*` and cvxpy's `*`, when applied to a combination of
`nd.array`s and `cvx.Variable`s. The former is for element-wise products, the latter is actual
matrix multiplication, as one would use with `np.matrix` rather than `np.array`. Just be careful.
