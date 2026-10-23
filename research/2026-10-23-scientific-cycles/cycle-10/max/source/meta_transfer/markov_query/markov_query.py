#!/usr/bin/env python3
"""One frozen exact Markov observation-refinement check; no owner suite rerun."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import math
import resource
import signal
import sys
import time
import traceback

BASE = Path(__file__).resolve().parent
sys.set_int_max_str_digits(0)
METRICS = {}
CHECKS = 0


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(name, obj):
    (BASE / name).write_text(json.dumps(obj, indent=2) + "\n")


def require(value, name):
    global CHECKS
    CHECKS += 1
    if not value:
        raise AssertionError(name)


def measure(name, fn):
    cpu, wall = time.process_time(), time.monotonic()
    result = fn()
    METRICS[name] = {"cpu_seconds": time.process_time()-cpu,
                     "wall_seconds": time.monotonic()-wall}
    write("PROGRESS.json", {"completed_stages": METRICS, "checks": CHECKS})
    return result


def raw(x):
    return [str(x.numerator), str(x.denominator)]


def parse(x):
    return F(int(x[0]), int(x[1]))


def described(x):
    exact = str(x.numerator) + "/" + str(x.denominator)
    result = {"float_diagnostic": float(x), "exact_sha256": sha(exact.encode()),
              "numerator_bits": abs(x.numerator).bit_length(),
              "denominator_bits": x.denominator.bit_length()}
    if len(exact) < 2000:
        result["exact"] = exact
    return result


def grouped(labels):
    groups = defaultdict(list)
    for i, label in enumerate(labels):
        groups[label].append(i)
    return sorted(groups.values(), key=lambda block: block[0])


def load_and_prepare(protocol):
    freeze = json.loads((BASE/"FREEZE.json").read_text())
    for item in freeze["files"]:
        p = (BASE/item["path"]).resolve()
        require(sha(p.read_bytes()) == item["sha256"], "frozen input changed: "+str(p))
    source = (BASE/protocol["source_root"]).resolve()
    native_inputs = json.loads((source/protocol["source_inputs"]).read_text())
    fixture = next(f for f in native_inputs["fixtures"]
                   if f["id"] == protocol["fixture_id"])
    evidence = json.loads((source/protocol["source_admission"]).read_text())
    require(evidence["all_frozen_gates_pass"], "source fixture not admitted")
    require(evidence["inputs"] == fixture, "admitted fixture identity differs")
    require(fixture["orientation"] == "expansion", "only frozen expansion allowed")
    eta, kappa, ratio = F(fixture["eta"]), F(fixture["kappa"]), F(fixture["R"])
    b, p, alpha = F(fixture["b"]), F(fixture["p"]), F(fixture["alpha"])
    m, depth, horizon = fixture["M"], fixture["depth"], fixture["n"]
    require(horizon == protocol["horizon"], "source horizon changed")
    z = F(m)/(ratio**int(kappa/eta))
    q = [b*z**i for i in range(depth+1)]
    pi = [p/F(horizon)**(2*(depth-i)) for i in range(depth+1)]
    q.append(1-sum(q)); pi.append(1-sum(pi))
    require(q == [parse(x) for x in evidence["quotient_q_exact"]], "source q mismatch")
    require(pi == [parse(x) for x in evidence["quotient_pi_exact"]], "source pi mismatch")
    levels, edges, cursor = [0], [], 0
    while cursor < len(levels):
        if levels[cursor] < depth:
            for _ in range(m):
                child = len(levels)
                levels.append(levels[cursor]+1)
                edges.append((cursor, child))
        cursor += 1
    levels.append(depth+1)
    n = len(levels)
    multiplicity = [levels.count(i) for i in range(depth+2)]
    qn = [q[level]/multiplicity[level] for level in levels]
    pin = [pi[level]/multiplicity[level] for level in levels]
    weights = [pin[i]/qn[i] for i in range(n)]
    proposal = [dict() for _ in range(n)]
    for parent, child in edges:
        proposal[parent][child] = 1/(m+ratio)
        proposal[child][parent] = ratio/(m+ratio)
    local = [dict() for _ in range(n)]
    edge_hash = hashlib.sha256()
    for x, row in enumerate(proposal):
        for y, qxy in row.items():
            qyx = proposal[y][x]
            qr = qyx/qxy
            target_ratio = pin[y]*qyx/(pin[x]*qxy)
            local[x][y] = qxy*min(F(1), target_ratio)
            edge_hash.update(f"{x},{y},{qxy},{qr},{target_ratio},{local[x][y]}\n".encode())
        local[x][x] = 1-sum(local[x].values(), F(0))
    require(edge_hash.hexdigest() == evidence["native_edge_digest"], "native edge digest mismatch")
    global_kernel = [[F(0) for _ in range(n)] for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if x != y:
                global_kernel[x][y] = qn[y]*min(F(1), weights[y]/weights[x])
        global_kernel[x][x] = 1-sum(global_kernel[x])
    P = [[(F(x == y)+alpha*global_kernel[x][y]+(1-alpha)*local[x].get(y,F(0)))/2
          for y in range(n)] for x in range(n)]
    require(n == evidence["native_states"] == 32, "native dimension changed")
    require(all(min(row) >= 0 and sum(row) == 1 for row in P), "native stochasticity")
    require(all(pin[x]*P[x][y] == pin[y]*P[y][x]
                for x in range(n) for y in range(n)), "native detailed balance")
    old = grouped(levels)
    stored = [[parse(x) for x in row] for row in evidence["quotient_C_exact"]]
    for x in range(n):
        sums = [sum((P[x][y] for y in block),F(0)) for block in old]
        require(sums == stored[levels[x]], "native to source C mismatch")
    A = set(protocol["new_event_vertices"])
    require(0 < len(A) < multiplicity[depth], "not a proper terminal subset")
    require(all(levels[x] == depth for x in A), "event is not terminal")
    return {"P":P, "initial":qn, "pi":pin, "levels":levels,
            "old_partition":old, "event":[int(x in A) for x in range(n)],
            "full_event":[int(level == depth) for level in levels],
            "evidence":evidence, "fixture":fixture, "edge_digest":edge_hash.hexdigest()}


def refine(P, observation):
    blocks = grouped(observation)
    rounds = [blocks]
    while True:
        next_blocks = []
        for block in blocks:
            pieces = defaultdict(list)
            for x in block:
                signature = tuple(sum((P[x][y] for y in dest), F(0)) for dest in blocks)
                pieces[signature].append(x)
            next_blocks.extend(pieces.values())
        next_blocks = sorted(next_blocks, key=lambda block: block[0])
        if len(next_blocks) == len(blocks):
            require(next_blocks == blocks, "stable partition relabelled unexpectedly")
            return blocks, rounds
        blocks = next_blocks
        rounds.append(blocks)


def quotient(P, initial, observation, blocks):
    Q, start, obs = [], [], []
    for block in blocks:
        require(len({observation[x] for x in block}) == 1, "observation not block constant")
        reference = [sum((P[block[0]][y] for y in dest), F(0)) for dest in blocks]
        for x in block:
            require(reference == [sum((P[x][y] for y in dest),F(0)) for dest in blocks],
                    "claimed quotient not strongly lumpable")
        Q.append(reference)
        start.append(sum((initial[x] for x in block), F(0)))
        obs.append(observation[block[0]])
    return Q, start, obs


def averaged_quotient(P, initial, observation, blocks):
    start = [sum((initial[x] for x in block),F(0)) for block in blocks]
    Q = [[sum((initial[x]*P[x][y] for x in block for y in dest),F(0))/start[i]
          for dest in blocks] for i, block in enumerate(blocks)]
    obs = [observation[block[0]] for block in blocks]
    return Q, start, obs


def integer_model(P, initial):
    d = math.lcm(*(x.denominator for row in P for x in row))
    q = math.lcm(*(x.denominator for x in initial))
    matrix = [[(j,x.numerator*(d//x.denominator)) for j,x in enumerate(row) if x]
              for row in P]
    vector = [x.numerator*(q//x.denominator) for x in initial]
    return matrix, vector, d, q


def forward(vector, matrix):
    out = [0]*len(vector)
    for x, value in enumerate(vector):
        if value:
            for y, coefficient in matrix[x]:
                out[y] += value*coefficient
    return out


def query(P, initial, observation, horizon):
    matrix, vector, d, q = integer_model(P, initial)
    n = len(vector)
    powers = [1]
    backward = [observation[:]]
    for _ in range(horizon):
        powers.append(powers[-1]*d)
        previous = backward[-1]
        backward.append([sum(coefficient*previous[y] for y,coefficient in row)
                         for row in matrix])
    phases = [[value*(1-observation[x]) for x,value in enumerate(vector)],
              [value*observation[x] for x,value in enumerate(vector)],
              [0]*n, [0]*n]
    first_numerators = [sum(phases[1])]
    joint_numerators = [sum(phases[1][x]*backward[horizon][x] for x in range(n))]
    for t in range(1, horizon+1):
        z0,z1,z2,z3 = [forward(v,matrix) for v in phases]
        hit = [z0[x]*observation[x] for x in range(n)]
        first_numerators.append(sum(hit))
        joint_numerators.append(sum(hit[x]*backward[horizon-t][x] for x in range(n)))
        phases = [[z0[x]*(1-observation[x]) for x in range(n)],
                  [(z0[x]+z1[x])*observation[x] for x in range(n)],
                  [(z1[x]+z2[x])*(1-observation[x]) for x in range(n)],
                  [z3[x]+z2[x]*observation[x] for x in range(n)]]
        require(sum(map(sum,phases)) == q*powers[t], "history propagation lost mass")
    common = q*powers[horizon]
    first = [F(value,q*powers[t]) for t,value in enumerate(first_numerators)]
    joint = [F(value,common) for value in joint_numerators]
    survival = F(sum(phases[0]),common)
    reentered = F(sum(phases[3]),common)
    final_vector = [F(sum(phase[x] for phase in phases),common) for x in range(n)]
    final_event = sum((final_vector[x] for x in range(n) if observation[x]),F(0))
    require(sum(first)+survival == 1, "first hit plus survival mismatch")
    require(sum(joint) == final_event, "first hit final joint misses returns")
    return {"first_hit":first, "first_hit_and_final_event":joint,
            "survival":survival, "ever_hit":1-survival,
            "exit_then_reentry":reentered, "final_event":final_event,
            "final_vector":final_vector,
            "integer_kernel_denominator_bits":d.bit_length(),
            "integer_initial_denominator_bits":q.bit_length()}


def serial_law(law):
    result = {}
    for key, value in law.items():
        if isinstance(value,list):
            result[key] = [raw(x) for x in value]
        elif isinstance(value,F):
            result[key] = raw(value)
        else:
            result[key] = value
    return result


def main():
    resource.setrlimit(resource.RLIMIT_AS, (512*1024*1024,512*1024*1024))
    resource.setrlimit(resource.RLIMIT_CPU, (80,85))
    def timeout_handler(signum, frame):
        raise RuntimeError("Frozen CPU soft limit reached; no continuation or rerun")
    signal.signal(signal.SIGXCPU, timeout_handler)
    began_cpu, began_wall = time.process_time(), time.monotonic()
    started = datetime.now(timezone.utc).isoformat()
    try:
        protocol = json.loads((BASE/"PROTOCOL.json").read_text())
        model = measure("source_preparation_and_validation", lambda:load_and_prepare(protocol))
        P, initial, event = model["P"], model["initial"], model["event"]
        old, old_rounds = measure("ordinary_refinement_full_terminal",
                                  lambda:refine(P,model["full_event"]))
        require(old == model["old_partition"], "ordinary refinement differs from actual level quotient")
        blocks, rounds = measure("ordinary_refinement_changed_event",lambda:refine(P,event))
        Q, start, obs = measure("stable_quotient_certificate_and_build",
                                lambda:quotient(P,initial,event,blocks))
        level_member = grouped(list(zip(model["levels"],event)))
        A = {x for x,o in enumerate(event) if o}
        row7 = sum((P[7][y] for y in A),F(0))
        row8 = sum((P[8][y] for y in A),F(0))
        require(model["levels"][15] == model["levels"][17] and event[15] != event[17],
                "old level observation witness failed")
        require(model["levels"][7] == model["levels"][8] and event[7] == event[8],
                "level membership witness states differ")
        require(row7-row8 == F(1,7), "predeclared transition witness differs")
        averaged = measure("invalid_level_membership_averaged_build",
                           lambda:averaged_quotient(P,initial,event,level_member))
        horizon = protocol["horizon"]
        native_law = measure("full_native_exact_history_query",lambda:query(P,initial,event,horizon))
        quotient_law = measure("ordinary_refined_exact_history_query",lambda:query(Q,start,obs,horizon))
        invalid_law = measure("invalid_averaged_exact_history_query",lambda:query(*averaged,horizon))
        for key in ("first_hit","first_hit_and_final_event","survival",
                    "ever_hit","exit_then_reentry","final_event"):
            require(native_law[key] == quotient_law[key],"refined query mismatch: "+key)
        source_final = [parse(x) for x in model["evidence"]["full_law_exact"]]
        native_level_final = [sum((native_law["final_vector"][x] for x in block),F(0))
                              for block in old]
        require(native_level_final == source_final, "native full-law source output mismatch")
        require(native_law["final_event"] == source_final[4]/4,
                "symmetric native single-time subset marginal differs")
        native_aggregate_final = [sum((native_law["final_vector"][x] for x in block),F(0))
                                 for block in blocks]
        require(native_aggregate_final == quotient_law["final_vector"],"final block law mismatch")
        differences = []
        for key in ("first_hit","first_hit_and_final_event"):
            for t,(a,b) in enumerate(zip(native_law[key],invalid_law[key])):
                if a != b:
                    differences.append({"query":key,"first_differing_time":t,
                                        "native":described(a),"averaged":described(b),
                                        "native_minus_averaged":described(a-b)})
                    break
        require(bool(differences), "no observed q-start averaged history failure")
        exact = {"native":serial_law(native_law),"refined":serial_law(quotient_law),
                 "invalid_q_weighted_average":serial_law(invalid_law)}
        measure("exact_law_serialization",lambda:write("EXACT_LAWS.json",exact))
        certificate = {"event_vertices":sorted(A), "fixture":model["fixture"],
                       "native_edge_digest":model["edge_digest"],
                       "old_partition":old,"old_refinement_rounds":old_rounds,
                       "changed_partition":blocks,"changed_refinement_rounds":rounds,
                       "level_times_membership_partition":level_member,
                       "quotient_kernel":[[raw(x) for x in row] for row in Q],
                       "quotient_initial":[raw(x) for x in start],
                       "quotient_observation":obs,
                       "old_level_counterexample":{"states":[15,17],"level":4,"observations":[1,0]},
                       "level_times_membership_counterexample":{"states":[7,8],"level":3,
                           "observations":[0,0],"one_step_A":[raw(row7),raw(row8)],
                           "difference":raw(row7-row8)},
                       "q_start_history_failures":differences}
        measure("certificate_serialization",lambda:write("CERTIFICATE.json",certificate))
        result = {"status":"PASS_SCOPED_CONVENTIONAL_RECEIVING_CHECK",
                  "started_utc":started,"fixture_unchanged":True,
                  "inadmissible_coalescence_executed":False,"native_states":len(P),
                  "old_level_states":len(old),"old_level_membership_states":len(level_member),
                  "refined_states":len(blocks),
                  "old_strict_refinement_rounds":len(old_rounds)-1,
                  "changed_strict_refinement_rounds":len(rounds)-1,
                  "all_required_exact_queries_agree":True,
                  "q_start_history_failures":differences,
                  "probabilities":{key:described(native_law[key]) for key in
                                   ("survival","ever_hit","exit_then_reentry","final_event")},
                  "stage_costs":METRICS,"checks":CHECKS,
                  "cpu_seconds_before_result_write":time.process_time()-began_cpu,
                  "wall_seconds_before_result_write":time.monotonic()-began_wall,
                  "peak_rss_kib_linux":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  "development_inference_cost":"Unmetered; not included in executable timings",
                  "scope":"Ordinary exact aggregation is the tested operation; no novel algorithm, capability advantage, independent scientific invention, or asymptotic theorem.",
                  "freeze_sha256":sha((BASE/"FREEZE.json").read_bytes()),
                  "exact_laws_sha256":sha((BASE/"EXACT_LAWS.json").read_bytes()),
                  "certificate_sha256":sha((BASE/"CERTIFICATE.json").read_bytes())}
        write("RESULT.json",result)
        print(json.dumps({key:result[key] for key in ("status","native_states","refined_states",
                         "stage_costs","cpu_seconds_before_result_write","peak_rss_kib_linux")},indent=2))
        return 0
    except BaseException as exc:
        write("FAILURE.json",{"status":"FAILED_OR_INCOMPLETE_NO_RERUN","exception":repr(exc),
                              "traceback":traceback.format_exc(),"completed_stages":METRICS,
                              "checks":CHECKS,"cpu_seconds":time.process_time()-began_cpu,
                              "wall_seconds":time.monotonic()-began_wall})
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
