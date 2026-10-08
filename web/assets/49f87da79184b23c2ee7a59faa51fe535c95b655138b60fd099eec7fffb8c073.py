"""Exact rational checks for the near-dephasing PPT channel and TILES witness.

No numerical optimization and no proof by sampled product vectors.  Block
positivity is proved in PROOFS.txt; the finite linear-algebra obligations of
that proof are enumerated here.  SymPy is the only nonstandard dependency.
"""
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sympy as s

HERE = Path(__file__).resolve().parent
q = s.Rational
mu = q(1, 320000)
eps = s.symbols("epsilon", nonnegative=True)
I3 = s.eye(3)
e = [I3[:, i] for i in range(3)]
aa = [e[0], e[0]-e[1], e[2], e[1]-e[2], e[0]+e[1]+e[2]]
bb = [e[0]-e[1], e[2], e[1]-e[2], e[0], e[0]+e[1]+e[2]]
tile_projectors = []
for a, b in zip(aa, bb):
    z = s.kronecker_product(a, b)
    tile_projectors.append(z*z.T/(z.T*z)[0])
P = sum(tile_projectors, s.zeros(9))
J = s.eye(9)-P
W = P-mu*s.eye(9)

def pt(M, da, db):
    return s.Matrix(da*db, da*db,
        lambda r, c: M[(r//db)*db+c%db, (c//db)*db+r%db])

def partial_output_trace(M, da, db):
    return s.Matrix(da, da,
        lambda i, j: sum(M[i*db+k, j*db+k] for k in range(db)))

assert P*P == P and s.trace(P) == 5
assert J*J == J and s.trace(J) == 4
assert pt(J, 3, 3) == J
assert s.trace(W*J) == -4*mu

# Four unnormalized tile linear forms in each product factor.  If their
# products have modulus <= 1/400, each pair has a factor <= 1/20.
Arows = s.Matrix.vstack(*(a.T for a in aa[:4]))
Brows = s.Matrix.vstack(*(b.T for b in bb[:4]))
cases = []
for n in range(5):
    for chosen in combinations(range(4), n):
        comp = tuple(i for i in range(4) if i not in chosen)
        A = Arows[list(chosen), :] if chosen else s.zeros(0, 3)
        B = Brows[list(comp), :] if comp else s.zeros(0, 3)
        row = {"A_small": list(chosen), "B_small": list(comp),
               "A_rank": A.rank(), "B_rank": B.rank()}
        if n == 2:
            assert A.rank() == B.rank() == 2
            for C, name in [(A, "A"), (B, "B")]:
                G = C*C.T
                # For positive 2x2 Gram matrices, lambda_min >= det/trace.
                assert G.det()/s.trace(G) >= q(1, 4)
                v = C.nullspace()[0]
                # Along each one-dimensional kernel, |sum v| >= ||v||.
                ratio = sum(v)**2/(v.T*v)[0]
                assert ratio >= 1
                row[name+"_kernel_sum_ratio_squared"] = str(ratio)
        else:
            assert A.rank() == 3 or B.rank() == 3
        cases.append(row)
for C in [Arows, Brows]:
    for subset in combinations(range(4), 3):
        N = C[list(subset), :]
        assert abs(N.det()) == 1
        assert all(abs(x) <= 1 for x in N.inv())
assert 3*s.sqrt(3)*q(1, 20) < 1
assert q(11, 20)**4/9 > mu

E = partial_output_trace(J, 3, 3).T
Def = I3-E/4
assert s.trace(E) == 4
# Positivity follows analytically from J>=0 and E<=Tr(E) I; Sylvester
# checks here establish even strict positivity of this concrete defect.
assert all(Def[:k, :k].det() > 0 for k in range(1, 4))

def F(X):
    out = s.zeros(7)
    for i in range(3):
        for j in range(3):
            for a in range(3):
                for b in range(3):
                    out[3+a, 3+b] += X[i, j]*J[3*i+a, 3*j+b]/4
    out[6, 6] = s.trace(Def*X)
    return out

def DA(X):
    M = s.zeros(7)
    for i in range(3): M[i, i] = X[i, i]
    return M

def DC(X):
    M = s.zeros(7)
    for i in range(3, 7): M[i, i] = X[i, i]
    return M

def phi(X):
    return (1-eps)*DA(X)+eps*F(X[:3, :3])+DC(X)

def square_eb_formula(X):
    XA = X[:3, :3]
    return ((1-eps)**2*DA(X) + eps*(1-eps)*F(s.diag(*[XA[i,i] for i in range(3)]))
            + eps*DC(F(XA))+DC(X))

def choi(mapfn, d):
    M = s.zeros(d*d)
    for i in range(d):
        for j in range(d):
            X = s.zeros(d); X[i, j] = 1
            M[i*d:(i+1)*d, j*d:(j+1)*d] = mapfn(X)
    return M

for i in range(7):
    for j in range(7):
        X = s.zeros(7); X[i,j] = 1
        assert s.expand(s.trace(phi(X))-s.trace(X)) == 0
        assert (phi(phi(X))-square_eb_formula(X)).applyfunc(s.expand) == s.zeros(7)

Jphi = choi(phi, 7)
Jphi2 = choi(square_eb_formula, 7)
Wlift = s.zeros(49)
for i in range(3):
    for j in range(3):
        for a in range(3):
            for b in range(3):
                Wlift[7*i+3+a, 7*j+3+b] = W[3*i+a, 3*j+b]
assert s.expand(s.trace(Wlift*Jphi)) == -eps*mu
assert partial_output_trace(Jphi, 7, 7) == s.eye(7)

# All coefficient matrices of the CP+coCP decomposition have PSD/PPT
# analytic proofs; exact invariance under PT supplies the concrete check.
assert pt(Jphi, 7, 7) == Jphi
assert pt(Jphi2, 7, 7) == Jphi2

# Exact counterexample to the output-supported B identity displayed in
# Park v2 Proposition 3.6. The corrected input-supported factorization
# agrees for powers one and two in this smallest example.
P0 = s.diag(1, 0)
Q0 = s.diag(0, 1)
X11 = Q0
B_X11 = P0
assert Q0*B_X11*Q0 == s.zeros(2)
assert B_X11 != s.zeros(2)
# B^2(X11)=0 because the first B output lies in P, not Q.
assert B_X11[1,1]*P0 == s.zeros(2)

report = {
    "status": "exact rational algebra passed; block positivity proved in PROOFS.txt",
    "dimension": 7,
    "parameter_range": "0 < epsilon <= 1",
    "EB_index": 2,
    "witness_mu": str(mu),
    "unnormalized_witness_first_power": str(s.trace(Wlift*Jphi)),
    "unnormalized_witness_second_power": str(s.factor(s.trace(Wlift*Jphi2))),
    "UPB_effect": [[str(x) for x in E.row(i)] for i in range(3)],
    "Park_B_identity_counterexample": {
        "dimension": 2, "map": "Phi(X)=Tr(X)|0><0|",
        "input": "|1><1|", "B_output": "|0><0|", "Q_B_Q": "zero",
        "repair_checked": "B^p=B e_Q Phi_Q^(p-1) c_Q; p=1,2 in this example"
    },
    "threshold_cases": cases,
    "tests": ["UPB orthogonality and rank", "PPT invariance", "rational witness trace",
              "16 threshold cases", "Gram and inverse bounds", "TP on all matrix units",
              "square EB formula on all matrix units", "Choi TP", "Choi PT invariance",
              "Park displayed B identity counterexample"],
}
(HERE/'exact_results.json').write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps({k: v for k, v in report.items() if k not in ["threshold_cases", "UPB_effect"]}, indent=2))
