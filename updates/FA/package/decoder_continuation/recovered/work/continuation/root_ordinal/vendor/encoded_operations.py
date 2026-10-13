"""Acquire full executable arithmetic/order bodies from black-box behavior.

The modular-addition learner has a known broader affine-ARX prior-art comparator.
The scalar-comparison learner is a candidate pending closest-method screening.
No learner receives hidden matrices, target intermediate states, or source code.
"""
import argparse
import functools
import json
import random
import time
from pathlib import Path


def parity(x):
    return x.bit_count() & 1


def lin(cols, x):
    out = 0
    while x:
        bit = x & -x
        out ^= cols[bit.bit_length()-1]
        x ^= bit
    return out


def transpose(cols, n):
    return [sum(((cols[j] >> i) & 1) << j for j in range(n)) for i in range(n)]


def inverse(cols):
    n = len(cols)
    rows = [v | (1 << (n+i)) for i, v in enumerate(transpose(cols, n))]
    for j in range(n):
        pivot = next((i for i in range(j, n) if (rows[i] >> j) & 1), None)
        if pivot is None:
            raise ValueError("singular matrix")
        rows[j], rows[pivot] = rows[pivot], rows[j]
        for i in range(n):
            if i != j and (rows[i] >> j) & 1:
                rows[i] ^= rows[j]
    inv_rows = [v >> n for v in rows]
    return transpose(inv_rows, n)


def random_invertible(rng, n):
    while True:
        cols = [rng.getrandbits(n) for _ in range(n)]
        try:
            return cols, inverse(cols)
        except ValueError:
            pass


def kernel_basis(rows, n):
    a = list(rows)
    rank, pivots = 0, []
    for col in range(n):
        p = next((i for i in range(rank, len(a)) if (a[i] >> col) & 1), None)
        if p is None:
            continue
        a[p], a[rank] = a[rank], a[p]
        for i in range(len(a)):
            if i != rank and ((a[i] >> col) & 1):
                a[i] ^= a[rank]
        pivots.append(col)
        rank += 1
    out = []
    for col in range(n):
        if col not in pivots:
            v = 1 << col
            for row, p in zip(a, pivots):
                v |= ((row >> col) & 1) << p
            out.append(v)
    return out


def polynomial_matrix(a, n):
    mask = (1 << n)-1
    return [(a << j) & mask for j in range(n)]


def polynomial_inverse(a, n):
    b = 1
    for j in range(1, n):
        bit = 0
        for i in range(1, j+1):
            bit ^= ((a >> i) & 1) & ((b >> (j-i)) & 1)
        b |= bit << j
    return b


class AddTeacher:
    def __init__(self, encoder, decoder):
        self._encoder, self._decoder = encoder, decoder
        self.n, self.queries = len(encoder), 0
        self.transcript = []

    def query(self, x, y):
        self.queries += 1
        mask = (1 << self.n)-1
        z = lin(self._encoder, (lin(self._decoder, x)+lin(self._decoder, y)) & mask)
        self.transcript.append((x, y, z))
        return z


def acquire_add(n, query):
    if n < 2:
        raise ValueError("the theorem and pilot use n>=2")
    doubling = [query(1 << j, 1 << j) for j in range(n)]
    chain = None
    for j in range(n):
        current, proposed = 1 << j, []
        for _ in range(n):
            proposed.append(current)
            current = lin(doubling, current)
        if proposed[-1]:
            chain = proposed
            break
    if chain is None or current:
        raise ValueError("UNKNOWN: doubling has no length-n nilpotent Jordan chain")
    cinv = inverse(chain)
    a = 1
    for j in range(1, n-1):
        response = lin(cinv, query(chain[0], chain[j]))
        a |= ((response >> (j+1)) & 1) << j
    rcols = polynomial_matrix(a, n)
    ricols = polynomial_matrix(polynomial_inverse(a, n), n)
    decoder = [lin(rcols, v) for v in cinv]
    encoder = [lin(chain, v) for v in ricols]
    return encoder, decoder


class CompareTeacher:
    def __init__(self, decoder, affine_offset):
        self._decoder, self._offset = decoder, affine_offset
        self.n, self.queries = len(decoder), 0
        self.transcript = []

    def query(self, x, y):
        if x == y:
            raise ValueError("strict comparator queries require x!=y")
        self.queries += 1
        result = ((lin(self._decoder, x) ^ self._offset) <
                  (lin(self._decoder, y) ^ self._offset))
        self.transcript.append((x, y, result))
        return result


def acquire_comparator(n, query):
    """Translation probes extract actual decoder rows; kernel probes avoid repeats."""
    rows, offsets, probe_cost = [], [], 0
    for _ in range(n):
        basis = kernel_basis(rows, n)
        if not basis:
            raise ValueError("UNKNOWN: premature zero kernel")
        w = basis[0]
        at_zero = int(query(0, w))
        row = 0
        for j in range(n):
            x = 1 << j
            row |= (int(query(x, x ^ w)) ^ at_zero) << j
        if parity(row & w) != 1:
            raise ValueError("UNKNOWN: query translation is not the promised parity")
        rows.append(row)
        offsets.append(1 ^ at_zero)
        probe_cost += n+1
    # Coordinates at this stage have unknown priority, but known actual bit values.
    unordered_decoder = transpose(rows, n)
    unordered_encoder = inverse(unordered_decoder)
    offset_word = sum(bit << j for j, bit in enumerate(offsets))
    origin = lin(unordered_encoder, offset_word)

    def priority(i, j):
        if i == j:
            return 0
        # x has bit i=0,j=1; x^w has bit i=1,j=0. Lower x means i dominates j.
        x = origin ^ unordered_encoder[j]
        w = unordered_encoder[i] ^ unordered_encoder[j]
        return -1 if query(x, x ^ w) else 1

    order_high_to_low = sorted(range(n), key=functools.cmp_to_key(priority))
    ordered_rows = [rows[i] for i in reversed(order_high_to_low)]
    ordered_offsets = [offsets[i] for i in reversed(order_high_to_low)]
    decoder = transpose(ordered_rows, n)
    offset = sum(bit << j for j, bit in enumerate(ordered_offsets))
    return decoder, offset, probe_cost


