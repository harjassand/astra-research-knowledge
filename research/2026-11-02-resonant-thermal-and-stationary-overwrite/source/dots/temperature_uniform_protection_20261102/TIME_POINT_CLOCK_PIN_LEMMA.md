# Beta-uniform vacuum time-point pins in the dynamic-flux clock gas

2026-11-02. Exact corollary of the existing normalized scalar pin lemma and DYNAMIC_FLUX_ROD_LEMMA.md; not an arbitrary matrix-unit bound.

Fix any prescribed flux history s and insert clock-vacuum projectors |0><0| at a finite collection of spacetime points (a_i,t_i). In the exact rod representation, this deletes each rod whose nonzero interval contains a pin on its own clock, and each wrap on such a clock. No new pair factor is needed. Write Z_pin[s] for this constrained trace.

Let

  E_a = exp(a0) integral_0^beta ell rho_a(ell) exp(b ell)dell,
  Wtilde_a = exp(a0) Tr exp[-beta(A_a-b I)].

Then

  exp[-sum_i(E_{a_i}+Wtilde_{a_i})]
    <= Z_pin[s]/Z[s]
    <= exp[sum_i(E_{a_i}+Wtilde_{a_i})].

The coefficients are independent of beta apart from the decreasing wrap term. For heterogeneous resonant clocks, E_a<=8 eta^2/M and Wtilde_a<=2 eta^2/M under the existing cold condition, so the exponent is at most 10 eta^2/M per pin.

Proof: a rod of length ell covers a fixed time point for exactly ell of the beta-circle start measure. Thus the external-pin cost in the normalized signed-gas ratio lemma is E_a+Wtilde_a. Several pins use the union bound or sequential interpolation. Flux multipliers do not change absolute activities. KP remains valid along deletion interpolations; all partition functions are real and nonzero, hence positive as in the dynamic-flux proof. There is no full-beta-column ownership cost.

This establishes that imposing clock vacuum at local source endpoints is cheap, without imposing global vacuum or dropping actual thermal wraps. It does NOT justify inserting vacuum projectors into an arbitrary physical perturbation as an approximation. To handle arbitrary clock matrix units exactly, one must retain and bound all complementary nonvacuum/open-path terms. Such terms can be organized as open excursions attached to pins and should be charged by the clock resolvent scale mu; that extension is not proved here.
