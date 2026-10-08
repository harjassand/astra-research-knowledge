"""Seed-moment replay from bit-mask Clifford algebra, independent of candidate code."""
from itertools import combinations
from pathlib import Path
import json
import sympy as sp

NQ = 5
ND = 2*NQ + 1
I = sp.I


def mul(a, b):
    """Multiply i^p X^x Z^z labels; local Y is i X Z."""
    p, x, z = a
    q, u, v = b
    sign = (z & u).bit_count() % 2
    return ((p + q + 2*sign) % 4, x ^ u, z ^ v)


def gammas():
    out = []
    for q in range(NQ):
        prefix = (1 << q) - 1
        out.append((0, 1 << q, prefix))       # Z_0 ... Z_(q-1) X_q
        out.append((1, 1 << q, prefix | (1 << q)))  # Z_0 ... Z_(q-1) Y_q
    out.append((0, 0, (1 << NQ)-1))
    return out


GAMMA = gammas()


def clifford_basis(k):
    for subset in combinations(range(ND), k):
        word = (0, 0, 0)
        for j in subset:
            word = mul(word, GAMMA[j])
        p, x, z = word
        yield subset, ((p + k*(k-1)//2) % 4, x, z)


def expect(word, support):
    phase, x, z = word
    amp = sp.Integer(1)/len(support)
    value = 0
    for src in support:
        dst = src ^ x
        if dst in support:
            sign = -1 if (z & src).bit_count() % 2 else 1
            value += amp * (I**phase) * sign
    value = sp.simplify(value)
    if sp.im(value) != 0:
        raise AssertionError((word, support, value))
    return sp.re(value)


def moments(support):
    scores = []
    for k in range(1, 6):
        score = sum(expect(word, support)**2 for _, word in clifford_basis(k))
        scores.append(sp.factor(score))
    if sum(scores) != 31:
        raise AssertionError((support, scores))
    return scores


def main():
    supports = {
        "coherent_basis_state": (0,),
        "two_weight_hamming_3": (0, 7),
        "two_weight_hamming_4": (0, 15),
        "two_weight_hamming_5": (0, 31),
    }
    expected = {
        "coherent_basis_state": [1, 5, 5, 10, 10],
        "two_weight_hamming_3": [0, 2, 7, 8, 14],
        "two_weight_hamming_4": [1, 1, 1, 14, 14],
        "two_weight_hamming_5": [0, 0, 5, 10, 16],
    }
    results = {}
    for name, support in supports.items():
        got = [int(x) for x in moments(support)]
        if got != expected[name]:
            raise AssertionError((name, got, expected[name]))
        results[name] = got
    out = {
        "status": "PASS",
        "method": "standalone bit-mask Clifford multiplication with P=i^p X^x Z^z; no candidate Python module imported",
        "number_of_clifford_words": sum(len(list(combinations(range(ND), k))) for k in range(1, 6)),
        "seed_moments": results,
        "canonical_orbit_channel_reason": "The spinor representation is irreducible, so Haar average of each rank-one projector is I/32. Each seed therefore gives a full-domain orbit POVM with effects 32 P_g dg and prepares P_g; its covariant transfer on irreducible grade k is the seed moment s_k/C(11,k).",
    }
    Path(__file__).with_name("independent_seed_replay.json").write_text(json.dumps(out, indent=2) + "\n")
    print("PASS: four exact seed moment vectors replayed from independent bit-mask algebra over 1023 words.")


if __name__ == "__main__":
    main()
