#!/usr/bin/env python3
"""Exact GF(2) check of the [[5,1,3]] syndrome-subsystem counterexample."""
from itertools import product

N = 5

def bits(word):
    x = tuple(int(c in "XY") for c in word)
    z = tuple(int(c in "ZY") for c in word)
    return x, z

def word(x, z):
    return "".join("Y" if a and b else "X" if a else "Z" if b else "I" for a, b in zip(x, z))

def xor(a, b):
    return tuple(x ^ y for x, y in zip(a, b))

def mul(a, b):
    ax, az = bits(a); bx, bz = bits(b)
    return word(xor(ax, bx), xor(az, bz))  # phase-free; enough for cosets

def weight(p):
    return sum(c != "I" for c in p)

# Standard cyclic [[5,1,3]] stabilizer.
gens = ["XZZXI", "IXZZX", "XIXZZ", "ZXIXZ"]
gbits = [bits(g) for g in gens]

def syndrome(p):
    x, z = bits(p)
    return tuple(sum((x[i] & gz[i]) ^ (z[i] & gx[i]) for i in range(N)) % 2
                 for gx, gz in gbits)

stab = set()
for coeff in product((0, 1), repeat=4):
    p = "IIIII"
    for take, g in zip(coeff, gens):
        if take:
            p = mul(p, g)
    stab.add(p)

paulis = ["I", "X", "Y", "Z"]
all_paulis = ["".join(v) for v in product(paulis, repeat=N)]
centralizer = [p for p in all_paulis if syndrome(p) == (0, 0, 0, 0)]
nontrivial_logicals = [p for p in centralizer if p not in stab]
distance = min(weight(p) for p in nontrivial_logicals)

single_errors = ["IIIII"] + ["".join(p if i == j else "I" for i in range(N))
                              for j in range(N) for p in "XYZ"]
by_syndrome = {}
for p in single_errors:
    s = syndrome(p)
    assert s not in by_syndrome
    by_syndrome[s] = p
assert len(by_syndrome) == 16

# L = X^5 * g1 = IYYIX, a weight-three logical representative.
L = "IYYIX"
assert syndrome(L) == (0, 0, 0, 0)
assert L not in stab
assert weight(L) == distance == 3

P = "IIXII"  # X on qubit 3
R_s_natural = by_syndrome[syndrome("IIIXX")]
R_t_natural = by_syndrome[syndrome("XXIII")]
s = syndrome(R_s_natural)
t = syndrome(R_t_natural)
assert s != t
assert tuple(a ^ b for a, b in zip(s, syndrome(P))) == t
Q = mul(mul(R_t_natural, P), R_s_natural)
assert syndrome(Q) == (0, 0, 0, 0)
assert Q not in stab
assert weight(Q) == 3
# Q and L differ by a stabilizer, so their induced logical class is the same.
assert mul(Q, L) in stab

# On the code sector, P is itself the chosen representative of its syndrome,
# so applying its inverse correction leaves the logical subsystem unchanged.
assert by_syndrome[syndrome(P)] == P

print({
    "code": "[[5,1,3]]",
    "syndrome_count": len(by_syndrome),
    "syndrome_reps_unique_at_weight_le_1": True,
    "selected_input_rep": R_s_natural,
    "selected_output_rep": R_t_natural,
    "fault_pauli": P,
    "input_syndrome": "".join(map(str, s)),
    "output_syndrome": "".join(map(str, t)),
    "decoded_residual": Q,
    "logical_representative": L,
    "Q_times_L_in_stabilizer": True,
    "logical_holonomy_on_syndrome_sector": "Xbar",
    "logical_action_on_code_sector_after_correction": "I",
    "r": 1,
    "two_r_lt_d": 2 * 1 < distance,
})
