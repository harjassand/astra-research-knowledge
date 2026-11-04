#!/usr/bin/env python3
"""Finite diagnostics for the bounded-component acquisition report.

Run from any directory: python /path/to/verify_bounded_acquisition.py
Writes only the adjacent results.json. These checks are numerical diagnostics,
not asymptotic proofs or interval-certified hardware validation.
"""
from __future__ import annotations

import hashlib
import json
import math
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import mpmath as mp
import numpy as np
import scipy
from scipy.integrate import quad_vec
from scipy.linalg import expm
from scipy.special import eval_laguerre

HERE = Path(__file__).resolve().parent
REPORT = HERE.parent / "Astra_P1_Bounded_Component_Acquisition.tex"
ATOL = 2e-10
MP_DPS = 240
mp.mp.dps = MP_DPS


def require(condition, message):
    if not bool(condition):
        raise AssertionError(message)


def norm2(a):
    return float(np.linalg.norm(a, ord=2))


def mstr(x, digits=32):
    return mp.nstr(x, digits)


def cascade_matrix(n):
    return -0.5 * np.eye(n) - np.tril(np.ones((n, n)), -1)


def laguerre_cascade():
    cases = []
    for n in (1, 2, 4, 7):
        a0 = cascade_matrix(n)
        for x in (0.0, 0.03, 0.5, 2.0, 7.0):
            actual = expm(a0 * x) @ np.ones(n)
            target = np.exp(-x / 2) * np.array(
                [eval_laguerre(j, x) for j in range(n)]
            )
            error = float(np.max(np.abs(actual - target)))
            require(error < ATOL, f"Laguerre identity: N={n}, x={x}, error={error}")
            cases.append({"N": n, "x": x, "max_abs_error": error})
    return {"passed": True, "cases": cases,
            "max_abs_error": max(c["max_abs_error"] for c in cases)}


def finite_vacuum_gram():
    cases = []
    for n in (1, 2, 4, 7):
        a0 = cascade_matrix(n)
        for u in (0.01, 0.7, 2.5):
            def integrand(x):
                v = np.exp(-x / 2) * np.array(
                    [eval_laguerre(j, x) for j in range(n)]
                )
                return np.outer(v, v)
            gram, quad_error = quad_vec(integrand, 0.0, u,
                                        epsabs=1e-12, epsrel=1e-12)
            evolution = expm(a0 * u)
            vacuum = evolution @ evolution.T
            residual = norm2(gram + vacuum - np.eye(n))
            eig = np.linalg.eigvalsh(gram)
            require(residual < ATOL, f"Finite Gram identity: N={n}, U={u}")
            require(eig.min() >= -ATOL and eig.max() <= 1 + ATOL,
                    f"Finite Gram is not a contraction: N={n}, U={u}")
            cases.append({"N": n, "U": u, "operator_norm_residual": residual,
                          "quadrature_error_estimate": float(quad_error),
                          "gram_min_eigenvalue": float(eig.min()),
                          "gram_max_eigenvalue": float(eig.max()),
                          "initial_vacuum_trace": float(np.trace(vacuum))})
    return {"passed": True, "cases": cases,
            "max_operator_norm_residual":
                max(c["operator_norm_residual"] for c in cases)}


def weyl_basis(q):
    shift = np.roll(np.eye(q, dtype=complex), 1, axis=0)
    phase = np.diag(np.exp(2j * np.pi * np.arange(q) / q))
    return [np.linalg.matrix_power(shift, a) @ np.linalg.matrix_power(phase, b)
            for a in range(q) for b in range(q)]


def bell(q):
    return np.eye(q, dtype=complex).reshape(-1) / np.sqrt(q)


