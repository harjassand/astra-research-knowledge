#!/usr/bin/env python3
"""FPT exact checker for channels with one common positive rational modifier.

Input rates are
    rho_e(x) = c_e * x**source_e * prod(A_j(x)) / prod(Q_j(x)),
where every A_j and Q_j is a finite sparse generalized polynomial with
strictly positive rational coefficients and is shared by all channels. Factors
are kept factored. The common positive scalar cancels from the source-order
test (and from trajectories up to a positive time change).

The decision enumerates the 3-way signs of channel projections and solves the
resulting exact rational LPs using SymPy's rational simplex implementation.
The theoretical branch count is m*3**(m-1). A REFUTED direction is replayed
with Fraction arithmetic; budget exhaustion or solver trouble returns UNKNOWN.
"""
from __future__ import annotations
import argparse
import itertools
import json
import signal
import sys
import time
from fractions import Fraction as F
from pathlib import Path
from typing import Any

try:
    import sympy
    from sympy import Rational
    from sympy.solvers.simplex import linprog, InfeasibleLPError
except ImportError:  # pragma: no cover
    sympy = None
    Rational = None
    linprog = None
    InfeasibleLPError = Exception

Vector = dict[int, F]


def frac(raw: Any) -> F:
    if isinstance(raw, bool):
        raise ValueError("boolean is not a rational number")
    return F(str(raw))


def parse_vector(raw: Any, dimension: int, label: str) -> Vector:
    if isinstance(raw, dict):
        pairs = raw.items()
    elif isinstance(raw, list):
        if len(raw) != dimension:
            raise ValueError(f"{label} dense vector must have dimension {dimension}")
        pairs = enumerate(raw)
    else:
        raise ValueError(f"{label} must be a dense list or sparse index:value object")
    out: Vector = {}
    for raw_i, raw_v in pairs:
        try:
            i = int(raw_i)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{label} coordinate index is not an integer") from exc
        if str(i) != str(raw_i) and not isinstance(raw_i, int):
            raise ValueError(f"{label} coordinate index is not canonical integer text")
        if i < 0 or i >= dimension:
            raise ValueError(f"{label} coordinate {i} is outside [0,{dimension})")
        value = frac(raw_v)
        if value:
            out[i] = out.get(i, F(0)) + value
    return {i: v for i, v in out.items() if v}


def parse_terms(raw: Any, dimension: int, label: str):
    if not isinstance(raw, list) or not raw:
        raise ValueError(f"{label} must be a nonempty positive support")
    terms = []
    for j, item in enumerate(raw):
        if isinstance(item, dict) and "exp" in item:
            exp = parse_vector(item["exp"], dimension, f"{label}[{j}].exp")
            coef = frac(item.get("coef", "1"))
        else:
            exp = parse_vector(item, dimension, f"{label}[{j}]")
            coef = F(1)
        if coef <= 0:
            raise ValueError(f"{label}[{j}] coefficient must be strictly positive")
        terms.append((exp, coef))
    # Duplicate exponents aggregate to a positive coefficient and stay present.
    combined: dict[tuple[tuple[int, F], ...], F] = {}
    for exp, coef in terms:
        key = tuple(sorted(exp.items()))
        combined[key] = combined.get(key, F(0)) + coef
    return tuple((dict(key), coef) for key, coef in sorted(combined.items()))


