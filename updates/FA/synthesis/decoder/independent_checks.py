"""Independent finite diagnostics; no producer imports, no scientific certification."""
from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb, exp
from pathlib import Path
import json
import random


def span(basis, mask):
    out = 0
    for i, value in enumerate(basis):
        if mask >> i & 1:
            out ^= value
    return out


def rank(vectors, n):
    pivots = {}
    for value in vectors:
        while value:
            k = value.bit_length()-1
            if k in pivots:
                value ^= pivots[k]
            else:
                pivots[k] = value
                break
    return len(pivots)


def points(n, degree):
    return [sum(1 << i for i in s) for size in range(min(n, degree)+1)
            for s in combinations(range(n), size)]


def evaluate(poly, x):
    return sum(bit for monomial, bit in poly.items()
               if x & monomial == monomial) & 1


def interpolate(values):
    coefficients = {}
    for m in sorted(values, key=lambda k: (k.bit_count(), k)):
        coefficients[m] = values[m] ^ evaluate(coefficients, m)
    return coefficients


class Teacher:
    def __init__(self, n, d, seed):
        self.n = n
        rng = random.Random(seed)
        while True:
            self.rows = [rng.getrandbits(n) for _ in range(n)]
            if rank(self.rows, n) == n:
                break
        self.offset = rng.getrandbits(n)
        self.g = [{m: rng.getrandbits(1) for m in points(i, d)} for i in range(n)]
        self.calls = 0

    def rank(self, x):
        u = sum((((row & x).bit_count() & 1) ^ (self.offset >> i & 1)) << i
                for i, row in enumerate(self.rows))
        value = 0
        for i, poly in enumerate(self.g):
            value = value*2+((u >> i & 1) ^ evaluate(poly, u))
        return value

    def compare(self, x, y):
        assert x != y
        self.calls += 1
        return int(self.rank(x) < self.rank(y))


def acquire(n, d, compare, rng, cap=24):
    suffix = [1 << i for i in range(n)]
    winners, polynomials = [], []
    accounting = Counter()
    for k in range(n):
        assert rank(winners+suffix, n) == n
        winner = suffix[0]
        for candidate in suffix[1:]:
            for _ in range(cap):
                x = rng.getrandbits(n)
                a = 1 ^ compare(x, x ^ candidate)
                b = 1 ^ compare(x, x ^ winner)
                accounting['matching'] += 2
                if a == b:
                    accounting['priority'] += 1
                    if compare(x ^ candidate, x ^ winner) == a:
                        winner = candidate
                    break
            else:
                return None, accounting
        values = {}
        for p in points(k, d):
            x = span(winners, p)
            values[p] = 1 ^ compare(x, x ^ winner)
            accounting['interpolation'] += 1
        poly = interpolate(values)
        row = []
        for v in suffix:
            if v == winner:
                row.append(1)
            else:
                row.append(values[0] ^ (1 ^ compare(v, v ^ winner)))
                accounting['response'] += 1
        pivot = suffix.index(winner)
        suffix = [v ^ (winner if row[i] else 0)
                  for i, v in enumerate(suffix) if i != pivot]
        winners.append(winner)
        polynomials.append(poly)
    assert rank(winners, n) == n
    return (winners, polynomials), accounting


def target_t(model, rank_value, prefix=None, free=0):
    basis, poly = model
    n = len(basis)
    k = n if prefix is None else prefix
    t = free << k
    for i in range(k):
        wanted = rank_value >> (k-i-1) & 1
        t |= (wanted ^ evaluate(poly[i], t & ((1 << i)-1))) << i
    return span(basis, t)


def check_decoder():
    cases = []
    for n, d in [(3,1),(4,1),(5,2),(6,2),(7,2),(8,2),
                 (4,3),(5,3),(7,3),(5,4),(6,4),(8,4)]:
        teacher = Teacher(n, d, 270000+n*100+d)
        model, counts = acquire(n, d, teacher.compare, random.Random(880000+n*100+d))
        assert model is not None
        D = sum(comb(n, j+1) for j in range(min(d,n-1)+1))
        P = comb(n,2)
        assert counts['interpolation'] == D and counts['response'] == P
        assert counts['priority'] == P and teacher.calls == sum(counts.values())
        # Enumerate all inverse ranks; a true permutation rank proves the
        # acquired inverse and forward model simultaneously on the whole cube.
        for desired in range(1 << n):
            assert teacher.rank(target_t(model, desired)) == desired
        prefix_seeds = 0
        for k in range(n+1):
            for prefix in range(1 << k):
                images = Counter(target_t(model, prefix, k, free)
                                 for free in range(1 << (n-k)))
                assert len(images) == 1 << (n-k) and set(images.values()) == {1}
                assert all(teacher.rank(x) >> (n-k) == prefix for x in images)
                prefix_seeds += sum(images.values())
        cases.append({'n':n,'d':d,'comparisons':teacher.calls,'D':D,
                      'P':P,'all_inverse_ranks':1<<n,
                      'all_prefix_target_suffix_seeds':prefix_seeds})
    # Identity order has different first exposed bits for basis e0 and e1.
    # Always picking x=e0 produces a mismatch, forcing explicit UNKNOWN.
    class FixedRandom:
        def getrandbits(self, n): return 1
    identity = lambda x,y: int(x<y)
    forced, counts = acquire(4,2,identity,FixedRandom(),cap=5)
    assert forced is None and counts['matching'] == 10
    return {'cases':cases,'forced_unknown':True,
            'total_complete_cases':len(cases),
            'scope':'Independent implementation, fixed PRNG seeds, finite all-rank and all-prefix enumeration; no priority or asymptotic validation.'}


