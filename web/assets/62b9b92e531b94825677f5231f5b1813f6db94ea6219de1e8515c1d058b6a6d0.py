"""Own exact transcription/falsification audit of c10_s02 COMMON_NONLINEAR.

No peer implementation is run or imported. These diagnostics supplement the
full analytic proof audit; they do not establish the infinite quantifiers.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import time


def W(x):
    a, b, c = x
    s = b+c
    return (1+F((a-1)**2, 8)+s+F(max(0, b-3*c)**2, 4*(s+1))
            +F(a, s+1)+F(a, 64*(b+1)))


def transitions(x, k):
    a, b, c = x
    return [(k*a*c, (a, b+1, c-1)), (a*b, (a, b-1, c+1)),
            (a*b, (a-1, b, c)), (b, (a+1, b, c)),
            (c, (a, b, c-1)), (1, (a, b, c+1))]


def gen(fn, x, k):
    old = fn(x)
    return sum((rate*(fn(y)-old) for rate, y in transitions(x, k) if rate), F(0))


def audit():
    start = time.perf_counter()
    states = set(product(range(9), repeat=3))
    stress = (0, 1, 2, 3, 4, 10, 1535, 1536, 1537, 20000, 10**6, 2**50)
    states.update(product(stress, repeat=3))
    for a in stress:
        for c in (1, 2, 4, 99, 10000, 20000, 10**6):
            for b in (max(0, 3*c-4), 3*c-1, 3*c, 3*c+1, 3*c+4, 7*c+1):
                states.add((a, b, c))
    states = {x for x in states if x[0]+x[1] >= 1}
    outside, generators, identities, bounds = 0, 0, 0, 0
    max_global_slack = None
    for x in sorted(states):
        a, b, c = x
        s = b+c
        for k in (F(1), F(2)):
            lw = gen(W, x, k)
            global_slack = F(1945)-F(a, 2)-F(s, 32)-lw
            assert global_slack >= 0, (x, k, lw, "global bound")
            max_global_slack = global_slack if max_global_slack is None else min(max_global_slack, global_slack)
            if a >= 1536 or s >= 20000:
                assert lw <= -1, (x, k, lw, "core return")
                outside += 1
            generators += 1
            assert gen(lambda z: F((z[0]-1)**2, 8), x, k) == F((-2*a*a+5*a-1)*b, 8)
            rb = (F(b*(1-a), b+1)
                  +(F(a*a, b+1) if b else 0)-F(k*a*a*c, (b+1)*(b+2)))/64
            assert gen(lambda z: F(z[0], 64*(z[1]+1)), x, k) == rb
            identities += 2
            if s:
                rs = F(b*(1-a), s+1)+F(a*c, s*(s+1))-F(a, (s+1)*(s+2))
                assert gen(lambda z: F(z[0], z[1]+z[2]+1), x, k) == rs
                identities += 1
                r = F(max(0, b-3*c), s)
                R = 1-F(6*r+r*r, 4)
                J = F((-2*a*a+5*a-1)*b, 8)-c*R-2*a*r*(b-2*c)
                if a <= 2:
                    assert J <= -F(s, 32)
                else:
                    assert J <= -F(s, 8)-F(a*a*b, 36)
                lf = gen(lambda z: z[1]+z[2]+F(max(0, z[1]-3*z[2])**2,
                                             4*(z[1]+z[2]+1)), x, k)
                assert lf <= -c*R-2*a*r*(b-2*c)+10*a+9
                bounds += 2
            else:
                assert lw == 1-F(a, 2)
                identities += 1
    return {"status": "NO_COUNTEREXAMPLE_FOUND_SCOPED_PROOF_CHECKED",
            "state_count": len(states), "endpoint_generator_checks": generators,
            "outside_core_endpoint_checks": outside, "exact_formula_checks": identities,
            "intermediate_inequality_checks": bounds,
            "minimum_global_bound_slack": str(max_global_slack),
            "wall_seconds": time.perf_counter()-start,
            "all_controls_justification": "Generator is affine in the sole k, so exact endpoint maxima cover the whole [1,2] interval at each tested state.",
            "proof_audit": [
                "Exact Q, Rs, Rb differences checked analytically; the b>=1 indicator is necessary.",
                "Positive-part square curvature bound and denominator shifts reproduce LF<=−cR(r)−2ar(b−2c)+10a+9.",
                "Small-A polynomial and Bernstein coefficients independently expanded; all constants are correct.",
                "H(a) split, b>=1 reciprocal corrections and b=0,c>=1 direct formula establish universal drift cases.",
                "Recovery word has <=2N+7 events, preserves A catalyst until B adjustment and stays at <=N+2; Lambda and post-abort R are conservative.",
                "Stopped nonnegative Dynkin bounds and geometric conditional retries do not assume independent policies; regenerative occupation bound cancels endpoint W(g) by Fatou without a stationary-W-moment premise."
            ],
            "limitations": "No formal/external verification or priority clearance; finite tests are implementation diagnostics. Expected total excursion firings remain unproved by this peer certificate."}


if __name__ == "__main__":
    result = audit()
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(__file__).with_name("NONLINEAR_PEER_AUDIT.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
