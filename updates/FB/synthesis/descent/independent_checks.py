"""Independent exact/finite fixtures. Does not import the producer program.

Full proofs are in LOCALITY_OBSTRUCTION.md and the source RESEARCH_NOTE.md.
Small numerical fixtures do not certify general theorems or physical capability.
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
import numpy as np
import sympy as sy
from scipy.linalg import expm


def dstar(b, h):
    r = b.conj().T @ b
    return b.conj().T @ h @ b - (r @ h + h @ r) / 2


def completed(e, b):
    """Row-outer-product construction, independent of source nested-entry code."""
    drops = np.asarray(e)[None, :] - np.asarray(e)[:, None]
    roots = np.sqrt(np.maximum(drops, 0))
    c = roots * b
    g = np.zeros_like(b)
    for m in range(len(e)):
        q = roots[m]
        denominator = q[:, None] + q[None, :]
        kernel = np.divide(q[:, None] - q[None, :], denominator,
                           out=np.zeros_like(denominator), where=denominator > 0)
        g += 0.5j * kernel * np.outer(b[m].conj(), b[m])
    return g, c


def exact_star_checks():
    outputs = []
    for size in range(2, 7):
        roots = list(range(1, size + 1))
        weights = [sy.Integer(q*q) for q in roots]
        b = sy.zeros(size + 1)
        for j in range(size):
            b[0, j+1] = sy.Rational(j+1, size) + sy.I * sy.Rational(1, j+2)
        h = sy.diag(0, *weights)
        c, g = sy.zeros(size+1), sy.zeros(size+1)
        for j in range(size):
            c[0, j+1] = roots[j] * b[0, j+1]
            for k in range(size):
                g[j+1, k+1] = (sy.I/2 * sy.Rational(roots[j]-roots[k], roots[j]+roots[k])
                               * sy.conjugate(b[0, j+1]) * b[0, k+1])
        r = b.conjugate().T * b
        drift = b.conjugate().T*h*b-(r*h+h*r)/2+sy.I*(g*h-h*g)
        assert (drift+c.conjugate().T*c).applyfunc(sy.simplify) == sy.zeros(size+1)
        assert (g-g.conjugate().T).applyfunc(sy.simplify) == sy.zeros(size+1)
        for j in range(size):
            for k in range(j+1, size):
                asserted_sq = (abs(b[0,j+1])**2 * abs(b[0,k+1])**2
                               * sy.Rational((roots[j]-roots[k])**2,
                                             4*(roots[j]+roots[k])**2))
                assert sy.simplify(abs(g[j+1,k+1])**2-asserted_sq) == 0
        outputs.append({"excited_levels": size, "exact_identity": True,
                        "simultaneous_entrywise_bound": True})

    # An exact dark-state heating witness after finite Cauchy truncation.
    bs = sy.Matrix([[sy.Rational(1,2), sy.Rational(1,16)]])
    z = sy.Matrix([1, -1])/sy.sqrt(2)
    b = sy.Matrix([[1, 1]])
    trunc = -b.T*b/2 + bs.T*bs/2
    value = sy.simplify((z.T*trunc*z)[0])
    assert value == sy.Rational(49, 1024)
    # Distinct-frequency Cauchy reservoir has positive determinant/full rank.
    ranks = []
    for n in range(2, 8):
        # w_i=i^2, so the kernel entries are rational.
        k = sy.Matrix(n,n,lambda i,j: sy.Rational(2*(i+1)*(j+1), (i+1)**2+(j+1)**2))
        assert k.det() > 0 and k.rank() == n
        ranks.append({"frequencies": n, "rank": int(k.rank()),
                      "determinant_positive_exact": True})
    d = sy.symbols("d", positive=True)
    q = (sy.sqrt(1+d)-1)/(2*(sy.sqrt(1+d)+1))
    series = sy.series(1-sy.sqrt(1-d*d-4*q*q), d, 0, 4)
    assert sy.expand(series.removeO()).coeff(d,2) == sy.Rational(17,32)
    return {"stars": outputs, "finite_truncation_dark_heating": str(value),
            "cauchy_reservoir_ranks": ranks, "near_degenerate_series": str(series)}


def exact_scope_and_gauge():
    # Oversized identity-containing candidate set falsifies source normalization.
    chars_x = (1, 1, -1, -1) # Conjugation by I,X,Y,Z respectively.
    invalid = [sy.Rational(1,4)*(1-sy.Rational(1+cx,2)) for cx in chars_x]
    valid = [sy.Rational(1,4)*(1-cx) for cx in chars_x]
    assert sum(invalid)==sy.Rational(1,2)
    assert sum(valid)==1

    # Gauge-adjusted local control may look coherent while the whole generator
    # still fixes a strict local minimum. Check the sign independently/exactly.
    h=sy.diag(1,0,2)
    m=sy.zeros(3); m[0,2]=1
    c=sy.Rational(2,3)+sy.I/5
    l=m+c*sy.eye(3)
    gg=sy.I/2*(sy.conjugate(c)*m-c*m.conjugate().T)
    g=-gg
    x=sy.diag(1,0,0)
    def ds(b,rho):
        rr=b.conjugate().T*b
        return b*rho*b.conjugate().T-(rr*rho+rho*rr)/2
    original=-sy.I*((h+g)*x-x*(h+g))+ds(l,x)
    rewritten=-sy.I*(h*x-x*h)+ds(m,x)
    assert original.applyfunc(sy.simplify)==sy.zeros(3)
    assert (original-rewritten).applyfunc(sy.simplify)==sy.zeros(3)
    return {"identity_in_candidate_set_probability_sum":str(sum(invalid)),
            "identity_removed_probability_sum":str(sum(valid)),
            "gauge_adjusted_strict_minimum_stationary_exact":True}


def random_completion_checks(rng):
    worst = 0.0
    count = 0
    for d in (3, 4, 7, 10):
        for rep in range(15):
            e = np.sort(rng.uniform(-3, 5, d))
            if rep % 3 == 0:
                e[1] = e[0]
            b = (rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)))
            b *= e[None,:] > e[:,None]
            b /= max(1.0,np.linalg.norm(b,2))
            g,c = completed(e,b)
            h = np.diag(e)
            residual = dstar(b,h)+1j*(g@h-h@g)+c.conj().T@c
            worst = max(worst,float(np.linalg.norm(residual,2)))
            assert np.linalg.norm(residual,2) < 2e-12
            count += 1
    return {"cases": count, "max_operator_residual": worst}


def channel_checks(rng):
    cases = []
    max_stinespring_ratio = 0.0
    max_reference_ratio = 0.0
    samples = 0
    for d in (2,3,4):
        lambdas = np.arange(1,d+1,dtype=float)
        lambdas /= lambdas.sum()
        rho = np.diag(lambdas)
        s = float(lambdas.min())
        omega = np.diag(np.sqrt(lambdas)).reshape(-1)
        pground = np.outer(omega,omega)
        h = np.eye(d*d)-pground
        for p in (0.,1e-6,.005,.1,.5,1.):
            for rep in range(3):
                z = rng.normal(size=(3*d,d))+1j*rng.normal(size=(3*d,d))
                iso,_ = np.linalg.qr(z)
                ks = [np.sqrt(1-p)*np.eye(d)]
                ks += [np.sqrt(p)*iso[a*d:(a+1)*d,:] for a in range(3)]
                assert np.linalg.norm(sum(k.conj().T@k for k in ks)-np.eye(d)) < 1e-12
                extended = [np.kron(k,np.eye(d)) for k in ks]
                sigma = sum(k@pground@k.conj().T for k in extended)
                eg = float(np.trace(h@sigma).real)
                fe = float(np.vdot(omega,sigma@omega).real)
                assert abs(eg-(1-fe)) < 1e-12
                # Align the Stinespring environment directly using ground overlaps.
                c = np.array([np.trace(rho@k) for k in ks])
                assert abs(np.vdot(c,c).real-fe) < 1e-12
                if np.linalg.norm(c) < 1e-12:
                    env = np.array([1.]+[0.]*(len(ks)-1))
                else:
                    env = c/np.linalg.norm(c)
                v = np.concatenate(ks,axis=0)
                target = np.concatenate([ea*np.eye(d) for ea in env],axis=0)
                w = v-target
                squared = float(np.linalg.norm(w,2)**2)
                exact_bound = 2*(1-np.sqrt(max(0.,fe)))/s
                assert squared <= exact_bound+2e-12
                if exact_bound > 1e-15:
                    max_stinespring_ratio=max(max_stinespring_ratio,squared/exact_bound)
                universal = min(2.,2*np.sqrt(2*max(eg,0.)/s))
                a = sum(k.conj().T@h@k for k in extended)-h
                epsilon_all = max(0.,float(np.linalg.eigvalsh((a+a.conj().T)/2).max()))
                for j in range(8):
                    psi = rng.normal(size=d*d)+1j*rng.normal(size=d*d)
                    psi /= np.linalg.norm(psi)
                    pure = np.outer(psi,psi.conj())
                    out = sum(k@pure@k.conj().T for k in extended)
                    dist = float(np.linalg.eigvalsh((out-pure+out.conj().T-pure.conj().T)/2).__abs__().sum())
                    assert dist <= universal+3e-12
                    if universal > 1e-14:
                        max_reference_ratio=max(max_reference_ratio,dist/universal)
                    samples += 1
                cases.append({"dimension_A":d,"mix_weight":p,"ground_energy_increase":eg,
                              "worst_state_heating":epsilon_all,
                              "Schmidt_min":s,"diamond_upper_from_ground":universal})
    # Exact qubit-unitary diamond formula provides a non-sampled control.
    exact_unitaries=[]
    for theta in (.0001,.005,.1,.4,1.0):
        exact = 2*abs(np.sin(theta))
        eg = np.sin(theta)**2 # Schmidt vector diagonal, generator X has mean zero.
        bound = min(2.,2*np.sqrt(2*eg/.5))
        assert exact <= bound+1e-14
        exact_unitaries.append({"theta":theta,"exact_diamond":exact,"upper":bound})
    return {"channels":cases,"channel_count":len(cases),"reference_samples":samples,
            "max_stinespring_ratio":max_stinespring_ratio,
            "max_reference_ratio":max_reference_ratio,"exact_unitaries":exact_unitaries}


def ising_checks():
    cases=[]
    for n,h in ((6,.2),(8,.7),(6,1.),(6,2.)):
        # Exact integer arithmetic for energy signs: h is a decimal rational.
        hq=sy.Rational(str(h))
        es=[]
        bits=list(itertools.product((0,1),repeat=n))
        for x in bits:
            z=[1-2*a for a in x]
            es.append(-sum(z[i]*z[(i+1)%n] for i in range(n))-hq*sum(z))
        trap=(1<<n)-1
        strict=min(n,int(sy.floor(2/hq))+1)
        safe=min(n,int(sy.ceiling(2/hq)))
        observed_strict=min(sum(a!=b for a,b in zip(bits[y],bits[trap]))
                            for y in range(1<<n) if es[y]<es[trap])
        observed_safe=min(sum(a!=b for a,b in zip(bits[y],bits[trap]))
                          for y in range((1<<n)-1) if es[y]<=es[trap])
        assert strict==observed_strict and safe==observed_safe
        enabled=[]; min_drop=None; all_safe=True
        for x in bits:
            src=int(''.join(map(str,x)),2)
            transitions=[]
            if all(x[j]==1 for j in range(strict)):
                y=list(x)
                for j in range(strict): y[j]=0
                transitions.append(int(''.join(map(str,y)),2))
            for i in range(n):
                if x[i]==1 and x[(i-1)%n]==0:
                    y=list(x); y[i]=0
                    transitions.append(int(''.join(map(str,y)),2))
            assert (len(transitions)>0)==(src!=0)
            for dst in transitions:
                assert sum(bits[dst])<sum(x)
                drop=es[src]-es[dst]
                assert drop>0
                min_drop=drop if min_drop is None else min(min_drop,drop)
            enabled.append(len(transitions))
        cases.append({"n":n,"h":str(hq),"strict_support_threshold":strict,
                      "nonheating_support_threshold":safe,"all_configurations_checked":1<<n,
                      "every_excited_configuration_has_enabled_lowering_move":True,
                      "minimum_energy_drop":str(min_drop),
                      "minimum_total_exit_rate":min(enabled[1:])})
    return cases


def finite_window_star():
    cases=[]
    for delta in (0.,.001,.01,.1):
        energies=np.array([0.,1.,1.+delta])
        jump=np.array([[0.,1.,1.],[0.,0.,0.],[0.,0.,0.]],complex)
        g,c=completed(energies,jump)
        h=np.diag(energies)[1:,1:]
        m=-1j*(h+g[1:,1:])-.5*(jump.conj().T@jump)[1:,1:]
        q=(c.conj().T@c)[1:,1:]
        assert abs(np.linalg.det(q))<1e-12 # Instantaneous coercivity fails.
        t=8.
        nojump=expm(m*t)
        gamma=h-nojump.conj().T@h@nojump
        inverse_root=np.diag(1/np.sqrt(energies[1:]))
        relative=inverse_root@gamma@inverse_root
        a=float(np.linalg.eigvalsh((relative+relative.conj().T)/2).min())
        assert a>=-1e-12
        if delta>0: assert a>0
        else: assert abs(a)<1e-12
        cases.append({'delta':delta,'window_T':t,'instantaneous_Q_rank':1,
                      'relative_window_coercivity_min':a,
                      'scope':'Two-level excited no-jump block; downward jumps end at zero-energy ground. Floating diagnostic, not interval certification.'})
    return cases


def main():
    rng=np.random.default_rng(2026101302)
    report={"status":"Internal exact algebra and finite numerical diagnostics only; no external or physical validation",
            "seed":2026101302,"exact_source_reconstruction":exact_star_checks(),
            "source_scope_and_local_generator_gauge":exact_scope_and_gauge(),
            "general_completion":random_completion_checks(rng),
            "local_approximate_rigidity":channel_checks(rng),
            "sharp_collective_support_and_escape":ising_checks(),
            "finite_window_star":finite_window_star()}
    path=Path(__file__).with_name('independent_results.json')
    path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({"exact_stars":len(report['exact_source_reconstruction']['stars']),
                      "completion_cases":report['general_completion']['cases'],
                      "approximate_local_channels":report['local_approximate_rigidity']['channel_count'],
                      "reference_samples":report['local_approximate_rigidity']['reference_samples'],
                      "Ising_fixtures":len(report['sharp_collective_support_and_escape'])},indent=2))


if __name__=='__main__':
    main()
