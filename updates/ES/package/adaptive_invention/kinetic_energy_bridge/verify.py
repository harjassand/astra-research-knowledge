"""Independent finite checks of the exact formulas in WORKING_MATHEMATICS.md.

These checks are for a two-body scattering law and a prescribed-field
transport-diffusion diagnostic, not for an N-body kinetic limit.
"""

import json
import math
from pathlib import Path


def simpson(f, a, b, n=20000):
    assert n % 2 == 0
    h = (b - a) / n
    total = f(a) + f(b)
    for j in range(1, n):
        total += (4 if j % 2 else 2) * f(a + j * h)
    return h * total / 3


def rutherford_check():
    # Set a=1 and change variable x=b/a. The transverse integral is J(z).
    rows = []
    for z in (0.1, 1.0, 10.0, 100.0):
        exact = 0.5 * (math.log1p(z*z) + 1/(1+z*z) - 1)
        numeric = simpson(lambda x: x**3/(1+x*x)**2, 0, z)
        assert abs(exact - numeric) < 1e-8
        rows.append({"B_over_a": z, "J_exact": exact,
                     "J_numerical": numeric, "error": abs(exact-numeric)})
    return rows


def echo_check(r, k=1.0, sigma=1.0):
    assert r % 2 == 0
    nu = 1 / r
    T = 1 / nu
    delta = T / (r + 0.5)
    starts = []
    eta = k * delta / 2
    damping_quadrature = 0.0
    for j in range(r):
        mode = k if j % 2 == 0 else -k
        starts.append(eta)
        eta_next = eta - mode * delta
        damping_quadrature += simpson(
            lambda u: (eta - mode*u)**2, 0, delta, n=100
        )
        assert abs(eta_next - (-1)**(j+1)*k*delta/2) < 1e-12
        eta = eta_next
    assert abs(eta - k*delta/2) < 1e-12
    damping_quadrature += simpson(lambda u: (eta-k*u)**2,
                                  0, delta/2, n=100)
    eta_final = eta-k*delta/2
    assert abs(eta_final) < 1e-12
    D = nu * k*k*delta**3*(r/12 + 1/24)
    assert abs(nu*damping_quadrature-D) < 1e-10
    vertex_magnitude = k*delta/2
    assert all(abs(abs(v)-vertex_magnitude) < 1e-12 for v in starts)

    # For r equal alternating legs without the final half leg, terminal
    # frequency zero gives every second vertex exactly zero.
    naive_nodes = []
    naive_eta = 0.0
    for j in range(r):
        mode = k if j % 2 == 0 else -k
        naive_eta -= mode*delta
        naive_nodes.append(naive_eta)
    assert all(abs(naive_nodes[j]) < 1e-12 for j in range(1, r, 2))

    return {
        "nu": nu, "r_main_legs": r, "T": T, "delta": delta,
        "vertex_magnitude": vertex_magnitude,
        "damping_exponent": D, "damping_quadrature": nu*damping_quadrature,
        "unit_impulse_log_word_magnitude":
            -sigma*sigma*k*k*delta*delta/8-D+r*math.log(vertex_magnitude),
        "naive_equal_leg_zero_vertex_count": r//2,
    }


def main():
    result = {
        "scope": "finite arithmetic checks only; no microscopic limit",
        "rutherford_J_checks": rutherford_check(),
        "echo_rows": [echo_check(r) for r in (32, 64, 128, 256, 512)],
    }
    out = Path(__file__).with_name("checks.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"written": str(out),
                      "max_J_error": max(row["error"] for row in result["rutherford_J_checks"]),
                      "last_damping_exponent": result["echo_rows"][-1]["damping_exponent"]}))


if __name__ == "__main__":
    main()