def parse_network(data: Any):
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")
    dimension = data.get("dimension")
    if not isinstance(dimension, int) or isinstance(dimension, bool) or dimension < 1:
        raise ValueError("dimension must be a positive integer")
    edges_raw = data.get("edges")
    if not isinstance(edges_raw, list) or not edges_raw:
        raise ValueError("edges must be a nonempty list")
    common = data.get("common_multiplier", {})
    if not isinstance(common, dict):
        raise ValueError("common_multiplier must be an object")
    num_factors = []
    den_factors = []
    for role, dest in (("numerator_factors", num_factors), ("denominator_factors", den_factors)):
        factors = common.get(role, [])
        if not isinstance(factors, list):
            raise ValueError(f"common_multiplier.{role} must be a list")
        for i, factor in enumerate(factors):
            if not isinstance(factor, dict):
                raise ValueError(f"{role}[{i}] must be an object")
            dest.append(parse_terms(factor.get("terms"), dimension, f"{role}[{i}].terms"))
    edges = []
    for j, raw in enumerate(edges_raw):
        if not isinstance(raw, dict):
            raise ValueError(f"edges[{j}] must be an object")
        name = str(raw.get("name", f"e{j}"))
        nu = parse_vector(raw.get("nu"), dimension, f"{name}.nu")
        source = parse_vector(raw.get("source"), dimension, f"{name}.source")
        coef = frac(raw.get("coef", "1"))
        if coef <= 0:
            raise ValueError(f"{name}.coef must be strictly positive")
        edges.append({"name":name,"nu":nu,"source":source,"coef":coef})
    return edges, dimension, num_factors, den_factors


def dot(a: Vector, b: Vector) -> F:
    if len(a) > len(b):
        a, b = b, a
    return sum((v*b.get(i,F(0)) for i,v in a.items()),F(0))


def verify_counterdirection(edges, r: Vector, dimension: int):
    rows=[]
    for e in edges:
        drift=dot(e["nu"],r)
        source=dot(e["source"],r)
        if drift:
            rows.append({"name":e["name"],"drift":drift,"source_score":source})
    if not rows:
        return None
    bottom=min(x["source_score"] for x in rows)
    bad=[x["name"] for x in rows if x["source_score"]==bottom and x["drift"]<0]
    if not bad:
        return None
    return {"r_min_orientation":[str(r.get(i,F(0))) for i in range(dimension)],
            "w_max_orientation":[str(-r.get(i,F(0))) for i in range(dimension)],
            "minimum_active_source_score":str(bottom),
            "negative_top_ties":bad,
            "active":[{"name":x["name"],"r_dot_nu":str(x["drift"]),
                       "source_score":str(x["source_score"]),
                       "minimum_tied":x["source_score"]==bottom} for x in rows]}


def to_sympy(x: F):
    return Rational(x.numerator,x.denominator)


def solve_branch(edges, dimension, signs, bad_index, coord_ids):
    """Exact LP for one active-sign branch and one negative top source."""
    index={coord:i for i,coord in enumerate(coord_ids)}
    n=len(coord_ids)
    width=2*n  # r = r_plus - r_minus, all LP variables nonnegative.
    A=[]; b=[]; Aeq=[]; beq=[]
    def row_for(v: Vector):
        row=[F(0)]*width
        for coord,value in v.items():
            j=index.get(coord)
            if j is not None:
                row[j]+=value
                row[n+j]-=value
        return row
    for i,(edge,sigma) in enumerate(zip(edges,signs)):
        row=row_for(edge["nu"])
        if sigma==0:
            Aeq.append([to_sympy(x) for x in row]); beq.append(Rational(0))
        elif sigma==1:
            A.append([to_sympy(-x) for x in row]); b.append(Rational(-1))
        else:  # sigma = -1
            A.append([to_sympy(x) for x in row]); b.append(Rational(-1))
    for j in range(len(edges)):
        if signs[j]==0:
            continue  # neutral channels are deleted before source minimization.
        diff={}
        for coord,value in edges[bad_index]["source"].items():
            diff[coord]=diff.get(coord,F(0))+value
        for coord,value in edges[j]["source"].items():
            diff[coord]=diff.get(coord,F(0))-value
        row=row_for(diff)  # r.(y_bad-y_j) <= 0
        A.append([to_sympy(x) for x in row]); b.append(Rational(0))
    if width==0:
        return None
    objective=[Rational(0)]*width
    try:
        value, point=linprog(objective, A=A or None, b=b or None,
                             A_eq=Aeq or None, b_eq=beq or None)
    except InfeasibleLPError:
        return None
    r={coord:F(point[j])-F(point[n+j]) for j,coord in enumerate(coord_ids)}
    return {i:v for i,v in r.items() if v}