def kraus_environment():
    cases = []
    for q in (2, 3):
        ws = weyl_basis(q)
        phi = bell(q)
        phi_density = np.outer(phi, phi.conj())
        for p in (0.0, 0.07, 0.6, 1.0):
            c0 = 1 - p + p / (q * q)
            v = np.zeros((q * q + 1, q * q), dtype=complex)
            v[0, 0] = np.sqrt((1 - p) / c0)
            v[1:, 0] = np.sqrt(p) / (q * np.sqrt(c0)) * phi
            for mu in range(1, q * q):
                v[1:, mu] = ws[mu].conj().reshape(-1) / np.sqrt(q)
            ks = [np.sqrt(c0) * np.eye(q)] + [np.sqrt(p) / q * w for w in ws[1:]]
            transformed = np.einsum("ij,jab->iab", v, np.asarray(ks))
            target = [np.sqrt(1 - p) * np.eye(q, dtype=complex)]
            for a in range(q):
                for b in range(q):
                    k = np.zeros((q, q), dtype=complex)
                    k[a, b] = np.sqrt(p / q)
                    target.append(k)
            iso_error = norm2(v.conj().T @ v - np.eye(q * q))
            kraus_error = max(norm2(a - b) for a, b in zip(transformed, target))
            tp_error = norm2(sum(k.conj().T @ k for k in transformed) - np.eye(q))
            choi = np.zeros((q * q, q * q), dtype=complex)
            for k in transformed:
                vector = np.kron(np.eye(q), k) @ phi
                choi += np.outer(vector, vector.conj())
            target_choi = (1 - p) * phi_density + p * np.eye(q * q) / (q * q)
            choi_error = norm2(choi - target_choi)
            require(max(iso_error, kraus_error, tp_error, choi_error) < ATOL,
                    f"Kraus/reset conversion: q={q}, p={p}")
            require(abs(np.trace(choi) - 1) < ATOL, "Choi state not normalized")
            cases.append({"q": q, "p": p, "isometry_error": iso_error,
                          "kraus_error": kraus_error, "trace_preserving_error": tp_error,
                          "normalized_choi_error": choi_error,
                          "normalized_choi_trace": float(np.trace(choi).real)})
    return {"passed": True, "cases": cases,
            "max_residual": max(max(c[k] for k in
                ("isometry_error", "kraus_error", "trace_preserving_error",
                 "normalized_choi_error")) for c in cases)}


def s2(x):
    return mp.exp(-x) * (1 + x + x*x/2)


def f3(x):
    # Integral representation avoids cancellation at the leading edge.
    return mp.gammainc(3, 0, x) / 2 if x >= 0 else mp.mpf(0)


def actuator_bounds():
    leading = []
    for text in ("1e-8", "1e-5", ".01", ".1", ".5", "1"):
        x = mp.mpf(text)
        lower = mp.exp(-1) * x**3 / 6
        ratio = f3(x) / lower
        require(ratio >= 1, "Three-pole leading-edge lower bound failed")
        leading.append({"Bt": text, "amplitude_to_lower_bound_ratio": mstr(ratio)})
    xs = [mp.mpf(k)/10 for k in range(801)] + [1 + mp.sqrt(3)]
    tail_ratio = max(s2(x) / (2 * mp.exp(-x/2)) for x in xs)
    require(tail_ratio <= 1, "S2(x) <= 2 exp(-x/2) failed")
    integral = mp.quad(lambda x: s2(x)**2, [0, 1, mp.inf])
    integral_error = abs(integral - mp.mpf(33)/16)
    require(integral_error < mp.mpf("1e-100"), "33/16 tail integral failed")
    impulse_mass = mp.quad(lambda x: x*x*mp.exp(-x)/2, [0, 1, mp.inf])
    require(abs(impulse_mass - 1) < mp.mpf("1e-100"), "Impulse DC gain failed")
    finite_commands = []
    for duration in (mp.mpf(".25"), mp.mpf(1), mp.mpf(4), mp.mpf(20)):
        tail_energy = mp.quad(lambda x: (s2(x)-s2(x+duration))**2,
                             [0, 1, mp.inf])
        require(tail_energy <= mp.mpf(33)/16, "Finite-command tail energy bound failed")
        finite_commands.append({"B_t1": mstr(duration),
                                "normalized_tail_energy": mstr(tail_energy)})
    readout = []
    duration = mp.pi/2  # B=Omega0=1; total exchange area pi/2.
    survival_integral = lambda x: mp.exp(-x)*(3+2*x+x*x/2)
    for guard in (mp.mpf(0), mp.mpf(1), mp.mpf(5), mp.mpf(12)):
        area = survival_integral(guard)-survival_integral(guard+duration)
        bound = 4*mp.exp(-guard/2)
        require(area >= 0 and area <= bound, "Readout finite-tail area bound failed")
        readout.append({"B_guard": mstr(guard), "remaining_area": mstr(area),
                        "remaining_area_to_bound_ratio": mstr(area/bound)})
    return {"passed": True, "mp_dps": MP_DPS, "leading_edge_cases": leading,
            "max_S2_to_exponential_bound_ratio": mstr(tail_ratio),
            "tail_energy_integral": mstr(integral, 70),
            "exact_tail_energy_fraction": "33/16",
            "tail_energy_integral_abs_error": mstr(integral_error),
            "impulse_integral": mstr(impulse_mass, 50),
            "finite_command_cases": finite_commands, "readout_tail_cases": readout}


