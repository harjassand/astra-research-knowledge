"""Exact finite-dimensional witness: local marginals and Jz law miss global coherence."""
import json
import numpy as np


def witness(n):
    d = 1 << n
    zero = np.zeros(d, dtype=complex)
    zero[0] = 1
    one = np.zeros(d, dtype=complex)
    one[-1] = 1
    ghz = (zero + one) / np.sqrt(2)
    pure = np.outer(ghz, ghz.conj())
    incoherent = (np.outer(zero, zero.conj()) + np.outer(one, one.conj())) / 2

    # Both states give probability 1/2 to each J_z eigenvalue +/-n/2.
    jz_law_equal = np.allclose(np.diag(pure).real, np.diag(incoherent).real, atol=1e-14, rtol=0)

    marginals_equal = True
    for k in range(1, n):
        da, de = 1 << k, 1 << (n - k)
        p4 = pure.reshape(da, de, da, de)
        c4 = incoherent.reshape(da, de, da, de)
        p_red = np.einsum("aibi->ab", p4)
        c_red = np.einsum("aibi->ab", c4)
        marginals_equal &= np.allclose(p_red, c_red, atol=1e-14, rtol=0)

    distance = 0.5 * np.linalg.svd(pure - incoherent, compute_uv=False).sum()
    return {
        "n": n,
        "all_proper_prefix_marginals_equal": bool(marginals_equal),
        "Jz_probability_laws_equal": bool(jz_law_equal),
        "trace_distance": float(distance),
        "expected_trace_distance": 0.5,
        "classical_comparator_is_separable": True,
    }


if __name__ == "__main__":
    print(json.dumps([witness(n) for n in range(2, 6)], indent=2))
