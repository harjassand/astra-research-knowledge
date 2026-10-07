"""Independent exact check of the phased swap-block second moment.

This deliberately imports no peer module. For each 2x2 swap block, the
site-phased skew entry is s_even - i*s_odd, whose squared modulus is 2.
The full-sector coefficient for k block-diagonal swaps is the product of
these squared moduli.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


rows = []
for k in range(1, 5):
    values = []
    for signs in product((-1, 1), repeat=2*k):
        x = 1
        for j in range(k):
            # Represent s_{2j} - i*s_{2j+1} by its exact (real,imag) pair.
            re, im = signs[2*j], -signs[2*j+1]
            x *= re*re + im*im
        values.append(x)
    mean = Fraction(sum(values), len(values))
    second = Fraction(sum(x*x for x in values), len(values))
    ratio = second/(mean*mean)
    assert min(values) == max(values) == 2**k
    assert mean == 2**k and ratio == 1
    rows.append({"k": k, "sign_words": len(values), "sample_min": min(values),
                 "sample_max": max(values), "mean": str(mean),
                 "relative_second_moment": str(ratio)})

out = {"status": "PASS_EXACT_INTEGER_ENUMERATION", "rows": rows,
       "scope": "Independent verification of the phased swap-block fixture only; no general residual certificate is tested."}
dest = Path(__file__).with_name("phase_variance_swap_check.json")
dest.write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