class BudgetExpired(Exception):
    pass


def recognize(edges, dimension, *, max_lps=None, timeout_seconds=None):
    if sympy is None:
        return {"status":"UNKNOWN","reason":"SymPy exact rational LP backend is unavailable","lp_checks":0}
    coord_ids=sorted({i for e in edges for v in (e["nu"],e["source"]) for i in v})
    started=time.monotonic(); checks=0
    def run_lp(signs,bad):
        nonlocal checks
        if max_lps is not None and checks>=max_lps:
            raise BudgetExpired("LP-query budget exhausted")
        if timeout_seconds is not None and time.monotonic()-started>=timeout_seconds:
            raise BudgetExpired("wall-clock budget exhausted")
        checks+=1
        return solve_branch(edges,dimension,signs,bad,coord_ids)
    m=len(edges)
    try:
        # Candidate edge e is known negative, so enumerate only signs of m-1 others.
        for e in range(m):
            other=[j for j in range(m) if j!=e]
            for rest in itertools.product((-1,0,1),repeat=m-1):
                signs=[0]*m; signs[e]=-1
                for j,sigma in zip(other,rest): signs[j]=sigma
                r=run_lp(signs,e)
                if r is not None:
                    witness=verify_counterdirection(edges,r,dimension)
                    if witness is None:
                        return {"status":"UNKNOWN","reason":"exact LP witness failed Fraction replay","lp_checks":checks}
                    return {"status":"REFUTED","reason":"negative active channel ties at the minimum active source score",
                            "lp_checks":checks,"witness":witness}
    except BudgetExpired as exc:
        return {"status":"UNKNOWN","reason":str(exc),"lp_checks":checks}
    except Exception as exc:
        return {"status":"UNKNOWN","reason":f"exact LP backend failure: {type(exc).__name__}: {exc}","lp_checks":checks}
    return {"status":"CERTIFIED","lp_checks":checks,
            "backend":f"SymPy {sympy.__version__} exact rational simplex",
            "trust_basis":"every sign/candidate LP was exactly infeasible; no proof objects are emitted",
            "branch_bound":f"{m}*3**({m}-1)",
            "meaning":"every active minimum-source channel points strictly inward in r=-w orientation"}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input",type=Path)
    parser.add_argument("--max-lps",type=int,default=None,help="LP query budget; exhaustion returns UNKNOWN")
    parser.add_argument("--timeout-seconds",type=float,default=None,help="wall budget checked between LP calls")
    args=parser.parse_args(argv)
    if args.max_lps is not None and args.max_lps<0: parser.error("--max-lps must be nonnegative")
    if args.timeout_seconds is not None and args.timeout_seconds<0: parser.error("--timeout-seconds must be nonnegative")
    try:
        edges,d,num_factors,den_factors=parse_network(json.loads(args.input.read_text()))
    except (OSError,json.JSONDecodeError,KeyError,TypeError,ValueError,ZeroDivisionError) as exc:
        print(json.dumps({"status":"INVALID_INPUT","reason":str(exc)},indent=2)); return 2
    if sympy is None:
        result={"status":"UNKNOWN","reason":"SymPy exact rational LP backend is unavailable","lp_checks":0}
    else:
        result=recognize(edges,d,max_lps=args.max_lps,timeout_seconds=args.timeout_seconds)
    result.update({"input":str(args.input),"dimension":d,"channels":len(edges),
                   "effective_LP_coordinates":len({i for e in edges for v in (e["nu"],e["source"]) for i in v}),
                   "shared_numerator_factors":sum(len(f) for f in num_factors),
                   "shared_denominator_factors":sum(len(f) for f in den_factors),
                   "common_factors_validated_but_not_expanded":True})
    print(json.dumps(result,indent=2,sort_keys=True))
    return {"CERTIFIED":0,"REFUTED":1,"UNKNOWN":3}.get(result["status"],2)

if __name__=="__main__":
    raise SystemExit(main())
