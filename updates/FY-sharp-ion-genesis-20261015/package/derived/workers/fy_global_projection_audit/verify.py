#!/usr/bin/env python3
"""Independent exact checks for the full-H projection gluing proof.

No producer code is imported. Exact checks supplement the separately written
universal analytic audit; they do not establish that audit by themselves.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import itertools
import json
from pathlib import Path
import platform
import subprocess
import sys

import sympy as s

HERE = Path(__file__).resolve().parent
W = Path('/Users/harjas/Documents/ChatGPT/ultra/work/astra-sharp-ion-20261015')
PIN = 'b32943eeb62d0d79929a9e572a344219a785ebf9'
checks = []


def check(name, predicate, detail=None):
    assert bool(predicate), name
    checks.append({'name': name, 'status': 'PASS', 'detail': detail})


def zero(expr):
    return s.cancel(s.expand(expr)) == 0


a, b, c, d, p, q, r, z, t = s.symbols('a b c d p q r z t', real=True)
entries = (a, b, c, d)
A = s.Matrix([[a, b], [c, d]])
I = s.eye(2)
I_sub = dict(zip(entries, (1, 0, 0, 1)))
u, v, w, j = a*a+c*c, b*b+d*d, a*b+c*d, a*d-b*c
basis = (u*u, v*v, u*v, w*w, u*w, v*w, u*j, v*j, w*j)
H = ((a-d)**2+(b+c)**2)**2
f = s.symbols('f0:9')
F = sum(fi*bi for fi, bi in zip(f, basis))
monomials = list(s.itermonomials(entries, 4))
monomials = sorted([m for m in monomials if s.total_degree(m) == 4], key=str)
Bmat = s.Matrix([[s.Poly(g, entries).coeff_monomial(mon) for g in basis]
                for mon in monomials])
check('nine invariant basis polynomials are independent', Bmat.rank() == 9)
check('H equals squared norm-minus-two-determinant',
      zero(H-(sum(e*e for e in entries)-2*j)**2))
for order in (1, 2, 3):
    check(f'H derivative order {order} vanishes at I',
          all(zero(s.diff(H, *[entries[k] for k in ks]).subs(I_sub))
              for ks in itertools.combinations_with_replacement(range(4), order)))

U = s.Matrix([[(a+d)/2, (b-c)/2], [(c-b)/2, (a+d)/2]])
V = A-U
norm2 = lambda X: sum(e*e for e in X)
check('conformal and anticonformal projections are orthogonal',
      zero(sum(x*y for x, y in zip(U, V))))
check('C norm is twice anticonformal Frobenius norm',
      zero((a-d)**2+(b+c)**2-2*norm2(V)))

R = s.Matrix([[p*r, p*z], [q*r, q*z]])
Rvec = s.Matrix(list(R))
h = s.expand((Rvec.T*s.hessian(F, entries)*Rvec)[0]/2)
check('rank-one C norm equals Frobenius norm',
      zero((R[0, 0]-R[1, 1])**2+(R[0, 1]+R[1, 0])**2-norm2(R)))
CH = s.Matrix([a-d, b+c])
CR = s.Matrix([R[0, 0]-R[1, 1], R[0, 1]+R[1, 0]])
full_H_curvature = (Rvec.T*s.hessian(H, entries)*Rvec)[0]
check('exact H rank-one Hessian identity',
      zero(full_H_curvature-4*norm2(CH)*norm2(CR)-8*(CH.dot(CR))**2))


def coords(poly):
    rhs = s.Matrix([s.Poly(s.expand(poly), entries).coeff_monomial(mon)
                    for mon in monomials])
    return Bmat.gauss_jordan_solve(rhs)[0]


def stationarity(pval, qval, rval, zval):
    sub = {**I_sub, p: pval, q: qval, r: rval, z: zval}
    values = [h.subs(sub)] + [s.diff(h, var).subs(sub)
                             for var in (*entries, p, q, r, z)]
    return s.Matrix([[s.expand(x).coeff(fi) for fi in f] for x in values])


M = stationarity(t, 1, 1, 0)
n = 1+t*t
L = t*w-j+v
Bt = v*(j-2*L/n)
N = s.Matrix.hstack(*[coords(g) for g in (H, L*L, Bt, v*v)])
check('generic stationary space contains proposed four polynomials',
      all(zero(x) for x in M*N))
kernel_minor = s.factor(N.extract((0, 8, 7, 1), range(4)).det())
check('generic basis four-minor has only excluded real root t=0',
      zero(kernel_minor+2*t*(t*t+3)/n), str(kernel_minor))

# Choose independent rows/columns over R(t), then expose the exact minor.
rows = list(M.T.rref()[1])
columns = list(M.extract(rows, range(9)).rref()[1])
rank_minor = s.factor(M.extract(rows, columns).det())
check('generic contact equations have five independent rows over R(t)',
      len(rows) == len(columns) == 5, {'rows': rows, 'columns': columns})
numer, denom = map(s.factor, s.fraction(rank_minor))
roots = s.polys.polytools.intervals(s.Poly(numer, t), eps=s.Rational(1, 100))
nonzero_roots = [interval for interval, mult in roots if interval != (0, 0)]
check('rank-five minor never vanishes for real nonzero t',
      not nonzero_roots, {'minor': str(rank_minor), 'real_root_intervals': str(roots)})

M0 = stationarity(0, 1, 1, 0)
N0 = s.Matrix.hstack(*[coords(g) for g in (H, v*v, j*j, v*j)])
check('t=0 stationary space is the conjugated shear space',
      M0.rank() == 5 and N0.rank() == 4 and all(zero(x) for x in M0*N0))
Ms = stationarity(1, 0, 0, 1)
Ns = s.Matrix.hstack(*[coords(g) for g in (H, u*u, j*j, u*j)])
check('e12 stationary space is the inherited entire shear space',
      Ms.rank() == 5 and Ns.rank() == 4 and all(zero(x) for x in Ms*Ns))
Mp = stationarity(1, 0, 1, 0)
Np = s.Matrix.hstack(*[coords(g) for g in (H, w*w, v*j, v*v)])
check('e11 stationary space is precisely N873 nonshear space',
      Mp.rank() == 5 and Np.rank() == 4 and all(zero(x) for x in Mp*Np))

J = s.Matrix([[0, -1], [1, 0]])
E21 = s.Matrix([[0, 0], [1, 0]])
E12 = E21.T
check('quarter-turn conjugation sends e21 to minus e12', J*E21*J.T == -E12)
S = s.Matrix([[t, 1], [1, -t]])
check('generic reflection numerator squares to nI and has determinant -n',
      S*S == n*I and zero(S.det()+n))
T_A = s.simplify(S*A*S/n)
check('generic reflection conjugation preserves determinant', zero(T_A.det()-j))
check('generic reflection conjugation preserves Frobenius norm',
      zero(norm2(T_A)-norm2(A)))
Rrow = s.Matrix([[t, 1], [0, 0]])
Rcol = s.Matrix([[t, 0], [1, 0]])
check('reflection conjugation exchanges requested row/column contacts',
      all(zero(x) for x in S*Rrow*S/n-Rcol))
check('generic reflection conjugation preserves H',
      zero(H.subs(dict(zip(entries, list(T_A))), simultaneous=True)-H))

k, ell, m = s.symbols('k ell m', real=True)
G = k*L*L+ell*Bt+m*v*v
x = -a+t*(b+c)+d
support = k*x*x+2*ell/n*(t*b-3*d)*x+(2*m-ell)*b*b+3*(2*m+ell)*d*d
Q0 = (s.Matrix(entries).T*s.hessian(G, entries).subs(I_sub)*s.Matrix(entries))[0]/2
check('generic determinant support identity independently differentiated',
      zero(Q0-3*ell*j-support))
C = s.Matrix([[k, ell*t/n, -3*ell/n],
              [ell*t/n, 2*m-ell, 0], [-3*ell/n, 0, 3*(2*m+ell)]])
Delta = k*n*n*(2*m-ell)*(2*m+ell)-ell*ell*(t*t*(2*m+ell)+3*(2*m-ell))
check('generic support determinant equals 3Delta/n^2',
      zero(C.det()-3*Delta/n**2))
JJ = s.Matrix([[-1, t, t, 1], [0, 1, 0, 0], [0, 0, 0, 1]])
check('positive-definite three-coordinate support has only contact kernel',
      JJ.rank() == 3 and JJ*s.Matrix(list(Rcol)) == s.zeros(3, 1))

AA, BB = 2*m-ell, 2*m+ell
kb = ell**2*(t*t*BB+3*AA)/(n*n*AA*BB)
Z = s.Matrix([[-(BB*t*t+AA)/(2*AA*n), -ell*t/(AA*n)],
              [(BB*t*t+AA)/(2*t*BB*n), ell/(BB*n)]])
check('generic singular-boundary second direction is rank one', zero(Z.det()))
check('generic singular-boundary second direction has x=1',
      zero(x.subs(dict(zip(entries, list(Z))), simultaneous=True)-1))
check('generic singular-boundary second direction is in support kernel',
      all(zero(e) for e in C.subs(k, kb)*JJ*s.Matrix(list(Z))))
P = m*BB**2*t*t+AA**2*(2*ell+m)
SS = BB**3*t**4+2*(4*m-3*ell)*AA*BB*t*t+3*AA**3
claimed_gradient = ell**3*t/(AA**3*BB**2*n**3)*s.Matrix([-4*t*P, SS, SS, 4*t*P])
Zvec = s.Matrix(list(Z))
for i, entry in enumerate(entries):
    actual = (Zvec.T*s.diff(s.hessian(G, entries), entry).subs(I_sub)*Zvec)[0]/2
    check(f'singular-boundary acoustic gradient component {i} independently differentiated',
          zero(actual.subs(k, kb)-claimed_gradient[i]))
Z0 = s.Matrix([[0, 1], [0, -t]])
Z0vec = s.Matrix(list(Z0))
gradient0 = s.Matrix([(Z0vec.T*s.diff(s.hessian(k*L*L, entries), entry).subs(I_sub)*Z0vec)[0]/2
                     for entry in entries])
check('ell=m=0 excluded boundary has nonzero stationarity vector',
      all(zero(e) for e in gradient0-2*k*n*s.Matrix([-1, t, t, 1])))
Q4 = JJ.T*C*JJ
e3 = sum(Q4.extract(ix, ix).det() for ix in itertools.combinations(range(4), 3))
check('rank-three rational spectral bound numerator is 3Delta/n', zero(e3-3*Delta/n))

ss, hh, rr = s.symbols('ss hh rr', real=True)
RH = (ss+2*hh+rr)**2-ss**2-4*ss*hh
check('H simultaneous background-quartic gap square identity',
      zero(RH-ss*rr-rr**2/5-(ss*rr-hh**2)-5*(hh+2*rr/5)**2))
check('H reserve one-third quartic gap square identity',
      zero(RH-rr**2/3-2*(ss*rr-hh**2)-6*(hh+rr/3)**2))
MM, kap = s.symbols('MM kap', positive=True)
K4 = s.Rational(625, 4)
A0 = 2592*MM**2/kap+8*MM
B0 = 512*MM**2/kap+3*MM
check('flat compiler coefficient simplifies to pinned threshold',
      zero(A0/2+5*K4*B0-401296*MM**2/kap-s.Rational(9391, 4)*MM))
check('extra H reserve has pinned 4/1875 margin', 1/(3*K4) == s.Rational(4, 1875))

source_names = [
    'AGENTS.md',
    '00_START_HERE.txt',
    'frontier/dossiers/N873.txt',
    'updates/FX-global-completion-axis-20261015/package/derived/workers/compatible_positivity_priority/CLASSICAL_FINITE_COMPLETION_COROLLARY.md',
    'updates/FX-global-completion-axis-20261015/package/derived/workers/compatible_positivity_priority/GENERAL_INVERTIBLE_CONTACT_NORMAL_FORM.md',
    'updates/FX-global-completion-axis-20261015/package/derived/workers/compatible_positivity_priority/PRIORITY_AND_APPLICABILITY.md',
    'updates/FX-global-completion-axis-20261015/package/derived/workers/global_completion_reconstruction/AUDIT.md',
    'updates/FX-global-completion-axis-20261015/package/derived/workers/full_invariant_genesis/REPORT.md',
    'updates/FX-global-completion-axis-20261015/package/derived/workers/full_invariant_genesis/GENERAL_FLAT_COMPLETION.md',
    'updates/FX-global-completion-axis-20261015/package/derived/workers/general_flat_completion_independent_audit/REPORT.md',
]
source_pins = [{'path': str(W/name), 'sha256': hashlib.sha256((W/name).read_bytes()).hexdigest()}
               for name in source_names]
head = subprocess.check_output(['git', '-C', str(W), 'rev-parse', 'HEAD'], text=True).strip()
check('checkout HEAD agrees with task pin', head == PIN, head)
generic = HERE.parent/'fy_contact_angle_genesis'/'REPORT.md'
if generic.exists():
    data = generic.read_bytes()
    snapshots = HERE/'input_snapshots'
    snapshots.mkdir(exist_ok=True)
    version = 1
    target = snapshots/f'generic_angle_REPORT.v{version:04d}.md'
    prior_snapshots = []
    while target.exists() and target.read_bytes() != data:
        prior_snapshots.append({'path': str(target),
                                'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
        version += 1
        target = snapshots/f'generic_angle_REPORT.v{version:04d}.md'
    if not target.exists():
        target.write_bytes(data)
    check('final generic report snapshot is byte-identical; older snapshots preserved',
          target.read_bytes() == data, {'version': version, 'prior_snapshots': prior_snapshots})
    generic_pin = {'source': str(generic), 'snapshot': str(target),
                   'sha256': hashlib.sha256(data).hexdigest(),
                   'admission': 'ACCEPTED_AFTER_READ_AND_INDEPENDENT_ANALYTIC_RECONSTRUCTION'}
else:
    generic_pin = {'source': str(generic), 'admission': 'NOT_AVAILABLE'}

receipt = {
    'generated_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
    'status': 'PASS_SCOPED_EXACT_ALGEBRA', 'checks_passed': len(checks),
    'checks': checks, 'python': sys.version, 'sympy': s.__version__,
    'platform': platform.platform(), 'worktree_pin': PIN,
    'source_pins': source_pins, 'generic_angle_dependency': generic_pin,
    'not_certified': [
        'Universal analytical conclusions by symbolic computation alone',
        'Historical novelty, external correctness, formal verification',
        'Same-alpha ROC-to-QC equivalence or sharp alpha',
        'Automatic rational contact acquisition for arbitrary rational full-space inputs',
    ],
}
(HERE/'EXACT_VERIFICATION.v0002.json').write_text(json.dumps(receipt, indent=2)+'\n')
(HERE/'EXACT_VERIFICATION.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps({'status': receipt['status'], 'checks_passed': len(checks),
                  'generic_dependency': generic_pin['admission'],
                  'rank_minor': str(rank_minor)}, indent=2))
