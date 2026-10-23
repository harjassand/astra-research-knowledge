# When local moves destroy a sampling guarantee, and which information restores it

**Astra PRO3 research checkpoint — 21 October 2026**

## Decision and strongest result

Continue the mathematical question of finite-time guarantees for learned-proposal Monte Carlo. This allocation establishes a precise separation: a fixed population forward-KL budget controls proposal-start independence Metropolis, but it does not give any uniform mixing-time bound after an arbitrary ordinary reversible local Metropolis update is mixed in. Adding a reverse-KL budget restores a uniform exponential-accuracy bound for the lazy random mixture. The leading exponent is exactly characterized in the regime where the reverse budget does not exceed the forward budget.

Let pi be the target, q the independent proposal, G the independence-Metropolis kernel, and L any fixed pi-reversible kernel. With fixed 0<alpha<1, define

    C = [I + alpha G + (1-alpha)L]/2, X0~q.

For K,J>0, let T(epsilon) be the supremum of the proposal-start TV mixing time over D(pi||q)<=K and D(q||pi)<=J, including all such L. The proved bracket is

    max{K,(1-alpha)J}
      <= liminf epsilon log T(epsilon)
      <= limsup epsilon log T(epsilon)
      <= max{K,J}.

In particular, for **0<J<=K**, the limit exists and equals **K**. For **J>K**, the sharp coefficient remains unresolved. The proof does not assert that the upper coefficient J is attainable.

These are internally proved and independently challenged mathematical results. The full arguments are `PROOF.md`, `JOINT_KL.md`, and `JOINT_KL_FUNNEL_NOTE.md`. Numerical checks supplement the arguments. Historical priority and external scientific acceptance are not established by this checkpoint.

## Why the question matters

An exact-target Metropolis kernel preserves the desired target, but preservation alone does not tell a scientist how long to run it. Learned proposals are often assessed by an average divergence, while practical samplers combine their global proposals with local transitions. The scientific bottleneck is whether the supplied information actually bounds finite-time bias, including the initial distribution. It is not merely whether an implementation satisfies a formal balance identity.

Published local/global methods can be effective under their additional assumptions. Samsonov et al. (NeurIPS 2022) obtain geometric guarantees using drift, level-set weight control and a second-moment condition. Those constants are not controlled by forward KL alone. The current result identifies a missing information condition; it does not contradict their theorem or claim that practical local moves are generally harmful.

No scientific dataset or physical experiment is claimed in this mathematical allocation. The three-state probabilities are directly sampleable, so their bad Metropolis behavior is not a lower bound for all possible samplers. This distinction prevents an artificial small example from being presented as an application or computational breakthrough.

## What was recovered and preserved

The actual owned B3 archive was retrieved and its exact bytes verified: `Astra_B3_EVIDENCE_20261021.zip`, 14,540,463 bytes, SHA256 `1fe700db2fda644e33bb90a4cd12170d0dd049109216a52c0fd88208527eef50`. Its source, measured rotation curves, fit outputs, unsuccessful diffusion case and frozen criterion remain in that unchanged private archive. The present package carries the unchanged decision, registration and main README plus the exact retrieval identity; it does not duplicate or rerun the 14.5 MB archive.

B3 retains the pISO enclosed-mass correction. The complete core-versus-cusp inference remains unaccepted because the predictive-adequacy gate failed, with numerical evidence-threshold limitations also retained. No new galaxies, revised gate, extended reduced-curve fits or raw-cube operation were used. The separate metadata-admission failure remains closed. The R3/anMC recipient rejection and conditional sampler also remain preserved and closed.

The recovered local checkpoint did not establish ownership of hidden entropy, N33, N557, IQM or Ultra's protected construction. This question was selected as a distinct programme after the former reserve instruction was superseded.

## Pure independence Metropolis is the strongest ordinary baseline here

With only D(pi||q)<=K and X0~q, define R_K(n)=sup TV(qG^n,pi). The independently proved sharp asymptotic is

    log(n) R_K(n) -> K.

Equivalently, the leading worst-case log mixing cost is K/epsilon. This is a close specialization/refinement of the established approximate-rejection-sampling framework, not a new entropy barrier. The corrected Block–Polyanskiy preprint is essential: its old proceedings tail lemma was corrected by the authors. The source distinction is recorded in the literature notes.