def run_add(n, seed):
    rng = random.Random(seed)
    enc, dec = random_invertible(rng, n)
    teacher = AddTeacher(enc, dec)
    start = time.perf_counter()
    learned_enc, learned_dec = acquire_add(n, teacher.query)
    seconds = time.perf_counter()-start
    acquisition = teacher.queries
    mask = (1 << n)-1
    pairs = ((x, y) for x in range(1 << n) for y in range(1 << n)) if n <= 6 else (
        (rng.getrandbits(n), rng.getrandbits(n)) for _ in range(1024))
    checked = 0
    for x, y in pairs:
        expected = lin(enc, (lin(dec, x)+lin(dec, y)) & mask)
        actual = lin(learned_enc, (lin(learned_dec, x)+lin(learned_dec, y)) & mask)
        assert actual == expected
        checked += 1
    # Test acquired execution on a new 64-step linear recurrence with unknown states.
    x, y = rng.getrandbits(n), rng.getrandbits(n)
    u, v = lin(dec, x), lin(dec, y)
    for _ in range(64):
        x, y = y, lin(learned_enc, (lin(learned_dec, x)+lin(learned_dec, y)) & mask)
        u, v = v, (u+v) & mask
        assert x == lin(enc, u) and y == lin(enc, v)
    assert teacher.queries == acquisition == 2*n-2
    return {"n": n, "seed": seed, "vector_queries": acquisition,
            "returned_bits": n*acquisition, "acquisition_seconds": seconds,
            "exact_heldout_pairs": checked, "new_recurrence_steps_exact": 64,
            "source_queries_during_execution": 0,
            "source_horner_or_matrix_bitwork_upper": acquisition*(3*n*n+n),
            "scope": "linear same encoding; addition prior art defeats broad novelty"}


def run_compare(n, seed):
    rng = random.Random(seed)
    enc, dec = random_invertible(rng, n)
    offset = rng.getrandbits(n)
    teacher = CompareTeacher(dec, offset)
    start = time.perf_counter()
    learned_dec, learned_offset, probes = acquire_comparator(n, teacher.query)
    seconds = time.perf_counter()-start
    acquisition = teacher.queries
    assert learned_dec == dec and learned_offset == offset
    pairs = ((x, y) for x in range(1 << n) for y in range(1 << n) if x != y) if n <= 6 else (
        (rng.getrandbits(n), rng.getrandbits(n)) for _ in range(1024))
    checked = 0
    for x, y in pairs:
        expected = (lin(dec, x) ^ offset) < (lin(dec, y) ^ offset)
        actual = (lin(learned_dec, x) ^ learned_offset) < (lin(learned_dec, y) ^ learned_offset)
        assert actual == expected
        checked += 1
    # New sorting task, acquired comparator body executes with no source calls.
    values = [rng.getrandbits(n) for _ in range(128)]
    sorted_values = sorted(values, key=lambda x: lin(learned_dec, x) ^ learned_offset)
    assert [lin(dec, x) ^ offset for x in sorted_values] == sorted(lin(dec, x) ^ offset for x in values)
    assert teacher.queries == acquisition
    return {"n": n, "seed": seed, "one_bit_queries": acquisition,
            "row_acquisition_queries": probes, "priority_sort_queries": acquisition-probes,
            "acquisition_seconds": seconds, "exact_decoder_and_offset": True,
            "exact_heldout_pairs": checked, "heldout_sort_items": len(values),
            "source_queries_during_execution": 0,
            "source_matrix_bitwork_upper": acquisition*(2*n*n+n),
            "persisted_decoder_and_offset_bits": n*n+n,
            "transcript": teacher.transcript if n <= 8 else None,
            "scope": "affine same decoder; exact scalar comparator; novelty uncleared"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="encoded_operation_evidence.json")
    args = parser.parse_args()
    addition, comparison = [], []
    for n in (2, 3, 4, 6, 8, 16, 32, 64, 128):
        for seed in (610021, 610022, 610023):
            a, c = run_add(n, seed), run_compare(n, seed)
            addition.append(a)
            comparison.append(c)
            print(json.dumps({"n": n, "seed": seed, "add_queries": a['vector_queries'],
                              "compare_queries": c['one_bit_queries'],
                              "compare_seconds": c['acquisition_seconds']}), flush=True)
    Path(args.output).write_text(json.dumps({
        "addition_status": "exactly_executed_known_broader_affine_ARX_operation",
        "comparison_status": "exactly_executed_candidate_priority_and_baseline_gate_open",
        "addition": addition, "comparison": comparison,
        "warning": "Acquired matrices are not supplied to either learner. Known class and chosen queries are supplied. Seeds reused across sizes; no independent across-size statistical claim."
    }, indent=2)+"\n")


if __name__ == "__main__":
    main()
