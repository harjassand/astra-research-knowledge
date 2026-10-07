#!/usr/bin/env python3
"""Fresh fixtures against copied peer engines and own direct determinant code."""
import importlib.util
import json
import random
from fractions import Fraction
from pathlib import Path


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


base = Path(__file__).parent
own = module("own_pf_audit", base.parent / "audit_c03_l10/pfaffian_prefix_checks.py")
lowrank = module("copied_l05", base / "replayed_sources/augmented_grassmann_dp.py")
rank = module("copied_l08", base / "replayed_sources/parity_treewidth_dp.py")
rng = random.Random(840317)
records = []

# The initial loop-DP prose must allow using one edge in BOTH colors. If
# choices were only none/red/blue once, this simplest norm would be lost.
f = [[own.ZERO, own.ONE], [own.ZERO, own.ZERO]]
assert own.direct_norm(f, 1) == 1
assert lowrank.exact_chiral_elimination(f, 2, [0, 1])[1] == (1, 0)
records.append({"claim": "both-colored single-edge term", "norm": 1,
                "scope": "initial connectivity transition needs a both-colors option; refined exterior engine includes it"})

for n, r in ((3, 1), (4, 1), (4, 2), (5, 2)):
    f, augmented = lowrank.make_case(rng, n, r)
    order = list(reversed(range(n))) + list(range(n, n + r))
    got = lowrank.exact_chiral_elimination(augmented, n, order)
    exact = [own.direct_norm(f, k) for k in range(n + 1)]
    assert got == [(x, 0) for x in exact]
    records.append({"claim": "sparse-plus-low-rank chiral contraction", "n": n, "r": r,
                    "exact_coefficients": exact})

for n, r in ((3, 1), (4, 2), (5, 2)):
    a = [[(Fraction(rng.randrange(-2, 3), 7), Fraction(rng.randrange(-2, 3), 5))
          for _ in range(r)] for _ in range(n)]
    b = [[(Fraction(rng.randrange(-2, 3), 3), Fraction(rng.randrange(-2, 3), 11))
          for _ in range(n)] for _ in range(r)]
    f = [[rank.sum_gaussian(own.mul(a[i][s], b[s][j]) for s in range(r))
          for j in range(n)] for i in range(n)]
    exact = [own.direct_norm(f, k) for k in range(r + 1)]
    got = rank.rank_transfer(a, b)
    assert got == exact
    acquired_a, acquired_b = rank.rank_factorization(f)
    assert rank.rank_transfer(acquired_a, acquired_b) == exact
    for k in range(r + 1):
        assert rank.rank_transfer_sector(acquired_a, acquired_b, k) == (exact[k], 0)
    records.append({"claim": "rank transfer with fresh rational complex factors", "n": n, "r": r,
                    "exact_coefficients": [str(x) for x in exact]})

# A down-mode swap can send a role-separated pair source onto up-idler sites.
# The resulting diagonal pair matrix has unprojected norm 2 but hard c_1=0.
separated = [[own.ZERO for _ in range(4)] for _ in range(4)]
separated[0][2] = separated[1][3] = own.ONE
overlapped = [[own.ZERO for _ in range(4)] for _ in range(4)]
overlapped[0][0] = overlapped[1][1] = own.ONE
assert own.direct_norm(separated, 1) == 2
assert own.direct_norm(overlapped, 1) == 0
records.append({"claim": "bipartite source scope repair", "separated_hard_norm": 2,
                "signal_swapped_overlap_hard_norm": 0, "unprojected_norm_both": 2})

result = {"status": "PASS", "fresh_fixtures": len(records), "records": records,
          "scope": "Finite new-fixture replays of copied engines with independent direct determinant comparator; asymptotics from separately reconstructed proofs; no peer writes"}
(base / "cross_exact_checks.json").write_text(json.dumps(result, indent=2, default=str) + "\n")
print(json.dumps({key: value for key, value in result.items() if key != "records"}))
