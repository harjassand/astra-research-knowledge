"""Exact pair-output compiler. No reference cutoff or numerical SDP.

Input: {"n": n, "P": [rational rows], "Q": [...]}.
Common output rays cancel first. Unmatched rows must have support <=2.
Output: rational polynomial/Sturm proof, or a faithful classical witness.
Python/SymPy root-isolation costs are charged by main().
"""
import argparse
import hashlib
import json
from pathlib import Path
from time import perf_counter

IMPORT_BEGIN = perf_counter()
import sympy as s
IMPORT_SECONDS = perf_counter() - IMPORT_BEGIN

t = s.Symbol("t")


def q(x):
    z = s.Rational(str(x))
    return z


def coeffs(p):
    return [str(v) for v in s.Poly(p, t, domain=s.QQ).all_coeffs()]


def validate(d):
    n = d["n"]
    if not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    out = {}
    for name in ("P", "Q"):
        rows = []
        for raw in d[name]:
            row = {int(i): q(v) for i, v in raw.items() if q(v) != 0}
            if not row or min(row) < 0 or max(row) >= n:
                raise ValueError("invalid nonzero row support")
            if any(v <= 0 for v in row.values()):
                raise ValueError("positive support coefficients required")
            rows.append(row)
        if any(sum(r.get(i, 0) for r in rows) != 1 for i in range(n)):
            raise ValueError("channel columns must sum exactly to one")
        out[name] = rows
    return n, out["P"], out["Q"]


def cancel_common_rays(P, Q):
    groups = []
    for rows in (P, Q):
        g = {}
        for row in rows:
            mass = sum(row.values())
            ray = tuple((i, row[i]/mass) for i in sorted(row))
            g[ray] = g.get(ray, 0) + mass
        groups.append(g)
    left, right, receipt = [], [], []
    for ray in sorted(set(groups[0]) | set(groups[1])):
        a, b = (g.get(ray, 0) for g in groups)
        common = min(a, b)
        receipt.append({'ray': [[i, str(z)] for i,z in ray], 'P_mass':str(a),
                        'Q_mass':str(b), 'cancelled_mass':str(common)})
        if a>common:
            left.append({i:(a-common)*z for i,z in ray})
        if b>common:
            right.append({i:(b-common)*z for i,z in ray})
    return left, right, receipt


def signed_poles(P, Q):
    edges = {}
    for sign, rows in ((-1, P), (1, Q)):
        for row in rows:
            if len(row) != 2:
                continue
            i, j = sorted(row)
            a, b = row[i], row[j]
            pole = a / b
            z = edges.setdefault((i, j), {})
            z[pole] = z.get(pole, 0) + sign * a
    return {e: {r: c for r, c in z.items() if c != 0} for e, z in edges.items()}


def sign_near_zero(p):
    cs = s.Poly(p, t, domain=s.QQ).all_coeffs()
    return next((s.sign(v) for v in reversed(cs) if v != 0), 0)


def variation(signs):
    z = [int(x) for x in signs if x]
    return sum(a != b for a, b in zip(z, z[1:]))


def sturm_record(p):
    chain = s.sturm(p, t)
    v0 = variation([sign_near_zero(z) for z in chain])
    vi = variation([s.sign(s.Poly(z, t).LC()) for z in chain])
    return {"chain": [coeffs(z) for z in chain], "variation_zero_plus": v0,
            "variation_infinity": vi, "positive_roots": v0 - vi}


def negative_point(p):
    """Exact rational isolation; no floating point sign decision."""
    p = s.Poly(p, t, domain=s.QQ)
    if p.eval(1) < 0:
        return s.Rational(1)
    bits = 8
    while True:
        intervals = p.intervals(eps=s.Rational(1, 2**bits))
        positive = [(a, b) for (a, b), _ in intervals if b > 0]
        candidates = [s.Rational(1), s.Rational(2)]
        for a, b in positive:
            candidates += [a, b, a / 2, b + 1]
        candidates += [(b + c) / 2 for (_, b), (c, _) in zip(positive, positive[1:]) if b < c]
        for r in candidates:
            if r > 0 and p.eval(r) < 0:
                return r
        bits *= 2


