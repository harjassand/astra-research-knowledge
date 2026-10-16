#!/usr/bin/env python3
"""Exact finite witnesses for the cut/support receiving investigation.

Only writes CHECK_RESULTS.json beside this script. No source files are executed.
These calculations do not establish an asymptotic memory theorem.
"""
import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Z = sp.diag(1, -1)
c, s = sp.sqrt(3)/2, sp.Rational(1, 2)


def kron(*xs):
    out = sp.Matrix([[1]])
    for x in xs:
        out = sp.kronecker_product(out, x)
    return out


def is_zero(m):
    return all(sp.simplify(v) == 0 for v in m)


def enc(v):
    return [[str(sp.simplify(x)) for x in row] for row in v.tolist()]


def symp(p, q):
    x, z = p
    y, w = q
    return ((x & w).bit_count() + (z & y).bit_count()) % 2


def subgroup(gens):
    result = {(0, 0)}
    for x, z in gens:
        result |= {(a ^ x, b ^ z) for a, b in list(result)}
    return result


def paulis_on(sites):
    out = []
    for terms in itertools.product(range(4), repeat=len(sites)):
        x = z = 0
        for site, term in zip(sites, terms):
            if term & 1:
                x |= 1 << site
            if term & 2:
                z |= 1 << site
        out.append((x, z))
    return out


results = {}

# Exact unchanged-predicate counterexample, including actual initial pinching.
P = [(I2+Z)/2, (I2-Z)/2]
U = c*I2-sp.I*s*X
old = sp.zeros(2)
endpoint = sp.zeros(2)
normal = sp.zeros(2)
for r, t in itertools.product(range(2), repeat=2):
    # skip/complete-pinch pattern has actual weights 1/2,1/2.
    for label, middle in [(None, I2/sp.sqrt(2))] + [
        (u, P[u]/sp.sqrt(2)) for u in range(2)
    ]:
        A = P[t]*U*middle*U*P[r]
        effect = sp.simplify(A.H*A)
        normal += effect
        if (t != r if label is None else label != r or t != label):
            old += effect
        if t != r:
            endpoint += effect
assert is_zero(normal-I2)
assert is_zero(old-sp.Rational(19, 32)*I2)
assert is_zero(endpoint-sp.Rational(18, 32)*I2)
results["predicate_counterexample"] = {
    "old_effect": enc(old), "endpoint_effect": enc(endpoint),
    "difference": enc(old-endpoint), "normalization_exact": True,
}

# [[4,2,2]] support kernels, enumerated modulo phases.
gens = [(15, 0), (0, 15)]
stab = subgroup(gens)
central = lambda region: [p for p in paulis_on(region)
                         if all(symp(p, g) == 0 for g in gens)]
one = central([0])
two = central([1])
both = central([0, 1])
assert set(one) <= stab and set(two) <= stab
violations = set(both)-stab
assert violations == {(3, 0), (0, 3), (3, 3)}
whole = central([0, 1, 2, 3])
assert len(whole) == 64 and len(stab) == 4
results["segmented_kernel_strict_gain"] = {
    "code_generators": ["XXXX", "ZZZZ"],
    "singleton_centralizers": [one, two],
    "union_kernel_nonstabilizers_xz_masks": sorted(violations),
    "whole_detector_centralizer_count": len(whole),
    "whole_detector_stabilizer_count": len(stab),
    "rank_obstruction": {"m": 4, "g": 2, "r": 2,
                         "centralizer_dimension": 6},
}

I16 = sp.eye(16)
G0, G1 = kron(X, X, X, X), kron(Z, Z, Z, Z)
projectors = [sp.simplify((I16+(-1)**r0*G0)*(I16+(-1)**r1*G1)/4)
              for r0, r1 in itertools.product(range(2), repeat=2)]
X1, X2 = kron(X, I2, I2, I2), kron(I2, X, I2, I2)
U1, U2 = c*I16-sp.I*s*X1, c*I16-sp.I*s*X2
V = sp.zeros(16, 4)
for col, basis in enumerate([0, 3, 5, 6]):
    V[basis, col] = 1/sp.sqrt(2)
    V[15-basis, col] = 1/sp.sqrt(2)
assert is_zero(V.H*V-sp.eye(4))
assert is_zero(projectors[0]*V-V)
L = sp.simplify(V.H*X1*X2*V)
assert is_zero(L*L-sp.eye(4)) and sp.trace(L) == 0

hist_effect = sp.zeros(16)
end_effect = sp.zeros(16)
joint_effect = sp.zeros(16)
normal = sp.zeros(16)
for r, u, t in itertools.product(range(4), repeat=3):
    A = projectors[t]*U2*projectors[u]*U1*projectors[r]
    E = sp.simplify(A.H*A)
    normal += E
    b1, b2 = u != r, t != u
    if b1 or b2:
        hist_effect += E
    if t != r:
        end_effect += E
    if b1 and b2:
        joint_effect += E
assert is_zero(normal-I16)
assert is_zero(hist_effect-sp.Rational(7, 16)*I16)
assert is_zero(end_effect-sp.Rational(3, 8)*I16)
assert is_zero(joint_effect-sp.Rational(1, 16)*I16)
encoded_return = [sp.simplify(V.H*projectors[0]*U2*projectors[u]*U1*V)
                  for u in range(4)]
