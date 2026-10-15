# PyGT and spectral-subspace-sparsification incumbent dossier

Acquisition and source review for the comparison requested in `computation_pasted.txt`. This dossier was assembled on 2026-10-15. It is a source inspection only: neither downloaded implementation code was executed, no package was installed, and no baseline runtime or benchmark result is claimed.

## Pinned PyGT implementation

`PyGT/` is a fresh clone of `https://github.com/tomswinburne/PyGT.git`, checked out detached at full commit `fa0e106958d9948209daff04360290d50de82572` (commit date 2023-03-26; message `Update README.md`). The checked commit matched the live `master`/`HEAD` returned by `git ls-remote` at acquisition. The project identifies itself as PyGT 0.3.0 (2020), a beta implementation of graph transformation for metastable Markov chains. The clone contains source, Sphinx documentation source, examples, setup metadata, and `LICENSE`.

The repository declares MIT in `setup.py` and the GitHub API reports SPDX `MIT`. The checked-in `LICENSE` grants the standard MIT permissions but its copyright line names “The Python Packaging Authority,” while the README names TD Swinburne and D Kannan as the project authors. That attribution discrepancy is preserved as received; see `PyGT/LICENSE` and `PyGT/README.md`. Do not silently replace the license file or assert that its copyright header was independently verified.

`setup.py` declares Python `>=3.6`, `scipy>=1.5`, `numpy>=1.17`, `matplotlib>=3`, `tqdm>=4.47`, and `pathos>=0.2`. None was installed or checked as a precondition because no execution was attempted.

## What PyGT already carries

The interface is a general finite CTMC, not a reversible-only capacity solver. Its column convention is `B_ij = k_(i<-j) tau_j`, where each column holds the branching probabilities out of state `j`; `tau_j` is its mean exponential sojourn time. `PyGT.tools.load_CTMC` converts an input rate matrix to `B` and `tau` (`PyGT/PyGT/tools.py:206-230`). `PyGT.io.load_ktn` can instead build rates and waiting times from an energy-landscape `min.data`/`ts.data` pair (`PyGT/PyGT/io.py:118-168`, `204-274`).

For a removed set `X` and retained set `Y`, the documented transformation is the stochastic Schur complement

`B' = B_YY + B_YX (I - B_XX)^(-1) B_XY`.

The code also updates the retained-state waiting-time vector using the Green matrix for visits through `X`. Thus it carries two key dynamic quantities through elimination: all path branching probabilities among retained states and expected waiting time accumulated on paths through eliminated states. The associated 2020 JCTC paper derives the waiting-time update by differentiating path-weighted branching matrices and states that GT preserves these expected waiting times and branching probabilities for the reduced network (downloaded paper, pp. 3–5; the arXiv/author manuscript is linked below). This is not preservation of the full first-passage-time distribution or its higher moments.

For a pair of singleton endpoints, `PyGT.mfpt.compute_MFPT(i,j,...)` marks `i` and `j` retained, transforms away every other state, then returns both directional MFPTs as the retained waiting time divided by the corresponding two-state branching probability (`PyGT/PyGT/mfpt.py:197-248`). It does not require `pi` for this pairwise calculation. This is directly stronger than a symmetric terminal response when the requested output is directional lifetime. The function's default `block=1` means the default path performs one-node elimination; `blockGT` itself has a separate default block size of 20 (`PyGT/PyGT/GT.py:66-114`, `mfpt.py:215-218`). A caller can choose a larger block, subject to conditioning and fill.

PyGT does not expose an occupation-weighted committor numerator under that name. It exposes the directional MFPT and, for sets, weighted MFPTs. Treat that as an equivalent final-output comparison only after checking the candidate's exact normalization identity; otherwise keep the direct-numerator interface distinction explicit.

For endpoint *sets* and occupation-weighted initial ensembles, `PyGT.stats.compute_rates` takes the stationary weights `pi`; by default it normalizes `pi` within each basin, or accepts caller-supplied `initA`/`initB`, and returns directional MFPTs and several rate conventions (`PyGT/PyGT/stats.py:208-282`, `297-368`). Its documented `fullGT` path can transform each source state separately when a direct reduced solve is judged ill-conditioned. This interface requires the occupation weights as input. The `blockGT` result itself is only `(B', tau')` (optionally also a reduced rate matrix); it does not return a transformed occupation-weight vector (`PyGT/PyGT/GT.py:104-114`, `230-232`). The separate approximate community/spectral reducer does return projected left/right stationary vectors and optional projected initial distribution, and selects modes using escape-time-moment tolerances (`PyGT/PyGT/spectral.py:1-73`, `116-192`).

The separate `compute_passage_stats` interface consumes `pi` and the full rate matrix, computes both directions' first and second FPT moments, and can return the FPT density by eigendecomposition of the absorbing submatrices (`PyGT/PyGT/stats.py:54-142`). `compute_escape_stats` similarly computes basin escape moments/distribution (`stats.py:144-206`). In the JCP paper, graph transformation is the reference route for MFPTs, while eigendecomposition is reported to lose numerical precision in rare-event regimes and kinetic-path sampling is used for higher FPT-distribution information (paper abstract and conclusions, pp. 1 and 18–20).

