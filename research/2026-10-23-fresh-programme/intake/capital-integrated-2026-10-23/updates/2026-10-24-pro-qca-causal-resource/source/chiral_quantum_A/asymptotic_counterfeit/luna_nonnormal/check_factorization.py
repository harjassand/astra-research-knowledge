#!/usr/bin/env python3
"""Exhaustive L=3, two-block check of the active-permutation identities."""

from itertools import product


def majority(bits):
    return int(sum(bits) > len(bits) // 2)


def encode(block):
    L = len(block)
    syndrome = tuple(block[j] ^ block[j + 1] for j in range(L - 1))
    return syndrome + (majority(block),)


def decode(block):
    L = len(block)
    syndrome, q = block[:-1], block[-1]
    base = [0] * L
    for j in range(L - 2, -1, -1):
        base[j] = base[j + 1] ^ syndrome[j]
    if majority(base) != q:
        base = [bit ^ 1 for bit in base]
    return tuple(base)


def block_gate(state, L, starts, gate):
    out = list(state)
    N = len(state)
    for start in starts:
        ids = tuple((start + j) % N for j in range(L))
        image = gate(tuple(state[i] for i in ids))
        for i, bit in zip(ids, image):
            out[i] = bit
    return tuple(out)


def shift_right(state):
    N = len(state)
    out = [0] * N
    for i, bit in enumerate(state):
        out[(i + 1) % N] = bit
    return tuple(out)


def rotate_right_blocks(state, L):
    starts = range(0, len(state), L)
    return block_gate(state, L, starts, lambda x: (x[-1],) + x[:-1])


def coarse_q_shift(state, L, direction):
    N = len(state)
    blocks = N // L
    out = list(state)
    qpos = [k * L + L - 1 for k in range(blocks)]
    for k, src in enumerate(qpos):
        dst = qpos[(k + direction) % blocks]
        out[dst] = state[src]
    return tuple(out)


def main():
    L, N = 3, 6
    starts = range(0, N, L)
    shifted_starts = range(1, N + 1, L)
    P = lambda x: block_gate(x, L, starts, encode)
    Pinv = lambda x: block_gate(x, L, starts, decode)
    Pshift_inv = lambda x: block_gate(x, L, shifted_starts, decode)

    checked = 0
    for state in product((0, 1), repeat=N):
        # Fine shift = blockwise cyclic right rotation after a coarse q shift.
        assert shift_right(state) == rotate_right_blocks(
            coarse_q_shift(state, L, +1), L
        )

        # Omega = S_right P^-1 C_left P.
        omega = shift_right(
            Pinv(coarse_q_shift(P(state), L, -1))
        )

        # Equivalent three-layer form: P_shifted^-1 R_block P.
        factored = Pshift_inv(rotate_right_blocks(P(state), L))
        assert omega == factored
        checked += 1

    print(f"PASS: both identities hold on all {checked} states (L=3, N=6).")


if __name__ == "__main__":
    main()
