from fractions import Fraction
import json


def check():
    cases = []
    for twice_j in range(1, 31):
        j = Fraction(twice_j, 2)
        d = twice_j + 1
        for Q in range(1, d):
            s = sum((Fraction(Q-k, Q)) ** 2 for k in range(Q))
            E = sum(Fraction(k, Q**2) * (2*j-k+1) for k in range(1, Q+1))
            s_closed = Fraction((Q+1)*(2*Q+1), 6*Q)
            ratio_closed = Fraction(3*d, 2*Q+1)-1
            ratio = E/s
            loss = ratio/(2*j*(j+1))
            loss_bound = Fraction(3, Q*(j+1))
            assert s == s_closed, (twice_j, Q, s, s_closed)
            assert ratio == ratio_closed, (twice_j, Q, ratio, ratio_closed)
            assert ratio <= Fraction(6, Q)*j, (twice_j, Q, ratio)
            assert loss <= loss_bound, (twice_j, Q, loss, loss_bound)
            if Q == 1:
                assert E == 2*j
                assert loss == 1/(j+1)
            cases.append({"twice_j": twice_j, "Q": Q, "E_over_s": str(ratio)})
    return {
        "cases": len(cases),
        "twice_j_max": 30,
        "checks": [
            "exact taper norm",
            "exact ladder commutator energy",
            "closed E/s identity",
            "E/s <= 6j/Q",
            "dipole loss <= 3/(Q(j+1))",
            "rank-one coherent-channel normalization",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
