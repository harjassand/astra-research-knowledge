"""Exact small-instance check for report 14_chemical_search.txt."""

from math import factorial, prod


def complexes(n: int, d: int) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []

    def compositions(prefix: tuple[int, ...], remaining: int) -> None:
        if len(prefix) == n - 1:
            result.append(prefix + (remaining,))
            return
        for value in range(remaining + 1):
            compositions(prefix + (value,), remaining - value)

    for total in range(d + 1):
        compositions((), total)
    return result


def falling(z: tuple[int, ...], y: tuple[int, ...]) -> int:
    return prod(prod(z_i - j for j in range(y_i)) for z_i, y_i in zip(z, y))


def determinant(matrix: list[list[int]]) -> int:
    if len(matrix) == 1:
        return matrix[0][0]
    return sum(
        (-1) ** j
        * matrix[0][j]
        * determinant([row[:j] + row[j + 1 :] for row in matrix[1:]])
        for j in range(len(matrix))
    )


def main() -> None:
    c = complexes(2, 2)
    p = [[falling(z, y) for y in c] for z in c]
    expected_diagonal_product = prod(prod(factorial(y_i) for y_i in y) for y in c)
    assert determinant(p) == expected_diagonal_product == 4

    jumps = [(-1, 2, 0), (-1, 0, 2), (-1, 1, 1)]
    two_channel_drift = tuple(jumps[0][i] + jumps[1][i] for i in range(3))
    one_channel_drift = tuple(2 * jumps[2][i] for i in range(3))
    assert two_channel_drift == one_channel_drift == (-2, 2, 2)
    assert len(set(jumps)) == 3

    print("C_2 =", c)
    print("P =", p)
    print("det(P) =", determinant(p))
    print("both concentration drift coefficients per k =", two_channel_drift)
    print("event jumps =", jumps)


if __name__ == "__main__":
    main()
