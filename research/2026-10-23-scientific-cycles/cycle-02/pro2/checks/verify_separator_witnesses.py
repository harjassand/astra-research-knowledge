#!/usr/bin/env python3
"""Independent exact verification of frozen separator/path witnesses.

No producer module is imported. This checks the saved rational inputs and
witnesses, not the universal all-design theorem or provenance beyond the
supplied archive's pinned manifest. Run with --witnesses DIR --output FILE.
"""
import argparse
import copy
import hashlib
import json
import resource
import time
from fractions import Fraction
from pathlib import Path

Q = Fraction


class VerificationError(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise VerificationError(message)


def scalar(value):
    need(isinstance(value, (str, int)) and not isinstance(value, bool), "non-exact scalar")
    return Q(value)


def inner(a, b):
    need(len(a) == len(b), "inner product dimension")
    return sum((x*y for x, y in zip(a, b)), Q(0))


def inverse_square(a):
    n = len(a)
    b = [list(row) + [Q(i == j) for j in range(n)] for i, row in enumerate(a)]
    need(all(len(row) == 2*n for row in b), "inverse shape")
    for j in range(n):
        p = next((i for i in range(j, n) if b[i][j] != 0), None)
        need(p is not None, "apex Gram singular")
        b[j], b[p] = b[p], b[j]
        factor = b[j][j]
        b[j] = [x/factor for x in b[j]]
        for i in range(n):
            if i != j:
                factor = b[i][j]
                b[i] = [x-factor*y for x, y in zip(b[i], b[j])]
    return [row[n:] for row in b]


def exact_rank(a, ncols):
    b = [row[:] for row in a]
    need(all(len(row) == ncols for row in b), "rank shape")
    p = 0
    for j in range(ncols):
        v = next((i for i in range(p, len(b)) if b[i][j]), None)
        if v is None:
            continue
        b[p], b[v] = b[v], b[p]
        factor = b[p][j]
        for i in range(p+1, len(b)):
            if b[i][j]:
                scale = b[i][j]/factor
                b[i] = [x-scale*y for x, y in zip(b[i], b[p])]
        p += 1
        if p == len(b):
            break
    return p


def read_entries(entries, s, m):
    n = s+m
    ans = {}
    for record in entries:
        need(isinstance(record, list) and len(record) == 3, "entry format")
        i, j, raw = record
        need(type(i) is int and type(j) is int and 0 <= i <= j < n, "entry indices")
        need(i == j or i < s or (i >= s and j == i+1), "entry outside joined-path support")
        need((i, j) not in ans, "duplicate entry")
        ans[i, j] = scalar(raw)
    return ans


def multiply(entries, x):
    n, q = len(x), len(x[0])
    y = [[Q(0) for _ in range(q)] for _ in range(n)]
    for (i, j), value in entries.items():
        for k in range(q):
            y[i][k] += value*x[j][k]
            if i != j:
                y[j][k] += value*x[i][k]
    return y


def squared_frobenius(a):
    return sum((inner(row, row) for row in a), Q(0))


def verify_outer(entries, w):
    active = [i for i, value in enumerate(w) if value]
    expected = {(i, j): w[i]*w[j] for i in active for j in active if i <= j}
    need({k: v for k, v in entries.items() if v} == expected, "rank-one matrix differs from ww^T")


def verify_payload(d):
    need(d.get("schema") == "astra.separator_flow.v1", "schema")
    s, m = d.get("s"), d.get("m")
    need(type(s) is int and s >= 0 and type(m) is int and m >= 2*(2*s+1), "dimensions")
    n, q = s+m, s+2
    x = [[scalar(a) for a in row] for row in d["X"]]
    need(len(x) == n and all(len(row) == q for row in x), "input shape")
    row_energy = [inner(row, row) for row in x]
    need(all(a <= 1 for a in row_energy), "row energy cap")
    kind = d.get("kind")
    base = {"kind": kind, "s": s, "m": m, "q": q,
            "maximum_row_energy": str(max(row_energy))}
    if kind in ("apex_kernel", "clique_kernel"):
        w = list(map(scalar, d["w"]))
        need(len(w) == n and any(w), "kernel vector")
        entries = read_entries(d["kernel_entries"], s, m)
        verify_outer(entries, w)
        need(all(sum((w[i]*x[i][k] for i in range(n)), Q(0)) == 0 for k in range(q)), "kernel vector action")
        need(squared_frobenius(multiply(entries, x)) == 0, "kernel matrix action")
        if kind == "apex_kernel":
            need(all(a == 0 for a in w[s:]), "apex witness leaks to path")
            need(exact_rank(x[:s], q) == d["constraint_rank"] < s, "apex rank metadata")
        else:
            leaves = [i-s for i in range(s, n) if w[i]]
            need(len(leaves) <= 2 and (len(leaves) < 2 or leaves[1] == leaves[0]+1), "clique witness support")
            # The null vector itself certifies dependence; reported local rank
            # is diagnostic and need not identify a unique containing clique.
        return {**base, "action_squared": "0", "operator_squared": str(inner(w,w)**2),
                "inverse_ratio": "infinity", "nonzero_entries": sum(v != 0 for v in entries.values())}

    need(kind == "flow", "unknown witness kind")
    h, K = d["h"], 2*s+1
    need(type(h) is int and h == m//(2*K) and h >= 1, "tent scale")
    c = list(map(scalar, d["flow"]))
    alpha = list(map(scalar, d["alpha"]))
    need(len(c) == m+1 and len(alpha) == K and c[0] == c[-1] == 0 and any(c), "flow shape/endpoints")
    tents = [[Q(max(0, h-abs(i-(2*j+1)*h))) for i in range(m+1)] for j in range(K)]
    need(all(c[i] == sum((alpha[j]*tents[j][i] for j in range(K)), Q(0)) for i in range(m+1)), "flow is not the stated tent combination")
    energy = sum(((c[i+1]-c[i])**2 for i in range(m)), Q(0))
    mass = inner(c,c)
    need(energy == scalar(d["tent_energy"]) and mass == scalar(d["tent_mass"]), "tent energy/mass")
    need(energy*h*h <= 3*mass, "tent spectral inequality")

    # Reconstruct the exact orthogonal projection from the input alone.
    t, leaf = x[:s], x[s:]
    if s:
        gi = inverse_square([[inner(a,b) for b in t] for a in t])
        r = [[sum((inner(v,t[b])*gi[b][a] for b in range(s)), Q(0)) for a in range(s)] for v in leaf]
    else:
        r = [[] for _ in leaf]
    z = [[v[k]-sum((r[i][a]*t[a][k] for a in range(s)), Q(0)) for k in range(q)] for i,v in enumerate(leaf)]
    need(all(inner(v, a) == 0 for v in z for a in t), "projection orthogonality")
    norm2 = [inner(v,v) for v in z]
    need(all(a > 0 for a in norm2), "zero quotient row")
    u, v = z[:2]
    kappa = inner(u,u)*inner(v,v)-inner(u,v)**2
    need(kappa > 0 and kappa == scalar(d["kappa"]), "oriented plane scale")
    jz = [[v[k]*inner(u,a)-u[k]*inner(v,a) for k in range(q)] for a in z]
    omega = [inner(jz[i],z[i+1]) for i in range(m-1)]
    need(all(omega), "dependent neighboring quotient rows")
    b = [c[i+1]/omega[i] for i in range(m-1)]
    diag = []
    for i in range(m):
        a = Q(0)
        if i: a += b[i-1]*inner(z[i],z[i-1])
        if i+1 < m: a += b[i]*inner(z[i],z[i+1])
        diag.append(-a/norm2[i])
    flow_entries = read_entries(d["flow_entries"],s,m)
    need(all(flow_entries.get((s+i,s+i),Q(0)) == diag[i] for i in range(m)), "path diagonal formula")
    need(all(flow_entries.get((s+i,s+i+1),Q(0)) == b[i] for i in range(m-1)), "path edge formula")
    br = [[diag[i]*r[i][a] + (b[i-1]*r[i-1][a] if i else 0) +
           (b[i]*r[i+1][a] if i+1 < m else 0) for a in range(s)] for i in range(m)]
    need(all(flow_entries.get((a,s+i),Q(0)) == -br[i][a] for a in range(s) for i in range(m)), "lift border formula")
    need(all(flow_entries.get((a,b0),Q(0)) == sum((r[i][a]*br[i][b0] for i in range(m)),Q(0))
             for a in range(s) for b0 in range(a,s)), "lift apex formula")
    action = multiply(flow_entries,x)
    need(all(value == 0 for row in action[:s] for value in row), "apex action does not cancel")
    need(all(action[s+i][k] == (c[i+1]-c[i])*jz[i][k]/(kappa*norm2[i])
             for i in range(m) for k in range(q)), "transverse action identity")
    action2 = squared_frobenius(action)
    need(action2 > 0 and action2 == scalar(d["flow_action_squared"]), "flow action norm")
    op_lower2 = max(a*a for a in b)
    ratio2 = op_lower2/action2
    need(op_lower2 == scalar(d["flow_operator_lower_squared"]) and ratio2 == scalar(d["flow_ratio_squared"]), "flow operator/ratio lower bound")

    # Independent finite-dimensional rank check of the homogeneous constraints.
    matrix=[]
    for a in range(s):
        for basis in (u,v):
            matrix.append([sum((r[i][a]*(f[i+1]-f[i])*inner(jz[i],basis)/norm2[i]
                                for i in range(m)),Q(0)) for f in tents])
    rank=exact_rank(matrix,K)
    need(rank == d["constraint_rank"] and rank <= 2*s, "constraint rank")
    need(all(inner(row,alpha) == 0 for row in matrix), "tent coefficients do not cancel constraints")

    w=list(map(scalar,d["local_w"]))
    need(len(w) == n, "local vector length")
    leaves=[i for i in range(m) if w[s+i] != 0]
    need(len(leaves) == 1, "local witness needs one path vertex")
    i=leaves[0]
    need(w[s+i] == 1 and w[:s] == [-a for a in r[i]], "local projection witness")
    need(norm2[i] == min(norm2), "local witness not at minimum quotient row")
    local_entries=read_entries(d["local_entries"],s,m)
    verify_outer(local_entries,w)
    local_action2=squared_frobenius(multiply(local_entries,x))
    w2=inner(w,w)
    need(local_action2 == w2*norm2[i] == scalar(d["local_action_squared"]), "local action identity")
    need(w2*w2 == scalar(d["local_operator_squared"]), "local operator norm")
    local_ratio2=w2*w2/local_action2
    need(local_ratio2 == scalar(d["local_ratio_squared"]), "local exact ratio")
    bound=Q(h*h,3*(m-1))
    need(bound == scalar(d["guaranteed_ratio_fourth"]), "uniform rational bound")
    maximum=max(ratio2,local_ratio2)
    need(maximum**2 >= bound, "rational fourth-power bound not certified")
    return {**base,"constraint_rank":rank,"flow_action_squared":str(action2),
            "flow_operator_lower_squared":str(op_lower2),"flow_ratio_squared":str(ratio2),
            "local_ratio_squared":str(local_ratio2),"maximum_certified_ratio_squared":str(maximum),
            "maximum_certified_ratio_approx":float(maximum)**0.5,
            "guaranteed_ratio_fourth":str(bound),"flow_nonzero_entries":sum(a != 0 for a in flow_entries.values())}


def main(witnesses,output):
    begin=time.perf_counter();cpu=time.process_time()
    receipt_path=witnesses/"PRODUCER_RECEIPT.json"
    receipt_bytes=receipt_path.read_bytes()
    producer=json.loads(receipt_bytes)
    need(producer["status"] == "passed" and producer["case_count"] == 7 and len(producer["cases"]) == 7,"producer manifest count")
    records=[]
    for rec in producer["cases"]:
        start=time.perf_counter();cstart=time.process_time()
        path=witnesses/rec["filename"]
        data=path.read_bytes();digest=hashlib.sha256(data).hexdigest()
        need(len(data) == rec["bytes"] and digest == rec["sha256"],"source byte identity")
        answer=verify_payload(json.loads(data))
        need(answer["kind"] == rec["kind"] and answer["s"] == rec["s"] and answer["m"] == rec["m"] and answer["q"] == rec["q"],"manifest dimensions")
        if answer["kind"] == "flow":
            need(answer["maximum_certified_ratio_squared"] == rec["max_certified_ratio_squared"],"manifest ratio")
        records.append({"filename":path.name,"bytes":len(data),"sha256":digest,**answer,
                        "wall_seconds":time.perf_counter()-start,"cpu_seconds":time.process_time()-cstart})
    small=json.loads((witnesses/"flow_s2_m20.json").read_text())
    mutations=[]
    bad=copy.deepcopy(small)
    index=next(i for i,(a,b,value) in enumerate(bad["flow_entries"]) if a>=bad["s"] and b==a+1)
    bad["flow_entries"][index][2]=str(scalar(bad["flow_entries"][index][2])+1)
    mutations.append(("change path coefficient",bad))
    bad=copy.deepcopy(small);bad["flow_entries"].append([bad["s"],bad["s"]+2,"1"])
    mutations.append(("add forbidden support edge",bad))
    bad=copy.deepcopy(small);bad["X"][0][0]="2"
    mutations.append(("violate row cap",bad))
    bad=copy.deepcopy(small);bad["guaranteed_ratio_fourth"]="1000000"
    mutations.append(("inflate lower bound",bad))
    rejected=[]
    for label,bad in mutations:
        try: verify_payload(bad)
        except VerificationError as exc: rejected.append({"mutation":label,"rejected_by":str(exc)})
        else: raise VerificationError("tamper accepted: "+label)
    result={"status":"passed","scope":"Independent Fraction verification; no producer import, solver, input regeneration or old benchmark",
            "source_binding":"Each frozen exact-X witness is byte/hash matched to PRODUCER_RECEIPT.json; archive trust requires its external digest.",
            "producer_receipt_sha256":hashlib.sha256(receipt_bytes).hexdigest(),"case_count":len(records),"cases":records,
            "tamper_rejections":rejected,"wall_seconds":time.perf_counter()-begin,"cpu_seconds":time.process_time()-cpu,
            "peak_rss_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
            "timer_scope":"Body including file reads, hash checks, exact arithmetic, four tamper checks; per-case timers nested in body; imports excluded"}
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--witnesses",type=Path,default=Path(__file__).resolve().parents[1]/"witnesses")
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args();main(args.witnesses,args.output)
