"""Acquired hinge cores and finite-jump reciprocal attachments.

All writes are in this owned directory. INITIAL dependencies are imported,
never executed as scripts. Output constants use explicit rational-power
expressions; expanded-output costs are charged in MODULAR_RECOVERY.txt.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import ceil
from pathlib import Path
import hashlib
import json
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from hinge_compiler import compile_hinges
from compiler import reaction, falling, serialize, check_weak_reversibility


def support(v):
    return {i for i, x in enumerate(v) if x}


def project(rs, indices):
    return [reaction(tuple(r.y[i] for i in indices),
                     tuple(r.yp[i] for i in indices), r.lo, r.hi, r.name)
            for r in rs]


def aggregate(table, i, r):
    lo, hi = table.get(i, (F(0), F(0)))
    table[i] = (lo+r.lo, hi+r.hi)


def peel_leaf(rs, leaf):
    """Recognize every incident reaction; no unaccounted leaf dynamics."""
    core, birth, death = [], {}, {}
    for r in rs:
        if not (r.y[leaf] or r.yp[leaf]):
            core.append(r)
            continue
        changed = tuple(b-a for a, b in zip(r.y, r.yp))
        others = [i for i, z in enumerate(r.y) if z and i != leaf]
        if any(changed[i] for i in range(len(changed)) if i != leaf):
            return None
        if len(others) != 1 or r.y[others[0]] != 1:
            return None
        parent = others[0]
        if (sum(r.y) == 1 and r.y[leaf] == 0
                and sum(r.yp) == 2 and changed[leaf] == 1):
            aggregate(birth, parent, r)
        elif (sum(r.y) == 2 and r.y[leaf] == 1
                and sum(r.yp) == 1 and changed[leaf] == -1):
            aggregate(death, parent, r)
        else:
            return None
    if not birth or birth.keys() != death.keys():
        return None
    return core, birth, death


def gate_certificate(core, birth, death):
    parents = sorted(birth)
    pset = set(parents)
    immigration_lower, unary_loss_upper, binary_loss_upper = F(0), F(0), F(0)
    for r in core:
        jump = sum(r.yp[i]-r.y[i] for i in parents)
        if not any(r.y) and jump > 0:
            immigration_lower += r.lo
        if jump < 0:
            if not support(r.y) <= pset:
                return None, "negative gate jump has a reactant outside its gate"
            if sum(r.y) == 1:
                unary_loss_upper += r.hi
            elif sum(r.y) == 2:
                binary_loss_upper += r.hi
            else:
                return None, "gate loss has unsupported molecularity"
    if not immigration_lower:
        return None, "gate has no zero-source immigration"
    beta = min(lo for lo, _ in death.values())
    alpha = max(hi for _, hi in birth.values())
    loss_cap = unary_loss_upper/2+2*binary_loss_upper
    c = min(F(1), beta/(2*loss_cap)) if loss_cap else F(1)
    gamma = min(c*immigration_lower/2, beta/2)
    return {"parents": parents, "birth": birth, "death": death,
            "immigration_lower": immigration_lower,
            "unary_loss_upper": unary_loss_upper,
            "binary_loss_upper": binary_loss_upper,
            "loss_cap": loss_cap, "c": c, "G": 1+c,
            "gamma": gamma, "tag_decay": gamma/(1+c),
            "alpha_max": alpha}, None


def recognize(rs):
    d = len(rs[0].y) if rs else 0
    if not d or any(len(r.y) != d or len(r.yp) != d or
                    any(type(x) is not int or x < 0 for x in r.y+r.yp) or
                    sum(r.y) > 2 or sum(r.yp) > 2 or not 0 < r.lo <= r.hi
                    for r in rs):
        return {"status": "REJECTED_CLASS", "reason": "invalid binary input"}
    memo, failures = {}, []

    def search(active, current):
        key = tuple(active)
        if key in memo:
            return memo[key]
        # Additional binary two-count drains decrease every hinge and its
        # exponential. They preserve the earlier inequalities by omission.
        extras = [r for r in current if sum(r.y) == 2 and not any(r.yp)]
        retained = [r for r in current if not (sum(r.y) == 2 and not any(r.yp))]
        base = compile_hinges(project(retained, active), expand_probability=False)
        if base["status"] == "CERTIFIED" and check_weak_reversibility(current):
            H = sum(base["thresholds"])
            scale = H+1
            cert = {"status": "CERTIFIED", "base_species": list(active),
                    "base_hinge": base, "base_scale": scale,
                    "base_extra_monotone_drains": len(extras),
                    "attachments": [], "B": scale*base["B"],
                    "delta": base["delta"], "upper_linear_factor": F(scale)}
            memo[key] = cert
            return cert
        for leaf in active:
            peeled = peel_leaf(current, leaf)
            if peeled is None:
                continue
            core, birth, death = peeled
            gate, reason = gate_certificate(core, birth, death)
            if gate is None:
                failures.append({"leaf": leaf, "parents": sorted(birth), "reason": reason})
                continue
            rest = search(tuple(i for i in active if i != leaf), core)
            if rest is None:
                continue
            M = max(F(1), (gate["G"]*gate["alpha_max"]+1)/rest["delta"])
            delta = min(1/M, gate["gamma"]/gate["G"])
            attachment = dict(gate, leaf=leaf, core_scale=M,
                              previous_B=rest["B"], previous_delta=rest["delta"])
            cert = dict(rest, attachments=rest["attachments"]+[attachment],
                        B=M*rest["B"]+delta, delta=delta,
                        upper_linear_factor=1+M*rest["upper_linear_factor"]+gate["G"])
            memo[key] = cert
            return cert
        memo[key] = None
        return None

    cert = search(tuple(range(d)), rs)
    if cert is None:
        return {"status": "REJECTED_CLASS", "reason": "no admitted hinge/gate decomposition",
                "failed_gates": failures, "searched_subsets": len(memo)}
    cert["searched_subsets"] = len(memo)
    cert["failed_gates"] = failures
    return cert


def potential(cert, x):
    b = cert["base_species"]
    V = cert["base_scale"]*(1+sum(max(0, x[i]-h)
                                    for i, h in zip(b, cert["base_hinge"]["thresholds"])))
    for a in cert["attachments"]:
        S = sum(x[i] for i in a["parents"])
        V = 1+a["core_scale"]*V+(1+a["c"]/(S+1))*x[a["leaf"]]
    return V


def generator_box_max(rs, cert, x):
    old = potential(cert, x)
    result = F(0)
    for r in rs:
        f = falling(x, r.y)
        if f:
            xp = tuple(n+b-a for n, a, b in zip(x, r.y, r.yp))
            jump = potential(cert, xp)-old
            result += f*max(r.lo*jump, r.hi*jump)
    return result


def recipes(rs, cert):
    d = len(rs[0].y)
    production, base_death, leaf_death = {}, {}, {}
    for i in cert["base_species"]:
        production[i] = {"edge": next(k for k, r in enumerate(rs)
                                      if not any(r.y) and r.yp[i] == 1 and sum(r.yp) == 1),
                         "dependencies": [], "length": 1}
        base_death[i] = next(k for k, r in enumerate(rs)
                             if r.y[i] == 1 and sum(r.y) == 1 and not any(r.yp))
    for a in cert["attachments"]:
        j = a["leaf"]
        parent = min(a["parents"], key=lambda i: (production[i]["length"], i))
        production[j] = {"edge": next(k for k, r in enumerate(rs)
                                      if r.y[parent] == 1 and sum(r.y) == 1
                                      and r.yp[j] == 1 and r.yp[parent] == 1 and sum(r.yp) == 2),
                         "dependencies": [parent], "length": production[parent]["length"]+1}
        leaf_death[j] = next(k for k, r in enumerate(rs)
                             if r.y[j] == r.y[parent] == 1 and sum(r.y) == 2
                             and r.yp[parent] == 1 and sum(r.yp) == 1)
    assert len(production) == d
    return {"production": production, "base_death": base_death,
            "leaf_death": leaf_death,
            "one_of_every_species_steps": sum(z["length"] for z in production.values())}


def power(base, exponent):
    return {"rational_base": base, "integer_exponent": exponent}


def compile_network(rs, q=2):
    if type(q) is not int or q < 1:
        return {"status": "REJECTED_CLASS", "reason": "invalid target count"}
    cert = recognize(rs)
    if cert["status"] != "CERTIFIED":
        return cert
    words = recipes(rs, cert)
    B, delta = cert["B"], cert["delta"]
    exponential_core = 2*(B+delta+1)/delta
    count_core = ceil(exponential_core)  # V>=N, W=1+V; deliberately loose.
    d = len(rs[0].y)
    A1 = words["one_of_every_species_steps"]
    Aq = q*A1
    # Every selected production edge adds exactly one molecule, and every
    # selected drain removes exactly one; competing events are suppressed.
    H = count_core+2*A1+Aq
    D = max(count_core+A1, Aq)
    U = sum((r.hi for r in rs), F(0))
    Q = U*(D+1)**2
    alpha = min(r.lo for r in rs)/(2*Q)
    t0 = F(H)/Q
    eta_return = min(delta/2, 1/(2*t0))
    cycle_mgf_cap = 2*(1+exponential_core+B*t0)
    cert["boundary"] = {"q": q, "recipes": words, "exponential_core_W": exponential_core,
                        "core_count_cap": count_core, "attempt_steps": H,
                        "path_count_cap": D, "total_rate_coefficient": U,
                        "total_rate_cap": Q, "one_step_probability": alpha,
                        "attempt_duration": t0, "success_probability": power(alpha, H),
                        "cycle_mgf_at_eta_cap": cycle_mgf_cap, "eta_return": eta_return,
                        "target_decay_expression": "eta_return*p/(2*(cycle_mgf_at_eta_cap+p))",
                        "target_mgf_expression": "(1+V(x))*(2+4/p)",
                        "target_mean_expression": "V(x)+(exponential_core_W+(B+1)*attempt_duration)/p"}
    # A linear recurrence stores each moment node once; no expanded power or
    # duplicated recursive expression tree is hidden in compact acquisition.
    moment_layers = []
    birth_counter_factor = F(2**24, 12)
    for a in cert["attachments"]:
        eta, G, A = a["tag_decay"], a["G"], a["alpha_max"]
        T = (1+4/eta)**4
        moment_layers.append({"leaf": a["leaf"],
                              "old_total_fourth_moment_coefficient":
                                  8*(1+8*G*T*birth_counter_factor*20*A**4),
                              "leaf_initial_fourth_power_coefficient": 64*G,
                              "constant": 64*G*T*birth_counter_factor*16})
    cert["fourth_moment_recurrence"] = moment_layers
    cert["firing_bound_expression"] = "(2/target_decay)*(1+8*U^2*(M4(x)+1)*(1+V(x))*(2+4/p))"
    return cert


def fourth_moment(cert, x):
    """Explicit evaluation can be exponential in count encoding; not acquisition."""
    h = cert["base_hinge"]
    H = sum(h["thresholds"])
    z0 = sum(max(0, x[i]-v) for i, v in zip(cert["base_species"], h["thresholds"]))
    base = h["exponential_base"]
    eps = base-1
    offset = h["exponential_offset_compact"]
    offset_value = offset["rational_coefficient"]*offset["rational_base"]**offset["integer_exponent"]
    exp_bound = base**z0+offset_value/h["exponential_decay"]
    ans = 8*(1296+384*exp_bound/eps**4+H**4)
    for a in cert["fourth_moment_recurrence"]:
        ans = (a["old_total_fourth_moment_coefficient"]*ans
               +a["leaf_initial_fourth_power_coefficient"]*x[a["leaf"]]**4+a["constant"])
    return ans


def expanded_produce(words, i):
    z = words["production"][i]
    return [k for parent in z["dependencies"] for k in expanded_produce(words, parent)]+[z["edge"]]


def apply_word(rs, x, word):
    current, cap = tuple(x), sum(x)
    for k in word:
        r = rs[k]
        assert falling(current, r.y), (current, k)
        current = tuple(n+b-a for n, a, b in zip(current, r.y, r.yp))
        cap = max(cap, sum(current))
    return current, cap


def recovery_word(rs, cert, x, q):
    words = cert["boundary"]["recipes"]
    current, full = tuple(x), []
    for i in range(len(x)):
        w = expanded_produce(words, i)
        after, _ = apply_word(rs, current, w)
        assert all(a >= b+int(j == i) for j, (a, b) in enumerate(zip(after, current)))
        current = after
        full += w
    for a in reversed(cert["attachments"]):
        j = a["leaf"]
        w = [words["leaf_death"][j]]*current[j]
        current, _ = apply_word(rs, current, w)
        full += w
    for i in cert["base_species"]:
        w = [words["base_death"][i]]*current[i]
        current, _ = apply_word(rs, current, w)
        full += w
    assert not any(current)
    for i in range(len(x)):
        w = expanded_produce(words, i)*q
        current, _ = apply_word(rs, current, w)
        full += w
    assert all(n >= q for n in current)
    _, cap = apply_word(rs, x, full)
    A1 = words["one_of_every_species_steps"]
    assert len(full) == sum(x)+2*A1+q*A1
    assert cap <= max(sum(x)+A1, q*A1)
    return len(full), cap


def fixtures():
    def e(d, i): return tuple(int(j == i) for j in range(d))
    def add_leaf(rs, d, parent_set, leaf):
        for parent in parent_set:
            pair = tuple(a+b for a, b in zip(e(d, parent), e(d, leaf)))
            rs.extend([reaction(e(d, parent), pair, F(1, 2), F(3, 2)),
                       reaction(pair, e(d, parent), F(2, 3), F(5, 3))])
    # Nonlinear reciprocal hinge core A,B; no primitive leaf flows.
    d = 4
    zero = (0,)*d
    core = []
    for i in (0, 1):
        core += [reaction(zero, e(d, i), 1, 2), reaction(e(d, i), zero, 1, 2)]
    ab = tuple(a+b for a, b in zip(e(d, 0), e(d, 1)))
    core += [reaction(e(d, 0), ab, 2, 3), reaction(ab, e(d, 0), 1, 2),
             reaction(e(d, 1), ab, 3, 5), reaction(ab, e(d, 1), 1, 2)]
    nonlinear = core[:]
    add_leaf(nonlinear, d, [0, 1], 2)
    add_leaf(nonlinear, d, [0, 1, 2], 3)
    # Self-autocatalytic core exercises exact 2A falling factorials.
    d = 2
    self_core = [reaction((0, 0), (1, 0)), reaction((1, 0), (0, 0)),
                 reaction((1, 0), (2, 0), 2), reaction((2, 0), (1, 0))]
    add_leaf(self_core, d, [0], 1)
    # Genuine two-count negative gate jump, handled by finite-jump inequality.
    pair_loss = [reaction((0, 0), (1, 0)), reaction((1, 0), (0, 0)),
                 reaction((1, 0), (2, 0), 2), reaction((2, 0), (1, 0)),
                 reaction((2, 0), (0, 0), 1, 2)]
    add_leaf(pair_loss, d, [0], 1)
    # Already-known two-layer scope, compiled without a supplied partition.
    d = 3
    roots = []
    for i in (0, 1):
        roots += [reaction((0,)*d, e(d, i), F(1, 3), F(4, 3)),
                  reaction(e(d, i), (0,)*d, F(1, 4), F(5, 4))]
    add_leaf(roots, d, [0, 1], 2)
    # Bare chain has no syntactically drain-closed immigration gate for C.
    bare = [reaction((0, 0, 0), (1, 0, 0)), reaction((1, 0, 0), (0, 0, 0))]
    add_leaf(bare, 3, [0], 1)
    add_leaf(bare, 3, [1], 2)
    return {"hinge_core_two_attachment_depths": nonlinear,
            "self_autocatalytic_core_leaf": self_core,
            "two_count_gate_loss": pair_loss, "two_layer_overlap": roots}, bare


def verify():
    started = time.perf_counter()
    cases, bare = fixtures()
    output = {"fixtures": {}, "scope": "exact finite diagnostics; full proof in MODULAR_RECOVERY.txt"}
    all_counts = {"complete_generator": 0, "gate_killing_coefficients": 0,
                  "production_and_recovery_words": 0, "moment_acquisition": 0}
    for name, rs in cases.items():
        cert = compile_network(rs)
        assert cert["status"] == "CERTIFIED", (name, cert)
        d = len(rs[0].y)
        states = list(product(range(5), repeat=d))
        states += [tuple(10**6 if i == j else int(i % 2) for i in range(d)) for j in range(d)]
        for x in states:
            V = potential(cert, x)
            assert V >= max(1, sum(x))
            assert generator_box_max(rs, cert, x) <= cert["B"]-cert["delta"]*V
            all_counts["complete_generator"] += 1
            active = set(cert["base_species"])
            for a in cert["attachments"]:
                S = sum(x[i] for i in a["parents"])
                g = 1+a["c"]/(S+1)
                Lg = F(0)
                for r in rs:
                    if not (support(r.y)|support(r.yp)) <= active:
                        continue
                    f = falling(x, r.y)
                    if f:
                        Sp = S+sum(r.yp[i]-r.y[i] for i in a["parents"])
                        dg = 1+a["c"]/(Sp+1)-g
                        Lg += f*max(r.lo*dg, r.hi*dg)
                killing = sum(a["death"][i][0]*x[i] for i in a["parents"])
                assert Lg-killing*g <= -a["gamma"]
                all_counts["gate_killing_coefficients"] += 1
                active.add(a["leaf"])
        for x in product(range(3), repeat=d):
            recovery_word(rs, cert, x, 2)
            all_counts["production_and_recovery_words"] += 1
        m4 = fourth_moment(cert, (1,)*d)
        assert m4 >= d**4
        all_counts["moment_acquisition"] += 1
        output["fixtures"][name] = {"certificate": cert, "state_count": len(states),
                                    "M4_at_all_ones": m4,
                                    "M4_height_bits": max(m4.numerator.bit_length(), m4.denominator.bit_length())}
    rejection = compile_network(bare)
    assert rejection["status"] == "REJECTED_CLASS"
    output["bare_chain_rejection"] = rejection
    # Interpolation algebra, independent of rare-event-expanded fixture powers.
    # log M<=M−1 and log(1−p)<=−p imply contraction at theta=p/[2(M+p)].
    interpolation_checks = 0
    for p in (F(1, 100), F(1, 7), F(1, 2)):
        for M in (F(2), F(17, 2), F(10000)):
            theta = p/(2*(M+p))
            assert -(1-theta)*p+theta*(M-1) <= -p/2
            interpolation_checks += 1
    output["interpolation_rational_checks"] = interpolation_checks
    output["counts"] = all_counts
    output["wall_seconds"] = time.perf_counter()-started
    output["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE/"modular_checks.json").write_text(json.dumps(serialize(output), indent=2)+"\n")
    print(json.dumps({"counts": all_counts, "interpolation_checks": interpolation_checks,
                      "wall_seconds": output["wall_seconds"],
                      "fixtures": {k: {"base": v["certificate"]["base_species"],
                                      "leaves": [a["leaf"] for a in v["certificate"]["attachments"]],
                                      "B": str(v["certificate"]["B"]),
                                      "delta": str(v["certificate"]["delta"]),
                                      "attempt_steps": v["certificate"]["boundary"]["attempt_steps"],
                                      "M4_bits": v["M4_height_bits"]}
                                   for k, v in output["fixtures"].items()}}, indent=2))


if __name__ == "__main__":
    verify()
