"""Independent deterministic checks; no source actor, sampling, or learner oracle.

This is a proof sanity check, not a count-acquired experiment and not a proof
of the acquisition module. All supplied/received manuscripts remain unchanged.
"""
import hashlib
import itertools
import json
import math
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parent

def h2(x):
    return -(x * math.log2(x) if x else 0) - ((1-x)*math.log2(1-x) if x < 1 else 0)

I = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.diag(1, -1)
kron = sp.kronecker_product
Id = sp.eye(4)
rho = Id / 4
c, s = sp.Rational(1599, 1601), sp.Rational(80, 1601)
U = c * Id - sp.I * s * kron(Z, Z)
assert sp.simplify(U.H * U) == Id
local = [(kron(X, I), kron(Y, I), kron(Z, I)),
         (kron(I, X), kron(I, Y), kron(I, Z))]
witnesses = []
for i, (vx, vy, vz) in enumerate(local):
    bx, by, bz = [sp.simplify(U * a * U.H) for a in (vx, vy, vz)]
    dx, dz = [sp.simplify(sp.trace(rho * (b-v)**2)) for b, v in ((bx, vx), (bz, vz))]
    P, Q = (Id+bz)/2, (Id-bz)/2
    Pp, Qp = (Id+vz)/2, (Id-vz)/2
    V0 = P.col_join(bx*Q)
    Vp = Pp.col_join(vx*Qp)
    assert sp.simplify(V0.H*V0) == Id and sp.simplify(Vp.H*Vp) == Id
    norm2 = sp.simplify(sp.trace(rho * (Vp-V0).H * (Vp-V0)))
    ax = (vx-vz*vx*vz)/2
    ay = sp.I*(vx*vz-vz*vx)/2
    az = vz
    bell_loss = sp.simplify((3-sum(sp.trace(rho*b*a) for b, a in zip((bx, by, bz), (ax, ay, az))))/4)
    assert dx == 4*s*s and dz == 0 and bell_loss == s*s
    assert bell_loss <= norm2 <= 2*dx + sp.Rational(3,4)*dz
    other_x = local[1-i][0]
    assert bx*other_x != other_x*bx  # true logical X is not locally supported
    ideal_ax = (bx-bz*bx*bz)/2
    ideal_ay = sp.I*(bx*bz-bz*bx)/2
    assert sp.simplify(ideal_ax-bx) == sp.zeros(4) and sp.simplify(ideal_ay-by) == sp.zeros(4)
    witnesses.append(dict(logical=i+1, delta_X=str(dx), delta_Z=str(dz),
                          proxy_Bell_loss=str(bell_loss), isometry_distance2=str(norm2),
                          proxy_isometry_exact=True, true_X_nonlocal=True,
                          ideal_local_target_fidelity_exact_one=True))

# Exhaustively check a small interval domain satisfying the consequence of
# approximate packing: every interval J contains at most 2|J| envelopes.
# If an envelope is inside J, so is its witness proxy support; this condition
# is therefore weaker than the full quantum theorem but sufficient here.
geometry_cases = 0
for n in range(1, 7):
    for W in range(1, min(n, 3)+1):
        intervals = [(a, b) for a in range(n) for b in range(a, min(n, a+W))]
        for q in range(1, min(n, 4)+1):
            for family in itertools.combinations_with_replacement(intervals, q):
                if any(sum(a <= l and r <= b for l, r in family) > 2*(b-a+1)
                       for a in range(n) for b in range(a, n)):
                    continue
                # Left-end sweep, retaining private labels for repeated intervals.
                colors, rightmost = [], []
                for a, b in family:
                    color = next((k for k, r in enumerate(rightmost) if r < a), len(rightmost))
                    if color == len(rightmost): rightmost.append(b)
                    else: rightmost[color] = b
                    colors.append(color)
                C = min(q, 4*W-2)
                assert len(rightmost) <= C
                span_cap = W+2*(C-1)*(W-1)
                K = min(q, 2*span_cap)
                anc = [{i} for i in range(q)]
                for i in sorted(range(q), key=lambda k: colors[k]):
                    ai, bi = family[i]
                    for j in range(q):
                        aj, bj = family[j]
                        if colors[j] < colors[i] and max(ai, aj) <= min(bi, bj):
                            anc[i] |= anc[j]
                for group in anc:
                    span = max(family[i][1] for i in group)-min(family[i][0] for i in group)+1
                    assert span <= span_cap and len(group) <= K
                assert all(sum(j in group for group in anc) <= K for j in range(q))
                geometry_cases += 1

received = [
    'ordinary_colored_pooled_joint_recovery_20261028.md',
    'ordinary_joint_local_logical_swap_recovery_20261028.md',
    'ordinary_local_mixed_gauge_decoder_tournament_20261028.md',
]
result = dict(
    status='PASS_DETERMINISTIC_PROOF_SANITY_CHECKS', source_calls=0,
    new_sampling=False, source_actor_or_private_files_read=False,
    guard=dict(tau_max='1/8', eta0_max='11/256',
               bell_fano_at_max=h2(11/256)+(11/256)*math.log2(3),
               binary_fano_at_max=h2(1/256)),
    exact_rational_nonlocal_unitary=dict(c=str(c), s=str(s), witnesses=witnesses),
    exhaustive_interval_cases=geometry_cases,
    interval_domain=dict(n_max=6, width_max=3, q_max=4),
    received_sha256={name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in received},
)
assert result['guard']['bell_fano_at_max'] < 0.5
assert result['guard']['binary_fano_at_max'] < 0.5
out = ROOT / 'approximate_local_algebra_packing_controls_check_20261028.json'
out.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
