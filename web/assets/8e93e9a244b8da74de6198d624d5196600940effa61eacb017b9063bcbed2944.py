"""Second cone-cover certificate for C_W with proper decoder outputs."""

from finite_checks import C, all_faces, face, vc_dimension, teaching_size


# (support mask, support labels, decoded class member), in bit-position order.
DECODER = (
    (0, 0, 22), (1, 1, 17), (2, 0, 13), (2, 2, 11), (3, 0, 24),
    (3, 1, 21), (3, 2, 6), (3, 3, 3), (4, 0, 11), (5, 0, 24),
    (5, 1, 17), (5, 4, 22), (5, 5, 13), (6, 0, 17), (6, 2, 26),
    (6, 4, 12), (8, 0, 17), (8, 8, 11), (9, 1, 21), (9, 8, 24),
    (10, 0, 21), (10, 10, 26), (12, 0, 3), (12, 4, 22),
    (12, 8, 24), (12, 12, 12), (16, 0, 12), (16, 16, 17),
    (17, 0, 6), (17, 1, 11), (17, 17, 21), (18, 0, 12),
    (18, 2, 3), (18, 16, 21), (20, 4, 6), (20, 16, 24),
    (24, 0, 3), (24, 8, 12), (24, 24, 24),
)


def verify():
    n = len(C[0])
    class_vertices = {
        sum(int(c[i]) << i for i in range(n)) for c in C
    }
    faces = all_faces(C)
    assert vc_dimension(C) == 2
    assert {teaching_size(c, C) for c in C} == {3}
    assert len(faces) == 176
    roots = [(mask, value) for mask, value, _ in DECODER]
    assert len(roots) == len(set(roots))
    for mask, value, hypothesis in DECODER:
        assert mask.bit_count() <= 2
        assert hypothesis & mask == value
        assert hypothesis in class_vertices
    for face_mask, face_value in faces:
        assert any(
            root_mask & face_mask == root_mask
            and hypothesis & face_mask == face_value
            for root_mask, _root_value, hypothesis in DECODER
        ), (face_mask, face_value)
    return len(faces), len(DECODER)


if __name__ == "__main__":
    face_count, code_count = verify()
    print(
        f"PASS: {code_count} proper decoder entries cover all {face_count} "
        "realizable partial samples of C_W with support size <= 2 and no side bits."
    )
