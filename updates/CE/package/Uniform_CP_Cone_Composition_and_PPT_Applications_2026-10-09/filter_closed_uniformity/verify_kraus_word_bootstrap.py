"""Small deterministic stress test for the Kraus-word EB approximation lemma.

The random references are known EB-TP maps, not numerically certified nearest
EB-TP maps. All bounds hold with distance to any chosen EB-TP reference.
This script checks finite-dimensional inequalities; it is not a proof or a
numerical separability oracle. Run from any directory with NumPy installed.
"""

import json
from pathlib import Path

import numpy as np


RNG = np.random.default_rng(930173)
TOL = 2e-11


def fro(x):
    return float(np.linalg.norm(x))


def herm(x):
    return (x + x.conj().T) / 2


def psqrt(x):
    vals, vecs = np.linalg.eigh(herm(x))
    assert vals.min() >= -TOL
    return (vecs * np.sqrt(np.maximum(vals, 0))) @ vecs.conj().T


def pinvsqrt(x):
    vals, vecs = np.linalg.eigh(herm(x))
    assert vals.min() > 0
    return (vecs / np.sqrt(vals)) @ vecs.conj().T


def znormal(shape):
    return RNG.normal(size=shape) + 1j * RNG.normal(size=shape)


def normalize_tp(ks):
    h = pinvsqrt(sum(k.conj().T @ k for k in ks))
    return [k @ h for k in ks]


def random_channel(d):
    return normalize_tp([znormal((d, d)) for _ in range(d * d)])


def random_eb(d, rank):
    return normalize_tp([
        np.outer(znormal(d), znormal(d).conj()) for _ in range(rank)
    ])


def choi(ks):
    return sum(np.outer(k.ravel(), k.ravel().conj()) for k in ks)


def super_from_choi(j, d):
    return j.reshape(d, d, d, d).transpose(0, 2, 1, 3).reshape(d*d, d*d)


def choi_from_super(s, d):
    return s.reshape(d, d, d, d).transpose(0, 2, 1, 3).reshape(d*d, d*d)


def pt(j, d):
    return j.reshape(d, d, d, d).transpose(0, 3, 2, 1).reshape(d*d, d*d)


def wedge_norm(a):
    sv = np.linalg.svd(a, compute_uv=False)
    return float(sv[0] * sv[1])


def truncate(a):
    u, s, vh = np.linalg.svd(a, full_matrices=False)
    return s[0] * np.outer(u[:, 0], vh[0, :])


def aligned_lift(j, k0):
    d = k0[0].shape[0]
    w0 = np.zeros((d*d, d**4), dtype=complex)
    w0[:, :len(k0)] = np.column_stack([k.ravel() for k in k0])
    left, sv, vh = np.linalg.svd(w0, full_matrices=True)
    u = left @ vh[:d*d, :]
    root0 = (left * sv) @ left.conj().T
    root = psqrt(j)
    w = root @ u
    assert fro(u @ u.conj().T - np.eye(d*d)) < TOL
    assert fro(root0 @ u - w0) < TOL
    assert fro(w @ w.conj().T - j) < TOL
    assert abs(fro(w-w0)**2-fro(root-root0)**2) < TOL
    ks = [w[:, i].reshape(d, d) for i in range(d**4)
          if np.linalg.norm(w[:, i]) > 1e-14]
    return ks, fro(w-w0)


def ratio(a, b):
    # Ratios below the absolute test resolution are dominated by roundoff.
    return float(a / b) if b > TOL else None


