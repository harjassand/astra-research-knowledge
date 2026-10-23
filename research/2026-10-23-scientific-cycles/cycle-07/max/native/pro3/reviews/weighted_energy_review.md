# Source-bound review of weighted boundary energy and the global upper

Reviewer: `/root/critical_budget`. Scientific date: 22 October 2026,
Australia/Brisbane. Complete source read; focused analytic challenge completed
at 2026-10-22 00:15:15 UTC (10:15:15 Australia/Brisbane).

## Reviewed source, decision and independence boundary

`GLOBAL_BOUNDARY_THEOREM.md`:

- Bytes: **21,990**.
- SHA256: **b381b6a052c309ea66716014820573040b6038ed83de0f19b112754d52233c3c**.

**Decision: accept Sections 2--6 and Appendix A without repair.** They prove
the general finite weighted energy inequality, the full-return finite TV
certificate and the all-class global-dominant critical upper in their stated
scope. No source amendment is required by this review.

The complete document was read to establish its dependencies and scope.
The independent contributor's one-crossing construction, full-law sandwich
and same-instance pure-IMH calculation in Sections 7--8 were **not assigned
for a duplicate source-bound challenge**. Their contributor proof and principal
acceptance remain distinct dependencies for the matching lower and Theorem 2.
The elementary Q=I lower is unchanged received capital.

This reviewer supplied the information-allocation reduction independently
before the principal's synthesis. Therefore the review independently challenges
the principal's new weighted operator and its incorporation of that reduction;
it does not describe the reviewer's own allocation contribution as independently
audited by this same reviewer. Principal acceptance of that contribution is
separately recorded. The earlier contributor source and receipt are unchanged.

This is internal mathematical acceptance. It establishes no historical
priority, external acceptance, formal machine verification, implementation
speedup or physical performance claim.

## 1. General finite lemma for arbitrary w>=1

The review independently recalculated the local, global and mixture bounds
for **any** finite w>=1, not only the later canonical choice. The proof kernel
retains actual A entries and kills only exits to B\E, without renormalization;
E absorbs. Its identity (6) is exactly the first-B-hit event, starting from
the restricted subprobability q1_A.

At p=1/(1-eta) and D=diag(q^eta), the equality
`v_x^p=q_x(mu_x/q_x)^p` follows from `p(1-eta)=1`. This ensures that the
counting local calculation and the q-density global calculation refer to the
same input p-energy.

### Local weighted Jensen

At theta=eta the transformed off-diagonal entries are directly bounded by
Q_xy. This holds for both directions of a q-ratio and for the actual second
acceptance factor. Each counting column has sum at most two. In particular,
a column in the absorbed set E has its new diagonal one plus incoming A
entries bounded by the corresponding Q column; no E-to-A term is retained.

Multiplying output-coordinate Jensen by omega_y in {1,w} gives weighted
row sums at most `L_xx+w sum_(y!=x)Q_xy<=1+w` on A, exactly w on E.
The step uses w>=1 and the actual rejection diagonal. It does not extend the
older scalar F(c) theorem past its hypotheses or infer contraction from
acceptance ordering. This proves equation (11) for arbitrary w>=1.

### Global weighted density Jensen

Every A-to-B independence proposal is accepted. Consequently the actual
G[A,A] row mass is b and G_yy<=b on A. The q-density column sums of G^E are
at most 2b on A and exactly 1+b on E. In the latter case, the absorbing row
contributes one and all incoming A proposal mass contributes b.

After weighted Jensen, multiplication by q_y omega_y and summation gives the
actual weighted output-row mass b+w e on A and w on E. This proves equation
(12). The q measure restricted to A union E need not be normalized; the proof
uses the actual column-weight sums, so no hidden normalization assumption or
minimum-q constant appears.

### Mixture and positive deficit

Convexity under the actual mixture weights gives A coefficient

`1/2+2^(p-1)/2 [1+beta w-alpha(1-b)+alpha w e]`.

The E coefficient, relative to its already weighted energy, is
`1/2+2^(p-1)/2`. Taking
`Delta_w=[beta w-alpha(1-b)]_+` bounds both by Gamma_w(e), independently of
the sign of beta w-alpha(1-b). Thus the arbitrary-weight statement is valid.
No boundedness of w is needed for this finite inequality; boundedness is
introduced only for the canonical asymptotic application.

The initial transformed energy is b. Weighted Holder on E divides its
energy by w before taking the 1/p power. The result is exactly
`(b/w)^(1-eta)e^eta Gamma_w(e)^(N(1-eta))`, with the exponent on w and
Gamma correct. Empty A/E is separately harmless.

## 2. Canonical boundary balance and small-b control

For `w=max(1,r_b)` the identity
`beta w-alpha(1-b)=[beta-alpha(1-b)]_+`
is exact. The boundary weight pays for excess global killing when r_b>=1;
when r_b<1, the deficit is explicitly charged. The proof never divides by
r_b-1 and therefore includes r_0=1 and its finite-cutoff excursion below one.

Weighted AM-GM supplies `x^(1-eta)<=(1-eta)x+eta<=x+eta` for x>=0;
applying it to x=b/w in [0,1], and using w>=r_b, proves equation (14)
uniformly as b tends to zero. There is no relative error divided by b.

