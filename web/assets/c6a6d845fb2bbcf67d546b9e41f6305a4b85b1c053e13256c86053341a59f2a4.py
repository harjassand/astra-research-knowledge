"""Numerical falsification probes of the full-separability construction.

No hardware quantum gates are run. Exact sector matrices and a finite positive
Gaussian-filter mixture are simulated with numpy only.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
import numpy as np
from spin_glass_checks import sector_data, spin_operators


A = np.diag([.1, -.08, .03])
b = np.array([.12, .08, .11])
M = .1
B = .2


def exp_hermitian(H):
    vals, vecs = np.linalg.eigh(H)
    return (vecs*np.exp(vals)[None, :])@vecs.conj().T


def irrep_spins(j2):
    j = j2/2
    m = np.arange(j, -j-1, -1)
    plus = np.zeros((j2+1, j2+1), complex)
    for k in range(1, j2+1):
        plus[k-1, k] = math.sqrt((j-m[k])*(j+m[k]+1))
    return [(plus+plus.conj().T)/2,
            (plus-plus.conj().T)/2j, np.diag(m).astype(complex)]


def exact_filter_semigroup_I(H, Js, cs):
    squares = [J@J for J in Js]
    def L(X):
        answer = (H@X+X@H)/2
        for c, J, Jsq in zip(cs, Js, squares):
            answer -= c/4*(Jsq@X-2*J@X@J+X@Jsq)
        return answer
    total = np.eye(len(H), dtype=complex)
    term = total.copy()
    for k in range(1, 80):
        term = L(term)/k
        total += term
        if np.linalg.norm(term, 'fro') < 1e-15*np.linalg.norm(total, 'fro'):
            break
    else:
        raise RuntimeError('Taylor series did not converge')
    return (total+total.conj().T)/2


def finite_filter_mixture_I(Js, cs, v, steps):
    # The quadratic eigenbasis formula is the EXACT Gaussian expectation.
    quadratic = []
    for J, c in zip(Js, cs):
        vals, vecs = np.linalg.eigh(J)
        multiplier = np.exp(c/(4*steps)*(vals[:, None]+vals[None, :])**2)
        quadratic.append((vecs, multiplier))
    field = exp_hermitian(sum(v[k]*Js[k] for k in range(3))/(2*steps))
    X = np.eye(len(Js[0]), dtype=complex)
    for _ in range(steps):
        for vecs, mult in quadratic:
            X = vecs@((vecs.conj().T@X@vecs)*mult)@vecs.conj().T
        X = field@X@field
    return (X+X.conj().T)/2


def public_bound(N):
    js, rs, weights = sector_data(N)
    tilt = M*rs**2+B*rs
    P = 4*M*rs**2+B*rs/2+(4*M*rs**2+B*rs)**2/3
    ratio = float(np.sum(weights*np.exp(tilt)*P)/np.sum(weights*np.exp(-tilt)))
    result = 3*M/(2*N**1.5)*ratio
    return dict(N=N, bound=result, N_3_2_times_bound=result*N**1.5, moment_ratio=ratio)


def whole_sector_check(N, finite_steps=(1, 2, 4, 8)):
    js, rs, a = sector_data(N)
    scalar = a*np.exp(-M*js*(js+1)/N**1.5)/(2*js+1)
    cs = np.diag(A+M*np.eye(3))/N**1.5
    v = b/N**.75
    targets, factories = [], []
    finite = {steps: [] for steps in finite_steps}
    for j in js:
        Js = irrep_spins(int(round(2*j)))
        H = sum(cs[k]*Js[k]@Js[k]+v[k]*Js[k] for k in range(3))
        target = exp_hermitian(H)
        factory = exact_filter_semigroup_I(H, Js, cs)
        assert min(np.linalg.eigvalsh(factory)) > -1e-11
        targets.append(target)
        factories.append(factory)
        for steps in finite_steps:
            finite[steps].append(finite_filter_mixture_I(Js, cs, v, steps))
    def trace_sum(blocks):
        return sum(w*np.trace(X).real for w,X in zip(scalar, blocks))
    Ztarget, Zfactory = trace_sum(targets), trace_sum(factories)
    def T(blocks1, Z1, blocks2, Z2):
        return sum(w*sum(abs(np.linalg.eigvalsh(X/Z1-Y/Z2)))/2
                   for w,X,Y in zip(scalar, blocks1, blocks2))
    error = float(T(targets, Ztarget, factories, Zfactory))
    certificate = public_bound(N)['bound']
    assert error <= certificate+1e-12
    return dict(N=N, exact_semigroup_trace_error=error,
                N_3_2_times_error=error*N**1.5,
                public_bound=certificate,
                trace_ratio=Zfactory/Ztarget,
                finite_Trotter=[dict(steps=steps,
                    trace_error_to_Gibbs=float(T(targets,Ztarget,blocks,trace_sum(blocks))),
                    trace_error_to_semigroup=float(T(factories,Zfactory,blocks,trace_sum(blocks))))
                    for steps,blocks in finite.items()])


def weighted_product_simulation(N=4, steps=8, samples=12000, seed=1037):
    """An actual finite sampler diagnostic, with an un-certified CDF grid."""
    rng = np.random.default_rng(seed)
    t0 = 2/N-M/N**1.5
    radial = np.linspace(0, 14, 140001)
    half = radial/2
    logsinch = np.zeros_like(radial)
    logsinch[1:] = np.log(np.sinh(half[1:])/half[1:])
    logdensity = np.full_like(radial, -np.inf)
    logdensity[1:] = (2*np.log(radial[1:])+logsinch[1:]
                       -radial[1:]**2/(4*t0)
                       +N*np.logaddexp(half[1:], -half[1:]))
    density = np.exp(logdensity-np.max(logdensity))
    cdf = np.concatenate(([0.], np.cumsum((density[1:]+density[:-1])/2)))
    cdf /= cdf[-1]
    paulis = [np.array([[0,1],[1,0]], complex),
              np.array([[0,-1j],[1j,0]], complex), np.diag([1,-1]).astype(complex)]
    cs = np.diag(A+M*np.eye(3))/N**1.5
    v = b/N**.75
    vnorm = np.linalg.norm(v)
    field = np.cosh(vnorm/(4*steps))*np.eye(2)+np.sinh(vnorm/(4*steps))*sum(v[k]/vnorm*paulis[k] for k in range(3))
    output = np.zeros((2**N,2**N), complex)
    weight_sum = weight_sq_sum = 0.
    for _ in range(samples):
        radius = np.interp(rng.random(), cdf, radial)
        z = rng.uniform(-1,1)
        phi = rng.uniform(0, 2*math.pi)
        u = np.array([math.sqrt(1-z*z)*math.cos(phi), math.sqrt(1-z*z)*math.sin(phi), z])
        tau = (np.eye(2)+math.tanh(radius/2)*sum(u[k]*paulis[k] for k in range(3)))/2
        g = np.eye(2, dtype=complex)
        for _ in range(steps):
            for k in range(3):
                boost = math.sqrt(cs[k]/(2*steps))*rng.normal()/2
                g = (math.cosh(boost)*np.eye(2)+math.sinh(boost)*paulis[k])@g
            g = field@g
        local = g@tau@g.conj().T
        normalization = np.trace(local).real
        weight = normalization**N
        local /= normalization
        branch = np.ones((1,1), complex)
        for _ in range(N):
            branch = np.kron(branch, local)
        output += weight*branch
        weight_sum += weight
        weight_sq_sum += weight*weight
    output /= weight_sum
    Js = spin_operators(N)
    Jsq = sum(J@J for J in Js)
    H = sum(cs[k]*Js[k]@Js[k]+v[k]*Js[k] for k in range(3))
    base = exp_hermitian(t0*Jsq)
    # finite_filter_mixture_I handles I; central base commutes with all filters.
    exact_finite = base@finite_filter_mixture_I(Js, cs, v, steps)
    exact_finite /= np.trace(exact_finite).real
    target = exp_hermitian(t0*Jsq+H)
    target /= np.trace(target).real
    empirical_ratio = samples*weight_sq_sum/weight_sum**2
    return dict(N=N, steps=steps, proposals=samples, seed=seed,
                empirical_weight_second_moment_ratio=empirical_ratio,
                density_simulation_trace_error_to_finite_mixture=float(sum(abs(np.linalg.eigvalsh(output-exact_finite)))/2),
                density_simulation_trace_error_to_Gibbs=float(sum(abs(np.linalg.eigvalsh(output-target)))/2),
                exact_finite_trace_error_to_Gibbs=float(sum(abs(np.linalg.eigvalsh(exact_finite-target)))/2),
                scope='Numerical CDF grid and finite Monte Carlo, not certified sampler or quantum hardware.')


def main():
    data = dict(scope='Numerical diagnostics; analytical proof remains separate.',
                whole_density=[whole_sector_check(N) for N in [8,16,32,64]],
                public_certificates=[public_bound(N) for N in [64,256,1024,4096,16384]],
                weighted_product_sampler=weighted_product_simulation())
    target = Path(__file__).with_name('spin_sep_checks.json')
    target.write_text(json.dumps(data, indent=2))
    print(json.dumps(data, indent=2))
    print('Saved', target)


if __name__ == '__main__':
    main()
