"""Exact finite-dimensional checks of the Hubbard capture/return construction.

These checks expose algebraic mistakes and test noncommuting source examples.
They do not replace the source-uniform analytic bounds in the companion note,
and are not a simulated or measured semiconductor device window.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad


OUT = Path(__file__).resolve().parent
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)


def annihilator(mode: int, modes: int = 4) -> np.ndarray:
    out = np.zeros((2**modes, 2**modes), complex)
    for state in range(2**modes):
        if state & (1 << mode):
            sign = (-1) ** ((state & ((1 << mode) - 1)).bit_count())
            out[state ^ (1 << mode), state] = sign
    return out


def fermion_check() -> dict:
    # Mode order: L up, L down, R up, R down.
    a = [annihilator(i) for i in range(4)]
    vac = np.eye(16, dtype=complex)[:, 0]
    pair = lambda i, j: a[i].conj().T @ a[j].conj().T @ vac
    t_plus = pair(0, 2)
    t_zero = (pair(0, 3) + pair(1, 2)) / np.sqrt(2)
    t_minus = pair(1, 3)
    singlet = (pair(0, 3) - pair(1, 2)) / np.sqrt(2)
    dl, dr = pair(0, 1), pair(2, 3)
    basis = np.column_stack([t_plus, t_zero, t_minus, singlet, dl, dr])
    hop = sum(a[i + 2].conj().T @ a[i] + a[i].conj().T @ a[i + 2]
              for i in range(2))
    reduced = basis.conj().T @ hop @ basis
    expected = np.zeros((6, 6), complex)
    expected[3, 4] = expected[4, 3] = np.sqrt(2)
    expected[3, 5] = expected[5, 3] = np.sqrt(2)
    assert np.linalg.norm(reduced - expected) < 1e-13
    return {
        "basis_orthogonality_error": float(np.linalg.norm(basis.conj().T @ basis - np.eye(6))),
        "hopping_reduction_error": float(np.linalg.norm(reduced - expected)),
        "triplet_hopping_norm": float(np.linalg.norm(reduced[:3, :])),
        "singlet_hopping_matrix": reduced[3:, 3:].real.tolist(),
    }


def singlet_hamiltonian(source_h, gain, selected, other_detuning, d=0.0):
    # Charge order is S(1,1), D_L, D_R. Exact retention of both double states.
    h = np.kron(np.eye(3), source_h).astype(complex)
    other = 3 - selected
    h[2 * other:2 * other + 2, 2 * other:2 * other + 2] += other_detuning * I2
    for j in [1, 2]:
        h[:2, 2 * j:2 * j + 2] += np.sqrt(2) * gain
        h[2 * j:2 * j + 2, :2] += np.sqrt(2) * gain
    if d:
        h[2:4, 2:4] += d * X
        h[4:6, 4:6] += d * Z
    return h


def block(u, final, initial):
    return u[2 * final:2 * final + 2, 2 * initial:2 * initial + 2]


def exact_pulse_checks() -> dict:
    g, h, d = 0.6, 1.4, 0.2
    gain = (g + h) / 2 * I2 + (h - g) / 2 * Z
    norm_bound = 2 * h + d
    tau = g / norm_bound**2
    r_bound = (np.sqrt(2) - 0.5)**2 * (g / norm_bound)**4
    rows = []
    for omega in [0, .5, 5, 50, 500, 5000]:
        source_h = omega * X + .37 * Y
        for charge_gap in [0, 1, 10, 100, 1000]:
            for selected in [1, 2]:
                u = expm(-1j * tau * singlet_hamiltonian(source_h, gain, selected, charge_gap, d))
                p_capture = np.linalg.svd(block(u, selected, 0), compute_uv=False)[-1]**2
                p_return = np.linalg.svd(block(u, 0, selected), compute_uv=False)[-1]**2
                assert min(p_capture, p_return) + 1e-11 >= r_bound
                rows.append({"omega": omega, "other_scalar_charge_gap": charge_gap,
                             "selected_double": selected, "min_capture_probability": float(p_capture),
                             "min_return_probability": float(p_return)})

    # Piecewise rapidly changing source, gain axes, and residual charge shifts.
    # No numerical derivative or source adiabatic assumption is used.
    rng = np.random.default_rng(82105)
    random_rows = []
    for trial in range(24):
        selected = 1 + trial % 2
        charge_gap = 1000 if trial % 3 == 0 else 7
        u = np.eye(6, dtype=complex)
        for k in range(17):
            axis = rng.normal(size=3)
            axis /= np.linalg.norm(axis)
            gain_k = (g+h)/2 * I2 + (h-g)/2 * (axis[0]*X+axis[1]*Y+axis[2]*Z)
            source_axis = rng.normal(size=3)
            source_h = (1 + 10**(trial % 5)) * sum(v*p for v, p in zip(source_axis, [X,Y,Z]))
            hk = singlet_hamiltonian(source_h, gain_k, selected, charge_gap, d)
            u = expm(-1j*tau/17*hk) @ u
        p1 = np.linalg.svd(block(u, selected, 0), compute_uv=False)[-1]**2
        p2 = np.linalg.svd(block(u, 0, selected), compute_uv=False)[-1]**2
        assert min(p1, p2) + 1e-11 >= r_bound
        random_rows.append(float(min(p1, p2)))
    return {"g": g, "h": h, "d": d, "tau": tau, "uniform_probability_bound": float(r_bound),
            "constant_source_cases": rows,
            "piecewise_source_minimum_probabilities": random_rows,
            "smallest_observed_probability": min([min(x["min_capture_probability"], x["min_return_probability"]) for x in rows] + random_rows)}


def failure_tail_checks() -> dict:
    # An illustrative active source, with no source reset between attempts.
    g, h, d = .6, 1.4, .2
    gain = I2 + .4 * Z
    hs = 23.0 * X + .37 * Y
    tau = g / (2*h+d)**2
    r = (np.sqrt(2)-.5)**2 * (g/(2*h+d))**4
    # During each charge readout the source can continue to rotate.
    source_read = expm(-1j*(.731*X + 2.13*Z))
    pulse = {j: np.kron(np.eye(3), source_read) @ expm(-1j*tau*singlet_hamiltonian(hs, gain, j, 31., d)) for j in [1,2]}
    k00 = block(pulse[2], 0, 0)
    k_power = np.eye(2, dtype=complex)
    effects = {1: I2.copy(), 2: I2.copy()}
    rows = []
    for n in range(1, 501):
        k_power = k00 @ k_power
        effects = {j: sum(block(pulse[j], k, j).conj().T @ effects[k] @ block(pulse[j], k, j) for k in [1,2]) for j in [1,2]}
        if n in [1,2,5,10,50,100,500]:
            cap = float(np.linalg.norm(k_power, 2)**2)
            ret = max(float(np.linalg.eigvalsh(effects[j])[-1]) for j in [1,2])
            bound = float((1-r)**n)
            assert cap <= bound+1e-10 and ret <= bound+1e-10
            rows.append({"attempts":n, "worst_source_capture_failure":cap,
                         "worst_source_return_failure":ret, "uniform_geometric_bound":bound})
    return {"source_reset":False, "rows":rows}


def pair_projector(i, j):
    # Three distinguishable spin positions; exchange projects onto singlet.
    swap = np.zeros((8,8), complex)
    for x in range(8):
        bits = [(x>>(2-k)) & 1 for k in range(3)]
        bits[i],bits[j]=bits[j],bits[i]
        y=sum(b<<(2-k) for k,b in enumerate(bits))
        swap[y,x]=1
    return (np.eye(8)-swap)/2


def teleportation_checks() -> dict:
    p12, p23 = pair_projector(0,1), pair_projector(1,2)
    q12,q23=np.eye(8)-p12,np.eye(8)-p23
    singlet=np.array([0,1,-1,0],complex)/np.sqrt(2)
    v=np.column_stack([np.kron(I2[:,j],singlet) for j in [0,1]])
    w=np.column_stack([np.kron(singlet,I2[:,j]) for j in [0,1]])
    first=w.conj().T@p12@v
    relation_error=np.linalg.norm(p12@p23@p12-p12/4)
    assert relation_error < 1e-13
    assert np.linalg.norm(first + I2/2) < 1e-13
    f=q12@v/np.sqrt(.75)
    probabilities=[]
    for a in [p23,q23]:
        z=a@f
        branch=float(np.trace(z.conj().T@z).real/2)
        succeed=p12@z
        success_given_branch=float(np.trace(succeed.conj().T@succeed).real/2/branch)
        transfer=w.conj().T@succeed
        scalar=np.trace(transfer)/2
        assert np.linalg.norm(transfer-scalar*I2) < 1e-13
        probabilities.append({"intermediate_outcome": "S" if a is p23 else "T", "probability":branch,
                              "subsequent_success_probability":success_given_branch})
    next_success=sum(x["probability"]*x["subsequent_success_probability"] for x in probabilities)
    assert abs(next_success-3/8)<1e-13
    return {"recoupling_identity_error":float(relation_error),
            "first_transfer_coefficient":float(first[0,0].real),
            "after_first_failure":probabilities,
            "subsequent_attempt_success":next_success,
            "expected_STP_calls":1+2*(3/4)/(3/8),
            "tail_after_K_attempts":"(3/4)*(5/8)**(K-1), K>=1"}


def dark_charge_counterexample() -> dict:
    g=np.eye(2)
    h=singlet_hamiltonian(np.zeros((2,2)),g,1,0)
    dark=np.kron(np.array([0,1,-1])/np.sqrt(2),np.array([1,0]))
    assert np.linalg.norm(h@dark)<1e-13
    # A fully charge-resolving measurement of D_L has 1/2 overlap with D_-.
    return {"symmetric_D_minus_hopping_norm":float(np.linalg.norm(h@dark)),
            "D_left_dark_charge_weight":.5,
            "consequence":"A two-level S-D_plus return proof cannot be reused after a detector has resolved D_left versus D_right."}


def loading_check() -> dict:
    c = [annihilator(i, modes=2) for i in range(2)]
    n = [a.conj().T @ a for a in c]
    hs = np.kron(np.eye(4), 19*X) + np.kron(n[0]+n[1], .7*Z) + np.kron(3*n[0]@n[1], I2)
    jin = [np.kron(a.conj().T, I2) for a in c]
    jout = [np.kron(a, I2) for a in c]
    def adjoint(o, jumps):
        out = 1j*(hs@o-o@hs)
        for jump in jumps:
            effect = jump.conj().T@jump
            out += jump.conj().T@o@jump - (effect@o+o@effect)/2
        return out
    holes = [np.kron(np.eye(4)-b, I2) for b in n]
    errors = [float(np.linalg.norm(adjoint(h, jin)+h)) for h in holes]
    number = np.kron(n[0]+n[1], I2)
    drain_error = float(np.linalg.norm(adjoint(number, jout)+number))
    assert max(errors+[drain_error]) < 1e-13
    return {"hole_decay_adjoint_errors":errors, "emptying_number_decay_error":drain_error,
            "uniform_loading_failure_bound":"2*exp(-kappa_in*t)",
            "scope":"Single orbital, spin-independent charge-diagonal source shifts, full two-spin injection; no reservoir bandwidth qualification inferred."}


def coulomb_projection_check() -> dict:
    sigma,a=1.,1.5
    s=np.exp(-a*a/(sigma*sigma))
    normal=1/(np.sqrt(np.pi)*sigma)
    mean=lambda y,center: quad(lambda x: normal*np.exp(-(x-center)**2/sigma**2)/np.sqrt(x*x+y*y),-np.inf,np.inf,epsabs=1e-13)[0]
    rows=[]
    for y in [1.,2.,3.,10.,30.]:
        central,well=mean(y,0),mean(y,a)
        b=s*(central-well)/(1-s*s)
        asym=s*a*a/(2*(1-s*s)*y**3)
        assert b>0
        rows.append({"source_distance":y,"common_diagonal_raw_average":well,
                     "orthogonalized_hopping_matrix_element":b,
                     "leading_far_source_curvature_term":asym})
    assert abs(rows[-1]["orthogonalized_hopping_matrix_element"]/rows[-1]["leading_far_source_curvature_term"]-1)<.01
    return {"gaussian_width":sigma,"half_well_separation":a,"overlap":float(s),
            "constant_potential_hopping_matrix_element":0.,"source_distance_rows":rows,
            "scope":"Projected Coulomb matrix element after exact symmetric orthogonalization; no double-well spectral qualification inferred."}


if __name__ == "__main__":
    report={"fermionic_algebra":fermion_check(),"pulse_bounds":exact_pulse_checks(),
            "actual_history_tails":failure_tail_checks(),"forced_teleportation":teleportation_checks(),
            "dark_charge_counterexample":dark_charge_counterexample(),"offline_singlet_loading":loading_check(),
            "electrostatic_common_hopping":coulomb_projection_check()}
    path=OUT/"hubbard_cycle_results.json"
    path.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"output":str(path),"fermionic_reduction_error":report["fermionic_algebra"]["hopping_reduction_error"],
                      "uniform_pulse_bound":report["pulse_bounds"]["uniform_probability_bound"],
                      "smallest_observed_probability":report["pulse_bounds"]["smallest_observed_probability"],
                      "routing_expected_STP_calls":report["forced_teleportation"]["expected_STP_calls"]},indent=2))
