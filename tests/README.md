# Testing EMD Accuracy and Scalability

The `emd.py` here is inspired from the one at the top-level directory, except I am moving all
subsequent tests over here.



## 10 x 10 Cost Matrix

Running `python emd.py` with default settings, five times, results in:
 
- Status: solved/optimal, all the time.
- Number of iterations: 100, 100, 125, 100, 100
- Sum of thresholded elements: 10.079, 9.906, 10.104, 10.008, 9.94
- Len unique: 10/10, all the time.

So, things are reasonably good, and sometimes we need 100, 125, or 150 iterations (I get 150
sometimes). Looks good, and the sum of thresholded elements is indeed around 10.

## 100 x 100 Cost Matrix



## 1000 x 1000 Cost Matrix
