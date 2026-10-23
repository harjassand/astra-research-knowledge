# Scoped Gaussian-linker and kinetic-race audit

## Geometry ratio

Use the **open-mask reference state** of the stated three-state partition
model, conditioned only on the existing local anchor pairings: H is anchored
to M at `b`, and L remains anchored to M at `a`. In the proposed nonthreaded
contour order `b -> M tag -> a`, write the zero-mean phantom-linker endpoint
vectors as independent isotropic Gaussian sums. In Kuhn-segment variance
units, the relative endpoint vectors are

`R_M = X_H + X_(M,b->tag)`,

`R_L = X_H + X_(M,b->a) + X_(L,return)`.

Thus the per-coordinate variances are the stated
`v_M=N_H+N_M(b->tag)` and
`v_L=N_H+N_M(b->a)+N_Lreturn`. Since the tag is between `b` and `a`,
`N_M(b->a)=N_M(b->tag)+N_M(tag->a)`, and `N_M(tag->a),N_Lreturn>=0`;
therefore `v_L>=v_M`. At zero endpoint offset, the 3-D Gaussian contact
density is proportional to `v^(-3/2)`. With the same capture volume and
orientation factor for the two identical targets,

`c_L/c_M = (v_M/v_L)^(3/2) <= 1`.

This is a conditional ideal-linker result, not a DNA prediction. The ratio
uses the open-state ensemble with the two specified anchor constraints; it
must not be computed by treating an already H-L-closed loop as an independent
open coil. Extra cycle/loop constraints require a conditional covariance
calculation. A fixed nonzero endpoint offset changes the density to
`v^(-3/2)*exp(-|R_0|^2/(2*sigma^2*v))`; the exponential can reverse the
ordering. Unequal capture/orientation factors, excluded volume, stiffness,
threading, or sequence-specific interactions also remove the stated ratio
conclusion.

## Consequence for the three-state partition model

Retain its definitions

`p_pre = c_M/(K_d+c_L+c_M)`,

`p_post = c_M/(c_M+(K_d+[L])B_T)`,

with `K_d>0`, `[L]>=0`, and `B_T>=1`. If `p_post>=1-delta`, then
`(K_d+[L])B_T <= delta*c_M/(1-delta)`, hence
`K_d <= delta*c_M/(1-delta)`. Combining with the scoped geometry bound
`c_L<=c_M` gives

`p_pre >= c_M/(K_d+2*c_M) >= (1-delta)/(2-delta)`.

The bound is sharp within these assumptions: equality occurs at
`[L]=0`, `B_T=1`, `c_L=c_M`, and `K_d=delta*c_M/(1-delta)`. Therefore a
simultaneous pre-mask target `p_pre<=epsilon` requires
`epsilon >= (1-delta)/(2-delta)`; for small post-error `delta`, the input
must already be masked at least about half the time. The inequality is not a
universal chemical no-go: it depends on common `K_d`, common `c_M`, and the
Gaussian geometry ordering.

## Three-state first-passage time

For `C -> O` at rate `u>0`, `O -> M` at `v>0`, `O -> C` at `w>=0`, and
absorbing target `M`, let `T_C,T_O` be the mean hitting times from C and O.
First-step equations give

`T_C = 1/u + T_O`,
`T_O = 1/(v+w) + [w/(v+w)]*T_C`,

so `T_C=(u+v+w)/(u*v)`. With the same `u,v` pre- and post-admission,
`w_pre<=v` and `w_post>=0` imply

`t_pre/t_post <= (u+2v)/(u+v) < 2`,

and in particular `t_pre<=2*t_post`. Thus this Markov model cannot provide
an arbitrarily long protected-input waiting time together with a much faster
post-admission M capture: the mean-time selectivity is less than two. The
kinetic conclusion additionally requires that equal capture/orientation
factors make `w_pre<=v` a rate inequality and that `u,v` really are unchanged
across the operation; an equilibrium effective-concentration ratio alone
does not force those kinetic assumptions.
