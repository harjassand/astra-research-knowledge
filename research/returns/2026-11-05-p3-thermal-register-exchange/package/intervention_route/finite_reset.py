"""Finite-window harmonic reset and sine-mark certificate.

This script checks exact analytic identities using high precision quadrature.
It is not a stochastic proof and not a hardware simulation.  The companion
note supplies the instrument proof and physical resource contract.
"""
from __future__ import annotations

import json
from pathlib import Path
import mpmath as mp

mp.mp.dps = 65


def derivative(c, order=1):
    c = list(c)
    for _ in range(order):
        c = [mp.mpf(j) * c[j] for j in range(1, len(c))]
    return c or [mp.mpf("0")]


def value(c, r):
    return mp.polyval(list(reversed(c)), r)


def add(*terms):
    out = [mp.mpf("0")] * max(len(c) for _, c in terms)
    for scale, c in terms:
        for j, a in enumerate(c):
            out[j] += scale * a
    return out


def integrate_product(a, b):
    return mp.fsum(x*y/mp.mpf(i+j+1)
                   for i, x in enumerate(a) for j, y in enumerate(b))


def pulse(mass, gamma, lam, H):
    """Root's uniform degree-13 Hermite compiler, in r=t/H coordinates."""
    nu = gamma - lam
    phi = [mp.mpf("0")] * 14
    phi[3] = mp.mpf(1)/mp.factorial(3)
    phi[5] = H**2 * (lam**2 + nu**2) / mp.factorial(5)
    matrix = mp.matrix(7, 7)
    rhs = mp.matrix(7, 1)
    for j in range(7):
        rhs[j] = -value(derivative(phi, j), 1)
        for q, k in enumerate(range(7, 14)):
            matrix[j, q] = mp.factorial(k)/mp.factorial(k-j)
    tail = mp.lu_solve(matrix, rhs)
    for q, k in enumerate(range(7, 14)):
        phi[k] = tail[q]
    h = add((1, derivative(phi, 3)),
            (gamma*H, derivative(phi, 2)),
            (lam*nu*H**2, derivative(phi, 1)))
    gt = add((1, derivative(phi, 5)),
             (-H**2*(lam**2+nu**2), derivative(phi, 3)),
             (H**4*lam**2*nu**2, derivative(phi, 1)))
    return {
        "phi": phi, "h": h, "g_tilde": gt,
        "g": lambda t: mass/H**2 * value(gt, t/H),
        "h_at": lambda t: value(h, t/H),
    }


def expA(t, mass, gamma, lam):
    nu = gamma-lam
    if lam == nu:
        r = lam
        return mp.exp(-r*t) * mp.matrix([
            [1+r*t, t/mass], [-mass*r*r*t, 1-r*t]])
    el, en = mp.exp(-lam*t), mp.exp(-nu*t)
    return mp.matrix([
        [(nu*el-lam*en)/(nu-lam), (el-en)/(mass*(nu-lam))],
        [-mass*lam*nu*(el-en)/(nu-lam), (-lam*el+nu*en)/(nu-lam)]])


def matrix_integral(fn, a, b):
    m = fn((a+b)/2)
    return mp.matrix([[mp.quad(lambda t: fn(t)[i, j], [a, b])
                       for j in range(m.cols)] for i in range(m.rows)])


def max_abs_sampled(fn, left, right, points=2001):
    return max(abs(fn(left+(right-left)*j/(points-1))) for j in range(points))


