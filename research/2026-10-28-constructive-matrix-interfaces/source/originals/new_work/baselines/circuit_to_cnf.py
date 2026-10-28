#!/usr/bin/env python3
"""Full Tseitin equivalences for the recovered original-input circuit format.

Input wires are 0..inputs-1, gate i produces wire inputs+i. DIMACS identifiers
are wire+1. Every gate is an equivalence, not a one-way implication: each input
assignment has exactly one internal-wire extension. Counting all CNF variables
therefore counts exactly the original accepted input assignments.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time


def clauses_for_gate(op, args, z, value=None):
    if op == "const":
        if args or value not in (0, 1):
            raise ValueError("invalid constant")
        return [[z if value else -z]]
    if op in ("not", "identity", "id"):
        if len(args) != 1:
            raise ValueError("unary gate arity")
        a = args[0]
        return [[z, a], [-z, -a]] if op == "not" else [[-z, a], [z, -a]]
    if len(args) != 2:
        raise ValueError("binary gate arity")
    a, b = args
    if op == "and":
        return [[-z, a], [-z, b], [z, -a, -b]]
    if op == "or":
        return [[z, -a], [z, -b], [-z, a, b]]
    if op == "xor":
        return [[-a, -b, -z], [a, b, -z], [a, -b, z], [-a, b, z]]
    raise ValueError("unsupported gate " + op)


def check_gate_templates():
    operations = {"and": lambda a, b: a & b, "or": lambda a, b: a | b,
                  "xor": lambda a, b: a ^ b}
    for op, function in operations.items():
        clauses = clauses_for_gate(op, [1, 2], 3)
        for a, b, z in itertools.product((0, 1), repeat=3):
            assignment = {1: a, 2: b, 3: z}
            sat = all(any(assignment[abs(lit)] == (lit > 0) for lit in clause)
                      for clause in clauses)
            assert sat == (z == function(a, b)), (op, a, b, z)
    for op in ("not", "identity", "id"):
        clauses = clauses_for_gate(op, [1], 2)
        for a, z in itertools.product((0, 1), repeat=2):
            assignment = {1: a, 2: z}
            sat = all(any(assignment[abs(lit)] == (lit > 0) for lit in clause)
                      for clause in clauses)
            assert sat == (z == (1-a if op == "not" else a))


def convert(source, target):
    start = time.perf_counter()
    raw = Path(source).read_bytes()
    circuit = json.loads(raw)
    n = circuit["inputs"]
    if not isinstance(n, int) or n < 0:
        raise ValueError("bad original input count")
    clauses = []
    for i, gate in enumerate(circuit["gates"]):
        wire = n+i
        args = gate["args"]
        if any(not isinstance(a, int) or a < 0 or a >= wire for a in args):
            raise ValueError("input is not a topologically ordered gate DAG")
        clauses.extend(clauses_for_gate(gate["op"], [a+1 for a in args],
                                        wire+1, gate.get("value")))
    total = n+len(circuit["gates"])
    output = circuit["output"]
    if not isinstance(output, int) or not 0 <= output < total:
        raise ValueError("invalid output wire")
    clauses.append([output+1])
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w") as f:
        f.write("c Full Tseitin equivalences; exactly one gate-wire extension per original input.\n")
        f.write(f"c original_inputs {n}\n")
        f.write(f"p cnf {total} {len(clauses)}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause))+" 0\n")
    elapsed = time.perf_counter()-start
    return {"source": str(Path(source).resolve()), "source_sha256": hashlib.sha256(raw).hexdigest(),
            "cnf": str(target.resolve()), "cnf_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "original_inputs": n, "gates": len(circuit["gates"]), "cnf_variables": total,
            "cnf_clauses": len(clauses), "cnf_bytes": target.stat().st_size,
            "translation_seconds": elapsed,
            "count_contract": "all declared CNF variables; unique internal extension; original accepted inputs"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("target")
    parser.add_argument("--metadata")
    args = parser.parse_args()
    check_gate_templates()
    result = convert(args.source, args.target)
    text = json.dumps(result, indent=2)+"\n"
    if args.metadata:
        Path(args.metadata).write_text(text)
    print(text, end="")
