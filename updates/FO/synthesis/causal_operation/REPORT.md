# Chemical-state interventions: when a targeted decision survives imperfect selectivity

**Status.** This is an internally derived identification result and a literature-grounded experimental design. No experiment was run here. The N813 isotope-ancestry results remain source-derived and unreviewed; this report does not validate them. I found an already-published, physically implemented site-population intervention for a bounded catalytic question, so I do not claim a new intervention or an advantage for temporal isotope coding.

## Finding

If two mechanisms induce the same complete atom-entry-age law, every isotope-neutral feed waveform produces the same one-product isotope-count law under N813's conditional independent-label model. A new waveform cannot reveal a chemical state that the observation map never encodes. A state-conditioned mark or a perturbation of a chemically localized population changes that map.

The sharp finite-experiment criterion is linear estimability: after stacking the calibrated intervention, scrambling, and detector channels, a target is identifiable exactly when its contrast lies in the row space of the measured response map (including known constraints). Full pathway recovery is unnecessary. If channel parameters, collateral effects, or measurement error are bounded rather than exact, the sharp answer is the range of the target over all compatible latent states and channels; a decision is certified only if that entire range lies on one side of its threshold.

For a concrete operation, Ezenwa et al. co-fed 2,6-di-tert-butylpyridine (DTBP) to suppress extracrystalline Brønsted sites during MFI toluene methylation at 403 K, measuring product rates and xylene isomer selectivity by online GC. They calibrated poisoning on an unconfined-acid MCM-41 control and report a small initial-rate change but later rate and selectivity differences. This is a real operation for asking whether an external-site population contributes to this low-temperature reaction and its deactivation. It is not evidence for applying the same selectivity or mechanism at high-temperature methanol-to-olefins conditions.

The experimentally relevant distinction is therefore conditional. A randomized comparison can certify the total effect of the *DTBP co-feed package* without identifying every pathway or assuming perfect poisoning. Attributing that effect to external rather than internal sites requires the calibrated selectivity contrast and a bound on collateral changes. The existing paper supplies substantial selectivity evidence but not all numerical bounds needed for a new, robust population-share interval. An ideal selective oracle is not needed; an acquired, nonzero channel contrast and enough calibration to keep the decision interval away from its threshold are.

## Information boundary inherited from N813

Write a product's unordered entry-age multiset as \(\Xi=\{A_1,\dots,A_n\}\), with law \(\mu\). Under the N813 label model, at actual calibrated feed-label probability \(p\),

\[
G_{\mu,p}(z)=\mathbb E_\mu\prod_i(1-p(A_i)+zp(A_i)).
\]

Thus equal \(\mu\) gives equal count response for every neutral waveform \(p\), including arbitrary deterministic and adaptive controls when the full emitted-history process is coupled identically. This is an observation-boundary result, not a claim that any particular pair of catalysts has equal \(\mu\). It separates temporal provenance at a declared feed boundary from internal chemical identity, site identity, bond history, and intervention response.

The supplied ancestry report itself proposes chemical-state-conditioned marking and population perturbation as the next information interface, while flagging selectivity, scrambling, inventory, detector response, collateral effects, and chemistry neutrality as unacquired. I treat that list as the starting contract, not as a realizable operation. The exact N813 source and incoming-report pins are in `READ_LEDGER.md`.

## Finite-channel theorem

Let \(x\in\mathbb R^d\) be a finite vector of latent chemical-state or population weights. A protocol uses a set of legal operations indexed by \(m\). The calibrated linear mean response is

\[
y=Hx,\qquad H=\begin{pmatrix}D_1S_1A_1\\ \vdots\\D_MS_MA_M\end{pmatrix},
\]

where \(A_m\) is the operation's state-selectivity/eligibility map, \(S_m\) is the chemical scrambling or state-transition map between operation and readout, and \(D_m\) is the detector response. Known linear constraints are \(Rx=r\). A target is \(\psi(x)=c^Tx\).

**Theorem 1 (sharp estimability criterion).** Suppose the feasible latent set has nonempty relative interior in the affine space \(Rx=r\), and the channels \(H,R\) are known. The target \(c^Tx\) is constant over every pair of latent states giving the same noiseless observations iff

