#!/usr/bin/env python3
"""Exact finite diagnostic. No old fixture and no asymptotic estimate."""
from fractions import Fraction as F
from pathlib import Path
import datetime
import hashlib
import json
import resource
import time

ROOT = Path(__file__).resolve().parent
start_wall = time.perf_counter()
start_cpu = time.process_time()
raw = (ROOT / "INPUTS.json").read_bytes()
inp = json.loads(raw)
freeze = json.loads((ROOT / "FREEZE.json").read_text())
assert hashlib.sha256(raw).hexdigest() == freeze["sha256"]
q0 = list(map(F, inp["q_unnormalized"]))
sq = list(map(F, inp["q_unnormalized_square_roots"]))
assert all(x*x == y for x,y in zip(sq,q0))
q = [x / sum(q0) for x in q0]
pi = list(map(F, inp["pi"]))
Q = [list(map(F,row)) for row in inp["Q"]]
alpha = F(inp["alpha"])
beta = 1-alpha
assert F(inp["eta"]) == F(1,2) and F(inp["kappa"]) == 0
size = len(q)
assert sum(q) == sum(pi) == 1
assert all(x > 0 for x in q+pi)
assert all(sum(row) == 1 and all(x > 0 for x in row) for row in Q)
ratios = [Q[y][x]/Q[x][y] for x in range(size) for y in range(size) if x != y]
assert min(ratios) == F(1,2) and max(ratios) == 2
assert min(q) == F(1,14000001) and 14000001 < 2**24
W = [pi[x]/q[x] for x in range(size)]
A = set(inp["A_states"])
E = set(inp["E_states"])
h = F(inp["h"])
assert A == {x for x in range(size) if W[x] < h}
assert E == set(range(size))-A
N = inp["N"]
threshold = F(inp["exp_U_over_eta"])
assert N == 5 and threshold == 2

L = [[F(0) for _ in range(size)] for _ in range(size)]
G = [[F(0) for _ in range(size)] for _ in range(size)]
for x in range(size):
    for y in range(size):
        if x == y:
            continue
        S = sq[y]/sq[x]
        target_ratio = pi[y]*Q[y][x]/(pi[x]*Q[x][y])
        L[x][y] = Q[x][y]*min(F(1),S)*min(F(1),target_ratio/S)
        G[x][y] = q[y]*min(F(1),W[y]/W[x])
    L[x][x] = 1-sum(L[x])
    G[x][x] = 1-sum(G[x])
C = [[(F(x==y)+alpha*G[x][y]+beta*L[x][y])/2
      for y in range(size)] for x in range(size)]
for P in (L,G,C):
    assert all(sum(row)==1 and all(z>=0 for z in row) for row in P)
    assert all(pi[x]*P[x][y] == pi[y]*P[y][x]
               for x in range(size) for y in range(size))

# Each record is (destination, kind, actual factor, reference factor,
#                 reversed reference factor, exp(signed_increment/eta)).
tags = [[] for _ in range(size)]
for x in range(size):
    tags[x].append((x,"hold",C[x][x],C[x][x],C[x][x],F(1)))
    for y in range(size):
        if x==y:
            continue
        tags[x].append((y,"local",beta*L[x][y]/2,beta*Q[x][y]/2,
                        beta*Q[y][x]/2,q[x]*Q[x][y]/(q[y]*Q[y][x])))
        tags[x].append((y,"global",alpha*G[x][y]/2,alpha*q[y]/2,
                        alpha*q[x]/2,F(1)))
    assert sum(t[2] for t in tags[x]) == 1
    assert sum(t[3] for t in tags[x]) <= F(3,2)
    assert all(t[2] <= t[3] for t in tags[x])
    for y,kind,actual,ref,rev,R in tags[x]:
        assert q[x]*ref == R*q[y]*rev
        if kind == "global":
            assert R == 1

cycle = [0,1,2,0]
cycle_R = F(1)
for x,y in zip(cycle,cycle[1:]):
    cycle_R *= q[x]*Q[x][y]/(q[y]*Q[y][x])
assert cycle_R == 8
reverse_cycle_R = 1/cycle_R
assert reverse_cycle_R == F(1,8)

stats = {"captured_paths":0,"high_signed_paths":0,"low_signed_paths":0,
         "high_signed_global_final_paths":0,"identity_checks":0}
sums = {"capture":F(0),"low_actual":F(0),"low_reference":F(0),
        "low_reverse":F(0),"global_final":F(0),"local_final":F(0)}
