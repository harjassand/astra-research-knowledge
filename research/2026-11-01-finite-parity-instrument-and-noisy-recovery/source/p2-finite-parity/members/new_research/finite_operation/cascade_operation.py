"""Exact conditional-coherent finite-duration parity operation.

Two data qubits, source b, and unidirectional corrector c. All oscillators
and Markov inputs start in vacuum. No Fock truncation is used for the main
calculation. Units hbar=1; frequency scale kappa_e=1 unless overridden.

Real u(t), A=Z1+Z2:
  x' = -(ke+kb)x/2 - i u
  y_q' = -[(ks+ki)/2+i chi q]y_q - sqrt(ke ks)x.
Data branch source/corrector amplitudes are A x and A y_q.
Main output is A(sqrt(ke)x+sqrt(ks)y_q); bypass A sqrt(kb)x;
corrector internal output A sqrt(ki)y_q.

The sine-basis pulse is chosen in the exact three-real-dimensional terminal
nullspace x(T)=y_+(T)=0 and scaled to a specified homodyne assignment error.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from scipy.linalg import eigh, null_space
from scipy.integrate import simpson
from scipy.special import ndtri


@dataclass
class Model:
    T: float = 8.0
    ke: float = 1.0
    kb: float = 0.0
    ks: float = 10.0
    ki: float = 0.0
    chi: float | None = None
    eta: float = 0.5
    modes: int = 8
    assignment_error: float = 1e-3

    def __post_init__(self):
        if self.chi is None:
            # Zero-frequency logical leakage in the main output vanishes
            # even with ki>0 when ks>ki. Internal loss is still charged.
            self.chi = 0.5 * np.sqrt(max(0.0, self.ks**2-self.ki**2))


def convolution(a, omega, t):
    """Integral_0^t exp[-a(t-s)] sin(omega s) ds."""
    return (a*np.sin(omega*t)-omega*np.cos(omega*t)+omega*np.exp(-a*t))/(a*a+omega*omega)


def basis(model: Model, t):
    t = np.asarray(t)[..., None]
    omega = np.arange(1, model.modes+1)[None, :]*np.pi/model.T
    ae = (model.ke+model.kb)/2
    ac = (model.ks+model.ki)/2+1j*model.chi
    fa = convolution(ae, omega, t)
    fc = convolution(ac, omega, t)
    x = -1j*fa
    y = 1j*np.sqrt(model.ke*model.ks)*(fa-fc)/(ac-ae)
    u = np.sin(omega*t)
    du = omega*np.cos(omega*t)
    dx = -ae*x-1j*u
    ddx = -ae*dx-1j*du
    return {
        "u": u, "x": x, "y": y, "ddx": ddx,
        "main": 2*(np.sqrt(model.ke)*x+np.sqrt(model.ks)*y),
        "bypass": 2*np.sqrt(model.kb)*x,
        "internal": 2*np.sqrt(model.ki)*y,
    }


def gram(v, t):
    return simpson(v[:, :, None]*v[:, None, :], x=t, axis=0)


def solve(model: Model, samples=12001):
    t = np.linspace(0.0, model.T, samples)
    B = basis(model, t)
    E = np.stack([B["x"][-1].imag, B["y"][-1].real, B["y"][-1].imag])
    N = null_space(E, rcond=1e-12)
    H = gram(B["main"].real, t)
    Vmain = gram(B["main"].imag, t)
    Vi = gram(B["internal"].imag, t)
    Vb = gram(B["bypass"].imag, t)
    cost = (1-model.eta)*Vmain+Vi+Vb
    vals, vecs = eigh(N.T@cost@N, N.T@H@N)
    c = N@vecs[:, 0]
    target_H = ndtri(model.assignment_error)**2/model.eta
    c *= np.sqrt(target_H/(c@H@c))
    if np.max(B["u"]@c) < -np.min(B["u"]@c):
        c *= -1
    out = {key: value@c for key, value in B.items()}
    integrate = lambda v: float(simpson(v, x=t))
    ports = {}
    for key in ("main", "bypass", "internal"):
        h, v = out[key].real, out[key].imag
        ports[key] = {"H": integrate(h*h), "V": integrate(v*v), "C": integrate(h*v)}
    D = (1-model.eta)*ports["main"]["V"]+ports["bypass"]["V"]+ports["internal"]["V"]
    residual_modes = 4*(abs(out["x"][-1])**2+abs(out["y"][-1])**2)
    result = {
        "model": asdict(model), "sine_coefficients": c.tolist(),
        "constraint_singular_values": np.linalg.svd(E, compute_uv=False).tolist(),
        "constraint_nullity": N.shape[1],
        "terminal_source_amplitude_abs_bright": float(2*abs(out["x"][-1])),
        "terminal_corrector_amplitude_abs_bright": float(2*abs(out["y"][-1])),
        "terminal_bright_photons": float(residual_modes),
        "ports": ports,
        "dephasing_exponent_half_D": D,
        "even_coherence_after_full_record_feedback": float(np.exp(-2*D)),
        "even_phase_flip_probability": float(-np.expm1(-2*D)/2),
        "peak_force_u": float(np.max(abs(out["u"]))),
        "peak_source_photons_bright": float(np.max(4*abs(out["x"])**2)),
        "peak_corrector_photons_bright": float(np.max(4*abs(out["y"])**2)),
        "source_photon_exposure_bright": integrate(4*abs(out["x"])**2),
        "corrector_photon_exposure_bright": integrate(4*abs(out["y"])**2),
        "source_main_emitted_photons_bright": integrate(4*model.ke*abs(out["x"])**2),
        "fourth_moment_V_bound_lossless_only": 16*model.ke/model.ks**4*integrate(abs(out["ddx"])**2),
        "measured_homodyne_separation_sigma": float(2*np.sqrt(model.eta*ports["main"]["H"])),
    }
    return result, t, out


def continuous_instrument_gram(result, reported_even: bool):
    """Schur multiplier for the binned full two-qubit instrument.

    Ordering ++,+-,-+,--. We apply the record-dependent local Z correction,
    but do not apply an optional deterministic local phase to remove the
    unobserved even-sector C phase. Main output record is entire homodyne
    record; only its h statistic decides the report. Its v statistic is
    retained for the correction, which is why this is a complete instrument.
    """
    from scipy.special import ndtr
    eta = result["model"]["eta"]
    H = result["ports"]["main"]["H"]
    e = np.array([1.0, 0.0, 0.0, 1.0])
    q = np.array([1.0, 0.0, 0.0, -1.0])
    M = np.zeros((4,4), dtype=complex)
    for i in range(4):
        for j in range(4):
            # Real overlap of the collected coherent quadrature wavefunctions.
            bh = np.exp(-eta*(e[i]-e[j])**2*H/2)
            # Under their normalized product, matched statistic is N(mean,1).
            z = (e[i]+e[j]-1)*np.sqrt(eta*H)
            region = ndtr(z if reported_even else -z)
            exponent = 0j
            for name, factor in (("main",1-eta),("bypass",1),("internal",1)):
                P = result["ports"][name]
                exponent += factor*(-0.5*((e[i]-e[j])**2*P["H"]+(q[i]-q[j])**2*P["V"])
                                    +1j*(e[j]*q[i]-q[j]*e[i])*P["C"])
            M[i,j] = bh*region*np.exp(exponent)
    return M


def checks(result):
    p = result["ports"]
    M0, M1 = [continuous_instrument_gram(result,b) for b in (False,True)]
    d = result["model"]
    return {
        "instrument_min_eigenvalue_even": float(np.linalg.eigvalsh(M1).min()),
        "instrument_min_eigenvalue_odd": float(np.linalg.eigvalsh(M0).min()),
        "instrument_trace_preservation_error": float(np.max(abs(np.diag(M0+M1)-1))),
        "passive_corrector_energy_balance_error": abs(p["main"]["H"]+p["main"]["V"]+p["internal"]["H"]+p["internal"]["V"]-result["source_main_emitted_photons_bright"]),
        "main_assignment_even": float(1-M1[0,0].real),
        "main_assignment_odd": float(1-M0[1,1].real),
        "finite_moment_bound_holds_lossless": (p["main"]["V"] <= result["fourth_moment_V_bound_lossless_only"]*(1+1e-7)) if d["ki"]==0 and d["kb"]==0 else None,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",default=str(Path(__file__).with_name("cascade_results.json")))
    args = parser.parse_args()
    results = []
    for T in (2,4,8,16,32):
        for loss in (0.0,1e-5,1e-4,1e-3):
            m = Model(T=T,kb=loss,ki=10*loss)
            r,_,_ = solve(m)
            r["checks"] = checks(r)
            results.append(r)
    Path(args.output).write_text(json.dumps({"cases":results},indent=2))
    for r in results:
        d=r["model"]
        print(f"T={d['T']:>4}, loss={d['kb']:.0e}: pZeven={r['even_phase_flip_probability']:.8g}, "
              f"upeak={r['peak_force_u']:.5g}, nsource={r['peak_source_photons_bright']:.5g}, "
              f"ncorr={r['peak_corrector_photons_bright']:.5g}, "
              f"V={r['ports']['main']['V']:.5g}, residual={r['terminal_bright_photons']:.3g}")


if __name__=="__main__":
    main()
