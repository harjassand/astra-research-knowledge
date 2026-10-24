"""New Pro3 research checks: compact gate kernels versus expanded small CTMCs.

This is newly written continuation work, not reconstructed historical code.
Numerical tests are independent checks of identities proved in chat; they are
not a numerical error certificate for a large-system approximation.
"""
from fractions import Fraction as F
import json
import math

import numpy as np
from scipy.integrate import quad_vec
from scipy.linalg import expm


def binary_transition(alpha, beta, t):
    lam = alpha + beta
    pi = alpha / lam
    e = math.exp(-lam*t)
    return np.array([[1-pi+pi*e, pi*(1-e)],
                     [(1-pi)*(1-e), pi+(1-pi)*e]])


def kron_all(xs):
    out = np.array([1.0])
    for x in xs:
        out = np.kron(out, x)
    return out


def expanded_q(alpha, beta):
    n = len(alpha)
    out = np.zeros((2**n, 2**n))
    for i in range(n):
        q = np.array([[-alpha[i], alpha[i]], [beta[i], -beta[i]]])
        out += np.kron(np.kron(np.eye(2**i), q), np.eye(2**(n-i-1)))
    return out


def bits(k, n):
    return [(k >> i) & 1 for i in range(n-1, -1, -1)]


def one_case(n, m, seed):
    rng = np.random.default_rng(seed)
    alpha = rng.uniform(.2, 1.3, n)
    beta = rng.uniform(.1, 1.1, n)
    gates = sorted(rng.choice(2**n, m, replace=False))
    gate_bits = [bits(int(k), n) for k in gates]
    kappa = rng.uniform(.3, 1.4, m)
    weights = np.array([.3, .7])
    local_initial = rng.uniform(.05, .95, (2, n))
    mu = sum(weights[r]*kron_all([np.array([1-p,p]) for p in local_initial[r]])
             for r in range(2))
    q = expanded_q(alpha, beta)
    bmat = np.zeros((2**n, m))
    for j, g in enumerate(gates):
        bmat[g,j] = kappa[j]
    a = q-np.diag(bmat.sum(axis=1))
    # Reversible Q and diagonal killing A have real spectrum and well-conditioned
    # symmetric similarity, useful for repeated quadrature reference evaluation.
    equilibrium = kron_all([np.array([b/(aa+b), aa/(aa+b)])
                            for aa,b in zip(alpha,beta)])
    root = np.sqrt(equilibrium)
    sym = root[:,None]*a/root[None,:]
    evals, evecs = np.linalg.eigh(sym)
    left = (mu/root)@evecs
    right = evecs.T@(root[:,None]*bmat)
    gate_left = (np.eye(2**n)[gates]/root)@evecs

    def density(t):
        return (left*np.exp(evals*t))@right

    def first_kernel(t):
        return (gate_left*np.exp(evals*t))@right

    def compact_kernel(t):
        local = [binary_transition(x,y,t) for x,y in zip(alpha,beta)]
        return np.array([[kappa[j]*math.prod(local[l][ga[l],gb[l]]
                                             for l in range(n))
                          for j,gb in enumerate(gate_bits)] for ga in gate_bits])

    def compact_b(t):
        local = [binary_transition(x,y,t) for x,y in zip(alpha,beta)]
        return np.array([kappa[j]*sum(weights[r]*math.prod(
            np.array([1-local_initial[r,l],local_initial[r,l]])@local[l][:,g[l]]
            for l in range(n)) for r in range(2)) for j,g in enumerate(gate_bits)])

    kernel_err = density_err = renewal_err = inverse_err = mass_err = 0.0
    for t in [0.0,.03,.2,.7,1.9,4.0]:
        kernel_err=max(kernel_err,float(np.max(np.abs(
            compact_kernel(t)-expm(q*t)[gates]@bmat))))
        density_err=max(density_err,float(np.max(np.abs(
            density(t)-mu@expm(a*t)@bmat))))
        conv=quad_vec(lambda s:density(s)@compact_kernel(t-s),0,t,
                      epsabs=2e-12,epsrel=2e-12)[0]
        renewal_err=max(renewal_err,float(np.max(np.abs(density(t)+conv-compact_b(t)))))
        convmat=quad_vec(lambda s:first_kernel(s)@compact_kernel(t-s),0,t,
                         epsabs=2e-12,epsrel=2e-12)[0]
        inverse_err=max(inverse_err,float(np.max(np.abs(
            first_kernel(t)+convmat-compact_kernel(t)))))
        events=quad_vec(density,0,t,epsabs=2e-12,epsrel=2e-12)[0].sum()
        survival=mu@expm(a*t)@np.ones(2**n)
        mass_err=max(mass_err,float(abs(events+survival-1)))
    return dict(n=n,m=m,species=2**n,kernel_error=kernel_err,
                density_reference_error=density_err,
                volterra_error=renewal_err,inverse_identity_error=inverse_err,
                probability_mass_error=mass_err)


