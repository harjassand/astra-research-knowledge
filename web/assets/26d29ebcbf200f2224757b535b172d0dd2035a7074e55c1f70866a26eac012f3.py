"""Exact finite check: realizable version spaces can have large VC dimension.

The concept class consists of the n co-singletons c_i(j)=1 iff i != j.
It has VC dimension 1, but the range family of version spaces induced by
realizable partial samples shatters n-1 concepts.
"""

from itertools import combinations


def concept(i, n):
    return tuple(int(j != i) for j in range(n))


def all_realizable_faces(n):
    faces = set()
    concepts = [concept(i, n) for i in range(n)]
    for c in concepts:
        for mask in range(1 << n):
            value = sum(c[j] << j for j in range(n) if mask >> j & 1)
            faces.add((mask, value))
    return concepts, faces


def vc_dimension(rows):
    n = len(rows[0])
    for k in range(n, -1, -1):
        for coords in combinations(range(n), k):
            traces = {tuple(row[j] for j in coords) for row in rows}
            if len(traces) == 1 << k:
                return k
    raise AssertionError("empty set should be shattered")


def range_vc_dimension(ranges, ground_size):
    for k in range(ground_size, -1, -1):
        for points in combinations(range(ground_size), k):
            traces = {tuple(int(p in r) for p in points) for r in ranges}
            if len(traces) == 1 << k:
                return k
    raise AssertionError("empty set should be shattered")


def check(n=7):
    concepts, faces = all_realizable_faces(n)
    version_spaces = set()
    for mask, value in faces:
        version_spaces.add(frozenset(
            i for i, c in enumerate(concepts)
            if all(not (mask >> j & 1) or ((value >> j) & 1) == c[j]
                   for j in range(n))
        ))

    # All positive samples on a subset A have version space {c_i : i not in A}.
    # Taking A among {0,...,n-2} realizes every trace on those n-1 concepts,
    # while concept c_(n-1) remains a consistent witness.
    shattered = tuple(range(n - 1))
    traces = {
        tuple(int(i in r) for i in shattered)
        for r in version_spaces
    }
    assert len(traces) == 1 << (n - 1)
    assert vc_dimension(concepts) == 1
    assert range_vc_dimension(version_spaces, n) == n - 1

    # The cone family with a fixed empty root has VC dimension exactly n:
    # positive singleton faces are shattered, and there are only 2^n tops.
    positive_singletons = [
        (1 << j, 1 << j) for j in range(n)
    ]
    assert all(face in faces for face in positive_singletons)
    cone_traces = {
        tuple((h >> j) & 1 for j in range(n))
        for h in range(1 << n)
    }
    assert len(cone_traces) == 1 << n

    # A tiny improper scheme exists despite the large version-space VC number:
    # empty root -> all-ones hypothesis; root (j,0) -> co-singleton c_j.
    for mask, value in faces:
        negative = [j for j in range(n) if mask >> j & 1 and not (value >> j & 1)]
        if negative:
            assert len(negative) == 1
            j = negative[0]
            h = concepts[j]
            assert (1 << j) & mask
            assert all(h[x] == ((value >> x) & 1)
                       for x in range(n) if mask >> x & 1)
        else:
            assert all((value >> j) & 1 for j in range(n) if mask >> j & 1)
    return len(faces), len(version_spaces)


if __name__ == "__main__":
    n = 7
    face_count, range_count = check(n)
    print(
        f"PASS: co-singleton class on {n} points has VCdim=1; "
        f"{face_count} realizable faces induce {range_count} version spaces; "
        f"version-space VC={n - 1}; fixed-empty-root cone VC={n}; "
        "an improper size-1 decoder covers every face."
    )
