# Literature boundary for an independence-MH prefix before a lazy hybrid

Prepared by `/root/prefix_literature`, 21 October 2026. This is a focused source check, not an independent proof of the owner's proposed prefix theorem. No owner proof or previous scientific operation was changed or rerun.

## Assessment

The proposed operation is ordinary independence Metropolis–Hastings (IMH) for an initial block, followed by the already specified lazy reversible mixture. Both the sampler and several of the strongest facts about its initial block are established. A contribution should therefore be framed as a **sharp robustness threshold for composition under the stated population information**, subject to a complete proof, rather than as a new sampler, a new importance-weight ordering, or a computational speedup.

The focused primary-source investigation did not locate either (i) the precise one-step removal of the reverse-KL leading coefficient for `q G C^t`, or (ii) the proposed forward-KL-only critical prefix constant `1 / [-log(1-exp(-K))]`. This does not establish historical novelty or priority. The exact IMH law makes such initial-block estimates close to existing machinery, so that dependence should be explicit.

## Closest exact result: known finite-budget IMH law

**Alexey Kurennoy, Ramil Yarullin, Fergal Reid.** *Metropolis–Hastings Dominates Importance Resampling for Policy Composition*. arXiv:2610.03480v1, 2 October 2026.

Primary source: <https://arxiv.org/html/2610.03480v1>; PDF: <https://arxiv.org/pdf/2610.03480v1>.

Its budget includes initialization: `H_N=qG^(N-1)`. Lemma 2 identifies this law with the largest `W(Y_i)/U_i` among iid proposals and independent uniforms. For a fixed tagged pool, equality uses randomized processing order. Equation (21), in normalized units, is

`dH_N/dpi(w) = N integral_0^(1/w) B(u)^(N-1) du`,

where `B(u)=E_q[(1-uW)_+]`. In particular this density is nonincreasing in `w`. Lemma 4 represents the output as a target distribution truncated at its maximum priority. Theorem 1 establishes ordinary IMH's same-budget dominance over SIR for convex f-divergences. These are appropriate starting facts and strong comparators, not new claims of the continuation.

Its principal theorem assumes positive common finite support. General measurable spaces require an extension by iid integration or a direct IMH proof. The paper attributes the marginal formula to Smith–Tierney's 1996 exact-transition work, restated in Wang's 2022 Theorem 4.

## General-measure threshold representation already available

**Seiyun Shin, Juhyeong Pang, Kwang-Sung Jun.** *Uniform Race: Parameter-Free Approximate Rejection Sampling*. arXiv:2609.34639v1, 28 September 2026.

Primary source: <https://arxiv.org/abs/2609.34639v1>; PDF: <https://arxiv.org/pdf/2609.34639v1>.

Section 1 uses Radon–Nikodym weights with `0<W<infinity` proposal-almost surely and arbitrary measurable test sets. Proposition 1 and Appendix B.2–B.3 supply a general-measure joint law. If `F(s)=E_q[(1-W/s)_+]` and `Lambda=max_i W(Y_i)/U_i`, then

`Pr(Y_winner in dy, Lambda in ds) = N F(s)^(N-1) s^(-2) 1{W(y)<s} pi(dy) ds`.

Integrating gives a mixture of normalized restrictions `pi(. | W<s)`. This formula can be used without assuming the existence of a separate abstract disintegration theorem: the measurable probability kernel is exhibited directly. Its Theorem 1 bounds TV by `inf_R { E_q[(W-R)_+] + (1-E_q[min(W,R)]/R)^N }`. It does not state the proposed hybrid-prefix threshold.

The priority rule itself is identical to the marginal IMH representation just described. Calling it an improved replacement for IMH at the same proposal budget would therefore be incorrect.

## Entropy-only cost scale is established

**Adam Block, Yury Polyanskiy.** *The Sample Complexity of Approximate Rejection Sampling with Applications to Smoothed Online Learning*. COLT 2023; corrected arXiv:2302.04658v3, 23 February 2024.

Primary corrected source: <https://arxiv.org/html/2302.04658v3>; proceedings: <https://proceedings.mlr.press/v195/block23a.html>.

They study selecting one of iid proposals under an f-divergence constraint, including the exponential sample cost under forward KL. The corrected tail estimate carries the asymptotic leading constant needed for sharp KL refinements. Consequently the `K` baseline is a precise specialization of existing sampling machinery, not a newly discovered entropy barrier. A prefix result concerns how safely that existing correction can be composed with another kernel.

This also distinguishes two costs: preparing a distribution safe for later smoothing need not already produce an epsilon-accurate sample. A logarithmic prefix, if proved, cannot be advertised as solving epsilon sampling in logarithmic cost; the subsequent mixing remains part of the operation.

## Functional-inequality comparison does not supply the new initialization step

