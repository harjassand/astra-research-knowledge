#!/usr/bin/env python3
"""High-precision check of the dissipation certificate on its sharp mode.

For a unit-normalized no-slip shear eigenmode b with eigenvalue lambda_1,
u(t)=q(t)b, q' + nu*lambda_1*q = F, q(0)=0.  The PDE nonlinearity vanishes
for this shear, so the storage bound is attained exactly.  This script checks
K(T) = K_star and W(T)-K(T) = integral_0^T epsilon(t) dt.
"""

from decimal import Decimal, getcontext


def check(T_text: str, F_text: str, nu_text: str, lam_text: str) -> None:
    D = Decimal
    T, F, nu, lam = map(D, (T_text, F_text, nu_text, lam_text))
    gamma = nu * lam
    e1 = (-gamma * T).exp()
    e2 = (-2 * gamma * T).exp()
    qT = F / gamma * (1 - e1)
    K = qT * qT / 2
    K_star = F * F / (2 * gamma * gamma) * (1 - e1) ** 2
    W = F * F / gamma * (T - (1 - e1) / gamma)
    dissipation = F * F / gamma * (
        T - 2 * (1 - e1) / gamma + (1 - e2) / (2 * gamma)
    )
    assert abs(K - K_star) < D("1e-55")
    assert abs((W - K) - dissipation) < D("1e-45")
    eta = D("0.001") * T  # certified average work-sensor error 0.001
    interval_width_bound = (K_star + 2 * eta) / T
    print(
        f"T={T}: K(T)={K}, K_star={K_star}, W-K-D={W-K-dissipation}, "
        f"certificate_width_bound={interval_width_bound}"
    )


def main() -> None:
    getcontext().prec = 60
    for t in ("0.1", "1", "5", "20"):
        check(t, "2", "0.5", "1")


if __name__ == "__main__":
    main()