by_depth = [F(0) for _ in range(N+1)]

def visit(x,depth,actual_mass,forward_ref,reverse_product,signed_R,positive_R,
          first_threshold,initial_state):
    if depth == N:
        return
    for y,kind,actual,ref,rev,R in tags[x]:
        j = depth+1
        am = actual_mass*actual
        fm = forward_ref*ref
        rp = reverse_product*rev
        sr = signed_R*R
        pr = positive_R*max(R,F(1)) if kind=="local" else positive_R
        crossing = first_threshold
        if crossing is None and pr >= threshold:
            crossing = j
        assert fm == q[y]*rp*sr
        assert am <= fm
        stats["identity_checks"] += 1
        if y in E:
            stats["captured_paths"] += 1
            sums["capture"] += am
            sums[kind+"_final"] += am
            by_depth[j] += am
            if sr >= threshold:
                stats["high_signed_paths"] += 1
                assert crossing is not None and crossing <= j
                if kind == "global":
                    stats["high_signed_global_final_paths"] += 1
                    assert crossing < j
            else:
                stats["low_signed_paths"] += 1
                sums["low_actual"] += am
                sums["low_reference"] += fm
                sums["low_reverse"] += q[y]*rp
            continue
        assert y in A
        visit(y,j,am,fm,rp,sr,pr,crossing,initial_state)

for x in sorted(A):
    visit(x,0,q[x],q[x],F(1),F(1),F(1),None,x)

e = sum(q[x] for x in E)
reverse_bound = e*sum(F(3,2)**j for j in range(1,N+1))
assert sums["low_actual"] <= sums["low_reference"]
assert sums["low_reference"] <= threshold*sums["low_reverse"]
assert sums["low_reverse"] <= reverse_bound
assert reverse_bound <= 3*e*F(3,2)**N

# Independent finite first-hit recurrence, using original C rows.
mu = [q[x] if x in A else F(0) for x in range(size)]
captured = F(0)
dynamic_by_depth = [F(0)]
for _ in range(N):
    hit = sum(mu[x]*C[x][y] for x in A for y in E)
    captured += hit
    dynamic_by_depth.append(hit)
    mu = [sum(mu[x]*C[x][y] for x in A) if y in A else F(0)
          for y in range(size)]
assert captured == sums["capture"]
assert dynamic_by_depth == by_depth
assert stats["high_signed_global_final_paths"] > 0
assert sums["global_final"] > 0 and sums["local_final"] > 0

def encode(x):
    if isinstance(x,F):
        return {"exact":str(x),"approx":float(x)}
    if isinstance(x,list):
        return [encode(v) for v in x]
    if isinstance(x,dict):
        return {k:encode(v) for k,v in x.items()}
    return x

result = {
    "status":"PASS exact rational checks",
    "scope":"finite tagged-path identities and event containment; not a proof of asymptotics or historical novelty",
    "input_sha256":hashlib.sha256(raw).hexdigest(),
    "inputs_tuned":False,
    "native_admission":"K=24 certified; K=1 neither required nor asserted",
    "q":q,"pi":pi,"Q":Q,"L":L,"G":G,"C":C,
    "reference_row_sums":[sum(t[3] for t in row) for row in tags],
    "cycle_progress_ratio":cycle_R,
    "reverse_cycle_progress_ratio":reverse_cycle_R,
    "counts":stats,"path_masses":sums,"first_hit_by_depth":by_depth,
    "reverse_sum_bound":reverse_bound,
    "low_progress_mass_bound":threshold*reverse_bound,
    "actual_global_kill_probability":alpha*e/2,
    "first_hit_dynamic_matches_path_enumeration":True,
    "all_checks_exact":True
}
(ROOT/"RESULT.json").write_text(json.dumps(encode(result),indent=2)+"\n")
receipt = {
    "utc_finished":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "cpu_seconds":time.process_time()-start_cpu,
    "wall_seconds":time.perf_counter()-start_wall,
    "max_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    "inputs_sha256":hashlib.sha256(raw).hexdigest(),
    "code_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "result_sha256":hashlib.sha256((ROOT/"RESULT.json").read_bytes()).hexdigest(),
    "discovery_inference_token_design_costs":"unknown",
    "old_suites_or_fixtures_rerun":False
}
(ROOT/"RESOURCE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps({"status":result["status"],"counts":stats,"resource":receipt},indent=2))