\[
c\in\operatorname{rowspan}\!\begin{pmatrix}H\\R\end{pmatrix}.
\]

The theorem concerns one decision contrast; \(H\) need not have full column rank and \(x\) need not be reconstructed.

**Proof.** If \(c=H^T\lambda+R^T\nu\), then \(c^Tx=\lambda^Ty+\nu^Tr\), so every compatible state has the same target. Conversely, if \(c\) is outside that row space, finite-dimensional orthogonality gives a vector \(v\) with \(Hv=0\), \(Rv=0\), and \(c^Tv\ne0\). Choose any feasible relative-interior point \(x_0\). For sufficiently small \(\epsilon>0\), both \(x_0+\epsilon v\) and \(x_0-\epsilon v\) remain feasible. They give the same observations and different targets. This also supplies a constructive indistinguishability witness. \(\square\)

For a simplex or other constrained polytope with active boundary restrictions, the exact global version is: every pair \(x,x'\) in the feasible set with \(Hx=Hx'\) must satisfy \(c^T(x-x')=0\). The row-space condition is exact on the affine hull whenever the feasible set has relative interior there. If it fails, the feasible target set is the sharp interval

\[
\Psi(y)=\left[\min_{x\in\mathcal F(y)}c^Tx,\;\max_{x\in\mathcal F(y)}c^Tx\right],\quad
\mathcal F(y)=\{x:Rx=r,\;Hx=y,\;x\in\mathcal X\}.
\]

For a decision threshold \(\tau\), certification is exact: certify “above” only when \(\inf\Psi(y)>\tau\), and “below” only when \(\sup\Psi(y)<\tau\). If the interval crosses \(\tau\), the experiment has not resolved that decision, even if it has narrowed many other components of \(x\).

### Detector noise and calibration uncertainty

If the observation is \(\widehat y=Hx+e\), with a stated bounded error set \(e\in\mathcal E\), replace the equality in \(\mathcal F\) by \(\widehat y-Hx\in\mathcal E\). Calibration uncertainty \(\gamma\in\Gamma\) is handled by taking the union over \(H(\gamma)=D(\gamma)S(\gamma)A(\gamma)\). The resulting target interval is sharp by construction: its endpoints are attained by feasible latent/channel states when the set is compact. No statistical confidence claim follows from an error bar unless the sampling and coverage model justify it.

With a known fixed channel and mean-zero measurement noise of covariance \(\Sigma\), any linear unbiased estimator \(\lambda^T\widehat y\) of \(c^Tx\) must solve \(H^T\lambda=c\) (modulo known constraints). Such an estimator exists exactly under the theorem. Its variance is \(\lambda^T\Sigma\lambda\); the minimum over valid \(\lambda\) charges both detector noise and channel conditioning. Full-column-rank \(D\) is sufficient to recover a whole count vector, but it is not necessary to estimate a particular target.

### Two-state chemical mark with imperfect selection, scrambling, and detection

For a mark that classifies an atom as originating in chemical state \(A\) or \(B\), let \(x\) be the fraction from \(A\). Let marking eligibility be \(e_A,e_B\), scrambling swap a fraction \(s\) of marked origins, and let the binary detector classify correctly with probability \(d\). The chance that a source-\(A\) atom is both marked and reported as \(A\) is

\[
h_A=e_A[d(1-s)+(1-d)s],
\]

and for a source-\(B\) atom it is

\[
h_B=e_B[(1-d)(1-s)+ds].
\]

After subtracting a separately measured false-positive background, the reported-\(A\) fraction is \(y_A=h_Ax+h_B(1-x)\). Hence

\[
x=\frac{y_A-h_B}{h_A-h_B}
\quad\text{iff}\quad h_A\ne h_B.
\]

If eligibility is equal, \(e_A=e_B=e\), the effective contrast is

\[
h_A-h_B=e(2d-1)(1-2s).
\]

This is sharp: the provenance fraction is unidentifiable when the allowed channel includes \(e=0\), an uninformative detector \(d=1/2\), or complete two-state scrambling \(s=1/2\). More generally, for interval-valued calibration the *uniform* criterion is \(\inf_{\gamma\in\Gamma}|h_A(\gamma)-h_B(\gamma)|>0\), with its sign fixed; if the calibrated set permits equal effective responses, there is no uniform separation guarantee. For fixed nominal \(h_A,h_B\) with contrast \(\delta=h_A-h_B\), absolute observation error at most \(\rho\) and effective channel-column error at most \(\kappa\) imply

\[
|\widehat x-x|\leq\frac{\rho+\kappa}{|\delta|},
\]

before clipping to \([0,1]\). The \(1/|\delta|\) factor is the experimentally paid conditioning cost; “imperfect” need not mean “unusable,” but small contrast can erase a practically relevant decision.

For multiple chemical classes and multiple mark/assay settings, stack the corresponding \(D_mS_mA_m\) rows and apply Theorem 1 to the selected provenance contrast. One can identify a precursor-class total while leaving all pathway details in the nullspace. Conversely, a mark does not help if scrambling and detector coarsening map the target classes to identical columns.

## Population perturbation: a backed operation and its limit

### Two-population rate model

Let \(r_E,r_I\geq0\) denote external and internal contributions to a chosen instantaneous product-rate outcome under a fixed catalyst/feed state. A no-poison measurement is \(R_0=r_E+r_I\). A site-targeted treatment suppresses fractions \(\alpha_E,\alpha_I\) and may create a collateral rate shift \(c\), so

\[
R_1=(1-\alpha_E)r_E+(1-\alpha_I)r_I+c.
\]

Put \(\theta=r_E/R_0\) and \(h=1-(R_1-c)/R_0\). In the no-collateral exact-calibration case,

\[
h=\alpha_E\theta+\alpha_I(1-\theta),\qquad
\theta=\frac{h-\alpha_I}{\alpha_E-\alpha_I}
\quad\text{iff}\quad \alpha_E\ne\alpha_I.
\]

The determinant of the two-arm design for \((r_I,r_E)\) is \(\alpha_I-\alpha_E\). A perfectly selective oracle is not required: known imperfect suppressions identify the two contributions whenever they differ. If the effects are identical on both populations, the intervention contributes no separating information.

Write the *observed* normalized reduction as \(h_{obs}=1-R_1/R_0\). Since \(h_{obs}=\alpha_E\theta+\alpha_I(1-\theta)-c/R_0\), if \(\alpha_E\in[a_-,a_+]\), \(\alpha_I\in[i_-,i_+]\), normalized collateral satisfies \(|c|/R_0\leq\kappa\), and \(h_{obs}\in[h_-,h_+]\), the sharp feasible set is

\[
\Theta_E=\left\{\theta\in[0,1]:
a_-\theta+i_-(1-\theta)-\kappa\leq h_+,\;
a_+\theta+i_+(1-\theta)+\kappa\geq h_-
\right\}.
\]

This follows because the image of the independent calibration box at fixed \(\theta\) is exactly the interval between those two endpoints. With an exact rate ratio and point calibrations, it collapses to the formula above. With bounded response errors, fold their ratio interval into \([h_-,h_+]\); with a detector matrix, first include its full compatible response interval. The interval criterion certifies an external-share threshold only if all of \(\Theta_E\) clears it.

This decomposition is conditional on additive contributions and a stable state across arms. In a coupled catalytic network, blocking one population can alter transport, coverage, acid strength, or another population's turnover; such effects belong in \(c\) or in a richer response model. If that nuisance term is unbounded, the site attribution is not identified. The *total intervention effect* \(R_1-R_0\), in contrast, is an operational estimand: a randomized, matched comparison can estimate it even when the treatment hits more than one site class. It answers “what does this co-feed package do?” It does not by itself answer “which hidden site caused the change?”

### Exact observational examples

Let two mechanisms have exactly the same unordered entry-age law and the same baseline rate \(R_0=1.5\). Under every neutral feed-isotope waveform their isotope-count records agree.

| Model | Internal contribution \(r_I\) | External contribution \(r_E\) | No-poison rate | Rate with ideal external-only suppression |
|---|---:|---:|---:|---:|
| A | 1 | 0.5 | 1.5 | 1 |
| B | 1.5 | 0 | 1.5 | 1.5 |

The legal DTBP-like intervention separates these models if its internal suppression and collateral shift are calibrated to zero: the intervention's rate response is different despite identical neutral-isotope observations. This is an algebraic witness, not a fitted catalyst model.

If collateral is unconstrained, Model B can instead have a \(-0.5\) treatment-specific rate shift and reproduce Model A's treated rate. The observed two-arm data then agree while \(r_E/R_0\) differs. This is the exact reason a selective-site claim needs measured uptake/suppression and a collateral bound. It is not repaired by more isotope feed waveforms or more products from the same observation map.

### Literature-backed implementation, kept in its demonstrated regime

Ezenwa, Norfleet, Hibbitts, and Gounder, *Journal of Catalysis* 454 (2026), 116653, DOI [10.1016/j.jcat.2025.116653](https://doi.org/10.1016/j.jcat.2025.116653), report the operation on MFI zeolites during low-temperature toluene methylation. The open primary PDF was read at the methods and site-poisoning/deactivation results sections (see `READ_LEDGER.md`). Their relevant facts are:

- A fixed-bed gas-phase setup ran at 403 K, approximately 4.2 kPa toluene, 66 kPa dimethyl ether, and 36 kPa He, normally below 1% conversion. MFI particles were 180–250 μm and active catalyst mass was 0.011–0.352 g in a 1 g quartz-diluted bed.
- A bulky base, 2,6-di-tert-butylpyridine (DTBP; cited kinetic diameter about 0.80 nm versus MFI pore limiting diameter about 0.55 nm), was co-fed to titrate external Brønsted sites. The paper validates 5 Pa DTBP on MCM-41, which has only unconfined sites: xylene formation falls by >99% after 2 h. At 10–40 Pa in MFI, initial xylene formation rates differ by <5% from no-DTBP values, and the feed exceeds the measured external-site inventory. These controls support selective access under the study conditions; they do not provide a formal zero-leakage bound on \(\alpha_I\) for every catalyst/time.
- At 6 h, the unpoisoned xylene formation rates are reported at about 2× the DTBP-arm rate for MFI-TPA-C and MFI-EDA-3, and 5× for MFI-DABCO-1. On MFI-EDA-3 and MFI-DABCO-1, DTBP also preserves a para-selective pattern longer; the paper interprets later untreated selectivity as increasingly reflecting external sites as intracrystalline sites deactivate. This is population-level evidence from a site-selective intervention under the paper's experimental assumptions, not a complete pathway reconstruction.
- In the limiting model where DTBP suppresses all external contribution, leaves internal rates unchanged, and has zero collateral effect, those 2× and 5× ratios correspond to external shares of 1/2 and 4/5 of the untreated 6 h rate. These are conditional algebraic translations of the reported ratios, not measured site fractions; partial suppression or collateral shifts change them by the interval formula above.
- A separate strong benchmark for a different but related decision is Hwang, Johnson, and Bhan (2019), DOI [10.1016/j.jcat.2018.10.022](https://doi.org/10.1016/j.jcat.2018.10.022): site-specific isotope tracing separates aromatic-methyl from ring-carbon origins in HSAPO-34, and a deliberately shifted entrained methylbenzene distribution changes the propylene/ethylene selectivity ratio. I inspected the article abstract only. It is a strong provenance-plus-intervention baseline for that HSAPO-34 question; it does not establish the same mechanism or effect in H-ZSM-5 or low-temperature MFI toluene methylation.

For the first study's **same-regime** follow-up, a reviewable operation is two independently prepared, matched MFI-TPA-C beds randomized within synthesis/packing blocks to 0 or the published 0.009 kPa DTBP co-feed. Keep toluene, DME, He, total flow, temperature, catalyst mass, particle range, and pretreatment fixed; record 25–30 min online GC observations through 6–10 h. Use an external-only MCM-41 positive control at the published 0.005 kPa, an inert/sham co-feed, and a site-uptake/titration assay to bound both external suppression and internal leakage. Make the primary endpoint prospectively one scalar (for example, the 6 h xylene-rate ratio or integrated xylene production through 6 h); report isomer-selectivity endpoints separately. Use bed/run, not individual chromatograms, as the independent unit unless a validated time-series covariance model says otherwise. This prospective randomized design identifies the total DTBP-operation effect; the calibrated two-site model is only used if its selectivity and collateral bounds are actually obtained.

The paper already performed closely related co-feed/site-selectivity experiments, so this is a replication/robustness design, not a novel operation claim. It should not be transferred to 573–773 K methanol-to-olefins chemistry: the authors explicitly distinguish low-temperature pore-blocking by retained polymethylbenzenes from high-temperature formaldehyde/diene/coke chemistry. A chemically specific label for a trapped internal species is still not established by the literature inspected here.

## Decision and cost ledger

**What can be decided without full pathways.** With randomized matched beds and an outcome measured on a calibrated GC channel, one can decide whether the *specified DTBP co-feed* changes a selected rate/selectivity endpoint. This is an intention-to-treat operational decision; it does not require an ideal poison. A site-class share or site-specific causal attribution can be decided only if calibration narrows \(\Theta_E\) past the decision threshold. The published observation that MFI untreated/DTBP rate ratios at 6 h are about 2–5 is scientifically relevant evidence about relative site accessibility, but the paper's uncertainty and calibration are not enough to promote a new exact share interval here.

**Documented experimental burden in the primary implementation.** Per run: catalyst bed preparation/packing, 773 K oxidation in 5% O2/He for 4 h, cooling to 403 K at 0.083 K s−1 (about 1.24 h for the stated 370 K drop), 1 h He flush, >2 h bypass feed stabilization/GC verification, and a fixed-condition reaction lasting typically 6–22 h. The published rate/selectivity readout samples online GC every 25–30 min (roughly 12–53 time points per run over that run range); these are repeated measures, not independent catalyst trials. The paper states rate measurement uncertainties of ±15%. Methane internal standard flow is 0.05–0.08 cmSTP3 s−1 (1.5–2.3 kPa), and calculated rates agreed within 5% with the no-standard alternative under the authors' flow assumption. Catalyst regeneration, additional matched beds, external-site titration, standards, and GC calibration add to that burden.

The active-catalyst mass range is 0.011–0.352 g per 1 g solids bed. DTBP partial pressures were 0.005 kPa on the MCM-41 calibration control, 0.009 kPa on MFI-TPA-C, 0.022 kPa on MFI-EDA-3, and 0.040 kPa on MFI-DABCO-1. For MFI-TPA-C, the paper reports one cumulative DTBP molecule fed per total H+ at 1.1 h and per external H+ at 0.05 h. These are feed-exposure ratios, not measured uptake or cost savings.

Unknown and therefore unpriced: reactor/personnel cost; independent-bed count for a prespecified power; catalyst-lot variance and within-run covariance; quantitative internal-site leakage and site occupancy over time; a hard collateral bound under aged catalyst conditions; GC response-matrix/peak-overlap covariance; disposal/safety overhead; and the economics of any process change. The 2019 site-specific isotope baseline additionally requires preparation/verification of differently labeled methylbenzene positions and solid-phase/product analyses; its time, isotope dose, and monetary cost were not present in the abstract examined. No matched cost advantage is claimed for either baseline.

## Scientific status and decisive next gate

This closes the narrow question as follows:

1. Neutral feed-isotope waveforms cannot separate same-entry-law causal models; this follows from the N813 observation law.
2. A state-selective mark is mathematically useful exactly when its combined eligibility/scrambling/detector columns retain target contrast. A mark with uncalibrated scrambling or rank-collapsing detection is not a physical oracle.
3. A real selective population perturbation exists for external versus internal site contributions in low-temperature MFI toluene methylation. The strongest existing same-question comparator is already the DTBP co-feed/site-titration method; it has no novelty advantage to claim.
4. The total operational effect can be measured without full pathway recovery. A latent site attribution needs a measured response matrix and bounded collateral effects; otherwise an explicit indistinguishable pair remains.
5. No physically validated internal-state mark, high-temperature MTO site-selective intervention, isotope-scrambling calibration, total-cost superiority, external review of this derivation, or new catalytic capability is established here. Status for those claims is **UNKNOWN**.

The decisive gate is a source-matched replicated DTBP trial with feed/reactor controls and a measured calibration set \((\alpha_E,\alpha_I,c,D,\Sigma)\); then publish the feasible target interval and test whether it certifies a preregistered catalyst-design threshold. If the calibration set admits equal effective site responses or arbitrary collateral, retain only the randomized operation-level effect and abandon the site-attribution claim.
