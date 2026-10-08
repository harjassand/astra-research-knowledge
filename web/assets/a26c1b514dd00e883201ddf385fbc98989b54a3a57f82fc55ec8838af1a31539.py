from fractions import Fraction as F
import json
from pathlib import Path


def add(A, i, j, v):
    A[i][j] += v


def check(L, J, kappa, lam):
    S = L - 1
    dim = 1 << S
    target = [[F(0) for _ in range(dim)] for _ in range(dim)]
    rhs = [[F(0) for _ in range(dim)] for _ in range(dim)]
    delta = F(1) + kappa / (4 * J * L * L)
    b = (kappa + lam) / (2 * L * L)
    C = 2 * J - kappa * (S - 1) / (2 * L * L) - lam * S / (2 * L * L)

    def z(bit):
        return 1 - 2 * bit

    for x in range(dim):
        occ = [(x >> i) & 1 for i in range(S)]
        diag_h = F(0)
        # Hcrit diagonal and contact/chemical terms.
        for i in range(S - 1):
            diag_h += J * (1 - z(occ[i]) * z(occ[i + 1]))
            diag_h -= kappa / (L * L) * occ[i] * occ[i + 1]
        # Both endpoint fields are retained, including S=1.
        diag_h += J * (1 - z(occ[0]))
        diag_h += J * (1 - z(occ[-1]))
        diag_h -= lam / (L * L) * sum(occ)
        add(target, x, x, diag_h)

        diag_g = F(0)
        for i in range(S - 1):
            diag_g += delta * (z(occ[i]) * z(occ[i + 1]) - 1)
        diag_g += delta * z(occ[0])
        diag_g += delta * z(occ[-1])
        add(rhs, x, x, C + b * sum(z(bit) for bit in occ) - J * diag_g)

        # The XX+YY matrix element is -2J for each allowed exclusion hop.
        for i in range(S - 1):
            if occ[i] != occ[i + 1]:
                y = x ^ (1 << i) ^ (1 << (i + 1))
                add(target, x, y, -2 * J)
                add(rhs, x, y, -2 * J)

    if target != rhs:
        raise AssertionError((L, target, rhs))
    return {"L": L, "sites": S, "dimension": dim, "entries_checked": dim * dim,
            "Delta": str(delta), "b": str(b), "exact_equal": True}


def main():
    fixtures = []
    params = (F(3, 2), F(5, 3), F(-2, 5))
    for L in range(2, 8):
        fixtures.append(check(L, *params))
    out = {
        "status": "FINITE-EVIDENCE",
        "arithmetic": "exact fractions",
        "scope": "matrix identity only; not proof of Bethe completeness or asymptotics",
        "fixtures": fixtures,
        "total_matrix_entries_compared": sum(x["entries_checked"] for x in fixtures),
    }
    path = Path(__file__).with_name("exact_check.json")
    path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