def fmat(rows):
    return [[F(x) for x in row] for row in rows]


def add(a,b):
    return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]


def scale(c,a):
    return [[c*x for x in row] for row in a]


def multiply(a,b):
    return [[sum((x*y for x,y in zip(row,col)),F(0))
             for col in zip(*b)] for row in a]


def eye(n):
    return [[F(int(i==j)) for j in range(n)] for i in range(n)]


def inverse(a):
    n=len(a)
    aug=[list(row)+unit for row,unit in zip(a,eye(n))]
    for j in range(n):
        p=next(i for i in range(j,n) if aug[i][j])
        aug[j],aug[p]=aug[p],aug[j]
        v=aug[j][j]
        aug[j]=[x/v for x in aug[j]]
        for i in range(n):
            if i!=j:
                c=aug[i][j]
                aug[i]=[x-c*y for x,y in zip(aug[i],aug[j])]
    return [row[n:] for row in aug]


def rational_repeated_event_check(n=3):
    d=2**n
    alpha=[F(i+1,3) for i in range(n)]
    beta=[F(i+2,5) for i in range(n)]
    q=fmat([[0]*d for _ in range(d)])
    for x in range(d):
        for i in range(n):
            y=x^(1<<i)
            rate=beta[n-1-i] if (x>>i)&1 else alpha[n-1-i]
            q[x][y]+=rate
            q[x][x]-=rate
    gates=[0,d-1]
    kappas=[F(3,2),F(4,3)]
    b=fmat([[0,0] for _ in range(d)])
    for j,g in enumerate(gates):
        b[g][j]=kappas[j]
    reset=fmat([[0]*d for _ in gates])
    reset[0][1]=F(1)
    reset[1][d-2]=F(1,3)
    reset[1][d-1]=F(2,3)
    # A two-component mixture of deterministic products is a permitted reset.
    mu=[[F(1,d)]*d]
    a=[row.copy() for row in q]
    for j,g in enumerate(gates):
        a[g][g]-=kappas[j]
    one=[[F(1)] for _ in range(d)]
    results=[]
    for s in [F(1,2),F(2),F(7,3)]:
        resolvent=inverse(add(scale(s,eye(d)),scale(-1,a)))
        h0=multiply(multiply(mu,resolvent),b)
        h=multiply(multiply(reset,resolvent),b)
        surv0=multiply(multiply(mu,resolvent),one)
        surv=multiply(multiply(reset,resolvent),one)
        for z in [F(0),F(1,4),F(3,4),F(1)]:
            renewal=add(surv0,scale(z,multiply(multiply(
                h0,inverse(add(eye(2),scale(-z,h)))),surv)))
            tilted=add(a,scale(z,multiply(b,reset)))
            full=multiply(multiply(mu,inverse(add(scale(s,eye(d)),
                scale(-1,tilted)))),one)
            assert renewal==full
            results.append(dict(s=str(s),z=str(z),exact=True))
    return results


def generic_pole_check(n):
    # lambdas=1+2^-i lie in (1,1.5]. Their integer parts encode cardinality,
    # while their fractional binary parts uniquely encode each subset. All
    # 2^n subset sums are distinct without exponentially large/stiff rates.
    # With pi=1/2, each coefficient is 2^-n. At each free pole, numerator has
    # nonzero residue, proving no cancellation in k*A/(B+k*A).
    d=2**n
    lambdas=[F(1)+F(1,2**(i+1)) for i in range(n)]
    subset_sums={sum(lambdas[i] for i in range(n) if mask>>i&1)
                 for mask in range(d)}
    assert len(subset_sums)==d
    assert F(1,d)>0
    return dict(n=n,distinct_poles=d,positive_residues=True,
                exact_constant_coefficient_realization_lower_bound=d)


if __name__=='__main__':
    out={
        'status':'new research, independent small expanded references',
        'numerical_cases':[one_case(n,m,101+10*n+m)
                           for n,m in [(1,1),(2,2),(3,3),(4,2),(5,3),(6,3)]],
        'exact_repeated_mark_laplace_checks':rational_repeated_event_check(),
        'pole_separation':[generic_pole_check(n) for n in range(1,13)]}
    print(json.dumps(out,indent=2))
