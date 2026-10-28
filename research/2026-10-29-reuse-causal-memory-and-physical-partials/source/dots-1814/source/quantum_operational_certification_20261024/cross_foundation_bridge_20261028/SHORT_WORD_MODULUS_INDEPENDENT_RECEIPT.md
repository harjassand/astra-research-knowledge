# Independent review of short experiment physical prediction

28 October 2026. Reviewer: `producer-workspace/review_boundary_residual_simulator`.

**Verdict: ACCEPT at the stated conditional mathematical and finite-computability scope.** The short-word equivalence relation, global semialgebraic error bound, terminating exact constant search, physical CP comparison and count-only acquisition construction are sound. No unresolved load-bearing proof obligation was found. This acceptance does not assert that a generic modulus, physical candidate or useful acquisition budget has actually been computed.

This receipt binds `SHORT_WORD_SEMIALGEBRAIC_PHYSICAL_PREDICTION.md`, SHA256 `b5f83e2d812b7dd64f0e244b7a55093f78f8d02feaff30026d9bfc86468d37fb`. I read the initially assigned hash `a2d4feb06f478728468809daaf7c2bdda9657941fd5e33d5693da2733a9b9a54` and the complete final delta. The delta clarifies rational budgets and confidence-valid intervals and adds quantum-automata prior art; it changes no theorem constants. The earlier normalized/raw-core accepted sources and receipts were not edited. This is a separate post-freeze result, not a retroactive modification of the 16:16 archive.

## Compact physical class and exact short equivalence

For a fixed finite library and physical dimension `d`, the density and full Choi constraints define a nonempty compact rational semialgebraic set. Positivity and branch-sum TP imply `Tr(J_z)<=d`, which bounds every matrix entry. Optional complete POVMs also form a compact factor. Hermitian real/imaginary entry coordinates with the stated Frobenius weights give an explicit positive quadratic metric with rational coefficients; no irrational coordinate oracle is needed.

The source can be embedded from smaller dimension into `d` by a separate TP completion on an unused block. The actual unknown entries remain existentially quantified, not supplied calibration information. A finite stationary physical-dimension bound is indispensable; this construction does not infer one from data.

The short-equivalence proof is correct. The direct sum of two real Hermitian Liouville representations has dimension at most `2d^2`. Starting from the nonzero pair of initial states, a reachable-word span either grows or is invariant forever. It therefore stabilizes by word length `2d^2-1`. The trace-difference functional, and each declared terminal-effect difference functional, annihilate every reachable vector if they annihilate these short vectors. This proves all-word equality. Feedback chooses a word on each record branch, so the same statement gives complete classical-law equality, including private randomization and clocked stopping.

