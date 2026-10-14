# Independent audit of the ancestry prose intake

**Result.** The principal all-waveform map and ideal finite-bin recovery claim in the incoming source are already covered, more strongly, by N813's internal ancestry-information proof. The new scoped findings include pooled odd-carbon telegraph parity cancellation, a strict general Fisher-information loss under parity coarsening, a target-specific detector row-space criterion, and an exact one-carbon deletion channel that erases the synthetic C4 parity distinction. The intake also gives a conditional first-order mixing attenuation calculation and relies on an independent feed-label premise that remains physically unmeasured. Its eta a^8 scaling is correct for the ideal four-carbon even/odd local model with observable intact/fragment class and uninformative fragments, but it is not a universal detector law. A chemical-state mark measures conditional fate; it does not identify the effect of changing that state.

The most useful strengthened boundary is causal: even perfect recovery of the complete unordered entry-age law under every neutral feed waveform cannot identify the counterfactual response to an intervention on an internal chemical state. If the decision is about the effect of changing that state, the experiment must manipulate it and measure the outcome, or supply a separately justified model linking fate to intervention effect. This is not a general no-go for temporal coding: different entry-age laws remain identifiable under ideal real-valued controls, and N813's conditions for physical use remain open.

## Scope and pinned material

I read the supplied contract and pin, the N813 dossier, both N813 gates, the original temporal-ancestry note, and the N813 internal identifiability proof. The checkout pin is 1c45f77e32d6fbd72483aed5014061c7bda4f372; the incoming pasted file is 22,866 bytes with SHA-256 08b76f1d075c26857f6fb198147f3285d103a0579cc39139c9f7c63330f20d23, as recorded by the intake manifest. The ancestry input is prose only; no ancestry producer program or data set accompanies it. I wrote and ran a new standard-library Fraction checker in this directory. It imports and executes no source-directory code.

The current N813 status is source_derived_unreviewed. Its dossier says external correctness, novelty, and physical capability remain unknown; its review and capability gates are both open. The capability gate still asks for a real, isotope-neutral, stationary, whole-parent C4 count interface with measured inlet transfer, prehistory, and covariance, plus a chemistry-backed held-out decision against equally informed pulse, multipulse, and frequency-response baselines at matched total cost. The incoming prose supplies none of those measurements, so it cannot close either gate.

## Exact reconstruction

### 1. All-waveform entry-age observation map

Let a detected product contain n tracked carbon atoms with unordered feed-entry ages A_1,...,A_n. Conditional on those ages, assume independent labels with heavy-isotope probabilities p_i=p(t-A_i). For the intact product's heavy-carbon count K,

\[
  \mathbb E[z^K\mid A_1,\ldots,A_n]
  =\prod_{i=1}^n\bigl(1-p_i+zp_i\bigr),\qquad
  G_{\mu,p}(z)=\mathbb E_\mu\prod_i\bigl(1+(z-1)p(t-A_i)\bigr).
\]

This is a direct conditional-Bernoulli calculation. The count probabilities are the coefficients of G; the parity contrast is G(-1)=E[(-1)^K]. If two mechanisms have the same unordered joint age law mu, their one-product count laws agree for every prescribed waveform p, provided the ancestry law is independent of isotope composition and the label/count interface is the one assumed. This includes arbitrary shaped and periodic waveforms. It does not imply that any specified pair of real catalytic mechanisms has the same mu.

One-product equality is not equality of a time series. To couple whole records under adaptive controls, the conditional process kernels must agree after every possible selected-code history for the complete emitted-product/ancestry process, including product times and any shared input-carbon identities that can induce cross-product label dependence. Conditional independent labels are then coupled to the same input labels and detector randomness. Induction over adaptive choices gives identical records. This requires the stronger process-level equality and code-neutral chemistry; matching one-product marginals alone does not suffice.

For age bins j=1,...,B, let N_j be the occupancy count of a product's atoms in bin j. Under ideal independently selectable bin probabilities,

\[
  \Pr(K=n\mid p_1,\ldots,p_B)=\mathbb E\prod_j p_j^{N_j}.
\]

The right side is a multivariate polynomial whose monomial coefficient at exponent vector m, sum_j m_j=n, is Pr(N=m). Thus exact access to an open box of independently varied real probabilities identifies the unordered bin-occupancy law by polynomial interpolation. This is not a finite-cost reconstruction guarantee. It also does not follow from arbitrary timing of a binary-only feed: the interpolation argument needs an interval of values. N813 already records a six-atom, three-bin exact alias showing that even all binary masks can fail to identify the full unordered law.

