"""Exact product-phase recognizer and bounded rational compiler primitives.

This is not a counting/Gibbs sampler implementation. Gaussian rationals are
pairs of Fractions; no numerical phase tests or irrational equality tests.
"""
from fractions import Fraction as F
from math import isqrt
import json
from pathlib import Path
from time import perf_counter

def c(x=0, y=0):
    return (F(x), F(y))

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def mul(a, b):
    return (a[0]*b[0] - a[1]*b[1], a[0]*b[1] + a[1]*b[0])

def conj(a):
    return (a[0], -a[1])

def scale(a, s):
    return (a[0]*s, a[1]*s)

def norm2(a):
    return a[0]**2 + a[1]**2

def positive_real(a):
    return a[1] == 0 and a[0] > 0

def acquire_gauge(n, edges, fields):
    """edges=(u,v,h,gamma), directed h for S+_u S-_v; q field."""
    adj = [[] for _ in range(n)]
    for u, v, h, gamma in edges:
        if gamma**2 > norm2(h):
            return {"accepted": False, "reason": "EASY_PLANE_CONE", "edge": (u,v)}
        if norm2(h) == 0:
            continue
        adj[u].append((v, conj(h)))
        adj[v].append((u, h))
    t = [None] * n
    components = []
    for root in range(n):
        if t[root] is not None:
            continue
        t[root] = c(1)
        comp, queue = [], [root]
        for u in queue:
            comp.append(u)
            for v, factor in adj[u]:
                if t[v] is None:
                    t[v] = mul(t[u], factor)
                    queue.append(v)
        components.append(comp)
    for u, v, h, gamma in edges:
        if norm2(h) and not positive_real(mul(mul(h, conj(t[u])), t[v])):
            return {"accepted": False, "reason": "EDGE_HOLONOMY", "edge": (u,v)}
    for comp in components:
        anchors = [(v, mul(fields[v], conj(t[v])))
                   for v in comp if norm2(fields[v])]
        if not anchors:
            continue
        v0, p0 = anchors[0]
        for v, p in anchors:
            if not positive_real(mul(p, conj(p0))):
                return {"accepted": False, "reason": "FIELD_ANCHOR_CONFLICT",
                        "vertices": (v0,v)}
        for v in comp:
            t[v] = mul(p0, t[v])
    for u, v, h, gamma in edges:
        assert not norm2(h) or positive_real(mul(mul(h, conj(t[u])), t[v]))
    for v, q in enumerate(fields):
        assert not norm2(q) or positive_real(mul(q, conj(t[v])))
    return {"accepted": True, "unnormalized_gauge": t, "components": components}

def ceil_sqrt_dyadic(q, k):
    """Least nonnegative multiple of 2^-k at least sqrt(q), q rational."""
    assert q >= 0 and k >= 0
    target = q.numerator * 2**(2*k)
    root = isqrt(target // q.denominator)
    if root*root*q.denominator < target:
        root += 1
    out = F(root, 2**k)
    assert out*out >= q
    low = out - F(1, 2**k)
    assert low < 0 or low*low < q or q == 0
    return out

def precision_k(max_error):
    """A bounded-length binary loop; O(encoding length + log inverse error)."""
    assert max_error > 0
    k, grid = 0, F(1)
    while grid > max_error:
        k += 1
        grid /= 2
    return k

def rational_unit_phase(t, delta_w):
    """Exact rational unit point within 2*delta_w of t/abs(t)."""
    assert norm2(t) > 0 and 0 < delta_w < F(1,4)
    sign = 1 if t[0] >= 0 else -1
    a, b = sign*t[0], sign*t[1]
    lower = max(abs(a), abs(b))
    k = precision_k(delta_w * lower)
    radius_up = ceil_sqrt_dyadic(norm2(t), k)
    w = b/(radius_up+a)
    zhat = scale(c((1-w*w)/(1+w*w), 2*w/(1+w*w)), sign)
    assert norm2(zhat) == 1
    # Exact algebraic error certification: distance^2 = 2-2inner/sqrt(norm2(t)).
    error = 2*delta_w
    inner = mul(zhat, conj(t))[0]
    threshold = 1-error*error/2
    assert inner >= 0 and inner*inner >= threshold*threshold*norm2(t)
    return zhat, k

def encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k:encode(v) for k,v in value.items()}
    if isinstance(value, (tuple,list)):
        return [encode(v) for v in value]
    return value

def bitheight(t):
    return max(max(abs(x.numerator).bit_length(), x.denominator.bit_length()) for x in t)

