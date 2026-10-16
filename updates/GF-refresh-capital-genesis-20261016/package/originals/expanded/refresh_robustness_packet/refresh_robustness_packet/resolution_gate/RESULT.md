# A resolution gate for the exact Schur refresh optimizer

16 October 2026. Derived directly from the verified Schur variational formula; conditional mathematics, not a hardware certificate.

Let p,q in [0,1], Q=p+q-pq, h=sqrt(pq(1-p)(1-q)), and mu=max_j |c_j| for C=[[1,c†],[c,B]] positive semidefinite with unit diagonal. The exact endpoint value F satisfies

  L=Q+max(0,2h mu-pq) <= F <= U=min(1,Q+2h mu).

In particular U-L <= pq.

Proof: B is positive semidefinite, so the quadratic penalty is nonnegative. The complex l1 dual norm gives Re(c†z)<=mu. For a maximizing coordinate j, choose z_j=exp(i arg c_j), others zero. Its quadratic penalty is exactly pq because B_jj=1; z=0 gives zero improvement. The physical probability bound gives the upper cap. No smoothness, inversion, sector symmetry or conditioning assumptions are required.

For independent binary-generator dephasing with the full binary syndrome-label set present, mu=max_a |eta_a|, since every nonempty product of multipliers of magnitude at most one is bounded by the largest singleton multiplier. If some syndrome sectors are absent, max_a |eta_a| is still an upper bound on mu but need not be attained; that substitution then certifies the upper bound only, not the stated lower bound. Consequently, in the full-sector case this bracket costs O(m) arithmetic and O(1) working storage, even when the exact constrained QP has 2^m-1 variables. At requested absolute tolerance at least pq, no exponential sector enumeration is necessary. Directed rounding is additionally required for a floating-point certified implementation; the algebraic bracket itself is exact.

This does not supersede the exact optimizer when tighter tolerance matters or p,q are substantial. But it exposes a scientific priority issue: in the small-action regime p≈a²,q≈b², all information beyond the maximum good-to-bad coherence affects the bound by at most order a²b². Full inter-bad-sector tomography or a large optimization may resolve less than the hardware qualification uncertainty. A measured reduced coherence is still NOT the full-joint c required by this theorem.

Example p=q=1/10000, mu=1/4: h=9999/100000000. Then U=49997/200000000 and L=49995/200000000; width=1/100000000. Thus a full Schur optimizer can improve this cheap upper certificate by at most 1e-8 per parent in this example. This does not infer any actual experimental error rate.

For joint bounds product_i F_i, use product_i L_i and product_i U_i to quantify the actual decision resolution. Where L_i>0, the multiplicative enclosure is at most product_i(1+p_i q_i/L_i). Absolute per-parent smallness alone need not imply negligible relative error for an arbitrarily large selected set. Use log-domain or exact arithmetic and retain the endpoint full-input/lifecycle contracts.

No claim of historical novelty is made for this elementary optimization bound. Its value is a concrete computational stopping rule and a check against overinvesting in exact sector structure before physical qualification is accurate enough.
