# Literature boundary: proposal-start IMH, entropy-only control, and hybrid kernels

Research date: 2026-10-21. Prepared by the independent literature subagent for Astra Restore PRO3. This is a source and scope check, not the main proof certificate. The current constructive proof and experiments are owned by the parent investigator and its independent challenge agent.

## Assessment

1. The order `exp(Theta(K/epsilon))` for selecting one of iid proposals under `D_KL(pi||q) <= K` is established by Block and Polyanskiy (COLT 2023; corrected arXiv v3, February 2024). It must not be presented as a newly discovered entropy barrier.
2. Their corrected proof contains an intermediate inequality with the leading constant needed for a sharp asymptotic specialization. With the proposal-start IMH likelihood-tail bound or its priority-sampling representation established in 2026, the proposed limit `log(n) sup TV(q P^n, pi) -> K` lies very close to existing results. It is useful as a precise independently proved baseline, but claiming a major new sampler theorem from this specialization would be unsupported.
3. The finite-time IMH distribution is already explicitly known. The recent priority representation and older exact-transition formula provide stronger comparators than a generic coupling bound. The examined papers do not state that the *KL-constrained finite-time IMH extremum* is attained by two likelihood values. The existence of Bernoulli extremizers for certain pairs of f-divergences does not by itself establish this nonlinear statement.
4. General statements that extra invariant/reversible updates can delay mixing are old. Holroyd (2011) supplies explicit finite-schedule counterexamples. Consequently the new three-state hybrid construction should be scoped to the destruction of a **uniform proposal-start mixing bound controlled only by forward KL**, with a fixed local proposal graph, rather than advertised as the first harmful hybrid update.
5. The strongest practical local/global comparator examined, Samsonov et al. (NeurIPS 2022), imposes local drift and likelihood-ratio/second-moment controls. Its theorem is not contradicted by a family where those constants diverge. Forward KL alone is a materially weaker contract.
6. No paper in this focused investigation stated the exact fixed-forward-KL, proposal-start, three-state hybrid impossibility result now being constructed. This is a bounded negative search result, not a certificate of novelty or priority.

## 1. Approximate rejection sampling already gives the entropy scale

**Adam Block and Yury Polyanskiy.** *The Sample Complexity of Approximate Rejection Sampling with Applications to Smoothed Online Learning.* COLT 2023, PMLR 195; corrected arXiv:2302.04658v3, 2024-02-23.

- Primary proceedings: <https://proceedings.mlr.press/v195/block23a.html>
- Corrected source: <https://arxiv.org/abs/2302.04658>
- Corrected HTML: <https://arxiv.org/html/2302.04658v3>
- Corrected PDF: <https://arxiv.org/pdf/2302.04658v3>
- Local corrected PDF: `block_polyanskiy_2302.04658v3_corrected.pdf`.

The experiment is to observe `n` independent samples from `mu` and output one of them so that its marginal law approximates `nu` in total variation. The rule may use target/proposal information. The paper studies classes defined by `D_f(nu||mu) <= D`.

Corrected Theorem 3 gives a sufficient budget

`n >= [2/(1-epsilon)] log(2/epsilon) (f')^{-1}(4 D_f/epsilon)`, with a lower floor of 2.

For `f(x)=x log x-x+1`, this gives an exponential upper bound with exponent `4K/epsilon`. Theorem 5 gives, for `0<epsilon<=1/4` and divergence budget `delta>2f(1/2)`, an adversarial pair requiring

`n >= (1/2) (f')^{-1}(delta/(2 epsilon))`.

The lower proof uses Bernoulli pairs, together with the fact that any selector's output density relative to the proposal is bounded by `n`, so its TV error is at least the hockey-stick divergence `E_n(nu||mu)`. Theorem 6 (formal Theorem 34 in the corrected version) supplies a fixed pair, independent of `n`, with an almost matching logarithmic/polynomial tail rate under a growth condition on `f`. It does not give a fixed pair attaining the positive KL minimax coefficient at all large `n`.

### The corrected proof is the right source

The proceedings version's Lemma 27 incorrectly asserted

`nu{W>M} <= D_f(nu||mu)/f'(M)`.

Its layer-cake calculation dropped a boundary term. This was already corrected by the authors in arXiv v3; the abstract page explicitly identifies the correction, and the acknowledgements name the people who found the original error. It is not a new Astra correction.

