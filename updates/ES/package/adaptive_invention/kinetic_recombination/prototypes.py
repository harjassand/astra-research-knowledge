"""Numerical checks of ring resummation and the smooth chaotic-dimer obstruction.

These are finite checks of explicitly stated formulas, not a kinetic-limit proof.
The many-body dimer experiment uses the exact repulsive 1/r potential in R^3.
The proof note separately treats neutralized periodic Coulomb dynamics.
"""

from pathlib import Path
import json
import math
import time

import numpy as np

HERE = Path(__file__).resolve().parent


def pair_solution(s, b=1.0):
    """s = b^(3/2)/2 * (y sqrt(1+y^2) + asinh(y))."""
    lo, hi = 0.0, max(1.0, math.sqrt(2 * s / b**1.5) + 1)
    for _ in range(80):
        y = (lo + hi) / 2
        val = b**1.5 / 2 * (y * math.sqrt(1 + y * y) + math.asinh(y))
        if val < s:
            lo = y
        else:
            hi = y
    y = (lo + hi) / 2
    return b * (1 + y * y), y / math.sqrt(b * (1 + y * y))


def many_body_dimer(n, step=0.005, s_end=2.0, seed=822):
    """Velocity Verlet for x'=v/N, v'=N^-2 sum r/r^3, prime=d/ds."""
    rng = np.random.default_rng(seed + n)
    centers = rng.uniform(-0.5, 0.5, (n // 2, 3))
    normals = rng.normal(size=(n // 2, 3))
    normals /= np.linalg.norm(normals, axis=1)[:, None]
    covariance = np.array([4.0, 1.0, 0.1])
    shared_v = rng.normal(size=(n // 2, 3)) * np.sqrt(covariance)
    x = np.empty((n, 3))
    v = np.repeat(shared_v, 2, axis=0)
    x[0::2] = centers + normals / (2 * n)
    x[1::2] = centers - normals / (2 * n)

    def acceleration(xx):
        r = xx[:, None, :] - xx[None, :, :]
        r2 = np.einsum("ijk,ijk->ij", r, r)
        np.fill_diagonal(r2, np.inf)
        return np.einsum("ij,ijk->ik", r2**-1.5, r) / n**2

    def energy(xx, vv):
        r = xx[:, None, :] - xx[None, :, :]
        r2 = np.einsum("ijk,ijk->ij", r, r)
        np.fill_diagonal(r2, np.inf)
        return float(np.sum(vv * vv) / 2 + np.sum(r2**-0.5) / (2 * n))

    e0 = energy(x, v)
    a = acceleration(x)
    steps = round(s_end / step)
    h = s_end / steps
    for _ in range(steps):
        v += 0.5 * h * a
        x += h * v / n
        a = acceleration(x)
        v += 0.5 * h * a
    rho, q = pair_solution(s_end)
    predicted = np.repeat(shared_v, 2, axis=0)
    predicted[0::2] += q * normals
    predicted[1::2] -= q * normals
    actual_rho = n * np.linalg.norm(x[0::2] - x[1::2], axis=1)
    residual = np.linalg.norm(v - predicted, axis=1)
    return {
        "N": n,
        "step_s": h,
        "s_end": s_end,
        "physical_end_time": s_end / n,
        "predicted_kick": q,
        "predicted_scaled_pair_separation": rho,
        "rms_velocity_error": float(np.sqrt(np.mean(residual**2))),
        "median_velocity_error": float(np.median(residual)),
        "max_velocity_error": float(np.max(residual)),
        "median_scaled_pair_separation_error": float(np.median(np.abs(actual_rho - rho))),
        "relative_energy_error": (energy(x, v) - e0) / e0,
        "kinetic_energy_change_per_particle": float(
            np.sum(v * v) / (2 * n) - np.sum(shared_v * shared_v) / n
        ),
        "isolated_pair_kinetic_energy_change_per_particle": q * q / 2,
    }


def dawson(x):
    """Stable positive-real integral x int_0^1 exp[-x^2(1-u^2)] du."""
    nodes, weights = np.polynomial.legendre.leggauss(128)
    u = (nodes + 1) / 2
    return float(x * np.sum(weights * np.exp(-x*x * (1-u*u))) / 2)


def susceptibility(variance, phase_velocity):
    z = phase_velocity / math.sqrt(2 * variance)
    return complex(1 - 2*z*dawson(z), math.sqrt(math.pi)*z*math.exp(-z*z)) / variance


def radial_J(c, cutoff):
    """Exact int_0^K r^3 / |r^2+c|^2 dr, c=a+ib, b>=0."""
    a, b = c.real, c.imag
    if abs(b) < 1e-14:
        if a <= 0:
            raise ValueError("undamped real pole: not allowed in this formula")
        return (math.log1p(cutoff**2 / a) + a / (cutoff**2 + a) - 1) / 2
    return (
        math.log(((cutoff**2+a)**2+b*b)/(a*a+b*b)) / 4
        - a/(2*b)*(math.atan((cutoff**2+a)/b)-math.atan(a/b))
    )


def radial_J_quadrature(c, cutoff):
    """Independent log-radius trapezoid plus resonance-resolving linear mesh."""
    lo = np.geomspace(1e-8, cutoff, 200001)
    a, b = c.real, abs(c.imag)
    if a < 0 and b > 0:
        root = math.sqrt(-a)
        width = b / (2 * root)
        extra = root + width * np.linspace(-100, 100, 100001)
        lo = np.unique(np.concatenate((lo, extra[(extra > 0) & (extra < cutoff)])))
    integrand = lo**3 / np.abs(lo*lo+c)**2
    return float(np.trapezoid(integrand, lo))


def volterra_response(variance=0.1, k=1.0, end=30.0, step=0.005, order=6):
    """Solve rho = free - p*rho with causal p=t exp(-a k^2 t^2/2)."""
    t = np.arange(round(end / step) + 1) * step
    free = np.exp(-variance*k*k*t*t/2)
    p = t * free
    rho = np.zeros_like(t)
    rho[0] = 1
    for n in range(1, len(t)):
        rho[n] = free[n] - step * (
            np.dot(p[1:n], rho[n-1:0:-1]) + 0.5*p[n]*rho[0]
        )

    # Independent finite Neumann history sum; use FFT only for convolutions.
    fft_size = 1 << ((2*len(t)-1).bit_length())
    p_fft = np.fft.rfft(p, n=fft_size)
    term = free.copy()
    partial = term.copy()
    errors = []
    for m in range(1, order+1):
        conv = np.fft.irfft(p_fft*np.fft.rfft(term, n=fft_size), n=fft_size)[:len(t)]
        term = -step * (conv - 0.5*p*term[0])
        partial += term
        errors.append({"order":m, "sup_error":float(np.max(np.abs(partial-rho))),
                       "sup_absolute_history_term":float(np.max(np.abs(term)))})
    return {
        "variance":variance, "k":k, "end":end, "step":step,
        "kernel_L1_norm_exact":1/(variance*k*k),
        "exact_causal_response_max":float(np.max(np.abs(rho))),
        "exact_causal_response_at_end":float(rho[-1]),
        "late_response_max":float(np.max(np.abs(rho[t >= end/2]))),
        "finite_ring_history_errors":errors,
        "sample_times":t[::round(1/step)].tolist(),
        "sample_response":rho[::round(1/step)].tolist(),
    }


def echo_check():
    """Exact free-streaming derivative/pulse operator; not self-consistent plasma."""
    # h_-1(t,v)=A(v) exp(+itv); a k2=2 force pulse at t=L.
    # Outgoing k=1 density at t: i(t-L) Ahat(t-2L), Ahat=exp(-a q^2/2).
    a = 0.1
    rows = []
    for L in [10, 30, 100, 300]:
        hidden_density = math.exp(-a*L*L/2)
        echo = L
        rows.append({"layer_age":L, "pre_pulse_density":hidden_density,
                     "unit_amplitude_echo_density_absolute":echo,
                     "kinetic_N_over_logN_iid_sized_two_leg_scaling_at_N_1e6":
                     1/math.log(1e6)})
    return {
        "statement":"Operator counterexample only; prescribed pulse, not an iid microscopic plasma counterexample.",
        "projection_variance":a, "incoming_k":-1,"pulse_k":2,"outgoing_k":1,
        "rho_after_pulse":"i*(t-L)*exp[-a*(t-2L)^2/2]",
        "rows":rows,
    }


def main():
    started = time.time()
    pair_rows = []
    for n in [32,64,128,256,512]:
        row = many_body_dimer(n)
        pair_rows.append(row)
        print("dimer", n, row["rms_velocity_error"], row["relative_energy_error"], flush=True)
    pair_rows.append(many_body_dimer(128, step=0.0025))
    (HERE/"dimer_experiment.json").write_text(json.dumps({
        "model":"exact repulsive Coulomb 1/(N r) Hamiltonian in R3; no screening supplied",
        "seed_rule":"822+N", "Sigma_diagonal":[4,1,0.1],
        "matched_pair_probability_for_two_tags":"1/(N-1)",
        "TV_bound_for_s_tags":"s*(s-1)/(2*(N-1))", "rows":pair_rows,
    }, indent=2))

    radial_rows=[]
    for a,u in [(0.1,0),(0.1,1),(0.1,1.2),(0.1,1.5),(1,0),(4,0)]:
        c=susceptibility(a,u)
        K=100.0
        value=radial_J(c,K)
        check=radial_J_quadrature(c,K)
        radial_rows.append({"projection_variance":a,"phase_velocity":u,
            "chi_real":c.real,"chi_imag":c.imag,"K":K,
            "J_exact":value,"J_numeric":check,"relative_check_error":abs(value-check)/max(1,abs(value)),
            "J_minus_logK":value-math.log(K),
            "static_Debye_J":radial_J(complex(1/a,0),K),
            "leading_log_fraction_at_K_1e6":radial_J(c,1e6)/math.log(1e6)})
    (HERE/"radial_screening.json").write_text(json.dumps(radial_rows,indent=2))
    ring=volterra_response()
    refined=volterra_response(step=0.0025,order=0)
    ring["refined_grid_late_response_max"]=refined["late_response_max"]
    ring["refined_grid_response_at_end"]=refined["exact_causal_response_at_end"]
    (HERE/"ring_response.json").write_text(json.dumps(ring,indent=2))
    (HERE/"echo_counterexample.json").write_text(json.dumps(echo_check(),indent=2))
    print("radial", radial_rows, flush=True)
    print("ring", {k:v for k,v in ring.items() if not k.startswith("sample")},flush=True)
    print("elapsed_seconds",time.time()-started,flush=True)


if __name__ == "__main__":
    main()
