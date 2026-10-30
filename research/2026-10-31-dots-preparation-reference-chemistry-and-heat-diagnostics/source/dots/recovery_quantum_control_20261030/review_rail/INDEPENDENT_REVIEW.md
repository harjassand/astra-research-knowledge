# Independent local review: absorbing receiver rail V1/V2

30 October 2026. Verdict: **SCOPED PASS** for the explicit finite physical transfer, its canonical factorization, source-only done-sector firewall, full-state V2 completion witness, and the stated bounded-noise moment hierarchy. This does not certify an encoded handoff, late acquisition, arbitrary-strength source-noise composition, an output stopping instrument or universal computation.

## Exact reviewed files

- ABSORBING_RECEIVER_RAIL.md: 239e3e2a493cd8ddd08e76dbad0ae5b53c5d22e99ac1dba3fb65d03d65443aba
- ABSORBING_RECEIVER_RAIL_V2.md (including unloaded-bank failure section 5): 11ba8ca5bd583e936b8706acb0501d6f3c058e2ab980f3a4df1f0b83bbed11ab
- check_absorbing_rail.py: 1dbd40825c113320d31818e5666657899bc747504a6d6c0fe8d9871a0eb19fd3

## Independent reconstruction

I rebuilt the 18-state basis map in a different gauge ordering. Every physical basis state occurs once. Both physical H and the receiver-only coherent J match I_logical tensor their declared gauge operators, including V2's four extra physical matrix elements. The new H terms are genuine A/B two-site couplings, and J is genuinely receiver-onsite. The allowed physical model must retain these arbitrary finite-level coefficients or explicitly compile them; elementary-qubit locality is not shown.

The jump MUST be a single coherent logical-label-preserving retirement. Splitting it into logical-label-resolved jumps destroys entanglement. An independent reference/Bell diagnostic gives fidelity 1 for the coherent retirement and 1/2 for the resolved alternative. This is a real physical hypothesis, not an optional representation choice.

For V1, admitted source/vacuum loading identifies the actual unknown A qubit with the canonical logical factor and gauge s. Other canonical sectors need not identify A as logical. V2 preserves this nominal source trajectory while adding two additional u/e/d chains.

## Gramian and all-state completion

The stated 2x2 positive R satisfies i[H_a,R]-(kappa/2){P_e,R}=-I. Placing it on all three V2 active pairs gives L*R_all=-B_active exactly on the entire gauge Hilbert space. The coherent jump between three chains creates no missing cross term: R_all vanishes on its output, and J*J is kappa times the excited-sector projection.

Thus A=R_all/||R|| obeys a0 B_active<=A<=B_active and L*A=-r B_active<=-r A. This proves the full-state nominal output-location tail, reference-stably. It is not a provenance or fidelity statement from arbitrary startup.

## Noisy inclusion moment: factors checked

For m=|S| and M_S=product A_i, nominal drift is at most -rm M_S. A local HP perturbation term touching K subset S contributes at most its cb norm times M_(S\K); identity annihilation makes the K-empty term zero. The common bath does not invalidate pulling out untouched system-gauge factors.

Let f_S=Tr(rho M_S). The upper hierarchy is

    f'_S <= -rm f_S + sum_(Z intersects S) eta_Z f_(S\Z).

Inductively f_(S\Z)<=p^(m-|K|)<=p^(m-q) because 0<p<=1 and |K|<=q. The incident sum is at most m eta. Hence p'=-rp+eta p^(1-q) supplies the supersolution p^m with p(0)=1; its stated solution is correct. No factor q or factor 2 is missing when eta denotes the stated JOINT cb-norm budget. If eta is instead a raw Lindblad jump rate, that conversion must be paid, as the false-done example explicitly does.

Commuting product operator order gives product B_active,i <= a0^(-m) M_S, proving the advertised inclusion bound. It is useful only after its right side drops below one. Choosing finite dwell and eta after fixing physical constants is legitimate; no practical threshold estimate follows.

For the killed-state extension, the required premise is that the actual killed projection P commutes all gauge tests. Writing Q=I-P and using complete positivity of the full generator gives

    P L*(P M P) P <= P L*(M) P

because the omitted P L*(Q M Q) P is positive for M>=0 commuting P. The Hamiltonian contributes zero to this omitted compressed cross term, while jump gains are positive. Thus the full-loss killed generator inherits the full-generator drift upper bound. This does not permit an unverified actual composed memory projection to be assumed gauge-independent.

## Exact firewall and startup failures

All declared H terms and J annihilate the full B-done subspace. Every source-only operation preserves it and acts only on the A gauge there. Arbitrary source/environment CPTP dynamics therefore cannot change the done B marginal without a later B interaction. The statement remains true for pre-existing source/B/environment correlations by no-signalling. B-touching noise and reopened-transfer intervals retain their own actual budget; arbitrary strong source dynamics are not covered during those intervals.

V2's empty-pair failure is correct: physical |v,v> is logical 0/gauge f0 and undergoes nominal relaxation toward |0,d0>. Thus late arrival cannot be inferred from full-state completion. V1 instead leaves the empty pair stationary, but the receiver-local poison jump fills false done with exact probability 1-exp(-epsilon T). Its generator cb norm is at most 2 epsilon. An eventually arriving unknown source is then rejected by the same exact absorbing rail. These failures are preserved, not repaired by canonical factorization.

## Checks and boundaries

The supplied executable replay passes. Independent reconstruction residuals are zero for V, H, J and dark-rail identities; full Gramian residual is 1.02e-15 at independently chosen Omega=1.7, kappa=0.9. R eigenvalues are positive, approximately 1.96447 and 2.55783. Full data are in check_independent.json and source_replay.json.

The review covers this local primitive and conditional moment calculation only. A real canonical memory composition, physical loading immediately before unknown-state exposure, endpoint correctable-span proof, controller/prefix safety, and late requested handoff remain absent. Full-state output-location concentration must not be reported as arbitrary-start input acquisition or an already autonomous computing architecture.
