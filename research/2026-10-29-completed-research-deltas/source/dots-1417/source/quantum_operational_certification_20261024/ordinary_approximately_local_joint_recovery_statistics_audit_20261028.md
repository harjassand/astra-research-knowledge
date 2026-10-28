# Approximately local joint recovery: full statistics and cap audit

28 October 2026. Independent analytic statistics review. Zero new source calls, simulations, count samples, or private source/seed reads. Received exact-local sources, pilots, and the separate fine-ERM derivation receipt are preserved unchanged.

This review covers the full manuscript `ordinary_approximately_local_joint_recovery_20261028.md`; the final source SHA256 is `1ae8d8f836d366268a4c8f182b9c8b679ba77aea9fde5ebe669e5e576ad74c4d`. Its independently received mathematical/control imports and every dependency hash are specified in the companion receipt. The mathematical coarse-localization and control arguments are received through the other independent reviews; this audit checks their statistical interfaces, finite budgets, bad-history handling and final comparator conclusion. It is not a count-acquired experiment or an empirical model-membership certificate.

## 1. Full statistical event structure

The theorem inherits integer domains 1<=q<=n, 1<=w<=n and 0<epsilon,gamma<=1, uses 0<kappa<=1 and supplied 0<=tau<=kappa/8, and needs strictly positive beta_L,beta_F,beta_T,beta_C with sum<=epsilon/8. All source calls independently reset. One linked whole-process operational discrepancy is nu<=epsilon/8; it is not reallocated independently per phase.

Let M=n-w+1 and R_max=min(M,2w-1). There are at most 2qM coarse density estimates. Their individual failure allowances beta_L/(2qM) yield a simultaneous event E_L with failure at most beta_L. The coarse root-deficit target m0=kappa^2/512, trace/numerical error budgets and supplied tail give the required fixed score gap: true proxy patch >=11kappa/16, every disjoint patch <=5kappa/16, threshold kappa/2. On E_L a first passing interval overlaps the proxy patch, so its expanded envelope contains that patch. This is overlap acquisition, not exact support identification.

The observable color-count guard is essential: if more than C=min(q,4W-2) colors are needed, the process stops with a fixed physical replacement and predetermined encoder. On E_L the received packing proof excludes this trigger. If no coarse patch passes, the inherited fixed replacement also applies. No guard is an empirical validation of tau or of source-family membership. Bad histories may terminate early but retain every executed call in their ledger.

Conditional on any preceding coarse history for which the chosen finite bank schedule is executed, each ONE fine sign-bank estimator has its required iid marginal. There are at most 4qR_max individual state estimates. Each has allowance beta_F/(4qR_max), so the simultaneous fine failure probability conditional on that prior history is at most beta_F. This remains true with correlations between different patches, logical labels, and plus/minus banks. It does not license a statement conditional on all eventual global records.

The antithetic construction uses exactly two real reset calls per pair, independently chosen anchors, and one fresh uniform sign vector and its negation. Own-sign routing gives exactly N_B copies to each individual bank. Every individual density-estimator instrument is fixed and separate until all estimates freeze, and uses only its own bank, own routing labels and own internal records. Other current signs, shared anchors, opposite-sign outcomes and peer outcomes are not inputs to that estimator's adaptive policy. Thus no sign-fill probability, rejection sampling, hidden register cloning, joint-product assertion or retrospective postselection is introduced.

After candidate CPTP maps freeze, tournament batches use fresh independent axes/signs per call, not antithetic pairs. Given the entire PAST batch history, a contender pair and its physical spectrum-valued measurement are fixed. Each own comparison has the received mean and variance bound; peers' current measurements may correlate but do not change its marginal. Conditional Bernstein failure per comparison is beta_T/[q(R_max-1)]. Union over at most q(R_max-1) executed comparisons costs beta_T, with no independence assumption across peers or bracket nodes. For R_max=1 there are no comparison calls or comparison parameters.

After the actual color-ordered joint receiver is frozen, the global encoder event E_C is conditioned on that frozen history and uses new actual source calls. Its failure allowance is beta_C. Ordinary globally entangled stabilizer inputs and a joint inverse-Clifford test, not products of marginal fidelities, give the true joint Bell-risk scalar for this fixed decoder. By the tower property and union bounds, the four bad-event allowances sum to at most beta_L+beta_F+beta_T+beta_C. Conditional validity is always used before the future data in question, not after conditioning on final success.

## 2. Fine ERM, tournament and finite signs

The full manuscript matches the independently bound new derivation `ordinary_approximate_locality_fine_erm_statistics_audit_20261028.md`. Crucially, local empirical optimality is compared to the feasible imperfect local D0, not the generally nonlocal exact ideal decoder. With r0<=11tau^2/4, four root deficits <=m and empirical gap zeta, the pointwise Uhlmann argument gives

    r <= r0+zeta+4sqrt[2m(r+r0)/kappa]+2m
      <=2r0+40m/kappa+2zeta.

For zeta<=m and m=kappa^2 eta/512 this gives r_min<=2r0+42m/kappa. The inherited tournament with t=kappa eta/(4h^2) produces

    r_selected<=11tau^2+(53/128)kappa eta,
    ell0_i<=22tau^2/kappa+(53/64)eta.

For R_max=1, the direct ERM gives the smaller bound ell0_i<=11tau^2/kappa+(21/128)eta; the displayed common bound is therefore valid without inventing t or dividing by h=0. All candidate channels remain CPTP on bad histories through the received finite rational Choi feasibility repair.