A diagnostic example for the obsolete statement is `nu=Ber(0.5)`, `mu=Ber(0.001)`, `M=499`: the high weight is 500, the actual target tail is 0.5, while `D_KL/log(499) = 0.4444561053027615`. The corrected Lemma 27 states a weaker bound with `2D_f/f'(M/2)` and proves the more informative intermediate inequality

`nu{W>M} <= M D_f(nu||mu)/f(M)`.

For KL, this is

`nu{W>M} <= K/(log M - 1 + 1/M)`.

This directly carries leading coefficient 1 asymptotically. Allocate a vanishing fraction of the TV error to rejection failure, and an upper cost with `epsilon log n -> K` follows. A matching coefficient is accessible by sharpening the same Bernoulli coverage construction. Therefore an independently proved sharp coefficient should be described as a precise refinement/specialization of this established framework.

The inverse-gradient formulas and broad tilde notation in the paper should not be read as an already stated exact-constant result. The direct inequalities above are the appropriate comparison.

## 2. Proposal-start IMH has a sharper existing finite-budget description

**Alexey Kurennoy, Ramil Yarullin, and Fergal Reid.** *Metropolis–Hastings Dominates Importance Resampling for Policy Composition.* arXiv:2610.03480v1, 2026-10-02.

- <https://arxiv.org/abs/2610.03480>
- <https://arxiv.org/html/2610.03480v1>
- <https://arxiv.org/pdf/2610.03480v1>
- Local PDF: `kurennoy_etal_2610.03480v1.pdf`.

Here `H_M=q P^(M-1)`: the budget `M` includes the first proposal used for initialization. The main source works with positive target/proposal probabilities on common finite supports.

For normalized weight `W=pi/q`, define

`alpha_B=E_q[min(W,B)]`, `t_B=E_q[(W-B)_+]=1-alpha_B`.

Proposition 3 gives

`t_M <= inf_{all M-candidate selectors} TV(output,pi) <= TV(H_M,pi)`

and

`TV(H_M,pi) <= inf_{B>0} { t_B + (1-alpha_B/B)^M }`.

The power term can be relaxed to `exp(-M alpha_B/B)`. This is a theorem for ordinary IMH with the original weights; clipping is an analysis device. It imposes no warm-start condition beyond initializing from `q`. A core/tail argument based on this fact is prior art.

Theorem 1 proves that, at the same finite candidate budget, proposal-start IMH is at least as close to the target as ordinary sampling-importance-resampling under every convex f-divergence, with appropriate strictness. Appendix B.2, Proposition 4, proves an **exact minimax TV value over a bounded-weight class**: for `W<=1/kappa`, `kappa>=eta`,

`inf_selectors sup_instances TV = sup_instances TV(H_M,pi) = (1-eta)^M`.

This is not a KL-constrained minimax theorem. Its lower extremal sequence has two weight levels, with one target mass tending to zero.

### Exact output law and priority representation

Lemma 2 identifies the marginal law of proposal-start IMH with choosing the largest of the independent priorities `w_i/U_i` from the iid proposal pool. For a fixed candidate pool, equality is with IMH in uniformly randomized candidate order; iid proposals make randomization of order irrelevant to the marginal output law.

Let `B(u)=E_q[(1-uW)_+]`. Equation (21) gives

`dH_M/dpi(w) = M integral_0^(1/w) B(u)^(M-1) du`.

This ratio is decreasing in `w`. Lemma 4 conditions on the maximal priority: the returned sample has the target law restricted to weights below that priority. The paper relates (21) to the exact transition probabilities of Smith and Tierney (1996), restated in Wang (2022), Theorem 4.

These formulas are directly relevant to a finite-time variational problem. No claim that the nonlinear KL extremum reduces to two weight levels was found in this source.

**Seiyun Shin, Juhyeong Pang, and Kwang-Sung Jun.** *Uniform Race: Parameter-Free Approximate Rejection Sampling.* arXiv:2609.34639v1, 2026-09-28.

- <https://arxiv.org/abs/2609.34639>
- <https://arxiv.org/pdf/2609.34639v1>
- Local PDF: `uniform_race_2609.34639v1.pdf`.

