# Exact BUSY completion for bounded old-bank reuse
30 October 2026. Root completion to BOUNDED_OLD_BANK_REUSE_V1.md. Review pending; the V1 conditional wording remains historically unchanged.

The actual direct singleton BUSY proof supplies a positive physical witness G_b, commuting all strong BUSY masks, with

 exp(theta_b M_b)<=G_b<=exp(Theta_b M_b),
 L_mem^*G_b<=-lambda_b G_b log G_b+rho_b N G_b.

These are the exact form used in ACTUAL_BUSY_HORIZON_AND_JOINT_CUT.md and its scoped review, ultimately from DIRECT_SINGLETON_DERIVATION_V1.md. In canonical G coordinates this witness is on memory variables only; the physical combined witness is G(G_b V_r)G†. In particular no operator Jensen for a CP pullback is needed on this BUSY side.

Let W_b=G_b V_r. The same active-corner relative norm bound as V1, using the BUSY witness's actual finite-depth local norm control, gives

 L_total^* W_b <= -lambda_b W_b log G_b
                 -(c_r-C_hot,b J) M_r W_b
                 +(rho_b+C_noise,b eta)N W_b.

Since log V_r<=log(1+u)M_r and G_b,V_r commute, choose

 c_r-C_hot,b J >= lambda_b log(1+u).

Then L_total^*W_b<=-lambda_b W_b log W_b+(rho_b+C_noise,b eta)N W_b. Spectral Jensen gives the full-state scalar log moment. Initial ready memory has G_b=I on its source, so log Tr W_b rho(0)<=log(1+u)N. Because W_b>=G_b>=exp(theta_b M_b), this proves

 Pr{M_b>=b_b N} <= exp[-N(theta_b b_b-max(log(1+u),(rho_b+C_noise,b eta)/lambda_b))].

Choose u so log(1+u)<theta_b b_b with a strict margin, then select native epsilon/noise and Lambda in the consistent order below. This is pointwise, including during the initial transfer, not an anytime claim.

## One noncircular selection order
1. Fix the actual code, native fast hardware and common decoding/basin radii. Fix allowed q_hot and incident strong source budget J.
2. Choose sufficiently small native first amplitude/proof strengths so both the canonical limiting coefficient and the old BUSY limiting coefficient fit strict chosen energy/BUSY margins, initially with zero weak physical noise. Freeze those witnesses/local relative constants.
3. Choose u>0 small enough for BOTH initial coefficients: g+log(1+u) below the memory barrier and log(1+u) below theta_b b_b. Router rate ratios and normalized A are fixed.
4. Choose Lambda large enough for BOTH absorption inequalities in V1 and this completion, and for the routing-only active-corner estimate with a strict positive remaining decay. All are inequalities of the form Lambda times a fixed positive number > fixed constants times J plus fixed native rates. Such a finite Lambda exists. Its hardware/power cost is not suppressed.
5. Choose the common weak-noise strength eta below the now-fixed positive thresholds. Then choose a constant startup dwell from the routing-only moment inequality.

This supplies the previously missing exact BUSY receiving form. The combined canonical comparison, physical BUSY tail and physical routing tail remain separate positive arguments until their final gentle-cut composition. No product of their full native witnesses is asserted.
