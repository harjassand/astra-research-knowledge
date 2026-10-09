"""Finite certificate for cone-cover compression on Warmuth's class C_W.

Coordinates are indexed 0,...,4 in the strings below.  A face is encoded as
(mask, value), where mask selects observed coordinates and value stores their
labels in the same bit positions.  A decoder entry (mask, value, h) retains
that labeled root and reconstructs the fixed binary hypothesis h.
"""

from itertools import combinations


C = (
    "00011",
    "00110",
    "01100",
    "11000",
    "10001",
    "01011",
    "10110",
    "01101",
    "11010",
    "10101",
)

# Exact cone cover found by finite search.  The table has one decoder output
# per labeled root, so it uses no side information.
DECODER = (
    (12, 4, 21), (4, 0, 25), (3, 1, 13), (17, 0, 14), (20, 20, 23),
    (5, 1, 3), (8, 0, 17), (9, 8, 12), (2, 2, 10), (1, 0, 0),
    (24, 8, 9), (6, 2, 27), (16, 16, 30), (20, 4, 6), (18, 16, 29),
    (3, 0, 24), (20, 16, 27), (3, 3, 15), (5, 0, 26), (12, 12, 14),
    (10, 2, 3), (8, 8, 9), (17, 17, 21), (16, 0, 4), (18, 0, 5),
    (24, 16, 22), (6, 4, 4), (20, 0, 1), (3, 2, 30), (12, 8, 11),
    (9, 0, 6), (0, 0, 30), (9, 9, 13), (1, 1, 5), (2, 0, 13),
    (10, 10, 31), (6, 0, 0), (6, 6, 23),
)


def face(word, coordinates):
    mask = sum(1 << i for i in coordinates)
    value = sum(int(word[i]) << i for i in coordinates)
    return mask, value


def all_faces(concepts):
    n = len(concepts[0])
    faces = set()
    for concept in concepts:
        for size in range(n + 1):
            for coordinates in combinations(range(n), size):
                faces.add(face(concept, coordinates))
    return faces


def vc_dimension(concepts):
    n = len(concepts[0])
    shattered = []
    for size in range(n + 1):
        for coordinates in combinations(range(n), size):
            traces = {
                tuple(concept[i] for i in coordinates)
                for concept in concepts
            }
            if len(traces) == 1 << size:
                shattered.append(size)
    return max(shattered)


def teaching_size(concept, concepts):
    n = len(concept)
    for size in range(n + 1):
        for coordinates in combinations(range(n), size):
            trace = tuple(concept[i] for i in coordinates)
            if sum(
                tuple(other[i] for i in coordinates) == trace
                for other in concepts
            ) == 1:
                return size
    raise AssertionError("a finite distinct concept must be teachable")


def verify():
    assert len(C) == len(set(C)) == 10
    assert vc_dimension(C) == 2
    assert {teaching_size(c, C) for c in C} == {3}

    # Each code root is labeled consistently with its fixed decoded hypothesis.
    roots = [(mask, value) for mask, value, _ in DECODER]
    assert len(roots) == len(set(roots))
    for mask, value, hypothesis in DECODER:
        assert hypothesis & mask == value
        assert mask.bit_count() <= 2

    faces = all_faces(C)
    assert len(faces) == 176
    uncovered = []
    for face_mask, face_value in faces:
        covered = any(
            root_mask & face_mask == root_mask
            and hypothesis & face_mask == face_value
            for root_mask, _root_value, hypothesis in DECODER
        )
        if not covered:
            uncovered.append((face_mask, face_value))
    assert not uncovered, uncovered
    return len(faces), len(DECODER)


if __name__ == "__main__":
    face_count, code_count = verify()
    print(
        f"PASS: VCdim=2; all 10 concepts have teaching size 3; "
        f"{code_count} fixed decoder entries cover all {face_count} "
        "realizable partial samples with support size <= 2 and no side bits."
    )
