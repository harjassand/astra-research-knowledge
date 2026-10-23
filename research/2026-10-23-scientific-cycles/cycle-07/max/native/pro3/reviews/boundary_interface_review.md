# Focused boundary review: full returns, uniform endpoint, one budget

Reviewer: `/root/heterogeneous_transport`. Scientific date: 22 October 2026,
Australia/Brisbane. Exact source identity is in the adjacent receipt.

## Verdict and independence scope

**ACCEPT Sections 4-6 and their interfaces without repair.** The finite
first-hit certificate preserves all post-hit returns, the limiting argument
is uniform at r0=1 and when b tends to zero, and the convex maximum follows
from the same single KL budget used by the transport estimate.

I read the entire principal source for hypotheses and notation. Section 2's
weighted energy algebra is the other reviewer's distinct focused obligation;
the interface assessment below takes its stated finite Lemma 3 as its input.
I inspected Sections 2-3 enough to verify the forms consumed by Sections 4-6,
especially the canonical weight and the additive small-b control.

I am the author of the separate one-crossing lower. My comparison of Section 7
and its corresponding same-instance formulas with that source is explicitly
**a transcription check, not an independent audit of my own lower**. The
principal's acceptance and any separate review of that construction must remain
separate statuses. No old interior proof or old ordinary lower was re-audited.

## 1. The full-chain interface is exact

For fixed 0<=f<=1, g_j=C^(n-j)f, z_j and the union E in Section 4 are all
deterministic functions of the instance and f. In particular E is not chosen
from a realized trajectory. Lemma 3 is valid for any such E; a bound uniform
in f can then be used for the TV supremum.

The common high-weight set is charged once by a/R. For each of the N+1 band
deviation sets, q=pi/W and max(W,M)/W<=M/h+1 imply the Chebyshev charge
`(M/h+1)J/d_test^2`. The selected J applies to every n-j>=n-N. Thus q(E)<=bar e
without a support-size factor, and E is indeed contained in B.

The proof chain P^E counts the first B hit only. Original paths first entering
B minus E are killed in this counter and cannot later add to its E mass.
That is exactly the event in equation (6), rather than an approximation to
the final sampler law. In equation (19), by contrast, every unnormalized
first-hit measure nu_j is propagated by the full original C^(n-j). Therefore
paths that later leave B, re-enter A, return to E, or make arbitrary local and
global excursions remain in the actual test expectation g_j. No conditional
first-hit law is substituted for the original unnormalized subprobability.

Time-zero B mass is nu_0=q 1_B. Its bad part costs q(E), while the bad mass
that begins in A is exactly the absorbed quantity. These two terms do not
overlap. On the good first-hit portion |g_j-z_j|<=d_test. The total first-hit
mass is at most one, so neither this charge nor the stationary comparison
acquires an extra factor N.

Stationarity gives pi(g_j)=pi(f), allowing each anchor scalar z_j to cancel.
The high tail contributes at most a to pi|g_j-z_j| because g_j,z_j lie in
[0,1]; the rest contributes sqrt((M+R)J) by weighted Cauchy-Schwarz. The
remaining unhit subprobability differs from its equal-mass stationary measure
by TV at most b rho^N. The bounded-test argument therefore gives the stated
half-l1 TV certificate with no missing factor two.

Replacing q(E) by bar e in the absorbed term is legitimate: e^eta and
Gamma_w(e) are increasing, and w is fixed from b rather than selected by the
realized trajectory. The entire auxiliary construction remains a verifier
bound, not a sampler with an uncharged target oracle.

## 2. The boundary r0=1 is included with controlled errors

The canonical choice w=max(1,r_b) keeps w bounded by max(1,alpha/beta), and
r_b=alpha(1-b)/beta is bounded away from zero by the entropy lower bound on
q(B). Thus b/r_b is finite uniformly over the native class.

At r0=1, finite h does permit r_b slightly below one. The proof does not
silently replace it by one or divide by r_b-1. It chooses w=1 in that case and
charges the actual deficit

    Delta=[beta-alpha(1-b)]_+
          <=alpha[e^-K-exp(-k_h)]_+
          =O(h log(1/h)).

For r0>1 this upper bound remains valid (and the deficit is eventually zero).
Since N=O(u) and h=u^-4, its accumulated contribution is
`N Delta=O(u^-3 log u)->0`. The argument therefore covers the equality case
without appealing to a uniform limit of strict r0>1 proofs.

