# Focused review: first-hit interface and uniform critical limit

Reviewer: heterogeneous_transport. Scientific date: 22 October 2026,
Australia/Brisbane. Source: `CRITICAL_ENDPOINT_THEOREM.md`, bound by the adjacent
receipt's exact byte count and SHA256. This is a new focused review of the
principal's endpoint argument. It is not a replay of the old lower theorem or
a duplicate audit of Section 3's local/independence energy algebra.

## Verdict

**ACCEPT in the assigned scope; no repair required.** The absorbed-boundary
process does not delete returns from the sampler law. The test-dependent bad
set is legitimate and has the stated uniform q-mass. The endpoint tuning and
single-budget subsequence split establish the claimed uniform limsup, provided
the finite absorbed-energy lemma has the separately reviewed validity stated
in Section 3. The unchanged lower then supplies the limit, at its exact scope
r0<1.

The entire source was read for hypotheses and dependencies. The detailed
checks below target Section 4 and Sections 6-7. Historical priority, formal
verification, practical speedup, and external acceptance are not inferred.

## 1. One union of test deviations is a valid deterministic set

For each fixed test 0<=f<=1, all functions `g_j=C^(n-j)f`, anchor scalars z_j,
and the set E in equation (16) are deterministic functions of the admitted
instance and the test. E is not selected from a realized chain history, so
there is no optional or adaptive selection hidden in Lemma 1's application.
A bound uniform over this f suffices when taking the supremum defining TV.

The common high-weight portion `{W>R}` is included only once. For each of the
N+1 remaining portions,

    sum_(h<=W<=R) q (g_j-z_j)^2
       <= (M/h+1) J,

because q=pi/W and `max(W,M)/W <= 1+M/h` on that band. Every `n-j>=n-N`, so
the same J applies. Chebyshev and a union bound therefore give

    q(E) <= a/R +(N+1)(M/h+1)J/d_test^2.

Since E is contained in B, its q-mass is also at most 1-b. This proves the
stated cap and entails no support-size constant or assumption about overlap.

## 2. Absorption counts a first hit, not subsequent evolution

On A, P^E retains exactly the original C probabilities into A union E; mass
entering B minus E is killed without renormalization. Rows in E are identity.
Therefore `(q 1_A)(P^E)^N(E)` is exactly the mass whose original first B hit
occurs by N and lands in E. An original path that first hits B minus E and
later returns to E is correctly not counted by this first-hit quantity.

That does not lose its effect on the sampler: in equation (17) the full
unnormalized first-hit measure nu_j, including the part in B minus E, is
propagated by the original `C^(n-j)`. Thus every post-hit excursion, return,
local/global transition and rejection is still included in g_j. The proof
uses two distinct processes for two distinct purposes and connects them by
an exact first-hit identity, rather than identifying their final laws.

The initial measure is q 1_A, not q conditioned on A. Its mass b remains in
the energy input and in the finite certificate. The time-zero boundary hit
is nu_0=q 1_B; its bad portion is charged separately by q(E). This avoids
both losing and double-counting initial B mass.

## 3. Finite test comparison and all error terms

For each first-hit time, stationarity gives pi(g_j)=pi(f). Subtracting the
anchor z_j therefore cancels the common scalar exactly when comparing
`nu_j(g_j)` with `nu_j(Omega) pi(f)`. The triangle bound has two parts:

- On the first-hit side, good boundary points contribute at most d_test in
  total, time-zero bad points at most q(E), and the remaining bad first-hit
  mass is exactly what Lemma 1 bounds.
- On the stationary side, `|g_j-z_j|<=1` on the high-weight tail gives a,
  and weighted Cauchy-Schwarz gives `sqrt((M+R)J)` elsewhere. Multiplication
  by nu_j(Omega) and summation does not add an N factor because the masses
  sum to at most one.

The residual subprobability has mass at most b rho^N. Its difference from
its equal-mass stationary comparison has TV at most that mass. The proof
is valid for each bounded test and its negative absolute difference, so it
bounds half-l1 TV with no missing factor two. Replacing e by bar e is valid:
e^theta and Gamma(e) are increasing, while the other quantities are fixed.

## 4. Endpoint tuning is genuinely uniform

At the specified policy u is asymptotic to log L/c*, so N=O(u). The band
parameter h=u^-4 gives a uniform positive q(B) floor through delta_h. The
non-cap expression for bar e is both bounded above by
`O(n^-1 L^4 u^5)` and bounded below by a positive constant times `n^-1 L^4`.
The lower bound comes from the deterministic Chebyshev allowance, even if
the actual high-weight mass a is zero. Thus the cap is eventually inactive
uniformly and

    log bar e = -L + O(log L)

has constants independent of the instance and its support. Multiplying its
error by theta=O(u/L) gives o(1). There is no unproved lower bound on the
actual E mass; only its deterministic overestimate is used.

With c=c*, the endpoint deficit obeys the stated
`Delta=O(h log(1/h))`. Hence the three accumulated quantities are uniformly
small:

    N theta = O(u^2/L),
    N Delta = O(u^-3 log u),
    N bar e = o(1).

The energy multiplier is allowed to exceed one; its N-step gain nevertheless
tends to one. This differs from asserting forbidden strict endpoint norm
contraction. The selected N also gives `b rho^N<=L^-2` once
q(B)>=exp(-K)/2. The stationary smoothing, test tolerance and q(E) allowance
are all o(1/L). Finally `sup_b |b^(1-theta)-b|=o(1)`, and the capture scale
is asymptotic to `L^-1 exp(-c*s)`. These facts justify equation (26) with
uniform remainders.

## 5. The single-budget split excludes a larger mixed amplitude

The allocation inequality supplies

    k_n+a_n log R <= K+o(u^-2),

uniformly, while k_n is bounded and nonnegative. Any sequence of instances
therefore has a subsequence with k_n tending to some k in [0,K].

If k<K, continuity and strict monotonicity of F permit a fixed c>c* with
`beta F(c)<alpha exp(-k)`. On this subsequence the actual killed mass makes
Delta zero eventually, and the same finite certificate gives a capture term
`O(L^(-c/c*))=o(1/L)`. The surviving tail coefficient is at most K-k.
This fixed c may depend on the subsequential k; that is sufficient for the
contradiction argument and is not claimed as one universal tuning for every
instance.

If k=K, the allocation inequality forces `a_n log R->0`, hence `L a_n->0`.
This remains true if k_n approaches K arbitrarily slowly, or from slightly
above K within its vanishing admissible remainder. The endpoint capture bound
then has coefficient b_K exp(-c*s). A sequence cannot retain a positive
leading ordinary-tail coefficient while also retaining the endpoint transport
exponent. No two budgets have been added.

The two cases imply the maximum envelope for every subsequential limit.
If a uniform class supremum violated it, choosing an instance within, for
example, 1/L^2 of that supremum and extracting a k_n subsequence produces a
contradiction. No supremum attainment, fixed support, common probability
space, monotonicity of eta_n, or optional-time substitution is needed.

## 6. Scope and resources

The proof is an exact-real theorem for finite positive instances, a fixed
reversible lazy mixture per run, proposal initialization, and one supplied
population forward-KL budget. It makes no claim for empirical KL estimates,
adaptation, deterministic composition, nonreversibility, numerical acceptance
error, or a disclosed full target table. The r0>=1 critical endpoint is not
silently included.

This was a source-based mathematical review; no numerical jobs, simulation,
external searches, or old-source replays were run. Exact source identity and
completion time are recorded in the adjacent JSON receipt. Active reasoning
cost, tokens and monetary cost are unknown. The review does not establish
historical originality or external acceptance.
