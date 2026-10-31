# Prior matching, comparable methods, and what is actually new here

This note belongs to the separate feedback checkpoint, not the earlier frozen
large-acquisition receipt. No historical novelty claim is made.

## Established ingredients, not new capabilities by renaming

1. Finite-horizon Bellman dynamic programming is the ordinary reduced-MDP
   planner. Any retained community/spectral/Krylov/range method supplied with
   this acquired operator certificate and coarse actions obtains the same
   planning capability. Giving it the certificate does not erase a possible
   contribution of the certificate's assembly; it rules out an exclusive
   planner advantage. Exact prior matching of the assembled statistical,
   mixed-norm, finite-bit receiving construction remains unresolved.
2. Block operator norms dominating block-vector norms are classical. See
   Feingold and Varga (1962), *Block Diagonally Dominant Matrices and
   Generalizations of the Gerschgorin Circle Theorem*, equations (2.3),
   (2.8') and the proof of Theorem 1:
   https://msp.org/pjm/1962/12-4/pjm-v12-n4-p08-s.pdf .
   Their displayed theorem concerns nonsingularity/eigenvalue inclusion, not
   this exact feedback certificate. The elementary inequality we use is
   proved in BLOCK_COMPARISON_PROOF.md; it is not claimed as a new norm theorem.
3. Collision-based L2 closeness testing already supplies the characteristic
   square-root-domain acquisition rate. Diakonikolas, Gouleakis, Peebles and
   Price (2016), Theorem 8, distinguishes L2 distances at most eta/2 and at
   least eta using O(sqrt(b)/eta²) samples from each law when both squared
   L2 norms are at most b, with constant success probability:
   https://arxiv.org/pdf/1611.03579 . Ordinary independent amplification
   supplies a logarithmic failure-probability factor. Thus a sqrt(n) sample
   exponent by itself is NOT new learning theory.
4. The underlying stochastic reduction/state-aggregation literature and
   matrix/probe/empirical-Bernstein ingredients are identified in the accepted
   parent-directory LARGE_PRIOR_AND_LIMITS.md and its source dependencies.
   We do not infer novelty merely because one source does not state all
   components together. Vantilborgh's 1985 paper titled *Aggregation with an
   Error O(eps²)* remains a relevant unread full-text lead (publisher access
   returned 403); no theorem-level equivalence or difference is asserted.

## Explicit reduction of the leakage rate to prior L2 tests

These are elementary reductions developed here, not claims that the cited
paper discusses this particular aggregation interface. For an outgoing
pooled row p=(WA_a)[g,:], let q=Pp (with vectors oriented consistently).
Sample q by drawing p then uniformly relabelling the destination inside its
acquired block. Independent p/q samples each cost an ordinary source draw
plus paid known relabelling. If p_max<=kappa/n, both squared L2 norms are at
most kappa/n, and the desired scaled residual n||p-q||2²<=theta² corresponds
to eta=theta/sqrt(n). The prior theorem gives
O(sqrt(kappa*n)/theta²) samples, up to confidence amplification, for a gapped
admission. This matches the dimension-rate of the quadratic outgoing test.

For incoming block probabilities R_ih, sample joint p(i,h)=R_ih/n by choosing
a uniform source state and observing the destination block. Sample q by
uniformly relabelling i inside its original source block after observing h.
Then q(i,h) is the block-average row law divided by n. Both joint coordinates
are at most 1/n and their squared L2 norms are at most 1/n. For balanced
blocks pi_h=1/r, the incoming weighted squared residual is exactly

    v = n*r*||p-q||2².

Hence the old test gives O(r*sqrt(n)/theta²), up to confidence amplification.
For unequal blocks, v <= n/pi_min * ||p-q||2² gives the sufficient rate
O(sqrt(n)/(pi_min*theta²)). The actual stratified, covariance-pilot procedure
can exploit smaller variance and has explicit finite constants, row floors
and failed rounds; this is not evidence of a new asymptotic testing exponent.
This reduction is not a generic tolerant-TV test: its completeness is the
stronger scaled L2 proximity condition, with a fixed gap. Testing support,
threshold and sample count must be fixed before the fresh batch or receive
a valid sequential confidence construction. Uniform within-block relabelling
requires the retained membership lists or paid rejection using the map
(expected n/|block| draws); these rates count source calls, not all sampling
bit operations or inverse-map storage.

## Paid downstream and comparator scope

The current route acquires all m r² local norms and then executes ordinary
O(L m r²) Bellman scalar products with exact integer comparisons. On this
n=4096,r=4,m=2,L=24 synthetic fixture:

- Retained represented source calls: 3,298,951,680. These are aggregate
  multinomially generated logical calls, not individually executed queries.
- Original per-action norm work: 132,498,046 sparse integer products.
- Historical explicit policy-family attempt: 1,174,922,432 additional products.
- Current polynomial local-norm acquisition: 146,865,304 additional products.
- Measured cumulative norm acquisition: 1,454,285,782 products; no refund for
  the historical attempt. The current receiver replays 279,363,350 products.
- Original-goal DP: 768 scalar products, 669-bit peak accumulator; known
  common denominator 240,000,000 is acquired/paid, not exact-real advice.
- Stored original map/policy/task interface: 2060 packed bytes, ADDITIONAL
  to 468-byte coarse model, counts/certificates, metadata and registers.
- New compatible indicator goals pay new DPs. No new source observations are
  required under the already uniform operator event. This is restricted
  block-task transfer, not arbitrary future microscopic task reuse.

Every comparison receives the same observations and retained work. Ordinary
reduced-MDP planning plus this certificate is the principal constructive
comparator, not a weakened no-memory baseline. Goal-oriented/variance-aware
Monte Carlo, adaptive model learning, approximate bisimulation and task
caching are not proved inferior. A count of fewer downstream scalar products
does not establish an end-to-end practical win after the large acquisition.

## Informative failure of the polynomial certificate

`check_comparison_failure.py` gives an exact stochastic n=6 one-action
example. The true complement norm is at most 15/16, but a rational lower
bound on its block-norm comparison has squared norm greater than one.
Thus comparison geometry can refuse despite true contraction, even without
sampling or precision error. This does not claim the example would satisfy
all other task/leakage requirements. It prevents interpreting sufficient
polynomial admission as complete recognition of useful structure.
