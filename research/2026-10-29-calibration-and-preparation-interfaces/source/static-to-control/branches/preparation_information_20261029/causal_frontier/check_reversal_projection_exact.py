"""Independent exact checks of finite CTMC reversal projection.

Fractions and prime-log coefficient cancellation only. No trajectories,
physical records, floating entropy comparisons, or imported producer code.
"""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import hashlib
import json


def log_factor(x):
    out = defaultdict(F)
    for value, sign in [(x.numerator, 1), (x.denominator, -1)]:
        d = 2
        while d * d <= value:
            while value % d == 0:
                out[d] += sign
                value //= d
            d += 1
        if value > 1:
            out[value] += sign
    return {k: v for k, v in out.items() if v}


def add_log(out, coeff, arg):
    for prime, power in log_factor(arg).items():
        out[str(prime)] += coeff * power


def rate(p, q, h):
    out = defaultdict(F)
    for i in range(len(p)):
        for j in range(len(p)):
            if i != j:
                add_log(out, p[i]*q[i][j], q[i][j]/h[i][j])
                out['constant'] += p[i]*(h[i][j]-q[i][j])
    return {k: v for k, v in out.items() if v}


def initial(p, q):
    out = defaultdict(F)
    for a, b in zip(p, q):
        add_log(out, a, a/b)
    return {k: v for k, v in out.items() if v}


def residual(*terms):
    out = defaultdict(F)
    for coeff, item in terms:
        for k, v in item.items():
            out[k] += coeff*v
    return {k: str(v) for k, v in out.items() if v}


def generator(flux, p):
    n = len(p)
    q = [[flux[i][j]/p[i] if i != j else F(0) for j in range(n)] for i in range(n)]
    for i in range(n):
        q[i][i] = -sum(q[i])
    return q


def stationary(p, q):
    return all(sum(p[i]*q[i][j] for i in range(len(p))) == 0 for j in range(len(p)))


def run_case(n, theta):
    rho = [F((i+1)**2, sum((j+1)**2 for j in range(n))) for i in range(n)]
    q = [rho[theta[i]] for i in range(n)]
    mu = [(a+b)/2 for a,b in zip(rho,q)]
    flux = [[F(0) if i==j else F(1+2*(j==(i+1)%n)+(j==(i-1)%n)) for j in range(n)] for i in range(n)]
    rflux = [[flux[theta[j]][theta[i]] for j in range(n)] for i in range(n)]
    avg = [[(flux[i][j]+rflux[i][j])/2 for j in range(n)] for i in range(n)]
    L = generator(flux, rho)
    R = generator(rflux, q)
    Lbar = generator(avg, mu)
    raw_nu = [F(2+i+theta[i]) for i in range(n)]
    nu = [x/sum(raw_nu) for x in raw_nu]
    other_flux = [[F(0) if i==j else F(2+(j==(i+2)%n)) for j in range(n)] for i in range(n)]
    G = [[(other_flux[i][j]+other_flux[theta[j]][theta[i]])/2 for j in range(n)] for i in range(n)]
    H = generator(G, nu)
    assert stationary(rho,L) and stationary(q,R) and stationary(mu,Lbar) and stationary(nu,H)
    assert all(Lbar[i][i] == Lbar[theta[i]][theta[i]] for i in range(n))
    assert all(nu[i] == nu[theta[i]] for i in range(n))
    rate_projection = residual((1,rate(rho,L,H)),(-1,rate(rho,L,Lbar)),(-1,rate(mu,Lbar,H)))
    initial_projection = residual((1,initial(rho,nu)),(-1,initial(rho,mu)),(-1,initial(mu,nu)))
    forward_reverse_rate = residual((1,rate(rho,L,R)),(-1,rate(q,R,L)))
    forward_reverse_surrogate = residual((1,rate(rho,L,Lbar)),(-1,rate(q,R,Lbar)))
    assert not rate_projection and not initial_projection and not forward_reverse_rate and not forward_reverse_surrogate
    return {'states':n,'theta':theta,'rho':[str(v) for v in rho],
            'checks':'stationarity; paired clocks; exact initial/rate Pythagoras; equal reversal-related rates',
            'residuals':[rate_projection,initial_projection,forward_reverse_rate,forward_reverse_surrogate]}


def main():
    result={'status':'PASS','scope':'independent exact symbolic controls, not a proof of all models or a physical acquisition',
            'cases':[run_case(3,[1,0,2]),run_case(4,[1,0,2,3]),run_case(5,[1,0,3,2,4])],
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    path=Path(__file__).with_name('REVERSAL_PROJECTION_EXACT_REVIEW_CHECKS.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