### Precision and cost boundary

PyGT's stability design is real and relevant. Block removal estimates `cond(I-B_XX)` and refuses block inversion above `cond_thresh=1e13` or after a linear-algebra exception, allowing the outer routine to retry one state at a time (`GT.py:99-103`, `147-199`, `282-309`). For a state with a self-loop probability above 0.99, the scalar path computes the escape denominator from the sum of off-diagonal branches instead of subtracting two nearly equal numbers (`GT.py:310-326`). The module documentation explicitly describes this as a floating-point correction (`GT.py:235-269`). The 2020 paper gives the same cancellation-avoiding identity, replacing `1-B_ll` by the sum of other outgoing branches (JCTC paper, p. 4).

The implementation uses NumPy/SciPy floating-point arrays and ordinary matrix inversion/solves. It has no directed rounding, interval output, or end-to-end relative-error certificate for the final flux or MFPT. Its condition threshold is a guard on block inversion, not a proof of final forward error. The JCP paper says graph transformation reaches MFPTs in strongly metastable examples while eigendecomposition encounters low-temperature precision problems; that literature result does not certify this particular input or software run.

The repository gives no asymptotic or measured runtime guarantee for the complete pairwise elimination. `blockGT` may create fill, switches to dense storage below `N=50`, and performs matrix products for block updates (`GT.py:147-218`, `282-328`). For a single pair, the code can be asked to reduce a full supplied graph; the full graph, waiting times, and any occupation weights still have to be acquired and held. The Python package's default pair-MFPT elimination is one-node-at-a-time. The cost may therefore depend heavily on elimination order, fill, and block conditioning; no performance number is inferred here.

## Li–Schild: direct incumbent for the terminal response

The primary source is Li and Schild, *Spectral Subspace Sparsification*, arXiv:1810.03224 / FOCS 2018. Its definition guarantees, for every demand `x` in a selected subspace `S`, a reweighted graph minor `H` with

`(1-epsilon) x^T L_G^+ x <= x_H^T L_H^+ x_H <= (1+epsilon) x^T L_G^+ x`.

For the single terminal pair `s,t`, take `x=b_st=e_s-e_t`; then `x^T L^+ x=R_st`, the effective resistance. In the reversible CTMC setting of the pasted task, `c_ij=w_i q_ij` defines the undirected conductance Laplacian, `C_st=1/R_st`, and `nu_st=C_st/Z=1/(Z R_st)`. Consequently, a multiplicative effective-resistance approximation is a multiplicative approximation to the requested terminal flux after inversion, provided `Z` is independently known to the required precision. The SSS theorem does not compute the partition function or certify uncertainty in the `w_i`/`q_ij` inputs.

The paper's terminal-set theorem constructs an `epsilon` subspace sparsifier with `min(m, O(|S| polylog(n)/epsilon^2))` edges in random-spanning-tree time plus `O(m polylog(n))`, stated as `m^(1+o(1))`. Its effective-resistance corollary gives `m^(1+o(1)) + Otilde(|P|/epsilon^2)` time for specified pair queries. For one pair, this is a direct theoretical response to the candidate's terminal-capacity output. The graph is the full weighted input; the theorem does not avoid reading/acquiring it. The guarantees are randomized/theoretical and the paper uses approximate uniform random spanning trees and Laplacian-solver primitives.

This output is narrower than PyGT's kinetic interface: SSS preserves a symmetric Laplacian pseudoinverse response. It has no `tau`/mean-sojourn state, does not return directional MFPTs or FPT distributions, and does not carry stationary occupation weights. Conversely, it is directly response-focused and uses the same broad contraction/deletion/reweighting family as the candidate. It is therefore close prior art for claims of novelty in terminal-specific graph contraction/deletion, even though it is not a kinetic simulator.

### Code status and precision

I acquired the full arXiv source tar and PDF and searched the source text for software, GitHub, and implementation references. The PDF provides theorem statements, algorithm pseudocode, and proofs. In particular, its `ResApx` pseudocode is captioned “never executed” (`primary_papers/res-apx.tex:13-44`); it is not a tested implementation receipt. A GitHub repository search for the exact work title returned zero repositories, and neither author publication page links an implementation. This is bounded evidence that no public code was located in those sources/searches, not proof that no private or differently named implementation exists. No SSS code license can be assigned from these materials; the acquired arXiv TeX is a paper source package, not software.

The paper states a multiplicative `1+epsilon` response error and algorithmic runtime, but the materials inspected supply no executable arithmetic/error-budget certificate for exponential kinetic weights. No numerical precision extension, partition-function computation, or physical-rate uncertainty guarantee is being attributed to Li–Schild.

