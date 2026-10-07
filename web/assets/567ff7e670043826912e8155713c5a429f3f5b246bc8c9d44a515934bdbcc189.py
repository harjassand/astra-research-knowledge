"""JSON command line for the delivered exact rational algorithms.

Example: python3 bcs_count_sample.py fixture.json
An entry is an integer, rational string, or {"re": "1/2", "im": "-3/7"}.
Methods: mps, green, balanced_tree, forest, separator, supplied_tree.
All methods expose an explicit max_dimension cap. No width optimization,
floating rank truncation, multiplicative oracle or postselection is hidden.
"""
from cutrank_bcs import *
from treecut_bcs import *
from green_bcs import *
import argparse
import json
from pathlib import Path


def rational(x):
    if isinstance(x, float):
        raise ValueError('encode rational input as an integer or fraction string')
    return Q(x)


def complex_rational(x):
    if isinstance(x, dict):
        return C(rational(x.get('re', 0)), rational(x.get('im', 0)))
    return C(rational(x))


def tuple_tree(x):
    if isinstance(x, int):
        return x
    if not isinstance(x, list) or len(x) != 2:
        raise ValueError('binary tree is a site index or two children')
    return tuple_tree(x[0]), tuple_tree(x[1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text())
    F = [[complex_rational(x) for x in row] for row in data['F']]
    n = len(F)
    t = [rational(x) for x in data.get('t', [0]*n)]
    cap = data.get('max_dimension', 64)
    method = data.get('method', 'mps')
    allowed = data.get('allowed')
    out = {'method': method, 'arithmetic': 'exact Q(i)', 'max_dimension_cap': cap}
    if method == 'green':
        if any(t):
            raise ValueError('the fast Green algorithm requires hard filters t=0')
        params = acquire_dense_green(F)
        local = None if allowed is None else [[Q(int(x in s)) for x in (0,1,2)] for s in allowed]
        counter = GreenCounter(params,local)
        cs = counter.counts()
        draw = lambda k, rng: counter.sample(k,rng)
        out['admission'] = 'acquired dense complex diagonally gauged Green off-diagonal kernel'
        out.pop('max_dimension_cap')
    elif method == 'mps':
        compiled = acquire_mps(F, max_dimension=cap)
        cs = counts(compiled, t, allowed)
        draw = lambda k, rng: sample(compiled, k, t, allowed=allowed, rng=rng)
        out['cut_ranks'] = [x.rank for x in compiled.cuts]
        out['bond_dimensions'] = [x.dim for x in compiled.cuts]
    else:
        if method == 'balanced_tree':
            tree = balanced_order_tree(n)
        elif method == 'forest':
            tree = forest_tree(F)
            if tree is None:
                raise ValueError('off-diagonal support is not a forest')
        elif method == 'separator':
            bound = data.get('separator_bound', 1)
            tree, witness = separator_tree(F, bound)
            out['separator_bound'] = bound
            out['separator_witness'] = witness
        elif method == 'supplied_tree':
            tree = tuple_tree(data['tree'])
        else:
            raise ValueError('unknown method')
        compiled = acquire_tree(F, tree, max_dimension=cap)
        cs = tree_counts(compiled, t, allowed)
        draw = lambda k, rng: tree_sample(compiled, k, t, rng=rng, allowed=allowed)
        out['site_order'] = compiled.order
        out['tree'] = tree
        out['cut_ranks'] = [x.basis.rank for x in compiled.nodes]
        out['bond_dimensions'] = [x.basis.dim for x in compiled.nodes]
    out['coefficients'] = [str(x) for x in cs]
    out['grandcanonical_norm'] = str(sum(cs))
    out['zero_sectors'] = [k for k, x in enumerate(cs) if not x]
    number = data.get('samples', 0)
    if number:
        k = data['pair_count']
        if not isinstance(k, int) or not 0 <= k <= n or not cs[k]:
            raise ValueError('requested sector is invalid or zero')
        rng = random.Random(data['seed']) if 'seed' in data else random.SystemRandom()
        out['sample_states'] = [draw(k, rng) for _ in range(number)]
        out['sample_encoding'] = ['empty', 'up', 'down', 'both']
        out['rng'] = 'seeded reproducibility fixture' if 'seed' in data else 'OS random-bit interface'
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
