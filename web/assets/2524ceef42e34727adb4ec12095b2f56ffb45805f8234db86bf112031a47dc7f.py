#!/usr/bin/env python3
"""Exact tiny checks for the post-projection transfer gate; standard library only."""
from fractions import Fraction
from itertools import combinations
import json
from pathlib import Path

# Four orbitals in canonical order: u_i,u_j,d_i,d_j.
# The Gaussian mode swap exchanges u_i and u_j.
perm = (1, 0, 2, 3)

def swap_state(state):
    out = {}
    for bits, amp in state.items():
        occupied = [i for i in range(4) if bits >> i & 1]
        image = [perm[i] for i in occupied]
        inversions = sum(image[a] > image[b] for a in range(len(image)) for b in range(a + 1, len(image)))
        sign = -1 if inversions % 2 else 1
        dst = sum(1 << i for i in image)
        out[dst] = out.get(dst, 0) + sign * amp
    return {k: v for k, v in out.items() if v}

def hard_project(state):
    # Site i has (u_i,d_i)=(0,2); site j has (u_j,d_j)=(1,3).
    return {bits: amp for bits, amp in state.items()
            if not ((bits & 1) and (bits & 4)) and not ((bits & 2) and (bits & 8))}

psi = {1 | 8: 1}  # u_i^dagger d_j^dagger |vac>
pg = hard_project(swap_state(psi))
gp = swap_state(hard_project(psi))
assert pg == {}
assert gp == {2 | 8: 1}

# Bipartite source norm: sum_{I,J, |I|=|J|=k} |det M[I,J]|^2.
M = [[Fraction(1), Fraction(1), Fraction(0)],
     [Fraction(0), Fraction(1), Fraction(1)]]

def det(A):
    if not A:
        return Fraction(1)
    if len(A) == 1:
        return A[0][0]
    total = Fraction(0)
    for j, x in enumerate(A[0]):
        minor = [row[:j] + row[j+1:] for row in A[1:]]
        total += (-1 if j % 2 else 1) * x * det(minor)
    return total

def direct(k):
    total = Fraction(0)
    for I in combinations(range(len(M)), k):
        for J in combinations(range(len(M[0])), k):
            d = det([[M[i][j] for j in J] for i in I])
            total += d*d
    return total

# For this real-rational example, MM^T=[[2,1],[1,2]],
# so the elementary symmetric coefficients are e_0=1,e_1=4,e_2=3.
source_norms = [direct(k) for k in range(3)]
assert source_norms == [1, 4, 3]

result = {
    "mode_order": ["u_i", "u_j", "d_i", "d_j"],
    "input": "u_i^dagger d_j^dagger|vac>",
    "P_after_G": pg,
    "G_after_P": {str(k): v for k, v in gp.items()},
    "noncommutation_witness": "P G |psi> = 0 while G P |psi> = u_j^dagger d_j^dagger|vac> != 0",
    "bipartite_M": [[str(x) for x in row] for row in M],
    "direct_minor_squared_norms_by_k": [str(x) for x in source_norms],
    "eigenvalue_free_MMdagger_elementary_coefficients": ["1", "4", "3"],
    "status": "PASS",
}
out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