def anf_degree(values, n):
    coeff = list(values)
    for i in range(n):
        for x in range(1 << n):
            if x >> i & 1:
                coeff[x] ^= coeff[x ^ (1 << i)]
    return max((m.bit_count() for m,c in enumerate(coeff) if c),default=-1)


def check_recognition():
    records = []
    for n in range(3,8):
        N = 1 << n
        for a in range(N//2):
            p = 2*a
            bad = [x ^ int(x//2 == a) for x in range(N)]
            assert sorted(bad) == list(range(N))
            differences = [(x,y) for x in range(N) for y in range(x+1,N)
                           if (bad[x] < bad[y]) != (x<y)]
            assert differences == [(p,p+1)]
            degree = anf_degree([v & 1 for v in bad],n)
            assert degree == n-1
            records.append({'n':n,'prefix':a,'only_changed_pair':[p,p+1],
                            'last_coordinate_degree':degree})
    # Exact Boolean degree is invariant under each invertible affine scramble.
    rng = random.Random(900011)
    affine_checks = 0
    for n in range(3,7):
        for _ in range(12):
            while True:
                rows = [rng.getrandbits(n) for _ in range(n)]
                if rank(rows,n) == n:break
            offset = rng.getrandbits(n)
            a = rng.randrange(1 << (n-1))
            values=[]
            for x in range(1 << n):
                u = sum(((row & x).bit_count() & 1) << j for j,row in enumerate(rows)) ^ offset
                values.append((u & 1) ^ int(u//2 == a))
            assert anf_degree(values,n) == n-1
            affine_checks += 1
    return {'adjacent_swap_cases':len(records),'records':records,
            'affine_degree_invariance_fixtures':affine_checks,
            'scope':'Exhaustive finite witnesses supplement the symbolic proof; exponential lower bound comes from transcript coupling, not finite enumeration.'}


def check_noise():
    fixtures=[]
    for rho in [Fraction(1,10),Fraction(1,4),Fraction(2,5)]:
        p = Fraction(1,2)-rho
        for r in [1,3,5,11,21,51]:
            exact=sum(Fraction(comb(r,j))*p**j*(1-p)**(r-j)
                      for j in range((r+1)//2,r+1))
            bound=exp(-2*r*float(rho)**2)
            assert float(exact) <= bound
            fixtures.append({'rho':str(rho),'repeats':r,
                             'exact_iid_majority_error':str(exact),
                             'hoeffding_bound':bound})
    correlated=Fraction(1,4)
    assert correlated > exp(-2*51*.25**2)
    return {'iid_binomial_fixtures':fixtures,
            'correlated_all_flip_marginal_error':str(correlated),
            'correlated_odd_majority_error':str(correlated),
            'scope':'Exact iid tails and a correlated-noise falsifier; no acquired physical noise model.'}


def check_prefix_vs_common_radical():
    def prefix(x):
        a,b,c = (x>>i & 1 for i in range(3))
        return a*4+b*2+(c^(a&b))
    counts=Counter(prefix(x) for x in range(16))
    assert set(counts.values()) == {2} and len(counts) == 8
    radical=[]
    for v in range(16):
        if all((prefix(x^v)^prefix(x)^prefix(v)^prefix(0)) == 0
               for x in range(16)):
            radical.append(v)
    assert radical == [0,4,8,12]
    image={prefix(v)^prefix(0) for v in radical}
    assert image == {0,1}
    return {'n':4,'prefix_bits':3,'fiber_counts':dict(counts),
            'common_radical_vectors':radical,'output_translation_image':sorted(image),
            'translation_rank':1,'required_right_inverse_rank':3,
            'scope':'Triangular prefix sampling still works when the sufficient common-radical certificate fails.'}


def main():
    result={'decoder':check_decoder(),'recognition':check_recognition(),
            'noise':check_noise(),'prefix_vs_common_radical':check_prefix_vs_common_radical(),
            'all_passed':True}
    Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'all_passed':True,'decoder_cases':result['decoder']['total_complete_cases'],
                      'recognition_cases':result['recognition']['adjacent_swap_cases'],
                      'affine_fixtures':result['recognition']['affine_degree_invariance_fixtures'],
                      'noise_fixtures':len(result['noise']['iid_binomial_fixtures'])}))


if __name__ == '__main__':main()