**Christophe Andrieu, Anthony Lee, Sam Power, Andi Q. Wang.** *Comparison of Markov chains via weak Poincare inequalities with application to pseudo-marginal MCMC*. Annals of Statistics 50(6), 3592–3618 (2022); arXiv:2112.05605v2.

Primary source: <https://arxiv.org/abs/2112.05605v2>; PDF: <https://arxiv.org/pdf/2112.05605v2>.

Proposition 28 gives IMH a weak Poincare bound controlled by the target mass of large importance weights. Theorem 22 converts such inequalities to decay; comparison results transfer them to other reversible positive kernels. Remark 12 separately requires control of a functional of the initial density to infer TV convergence. Thus Dirichlet comparison alone does not justify replacing a warm start with `q`, or the new prefixed law. The prefix construction should explicitly supply the missing initial-law estimate and preserve constants when using the anchored observable argument.

## Closest local/global algorithmic comparison has stronger hypotheses

**Sergey Samsonov, Evgeny Lagutin, Marylou Gabrie, Alain Durmus, Alexey Naumov, Eric Moulines.** *Local-Global MCMC kernels: the best of both worlds*. NeurIPS 2022; arXiv:2111.02702.

Primary proceedings: <https://papers.neurips.cc/paper_files/paper/2022/hash/21c86d5b10cdc28664ccdadf0a29065a-Abstract-Conference.html>.

Theorem 2 treats local/global composition with local drift, level-set likelihood-ratio bounds and a finite weight second moment. Those constants are useful for an actual numerical comparison, but they are not provided by a forward-KL budget alone. A uniform impossibility or a sharp prefix threshold over the larger entropy-only class is compatible with their geometric convergence theorem for its smaller class.

## Nearby warm-start work, screened rather than imported

Two primary records confirm that constructing a short preliminary phase for a later adjusted sampler is a familiar general strategy:

- **Jakob Robnik, Uros Seljak**, *Faster Parallel MCMC: Metropolis Adjustment Is Best Served Warm*, AISTATS 2026, PMLR 300:2719–2727: <https://proceedings.mlr.press/v300/robnik26a.html>. Its abstract describes an ensemble-adapted unadjusted phase followed by adjusted MCMC. This is a different operation, and no theorem from it is used here.
- **Nawaf Bou-Rabee, Siddharth Mitra, Andre Wibisono**, *Tail-Sensitive KL and Renyi Convergence of Unadjusted Hamiltonian Monte Carlo via One-Shot Couplings*, arXiv:2601.09019v1: <https://arxiv.org/abs/2601.09019v1>. Its abstract describes upgrading Wasserstein information through transition smoothing to density-sensitive bounds useful for warm starts. This is a different kernel and set of regularity hypotheses; its abstract alone does not establish an overlap with the precise proposed prefix threshold.

The proximal-posterior method of Chen–Biros, arXiv:2602.21426v2, was also screened at its primary abstract. It modifies the proposal via an auxiliary optimization rather than performing the proposed fixed IMH prefix; no theorem or implementation claim from it is imported.

## Mechanistic and novelty boundaries to retain

1. The output still begins from an iid proposal and uses ordinary MH acceptance with unnormalized weights. The prefix creates no new sampling primitive.
2. Existing marginal and priority formulas already explain why proposal-overweight low-weight mass can shrink by a power of its original probability. Any use of that mechanism must credit the sources above.
3. A theorem for `qG^m C^t` is a distinct initialized operation. It does not revise the accepted coefficient for the original `qC^t` contract.
4. The best ordinary comparison is pure proposal-start IMH, at matched total proposal counts. SIR cannot be substituted as the supposedly strongest baseline.
5. Matching pure IMH's worst-case exponential coefficient would establish robustness to later fixed reversible local updates. It would not establish lower finite-time error, shorter wall time, useful stationary variance, or empirical benefit on an application.
6. The forward-only threshold, if proved, must distinguish finite fixed `m`, an epsilon-dependent deterministic prefix, finite uniform mixing above the threshold, the leading constant in subsequent mixing, and any unresolved critical window. Neither a toy matrix calculation nor a limiting singular pair establishes those distinctions on its own.

## Source and execution record

Read the preserved literature note; the relevant full-text sections of the four local primary papers above (Kurennoy, Shin, Block via current HTML, Andrieu); and current official records for Samsonov and the screened recent warm-start methods. Used both available web search engines for focused queries about IMH initialization, warm starts, composition, entropy and exact transitions. Several literal queries returned irrelevant results; these were not treated as evidence. The current Uniform Race HTML request timed out, while its primary abstract and preserved full PDF text were available.

No new dataset was acquired, no scientific simulation was run, and no model, package or hardware was installed. No priority claim follows from the bounded search. No external recipient was contacted. Source hashes for reused PDFs and a retrieval summary are in the companion `prefix_literature_sources.json`.
