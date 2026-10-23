#!/usr/bin/env python3
"""Independent exact verifier for the new cone/core/projection witnesses.

Imports no producer code. All certificate arithmetic is fractions.Fraction.
The all-design theorem is a separate proof; this checks the saved exact inputs.
"""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from functools import reduce
from math import gcd, lcm
from pathlib import Path
import argparse
import hashlib
import json
import resource
import time


F = Fraction
RANK_CACHE = {}


class VerificationError(Exception):
    pass


def need(condition, message):
    if not condition:
        raise VerificationError(message)


def rational(value):
    need(isinstance(value, str), "non-string rational")
    try:
        result = F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise VerificationError("invalid rational") from exc
    need(str(result) == value, "noncanonical rational")
    return result


def dot(a, b):
    need(len(a) == len(b), "dot dimension")
    return sum((x*y for x, y in zip(a, b)), F(0))


def matrix(rows, width):
    need(isinstance(rows, list), "matrix format")
    result = []
    for row in rows:
        need(isinstance(row, list) and len(row) == width, "matrix width")
        result.append([rational(x) for x in row])
    return result


def entries(raw, n, edges):
    result = {}
    for item in raw:
        need(isinstance(item, list) and len(item) == 3, "coefficient format")
        i, j, value = item
        need(type(i) is int and type(j) is int and 0 <= i <= j < n,
             "coefficient index")
        need((i,j) not in result, "duplicate coefficient")
        need(i == j or (i,j) in edges, "forbidden support")
        value = rational(value)
        need(value != 0, "explicit zero coefficient")
        result[i,j] = value
    return result


def multiply(d, x, width):
    y = [[F(0)]*width for _ in x]
    for (i,j), value in d.items():
        for k in range(width):
            y[i][k] += value*x[j][k]
            if i != j:
                y[j][k] += value*x[i][k]
    return y


def norm_squared(a):
    return sum((dot(row,row) for row in a), F(0))