def amplitude_damping_witness():
    phi = bell(2)
    cases = []
    for eta in (0.0, 1e-6, 0.04, 0.3, 0.81, 1.0):
        ks = [np.diag([1, np.sqrt(eta)]),
              np.array([[0, np.sqrt(1-eta)], [0, 0]])]
        rho = np.zeros((4, 4), dtype=complex)
        for k in ks:
            vector = np.kron(np.eye(2), k) @ phi
            rho += np.outer(vector, vector.conj())
        y = 0.5*np.diag([1+np.sqrt(eta), eta+np.sqrt(eta)])
        upper = np.kron(np.eye(2), y)
        slack_min = float(np.linalg.eigvalsh(upper-rho).min())
        fidelity = float(np.vdot(phi, rho @ phi).real)
        claimed = (1+np.sqrt(eta))**2/4
        dual_value = float(np.trace(y)/2)
        reference = np.trace(rho.reshape(2, 2, 2, 2), axis1=1, axis2=3)
        require(abs(np.trace(rho)-1) < ATOL, "Amplitude-damping Choi trace failed")
        require(norm2(reference-np.eye(2)/2) < ATOL, "Reference normalization failed")
        require(slack_min >= -ATOL, "Amplitude-damping positive witness failed")
        require(max(abs(fidelity-claimed), abs(dual_value-claimed)) < ATOL,
                "Amplitude-damping witness normalization factor failed")
        rho2, upper2 = np.kron(rho, rho), np.kron(upper, upper)
        phi2 = np.kron(phi, phi)
        slack2 = float(np.linalg.eigvalsh(upper2-rho2).min())
        f2 = float(np.vdot(phi2, rho2 @ phi2).real)
        require(slack2 >= -ATOL and abs(f2-claimed**2) < ATOL,
                "Two-copy witness diagnostic failed")
        cases.append({"eta": eta, "rho_trace": float(np.trace(rho).real),
                      "slack_min_eigenvalue": slack_min,
                      "identity_recovery_Bell_overlap": fidelity,
                      "Tr_Y_over_2": dual_value, "claimed_optimum": claimed,
                      "two_copy_slack_min_eigenvalue": slack2,
                      "two_copy_Bell_overlap": f2})
    return {"passed": True, "cases": cases,
            "minimum_witness_slack_eigenvalue": min(c["slack_min_eigenvalue"] for c in cases),
            "max_normalization_error": max(abs(c["Tr_Y_over_2"]-c["claimed_optimum"])
                                           for c in cases)}


