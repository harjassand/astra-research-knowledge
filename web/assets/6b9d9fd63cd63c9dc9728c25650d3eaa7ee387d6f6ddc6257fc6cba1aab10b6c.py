"""Exact finite-window counterexample for entropy-rate claims.

A de Bruijn cycle of order N has every binary N-word once. The q=2**N
intervals on T^3 are advanced by the time-one map of X=(1/q) d/dtheta.
A measurable binary label copied from the cycle has maximal block entropy
for every n<=N, while the smooth flow itself has finite order q, zero KS
entropy, and zero strain. This is a diagnostic construction, not a proof of
the entropy-energy theorem.
"""
from collections import Counter
from math import log


def de_bruijn_binary(order: int) -> list[int]:
    if order < 1:
        raise ValueError("order must be positive")
    # Hierholzer on the directed (order-1)-bit de Bruijn graph.
    start = "0" * (order - 1)
    outgoing = {format(i, f"0{order-1}b") if order > 1 else "": [1, 0]
                for i in range(2 ** (order - 1))}
    stack = [(start, None)]
    reversed_edges: list[int] = []
    while stack:
        vertex, _ = stack[-1]
        if outgoing[vertex]:
            bit = outgoing[vertex].pop()
            next_vertex = (vertex[1:] + str(bit)) if order > 1 else ""
            stack.append((next_vertex, bit))
        else:
            _, incoming = stack.pop()
            if incoming is not None:
                reversed_edges.append(incoming)
    return list(reversed(reversed_edges))


def cyclic_word_counts(sequence: list[int], width: int) -> Counter[tuple[int, ...]]:
    q = len(sequence)
    return Counter(tuple(sequence[(i + j) % q] for j in range(width))
                   for i in range(q))


def main() -> None:
    order = 6
    sequence = de_bruijn_binary(order)
    q = 2**order
    assert len(sequence) == q
    checks = {}
    for width in range(1, order + 1):
        counts = cyclic_word_counts(sequence, width)
        expected = 2 ** (order - width)
        checks[f"width_{width}_uniform"] = (
            len(counts) == 2**width and set(counts.values()) == {expected}
        )
        empirical_block_entropy = -sum(
            (count / q) * log(count / q) for count in counts.values()
        )
        checks[f"width_{width}_entropy_maximal"] = abs(
            empirical_block_entropy - width * log(2)
        ) < 1e-12
    assert all(checks.values()), checks
    print({
        "order": order,
        "period_q": q,
        "all_block_widths_1_to_N_uniform": all(
            checks[f"width_{n}_uniform"] for n in range(1, order + 1)
        ),
        "finite_block_entropies_nats": {
            str(n): n * log(2) for n in range(1, order + 1)
        },
        "time_one_map_order": q,
        "actual_ks_entropy_nats_per_step": 0,
        "flat_torus_vector_field": "X=(1/q) d/dtheta",
        "strain_norm_squared": 0,
        "status": "PASS",
        "scope": "Exact finite-window obstruction; does not test Ruelle or the general theorem.",
    })


if __name__ == "__main__":
    main()
