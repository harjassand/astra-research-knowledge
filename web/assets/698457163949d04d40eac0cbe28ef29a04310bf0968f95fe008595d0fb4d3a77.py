"""Small arithmetic checks for the active-space compression audit.

This checks only finite formulas quoted in the report. It is not a molecular
integral calculation and does not validate the source article's chemistry.
"""
from math import comb, sqrt

HA_TO_KCAL_MOL = 627.509474

# Fixed N_alpha=N_beta determinant-sector sizes for the two source CAS spaces.
full_dimension = comb(11, 8) ** 2
reduced_dimension = comb(8, 5) ** 2

# Frozen natural-orbital occupations reported for n_active=8.
reactant_frozen = (1.99999980, 1.99999927, 1.99999859)
product_frozen = (1.99999988, 1.99999729, 1.99981175)
deficit = lambda occupations: sum(2.0 - x for x in occupations)

# Source table gives reduced-minus-parent CASCI errors per state.
truncation = {
    4: (29.2, 21.9),
    7: (2.5, 1.7),
    8: (0.002, 0.205),
}
barrier_or_reaction_error = {n: p - r for n, (r, p) in truncation.items()}

# Sharp 2x2 counterexample. For H=[[0,v],[v,gap]], fixed discarded-state
# population p determines v and the omitted-energy lowering delta.
p = deficit(product_frozen)
gap_ha = 10.0
v_ha = gap_ha * sqrt(p * (1.0 - p)) / (1.0 - 2.0 * p)
delta_ha = gap_ha * p / (1.0 - 2.0 * p)

# Block-gap certificate f(gamma,beta)=(sqrt(gamma^2+4 beta^2)-gamma)/2.
def block_shift_bound(gamma, beta):
    return (sqrt(gamma * gamma + 4.0 * beta * beta) - gamma) / 2.0

# Nontrivial but small certified-coupling illustration, not measured chemistry.
example_bound_ha = block_shift_bound(0.01, 0.001)

print(f"fixed-Ms determinant dimensions: full={full_dimension}, reduced={reduced_dimension}")
print(f"frozen occupation deficits: R={deficit(reactant_frozen):.9g}, P={p:.9g}")
print("paired reaction-energy truncation errors (reduced - parent, kcal/mol):",
      {n: round(x, 3) for n, x in barrier_or_reaction_error.items()})
print(f"toy fixed-occupation counterexample: p={p:.9g}, gap={gap_ha:g} Ha, "
      f"coupling={v_ha:.9g} Ha, omitted lowering={delta_ha:.9g} Ha "
      f"({delta_ha * HA_TO_KCAL_MOL:.6g} kcal/mol)")
print(f"block certificate example: gamma=.01 Ha, beta=.001 Ha, "
      f"bound={example_bound_ha:.9g} Ha "
      f"({example_bound_ha * HA_TO_KCAL_MOL:.6g} kcal/mol per state)")
