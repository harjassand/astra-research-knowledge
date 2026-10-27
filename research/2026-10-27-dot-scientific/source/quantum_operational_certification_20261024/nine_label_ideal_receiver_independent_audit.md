# Independent receipt: ideal nine-label noise-adapted receiver

27 October 2026. PASS for the ideal analysis only. Unknown projectors are analytical comparison objects; no source oracle or learned implementation is received here.

The code component of chi is sqrt(f)(I tensor VG)Phi; tracing B removes cross terms with its outside-code component. Thus chi_A=f(G²)^T/3+Kout, and TrKout<=1-f because TrG²>=3. The displayed norm estimate5.125t follows from||G-I||<=3t,||G||<=1.5. Weyl twirling gives frame operator3I_A tensor chi_B; its nonzero eigenvalues equal3 times those of chi_A, each repeated3. Hence the9x9 Gram deviation<=16t is correct.

The ordered rejection-product row identity is exact, and each row has norm<=1. Its perturbation from the single-label row is<=128t. Bell contraction divides the row norm bysqrt3; the known Weyl transpose correction removes the label's unitary and leaves the same sqrt(f)G/3 code map. Thus corrected sequential code Kraus deviation<=130t and norm<=1/sqrt3. Accepted-map errors sum to1170t, and the erased rejection effect costs at most the same, giving complete genuine-code error2340t. No normalized-only acceptance comparison is used.

For reset acceptance, the actual marginal tested by rows is I_A/3 tensor tau, even though the local Bell ancilla purifies its A factor. The triangular row recurrence applies to Hilbert-Schmidt amplitudes. Its strictly lower Gram matrix has norm<=Frobenius norm<=3||F-I||<=48t<=1/2, so total squared reset amplitudes are at most four times the single-row sum. Weyl rotations preserve reset expectations, yielding weighted acceptance<=30e and complete reset-versus-erasure error<=60e. Together with t<=5e/(3p), total error<=3960e<=19800epsilon_ent at target p identity+(1-p)erasure.

The e<=p/160 premise ensures t<=1/96. Constants are loose and need substantially smaller e for useful relative accuracy. This preserves the sufficient Delta~p² signal scale, but by itself proves no source-unknown cost, no reusable program and no full learned nine-label theorem. The weighted branch lemma and an explicit multi-label/resource assembly are still needed.
