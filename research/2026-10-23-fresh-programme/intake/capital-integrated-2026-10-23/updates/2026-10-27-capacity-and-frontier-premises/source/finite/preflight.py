"""Preparatory source-faithful check; no experimental treatment or novelty claim.

Reuses the existing BG exact eigenvalue/log interval routines, with their mains
disabled, on ordinary rational adaptations of its fixed-reference state family.
Writes only this preflight's small result file. All assertions use rational data.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import html
import json
import re
import sys
import time
import types
import sympy as s

HERE = Path(__file__).resolve().parent
WORK = Path('/Users/harjas/Documents/ChatGPT/coordination/work')
REPO = WORK / 'astra-retrieval-knowledge-20261025/repo'
PAGES = REPO / 'web/pages'
SOURCE_MAP = {
    'exact_triangle_certificate': ('d-7904726a2bf560da.html', 'updates/BG/package/adaptive/exact_triangle_certificate.py'),
    'exact_fixed_reference_certificate': ('d-33ac0978b4a4cfcf.html', 'updates/BG/package/adaptive/exact_fixed_reference_certificate.py'),
}
provenance = []
for name, (page, original) in SOURCE_MAP.items():
    path = PAGES / page
    page_text = path.read_text()
    code = html.unescape(re.search(r'<pre>(.*?)</pre>', page_text, re.S).group(1))
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(code, str(path), 'exec'), module.__dict__)
    provenance.append({'original_path': original, 'local_read_path': str(path),
        'html_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'extracted_utf8_sha256': hashlib.sha256(code.encode()).hexdigest(),
        'main_executed': False})

from exact_triangle_certificate import Interval, decimal_outer, sqrt_endpoint, log_endpoint
from exact_fixed_reference_certificate import block, entropy_potential


def ff(x):
    return F(int(x.p), int(x.q))


def psd(a):
    import itertools
    assert a == a.T
    for count in range(1, a.rows + 1):
        for ids in itertools.combinations(range(a.rows), count):
            assert a.extract(ids, ids).det() >= 0


def states(n, t, mix):
    p = s.Rational(1, 1 + n*n)
    q = 1-p
    cross = s.Rational(n, 1+n*n)
    assert cross*cross == p*q
    assert t*t < s.Rational(1, 3)
    us = [s.Matrix([s.Rational(1, 2), 0]),
          s.Matrix([0, s.Rational(1, 2)]),
          s.Matrix([-s.Rational(1, 2), -s.Rational(1, 2)])]
    rho = [(1-mix)*block(u, q, t*cross, p/3) + mix*s.eye(3)/9 for u in us]
    omega = [(1-mix)*block(u, q, s.Rational(0), p/3) + mix*s.eye(3)/9 for u in us]
    assert sum(rho, s.zeros(3)) == sum(omega, s.zeros(3))
    assert sum(s.trace(a) for a in rho) == sum(s.trace(a) for a in omega) == 1
    assert all(s.trace(a) == s.trace(b) for a,b in zip(rho, omega))
    assert all(a[:2, :2] == b[:2, :2] and a[2, 2] == b[2, 2] for a,b in zip(rho,omega))
    for a in rho+omega:
        psd(a-mix*s.eye(3)/9)
    return rho, omega


def apply(a, blocks):
    return [sum((a[y,x]*blocks[x] for x in range(3)), s.zeros(3)) for y in range(3)]


def divergence(rho, omega):
    # Only off-diagonal active/vacuum blocks differ, while log(omega) is block
    # diagonal. Hence Tr rho log omega == Tr omega log omega exactly.
    for a,b in zip(rho,omega):
        assert a[:2,:2] == b[:2,:2] and a[2,2] == b[2,2]
    return sum((entropy_potential(a)-entropy_potential(b) for a,b in zip(rho,omega)), Interval.of(0))


def trace_distance(rho, omega):
    ans = Interval.of(0)
    for a,b in zip(rho,omega):
        d = a-b
        assert d[:2,:2] == s.zeros(2) and d[2,2] == 0
        # Its eigenvalues are +/- norm(z), 0; half the trace norm is norm(z).
        z = d[:2,2]
        ans += sqrt_endpoint(ff((z.T*z)[0]))
    return ans


def check(name, k, l, n, t, mix, ordinary_upper):
    for a in [k,l]:
        assert all(x>0 for x in a)
        assert all(sum(a[:,i]) == 1 for i in range(3))
    assert l.det() != 0
    rho, omega = states(n,t,mix)
    kr,ko = apply(k,rho),apply(k,omega)
    lr,lo = apply(l,rho),apply(l,omega)
    dk,dl = divergence(kr,ko),divergence(lr,lo)
    assert dl.lo>0
    ratio = dk/dl
    assert ratio.lo > ff(ordinary_upper)
    tk,tl = trace_distance(kr,ko),trace_distance(lr,lo)
    # A single-copy Helstrom binary measurement separates outcome probabilities
    # by T. Repeating it N times and thresholding halfway gives either error
    # <=exp(-N*T^2/2) by Hoeffding; this is sufficient, not optimal copy cost.
    copy_bounds = {}
    for label,td in [('K',tk),('L',tl)]:
        log20 = log_endpoint(F(20)).hi
        ncopy = (2*log20/(td.lo*td.lo)).numerator // (2*log20/(td.lo*td.lo)).denominator + 1
        assert F(ncopy)*td.lo*td.lo/2 > log20
        copy_bounds[label] = ncopy
    entries = list(k)+list(l)+[v for a in rho+omega for v in a]
    return {'id':name,'parameters':{'n':n,'t':str(t),'identity_mix':str(mix)},
        'K':[[str(v) for v in row] for row in k.tolist()],
        'L':[[str(v) for v in row] for row in l.tolist()],
        'reference_dimension':3,'same_reference_and_classical_marginals':'exact rational identities',
        'input_block_spectrum_floor':str(mix/9),
        'spectrum_floor_scope':'chosen mathematical property; not a physical preparation cost',
        'D_K_nats':decimal_outer(dk,15),'D_L_nats':decimal_outer(dl,15),
        'ratio':decimal_outer(ratio,15),'certified_ordinary_upper':str(ordinary_upper),
        'strict_gap':'ratio lower exceeds exact ordinary upper',
        'trace_distance_K':decimal_outer(tk,15),'trace_distance_L':decimal_outer(tl,15),
        'single_copy_helstrom_success_K':decimal_outer((1+tk)/2,15),
        'single_copy_helstrom_success_L':decimal_outer((1+tl)/2,15),
        'sufficient_independent_copy_count_for_each_error_at_most_0.05':copy_bounds,
        'copy_count_scope':'specific known states and per-copy Helstrom measurements; sufficient Hoeffding bounds, not optimal or a classical-versus-quantum copy advantage',
        'largest_entry_numerator_bits':max(abs(int(v.p)).bit_length() for v in entries),
        'largest_entry_denominator_bits':max(int(v.q).bit_length() for v in entries)}


def main():
    start = time.perf_counter()
    ident = s.eye(3)
    uniform = s.ones(3)/3
    l = s.Rational(99,100)*ident+s.Rational(1,100)*uniform
    exclusion = (s.ones(3)-ident)/2
    k0 = s.Rational(49,50)*exclusion+s.Rational(1,50)*uniform
    t0 = s.ones(3)*s.Rational(148,297)
    for i in range(3):t0[i,i]=s.Rational(1,297)
    assert t0*l == k0
    eta0 = s.Rational(2401,4917)
    assert eta0 == (t0[0,0]-t0[0,1])**2/(t0[0,0]+t0[0,1])
    perm = s.Matrix([[0,0,1],[1,0,0],[0,1,0]])
    k = s.Rational(99,100)*k0+s.Rational(1,100)*perm*l
    ordinary = s.Rational(99,100)*eta0+s.Rational(1,100)
    assert ordinary == s.Rational(20218,40975)
    # Joint convexity + exact ordinary contraction for t0 + permutation DPI.
    case1 = check('asymmetric_positive_known_family',k,l,3,s.Rational(1,2),s.Rational(1,100),ordinary)
    kcontrol = ident/2+uniform/2
    tc = kcontrol*l.inv()
    etac = (tc[0,0]-tc[0,1])**2/(tc[0,0]+tc[0,1])
    assert etac == s.Rational(625,2046)
    case2 = check('existing_quantum_control_finite_pair',kcontrol,l,10,s.Rational(3,10),s.Rational(1,1000),etac)
    result = {'status':'NO_ADMISSION_FOR_FINITE_SIGNAL_EXISTENCE',
        'scope':'PREPARATION ONLY; known construction and known exact-check machinery, no new randomized arms, mechanism or performance credit',
        'source_repo_commit_observed':'65aae508a61d02e4a6ba5b368a94779ae6d744cf',
        'sources':provenance,'cases':[case1,case2],
        'exact_check_seconds_excluding_interpreter_and_imports':time.perf_counter()-start,
        'physical_preparation_and_measurement_cost':'UNACQUIRED; matrix encoding bits are not physical cost'}
    (HERE/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'seconds':result['exact_check_seconds_excluding_interpreter_and_imports'],
        'cases':[{key:c[key] for key in ['id','D_K_nats','D_L_nats','ratio','certified_ordinary_upper','trace_distance_K','trace_distance_L','sufficient_independent_copy_count_for_each_error_at_most_0.05','largest_entry_denominator_bits']} for c in result['cases']]},indent=2))


if __name__ == '__main__':
    main()
