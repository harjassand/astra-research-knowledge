"""Exact signed reference-row conversion and a finite opaque-source protocol.

Only the row conversion is executed by the associated consumer.  The optional
source protocol is a literal implementation contract, not a simulated quantum
experiment.  The public C compiler is consumed read-only with a byte binding.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
from pathlib import Path
import types


COMPILER_PATH = Path(__file__).resolve().parents[1] / "c_classical_decoder" / "pauli_compiler.py"
COMPILER_SHA256 = "73ee0ca2d52b62680c545b1a01a9dc18687cb1ba1966bf43cf12aa5135473d43"


def load_compiler():
    source = COMPILER_PATH.read_bytes()
    if hashlib.sha256(source).hexdigest() != COMPILER_SHA256:
        raise ValueError("the independently supplied compiler bytes changed")
    # Compile the pinned public bytes in memory: no __pycache__ write in the
    # frozen supplier directory, and no dependence on a cached bytecode file.
    module = types.ModuleType("shared_exact_pauli_compiler")
    exec(compile(source, str(COMPILER_PATH), "exec"), module.__dict__)
    return module


pc = load_compiler()


class BinarySpan:
    """GF(2) row space with exact certificates in the supplied generator order."""

    def __init__(self, rows=()):
        self.pivots = {}
        self.rows = []
        for row in rows:
            if not self.add(row):
                raise ValueError("dependent supplied reference rows")

    def reduce(self, row, combination=0):
        while row:
            pivot = row.bit_length() - 1
            if pivot not in self.pivots:
                break
            value, certificate = self.pivots[pivot]
            row ^= value
            combination ^= certificate
        return row, combination

    def contains(self, row):
        return self.reduce(row)[0] == 0

    def add(self, row):
        residue, combination = self.reduce(row, 1 << len(self.rows))
        if not residue:
            return False
        self.pivots[residue.bit_length() - 1] = residue, combination
        self.rows.append(row)
        return True

    def solve(self, row):
        residue, certificate = self.reduce(row)
        if residue:
            raise ValueError("target outside the supplied reference span")
        check = 0
        for j, original in enumerate(self.rows):
            if (certificate >> j) & 1:
                check ^= original
        assert check == row
        return certificate


def record_paulis(record):
    """The sign is carried on the physical half of a canonical joint Pauli."""
    r = pc.canonical(record["rx"], record["rz"])
    b = pc.canonical(record["px"], record["pz"], record["negative"])
    return r, b


def canonical_pairs(records, q, n):
    """Convert arbitrary independent reference labels, including Y, exactly.

    Return physical (X_i,Z_i) pairs and literal mod4 conversion receipts.  No
    hidden encoding, source state, expectation, or candidate law is an input.
    """
    if not (1 <= q <= n) or len(records) != 2 * q:
        raise ValueError("need exactly2q rows and1<=q<=n")
    rows = []
    for record in records:
        if any(record[key] < 0 for key in ("rx", "rz", "px", "pz")):
            raise ValueError("negative Pauli mask")
        if (record["rx"] | record["rz"]) >> q:
            raise ValueError("reference mask out of range")
        if (record["px"] | record["pz"]) >> n:
            raise ValueError("physical mask out of range")
        rows.append(record_paulis(record))
    for i, (r, b) in enumerate(rows):
        for rr, bb in rows[i + 1:]:
            if pc.symp(r, rr) != pc.symp(b, bb):
                raise ValueError("supplied signed joint rows do not commute")
    span = BinarySpan(r[0] | (r[1] << q) for r, _ in rows)
    flat, receipts = [], []
    for i in range(q):
        for kind, target in (("X", 1 << i), ("Z", 1 << (q + i))):
            combination = span.solve(target)
            reference, physical = (0, 0, 0), (0, 0, 0)
            selected = []
            for j, (r, b) in enumerate(rows):
                if (combination >> j) & 1:
                    selected.append(j)
                    reference = pc.mul(reference, r)
                    physical = pc.mul(physical, b)
            assert reference[:2] == ((1 << i, 0) if kind == "X" else (0, 1 << i))
            # Joint product = (i^ell R_target) tensor B_raw.  Move i^ell to
            # the physical factor: ADD ell.  Ignoring it or subtracting it is
            # incorrect when reference products pass through +/-i phases.
            converted = physical[0], physical[1], (physical[2] + reference[2]) % 4
            pc.sign(converted)  # Exact Hermiticity admission, including sign.
            flat.append(converted)
            receipts.append({"logical": i, "kind": kind,
                             "selected_rows": selected,
                             "raw_reference": list(reference),
                             "raw_physical": list(physical),
                             "converted_physical": list(converted)})
    pairs = list(zip(flat[::2], flat[1::2]))
    for i, a in enumerate(flat):
        for j, b in enumerate(flat):
            if pc.symp(a, b) != int(i // 2 == j // 2 and i != j):
                raise ValueError("converted physical frame is not canonical")
    return pairs, receipts


def compile_records(records, q, n, outputs=None):
    pairs, receipts = canonical_pairs(records, q, n)
    gates = pc.compile_pairs(pairs, n, outputs)
    return {"pairs": pairs, "conversion": receipts, "gates": gates,
            "compiler_sha256": COMPILER_SHA256}


def ceil_fraction(value):
    value = Fraction(value)
    return -(-value.numerator // value.denominator)


def ceil_log2(value):
    """Exact nonnegative integer upper bound for ln(value), for value>=1."""
    value = Fraction(value)
    if value < 1:
        raise ValueError("log upper bound requires value>=1")
    k = max(0, value.numerator.bit_length() - value.denominator.bit_length())
    if (value.denominator << k) < value.numerator:
        k += 1
    assert (value.denominator << k) >= value.numerator
    return k


def acquisition_budget(q, t, tau, delta):
    """Finite conservative budget; logarithms replaced by exact upper bounds."""
    tau, delta = Fraction(tau), Fraction(delta)
    if not (q >= 1 and t >= 0 and 0 < tau <= Fraction(1, 8) and 0 < delta < Fraction(1, 2)):
        raise ValueError("parameters outside the governing theorem")
    pstar = Fraction(1, 2 * 4 ** (t + 1))
    trials = ceil_fraction(2 / pstar * ceil_log2(Fraction(8 * q) / delta))
    candidates = 2 * q * trials
    shots = ceil_fraction(Fraction(256) / tau * ceil_log2(Fraction(16 * candidates) / delta))
    return {"trials_per_stage": trials, "max_candidates": candidates,
            "shots_per_test": shots, "max_source_calls": candidates * (4 + shots)}


def acquire_from_opaque_source(source, q, n, t, tau, delta):
    """Literal native interface, NOT executed in ROW_EXECUTION.json.

    source.bell_difference() returns (x,z) on q reference then n output bits,
    using FOUR fresh Bell-input forward calls.  source.measure_pauli(x,z,V)
    returns the minus count from V fresh actual Choi states, measuring the
    canonical Hermitian Pauli.  The caller supplies the theorem's distribution
    error/readout-bias warrants.  There is no state/moment/hidden-encoding API.
    """
    budget = acquisition_budget(q, t, tau, delta)
    tau = Fraction(tau)
    ref_mask = (1 << q) - 1
    span, records = BinarySpan(), []
    calls, candidates, tests = 0, 0, 0
    for _stage in range(2 * q):
        for _trial in range(budget["trials_per_stage"]):
            x, z = source.bell_difference()
            calls += 4
            candidates += 1
            if x < 0 or z < 0 or (x | z) >> (n + q):
                raise ValueError("source returned an invalid public outcome")
            rx, rz, px, pz = x & ref_mask, z & ref_mask, x >> q, z >> q
            label = rx | (rz << q)
            if span.contains(label):
                continue
            shots = budget["shots_per_test"]
            minus = source.measure_pauli(x, z, shots)
            calls += shots
            tests += 1
            if not isinstance(minus, int) or not 0 <= minus <= shots:
                raise ValueError("invalid public measurement count")
            if Fraction(min(minus, shots - minus), shots) > tau / 2:
                continue
            record = {"rx": rx, "rz": rz, "px": px, "pz": pz,
                      "negative": 2 * minus > shots}
            rr, bb = record_paulis(record)
            if any(pc.symp(rr, r) != pc.symp(bb, b)
                   for r, b in map(record_paulis, records)):
                continue
            assert span.add(label)
            records.append(record)
            break
        else:
            return {"status": "ABORT", "records": records,
                    "source_calls": calls, "candidates": candidates, "tests": tests,
                    "budget": budget}
    compiled = compile_records(records, q, n)
    assert calls <= budget["max_source_calls"]
    return {"status": "RETURNED", "records": records, **compiled,
            "source_calls": calls, "candidates": candidates, "tests": tests,
            "budget": budget}
