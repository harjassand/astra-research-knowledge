# Mixed raw-bit / dirty-target seed subset bound
30 October 2026, 17:19 UTC. Explicit receiving calculation for the subset premise in GENUINE_CLASSICAL_SEED_RECEIVING.md. It uses the accepted weighted-cb subset inequality, not a new stochastic-noise model.

Fix a genuine outcome vector m. Raw input bits are |m>; target bits may be arbitrary and correlated with DATA/bath. For selected raw indices R and selected target indices A, define wrong-bit projectors B_i relative to m on raw bits and to0 on targets. They commute. During target resetting use

 F_(R,A)(t)=exp[theta_hi sum_(i in R) B_i
                      +theta_A(t) sum_(i in A) B_i].

Only targets are nominally reset. Choose theta_lo>0 and

 theta_A(t)=log(1+(exp(theta_lo)-1) exp(kappa t)),
 tau=log[(exp(theta_hi)-1)/(exp(theta_lo)-1)]/kappa.

Thus theta_A(0)=theta_lo, theta_A(tau)=theta_hi, and

 theta_A'=kappa(1-exp(-theta_A)).

The derivative EXACTLY cancels the target-reset adjoint term on this test. Raw bits are not secretly reset. Initially their defect projectors vanish, while arbitrary target state gives

 Tr(F_(R,A)(0)rho)<=exp(theta_lo |A|).

The accepted local relative-norm subset lemma, with max exponent theta_hi and arbitrary retained bath, gives

 (partial_t+L_actual^*)F_(R,A)
       <=C eta (|R|+|A|) exp(a theta_hi) F_(R,A).

Consequently, at reset end all selected projectors have the same exponent theta_hi and their joint all-defective probability is at most

 exp{[-theta_hi+theta_lo+C eta tau exp(a theta_hi)](|R|+|A|)}.  (SR1)

The use of theta_lo |A|<=theta_lo(|R|+|A|) is the only relaxation. Conditioning on m does not change constants, since the conditional bath is arbitrary and the bound is uniform on it.

Now run the fixed-depth CNOT seed copy circuit for fixed time tau_c, with all its noise included. In its ideal partial-circuit frame, every perturbation has only a fixed support/incidence enlargement. The same subset calculation adds at most

 C_c eta tau_c exp(a_c theta_hi)(|R|+|A|)

to the logarithmic moment. Thus the final commuting INPUT-DEFECT projectors in the toggling chart have local-stochastic parameter

 p0=exp[-theta_hi+theta_lo+eta A(theta_hi)],
 A(theta_hi)=C tau exp(a theta_hi)+C_c tau_c exp(a_c theta_hi).  (SR2)

No system-size prefactor appears. Bit phase errors need not be counted for the classical seed relation. Any nominal dynamics acting only on DATA/bath commutes this test. The same regularity/identity-annihilation assumptions as the accepted subset lemma apply.

## Parameter order and resources
After fixing n0 and the needed exponential seed-weight bound w_max, choose a desired p0 small enough that c0 p0 w_max is below the seed moment margin. Fix theta_lo (e.g.1), then choose theta_hi so exp(theta_lo-theta_hi) is below half that desired p0. This fixes tau and every circuit/noise constant. Finally choose eta so eta A(theta_hi) fits the remaining logarithmic margin. Raw exposure during the whole reset time is included in A, not ignored.

All times/degrees/body sizes are fixed independently of horizon. This proves an explicit fixed-parameter threshold statement; it does not label a fixed nominal reset floor O(eta). If one wants asymptotic eta^a scaling, the calibration schedule and its logarithmic factors must be specified separately. For the record-resource theorem, an arbitrarily small fixed effective seed parameter is sufficient if declared.

This is a source subset/initial-state lemma, not long retention, final readout, or coherent-pointer capture. It should be received together with the actual classical instrument convention and the later signed/quantum receiving map.
