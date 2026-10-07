"""Exact scaling audit for the narrow-margin m=2 return certificate."""

from fractions import Fraction as F
import json
from pathlib import Path


def ceil_q(x):
    return (x.numerator + x.denominator - 1) // x.denominator


rows = []
for b in range(2, 13):
    M = 1 << b
    N = M + 1
    p = F(1, N)
    q = F(M, N * N)
    fq = (1 - q) ** 2 - M * M * q * q
    closed = F(2 * M**3 + 3 * M**2 + 2 * M + 1, N**4)
    assert fq == closed
    eta = fq / (4 * (1 + M * M))
    raw = max(4, ceil_q(2 / q), ceil_q(1 / eta))
    V0 = raw if raw % 2 == 0 else raw + 1
    rows.append({
        "b": b,
        "M": M,
        "rate_K": M * M,
        "p": str(p),
        "q": str(q),
        "p_minus_q": str(p - q),
        "f_q": str(fq),
        "eta": str(eta),
        "even_volume_floor": V0,
        "V0_over_M_cubed": str(F(V0, M**3)),
    })

result = {
    "status": "PASS",
    "exact_identity": "f(q)=(2 M^3+3 M^2+2 M+1)/(M+1)^4",
    "certificate_eta": "f(q)/(4(1+M^2))",
    "asymptotic_derivation": {
        "q": "M/(M+1)^2 ~ M^-1",
        "f_q": "~ 2/M",
        "eta": "~ 1/(2 M^3)",
        "sufficient_even_volume_floor": "V0 ~ 2 M^3 = 2^(3b+1)",
        "meaning": "a sufficient certificate threshold only, not a necessary volume or an algorithmic lower bound",
    },
    "rows": rows,
}
out = Path(__file__).with_name("margin_volume_scaling.json")
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
