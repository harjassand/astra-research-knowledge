# Independent exact receipt: global l-weighted clock derivatives

Source: `../GLOBAL_L_WEIGHTED_CLOCK_DERIVATIVES.md`, SHA-256 `20dff0a1775870b93aa81a12bb88125892f242a0986438b3ce9e63e0c4d83ccb`.

**PASS. No repair required.** This is acceptance of deterministic derivative identities and analytic ceilings, conditional on the already defined deterministic remaining clock. No actual path admission, finite-N martingale, normal approximation or computational-cost conclusion is included. The source was not changed.

## 1. Inverse-flow tails, without a ratio gate

In increment coordinates, `L'=1/(2L²)+(3/2)(e+w)`, `L(0)=l>0`, and `J'= -J L^-3`, `J(0)=1`. Since `e>=0`,

`L(w)>=l+3w²/4`.

Thus `|b_l|=1-J_inf<=min(1,integral L^-3 dw)`. The elementary integrals are exactly

`integral_0^infinity (l+3w²/4)^-3 dw=(sqrt(3) pi/8)l^-5/2`,
`3 integral_0^infinity (l+3w²/4)^-4 dw=(5sqrt(3) pi/16)l^-7/2`.

The already derived second derivative `b_ll=3J_inf integral J L^-4` is positive, and `0<J<=1`. Consequently both tail constants and the coarse rational bounds `1` and `5/2` are correct, using only `pi<4` and `sqrt(3)<2`. These statements are uniform over all `e>=0`; no omitted lower/upper e/l ratio is used.

## 2. Uniform startup sensitivity

For `h=1/(2sqrt(1+e))`, the case `l>=h` is immediate because `10(1+e)l²>=5/2>1>=J_inf`. Otherwise the level `L=h` is reached, and

`w_h<=2(h³-l³)/3<=2h³/3`.

The exact identity obtained by differentiating `log L` is

`J(w_h)=(l/h)² exp[integral_0^{w_h} 3(e+w)/L dw]`.

Since `dw/dL<=2L²` and `w<=2h³/3` before that level, the exponent is at most `3e h²+2h^5<=13/16`. Hence

`J_inf<=J(w_h)<=4(1+e)l² exp(13/16)<10(1+e)l²`.

The checker supplies an exact rational Taylor-sum/geometric-remainder certificate for `exp(13/16)<5/2`; no numerical exponential estimate is needed.

Also

`b_ll<= (3J_inf/l) integral J L^-3 dw =3J_inf(1-J_inf)/l`.

Combining the two independent bounds gives

`b_ll<=min(30(1+e)l,3/(4l))<=sqrt((45/2)(1+e))<=5sqrt(1+e)`.

All formulas here are evaluated at `l>0`. Boundary extensions use the already received smooth forward-flow construction, not literal division by zero.

## 3. Mixed derivative sign and startup control

Differentiating with respect to e at fixed l in increment coordinates gives

`Y'=-L^-3Y+3/2`, `Y(0)=0`, so `0<=Y<=3w/2`.

Differentiation under the convergent sensitivity integral yields

`b_le=3J_inf integral L^-4Y dw>=0`.

This sign is consistent with the exact fixed-coordinate identity

`b_le=J_inf/l³-alpha b_ll`, `alpha=3e/2+1/(2l²)`,

and therefore also implies `b_le<=l^-3`. The formula for `b_ee=-(3/2)b_l-alpha b_le` is unchanged.

Now impose `e²<=3l`. For `l<=1/2`, one has `e<5/4`. At the fixed level `L=1/2`, the preceding logarithmic exponent is strictly below one, so `J_inf<4 exp(1)l²<12l²`. Before that level,

`Y<=3w/2<=L³-l³`, `dw/dL<=2L²`,

and hence `integral L^-4Y dw<=integral_l^{1/2}2L dL<=1/4`.

After the level, use the new coordinate z. The bounds `Y<=1/8+(3/2)z` and `L>=1/2+3z²/4` are valid. The two tail integrals are exactly

`(1/8) integral_0^infinity (1/2+3z²/4)^-4 dz =5sqrt(6)pi/48<5/4`,
`(3/2) integral_0^infinity z(1/2+3z²/4)^-4 dz =8/3`.

Thus the full integral is less than `25/6`. Multiplying first by `3J_inf<=3`, then by `3J_inf<36l²`, gives respectively `b_le<25/2<13` and `b_le<150l²`. For `l>=1/2`, the separate bound `b_le<=l^-3<=8` applies. No small-l constant is extrapolated without its threshold.

## 4. Every padded-cone ceiling

The global displayed constants on `e²<=3l` follow as follows:

- `|b_l|<=1` was already global.
- Cooperative monotonicity gives `b_e<=0`; the exact expression gives `b_e>=-J_inf/(2l²)`. Thus `|b_e|<6` for `l<=1/2` using `J_inf<12l²`, while `|b_e|<=1/(2l²)<=2` for `l>=1/2`.
- For `l<=1`, `e<2`, so `b_ll<=5sqrt(1+e)<5sqrt(3)<9`. For `l>=1`, the tail bound gives `b_ll<=5/2<9`.
- `0<=b_le<=13` follows from the two preceding mixed-derivative regimes.
- For `l<=1/2`,
  `|b_ee|<3/2+[15/8+1/(2l²)]150l²<=2349/16<148`.
  For `l>=1/2`, use `e<2sqrt(l)`, `b_le<=l^-3` and `|b_l|<=1`; the resulting upper bound `3/2+3l^-5/2+(1/2)l^-5` is at most `35.5`, already far below 148.

For `l>=1`, `e<2sqrt(l)` and the decay bound on `b_l` yield

`|b_ee|<=(3/2)l^-5/2+3l^-5/2+(1/2)l^-5<=5l^-5/2`.

All other stated tails are the earlier global bounds. Thus the constants `6,9,13,148,5` are supported analytically, not by fitted numerical evaluations.

## 5. Weight and segment scope

Squaring `|b_l|<=min(1,l^-5/2)` gives the stated `psi(l)=min(1,l^-5)` bound, with integral `1+1/4=5/4`. This deterministic integrability is not an actual stochastic occupation or bracket estimate.

On `l>0`, the function `e²/l` is convex. Equivalently the padded set is the epigraph `l>=e²/3`, intersected with `l>0,e>=0`. Checking both segment endpoints therefore guarantees this geometric condition along a straight Taylor segment. A current-state check alone is insufficient; actual jump padding and exits still must be received. Segments touching `l=0` require the separate smooth boundary/startup receiver rather than direct use of the inverse expressions.

All inequalities and integral constants have focused executable exact checks in this receipt directory. No source or dependency/cache experiment was performed.
