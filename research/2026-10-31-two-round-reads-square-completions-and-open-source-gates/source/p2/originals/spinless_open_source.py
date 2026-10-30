"""Active entangling leaves with an arbitrary commuting central source.

This is a finite-dimensional check of the active system and exact source
commutators. The accompanying proof, not a finite-bath simulation, extends
the statement to any well-defined central reservoir with the specified
coupling algebra. No raw spinful or higher-orbital protection is claimed.

Run from this directory or by absolute path. Units: hbar = Delta = 1.
"""
from pathlib import Path
import importlib.util
import json
import math
import numpy as np
from scipy.linalg import eigh, expm

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("spinless_model", HERE / "alternatives" / "spinless.py")
sm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sm)


def norm(a):
    return float(np.linalg.norm(a, 2))


def comm(a, b):
    return a @ b - b @ a


def main():
    m = sm.model()
    eye = np.eye(16)
    E = sm.two_code(m["E"])
    p = E @ E.conj().T
    q = np.eye(256) - p
    na = np.kron(m["no"], eye)
    nb = np.kron(eye, m["no"])
    k = np.kron(m["ne"], eye) + 2 * np.kron(eye, m["ne"])
    d = sum(np.kron(m["n"][j], m["n"][j]) for j in range(1, 4))
    # No_A, No_B are diagonal in the original occupation basis.
    nav = np.diag(na).real
    nbv = np.diag(nb).real
    domain = np.flatnonzero(np.isin(nav, [1, 2]) & np.isin(nbv, [1, 2]))
    center = (np.maximum(0, nav + nbv - 3) + np.minimum(nav, nbv)) / 2
    r = d - np.diag(center)
    odd_parity = np.diag([(-1) ** i.bit_count() for i in range(16)])
    sources = {
        "central_annihilation_A": np.kron(m["c"][0], eye),
        "central_annihilation_B_fermionic_order": np.kron(odd_parity, m["c"][0]),
        "outer_number_A": na,
        "outer_number_B": nb,
        "central_A_to_outer_B_capacitance": np.kron(m["n"][0], m["no"]),
        "outer_A_to_central_B_capacitance": np.kron(m["no"], m["n"][0]),
        "central_pair_capacitance": np.kron(m["n"][0], m["n"][0]),
        "outer_monopole_capacitance": na @ nb,
    }
    commutators = {}
    for label, s in sources.items():
        sp = E.conj().T @ s @ E
        sg = sm.partial_gauge(sp, 4, 16)
        commutators[label] = {
            "offset_commutator": norm(comm(k, s)),
            "interaction_commutator": norm(comm(d, s)),
            "projected_logical_identity_residual": norm(sp - np.kron(np.eye(4), sg)),
        }
    hop = np.kron(m["c"][0].conj().T @ m["b"] + m["b"].conj().T @ m["c"][0], eye)
    projected_d = E.conj().T @ d @ E
    logical_d = (np.kron(sm.X, sm.X) + np.kron(sm.Z, sm.Z)) / 6
    gauge_d = sm.partial_gauge(projected_d, 4, 16)
    rows = []
    for ratio in [.02, .01, .005, .002]:
        h = k + ratio * d
        time = 3 * math.pi / (2 * ratio)
        en, vec = eigh(h)
        output = vec @ (np.exp(-1j * en * time)[:, None] * (vec.conj().T @ E))
        hp = E.conj().T @ h @ E
        target = E @ expm(-1j * hp * time)
        gap = 1 - ratio
        bound = ratio / (3 * gap) * (4 + math.sqrt(2) * math.pi * math.exp(4 * ratio / (3 * gap)))
        rows.append({
            "delta_V_over_Delta": ratio,
            "duration_in_hbar_over_Delta": time,
            "joint_isometry_error_vs_projected_dynamics": norm(output - target),
            "leakage_amplitude": norm(q @ output),
            "analytic_joint_isometry_bound": bound,
        })
    out = {
        "scope": "Full 256-state active system; 64-dimensional logical-plus-gauge input. Exact commuting source algebra permits arbitrary reservoir dynamics. Numerical checks are floating point, not certified enclosures.",
        "invariant_outer_number_domain_dimension": int(len(domain)),
        "centered_contact_norm_in_domain": norm(r[np.ix_(domain, domain)]),
        "centered_contact_norm_on_entire_Fock_space": norm(r),
        "expected_centered_contact_norm": .5,
        "off_sector_contact_norm": norm(q @ d @ E),
        "expected_off_sector_contact_norm": math.sqrt(2) / 3,
        "projected_logical_plus_gauge_residual": norm(projected_d - np.kron(logical_d, np.eye(16)) - np.kron(np.eye(4), gauge_d)),
        "source_algebra_checks": commutators,
        "unpaused_central_bright_hopping_interaction_commutator": norm(comm(d, hop)),
        "invariant_bright_number_interaction_commutator": norm(comm(d, np.kron(m["nb"], eye))),
        "gate_checks": rows,
    }
    path = HERE / "spinless_open_source_results.json"
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
