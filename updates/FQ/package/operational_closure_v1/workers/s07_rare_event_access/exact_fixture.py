"""Exact toy algebra for the proposed catalyst pulse/thermodynamic relay.

No experimental observations are represented here.  Run with Python 3's
standard library: python3 exact_fixture.py
"""

from fractions import Fraction as F
from json import dumps


def native(alpha, beta, gamma, delta=F(0)):
    total = alpha + beta + gamma + delta
    return {
        "R": total,
        "steady_I": alpha / total,
        "formate_flux": alpha * gamma / total,
        "hydrogen_flux": alpha * delta / total,
    }


def reconstructed(K, R, gamma, delta=F(0)):
    beta = (R - gamma - delta) / (1 + K)
    alpha = K * beta
    return native(alpha, beta, gamma, delta)


def out(d):
    return {k: {"exact": str(v), "decimal": float(v)} for k, v in d.items()}


K_off = F(1, 1_000_000)
alpha_off = F(1, 100_000)
beta_off = F(10)
gamma = F(1)

# Transport-valid world: native formation/reversal equal the product-free pair.
world_0 = native(alpha_off, beta_off, gamma)
recovered_0 = reconstructed(K_off, world_0["R"], gamma)
assert world_0 == recovered_0

# An unobserved substrate effect doubles native formation and compensates in
# native reversal, so the pulse relaxation R and product slope gamma are the
# same.  The product-free titration remains unchanged.
alpha_1 = F(2, 100_000)
beta_1 = world_0["R"] - gamma - alpha_1
world_1 = native(alpha_1, beta_1, gamma)
assert world_1["R"] == world_0["R"]
assert world_1["formate_flux"] == 2 * world_0["formate_flux"]

print(dumps({
    "status": "exact toy algebra only; no physical data",
    "product_free_K": str(K_off),
    "pulse_observables_common_to_both_worlds": {
        "R": str(world_0["R"]), "gamma": str(gamma)
    },
    "transport_valid_world": out(world_0),
    "transport_failed_world": out(world_1),
    "formula_infers_world_0_from_common_observables": out(recovered_0),
}, indent=2))
