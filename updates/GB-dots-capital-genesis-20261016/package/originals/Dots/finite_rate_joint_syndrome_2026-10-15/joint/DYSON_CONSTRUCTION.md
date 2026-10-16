# Joint endpoint dephasing bound: Dyson construction

2026-10-15. Construction record. The endpoint theorem has since been independently reconstructed in ../independent/INDEPENDENT_ENDPOINT_SUBSET_PROOF.md and by the block-norm proof in REPORT.md. This document preserves the original derivation route; it is not a separate unreviewed final claim. No novelty or memory-lifetime claim.

Let commuting parity involutions Z_i act on a finite joint memory/bath space. Let H=H_0+sum_i V_i with [H_0,Z_i]=0, {V_i,Z_i}=0, [V_i,Z_j]=0 for i != j, and ||V_i(t)|| <= J_i. Include independent exact Markov generators gamma_i(Ad Z_i-I). Start in a specified joint parity sector, with arbitrary correlated finite bath/reference. At deterministic time T, actually measure all selected parities. For selected S, all unselected V_j commute selected parities and may be absorbed into a baseline, with their dephasing realized by independent classical random unitary clocks. Conditioning those clocks leaves a unitary baseline commuting selected parities. No bound on its norm or bath dimension is required.

Construction: the actual CP effect for flipping every parity in S is at most product_i q_i(T) times the initial-sector projector, where
q_i(T) <= [exp(2 J_i^2 T/gamma_i)-1]/2.
One may replace individual q_i exceeding one by one by applying the theorem to the smaller selected subset. This is a joint probability/effect bound, not a claim of independent physical errors.

Proof route: use the exact independent telegraph toggling signs xi_i(t). In the H_0 interaction picture V_i remains odd only under Z_i and norm-bounded. Expand only selected interactions on the ket and bra. Endpoint projection requires odd occurrences of every selected label on each branch. For label i with total 2m insertions across both branches, its average telegraph moment, after arranging the insertion times u_1<...<u_2m, is exp[-2 gamma_i sum_{r=1}^m(u_2r-u_(2r-1))]. It is nonnegative. Initial sign may be fixed: total count even makes the interval before u_1 irrelevant. The bath operator product norm is at most product J_i^(2m_i), without interchanging any bath operators.

The separate ket/bra ordered domains merge into shuffles. For each label i, summing odd ket count a and odd bra count 2m-a gives sum_{a odd} binom(2m,a)=2^(2m-1). Summing all species interleavings produces the product of each label's ordered-time domains. This counting step is checked in the independent endpoint proof; it is not an assumption that physical propagators factorize.

The ordered positive kernel integral I_m(T) is bounded by T^m/[m!(2 gamma)^m]. Use x_r=u_(2r-1) and d_r=u_2r-u_(2r-1); drop the constraints x_(r+1)>=x_r+d_r, retaining 0<=x_1<=...<=x_m<=T and d_r>=0. The x-simplex volume is T^m/m!, and integrating all gaps independently gives (2 gamma)^(-m). Thus sum_{m>=1} 2^(2m-1) J^(2m) I_m <= (exp(2J^2 T/gamma)-1)/2.

The exact positive series with I_m retained equals, as independently reconstructed,
q_plus(T)={exp(-gamma T)[cosh(d T)+(gamma/d)sinh(d T)]-1}/2,
d=sqrt(gamma^2+4J^2),
by the scalar Volterra/second-order ODE. It is tighter than the exponential majorant and begins with (J^2/gamma)[T-(1-exp(-2gamma T))/(2gamma)]. An independent derivation obtains this through parity-block norm comparison; the two routes have now received independent endpoint reconstruction; see the proof-status record above.

Limits: one term flipping two selected parities violates the premise and defeats naive multiplication. Generic local noise must be grouped or colored before attempting application. Actual endpoint syndrome does not record intermediate coherent excursions, and zero final syndrome need not be a good memory branch. No common-decoder support predicate, spatial memory theorem, physical randomizer qualification, or novelty claim follows yet.
