"""Executable demonstration of learning a finite-state program from exact snapshots.

The learner sees only reset() and step(snapshot, symbol). The target transition
 table lives in `oracle_step`; it is not passed to `learn`.
"""
from collections import deque
from itertools import product

ALPHABET = ("0", "1")
# (next_state, output) for each hidden state and input symbol.
_HIDDEN = {
    0: {"0": (1, "a"), "1": (2, "b")},
    1: {"0": (1, "b"), "1": (3, "a")},
    2: {"0": (3, "b"), "1": (2, "a")},
    3: {"0": (0, "a"), "1": (3, "b")},
}


def snapshot(state: int) -> bytes:
    # Canonical state identity, encoded as one byte in this finite example.
    return bytes([state])


def reset() -> bytes:
    return snapshot(0)


def oracle_step(state_snapshot: bytes, symbol: str) -> tuple[bytes, str]:
    state = state_snapshot[0]
    next_state, output = _HIDDEN[state][symbol]
    return snapshot(next_state), output


def learn(step, initial: bytes, alphabet: tuple[str, ...]):
    """Explore each reachable state/symbol pair once; return a Mealy table."""
    states = [initial]
    known = {initial}
    todo = deque([initial])
    transitions = {}
    calls = 0
    reply_bits = 0
    while todo:
        state = todo.popleft()
        for symbol in alphabet:
            dest, output = step(state, symbol)
            calls += 1
            # The demo transports IDs as one byte and outputs one binary symbol.
            # The information content is 2+1 bits, but the actual payload is 8+1.
            reply_bits += 9
            transitions[(state, symbol)] = (dest, output)
            if dest not in known:
                known.add(dest)
                states.append(dest)
                todo.append(dest)
    return states, transitions, calls, reply_bits


def run_learned(initial, transitions, word):
    state = initial
    output = []
    for symbol in word:
        state, bit = transitions[(state, symbol)]
        output.append(bit)
    return tuple(output)


def run_target(initial, word):
    state = initial
    output = []
    for symbol in word:
        state, bit = oracle_step(state, symbol)
        output.append(bit)
    return tuple(output)


def main():
    initial = reset()
    states, transitions, calls, reply_bits = learn(oracle_step, initial, ALPHABET)
    checked = 0
    for length in range(9):
        for symbols in product(ALPHABET, repeat=length):
            word = "".join(symbols)
            assert run_learned(initial, transitions, word) == run_target(initial, word)
            checked += 1
    print(f"reachable states learned: {len(states)}")
    print(f"transition queries: {calls} (bound N*|Sigma| = {len(states)*len(ALPHABET)})")
    print(f"actual snapshot/output payload bits in this example: {reply_bits}")
    print(f"ideal snapshot/output information bits: {calls * 3}")
    print(f"exhaustive validation words (validation cost, separate): {checked}")


if __name__ == "__main__":
    main()