The Uniform Race rule also selects the largest independent `w_i/U_i`. The paper describes it as a one-shot candidate selector, but the preceding IMH representation identifies the same marginal output law. It requires neither the target normalizer nor an envelope/clipping parameter as input. Theorem 1 simultaneously matches every fixed-threshold approximate-rejection upper bound. Proposition 1 gives the conditional target-truncation law. Corollary 1 gives the exact minimax value `(1-1/C)^N` over `W<=C`, and an `O(E_q W^2/N)` bound. It does not state the sharp KL minimax limit or the hybrid obstruction.

## 3. Other IMH results and their hypotheses

**Alireza Daeijavad and Shahab Asoodeh.** *Local and Global Contraction Principles for MCMC Mixing.* arXiv:2606.03033v1, 2026-06-02.

- <https://arxiv.org/abs/2606.03033>
- <https://arxiv.org/pdf/2606.03033v1>
- Local PDF: `daeijavad_asoodeh_2606.03033v1.pdf`.

Theorem 3 considers a non-atomic proposal and an `L`-warm start `mu_0<=L pi`. For the weight core `C_R={w<=R}`, core target mass `h_R`, and omitted mass `H_R`, it bounds the relevant hockey-stick distance by an explicit constant times

`h_R rho_alpha(R)^k + H_R <= exp(-k h_R/R)+H_R`.

Lemma 2 is a coupling/rejection-profile TV bound for arbitrary initialization. The paper gives several unbounded-weight tail regimes, including logarithmic rates, but does not state a target/proposal KL minimax result. The warm-start condition cannot be silently replaced by `X_0~q`: forward KL does not bound `q/pi`.

**George Deligiannidis, Pierre E. Jacob, El Mahdi Khribch, and Guanyang Wang.** *On importance sampling and independent Metropolis–Hastings with an unbounded weight function.* arXiv:2411.09514v3, 2026-07-02.

- <https://arxiv.org/abs/2411.09514>
- <https://arxiv.org/pdf/2411.09514v3>
- Local PDF: `deligiannidis_etal_2411.09514v3.pdf`.

Theorem 3.1 establishes the maximality of the common-randomness coupling and exact pairwise point-start TV in terms of rejection probabilities (for distinct starts). The moment-based theorems cover `E_q W^p<infinity`, including `p` between 1 and 2, and give polynomial rates. Those moment assumptions are stronger than finite forward KL. This is an appropriate attribution for the coupling mechanism, not a claim of a previously unknown sampler construction.

**Guanyang Wang.** *Exact Convergence Analysis of the Independent Metropolis–Hastings Algorithms.* Bernoulli 28(3), 2022; arXiv:2008.02455v6.

- <https://arxiv.org/html/2008.02455v6>
- <https://arxiv.org/pdf/2008.02455v6>
- Local PDF: `wang_2008.02455v6.pdf`.

Its exact worst-point geometric rate concerns bounded importance weights `w*<infinity`, with continuous-state and discrete variants and qualifications on initialization. It also records the older exact-transition formula relevant above. It is not an entropy-only proposal-start minimax theorem.

**Sourav Chatterjee and Persi Diaconis.** *The sample size required in importance sampling.* Annals of Applied Probability, 2018; arXiv:1511.01437v3.

- <https://arxiv.org/abs/1511.01437>
- <https://arxiv.org/pdf/1511.01437>
- Local PDF: `chatterjee_diaconis_1511.01437.pdf`.

Theorem 1.1 gives expectation-estimation upper and lower bounds around `n=exp(D_KL(target||proposal))`, with additional tail probabilities for the target log likelihood ratio. The simple exponential-KL headline requires concentration of that random log ratio. It is not a universal fixed-KL guarantee at arbitrary TV precision. Ordinary expectation estimation and a single approximate sample are distinct output contracts.

## 4. Hybrid kernels: closest meaningful theorems and cautions

**Sergey Samsonov, Evgeny Lagutin, Marylou Gabrié, Alain Durmus, Alexey Naumov, and Eric Moulines.** *Local-Global MCMC kernels: the best of both worlds.* NeurIPS 2022; arXiv:2111.02702.

- <https://papers.neurips.cc/paper_files/paper/2022/hash/21c86d5b10cdc28664ccdadf0a29065a-Abstract-Conference.html>
- <https://papers.nips.cc/paper_files/paper/2022/file/21c86d5b10cdc28664ccdadf0a29065a-Paper-Conference.pdf>
- Local PDF: `samsonov_etal_2022.pdf`.

