#!/usr/bin/env python3
"""One-point six-state electron/TLS scattering check for the local ring model."""
import numpy as np


def solve(*, energy=0.5, delta=1.0, onsite=(0.0, 0.3, -0.2),
          hopping=(1.0, 1.0, 1.0), eta=0.4, phi=np.pi / 2,
          lead_hop=1.0, contact=1.0):
    t12, t23, t31 = hopping
    eps = np.asarray(onsite, dtype=float)
    n_tls = np.diag([0.0, 1.0])
    tau_x = np.array([[0.0, 1.0], [1.0, 0.0]])
    I3 = np.eye(3)
    I2 = np.eye(2)
    lead_sigma = []
    gamma = []
    for n in (0, 1):
        en = energy - n * delta
        if abs(en) >= 2 * lead_hop:
            raise ValueError("Both TLS sideband lead channels must be open here")
        root = np.sqrt(4 * lead_hop**2 - en**2)
        sig = contact**2 * (en - 1j * root) / (2 * lead_hop**2)
        lead_sigma.append(sig)
        gamma.append(-2 * sig.imag)

    outputs = {}
    for spin in (+1, -1):
        he = np.diag(eps).astype(complex)
        he[0, 1] = he[1, 0] = t12
        he[1, 2] = he[2, 1] = t23
        # Oriented 3->1 ring edge. Its reverse edge is the Hermitian conjugate.
        he[2, 0] = t31 * np.exp(1j * spin * phi)
        he[0, 2] = np.conj(he[2, 0])
        H = (np.kron(he, I2) + np.kron(I3, delta * n_tls)
             + eta * np.kron(np.diag([0.0, 0.0, 1.0]), tau_x))

        # Channel order: L0,L1,R0,R1. Contacts preserve TLS state.
        sigma_int = np.zeros((6, 6), dtype=complex)
        W = np.zeros((6, 4), dtype=complex)
        channels = []
        for lead_index, site in enumerate((0, 1)):
            for n in (0, 1):
                channel = 2 * lead_index + n
                channels.append((lead_index, n))
                sigma_int[2 * site + n, 2 * site + n] = lead_sigma[n]
                W[2 * site + n, channel] = np.sqrt(gamma[n])
        G = np.linalg.inv(energy * np.eye(6) - H - sigma_int)
        S = np.eye(4, dtype=complex) - 1j * W.conj().T @ G @ W
        outputs[spin] = {"H": H, "S": S, "W": W, "G": G,
                         "sigma": lead_sigma, "gamma": gamma}

    # Incoming L,n=0 is column 0; transmitted outgoing R,n=0,1 are rows 2,3.
    probs = {}
    for spin, result in outputs.items():
        S = result["S"]
        p_by_final_tls = np.abs(S[2:4, 0])**2
        T = float(p_by_final_tls.sum())
        R = float(np.abs(S[0:2, 0]).dot(np.abs(S[0:2, 0])))
        probs[spin] = {"transmitted_by_final_tls": p_by_final_tls,
                       "T": T, "R": R}
    Tup = probs[+1]["T"]
    Tdn = probs[-1]["T"]
    ptrans = (Tup - Tdn) / (Tup + Tdn)
    return outputs, probs, ptrans


def main():
    outputs, probs, ptrans = solve()
    S_up = outputs[+1]["S"]
    S_dn = outputs[-1]["S"]
    for spin, sign in ((+1, "up"), (-1, "down")):
        err = np.linalg.norm(outputs[spin]["S"].conj().T @ outputs[spin]["S"] - np.eye(4))
        q = probs[spin]
        print(f"{sign}: unitarity_error={err:.3e}, T={q['T']:.12f}, R={q['R']:.12f}, T+R={q['T']+q['R']:.12f}")
        print("  transmitted by final TLS n=0,1:", *(f"{x:.12g}" for x in q["transmitted_by_final_tls"]))
    print("TR transpose error:", f"{np.linalg.norm(S_dn - S_up.T):.3e}")
    print("transmitted polarization:", f"{ptrans:.12f}")
    print("whole-output z spin for unpolarized L,n=0:",
          f"{0.5*((probs[+1]['T']+probs[+1]['R'])-(probs[-1]['T']+probs[-1]['R'])):.3e}")

    # Useful degeneracy controls: no vibronic transition, no loop, or no SOC phase.
    for label, kwargs in (("eta=0", {"eta": 0.0}),
                          ("t12=0 tree with SOC link retained", {"hopping": (0.0, 1.0, 1.0)}),
                          ("phi=0", {"phi": 0.0})):
        _, _, p = solve(**kwargs)
        print(f"{label} polarization:", f"{p:.3e}")


if __name__ == "__main__":
    main()
