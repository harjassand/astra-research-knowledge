"""Evaluate the frozen witness using only observed seven-letter words.

--word accepts the observations at -t-h,-t,-h,0,h,t,t+h.
--counts accepts a CSV with no header: seven letters followed by count.
No hidden chain or source-model artifact is read.
"""
from fractions import Fraction as F
from pathlib import Path
from decimal import Decimal, localcontext
import argparse
import csv
import json


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def mv(a, b):
    return [dot(row, b) for row in a]


def raw(first, second):
    return ([F(first == 0)]
            + [F(first == 0 and second == k + 1) for k in range(5)]
            + [F(first == k) for k in range(1, 6)])


def decimal_string(value):
    with localcontext() as ctx:
        ctx.prec = 70
        return str(Decimal(value.numerator) / Decimal(value.denominator))


class Witness:
    def __init__(self, filename):
        data = json.loads(Path(filename).read_text())
        self.F = [[F(x) for x in row] for row in data['feature_matrix']]
        self.D = [[F(x) for x in row] for row in data['facet_residual_matrix']]
        self.K = [[F(x) for x in row] for row in data['K']]
        self.alpha = [F(x) for x in data['quadratic_coefficients']]
        self.constants = {name: F(value) for name, value in data['constants'].items()}

    def __call__(self, word):
        if len(word) != 7 or any(x not in range(6) for x in word):
            raise ValueError('A word must have exactly seven letters in {0,...,5}.')
        before = raw(word[3], word[2])
        after = raw(word[3], word[4])
        shifted_before = raw(word[1], word[0])
        shifted_after = raw(word[5], word[6])
        fm = mv(self.F, before)
        fp = mv(self.F, after)
        fsm = mv(self.F, shifted_before)
        fsp = mv(self.F, shifted_after)
        gm = [x - y for x, y in zip(fsm, mv(self.K, fm))]
        gp = [x - y for x, y in zip(fsp, mv(self.K, fp))]
        dm = mv(self.D, before)
        dp = mv(self.D, after)
        p0 = F(word[3] == 0)
        s2 = fm[1] * fp[1] + fm[2] * fp[2]
        a = self.alpha
        sq = (a[0] * p0 + a[1] * (fm[1] + fp[1]) / 2
              + a[2] * (fm[2] + fp[2]) / 2 + a[3] * fm[1] * fp[1]
              + a[4] * (fm[1] * fp[2] + fm[2] * fp[1]) / 2)
        rh = dot(dm, dp)
        rt = dot(gm, gp)
        c = self.constants
        value = (sq + c['circle_coefficient'] * (p0 - s2)
                 + (c['finite_facet_coefficient'] + c['tau']) * (p0 + s2)
                 + c['tau'] * p0 + c['Lambda'] * rh + c['Mu'] * rt) / c['M']
        if abs(value) > 1:
            raise RuntimeError('The supplied coefficient artifact violates its certified range.')
        return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', default=str(Path(__file__).with_name('witness_rational_v1.json')))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--word', nargs=7, type=int)
    group.add_argument('--counts')
    args = parser.parse_args()
    witness = Witness(args.certificate)
    if args.word is not None:
        value = witness(args.word)
        result = {'word': args.word, 'statistic': decimal_string(value), 'range':[-1,1]}
    else:
        total = 0
        weighted = F(0)
        rows = 0
        with open(args.counts, newline='') as handle:
            for row in csv.reader(handle):
                if len(row) != 8:
                    raise ValueError('Each CSV row must contain seven letters and one count.')
                values = [int(x) for x in row]
                count = values[7]
                if count < 0:
                    raise ValueError('Counts must be nonnegative integers.')
                weighted += count * witness(values[:7])
                total += count
                rows += 1
        if total == 0:
            raise ValueError('At least one observation window is required.')
        value = weighted / total
        delta = witness.constants['normalized_gap']
        result = {'windows':total, 'distinct_rows':rows, 'mean_statistic':decimal_string(value),
                  'below_target_half_gap':value < -delta / 2,
                  'half_gap_threshold':decimal_string(-delta / 2),
                  'sampling_note':'Confidence requires independent stationary windows or a separate dependence analysis.'}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
