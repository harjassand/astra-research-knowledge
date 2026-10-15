"""Exact comparison receipt; no optimizer and no heat-exclusion reproof."""
import hashlib
import json
from pathlib import Path

import sympy as S

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "heat_cone_genesis_sol"
a, b, c, d, k, s, t = S.symbols("a b c d k s t", real=True)
z = S.Matrix([a, b, c, d])
u, v, w, q = a*a+c*c, b*b+d*d, a*b+c*d, a*d-b*c
basis = [u*u, v*v, u*v, w*w, u*w, v*w, q*u, q*v, q*w]
p = S.Matrix([1, 1, S.Rational(166, 3), -S.Rational(460, 9),
              0, 0, -S.Rational(52, 9), S.Rational(52, 9), 0])
F = S.expand(sum(pi*bi for pi, bi in zip(p, basis)))
checks = {}

restriction = S.expand(F.subs({a:s, b:t, c:0, d:0}))
assert restriction == s**4+t**4+S.Rational(38, 9)*s*s*t*t
assert S.Rational(38, 9) not in (2, -2)
checks["rank_one_binary_not_quadratic_square"] = True
assert F.subs({a:1,b:0,c:0,d:0}) == 1
assert S.simplify(F.subs({a:S.sqrt(2)/2,b:S.sqrt(2)/2,c:0,d:0})) == S.Rational(14,9)
checks["not_right_rotation_invariant"] = True

adm = S.expand((u+v)**2-2*(u+v)*q)
adm_p = [1,1,2,0,0,0,-2,-2,0]
assert S.expand(adm-sum(pi*bi for pi,bi in zip(adm_p,basis))) == 0
aubert = S.expand((u+v)**2/3-q*q/6-S.Rational(2,3)*(u+v)*q)
aubert_p = [S.Rational(1,3),S.Rational(1,3),S.Rational(1,2),
            S.Rational(1,6),0,0,-S.Rational(2,3),-S.Rational(2,3),0]
assert S.expand(aubert-sum(pi*bi for pi,bi in zip(aubert_p,basis))) == 0
checks["predecessor_coefficient_vectors"] = True

def acoustic(poly):
    value = S.diff(poly,a,2)+2*k*S.diff(poly,a,b)+k*k*S.diff(poly,b,2)
    return S.hessian(value,z)/2

M = acoustic(F)
M11 = M.subs(k,0)
M12 = M.diff(k).subs(k,0)/2
M22 = M.diff(k,2)/2
K = S.zeros(4)
for (i,j),val in zip([(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],
                      [S.Rational(8,9),S.Rational(8,9),0,0,
                       -S.Rational(8,9),S.Rational(488,9)]):
    K[i,j], K[j,i] = val,-val
Q = M11.row_join(M12+K).col_join((M12-K).row_join(M22))
B = S.zeros(8,4)
for col, positions, entries in [
    (0,[0,3,5,6],[2,-1,2,-1]), (1,[0,3,5,6],[1,-9,-1,9]),
    (2,[1,2,4,7],[3,2,3,2]), (3,[1,2,4,7],[1,1,-1,-1])]:
    for pos,entry in zip(positions,entries):
        B[pos,col] = entry
D = S.diag(S.Rational(8,3),S.Rational(4,3),S.Rational(8,9),S.Rational(4,9))
assert Q == B*D*B.T
assert B.rank() == 4 and M11.rank() == 4
checks["rank_four_acoustic_factor_identity"] = True
checks["ambient_biform_is_not_bilinear_square"] = True

P = 17*k**4-314*k*k+17
contact = S.Matrix([203-17*k*k,k*(85*k*k-1551),2*k*(944-51*k*k),134])
rem = lambda expr: S.rem(S.expand(expr),P,k)
assert all(rem(x)==0 for x in M*contact)
assert S.expand(M.det()-S.Rational(1024,729)*P*P) == 0
columns = []
for bi in basis:
    Mi = acoustic(bi)
    equations = list(Mi*contact) + [(contact.T*Mi.diff(k)*contact)[0]]
    columns.append(S.Matrix([S.expand(rem(e)).coeff(k,j)
                             for e in equations for j in range(4)]))
C = S.Matrix.hstack(*columns)
assert C.shape == (20,9) and C.rank() == 8 and C*p == S.zeros(20,1)
checks["four_contacts_and_rank_eight_criticality"] = True

author_inputs = {}
for filename in ["PROOF.md","verify_heat_separation.py","HEAT_SEPARATION_CERTIFICATE.json"]:
    data = (AUTHOR/filename).read_bytes()
    author_inputs[filename] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes":len(data)}
receipt = {
    "scope":"Exact coefficient/orbit and acoustic/contact comparison only; no full heat-exclusion reproof",
    "coefficient_order":["u^2","v^2","uv","w^2","uw","vw","qu","qv","qw"],
    "candidate_coefficients":[str(x) for x in p],
    "rank_one_restriction":str(restriction),
    "verified_groups":checks,
    "M11_rank":4,"acoustic_Gram_rank":4,"criticality_shape":[20,9],"criticality_rank":8,
    "not_in_bi_SO2_GL_input_output_transpose_orbit":True,
    "nonorbit_proof":"Every transformed classical bi-SO2 quartic restricts at fixed output to a constant times a real quadratic square or zero. Leading coefficients 1 and vanishing cubic cross terms force square cross coefficient +/-2, not 38/9.",
    "author_inputs":author_inputs,
    "historical_originality":"UNKNOWN","candidate_PC":"UNKNOWN","candidate_QC":"UNKNOWN",
    "sympy_version":S.__version__
}
(HERE/"PRIORITY_EXACT_COMPARISON.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"verified_groups":len(checks),"all_passed":all(checks.values()),
                  "criticality_rank":8,"historical_originality":"UNKNOWN"},indent=2))
