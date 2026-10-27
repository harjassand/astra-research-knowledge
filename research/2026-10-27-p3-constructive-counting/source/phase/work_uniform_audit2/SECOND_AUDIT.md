# Second audit of the growing-width construction

27 October 2026. Independently checked against the locally supplied pinned PDF text, especially Lemmas 4.7, 5.2, A.1--A.3, Proposition 5.3 and Appendix B.

## Findings

I found no fatal gap in `work_prior_agent/growing_width_exact_counting.md` in its stated parameter range. This finding is conditional on the governing manuscript. It is not a new verification of every lemma in that manuscript, nor a historical-priority or practical-performance claim.

The squared-factorial thresholds preserve Appendix A's insertion argument. Lemma A.2 uses only the threshold indexed by the residual width and the two branching priorities; it does not require geometric multiplicativity. The recurrence with theta_j=M^j(j!)^2 is therefore legitimate. Separating the i=1 term gives the stated normalized bound 8+32 sum_{b=1}^{j-2} binom(j-1,b)^(-2)<=16. Each B-branch inserts enough new, immediately surviving petals; the original antichain proof is unchanged. Thus the total B-choice bound 32N/M and the explicit depth constant are sound.

The proposed implementation avoids the source's optional universe of all n^k clauses. It need only store current clauses and enumerate their own subsets. The dynamic number of stored clauses is bounded by the input count plus the insertion count; the universal polynomial-space guard covers this quantity. I checked that all constant-one neutral factors can be included without raising the degree budget.

The Section 6 preprocessing bounds do not conceal a disastrous exponential dependence on k. The shift enumeration is exponential in D_0 log m; the local matrix enumeration is exponential in O(D_0^2/B+D_0); the tested words add at most O(D_0) to this exponent. Greedy row candidates add a factor (2m)^P, hence an additive O(P log m) exponent. The actual polynomial-system scopes have size at most kD_0, rather than 2^kD_0. Their lists have the latter harmless subpolynomial expansion factor in the claimed range.

Lemma 4.7 has universal polynomial complexity in its explicit incidence, scope, and array-size parameters. The proposed tail certificate is valid for the actual Bin(Q,(r-1)/(2r)) law: R>=32 and 6R<=Q justify the centered interval, and R^2>=8QA gives the required tail. Since k nu=O(lambda^(1/3) nu^(2/3))=o(lambda) uniformly over k^3 nu/lambda<=1/16, the size guards eventually pass uniformly. R/Q tends to zero uniformly, even when a=k^3 nu/lambda remains a positive constant, because k increases while the ratio before multiplication by k decreases. If a tends to zero, the correction order divided by N also tends to zero.

Proposition 5.3 and Appendix B expose the exact arithmetic dependence, including log Omega=O(k m_test ell Q log(Q+2)). Their polynomial exponents do not depend on k. The shared V-order truncation gives d=k(m_test+2(ell-1)); treating each factor as having an independent truncation budget would be wrong, but the proposed construction does not do that. The entropy multiplier in log C_q is necessary and is included.

The long-clause split is disjoint and its path bound is correct. A short clause never becomes long under simplification. The number of A-steps is bounded by the initial number of long clauses, and B-steps fix k new free variables. Retaining all original declared variables with unit clauses at leaves is the right way to apply the uniform width theorem without accidentally changing its width-versus-input-size condition.

## What the audit changed

The growing-width theorem is not the strongest route to the dense AND/OR-circuit consequence. Its k^3 term combines a degree factor k with a tail parameter whose log incidence is O(k log log n), caused by sparsifying every k-clause together.

For the circuit encoding, only the few reverse-gate clauses are long; all arbitrarily numerous forward implications are binary. Compiling the binary part alone and attaching the remaining clause incidences as ordinary tensor ports avoids growing-k sparsification entirely. The complete construction and costs are in `HYBRID_DENSE_CIRCUIT_BOUND.md`. It yields the sharper explicit bound

    poly(L+N) 2^[O(N sqrt(log log N)/(log N)^(1/4))],  N=n+g.

The qualitative dense-linear-gate result remains a routine consequence of the source. Neither theorem resolves the arbitrary-many-internal-states obstruction, and neither accompanied program is a practical implementation of the source's asymptotic contraction algorithm.
