"""Exact-layout/numerical discovery scan for d=5 Weyl mode subsets.

Each mode is one real two-dimensional +/- Weyl pair; H_g is its exact
star-Hamiltonian summand. The spectrum scan is diagnostic only; it neither
proves the all-subsets envelope nor searches for a channel counterexample.
"""
from itertools import combinations
import numpy as np

D = 5
ROOT = np.exp(2j * np.pi / D)
I = np.eye(D, dtype=complex)
X = np.roll(I, 1, axis=1)
Z = np.diag([ROOT**j for j in range(D)])
LINES = [(0, 1)] + [(1, k) for k in range(D)]
MODES = [((a*t) % D, (b*t) % D) for a,b in LINES for t in (1,2)]


def weyl(a,b):
    return np.linalg.matrix_power(X, a) @ np.linalg.matrix_power(Z, b)


def star_mode(a,b):
    W = weyl(a,b)
    A = (W + W.conj().T) / np.sqrt(2)
    B = (W - W.conj().T) / (1j*np.sqrt(2))
    out = np.zeros((D**3,D**3), dtype=complex)
    for H in (A,B):
        out += np.kron(np.kron(H.T,H),I) + np.kron(np.kron(H.T,I),H)
    return out


def main():
    full_modes = [star_mode(*g) for g in MODES]
    inds = [D*r+a+b*0 for r in range(D) for a in range(D) for b in range(D)
            if (a+b-r) % D == 0]
    # Fix flattening index consistent with numpy Kronecker order R,A,B.
    inds = [D*D*r + D*a + b for r in range(D) for a in range(D) for b in range(D)
            if (a+b-r) % D == 0]
    block_modes = [H[np.ix_(inds,inds)] for H in full_modes]
    # Exact group symmetry predicts the selected multiplicity block captures
    # each distinct eigenvalue; check this equality numerically for generators.
    for i in (0,1,5,11):
        full = np.linalg.eigvalsh(full_modes[i])
        block = np.linalg.eigvalsh(block_modes[i])
        if not np.allclose(full, np.repeat(block, D), atol=1e-9):
            raise RuntimeError(f"full/block spectral mismatch for mode {MODES[i]}")
    # All 2^12 supports. This is a floating-point diagnostic; exact proof must
    # replace it with symbolic SOS/charpoly or a uniform operator inequality.
    best_by_size = {}
    for size in range(len(MODES)+1):
        vals=[]
        for sub in combinations(range(len(MODES)), size):
            H = sum((block_modes[i] for i in sub), np.zeros_like(block_modes[0]))
            vals.append(float(np.linalg.eigvalsh(H)[-1]) if size else 0.0)
        best_by_size[size] = (min(vals), max(vals), len({round(x,8) for x in vals}))
    print("modes", MODES)
    print("full_vs_block_repeated_d", "PASS")
    for size,(lo,hi,distinct) in best_by_size.items():
        max_line = min(size, (D-1)//2) # diagnostic only; actual support per line count below
        print(f"size={size:2d} max_lambda={hi:.12f} min_lambda={lo:.12f} distinct={distinct} crude_target={2*(size+max_line):.12f}")
    # Stronger layer-cake support uses maximum occupancy in a projective line.
    best_gap = (-1e9,None,None,None)
    for size in range(1,len(MODES)+1):
        for sub in combinations(range(len(MODES)),size):
            counts=[sum(i//2==line for i in sub) for line in range(D+1)]
            target=2*(size+max(counts))
            H=sum((block_modes[i] for i in sub),np.zeros_like(block_modes[0]))
            top=float(np.linalg.eigvalsh(H)[-1])
            gap=top-target
            if gap>best_gap[0]: best_gap=(gap,sub,top,target)
    print("worst_global_layercake_gap",best_gap)

if __name__ == '__main__':
    main()
