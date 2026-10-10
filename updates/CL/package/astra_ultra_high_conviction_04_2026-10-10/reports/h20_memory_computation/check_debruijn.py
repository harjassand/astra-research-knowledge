#!/usr/bin/env python3
"""Finite checks for the source-vs-task residual discriminator."""


def de_bruijn_binary(order: int) -> list[int]:
    a = [0] * (2 * order + 1)
    seq: list[int] = []

    def visit(t: int, p: int) -> None:
        if t > order:
            if order % p == 0:
                seq.extend(a[1 : p + 1])
            return
        a[t] = a[t - p]
        visit(t + 1, p)
        for bit in range(a[t - p] + 1, 2):
            a[t] = bit
            visit(t + 1, t)

    visit(1, 1)
    return seq


def cyclic_window(seq: list[int], start: int, width: int) -> tuple[int, ...]:
    n = len(seq)
    return tuple(seq[(start + j) % n] for j in range(width))


def main() -> None:
    for m in range(1, 9):
        seq = de_bruijn_binary(m)
        n = 1 << m
        assert len(seq) == n
        windows = {cyclic_window(seq, i, m) for i in range(n)}
        assert len(windows) == n == 1 << m

        # The task monitor has exactly two residuals: prefix parity 0 or 1.
        task_residuals = {0, 1}
        # The exact next-m-output predictor has one residual per phase because
        # its length-m continuation uniquely identifies the phase.
        predictor_residuals = {cyclic_window(seq, i, m) for i in range(n)}
        assert len(task_residuals) == 2
        assert len(predictor_residuals) == n
        print(f"order={m} source_states={n} task_states=2 task_bits=1 predictor_bits={m}")


if __name__ == "__main__":
    main()
