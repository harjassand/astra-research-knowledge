#!/usr/bin/env python3
"""Finite adversarial diagnostics, independently written from the displayed maps.

These checks do not establish an infinite-volume theorem or a noise threshold.
Only this worker directory is written. All chains are over F_2.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, product
from math import factorial
from pathlib import Path
import hashlib
import json
import time

OUT = Path(__file__).resolve().parent
D = 4
ORIENTATIONS = tuple(combinations(range(D), 2))
ORIGIN = (0,) * D


def step(x, direction, amount=1, period=None):
    y = list(x)
    y[direction] += amount
    if period:
        y[direction] %= period
    return tuple(y)


def face_edges(face, period=None):
    x, a, b = face
    return {(x, a), (step(x, b, period=period), a),
            (x, b), (step(x, a, period=period), b)}


def boundary(chain, period=None):
    ans = set()
    for f in chain:
        ans ^= face_edges(f, period)
    return ans


def endpoints(edge, period=None):
    x, d = edge
    return x, step(x, d, period=period)


def edge_vertices(edges, period=None):
    return {x for e in edges for x in endpoints(e, period)}


def infection_update(infected, v):
    old = set(infected)
    result = old.copy()
    if v in old and all(step(v, i, -1) not in old for i in range(D)):
        result.discard(v)
    for a, b in ORIENTATIONS:
        if {v, step(v, a), step(v, b)} <= old:
            result.add(step(step(v, a), b))
    return result


def correction_faces(edges, v, period=None):
    incoming = [i for i in range(D) if (step(v, i, -1, period), i) in edges]
    outgoing = [i for i in range(D) if (v, i) in edges]
    assert (len(incoming) + len(outgoing)) % 2 == 0
    if incoming:
        return set()
    return {(v, outgoing[j], outgoing[j + 1])
            for j in range(0, len(outgoing), 2)}


def local_map_diagnostics():
    stencil = [ORIGIN] + [step(ORIGIN, i, -1) for i in range(D)]
    stencil += [step(ORIGIN, i) for i in range(D)]
    stencil += [step(step(ORIGIN, a), b) for a, b in ORIENTATIONS]
    assert len(set(stencil)) == 15
    # Independent set-valued evaluation of all Boolean inputs.
    images = []
    for mask in range(1 << 15):
        old = {stencil[j] for j in range(15) if mask >> j & 1}
        new = infection_update(old, ORIGIN)
        images.append(sum(1 << j for j in range(15) if stencil[j] in new))
    covers = 0
    for mask in range(1 << 15):
        for j in range(15):
            if not (mask >> j & 1):
                assert images[mask] & ~images[mask | (1 << j)] == 0
                covers += 1
    # All even center-star patterns. Other vertices need not be even in
    # this purely local algebra diagnostic; the written proof supplies
    # the extension to actual cycles, using only parity at the center.
    local_patterns = active_two_face = 0
    for bits in range(1 << 8):
        if bits.bit_count() % 2:
            continue
        edges = {(step(ORIGIN, i, -1), i) for i in range(D) if bits >> i & 1}
        edges |= {(ORIGIN, i) for i in range(D) if bits >> (D + i) & 1}
        faces = correction_faces(edges, ORIGIN)
        assert edge_vertices(edges ^ boundary(faces)) <= infection_update(
            edge_vertices(edges), ORIGIN)
        local_patterns += 1
        active_two_face += len(faces) == 2
    # A perimeter of a 2x2 square has no interior opposite corner initially.
    square = {((a, b, 0, 0), 0, 1) for a in range(2) for b in range(2)}
    edges = boundary(square)
    old = edge_vertices(edges)
    physical = edge_vertices(edges ^ boundary(correction_faces(edges, ORIGIN)))
    correct = infection_update(old, ORIGIN)
    wrong = old.copy()
    wrong.discard(ORIGIN)
    for a, b in ORIENTATIONS:
        if {ORIGIN, step(ORIGIN, a), step(ORIGIN, b)} <= wrong:
            wrong.add(step(step(ORIGIN, a), b))
    assert physical <= correct and not physical <= wrong
    return {'boolean_inputs': len(images), 'monotonicity_cover_relations': covers,
            'even_local_star_patterns': local_patterns,
            'two_face_local_patterns': active_two_face,
            'new_state_counterexample_confirmed': True}


def multiset_orders(counts):
    if not sum(counts):
        yield ()
        return
    for j, count in enumerate(counts):
        if count:
            nxt = list(counts)
            nxt[j] -= 1
            for rest in multiset_orders(tuple(nxt)):
                yield (j,) + rest


def ordered_clock_diagnostics():
    counts = (3, 2, 2)
    orders = list(multiset_orders(counts))
    length = 4
    totals = Counter()
    for order in orders:
        for indices in combinations(range(len(order)), length):
            totals[tuple(order[i] for i in indices)] += 1
    tested = 0
    for word in product(range(len(counts)), repeat=length):
        multiplicities = Counter(word)
        numerator = 1
        for label, used in multiplicities.items():
            numerator *= (factorial(counts[label]) // factorial(counts[label] - used)
                          if used <= counts[label] else 0)
        assert Fraction(totals[word], len(orders)) == Fraction(numerator, factorial(length))
        tested += 1
    # Literal enlarged guard face count, contrasted with the inherited
    # earlier erroneous expression. This does not challenge the canonical bound.
    radius, block = 1, 4
    side = (2 * radius + 1) * block
    exact = 6 * side ** 2 * (side + 1) ** 2
    old_bound = 6 * (2 * radius * block + 3) ** 4
    assert exact > old_bound
    canonical_side = (2 * radius + 5) * block
    assert 6 * canonical_side ** 2 * (canonical_side + 1) ** 2 <= 6 * (canonical_side + 3) ** 4
    return {'conditional_interleavings': len(orders), 'all_length_four_words': tested,
            'repeated_clock_factorial_identity_exact': True,
            'older_guard_counterexample': {'R': radius, 'b': block,
                                           'exact': exact, 'old_bound': old_bound},
            'canonical_guard_bound_passes': True}


def eroder_diagnostics():
    radius = 1
    offsets = list(product(range(-radius, radius + 1), repeat=D))
    forcing = [[w for w in offsets if w[i] >= 0] for i in range(D)]
    forcing.append([w for w in offsets if sum(w) <= -1])
    seeds = [x + (0,) for x in product(range(2), repeat=3)]
    trajectories = rounds = 0
    for mask in range(1 << len(seeds)):
        zeros = {x for j, x in enumerate(seeds) if mask >> j & 1}
        if not zeros:
            trajectories += 1
            continue
        maxima = [max(x[i] for x in zeros) for i in range(D)]
        minimum = min(map(sum, zeros))
        deadline = sum(maxima) - minimum + 1
        t = 0
        while zeros:
            candidates = {tuple(x[i] - a[i] for i in range(D))
                          for x in zeros for a in forcing[0]}
            nxt = {x for x in candidates
                   if all(any(tuple(x[i] + a[i] for i in range(D)) in zeros
                              for a in group) for group in forcing)}
            if nxt:
                assert all(max(x[i] for x in nxt) <= max(x[i] for x in zeros)
                           for i in range(D))
                assert min(map(sum, nxt)) >= min(map(sum, zeros)) + 1
            zeros = nxt
            t += 1
            rounds += 1
            assert t <= deadline
        trajectories += 1
    return {'dimension': D, 'toy_radius': radius,
            'complete_seed_family': 'all subsets of {0,1}^3 x {0}',
            'seed_trajectories': trajectories, 'round_transitions': rounds,
            'extrema_and_deadline_hold': True,
            'limitation': 'A finite diagnostic of the algebraic extrema proof; not the enormous canonical R.'}


def torus_distance_squared(a, b, period):
    dx = (a[0] - b[0]) % period
    dx = min(dx, period - dx)
    return dx * dx + (a[1] - b[1]) ** 2


def component_of(p, revealed, period):
    found = {p}
    todo = [p]
    while todo:
        q = todo.pop()
        more = {r for r in revealed - found if 4 * torus_distance_squared(q, r, period) <= 9}
        found |= more
        todo.extend(more)
    return found


def toy_layers(marks, period, slabs):
    zeros = [set()]
    for t in range(slabs):
        dead = {x for x in range(period) if (x, t) in marks or ((x + 1) % period, t) in marks}
        nxt = dead | {x for x in range(period) if x in zeros[-1] and (x + 1) % period in zeros[-1]}
        zeros.append(nxt)
    return zeros


def replay_diagnostics():
    period, slabs, patch = 32, 3, 7
    primitive_indices = list(product(range(period), range(slabs)))
    histories = first_escapes = seam_escapes = unrevealed_cases = 0
    for count in range(3):
        for locations in combinations(primitive_indices, count):
            histories += 1
            marks = set(locations)
            zeros = toy_layers(marks, period, slabs)
            revealed = set()
            stopped = None
            for t in range(1, slabs + 1):
                for x in sorted(zeros[t]):
                    p = (x, t)
                    revealed.add(p)
                    comp = component_of(p, revealed, period)
                    if any(4 * torus_distance_squared(a, b, period) >= 25
                           for a in comp for b in comp):
                        stopped = (p, comp)
                        break
                if stopped:
                    break
            if not stopped:
                continue
            first_escapes += 1
            p, comp = stopped
            # First-insertion radius is ell+k=4; all previous components
            # have diameter strictly below ell=5/2.
            assert all(torus_distance_squared(q, p, period) < 16 for q in comp)
            lift = lambda x: ((x - p[0] + period // 2) % period) - period // 2
            lifted = {(lift(x), t) for x, t in comp}
            for x, t in comp:
                forced = (x, t - 1) in marks or ((x + 1) % period, t - 1) in marks
                if not forced:
                    assert (x, t - 1) in comp and ((x + 1) % period, t - 1) in comp
            for a in comp:
                for b in comp:
                    da, db = (lift(a[0]), a[1]), (lift(b[0]), b[1])
                    lifted_dist = (da[0] - db[0]) ** 2 + (da[1] - db[1]) ** 2
                    assert lifted_dist == torus_distance_squared(a, b, period)
            seam_escapes += any(abs(a[0] - b[0]) > period // 2 for a in comp for b in comp)
            unrevealed_cases += any((x, p[1]) not in revealed for x in zeros[p[1]])
            copied = {(lift(x), t) for x, t in marks if abs(lift(x)) <= patch}
            # Full deterministic anchor patch, then both extreme exterior
            # extensions. The witness must survive even the healthy extension.
            for exterior in [0, 1]:
                current = set()
                for t in range(slabs):
                    def raw(x):
                        return (x, t) in copied if abs(x) <= patch else bool(exterior)
                    next_zeros = {x for x in range(-16, 17)
                                  if raw(x) or raw(x + 1) or (x in current and x + 1 in current)}
                    for x, layer in lifted:
                        if layer == t + 1:
                            assert x in next_zeros
                    current = next_zeros
    # The selected-primitive law is biased, illustrating why a deterministic
    # candidate-anchor patch is essential.
    selected_ones = 0
    for a, b in product([0, 1], repeat=2):
        selected_ones += a if a else b
    assert Fraction(selected_ones, 4) == Fraction(3, 4)
    # Whole-path zero inclusion for arbitrary lower initialization and one
    # shared future death field; no stationarity claim is tested here.
    path_comparisons = 0
    for initial in range(16):
        for deaths in range(256):
            lower = {x for x in range(4) if initial >> x & 1}
            cold = set(range(4))
            for t in range(2):
                dead = {x for x in range(4) if deaths >> (4 * t + x) & 1}
                lower = {x for x in range(4) if (x in lower or (x + 1) % 4 in lower) and x not in dead}
                cold = {x for x in range(4) if (x in cold or (x + 1) % 4 in cold) and x not in dead}
                assert lower <= cold
            path_comparisons += 1
    return {'toy_rule': 'phi=x_0 OR x_1; B(x,t)=P(x,t) OR P(x+1,t)',
            'torus_sites': period, 'slabs': slabs, 'primitive_mark_limit': 2,
            'k': '3/2 (Euclidean spacetime)', 'ell': '5/2',
            'histories': histories, 'first_escapes': first_escapes,
            'seam_escapes': seam_escapes, 'unrevealed_same_layer_cases': unrevealed_cases,
            'closed_witness_and_both_exterior_replays_pass': True,
            'shared_future_path_comparisons': path_comparisons,
            'adaptive_selected_one_probability': '3/4 from Bernoulli(1/2) primitives',
            'limitation': 'Toy replay adapter only; no simulation of canonical block scales or threshold.'}


def edge_components(edges, period):
    incident = defaultdict(set)
    for e in edges:
        for v in endpoints(e, period):
            incident[v].add(e)
    unseen = set(edges)
    comps = []
    while unseen:
        found = {min(unseen)}
        todo = list(found)
        while todo:
            e = todo.pop()
            neighbors = set().union(*(incident[x] for x in endpoints(e, period)))
            fresh = neighbors - found
            found |= fresh
            todo.extend(fresh)
        comps.append(found)
        unseen -= found
    return comps


def short_component_fill(component, period):
    verts = edge_vertices(component, period)
    anchor = min(verts)
    def lift(x):
        return tuple(anchor[i] + ((x[i] - anchor[i] + period // 2) % period) - period // 2
                     for i in range(D))
    lifted = set()
    for x, direction in component:
        y = step(x, direction, period=period)
        assert lift(y) == step(lift(x), direction)
        lifted.add((lift(x), direction))
    minimum = tuple(min(lift(x)[i] for x in verts) for i in range(D))
    faces = set()
    cycle = lifted
    for coordinate in range(D):
        projected = set()
        for x, direction in cycle:
            if direction == coordinate:
                continue
            y = list(x)
            y[coordinate] = minimum[coordinate]
            projected.symmetric_difference_update({(tuple(y), direction)})
            for value in range(minimum[coordinate], x[coordinate]):
                base = list(x)
                base[coordinate] = value
                faces.symmetric_difference_update({(tuple(base), *sorted([coordinate, direction]))})
        cycle = projected
    assert not cycle
    wrapped = {(tuple(c % period for c in x), i, j) for x, i, j in faces}
    assert boundary(wrapped, period) == component
    return wrapped


def decoder(edges, period):
    ans = set()
    for comp in edge_components(edges, period):
        ans ^= short_component_fill(comp, period)
    return ans


def homology(closed, period):
    assert not boundary(closed, period)
    return tuple(sum(x[i] == 0 and x[j] == 0 for x, a, b in closed if (a, b) == (i, j)) % 2
                 for i, j in ORIENTATIONS)


def topology_diagnostics():
    period = 128
    states = noise_events = correction_events = two_face_events = nonzero_closed = 0
    family_counts = Counter()
    for base in [(3, 4, 5, 6), (period - 1,) * D]:
        families = []
        common = [(base, a, b) for a, b in ORIENTATIONS]
        families.append(('common_corner', common))
        for triple in combinations(range(D), 3):
            shell = []
            for a, b in combinations(triple, 2):
                other = next(i for i in triple if i not in [a, b])
                shell += [(base, a, b), (step(base, other, period=period), a, b)]
            families.append(('three_cube_shell', shell))
        planar = [(step(step(base, 0, a, period), 1, b, period), 0, 1)
                  for a in range(3) for b in range(3)]
        families.append(('planar_3x3', planar))
        for name, faces in families:
            for mask in range(1 << len(faces)):
                error = {f for j, f in enumerate(faces) if mask >> j & 1}
                old_s = boundary(error, period)
                old_d = decoder(old_s, period)
                old_h = homology(error ^ old_d, period)
                assert old_h == (0,) * 6
                states += 1
                family_counts[name] += 1
                updates = [('noise', {f}) for f in faces]
                for vertex in sorted(edge_vertices(old_s, period)):
                    f = correction_faces(old_s, vertex, period)
                    if f:
                        updates.append(('correction', f))
                for kind, written in updates:
                    new_s = old_s ^ boundary(written, period)
                    new_d = decoder(new_s, period)
                    difference = written ^ old_d ^ new_d
                    assert not boundary(difference, period)
                    assert homology(difference, period) == (0,) * 6
                    assert homology(error ^ written ^ new_d, period) == old_h
                    nonzero_closed += bool(difference)
                    if kind == 'noise':
                        noise_events += 1
                    else:
                        correction_events += 1
                        two_face_events += len(written) == 2
    # A hidden accumulated logical torus cannot be erased from the record
    # when its remaining small syndrome disappears.
    base = (period - 1,) * D
    membrane = {((a, b, base[2], base[3]), 0, 1)
                for a in range(period) for b in range(period)}
    face = {(base, 0, 1)}
    error = membrane ^ face
    before = homology(error ^ decoder(boundary(error, period), period), period)
    after = homology(error ^ face ^ decoder(boundary(error ^ face, period), period), period)
    assert before == after == (1, 0, 0, 0, 0, 0)
    ribbons = []
    for length in range(3, 10):
        ribbon = {((a, 0, 0, 0), 0, 1) for a in range(length)}
        syn = boundary(ribbon, length)
        assert all(not correction_faces(syn, v, length) for v in edge_vertices(syn, length))
        ribbons.append(length)
    return {'period': period, 'r': 'L/32=4', 'rho': 'L/8=16',
            'state_families': dict(family_counts), 'states': states,
            'noise_transition_checks': noise_events,
            'accepted_correction_transition_checks': correction_events,
            'two_face_corrections': two_face_events,
            'nonzero_closed_transition_differences': nonzero_closed,
            'seam_and_ordinary_locations': True,
            'hidden_historical_homology_preserved': True,
            'winding_fixed_ribbon_periods': ribbons,
            'limitation': 'Finite chain arithmetic; universal contractible-box argument is separate.'}


if __name__ == '__main__':
    start = time.monotonic()
    results = {'local_envelope': local_map_diagnostics(),
               'ordered_clocks_and_guard': ordered_clock_diagnostics(),
               'eroder': eroder_diagnostics(),
               'stopped_replay': replay_diagnostics(),
               'topology': topology_diagnostics(),
               'universal_stability_established_by_diagnostics': False}
    results['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    results['elapsed_seconds'] = time.monotonic() - start
    (OUT / 'DIAGNOSTICS.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))
