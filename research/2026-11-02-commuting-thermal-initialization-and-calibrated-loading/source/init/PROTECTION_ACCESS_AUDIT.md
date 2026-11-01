# Protection/access bound: independent algebraic receipt

2026-11-01. **PASS**, with the minor precision notes below. This is an elementary access-versus-protection inequality, not a loading impossibility theorem or novelty claim.

## Hamiltonian statement

For every admitted term H_X on memory plus arbitrary input/controller/bath degrees of freedom, protection of the ENTIRE operator algebra on its memory footprint implies [Q,H_X]P_good=0. Expanding in a memory operator basis proves this even with arbitrary external operator coefficients; no classical-control or product-state assumption is needed. H_X is Hermitian, so the commutator is anti-Hermitian and also vanishes on the other side. Therefore i[H_X,Q]=P_bad i[H_X,Q]P_bad, and its norm is at most 2||H_X||.

Summing actual term norms, rather than norms of an unnecessarily expanded external-coefficient representation, gives

    |d<Q>/dt| <= 2 sum_X ||H_X(t)|| p_bad(t)
               <= 2 n h(t) p_bad(t).

Terms acting solely outside memory commute with Q and contribute zero. The state can be arbitrarily correlated with controllers or reference. Bounded local strength is a bound on actual interaction norms: an external controller with an unbounded operator coefficient is not permitted unless its resulting term norm satisfies that bound. Norms may include the passive Hamiltonian; terms commuting identically with Q may be omitted.

## Dissipator caveat

The additional 2n gamma(t) bound is valid if every Heisenberg dissipator contribution D_J^*(Q) is bad-supported on BOTH sides. Its norm is at most 2||J||^2. The root explicitly demands this full logical correctability, which is sufficient. Merely asserting [Q,J]P_good=0 is not a substitute: the J†QJ and anticommutator terms require the complete condition. The Hamiltonian result alone suffices for the current exact-autonomous storage model and coherent control question.

## Integrated access and collision budget

Use Delta=|<Q>_tau-<Q>_0| and A=integral_0^tau(h+gamma)dt. Integration gives

    Delta <= 2n A ess_sup_t p_bad(t).

If a separately established comparison gives p_bad(t)<=sqrt(K(t) r_n) throughout the write, then

    ess_sup_t K(t) >= Delta^2/(4n^2 A^2 r_n).

For Delta bounded below by a positive constant, A polynomial in n and r_n=poly(n) exp(-c n^eta), this forces log ess_sup K >= c n^eta-O(log n). Thus a polynomial-action write cannot remain in a log K=o(n^eta) admission region throughout its path. “Essential supremum” is the precise version of “max” for merely measurable controls; continuous finite circuits can use max.

In the earlier second-moment result, K is measured relative to a specified comparison state. During driven loading one must NOT assume the driven comparison state remains thermal or has small bad population. The root avoids this mistake by explicitly making p_bad<=sqrt(K r_n) a hypothesis. One valid fixed comparison is the original logical-twirled Gibbs state sigma: Tr(P_bad sigma)=p exactly since P_bad commutes with the logical twirl. Then K(t)=Tr[omega_MB(t) sigma^(-1) omega_MB(t)] directly gives p_bad(t)<=sqrt(K(t)p), without stationarity of the driven state. Another admissible comparison is the idle-evolved twirl with its already-proved small bad population. The metric and comparison must be stated consistently.

The nonzero-Delta qualification matters. A particular write may leave the expectation of one chosen Q unchanged. Universal logical overwrite nevertheless includes inputs requiring order-one change for at least one Pauli, starting for example from near-maximally-mixed equilibrium logical data. The bound is not a statement that every gate or every input must change every logical expectation.

## Scope

The conclusion constrains the PATH, not its endpoint. It allows transient population in the decoder-bad sector followed by a demonstrated coherent and fault-tolerant return to an admissible endpoint. It also allows changed protected algebras, code deformation, charged cooling/reset resources or interactions outside the original footprint class. It supplies no lower bound ruling out polynomial-time loading followed by recovery, and no historical priority claim.

The constructive endpoint problem remains exactly as stated: preserve arbitrary input-reference coherence through the transient AND prove a post-loading storage admission condition. No further research or scope expansion was performed in this receipt.