def certificate(lam="0.2", H="0.05", delay="0.05", L="0.1",
                gamma="1", mass="1", sigma2="1", G="1",
                pointer_q_variance="0.1", pointer_p_variance="1e-10",
                eta="0.5"):
    lam, H, delay, L, gamma, mass, sigma2, G, vQ, vP, eta = map(
        mp.mpf, [lam, H, delay, L, gamma, mass, sigma2, G,
                 pointer_q_variance, pointer_p_variance, eta])
    nu = gamma-lam
    T = H+delay+L
    A = mp.matrix([[0, 1/mass], [-mass*lam*nu, -gamma]])
    B = mp.matrix([[0], [1]])
    E = lambda t: expA(t, mass, gamma, lam)
    d = E(T)*B
    p = pulse(mass, gamma, lam, H)
    g, h = p["g"], p["h_at"]
    vb = 2*gamma*sigma2*H*integrate_product(p["h"], p["h"])
    vm = vQ/G**2
    v = vb+vm
    tau2 = sigma2-v
    if tau2 <= 0:
        raise ValueError("The supplied pulse exceeds the reset noise budget")
    mark_amplitude = eta*mp.exp(v/(2*tau2))
    g_action = mass**2/H**3 * integrate_product(p["g_tilde"], p["g_tilde"])
    c_self = mass/H * integrate_product(p["h"], p["g_tilde"])
    moments = []
    for a in [mp.mpf(0), lam, nu, -lam, -nu]:
        got = mp.quad(lambda t: g(t)*mp.exp(a*t), [0, H])
        moments.append(abs(got-mass*a))
    endpoint_cov = mp.matrix([
        [2*gamma*sigma2*mp.quad(lambda s: h(s)*E(H-s)[j, 1], [0, H])]
        for j in range(2)])
    meter_kick = mp.matrix([
        [G*mp.quad(lambda s: E(T-s)[j, 1]*g(s), [0, H])]
        for j in range(2)])
    meter_kick_formula = -G*mass*E(T)*A*B
    w = lambda s: mp.sin(mp.pi*s/L)**2
    W = matrix_integral(
        lambda s: w(s)*(E(L-s)*B)*(E(L-s)*B).T, 0, L)
    c = W**-1*d
    force = lambda s: (w(s)*B.T*E(L-s).T*c)[0]
    feed_endpoint = mp.matrix([
        [mp.quad(lambda s: E(L-s)[j, 1]*force(s), [0, L])]
        for j in range(2)])
    feed_action = mp.quad(lambda s: force(s)**2, [0, L])
    # The coefficient multiplying E in the final source is -d.  Its cross
    # covariance with all remaining endpoint noise is zero by the previous
    # endpoint_cov test, propagated through the delay and feedforward window.
    endpoint_noise = matrix_integral(
        lambda s: 2*gamma*sigma2*(E(T-s)*B)*(E(T-s)*B).T, 0, T)
    endpoint_noise += vP*meter_kick*meter_kick.T
    contrast = 2*eta*mp.sqrt(sigma2)*mp.exp(-mp.mpf("0.5"))*E(T)[1, 1]
    # Independent numerical Gaussian integral for the arm-channel identity.
    arm_errors = []
    cond_variance = v*tau2/sigma2
    for zeta in [-2, -1, 0, 1, 2]:
        mean = tau2/sigma2*zeta
        expected = mp.quad(
            lambda z: (1+mark_amplitude*mp.sin(
                mp.sqrt(sigma2)*(mean+mp.sqrt(cond_variance)*z)/tau2))/2
                *mp.exp(-z*z/2)/mp.sqrt(2*mp.pi), [-mp.inf, mp.inf])
        target = (1+eta*mp.sin(zeta/mp.sqrt(sigma2)))/2
        arm_errors.append(abs(expected-target))
    result = {
        "parameters": {"lambda": lam, "nu": nu, "gamma": gamma,
                       "H": H, "rotation_delay": delay, "L": L, "T": T,
                       "sigma_squared": sigma2, "mass": mass, "eta": eta,
                       "G": G, "pointer_q_variance": vQ,
                       "pointer_p_variance": vP},
        "bath_noise_variance": vb,
        "meter_position_noise_variance": vm,
        "total_meter_noise_variance": v,
        "fresh_actuator_variance": tau2,
        "corrected_sine_amplitude": mark_amplitude,
        "mark_probability_margin": (1-mark_amplitude)/2,
        "meter_force_action": G**2*vP*g_action,
        "meter_self_backaction_coefficient": c_self,
        "meter_peak_g_sampled": max_abs_sampled(g, 0, H),
        "meter_peak_g_derivative_sampled": max_abs_sampled(
            lambda t: mass/H**3*value(derivative(p["g_tilde"]), t/H), 0, H),
        "feedforward_force_action_per_E_U_squared": feed_action,
        "feedforward_peak_coefficient_sampled": max_abs_sampled(force, 0, L),
        "minimum_gramian_eigenvalue": min(mp.eigsy(W, eigvals_only=True)),
        "meter_endpoint_kick_per_unit_P": list(meter_kick),
        "loaded_endpoint_noise_covariance": [list(endpoint_noise[i, :]) for i in range(2)],
        "observable_momentum_arm_contrast": contrast,
        "verification": {
            "max_exponential_moment_error": max(moments),
            "max_endpoint_noise_cross_covariance": max(abs(x) for x in endpoint_cov),
            "max_meter_kick_identity_error": max(abs(x) for x in meter_kick-meter_kick_formula),
            "max_feedforward_endpoint_error": max(abs(x) for x in feed_endpoint-d),
            "max_mark_channel_error": max(arm_errors),
            "pulse_endpoint_g_error": max(abs(g(0)), abs(g(H))),
            "pulse_endpoint_g_derivative_error": max(
                abs(mass/H**3*value(derivative(p["g_tilde"]), r)) for r in [0, 1]),
        },
    }
    return result


def jsonable(x):
    if isinstance(x, dict):
        return {k: jsonable(v) for k, v in x.items()}
    if isinstance(x, list):
        return [jsonable(v) for v in x]
    if isinstance(x, mp.mpf):
        return float(x)
    return x


if __name__ == "__main__":
    reports = [certificate(lam=lam) for lam in ["0.2", "0.5", "1e-8"]]
    reports.append(certificate(H="0.2", delay="0.05", L="0.5",
                               pointer_p_variance="1e-8"))
    result = {
        "description": "Analytic finite reset certificates; not a hardware simulation.",
        "limiting_h_squared_integral": float(mp.mpf(41440)/46189),
        "limiting_g_tilde_squared_integral": float(mp.mpf(48384000)/2431),
        "cases": jsonable(reports),
    }
    target = Path(__file__).with_name("finite_reset_results.json")
    target.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
