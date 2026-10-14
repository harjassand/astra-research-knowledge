#!/usr/bin/env python3
"""Checks for a proposed electronic pressure-isolation operation.

These are algebraic and lumped-network checks, not experimental evidence,
not a microscopic material simulation, and not a novelty certification.
Dependencies: numpy, sympy. Run: python check_model.py
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import sympy as sp


def hydraulic_matrix(k: np.ndarray, c: np.ndarray, g: np.ndarray,
                     y: np.ndarray) -> np.ndarray:
    """Eliminate a passive electrical load from reciprocal wet transducers."""
    k, c, g, y = map(lambda z: np.asarray(z, dtype=float), (k, c, g, y))
    n = len(k)
    if c.shape != (n,) or g.shape != (n,) or y.shape != (n, n):
        raise ValueError('Incompatible dimensions')
    if np.any(k <= 0) or np.any(g <= 0) or np.any(c*c >= k*g):
        raise ValueError('Wet transducers must be strictly passive')
    if np.linalg.eigvalsh((y+y.T)/2).min() < -1e-10:
        raise ValueError('The electrical load is not passive')
    cm = np.diag(c)
    return np.diag(k) - cm @ np.linalg.solve(np.diag(g)+y, cm)


def single_converter_eta(z: float) -> float:
    """Maximum linear-response hydraulic/electrical conversion efficiency."""
    if z < 0:
        raise ValueError('z must be nonnegative')
    # This expression is stable for small z.
    return z/(1+np.sqrt(1+z))**2


def symbolic_checks() -> list[str]:
    k1,k2,c1,c2,g1,g2,gp,gm = sp.symbols(
        'k1 k2 c1 c2 g1 g2 gp gm', positive=True)
    c = sp.diag(c1,c2)
    y = sp.Matrix([[gp+gm,-gm],[-gp,gp+gm]])
    a = sp.diag(g1,g2)+y
    h = sp.diag(k1,k2)-c*a.inv()*c
    assert sp.simplify(h[1,0]*gm-h[0,1]*gp)==0
    assert sp.simplify(h-h.T-c*a.inv().T*(y-y.T)*a.inv()*c)==sp.zeros(2)
    # In the ideal chiral limit reverse hydraulic influence vanishes.
    assert sp.simplify(h[0,1].subs(gm,0)) == 0

    # Fixed hydraulic matrix H=[[kappa1,0],[b,kappa2]], output resistance R.
    b,kap1,kap2,r,p = sp.symbols('b kap1 kap2 r p', positive=True)
    q2 = b*p/(1+kap2*r)
    eta = sp.cancel(r*q2**2/(kap1*p**2))
    derivative = sp.factor(sp.diff(eta,r))
    assert sp.simplify(derivative-b*b*(1-kap2*r)/(kap1*(1+kap2*r)**3))==0
    assert sp.simplify(eta.subs(r,1/kap2)-b*b/(4*kap1*kap2))==0

    # Dimensionless matching: chi=1-s^2, 0<s<1; t=g_H/G.
    s,t = sp.symbols('s t', positive=True)
    f = (1-s*s)*t/((1+t)*(t+s*s))
    assert sp.simplify(sp.diff(f,t)-(1-s*s)*(s*s-t*t)/((1+t)**2*(t+s*s)**2))==0
    assert sp.simplify(f.subs(t,s)-(1-s)/(1+s))==0
    # Product bound: eta_iso,max = eta_converter(Z1)*eta_converter(Z2)/4.
    return [
        'exact off-diagonal asymmetry transfer',
        'exact antisymmetric Schur-complement identity',
        'zero reverse response in the ideal chiral limit',
        'optimal output hydraulic load R=1/kappa2',
        'optimal electrical matching t=sqrt(1-chi)',
        'factorized conversion/4 efficiency ceiling',
    ]


def numerical_checks(seed: int = 20261014, trials: int = 1000) -> dict:
    rng = np.random.default_rng(seed)
    worst_passivity_eigenvalue = float('inf')
    max_reciprocity_error = 0.0
    max_power_residual = 0.0
    max_antisymmetric_identity_error = 0.0
    for _ in range(trials):
        n=4
        k=np.exp(rng.uniform(-2,2,n)); g=np.exp(rng.uniform(-2,2,n))
        chi=rng.uniform(0.01,0.99,n)
        c=np.sqrt(chi*k*g)*rng.choice([-1,1],n)
        w=rng.normal(size=(n,n)); d=w@w.T/4
        v=rng.normal(size=(n,n)); a=(v-v.T)/2
        y=d+a
        h=hydraulic_matrix(k,c,g,y)
        hb=hydraulic_matrix(k,c,g,y.T)
        max_reciprocity_error=max(max_reciprocity_error,float(np.max(abs(hb-h.T))))
        worst_passivity_eigenvalue=min(worst_passivity_eigenvalue,float(np.linalg.eigvalsh((h+h.T)/2).min()))
        am=np.diag(g)+y; cm=np.diag(c); ai=np.linalg.inv(am)
        rhs=cm@ai.T@(y-y.T)@ai@cm
        max_antisymmetric_identity_error=max(max_antisymmetric_identity_error,float(np.max(abs(h-h.T-rhs))))
        p=rng.normal(size=n)
        volt=-np.linalg.solve(am,c*p)
        q=k*p+c*volt
        current=c*p+g*volt
        wet=float(p@q+volt@current)
        dry=float(volt@y@volt)
        residual=float(p@q-wet-dry)
        max_power_residual=max(max_power_residual,abs(residual))
        assert wet>=-1e-10 and dry>=-1e-10
        assert np.linalg.matrix_rank(h-h.T)==np.linalg.matrix_rank(y-y.T)
    assert worst_passivity_eigenvalue>0
    assert max_reciprocity_error<1e-10
    assert max_power_residual<1e-10
    assert max_antisymmetric_identity_error<1e-10
    return dict(seed=seed,trials=trials,ports_per_trial=4,
        minimum_symmetric_hydraulic_eigenvalue=worst_passivity_eigenvalue,
        maximum_onsager_casimir_error=max_reciprocity_error,
        maximum_power_balance_residual=max_power_residual,
        maximum_antisymmetric_identity_error=max_antisymmetric_identity_error,
        note='Finite floating-point diagnostics of a specified network model only.')


def table() -> list[dict]:
    rows=[]
    for z in [0.0004,1.,11.,100.,1000.]:
        eta=single_converter_eta(z)
        rows.append(dict(z=z,single_converter_max_efficiency=eta,
            ideal_chiral_isolator_max_efficiency=eta*eta/4,
            ideal_lossless_gyrator_pair_max_efficiency=eta*eta,
            provenance=('Published theoretical estimate used as a conditional input; '
                        'not a measured complete transducer.' if z in (0.0004,11.)
                        else 'Hypothetical dimensionless input; not a material claim.')))
    return rows


def check_matching_grid() -> dict:
    points=0
    max_excess=0.
    for z1,z2 in [(0.0004,0.0004),(1,11),(11,11),(100,1000)]:
        chi1=z1/(1+z1); chi2=z2/(1+z2)
        target=single_converter_eta(z1)*single_converter_eta(z2)/4
        for t1 in np.logspace(-4,4,101):
            for t2 in np.logspace(-4,4,101):
                f1=chi1*t1/((1+t1)*(1+t1-chi1))
                f2=chi2*t2/((1+t2)*(1+t2-chi2))
                max_excess=max(max_excess,float(f1*f2/4-target))
                points+=1
        ts=[np.sqrt(1-chi1),np.sqrt(1-chi2)]
        fs=[ch*t/((1+t)*(1+t-ch)) for ch,t in zip([chi1,chi2],ts)]
        assert abs(fs[0]*fs[1]/4-target)<1e-12
    assert max_excess<1e-12
    return dict(points=points,maximum_excess_above_bound=max_excess)


if __name__=='__main__':
    report=dict(status='MODEL CHECKS ONLY; NO PHYSICAL EXPERIMENT',
        symbolic_checks=symbolic_checks(),network_checks=numerical_checks(),
        matching_grid=check_matching_grid(),conditional_table=table())
    path=Path(__file__).resolve().parent/'model_checks.json'
    path.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
