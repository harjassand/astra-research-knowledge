"""Own exact checks; peer implementations execute only from owned copies."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).with_name('peer_copies')))
from cutrank_bcs import *
from check_lowk_bcs import leibniz
from functional_digraph_dp import count_poly
import treewidth_filtered_parity as peer_tree
import itertools
import json


def direct(f, t, allowed=None):
    n = len(f)
    allowed = [set(range(4)) for _ in range(n)] if allowed is None else allowed
    out = [Q(0)]*(n+1)
    for k in range(n+1):
        for i in itertools.combinations(range(n), k):
            for j in itertools.combinations(range(n), k):
                if any((int(h in i)+2*int(h in j)) not in allowed[h] for h in range(n)):
                    continue
                w = leibniz([[f[a][b] for b in j] for a in i]).abs2()
                for h in set(i) & set(j):
                    w *= t[h]
                out[k] += w
    return out


def main():
    skew = [[C(0 if i == j else 1 if i < j else -1) for j in range(4)] for i in range(4)]
    assert direct(skew, [0]*4)[2] == 8
    base, tagged = 49, [[ZERO for _ in range(4)] for _ in range(4)]
    for e, (i, j) in enumerate(itertools.combinations(range(4), 2)):
        tagged[i][j] = tagged[j][i] = C(base**(3**e))
    encoded = direct(tagged, [0]*4)[2]
    assert encoded.denominator == 1
    value, pos, extracted = encoded.numerator, 0, 0
    while value:
        value, digit = divmod(value, base)
        if digit > 24:
            digit -= base
            value += 1
        assert abs(digit) <= 24
        p, trits = pos, []
        for _ in range(6):
            p, d = divmod(p, 3)
            trits.append(d)
        if p == 0 and all(d in (0, 2) for d in trits) and trits.count(2) == 2:
            extracted += digit
        pos += 1
    assert extracted == 12
    cancel = [[C(int(i != j)) for j in range(4)] for i in range(4)]
    assert direct(cancel, [0]*4)[2] == 0
    f2 = [[ZERO, ONE], [ONE, ZERO]]
    assert direct(f2, [0, 0])[1] == 2
    assert direct([[z/8 for z in row] for row in f2], [0, 0])[1] == Q(1, 32)
    p = [1, 1, 3, 4, 3, None]
    f = zeros(6, 6)
    for i, j in enumerate(p):
        if j is not None:
            f[i][j] = C(i+1, Q(1, i+2))
    w = [Q(0) if j is None else f[i][j].abs2() for i, j in enumerate(p)]
    t = [Q(0), Q(3), Q(1, 2), Q(5), Q(2), Q(0)]
    assert count_poly(p, w, t) == direct(f, t)
    row, col = {0: 1, 4: 0}, {1: 1, 2: 0}
    masks = [{s for s in range(4) if (i not in row or (s & 1) == row[i]) and
              (i not in col or ((s >> 1) & 1) == col[i])} for i in range(6)]
    assert count_poly(p, w, t, row, col) == direct(f, t, masks)
    rng = random.Random(3039)
    f = [[C(rng.randrange(-1, 2), Q(rng.randrange(-1, 2), 2)) for _ in range(4)] for _ in range(4)]
    t = [Q(0), Q(3), Q(1, 2), Q(5)]
    masks = [set(range(4)), {0, 3}, {1, 2, 3}, {0, 1, 2}]
    pf = [[(z.re, z.im) for z in row] for row in f]
    labels = ('0', 'u', 'd', 'ud')
    allowed = [{labels[s] for s in a} for a in masks]
    exact = direct(f, t, masks)
    order_checks = 0
    for order in ((0,1,2,3), (3,1,0,2), (2,0,3,1)):
        assert peer_tree.counts(pf, t, allowed, order) == exact
        order_checks += 1
    assert counts(acquire_mps(f, max_dimension=16), t, masks) == exact
    diag = [[peer_tree.qc(2), peer_tree.ZERO], [peer_tree.ZERO, peer_tree.qc(1)]]
    assert peer_tree.counts(diag, [Q(5), Q(3)]) == [Q(1), Q(23), Q(60)]
    out = {'status': 'PASS', 'scope': 'bounded independent exact peer-claim checks; not external proof or priority validation',
           'l03_K4_norm': 8, 'l03_tagged_K4_decoded_2powk_PM': extracted,
           'tagged_largest_entry_bits': max(z.re.numerator.bit_length() for row in tagged for z in row),
           'l06_K4_zero_and_scale_check': True, 'l09_functional_full_and_prefix_vectors': 2,
           'l09_filtered_tree_order_vectors': order_checks, 'l09_independent_MPS_comparison': True,
           'l09_diagonal_overlap_sign_fixture': [1,23,60],
           'peer_file_mutations': [], 'execution_copies': 'reviews/peer_copies; imports and pycache remain owned'}
    Path(__file__).with_name('checks_assigned_peers.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
