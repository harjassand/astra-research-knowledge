"""Definition-first finite oracle. No imports from the proposed sampler.

Vectors and rows are integers with least-significant coordinate first.
The rank of two binary images is computed by their explicit four-point span.
This deliberately enumerates 4**m pairs; it is not an FPT implementation.
"""
from itertools import combinations
from random import Random


def validate(m, blocks):
    if type(m) is not int or m < 0:
        raise ValueError("m must be a nonnegative integer")
    if any(type(r) is not int or not 0 <= r < 2**m
           for rows in blocks for r in rows):
        raise ValueError("rows must be m-bit nonnegative integers")


def image(rows, x):
    # Tuple-valued output avoids depending on the source's packed-image code.
    return tuple(bin(x & r).count('1') % 2 for r in rows)


def xor(a, b):
    return tuple((x + y) % 2 for x, y in zip(a, b))


def valid(blocks, u, v):
    for rows in blocks:
        a, b = image(rows, u), image(rows, v)
        zero = (0,) * len(rows)
        if len({zero, a, b, xor(a, b)}) not in (1, 4):
            return False
    return True


def enumerate_pairs(m, blocks):
    validate(m, blocks)
    return [(u, v) for u in range(2**m) for v in range(2**m)
            if valid(blocks, u, v)]


def prefix_counts(m, pairs):
    counts = {}
    for k in range(2*m + 1):
        for code in range(2**k):
            bits = tuple((code >> i) & 1 for i in range(k))
            counts[bits] = sum(((u + (v << m)) % 2**k) == code
                               for u, v in pairs)
    return counts


def joint_kernel(m, blocks):
    return [x for x in range(2**m)
            if all(not any(image(rows, x)) for rows in blocks)]


def kernel_representatives(m):
    """Every row space has a basis of <=m rows. Deduplicate by full kernel.

    Intended only for m<=3. It does not use source subspace-generation code.
    Choosing unordered bases suffices; dependent rows and zero rows give no
    extra kernels. Output bases need not be row-reduced.
    """
    found = {}
    for n in range(m + 1):
        for rows in combinations(range(1, 2**m), n):
            key = tuple(joint_kernel(m, [rows]))
            found.setdefault(key, list(rows))
    return [found[key] for key in sorted(found)]


def rejection(m, blocks, count, seed, max_proposals=1_000_000):
    """Plain iid rejection, with an explicit stop and retained partial count."""
    rng = Random(seed)
    draws, proposals = [], 0
    while len(draws) < count and proposals < max_proposals:
        pair = (rng.randrange(2**m), rng.randrange(2**m))
        proposals += 1
        if valid(blocks, *pair):
            draws.append(pair)
    return {"draws": draws, "proposals": proposals,
            "status": "passed" if len(draws) == count else "proposal_limit"}