The exact length lemma is not new quantum-automata theory. I checked [Li and Qiu, Theorem 5](https://arxiv.org/pdf/quant-ph/0604085), which gives the corresponding sum-of-squared-dimensions-minus-one result for quantum sequential machines. [Kiefer et al., Proposition 2](https://www.cs.ox.ac.uk/andrzej.murawski/papers/cav11.pdf) gives the conventional weighted-automaton short-witness principle; its stated bound is the sum of dimensions, while the source's explicit span argument supplies the precise minus-one bound used here for general CP instruments.

## The relation distance modulus and its terminating computation

The crucial target is `Z={(theta,theta'):S(theta)=S(theta')}`, not the diagonal and not a chosen physical gauge. On the compact pair space, `F=||S(theta)-S(theta')||_2^2` is a nonnegative polynomial and `g=dist((theta,theta'),Z)^2` is continuous and semialgebraic. The set `Z` is compact, nonempty and exactly the zero set of both functions.

I directly checked [Basu and Mohammad-Nezhad, Theorem 1.1](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/improved-effective-lojasiewicz-inequality-and-applications/022BF859F5714FDA8050F6DC1992E48B). Its compact semialgebraic hypotheses apply with `f=F` and `g=dist^2`; it supplies a positive integer exponent and finite constant. Enlarging the latter to a positive integer is legitimate over the ordinary real parameter space.

Equation (5) is a genuine rational-polynomial decision problem, not a hidden distance or identification oracle. Its existential witness is an equivalent physical pair in `Z`, and compactness makes the nearest-point minimum attained. Thus the quantified sentence is equivalent to `g^n<=C F`. Enumerating positive integer pairs in finite-diagonal order and deciding each sentence by exact real quantifier elimination terminates because at least one integer pair satisfies the inequality. The algorithm need not know a convenient exponent in advance.

All model variables, principal-minor constraints, short probabilities and quadratic distances have finite explicit encodings. If the ambient model coordinate count is `q`, each sentence has `2q` universally quantified pair coordinates and `2q` existential witness coordinates. Native short probabilities have degree at most `L+1`, terminal-seeded ones at most `L+2`; `F` has at most twice those degrees and the distance power has degree `2n`. These observations establish finite construction, not a manageable formula size. The number of short words, constraints, tested integer pairs, coefficient sizes, algebraic signs and quantifier-elimination work can be enormous. No generic `n,C` has been computed by the source or by this review.

## Physical comparison and constants

The nearest equivalent pair may be used only to compare each original model with its own nearby barred model. The two barred models have equal **classical laws**, not equal memory channels or states. The proof respects this distinction.

For one model displacement `u`, the initial half trace distance is bounded by `sqrt(d) u/2`. For a Hermitian Choi difference `Delta J`, let `kappa=||Delta J||_op`. The Choi matrices `kappa I +/- Delta J` are PSD. Their CP-order domination implies that an inserted map difference, including on a reference-assisted positive input, has trace norm at most `d kappa`; hence `||Delta Phi||_diamond<=d||Delta J||_F`. Summing branches of one complete instrument and applying Cauchy-Schwarz gives the stated half-diamond bound `d sqrt(b) u/2`. The maximum number of outcomes **per action**, not the total number of branches across all actions, is the correct factor.

For a final test with at most `t` outcomes, its same-state half-l1 change is at most `sqrt(t) u/2`. Summing the two physical comparisons uses `u_1+u_2<=sqrt(2)||y-z||`. A valid sharper coefficient before rational loosening is therefore

    sqrt(d/2) + d sqrt(b/2) H + sqrt(t/2),

with the final term omitted when there is no final readout. The source's `d(1+bH)+t` dominates it. Thus there is no missing factor of two, branch count, dimension or terminal-library size in Equations (7)-(8).

The ordinary physical telescope retains the complete record and remains valid for arbitrary classical feedback. A pre-call clock bounds the native expectation in each outer physical comparison by `gamma/delta`, independently of state and policy. Finite censor-labelled truncations and uniform clock tails justify the infinite completed-law limit. Initial-state error is paid once; a genuinely final POVM is paid once; actual memory-retaining macro-readouts must be complete native instruments. This proves Equation (9). It does not imply a uniform useful bound for unrestricted unclocked infinite horizons.

## Confidence and exact candidate acquisition

The final source correctly uses rational accuracy/confidence budgets, or certified rational budgets no larger than the requested ones. For confidence-valid intervals of radius at most `w`, both the source and any compatible physical candidate differ by at most `2w` on every uncertain short probability. Consequently `F<=4K w^2`, and Equation (10) is exactly the condition obtained by raising the target inequality to power `2n`. A dyadic search tests this with rational arithmetic; the logarithmic shot allocation requires an outward integer bound. Arbitrarily narrowing an interval is not permitted. If `K=0`, there are no uncertain events and the per-event allocation is vacuous.

The count experiment is a raw joint-event experiment from a repeatable full-process start. Prefix failures count as zero indicators and still consume charged starts/calls. No successful-prefix normalization or retained quantum calibration reference is introduced. Simultaneous confidence covers the fixed short vector before candidate or controller selection, so selection requires no additional controller union bound.

Candidate feasibility consists only of physicality and the finite rational bands. No rank equality, spectral gap, core inverse or strict CP-interior premise has returned indirectly. On the confidence event the actual finite-dimensional realization is a real feasible point. Standard exact real-algebraic sampling therefore supplies an algebraic candidate, including on boundaries; rational approximation is not presumed to preserve PSD, normalization or rank. A resource cap may return UNKNOWN. Count acquisition, candidate sampling, implementation synthesis and planning were not executed in this work.

## Comparison with direct horizon acquisition

The source identifies the proper baseline. With no dimension promise, acquiring every raw word through `H` already gives finite all-policy prediction. One may enforce nonnegativity and causal consistency on the finite joint table and choose any confidence-compatible table. For a deterministic policy, summing entry errors over its terminal leaves bounds full-law TV; private randomization follows by averaging. This baseline can have exponentially many settings/leaves and exponentially small required entry widths, but it needs neither a physical model nor a rank/core promise.

The accepted increment is fixed maximum native experiment length `2d^2-1`, independent of deployment horizon, with a computable propagation modulus that pays rank singularities globally. For fixed dimension/library and a once-computed `n,C`, choosing a dyadic width within a constant factor of the threshold gives a total shot upper bound of order

    C K^2 (M_H/epsilon)^(2n) log(2K/alpha),

up to numerical constants and ceilings. Thus the displayed acquisition bill is polynomial in `H` for fixed class constants, unlike literal exhaustive-H enumeration. This is not a practical or incumbent separation: the exponent/constants and offline algebraic computation may be prohibitive, other dimension-aware methods can use the same mathematics, and policy search may still be exponential. No sharp lower bound on required experiment length is established by this receipt.

## Independent exact checks and limits of the evidence

The author's full `d=1` binary and restricted `d=3` one-shot diagnostics were replayed outside the source directory; the final JSON was byte-identical. I separately checked their formulas. In the restricted family, the physical metric is `2(da^2+db^2)` per model, the short discrepancy is `2L(ab-a'b')^2`, and the stated repair and singular-ray identity are valid. The exponent-one failure concerns that constrained family only, not the full dimension-three relation; the source correctly preserves this distinction.

The separately authored `short_word_modulus_independent_check.py` adds noncommuting qubit evidence. An exactly equivalent gauge-related pair has squared physical parameter separation `1465/144`, but its pair belongs to `Z`. Nearby original endpoints have independently perturbed initial states, complete instruments and final POVMs. Direct-sum span saturation gives dimensions four for the equivalent pair and eight for the perturbed pair. All 32 exact combinations of horizons zero through seven, bounded/clocked feedback and trace/final-readout interfaces satisfy the physical triangle comparison and the source's conservative constants.

For example, at horizon seven with final tests, the exact endpoint TV is approximately `0.001313666`; the sum of outer physical TVs is approximately `0.003247913`. The chosen equivalent-pair repair has distance approximately `0.005246252`, and `M_H=32` safely bounds the latter comparison. These checks verify the physical comparison step with an explicit witness, **not** a generic global Łojasiewicz constant.

An independent boundary-unitary attack checks terminal completeness. Starting from `|+>`, compare identity with `U=(62499 I+500 iZ)/62501` and use a final Y test. Every native-only word probability is one, so omitting terminal seeds gives `F=0` despite a nonzero final discrepancy. Through `L=7`, the maximum final-event discrepancy is below `1/16`; at horizon 98 the final TV exceeds `0.499`. Both comparisons were checked exactly by rational inequalities. This confirms why terminal seeds and horizon dependence cannot be dropped.

All independent diagnostics use zero source calls, episodes or RNG calls. No generic quantifier elimination, candidate feasibility solve or laboratory synthesis was executed. Their role is to attack load-bearing identities and boundaries; the general theorem rests on the reviewed derivation and standard compact semialgebraic machinery.

## Final scope

**No blocking correction is required for hash `b5f83e2d…`.** Accepted scope is finite-library classical full-law prediction from the specified repeatable start, with a supplied finite physical memory dimension and explicit accuracy/computation costs. It excludes dimension discovery, arbitrary coherent controls/references, microscopic identification, source-memory state distance, practical resource advantage and novelty certification. The earlier residual providers and their stronger or differently scoped guarantees remain separate. The received terminal-test/payload transfer retains its own independent-datum and same-actual-terminal-operation premises.
