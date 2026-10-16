"""Finite crossed-counter discharge check for the one-layer, five-tile fixture.

This exhausts controller states in the stated restricted fixture. The quantum
claim uses the [[5,1,3]] code's one-qubit Knill--Laflamme property separately.
It is not a check of arbitrary noise, recycling, or recursive self-simulation.
"""

from itertools import combinations

SIDE = 10
MODULUS = 8
ACTIVE = ((2, 2), (2, 6), (4, 4), (6, 2), (6, 6))
TARGET = (4, 4)
FLAG_SITES = ((2, 3), (2, 7), (4, 5))
SITE_SET = set()
INTERIOR = tuple((x, y) for x in range(1, SIDE - 1) for y in range(1, SIDE - 1))


def tile(x, y, parity):
    a = x - x % 2 if parity == 0 else x - (1 if x % 2 == 0 else 0)
    b = y - y % 2 if parity == 0 else y - (1 if y % 2 == 0 else 0)
    assert 0 <= a < SIDE - 1 and 0 <= b < SIDE - 1
    return tuple((a + i, b + j) for i in range(2) for j in range(2))


for anchor in ACTIVE:
    SITE_SET.update(tile(*anchor, 0))


def valid(values, support, parity):
    residues = {values[v] % MODULUS for v in support}
    return len(residues) == 1 or any(
        residues == {a, (a + 1) % MODULUS} and a % 2 != parity
        for a in range(MODULUS)
    )


def star_valid(values, site):
    return all(valid(values, tile(*site, p), p) for p in (0, 1))


def candidates(values, site):
    result = []
    for z in range(MODULUS):
        changed = dict(values)
        changed[site] = z
        if star_valid(changed, site):
            result.append(z)
    return tuple(result)


def unique_repairs(values):
    for site in INTERIOR:
        choices = candidates(values, site)
        if len(choices) == 1 and choices[0] != values[site]:
            yield site, choices[0]


def clean_state(fired):
    values = {(x, y): 0 for x in range(SIDE) for y in range(SIDE)}
    for anchor in fired:
        for site in tile(*anchor, 0):
            values[site] = 1
    return values


def gate_ready(values, anchor):
    support = tile(*anchor, 0)
    return all(values[v] == 0 and star_valid(values, v) for v in support)


def emergency_ready(values):
    support = tile(*TARGET, 0)
    return (
        {values[v] for v in support} == {0, 1}
        and sum(values[v] for v in support) == 2
        and not valid(values, support, 0)
        and all(len(candidates(values, v)) != 1 for v in support)
    )


def phase_completions(counter_phase, early_ready, second_done, word):
    """All finite ideal G/H completions after any local phase-bit alteration."""
    if counter_phase == 1 and second_done == 1:
        return {word}
    words = set()
    if counter_phase == 0:
        words.update(phase_completions(1, 1, second_done, word + ("G",)))
    if second_done == 0 and (counter_phase == 1 or early_ready == 1):
        words.update(phase_completions(counter_phase, early_ready, 1, word + ("H",)))
    assert words
    return words


def run():
    clean_checked = 0
    one_fault_checked = 0
    fork_checked = 0
    flag_checked = 0
    phase_checked = 0
    phase_words = set()

    # A terminal authorization bit stored at three non-data sites is read by
    # majority. One arbitrary onsite bit change cannot suppress its live state
    # before transfer or recreate it after transfer.
    assert all(site in SITE_SET for site in FLAG_SITES)
    for original in (0, 1):
        for broken in range(3):
            flags = [original] * 3
            flags[broken] = 1 - original
            assert sum(flags) >= 2 if original == 1 else sum(flags) <= 1
            flag_checked += 1

    # Local clean cut is before G, between G/H, or after H. An onsite fault
    # may change both local one-bit phase markers at once. Every branch still
    # has a terminal service word; H,G is a real reordered branch.
    for counter_phase, prefix in ((0, ()), (1, ("G",)), (1, ("G", "H"))):
        for early_ready in (0, 1):
            for second_done in (0, 1):
                words = phase_completions(
                    counter_phase, early_ready, second_done, prefix
                )
                assert words
                phase_words.update(words)
                phase_checked += 1
    assert ("H", "G") in phase_words
    assert ("G",) in phase_words
    assert ("G", "H", "H") in phase_words

    # All clean interleavings of the five disjoint even-tile gates.
    for mask in range(1 << len(ACTIVE)):
        fired = {anchor for i, anchor in enumerate(ACTIVE) if mask & (1 << i)}
        state = clean_state(fired)
        assert all(star_valid(state, site) for site in SITE_SET)
        assert all(gate_ready(state, anchor) for anchor in ACTIVE if anchor not in fired)
        assert not emergency_ready(state)
        clean_checked += 1

        # A single arbitrary residue change on any mutable interior counter
        # has precisely the source one-site repair and no emergency jump.
        for faulty_site in INTERIOR:
            for z in range(MODULUS):
                if z == state[faulty_site]:
                    continue
                faulty = dict(state)
                faulty[faulty_site] = z
                assert tuple(unique_repairs(faulty)) == ((faulty_site, state[faulty_site]),)
                assert not emergency_ready(faulty)
                one_fault_checked += 1

    # Two indistinguishable branches at the middle tile. In the first, its
    # quantum X gate did not fire; in the second it did. Counters and all other
    # classical controls are identical after the two counter changes.
    target_sites = tile(*TARGET, 0)
    other_tiles = tuple(anchor for anchor in ACTIVE if anchor != TARGET)
    for other_mask in range(1 << len(other_tiles)):
        other_fired = {a for i, a in enumerate(other_tiles) if other_mask & (1 << i)}
        for raised_pair in combinations(target_sites, 2):
            before = clean_state(other_fired)
            after = dict(before)
            for site in raised_pair:
                after[site] = 1
            # Equivalently: start with target gate completed and roll back the
            # other two sites to zero. The observed controller state is 'after'.
            post_gate = clean_state(other_fired | {TARGET})
            for site in set(target_sites) - set(raised_pair):
                post_gate[site] = 0
            assert post_gate == after
            assert emergency_ready(after)
            assert tuple(unique_repairs(after)) == ()
            assert not gate_ready(after, TARGET)
            assert all(gate_ready(after, a) for a in other_tiles if a not in other_fired)

            # Emergency writes the target tile to completed state but applies
            # no quantum gate. Its counter result is a clean reachable cut.
            repaired = dict(after)
            for site in target_sites:
                repaired[site] = 1
            assert repaired == clean_state(other_fired | {TARGET})
            assert tuple(unique_repairs(repaired)) == ()
            assert all(gate_ready(repaired, a) for a in other_tiles if a not in other_fired)
            fork_checked += 1

    print({
        "clean_states": clean_checked,
        "single_interior_counter_faults": one_fault_checked,
        "two_fault_fork_states": fork_checked,
        "single_terminal_flag_flips": flag_checked,
        "local_phase_alterations": phase_checked,
        "distinct_local_gate_words": len(phase_words),
        "controller_checks": "PASS",
        "quantum_claim": "analytic one-qubit QEC proof in FINITE_DISCHARGE.md",
    })


if __name__ == "__main__":
    run()
