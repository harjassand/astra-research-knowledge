"""Exact support and componentwise-rank certificates for actual positive cuts."""
import sys
sys.dont_write_bytecode = True
import json, time, hashlib
import numpy as np
import sympy as S
from scipy.linalg import qr
from positive_gate import BASE, factors


def rational_tensors(delta):
    pairs, _, G, _ = factors(delta)
    # Positive diagonal similarity removes all square roots.  This changes
    # neither support nor rank, and preserves relative entrywise errors.
    D = S.diag(1, 2, 2*S.sqrt(6), 12, 24)
    Di = D.inv(); DD = S.kronecker_product(D, D)
    L = [(Di*a*D).applyfunc(S.simplify) for a, b in pairs]
    R = [(Di*b*D).applyfunc(S.simplify) for a, b in pairs]
    GG = (DD.inv()*G*DD).applyfunc(S.simplify)
    assert all(v.is_Rational and v >= 0 for M in L+R+[GG] for v in M)
    C = [[S.SparseMatrix(GG)*S.kronecker_product(S.SparseMatrix(L[x]),
          S.SparseMatrix(R[z])) for z in range(9)] for x in range(9)]
    return C


def cut_entry(C, cut, row, col):
    x, p = divmod(int(row), 25); z, q = divmod(int(col), 25)
    return C[x][z][p, q] if cut == 'x_a_z_b' else C[x][z][q, p]


def run():
    start = time.monotonic()
    source = BASE/'results/POSITIVE_CUT_TEST.json'
    proposals = json.loads(source.read_text())
    cnumeric = np.load(BASE/'results/positive_local_delta001.npz')['C'].reshape(9, 9, 25, 25)
    all_records = []
    for delta in (S.Rational(1, 1000), S.Rational(64, 2387589)):
        C = rational_tensors(delta)
        for old in proposals['records']:
            cut = old['cut']; perm = (0, 2, 1, 3) if cut == 'x_a_z_b' else (0, 3, 1, 2)
            numeric = cnumeric.transpose(perm).reshape(225, 225)
            support = np.array([[cut_entry(C, cut, i, j) != 0
                                 for j in range(225)] for i in range(225)], dtype=bool)
            assert np.array_equal(support, numeric > 0)
            selected = old['fooling_set']
            assert all(support[i, j] for i, j in selected)
            assert all(not(support[i, l] and support[k, j])
                       for a, (i, j) in enumerate(selected)
                       for k, l in selected[a+1:])
            balanced = numeric.copy()
            for _ in range(20):
                scale = balanced.max(axis=1); scale[scale == 0] = 1
                balanced /= scale[:, None]
                scale = balanced.max(axis=0); scale[scale == 0] = 1
                balanced /= scale[None, :]
            cols = qr(balanced, pivoting=True, mode='economic')[2][:25]
            rows = qr(balanced[:, cols].T, pivoting=True, mode='economic')[2][:25]
            A = S.Matrix([[cut_entry(C, cut, i, j) for j in cols] for i in rows])
            inverse = A.inv(method='DM')
            assert inverse*A == S.eye(25)
            conditioning = inverse.applyfunc(abs)*A.applyfunc(abs)
            kappa = max(sum(conditioning[i, j] for j in range(25)) for i in range(25))
            ceiling = int(S.ceiling(kappa)); safe_epsilon = S.Rational(1, 2*ceiling)
            assert safe_epsilon*kappa < 1
            record = dict(delta=str(delta), cut=cut,
                exact_support_checked_positions=int(support.size),
                exact_positive_positions=int(support.sum()),
                exact_fooling_set=selected,
                nonnegative_rank_lower_bound_for_relative_error_below_one=len(selected),
                tensor_power_support_bound=f'{len(selected)}**m for the uncontracted product boundary matrix',
                rank25_minor_rows=rows.tolist(), rank25_minor_cols=cols.tolist(),
                inverse_checked_exactly=True,
                componentwise_inverse_condition_ceiling=ceiling,
                certified_relative_error_below_which_any_approximant_has_rank_at_least25=str(safe_epsilon))
            all_records.append(record)
            print(str(delta), cut, 'fooling', len(selected), 'rank25 safe epsilon', str(safe_epsilon), flush=True)
    result = dict(status='EXACT_RATIONAL_SUPPORT_AND_COMPONENTWISE_RANK_CERTIFICATES',
        proposal_sha256=hashlib.sha256(source.read_bytes()).hexdigest(), records=all_records,
        interpretation='The proposed uniform componentwise positive tensor compression cannot discard these modes. The tensor-power bound is for arbitrary uncontracted boundary data, not a lower bound on a closed partition-function algorithm or trace-specific approximation.',
        elapsed_seconds=time.monotonic()-start)
    (BASE/'results/EXACT_CUT_CERTIFICATE.json').write_text(json.dumps(result, indent=2)+'\n')
    print('elapsed', result['elapsed_seconds'])


if __name__ == '__main__':
    run()
