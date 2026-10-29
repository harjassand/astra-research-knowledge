# Governing qualification to the remote seeded rate limit
2026-10-29. Independent review identified a missing asymptotic qualifier in Section7 of GOVERNING_INTEGRATED_THEOREM_v1.md. This addendum governs that limit; the frozen manuscript and finite budget examples are preserved.

The conditions t/B->0, r->0 and packing efficiency->1 alone do not imply that seed overhead vanishes. One must also choose the probe budget near its stated sufficient lower bound and control the requested seed-abort failure rate. Specifically choose

  P=ceil(max(4rJ,6 ln(1/delta_seed)))

(or an integer conservative implementation with P=O(rJ+log(1/delta_seed)+1)), and require

  log(1/delta_seed)=o(J).

Then P/J->0, so the probe cap and nP trusted-seed debit have vanishing normalized overhead. Fixed delta_seed or polynomially decreasing delta_seed meet this condition. Exponentially small delta_seed with exponent proportional toJ does not: its required seed reserve can remain linear inJ, and the asserted k0/n net-rate limit need not hold. Nor is that limit asserted if one deliberately chooses a much larger P than needed.

With these qualifications, fixedn,k0, t/B->0 and packing efficiency->1 imply

  (K-nP)/(n(J+P)) -> k0/n.

Every finite statement and the reported finite remote budget case remain unchanged. Vanishing total decoding error additionally requires choosing epsilon_fault and delta_seed to vanish while maintaining the displayed overhead conditions; the stated fixed-error rate examples do not by themselves prove a vanishing-error limit. For example polynomially small error targets and B growing with m fixed permit both conditions using r on order sqrt((m+log(1/epsilon_fault))/B).
