"""Exact scaling audit for the c08_l09 fixed-power microcopy construction.

This verifies algebraic powers of the copy scale only. It does not construct
or validate the imported positive-entropy gadget or the statistical channel.
"""

import json
from pathlib import Path

import sympy as sp


n, alpha, v0, c, h0, e0, g0 = sp.symbols(
    "n alpha v0 c h0 e0 g0", positive=True
)
r = (alpha / (n**3 * v0)) ** sp.Rational(1, 3)
copy_volume = v0 * r**3
num_copies = n**3

entropy = sp.simplify(num_copies * copy_volume * c * h0)
strain_energy = sp.simplify(num_copies * copy_volume * c**2 * e0)
speed_scale = sp.simplify(r * c)
gradient_scale = c
higher_derivative_scale = sp.simplify(c * r ** (1 - sp.Symbol("k")))
gradient_strain_energy = sp.simplify(
    num_copies * copy_volume * c**2 * r**-2 * g0
)

assert sp.simplify(copy_volume - alpha / n**3) == 0
assert sp.simplify(entropy - alpha * c * h0) == 0
assert sp.simplify(strain_energy - alpha * c**2 * e0) == 0
assert sp.simplify(gradient_strain_energy - alpha * c**2 * g0 / r**2) == 0
assert sp.simplify(speed_scale / (c * alpha ** sp.Rational(1, 3)
                                  / (v0 ** sp.Rational(1, 3) * n)) - 1) == 0

eta = sp.symbols("eta", positive=True)
c_eta = eta / (alpha * h0)
assert sp.simplify(entropy.subs(c, c_eta) - eta) == 0
assert sp.simplify(strain_energy.subs(c, c_eta)
                   - eta**2 * e0 / (alpha * h0**2)) == 0

result = {
    "status": "PASS",
    "copy_volume": str(copy_volume),
    "total_entropy": str(entropy),
    "total_strain_energy": str(strain_energy),
    "speed_scale": str(speed_scale),
    "gradient_scale": str(gradient_scale),
    "kth_derivative_scale": str(higher_derivative_scale),
    "integrated_gradient_strain_energy": str(gradient_strain_energy),
    "scope": "exact scaling identities only; imported gadget and observation theorem not checked",
}
output = Path(__file__).with_suffix(".json")
output.write_text(json.dumps(result, indent=2) + "\n")
print(result)
