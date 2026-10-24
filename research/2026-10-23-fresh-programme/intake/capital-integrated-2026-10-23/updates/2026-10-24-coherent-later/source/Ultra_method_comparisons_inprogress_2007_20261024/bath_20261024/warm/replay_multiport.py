#!/usr/bin/env python3
"""Scientific replay for the warm arm's declared two-native-port model.

No experimental parameter inference.  Numpy only; no scipy.  Exact Fraction
identities, passive-collector algebra, and independent output-kernel integration
are retained.  The finite numerical example is a supplied dimensionless model.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path

import numpy as np


def integrate(y: np.ndarray, dt: float) -> np.ndarray:
    assert (len(y) - 1) % 2 == 0
    weights = np.ones(len(y))
    weights[1:-1:2] = 4
    weights[2:-1:2] = 2
    return np.tensordot(weights, y, axes=(0, 0)) * dt / 3


def exact_mode_data() -> dict:
    # z=d+i d' on [0,2pi], d=5/16-9cos(2t)/16+cos(3t)/4.
    # z(t)=sum c_k exp(ikt), so Parseval norms are 2pi sum k^(2j)c_k^2.
    coeff = {0: F(5, 16), 2: F(9, 32), -2: F(-27, 32),
             3: F(-1, 4), -3: F(1, 2)}
    norms = {j: 2 * sum((F(k) ** (2*j)) * c*c for k, c in coeff.items())
             for j in range(5)}
    endpoint = {j: sum(((1j*k) ** j) * float(c) for k, c in coeff.items())
                for j in range(4)}
    assert norms[0] == F(615, 256)
    assert norms[1] == F(765, 64)
    assert norms[1] / norms[0] == F(204, 41)
    assert all(abs(endpoint[j]) < 1e-12 for j in range(3))
    assert abs(endpoint[3] - 1j*45/4) < 1e-12
    # Four integrations by parts: both endpoint third derivatives plus ||z''''||_1.
    c4 = 45/2 + 2*math.pi*math.sqrt(float(norms[4])/2)
    tail_constant = c4*c4/(7*math.pi*(math.pi*float(norms[0])))
    return {
        "fourier_coefficients": {str(k): str(c) for k, c in coeff.items()},
        "norms_over_pi": {str(j): str(n) for j, n in norms.items()},
        "normalized_derivative_energy": str(norms[1]/norms[0]),
        "fourth_IBP_constant": c4,
        "relative_hard_band_tail_upper_bound": f"min(1,{tail_constant:.12g}/B**7)",
    }


def collector(gammas: np.ndarray, taps: np.ndarray) -> dict:
    c = np.sqrt(gammas)
    if np.any((gammas > 0) & (taps <= 0)):
        return {"full_bright_recoverable": False}
    h = np.sqrt(gammas/taps)
    h /= np.linalg.norm(h)
    eta = float(gammas.sum()/np.sum(gammas/taps))
    target = math.sqrt(eta) * c / np.linalg.norm(c)
    assert np.max(np.abs(h*np.sqrt(taps)-target)) < 1e-14
    vac = float(np.sum(h*h*(1-taps)))
    assert abs(vac-(1-eta)) < 1e-14
    return {"full_bright_recoverable": True, "hybrid_amplitudes": h.tolist(),
            "eta_spatial": eta, "vacuum_amplitude_squared": vac}


def u_derivative(t: np.ndarray, order: int) -> np.ndarray:
    # omega=1,u0=1.  Coefficients of sin^6(t/2).
    ans = np.zeros_like(t)
    if order == 0:
        ans += 5/16
    for k, c in [(1, -15/32), (2, 3/16), (3, -1/32)]:
        ans += c * k**order * np.cos(k*t + order*math.pi/2)
    return ans


def pulse(grid: np.ndarray, gamma: float, kappa: float) -> dict:
    uu = [u_derivative(grid, k) for k in range(6)]
    w2 = 1+gamma*gamma/4
    d = uu[2] + gamma*uu[1] + w2*uu[0]
    dp = uu[3] + gamma*uu[2] + w2*uu[1]
    dpp = uu[4] + gamma*uu[3] + w2*uu[2]
    e, ep = -kappa*uu[0], -kappa*uu[1]
    force = (uu[4] + 2*gamma*uu[3] + (2+1.5*gamma**2)*uu[2]
             + 2*gamma*w2*uu[1] + (w2*w2-kappa*kappa)*uu[0])
    rd = np.stack((d, dp+gamma*d/2), axis=1)
    re = np.stack((e, ep+gamma*e/2), axis=1)
    rdp = np.stack((dp, dpp+gamma*dp/2), axis=1)
    dt = grid[1]-grid[0]
    raw = float(integrate(force*e, dt))
    fb = float(gamma*integrate(d*ep-dp*e, dt))
    logical = float(-kappa*integrate(d*d-kappa*kappa*uu[0]*uu[0], dt))
    assert abs(raw+fb-logical) < 2e-12
    # Driven positions AND canonical momenta close, not arbitrary-state identity.
    assert np.max(np.abs(np.concatenate((rd[[0, -1]], re[[0, -1]])))) < 1e-12
    return {"rd": rd, "re": re, "force": force, "raw": raw, "fb": fb,
            "logical": logical, "A_self_without_gamma": float(integrate(np.sum(rd*rd, axis=1), dt)),
            "A_cross_without_gamma": float(integrate(np.sum(re*re, axis=1), dt)),
            "derivative_ratio": float(integrate(np.sum(rdp*rdp, axis=1), dt)/integrate(np.sum(rd*rd, axis=1), dt))}


def residual_kernel(rd: np.ndarray, re: np.ndarray, gammas: np.ndarray,
                    captured_row: np.ndarray, gain: float = 1.0) -> np.ndarray:
    """Real quadrature coefficient k with D(w)=exp(i integral k^T dY).

    Captured row h has norm 1.  gain=1 erases its deterministic self vector.
    h=c/||c|| is full bright capture.  h=(1,0) leaves physical port 2 native/hot.
    Output ordering A1(Q,P),A2(Q,P),B1(Q,P),B2(Q,P).
    """
    c = np.sqrt(gammas)
    alpha = np.dot(captured_row, c)
    own = c-gain*alpha*captured_row
    disp = np.zeros((len(rd), 8, 2))
    for j in range(2):
        disp[:, 2*j:2*j+2, 0] = own[j]*rd
        disp[:, 2*j:2*j+2, 1] = c[j]*re
        disp[:, 4+2*j:6+2*j, 0] = c[j]*re
        disp[:, 4+2*j:6+2*j, 1] = own[j]*rd
    kernel = np.empty_like(disp)
    kernel[:, 0::2] = disp[:, 1::2]
    kernel[:, 1::2] = -disp[:, 0::2]
    return kernel


def actual_output_G(grid: np.ndarray, kernel: np.ndarray, gamma: float,
                    kappa: float, gammas: np.ndarray, occupancies: np.ndarray,
                    mechanical_variance: float) -> np.ndarray:
    """Actual OUTPUT characteristic using backward adjoint kernel; no Vout=vI shortcut."""
    A = np.array([[-gamma/2, 1, 0, 0], [-1, -gamma/2, -kappa, 0],
                  [0, 0, -gamma/2, 1], [-kappa, 0, -1, -gamma/2]])
    C = np.zeros((4, 8))
    for j, g in enumerate(gammas):
        C[:2, 2*j:2*j+2] = math.sqrt(g)*np.eye(2)
        C[2:, 4+2*j:6+2*j] = math.sqrt(g)*np.eye(2)
    assert np.max(np.abs(C@C.T-gamma*np.eye(4))) < 1e-15
    ngrid = len(grid)-1
    dt = grid[1]-grid[0]
    adjoint = np.zeros((ngrid+1, 4, 2))
    # J'(s)=-C k(s)-A^T J(s), J(T)=0; step backward by RK4.
    for j in range(ngrid, 0, -1):
        cur, step = adjoint[j], -dt
        k0, k1 = kernel[j], kernel[j-1]
        km = (k0+k1)/2
        def rhs(x: np.ndarray, k: np.ndarray) -> np.ndarray:
            return -C@k-A.T@x
        z1 = rhs(cur, k0)
        z2 = rhs(cur+step*z1/2, km)
        z3 = rhs(cur+step*z2/2, km)
        z4 = rhs(cur+step*z3, k1)
        adjoint[j-1] = cur+step*(z1+2*z2+2*z3+z4)/6
    b = kernel-np.einsum('ij,tjk->tik', C.T, adjoint)
    vfield = np.repeat(np.tile(occupancies+0.5, 2), 2)
    out = mechanical_variance*(adjoint[0].T@adjoint[0])
    out += integrate(np.einsum('tia,i,tib->tab', b, vfield, b), dt)
    out = (out+out.T)/2
    assert np.linalg.eigvalsh(out).min() > -1e-10
    return out


def spin_metrics(theta: float, G: np.ndarray) -> dict:
    spins = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]])
    rho = np.empty((4, 4), complex)
    for a, s in enumerate(spins):
        for b, z in enumerate(spins):
            delta = s-z
            rho[a, b] = np.exp(1j*theta*(np.prod(s)-np.prod(z))
                               -0.5*(delta@G@delta))/4
    pt = rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)
    vals = np.linalg.eigvalsh(pt)
    target = np.exp(1j*theta*np.prod(spins, axis=1))/2
    return {"G": G.tolist(), "single_flip_exponents": (2*np.diag(G)).tolist(),
            "PT_eigenvalues": vals.tolist(), "negativity": float(-vals[vals<0].sum()),
            "fidelity_to_same_phase_pure_state": float(np.real(target.conj()@rho@target)),
            "rho_min_eigenvalue": float(np.linalg.eigvalsh(rho).min())}


def example(n: int) -> dict:
    grid = np.linspace(0, 2*math.pi, n+1)
    dt = grid[1]-grid[0]
    gamma, kappa = 1e-4, 1e-2
    gammas = gamma*np.array([0.6, 0.4])
    ns = np.array([1000.0, 500.0])
    taps = np.array([0.6, 0.2])
    eta_detector, bandwidth = 0.9, 5.0
    p = pulse(grid, gamma, kappa)
    col = collector(gammas, taps)
    eta_bw = 1/(1+p["derivative_ratio"]/bandwidth**2)
    eta = col["eta_spatial"]*eta_bw*eta_detector
    w = (1-eta)/(2*eta)
    amplitude_squared = (math.pi/4)/abs(p["logical"])
    theta = p["logical"]*amplitude_squared
    A = gamma*p["A_self_without_gamma"]
    bright = np.sqrt(gammas/gamma)
    k_full = residual_kernel(p["rd"], p["re"], gammas, bright)
    Gcross = actual_output_G(grid, k_full, gamma, kappa, gammas, ns, 1000.5)
    Gfull = (Gcross+w*A*np.eye(2))*amplitude_squared
    one_row = np.array([1.0, 0.0])
    k_one = residual_kernel(p["rd"], p["re"], gammas, one_row)
    theta_one = (p["raw"]+0.6*p["fb"])*amplitude_squared
    # Port 1 alone is perfectly homodyned.  This generously gives it no extra detector floor.
    Gone = actual_output_G(grid, k_one, gamma, kappa, gammas, ns, 1000.5)*amplitude_squared
    k_none = residual_kernel(p["rd"], p["re"], gammas, bright, gain=0)
    Gnone = actual_output_G(grid, k_none, gamma, kappa, gammas, ns, 1000.5)*amplitude_squared
    # Matched cold-input comparator: same actual damping, supplied vacuum native inputs/mechanics.
    Gcold = actual_output_G(grid, k_none, gamma, kappa, gammas, np.zeros(2), 0.5)*amplitude_squared
    # General symmetric feedback t: explicitly retain its changed coherent phase.
    gains = []
    for t in [0.0, 0.5, 1.0, 1.25]:
        kt = residual_kernel(p["rd"], p["re"], gammas, bright, gain=t)
        Gt = actual_output_G(grid, kt, gamma, kappa, gammas, ns, 1000.5)
        Gt += w*t*t*A*np.eye(2)
        th = (p["raw"]+t*p["fb"])*amplitude_squared
        gains.append({"relative_feedback_gain": t, "theta": th,
                      **spin_metrics(th, Gt*amplitude_squared)})
    return {"supplied_dimensionless_model_only": True, "intervals": n,
            "gamma": gamma, "kappa": kappa, "native_occupancies": ns.tolist(),
            "mechanical_variance": 1000.5, "taps": taps.tolist(),
            "eta_detector": eta_detector, "filter_B_over_omega": bandwidth,
            "collector": col, "eta_bandwidth": eta_bw, "eta_total": eta,
            "feedback_normalized_vacuum_variance": w,
            "u0_squared_for_pi_over_four": amplitude_squared,
            "theta_raw": p["raw"]*amplitude_squared,
            "theta_feedback": p["fb"]*amplitude_squared,
            "theta_total": theta,
            "force_peak": float(np.max(np.abs(p["force"]))*math.sqrt(amplitude_squared)),
            "full_native_hybrid_filtered_homodyne": spin_metrics(theta, Gfull),
            "perfect_port1_only_port2_absent": spin_metrics(theta_one, Gone),
            "hot_no_output_readout": spin_metrics(p["raw"]*amplitude_squared, Gnone),
            "paid_cold_input_and_mechanics_no_output_readout": spin_metrics(p["raw"]*amplitude_squared, Gcold),
            "general_gain_phase_and_noise": gains}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('REPLAY_RESULTS.json'))
    parser.add_argument('--intervals', type=int, default=4096)
    args = parser.parse_args()
    assert args.intervals % 2 == 0
    result = {"exact_temporal_mode": exact_mode_data(), "fine": example(args.intervals),
              "coarse": example(args.intervals//2)}
    fine, coarse = result['fine'], result['coarse']
    convergence = {}
    for case in ['full_native_hybrid_filtered_homodyne', 'perfect_port1_only_port2_absent',
                 'hot_no_output_readout', 'paid_cold_input_and_mechanics_no_output_readout']:
        convergence[case] = float(np.max(np.abs(np.array(fine[case]['G'])-np.array(coarse[case]['G']))))
    result['coarse_fine_max_absolute_G_difference'] = convergence
    assert fine['full_native_hybrid_filtered_homodyne']['negativity'] > 0.3
    assert fine['perfect_port1_only_port2_absent']['negativity'] < 1e-6
    assert max(convergence.values()) < 2e-5
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({"output": str(args.output), "eta_total": fine['eta_total'],
          "negativity": fine['full_native_hybrid_filtered_homodyne']['negativity'],
          "missing_port_negativity": fine['perfect_port1_only_port2_absent']['negativity'],
          "coarse_fine_G_error": convergence}, indent=2))


if __name__ == '__main__':
    main()
