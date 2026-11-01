# Exact independent receipt: cone-weighted clock derivatives

Reviewed source: `../CONE_WEIGHTED_CLOCK_DERIVATIVES.md`, SHA-256 `2293739c573815ba5cfcf721ed020a71fbb24047f95d348a50f4fbd005ea6847`.

**PASS, deterministic conditional scope only.** All first and second derivative identities, constants and domain qualifications in this exact source are correct. The earlier accepted clock/window files are unchanged by this review. No actual cone-admission probability, jump-segment admission, finite-N bridge, CLT or clearance follows.

## Proof check

For `e>0`, `0<g<=3/4`, `l>=g e²`, inverse-flow monotonicity gives

`L(v)>=l+(3/4)(v²-e²)>=g v²`, `v>=e`.

With `J(v)=exp(-integral_e^v L^-3)`, one has `partial_l L(v)=J(v)` and

`b_l=J_infinity-1`,
`b_ll=3J_infinity integral_e^infinity J(v)L(v)^-4 dv>0`.

Since `0<J<=1`, integrating `(g v²)^-3` and `3(g v²)^-4` proves respectively

`|b_l|<=1/(5g³e^5)`, `b_ll<=3/(7g^4e^7)`.

Cooperative comparison implies `b_e<=0`. The PDE

`(1+3l²e)b_l+2l²b_e=-1`

then gives `b_e>=-1/(2l²)`, so `|b_e|<=1/(2g²e^4)`. This combines comparison with the PDE; the PDE alone would not give the sign.

Put `alpha=3e/2+1/(2l²)`. The exact identity `b_e=3e/2-alpha J_infinity` gives

`b_le=J_infinity/l³-alpha b_ll`,
`b_ee=-(3/2)b_l-alpha b_le`.

For `e>=1`, bounding the first mixed term by `g^-3e^-6` and the two terms of `alpha b_ll` separately gives

`|b_le| <= [g^-3+9/(14g^4)]e^-6+[3/(14g^6)]e^-11`
`          <= K_le(g)e^-6`.

Next,

`|b_ee| <= [3/(10g³)+(3/2)K_le(g)]e^-5 + [K_le(g)/(2g²)]e^-10`
`          <= K_ee(g)e^-5`.

Thus the lower `e>=1` threshold is used exactly when replacing `e^-11` by `e^-6` and `e^-10` by `e^-5`; it cannot be silently dropped.

At `g=1/2`, exact rational arithmetic gives

- `1/(2g²)=2`;
- `3/(7g^4)=48/7`;
- `K_le=8+72/7+96/7=32`;
- `K_ee=12/5+(7/2)32=572/5`.

The accompanying `|b_l|` constant is `8/5`. No ODE numerical evaluation is needed for these analytic ceilings.

## Segment and boundary scope

The derivatives exist on the full interior `l>0,e>0`; the cone is a region on which they satisfy these estimates, not an assertion that perturbations remain there. Here `e>0` and the cone already imply `l>0`, so no singular `l=0` evaluation occurs.

For a Taylor remainder, the entire segment must lie in the admitted set. The source's warning that a current-state bound alone is insufficient is correct. The set `{e>=1,l>=g e²}` is convex, so checking **both** actual endpoints in it is sufficient for the straight segment. Weighted suprema along a downward-`e` jump must use the segment's minimum `e`, not automatically the pre-jump value.

No counterexample to the displayed formulas under their stated hypotheses was found. Without the cone, the old counterexample remains: at `e=1`, `l` tending to zero gives `|b_l|` tending to one, not an arbitrary large-`e` decay law. Without the `e>=1` threshold the displayed single-power mixed/second envelopes are not established by these estimates.

The independent checker records exact coefficient identities and source hashes. Its finite/symbolic checks support, rather than replace, the comparison and differentiation arguments above.
