"""Exact subset-orbit audit for PGL(2,8) on P^1(F_8)."""
from itertools import combinations, product

MODULUS = 0b1011  # x^3 + x + 1


def add(a, b):
    return a ^ b


def mul(a, b):
    z = 0
    for i in range(3):
        if (b >> i) & 1:
            z ^= a << i
    for k in range(4, 2, -1):
        if (z >> k) & 1:
            z ^= MODULUS << (k - 3)
    return z


def inv(a):
    assert a
    for b in range(1, 8):
        if mul(a, b) == 1:
            return b
    raise AssertionError(a)


def norm_projective_matrix(M):
    for x in M:
        if x:
            z = inv(x)
            return tuple(mul(y, z) for y in M)
    raise AssertionError("zero matrix")


def projective_group():
    mats = set()
    for a, b, c, d in product(range(8), repeat=4):
        if add(mul(a, d), mul(b, c)) != 0:
            mats.add(norm_projective_matrix((a, b, c, d)))
    assert len(mats) == 504

    # Point labels 0..7 are F_8 elements; 8 denotes infinity.
    perms = set()
    for a, b, c, d in mats:
        image = []
        for x in range(8):
            numerator = add(mul(a, x), b)
            denominator = add(mul(c, x), d)
            image.append(8 if denominator == 0 else mul(numerator, inv(denominator)))
        image.append(8 if c == 0 else mul(a, inv(c)))
        assert sorted(image) == list(range(9))
        perms.add(tuple(image))
    assert len(perms) == 504
    return sorted(perms)


def orbit_sizes(perms, k):
    all_sets = set(combinations(range(9), k))
    sizes = []
    reps = []
    while all_sets:
        seed = min(all_sets)
        orb = {tuple(sorted(p[i] for i in seed)) for p in perms}
        assert orb <= all_sets
        all_sets -= orb
        sizes.append(len(orb))
        reps.append(seed)
    return sorted(zip(reps, sizes), key=lambda x: x[0])


def main():
    perms = projective_group()
    print("PGL(2,8) order:", len(perms))
    for k in range(1, 5):
        orbs = orbit_sizes(perms, k)
        print(f"k={k}, C(9,k)={len(list(combinations(range(9), k)))}, "
              f"orbits={len(orbs)}, sizes={[n for _, n in orbs]}, "
              f"representatives={[r for r, _ in orbs]}")
    assert [len(orbit_sizes(perms, k)) for k in range(1, 5)] == [1, 1, 1, 1]
    print("PASS: exact field/group action; PGL(2,8) is 4-homogeneous on nine points")


if __name__ == "__main__":
    main()
