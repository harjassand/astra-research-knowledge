"""Exact elementary entropy certificate plus finite Gaussian/Fock diagnostics.

The rational arithmetic establishes the entropy comparison. NumPy checks
are supporting finite diagnostics; the universal arguments are in the report.
"""
from fractions import Fraction as F
import json
from pathlib import Path


def log_interval(x, terms=90):
    """Rational enclosure of log(x), from the atanh series."""
    assert x > 0
    k = 0
    y = x
    while y >= 2:
        y /= 2
        k += 1
    while y < 1:
        y *= 2
        k -= 1

    def series(q):
        z = (q - 1) / (q + 1)
        value = sum((2 * z ** (2*j + 1) / (2*j + 1) for j in range(terms)), F(0))
        remainder = 2 * z ** (2*terms + 1) / ((2*terms + 1) * (1-z*z))
        assert z >= 0
        return value, value + remainder

    lo, hi = series(y)
    l2, h2 = series(F(2))
    return ((lo+k*l2, hi+k*h2) if k >= 0 else (lo+k*h2, hi+k*l2))


def g_interval(x):
    assert x >= 0
    if x == 0:
        return F(0), F(0)
    lp, hp = log_interval(x+1)
    lm, hm = log_interval(x)
    return (x+1)*lp-x*hm, (x+1)*hp-x*lm


def interval_display(pair):
    return [float(pair[0]), float(pair[1])]


def entropy_certificate():
    # V_AM=[[160 I, sqrt(25536) Z], [sqrt(25536) Z, 160 I]],
    # and B is the independent one-mode thermal state of mean photon number 1.
    gn = g_interval(F(15, 2))
    gm = g_interval(F(319, 2))
    sa = (2*gn[0]-gm[1], 2*gn[1]-gm[0])
    input_photon_lower = F(2, 125)  # .016
    assert g_interval(input_photon_lower)[1] < sa[0]
    assert sa[0] > 0

    # Exact symplectic eigenvalues of the two-mode retained CM covariance:
    # (sqrt(110217)-317)/8 and (sqrt(110217)+317)/8.
    root_lo = F(331989457663, 10**9)
    root_hi = F(331989457664, 10**9)
    assert root_lo**2 < 110217 < root_hi**2
    vm_hi = (root_hi-317)/8
    vp_hi = (root_hi+317)/8
    gvm = g_interval(vm_hi-F(1,2))
    gvp = g_interval(vp_hi-F(1,2))
    conditional_output_upper = gvm[1]+gvp[1]-gm[0]
    conditional_photon_rhs_lower = g_interval((input_photon_lower+1)/2)[0]
    certified_margin = conditional_photon_rhs_lower-conditional_output_upper
    assert certified_margin > F(269, 10000)  # > .0269 nats

    return {
        "method": "exact rational atanh-series log intervals and rational square-root enclosure",
        "log_series_terms": 90,
        "conditional_input_entropy_interval": interval_display(sa),
        "input_entropy_photon_lower": str(input_photon_lower),
        "root_bounds": [str(root_lo), str(root_hi)],
        "conditional_output_entropy_upper": float(conditional_output_upper),
        "proposed_conditional_EPnI_rhs_lower": float(conditional_photon_rhs_lower),
        "certified_violation_strictly_greater_than": ".0269 nats",
        "certified_margin_lower": float(certified_margin),
        "rational_certificate_assertions_passed": True,
    }


def long_even_cycle_checks():
    """Check nested signs on nonuniform induced cycles; not Fock measurements."""
    import numpy as np

    results = []
    for m in [4, 6, 8, 10]:
        C = .5*np.eye(m, dtype=complex)
        pair_matrices = []
        magnitudes = []
        W = 1.+0j
        for j in range(m):
            nxt = (j+1) % m
            r = .05+.004*j
            z = r*np.exp(.2j*(j+1))
            C[j,nxt] = z
            C[nxt,j] = z.conjugate()
            magnitudes.append(r)
            W *= z
            pair = np.zeros_like(C)
            alpha = -2*np.arctanh(2*r)/r
            pair[j,nxt] = alpha*z
            pair[nxt,j] = alpha*z.conjugate()
            pair_matrices.append(pair)
        # Matrix form of the genuine nested commutator on path 2,...,m.
        D = pair_matrices[m-2]
        for j in range(m-3, 0, -1):
            A = pair_matrices[j]
            D = A@D-D@A
        value = 1j*np.trace(C@(np.eye(m)-C)@D)
        coefficient = np.prod([-2*np.arctanh(2*magnitudes[j])/magnitudes[j] for j in range(1,m-1)])
        predicted = 2*coefficient*W.imag
        assert abs(value-predicted) < 1e-12
        X = C-.5*np.eye(m)
        Xabs = np.abs(X)
        recovered_real = np.prod(magnitudes)+(np.trace(np.linalg.matrix_power(X,m))-np.trace(np.linalg.matrix_power(Xabs,m)))/(2*m)
        assert abs(recovered_real-W.real) < 1e-12
        results.append({"cycle_length":m, "nested_Wick_expression":float(value.real), "predicted":float(predicted), "real_loop_recovery_error":float(abs(recovered_real-W.real))})
    return {"cases":results, "status":"finite one-particle/Wick-formula diagnostics, not additional many-body acquisition"}


