"""Rational coordinate-hinge certificates for reciprocal catalytic networks.

Own worker extension after frozen INITIAL. Proof: HINGE_RECOVERY.txt.
The compact certificate needs no LP, CAD, stationary oracle or floating point.
"""

from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import ceil
import hashlib
import json
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "initial"))
from compiler import reaction, falling, serialize, check_weak_reversibility, fixtures


def coordinate_unit(y):
    return y.index(1) if sum(y) == 1 and max(y) == 1 else None


def add_rate(table, key, r):
    old = table.get(key, (F(0), F(0)))
    table[key] = (old[0]+r.lo, old[1]+r.hi)


def acquire_pattern(rs):
    if not rs:
        return None, "empty input"
    d = len(rs[0].y)
    immigration, degradation, beta, gamma, conversions = {}, {}, {}, {}, {}
    for r in rs:
        if len(r.y) != d or len(r.yp) != d or not 0 < r.lo <= r.hi:
            return None, "invalid dimension/rate box"
        if any(not isinstance(v, int) or v < 0 for v in r.y+r.yp):
            return None, "noninteger complex"
        i, j = coordinate_unit(r.y), coordinate_unit(r.yp)
        if sum(r.y) == 0 and j is not None:
            add_rate(immigration, j, r)
        elif i is not None and sum(r.yp) == 0:
            add_rate(degradation, i, r)
        elif i is not None and j is not None and i != j:
            add_rate(conversions, (i, j), r)
        elif i is not None and sum(r.yp) == 2:
            extra = tuple(b-a for a,b in zip(r.y, r.yp))
            added = coordinate_unit(extra) if min(extra) >= 0 else None
            if added is None:
                return None, "noncatalytic first-order branching"
            add_rate(beta, (added, i), r)
        elif sum(r.y) == 2 and j is not None:
            removed_vector = tuple(a-b for a,b in zip(r.y, r.yp))
            removed = coordinate_unit(removed_vector) if min(removed_vector) >= 0 else None
            if removed is None:
                return None, "quadratic reaction is not single-count removal"
            add_rate(gamma, (removed, j), r)
        else:
            return None, "reaction outside declared pattern"
    if any(i not in immigration or i not in degradation for i in range(d)):
        return None, "requires positive immigration and degradation for every species"
    if any((j,i) not in gamma for i,j in beta):
        return None, "missing reciprocal removal of a birth catalyst"
    if not check_weak_reversibility(rs):
        return None, "not weakly reversible"
    return {"d": d, "immigration": immigration, "degradation": degradation,
            "beta": beta, "gamma": gamma, "conversions": conversions}, None


def value(x, thresholds):
    return 1+sum(max(0, n-h) for n,h in zip(x, thresholds))


def compile_hinges(rs, q=2, expand_probability=True):
    p, error = acquire_pattern(rs)
    if p is None or not isinstance(q,int) or q < 1:
        return {"status": "REJECTED_CLASS", "reason": error or "invalid q"}
    d, beta, gamma = p["d"], p["beta"], p["gamma"]
    h = [1]*d
    for (i,j), (_,upper) in beta.items():
        h[i] = max(h[i], 1+ceil(upper/gamma[j,i][0]))
    delta = min(z[0] for z in p["degradation"].values())
    immigration_upper = sum((z[1] for z in p["immigration"].values()), F(0))
    birth_constant = sum((z[1]*h[j] for (i,j),z in beta.items()), F(0))
    conversion_constant = sum((z[1]*h[i] for (i,j),z in p["conversions"].items()), F(0))
    c = immigration_upper+birth_constant+conversion_constant
    b = c+delta
    linear_birth_slope=max((sum((z[1] for (i,jj),z in beta.items() if jj==j),F(0))
                           for j in range(d)),default=F(0))
    eta=delta/(2*(linear_birth_slope+delta))
    exponential_base=1+eta
    exponential_decay=eta/exponential_base
    exponential_core=ceil((3*c+2)/delta)
    exponential_factor=exponential_decay*(1+3*c/2)
    core_v = (b+1)/delta
    core_n = ceil(core_v+sum(h))
    a = d*q
    steps = core_n+a
    count_cap = max(core_n,a)
    rate_cap = sum((r.hi for r in rs), F(0))*(count_cap+1)**2
    alpha = min(r.lo for r in rs)/(2*rate_cap)
    duration = F(steps)/rate_cap
    cert = {"status": "CERTIFIED", "d": d, "q": q, "thresholds": h,
            "pattern": p, "delta": delta, "C": c, "B": b,
            "linear_birth_slope":linear_birth_slope,
            "exponential_base":exponential_base,"exponential_decay":exponential_decay,
            "exponential_core_Z":exponential_core,
            "exponential_offset_compact":{"rational_coefficient":exponential_factor,
                                          "rational_base":exponential_base,
                                          "integer_exponent":exponential_core},
            "core_V_radius": core_v, "core_count_cap": core_n,
            "target_word_length": a, "attempt_steps": steps,
            "path_count_cap": count_cap, "total_rate_cap": rate_cap,
            "one_step_probability": alpha, "attempt_duration": duration,
            "success_probability_compact": {"rational_base": alpha,"integer_exponent": steps}}
    if expand_probability:
        cert["exponential_offset"]=exponential_factor*exponential_base**exponential_core
        success = alpha**steps
        recovery = (core_v+(b+1)*duration)/success
        cert.update({"success_probability":success,"recovery_constant":recovery,
                     "expanded_height_bits":max(recovery.numerator.bit_length(),
                                                recovery.denominator.bit_length())})
    return cert


