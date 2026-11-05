"""Exact rational box-kernel construction from the preserved acquired table.

The inherited response bound is conditional on its existing physical event.
No new source trajectory, meter record or response oracle is invented here.
"""
from __future__ import annotations
from bisect import bisect_right
from fractions import Fraction as F
from functools import lru_cache
from math import isqrt
from pathlib import Path
from time import perf_counter
import json

ROOT = Path(__file__).resolve().parent
TABLE = ROOT.parent / "next_programme/bridge/acquired_step_response.json"


def sqrt_upper(q, bits=80):
    assert q >= 0
    scale = 1 << bits
    z = isqrt((q.numerator * scale * scale) // q.denominator)
    if F(z*z, scale*scale) < q:
        z += 1
    return F(z, scale)


def solve(matrix, rhs):
    n = len(rhs)
    work = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for i in range(n):
        pivot = next(j for j in range(i, n) if work[j][i])
        work[i], work[pivot] = work[pivot], work[i]
        div = work[i][i]
        work[i] = [v / div for v in work[i]]
        for j in range(n):
            if j != i:
                mul = work[j][i]
                work[j] = [v - mul*w for v,w in zip(work[j], work[i])]
    return [row[-1] for row in work]


def quadratic(matrix, vector):
    return sum((vector[i]*matrix[i][j]*vector[j]
                for i in range(len(vector)) for j in range(len(vector))), F(0))


def ldl_pivots(matrix):
    n = len(matrix)
    low = [[F(i == j) for j in range(n)] for i in range(n)]
    diag = []
    for i in range(n):
        d = matrix[i][i] - sum((low[i][k]**2*diag[k] for k in range(i)), F(0))
        assert d > 0
        diag.append(d)
        for j in range(i+1,n):
            low[j][i] = (matrix[j][i] - sum((low[j][k]*low[i][k]*diag[k]
                                             for k in range(i)),F(0))) / d
    return diag


def main():
    start = perf_counter()
    data = json.loads(TABLE.read_text())
    knots = [F(x) for x in data["times_exact"]]
    vals = [F(x) for x in data["values_exact"]]
    eps = F(data["response_error_exact"])
    gamma = F(data["gamma_exact"]); mu = F(data["stiffness_exact"])
    horizon = F(data["horizon_exact"])
    pieces = []
    for a,b,va,vb in zip(knots[:-1],knots[1:],vals[:-1],vals[1:]):
        slope = (vb-va)/(b-a)
        pieces.append((a,b,slope,va-slope*a))

    @lru_cache(None)
    def response(t):
        if t < 0:
            return F(0)
        assert t <= horizon
        if t == horizon:
            return vals[-1]
        k = bisect_right(knots,t)-1
        _,_,slope,intercept = pieces[k]
        return slope*t+intercept

    @lru_cache(None)
    def second_primitive(z):
        z = abs(z)
        assert z <= horizon
        total = F(0)
        for left,right,slope,intercept in pieces:
            if left >= z:
                break
            right = min(right,z)
            total += z*(slope*(right**2-left**2)/2+intercept*(right-left))
            total -= slope*(right**3-left**3)/3+intercept*(right**2-left**2)/2
        return total

    boxes = [(F(0),F(1,10)), (F(3,10),F(4,10)),
             (F(6,10),F(7,10)), (F(9,10),F(1))]

    def h(box, u):
        a,b = box
        return (response(b-u)-response(a-u))/(b-a)

    def integrate_h_product(box1,box2):
        cuts = {F(0),horizon}
        for box in (box1,box2):
            for endpoint in box:
                cuts.update(endpoint-t for t in knots if 0 < endpoint-t < horizon)
        cuts = sorted(cuts)
        total = F(0)
        for left,right in zip(cuts[:-1],cuts[1:]):
            length = right-left; mid = (left+right)/2
            q1 = (3*left+right)/4; q3 = (left+3*right)/4
            v1 = h(box1,mid); v2 = h(box2,mid)
            s1 = 2*(h(box1,q3)-h(box1,q1))/length
            s2 = 2*(h(box2,q3)-h(box2,q1))/length
            total += length*v1*v2 + length**3*s1*s2/12
        return total

    p = len(boxes)
    ghat = [[F(0) for _ in range(p)] for _ in range(p)]
    for i,(a,b) in enumerate(boxes):
        for j,(c,d) in enumerate(boxes[:i+1]):
            mean_step = (second_primitive(b-c)+second_primitive(a-d)
                         -second_primitive(b-d)-second_primitive(a-c))/((b-a)*(d-c))
            ghat[i][j] = 1/mu-mean_step-2*gamma*integrate_h_product(boxes[i],boxes[j])
            ghat[j][i] = ghat[i][j]
    q_upper = sqrt_upper(1/(2*gamma*mu))
    e = 2*eps*sqrt_upper(horizon)/min(b-a for a,b in boxes)
    beta = eps+2*gamma*(2*q_upper*e+e*e)
    upper = [[ghat[i][j]+(p*beta if i==j else 0) for j in range(p)] for i in range(p)]
    pivots = ldl_pivots(upper)
    weights_exact = solve([row[:-1] for row in upper[:-1]], [row[-1] for row in upper[:-1]])
    # Finite 32-bit coefficients, with the actual rounded vector re-certified.
    scale = 1 << 32
    weights = [F(round(a*scale),scale) for a in weights_exact]
    vec = [-a for a in weights]+[F(1)]
    energy = F(1,2)
    eta = F(1,1000)
    radius = sqrt_upper(2*energy*quadratic(upper,vec))+eta*sum(abs(a) for a in weights)
    generic_energy_radius = sqrt_upper(2*energy/mu)
    result = {
        "scope": "Exact rational transformation conditional on the preserved acquired-response event. No new physical source or meter execution.",
        "input_table": str(TABLE.relative_to(ROOT.parent.parent)),
        "inherited_event_probability_exact": data["resources"]["joint_valid_event_probability_exact"],
        "inherited_actual_protocol_time_exact": data["resources"]["actual_protocol_time_exact"],
        "epsilon_response_exact": str(eps),
        "boxes_exact": [[str(a),str(b)] for a,b in boxes],
        "target_is_last_box": True,
        "gram_hat_exact": [[str(x) for x in row] for row in ghat],
        "entry_error_beta_exact": str(beta),
        "upper_gram_exact": [[str(x) for x in row] for row in upper],
        "positive_LDL_pivots_exact": [str(x) for x in pivots],
        "rounded_predictor_weights_exact": [str(x) for x in weights],
        "assumed_new_record_error_each_exact": str(eta),
        "assumed_new_initial_energy_exact": str(energy),
        "certified_prediction_radius_upper_exact": str(radius),
        "unconditional_energy_only_radius_upper_exact": str(generic_energy_radius),
        "certificate_improves_energy_only_radius": radius < generic_energy_radius,
        "summary_float": {"epsilon_response": float(eps),"beta": float(beta),
                           "prediction_radius": float(radius),
                           "energy_only_radius": float(generic_energy_radius),
                           "weights": [float(a) for a in weights]},
        "interpretation": "The inherited table is too coarse for this finite-error Gram bound to certify useful short-box deterministic readiness. This is a limitation of this sufficient certificate at the inherited precision, not an impossibility theorem for every method using the same reports.",
        "arithmetic_seconds": perf_counter()-start,
        "table_intervals": len(pieces),
        "boxes": p,
    }
    (ROOT / "acquired_box_kernel_results.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result["summary_float"],indent=2))
    print("certificate_improves_energy_only_radius:", result["certificate_improves_energy_only_radius"])


if __name__ == "__main__":
    main()
