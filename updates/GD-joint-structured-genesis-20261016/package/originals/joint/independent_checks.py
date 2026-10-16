"""Original bounded diagnostic checks; no repository code is imported or run."""
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.linalg import expm

ROOT = Path(__file__).resolve().parent
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)


def sine(a):
    return float(np.sin(min(float(a), np.pi / 2)) ** 2)


def q(actions):
    return float(1 - np.prod([1 - sine(a) for a in actions]))


def colored(edges, d=2):
    out = np.zeros((4 * d, 4 * d), complex)
    for p, r, block in edges:
        block = block / np.linalg.norm(block, 2)
        out[p*d:(p+1)*d, r*d:(r+1)*d] = block
        out[r*d:(r+1)*d, p*d:(p+1)*d] = block.conj().T
    return out


def pieces(variant, a1=0.71, a2=0.93):
    """Three noncommuting pieces with conditional bath blocks on each edge."""
    weights1 = np.array([0.20, 0.35, 0.45])
    weights2 = np.array([0.40, 0.10, 0.50])
    result = []
    for k in range(3):
        phase = (variant + 1) * (k + 1) * np.pi / 7
        c10 = X + 0.37j * np.exp(1j*phase) * Z
        c11 = Z + 0.41 * np.exp(-1j*phase) * Y
        c20 = Y + 0.29j * np.exp(-1j*phase) * X
        c21 = X + 0.53 * np.exp(1j*phase) * Z
        v1 = colored([(0, 2, c10), (1, 3, c11)])
        v2 = colored([(0, 1, c20), (2, 3, c21)])
        h0 = np.zeros((8, 8), complex)
        for r in range(4):
            block = ((r-1.5)*0.17*X + (k-1)*0.23*Y
                     + (variant-1.5)*0.13*(r+1)*Z)
            h0[2*r:2*r+2, 2*r:2*r+2] = block
        b1, b2 = a1*weights1[k], a2*weights2[k]
        result.append((h0, b1*v1, b2*v2, b1, b2))
    return result


def diagnostics(data):
    z1, z2 = np.kron(np.diag([1, 1, -1, -1]), I), np.kron(np.diag([1, -1, 1, -1]), I)
    errs = []
    for h0, v1, v2, b1, b2 in data:
        errs += [np.linalg.norm(h0@z1-z1@h0, 2), np.linalg.norm(h0@z2-z2@h0, 2),
                 np.linalg.norm(v1@z1+z1@v1, 2), np.linalg.norm(v2@z2+z2@v2, 2),
                 np.linalg.norm(v1@z2-z2@v1, 2), np.linalg.norm(v2@z1-z1@v2, 2),
                 max(0, np.linalg.norm(v1, 2)-b1), max(0, np.linalg.norm(v2, 2)-b2)]
    return float(max(errs))


def endpoint(data, cuts):
    """Return maximum endpoint effect eigenvalue over the entering bath."""
    ks = [np.eye(8, dtype=complex)[:, :2]]
    masks = [np.repeat([1, 1, 0, 0], 2), np.repeat([1, 0, 1, 0], 2)]
    for k, (h0, v1, v2, _, _) in enumerate(data):
        u = expm(-1j*(h0+v1+v2))
        ks = [u@v for v in ks]
        for coordinate in cuts.get(k, []):
            mask = masks[coordinate][:, None]
            ks = [p*v for v in ks for p in [mask, 1-mask]]
    effect = sum((v[6:8, :].conj().T@v[6:8, :] for v in ks), np.zeros((2, 2), complex))
    return float(np.linalg.eigvalsh(effect)[-1])


