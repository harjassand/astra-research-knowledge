# Killed finite-phase factorial certificate without scalar first-up bias
Status: NEW PERSONAL DERIVATION, unreviewed; not a frozen-v1 dependency. This is a local killed certificate, not a bound on physical tail-to-head feedback.

## Contract
Finite modes j, one count x. Internal reactions (a,j)->(b,k) have rates k_e(x)_a. Killing reactions leave from specified complexes (a,j), with the same rate form. Assume (i) every projected mode reaches killing, and (ii) every internal complex edge has a directed complex path from its target back to its source OR to killing. Mode-graph irreducibility alone is insufficient.

Claim: for sufficiently small rational alpha>0, there is positive normlike V(x,j), factorial times a positive rational-Puiseux factor in each mode, with actual killed-generator inequality LV<=-Gamma(x+beta_j+1)^alpha outside a finite set. No per-phase first-up bound is assumed.

## Positive cofactor weights and exact imbalance
The projected killed generator Q_0(x) is transient for large x. Set tau(x)=(-Q_0(x)^T)^(-1)1. Positive forest formulas give strictly positive rational entries with positive leading coefficients. Let beta_j be the integer leading power of tau_j. Recenter r=x+beta_j and recompute Q(r) using lambda_e(r-beta_j). Fixed shifts preserve positive forest leading degrees, so its recomputed tau=(-Q(r)^T)^(-1)1 has the SAME exponents beta_j.

Write F_e=tau_j lambda_e and K_j=tau_j kill_j. The exact internal incoming minus outgoing flux at j is K_j-1. Hence

    u^T diag(tau) Q u
     = -1/2 sum_internal F_e(u_k-u_j)^2
       -1/2 sum_j(K_j+1)u_j^2.                           (1)

Self-mode edges have zero difference term but their tilted gains below remain present.

## Return-or-kill paths absorb upward factorial tilts
Height of complex (a,j) is a+beta_j. Residual increment delta=b-a+beta_k-beta_j is integer. Fix epsilon>0 and multiply internal gains by

    t_e=(1+epsilon)r^(alpha delta) if delta!=0; t_e=1 otherwise.

Keep all original outgoing and killing losses; call the Metzler matrix G. Combining an edge with its part of (1), downward delta gives

    -t_e F_e(u_k-u_j)^2/2
    -(1-t_e)F_e(u_j^2+u_k^2)/2.

For upward delta, writing b=t_e-1 and using Young gives a bound

    -F_e(u_k-u_j)^2/4 +(b+b^2)F_e u_k^2.

Follow the upward edge's return-or-kill path from its target until the first vertex of height at most the original source height, or killing. Every preceding source height is at least one higher than the original source. Its flux thus exceeds the original upward flux by at least c r. The final event is either a downward sink or a killing sink at such a higher source. Telescoping mode values along the preceding path bounds u_k^2 by finitely many differences and the final sink value. Repeated modes cause no problem. For downward edges, their negative sum-of-squares also controls their mode difference with a uniform constant, so vanishing t_e is not an obstacle.

Choose 2 alpha max(delta_+)<1, with no such restriction if no upward edges exist. Finiteness of all paths allows every upward burden to be absorbed by a fixed fraction of the higher-source difference/downward/killing terms for sufficiently large r. The extra -1/2 sum_j u_j^2 survives. Thus the symmetric part of diag(tau)G is strictly negative definite. G is Metzler and Hurwitz; v=(-G)^(-1)1 is strictly positive.

For rational alpha, v has rational-Puiseux entries. Eventual positivity implies v_j(r+ell)/v_j(r)=1+O(1/r) for every fixed integer ell.

## Exact primal lift
Put phi(r)=Gamma(r+1)^alpha, V(x,j)=phi(x+beta_j)v_j(x+beta_j) for large x, and extend positively on the finite remainder. For delta!=0,

    phi(r+delta)v_k(r+delta)/(phi(r)v_k(r))
      =r^(alpha delta)[1+O(1/r)] <= t_e.

For delta=0 there is no argument shift. Consequently LV/phi <=Gv=-1. Killing has exterior value zero and is already included. Factorial growth dominates the polynomial profile, so V is normlike. Stopped localization then earns finite expected phi-cost until killing or entry into a finite low-count set; recurrence was not assumed.

## Actual finite truncations of a weakly reversible network
Let S be ANY finite set of internal population vectors; retain one count X. Lift every original reaction aX+y -> bX+y' enabled at z in S, with coefficient kappa(z)_y, to mode z-y+y' when that mode is in S, otherwise to killing.

Follow an original complex return path holding the internal residual z-y fixed. Either it returns to the lifted source complex or first leaves S and is killed. Thus condition (ii) is automatic. Condition (i) still needs every mode to reach actual exit; closed internal components must be handled separately.

This does not replace physical exit by killing without cost. Extending the function by zero creates incoming boundary forcing under the full process. That must still be bounded and absorbed.

## Remaining obstruction
The theorem repairs scalar first-up failure on a FIXED finite head. It does not bound the growth of beta_j, forest coefficients, or the required M-matrix threshold as the head grows. Generic forest bounds may give polynomial profile exponents proportional to the number of modes, while the available factorial collar separation is only linear in total population. Slowing a cap does not automatically repair these competing coefficients of log s. Nor is a physical boundary-return operator controlled here. No general recurrence claim follows.
