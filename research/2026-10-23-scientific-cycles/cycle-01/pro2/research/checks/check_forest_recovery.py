"""Exact fixtures for the constructive forest recovery and its noise bound."""
import time
START = time.perf_counter()
CPU = time.process_time()
from fractions import Fraction as F
from pathlib import Path
import sys, json, resource
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from forest_recovery import forest_design, recover, apply_supported


def norm2(rows):
    return sum(x*x for row in rows for x in row)


def run():
    # Isolated vertices, paths, star, branching tree, multiple components,
    # and a parent ordering that is not topological. These check the actual
    # recovery map and noise identity, not a numerical proxy for the proof.
    examples = [[-1], [-1, -1, -1], [-1, 0], [-1, 0, 1, 2, 3, 4],
                [-1, 0, 0, 0, 0, 0, 0], [-1, 0, 0, 1, 1, 2, 2, 4],
                [-1, 0, 1, -1, 3, 3, 5], [3, 0, 0, -1, 3, 4, 2]]
    receipts = []
    for parents in examples:
        n = len(parents)
        colors, seed = forest_design(parents)
        a = [F(2*i-3, i+2) for i in range(n)]
        b = [F(0) if p == -1 else F((-1)**i*(i+3), i+1)
             for i, p in enumerate(parents)]
        y = apply_supported(parents, a, b, seed)
        assert recover(parents, y) == (a, b)
        child_sums = [F(0) for _ in parents]
        for v, p in enumerate(parents):
            if p != -1:
                child_sums[p] += b[v]
        assert norm2(y) == sum(v*v for v in a) + sum(v*v for v in b) + sum(v*v for v in child_sums)
        dn = sum(v*v for v in a) + 2*sum(v*v for v in b)
        assert dn <= 2*norm2(y)
        err = [[F((-1)**(i+j)*(i+2*j+1), 17*(i+j+1)) for j in range(3)] for i in range(n)]
        noisy = [[y[i][j]+err[i][j] for j in range(3)] for i in range(n)]
        ar, br = recover(parents, noisy)
        error_squared = sum((x-z)**2 for x, z in zip(a, ar)) + 2*sum((x-z)**2 for x, z in zip(b, br))
        assert error_squared <= 2*norm2(err)
        receipts.append({'vertices':n,'components':parents.count(-1),'exact_recovery':True,
                         'exact_energy_identity':True,'arbitrary_action_noise_bound':True})
    rejected = 0
    for parents in [[0], [1, 0], [1, 2, 0], [-2], [5]]:
        try:
            forest_design(parents)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError('invalid forest accepted')
    assert rejected == 5
    out = {'PASS':True,'fixtures':receipts,'invalid_forest_rejections':rejected,
           'new_NIST_queries':0,'floating_optimization':False,
           'wall_seconds':time.perf_counter()-START,'cpu_seconds':time.process_time()-CPU,
           'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024}
    (ROOT/'results/forest_recovery_checks.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__ == '__main__':
    run()