def explicit_recipe():
    cases = []
    one, two = mp.mpf(1), mp.mpf(2)
    epsilon, q, r, B, g0, omega0 = mp.mpf(".1"), 2, one, one, one, one
    eta = epsilon/32
    for n in (1, 4):
        # Realizable bounds: .125 Z for n=1; disjoint .125 ZZ pairs for n=4.
        beta, chi = (mp.mpf(0) if n == 1 else mp.mpf(".25")), mp.mpf(".25")
        F, nu, c = n*(q*q-1), r/(q*q), r*(1-one/(q*q))
        Rp, ell, kappa = F*nu, mp.sqrt(r)/q, r-beta
        T = two/kappa*mp.log(4*n/eta**2)
        t0 = min(one/B, eta/(2*Rp))
        t1, tau0 = t0+T, mp.pi/(2*omega0)
        delta_max = min(one/r, kappa/r**2,
                        eta/(2*chi*mp.sqrt(Rp*T+(Rp*T)**2)),
                        eta**2/(2*n*c*c*T))
        bins = max(1, int(mp.ceil(T/delta_max)))
        delta = T/bins
        pQ = (eta/4)**2
        alpha = g0*g0*mp.exp(-2)*(B*t0)**6/36
        K1 = 2*g0*g0*B
        q0 = 1+(mp.e-1)*Rp/B+mp.log(1/pQ)
        z0 = 16*q0*q0/eta**2
        X0 = g0*g0*(t1+mp.mpf(33)/(16*B))
        P0 = 2+16*F*(nu/B)**2/eta**2
        M0 = (1+bins+256*X0*bins**2*z0**2/(alpha**2*delta**2)
              +4*X0*bins*K1**2*z0/alpha**4+2*X0*bins*z0)
        D0, a = F*P0*M0, 1+B*(t1+tau0)
        C = (12*F*ell*g0*M0*mp.sqrt(P0)/B
             +12*F*P0*M0**2*g0**2/B+16*D0*omega0/B)
        b_star = 4*mp.log(max(mp.e, C*a**11/eta))
        y_star = 2*b_star+2*44**2
        guard = y_star/(2*B)
        active, z = t1+tau0+2*guard, a+y_star
        cutoff = int(mp.ceil((mp.e-1)*Rp*active+mp.log(1/pQ)))
        zeta = eta**2/(16*cutoff**2)
        mode_rhs = (256*X0*bins**2/(alpha**2*delta**2*zeta**2)
                    +4*X0*bins*K1**2/(alpha**4*zeta)+2*X0*bins/zeta)
        modes = max(bins, int(mp.ceil(mode_rhs)))
        rail_threshold = max(one, 8*F*nu**2*active**2/eta**2)
        rails = 2**max(0, int(mp.ceil(mp.log(rail_threshold, 2))))
        cells = F*rails*modes
        require(len(str(modes)) < MP_DPS-40, "Insufficient arithmetic precision for recipe rounding")
        tol = mp.mpf("1e-100")
        ratios = {"Q_over_q0z": cutoff/(q0*z),
                  "N_over_M0z4": modes/(M0*z**4),
                  "P_over_P0z2": rails/(P0*z**2),
                  "D_over_D0z6": cells/(D0*z**6)}
        require(all(v <= 1+tol for v in ratios.values()), "Polynomial majorant violated")
        dg, atail = 2*g0*mp.exp(-B*guard/2), 4*omega0/B*mp.exp(-B*guard/2)
        switching = ((tau0+guard)*(6*F*ell*modes*mp.sqrt(rails)*dg
                     +3*F*rails*modes**2*dg**2)+4*cells*atail)
        majorant = C*z**11*mp.exp(-(z-a)/4)
        require(switching <= majorant*(1+tol) and majorant <= eta*(1+tol),
                "Switching guard bound failed")
        reset_p = r*delta/(1+c*delta)
        reff = -mp.log(1-reset_p)/delta
        budgets = {"edge": 2*Rp*t0,
                   "split": 2*chi*delta*mp.sqrt(Rp*T+(Rp*T)**2),
                   "one_jump": 2*mp.sqrt(n*c*c*T*delta/2),
                   "reverse": 2*mp.sqrt(n*mp.exp(-(reff-beta)*T)),
                   "rail": 4*mp.sqrt(F*nu**2*active**2/(2*rails)),
                   "number": 4*mp.sqrt(pQ),
                   "modes": 4*cutoff*mp.sqrt(zeta),
                   "switching": switching}
        require(all(v <= eta*(1+tol) for v in budgets.values()),
                "An allocated recipe budget was exceeded")
        require(mp.exp((mp.e-1)*Rp*active-cutoff) <= pQ*(1+tol),
                "Exponential photon cutoff bound failed")
        w = delta*zeta/(8*bins)
        gram_upper = bins*(4*w/(3*delta)+(8*X0/(alpha**2*delta*w)
                        +X0*K1**2/alpha**4+X0/2)/(modes+mp.mpf(".5")))
        require(gram_upper <= zeta*(1+tol), "Modal Gram recipe bound failed")
        cases.append({"n": n, "q": q, "epsilon": ".1", "r": "1", "B": "1",
                      "g0": "1", "Omega0": "1", "beta": mstr(beta), "chi": mstr(chi),
                      "T": mstr(T), "t0": mstr(t0), "K_bins": bins, "Delta": mstr(delta),
                      "G_star": mstr(guard), "A_active": mstr(active),
                      "Q_photons": cutoff, "P_rails": rails, "N_modes_exact_integer": str(modes),
                      "log10_N": mstr(mp.log10(modes)), "log10_material_cells": mstr(mp.log10(cells)),
                      "majorant_ratios": {k: mstr(v) for k, v in ratios.items()},
                      "budget_to_eta_ratios": {k: mstr(v/eta) for k, v in budgets.items()},
                      "Gram_bound_over_zeta": mstr(gram_upper/zeta),
                      "log10_switching_bound": mstr(mp.log10(switching)),
                      "log10_switching_majorant": mstr(mp.log10(majorant))})
    return {"passed": True, "mp_dps": MP_DPS,
            "scope": "Scalar arithmetic only; no receiver matrices of N_modes size are allocated.",
            "cases": cases}


