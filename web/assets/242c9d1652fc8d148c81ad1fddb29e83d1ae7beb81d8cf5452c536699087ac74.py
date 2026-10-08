"""New finite conventions for GLOBAL_CAPTURE.txt; not theorem validation."""
import json
import math
from pathlib import Path

import numpy as np

from check_transverse_gram import matrices


def hs2(a):
    return float(np.vdot(a, a).real)


def avg_f(m, k, r, cutoff, u):
    trials = m+k-r
    return sum((cutoff+1-j)/(cutoff+1)*math.comb(trials, j)*
               u**j*(1-u)**(trials-j)
               for j in range(min(cutoff, trials)+1))


def scalar_check(k, m, cutoff):
    d = (k+1)*(m+1)*(m+k+2)/2
    s = (k+1)*(cutoff+2)**2*(cutoff+3)/(12*(cutoff+1))
    ratio = (4*m+2*k-3*cutoff)/(cutoff+2)
    x, w = np.polynomial.legendre.leggauss(m+k+3)
    c_integral = i_integral = 0.
    for u, wt in zip((x+1)/2, w/2):
        entries = [avg_f(m, k, r, cutoff, u) for r in range(k+1)]
        c_integral += wt*2*u*sum(a*a for a in entries)
        i_integral += wt*2*u*sum(r*(k-r+1)*(entries[r]-entries[r-1])**2
                                 for r in range(1, k+1))
    c0 = d*c_integral/(s*(k+1))
    leakage = 1-c0
    assert -1e-11 <= leakage <= 1+1e-11
    assert leakage <= 2*ratio/m+1e-11
    dipole = 0.
    bound = (m+k+2)*(cutoff+4)/((cutoff+2)*(m+2)*(m+3)*(m+4))
    if k:
        j = k/2
        dipole = d*i_integral/(2*s*(k+1)*j*(j+1))
        assert dipole <= bound+1e-12
    return {'k':k,'m':m,'K':cutoff,'leakage':leakage,
            'leakage_bound':2*ratio/m,'c0_dipole_gap':dipole,'dipole_bound':bound}


def h_poly(trace, det, order):
    if order == 0:
        return 1.
    last, current = 1., trace
    for degree in range(2, order+1):
        last, current = current, trace*current-det*last
    return current


def positive_p_trace(k, m):
    p = (0.45, 0.35, 0.20)
    d = (k+1)*(m+1)*(m+k+2)/2
    x, wt = np.polynomial.legendre.leggauss(m+k+3)
    nodes, weights = (x+1)/2, wt/2
    val = 0.
    for t1, w1 in zip(nodes, weights):
        for t2, w2 in zip(nodes, weights):
            prob = (t1, (1-t1)*t2, (1-t1)*(1-t2))
            det = math.prod(p)*sum(prob[i]/p[i] for i in range(3))
            trace = sum(p)-sum(prob[i]*p[i] for i in range(3))
            val += w1*w2*2*(1-t1)*det**m*h_poly(trace, det, k)
    integral_trace = d/(k+1)*val
    schur = 0.
    for s in range(k+1):
        for t in range(m+1):
            mu1, mu2 = m+k-s, m-t
            deg = mu1-mu2
            h = sum(p[0]**(deg-j)*p[1]**j for j in range(deg+1))
            schur += (p[0]*p[1])**mu2*h*p[2]**(s+t)
    relative = abs(integral_trace-schur)/schur
    assert relative < 1e-10
    return relative


