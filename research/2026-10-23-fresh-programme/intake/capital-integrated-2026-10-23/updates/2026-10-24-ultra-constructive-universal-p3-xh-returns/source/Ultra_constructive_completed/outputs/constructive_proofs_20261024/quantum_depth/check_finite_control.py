#!/usr/bin/env python3
"""Finite shared-bath counterexample search for the declared compiler.

Two memory qubits + one persistent bath qubit; finite rectangular controls.
This is model algebra, not hardware data, a diamond-norm SDP, or a proof.
"""
import itertools
import json
import math
from pathlib import Path

import numpy as np


PAULI = [np.eye(2), np.array([[0, 1], [1, 0]]),
         np.array([[0, -1j], [1j, 0]]), np.diag([1, -1])]


def tensor(*xs):
    ans = np.ones((1, 1), complex)
    for x in xs:
        ans = np.kron(ans, x)
    return ans


def exp_hermitian(H, duration):
    val, vec = np.linalg.eigh(H)
    return (vec*np.exp(-1j*duration*val))@vec.conj().T


def norm(H):
    return float(np.linalg.norm(H, 2))


def conditional_expectation(K, sites):
    for i in sites:
        out = np.zeros_like(K)
        for p in PAULI:
            op = tensor(p, PAULI[0], PAULI[0]) if i == 0 else tensor(PAULI[0], p, PAULI[0])
            out += op@K@op/4
        K = out
    return K


def choi_from_kraus(ks):
    d = ks[0].shape[0]
    J = np.zeros((d*d, d*d), complex)
    for K in ks:
        vec = K.flatten(order='F')
        J += np.outer(vec, vec.conj())
    return (J+J.conj().T)/2


def diamond_bounds(J, d):
    ev, V = np.linalg.eigh((J+J.conj().T)/2)
    absolute = (V*np.abs(ev))@V.conj().T
    # ||J/d||_1 is a lower bound obtained using a maximally entangled input.
    lower = float(np.abs(ev).sum()/d)
    # CP Jordan decomposition gives ||Phi||diamond <= ||Tr_output |J|||.
    partial = np.einsum('iaja->ij', absolute.reshape(d, d, d, d))
    upper = float(np.linalg.eigvalsh((partial+partial.conj().T)/2).max())
    return lower, upper, float(ev.min())


def main():
    I, X, Y, Z = PAULI
    HB = .31*tensor(I, I, Z)+.12*tensor(I, I, X)
    raw = [tensor(X, I, X)+.7*tensor(Z, I, Y),
           tensor(I, Y, Z)+.3*tensor(I, Z, X)]
    hs = [.03, .04]
    Hs = [h*H/norm(H) for h, H in zip(hs, raw)]
    tau, tp = .8, .001
    omega = math.pi/tp
    idle = exp_hermitian(HB+sum(Hs), tau)
    d = 8
    G = {}
    for mask in range(4):
        selected = [i for i in range(2) if mask & (1 << i)]
        ks = []
        for key in itertools.product(range(4), repeat=2):
            ctrl = np.zeros((d, d), complex)
            for i in range(2):
                if key[i]:
                    ctrl += omega/2*(tensor(PAULI[key[i]], I, I) if i == 0
                                           else tensor(I, PAULI[key[i]], I))
            native = HB+sum(Hs[i] for i in range(2) if i not in selected)
            pre = exp_hermitian(ctrl+native, tp)
            post = exp_hermitian(-ctrl+native, tp)
            U = post@idle@pre
            assert norm(U.conj().T@U-np.eye(d)) < 2e-13
            # R_mask switches off selected control-slab errors; P0_mask is
            # the normalized identity-Pauli Kraus coefficient at those sites.
            ks.append(conditional_expectation(U, selected)/4)
        G[mask] = choi_from_kraus(ks)

    eta = np.array(hs)*tau
    alpha = np.array(hs)*2*tp
    q = eta*eta+2*alpha
    rows = []
    for mask in [1, 2, 3]:
        sub = [s for s in range(4) if s & ~mask == 0]
        J = sum((-1)**s.bit_count()*G[s] for s in sub)
        lower, upper, min_eig = diamond_bounds(J, d)
        selected = [i for i in range(2) if mask & (1 << i)]
        bound = float(np.prod(q[selected]))
        assert lower <= bound+2e-12
        assert upper <= bound+2e-12
        rows.append({'selected_sites': selected,
                     'Choi_trace_norm_lower_bound_on_diamond': lower,
                     'CP_Jordan_upper_bound_on_diamond': upper,
                     'analytic_fault_path_bound': bound,
                     'minimum_Choi_eigenvalue_not_a_CP_fault_probability': min_eig})

    # Exact expansion and support: NF=sum_{T subset F}(-1)^|T| G_(Fc union T).
    Ns = {}
    for f in range(4):
        comp = 3 ^ f
        Ns[f] = sum((-1)**s.bit_count()*G[comp | s]
                    for s in range(4) if s & ~f == 0)
    expansion_error = norm(sum(Ns.values())-G[0])
    assert expansion_error < 1e-12
    support_error = 0.
    for f, J in Ns.items():
        for i in range(2):
            if not f & (1 << i):
                liouville = np.zeros((d*d,d*d),complex)
                for p in PAULI:
                    op = tensor(p,I,I) if i == 0 else tensor(I,p,I)
                    liouville += np.kron(op.conj(),op)/4
                support_error = max(support_error, norm(J-liouville@J@liouville.conj().T))
    assert support_error < 1e-12
    result = {'not_hardware_or_general_proof': True, 'memory_qubits': 2,
              'persistent_bath_dimension': 2, 'native_h': hs, 'idle_tau': tau,
              'physical_rectangular_pi_duration': tp, 'physical_control_angular_rate': omega,
              'idle_eta': eta.tolist(), 'pulse_alpha': alpha.tolist(),
              'q_eta_squared_plus_two_alpha': q.tolist(),
              'selected_fault_path_checks': rows,
              'exact_fault_expansion_error': expansion_error,
              'outside_fault_set_identity_support_error': support_error,
              'scope': 'uniform fresh local keys; key noise is native local H_i during finite pulse slabs; Choi lower/upper bounds are not exact diamond SDP values'}
    path = Path(__file__).with_name('FINITE_CONTROL_CHECK.json')
    path.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