The label-independence premise is substantive, not a consequence of measuring the marginal feed composition p(t). For example, two entries with p=1/2 each have count law (1/4,1/2,1/4) under independent labels, but (1/2,0,1/2) if a shared batch variable makes both labels equal to one common fair Bernoulli draw. Their ages and one-carbon marginals are identical, while the product-count law differs. Independent isotope assignment is a reasonable ideal model for separate carbon-bearing feed molecules drawn independently from a well-mixed reservoir; it still needs support at the declared feed boundary, including checks for shared batch fluctuations or common upstream labeling. If carbon atoms share a labeled molecule, or the effective p itself fluctuates across the atoms' entries, the product law must instead include the joint label distribution. Across products, reuse of the same feed-carbon identity can also create record-level dependence even when distinct feed molecules are independently labeled.

**Physical interface assessment.** The prose does not provide a measured joint-label calibration or establish that the actual reactor feed implements independent draws at every relevant entry time. Its ancestry identity is therefore conditional on that physical assumption, as is N813 equation (1); neither marginal isotope composition nor unchanged bulk yield proves label independence or isotope-neutrality. A real test should measure the boundary waveform and quantify relevant within-product label covariance (or validate the independent-feed sampling model), while separately measuring whether isotope substitution changes unlabelled chemistry.

**N813 comparison.** The incoming equation and same-law implication (source lines 27–48) duplicate N813 IDENTIFIABILITY.md equation (1), then restate a strict subset of Theorem 1 (lines 25–56), which proves that ideal interval-valued arbitrary controls identify the entire unordered age law. The incoming finite-bin polynomial (source lines 49–57) is also covered by that theorem's interpolation logic. N813 is stronger because it supplies the converse identifiability result, states the exact ideal-control and clock-alignment assumptions, separates it from finite-cost recovery, and warns that two-level controls do not imply arbitrary real-valued control. The new all-record qualification in the prose is useful but is a standard coupling extension; it does not alter N813's physical gate.

### 2. Odd-carbon pooled telegraph parity

For a fair stationary telegraph sign process sigma, the transformation of the entire path sigma -> -sigma preserves its law. For fixed entry times and odd n,

\[
  \mathbb E_\sigma\prod_{i=1}^n\sigma(S_i)
  =\mathbb E_\sigma\prod_i(-\sigma(S_i))
  =-\mathbb E_\sigma\prod_i\sigma(S_i),
\]

so the mean is zero. Averaging over any code-independent ancestry law preserves zero. With symmetric isotope levels, the corrected count-parity estimator has this pooled expectation; hence the random-phase, ensemble-averaged telegraph parity mean gives no ancestry signal for odd-carbon products such as C3 propylene. This does not make their full isotope counts or code-referenced time-series correlations uninformative. Conditioning on a realized sign, retaining its phase, or using an asymmetric/nonstationary code changes the observable. The cancellation is specifically for the fair stationary code average.

This is a valid new extension beyond N813's even-carbon n=2m construction. The exact code spot-check enumerates a five-time fair two-state chain with rational transition probabilities and returns zero; the proof is the path sign-reversal argument above.

### 3. Full count versus parity

Let q_k(theta) be a differentiable count law with a common positive support, and let m(theta)=sum_k (-1)^k q_k(theta). Coarsening to parity gives even and odd probabilities (1+m)/2 and (1-m)/2, hence

