#!/usr/bin/env python3
"""Exhaustively check the reachable residual count in the H22 machine family."""

from collections import deque


def check(n: int) -> tuple[int, int, int]:
    states = list(range(1 << n))
    alphabet = ["inc", "dec"] + [f"swap{i}" for i in range(n - 1)]

    def weight(x: int) -> int:
        return x.bit_count()

    def step(x: int, action: str) -> int:
        if action == "inc":
            for i in range(n):
                if not (x >> i) & 1:
                    return x | (1 << i)
            return x
        if action == "dec":
            for i in range(n):
                if (x >> i) & 1:
                    return x & ~(1 << i)
            return x
        i = int(action[4:])
        bi, bj = (x >> i) & 1, (x >> (i + 1)) & 1
        if bi == bj:
            return x
        return x ^ (1 << i) ^ (1 << (i + 1))

    reachable = {0}
    queue = deque([0])
    while queue:
        x = queue.popleft()
        for action in alphabet:
            y = step(x, action)
            if y not in reachable:
                reachable.add(y)
                queue.append(y)

    # Moore-style refinement for a Mealy machine. The output on each action is
    # the current Hamming weight; successor block IDs refine future behavior.
    block = {x: weight(x) for x in states}
    while True:
        old_partition = {
            frozenset(x for x in states if block[x] == b) for b in set(block.values())
        }
        signatures = {
            x: tuple((weight(x), block[step(x, a)]) for a in alphabet)
            for x in states
        }
        sig_to_block = {}
        refined = {}
        for x in states:
            sig = signatures[x]
            if sig not in sig_to_block:
                sig_to_block[sig] = len(sig_to_block)
            refined[x] = sig_to_block[sig]
        new_partition = {
            frozenset(x for x in states if refined[x] == b) for b in set(refined.values())
        }
        block = refined
        if old_partition == new_partition:
            break

    # Count blocks and directly check that the blocks are exactly weights.
    assert len(reachable) == 1 << n
    assert len(set(block.values())) == n + 1
    assert all((block[x] == block[y]) == (weight(x) == weight(y)) for x in states for y in states)
    return len(states), len(reachable), len(set(block.values()))


if __name__ == "__main__":
    for n in range(1, 9):
        total, reachable, residuals = check(n)
        print(f"n={n}: raw={total}, reachable={reachable}, residuals={residuals}")