def check_case(j, k0, depths, label, exact_f=None):
    d = k0[0].shape[0]
    j0 = choi(k0)
    ks, epsilon = aligned_lift(j, k0)
    g = fro(j-j0)
    trace_dist = float(np.abs(np.linalg.eigvalsh(herm(j-j0))).sum())
    b = sum(wedge_norm(k) for k in ks)
    assert epsilon**2 <= trace_dist + TOL
    assert trace_dist <= d*g + TOL
    assert b <= np.sqrt(d)*epsilon + TOL
    s = super_from_choi(j, d)
    rows = []
    words = [np.eye(d, dtype=complex)]
    for n in range(1, max(depths)+1):
        words = [k @ a for k in ks for a in words]
        if n not in depths:
            continue
        ls = [truncate(a) for a in words]
        sn = np.linalg.matrix_power(s, n)
        e = super_from_choi(choi(ls), d)
        delta = fro(sn-e)
        wedge_sum = sum(wedge_norm(a) for a in words)
        bound = np.sqrt(d*d-1) * b**n
        assert wedge_sum <= b**n + TOL
        assert delta <= bound + TOL
        e_star_i = herm((e.conj().T @ np.eye(d).ravel()).reshape(d,d))
        assert np.linalg.eigvalsh(np.eye(d)-e_star_i).min() >= -TOL
        assert np.linalg.norm(e_star_i-np.eye(d), 2) <= np.sqrt(d)*delta + TOL
        comp_error = fro(sn @ sn - e @ e)
        assert comp_error <= 2*np.sqrt(d)*delta + TOL
        for a, l in zip(words, ls):
            diff = np.outer(a.ravel(), a.ravel().conj()) - np.outer(l.ravel(), l.ravel().conj())
            assert fro(diff) <= np.sqrt(d*d-1)*wedge_norm(a) + TOL
            assert np.linalg.eigvalsh(herm(a.conj().T@a-l.conj().T@l)).min() >= -TOL
        row = dict(n=n, word_count=len(words), delta=delta, bound=bound,
                   bound_below_absolute_resolution=bool(bound <= TOL),
                   delta_bound_ratio=ratio(delta,bound),
                   wedge_product_ratio=ratio(wedge_sum,b**n),
                   composition_ratio=ratio(comp_error,2*np.sqrt(d)*delta),
                   min_effect_eigenvalue=float(np.linalg.eigvalsh(e_star_i).min()))
        if exact_f is not None:
            f = float(exact_f(n))
            threshold = f/(4*d*d*(2*np.sqrt(d)+1))
            row.update(f=f, original_threshold=threshold,
                       original_certificate=bool(delta <= threshold),
                       bound_only_certificate=bool(bound <= threshold))
            if delta <= threshold:
                worst = 1.0
                for l in ls:
                    tr = fro(l)**2
                    if tr < 1e-25:
                        continue
                    sigma = l @ l.conj().T / tr
                    out = herm((e @ sigma.ravel()).reshape(d,d))
                    worst = min(worst,float(np.linalg.eigvalsh(out).min()))
                assert worst >= f/2 - TOL
                assert np.linalg.eigvalsh(e_star_i).min() >= .5 - TOL
                assert comp_error <= f/(4*d*d) + TOL
                row['min_preparation_output_eigenvalue'] = worst
                row['min_partial_transpose_at_2n'] = float(np.linalg.eigvalsh(
                    herm(pt(choi_from_super(sn@sn,d),d))).min())
        rows.append(row)
    return dict(label=label,d=d,reference_rank=int(np.linalg.matrix_rank(j0)),
                g_reference=g,epsilon=epsilon,b=b,
                powers_stormer_ratio=ratio(epsilon**2,trace_dist),
                trace_frobenius_ratio=ratio(trace_dist,d*g),
                improved_b_ratio=ratio(b,np.sqrt(d)*epsilon),checks=rows)


def main():
    cases = []
    for d in (2,3,4):
        for rank in (d,d*d):
            for t in (.2,1e-3,1e-6):
                k0 = random_eb(d,rank)
                j = (1-t)*choi(k0) + t*choi(random_channel(d))
                cases.append(check_case(j,k0,[1,2,3] if d<=3 else [1,2],
                                        f'random_d{d}_rank{rank}_t{t}'))
    for eps in (1e-2,1e-3):
        d=2
        noise=eps**2
        k0=[np.diag([1.,0.]),np.diag([0.,1.])]
        j=(1-eps-noise)*choi(k0)+eps*choi([np.eye(d)])+noise*np.eye(d*d)/d
        cases.append(check_case(j,k0,[1,2,3],f'non_EB_primitive_eps{eps}',
                                exact_f=lambda n,s=noise:(1-(1-s)**n)/d))
    sharp=[]
    for d in (2,3,4,7):
        a=np.eye(d)
        l=truncate(a)
        error=fro(np.outer(a.ravel(),a.ravel())-np.outer(l.ravel(),l.ravel()))
        sharp.append(dict(d=d,error=error,bound=float(np.sqrt(d*d-1)),
                          ratio=error/np.sqrt(d*d-1)))
        assert abs(error-np.sqrt(d*d-1))<TOL
    all_checks=[row for case in cases for row in case['checks']]
    result=dict(seed=930173,tolerance=TOL,status='PASS',case_count=len(cases),
                word_depth_checks=len(all_checks),
                total_kraus_words_checked=sum(row['word_count'] for row in all_checks),
                max_improved_b_ratio=max(c['improved_b_ratio'] for c in cases),
                max_delta_bound_ratio=max(c['delta_bound_ratio'] for c in all_checks
                                          if c['delta_bound_ratio'] is not None),
                max_composition_ratio=max(c['composition_ratio'] for c in all_checks
                                          if c['composition_ratio'] is not None),
                absolute_resolution_limited_checks=sum(c['bound_below_absolute_resolution'] for c in all_checks),
                certificates=sum(c.get('original_certificate',False) for c in all_checks),
                sharp_truncation_examples=sharp,cases=cases,
                scope='Known EB references; no nearest-point optimization or general separability test. '
                      'Ratios with denominator <= absolute tolerance are null; those tests are only absolute-resolution checks.')
    path=Path(__file__).with_name('kraus_word_bootstrap_verification.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('cases','sharp_truncation_examples')},indent=2))


if __name__=='__main__':
    main()
