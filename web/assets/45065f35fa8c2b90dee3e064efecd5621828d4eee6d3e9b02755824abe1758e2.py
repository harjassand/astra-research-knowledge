"""Stable exact-qubit formula diagnostic; elementary proof is in exact_family.md."""
import math


def family(C, L):
    v = C / math.sqrt(3)
    d = 2 * C / 3
    Rp = math.hypot(L - d, 2 * v)
    Rm = math.hypot(L + d, 2 * v)
    tp = math.tanh(Rp / 2)
    tm = math.tanh(Rm / 2)
    theta_p = math.atan2(2 * v, L - d)
    theta_m = math.atan2(2 * v, L + d)
    distance = math.sqrt(
        (tp - tm) ** 2 + 4 * tp * tm * math.sin((theta_p - theta_m) / 2) ** 2
    ) / 2
    # epsilon=(16C^2/9)/(1+e^L); no overflow or underflow needed.
    log_inv_eps = L - math.log(16 * C * C / 9) + math.log1p(math.exp(-L))
    coefficient = 4 * C * C / (3 * math.sqrt(3))
    return distance, log_inv_eps, coefficient


if __name__ == "__main__":
    print("C,L,T,L^2*T,target,(log(1/epsilon))^2*T/target")
    for C in (0.25, 1.0, 3.0):
        for L in (10.0, 30.0, 100.0, 300.0, 1000.0):
            T, ell, target = family(C, L)
            print(f"{C:g},{L:g},{T:.12g},{L*L*T:.12g},{target:.12g},{ell*ell*T/target:.12g}")