The global kernel is iterative SIR with `N` proposals, followed by a target-invariant local rejuvenation kernel `R`. Theorem 2 gives `V`-uniform geometric convergence for the composition, under:

- A1: a Foster–Lyapunov drift inequality for the local kernel, with explicit constants on the level sets of `V`;
- A2(i): normalized likelihood weights bounded on those level sets;
- A2(ii): finite variance of the weights, equivalently finite `chi²(pi||q)`.

The rate and prefactor depend on those constants and on initial `V`. The paper does not promise that a KL-trained proposal alone controls a hybrid's finite-time error. A fixed three-node proposal graph with target-dependent Metropolis acceptance may have arbitrarily poor drift/escape constants as the target varies. Every individual finite positive example is geometrically ergodic; the issue is the lack of a bound uniform over the KL class. This is consistent with the published theorem.

**Yuval Peres and Peter Winkler.** *Can extra updates delay mixing?* Communications in Mathematical Physics, 2013; arXiv:1112.0603.

- <https://arxiv.org/abs/1112.0603>
- <https://arxiv.org/pdf/1112.0603>
- Local PDF: `peres_winkler_1112.0603.pdf`.

The censoring theorem applies to monotone spin systems and an extremal start (more generally, an initial density increasing in the system order). Inserting updates cannot increase the TV distance there. The ordering and initialization hypotheses are essential; target invariance or reversibility alone is not their theorem.

**Alexander E. Holroyd.** *Some circumstances where extra updates can delay mixing.* Journal of Statistical Physics 145, 2011; arXiv:1101.4690v1.

- <https://arxiv.org/html/1101.4690v1>
- <https://arxiv.org/pdf/1101.4690v1>
- Local PDF: `holroyd_1101.4690v1.pdf`.

Propositions 1 and 2 construct failures of censoring for proper four-colorings of a triangle and lazy transpositions of four objects. Starting from a fixed configuration, an inserted valid local update can increase the final error for any continuous metric. These are finite prescribed update schedules; there is no independence sampler, entropy-constrained proposal class, or uniform proposal-start mixing guarantee. They establish the broader caution, but do not state the precise current obstruction.

**Luke Tierney.** *A Note on Metropolis–Hastings Kernels for General State Spaces.* Annals of Applied Probability 8(1), 1998, pp. 1–9.

- Accessible original: <https://www2.stat.duke.edu/~scs/Courses/Stat376/Papers/TransdimMCMC/TierneyAAP1998.pdf>
- Local PDF: `tierney_1998.pdf`.

Theorem 4 extends Peskun's ordering: off-diagonal domination of reversible kernels orders the asymptotic variances of stationary sample-path averages. The source explicitly notes that higher-lag correlations need not be ordered. This is not an ordering of finite-time TV error from a chosen initial distribution.

For the current mixture `H=alpha P+(1-alpha)L`, off-diagonal domination holds relative to the lazified global kernel `J=alpha P+(1-alpha)I`. Thus a harmful proposal-start transient is compatible with better stationary asymptotic variance and with a Dirichlet-form comparison. These are different performance questions.

The proposed three-state family has `q(B)/pi(B)` diverging. A bounded-warmness theorem cannot be applied to it with a fixed constant. This identifies an actual missing initialization control rather than a violation of known invariant-kernel contraction.

## 5. Practical motivation source, without claiming an empirical application

**Louis Grenioux, Alain Oliviero Durmus, Éric Moulines, and Marylou Gabrié.** *On Sampling with Approximate Transport Maps.* ICML 2023, PMLR 202.

- <https://proceedings.mlr.press/v202/grenioux23a.html>
- <https://proceedings.mlr.press/v202/grenioux23a/grenioux23a.pdf>
- Local PDF: `grenioux_etal_2023.pdf`.

This compares flow proposals, importance sampling, and flow-assisted or reparameterized local MCMC. Its IMH mixing theorem uses a beta-warm initial distribution plus local approximation/regularity assumptions; it is not a KL-only result. It supports the relevance of distinguishing trained-proposal accuracy from guaranteed mixing, but this checkpoint contains no new empirical normalizing-flow benchmark or application claim.

## Limits of the literature investigation

This was a focused search of approximate rejection sampling, exact IMH laws, warm-start/core-tail IMH bounds, local/global MCMC guarantees, and censoring/Peskun counterexamples. It does not certify that no unpublished, differently worded, or inaccessible theorem exists. The current hybrid result needs its own complete proof and replay; its precise hypotheses must remain attached to every claimed implication.

