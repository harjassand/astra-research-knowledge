"""New off-diagonal trace, range-width and finite Fantope conventions only."""
import itertools
import json
import math
from pathlib import Path

import numpy as np


def hs2(a):
    return float(np.vdot(a,a).real)


def kraus_cases(rng):
    rows = []
    for d,q,scale in ((4,1,.01),(6,2,.03),(8,3,.08),(8,2,.2)):
        a0 = np.diag([1.]+[.8]*(q-1)+[0.]*(d-q)).astype(complex)
        aa = [a0]
        for i in range(1,d):
            a = np.zeros((d,d),complex)
            a[0,i] = math.sqrt(1-abs(a0[i,i])**2)
            aa.append(a)
        assert np.linalg.norm(sum((a.conj().T@a for a in aa),np.zeros((d,d)))-np.eye(d)) < 1e-12
        xx = [np.eye(d,dtype=complex)[:,0]]
        for _ in range(5):
            x = scale*(rng.normal(size=d)+1j*rng.normal(size=d))
            x[0] += 1
            x /= np.linalg.norm(x)
            xx.append(x)
        lam = np.array([[np.vdot(x,a@x) for x in xx] for a in aa])
        rr = [[a@x-lam[i,s]*x for i,a in enumerate(aa)] for s,x in enumerate(xx)]
        errors = []
        coherence = []
        for s,x in enumerate(xx):
            rho = np.outer(x,x.conj())
            out = sum((a@rho@a.conj().T for a in aa),np.zeros_like(rho))
            trace = .5*np.abs(np.linalg.eigvalsh(out-rho)).sum()
            ff = sum(hs2(r) for r in rr[s])
            u = sum((lam[i,s].conjugate()*r for i,r in enumerate(rr[s])),np.zeros(d,complex))
            assert ff <= trace+1e-12
            assert np.linalg.norm(u) <= trace+1e-12
            errors.append(float(trace))
            coherence.append(float(np.linalg.norm(u)))
        eps = max(errors)
        max_slack = 0.
        for s,t in itertools.combinations(range(len(xx)),2):
            b = abs(np.vdot(xx[s],xx[t]))
            distance = np.linalg.norm(lam[:,s]-lam[:,t])
            lhs = b*abs(1-np.vdot(lam[:,s],lam[:,t]))
            rhs = 3*eps+2*math.sqrt(eps)*distance
            assert lhs <= rhs+1e-12
            assert distance <= 6*math.sqrt(eps)/b+1e-12
            max_slack = max(max_slack,float(lhs-rhs))
        banchor = min(abs(np.vdot(xx[0],x)) for x in xx)
        tt = np.zeros((d,d),complex)
        weight = float(np.sum(np.abs(lam[:,0])**2))
        for i,a in enumerate(aa):
            uu,ss,_ = np.linalg.svd(a)
            use = ss > 1e-12
            assert use.sum() <= q
            pp = uu[:,use]@uu[:,use].conj().T
            tt += abs(lam[i,0])**2/weight*pp
        assert np.linalg.eigvalsh(tt).min() >= -1e-12
        assert np.linalg.eigvalsh(tt).max() <= 1+1e-12
        assert np.trace(tt).real <= q+1e-12
        worst_tail = max(1-float(np.vdot(x,tt@x).real) for x in xx)
        assert worst_tail <= 148*eps/banchor**2+1e-12
        covariance = sum((np.outer(x,x.conj()) for x in xx),np.zeros_like(tt))/len(xx)
        prior_tail = 1-np.linalg.eigvalsh(covariance)[-q:].sum()
        assert eps >= banchor**2*prior_tail/148-1e-12
        rows.append({'D':d,'Q':q,'scale':scale,'error':eps,'anchor_overlap':banchor,
                     'maximum_offdiag':max(coherence),'range_width_tail':worst_tail,
                     'prior_covariance_tail':float(prior_tail),'pair_slack':max_slack})
    return rows


def fantope_cases(rng):
    rows = []
    for d,q in ((3,1),(4,2),(5,2),(6,3)):
        vertices = []
        for r in range(q+1):
            for subset in itertools.combinations(range(d),r):
                v = np.zeros(d)
                v[list(subset)] = 1
                vertices.append(v)
        vertices = np.array(vertices).T
        weight = rng.random(vertices.shape[1]); weight /= weight.sum()
        target = vertices@weight
        live = np.arange(len(weight))
        while len(live) > d+1:
            mat = np.vstack([np.ones(len(live)),vertices[:,live]])
            _,_,vh = np.linalg.svd(mat,full_matrices=True)
            null = vh[-1,:]
            use = null > 1e-12
            assert use.any()
            amount = np.min(weight[live][use]/null[use])
            weight[live] -= amount*null
            weight[np.abs(weight) < 1e-12] = 0
            live = np.flatnonzero(weight > 0)
        assert len(live) <= d+1
        assert abs(weight.sum()-1) < 1e-11
        assert np.linalg.norm(vertices@weight-target) < 1e-11
        assert weight.min() >= -1e-12
        assert target.min() >= 0 and target.max() <= 1
        assert target.sum() <= q+1e-12
        rows.append({'D':d,'Q':q,'initial_vertices':vertices.shape[1],
                     'finite_labels':len(live),'barycenter_error':float(np.linalg.norm(vertices@weight-target))})
    return rows


def ball_cases():
    rows = []
    for r in (1.,2.,3.):
        mu = r*r
        probs = [math.exp(-mu)*mu**n/math.factorial(n) for n in range(161)]
        eigen = [2/r**4*sum(probs[n+2:]) for n in range(80)]
        mass = sum((n+1)*p for n,p in enumerate(eigen))
        assert abs(mass-1) < 2e-12
        assert max(eigen) <= 2/r**4+1e-12
        assert all(a >= b for a,b in zip(eigen,eigen[1:]))
        for q in (1,3,6,10):
            sorted_values = [p for n,p in enumerate(eigen) for _ in range(n+1)]
            tail = 1-sum(sorted_values[:q])
            assert tail >= max(0.,1-2*q/r**4)-1e-12
        rows.append({'R':r,'covariance_mass':mass,'op_norm':eigen[0],
                     'proved_op_bound':2/r**4})
    return rows


def main():
    rng = np.random.default_rng(92018)
    result = {'status':'FINITE-EVIDENCE',
              'scope':'Four new rank-Q/nonunital off-diagonal-range fixtures, four finite commuting projection decompositions, three uniform coherent-ball covariance spectra only',
              'kraus_cases':kraus_cases(rng),'fantope_cases':fantope_cases(rng),
              'ball_cases':ball_cases(),'old_suites_rerun':False,
              'uniform_mixed_iid_external_or_novelty_validation':False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v if not k.endswith('_cases') else len(v)
                      for k,v in result.items()},indent=2))


if __name__ == '__main__':
    main()