def main():
    started = time.perf_counter()
    report_bytes = REPORT.read_bytes()
    functions = [laguerre_cascade, finite_vacuum_gram, kraus_environment,
                 actuator_bounds, amplitude_damping_witness, explicit_recipe]
    results = {}
    for function in functions:
        group_started = time.perf_counter()
        try:
            result = function()
        except Exception as exc:
            result = {"passed": False, "exception_type": type(exc).__name__, "message": str(exc)}
        result["duration_seconds"] = round(time.perf_counter()-group_started, 6)
        results[function.__name__] = result
        print(f"{function.__name__}: {'PASS' if result['passed'] else 'FAIL'}", flush=True)
        if not result["passed"]:
            print(f"  {result['exception_type']}: {result['message']}", flush=True)
    passed = all(result["passed"] for result in results.values())
    report = {
        "schema_version": 1, "passed": passed,
        "purpose": "Finite numerical diagnostics, not asymptotic proofs or interval-certified hardware verification.",
        "utc_run_time": datetime.now(timezone.utc).isoformat(),
        "provenance": {"python": sys.version, "platform": platform.platform(),
                       "numpy": np.__version__, "scipy": scipy.__version__, "mpmath": mp.__version__,
                       "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                       "source_report": str(REPORT.relative_to(HERE.parent)),
                       "source_report_sha256_at_start": hashlib.sha256(report_bytes).hexdigest(),
                       "source_report_sha256_at_end": hashlib.sha256(REPORT.read_bytes()).hexdigest(),
                       "randomness": "None: all parameter grids are deterministic.",
                       "float_absolute_tolerance": ATOL, "mp_decimal_digits": MP_DPS},
        "diagnostics": results, "total_duration_seconds": round(time.perf_counter()-started, 6)}
    destination = HERE / "results.json"
    destination.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(f"overall: {'PASS' if passed else 'FAIL'}; results: {destination}", flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
