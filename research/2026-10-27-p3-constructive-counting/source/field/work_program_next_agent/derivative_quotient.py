#!/usr/bin/env python3
"""Acquire all directions whose additive derivative is affine.

Exact sparse-ANF construction. It does not infer a degree promise from value
queries to an unrestricted circuit. Gaussian leaves below are evaluated by
an independent finite exhaustive backend, clearly labelled in the result.
"""
from itertools import combinations
import json
from pathlib import Path
import random

from field_acquisition_audit import kernel, linear_apply, rank


def eval_poly(poly, x):
    return sum((x & m) == m for m in poly) & 1


def derivative(poly, a):
    out = set(poly)
    for monomial in poly:
        shift = monomial & a
        base = monomial ^ shift
        subset = shift
        while True:
            term = base | subset
            if term in out:
                out.remove(term)
            else:
                out.add(term)
            if not subset:
                break
            subset = (subset-1) & shift
    return out


def degree(poly):
    return max((s.bit_count() for s in poly), default=-1)


def derivative_spaces(poly, n, target=1):
    """Compute R_j={a:degree(Delta_a poly)<=j}, down to target."""
    k = degree(poly)
    basis = [1 << i for i in range(n)]
    records = [{"derivative_degree":max(k-1,target),"basis":basis[:]}]
    for j in range(k-2, target-1, -1):
        derivatives = [derivative(poly,a) for a in basis]
        assert all(degree(p) <= j+1 for p in derivatives)
        monomials = sorted(set().union(*(p for p in derivatives)))
        monomials = [m for m in monomials if m.bit_count() == j+1]
        columns = [sum((m in p)<<i for i,m in enumerate(monomials))
                   for p in derivatives]
        combinations = kernel(columns)
        basis = [linear_apply(basis,coefficients) for coefficients in combinations]
        records.append({"derivative_degree":j,"basis":basis[:]})
    return basis,records


def acquire_quotient(poly,n):
    radical,levels = derivative_spaces(poly,n)
    full = radical[:]
    complement = []
    for i in range(n):
        e = 1 << i
        if rank(full+[e]) > len(full):
            full.append(e)
            complement.append(e)
    columns = complement+radical
    r = len(complement)
    c = eval_poly(poly,0)
    q = set()
    for j in range(r,n):
        if eval_poly(poly,columns[j]) ^ c:
            q.add(1<<j)
    for i in range(n):
        for j in range(max(i+1,r),n):
            if (eval_poly(poly,columns[i]^columns[j]) ^ eval_poly(poly,columns[i])
                    ^ eval_poly(poly,columns[j]) ^ c):
                q.add((1<<i)|(1<<j))
    return {"columns":columns,"nonlinear_dimension":r,
            "quadratic_monomials":sorted(q),"levels":levels}


def substitute(poly, rows):
    out = set()
    for monomial in poly:
        terms = {0}
        for i,row in enumerate(rows):
            if monomial >> i & 1:
                nxt = set()
                for t in terms:
                    for j in range(len(rows)):
                        if row >> j & 1:
                            mask = t | (1<<j)
                            if mask in nxt:
                                nxt.remove(mask)
                            else:
                                nxt.add(mask)
                terms = nxt
        out.symmetric_difference_update(terms)
    return out


def run():
    rng = random.Random(20261027151)
    records = []
    global_checks = filtration_checks = 0
    for n,r,k in [(6,3,3),(7,4,4),(8,5,5),(9,5,4),(9,6,6)]:
        for trial in range(4):
            core = {sum(1<<i for i in comb) for s in range(k+1)
                    for comb in combinations(range(r),s) if rng.randrange(2)}
            core.add((1<<k)-1)
            hidden = set(core)
            hidden.symmetric_difference_update(sum(1<<i for i in comb)
                for s in (1,2) for comb in combinations(range(n),s) if rng.randrange(2))
            rows = [1<<i for i in range(n)]
            for _ in range(20*n):
                a,b = rng.sample(range(n),2)
                rows[a] ^= rows[b]
            raw = substitute(hidden,rows)
            compiled = acquire_quotient(raw,n)
            columns = compiled["columns"]
            active = compiled["nonlinear_dimension"]
            assert active <= r
            for rec in compiled["levels"]:
                actual = {a for a in range(1<<n)
                          if degree(derivative(raw,a)) <= rec["derivative_degree"]}
                found = {linear_apply(rec["basis"],a)
                         for a in range(1<<len(rec["basis"]))}
                assert actual == found
                filtration_checks += 1
            Z = 0
            for y in range(1<<n):
                x = linear_apply(columns,y)
                u = y & ((1<<active)-1)
                right = eval_poly(raw,linear_apply(columns,u)) ^ eval_poly(compiled["quadratic_monomials"],y)
                assert eval_poly(raw,x) == right
                Z += (-1)**right
                global_checks += 1
            assert Z == sum((-1)**eval_poly(raw,x) for x in range(1<<n))
            records.append({"inputs":n,"planted_active_bound":r,"raw_degree":degree(raw),
                            "raw_terms":len(raw),"acquired_active_dimension":active,
                            "signed_count":Z,"levels":[[v["derivative_degree"],len(v["basis"])]
                                                         for v in compiled["levels"]]})
    # Decisive low-weight-query failure for an unrestricted program.
    bad_n = 8
    bad = {(1<<bad_n)-1}
    assert all(eval_poly(bad,x)==0 for x in range(1<<bad_n) if x.bit_count()<=3)
    assert eval_poly(bad,(1<<bad_n)-1)==1
    return {"status":"all exact assertions passed","fixtures":len(records),
            "filtration_subspace_checks":filtration_checks,
            "pointwise_quotient_checks":global_checks,
            "count_backend":"exhaustive finite quadratic fibers",
            "raw_program_low_weight_certification_counterexample":True,
            "records":records}


if __name__ == "__main__":
    result = run()
    Path(__file__).with_name("derivative_quotient_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k!="records"},indent=2))
