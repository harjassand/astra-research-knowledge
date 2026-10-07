"""JSON interface for exact-bit low-k relative counts and TV samples."""
from lowk_bcs import *
import argparse
import json
from pathlib import Path


def rational(x):
    if isinstance(x, float):
        raise ValueError('encode exact rationals as integers or fraction strings')
    return Q(x)


def entry(x):
    return C(rational(x.get('re', 0)), rational(x.get('im', 0))) if isinstance(x, dict) else C(rational(x))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text())
    f = [[entry(x) for x in row] for row in data['F']]
    counter = LowKCounter(f, data['pair_count'], data.get('exact_sign_cap', 256), data.get('sign_budget', 1000000))
    rng = random.Random(data['seed']) if 'seed' in data else random.SystemRandom()
    out = {'method': 'paired-Pfaffian row projection and exact column volumes', 'arithmetic': 'Q(i) and Gaussian integers',
           'rng': 'seeded reproducibility fixture' if 'seed' in data else 'OS random-bit interface',
           'admitted_scope': 'arbitrary explicit rational-complex F, hard filters, prescribed low k',
           'pair_count': counter.k, 'sector_moment_bound': math.comb(2*counter.k, counter.k)}
    try:
        estimate, receipt = counter.estimate(eta=rational(data.get('count_relative_accuracy', '1/4')),
                                             delta=rational(data.get('count_failure_probability', '1/16')),
                                             rng=rng, mode=data.get('mode', 'auto'))
        out['norm_estimate'], out['count_receipt'] = str(estimate), receipt
        exact = receipt['kind'].startswith('EXACT')
        number = data.get('samples', 1)
        if number and exact and not estimate:
            out['sample_status'] = 'ZERO_SECTOR_EXACT'
        elif number and not exact and not data.get('positive_sector_promise', False):
            out['sample_status'] = 'UNKNOWN: randomized count is not an exact positive-sector certificate; promise required'
        else:
            samples = []
            for _ in range(number):
                i, j, sample_receipt = counter.sample(rational(data.get('epsilon', '1/10')), rng, data.get('mode', 'auto'))
                samples.append({'up': list(i), 'down': list(j), 'receipt': sample_receipt})
            out['samples'] = samples
            out['sample_accuracy_scope'] = 'each draw has stated TV bound on the positive-sector promise'
    except BudgetExceeded as e:
        out['status'] = 'RUN_BUDGET_EXCEEDED'
        out['reason'] = str(e)
        out['accuracy_status'] = 'no estimate or sample guarantee is claimed for an incomplete call'
    out['stats'] = counter.stats
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
