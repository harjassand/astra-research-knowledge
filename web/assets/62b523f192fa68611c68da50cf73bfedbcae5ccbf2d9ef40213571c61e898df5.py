"""Exact finite CSS teleportation covariance checks.

This checks a [[4,2,2]] CSS block algebra, not a threshold or QTC implementation.
Uses only Python standard library; scalars are unnormalised integers, preserving
exact signs and zeroes. X stabilizer space A=<1111>, Z space B=<1111>.
"""
from itertools import product

N = 4
SIZE = 1 << N
A = (0, 15)
REPS = (0, 3, 5, 9)


def parity(x):
    return x.bit_count() & 1


def sign(x):
    return 1 - 2 * parity(x)


def encoded_basis(u):
    v = [0] * SIZE
    for a in A:
        v[u ^ a] = 1
    return v


def pauli(v, x, z):
    out = [0] * SIZE
    for y, amp in enumerate(v):
        out[y ^ x] = amp * sign(z & y)
    return out


def branch_output(u, ax, az, bx, bz, outcome, readout_flip):
    va = pauli(encoded_basis(u), ax, az)
    vb = pauli(encoded_basis(0), bx, bz)
    out = [0] * SIZE
    # CNOT A->B, X measurement A, Z feedforward to B using recorded outcome.
    for y, amp_a in enumerate(va):
        if not amp_a:
            continue
        for z, amp_b in enumerate(vb):
            if not amp_b:
                continue
            target = y ^ z
            out[target] += amp_a * amp_b * sign(outcome & y) * sign((outcome ^ readout_flip) & target)
    return out


def check():
    transitions = 0
    # Every one-site source/target Pauli, and all readout flip patterns. For
    # each branch check one common scalar across all logical basis vectors.
    # An initial all-16^5-error-pattern run was interrupted as oversized;
    # this bounded test is the reported scope. The general theorem is algebraic.
    local_paulis = [(0, 0)] + [(1 << i, 0) for i in range(N)] + [(0, 1 << i) for i in range(N)] + [(1 << i, 1 << i) for i in range(N)]
    for (ax, az), (bx, bz), delta in product(local_paulis, local_paulis, range(SIZE)):
        for outcome in range(SIZE):
            scalar = None
            for u in REPS:
                actual = branch_output(u, ax, az, bx, bz, outcome, delta)
                expected = pauli(encoded_basis(u), ax ^ bx, az ^ delta)
                branch_scalar = next((v // e for v, e in zip(actual, expected) if e), 0)
                assert all(v == branch_scalar * e for v, e in zip(actual, expected))
                if scalar is None:
                    scalar = branch_scalar
                assert scalar == branch_scalar
            transitions += 1
    print(f"PASS: {transitions} branch/operator covariances, common scalar across all 4 logical basis states")


if __name__ == "__main__":
    check()
