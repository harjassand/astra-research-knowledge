"""Focused checks of interpolation and numerical-gradient certificates."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import numpy as np
from check_gaussian_quadratic import gaussian_grid, complement


def interpolation_vertices(n):
    count = (n+1)*(n+2)//2
    maximum = F(0)
    for errors in product((-1,1), repeat=count):
        c = F(errors[0])
        plus, minus = errors[1:1+n], errors[1+n:1+2*n]
        b = [F(plus[i]-minus[i],2) for i in range(n)]
        d = [[F(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            d[i][i] = F(plus[i]+minus[i]-2*errors[0],2)
        index = 1+2*n
        for i in range(n):
            for j in range(i+1,n):
                d[i][j] = d[j][i] = F(errors[index]-plus[i]-plus[j]+errors[0],2)
                index += 1
        error = (2*sum(v*v for row in d for v in row) + sum(v*v for v in b)
                 + (sum(d[i][i] for i in range(n))+c)**2)
        maximum = max(maximum,error)
    assert maximum == 12*n*n-4*n+1
    return dict(n=n,stencil_points=count,vertices=2**count,
                maximum_squared_error=int(maximum))


def noiseless_check(rng,n,r):
    raw = rng.normal(size=(n,n))
    a = (raw+raw.T)/2
    b = rng.normal(size=n)
    u = np.linalg.qr(rng.normal(size=(n,n)))[0][:,:r]
    v = complement(u)
    q = v@v.T
    m = u@rng.normal(size=r)
    d = q@a@q
    t = q@(b+2*a@m)
    approximate_t = t+0.2*v@rng.normal(size=n-r)
    w = approximate_t/np.linalg.norm(approximate_t)
    alpha = w@a@w
    const = m@a@m+b@m+np.trace(d)
    measured = [0.0,0.0]
    for z,weight in gaussian_grid(n-r):
        x = m+v@z
        last = w@x
        target = x@a@x+b@x
        for i,coefficient in enumerate((t@w,np.linalg.norm(approximate_t))):
            prediction = const+coefficient*last+alpha*(last**2-1)
            measured[i] += weight*(target-prediction)**2
    base = 2*(np.sum(d*d)-alpha**2)
    predicted = [base+np.dot(t,t)-(t@w)**2,
                 base+np.sum((t-approximate_t)**2)]
    discrepancies = [abs(x-y) for x,y in zip(measured,predicted)]
    assert max(discrepancies)<1e-10*(1+max(predicted))
    return max(discrepancies)


def noisy_zero_block_check(rng,r,d,s):
    alpha = 1/(1+s)
    variance_u = 1-alpha
    raw = rng.normal(size=(r,r))
    h = (raw+raw.T)/2
    cross = rng.normal(size=(r,d))
    bu,bv = rng.normal(size=r),rng.normal(size=d)
    first_y = rng.normal(size=r)*np.sqrt(1+s)
    mu = alpha*first_y
    t = bv+2*cross.T@mu
    approximate_t = t+0.2*rng.normal(size=d)
    w = approximate_t/np.linalg.norm(approximate_t)
    sqrt_v_cov = np.eye(d)+(np.sqrt(1-alpha)-1)*np.outer(w,w)
    constant = mu@h@mu+variance_u*np.trace(h)+bu@mu+0.31
    measured = 0.0
    for z,weight in gaussian_grid(r+d+1):
        last = np.sqrt(1+s)*z[-1]
        u = mu+np.sqrt(variance_u)*z[:r]
        v = alpha*w*last+sqrt_v_cov@z[r:r+d]
        target = u@h@u+2*u@cross@v+bu@u+bv@v+0.31
        prediction = constant+alpha*np.linalg.norm(approximate_t)*last
        measured += weight*(target-prediction)**2
    before = (2*variance_u**2*np.sum(h*h)
              +variance_u*np.sum((2*h@mu+bu)**2)
              +np.sum(t*t)+4*variance_u*np.sum(cross*cross))
    predicted = before-alpha*np.sum(t*t)+alpha*np.sum((t-approximate_t)**2)
    discrepancy = abs(measured-predicted)
    assert discrepancy<1e-10*(1+predicted)
    return discrepancy


def main():
    rng = np.random.default_rng(20261030)
    results = dict(seed=20261030,
                   exact_interpolation_vertex_checks=[interpolation_vertices(n) for n in (1,2,3)],
                   noiseless_direction_certificate_checks=0,
                   noisy_zero_block_gradient_checks=0,
                   max_noiseless_absolute_discrepancy=0.0,
                   max_noisy_absolute_discrepancy=0.0)
    for n in (2,3,4,5,6):
        for r in range(n):
            discrepancy = noiseless_check(rng,n,r)
            results["noiseless_direction_certificate_checks"] += 2
            results["max_noiseless_absolute_discrepancy"] = max(
                results["max_noiseless_absolute_discrepancy"],float(discrepancy))
    for r,d in ((1,1),(2,2),(2,3)):
        for s in (0.01,1.0,2.0):
            for _ in range(3):
                discrepancy = noisy_zero_block_check(rng,r,d,s)
                results["noisy_zero_block_gradient_checks"] += 1
                results["max_noisy_absolute_discrepancy"] = max(
                    results["max_noisy_absolute_discrepancy"],float(discrepancy))
    results["status"] = "PASS"
    Path(__file__).with_name("check_model_robustness_results.json").write_text(
        json.dumps(results,indent=2)+"\n")
    print(json.dumps(results,indent=2))


if __name__ == "__main__":
    main()