The finite bound on Gamma_w is also strong enough after iteration. Indeed
Gamma_w is at most 2^(p-1)(1+Delta+alpha w e), and
`(p-1)/p=eta`, yielding equation (15). With the selected parameters,
N eta, N Delta and N w bar e all tend to zero uniformly. Gamma_w may exceed
one; the statement actually needed and proved is that its accumulated power
is 1+o(1).

## 3. Small b causes no hidden relative-error problem

For x in [0,1], weighted AM-GM gives
`x^(1-eta)<=x+eta`. Applying this to x=b/w and using w>=r_b yields

    (b/w)^(1-eta)<=b/r_b+eta.

This is an additive uniform estimate, valid at b=0, not an expansion involving
eta log b or division by b. Empty A makes the exact absorbed mass zero. The
added eta, multiplied by the critical transport scale and then by log n,
vanishes because eta->0 and `(log n) exp(-u)->exp(-s)`. Hence the finite-energy
factor cannot hide a nonvanishing amplitude in sequences with b tending to
zero or with extremely small positive b.

## 4. The cutoffs and error estimates are support-uniform

The deterministic Chebyshev allowance ensures the non-cap expression for
bar e is bounded below by a positive constant times `n^-1 ell^4`, even if the
actual high-weight tail or actual E is empty. Its upper bound is
`O(n^-1 ell^4 u^5)`. Meanwhile 1-b is bounded below by exp(-k_h), tending to
the fixed positive e^-K. Thus the cap is uniformly inactive eventually and

    log bar e=-ell+O(log ell),
    bar e^eta=exp(-u)(1+o(1))

hold uniformly in finite support, pi, q, and Q. This does not assert a lower
bound on q(E); only its deterministic allowance is bounded below.

The smoothing term and test tolerance are O(ell^-2); bar e is o(ell^-1).
The fixed coefficient in N makes b rho^N=O(ell^-2). Combining these controls
with the weighted-energy estimate gives equation (25) with a uniform remainder.
The factor b/r_b is uniformly bounded, so multiplying its term by the uniform
1+o(1) growth and bad-set factors remains legitimate. The policy u is common
to every instance at the same horizon, not estimated from each run.

## 5. The maximum uses the actual finite single-budget interval

Equation (21), the individual bounds a<=a_max and k<=k_h, and
`ell-log R=4 log ell` imply the deterministic finite inequality

    k+ell a <= K+delta_n.

The allowance delta_n in equation (26) is nonnegative for the selected large-n
parameters and tends to zero. Since a>=0, the actual k belongs to
[0,K+delta_n]. This is not an assumption of two separately attainable KL
budgets.

Multiplying the transport estimate by ell produces

    ell TV <= K+delta_n-k+C_n(e^k-1)+o(1),
    C_n=(beta/alpha)ell exp(-u)>0.

The displayed deterministic function has second derivative C_n e^k>0. Its
maximum on the full finite interval is therefore exactly at an endpoint:
K+delta_n at zero, or C_n(exp(K+delta_n)-1) at the other endpoint. The result
is pointwise in every admitted instance with a common uniform remainder, so
one can take the class supremum before the limit. No supremum attainment,
fixed support, subsequence allocation assumption, or stability of an optimizer
is needed. Mixed information allocations cannot exceed the maximum.

This argument also covers k tending to zero or K at arbitrary rates. It does
not depend on an unproved strict separation of transport and ordinary-tail
regimes. The final limit of C_n is (beta/alpha)exp(-s), giving precisely the
claimed global-dominant upper envelope.

## 6. Lower transcription and scope checks

The source's Section 7 faithfully reproduces the contributor's three-state
q,pi,Q, per-state screen sigma, reverse acceptance sigma/n^2, exact global
matrix, root competition rates, leaf escape, finite lower/upper sandwich,
and amplitude. The same-instance IMH bounds in Section 8 also match that
source. This is a transcription statement only, as explained above.

The theorem keeps K,alpha fixed, starts from q, and keeps eta,Q fixed within
each run. It does not introduce adaptation, deterministic composition,
nonreversibility, empirical-KL certification, a free target normalizer or
finite-precision validity. Agreement at r0=1 does not imply a uniform double
limit in r0,n, and the source correctly declines that extra claim.

## 7. Review resources and status

This focused review used source reading and mathematical checking only. No
numerical jobs, old-source replays, external searches, spending, or outreach
were performed. Exact source/review hashes and an observed completion time
are in the JSON receipt. Active inference time, tokens, monetary cost and
historical discovery totals are unknown. This review is internal evidence of
correctness at its stated scope, not historical originality, formal proof
verification, practical speedup, or external acceptance.
