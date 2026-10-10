"""Finite moderate-frequency residue recovery of the observable contraction.

All kernel values are auditor-computed. This verifies the algebra, numerical
conditioning and target noise amplification only; raw nonlinear phase-cycling
data and modal calibration are not supplied by an actual physical experiment.
"""
import json
import numpy as np
from pathlib import Path
from check_recovery import world, v, q, AfromB, quotient_error, RNG

OUT = Path(__file__).resolve().parent


def pole_design(w, c, hfactor=100):
    gamma, n = w['gamma'], w['n']
    modal = -gamma / 2 + 1j * np.sqrt(w['lam'] - gamma**2 / 4)
    modal = np.r_[modal, modal.conj()]
    poles = np.r_[modal - c, c - modal]
    order = np.argsort(poles.imag)
    imag_modal = np.sort(modal.imag)
    same_side_gap = float(np.min(np.diff(imag_modal)))
    # The min extends the design to broader damping as an instance diagnostic.
    # Only the conservative hfactor*n*gamma branch has the universal bound.
    threshold = min(hfactor * n * gamma, same_side_gap / 4)
    groups = []
    for j in order:
        if groups and poles[j].imag - poles[groups[-1][-1]].imag < threshold:
            groups[-1].append(int(j))
        else:
            groups.append([int(j)])
    samples = []
    for group in groups:
        if len(group) == 1:
            samples.append(poles[group[0]].imag)
        elif len(group) == 2:
            eta = poles[group].imag
            if abs(eta[1] - eta[0]) >= gamma:
                samples.extend(eta)
            else:
                center = float(np.mean(eta))
                samples.extend([center - gamma / 2, center + gamma / 2])
        else:
            raise ValueError('The promised pole-separation condition failed: cluster >2')
    R = 1j * np.asarray(samples)
    C = 1 / (R[:, None] - poles[None, :])
    return poles, R, C, max(map(len, groups))


def p8(w, c):
    d = 2 * c + w['gamma']
    e = c*c + w['gamma']*c
    m1 = float(np.dot(w['a']**2, w['lam']))
    m2 = float(np.dot(w['a']**2, w['lam']**2))
    return d**4 - 4*d*d*(e+m1) + 3*e*e + 6*m1*e + m1*m1 + 2*m2


def query_vector(w, s, t, R):
    c = (s - t) / 2
    low = w['alpha'] * q(w, s, True) * q(w, t, True)
    qp = np.array([q(w, r+c, True) for r in R])
    qm = np.array([q(w, c-r, True) for r in R])
    return (qp * qm) @ low


def B_residue(w, s, t, sigma=0):
    c = (s-t)/2
    poles, R, C, cluster = pole_design(w, c)
    target = poles**7 - p8(w, c) * poles**3
    # C*r=F and B=target*r. Solve the transpose once for target weights.
    weights = np.linalg.solve(C.T, target)
    obs = query_vector(w, s, t, R)
    if sigma:
        obs += sigma*(RNG.normal(size=len(R))+1j*RNG.normal(size=len(R)))/np.sqrt(2)
    return weights @ obs, dict(sigma_min_gamma_C=float(np.linalg.svd(w['gamma']*C, compute_uv=False)[-1]),
        target_weight_norm=float(np.linalg.norm(weights)), maximum_cluster=cluster,
        max_abs_input_frequency=float(max(np.max(np.abs((R+c).imag)),np.max(np.abs((c-R).imag)),abs(t.imag))))


def run():
    result = {'disclosure': __doc__.strip(), 'reconstructions': [], 'noise': [],
              'moderate_damping': []}
    for n in [4, 8, 16]:
        w = world(n)
        # Conservative theorem promise, rather than the looser empirical gamma.
        w['gamma'] /= 50
        ss = 1j*np.sqrt(w['lam'])
        V = np.array([v(w,s,True) for s in ss]).T
        B = np.zeros((n,n), complex)
        ds = []
        for i,s in enumerate(ss):
            for j,t in enumerate(ss):
                B[i,j], d = B_residue(w,s,t)
                ds.append(d)
        A = AfromB(V,B)
        err,gap=quotient_error(w,A)
        result['reconstructions'].append(dict(n=n,gamma=w['gamma'], cubic_queries=4*n**3,
            A_error=float(np.linalg.norm(A-w['A'],2)),K_error=err,beta_gap=gap,
            minimum_sigma_min_gamma_C=min(d['sigma_min_gamma_C'] for d in ds),
            max_target_weight_norm=max(d['target_weight_norm'] for d in ds),
            maximum_input_frequency=max(d['max_abs_input_frequency'] for d in ds)))
        if n==8:
            # Noise here is on already-extracted H3; no physical noise claim.
            for sigma in [1e-10,1e-8,1e-6,1e-4,1e-2,1]:
                Bnoise=np.array([[B_residue(w,s,t,sigma)[0] for t in ss] for s in ss])
                Anoise=AfromB(V,Bnoise)
                kerr,_=quotient_error(w,Anoise)
                result['noise'].append(dict(n=n,gamma=w['gamma'],raw_H3_complex_noise=sigma,
                    A_error=float(np.linalg.norm(Anoise-w['A'],2)),K_error=kerr))
    for n in [4,8,16]:
        w=world(n)
        for gamma in [0.01,0.03,0.1]:
            w['gamma']=gamma
            ss=1j*np.sqrt(w['lam'])
            V=np.array([v(w,s,True) for s in ss]).T
            B=np.zeros((n,n),complex)
            ds=[]
            for i,s in enumerate(ss):
                for j,t in enumerate(ss):
                    B[i,j],d=B_residue(w,s,t)
                    ds.append(d)
            A=AfromB(V,B)
            err,gap=quotient_error(w,A)
            result['moderate_damping'].append(dict(n=n,gamma=gamma,condV=float(np.linalg.cond(V)),
                A_error=float(np.linalg.norm(A-w['A'],2)),K_error=err,beta_gap=gap,
                minimum_sigma_min_gamma_C=min(d['sigma_min_gamma_C'] for d in ds),
                max_target_weight_norm=max(d['target_weight_norm'] for d in ds)))
    (OUT/'residue_results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    run()