def canonical_input_hash(data):
    value = {key:data[key] for key in ("n", "q", "edges", "X")}
    return hashlib.sha256(json.dumps(value, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def rank(a):
    """Integer row elimination after clearing denominators; no producer RREF."""
    if not a:
        return 0
    rows = []
    for row in a:
        den = lcm(*(x.denominator for x in row))
        values = [x.numerator*(den//x.denominator) for x in row]
        divisor = reduce(gcd, values, 0)
        rows.append([x//divisor for x in values] if divisor else values)
    width, pivot = len(rows[0]), 0
    for column in range(width):
        chosen = next((i for i in range(pivot,len(rows)) if rows[i][column]), None)
        if chosen is None:
            continue
        rows[pivot], rows[chosen] = rows[chosen], rows[pivot]
        p = rows[pivot][column]
        for i in range(pivot+1,len(rows)):
            value = rows[i][column]
            if value:
                new = [p*rows[i][j]-value*rows[pivot][j]
                       for j in range(column+1,width)]
                divisor = reduce(gcd, new, 0)
                if divisor:
                    new = [x//divisor for x in new]
                rows[i] = [0]*(column+1)+new
        pivot += 1
        if pivot == len(rows):
            break
    return pivot


def clique_path_edges(clique, path):
    edges = {(min(u,v),max(u,v)) for i,u in enumerate(clique) for v in clique[i+1:]}
    edges.update((min(u,v),max(u,v)) for u in clique for v in path)
    edges.update((min(u,v),max(u,v)) for u,v in zip(path,path[1:]))
    return edges


def core_check(data, x, d, y, edges):
    p = data["parameters"]
    t, copies, length = p["t"],p["N"],p["M"]
    need(type(t) is int and t >= 2 and copies > 0 and length >= 2,
         "core parameters")
    s, h = t-1,t*(t+1)//2
    q = h+t
    m = q*s-t*s//2+2
    n0 = s+m
    need((p["h"],p["q"],p["root_path"],p["root_n"],data["q"])
         == (h,q,m,n0,q), "core parameter identities")
    root_edges = clique_path_edges(list(range(s)),list(range(s,n0)))
    expected_edges = set(root_edges)
    b = entries(data["core_D"],n0,root_edges)
    need({ij:v for ij,v in d.items() if ij[1] < n0} == b,
         "principal core mismatch")
    need(max((a*a for a in b.values()),default=F(0))
         >= rational(data["operator_lower_squared"]), "core operator entry bound")
    by = multiply(b,x[:n0],q)
    need(all(not any(row) for row in y[:n0]), "nonzero root action")
    need(all(not any(by[i]) for i in range(s)), "nonzero core clique action")
    ports = data["ports"]
    need([port["vertex"] for port in ports] == list(range(s,n0)), "port vertices")
    used = set()
    expected_d = dict(b)
    projections = {}
    for port in ports:
        v = port["vertex"]
        u = matrix(port["basis"],q)
        need(len(u) == h, "port dimension")
        need(all(dot(a,b) == int(i==j) for i,a in enumerate(u) for j,b in enumerate(u)),
             "port frame not orthonormal")
        projection = [[sum((row[i]*row[j] for row in u),F(0))
                       for j in range(q)] for i in range(q)]
        projections[v] = projection
        leaves = port["vertices"]
        need(len(leaves) == copies*(length+s-1), "port leaf count")
        need(all(type(i) is int and n0 <= i < data["n"] for i in leaves),
             "port leaf index")
        need(len(set(leaves)) == len(leaves) and not used.intersection(leaves),
             "overlapping child vertices")
        used.update(leaves)
        local_copies = port["copies"]
        need(len(local_copies) == copies, "child copy count")
        need([i for local in local_copies for i in local[1:]] == leaves,
             "child/port vertex mismatch")
        for local in local_copies:
            need(len(local) == s+length and local[0] == v and len(set(local)) == len(local),
                 "child graph vertices")
            expected_edges.update(clique_path_edges(local[:s],local[s:]))
        scale = rational(port["gram_scale"])
        need(scale == F(len(leaves),h) and scale > 0, "port Gram scale")
        counts = Counter(tuple(x[i]) for i in leaves)
        gram = [[sum((count*row[i]*row[j] for row,count in counts.items()),F(0))
                 for j in range(q)] for i in range(q)]
        need(gram == [[scale*a for a in row] for row in projection], "actual port Gram")
        need([dot(row,by[v]) for row in projection] == by[v], "core action outside port")
        for leaf in leaves:
            value = -dot(x[leaf],by[v])/scale
            if value:
                expected_d[min(v,leaf),max(v,leaf)] = value
    need(used == set(range(n0,data["n"])), "uncovered child vertices")
    need(expected_edges == edges, "full core/child graph mismatch")
    need(expected_d == d, "spoke cancellation coefficient mismatch")
    variables = [(i,i) for i in range(n0)]+sorted(root_edges)
    need(data["root_variables"] == len(variables) == (t+1)*m+t*(t-1)//2-1,
         "core variable count")
    need(data["constraint_rows"] == t*m+q*s == len(variables)-1,
         "core constraint count")
    cache_key = json.dumps({"x":data["X"][:n0],"ports":[p["basis"] for p in ports],"t":t},
                          sort_keys=True,separators=(",",":"))
    if cache_key not in RANK_CACHE:
        conditions = []
        for v in range(n0):
            complement = [[F(i==j) for j in range(q)] for i in range(q)]
            if v in projections:
                complement = [[a-b for a,b in zip(row,pr)]
                              for row,pr in zip(complement,projections[v])]
            for functional in complement:
                conditions.append([dot(x[j],functional) if i==v else
                                   dot(x[i],functional) if j==v else F(0)
                                   for i,j in variables])
        RANK_CACHE[cache_key] = rank(conditions)
    observed_rank = RANK_CACHE[cache_key]
    need(data["constraint_rank"] == observed_rank, "core constraint rank")
    return {"root_rows_zero":n0,"ports":len(ports),"constraint_rank":observed_rank,
            "all_port_Grams_exact":True,"all_spoke_coefficients_exact":True}


def cone_check(data, x, d, y, edges):
    p = data["parameters"]
    k, copies, m = p["k"],p["copies"],p["m"]
    q = data["q"]
    apex = rational(p["apex"])
    need(apex != 0 and q == k+1 and copies == k+1 and data["n"] == 1+copies*m,
         "cone parameters")
    need(x[0] == [F(0)]*k+[apex], "cone apex row")
    alpha = [rational(a) for a in data["alpha"]]
    need(len(alpha) == copies and max(abs(a) for a in alpha) == 1,
         "cone coefficient normalization")
    need(len(data["local_data"]) == copies, "cone block count")
    expected_edges, expected_d, constraints = set(),{},[]
    a00 = F(0)
    local_action_sum = F(0)
    for block, local in enumerate(data["local_data"]):
        offset = 1+block*m
        local_edges = {(i,i+1) for i in range(m-1)}
        expected_edges.update((0,offset+i) for i in range(m))
        expected_edges.update((offset+i,offset+j) for i,j in local_edges)
        z = matrix(local["Z"],k)
        r = [rational(value) for value in local["R"]]
        need(len(z) == m and len(r) == m, "cone local dimensions")
        need(z == [row[:k] for row in x[offset:offset+m]], "cone Z input binding")
        need(r == [row[k]/apex for row in x[offset:offset+m]], "cone R input binding")
        b = entries(local["B"],m,local_edges)
        bz = multiply(b,z,k)
        constraint = [sum((r[i]*bz[i][j] for i in range(m)),F(0)) for j in range(k)]
        need(constraint == [rational(a) for a in local["constraint"]], "cone local constraint")
        constraints.append(constraint)
        weighted = {ij:alpha[block]*a for ij,a in b.items() if alpha[block]*a}
        br = multiply(weighted,[[a] for a in r],1)
        for (i,j),a in weighted.items():
            expected_d[offset+i,offset+j] = a
        for i,row in enumerate(br):
            if row[0]:
                expected_d[0,offset+i] = -row[0]
        a00 += sum((r[i]*br[i][0] for i in range(m)),F(0))
        need(y[offset:offset+m] == [[alpha[block]*a for a in row]+[F(0)] for row in bz],
             "cone lifted block action")
        local_action_sum += alpha[block]**2*norm_squared(bz)
    if a00:
        expected_d[0,0] = a00
    need(edges == expected_edges and d == expected_d, "cone support/lift mismatch")
    need(all(sum((alpha[j]*constraints[j][i] for j in range(copies)),F(0)) == 0
             for i in range(k)), "cone mixing constraint")
    observed_rank = rank([[constraints[j][i] for j in range(copies)] for i in range(k)])
    need(observed_rank == data["constraint_rank"], "cone constraint rank")
    need(not any(y[0]) and all(row[-1] == 0 for row in y), "cone uncancelled action")
    need(norm_squared(y) == local_action_sum, "cone orthogonal block norm")
    need(max((a*a for (i,j),a in d.items() if i>0),default=F(0))
         >= rational(data["operator_lower_squared"]), "cone principal entry bound")
    return {"apex_action_zero":True,"last_coordinate_actions_zero":True,
            "constraint_rank":observed_rank,"all_lift_entries_exact":True}


def projection_check(data, x, d, y, edges):
    q, p = data["q"],data["parameters"]
    length, copies = p["M"],p["N"]
    need(q == 5 and data["n"] == 7+6*copies*length, "projection fixture size")
    expected_edges = clique_path_edges([0],list(range(1,7)))
    next_vertex = 7
    expected_selected = None
    for apex in range(1,7):
        for _ in range(copies):
            path = list(range(next_vertex,next_vertex+length))
            expected_edges.update(clique_path_edges([apex],path))
            if expected_selected is None:
                expected_selected = [apex]+path
            next_vertex += length
    need(edges == expected_edges, "projection graph mismatch")
    selected = data["selected_vertices"]
    need(selected == expected_selected, "selected child input binding")
    lookup = {v:i for i,v in enumerate(selected)}
    need(all(i in lookup and j in lookup for i,j in d), "projection witness not child-supported")
    local_d = {(lookup[i],lookup[j]):value for (i,j),value in d.items()}
    original = [x[i] for i in selected]
    projected = matrix(data["projected_rows"],q)
    need(len(projected) == len(selected) and projected[0] == original[0],
         "projection apex changed")
    need(all(dot(row,row)<=1 for row in projected), "projected row cap")
    path_rank = rank(projected[1:])
    full_rank = rank(projected)
    need(path_rank <= 2 and full_rank <= 3, "projected rank")
    delta = [[a-b for a,b in zip(row,pr)] for row,pr in zip(original,projected)]
    # Orthogonality certifies these are the actual orthogonal projections
    # onto the span of the projected nonapex rows, without trusting a solver.
    distinct_path_rows = set(tuple(row) for row in projected[1:])
    need(all(dot(row,basis_row)==0 for row in delta[1:] for basis_row in distinct_path_rows),
         "path projection not orthogonal")
    error2 = norm_squared(delta)
    need(error2 == rational(data["projection_error_squared"]) and error2>0,
         "projection error norm")
    py = multiply(local_d,projected,q)
    ey = multiply(local_d,delta,q)
    need(norm_squared(py) == rational(data["projected_action_squared"]), "projected action norm")
    perturb2 = norm_squared(ey)
    need(perturb2 == rational(data["perturbation_action_squared"]) and perturb2>0,
         "actual projection-error action")
    need([y[i] for i in selected] == [[a+b for a,b in zip(r,s)] for r,s in zip(py,ey)],
         "actual input action bridge")
    need(all(not any(row) for i,row in enumerate(y) if i not in lookup), "outside-child action")
    bf2 = sum(((1 if i==j else 2)*a*a for (i,j),a in local_d.items()),F(0))
    need(bf2 == rational(data["local_frobenius_squared"]), "local matrix Frobenius norm")
    need(perturb2 <= bf2*error2, "input perturbation norm allowance")
    cross = sum((dot(a,b) for a,b in zip(py,ey)),F(0))
    need(norm_squared(y) == norm_squared(py)+perturb2+2*cross, "full actual action identity")
    return {"projected_path_rank":path_rank,"projected_full_rank":full_rank,
            "projection_error_squared":str(error2),"perturbation_action_squared":str(perturb2),
            "cross_inner_product":str(cross),"actual_input_bridge_exact":True}


def verify(data):
    need(data.get("schema") == "astra.cone_core_witness.v1", "schema")
    n,q = data["n"],data["q"]
    need(type(n) is int and type(q) is int and n>0 and q>0, "matrix dimensions")
    need(data["input_sha256"] == canonical_input_hash(data), "input SHA256 mismatch")
    edges = set()
    for pair in data["edges"]:
        need(isinstance(pair,list) and len(pair)==2, "edge format")
        i,j = pair
        need(type(i) is int and type(j) is int and 0<=i<j<n and (i,j) not in edges,
             "edge index/duplicate")
        edges.add((i,j))
    x = matrix(data["X"],q)
    need(len(x) == n, "query row count")
    need(all(dot(row,row)<=1 for row in set(tuple(row) for row in x)), "actual row cap")
    d = entries(data["D"],n,edges)
    need(bool(d), "zero witness")
    y = multiply(d,x,q)
    actual2 = norm_squared(y)
    need(actual2 == rational(data["action_squared"]) and actual2>0, "actual action norm")
    op2 = rational(data["operator_lower_squared"])
    need(0<op2<=max(a*a for a in d.values()), "operator entry lower bound")
    need(rational(data["ratio_lower_squared"]) == op2/actual2, "actual inverse ratio")
    handlers = {"core_cancellation":core_check,"cone_lift":cone_check,"low_projection":projection_check}
    need(data["kind"] in handlers, "unknown witness kind")
    details = handlers[data["kind"]](data,x,d,y,edges)
    return {"kind":data["kind"],"n":n,"q":q,"graph_edges":len(edges),
            "nonzero_coefficients":len(d),"action_squared":str(actual2),
            "operator_lower_squared":str(op2),"ratio_lower_squared":str(op2/actual2),
            "input_sha256":data["input_sha256"],"details":details,"status":"passed"}


def tamper_cases(core, low):
    cases = []
    changed = deepcopy(core)
    changed["D"][0][2] = str(F(changed["D"][0][2])+1)
    cases.append(("changed supported coefficient",changed))
    changed = deepcopy(core)
    edges = {tuple(edge) for edge in changed["edges"]}
    ij = next((i,j) for i in range(changed["n"]) for j in range(i+1,changed["n"]) if (i,j) not in edges)
    changed["D"].append([*ij,"1"])
    cases.append(("forbidden support coefficient",changed))
    changed = deepcopy(core)
    changed["X"][0] = ["2"]+["0"]*(changed["q"]-1)
    changed["input_sha256"] = canonical_input_hash(changed)
    cases.append(("row cap violation with updated input hash",changed))
    changed = deepcopy(low)
    changed["projection_error_squared"] = "0"
    cases.append(("understated projection error",changed))
    result = []
    for label, data in cases:
        try:
            verify(data)
        except VerificationError as exc:
            result.append({"case":label,"status":"rejected","reason":str(exc)})
        else:
            raise VerificationError("tamper accepted: "+label)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness-dir",type=Path,default=Path(__file__).resolve().parents[1]/"witnesses")
    parser.add_argument("--output",type=Path,required=True)
    args = parser.parse_args()
    started,cpu = time.perf_counter(),time.process_time()
    files = sorted(args.witness_dir.glob("*.json"))
    need(len(files)==5,"expected five frozen witnesses")
    records, decoded = [],{}
    for path in files:
        case_start = time.perf_counter()
        raw = path.read_bytes()
        data = json.loads(raw)
        verified = verify(data)
        verified.update({"filename":path.name,"file_bytes":len(raw),
                         "file_sha256":hashlib.sha256(raw).hexdigest(),
                         "case_wall_seconds":time.perf_counter()-case_start})
        records.append(verified)
        decoded[path.name] = data
    tamper = tamper_cases(decoded["core_t2_narrow.json"],decoded["low_projection_actual_input.json"])
    receipt = {"schema":"astra.independent_cone_core_check.v1","status":"passed",
               "cases":records,"tamper_checks":tamper,
               "body_wall_seconds":time.perf_counter()-started,
               "body_cpu_seconds":time.process_time()-cpu,
               "max_rss_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
               "checker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "producer_imports":False,
               "scope":"Exact saved inputs, support, full actions, lifts, projections, ranks and inequalities; universal theorem is separate."}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,indent=2))


if __name__ == "__main__":
    main()
