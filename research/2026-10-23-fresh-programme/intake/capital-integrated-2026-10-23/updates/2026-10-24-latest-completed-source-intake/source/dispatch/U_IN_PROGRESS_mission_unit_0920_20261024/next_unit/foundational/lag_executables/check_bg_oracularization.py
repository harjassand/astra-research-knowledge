"""Exact tiny replay of the stated BG-oracularization completion model.

Inputs are X,Y in [k]^r, uniformly; tags are independent uniform in
{A,B}^r. A homogeneous tag checks only the fully visible side's consistency,
so every actual Gamma edge passes. For a mixed tag and visible context, Bob
chooses one completion. Consistency passes on that completion only, so the
best number of successful actual inputs in this fiber is 1 iff the fiber has
at least one Gamma edge, and 0 otherwise.

This verifies the finite counting formula under that exact interface; it is
not a model-independent proof that every BG-oracularization has this form.
"""

from fractions import Fraction
from itertools import product


def words(k, r):
    return list(product(range(k), repeat=r))


def mixed_visible_fiber_count(gamma, k, r):
    """Count (mixed tag, visible context) pairs whose fiber hits Gamma."""
    W = words(k, r)
    count = 0
    for tag in product((0, 1), repeat=r):  # 0 reveals X; 1 reveals Y
        if all(bit == tag[0] for bit in tag):
            continue
        for visible in W:
            hit = False
            for X in W:
                for Y in W:
                    if (all((X[i] if tag[i] == 0 else Y[i]) == visible[i]
                            for i in range(r)) and (X, Y) in gamma):
                        hit = True
                        break
                if hit:
                    break
            count += int(hit)
    return count


def exact_source_value(gamma, k, r):
    """Optimize Bob independently per visible context, exactly."""
    W = words(k, r)
    edge_count = len(gamma)
    denominator = (2**r) * (k ** (2 * r))

    # Homogeneous tags: 2 choices, and each Gamma edge wins.
    homogeneous_success_units = 2 * edge_count
    # Mixed tag/context: explicitly score every candidate completion against
    # the actual inputs in that fiber, then optimize Bob's local response.
    mixed_success_units = 0
    for tag in product((0, 1), repeat=r):
        if all(bit == tag[0] for bit in tag):
            continue
        for visible in W:
            fiber = [(X, Y) for X in W for Y in W
                     if all((X[i] if tag[i] == 0 else Y[i]) == visible[i]
                            for i in range(r))]
            scores = [sum(int(actual == guess and actual in gamma)
                          for actual in fiber)
                      for guess in fiber]
            mixed_success_units += max(scores, default=0)
    return Fraction(homogeneous_success_units + mixed_success_units,
                    denominator)


def formula_value(gamma, k, r):
    density = Fraction(len(gamma), k ** (2 * r))
    nonempty = mixed_visible_fiber_count(gamma, k, r)
    return (Fraction(2, 2**r) * density
            + Fraction(nonempty, (2**r) * k ** (2 * r)))


def exhaustive_k2_r2():
    k, r = 2, 2
    W = words(k, r)
    universe = [(X, Y) for X in W for Y in W]
    checked = 0
    for mask in range(1 << len(universe)):
        gamma = {universe[j] for j in range(len(universe))
                 if (mask >> j) & 1}
        exact = exact_source_value(gamma, k, r)
        predicted = formula_value(gamma, k, r)
        assert exact == predicted, (mask, exact, predicted)
        checked += 1
    complete = set(universe)
    assert exact_source_value(complete, k, r) == Fraction(5, 8)
    # Nontrivial predicate: first coordinates agree.
    nontrivial = {(X, Y) for X in W for Y in W if X[0] == Y[0]}
    assert len(nontrivial) == 8
    assert mixed_visible_fiber_count(nontrivial, k, r) == 8
    assert exact_source_value(nontrivial, k, r) == Fraction(3, 8)
    return checked


def parity_fixture_k2_r3():
    k, r = 2, 3
    W = words(k, r)
    gamma = {(X, Y) for X in W for Y in W
             if sum(X) % 2 == sum(Y) % 2}
    nonempty = mixed_visible_fiber_count(gamma, k, r)
    assert len(gamma) == 32
    assert nonempty == 48  # every mixed fiber has a completion of matching parity
    assert exact_source_value(gamma, k, r) == Fraction(7, 32)
    complete = {(X, Y) for X in W for Y in W}
    assert mixed_visible_fiber_count(complete, k, r) == 48
    assert exact_source_value(complete, k, r) == Fraction(11, 32)
    return len(gamma), nonempty


if __name__ == "__main__":
    print("k=2,r=2 predicates exhaustively checked:", exhaustive_k2_r2())
    print("k=2,r=3 parity-equality |Gamma|, mixed fibers:",
          parity_fixture_k2_r3())
