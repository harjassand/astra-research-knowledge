# FL isotope-prior audit: joint ancestry versus isotope transients

**Date:** 14 October 2026  
**Scope:** Compare the proposed joint temporal-ancestry observable with primary isotope-transient, isotope-pulse, and nonlinear frequency-response methods.  
**Status:** Full text of Hartfelder et al. (2012) was not accessible in this run, so its exact coverage remains unknown. The audit does establish substantial capability overlap with published multi-pulse isotope-count measurements. No priority, novelty, experimental advantage, or breakthrough claim is made.

## Finding

The proposed statistic is a particular high-order projection of product isotope-count data under a selected isotope input code. The underlying acquisition components already exist in the closest catalytic literature: isotope-switch pulse sequences, online or pulse-resolved mass spectrometry, and measured distributions over the number of labelled atoms in multi-carbon products.

Most directly, Li et al. (2011) report per-pulse isotope-count distributions for C2–C6 effluent products after switching from repeated 12C-methanol pulses to successive 13C-methanol pulses. Their H-ZSM-5 measurements include C4 butenes, and their figures display the full number-of-13C-atoms distribution for each product and pulse. An alternating sum of those bins is already a computable statistic of the same data type as the proposed parity readout.

Liu et al. (2023) use repeated 13C/12C methanol pulse switching and online mass spectrometry. Their supporting information reconstructs eight C7H8 isotope-count components from m/z 91–99 using a fragmentation matrix, and fits C3+ aliphatic fragment responses to four C3 isotope-count components. The C7 reconstruction is semi-quantitative; the C3+ result mixes fragments from several products and is less direct.

Neither paper reports the exact telegraph-averaged kernel

\[
Q_n(r)=\mathbb{E}\exp\!\left[-2r\sum_{j=1}^{n/2}(S_{2j}-S_{2j-1})\right].
\]

Their experiments use different pulse schedules, sample products over pulse-response windows, and study catalyst pools whose states can change with pulse history. Thus they do not establish that this exact statistic was previously calculated. They do establish that the isotope-count output required for it, and multi-pulse isotope intervention at a relevant catalytic platform, are already experimentally available. The candidate has not shown that its target needs a new detector or a new isotope-sensing modality.

The strict information separation in the temporal-ancestry note is confined to a baseline of one ideal step or one ideal rectangular pulse. A square-wave or suitably designed multi-pulse code distinguishes its four-carbon even/odd example perfectly. General nonlinear frequency-response methods also already treat higher-order Volterra responses to periodic forcing, though the cited catalytic implementation modulates reactant concentration and does not itself measure isotope ancestry. Consequently, no general information separation or economic separation from optimized multi-pulse and nonlinear-response methods currently survives.

The exact Hartfelder comparison remains unresolved: the accessible abstract describes a theoretical isotope-composition frequency-response method under quasi-steady-state conditions and calls its response linear. It does not reveal whether the full paper considers high-order product isotopologue correlations or any equivalent parity construction. The RSC full-text route failed at authentication, described in the ledger.

## The exact acquisition operator

Let a product have an even number \(n=2m\) of labelled carbon atoms whose entry times through the controlled feed boundary are \(S_1,\ldots,S_n\). Let \(K\) be the number of heavy-isotope atoms in the product. For a symmetric isotope code with heavy probability

\[
p_H(t)=\frac{1+a\,u(t)}{2}, \qquad |u(t)|\leq 1,\quad 0<a\leq 1,
\]

conditional independence of the entering labels gives

\[
\mathbb{E}[(-1)^K\mid S_1,\ldots,S_n,u]
=a^n\prod_{i=1}^{n}u(S_i).
\]

Thus the measured count histogram \(P_k=\Pr(K=k)\) supplies

\[
\frac{\sum_{k=0}^{n}(-1)^kP_k}{a^n}
=\mathbb{E}_{S}\prod_{i=1}^{n}u(S_i).
\]

This is not merely a mean isotope fraction. It is an \(n\)-factor input-output functional of the ancestry times. Equivalently, the full mass-isotopomer generating function is