## Comparison interfaces to preserve

| Output axis | PyGT at the pinned revision | Li–Schild SSS | Consequence for the candidate |
|---|---|---|---|
| Terminal response | Can reduce a CTMC to two kept states; its directional MFPT is read from reduced branching probabilities and waiting time. It also computes rates/MFPTs for sets. | Direct multiplicative approximation of `R_st`; for reversible rates this gives `C_st` and then `nu_st` if `Z` is supplied. | Treat terminal capacity/flux as already addressed by a direct graph response theorem; compare complete costs and required precision. |
| Mean waiting time | Carries updated mean waiting time on retained states through graph transformation. | No waiting-time state. | A certificate for `tau`-weighted directional response may distinguish the outputs, but PyGT already has a direct directional-MFPT routine. |
| Occupation weights | Consumes `pi`/custom initial occupation for weighted basin statistics; `blockGT` does not itself return a transformed `pi`. A separate spectral community reduction projects stationary vectors. | No occupation-weight state. | The comparison must charge acquisition of `pi` and determine whether a claimed numerator can be obtained from PyGT's exact endpoint MFPT API. |
| Direction/FPT law | Pairwise code returns both MFPT directions. Additional routines compute moments/distributions, with eigendecomposition precision caveats. | Symmetric resistance only. | A new directional-lifetime claim should be compared to PyGT's per-direction exact-GT interface, not only to terminal resistance. |
| Precision evidence | Stability guard and cancellation avoidance in float arithmetic; no outward interval/certification. | Randomized multiplicative theorem; no executable code or kinetic-scale arithmetic certificate found. | Preserve theorem-vs-implementation distinctions; no head-to-head execution exists in this intake. |
| Complete-input cost | Requires supplied full transition graph/rates and possibly `pi`; elimination fill and pairwise reduction dominate, with no source-based runtime guarantee. | Requires supplied weighted graph; stated near-linear input-processing plus query term. Does not calculate `Z`. | Candidate's graph acquisition and partition normalization remain charged; state-count reduction alone does not settle cost. |

Neither implementation was executed in this tranche. The local copy is for audited reading and future controlled comparison only. No run was attempted and no dependencies were installed.

## Local source map

- PyGT code and license: `PyGT/` (detached at the full SHA above). Highest-value files: `PyGT/PyGT/GT.py`, `mfpt.py`, `stats.py`, `tools.py`, `io.py`, `spectral.py`; `README.md`, `setup.py`, `LICENSE`; Sphinx source in `docs/`.
- Captured official rendered docs: `source_receipts/pygt_readthedocs_GT.html`, `pygt_readthedocs_mfpt.html`, `pygt_readthedocs_tools.html`.
- Li–Schild primary paper: PDF and arXiv source in `primary_papers/li_schild_2018_spectral_subspace_sparsification.pdf`, `li_schild_2018_source.tar`, and extracted `.tex` files. Key lines: `intro.tex:3-14`, `26-54`; `res-apx.tex:6-44` (includes explicit unexecuted-pseudocode caption).
- PyGT primary manuscripts: `primary_papers/swinburne_wales_2020_jctc_kinetic_transition_networks.pdf` (23 pp) and `swinburne_kannan_sharpe_wales_2020_jcp_first_passage.pdf` (21 pp), plus text extractions for searching.
- Acquisition URLs, API snapshots, live refs, hashes, and search record: `source_receipts/` (manifest is `SOURCE_MANIFEST.json`).

## Primary source links

- [PyGT upstream repository](https://github.com/tomswinburne/PyGT) and [pinned commit](https://github.com/tomswinburne/PyGT/tree/fa0e106958d9948209daff04360290d50de82572).
- [PyGT graph-transformation API docs](https://pygt.readthedocs.io/en/latest/GT.html), [MFPT API docs](https://pygt.readthedocs.io/en/latest/mfpt.html), and [tools docs](https://pygt.readthedocs.io/en/latest/tools.html).
- Swinburne and Wales, [*Defining, Calculating, and Converging Observables of a Kinetic Transition Network*](https://doi.org/10.1021/acs.jctc.9b01211); [Cambridge author manuscript](https://api.repository.cam.ac.uk/server/api/core/bitstreams/a12ad43b-9a0b-4aab-b330-54ba390bb9e2/content).
- Swinburne, Kannan, Sharpe, and Wales, [*Rare Events and First Passage Time Statistics From the Energy Landscape*](https://doi.org/10.1063/5.0016244); [Cambridge repository PDF](https://api.repository.cam.ac.uk/server/api/core/bitstreams/d3215c82-b9a5-4e83-ab6a-5d164429c79a/content).
- Li and Schild, [*Spectral Subspace Sparsification*](https://arxiv.org/abs/1810.03224); [author-hosted paper PDF](https://aschild.github.io/papers/sss-camera.pdf); [Huan Li's publication page](https://huanli.me/); [Aaron Schild's publication page](https://aschild.github.io/).
