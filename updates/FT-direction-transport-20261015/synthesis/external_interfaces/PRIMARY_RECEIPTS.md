# Primary-source receipts and comparator boundaries

Date: 15 October 2026. All technical claims below were checked against actual primary text. Search results were navigation only. Source snapshots remain in scratch `sources/` and are excluded from the authored delivery inventory. Exact acquired bytes and SHA256 hashes are in FETCH_RECEIPTS.json and source_manifest.json. Equations in LOAD_TASK_QUOTIENT.md are independently reconstructed; they are not quotations or claims of historical novelty.

## 1. Nonreciprocal reconstruction: the load-control comparator

Philipp del Hougne, *Virtual VNA 3.0: Unambiguous Scattering Matrix Estimation for Non-Reciprocal Systems by Leveraging Tunable and Coupled Loads*, [arXiv:2503.07239v1](https://arxiv.org/html/2503.07239v1), 10 March 2025.

Actual read: Sections III, IV-A2--IV-A6, IV-B1 and V-A--V-C; particularly Eqs. (1),(11)--(25), the paragraph preceding Eq. (1), and experimental acquisition description. Web extraction ranges: lines 112--131,164--297,308--323,344--370. The full source HTML was acquired and hashed.

Source claim: known individual and coupled loads permit nonreciprocal full terminal-scattering estimation. Steps 2--4 leave a correlated diagonal scaling, Eq. (25); later coupled-load steps remove it. The closed-form full-characterization count is 1+3Ns+Ns(Ns-1)/2 load configurations for Na>2, with one further setting when Na=2. The experiment uses four actual and four virtual ports on an eight-port transmission-line DUT containing four circulators; its 19 settings each acquire a transfer matrix. Actual measurements span 401 frequencies,450--700MHz,500Hz IF bandwidth,12dBm power. Those are the researchers' acquisition settings, not a time/energy budget for this candidate.

Reconstruction: the remaining diagonal gauge cancels for every diagonal-load task. Our proof gives an explicit two-input/two-output recovery with pair-rank assumptions; it does not infer these assumptions from port count. Neither source experiment nor our exact examples certify arbitrary microscopic nonreciprocity support.

## 2. Rank-one differential response is acquired behavior, not a support certificate

Philipp del Hougne, *Frozen differential scattering in reconfigurable complex media*, [arXiv:2509.09506v1](https://arxiv.org/html/2509.09506v1), 11 September 2025. Publisher record [DOI10.1002/lpor.202502660](https://doi.org/10.1002/lpor.202502660) is available for the 2026 publication. The authored proof here uses the pinned preprint text, not an assumed identity of all publication revisions.

Actual read: Sections2.2.1--2.2.2,3 and supporting coupled-dipole proof; web lines77--113,277--287. The HTML was acquired and hashed. The paper factors the differential matrix for a qualified one-lump perturbation; no reciprocity is needed for that factorization. Its experiment uses eight antennas,225 meta-atoms, changes one PIN diode, and operates at2.45GHz. Measured rank is approximate; the primary text explicitly notes finite perturber size. A dominant observed singular direction does not prove a unique microscopic support or absence of other unobserved changes.

The 2026 publisher page was search-visible, but a direct web open failed. Search-visible data-availability text says data are available on reasonable request. No raw experimental data or author code was obtained or reanalysed here, and no request was sent.

## 3. The original Virtual VNA is a reciprocal comparator

Philipp del Hougne, *Virtual VNA: Minimal-Ambiguity Scattering Matrix Estimation with a Fixed Set of Virtual Load-Tunable Ports*, [arXiv:2403.08074v3](https://arxiv.org/html/2403.08074v3). Published metadata: [IEEE TIM DOI10.1109/TIM.2025.3551897](https://doi.org/10.1109/TIM.2025.3551897).

Actual read: SectionII-A and SectionIV, web lines104--131,351--373; noise/acquisition discussion lines408--415. Its stated assumptions include reciprocity. Its accessible loaded-scattering and impedance formulas are standard. It discusses tasks where internal ambiguities are harmless, and warns that closed-form recovery degrades when one-/two-load differential responses approach measurement noise. This rules out treating internal-gauge tolerance, three-load calibration, or low-rank difference recovery as a new broad principle. No experimental error number is transferred to our theorem.

## 4. Known intertwiners are a cheaper comparator in their actual class

Cyrill Bösch, Yiğithan Gediz, Clara C.Wanjura and Hakan E.Türeci, *Unifying Physical Backpropagation*, [arXiv:2608.11585v2](https://arxiv.org/html/2608.11585v2), revised23 September2026. Version availability and date were verified from the primary arXiv record; full HTML was fetched.

Actual read: Section9 and9.1, web lines694--790. Eq.(79) requires a known invertible transformation fixed throughout the experiment, satisfying the transpose-intertwining identity at every time. The proof substitutes the transformed adjoint, Eq.(85). Its implementation paragraph requires transformed drive/initial-condition access and inverse-weighted recovery, and states one additional finite-amplitude run. Parameter-dependent transformations must be recalibrated; condition number sets dynamic-range cost. The nonlinear case has additional trajectory and time-reversal obligations and is not imported here.

This is an equally informed, potentially cheaper comparator when the physical transformation and access already exist. It does not provide experimental discovery of an arbitrary unknown intertwiner or guarantee that the transformed excitation is accessible.

## 5. The 2026 RLC experiment exists; broad access is not automatic

Hoyeong Kwon, Arunn Suntharalingam, Laureano Bulus-Rossini and Tsampikos Kottos, *In-situ Time-domain Physical Adjoint Optimization of Complex Wave Dynamics*, [arXiv:2608.19456v1](https://arxiv.org/abs/2608.19456v1),19 August2026.

Actual PDF acquired:23 pages. Read pp.3--4,6--8,14--15. Page14 was extracted and rendered with macOS sips, composited over a white page for inspection, and visually checked. Its displayed Theta block and operator identity match the extracted equations. Our verifier independently checks HTheta=ThetaH^T for diagonal capacitance/conductance blocks and symmetric inductive block.

The paper reports a coupled RLC tetramer and chain implementation, discretized tuning, and finite updates guided mainly by gradient sign. Its demonstrated circuit does not establish arbitrary nonreciprocal apparatus coverage merely because its mixed-state first-order H is nonsymmetric. The existence of the displayed transformation does not alone establish transformed source/readout access in a different plant. Full supplementary derivations and raw data were not obtained, and no replication or experimental gradient-error estimate is claimed. The direct HTML endpoint failed; the actual PDF, not an abstract alone, supports this scoped comparator.

## 6. Compact learned models already provide open-loop wave control

Jérôme Sol, Hugo Prod'homme, Luc Le Magoarou and Philipp del Hougne, *Experimentally realized physical-model-based frugal wave control in metasurface-programmable complex media*, [Nature Communications15,2841(2024)](https://doi.org/10.1038/s41467-024-46916-2).

Actual publisher HTML acquired despite a cookie-warning query string. Read Results/Physical model, Discussion, Methods/Physical-model calibration and Data/Code availability. Local text read ranges434--543,780--830,834--896,1179--1182. The article estimates compact reciprocal interaction models for an unknown programmable scattering medium and uses them for open-loop control. It explicitly accepts parameter nonuniqueness when the task transfer agrees. It demonstrates model calibration using partial and/or phaseless observations; such capability is existing prior art, not established by our coherent theorem.

Data availability points to the paper and supplementary material. Code is available upon request; none was obtained, requested, or executed. No source-trained experimental model, measured performance ratio, or error distribution is reused here. The present exact finite reconstruction is a restricted analytically auditable comparator, not a demonstrated improvement on their fitting procedure.

## 7. Current OpenAI/math pin and actual relevance check

Current [openai/math](https://github.com/openai/math) main was freshly read through the GitHub API and pinned at1581d4cbdd69a0faf34b2089614fe2a814316a6a. Complete current preprints tree df0564b2deaab87e07854b6344d8c2f037682e77 was fetched (13,223 entries;not truncated), and is structurally identical to the old navigation snapshot. No older proof receipt was presumed current merely from a title.

Selectively fetched actual proof files for *Backward intertwiners and a transitive commutant*: full `introduction.tex` and `intertwiner.tex`. Raw Git blobs were recomputed and matched the current tree. The actual proof constructs a bounded commuting weighted backward shift by a two-ended coefficient recurrence and measurable normalization. Its concluding paragraph explicitly asserts density instead of surjectivity and does not assert a bounded inverse. Therefore it supplies neither the required acquired invertible transpose intertwiner nor a finite-load identification protocol. No theorem from it is imported, and its wider hyperinvariant-subspace claim was not audited. This is a rejected transfer after reading the actual proof, not a terminology analogy.

## 8. What was not established

No false future citation was found among the two checked2026 adjoint references. That availability result is separate from theorem correctness or independent validation of their reported experiments. No priority search establishes historical novelty. No measurements from the cited experiments establish the incoming closure model's joint noise, all-profile fixed operator, hidden reciprocity, actuator derivatives or practical dominance. Those remain actual acquisition obligations.