nonzero_returns = [a for a in encoded_return if not is_zero(a)]
assert len(nonzero_returns) == 2
assert is_zero(nonzero_returns[0]-sp.Rational(3, 4)*sp.eye(4))
assert is_zero(nonzero_returns[1]+sp.Rational(1, 4)*L)
K_uncut = sp.simplify(V.H*projectors[0]*U2*U1*V)
assert is_zero(K_uncut-(3*sp.eye(4)-L)/4)
alpha = sp.symbols("alpha", positive=True)
# In normalized vec(I),vec(L), each vec has norm sqrt(4)=2.
J_uncut_restricted = sp.Matrix([[sp.Rational(9, 4), -sp.Rational(3, 4)],
                                [-sp.Rational(3, 4), sp.Rational(1, 4)]])
J_id_restricted = sp.diag(4, 0)
assert J_uncut_restricted.rank() == 1
minorant_det = sp.factor((J_uncut_restricted-alpha*J_id_restricted).det())
assert minorant_det == -alpha
results["actual_cut_logical_return"] = {
    "logical_return_operator": enc(L),
    "endpoint_zero_nonzero_encoded_kraus": [enc(a) for a in nonzero_returns],
    "history_mismatch_effect_scalar": "7/16",
    "endpoint_mismatch_effect_scalar": "3/8",
    "both_segment_mismatches_effect_scalar": "1/16",
    "no_segment_mismatch_encoded_map": "(9/16) Id",
    "endpoint_zero_encoded_map": "(9/16) Id + (1/16) Ad_L",
    "uncut_zero_endpoint_kraus": enc(K_uncut),
    "uncut_choi_minus_alpha_identity_determinant": str(minorant_det),
    "all_effect_equalities_on_full_physical_input": True,
}

# Native completed pair is identity on coherence between inactive sectors.
Pi = sp.diag(0, 0, 0, 1)
I4, Q = sp.eye(4), kron(X, X)
C = lambda rho: sp.simplify(Q*Pi*rho*Pi*Q.H+(I4-Pi)*rho*(I4-Pi))
D = lambda rho: sp.diag(*list(rho.diagonal()))
coherence = sp.zeros(4)
coherence[0, 1] = 1
assert is_zero(C(coherence)-coherence) and is_zero(D(coherence))
psi = sp.Matrix([1/sp.sqrt(2), 1/sp.sqrt(2), 0, 0])
rho = psi*psi.H
diff = sp.simplify(C(rho)-D(rho))
trace_norm = sum(abs(eig)*mult for eig, mult in diff.eigenvals().items())
assert trace_norm/2 == sp.Rational(1, 2)
results["native_pair_not_full_cut"] = {
    "inactive_coherence_survives": True,
    "generator_annihilates_that_coherence": True,
    "full_pinching_annihilates_that_coherence": True,
    "prepared_state_half_trace_distance": "1/2",
}

# Four-dimensional cubical toric local support and same-CSS blind direction.
side = 3
coords = list(itertools.product(range(side), repeat=4))
axis_pairs = list(itertools.combinations(range(4), 2))
face_id = {(v, ij): n for n, (v, ij) in enumerate(itertools.product(coords, axis_pairs))}


def shift(v, a, amount):
    v = list(v)
    v[a] = (v[a]+amount) % side
    return tuple(v)


def edge_x(v, axis):
    support = set()
    for other in range(4):
        if other != axis:
            pair = tuple(sorted((axis, other)))
            support |= {face_id[(v, pair)], face_id[(shift(v, other, -1), pair)]}
    return sum(1 << j for j in support), 0


def cube_z(v, axes):
    support = set()
    for pair in itertools.combinations(axes, 2):
        missing = next(a for a in axes if a not in pair)
        support |= {face_id[(v, pair)], face_id[(shift(v, missing, 1), pair)]}
    return 0, sum(1 << j for j in support)


origin = (0, 0, 0, 0)
g1, g2 = edge_x(origin, 0), edge_x(origin, 1)
face = face_id[(origin, (0, 1))]
xf, zf = (1 << face, 0), (0, 1 << face)
cube = cube_z(origin, (0, 1, 2))
assert (g1[0] | g2[0]).bit_count() == 11
assert symp(g1, cube) == symp(g2, cube) == 0
assert symp(xf, g1) == symp(xf, g2) == 0
assert symp(xf, cube) == 1
assert symp(zf, g1) == symp(zf, g2) == 1
results["actual_4d_pair_blind_error"] = {
    "torus_side_for_local_algebra": side,
    "each_edge_check_weight": [g1[0].bit_count(), g2[0].bit_count()],
    "pair_full_data_support_count": (g1[0] | g2[0]).bit_count(),
    "X_face_commutes_with_both_pair_checks": True,
    "X_face_anticommutes_with_incident_Z_cube": True,
    "Z_face_toggles_both_pair_checks": True,
    "scope": "finite local symplectic algebra, not dynamics or lifetime",
}

payload = {
    "status": "ALL_EXACT_CHECKS_PASSED",
    "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "sympy_version": sp.__version__,
    "checks": results,
    "claims_not_established": ["asymptotic lifetime", "physical qualification",
                               "useful threshold", "historical priority",
                               "external proof certification"],
}
(HERE/"CHECK_RESULTS.json").write_text(json.dumps(payload, indent=2)+"\n")
print(json.dumps({"status": payload["status"], "check_groups": list(results)}, indent=2))
