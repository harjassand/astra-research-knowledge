"""Exact finite checks and executable calibrated DNF coverage sampler.

All confidence claims concern ideal independent randomness. random.Random is
used only for a reproducible diagnostic. The product-form and coverage
estimators are established methods; see RESULT.md for provenance and scope.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
from random import Random
from pathlib import Path
import json
import time


def atoms(d):
    return list(product((0, 1), repeat=d))


def product_mass(x, probs):
    out = F(1)
    for bit, p in zip(x, probs):
        out *= p if bit else 1 - p
    return out


def low_order_alternative(d, k, a, eta=F(1)):
    """P0 product; P1 has same <=k marginals and (1+eta) target mass."""
    assert 0 <= k < d and 0 < a <= F(1, 2) and 0 < eta <= 1
    r = k + 1
    p = a**d
    p0, p1 = {}, {}
    for x in atoms(d):
        base = product_mass(x, [a] * d)
        perturb = F(0)
        if all(x[:d-r]):
            perturb = eta * p * (-1)**sum(1-v for v in x[d-r:])
        p0[x], p1[x] = base, base + perturb
    return p0, p1


def marginal(law, subset):
    out = {}
    for x, p in law.items():
        key = tuple(x[j] for j in subset)
        out[key] = out.get(key, F(0)) + p
    return out


def exact_obstruction_checks():
    checks, rows = 0, []
    for d in (3, 5, 7):
        for k in range(min(3, d-1) + 1):
            for a in (F(1, 4), F(1, 2)):
                for eta in (F(1, 3), F(1)):
                    p0, p1 = low_order_alternative(d, k, a, eta)
                    assert sum(p1.values()) == 1 and min(p1.values()) >= 0
                    assert p1[(1,)*d] == (1+eta)*a**d
                    for order in range(k+1):
                        for subset in combinations(range(d), order):
                            assert marginal(p0, subset) == marginal(p1, subset)
                            checks += 1
                    chi2 = sum((p1[x]-p0[x])**2/p0[x] for x in p0)
                    expected = eta**2*a**d/(1-a)**(k+1)
                    assert chi2 == expected
                    rows.append({"d":d,"k":k,"a":str(a),"eta":str(eta),
                                 "chi2":str(chi2),"event_p":str(a**d)})
    return {"exact_marginal_equalities_checked":checks, "models":rows}


def kernel_alternative(d, k, a, eta=F(1)):
    """Minimum-chi-square high-order perturbation; verify positivity gate."""
    assert 0 <= k < d and 0 < a <= F(1,2) and 0 < eta <= 1
    b = (1-a)/a
    low_diagonal = sum(F(comb(d,j))*b**j for j in range(k+1))
    high_diagonal = a**(-d)-low_diagonal
    assert eta*low_diagonal <= high_diagonal
    p0, p1 = {}, {}
    for x in atoms(d):
        terms = [b if bit else F(-1) for bit in x]
        # Coefficients of product_j(1+t_j z), retaining degree <= k.
        coefficients = [F(1)] + [F(0)]*k
        for term in terms:
            for j in range(k,0,-1):
                coefficients[j] += term*coefficients[j-1]
        low_kernel = sum(coefficients)
        high_kernel = (a**(-d) if all(x) else F(0))-low_kernel
        p0[x] = product_mass(x,[a]*d)
        p1[x] = p0[x]*(1+eta*high_kernel/high_diagonal)
    return p0,p1,high_diagonal


def exact_kernel_checks():
    rows, checks = [], 0
    for d in (3,5,7):
        for a in (F(1,4),F(1,2)):
            for k in range(d):
                diagonal = sum(F(comb(d,j))*((1-a)/a)**j for j in range(k+1))
                if 2*diagonal > a**(-d):
                    continue
                p0,p1,K = kernel_alternative(d,k,a)
                assert sum(p1.values()) == 1 and min(p1.values()) >= 0
                assert p1[(1,)*d] == 2*a**d
                for order in range(k+1):
                    for subset in combinations(range(d),order):
                        assert marginal(p0,subset) == marginal(p1,subset)
                        checks += 1
                chi2 = sum((p1[x]-p0[x])**2/p0[x] for x in p0)
                assert chi2 == 1/K and chi2 <= 2*a**d
                rows.append({"d":d,"k":k,"a":str(a),"chi2":str(chi2),
                             "chi2_over_event_probability":str(chi2/a**d)})
    return {"exact_marginal_equalities_checked":checks,"models":rows}


class CompactKernelLaw:
    """Polynomial-size exact evaluator and rejection sampler for Theorem 1."""
    def __init__(self,d,k,a):
        assert 0<=k<d and 0<a<=F(1,2)
        self.d,self.k,self.a = d,k,a
        self.b = (1-a)/a
        self.D = sum(F(comb(d,j))*self.b**j for j in range(k+1))
        self.K = a**(-d)-self.D
        assert self.D<=self.K
        self.trials = self.samples = 0

    def likelihood_ratio(self,x):
        assert len(x)==self.d and all(v in (0,1) for v in x)
        coefficients = [F(1)]+[F(0)]*self.k
        for bit in x:
            term = self.b if bit else F(-1)
            for j in range(self.k,0,-1):
                coefficients[j] += term*coefficients[j-1]
        L = sum(coefficients)
        H = (self.a**(-self.d) if all(x) else F(0))-L
        ratio = 1+H/self.K
        assert 0<=ratio<=2
        return ratio

    def sample(self,rng):
        while True:
            self.trials += 1
            x = tuple(int(rng.randrange(self.a.denominator)<self.a.numerator)
                      for _ in range(self.d))
            accept = self.likelihood_ratio(x)/2
            if rng.randrange(accept.denominator)<accept.numerator:
                self.samples += 1
                return x


def compact_kernel_diagnostic():
    law = CompactKernelLaw(80,40,F(1,4))
    rng = Random(82726)
    for _ in range(20):
        law.sample(rng)
    assert law.likelihood_ratio((1,)*80)==2
    return {"d":80,"k":40,"a":"1/4","samples":law.samples,
            "rejection_proposals":law.trials,"expected_proposals_per_sample":2,
            "target_probability_under_P0":str(F(1,4)**80),
            "chi2":str(1/law.K),"K_numerator_bits":law.K.numerator.bit_length(),
            "all_ones_likelihood_ratio":2,
            "sample_count_is_not_a_distributional_test":True}


def empirical_pair_factor(x, y, p, n):
    return 1 + ((F(1, p if x else 1-p) if x == y else 0) - 1)/n


def exact_product_checks():
    d, n, probs = 3, 2, [F(1, 3), F(1, 4), F(2, 5)]
    space = atoms(d)
    masses = [product_mass(x, probs) for x in space]
    pair = {}
    for ix, x in enumerate(space):
        for iy, y in enumerate(space):
            val = masses[ix]*masses[iy]
            for j in range(d):
                val *= empirical_pair_factor(x[j], y[j], probs[j], n)
            pair[ix, iy] = val
    bound = F(1)
    for p in probs:
        bound *= 1 + (1/min(p, 1-p)-1)/n
    largest, maximizing = F(0), None
    for mask in range(1, 1 << len(space)):
        active = [i for i in range(len(space)) if mask >> i & 1]
        mean = sum(masses[i] for i in active)
        moment = sum(pair[i,j] for i in active for j in active)
        ratio = moment/mean**2
        assert ratio <= bound
        if ratio > largest:
            largest, maximizing = ratio, mask
    assert largest == bound

    # Independent explicit empirical-data enumeration for a nontrivial DNF.
    def f(x):
        return (x[0] and x[1]) or (x[1] and not x[2])
    true = sum(product_mass(x, probs) for x in space if f(x))
    first = second = F(0)
    for counts in product(range(n+1), repeat=d):
        probability = F(1)
        for j, c in enumerate(counts):
            p = probs[j]
            probability *= comb(n,c)*p**c*(1-p)**(n-c)
        phat = [F(c,n) for c in counts]
        value = sum(product_mass(x, phat) for x in space if f(x))
        first += probability*value
        second += probability*value**2
    assert first == true

    # Exact Hoeffding/ANOVA projections under the true product measure.
    projections, components = {}, {}
    subsets = [s for size in range(d+1) for s in combinations(range(d),size)]
    for subset in subsets:
        for x in space:
            total = F(0)
            for y in space:
                if all(y[j] == x[j] for j in subset):
                    weight = F(1)
                    for j in range(d):
                        if j not in subset:
                            weight *= probs[j] if y[j] else 1-probs[j]
                    total += f(y)*weight
            projections[subset,x] = total
            proper = [t for t in subsets if len(t)<len(subset) and set(t)<=set(subset)]
            components[subset,x] = total-sum(components[t,x] for t in proper)
    variance = F(0)
    for subset in subsets[1:]:
        norm2 = sum(product_mass(x,probs)*components[subset,x]**2 for x in space)
        variance += norm2/n**len(subset)
    assert second-true**2 == variance
    return {"all_nonempty_events_checked":255,"sharp_bound":str(bound),
            "attained_bound":str(largest),"maximizer_event_mask":maximizing,
            "dnf_mean":str(true),"dnf_variance":str(variance),
            "anova_equals_enumeration":True}


class EmpiricalDNFSampler:
    """Karp-Luby reciprocal-coverage estimator under empirical product law.

    Clauses are dict coordinate -> required bit; full coverage is counted.
    This intentionally simple sampler is not KLM's faster self-adjusting code.
    """
    def __init__(self, counts, n, clauses):
        assert n >= 1 and all(0 <= c <= n for c in counts)
        self.counts, self.n = tuple(counts), n
        self.d, self.clauses = len(counts), tuple(dict(c) for c in clauses)
        assert all(c and all(0<=j<self.d and v in (0,1) for j,v in c.items())
                   for c in self.clauses)
        self.width = max((len(c) for c in self.clauses), default=0)
        self.denominator = n**self.width
        self.weights = []
        self.literal_reads = 0
        for clause in self.clauses:
            weight = n**(self.width-len(clause))
            for j,v in clause.items():
                weight *= counts[j] if v else n-counts[j]
                self.literal_reads += 1
            self.weights.append(weight)
        self.total = sum(self.weights)
        self.draws = self.coordinate_draws = self.coverage_literal_tests = 0

    def sample(self, rng):
        self.draws += 1
        if self.total == 0:
            return F(0)
        index = rng.randrange(self.total)
        clause = None
        for candidate, weight in zip(self.clauses, self.weights):
            if index < weight:
                clause = candidate
                break
            index -= weight
        assert clause is not None
        x = []
        for j,c in enumerate(self.counts):
            if j in clause:
                x.append(clause[j])
            else:
                x.append(int(rng.randrange(self.n)<c))
                self.coordinate_draws += 1
        multiplicity = 0
        for mode in self.clauses:
            hit = True
            for j,v in mode.items():
                self.coverage_literal_tests += 1
                if x[j] != v:
                    hit = False
                    break
            multiplicity += hit
        assert multiplicity >= 1
        return F(self.total, self.denominator*multiplicity)


def dnf_probability_inclusion_exclusion(probs, clauses):
    # Small-M comparator/reference; exponential in M, never charged as free.
    total = F(0)
    for size in range(1,len(clauses)+1):
        sign = 1 if size % 2 else -1
        for chosen in combinations(clauses,size):
            literals, conflict = {}, False
            for clause in chosen:
                for j,v in clause.items():
                    if j in literals and literals[j] != v:
                        conflict = True
                    literals[j] = v
            if conflict:
                continue
            term = F(1)
            for j,v in literals.items():
                term *= probs[j] if v else 1-probs[j]
            total += sign*term
    return total


def diagnostic(groups=60):
    import numpy as np
    # Fixed synthetic reliability DNF. Common core makes this an easy scoped
    # diagnostic, and is explicitly not a frontier benchmark.
    d, n, inner = 48, 4096, 64
    probs = [F(1,4)]*d
    common = {j:1 for j in range(36)}
    tails = [(0,1,2),(2,3,4),(4,5,6),(6,7,8),
             (8,9,10),(9,10,11),(0,5,10),(1,6,11)]
    clauses = [common | {36+j:1 for j in tail} for tail in tails]
    t0 = time.perf_counter()
    exact = dnf_probability_inclusion_exclusion(probs, clauses)
    reference_seconds = time.perf_counter()-t0
    rng, data_rng = Random(20261010), np.random.default_rng(20261010)
    values, plugins, inner_variants = [], [], []
    coord_draws = literal_tests = preprocess = 0
    max_weight_bits = 0
    t0 = time.perf_counter()
    for _ in range(groups):
        # Binomial counts simulate the sufficient statistic exactly in law;
        # logical raw observation count remains n*d per independent group.
        counts = [int(x) for x in data_rng.binomial(n,0.25,size=d)]
        sampler = EmpiricalDNFSampler(counts,n,clauses)
        samples = [sampler.sample(rng) for _ in range(inner)]
        values.append(float(sum(samples,F(0))/inner/exact))
        plugin = dnf_probability_inclusion_exclusion([F(c,n) for c in counts],clauses)
        plugins.append(float(plugin/exact))
        inner_variants.append(float(sum((w-plugin)**2 for w in samples)/inner/exact**2))
        coord_draws += sampler.coordinate_draws
        literal_tests += sampler.coverage_literal_tests
        preprocess += sampler.literal_reads
        max_weight_bits = max(max_weight_bits, sampler.total.bit_length(),sampler.denominator.bit_length())
    elapsed = time.perf_counter()-t0
    M = len(clauses)
    B = F((M+1)**2,4*M)
    C = (1+F(3,n))**d
    # Verify exact finite sampler means by enumerating small product support.
    small = EmpiricalDNFSampler([1,2,3],4,[{0:1,1:1},{1:1,2:0}])
    psmall = [F(c,4) for c in small.counts]
    mu = second = F(0)
    for x in atoms(3):
        cover = sum(all(x[j]==v for j,v in c.items()) for c in small.clauses)
        if cover:
            q = product_mass(x,psmall)*cover/F(small.total,small.denominator)
            w = F(small.total,small.denominator*cover)
            mu += q*w
            second += q*w*w
    expected = dnf_probability_inclusion_exclusion(psmall,small.clauses)
    assert mu == expected and second <= F(9,8)*expected**2
    zero = EmpiricalDNFSampler([0,0],4,[{0:1},{1:1}])
    assert zero.sample(rng) == 0
    return {"d":d,"modes":M,"width":39,"n_full_vector_observations_per_group":n,
            "independent_groups":groups,"inner_draws_per_group":inner,
            "event_probability_exact":str(exact),"event_probability":float(exact),
            "logical_component_observations":groups*n*d,
            "logical_full_vector_observations":groups*n,
            "expected_passive_event_hits_in_all_logical_vectors":float(groups*n*exact),
            "coverage_samples":groups*inner,"conditional_coordinate_draws":coord_draws,
            "coverage_literal_tests":literal_tests,"preprocess_literal_reads":preprocess,
            "maximum_integer_weight_bits":max_weight_bits,
            "analytic_calibration_second_moment_bound":float(C),
            "analytic_inner_second_moment_bound":float(B),
            "analytic_combined_relative_variance_bound":float(C*(1+(B-1)/inner)-1),
            "empirical_normalized_mean":float(np.mean(values)),
            "empirical_normalized_variance":float(np.var(values,ddof=1)),
            "empirical_plugin_normalized_variance":float(np.var(plugins,ddof=1)),
            "empirical_mean_inner_variance_in_true_p_units":float(np.mean(inner_variants)),
            "reference_inclusion_exclusion_terms":2**M-1,
            "reference_seconds":reference_seconds,"total_diagnostic_seconds":elapsed,
            "runtime_includes_per_group_exact_plugin_comparator":True,
            "empirical_receipts_are_not_certificates":True,
            "sampler_small_exact_mean_and_zero_case_passed":True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--groups",type=int,default=60)
    parser.add_argument("--output",default=str(Path(__file__).with_name("results.json")))
    args = parser.parse_args()
    out = {"obstruction":exact_obstruction_checks(),"kernel_obstruction":exact_kernel_checks(),
           "compact_kernel_sampler":compact_kernel_diagnostic(),
           "product_form":exact_product_checks(),"diagnostic":diagnostic(args.groups)}
    Path(args.output).write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"output":args.output,"marginal_checks":out["obstruction"]["exact_marginal_equalities_checked"],
                      "all_event_checks":out["product_form"]["all_nonempty_events_checked"],
                      "diagnostic":out["diagnostic"]},indent=2))


if __name__ == "__main__":
    main()