def gaussian_fock_checks():
    import numpy as np

    m = 4
    t = .1
    C = .5*np.eye(m, dtype=complex)
    for i,j,z in [(0,1,t), (1,2,t), (2,3,t), (3,0,1j*t)]:
        C[i,j] = z
        C[j,i] = np.conj(z)
    G = np.diag([1,-1,1,-1])
    assert np.linalg.norm(G@C@G-(np.eye(m)-C)) < 1e-14
    assert np.linalg.eigvalsh(C)[0] > .3

    def k_matrix(cov):
        vals, vecs = np.linalg.eigh(cov)
        return (vecs*np.log((1-vals)/vals))@vecs.conj().T

    regions = []
    embedded = []
    spectrum_error = 0.
    for mask in range(1, 1 << m):
        ids = [i for i in range(m) if mask & (1 << i)]
        cov = C[np.ix_(ids,ids)]
        local = k_matrix(cov)
        k = np.zeros_like(C)
        k[np.ix_(ids,ids)] = local
        regions.append(ids)
        embedded.append(k)
        spectrum_error = max(spectrum_error, float(np.max(np.abs(np.linalg.eigvalsh(cov)-np.linalg.eigvalsh(cov.conj())))))
    modular_J_error = max(abs(1j*np.trace(C@(a@b-b@a))) for a in embedded for b in embedded)

    def pair(i,j):
        cov = C[np.ix_([i,j],[i,j])]
        k = np.zeros_like(C)
        k[np.ix_([i,j],[i,j])] = k_matrix(cov)
        return k

    A = pair(0,1)
    B = pair(1,2)
    E = pair(2,3)
    D = B@E-E@B
    jordan = 1j*np.trace(C@(A@D+D@A))
    W = C[0,1]*C[1,2]*C[2,3]*C[3,0]
    alpha = -2*np.arctanh(2*t)/t
    predicted = -2*alpha**3*np.imag(W)
    assert abs(jordan-predicted) < 1e-12

    I2 = np.eye(2)
    Z = np.diag([1,-1])
    lower = np.array([[0,1],[0,0]])
    pauli_X = np.array([[0,1],[1,0]])
    def tensor(items):
        out = np.array([[1.]])
        for item in items:
            out = np.kron(out,item)
        return out
    c = [tensor([Z if j<i else lower if j==i else I2 for j in range(m)]) for i in range(m)]
    def Q(matrix):
        out = np.zeros((1<<m,1<<m), dtype=complex)
        for i in range(m):
            for j in range(m):
                out += matrix[i,j] * c[i].conj().T@c[j]
        return out
    h = k_matrix(C)
    energy, vectors = np.linalg.eigh(Q(h))
    rho = (vectors*np.exp(-energy))@vectors.conj().T
    rho /= np.trace(rho)
    U = tensor([pauli_X]*m)
    density_conjugation_error = float(np.linalg.norm(U@rho@U.conj().T-rho.conj()))
    measured_C = np.array([[np.trace(rho@c[j].conj().T@c[i]) for j in range(m)] for i in range(m)])
    assert np.linalg.norm(measured_C-C) < 1e-12
    QA,QD = Q(A),Q(D)
    raw = 1j*np.trace(rho@(QA@QD+QD@QA))
    wick = 2j*np.trace(C@A@C@D)
    number = sum((op.conj().T@op for op in c), np.zeros_like(rho))
    charge_weighted = 1j*np.trace(rho@(number-2*np.eye(1<<m))@QD)
    charge_predicted = 2*alpha**2*np.imag(W)
    assert abs(charge_weighted-charge_predicted) < 1e-12
    # Recover the real part from the labelled four-site covariance spectrum.
    Xcov = C-.5*np.eye(m)
    loop_real_from_spectrum = (np.trace(np.linalg.matrix_power(Xcov,4))-24*t**4)/8
    assert abs(loop_real_from_spectrum-W.real) < 1e-12
    assert abs(raw) < 1e-12
    assert abs(raw+wick-jordan) < 1e-12
    assert density_conjugation_error < 1e-12

    return {
        "dimension": m,
        "fock_dimension": 1<<m,
        "flux_loop_product": [float(W.real), float(W.imag)],
        "covariance_eigenvalues": np.linalg.eigvalsh(C).tolist(),
        "all_nonempty_regions_checked": len(regions),
        "all_ordered_CAR_modular_pairs_checked": len(regions)**2,
        "max_covariance_spectrum_conjugation_error": spectrum_error,
        "max_modular_J_absolute": float(modular_J_error),
        "one_particle_Jordan_Lie": [float(jordan.real), float(jordan.imag)],
        "predicted_one_particle_Jordan_Lie": float(predicted),
        "genuine_many_body_anticommutator": [float(raw.real), float(raw.imag)],
        "separately_needed_Wick_term": [float(wick.real), float(wick.imag)],
        "genuine_charge_weighted_commutator": [float(charge_weighted.real), float(charge_weighted.imag)],
        "predicted_charge_weighted_commutator": float(charge_predicted),
        "loop_real_from_spectrum": [float(loop_real_from_spectrum.real), float(loop_real_from_spectrum.imag)],
        "max_density_conjugation_error": density_conjugation_error,
        "status": "finite floating-point diagnostics; general proof is analytical",
    }


if __name__ == "__main__":
    result = {"entropy_certificate": entropy_certificate(), "modular_checks": gaussian_fock_checks(), "long_even_cycle_checks":long_even_cycle_checks()}
    output = Path(__file__).with_name("check_results.json")
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