\[
G(z;u)=\mathbb{E}_{S}\prod_{i=1}^{n}\left(1-p_H(S_i)+z\,p_H(S_i)\right);
\]

the parity is its value at \(z=-1\), with the known purity correction.

The identity assumes a fixed isotope-neutral ancestry law, chemical feed held constant while only the isotope fraction changes, and feed-boundary carbon labels independent conditional on their entry times. These are model conditions, not established facts for a particular catalyst. With \(M\) independent detected products, the per-product corrected parity variable has magnitude \(a^{-n}\). Hoeffding's inequality therefore gives the idealized bound

\[
\Pr(|\widehat F-F|\geq\varepsilon)\leq 2\exp(-M\varepsilon^2a^{2n}/2),
\qquad M\geq \frac{2\log(2/\delta)}{a^{2n}\varepsilon^2}
\]

to reach absolute error \(\varepsilon\) with failure probability at most \(\delta\). This counts independent effective products only; serial correlation, product-flux weighting, uncertainty in feed purity, and MS inversion can increase the required sample. For fixed \(a<1\), isotope-label noise alone introduces an \(a^{-2n}\) sample penalty. The bound excludes isotope preparation, switching, calibration, and washout costs.

For the biased telegraph parametrization in the source note, \(p_H(t)=(1+b+a\sigma(t))/2\), the corresponding histogram weight is

\[
W_n(K)=\frac{(1-b)^K(-1-b)^{n-K}}{a^n}.
\]

Its expected value is \(\mathbb{E}_{S}\prod_i\sigma(S_i)\). If \(\sigma(t)\in\{-1,+1\}\) is a stationary telegraph process with Poisson flip rate \(r\), then for ordered entry times the product of signs is \((-1)\) raised to the number of flips in the disjoint intervals \([S_1,S_2]\cup\cdots\cup[S_{n-1},S_n]\). That count is Poisson with mean

\[
rL_n,\qquad L_n=\sum_{j=1}^{m}(S_{2j}-S_{2j-1}).
\]

Since \(\mathbb{E}[(-1)^N]=e^{-2\mathbb{E}N}\) for a Poisson variable,

\[
\mathbb{E}_{\sigma}\prod_i\sigma(S_i)=e^{-2rL_n},
\qquad
\mathbb{E}_{S,\sigma}W_n(K)=Q_n(r).
\]

This proves the acquisition identity. It also locates the prior-art boundary: \(Q_n\) is the telegraph-input average of an \(n\)-linear response functional. It is a special high-order response kernel/readout, not a new class of isotope-count measurement.

For a stationary product stream, write the atom entry ages at observation time \(t\) as \(A_i=t-S_i\). Then a deterministic code produces

\[
F_t[u]=\mathbb{E}\prod_{i=1}^{n}u(t-A_i).
\]

Expanding a multisine input \(u(t)=\sum_\ell c_\ell e^{i\omega_\ell t}\) yields terms proportional to

\[
\left(\prod_i c_{\ell_i}\right)e^{i(\sum_i\omega_{\ell_i})t}
\mathbb{E}\exp\!\left[-i\sum_i\omega_{\ell_i}A_i\right].
\]

The response coefficients therefore contain samples of the symmetrized joint age characteristic function. This is the high-order, multi-frequency object represented by a Volterra response kernel. A sufficiently rich, calibrated frequency-response campaign on the isotope-ratio channel could evaluate the target code functional if the relevant kernel is identifiable over the operative bandwidth. The cited catalytic frequency-response work uses concentration forcing and does not solve this isotope-specific inverse problem. A full reconstruction may require more experiments than estimating one selected scalar directly; no matched-resource result establishes which is cheaper.

## Closest primary isotope-correlation and pulse evidence