def diagnostics():
    start = perf_counter()
    one = c(1)
    z = [c(1), c(F(3,5), F(4,5)), c(F(5,13), F(-12,13)), c(0,1)]
    specs = [(0,1,F(1,2)),(1,2,F(2,3)),(2,0,F(3,4)),(2,3,F(5,7))]
    edges = [(u,v,scale(mul(z[u],conj(z[v])),alpha),
              alpha if j%2 else -alpha)
             for j,(u,v,alpha) in enumerate(specs)]
    fields = [scale(zv,F(v+1,11)) for v,zv in enumerate(z)]
    good = acquire_gauge(4,edges,fields)
    assert good["accepted"]

    fixtures = {"rational_nontrivial_phases":good,
                "irrational_unit_phase_from_rational_data":
                acquire_gauge(2,[(0,1,c(1,1),F(1))],[c(1),c(1,-1)]),
                "disconnected_unanchored_components":
                acquire_gauge(4,[(0,1,c(0,2),F(2)),(2,3,c(3,4),F(-5))],
                              [c(),c(),c(),c()]),
                "negative_triangle_flux":
                acquire_gauge(3,[(0,1,one,F(0)),(1,2,one,F(0)),
                                 (2,0,c(-1),F(0))],[c(),c(),c()]),
                "tree_conflicting_fields":
                acquire_gauge(2,[(0,1,one,F(0))],[one,c(0,1)]),
                "outside_cone":
                acquire_gauge(2,[(0,1,c(1,1),F(3,2))],[c(),c()])}
    assert fixtures["irrational_unit_phase_from_rational_data"]["accepted"]
    assert fixtures["disconnected_unanchored_components"]["accepted"]
    assert fixtures["negative_triangle_flux"]["reason"] == "EDGE_HOLONOMY"
    assert fixtures["tree_conflicting_fields"]["reason"] == "FIELD_ANCHOR_CONFLICT"
    assert fixtures["outside_cone"]["reason"] == "EASY_PLANE_CONE"

    phase_tests = []
    values = [c(1,1),c(-1,1),c(-1,-1),c(0,-1),c(F(1,2**80),F(-1,2**81)),
              c(F(7,13),F(2,3))]
    values += good["unnormalized_gauge"]
    for t in values:
        for delta in [F(1,100),F(1,100000)]:
            zhat,k = rational_unit_phase(t,delta)
            phase_tests.append({"t":t,"phase":zhat,"root_bits":k,
                                "input_height_bits":bitheight(t),
                                "phase_height_bits":bitheight(zhat),
                                "certified_error":2*delta})

    root_tests = []
    for q in [F(0),F(2),F(25),F(1,2**160),F(13,17),F(2**160+1)]:
        for k in [0,3,20,90]:
            alpha = ceil_sqrt_dyadic(q,k)
            root_tests.append({"norm_square":q,"grid_bits":k,"upper_root":alpha})

    # Complete exact Hamiltonian conjugation check, on 3 qubits only.
    n=3
    H=[[c() for _ in range(2**n)] for _ in range(2**n)]
    Hb=[[c() for _ in range(2**n)] for _ in range(2**n)]
    small_edges = edges[:3]
    cs = [F(1,7),F(-1,5),F(2,9)]
    for col in range(2**n):
        bits=[(col>>(n-1-v))&1 for v in range(n)]
        diag=sum(cs[v]*(1-2*bits[v]) for v in range(n))
        for u,v,h,gamma in small_edges:
            diag+=gamma*(1-2*bits[u])*(1-2*bits[v])
            if bits[u]!=bits[v]:
                row=col^(1<<(n-1-u))^(1<<(n-1-v))
                coefficient=scale(h if bits[u] else conj(h),2)
                H[row][col]=add(H[row][col],coefficient)
                # h has explicitly rational magnitude alpha in this fixture.
                magnitude = next(al for uu,vv,al in specs if uu==u and vv==v)
                Hb[row][col]=add(Hb[row][col],c(2*magnitude))
        H[col][col]=Hb[col][col]=c(diag)
        for v in range(n):
            row=col^(1<<(n-1-v))
            q=fields[v]
            H[row][col]=add(H[row][col],q if bits[v] else conj(q))
            Hb[row][col]=add(Hb[row][col],c(F(v+1,11)))
    diagD=[]
    for row in range(2**n):
        val=c(1)
        for v in range(n):
            if (row>>(n-1-v))&1:
                val=mul(val,z[v])
        diagD.append(val)
    for row in range(2**n):
        for col in range(2**n):
            assert mul(mul(diagD[row],H[row][col]),conj(diagD[col])) == Hb[row][col]

    result={"status":"PASS", "scope":"recognizer/compiler primitives only; no FPRAS",
            "recognition_fixtures":fixtures,"phase_compiler_fixtures":phase_tests,
            "root_compiler_fixtures":root_tests,
            "dense_conjugation_entries_checked":(2**n)**2,
            "wall_seconds":perf_counter()-start}
    path=Path(__file__).with_name("phase_gauge_checks.json")
    path.write_text(json.dumps(encode(result),indent=2)+"\n")
    print(json.dumps({"status":"PASS","recognition_fixtures":len(fixtures),
                      "phase_fixtures":len(phase_tests),"root_fixtures":len(root_tests),
                      "dense_conjugation_entries":(2**n)**2,
                      "wall_seconds":result["wall_seconds"]}))

if __name__ == "__main__":
    diagnostics()
