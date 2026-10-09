"""Five-beam check of equal-growth Lax roots and different first-pulse peaks."""

import numpy as np


V = np.array([-1.0, -0.5, 0.25, 0.6, 1.0])
G = np.array([-53 / 100, 544 / 2475, 548 / 1575, -425 / 924, 173 / 225])
ROOTS = (-0.3 + 0.2j, 0.4 + 0.2j)


def rhs(_t, flat):
    p = flat.reshape(len(V), 3)
    d0 = p.sum(axis=0)
    d1 = (V[:, None] * p).sum(axis=0)
    return np.cross(d0[None, :] - V[:, None] * d1[None, :], p).ravel()


def conversion(p):
    return 0.5 * np.sum(np.abs(G) - np.sign(G) * p[:, 2])


def rk4_step(t, y, h):
    k1 = rhs(t, y)
    k2 = rhs(t + h / 2, y + h * k1 / 2)
    k3 = rhs(t + h / 2, y + h * k2 / 2)
    k4 = rhs(t + h, y + h * k3)
    return y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6


def mode_matrix():
    g0 = G.sum()
    g1 = V @ G
    return (
        1j * np.diag(g0 - V * g1)
        - 1j * np.diag(G) @ np.ones((len(G), len(G)))
        + 1j * np.outer(V * G, V)
    )


def expected_pulse(root):
    a, b = root.real, root.imag
    chi = b**2 * V**2 / ((a**2 + b**2) * ((V - a) ** 2 + b**2))
    return float(np.abs(G) @ chi), chi


def integrate_mode(q, eps, gamma=0.2, dt=0.002):
    q0 = eps * q
    if np.max(np.abs(q0)) >= np.min(np.abs(G)):
        raise ValueError("seed is too large for the fixed-length initialization")
    z0 = np.sign(G) * np.sqrt(G**2 - np.abs(q0) ** 2)
    p = np.column_stack((q0.real, q0.imag, z0)).ravel()
    t_end = np.log(1 / eps) / gamma + 18.0
    n = int(np.ceil(t_end / dt))
    h = t_end / n
    best_c, best_t, best_state = -1.0, 0.0, None
    d0_initial = p.reshape(len(V), 3).sum(axis=0)
    max_d0_error = 0.0
    max_length_error = 0.0
    for j in range(n + 1):
        t = j * h
        frame = p.reshape(len(V), 3)
        c = conversion(frame)
        if c > best_c:
            best_c, best_t, best_state = c, t, frame.copy()
        max_d0_error = max(max_d0_error, np.max(np.abs(frame.sum(axis=0) - d0_initial)))
        max_length_error = max(
            max_length_error,
            np.max(np.abs(np.linalg.norm(frame, axis=1) - np.abs(G))),
        )
        if j < n:
            p = rk4_step(t, p, h)
    return best_c, best_t, best_state, max_d0_error, max_length_error


def main():
    A = mode_matrix()
    eigvals, eigvecs = np.linalg.eig(A)
    growing = [j for j, z in enumerate(eigvals) if z.real > 1e-8]
    growing.sort(key=lambda j: eigvals[j].imag, reverse=True)
    print(f"G0={G.sum():.12g}; G1={V @ G:.12g}")
    print(f"growing eigenvalues={[(eigvals[j]) for j in growing]}")
    print(f"target Lax roots={ROOTS}; both have Im(u)=0.2")
    for j, root in zip(growing, ROOTS):
        q = eigvecs[:, j]
        q /= np.max(np.abs(q))
        c_expected, chi = expected_pulse(root)
        print(f"root={root}; normalized q={q}")
        print(f"  analytic chi={chi}; analytic peak C={c_expected:.12g}")
        for eps in (1e-3, 1e-4):
            c_num, t_peak, p_peak, d0_err, length_err = integrate_mode(q, eps)
            print(
                f"  eps={eps:g}: numeric peak C={c_num:.12g}, t_peak={t_peak:.6f}, "
                f"z_peak={p_peak[:, 2]}, D0_err={d0_err:.3g}, "
                f"length_err={length_err:.3g}"
            )


if __name__ == "__main__":
    main()
