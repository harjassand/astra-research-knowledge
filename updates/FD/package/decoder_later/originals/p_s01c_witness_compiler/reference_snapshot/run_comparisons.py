"""Bounded source-isolated fixtures; no large exponential verification.

Truth is accessible only in this driver, after the learner returns. Learners
receive a callback, dimensions, their stated promises and seeds. Output is
saved incrementally per case in this lane's directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import random
import time

import adaptive_compiler as ac

HERE = Path(__file__).resolve().parent


class Teacher:
    """Synthetic comparison source; its construction is not given to learner.

full: all n outputs quadratic, h=n-r partial flag. prefix_arbitrary: only
the requested first k outputs are quadratic; remaining rank suffix can be
ANY separately supplied bijection of the residual hidden coordinates inside
each prefix fiber. The explicit demonstration uses a prefix-dependent cubic
reversible gate, odd modular multiplication and addition. Future hidden
x-directions supply the same codimension-r exposure promise for learned bits.
"""
    def __init__(self, n, r, seed, prefix_length=None, suffix_permutation=None):
        start = time.perf_counter()
        self.n, self.r, self.h = n, r, n-r
        self.k = self.h if prefix_length is None else prefix_length
        self.prefix_arbitrary = prefix_length is not None
        rng = random.Random(seed)
        # Invertibility is by elementary row operations, with no search cap.
        self.rows = [1 << i for i in range(n)]
        for _ in range(12*n):
            if n > 1:
                i, j = rng.sample(range(n), 2)
                self.rows[i] ^= self.rows[j]
        self.offset = rng.getrandbits(n)
        self.hidden_q = []
        for i in range(self.k):
            allowed = list(range(i)) + list(range(self.h, n))
            lin, upper = 1 << i, [0]*n
            for j in allowed:
                lin ^= rng.getrandbits(1) << j
            for a, j in enumerate(allowed):
                for l in allowed[a+1:]:
                    upper[j] |= rng.getrandbits(1) << l
            self.hidden_q.append(ac.Quadratic(rng.getrandbits(1), lin, upper))
        self.suffix_rows = [1 << i for i in range(r)]
        for _ in range(12*r):
            if r > 1:
                i, j = rng.sample(range(r), 2)
                self.suffix_rows[i] ^= self.suffix_rows[j]
        self.suffix_offset = rng.getrandbits(r)
        self.suffix_permutation = suffix_permutation or self._demo_suffix
        self.calls = self.rank_requests = self.fresh_ranks = 0
        self.cache = {}
        self.query_seconds = 0.0
        self.setup_seconds = time.perf_counter()-start
        self.seed = seed

    @staticmethod
    def _demo_suffix(t, prefix, m):
        if m >= 4:
            t ^= (((t >> 1) & 1) & ((t >> 2) & 1) & ((t >> 3) & 1))
        # Odd multiplication and addition are permutations modulo 2^m.
        a = 5 + 2*(prefix & 15)
        b = (0x9e3779b97f4a7c15*(prefix+1)) & ((1 << m)-1)
        return (a*t+b) & ((1 << m)-1)

    def rank(self, x):
        self.rank_requests += 1
        if x not in self.cache:
            self.fresh_ranks += 1
            u = ac.linear(self.rows, x) ^ self.offset
            prefix = 0
            for q in self.hidden_q:
                prefix = (prefix << 1) | q(u)
            if self.prefix_arbitrary:
                m = self.n-self.k
                suffix = self.suffix_permutation(u >> self.k, prefix, m)
                value = (prefix << m) | suffix
            else:
                z = u >> self.h
                if self.r >= 3:
                    z ^= (((z >> 1) & 1) & ((z >> 2) & 1))
                z = ac.linear(self.suffix_rows, z) ^ self.suffix_offset
                suffix = 0
                for j in range(self.r):
                    suffix = (suffix << 1) | ((z >> j) & 1)
                value = (prefix << self.r) | suffix
            self.cache[x] = value
        return self.cache[x]

    def query(self, x, y):
        start = time.perf_counter()
        self.calls += 1
        value = self.rank(x) < self.rank(y)
        self.query_seconds += time.perf_counter()-start
        return value

    def source_receipt(self):
        q = self.calls
        return dict(source="synthetic exact chosen-pair comparator", seed=self.seed,
                    comparison_calls=q, rank_requests=self.rank_requests,
                    fresh_rank_evaluations=self.fresh_ranks, cached_points=len(self.cache),
                    rank_cache_logical_payload_bits=2*self.n*len(self.cache),
                    query_argument_bits=2*self.n*q, comparison_answer_bits=q,
                    source_setup_seconds=self.setup_seconds,
                    measured_comparison_callback_seconds=self.query_seconds,
                    rank_boolean_work_conservative_upper=self.fresh_ranks*(8*self.n**3+8*self.n**2),
                    source_class_supplied=True, real_source_class_acquisition="UNKNOWN",
                    physical_fair_entropy="not acquired; seeded Python PRNG finite replay")


def truth_bodies(teacher, count):
    values = [dict() for _ in range(count)]
    for x in ac.coefficient_points(teacher.n):
        rank = teacher.rank(x)
        for i in range(count):
            values[i][x] = (rank >> (teacher.n-i-1)) & 1
    return [ac.interpolate(v, teacher.n) for v in values]


def partial_flag_algebra(teacher, truth, h):
    inv = ac.matrix_inverse(teacher.rows, teacher.n)
    raw_flag = [ac.linear(inv, 1 << i) for i in range(teacher.h)]
    for i, q in enumerate(truth[:h]):
        assert q.toggles(raw_flag[i])
        assert all(q.translation_invariant(v) for v in raw_flag[i+1:])
        assert all(old.translation_invariant(raw_flag[i]) for old in truth[:i])
    return dict(known_source_flag_verified_after_return=True,
                learned_prefix_length=h, latent_partial_flag_length=teacher.h,
                future_latent_flag_vectors_preserve_learned_prefix=True)


def complete_extension(model, n):
    previous, toggles = [], []
    for i, q in enumerate(model):
        S = ac.common_stabilizer(previous, n)
        polar = q.polar()
        columns = [ac.linear(polar, s) for s in S]
        equations = [sum(((image >> j) & 1) << a for a, image in enumerate(columns))
                     for j in range(n)]
        radical = [ac.combine(S, a) for a in ac.kernel(equations, len(S))]
        v = next((v for v in radical if (q(v) ^ q.constant)), None)
        if v is None:
            return dict(complete_flag=False, first_missing_stage=i,
                        method="global polar-kernel and affine-response algebra; no span enumeration")
        assert q.toggles(v) and all(old.translation_invariant(v) for old in previous)
        previous.append(q)
        toggles.append(v)
    return dict(complete_flag=True, toggle_count=len(toggles))


def verify_model(teacher, result, model, prefix, n, r, prefix_length):
    start = time.perf_counter()
    acquisition_calls, acquisition_fresh = teacher.calls, teacher.fresh_ranks
    count = n if prefix_length is None else prefix_length
    truth = truth_bodies(teacher, count)
    equal = [q.body() == t.body() for q, t in zip(model, truth)]
    assert len(equal) == count and all(equal)
    body_fresh = teacher.fresh_ranks-acquisition_fresh
    result["coefficient_check"] = dict(bodies=count, anchors_per_body=ac.M2(n),
                                      exact_body_equalities=sum(equal), all_equal=True,
                                      source_truth_access="post-return coordinate ranks only")
    result["source_promise_check"] = partial_flag_algebra(teacher, truth, len(prefix.q))
    # Retained own-toggles certify this intersection on arbitrary histories.
    combined = ac.echelon(prefix.toggles+prefix.stabilizer, n)[0]
    assert len(combined) == len(prefix.toggles)+len(prefix.stabilizer)
    result["candidate_geometry_check"] = dict(toggle_count=len(prefix.toggles),
                                              stabilizer_dimension=len(prefix.stabilizer),
                                              intersection_zero_by_exact_rank=True)
    meter = ac.Meter()
    rng = random.Random(teacher.seed+7770000)
    checked_prefixes = sorted({0, 1, len(prefix.q)//2, len(prefix.q)})
    checked_prefixes = [k for k in checked_prefixes if k <= len(prefix.q)]
    samplers = []
    for k in checked_prefixes:
        qs, ws = prefix.q[:k], prefix.toggles[:k]
        S = ac.common_stabilizer(qs, n, meter)
        sampler = ac.CompactPrefixSampler(qs, ws, S, n, meter)
        assert k <= sampler.d <= k+r
        factor_ok, bodies = sampler.factor_coefficient_check(qs)
        assert factor_ok and bodies == k
        targets = sorted({0, (1 << k)-1, rng.getrandbits(k)})
        seeds = [rng.getrandbits(n-k) for _ in range(16)]
        for target in targets:
            outputs = [sampler.sample_from_seed(target, s) for s in seeds]
            for x in outputs:
                true_prefix = teacher.rank(x) >> (n-k)
                assert true_prefix == target and sampler.prefix(x) == target
            assert len(set(outputs)) == len(set(seeds))
        samplers.append(dict(**sampler.payload(), exact_factor_coefficient_check=True,
                             tested_targets=len(targets), tested_seeds_per_target=len(seeds),
                             tested_seed_collisions=0))
    result["compact_execution"] = samplers
    points = sorted({0, (1 << n)-1} | {rng.getrandbits(n) for _ in range(256)})
    if prefix_length is None:
        compiled = ac.CompiledModel(model, prefix.toggles, n, r, meter)
        assert all(compiled.rank(x) == teacher.rank(x) for x in points)
        targets = sorted({0, (1 << n)-1} | {rng.getrandbits(n) for _ in range(64)})
        for target in targets:
            hits = compiled.inverse(target)
            assert len(hits) == 1 and teacher.rank(hits[0]) == target
        result["execution_check"] = dict(rank_points=len(points), rank_errors=0,
                                         inverse_targets=len(targets), inverse_errors=0,
                                         enumerated_points_per_inverse=1 << r,
                                         source_comparisons_during_execution=teacher.calls-acquisition_calls,
                                         full_cube_enumeration=False)
        result["complete_class_membership"] = complete_extension(truth, n)
    else:
        sampler = prefix.sampler()
        assert all(sampler.prefix(x) == teacher.rank(x) >> (n-prefix_length) for x in points)
        result["execution_check"] = dict(prefix_rank_points=len(points), prefix_errors=0,
                                         source_comparisons_during_execution=teacher.calls-acquisition_calls,
                                         full_cube_enumeration=False,
                                         arbitrary_suffix_fitted=False,
                                         suffix_quadratic_promise_required=False)
        # A finite explicit nonquadratic suffix witness, with a fixed prefix.
        m = n-prefix_length
        witness = None
        if m >= 4:
            for prefix_target in range(min(1 << prefix_length, 8)):
                for bit in range(min(m, 16)):
                    third = 0
                    for mask in range(8):
                        t = (((mask >> 0) & 1) << 1) | (((mask >> 1) & 1) << 2) | (((mask >> 2) & 1) << 3)
                        third ^= (teacher.suffix_permutation(t, prefix_target, m) >> bit) & 1
                    if third:
                        witness = dict(prefix=prefix_target, residual_output_bit=bit,
                                       third_derivative_directions=[1,2,3], third_derivative=1)
                        break
                if witness:
                    break
        assert witness is not None
        result["arbitrary_suffix_nonquadratic_witness"] = witness
    assert teacher.calls == acquisition_calls
    result["verification"] = dict(body_truth_fresh_ranks=body_fresh,
                                  total_fresh_ranks=teacher.fresh_ranks-acquisition_fresh,
                                  truth_comparisons=0, limited_sample_checks=True,
                                  local_operations=dict(meter.ops),
                                  seconds_including_external_truth=time.perf_counter()-start)
    return result


def run_case(n, r, seed, mode, prefix_length=None, beta=None):
    beta = n**-2 if beta is None else beta
    teacher = Teacher(n, r, seed, prefix_length)
    result, model, prefix = ac.acquire(n, r, teacher.query, seed+1000000,
                                       beta, prefix_length, mode)
    result["case"] = dict(n=n, r=r, seed=seed, mode=mode, prefix_length=prefix_length, beta=beta)
    result["source"] = teacher.source_receipt()
    result["learner_local_seconds_estimate"] = max(0.0, result["acquisition_seconds"]-teacher.query_seconds)
    if model is not None:
        result = verify_model(teacher, result, model, prefix, n, r, prefix_length)
    result["logical_output_bits"] = len(model or [])*ac.M2(n)+len(prefix.toggles)*n
    result["semantic_status"] = "Monte Carlo under supplied promise; successful finite receipt does not recognize the class"
    return result


def complete_tournament(n, query, seed, beta):
    """Earlier exact-on-completion complete-class compact control.