def direct_generator_box_max(rs, x, h):
    vx = value(x,h)
    result = F(0)
    for r in rs:
        f = falling(x,r.y)
        if not f:
            continue
        xp = tuple(a+b for a,b in zip(x,r.nu))
        dv = value(xp,h)-vx
        result += f*max(r.lo*dv,r.hi*dv)
    return result


def boundary_words(rs,x,q):
    d = len(x)
    unary_death, immigration = {}, {}
    for k,r in enumerate(rs):
        i,j = coordinate_unit(r.y),coordinate_unit(r.yp)
        if i is not None and sum(r.yp)==0:
            unary_death.setdefault(i,k)
        if sum(r.y)==0 and j is not None:
            immigration.setdefault(j,k)
    word = [unary_death[i] for i in range(d) for _ in range(x[i])]
    word += [immigration[i] for i in range(d) for _ in range(q)]
    current, cap = tuple(x), sum(x)
    for k in word:
        r = rs[k]
        assert falling(current,r.y)
        current = tuple(a+b for a,b in zip(current,r.nu))
        cap = max(cap,sum(current))
    assert current==(q,)*d and cap<=max(sum(x),d*q)
    assert len(word)==sum(x)+d*q
    return len(word)


def certify_cells(rs,cert):
    """Independent finite boundary/large-axis diagnostics, not proof replacement."""
    h, d = cert["thresholds"], cert["d"]
    lattice = list(product(*(range(z+3) for z in h)))
    lattice += [tuple((10**6 if i==j else a[i]) for i in range(d))
                for j in range(d) for a in product((0,1),repeat=d)]
    maximum_slack = None
    for x in lattice:
        gen = direct_generator_box_max(rs,x,h)
        slack = cert["B"]-cert["delta"]*value(x,h)-gen
        assert slack>=0,(x,gen,cert)
        # Independently evaluate the exact generator ratio of rational a^Z.
        ratio=F(0)
        z=value(x,h)-1
        for r in rs:
            f=falling(x,r.y)
            if not f:
                continue
            xp=tuple(a+b for a,b in zip(x,r.nu))
            dv=value(xp,h)-value(x,h)
            assert -1<=dv<=1
            change=cert["exponential_base"]**dv-1
            ratio+=f*max(r.lo*change,r.hi*change)
        if z>cert["exponential_core_Z"]:
            assert ratio<=-cert["exponential_decay"]
        else:
            assert ratio<=-cert["exponential_decay"]+cert["exponential_offset"]/cert["exponential_base"]**z
        maximum_slack = slack if maximum_slack is None else max(maximum_slack,slack)
    word_checks=0
    for x in product(range(3),repeat=d):
        boundary_words(rs,x,cert["q"])
        word_checks+=1
    # Exact rational cancellation verifies every acquired edge threshold.
    edges_checked=0
    for (i,j),(_,upper) in cert["pattern"]["beta"].items():
        lower = cert["pattern"]["gamma"][j,i][0]
        assert lower*h[i]>=upper
        edges_checked+=1
    return {"count_states_checked":len(lattice),"boundary_words_checked":word_checks,
            "rational_exponential_generator_states_checked":len(lattice),
            "edge_cancellations_checked":edges_checked,"largest_slack":maximum_slack}