\[
 I_{\rm parity}(\theta)=\frac{m'(\theta)^2}{1-m(\theta)^2}
 \leq \sum_k\frac{q'_k(\theta)^2}{q_k(\theta)}=I_{\rm full}(\theta).
\]

For the inequality, the full score is s(K)=q'_K/q_K; the parity score is E[s(K)|(-1)^K]. Conditional Jensen proves the result. At boundary points where probabilities vanish, this statement is interpreted on common support or by a regular limiting family. For two fixed hypotheses, parity is sufficient only when their likelihood ratio is constant within each parity class. A raw product-count histogram contains at least as much information for these hypotheses as its parity reduction.

The inequality can be strict. The exact check uses K~Binomial(2,theta) at theta=1/4: I_full=32/3 while I_parity=64/15. But it is not strict for every model. In the incoming synthetic C4 E/O family, the histogram difference is proportional to v=(1,-4,6,-4,1), precisely a parity-only direction. There parity is sufficient for the one-dimensional E/O mixture parameter. Thus “full count dominates parity” is correct as a general inequality, not evidence that parity wastes information in the actual E/O witness. The raw histogram need not require a new experiment if the detector already records the bins; an analysis can choose its statistic after specifying the hypotheses.

### 4. Detector estimability and the one-carbon deletion counterexample

Let P in R^(n+1) be a normalized intact-product count vector, D a known linear calibrated response, y=DP, and 1^T P=1. A linear target w^T P is identifiable for every point of the full probability simplex exactly when

\[
  w\in\operatorname{rowspan}\begin{pmatrix}D\\1^T\end{pmatrix}.
\]

If w=B^T c, where B=[D;1^T], then w^T P=c^T B P is determined by the detector output and normalization. Conversely, if w is not in row(B), linear algebra gives v in ker(B) with w^T v not equal to zero. Since 1^T v=0, the positive and negative parts of v, normalized by their common mass, form two valid distributions with the same DP but different target values. This is structural non-identifiability: more repetitions estimate the same y more accurately but cannot recover that target. Near-row-span targets can still be practically ill-conditioned. The necessity direction is for the full simplex; known physical restrictions on feasible P can change it. Unknown backgrounds, intensity normalization, response drift, or position-dependent fragmentation must be included in the observation model before applying the criterion.

For the source's illustrative channel, one uniformly chosen carbon is deleted from a C4 parent and the remaining three-carbon heavy count is measured. The column-stochastic response is

\[
D=\begin{pmatrix}
1&1/4&0&0&0\\
0&3/4&1/2&0&0\\
0&0&1/2&3/4&0\\
0&0&0&1/4&1
\end{pmatrix}.
\]

The upper-left 4-by-4 minor is triangular with determinant 3/32, so rank(D)=4. Since each column sums to one, 1^T is the sum of D's four rows and normalization adds no rank. The exhibited nonzero v is therefore a basis for the one-dimensional nullspace.

For P_E=(1,0,6,0,1)/8 and P_O=(0,4,0,4,0)/8,

\[
DP_E=DP_O=(1,3,3,1)/8.
\]

More strongly, with v=(1,-4,6,-4,1)^T, Dv=0, 1^T v=0, and the C4 parity vector w=(1,-1,1,-1,1)^T has w^T v=16. Thus parity is not in the augmented row span and is not estimable from this channel for general intact distributions. The exact checker confirms the matrix is normalized and both full fragment distributions agree. This is an exact counterexample for an illustrative random-deletion model, not a fitted fragmentation pattern or a claim that a real mass spectrometer necessarily erases this signal. It sharpens N813's existing requirement for a calibrated whole-parent count response; that earlier warning is broader but does not include this explicit null-vector witness.

### 5. The eta a^8 information scaling

For the antiperiodic C4 E/O toy family, the complete intact-count laws can be written

\[
 q_k(\theta)=\frac{\binom4k}{16}+(2\theta-1)\frac{a^4v_k}{16},
 \qquad v=(1,-4,6,-4,1),
\]

where theta mixes E versus O, a is the isotope contrast, and 0<a<1. At theta=1/2, q_k=binom(4,k)/16 and q'_k=a^4 v_k/8. Therefore

\[
 I_{\rm intact}(1/2)=\sum_k\frac{q_k'^2}{q_k}=4a^8.
\]

All differences arise in the fourth-order direction v, so this exact model is also parity-sufficient at that point. If the detected record carries an observed intact/fragment indicator, intact occurs with probability eta independently of theta, and fragment records have no theta-dependence, then the Fisher information per detected event is 4 eta a^8. A nonzero fragment channel can add information; an unobserved intact/fragment mixture can instead make the exact factor depend on the mixture law. Without those conditions eta alone does not determine the total Fisher information. This is a local, ideal independent-event result for the stated four-carbon contrast, not a universal information law.

The supplied prose's scaling is correct on that scoped interpretation. N813 already records the same a^(-8)/N conditional sampling-variance penalty for symmetric four-carbon corrected parity, so the exponent is a dual restatement of an existing cost. The factor eta is new as an explicit intact-channel accounting parameter, but no eta, independent-event count, detector response, or covariance is acquired for a real platform. The exact checker at a=49/50, eta=2/3 obtains I_intact=4a^8 and I_total=4 eta a^8.

### 6. Chemical-state marking, fate, and causal intervention

Suppose an internal population A contains N_A initially eligible atoms. Mark each eligible atom with probability epsilon_m, independently of its later fate, using a persistent, neutral marker. For atom i, let F_i(T) count the number of qualifying transfers into product class P by time T; use a first-transfer indicator if the target is atoms entering P only once. If the mean transfer-rate density per eligible atom is h_(A->P)(t), then linearity gives

\[
M_P(T)=\sum_{i=1}^{N_A}B_iF_i(T),\quad
\mathbb E M_P(T)=\epsilon_m\sum_i\mathbb E F_i(T)
 =\epsilon_mN_A\int_0^T h_{A\to P}(t)\,dt.
\]

For random inventory, the right side must be averaged or conditioned consistently; if fate rates depend on inventory, one cannot simply multiply two marginal means. The equality also assumes selective eligibility, persistent marking, no mark-induced chemistry change, no scrambling that invalidates ancestry, known N_A, and unbiased calibrated detection. It is a conditional fate measurement, not yet a built operation.

Fate does not identify causal leverage. Let natural operation hold an internal state at A=0, with the same unlabelled product process, atom ancestry law, and marker/fate law in two candidate systems. Give them identical ordinary outcomes at A=0, but distinct intervention response functions near zero: J_0(delta)=j and J_1(delta)=j+c delta, where c is nonzero. Because neutral isotope coding changes only feed labels and not delta, the entire all-waveform isotope record can be identical in the two systems, while their causal derivatives at zero are 0 and c. Thus no statistic of those records identifies chi_A=dJ(I_delta)/d delta at delta=0 without additional assumptions. An active catalyst population can control rates without donating atoms; conversely, a population can donate atoms without being rate- or selectivity-limiting.

The prose uses epsilon first for mark fraction and then again for a chemical intervention family. These should be written as separate parameters epsilon_m and delta. Under a neutral mark, changing epsilon_m changes the amount of recorded tracer, not the chemistry; it does not estimate the effect of a chemical delta-intervention. If one instead manipulates A, collateral changes to acidity, transport, coverage, temperature, or feed must be measured or controlled. The paper's linear mark/fate equation is valid; interpreting it as a causal-response estimate would be invalid.

## Literature check and limits

Primary sources consulted are listed with DOI, version, and depth in READ_LEDGER.md. The central comparator is Hwang, Johnson & Bhan, Journal of Catalysis 369 (2019), 86–94, DOI 10.1016/j.jcat.2018.10.022. The publisher record/abstract reports site-specific labels at aromatic-methyl versus aromatic-ring positions, assigns tetramethylbenzene to the side-chain ethylene route and penta-/hexamethylbenzene to the paring propylene route, and says the propylene/ethylene selectivity ratio increased after deliberately shifting the trapped methylbenzene distribution toward the latter species. This is a strong established comparator for that HSAPO-34 question. Full paper, raw data, methods, and complete controls were not available in the retrieved publisher view, so this audit does not certify the causal size or transportability of that effect to H-ZSM-5.

The full 9-page final published Liu et al. ACS Catalysis paper (2023), DOI 10.1021/acscatal.3c00168, confirms isotope-switching sequences plus online MS/FASPA under quasi-steady conditions and reports C3+ aliphatic responses over mixed propylene/butane/propane fragments, including fast scrambling. It supports the source's detector caution but does not give a calibrated intact C4 whole-parent histogram. This evidence was already summarized in the N813 application note. Hartfelder et al. (2012), DOI 10.1039/c2an35903k, is described as a linear isotope-frequency response in its abstract; only the abstract was available. That supports the source's caution against claiming this paper proves the full nonlinear ancestry identity, but it cannot establish absence of other nonlinear methods or resolve priority.

Liu et al., Nature Communications 10, 1462 (2019), DOI 10.1038/s41467-019-09449-7, report that with MeOH plus labeled formaldehyde, product groups all near the feed's 13C fraction indicate rapid label scrambling under their studied conditions and prevent tracing the formaldehyde pathway; adding 1-butene changes the observed isotope pattern, and the authors hypothesize reduced scrambling because the chemistry consumes MeOH/HCHO faster. This is chemistry- and condition-specific, not a theorem that richer temporal codes always fail.

The cited 2026 Ezenwa et al. Journal of Catalysis article, 454, 116653, DOI 10.1016/j.jcat.2025.116653, is a primary 13-page paper. It reports selective cofeed poisoning of extracrystalline acid sites using 2,6-di-tert-butylpyridine during 403 K toluene methylation in MFI, with suitability validated on MCM-41. This is a genuine different site-targeted intervention in that regime; it does not validate selective marking under high-temperature methanol-to-olefins operation. It supports the conceptual distinction between molecular coding and chemically targeted intervention without supplying the hypothetical marker required by the pasted proposal.

## Duplication, new negatives, and stop/archival decision

| Incoming topic | Relation to N813 | Audit result |
|---|---|---|
| Conditional generating function, same-age-law all-waveform equivalence, and finite-bin count polynomial | Duplicates N813 IDENTIFIABILITY.md lines 7–56; N813's arbitrary-control theorem is stronger and already warns that binary inputs alone do not give full-law identification. | Correct under known n, independent labels, actual calibrated boundary waveform, isotope-neutral and code-independent ancestry, accounted prehistory, and whole-parent counts. Not new capital. |
| Independent feed labels | Assumed in both the pasted observation map and N813 equation (1); no real boundary-joint-label calibration is supplied. | Essential physical premise: a shared fair batch label gives a different count law than independent labels at identical per-carbon p. This is an exact assumption-failure witness, not evidence that a particular reactor feed is correlated. |
| C4 cosine mean and first-order mixing attenuation | The unfiltered cosine value follows by substitution into N813's general arbitrary-waveform formula (original note lines 144–148); the explicit mixing-filter calculation is new in this intake. | Average of 2 cos^4(phi) is 3/4; a first-order filter at omega=pi/tau attenuates the four-factor signal by [1+(pi t_mix/tau)^2]^(-2). Correct if the measured feed is the filtered sinusoid and the filter is linear, stationary, and in steady state. This conditional attenuation has not been measured on the candidate platform and is not a matched efficiency result. |
| Neutrality, startup/prehistory, finite samples, total resource match, C2 pulse equivalence, and synthetic C4 single-pulse limitation | Explicitly covered in the original N813 note lines 20–28, 109–126, 128–193, 205–227. | Repeated scope; no invalidation. |
| Odd-n pooled sign cancellation | Outside N813's stated even-carbon transform. | New valid scoped negative for the pooled fair stationary telegraph parity mean; does not rule out code-referenced or asymmetric-code statistics. |
| Fisher-information comparison of full count to parity | Not explicit in N813. The exponent a^(-8) sampling penalty is already there. | New generic data-processing theorem. Strict loss is possible, but parity is sufficient in the constructed E/O family, so no E/O-specific loss is established. |
| Target-specific detector row-span condition and random deletion witness | N813 already requires whole-parent counts and calibrated response matrices, but does not give this target-estimability criterion or the exact deletion alias. | New exact channel counterexample. It is illustrative, not empirical fragmentation evidence. |
| Intact fraction eta | Not an acquired N813 value; conditional sampling variance already carries a^(-8). | Correct local 4 eta a^8 FI under explicit class-label and uninformative-fragment assumptions; real eta, independent event count, and covariance remain UNKNOWN. |
| Chemical-state mark/fate vs intervention effect | Not an N813 mathematical result. | Correct distinction and useful causal-identifiability no-go. Mark operation itself remains physically hypothetical. Hwang provides a strong same-question HSAPO-34 comparator, not a transferable H-ZSM-5 result. |

The source's stop recommendation is defensible as a local portfolio decision for the specified HSAPO-34 methylbenzene/selectivity question: a primary study already reports the key state-specific atom tracing and a manipulated precursor distribution with a changed product-selectivity ratio. It is not a proof that isotope ancestry measurements are useless, nor does it establish that the N813 H-ZSM-5 C4 opportunity is resolved. Same-age-law equivalence does not cover mechanisms with different mu; the ideal N813 arbitrary-control theorem says those laws are separable in principle. The incoming report itself does not construct a real remaining mechanism pair, matched-cost comparison, or measured detector/readout. Therefore its wording must not be used to close N813's review/capability gates or turn an untested route into a general physical no-go.

**Decision-changing boundary.** For an observational ancestry question, first decide whether the target depends only on the unordered entry-age law; then choose the full-count likelihood statistic, verify the target lies in the calibrated detector row span, and compare actual waveform/detector/preparation costs. For a causal question about changing an internal population, isotope-only feed waveforms cannot cross the boundary even if they recover that entire law. Prioritize a real, selective intervention and measure J under matched controls; use state-conditioned marking only to measure fate, not as a substitute for causal response. If a different H-ZSM-5 target is retained, the N813 next gate remains a held-out real C4 decision with calibrated inlet waveform, intact-count response/covariance, measured startup, isotope-neutrality evidence, and equal-resource optimization against shaped/multipulse/frequency baselines. Total experimental costs, a physical state-selective marker, and any same-platform H-ZSM-5 held-out mechanism decision remain UNKNOWN.

## Independent exact artifacts

independent_checks.py uses only Python's standard-library Fraction and itertools. It checks the permutation-invariant count law, a same-marginal label-correlation counterexample, odd-telegraph cancellation at a finite exact CTMC instance, full-versus-parity Fisher information values, the C4 intact/fragment information calculation, the deletion matrix image/rank/normalization, and the detector null vector. The analytic proofs above supply the general statements; these finite checks establish only the reported arithmetic.