def edge_record(poles):
    poles = dict(sorted(poles.items()))
    D = s.Poly(1, t, domain=s.QQ)
    for r in poles:
        D *= s.Poly(t + r, t, domain=s.QQ)
    N = s.Poly(0, t, domain=s.QQ)
    for r, mass in poles.items():
        quotient, rem = s.div(D, s.Poly(t + r, t, domain=s.QQ))
        assert rem.is_zero
        N += mass * quotient
    base = {"poles": [[str(r), str(m)] for r, m in poles.items()],
            "numerator": coeffs(N), "denominator": coeffs(D),
            "degree": N.degree() if not N.is_zero else -1}
    if N.is_zero:
        return dict(base, nonnegative=True, zero=True, factors=[])
    content, fs = s.sqf_list(N)
    records = []
    odd_roots = 0
    for f, multiplicity in fs:
        sr = sturm_record(f.as_expr())
        if multiplicity % 2:
            odd_roots += sr["positive_roots"]
        records.append({"factor": coeffs(f), "multiplicity": multiplicity, **sr})
    ok = bool(sign_near_zero(N) > 0 and odd_roots == 0)
    rec = dict(base, zero=False, content=str(content), factors=records,
               sign_near_zero=int(sign_near_zero(N)), nonnegative=ok)
    if not ok:
        r = negative_point(N)
        rec.update(negative_t=str(r), negative_kernel=str(N.eval(r) / D.eval(r)))
        assert q(rec["negative_kernel"]) < 0
    return rec


def fisher(rows, p, h):
    return sum(sum(row.get(i, 0) * h[i] for i in row)**2 /
               sum(row[i] * p[i] for i in row) for row in rows)


def witness(n, P, Q, edge, ratio):
    i, j = edge
    r = 0
    while True:
        epsilon = s.Rational(1, 2**r)
        z = [epsilon] * n
        z[i], z[j] = s.Rational(1), ratio
        Z = sum(z)
        p = [v / Z for v in z]
        f = [s.Rational(0)] * n
        f[i] = 1
        mean = p[i]
        h = [pi * (fi - mean) for pi, fi in zip(p, f)]
        gp, gq = fisher(P, p, h), fisher(Q, p, h)
        if gp < gq:
            assert sum(p) == 1 and min(p) > 0 and sum(h) == 0
            return {"edge": list(edge), "t": str(ratio), "dyadic_exponent": r,
                    "p": list(map(str, p)), "h": list(map(str, h)),
                    "gP": str(gp), "gQ": str(gq), "gap": str(gp-gq)}
        r += 1


def compile_channel(d):
    begin = perf_counter()
    n, P, Q = validate(d)
    residualP, residualQ, cancellation = cancel_common_rays(P, Q)
    if any(len(row)>2 for row in residualP+residualQ):
        return {'n':n, 'P_outputs':len(P),'Q_outputs':len(Q), 'eligible':False,
                'complete_order':None,'status':'OUTSIDE_EFFECTIVE_PAIR_SUPPORT_CLASS',
                'common_ray_cancellation':cancellation,
                'cost':{'compiler_seconds':perf_counter()-begin,'sympy_import_seconds':IMPORT_SECONDS,
                        'reference_dimensions_enumerated':0,'SDPs':0}}
    edges = signed_poles(residualP, residualQ)
    recs = []
    cache = {}
    fail = None
    for edge, poles in sorted(edges.items()):
        key = tuple(sorted(poles.items()))
        if key not in cache:
            cache[key] = edge_record(poles)
        er = dict(edge=list(edge), **cache[key])
        recs.append(er)
        if not er["nonnegative"] and fail is None:
            fail = witness(n, P, Q, edge, q(er["negative_t"]))
    return {"n": n, "P_outputs": len(P), "Q_outputs": len(Q),
            'eligible':True,'common_ray_cancellation':cancellation,
            "support_edges": len(edges), "distinct_polynomial_queries": len(cache),
            "complete_order": fail is None, "edges": recs, "failure_witness": fail,
            "cost": {"compiler_seconds": perf_counter()-begin,
                     "sympy_import_seconds": IMPORT_SECONDS,
                     "reference_dimensions_enumerated": 0, "SDPs": 0}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("output", type=Path)
    args = ap.parse_args()
    raw = args.input.read_bytes()
    result = compile_channel(json.loads(raw))
    result["input_sha256"] = hashlib.sha256(raw).hexdigest()
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: result.get(k) for k in ("n", "eligible", "support_edges", "complete_order", "cost")}))


if __name__ == "__main__":
    main()
