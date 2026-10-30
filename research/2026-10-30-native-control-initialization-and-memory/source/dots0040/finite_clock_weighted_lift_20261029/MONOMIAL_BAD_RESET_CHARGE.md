# Raw bad-reset charge from the already proved animal lemma
2026-10-30. Applies to the explicit monomial SIMPLE guarded compiler, not arbitrary transactional prefix instruments.

Use the explicit controlled-syndrome-XOR/controlled-Pauli gauge in MONOTONE_COMPILER_FLAGS.md. In every fixed joint syndrome/auxiliary-label sector, a normalized physical reset has one possible reset label and maps to one joint syndrome/label sector, up to a unitary within the syndrome degeneracy. It therefore acts deterministically on the commuting syndrome/bad-flag algebra. The adjoint preserves that algebra exactly; there are no raw good/bad or bad/bad off-diagonal blocks to pinching-bound.

Let k_reset bound the number of DATA syndrome bits changed by any gauged reset, including the bounded neighboring frame changes when an illegal occupancy is cleared. This is a fixed full-footprint bound, not necessarily the ordinary SSF changed-check bound. Add R identical unary occupied tokens for each C_h, with R>k_reset. A bad-source reset at h:
- removes all R h-tokens, because its own auxiliary becomes ready;
- creates NO bad flags or their tokens;
- changes at most k_reset syndrome bits;
- changes at most a fixed number D_flag of flag bundles.
Hence its actual occupied-vertex flip set D has
removed-minus-added >=R-k_reset>0,
|D|<=R D_flag+k_reset.
Make every possible such bounded reset footprint a clique in the fixed augmented graph. Thus every bad-source reset satisfies the original full-animal monotonicity lemma with
beta_bad=(R-k_reset)/(R D_flag+k_reset)>0.
Choose the animal c,theta for beta=min(beta_SSF,beta_bad) and the enlarged geometry. On every bad-source diagonal sector,
V_ext(pre)-V_ext(post)>=c0 sum_{B connected, D subset B}f_B(pre).

For the surgery argument one wants a charge to ALL animals containing the h-token bundle, not just those containing the full D. Given such an animal A, complete B=A union D. It is connected because A already contains h-tokens and D is a clique containing them. At most |D| vertices are added, so
f_B/f_A>=theta^{(1-c)|D|},
and there are at most 2^{|D|} source A per target B. Consequently
D_h^bad>=c_bad C_h sum_{A connected, all h-tokens subset A}f_A,
with c_bad>0 uniform over the finitely many local source patterns and independent of volume. This proves raw input (A) for the local-surgery reduction, provided the stated exact monomial gauge/no-new-flag identities have been verified.

No independence of identical token copies, stochastic Pauli approximation, pinching factor, or assumed classical dirty trajectory is used. The diagonal deterministic description is an exact algebraic consequence of the specifically engineered monomial completion.