The original source PDFs and extracted text were retrieved and read in the working research directory. The compact executable handoff includes these theorem comparisons and `SOURCE_MANIFEST.json`, which records exact public origins, byte sizes and SHA256 hashes, rather than embedding all complete third-party papers. Its mathematical proofs and new calculations are self-contained. Download receipts preserve failures: the OpenReview copy of the local/global paper returned a verification/403 response; the official NeurIPS copy was accessible and was used instead.

## Incremental novelty note: joint-KL lazy-hybrid envelope (2026-10-21)

**Question checked.** The internally proved `JOINT_KL.md` result uses
`C=(I+alpha G+(1-alpha)L)/2`, with arbitrary pi-reversible `L`, start `q`,
`D(pi||q)<=K` and `D(q||pi)<=J`. Its fixed anchor and bounded-observable
smoothing give `limsup log(t) sup TV(q C^t,pi)<=max(K,J)`, with matching
coefficient K when `J<=K`. This incremental check was limited to two primary
papers returned by a focused search. No priority claim is made.

**Check 1: established weak-Poincare/Dirichlet inheritance.** Christophe
Andrieu, Anthony Lee, Sam Power, and Andi Q. Wang, *Comparison of Markov
chains via weak Poincare inequalities with application to pseudo-marginal
MCMC*, Annals of Statistics 50(6), 3592–3618 (2022), arXiv:2112.05605v2.
Primary PDF: <https://arxiv.org/pdf/2112.05605v2>.
Proposition 28 gives the IMH inequality

`Var_pi(f) <= s E_G(f,f) + [pi tensor pi{max(W(x),W(y))>s}/2] osc(f)^2`.

Theorems 22, 35 and 38 turn weak inequalities and Dirichlet comparisons into
subgeometric bounds. These establish the general mechanism of transferring
tail-based control to a dominating positive reversible kernel. Remark 12's
stated TV consequence controls a functional of the initial density; for the
IMH oscillation inequality that requires bounded density oscillation, which
joint finite KL does not imply. The examined theorem statements and IMH
proof do not state the joint-entropy envelope, the `max(K,J)` coefficient,
or the fixed one-sided anchor calculation. They use the pairwise region
`{max(W(x),W(y))<=s}`. This source must be cited for the established
functional-inequality and comparison framework.

**Check 2: slice comparisons.** Sam Power, Daniel Rudolf, Bjorn Sprungk, and
Andi Q. Wang, *Weak Poincare inequality comparisons for Ideal and Hybrid
Slice Sampling*, arXiv:2402.13678v2 (2025-08-22).
Primary PDF: <https://arxiv.org/pdf/2402.13678v2>.
Theorem 12 compares ideal and hybrid slice kernels through Dirichlet forms
and slice-wise weak inequalities. Proposition 27 specializes that comparison
to IMH. Theorem 3 gives bounded-observable L2 decay; Corollary 4's displayed
TV bound retains an oscillation factor for `dmu_0/dpi-1`. It does not state
the entropy-only q-start envelope. Here "hybrid slice" means approximate
within-slice updates, not the arbitrary local/global random mixture in the
current construction; the terms should not be conflated.

**Disposition.** The current result belongs to an established
weak-Poincare/Dirichlet-comparison framework. Neither checked source directly
states the entropy-only maximum coefficient or the anchor inequality
`E_G(g,g) >= (s0/2) integral pi(dx)(g-m)^2/max(W(x),M)` used to replace the
earlier product `BR` by `M(B+1)+R`. This is a precise distinction from the
displayed prior theorems, not proof that the inequality has never been used.
Retain the independent proof and the scoped sharpness result without a
priority claim. No additional literature campaign was undertaken.

**New source receipts.** The downloaded arXiv PDFs were version-identified
from their first-page headers; each has a matching extracted text file.

- `andrieu_etal_2112.05605.pdf`: 721147 bytes; SHA256
  `56004ab5a7875601bc59277454d9eb10724a376e2acc9a134da9efc06d89162d`.
- `power_etal_2402.13678.pdf`: 825608 bytes; SHA256
  `5977c6ecc51ac478c21f5a37b669c776c6552a9b4a015f1ef0ac638b60d4f008`.
