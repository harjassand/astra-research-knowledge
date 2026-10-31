"""Endpoint parity, complete streaming loss instruments, and erasure codes.

Finite exact algebra checks for ENDPOINT_PARITY_ERASURE.txt.  These test the
polarization/interface algebra, not a fitted emitter/cavity apparatus.  The
inherited full optical/source trajectory tests remain in phase3_photon_closure.
"""
from pathlib import Path
from itertools import product, combinations
from math import comb, factorial
import json
import numpy as np
from scipy.linalg import norm
from scipy.stats import poisson, binom

ROOT = Path(__file__).resolve().parent
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
H = (X + Z) / np.sqrt(2)
PAULI = [I, X, Y, Z]


def kron_all(items):
    out = np.array([[1.]], dtype=complex)
    for a in items:
        out = np.kron(out, a)
    return out


def local_op(a, i, n):
    return kron_all([a if j == i else I for j in range(n)])


def proportional_identity_error(k):
    return float(norm(k - np.trace(k) * np.eye(k.shape[0]) / k.shape[0]))


def fine_stream_maps(n, mask):
    """Complete fine instrument for a fixed pattern of photon losses.

    Atomic states 0,1 are the C sector; state 2 is B.  Every lost photon is
    retained as an environmental polarization index, with no receiver CZ.
    Every collected photon receives the same CZ and an X measurement.
    Return maps from the input qubit to the correctly selected endpoint.
    """
    load = np.zeros((6, 2), complex)
    for j, a in product(range(2), repeat=2):
        load[2*j+a, j] = 1 / np.sqrt(2)
    if n == 0:
        yield load[[0, 2], :] * np.sqrt(2), (), None
        return
    for outcomes in product(range(2), repeat=n):
        k = load.copy()
        s = 0
        for p, bit in enumerate(outcomes):
            js = []
            for j in range(2):
                jj = np.zeros((3, 3), complex)
                if p % 2 == 0:
                    jj[2, j] = 1
                else:
                    jj[j, 2] = 1 / np.sqrt(2)
                js.append(jj)
            if mask[p]:
                step = np.kron(js[bit], I)
            else:
                step = (np.kron(js[0], I) + (-1)**bit*np.kron(js[1], Z)) / np.sqrt(2)
                s ^= bit
            k = step @ k
        if n % 2:
            out = np.linalg.matrix_power(Z, s) @ H @ k[4:6, :]
            yield out, outcomes, None
        else:
            for q in range(2):
                read = np.zeros((2, 6), complex)
                for j, a in product(range(2), repeat=2):
                    read[j, 2*j+a] = (-1)**(q*a)/np.sqrt(2)
                out = np.linalg.matrix_power(X, q) @ np.linalg.matrix_power(Z, s) @ read @ k
                yield out, outcomes, q


def stream_checks():
    completeness = []
    clean = []
    mismatch = []
    first_loss_constant = []
    patterns = 0
    maps = 0
    one_loss_maps = []
    two_loss_maps = []
    for n in range(7):
        for mask in product(range(2), repeat=n):
            ks = [k for k, _, _ in fine_stream_maps(n, mask)]
            patterns += 1
            maps += len(ks)
            completeness.append(float(norm(sum(k.conj().T @ k for k in ks) - I)))
            measured_endpoint = n % 2
            detected_parity = (n - sum(mask)) % 2
            mismatch.append(int((measured_endpoint ^ detected_parity) != sum(mask) % 2))
            if sum(mask) == 0:
                clean.extend(proportional_identity_error(k) for k in ks)
            if mask and mask[0]:
                outputs = []
                for a, b in product(range(2), repeat=2):
                    basis = np.zeros((2, 2), complex)
                    basis[a, b] = 1
                    outputs.append(sum(k @ basis @ k.conj().T for k in ks))
                first_loss_constant.append(max(float(norm(outputs[1])), float(norm(outputs[2])), float(norm(outputs[0]-outputs[3]))))
            if sum(mask) == 1 and n <= 4:
                one_loss_maps.extend(ks)
            if sum(mask) == 2 and n <= 4:
                two_loss_maps.extend(ks)
    return ({"photon_counts_checked": list(range(7)),
             "loss_patterns_checked": patterns,
             "complete_fine_maps_checked": maps,
             "max_instrument_completeness_error": max(completeness),
             "max_clean_fine_map_identity_error": max(clean),
             "endpoint_loss_parity_mismatches": max(mismatch),
             "max_first_photon_loss_constant_channel_error": max(first_loss_constant)},
            one_loss_maps, two_loss_maps)


def four_qubit_code():
    v = np.zeros((16, 2), complex)
    v[[0, 15], 0] = 1 / np.sqrt(2)
    v[[3, 12], 1] = 1 / np.sqrt(2)
    return v