| Primary source | Input and measured output | Exact overlap | Limit for the proposed claim |
|---|---|---|---|
| Li, J. et al. (2011), *Catalysis Today* 171, 221–228, DOI [10.1016/j.cattod.2011.02.027](https://doi.org/10.1016/j.cattod.2011.02.027). Full author-hosted PDF: [DICP](https://dmto.dicp.ac.cn/dnl12eng/2011-1.PDF). | Fixed-bed pulse MTO experiments at 450 °C; 15 pulses of 12C-methanol followed by four successive 13C-methanol pulses. Each pulse's effluent was analyzed by GC–MS. Figures 1–3 give the isotope-count distribution \(P(K=k)\) for C2–C6 olefins; Figure 2 is H-ZSM-5. Contact time was 0.08 s. | This is direct measurement of the count histogram needed for an alternating-parity projection, including even-carbon C2, C4, and C6 products. A deterministic isotope pulse train already interrogates multi-atom ancestry through the resulting product isotope counts. | The article does not compute \(Q_n(r)\), does not use randomized telegraph coding, and does not report a stationary history ensemble under constant chemical feed. It reports evolving pulse chemistry; the authors note ZSM-22 conversion falls across methanol pulses and discuss complications in mechanistic inference. |
| Liu, C. et al. (2023), *ACS Catalysis* 13, 5205–5212, DOI [10.1021/acscatal.3c00168](https://doi.org/10.1021/acscatal.3c00168); full final version from [TU Delft](https://pure.tudelft.nl/ws/portalfiles/portal/150495194/acscatal.3c00168.pdf). Supporting information DOI [10.1021/acscatal.3c00168.s001](https://doi.org/10.1021/acscatal.3c00168.s001). | Repeated 13C-methanol pulses establish a quasi-steady surface response; the sequence then switches to 12C-methanol pulses. Online MS monitors isotope fragments. The C7 aromatic parent count distribution is reconstructed from m/z 91–99; the C3+ aliphatic isotope mixture is estimated from m/z 39–47. | The C7 analysis explicitly estimates all eight \(^{12}C_n{}^{13}C_{7-n}\) count components. The supporting information gives the linear fragmentation system \(A c\approx obs\), with nine measured masses and eight isotope components. This is a measured high-order isotope-count distribution, not just atom-average enrichment. | C7 values are reconstructed through fragment correction; the authors describe their overall isotope-distribution estimate as semi-quantitative. The C3+ fit aggregates multiple products and assumes comparable component response, and further refinement was unavailable. Pulse intervals were 1.25 or 3.75 minutes; this is not the note's constant-feed stationary ancestry protocol. |
| Hartfelder, U. et al. (2012), *Analyst* 137, 5374–5381, DOI [10.1039/c2an35903k](https://doi.org/10.1039/c2an35903k). Accessible primary abstract: [PubMed record](https://pubmed.ncbi.nlm.nih.gov/23034591/). | The abstract describes a theoretical frequency-response method driven by changes in reactant isotope composition, under quasi-steady-state conditions. It calls the response linear. | Closest direct isotope-frequency-response theory; it prevents treating isotope-composition modulation or frequency-domain analysis as new. | Full paper unavailable here, so whether it contains any higher-order isotope-count/ancestry construction is UNKNOWN. Abstract-level “linear” language is insufficient to certify exclusion. |
| Petkovska, M. et al. (2010), *Chemical Engineering Science* 65, 3632–3637, DOI [10.1016/j.ces.2010.03.011](https://doi.org/10.1016/j.ces.2010.03.011). | Primary publisher text describes Volterra-based higher-order frequency response functions for periodic inlet-concentration modulation in a heterogeneous catalytic reactor. It derives the second-order \(G_2(\omega,-\omega)\) term for average reactor performance. | Establishes that nonlinear, multi-frequency reactor response and higher-order FRFs are existing analysis tools. | The studied input is reactant concentration and output is reactor conversion, not isotope-coded product ancestry or isotopologue parity. It is a general-method comparator, not an exact prior match. |
| Wang, R. et al. (2025), *ACS Catalysis* 15, 2677–2689, DOI [10.1021/acscatal.4c05157](https://doi.org/10.1021/acscatal.4c05157). | A pseudorandom binary sequence (PRBS) of reactant-concentration pulses is used for microkinetic parameter identification. The accessible abstract specifies that the comparison is based on synthetic reactor-performance data and reports better practical identifiability than a single-step inlet. | Direct published comparator for pseudorandom broadband transient input and the single-step baseline. It independently undermines novelty claims for PRBS excitation or for comparing it only with one step. | This is a concentration-forcing/model-identification study, not isotope modulation or an ancestry-count measurement. Full article was not available in this audit. |
| Weber, Z. et al. (2026), “Transient Pseudo-Random Binary Sequence Measurements for the Rapid Determination of Elementary Rate Constants for Heterogeneous Catalytic Reactions,” Research Square preprint, DOI [10.21203/rs.3.rs-9171848/v1](https://doi.org/10.21203/rs.3.rs-9171848/v1); complete public-text mirror [ResearchGate](https://www.researchgate.net/publication/404374733_Transient_Pseudo-Random_Binary_Sequence_Measurements_for_the_Rapid_Determination_of_Elementary_Rate_Constants_for_Heterogeneous_Catalytic_Reactions). | A custom packed-bed reactor pulses CO with PRBS on-time/off-time intervals of 1–6 s into steady O2/He over Pd/SiO2. An Ar tracer is co-pulsed; calibrated MS records CO, O2, CO2, Ar, and pressure at about 280 ms scan time. The authors reconstruct inlet profiles, fit an isothermal axial-dispersion/microkinetic model to roughly 300 time samples, and estimate ten elementary rate constants. The preprint reports about five minutes of transient data per temperature and a roughly 16-fold experiment-time and 4-fold total workflow-time reduction versus the stated steady-state workflow. | Strongest actual catalyst PRBS-transient comparator found: randomized multi-pulse excitation can carry more kinetic information than a single pulse and can support a substantial same-study workflow speedup. This makes a fair multi-input resource comparison essential. | Reactant concentration is deliberately perturbed, and outputs are gas concentrations fitted to a reaction model. The study does not modulate isotope fraction at fixed chemical feed, measure whole-product isotope-count histograms, or target joint carbon-entry ancestry/parity. Its speedup is not transferable to the candidate without a matched isotope-code campaign. It is a 2026 preprint, not a peer-reviewed result. |

Li et al. are the closest direct output comparison because they display the entire mass-count distribution for products with even carbon count. Liu et al. provide a recent example with faster online MS and a detailed isotope-fragment inversion, but the C3+ channel is less specific to a single whole product.

The 2025 PRBS study is simulation-based and compares parameter identifiability against a single-step inlet; the 2026 preprint supplies an experimental implementation with high-rate outlet measurements and explicit tracer-based inlet reconstruction. These are not isotope-ancestry measurements. Their relevance is that broadband/pseudorandom transient excitation and the claimed acceleration of catalyst characterization already have concrete comparators. Transferring either information or cost performance to a constant-chemical-feed isotope-ratio code would require a new matched experiment.

## What survives the stronger competitor

The original E/O construction does prove a scoped separation from ideal one-step and one-rectangle measurements. Four ordered atom ages are

\[
A_j=C+(j-1)\tau+\tau X_j,\quad j=1,\ldots,4,
\]

with \(X\) uniform over even-parity bit strings in one model and odd-parity bit strings in the other. Every marginal on at most three coordinates agrees. A single step has one label boundary and a single rectangular pulse has two, so the complete isotope-count output at each observation time depends on at most two nonconstant age coordinates. Those outputs coincide for the E/O models.

That separation disappears for a designed multi-pulse code. The exact parity contrast at fixed \(t,C\) is

\[
\Delta(t,C)=\frac18\prod_{j=0}^{3}
\left[u(t-C-j\tau)-u(t-C-(j+1)\tau)\right].
\]

For a square wave satisfying \(u(t-\tau)=-u(t)\), the corrected parity is \(+1\) on the even model and \(-1\) on the odd model, independent of the common delay. Its contrast is 2. The source note's telegraph setting \(r\tau=2\) yields contrast

\[
\frac{(1-e^{-2r\tau})^4}{8}\approx 0.11609
\]

and flips at rate \(r=2/\tau\), while the tuned square wave flips at rate \(1/\tau\). This mathematical benchmark shows that random coding is not the strongest available experiment when its scale is known. It does not prove a laboratory cost advantage for square-wave modulation; it refutes a general claim that the telegraph code is information- or switch-cost-optimal.

The same logic applies more broadly: if multiple isotope pulses can place enough boundaries across the candidate ancestry times, their isotope-count outputs evaluate a higher-order product of the input code. A multi-tone isotope waveform exposes corresponding higher-order frequency coefficients. Therefore the current information-separation result is relative to a deliberately narrow single-pulse comparator, not to the strongest existing transient-method family.

## Economic and information verdict

**Information:** A rigorous separation from ideal single-rectangle data survives for the artificial four-carbon E/O histories. It does not survive optimized multi-pulse input or general nonlinear frequency response in that example. The parity statistic is a projection of count data that primary pulse-isotope studies already acquire. The exact \(Q_n(r)\) target has not been found stated in the cited papers, but the measurement class needed to acquire it is not new.

**Economics:** No separation is established for the candidate. The candidate's code-variance bound covers only its own idealized random-code component and independent-product term. Even the idealized isotope-label estimator has an \(a^{-2n}\) effective-product penalty at fixed error and confidence when \(a<1\). The audit cannot assign a numeric total experiment cost for the candidate: labelled-carbon dose, feed switching, initial inventory clearance, product recovery, fragment inversion, response covariance, catalyst aging, and calibration have not been measured or matched to stronger baselines. The 2026 concentration-PRBS preprint reports a large speed advantage for its own CO-oxidation/model-identification workflow, but the input, output, target, and comparator differ. Existing isotope pulse studies likewise use different operating regimes. None of these resource claims establishes that the candidate is cheaper or faster at equal ancestry-decision accuracy.

A defensible economic result would require a same-catalyst comparison with (i) actual measured isotope feed waveforms, (ii) a resolved whole-product mass-count distribution, (iii) verified isotope-neutral ancestry and quantified startup inventory, (iv) an experimentally relevant ambiguity that remains after optimized pulse and nonlinear-response data, and (v) total resource/error accounting at matched information and decision accuracy.

## Missing decisive evidence

1. **Hartfelder full-text priority read.** Retrieve the complete 2012 article through an authorized institutional route. Until then, exact equivalence to its derivation is UNKNOWN.
2. **Real ancestry ambiguity.** Identify two chemically plausible, independently supported histories that agree on the best existing isotope-transient data and differ in \(Q_n(r)\). The current E/O laws are mathematical examples, not fitted catalyst histories.
3. **Matched competitor campaign.** Run the proposed code against optimized single/multiple pulses, periodic isotope modulation, and nonlinear frequency-response analysis with equal catalyst state, chemical feed, isotope budget, observation time, detector precision, and prior calibration.
4. **Measurement model.** For the candidate product, show that whole-product \(P(K=k)\) is recoverable with calibrated uncertainty; specify fragment response, natural-isotope correction, count covariance, product flux weighting, and effective sample size.
5. **Physical operating assumptions.** Measure isotope waveforms at the declared carbon-entry boundary, finite-switching response, old-carbon washout, stationary product selection, and any isotope-induced kinetic change.
6. **Cost theorem or data.** Prove a resource lower bound for every stronger multipulse/nonlinear-response comparator, or demonstrate on a real same-platform experiment that the scalar code estimator reaches a decision faster, more accurately, or at lower total cost.

## Conclusion

The most defensible result is a precise mapping: isotope-count-resolved pulse experiments already measure data from which a high-order parity observable can be computed; randomized telegraph coding specializes that observable to a Laplace transform of ordered atom-entry gaps. This provides a useful interpretation and a direct scalar target without fitting a full reaction network. It does not yet provide a novel measurement modality or a demonstrated economic advantage. The accessible prior literature makes multi-pulse and nonlinear-code comparisons mandatory, while Hartfelder et al.'s exact coverage remains unresolved because its full paper was not retrieved.

