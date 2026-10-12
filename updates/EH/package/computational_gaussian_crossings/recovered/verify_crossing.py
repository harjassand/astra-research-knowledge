"""Diagnostics for entry-biased finite-spectrum Gaussian hazard estimation.

This is NOT a general convex-body sampler or the complete finite-bit FPRAS.
Monte Carlo checks use independent single-frequency coordinates, for which all
proposal normalizers and conditional samplers are explicit. SymPy checks are
exact rational algebra. Floating-point roots are used only in the MC diagnostic.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.special import ndtr, ndtri_exp, log_ndtr, logsumexp, erfcx
from scipy.integrate import quad

SEED = 20261012
rng = np.random.default_rng(SEED)
W0, W1 = 0.25, 0.75
V0 = W0 + W1


def witness_count(c: np.ndarray, a: np.ndarray, b: np.ndarray,
                  threshold: float, phase: np.ndarray | None = None) -> np.ndarray:
    """W = indicator of being inside at phase + total full-period entries."""
    n, dim = c.shape
    if phase is None:
        phase = np.zeros(n)
    start = c + a*np.cos(phase[:, None]) + b*np.sin(phase[:, None])
    out = np.all(start > threshold, axis=1).astype(np.int64)
    for i in range(dim):
        amp = np.hypot(a[:, i], b[:, i])
        ratio = np.divide(threshold-c[:, i], amp,
                          out=np.full(n, np.inf), where=amp > 0)
        crossing = np.abs(ratio) < 1
        angle = np.arctan2(b[:, i], a[:, i]) - np.arccos(np.clip(ratio, -1, 1))
        vals = c + a*np.cos(angle[:, None]) + b*np.sin(angle[:, None])
        valid = crossing.copy()
        for j in range(dim):
            if j != i:
                valid &= vals[:, j] > threshold
        out += valid
    return out


def conditional_position_samples(n: int, dim: int, u: float) -> np.ndarray:
    logsf = log_ndtr(-u / np.sqrt(V0))
    uniforms = np.maximum(rng.random((n, dim)), np.finfo(float).tiny)
    return -np.sqrt(V0)*ndtri_exp(logsf + np.log(uniforms))


def proposal(n: int, dim: int, u: float):
    logq = log_ndtr(-u/np.sqrt(V0))
    lognu = .5*np.log(W1/V0) - u*u/(2*V0)
    logweights = np.array([dim*logq] + [lognu+(dim-1)*logq]*dim)
    logmu = float(logsumexp(logweights))
    probs = np.exp(logweights-logmu)
    component = rng.choice(dim+1, n, p=probs)
    z = conditional_position_samples(n, dim, u)
    c = rng.normal(scale=np.sqrt(W0), size=(n, dim))
    a = rng.normal(scale=np.sqrt(W1), size=(n, dim))
    b = rng.normal(scale=np.sqrt(W1), size=(n, dim))
    for i in range(dim):
        take = component == i+1
        z[take, i] = u
        b[take, i] = rng.rayleigh(scale=np.sqrt(W1), size=int(np.sum(take)))
    correction = z-(c+a)
    c += (W0/V0)*correction
    a += (W1/V0)*correction
    # The entry part is shifted by a uniform phase; the initial-inside part is not.
    phase = np.where(component > 0, rng.uniform(0, 2*np.pi, n), 0.0)
    w = witness_count(c, a, b, u, phase)
    if np.any(w < 1) or np.any(w > dim+1):
        raise AssertionError(f"Invalid witness count: {np.unique(w, return_counts=True)}")
    score = 1.0/w
    return logmu, score, w


def rare_diagnostic(dim: int, u: float, n: int = 40000):
    logmu, score, w = proposal(n, dim, u)
    mean = float(score.mean())
    rel_se = float(score.std(ddof=1)/np.sqrt(n)/mean)
    result = dict(dimension=dim, fourier_degree=1, threshold=u,
                  samples=n, log_normalizer=logmu,
                  log_probability_estimate=logmu+np.log(mean),
                  log10_probability_estimate=(logmu+np.log(mean))/np.log(10),
                  mean_inverse_witness=mean, estimated_relative_standard_error=rel_se,
                  relative_variance=float(score.var(ddof=1)/mean**2),
                  theoretical_relative_variance_bound=dim,
                  observed_witness_counts={str(int(k)):int(v) for k,v in zip(*np.unique(w,return_counts=True))})
    if dim == 1:
        # Exact P(C + sqrt(A^2+B^2) > u), C~N(0,W0), A,B~N(0,W1).
        logexact = logsumexp([
            log_ndtr(-u/np.sqrt(W0)),
            .5*np.log(W1/V0)-u*u/(2*V0)
            +log_ndtr(u*np.sqrt(W1/(W0*V0)))])
        result['log_probability_exact'] = float(logexact)
        result['relative_error_against_exact'] = float(np.expm1(result['log_probability_estimate']-logexact))
    if dim == 2 and u in (0., 1., 2.):
        n_direct=300000
        cc=rng.normal(scale=np.sqrt(W0),size=(n_direct,dim))
        aa=rng.normal(scale=np.sqrt(W1),size=(n_direct,dim))
        bb=rng.normal(scale=np.sqrt(W1),size=(n_direct,dim))
        hits=witness_count(cc,aa,bb,u)>0
        p=float(hits.mean())
        result['direct_samples']=n_direct
        result['direct_estimate']=p
        result['direct_standard_error']=float(np.sqrt(p*(1-p)/n_direct))
        result['proposal_estimate']=float(np.exp(result['log_probability_estimate']))
    return result


def exact_regression_check():
    dc=sp.eye(2)/4
    s=sp.eye(2)
    t=sp.Matrix([[0,sp.Rational(3,5)],[-sp.Rational(3,5),0]])
    cov=sp.diag(dc,s.row_join(t).col_join((-t).row_join(s)))
    obs=sp.Matrix([[1,0,1,0,0,0],[0,1,0,1,0,0],[0,0,0,0,1,0]])
    gain=cov*obs.T*(obs*cov*obs.T).inv()
    residual=sp.eye(6)-gain*obs
    assert obs*gain==sp.eye(3)
    assert obs*residual==sp.zeros(3,6)
    cond=residual*cov*residual.T
    assert cond==cov-gain*obs*cov
    # E[V+ 1(Y>u)] cannot in general be factored, even for stationary vector noise.
    u=1.0; var_y=1.25
    flux=[]
    for cv in [-.6,0.,.6]:
        sigma=np.sqrt(1-cv*cv/var_y)
        def integrand(y):
            mu=cv*y/var_y
            posmean=sigma*np.exp(-.5*(mu/sigma)**2)/np.sqrt(2*np.pi)+mu*ndtr(mu/sigma)
            return posmean*np.exp(-y*y/(2*var_y))/np.sqrt(2*np.pi*var_y)
        val,err=quad(integrand,u,np.inf,epsabs=1e-12)
        flux.append(dict(position_velocity_covariance=cv,flux=val,quadrature_error=err))
    return dict(constraints_preserved_exactly=True,conditional_covariance_identity=True,flux_comparison=flux)


def grazing_checks():
    x=sp.Symbol('x')
    k=sp.Integer(652)
    cs=(k*k-1)/(k*k+1); sn=2*k/(k*k+1)
    grid=np.arange(1024)*2*np.pi/1024
    out=[]
    for bits in [20,80,200,1000]:
        amp=1+sp.Rational(1,2**bits)
        poly=sp.Poly((amp*cs-1)+2*amp*sn*x+(-amp*cs-1)*x*x,x)
        roots=int(poly.count_roots(-sp.oo,sp.oo))
        assert roots==2
        vals=float(amp)*(float(cs)*np.cos(grid)+float(sn)*np.sin(grid))
        out.append(dict(excess_amplitude_bits=bits,exact_real_crossing_count=roots,
                        exact_entry_count=1,uniform_grid_points=1024,
                        grid_reports_hit=bool(np.any(vals>1)),grid_max=float(vals.max())))
    return out


def lifting_checks():
    out=[]
    for u in [0.,2.,8.,100.]:
        exact=np.sqrt(np.pi/2)*erfcx(u/np.sqrt(2))
        for k in [64,512,4096]:
            def fun(y):
                if y>=k:return 0.
                return np.exp(k*np.log1p(-y/k))/np.sqrt(u*u+2*y)
            upper=min(float(k),100.)
            approx,err=quad(fun,0.,upper,epsabs=1e-12,limit=200)
            out.append(dict(threshold=u,lift_dimension=k,shifted_integral_exact=float(exact),
                            shifted_integral_approx=float(approx),
                            relative_deficit=float(1-approx/exact),quadrature_error=float(err)))
    return out


def main():
    rows=[]
    for dim in [1,2]:
        for u in [-1.,0.,1.,2.,4.,8.,100.]:
            rows.append(rare_diagnostic(dim,u))
    results=dict(status='small-case diagnostics; not a general convex-body FPRAS implementation',
                 seed=SEED,rare_event_tests=rows,exact_regression=exact_regression_check(),
                 grazing=grazing_checks(),convex_power_lift=lifting_checks())
    path=Path(__file__).with_name('verification_results.json')
    path.write_text(json.dumps(results,indent=2))
    print(path)
    for row in rows:
        print(row['dimension'], row['threshold'], 'log10 p =', round(row['log10_probability_estimate'],6),
              'rel SE =', round(row['estimated_relative_standard_error'],6))
    print('Exact rational regression and grazing checks passed.')

if __name__=='__main__':
    main()