def make_cycle(d):
    def e(i): return tuple(int(j==i) for j in range(d))
    zero=(0,)*d
    rs=[]
    for i in range(d):
        rs += [reaction(zero,e(i),1,2,f"0->{i}"), reaction(e(i),zero,1,2,f"{i}->0")]
    for j,upper in enumerate([3,4,2]):
        i=(j+1)%d
        pair=tuple(a+b for a,b in zip(e(i),e(j)))
        rs += [reaction(e(j),pair,1,upper,f"{j}->{i}+{j}"),
               reaction(pair,e(i),1,2,f"{i}+{j}->{i}")]
    return rs


if __name__ == "__main__":
    start=time.perf_counter()
    cases={"initial_balanced_cross_rescued":fixtures()["balanced_cross_rejection"]}
    cases["strong_birth_rate_boxes"]=[reaction((0,0),(1,0),1,2),
                                     reaction((1,0),(0,0),1,2),
                                     reaction((0,0),(0,1),1,2),
                                     reaction((0,1),(0,0),1,2),
                                     reaction((1,0),(1,1),2,3),
                                     reaction((1,1),(1,0),1,2),
                                     reaction((0,1),(1,1),3,5),
                                     reaction((1,1),(0,1),1,2)]
    cases["three_species_directed_catalytic_cycle"]=make_cycle(3)
    cases["self_autocatalysis"]=fixtures()["autocatalytic"]
    cases["rational_conversions"]=(fixtures()["balanced_cross_rejection"]+
            [reaction((1,0),(0,1),F(1,3),F(2,3)),
             reaction((0,1),(1,0),F(1,5),F(3,5))])
    cases["parallel_rational_channels"]=[reaction((0,),(1,),F(1,4),F(1,2)),
            reaction((1,),(0,),F(1,3),F(2,3)),
            reaction((1,),(2,),F(1,7),F(2,7)),
            reaction((1,),(2,),F(1,11),F(3,11)),
            reaction((2,),(1,),F(1,5),F(3,5)),
            reaction((2,),(1,),F(1,13),F(2,13))]
    output={"scope":"exact rational compiler plus finite symbolic/large-axis diagnostics; no trajectory simulation",
            "fixtures":{}}
    for name,rs in cases.items():
        cert=compile_hinges(rs)
        assert cert["status"]=="CERTIFIED"
        output["fixtures"][name]={"reactions":[{"y":r.y,"yp":r.yp,"lo":r.lo,"hi":r.hi}
                                                     for r in rs],"certificate":cert,
                                  "exact_checks":certify_cells(rs,cert)}
    # This rejection is structural; it does not label the network unstable.
    missing_reciprocal=[reaction((0,0),(1,0)),reaction((1,0),(0,0)),
                        reaction((0,0),(0,1)),reaction((0,1),(0,0)),
                        reaction((1,0),(1,1)),reaction((1,1),(1,0))]
    output["missing_reciprocal_rejection"]=compile_hinges(missing_reciprocal)
    assert output["missing_reciprocal_rejection"]["status"]=="REJECTED_CLASS"
    huge=fixtures()["balanced_cross_rejection"][:4]+[
            reaction((1,0),(1,1),2**40),reaction((1,1),(1,0)),
            reaction((0,1),(1,1),2**40),reaction((1,1),(0,1))]
    compact_start=time.perf_counter()
    compact=compile_hinges(huge,expand_probability=False)
    compact_seconds=time.perf_counter()-compact_start
    assert compact["status"]=="CERTIFIED" and "exponential_offset" not in compact
    assert "success_probability" not in compact and "recovery_constant" not in compact
    assert compact["thresholds"]==[2**40+1,2**40+1]
    output["huge_threshold_compact_fixture"]={"certificate":compact,
            "compact_wall_seconds":compact_seconds,
            "json_bytes":len(json.dumps(serialize(compact)).encode())}
    output["wall_seconds"]=time.perf_counter()-start
    output["script_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    path=Path(__file__).with_name("hinge_checks.json")
    path.write_text(json.dumps(serialize(output),indent=2)+"\n")
    print(json.dumps({"path":str(path),"wall_seconds":output["wall_seconds"],
                      "fixtures":{k:{"thresholds":v["certificate"]["thresholds"],
                                       "C":str(v["certificate"]["C"]),
                                       "B":str(v["certificate"]["B"]),
                                       "expanded_height_bits":v["certificate"]["expanded_height_bits"],
                                       "checks":serialize(v["exact_checks"])}
                                  for k,v in output["fixtures"].items()}},indent=2))
