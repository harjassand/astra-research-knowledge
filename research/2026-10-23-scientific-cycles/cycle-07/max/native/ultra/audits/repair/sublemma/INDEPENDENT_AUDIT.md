# Independent audit of the pairwise score sublemma

Audit scope: the exact finite-dimensional statements in
PAIRWISE_SCORE_CRITERION.md. The parent and a separate proof-audit subagent
independently derived the Bell-fixing SEP argument; the audit subagent also
checked the isotropic criterion, queue coefficients, induction, and shared
randomness extension. This is an internal algebraic audit, not external peer
validation or a novelty assessment.

## Checked points

1. Product-Kraus SEP is essential. The weaker property of preserving the
   separable-state set is insufficient for Bell-fixing unitality.
2. Unit Bell overlap makes the output exactly the pure Bell projector.
   Every Kraus image must therefore be collinear with its Bell vector.
3. Zero-overlap Kraus branches cannot provide a loophole: trace preservation
   and the sum of nonnegative norm deficits force every such product
   operator to vanish.
4. The matched-unitary conclusion requires unchanged equal local dimensions.
   Effective SEP maps obtained with local ancillary processing satisfy the
   result when those dimensions are retained.
5. LOCC and its finite-dimensional closure are contained in product-Kraus
   SEP. Finite-dimensional SEP channels admit finite product Kraus
   decompositions through their separable Choi operators.
6. The separable boundary state is exactly
   \(\chi=(\Phi+D\nu)/(D+1)\). Its finite product-state decomposition in the
   proof establishes the coefficient inequality without a numerical claim.
7. The one-pair score bound is
   \(\Delta\le-(\alpha-\beta/D)(1-a)\), for unnormalized nonnegative
   \(\alpha,\beta\). The reset channel saturates it and verifies sharpness of
   the strict threshold.
8. The queue starts at \(k=1\), so the \(j=1\) step is deterministic Bell
   input and is treated separately. For \(j\ge2\), the exponent in
   \(\beta_j=L^{-1}\sum_{k<j}q^{j-1-k}\) accounts for the preceding noisy
   pairs only.
9. The strict queue coefficient gap follows from
   \(1-D/(D^2-1)>0\) for every integer \(D\ge2\). Only prefix tests
   \(1\le j\le L\) are needed.
10. In a convex shared-random mixture, all component score changes at each
    induction step are nonpositive. A nonnegative average makes every
    positive-weight component Bell-fixing; cancellation between beneficial
    and harmful branches is unavailable at that step.
11. Each factor in that mixture must itself be a fixed CPTP pair channel.
    Adaptive cross-pair instruments are not automatically representable in
    this form.
12. A deterministic suffix may be reset. This is consistent with both the
    pairwise criterion and the fact that a fixed Bell prefix does not imply
    unitality across an unconstrained larger space.
13. No initial shared entangled ancilla is free under the stated SEP model.
    Any extra resource must be charged explicitly. Local discard/preparation
    is allowed by the mathematical channel class, which can be broader than
    a physical free-operation class used by the parent argument.
14. Each original nonzero product-Kraus branch has
    \(K_s^\dagger K_s=|c_s|^2I\), so its probability is input-independent.
    The normalized conditional branch fixes both Bell and maximally mixed
    inputs. Retained classical records therefore cannot identify hidden
    noise positions or lower the uncertain-prefix optimized readout entropy.
    This statement includes conditioning on the complete shared label; it
    does not assert an analogous result for coherent quantum flags.

## Explicit exclusions

- No impossibility claim is established here for joint cross-pair LOCC,
  joint processing of the independent tasks, or state-dependent approximate
  repair.
- No quantitative approximate-preservation estimate follows from the exact
  Kraus equality argument alone.
- Retained coherent quantum flags, enlarged output spaces, and additional
  quantum resources need their own entropy and resource argument.
- A nonuniform queue requires checking its own coefficient inequalities.
- No tiny finite score fixture, numerical search, classification novelty,
  or solution of the parent research goal is claimed.

## Additional support check

Even without locality, a CPTP map fixing the entangled \(\Phi_D\) cannot map
\(\nu\) to a pure product: positivity gives
\[
 \Lambda(\nu)=D^{-2}\Lambda(\Phi)+
 D^{-2}\Lambda(I-\Phi)\ \ge D^{-2}\Phi.
\]
A rank-one output would have to be supported on the Bell vector. This
weaker support argument does not establish invariance of \(\nu\); that
stronger conclusion uses product-Kraus SEP.
