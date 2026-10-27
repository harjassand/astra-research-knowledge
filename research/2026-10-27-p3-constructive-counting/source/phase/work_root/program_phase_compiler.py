#!/usr/bin/env python3
"""Exact reference compiler for the Astra P3 polynomial-phase construction.

This executes the representation, truncation, and reconstruction identities.
Its finite counter uses subset-union dynamic programming, not the source's
asymptotic replacement-form counter.  No practical speed claim is made.

Only Python's standard library is required.  Run --validate for reproducible
checks or --compile INPUT.json --degree K --output OUTPUT.json to compile a
raw Boolean XOR/AND/NOT program into its checked canonical polynomials.
Wire indices are zero-based; input wires come first.  Constants have no args.
"""
import argparse
import json
import random
from collections import defaultdict
from pathlib import Path


def normalize_gate(op, args, polynomials):
    if op == "const0":
        return set()
    if op == "const1":
        return {0}
    if op == "not":
        assert len(args) == 1
        return polynomials[args[0]] ^ {0}
    if op == "xor":
        out = set()
        for arg in args:
            out.symmetric_difference_update(polynomials[arg])
        return out
    if op == "and":
        assert len(args) == 2
        out = set()
        for left in polynomials[args[0]]:
            for right in polynomials[args[1]]:
                term = left | right  # Boolean x_v^2=x_v
                if term in out:
                    out.remove(term)
                else:
                    out.add(term)
        return out
    raise ValueError("unknown gate: " + op)


def compile_program(spec, degree):
    """Manufacture and check normal forms; never assume supplied support."""
    n = int(spec["inputs"])
    polynomials = [{1 << i} for i in range(n)]
    peak_terms, peak_degree = 1, 1
    for gi, gate in enumerate(spec["gates"]):
        args = [int(a) for a in gate.get("args", [])]
        if any(a < 0 or a >= len(polynomials) for a in args):
            raise ValueError("noncausal/invalid source index at gate " + str(gi))
        poly = normalize_gate(gate["op"], args, polynomials)
        actual_degree = max((s.bit_count() for s in poly), default=0)
        if actual_degree > degree:
            raise ValueError("checked degree cap exceeded at gate " + str(gi))
        polynomials.append(poly)
        peak_terms = max(peak_terms, len(poly))
        peak_degree = max(peak_degree, actual_degree)
    outputs = [int(o) for o in spec["outputs"]]
    if any(o < 0 or o >= len(polynomials) for o in outputs):
        raise ValueError("invalid output index")
    return {
        "inputs": n,
        "gates": len(spec["gates"]),
        "checked_degree_cap": degree,
        "maximum_checked_degree": peak_degree,
        "peak_normal_form_terms": peak_terms,
        "output_monomials": [sorted(polynomials[o]) for o in outputs],
        "total_output_monomials": sum(len(polynomials[o]) for o in outputs),
        "monomial_encoding": "integer bit mask of zero-based input indices",
    }


def eval_program(spec, x):
    values = [(x >> i) & 1 for i in range(spec["inputs"])]
    for gate in spec["gates"]:
        op = gate["op"]
        args = [values[a] for a in gate.get("args", [])]
        if op == "const0":
            value = 0
        elif op == "const1":
            value = 1
        elif op == "not":
            value = 1 ^ args[0]
        elif op == "and":
            value = args[0] & args[1]
        elif op == "xor":
            value = sum(args) & 1
        else:
            raise ValueError(op)
        values.append(value)
    return tuple(values[o] for o in spec["outputs"])


def eval_poly(terms, x):
    return sum((x & mask) == mask for mask in terms) & 1


def preimage_phase(compiled, target):
    """Fourier-character bits replace only output tests, never gate states.

    Sum_x,lambda (-1)^[sum_i lambda_i(P_i(x)+target_i)]
    equals 2^t times the requested preimage count.
    """
    n = compiled["inputs"]
    polys = compiled["output_monomials"]
    assert len(polys) == len(target)
    terms = set()
    for i, (poly, bit) in enumerate(zip(polys, target)):
        local = set(poly)
        if bit:
            local.symmetric_difference_update({0})
        for mask in local:
            terms.symmetric_difference_update({mask | (1 << (n + i))})
    return n + len(polys), [(mask, 1) for mask in sorted(terms)]


