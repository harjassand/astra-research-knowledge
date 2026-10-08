"""Deterministic SU(2) star blocks for the highest multipole.

This computes a fixed analytically admitted family, not random SDP scans.
All Racah coefficients and pair eigenvalues are first formed exactly in
SymPy; only eigenspectra are floating-point diagnostics unless explicitly
requested with --exact. Reports do not certify all-spin inequalities.
"""
from functools import lru_cache
import argparse
import json
from pathlib import Path

import numpy as np
import sympy as sp
from sympy.physics.wigner import wigner_6j


@lru_cache(None)
def sixj(j, total, k, ell):
    return wigner_6j(j, j, k, j, total, ell)


def blocks(n, rank=None):
    """n=2j; BC labels l and AB labels k use the same allowed set."""
    j = sp.Rational(n, 2)
    rank = n if rank is None else rank
    first_total = sp.Rational(n % 2, 2)
    for step in range(int(3*j-first_total)+1):
        total = first_total + step
        labels = list(range(int(abs(total-j)), int(min(n,total+j))+1))
        u = sp.Matrix([
            [sp.sqrt((2*ell+1)*(2*k+1))*sixj(j,total,k,ell)
             for k in labels]
            for ell in labels
        ])
        pair_eigen = [
            (-1)**(rank+n+k) * (n+1)*(2*rank+1)
            * wigner_6j(j,j,rank,j,j,k)
            for k in labels
        ]
        pair = u*sp.diag(*pair_eigen)*u.T
        for parity in [0,1]:
            selected = [i for i,ell in enumerate(labels) if ell % 2 == parity]
            if not selected:
                continue
            block = 2*pair.extract(selected,selected)
            yield total, [labels[i] for i in selected], block


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, nargs='+', default=[1,3,5,7,9,11])
    parser.add_argument('--exact', action='store_true')
    parser.add_argument('--rank', type=int)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = []
    for n in args.n:
        rank = n if args.rank is None else args.rank
        winner = None
        orthogonal_error = 0.0
        all_blocks = []
        for total, labels, block in blocks(n,rank):
            arr = np.array(block.evalf(17),dtype=float)
            top = float(np.linalg.eigvalsh(arr)[-1])
            item = {'total':str(total),'bc_labels':labels,'star_top':top}
            if args.exact:
                item['matrix'] = [[str(x) for x in row] for row in block.tolist()]
                item['characteristic_polynomial'] = str(block.charpoly().as_expr().factor())
            all_blocks.append(item)
            if winner is None or top > winner['star_top']:
                winner = item
        volume = 2*rank+1
        classical_support = (n+1)/2 if rank == n and n % 2 else None
        row = {'n':n,'j':str(sp.Rational(n,2)),'rank':rank,'V':volume,
               'k_exact':classical_support,'winner':winner}
        if classical_support is not None:
            row['C2_margin_diagnostic'] = volume+classical_support-winner['star_top']
            row['ratio_diagnostic'] = 2*(volume-classical_support)/(2*volume-winner['star_top'])
        if args.exact:
            row['blocks']=all_blocks
        result.append(row)
        print(json.dumps(row if not args.exact else {k:v for k,v in row.items() if k!='blocks'}),flush=True)
    if args.out:
        args.out.write_text(json.dumps(result,indent=2)+'\n')


if __name__ == '__main__':
    main()
