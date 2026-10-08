"""New product normalized-score and global-rank conventions, not a proof."""
import json
import math
from pathlib import Path

import numpy as np

from check_cold_carrier import representation, nodes
from check_quantum_branch import spin, rotations


def hs2(a):
    return float(np.vdot(a, a).real)


def run_case(m, k, q, h, rng):
    occ, ee, pc = representation(m)
    dc, dh = len(occ), k + 1
    d, j = dc * dh, k / 2
    zc = sum((n + 1) * q**n for n in range(m + 1))
    purity_c = sum((n + 1) * q**(2*n) for n in range(m + 1)) / zc**2
    cold = []
    sc = np.zeros((dc**2, dc**2), complex)
    for v, w in nodes(m):
        nv = sum(v[a]*v[b].conjugate()*ee[a][b]
                 for a in range(3) for b in range(3))
        ev, uv = np.linalg.eigh(nv)
        if q == 0:
            coeff = (np.abs(ev-m) < 1e-8).astype(float)
        else:
            coeff = q**(m-ev) / zc
        rho = (uv*coeff) @ uv.conj().T
        cold.append((rho, w))
        sc += dc/purity_c*w*np.kron(rho.T, rho)
    js = spin(j)
    cas = np.zeros((dh**2, dh**2), complex)
    for t in js:
        ad = np.kron(np.eye(dh), t)-np.kron(t.T, np.eye(dh))
        cas += ad @ ad
    ev, uv = np.linalg.eigh(cas)
    ph = []
    for s in range(k+1):
        use = np.abs(ev-s*(s+1)) < 1e-8
        assert use.sum() == 2*s+1
        ph.append(uv[:, use] @ uv[:, use].conj().T)
    probs = np.exp(h*np.diag(js[2])/j)
    probs /= probs.sum()
    purity_h = float(probs @ probs)
    hot = []
    sh = np.zeros((dh**2, dh**2), complex)
    for u, w, _ in rotations(j):
        tau = (u*probs) @ u.conj().T
        hot.append((tau, w))
        sh += dh/purity_h*w*np.kron(tau.T, tau)
    cs = [float(np.trace(p@sc).real/((ell+1)**3)) for ell,p in enumerate(pc)]
    ts = [float(np.trace(p@sh).real/(2*s+1)) for s,p in enumerate(ph)]
    theta_h = (2/3)*h*h*math.exp(-6*h)
    for s, t in enumerate(ts):
        assert 1-t+1e-11 >= theta_h*s*(s+1)/k**2
    assert np.linalg.eigvalsh(sc).min() > -1e-10
    assert np.linalg.eigvalsh(sh).min() > -1e-10
    assert np.linalg.eigvalsh(sc).max() < 1+1e-10
    assert np.linalg.eigvalsh(sh).max() < 1+1e-10

    # Reshuffle from factor HS spaces to TOTAL input/output vectorization.
    g = np.empty(d*d, int)
    for co in range(dc):
        for ci in range(dc):
            for ho in range(dh):
                for hi in range(dh):
                    factor = (co+dc*ci)*dh*dh+(ho+dh*hi)
                    g[factor] = co*dh+ho+d*(ci*dh+hi)
    sg = np.zeros((d*d, d*d), complex)
    sg[np.ix_(g,g)] = np.kron(sc,sh)
    b = rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
    b /= math.sqrt(hs2(b))
    vb = b.ravel(order='F')
    direct = np.zeros_like(b)
    comm = 0.
    for rho, wc in cold:
        for tau, wh in hot:
            omega = np.kron(rho,tau)
            direct += d/(purity_c*purity_h)*wc*wh*omega@b@omega
            comm += wc*wh*hs2(omega@b-b@omega)
    factor_error = float(np.linalg.norm(direct.ravel(order='F')-sg@vb))
    assert factor_error < 5e-11
    energy = float(np.vdot(vb,(np.eye(d*d)-sg)@vb).real)
    assert abs(energy-d*comm/(2*purity_c*purity_h)) < 5e-11

    # All projector marginals and global rank, with no product Kraus premise.
    margin_error, rank_tests = 0., 0
    for cutoff in (.1,.4,.8):
        pf = sum((np.kron(p1,p2)
                  for ell,p1 in enumerate(pc) for s,p2 in enumerate(ph)
                  if 1-cs[ell]*ts[s] <= cutoff),
                 np.zeros_like(sg))
        pg = np.zeros_like(sg)
        pg[np.ix_(g,g)] = pf
        dim = float(np.trace(pg).real)
        p4 = pg.reshape(d,d,d,d,order='F')
        marg1 = np.einsum('aibi->ab',p4)
        marg2 = np.einsum('iaib->ab',p4)
        margin_error = max(margin_error,
                           float(np.linalg.norm(marg1-dim/d*np.eye(d))),
                           float(np.linalg.norm(marg2-dim/d*np.eye(d))))
        for rank in (1,2,min(dc,dh)):
            a = ((rng.normal(size=(d,rank))+1j*rng.normal(size=(d,rank)))
                 @ (rng.normal(size=(rank,d))+1j*rng.normal(size=(rank,d))))
            a /= math.sqrt(hs2(a))
            av = a.ravel(order='F')
            overlap = float(np.vdot(av,pg@av).real)
            assert overlap <= min(1.,rank*dim/d)+5e-11
            rank_tests += 1
    assert margin_error < 5e-11

    # Nonunital, factor-mixing rank-one channel tests the scalar self-score.
    r = rng.normal(size=(d,d))+1j*rng.normal(size=(d,d))
    unitary, _ = np.linalg.qr(r)
    aa = []
    for i in range(d):
        out = rng.normal(size=d)+1j*rng.normal(size=d)
        out /= np.linalg.norm(out)
        aa.append(np.outer(out,unitary[:,i].conj()))
    energies = sum(float(np.vdot((a/math.sqrt(d)).ravel(order='F'),
                               (np.eye(d*d)-sg)@(a/math.sqrt(d)).ravel(order='F')).real)
                   for a in aa)
    discrepancy = 0.
    max_effect_score = 0.
    w = float(probs.max()) / zc
    for rho, wc in cold:
        for tau, wh in hot:
            omega = np.kron(rho,tau)
            out = sum((a@omega@a.conj().T for a in aa),np.zeros_like(omega))
            gap = float(np.trace(omega@(omega-out)).real)
            discrepancy += wc*wh*gap
            trace = .5*np.abs(np.linalg.eigvalsh(omega-out)).sum()
            assert gap/w <= trace+5e-11
            max_effect_score = max(max_effect_score, gap/w)
    score_error = abs(discrepancy-purity_c*purity_h*energies)
    assert score_error < 5e-11
    return {'m':m,'k':k,'q':q,'h':h,'factor_error':factor_error,
            'marginal_error':margin_error,'score_error':score_error,
            'global_rank_fixtures':rank_tests,
            'hot_min_energy':min(1-t for t in ts[1:]),
            'nonunital_channel_effect_score':max_effect_score}


def main():
    rng = np.random.default_rng(73017)
    cases = [run_case(*x,rng) for x in
             ((1,1,.2,.5),(2,1,.4,.7),(1,3,0.,1.))]
    result = {'status':'FINITE-EVIDENCE',
              'scope':'Three exact-quadrature product sandwich kernels, hot all-harmonic coercivity, joint projector marginals/global rank and factor-mixing nonunital score only',
              'cases':cases,'old_suites_rerun':False,
              'uniform_iid_external_or_novelty_validation':False}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
