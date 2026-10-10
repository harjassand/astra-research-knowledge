"""Exact rational reconstruction for the frozen two-state example."""

from fractions import Fraction as Q


def observables(a, b, c, alpha, h, r):
    # K=[[a,b],[b,c]], k=K e1, and f=-Kx-alpha*x^3.
    k = (a, b)
    kx = (a * h + b * r, b * h + c * r)
    f = (
        -kx[0] - alpha * h**3,
        -kx[1] - alpha * r**3,
    )
    lf_h = f[0]
    lg_lf_h = -a - 3 * alpha * h**2
    z0 = -lf_h - alpha * h**3
    p = a**2 + b**2  # L_k z0, equivalently the input-output bracket formula D z0
    lf_z0 = k[0] * f[0] + k[1] * f[1]
    return lf_h, lg_lf_h, z0, p, lf_z0


def recover(alpha, h, obs, b_gauge):
    lf_h, lg_lf_h, z0, p, lf_z0 = obs
    a = -lg_lf_h - 3 * alpha * h**2
    b2 = p - a**2
    assert b_gauge**2 == b2
    r = (z0 - a * h) / b_gauge
    t = -lf_z0 - alpha * (a * h**3 + b_gauge * r**3)
    c = (t - p * h - a * b_gauge * r) / (b_gauge * r)
    return a, b2, r, c


def zero_state_step_coefficients(a, b, c, alpha, U, degree=4):
    """Exact right Taylor coefficients after a constant input step at rest.

    x_i(t)=sum_m coeff[i][m] t^m. The recurrence comes directly from
    (m+1)x[m+1] = [-Kx-alpha*x^3+Ue1][m].
    """
    zero = Q(0)
    coeff = [[zero for _ in range(degree + 1)] for _ in range(2)]
    K = ((a, b), (b, c))
    for m in range(degree):
        for i in range(2):
            linear = sum(K[i][j] * coeff[j][m] for j in range(2))
            cubic = sum(
                coeff[i][j] * coeff[i][k] * coeff[i][m - j - k]
                for j in range(m + 1)
                for k in range(m - j + 1)
            )
            forcing = U if i == 0 and m == 0 else zero
            coeff[i][m + 1] = (forcing - linear - alpha * cubic) / (m + 1)
    return coeff


def recover_from_step(alpha, U, output_coefficients):
    """Recover a,b^2,c from y's t^2,t^3,t^4 coefficients at zero state."""
    y2, y3, y4 = output_coefficients[2:5]
    a = -2 * y2 / U
    b2 = 6 * y3 / U - a**2
    c = (-24 * y4 / U - 6 * U**2 * alpha - a**3 - 2 * a * b2) / b2
    return a, b2, c


def main():
    alpha = Q(2, 3)
    h, r = Q(1, 5), Q(1, 4)
    truth = (Q(3), Q(1), Q(2))
    obs = observables(*truth, alpha, h, r)
    assert obs == (
        Q(-1283, 1500),
        Q(-77, 25),
        Q(17, 20),
        Q(10),
        Q(-39317, 12000),
    )
    a, b2, r_hat, c = recover(alpha, h, obs, Q(1))
    assert (a, b2, r_hat, c) == (Q(3), Q(1), Q(1, 4), Q(2))

    # Hidden sign conjugacy: b and r flip together, leaving all measured
    # quantities unchanged; the reconstruction returns the same c.
    obs_gauged = observables(Q(3), Q(-1), Q(2), alpha, h, Q(-1, 4))
    assert obs_gauged == obs
    a2, b2_2, r_hat2, c2 = recover(alpha, h, obs_gauged, Q(-1))
    assert (a2, b2_2, r_hat2, c2) == (Q(3), Q(1), Q(-1, 4), Q(2))

    # One known constant input step from the known zero equilibrium suffices
    # for n=2. Coefficients 2,3,4 reveal a,b^2,c, respectively.
    step = zero_state_step_coefficients(Q(3), Q(1), Q(2), alpha, Q(2))
    recovered = recover_from_step(alpha, Q(2), step[0])
    assert recovered == (Q(3), Q(1), Q(2))
    assert step[0][1:5] == [Q(2), Q(-3), Q(10, 3), Q(-17, 4)]

    # Exact port disconnection: b=0 makes output independent of c for x2=0.
    for c_value in (Q(1), Q(2), Q(7)):
        assert observables(Q(3), Q(0), c_value, alpha, h, Q(0))[0:3] == observables(
            Q(3), Q(0), Q(1), alpha, h, Q(0)
        )[0:3]
    print("PASS: exact n=2 recovery, single-step Taylor realization, hidden-sign symmetry, disconnected-port control")


if __name__ == "__main__":
    main()