Equation (15) follows because Gamma is at most
`2^(p-1)(1+Delta+alpha w e)`. Taking logarithms and using
`(p-1)/p=eta` gives precisely the exponent stated. This controls cumulative
growth at a growing first-hit horizon, rather than only one-step growth.

## 3. Complete finite TV certificate

The anchor is applied to each actual `C^(n-j)f` with its own scalar z_j.
The union set E includes every relevant j from zero through N, contains the
high-weight tail, and remains a subset of B. Chebyshev and the q high-tail
bound give equation (16), uniformly in f. The fact that E depends on f does
not alter the sampler or the first-hit lemma, which holds for every subset E.

The exact decomposition (19) retains the original C after every first hit.
Thus all later excursions and returns remain. Absorption is used only to
count first-hit locations. The good-hit term, initial bad mass q(E), absorbed
bad mass, stationary anchor comparison and residual mass are correctly
accounted for. The replacement e->bar e is valid because the hit bound is
increasing in e. This proves equation (17) for the stated integer horizons.

## 4. Uniform global-dominant tuning

At ell=log n and u=log ell+s+o(1), the selected parameters are admissible
for all sufficiently large n: h<1/2, R>e, eta<=1/2 and N<n. The canonical
weight is bounded by max(1,alpha/beta), a fixed number. The entropy bound on
q(B), together with r_0>=1, gives Delta=O(h log(1/h)), including equality
r_0=1. Constants depend only on the fixed parameters and the policy, not on
support, atom probabilities or Q.

The uncapped bar e is bounded below by a constant times n^-1 ell^4 and
above by a constant times n^-1 ell^4 u^5. Its cap 1-b is eventually inactive
because that quantity stays uniformly bounded away from zero. Hence
`log bar e=-ell+O(log ell)` and `bar e^eta=e^-u(1+o(1))` uniformly.

The accumulated errors are separately controlled:

- N eta=O(u^2/ell)->0.
- N Delta=O(u^-3 log u)->0.
- N bar e->0, with w bounded.

Equation (15) then gives Gamma_w(bar e)^(N/p)=1+o(1). The lower bound one
on this factor is immediate from Gamma_w>=1, so the equality notation is
justified. The ordinary smoothing, test and unhit-mass errors are O(ell^-2),
and the direct bar e term is o(ell^-1). The factor b/r_b is uniformly bounded
by the entropy bound on 1-b. These facts justify the uniform additive error
in equation (25), even when b is extremely small.

## 5. Budget incorporation and full-class maximization

Appendix A reproduces the received one-KL inequality correctly. The high-tail
entropy is bounded below by a log R. In the complementary term the actual
q mass is replaced by the larger 1-b in the direction lowering the bound.
The derivative in d=pi(A) is nonpositive on d<=hb whenever h+a<=1;
that hypothesis holds eventually uniformly under the selected cutoffs.
The b=0 endpoint is handled directly or by continuity.

The deterministic allowance delta_n in equation (26) is nonnegative for
the sufficiently large n under discussion, tends to zero, and implies
`k+ell a<=K+delta_n`. Thus the actual finite interval for k is
[0,K+delta_n]. The factor `b/r_b=(beta/alpha)(exp(k)-1)` is exact.
The function in equation (27) has second derivative C_n exp(k)>0, so its
maximum on this finite interval is one of the two displayed endpoints.
Uniformity permits taking the native class supremum directly in equation
(28), without assuming an attained supremum or a bounded support. No additional
KL budget is supplied to either term.

As stated above, this section verifies faithful incorporation of the
reviewer's original contribution; it is not a separate independent audit of
that contribution by its own author.

## 6. Appendix A and scope checks

The reciprocal MH factors give pi-reversibility, and the explicit lazy
mixture puts the spectrum in [0,1]. The anchor's Dirichlet-form restriction,
Jensen step and spectral constant combine to give 2/[alpha(2t+1)], as stated.
The entropy high-tail bound and low-weight binary bound have the stated
inequality directions. No initial L2 density or dimension condition is used.

The full source clearly fixes K,alpha and each run's kernel and screen. It
does not claim uniformity when alpha or r_0 changes with n. In particular the
agreement at r_0=1 is a fixed-parameter theorem and not an asserted double
limit. The finite weighted lemma has broader parameter scope than the critical
application, and those scopes are properly distinguished.

No assertion of practical speedup follows. The source preserves pure IMH,
full target enumeration when naturally available, caching and native evaluation
costs. The new upper is a robustness law under the exact stated information
contract; implementation and numerical errors remain separate.

## Resource and status record

No numerical jobs, matrix searches, simulations, external queries or historical
replays were performed for this source-bound review. The complete source read
returned at 00:13:44 UTC; final analytic inspection and identity verification
were recorded at 00:15:15 UTC. This observed 91-second interval is neither an
active-inference measurement nor a discovery-cost estimate. Total inference,
tokens, monetary cost and historical research costs are unknown.

The principal proof was not edited. Its exact hash above controls this review.
The prior contributor source and provisional algebraic checks remain preserved.
