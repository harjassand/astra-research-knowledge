"""Finite full-gate checks, including an uncertified legal coin-reuse variant.

The tested bath is H_M=Z/2. Results are normalized-Choi witnesses, not diamond
certificates. The analytic dimension-independent guarantee is separate.
"""

from itertools import product
from math import pi
import numpy as np

from exact_word_check import PROFILE
from moving_bath_checks import I, X, Y, Z, DATA, PAULIS, F_DATA, hermitian_unitary


def trace_memory_superoperator():
    out = np.zeros((16, 64), dtype=complex)
    for a in range(8):
        for b in range(8):
            if a % 2 == b % 2:
                out[a//2 + 4*(b//2), a + 8*b] = 1
    return out


def rectangular_choi_trace_norm(s, output_dimension=4, input_dimension=8):
    j = s.reshape(output_dimension, output_dimension,
                  input_dimension, input_dimension, order="F")
    j = j.transpose(0, 2, 1, 3).reshape(
        output_dimension*input_dimension, output_dimension*input_dimension, order="F"
    ) / input_dimension
    return np.sum(np.abs(np.linalg.eigvalsh((j + j.conj().T)/2)))


def main():
    trace = trace_memory_superoperator()
    e = hermitian_unitary(F_DATA, pi/4)
    ideal = np.kron(e.conj(), e) @ trace
    hm = np.kron(np.eye(4), Z/2)
    native = {h: np.kron(DATA[h], PAULIS[h]) for h in DATA}

    print("Target DMR->DR channel tested on normalized maximally entangled input.")
    print("Fresh coins are independent in every cycle. Reused coins are sampled just once.")
    for bath in ("constant_Z_half", "public_zero_mean_Z_half_each_cycle"):
        print("\n", bath)
        print("N delta T fresh_coin_witness fresh_witness/delta reused_coin_witness")
        for n in (1000, 8000, 64000, 512000, 4096000, 32768000):
            delta = (pi/(16*n))**(1/3)
            us = []
            for a, b in product((-1, 1), repeat=2):
                signs = {"A": a, "B": b, "C": a*b}
                u = np.eye(8, dtype=complex)
                for k, (h, orientation) in enumerate(PROFILE):
                    bath_sign = 1 if bath == "constant_Z_half" or k < 5 else -1
                    u = hermitian_unitary(bath_sign*hm + orientation*signs[h]*native[h], delta) @ u
                us.append(u)
            cycle_channel = sum(np.kron(u.conj(), u) for u in us)/4
            fresh = np.linalg.matrix_power(cycle_channel, n)
            reused_us = [np.linalg.matrix_power(u, n) for u in us]
            reused = sum(np.kron(u.conj(), u) for u in reused_us)/4
            err_fresh = rectangular_choi_trace_norm(trace @ fresh - ideal)
            err_reused = rectangular_choi_trace_norm(trace @ reused - ideal)
            print(f"{n} {delta:.9g} {10*n*delta:.9g} {err_fresh:.9g} "
                  f"{err_fresh/delta:.9g} {err_reused:.9g}")
    print("Finite numerical diagnostics only; matrix-power rounding accumulates with N.")


if __name__ == "__main__":
    main()