def cyclo_power(exponent, d):
    """Coordinates of zeta^exponent in Z[zeta], zeta^d=-1, q=2d."""
    exponent %= 2 * d
    out = [0] * d
    out[exponent % d] = 1 if exponent < d else -1
    return tuple(out)


def cyclo_mul(a, b, modulus=None):
    d = len(a)
    out = [0] * d
    for i, ai in enumerate(a):
        if not ai:
            continue
        for j, bj in enumerate(b):
            ij = i + j
            out[ij % d] += ai * bj * (1 if ij < d else -1)
    if modulus is not None:
        out = [v % modulus for v in out]
    return tuple(out)


def brute_phase(n, terms, b=1):
    d = 1 << (b - 1)
    out = [0] * d
    for x in range(1 << n):
        e = sum(coef for mask, coef in terms if (x & mask) == mask)
        value = cyclo_power(e, d)
        for i, c in enumerate(value):
            out[i] += c
    return tuple(out)


def truncated_phase(n, terms, b=1):
    """Execute the valuation truncation by an exact subset-union DP.

    Returns exact signed cyclotomic coordinates, centered after modulus
    2^(n+2).  Order ell=d*(n+2) suffices since (zeta-1)^d generates (2).
    DP overhead can be exponential in n: this is a validation backend.
    """
    d = 1 << (b - 1)
    modulus = 1 << (n + 2)
    ell = d * (n + 2)
    one = (1,) + (0,) * (d - 1)
    orders = [dict() for _ in range(min(ell, len(terms) + 1))]
    orders[0][0] = one
    peak_states = 1
    for ti, (mask, e) in enumerate(terms):
        delta = list(cyclo_power(e, d))
        delta[0] -= 1
        delta = tuple(v % modulus for v in delta)
        if not any(delta):
            continue
        for j in range(min(ti + 1, len(orders) - 1), 0, -1):
            for union, coefficient in list(orders[j - 1].items()):
                new_union = union | mask
                add = cyclo_mul(coefficient, delta, modulus)
                prev = orders[j].get(new_union, (0,) * d)
                value = tuple((a + v) % modulus for a, v in zip(prev, add))
                if any(value):
                    orders[j][new_union] = value
                else:
                    orders[j].pop(new_union, None)
        peak_states = max(peak_states, sum(len(o) for o in orders))
    residue = [0] * d
    for order in orders:
        for union, coefficient in order.items():
            mult = 1 << (n - union.bit_count())
            for i, c in enumerate(coefficient):
                residue[i] = (residue[i] + c * mult) % modulus
    signed = tuple(v if v < modulus // 2 else v - modulus for v in residue)
    assert all(abs(c) <= 1 << n for c in signed)
    return signed, {"variables": n, "phase_order": 2 * d, "factors": len(terms),
                    "truncation_order": ell, "modulus_bits": n + 2,
                    "discarded_orders_present": len(terms) >= ell,
                    "peak_dp_entries": peak_states}


def prefix_phase(n, terms, prefix, b):
    """Manufacture the two-copy polynomial for an IQP output prefix.

    First a bits are separately copied; last n-a bits are shared.
    Probability(prefix)=phase_sum/(2^(n+a)).
    """
    a = len(prefix)
    assert a <= n
    new_terms = defaultdict(int)
    for mask, coefficient in terms:
        left, right = 0, 0
        for i in range(n):
            if mask & (1 << i):
                if i < a:
                    left |= 1 << i
                    right |= 1 << (a + i)
                else:
                    left |= 1 << (a + i)
                    right |= 1 << (a + i)
        new_terms[left] += coefficient
        new_terms[right] -= coefficient
    for i, bit in enumerate(prefix):
        if bit:
            new_terms[1 << i] += 1 << (b - 1)
            new_terms[1 << (a + i)] += 1 << (b - 1)
    q = 1 << b
    return n + a, [(mask, c % q) for mask, c in sorted(new_terms.items()) if c % q]


def conjugate(value):
    d = len(value)
    out = [0] * d
    for i, c in enumerate(value):
        v = cyclo_power(-i, d)
        for j in range(d):
            out[j] += c * v[j]
    return tuple(out)


def random_program(n, m, padding, rng):
    """A raw program with nonlinear monomials and long XOR state histories."""
    gates, products = [], []
    def emit(op, args):
        gates.append({"op": op, "args": args})
        return n + len(gates) - 1
    for _ in range(m):
        variables = rng.sample(range(n), rng.randint(1, min(n, 3)))
        current = variables[0]
        for v in variables[1:]:
            current = emit("and", [current, v])
        products.append(current)
    current = emit("xor", products)
    # Two genuine raw states per round; exact cancellation is discovered.
    for _ in range(padding):
        v = rng.randrange(n)
        current = emit("xor", [current, v])
        current = emit("xor", [current, v])
    second = emit("xor", [current, 0])
    return {"inputs": n, "gates": gates, "outputs": [current, second]}


def validate():
    rng = random.Random(27032026)
    program_cases, checked_assignments, preimage_checks = [], 0, 0
    for n in range(2, 9):
        for rep in range(3):
            spec = random_program(n, 2*n + rep, 10*(rep+1), rng)
            comp = compile_program(spec, 3)
            histogram = defaultdict(int)
            for x in range(1 << n):
                direct = eval_program(spec, x)
                compiled = tuple(eval_poly(p, x) for p in comp["output_monomials"])
                assert direct == compiled
                histogram[direct] += 1
                checked_assignments += 1
            for target in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                nn, terms = preimage_phase(comp, target)
                phase, _ = truncated_phase(nn, terms)
                assert phase[0] % 4 == 0
                assert phase[0] // 4 == histogram[target]
                preimage_checks += 1
            program_cases.append({k: comp[k] for k in
                                  ["inputs", "gates", "peak_normal_form_terms",
                                   "total_output_monomials"]})
    phase_cases = []
    for b in [1, 2, 3]:
        for n in [4, 6, 8]:
            masks = [s for s in range(1 << n) if s.bit_count() <= 3]
            rng.shuffle(masks)
            terms = [(s, rng.randrange(1, 1 << b)) for s in masks]
            value, details = truncated_phase(n, terms, b)
            assert value == brute_phase(n, terms, b)
            details["exact_value"] = value
            phase_cases.append(details)
    # Exact strong-simulation identity, with no floating point amplitudes.
    prefix_checks = 0
    for b in [1, 2, 3]:
        n = 4
        terms = [(mask, rng.randrange(1, 1 << b)) for mask in range(1, 1 << n)
                 if mask.bit_count() <= 3]
        amplitudes = []
        for y in range(1 << n):
            with_linear = terms + [(1 << i, 1 << (b-1)) for i in range(n) if y >> i & 1]
            amp = brute_phase(n, with_linear, b)
            amplitudes.append(cyclo_mul(amp, conjugate(amp)))
        for a in range(n + 1):
            for z in range(1 << a):
                prefix = [(z >> i) & 1 for i in range(a)]
                nn, pterms = prefix_phase(n, terms, prefix, b)
                zvalue, _ = truncated_phase(nn, pterms, b)
                direct = [0] * (1 << (b - 1))
                for y, value in enumerate(amplitudes):
                    if y & ((1 << a) - 1) == z:
                        direct = [u + v for u, v in zip(direct, value)]
                assert tuple(direct) == tuple(c << (n - a) for c in zvalue)
                prefix_checks += 1
    # Degree failure is detected by computation, not silently truncated away.
    bad = {"inputs": 4, "gates": [{"op":"and","args":[0,1]},
            {"op":"and","args":[2,3]}, {"op":"and","args":[4,5]}],
            "outputs":[6]}
    try:
        compile_program(bad, 3)
        raise AssertionError("degree violation accepted")
    except ValueError:
        pass
    return {"status": "all assertions passed", "seed": 27032026,
            "backend": "exact subset-union DP and exhaustive independent evaluation; not the asymptotic counter",
            "program_cases": program_cases,
            "program_case_count": len(program_cases),
            "original_input_assignment_checks": checked_assignments,
            "exact_target_preimage_checks": preimage_checks,
            "cyclotomic_phase_cases": phase_cases,
            "exact_iqp_prefix_checks": prefix_checks,
            "degree_cap_rejection_checked": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--compile", type=Path)
    parser.add_argument("--degree", type=int, default=3)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.validate:
        result = validate()
    elif args.compile:
        result = compile_program(json.loads(args.compile.read_text()), args.degree)
    else:
        parser.error("choose --validate or --compile")
    output = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(output)
        print(json.dumps({"output": str(args.output), "status": result.get("status", "compiled")}))
    else:
        print(output)


if __name__ == "__main__":
    main()