Ordinary sampling-importance-resampling (SIR) is not promoted over IMH. Kurennoy, Yarullin and Reid (2026), Theorem 1, gives same-candidate-budget convex-divergence dominance of proposal-start IMH over SIR on finite positive supports. The executable comparison uses IMH. SIR is retained only as a transparent proof device for an approximate-warmness certificate.

One initialization draw plus n IMH transitions costs n+1 independent candidates and at most n+1 target/proposal evaluations with a cached current weight. This exact counting is used in the principal replay. No target normalizing constant is required.

## The cold-start obstruction

For fixed K>0, set c=K/4 and b=1-exp(-c). On states A-B-C use

    pi=(p, p exp(-2c/p), 1-p-p exp(-2c/p)),
    q =(p exp(-c/p), b, 1-b-p exp(-c/p)).

For the explicit range in the proof, D(pi||q)<=3K/4. The same symmetric nearest-neighbor proposal, with probability one half on each adjacent edge, produces an ordinary local MH kernel. The proposal starts with a substantial excess mass at B. A local transition transfers part of it to A, whose stationary mass p is small. Both local and global departures from A are exponentially rare in 1/p.

If H=alpha G+(1-alpha)L, d=b(1-alpha)/2 and h is its departure probability from A, then

    TV(qH^n,pi) >= d(1-h)^(n-1)-p.

For every fixed n, letting p tend to zero leaves a positive lower error d. Therefore there is no uniform finite mixing-time bound from K alone for all admitted hybrids, even though every individual finite chain is irreducible and convergent. The same obstruction survives both LG and GL schedules with exactly one global proposal per cycle. It is not explained merely by replacing global calls with local calls.

Earlier work already establishes that extra valid updates can delay mixing in general (Holroyd, 2011). The scoped result here concerns the loss of the forward-KL-only proposal-start guarantee with a fixed three-state ordinary local proposal graph. No priority claim is made for that precise construction.

## Reproducible numerical evidence and matched costs

The principal implementation constructs the general MH acceptance matrix from probabilities, rather than hard-coding the derived transition formulas. It propagates the full law by repeated squaring using 360-digit Decimal arithmetic. A second implementation uses the independently derived formulas at 350 digits. The principal result was also evaluated once at 440 digits.

For K=1, alpha=1/2 and p=0.001, actual forward KL is about 0.4987505002. At the same **1,000,001 total global candidates**, including the initial draw:

| Schedule | Global candidates | Additional local calls | TV error |
| --- | ---: | ---: | ---: |
| Pure IMH | 1,000,001 | 0 | 0.0010000000 |
| Local then global | 1,000,001 | 1,000,000 | 0.1095996085 |
| Global then local | 1,000,001 | 1,000,000 | 0.0234645468 |
| Equal random mixture | 1,000,001 in expectation | 1,000,000 in expectation | 0.0611765009 |
| 1,834 IMH initialization candidates, then LG | 1,000,001 | 998,167 | 0.0010000000 |

The mixture row uses 2,000,000 total non-lazy updates; its global budget is an expectation, unlike the deterministic schedules. Local proposals and their target evaluations are additional costs. Each call is a finite-state mathematical operation here; no equal-cost scientific simulator is assumed.

The initializer budget 1,834 is chosen from the proved conservative approximate-warmness formula at K=1 and epsilon=0.01. Its actual TV of 0.001 in this example is separately computed; approximate warmness is not mislabeled as a direct TV certificate. Pure IMH alone is already as good here and uses fewer local operations. No speedup is claimed.

The analytic no-exit lower bound at p=0.001 rules out mixture mixing to TV 0.01 up to a scale about 10^109.083 steps. This is a mathematical lower-bound evaluation, not a simulation of those steps. Matrix powering likewise represents large transition counts with logarithmic arithmetic work.

The numerical acceptance checks all passed: invariance, detailed balance where required, lower/upper inequalities, all checked IMH/SIR convex-divergence comparisons, and 36 matching TV values across independently coded implementations. The 360/440-digit comparison covered 472 numeric outputs; their maximum recorded difference was about 6.77e-355. These are rounded arithmetic checks, not interval certificates. Rounding an escape probability of order 1e-109 into a binary64 transition diagonal would erase it; the ideal-real theorem is separate from a floating-point sampler implementation.

## Constructive response and the sharper theorem

