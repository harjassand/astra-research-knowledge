# Primary-source check

Sources were checked on 10 October 2026. This is a targeted collision screen,
not an exhaustive novelty search. Statements below distinguish implemented
results, theory, and proposals. None establishes originality of this pass.

## Local simulation reuse

- Buhr, *Towards Automatic and Reliable Localized Model Order Reduction* (2019),
  https://arxiv.org/abs/1908.02074 . ArbiLoMod explicitly combines localized
  training, a localized a posteriori error estimator and enrichment, with reuse
  for successive simulations of locally changed geometry. Direct collision with
  the broad initial cache idea.
- Buhr and Smetana, *Randomized Local Model Order Reduction* (2017),
  https://arxiv.org/abs/1706.09179 . Random boundary solves approximate local
  transfer ranges with probabilistic adaptive error estimation. This blocks
  presenting a random local boundary-response bank as a fresh primitive.
- Ohlberger and Schindler, *Error Control for the Localized Reduced Basis
  Multiscale Method with Adaptive On-Line Enrichment* (2015),
  https://doi.org/10.1137/151003660 . Certified local error estimation and
  adaptive enrichment already exist for heterogeneous elliptic problems.
- Beckermann, Kressner and Schweitzer, *Low-Rank Updates of Matrix Functions*
  (2018), https://doi.org/10.1137/17M1140108 . Krylov low-rank matrix-function
  updates are another established baseline, not a new response-cache invention.

## Transformer cache reuse and certification

- Yao et al., *CacheBlend: Fast Large Language Model Serving for RAG with Cached
  Knowledge Fusion*, https://arxiv.org/abs/2405.16444 . Implements non-prefix
  KV reuse with selective recomputation. The reported gains are empirical
  quality/latency results; do not reinterpret them as exact next-token proofs.
- Zhang and Ilvovsk, *Thesis Proposal: Efficient KV Cache Reuse for
  Multi-Document Retrieval-Augmented Generation* (EACL SRW 2026),
  https://aclanthology.org/2026.eacl-srw.11.pdf . Full paper inspected. It proposes
  position alignment, attention perturbation bounds, document mass accounting,
  margin preservation, and depth-wise gating/recomputation. Its proposal status
  matters: future tense and proposed contraction conditions are not evidence of
  an implemented exact-preservation algorithm. Nonetheless it is direct prior
  conceptual overlap with the certificate idea, so that idea cannot be claimed
  new merely because approximate cache reuse lacks exact guarantees.
- Shi et al., *Robustness Verification for Transformers* (2020),
  https://arxiv.org/abs/2002.06622 . Already handles cross-position and
  cross-nonlinearity dependence with stronger bounds than naive interval
  propagation. Generic correlated affine verification is not a fresh invention.
- Bonaert et al., *Fast and Precise Certification of Transformers* (PLDI 2021),
  https://files.sri.inf.ethz.ch/website/papers/pldi21-transformers.pdf . A primary
  baseline for transformer robustness certification rather than edit acceleration.
- Zhang et al., *GaLileo: General Linear Relaxation Framework for Tightening
  Robustness Certification of Transformers* (AAAI 2024),
  https://ojs.aaai.org/index.php/AAAI/article/view/30180 . Exploits softmax-input
  dependencies for tighter certification; correlated relaxation is crowded terrain.

## Native computational costs and limits

- Alman and Song, *Fast Attention Requires Bounded Entries* (NeurIPS 2023),
  https://arxiv.org/abs/2302.13214 . Nearly linear approximation is possible in
  one bounded-entry regime; a different entry scale gives conditional
  subquadratic hardness under SETH. These are precise input regimes, not a
  blanket impossibility theorem for edits of a cached network.
- van den Brand, Song and Zhou, *Algorithm and Hardness for Dynamic Attention
  Maintenance in Large Language Models* (2023),
  https://arxiv.org/abs/2304.02207 . Gives dynamic attention update/query
  tradeoffs and conditional lower bounds. Its dynamic model must not be silently
  substituted for the full deep-network edit task.

Recent adjacent items inspected at abstract/page level only:

- *KVShareArena: KV-Cache Reuse Across Contexts and Model Checkpoints*,
  https://arxiv.org/abs/2609.10266 . Relevant benchmark and cost-accounting
  context; not used for a theorem claim in this report.
- *Error Certificates for KV-Cache Eviction via Randomized Design*,
  https://arxiv.org/abs/2607.21475 . Eviction-certificate work is adjacent; not
  treated as deterministic multi-layer non-prefix cache equivalence.
- *Request Order Matters: Cache-History Sensitivity in Selective KV-Cache Reuse
  for Rolling Agents*, https://arxiv.org/abs/2610.05833 . Reports sensitivity to
  history in a rolling-agent workload. Motivation only; no reported benchmark
  figure is used as evidence for the new proposal.

A current author-maintained draft implementation at
https://github.com/jonsmirl/ssa/blob/main/paper/subquadratic_attention.md
also discusses block key/value certificates and the problem of lifting local
bounds through deep transformers. It is not used as an authoritative theorem
baseline, but it is further reason not to call block summaries novel.