Same algorithm as root_ordinal/triangular_compact.py. Used only on a source
with r=0, where the stronger complete hidden-triangular promise is supplied.
"""
    pairs = n*(n-1)//2
    cap = max(0, math.ceil(math.log2(pairs/beta))) if pairs else 0
    rng, source = random.Random(seed), ac.Source(query)
    basis, functions, subspace = [], [], [1 << i for i in range(n)]
    meter = ac.Meter()
    start = time.perf_counter()
    for k in range(n):
        winner = subspace[0]
        source.phase = "tournament_matches"
        for v in subspace[1:]:
            for _ in range(cap):
                x = rng.getrandbits(n)
                meter.add("random_input_bits", n)
                a = 1 ^ source(x, x ^ v)
                b = 1 ^ source(x, x ^ winner)
                if a == b:
                    break
            else:
                return dict(status="UNKNOWN_MATCH_CAP", comparison_calls=source.calls), None
            if bool(source(x ^ v, x ^ winner)) == bool(a):
                winner = v
        source.phase = "compact_interpolation"
        values = {a: 1 ^ source(ac.combine(basis,a), ac.combine(basis,a) ^ winner)
                  for a in ac.coefficient_points(k)}
        functions.append(ac.interpolate(values, k, meter))
        source.phase = "linear_response"
        constant, row = values[0], 0
        for j, v in enumerate(subspace):
            response = 1 if v == winner else constant ^ (1 ^ source(v, v ^ winner))
            row |= response << j
        if not row:
            return dict(status="UNKNOWN_RESPONSE", comparison_calls=source.calls), None
        basis.append(winner)
        subspace = [ac.combine(subspace, a) for a in ac.kernel([row],len(subspace),meter)]
    basis_rows = [sum(((basis[j] >> i) & 1) << j for j in range(n)) for i in range(n)]
    coordinates = ac.matrix_inverse(basis_rows, n, meter)
    def rank(x):
        t, out = ac.linear(coordinates, x, meter), 0
        for i, f in enumerate(functions):
            out = (out << 1) | (((t >> i) & 1) ^ f(t & ((1 << i)-1), meter))
        return out
    out = dict(status="EXACT_ON_COMPLETION_UNDER_SUPPLIED_COMPLETE_CLASS",
               comparison_calls=source.calls, source_calls_by_phase=dict(source.by_phase),
               expected_comparison_bound=ac.D(n)+6*pairs,
               worst_comparison_bound=ac.D(n)+(2*cap+2)*pairs,
               unknown_bound=pairs*2.0**(-cap), completed_semantic_error_under_promise=0,
               acquisition_seconds=time.perf_counter()-start,
               local_operations=dict(meter.ops), coefficient_output_bits=ac.D(n),
               basis_bits=n*n, inverse_basis_bits=n*n,
               model=dict(basis=basis, functions=[f.body() for f in functions]))
    assert source.calls <= out["worst_comparison_bound"]
    return out, rank


def run_complete_control(n, seed, beta=None):
    beta = n**-2 if beta is None else beta
    teacher = Teacher(n, 0, seed)
    out, rank = complete_tournament(n, teacher.query, seed+1000000, beta)
    out["source"] = teacher.source_receipt()
    out["case"] = dict(n=n, r=0, seed=seed, mode="complete_tournament", beta=beta)
    if rank is not None:
        start, fresh = time.perf_counter(), teacher.fresh_ranks
        truth = truth_bodies(teacher,n)
        model = [ac.interpolate({x:(rank(x)>>(n-i-1))&1 for x in ac.coefficient_points(n)},n)
                 for i in range(n)]
        assert [q.body() for q in truth] == [q.body() for q in model]
        points = [random.Random(seed+j).getrandbits(n) for j in range(256)]
        assert all(rank(x) == teacher.rank(x) for x in points)
        out["verification"] = dict(all_raw_bodies_equal=True, body_count=n,
                                    sampled_rank_points=len(points), errors=0,
                                    fresh_truth_ranks=teacher.fresh_ranks-fresh,
                                    seconds=time.perf_counter()-start,
                                    full_cube_enumeration=False)
    return out


def tiny_fixtures():
    queried = []
    result, model, _ = ac.acquire(8,2,lambda x,y:queried.append((x,y)),123,beta=.1,force_zero_directions=True)
    assert result["status"] == "UNKNOWN" and model is None and not queried
    n=6
    q=ac.Quadratic(0,1,[0,4,0,0,0,0])
    S=ac.common_stabilizer([q],n)
    sampler=ac.CompactPrefixSampler([q],[1],S,n)
    assert sampler.d == 3
    for target in (0,1):
        outputs=[sampler.sample_from_seed(target,s) for s in range(1 << (n-1))]
        assert len(set(outputs)) == 1 << (n-1)
        assert all(q(x)==target for x in outputs)
    ok, count=sampler.factor_coefficient_check([q])
    assert ok and count==1
    # Deliberately nonquadratic true next bit, but a strict total-order source.
    # The chosen s=e1,t=e2+e3 has a nonzero cheap witness and zero full row.
    # This must abort UNKNOWN on the first duplicate/nonincreasing row.
    class ForcedTape:
        def __init__(self, values):
            self.values=iter(values)
        def getrandbits(self, size):
            return next(self.values)
    def cubic_rank(x):
        q=(x&1)^(((x>>1)&1)&((x>>2)&1)&((x>>3)&1))
        return (q<<3)|(x>>1)
    bad_source=ac.Source(lambda x,y:cubic_rank(x)<cubic_rank(y))
    bad_cfg=ac.parameters(4,2,.1)
    bad, bad_receipt=ac._candidate_adaptive(4,0,2,1,ac.AcquiredPrefix(4),bad_source,
                                           ForcedTape([2,12]),bad_cfg,ac.Meter())
    assert bad is None and bad_receipt["reason"]=="detected_polar_row_not_new"
    assert bad_source.calls==12
    # Missed image remains semantic error: a forced all-zero polar tape can
    # return x0 for x0+x2*x3, even though the exact own-toggle gate passes.
    qtrue=ac.Quadratic(0,1,[0,0,8,0])
    def missed_rank(x):
        return (qtrue(x)<<3)|(x>>1)
    missed_source=ac.Source(lambda x,y:missed_rank(x)<missed_rank(y))
    missed, missed_receipt=ac._candidate_adaptive(4,0,2,1,ac.AcquiredPrefix(4),missed_source,
             ForcedTape([0]*(2*bad_cfg["L"])),bad_cfg,ac.Meter())
    assert missed is not None and missed.toggles(1)
    errors=sum(missed(x)!=qtrue(x) for x in range(16))
    assert errors==4
    return dict(forced_zero_cap=dict(status=result["status"],reason=result["reason"],
                                     attempted_directions=len(result["stages"][0]["trials"]),
                                     source_queries=0,guessed_model=False),
                compact_sharp_fixture=dict(n=n,k=1,r=2,d=sampler.d,
                                           exact_uniform_seed_bijections=True,
                                           tested_total_seeds=1 << n,
                                           entropy_bits=n-1,
                                           factor_coefficient_check=True),
                nonquadratic_duplicate_row=dict(status="UNKNOWN",reason=bad_receipt["reason"],
                                                actual_comparison_source=True,comparison_calls=bad_source.calls),
                forced_missed_image=dict(accepted_wrong_candidate=True,own_toggle_passes=True,
                                         exact_error_numerator=errors,exact_domain_size=16,
                                         miss_budget_must_remain=True,forced_tape_is_not_uniform_run=True,
                                         comparison_calls=missed_source.calls,
                                         nondetection_cap=bad_cfg["L"]))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--case",default="16:2:920162")
    parser.add_argument("--modes",default="adaptive,fixed_j,raw_pair")
    parser.add_argument("--prefix-k",type=int)
    parser.add_argument("--beta",type=float)
    parser.add_argument("--complete-control",action="store_true")
    parser.add_argument("--output")
    args=parser.parse_args()
    n,r,seed=map(int,args.case.split(":"))
    label=f"n{n}_r{r}_seed{seed}"+(f"_prefix{args.prefix_k}" if args.prefix_k is not None else "")
    path=Path(args.output) if args.output else HERE/f"receipt_{label}.json"
    if not path.resolve().is_relative_to(HERE):
        raise ValueError("write only inside this lane directory")
    receipt=dict(scope="comparison-only synthetic promised source; no novelty/physical-source/mission claim",
                 cases=[],tiny_fixtures=tiny_fixtures(),sources={})
    for filename in ("adaptive_compiler.py","fixed_j_core.py","run_comparisons.py"):
        receipt["sources"][filename]=hashlib.sha256((HERE/filename).read_bytes()).hexdigest()
    for mode in filter(None,args.modes.split(",")):
        case=run_case(n,r,seed,mode,args.prefix_k,args.beta)
        receipt["cases"].append(case)
        path.write_text(json.dumps(receipt,indent=2)+"\n")
        print(json.dumps(dict(n=n,r=r,mode=mode,status=case["status"],
                              comparisons=case["comparison_calls"],
                              source_fresh_ranks=case["source"]["fresh_rank_evaluations"],
                              acquisition_seconds=round(case["acquisition_seconds"],3),
                              bodies_equal=case.get("coefficient_check",{}).get("all_equal"))),flush=True)
    if args.complete_control:
        assert r==0 and args.prefix_k is None
        case=run_complete_control(n,seed,args.beta)
        receipt["cases"].append(case)
        path.write_text(json.dumps(receipt,indent=2)+"\n")
        print(json.dumps(dict(n=n,r=0,mode="complete_tournament",status=case["status"],
                              comparisons=case["comparison_calls"],
                              acquisition_seconds=round(case.get("acquisition_seconds",0),3))),flush=True)


if __name__ == "__main__":
    main()
