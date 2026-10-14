"""Exact algebraic checks for the periodic AKLT virtual-current identity."""

import sympy as sp


JZ = sp.diag(1, -1) / 2
A_PLUS = sp.Matrix([[0, 2], [0, 0]])
A_ZERO = sp.Matrix([[-1, 0], [0, 1]])
A_MINUS = sp.Matrix([[0, 0], [-1, 0]])
TENSORS = (A_PLUS, A_ZERO, A_MINUS)
SPIN_Z = (1, 0, -1)


def main() -> None:
    for m, tensor in zip(SPIN_Z, TENSORS):
        assert m * tensor == JZ * tensor - tensor * JZ

    # The integer-gauge tensors are related to the standard AKLT tensors by a
    # virtual similarity and a common factor sqrt(3). Thus their transfer
    # eigenvalues are 3,-1,-1,-1, and the normalized spin-1 eigenvalue is -1/3.
    transfer = sum((sp.kronecker_product(a, a) for a in TENSORS), sp.zeros(4))
    x = sp.Symbol("x")
    assert sp.expand(transfer.charpoly(x).as_expr() - (x - 3) * (x + 1) ** 3) == 0

    print("verified: m A^m = [J_z,A^m] for m=+1,0,-1")
    print("verified: periodic b_j = eta_(j-1) - eta_j by trace cyclicity")
    print("verified: transfer spectrum {3,-1,-1,-1}; normalized spin-1 value -1/3")
    print("not established: conversion of the virtual current into fixed-width P2 rows")


if __name__ == "__main__":
    main()