def four_code_checks(one_loss_maps):
    v = four_qubit_code()
    errs = []
    gram = []
    for pos in range(4):
        fs = []
        for b in range(2):
            f = np.zeros((2, 2), complex)
            f[0, b] = 1
            fs.append(local_op(f, pos, 4))
        recovery = [np.sqrt(2)*v.conj().T @ f.conj().T for f in fs]
        for b, c in product(range(2), repeat=2):
            gram.append(float(norm(v.conj().T @ fs[b].conj().T @ fs[c] @ v - (I/2 if b == c else np.zeros((2, 2))))))
        for k in one_loss_maps:
            kk = local_op(k, pos, 4)
            # Discard flagged output and reload zero, then recover the code.
            for r, f in product(recovery, fs):
                errs.append(proportional_identity_error(r @ f @ kk @ v))
    return {"code": "[[4,1,2]]",
            "max_erasure_gram_error": max(gram),
            "corrected_fine_loss_histories": len(errs),
            "max_recovered_fine_map_identity_error": max(errs)}


def five_qubit_code():
    labels = ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]
    p = np.eye(32, dtype=complex)
    paulis = dict(zip("IXYZ", PAULI))
    for label in labels:
        p = p @ (np.eye(32) + kron_all([paulis[a] for a in label])) / 2
    zero = p[:, 0] / norm(p[:, 0])
    one = kron_all([X]*5) @ zero
    return np.stack([zero, one], axis=1)


def five_code_checks(two_loss_maps):
    v = five_qubit_code()
    pauli_errors = [np.eye(32, dtype=complex)]
    pauli_errors.extend(local_op(p, i, 5) for i in range(5) for p in [X, Y, Z])
    recover_no_flag = [v.conj().T @ e.conj().T for e in pauli_errors]
    gram = [float(norm(v.conj().T @ a.conj().T @ b @ v - (I if ia == ib else 0)))
            for ia, a in enumerate(pauli_errors) for ib, b in enumerate(pauli_errors)]
    hidden = []
    for pos in range(5):
        for k in two_loss_maps:
            kk = local_op(k, pos, 5)
            hidden.extend(proportional_identity_error(r @ kk @ v) for r in recover_no_flag)
    rng = np.random.default_rng(486313)
    double_flag = []
    two_erasure_gram = []
    for places in combinations(range(5), 2):
        errors = [kron_all([a if i == places[0] else b if i == places[1] else I for i in range(5)]) for a, b in product(PAULI, repeat=2)]
        recovery = [v.conj().T @ e.conj().T for e in errors]
        for ia, a in enumerate(errors):
            for ib, b in enumerate(errors):
                two_erasure_gram.append(float(norm(v.conj().T @ a.conj().T @ b @ v - (I if ia == ib else 0))))
        # A generic joint error at the flagged pair: includes correlations.
        coefficients = rng.normal(size=16) + 1j*rng.normal(size=16)
        k = sum(c*e for c, e in zip(coefficients, errors))
        k /= norm(k)
        double_flag.extend(proportional_identity_error(r @ k @ v) for r in recovery)
    return {"code": "[[5,1,3]]",
            "max_single_unknown_error_gram_error": max(gram),
            "max_two_erasure_gram_error": max(two_erasure_gram),
            "corrected_two_loss_same_stream_fine_histories": len(hidden),
            "max_hidden_two_loss_recovery_error": max(hidden),
            "max_correlated_two_flag_recovery_error": max(double_flag)}


def loss_bounds():
    rows = []
    for n, d in [(4, 2), (5, 3)]:
        for exposure in [.1, 1., 4.]:
            mu = n * exposure
            coefficient = sum(comb(n, j)*mu**(d-j)/factorial(d-j) for j in range(min(n, d)+1))
            for epsilon in [1e-4, 1e-3, 1e-2, .1]:
                # Dominating model: Poisson emissions during the drive, plus
                # at most one drain photon per emitter. Thin every photon.
                small = sum(binom.pmf(j, n, epsilon) * poisson.cdf(d-1-j, epsilon*mu) for j in range(min(n, d-1)+1))
                exact_tail = max(0., 1-small)
                bound = min(1., epsilon**d * coefficient)
                assert exact_tail <= bound + 3e-14
                rows.append({"n":n, "distance":d, "Gamma_T":exposure,
                             "loss_per_photon":epsilon,
                             "factorial_moment_bound":bound,
                             "dominating_process_exact_tail":exact_tail})
    return rows


def shelving_selection_rule():
    # Ordered x,y,z,a. A calibrated pi pulse on z <-> a is exactly identity
    # on the logical C sector. The angular-momentum realization discussed
    # in the note is F=1 --(pi light)--> F'=0.
    from scipy.linalg import expm
    h = np.zeros((4, 4), complex)
    h[2, 3] = h[3, 2] = 1
    u = expm(-1j*np.pi*h/2)
    return {"C_sector_identity_error":float(norm(u[:2, :2]-I)),
            "C_leakage_error":float(norm(u[2:, :2])),
            "z_to_shelf_probability":float(abs(u[3, 2])**2)}


def main():
    stream, one, two = stream_checks()
    results = {"stream_instrument":stream,
               "four_qubit_recovery":four_code_checks(one),
               "five_qubit_recovery":five_code_checks(two),
               "loss_bounds":loss_bounds(),
               "selective_shelving_algebra":shelving_selection_rule()}
    (ROOT / "endpoint_erasure_results.json").write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps({k:v for k,v in results.items() if k != "loss_bounds"}, indent=2))
    print("All 24 finite-duration thinning bounds verified.")


if __name__ == "__main__":
    main()