Known backward diagonalization error <=sqrt(eta)/2 and the weighted sign inequality give

    delta_ji<=440tau^2/kappa+25eta.

No source gauge floor, eigenvalue gap, compatible fitted Pauli algebra or independent learned-frame assumption appears. Finite known-matrix arithmetic certificates remain implementation requirements on every normalized estimated-state input, not extra statistical success assumptions.

The actual-only causal truncation and compatible ideal-subset hybrid are the necessary approximate-local replacements for the older exact-local proof. In particular, physically nonlocal ideal gates are NOT deleted using the actual spatial support cone. Received robust packing gives the conservative geometric constants C,K,A, and the full Bell-projector operator union yields

    ell0_joint<=1980qA tau^2/kappa+(225/2)qA eta.

No marginal-fidelity independence is used, and local CPTP fits are not sequentially deployed as joint decoders.

## 3. Every source-call multiplier and finite branch

With c=min(w,M), c1=min(w,R_max), and positive confidence allocations, the fixed bank sizes are

    N0=ceil[(80*4^w/m0)log(24*4^w qM/beta_L)],
    N_B=ceil[(80*4^w/m)log(48*4^w qR_max/beta_F)].

The log factors correspond respectively to 2qM and 4qR_max simultaneous density estimates. The exact raw-call multipliers are:

- Coarse: 2q c N0. Logical labels are acquired separately before supports are known; the factor q has not been discarded.
- Fine: 4C c1 N_B. There are two axes, two actual calls per antithetic pair, C envelope colors and c1 disjoint candidate-patch colors. Register reuse is only across disjoint physical patches of the SAME actual source output.
- Tournament: C(R_max-1)N_pair, with N_pair=ceil[2048h^2 L_T/(kappa^2 eta)] and L_T=log[2q(R_max-1)/beta_T]. Synchronized fixed bracket slots and disjoint envelopes permit this multiplier, not q(R_max-1). Empty slots trace unused registers. For R_max=1 this entire term is zero and h,t,L_T,N_pair are omitted.
- Fresh global encoder: the inherited deterministic N_count bound with scalar tolerance epsilon/8 and confidence beta_C.
- Payload: one additional q-input block call.

Consequently equation (16) counts all phases and the final payload. The observed-color guard ensures the stated fine/comparison cap even on statistical bad histories. Early termination can use fewer calls but cannot refund completed calls. The received global scalar design is rerun for this actual colored receiver; reordering incompatible learned swaps changes the channel, so older decoder data are not silently reused.

At fixed w, C,R_max,c1,A and 4^w have uniform q-independent upper bounds, so m^-1=O(q/(kappa^2 epsilon)) gives the claimed fine/comparison block-call scale, up to logarithms. This is not a claim of free qubit traffic: input uses qN_total, output exposures nN_total, up to 4qR_max local estimator instances, collective cross-copy memory, routing, actual receiver controls, input-state preparation and joint output readout remain paid. If w is chosen as a function of q or epsilon to reduce tau, its displayed exponential cost must be substituted before drawing a scaling conclusion.

## 4. Final relative comparator, approximation floor and bad histories

The separate global dominance promise and G(x)<=4Gbar transfer are retained. For the frozen acquired decoder, uniformly in the real encoder,

    ell(D E_x)-ell_star(x)
       <=F+(225/8192)epsilon,
    F=7920qA tau^2/kappa.

The fresh global stabilizer test has Bernoulli error [2^q/(2^q+1)] times the actual full Bell loss. The epsilon/8 scalar tolerance therefore gives Bell additive tolerance <=epsilon/4. The relative encoder guarantee multiplies the entire fixed-decoder comparator by (1+gamma), including F. On the total good event,

    ell_final <=(1+gamma)ell_star+(1+gamma)F
                +(1+gamma)(225/8192)epsilon+epsilon/4.

Using gamma<=1, bounded loss on exceptional histories, total statistical failure <=epsilon/8, and whole-process discrepancy <=epsilon/8 gives

    E ell_final <=(1+gamma)ell_star+(1+gamma)F
                  +(1/2+225/4096)epsilon
               <(1+gamma)ell_star+(1+gamma)F+3epsilon/5.

Thus the manuscript's weaker +epsilon conclusion is safe. The (1+gamma) factor on the approximation floor is present and necessary for this proof. The floor does not shrink with additional samples; the theorem neither learns nor validates the supplied structural tau bound. Clipping the final upper bound at1 is valid because loss is bounded by1, but does not strengthen the model contract.

## Result and scope

PASS for the full manuscript's statistical acquisition, conditional confidence, exact raw-call cap, canonical ERM/rounding constants and expected full-reference comparator, conditional on the stated source family and separately received coarse/control mathematics. The same construction is available to the strongest equally informed conventional learner. No generic unflagged-source theorem, empirical family certification, hardware execution, dimension-free untwirled diamond estimate, or quantum-over-classical separation is inferred.

## Received independent structural/control interfaces

The final source is also bound by `ordinary_approximately_local_joint_recovery_20261028_independent_receipt.json` (algebra/coarse proof) and `ordinary_approximately_local_joint_recovery_controls_receipt_20261028.json` (physical controls and packing). I read their full-source audits and reverified every manifest entry before binding this statistics receipt. Their exact rational prescribed-matrix evidence is not a source sample or acquisition simulation. My earlier fine-ERM derivation and receipt are retained byte-for-byte; the final manuscript uses exactly its canonical 512/old-t/440 budget.