The first constructive response was a safe initialization: N iid q candidates with SIR produce a good-output submeasure bounded by 4pi, outside a bad event of probability at most exp[-N/(16 exp(2K+1))]. The finite-space IMH dominance theorem transfers this guarantee to the stronger ordinary initializer. A self-contained weak-Poincare argument then controls every fixed reversible local mixture after laziness. It is a valid but very conservative initialization-plus-convergence bound.

The stronger continuation avoids that initialization phase when both KL budgets are available. For an event A, smooth its indicator g=C^t 1_A. Spectral calculus gives E_C(g,g)<=1/[4(2t+1)], and E_G<=2E_C/alpha. Let M=exp(2K+1), A0={W<=M}, and s0=pi(A0)>=1/2. Anchoring the Dirichlet form on A0 controls a weighted quadratic deviation of g.

For the shared core S={1/B<=W<=R}, the resulting bound is

    TV(qC^t,pi)
      <= max{pi(W>R)+q(W<1/B)/B,
             q(W<1/B)+pi(W>R)/R}
         + sqrt[(M(B+1)+R)/(alpha s0(2t+1))].

The two KL budgets control the two tails. Taking B=R=t/(log t)^4 gives the upper coefficient max(K,J). The principal constructed the indicator-smoothing argument; independent challenge improved the tail accounting from a sum to a maximum and the core cost from a product BR to a sum M(B+1)+R. Every changed bound and its role is recorded.

The closest general techniques are inherited: Dirichlet comparison, positive-kernel spectral smoothing and weak-Poincare control. The focused supplementary source check identifies Andrieu–Lee–Power–Wang (2022) as a particularly relevant comparison for IMH weak-Poincare bounds. The entropy-only proposal-start envelope needs the additional initial-law treatment supplied here; this is not a claim to have invented the general machinery.

## Resources, limits and next scientific step

The principal 360-digit replay took 0.199 s of measured process CPU and about 11.6 MiB peak process RSS. The 440-digit check took 0.297 s. The new joint-KL check took 0.476 s, testing every event of two fixed finite state spaces at 30 threshold/time combinations. The independent three-state check took about 0.211 s. Exact receipts are in the results, including source hashes and matrix-operation counts. These observations are arithmetic-check costs only. Total research, model, retrieval and end-to-end application costs were not measured.

The theorem assumes population KL bounds, exact transition probabilities, a fixed mixture weight, a fixed reversible local kernel, and the stated initialization. It supplies no certificate of global KL from a training sample and no guarantee for arbitrary adaptive kernel selection. The positive joint-KL theorem is for the lazy random mixture; deterministic LG and GL have separate negative examples and are not silently covered by its positive bound. This is not an applied computational gain or a claimed new physical observation.

The next owner step is now the **J>K sharp-coefficient problem**, with the same lazy random mixture and complete hypotheses. Determine whether the factor (1-alpha) in the reverse-KL lower construction is unavoidable, or whether a different reversible construction attains the upper coefficient J. The current anchor bound loses information about a global correction occurring before the first local transfer. More demonstrations of the old forward-only obstruction would not address that gap.

Max retains programme integration; the evaluator receives the same source. No private source is authorized for public publication by this handoff, and upload success is not receiver verification or scientific acceptance.

## Primary literature used

- Block and Polyanskiy, corrected arXiv:2302.04658v3 (2024): https://arxiv.org/html/2302.04658v3 . Approximate rejection sample complexity; prior entropy scale and corrected tail lemma.
- Kurennoy, Yarullin and Reid, arXiv:2610.03480v1 (2026): https://arxiv.org/html/2610.03480v1 . Finite-budget IMH versus SIR and exact output-law comparators.
- Samsonov et al., NeurIPS 2022: https://papers.neurips.cc/paper_files/paper/2022/hash/21c86d5b10cdc28664ccdadf0a29065a-Abstract-Conference.html . Local/global guarantees with stronger assumptions.
- Holroyd, arXiv:1101.4690 (2011): https://arxiv.org/abs/1101.4690 . General extra-update mixing delays.
- Andrieu, Lee, Power and Wang, arXiv:2112.05605v2 (2022): https://arxiv.org/abs/2112.05605v2 . Weak-Poincare and Dirichlet comparison framework; see the incremental novelty note for exact theorem scope.

The full comparison and exact public-source hashes are under `sources/`. Their presence is attribution and reproducibility, not an external endorsement of the new result.