def finite_frame_check(k, m, cutoff):
    a, num, spin, ps, gram, dyson, bd, physical = matrices(k, m, k+m+1)
    pe, pv = np.linalg.eigh(physical)
    basis = pv[:, pe>0.5]
    d = basis.shape[1]
    es = [[None]*3 for _ in range(3)]
    for i in (0, 1):
        for j in (0, 1):
            es[i][j] = basis.T@(spin[i][j]-a[j].T@a[i])@basis
        es[i][2] = basis.T@bd[i].T@basis
        es[2][i] = basis.T@bd[i]@basis
    es[2][2] = basis.T@num@basis
    lam1, lam2 = m+k, m
    gen = sum(math.log(p)*es[i][i] for i,p in enumerate((.45,.35,.20)))
    ev, evec = np.linalg.eigh(gen)
    prob = np.exp(ev-ev.max())
    rho = (evec*(prob/prob.sum()))@evec.T
    h = 1j*(.37*(es[0][2]-es[2][0])+.19*(es[1][2]-es[2][1]))
    he, hv = np.linalg.eigh(h)
    unit = (hv*np.exp(-1j*he))@hv.conj().T
    rotated = unit@rho@unit.conj().T
    frames = []
    ell = k+m
    count = 2*ell+1
    x, wt = np.polynomial.legendre.leggauss(ell+1)
    nodes, weights = (x+1)/2, wt/2
    complete = np.zeros((d,d), dtype=complex)
    out = np.zeros((d,d), dtype=complex)
    out_rot = np.zeros((d,d), dtype=complex)
    for t1, w1 in zip(nodes,weights):
        for t2,w2 in zip(nodes,weights):
            amps = np.sqrt([t1,(1-t1)*t2,(1-t1)*(1-t2)])
            for ph1 in range(count):
                for ph2 in range(count):
                    v = amps*np.exp(2j*math.pi*np.array([ph1,ph2,0])/count)
                    n_v = sum(v[i]*v[j].conjugate()*es[i][j]
                              for i in range(3) for j in range(3))
                    ne, nv = np.linalg.eigh(n_v)
                    rounded = np.rint(ne)
                    assert np.max(abs(ne-rounded)) < 1e-10
                    fvals = np.maximum(0.,(cutoff+1-rounded)/(cutoff+1))
                    filt = (nv*fvals)@nv.conj().T
                    weight = w1*w2*2*(1-t1)/count**2
                    complete += weight*filt@filt
                    out += weight*filt@rho@filt
                    out_rot += weight*filt@rotated@filt
    s = (k+1)*(cutoff+2)**2*(cutoff+3)/(12*(cutoff+1))
    tp_error = float(np.linalg.norm(d/s*complete-np.eye(d),2))
    cov_error = float(np.linalg.norm(d/s*(out_rot-unit@out@unit.conj().T),2))
    assert tp_error < 1e-10
    assert cov_error < 1e-10
    return {'k':k,'m':m,'K':cutoff,'nodes':((2*ell+1)*(ell+1))**2,
            'TP_error':tp_error,'covariance_error':cov_error}


def main():
    max_energy = max_binomial = max_gap_deficit = max_p_trace = 0.
    matrix_cases = 0
    scalar_cases = []
    for k in range(4):
        for m in range(1, 5):
            a, num, spin, ps, gram, dyson, bd, physical = matrices(k, m, k+m+1)
            p0 = ps[0, 0]
            outside = physical-p0
            eig, vec = np.linalg.eigh(outside)
            basis = vec[:, eig>0.5]
            lap = sum(b@b.T for b in bd)
            gap = float(np.linalg.eigvalsh(basis.T@lap@basis).min())
            max_gap_deficit = max(max_gap_deficit, max(0., m-gap))
            assert gap >= m-1e-10
            fock_dim = num.shape[0]//(k+1)
            zero_indices = [r*fock_dim for r in range(k+1)]
            generator = 1j*(bd[0]-bd[0].T)
            evals, evecs = np.linalg.eigh(generator)
            for cutoff in range(m+1):
                vals = np.maximum(0., (cutoff+1-np.diag(num))/(cutoff+1))
                f = physical@np.diag(vals)
                s_actual = hs2(f)
                energy = sum(hs2(b@f-f@b) for b in bd)
                ratio = (4*m+2*k-3*cutoff)/(cutoff+2)
                max_energy = max(max_energy, abs(energy/s_actual-ratio))
                assert abs(energy/s_actual-ratio) < 1e-10
                for theta in (0.17, 0.61):
                    unitary = (evecs*np.exp(-1j*theta*evals))@evecs.conj().T
                    projected = (unitary@f@unitary.conj().T)[np.ix_(zero_indices, zero_indices)]
                    expected = np.diag([avg_f(m, k, r, cutoff, math.sin(theta)**2)
                                        for r in range(k+1)])
                    err = float(np.linalg.norm(projected-expected, 2))
                    max_binomial = max(max_binomial, err)
                    assert err < 1e-10
                scalar_cases.append(scalar_check(k, m, cutoff))
                matrix_cases += 1
            max_p_trace = max(max_p_trace, positive_p_trace(k, m))
    for k in (1, 3, 7):
        for m in (64, 128):
            for cutoff in (24, 32):
                scalar_cases.append(scalar_check(k, m, cutoff))
    frame_cases = [finite_frame_check(k,m,cutoff)
                   for k,m,cutoff in ((0,1,0),(1,1,0),(0,2,1),(1,2,1))]
    report = {
        'status':'FINITE-EVIDENCE',
        'scope':'Radial energy, global gap, projected binomial kernel, internal dipole beta bound, positive-fiber trace normalization and four complete finite CP2 frame channels only',
        'matrix_taper_cases':matrix_cases,
        'scalar_beta_cases':len(scalar_cases),
        'max_energy_ratio_error':max_energy,
        'max_projected_binomial_error':max_binomial,
        'max_annihilation_gap_deficit':max_gap_deficit,
        'max_positive_P_trace_relative_error':max_p_trace,
        'scalar_cases':scalar_cases,
        'finite_frame_cases':frame_cases,
        'external_or_asymptotic_validation':False,
        'qubit_tests_rerun':False,
    }
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='scalar_cases'},indent=2))


if __name__ == '__main__':
    main()