rows = []
max_contract_error = 0.0
for variant in range(4):
    data = pieces(variant)
    max_contract_error = max(max_contract_error, diagnostics(data))
    b1 = [v[3] for v in data]
    b2 = [v[4] for v in data]
    cases = [
        ("one_gap", {}, [[sum(b1)], [sum(b2)]], True),
        ("synchronized_three_gaps", {0: [0, 1], 1: [0, 1]}, [b1, b2], True),
        ("coordinate_1_unpinched", {0: [1], 1: [1]}, [[sum(b1)], b2], True),
        ("asynchronous_two_gaps_diagnostic_only", {0: [0], 1: [1]},
         [[b1[0], sum(b1[1:])], [sum(b2[:2]), b2[2]]], False),
    ]
    for label, cuts, actions, proved in cases:
        actual = endpoint(data, cuts)
        product_q = q(actions[0])*q(actions[1])
        sine_union = np.prod([min(1, sum(sine(a) for a in acts)) for acts in actions])
        rows.append(dict(case=label, variant=variant, effect_norm=actual,
                         product_q=product_q, ratio_to_product_q=actual/product_q,
                         product_q_proved_for_class=proved,
                         proved_sine_union_bound=float(sine_union)))
        assert actual <= sine_union + 2e-12
        if proved:
            assert actual <= product_q + 2e-12

# Exact one-gap equality and an exact invalid-postselection shortcut.
a, b = np.arcsin(3/5), np.arcsin(5/13)
drive1 = expm(-1j*a*np.kron(X, I))
drive2 = expm(-1j*b*np.kron(I, X))
psi = (drive2@drive1)[:, 0]
product_exact = 9/169
one_gap_saturation_error = abs(abs(psi[3])**2-product_exact)
conditional_drive = expm(-1j*b*np.kron(np.diag([0, 1]), X))
psi_cond = (conditional_drive@drive1)[:, 0]
p2 = float(abs(psi_cond[1])**2+abs(psi_cond[3])**2)
p12 = float(abs(psi_cond[3])**2)
conditional_example = dict(joint_exact="9/169", singleton_1_exact="9/25",
                           joint_numerical=p12, conditional_flip_1_given_flip_2=p12/p2)
assert abs(p12-product_exact) < 2e-14
assert p12/p2 == 1.0

# Tensor sink witness for three synchronized gaps. This is authored directly.
cosines1 = [4/5, 12/13, 15/17]
cosines2 = [12/13, 4/5, 15/17]
actions1 = np.arccos(cosines1)
actions2 = np.arccos(cosines2)
local_dim = 8  # memory qubit times four bath states
zlocal = np.kron(Z, np.eye(4))
z1 = np.kron(zlocal, np.eye(local_dim))
z2 = np.kron(np.eye(local_dim), zlocal)
proj = [(np.eye(64)+z)/2 for z in [z1, z2]]
psi0 = np.zeros((64, 1), complex)
psi0[0, 0] = 1
ks = [psi0]
for k, (angle1, angle2) in enumerate(zip(actions1, actions2)):
    coupling = np.zeros((4, 4), complex)
    coupling[0, k+1] = coupling[k+1, 0] = 1
    local = np.kron(X, coupling)
    u = np.kron(expm(-1j*angle1*local), expm(-1j*angle2*local))
    ks = [u@v for v in ks]
    if k != 2:
        for p in proj:
            ks = [a@v for v in ks for a in [p, np.eye(64)-p]]
pwrong = (np.eye(64)-proj[0])@(np.eye(64)-proj[1])
sink_actual = float(sum(np.linalg.norm(pwrong@v)**2 for v in ks))
sink_target = q(actions1)*q(actions2)
sink_error = abs(sink_actual-sink_target)
assert sink_error < 3e-14

result = dict(
    method="Original deterministic finite matrices; no random sweep, optimization, or acquired code execution.",
    versions=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__),
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    number_conditional_shared_bath_cases=len(rows),
    maximum_hypothesis_residual=max_contract_error,
    rows=rows,
    one_gap_saturation=dict(exact_probability="9/169", absolute_error=one_gap_saturation_error),
    conditional_shortcut_counterexample=conditional_example,
    synchronized_sink_saturation=dict(gaps=3, bath_dimension=16, actual=sink_actual,
                                      product_q=sink_target, absolute_error=sink_error),
    conclusion="No numerical counterexample observed. The asynchronous diagnostic rows are not a proof. See PROOF.md for analytic scope.",
)
(ROOT/"independent_results.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
