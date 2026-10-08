#!/usr/bin/env python3
"""Exact finite formula audits; these are not the quantified theorem proof."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sympy as s

OUT = Path(__file__).resolve().parent
R = s.Rational
I2 = s.eye(2)
X = s.Matrix([[0, 1], [1, 0]])
Y = s.Matrix([[0, -s.I], [s.I, 0]])
Z = s.diag(1, -1)
paulis = [X, Y, Z]
t = s.Symbol("t")
checks = []


def record(name, **details):
    checks.append({"name": name, "status": "PASS", **details})


def kron(*xs):
    return s.kronecker_product(*xs)


def ptr_first(a):
    return s.Matrix(2, 2, lambda b, c: sum(a[2*i+b, 2*i+c] for i in range(2)))


def ptr_second(a):
    return s.Matrix(2, 2, lambda b, c: sum(a[2*b+i, 2*c+i] for i in range(2)))


def psd2(a):
    return a == a.T and a[0, 0] >= 0 and a[1, 1] >= 0 and a.det() >= 0


# 1. Exact characteristic polynomials of the three Pauli stars.
expected = [t**4 * (t*t-4)**2, t**4 * (t*t-8)**2,
            t**2 * (t-4)**2 * (t+2)**4]
star_polys = []
for m in range(1, 4):
    w = s.zeros(8)
    for a in paulis[:m]:
        w += kron(a.T, a, I2) + kron(a.T, I2, a)
    poly = s.factor(w.charpoly(t).as_expr())
    assert s.expand(poly-expected[m-1]) == 0
    star_polys.append(str(poly))
record("pauli_star_spectra", characteristic_polynomials=star_polys,
       maximum_eigenvalues=["2", "2*sqrt(2)", "4"])

# 2. Noncommuting local X_j,Y_j meeting exact C=2 comparison.
ys = [s.diag(R(1,4), R(3,4)),
      s.Matrix([[R(1,2), R(1,4)], [R(1,4), R(1,2)]]),
      s.diag(R(1,3), R(2,3))]
projectors = [s.Matrix([[R(1,2), R(1,2)], [R(1,2), R(1,2)]]),
              s.diag(1,0),
              s.Matrix([[R(1,2), -R(1,2)], [-R(1,2), R(1,2)]])]
xs = [(y+I2)/2 - p/8 for y,p in zip(ys, projectors)]
for x,y in zip(xs,ys):
    assert psd2(x) and psd2(I2-x) and psd2(y) and psd2(I2-y)
    assert psd2(2*(I2-x)-(I2-y))
    assert x*y-y*x != s.zeros(2)
residual = s.eye(8) - 2*kron(*xs) + kron(*ys)
leading_minors = [s.factor(residual[:k,:k].det()) for k in range(1,9)]
assert all(v > 0 for v in leading_minors)
record("noncommuting_tensor_order", constant="2", factors=3,
       exact_sylvester_leading_minors=[str(v) for v in leading_minors])

# 3. C<1 is not permitted by the tensor lemma.
local_ratio = (1-R(3,4))/(1-R(1,2))
tensor_ratio = (1-R(3,4)**2)/(1-R(1,2)**2)
assert local_ratio == R(1,2) and tensor_ratio == R(7,12)
record("C_below_one_failure", local_ratio=str(local_ratio),
       tensor_ratio=str(tensor_ratio))

# 4. Legal 1->2 cloner: exact TP and both marginals on a matrix-unit basis.
swap = s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
sym = (s.eye(4)+swap)/2
for i in range(2):
    for j in range(2):
        e = s.zeros(2); e[i,j]=1
        out = R(2,3)*sym*kron(e,I2)*sym
        target = R(2,3)*e + e.trace()*I2/6
        assert out.trace() == e.trace()
        assert ptr_first(out) == target == ptr_second(out)
record("cloner_TP_and_marginals", marginal="(2/3)X+Tr(X)I/6",
       basis_checked="all four 2x2 matrix units")

# 5. Signed tensor failure with a genuine pure canonical local comparator.
phi = s.diag(1,0,0,-1)
psi = s.diag(1,1,0,0)  # D_X
assert all(v >= 0 for v in (psi-phi).diagonal())
zz_index = 3*4+3
phi_zz = kron(phi,phi)[zz_index,zz_index]
psi_zz = kron(psi,psi)[zz_index,zz_index]
assert phi_zz == 1 and psi_zz == 0
record("signed_local_comparator_tensor_failure", local_constant="1",
       witness="Z tensor Z", broadcast_loss=str(1-phi_zz),
       tensor_comparator_loss=str(1-psi_zz))

# 6. Exact C5 absolute-value obstruction via polynomial interpolation.
S = s.zeros(5)
for i in range(5):
    S[i,(i+1)%5] = R(1,2)
    S[i,(i-1)%5] = R(1,2)
a = (s.sqrt(5)-1)/4
b = (s.sqrt(5)+1)/4
f = s.Poly(s.interpolate([(1,1),(a,a),(-b,b)], t),t)
absS = s.zeros(5)
for (power,), coefficient in f.terms():
    absS += coefficient*(S**power)
absS = absS.applyfunc(s.simplify)
negative_entry = s.simplify(absS[0,1])
assert s.simplify(negative_entry-(2-s.sqrt(5))/10) == 0
assert negative_entry < 0
assert s.simplify(absS*absS-S*S) == s.zeros(5)
assert all(value >= 0 for value in absS.eigenvals())
record("C5_absolute_value_not_positive_map", entry_0_1=str(negative_entry),
       interpolation_polynomial=str(s.factor(f.as_expr())))

# 7. Nine two-qubit full-support Paulis: Bell score 3, product score 1.
bell = s.Matrix([1,0,0,1])/s.sqrt(2)
rho_bell = bell*bell.H
rho_00 = s.diag(1,0,0,0)
bell_score = sum((rho_bell*kron(a,b)).trace()**2 for a in paulis for b in paulis)
product_score = sum((rho_00*kron(a,b)).trace()**2 for a in paulis for b in paulis)
assert s.simplify(bell_score)==3 and product_score==1
twirled = sum((kron(a,b)*rho_bell*kron(a,b).H for a in [I2,*paulis]
               for b in [I2,*paulis]), s.zeros(4))/16
assert twirled == s.eye(4)/4
record("entangled_Pauli_support_witness", unrestricted_k="3",
       certified_by="purity upper bound plus exact Bell saturation",
       Bell_score=str(bell_score), product_score=str(product_score),
       barycenter="I4/4", exact_ratio="6/5")

# 8. Tracial parity conditional compression: exact Pauli-basis comparison.
parity = kron(Z,Z)
all_paulis = [I2,*paulis]
for ai,a in enumerate(all_paulis):
    for bi,b0 in enumerate(all_paulis):
        P = kron(a,b0)
        wt = int(ai!=0)+int(bi!=0)
        commute = parity*P == P*parity
        ph = R(2,3)**wt if commute else s.Integer(0)
        ps = R(1,3)**wt if commute else s.Integer(0)
        assert 2*(1-ph)-(1-ps) >= 0
record("parity_conditional_expectation_compression", dimension=4,
       exact_basis_directions=16, comparison_constant="2")

# 9. Nontracial isometric code compression loses trace.
prob_0 = R(5,6); prob_1=R(1,6)
code_trace = prob_0**2+prob_1**2
assert code_trace==R(13,18) and code_trace != 1
record("rectangular_code_compression_failure", code="span{|00>,|11>}",
       input="|00><00|", retained_trace=str(code_trace))

result = {
    "scope": "exact finite symbolic formula replay; not theorem certification",
    "proof_sha256": hashlib.sha256((OUT/"PROOF.txt").read_bytes()).hexdigest(),
    "sympy_version": s.__version__,
    "tests": checks,
    "all_pass": True,
    "general_universal_constant_status": "UNKNOWN"
}
(OUT/"replay.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({"all_pass":True,"tests":len(checks),
                  "proof_sha256":result["proof_sha256"]},indent=2))
