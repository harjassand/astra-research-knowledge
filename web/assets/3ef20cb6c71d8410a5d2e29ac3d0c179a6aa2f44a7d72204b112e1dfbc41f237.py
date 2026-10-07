"""Exact arithmetic audit of the independently derived ACKN local certificate."""
from fractions import Fraction as Q
import json

eps = Q(1, 10000)
largest_hessian_bound = 30*Q(101,100) + 256*Q(101,100)**6
assert largest_hessian_bound < 310
remainder_ratio = 155*Q(12,5)**2*eps
assert remainder_ratio == Q(4464,5)*eps
inside_a_margin = Q(6,5)-Q(28,100)-remainder_ratio
inside_b_margin = Q(7,5)-Q(49,100)-remainder_ratio
assert inside_a_margin > Q(4,5)
assert inside_b_margin > Q(4,5)

def ambient_margins(collar_ratio):
    remainder = 155*(Q(12,5)+2*collar_ratio)**2*eps
    return [Q(6,5)-66*collar_ratio-remainder,
            Q(7,5)-83*collar_ratio-remainder]

ambient_original = ambient_margins(Q(1,100))
ambient_shrunk = ambient_margins(Q(1,1000))
assert min(ambient_original) > Q(2,5)
assert max(ambient_original) < Q(4,5)
assert min(ambient_shrunk) > Q(4,5)

print(json.dumps({
    "status": "PASS",
    "largest_triangle_Hessian_bound": float(largest_hessian_bound),
    "remainder_over_epsilon_inside_Q": float(remainder_ratio),
    "inside_slab_margins_over_epsilon": [float(inside_a_margin),float(inside_b_margin)],
    "ambient_original_margins_over_epsilon": list(map(float,ambient_original)),
    "ambient_shrunk_margins_over_epsilon": list(map(float,ambient_shrunk)),
    "interpretation": "gamma=0.8 epsilon requires inside slabs, or smaller ambient collar"
}, indent=2))
