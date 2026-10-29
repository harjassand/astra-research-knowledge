"""Independent ordinary physical-velocity moment hierarchy through degree 4.

Built from direct isotropic velocity-collision expansion, not marked dual.
Exact rational coefficient construction; SciPy expm is a floating diagnostic.
"""
from functools import lru_cache
from time import perf_counter
import numpy as np
import sympy as s
from scipy.linalg import expm


@lru_cache(None)
def construct():
    started = perf_counter()
    x = s.Matrix(s.symbols('x y z'))
    variables = tuple(x)
    monomials = [(i,j,4-i-j) for i in range(5) for j in range(5-i)]
    terms = [x[0]**i*x[1]**j*x[2]**k for i,j,k in monomials]
    norm2 = (x.T*x)[0]
    def lap(p): return sum(s.diff(p,v,2) for v in variables)
    def coeff(p):
        p = s.Poly(s.expand(p),*variables)
        return s.Matrix([p.coeff_monomial(m) for m in monomials])
    operator = s.Matrix.hstack(*[coeff(-s.Rational(7,8)*p+norm2*lap(p)/48
                                     +norm2**2*lap(lap(p))/960) for p in terms])
    covs = [s.diag(1,s.Rational(21,20),s.Rational(11,10)),
            s.Matrix([[s.Rational(26,25),s.Rational(1,25),0],
                      [s.Rational(1,25),s.Rational(26,25),0],
                      [0,0,s.Rational(21,20)]])]
    c0 = (covs[0]+covs[1])/2
    mu = s.trace(c0)/3
    tau = s.Symbol('tau')
    cov = mu*s.eye(3)+tau*(c0-mu*s.eye(3))
    nc = (x.T*cov*x)[0]
    forcing = (s.Rational(3,8)*nc**2+norm2*nc*s.trace(cov)/4
               -norm2*(x.T*cov**2*x)[0]/2
               +norm2**2*(s.trace(cov)**2/40+s.trace(cov**2)/20))
    forcing_vectors = [coeff(s.expand(forcing).coeff(tau,i)) for i in range(3)]
    augmented = s.zeros(18)
    augmented[:15,:15] = operator
    for i,vec in enumerate(forcing_vectors): augmented[:15,15+i] = vec
    augmented[16,16] = -s.Rational(1,2)
    augmented[17,17] = -1
    fourth0 = sum(3*(x.T*c*x)[0]**2 for c in covs)/2
    initial = coeff(fourth0).col_join(s.ones(3,1))
    return dict(matrix=np.array(augmented,float),initial=np.array(initial,float).ravel(),
                cov0=np.array(c0,float),mu=float(mu),monomials=monomials,
                exact_matrix=augmented,exact_initial=initial,
                build_seconds=perf_counter()-started)


def moments(t, direction):
    data = construct()
    y = expm(t*data['matrix']) @ data['initial']
    n = np.asarray(direction,float)
    powers = np.array([np.prod(n**np.array(m)) for m in data['monomials']])
    cov = data['mu']*np.eye(3)+np.exp(-t/2)*(data['cov0']-data['mu']*np.eye(3))
    return float(n@cov@n),float(powers@y[:15])


@lru_cache(None)
def construct_resolved(variance=8):
    """Six-axis bounded core plus a declared common Gaussian variance."""
    data=construct()
    x=s.Matrix(s.symbols('x y z')); norm2=(x.T*x)[0]
    variance=s.Rational(variance)
    mu=variance+s.Rational(1,3)
    source=s.Poly(mu**2*norm2**2,*tuple(x))
    initial=s.Poly((3*variance**2+2*variance)*norm2**2+sum(v**4 for v in x)/3,*tuple(x))
    aug=s.zeros(16);aug[:15,:15]=data['exact_matrix'][:15,:15]
    aug[:15,15]=s.Matrix([source.coeff_monomial(m) for m in data['monomials']])
    y0=s.Matrix([initial.coeff_monomial(m) for m in data['monomials']]+[1])
    return np.array(aug,float),np.array(y0,float).ravel()


def resolved_moments(t,direction,variance=8):
    data=construct();matrix,initial=construct_resolved(variance)
    y=expm(t*matrix)@initial
    n=np.asarray(direction)
    powers=np.array([np.prod(n**np.array(m)) for m in data['monomials']])
    return ((variance+1/3)*(n@n)).item(),(powers@y[:15]).item()


if __name__ == '__main__':
    print('build',construct()['build_seconds'])
    for t in [0,1,3,30]: print(t,moments(t,[1,0,0]))
