"""Literal fixed classical channel; no fault simulation or random-bit oracle.

The caller supplies the exact finite coin tickets. Hardware admission of the
atomic graph-range16 read is separate from this host reference function.
"""
from collections.abc import Sequence

WALK_LENGTH = 16
WALKS_PER_ATTEMPT = 3
FAIR_BITS_PER_ATTEMPT = 3 * WALK_LENGTH * WALKS_PER_ATTEMPT


def neighbor(side: int, vertex: int, ticket: int) -> int:
    if side < 2 or not 0 <= vertex < side * side or not 0 <= ticket < 8:
        raise ValueError("invalid graph coordinate or eight-way ticket")
    x, y = divmod(vertex, side)
    if ticket == 0:
        x += 2 * y
    elif ticket == 1:
        x -= 2 * y
    elif ticket == 2:
        x += 2 * y + 1
    elif ticket == 3:
        x -= 2 * y + 1
    elif ticket == 4:
        y += 2 * x
    elif ticket == 5:
        y -= 2 * x
    elif ticket == 6:
        y += 2 * x + 1
    else:
        y -= 2 * x + 1
    return (x % side) * side + y % side


def endpoint(side: int, root: int, tickets: Sequence[int]) -> int:
    if len(tickets) != WALK_LENGTH:
        raise ValueError("one walk needs exactly16 eight-way tickets")
    for ticket in tickets:
        root = neighbor(side, root, ticket)
    return root


def sampled_sites(side: int, target: int, tickets: Sequence[int]) -> tuple[int, int, int]:
    if len(tickets) != 3 * WALK_LENGTH:
        raise ValueError("one attempt needs exactly48 eight-way tickets")
    return tuple(endpoint(side, target, tickets[j * WALK_LENGTH:(j + 1) * WALK_LENGTH])
                 for j in range(3))


def nominal_value(source: Sequence[int], side: int, target: int,
                  tickets: Sequence[int]) -> int:
    if len(source) != side * side:
        raise ValueError("one source bit per graph vertex is required")
    sites = sampled_sites(side, target, tickets)
    values = [source[j] for j in sites]
    if any(x not in (0, 1) for x in values):
        raise ValueError("source contains a nonbinary value")
    return int(sum(values) >= 2)


def nominal_write(source: Sequence[int], destination: list[int], side: int,
                  target: int, tickets: Sequence[int]) -> None:
    """Same array gives restoring update; distinct arrays give buffered copy."""
    if len(destination) != side * side:
        raise ValueError("one destination bit per graph vertex is required")
    destination[target] = nominal_value(source, side, target, tickets)
