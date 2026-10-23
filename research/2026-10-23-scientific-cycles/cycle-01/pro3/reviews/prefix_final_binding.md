# Final bounded reconciliation: prefix upper mechanism and joint-KL consequence

Reviewer: `/root/prefix_upper_challenge`. Date: 21 October 2026.

## Exact reviewed source

- Logical file: `PREFIX_THEOREM.md`
- Reviewed bytes: 22424
- SHA-256: `f12c59d2f411011a8038e9c725796159661181aa5c2950b7ac8bae70ee3af9fe`
- Result: **ACCEPT within the review scope below.** No mathematical blocking gap found.

This binding describes the exact file bytes read for this review. If the proof
file changes, the hash must be updated only after reconciliation of the actual
delta. It is not a hash-based substitute for checking the mathematics.

## Scope and division of work

Read the complete principal file for definitions and cross-references. The
bounded reconciliation specifically covers Sections 3, 4, 5 and 8, using the
previous detailed lemma review in `prefix_tail_challenge.md`. It does not
independently re-certify the matching forward-only lower construction,
equality endpoint, exact critical integer threshold, or growing-prefix
scaling in Sections 6 and 7; those have separate reviewers. No historical
priority or external acceptance is claimed.

## Checks

1. **Section 3:** The first-high-candidate reset identity is exact on arbitrary
   measurable spaces. The initial index zero case, empty sum at N=1, and final
   first-high summand all have the right indexing. The output-candidate union
   bound gives the measure inequality mu_N <= N q. Invariance propagates
   q_hi <= pi/h, giving precisely (3.3).

2. **Section 4.1:** Binomial unimodality supplies the pointwise bound eta_t,
   rather than 2 eta_t. The argument involves bounded observable iterates;
   it does not require an L2 initial density.

3. **Section 4.2:** The one-leg anchor retains its factor 1/2. With the centered
   indicator variance at most 1/4, the resulting weighted smoothing constant is
   1/[alpha s0 (2t+1)]. The core multiplier U_N=M(N^2 B+1)+N^2+R is valid.
   Using this same, possibly larger, Delta_N for the q-absolute core integral
   is harmless. Equation (4.5) includes the full high-tail q contribution a/R.

4. **Section 4.3:** For x in D, G(x,D)=b exactly. The normalized restricted
   kernel P_D is a Markov kernel when b>0. Bounded suprema/infima close the
   inequalities with denominator 1-alpha b, without assuming attained extrema.
   The b=0 case has zero low-set measure and needs no normalization. Actual
   bounded kernel versions suffice pointwise; equivalence and invariance also
   validate the almost-everywhere version. No null-set or disintegration gap
   was found.

5. **Section 4.4:** Both signs of the outside integral were checked. The terms
   mu_N on D and -pi on E combine as a convex combination, giving the maximum
   in (4.9). The residual measures -pi on D and mu_N on E cost at most b/B and
   N a/R. Thus no sign assumption about the density of the prefix law is used.
   All mass substitutions in the budget-only envelope are monotone, including
   the clamped upper bound on d.

6. **Section 5:** With fixed N and B=R=t/(log t)^4, h=B^(-1/2), every displayed
   remainder vanishes uniformly. Both low-set mass envelopes tend to b_K, so
   the upper floor is beta b_K^N/(1-alpha b_K). The proof keeps the class
   supremum throughout; it does not exchange a fixed-pair limit with a
   supremum. This checks the upper floor, not its separate matching lower.

7. **Section 8:** Reverse KL gives b_h=O_J(1/log t); the prefix estimate raises
   this to the Nth power. For every fixed N>=2, d=o(1/log t), and all other
   errors in (4.9) are also o(1/log t). The remaining high-weight target tail
   therefore gives coefficient K uniformly, and uniform inversion is valid.
   The referenced two-state family has reverse divergence at most
   -log(1-p), so it meets every fixed positive J for small epsilon; a fixed
   prefix leaves its inherited exponent unchanged. The one-global-update
   conclusion is supported and does not rely on the forward-only scaling
   theorem.

## Delta reconciliation and resolved clarity note

The exact source binding above was updated after four limited edits supplied
by the principal. The proof mathematics covered in Sections 3--5 and 8 is
unchanged, except that the budget-only certificate now explicitly states
`1/B < h < 1/2`. This resolves the earlier nonblocking clarity note about the
domain of the entropy envelope (2.2).

Section 9 now explicitly distinguishes a fixed number of mixture steps from
stopping after an exact number of global proposals. The new caveat is correct:
one cannot replace the latter random stopping time by its expectation in the
fixed-time theorem.

The added elementary certificate bound eta_t <= sqrt(2/(t+1)) is valid.
For c_k=binom(2k,k)/4^k, c_0^2=1 and
c_(k+1)^2/c_k^2=((2k+1)/(2k+2))^2 <= (k+1)/(k+2), since after clearing
positive denominators the difference is 3k+2 >= 0. Thus c_k^2 <= 1/(k+1).
For even t=2k this is at most 2/(t+1); for odd t=2k+1 the central
probability is c_k(2k+1)/(2k+2), whose square is at most 1/(k+1)=2/(t+1).
This proves the stated loose bound for all nonnegative integer t without
an asymptotic approximation.

Section 10 adds a primary-literature boundary for the next research question.
It does not enter the proved theorem. Historical novelty and verification of
that cited external theorem remain outside this review's assigned scope.

No additional diagnostics were run: the reconciliation concerned precise
proof obligations, and no discrepancy requiring a new calculation appeared.
The earlier exact-rational reset/tail diagnostic receipt remains unchanged.
