# Intervention-assisted rare events: what is learned about the native clock?

15 October 2026 (Australia/Brisbane). **Disposition: exact adversarial obstruction; conditional repair; no demonstrated new physical capability.** This is an independent derivation on a finite continuous-time Markov model, accompanied by exact rational arithmetic. It is not a molecular experiment, a general no-go theorem for enhanced sampling, a priority claim, or a test of a particular published implementation. Scientific novelty of the repair is **UNKNOWN** and its algebra is close to standard system identification and likelihood-ratio sampling.

## Exact contract and the decisive counterexample

The target is the *control-off* first-exit rate $R_P$ from metastable state $A$ into an absorbing product set. The available discovery instrument can repeatedly prepare $A$, apply a controlled protocol, and record complete exit times, channel labels and its own feedback log. The instrument's reaction events, clock time, preparation, resets, control energy, calibration and native audits must all be charged. A high frequency of product observations under control is discovery evidence; a native rate requires a valid transfer from controlled law $Q$ to native law $P$.

Let $ε>0$. There are three labelled exits (x,y,z), all ending in the same product set. The native continuous-time hazards are

| World | $p_x$ | $p_y$ | $p_z$ | Native rate $R_P$ |
|---|---:|---:|---:|---:|
| $H_0$ | $ε$ | $0$ | $0$ | $ε$ |
| $H_1$ | $ε$ | $ε$ | $0$ | $2ε$ |

For every permitted positive-control setting $u$, the device induces hazards $q_x=b_uε, q_y=0, q_z=c_u$, with calibrated positive $b_u,c_u$, *in either world*. The actuator suppresses a native channel $y$ if present and opens a synthetic route $z$. This is a hypothetical control-response map, not a claim that hyperdynamics or infrequent metadynamics has this response when used within its assumptions. Even granting the experimenter exact $b_u,c_u$ and perfect timing and channel readout, a control-$u$ first-exit record has waiting time $\operatorname{Exp}(b_u\varepsilon+c_u)$, mark probabilities $b_u\varepsilon/(b_u\varepsilon+c_u),\,0,\,c_u/(b_u\varepsilon+c_u)$, and the same law in both worlds. Perfect event labeling does not rescue the native total rate.

**Adaptive version.** A feedback policy may choose $u_t$ using all previous controlled trajectories, clocks and randomization. Inductively, conditional on any common transcript, its next chosen setting and the next controlled observation have the same law under $H_0,H_1$. Thus the entire transcript has the same law, even for unlimited controlled time or population cloning of those trajectories. The intervals for a $25\%$-relative rate estimate are $[.75ε,1.25ε]$ and $[1.5ε,2.5ε]$, which are disjoint. Any estimator from controlled data has success probabilities summing to at most one, so it cannot succeed with probability $2/3$ in both worlds. This is an information statement about the declared interface, not an assertion that feedback itself is invalid.

The pathway-creation ambiguity can be made even more direct: set native $p_z=0$ versus $p_z=ε$, and let the actuator overwrite the $z$ hazard to the same $c_u$ in both worlds. Seeing many controlled $z$ transitions then cannot tell whether that route was native or instrument-created. In a physical system, zero is an ideal hard-forbidden channel; an arbitrarily small native hazard poses the corresponding relative-precision problem.

If a control-off sentinel run is permitted, it can resolve the ambiguity, but its exposure is a resource. Grant instantly resettable $A$ and a hard cap $T$ on total native exposure. Couple the two native worlds using the same $x$ Poisson clock and add an independent $y$ clock of rate $ε$ only in $H_1$. Their records agree unless that extra clock rings. Hence

\[
\operatorname{TV}(\mathcal L_{H_0},\mathcal L_{H_1})\leq 1-e^{-\varepsilon T}.
\]

Any test with success at least $2/3$ in both worlds needs total variation at least $1/3$; therefore $T\geq \log(3/2)/\varepsilon$. Native exposure is only one cost: if a full native generator row can be read or calculated exactly, that row immediately reveals $p_y$ and beats this observation-only lower bound. The lower bound does **not** apply to such a richer interface.

## Exactly where familiar recovery methods stand

For a known native marked jump process with hazards $p_j$ and a predictable feedback proposal with hazards $q_j(t\mid\mathcal H_t)$, the usual finite-horizon path likelihood is

\[
W_T=\exp\!\left(\int_0^T[\Lambda_q(t)-\Lambda_p(t)]\,dt\right)
       \prod_{i:\,t_i\leq T}\frac{p_{j_i}(t_i)}{q_{j_i}(t_i)},
\qquad \Lambda=\sum_j\text{hazard}_j.
\]

With common initial-law support, correctly known conditional hazards, and $q_j>0$ on every native-positive path, $E_Q[W_T1_E]=P(E)$. Feedback alone does not spoil the identity; its logged, history-dependent proposal enters every factor. A control-created $z$ event has weight zero if $p_z=0$ is *known*. In the counterexample $q_y=0<p_y$ under $H_1$, so $P\not\ll Q$; no weight on observed controlled trajectories can represent the missing native $y$ paths. If the native hazards are unknown, even formal support preservation leaves the acquisition of the numerator, validation of weight tails and relative-error control outstanding. Dynamic importance sampling already uses history-dependent changes of measure; this is not a proposed new result [Dupuis and Wang, 2005](https://arxiv.org/pdf/math/0503454).

**Hyperdynamics.** Voter's method raises basin energy away from transition states and restores elapsed physical time under its transition-state/dividing-surface conditions [Voter, 1997](https://doi.org/10.1103/PhysRevLett.78.3908). The *global* requirement that the bias vanish on the relevant dividing surface is explicit in Voter's later discussion [Voter, 2013](https://sanibelsymposium.qtp.ufl.edu/wp-content/uploads/sites/20/2013/Voter%2C%20Art.pdf). Our $Q$ violates channel preservation and so is **not** a counterexample to a valid hyperdynamics calculation. It shows why an unknown transition surface cannot be waved away by an observed boost factor. A newly seen controlled pathway should be tested for native support and the validity of its clock correction.

**Infrequent metadynamics.** Tiwary and Parrinello recover kinetics from a history-dependent basin bias in studied systems [original paper, 2013](https://doi.org/10.1103/PhysRevLett.111.230602). Their follow-up states the operative conditions as no bias deposited in the transition-state region and collective variables without hysteresis, and uses Poisson escape-time statistics as a reliability diagnostic [Salvalaglio, Tiwary and Parrinello, 2014](https://doi.org/10.1021/ct500040r). In the toy counterexample every controlled escape time is *exactly exponential* under either native world. Any exponential goodness-of-fit test on that marginal passes in principle while the native rates differ. This says the test alone cannot certify hidden channel coverage; it does not assert that the authors' full conditions hold in the toy model.

**Cloning and native-dynamics splitting.** The original cloning construction tilts the *specified original transition matrix* $U$ to $\tilde U_{C'C}=e^{sJ_{C'C}}U_{C'C}$, then normalizes and replicates/kills clones [Giardinà, Kurchan and Peliti, 2006](https://arxiv.org/pdf/cond-mat/0511248). Cloning $Q$ without a transfer to $P$ characterizes a controlled process. Cloning or weighted-ensemble resampling of *native* trajectories can instead retain native path statistics when correctly weighted; [Zhang, Jasnow and Zuckerman, 2010](https://doi.org/10.1063/1.3306345) establish a broad path-sampling exactness result. Neither procedure generates information about $H_0$ versus $H_1$ from the identical $Q$ transcript. If native trajectories are available, the single-step fixture provides no intermediate interface to exploit; its rare-channel exposure cost remains explicit. For systems with informative interfaces, [forward-flux sampling](https://arxiv.org/abs/cond-mat/0602269) and weighted ensembles are serious matched comparators, not ruled out by this toy.

## Substantive repair: complementary probes with a rank and coverage certificate

The obstruction is a missing identifiable contrast. Here is a *conditional* redesign that supplies one. Suppose there are finitely many candidate native channel rates λ and controlled nuisance creation rates $c$, and each control (a) has a *calibrated* linear intensity response $r_a=M_a\theta$, where θ stacks those unknown rates. Unmarked event counts suffice. For target native total $R=t^\top\theta$, an unlimited-precision collection of controlled rate measurements identifies $R$ for all interior admissible θ **if and only if** $t$ lies in the row space of the combined response matrix $M$. Sufficiency follows from $t=w^\top M$, giving $R=w^\top r$. Conversely, if $t\notin\operatorname{row}(M)$, some $v\in\ker M$ has $t^\top v\ne0$; two nearby nonnegative parameter vectors θ and θ+δv have identical controlled data but different native totals. This is exact linear algebra, with no asymptotic sampling claim beyond intensity identification.

A concrete three-probe repair of the fixture has unknown $\theta=(\lambda_x,\lambda_y,\gamma)$ and measured *unmarked* total intensities

\[
r_1=b\lambda_x+\gamma,\qquad
r_2=b\lambda_y+\gamma,\qquad
r_3=\gamma,\qquad
R=\lambda_x+\lambda_y=\frac{r_1+r_2-2r_3}{b}.
\]

Probe 2 exposes the formerly suppressed native $y$ channel; probe 3 calibrates the control-created background. With only probes 1 and 2, the direction $(-1/b,-1/b,1)$ leaves both measured rates fixed while changing $R$ by $-2/b$. Thus even a complementary native-channel probe is insufficient if the synthetic route is unmeasured. Alternatively, reliable channel labeling and a control-created-route classification could remove the nuisance without probe 3, but those are acquired observations and classifications.

For independent Poisson event counts $N_i$ over controlled exposures $T_i$, $\widehat R=(N_1/T_1+N_2/T_2-2N_3/T_3)/b$ is unbiased under this model and has exact variance

\[
\operatorname{Var}(\widehat R)=\frac{r_1/T_1+r_2/T_2+4r_3/T_3}{b^2}.
\]

This can beat native waiting for *statistical* precision if the boost is large and the nuisance small, but it is not free. In the rational fixture λ_x=λ_y=1/1024, $b=64,γ=1/64$, each probe has $T_i=16384$. The exact totals are $(5/64,5/64,1/64)$, $R=1/512$, and relative variance $7/8192\approx0.00085449$. A native Poisson count over the **same aggregate exposure** $3T_i=49152$ has relative variance $1/96\approx0.0104167$. The controlled ratio is $21/256\approx0.0820$. Yet those controlled runs cause 2816 expected events versus 96 native events: reset, sensing and reaction-energy costs may reverse the apparent gain. A stronger native simulator with exact generator rows computes $R$ without sampling in this fixture.

The repair also needs a **support ledger**. If an unmodeled native channel carries unknown total hazard Δ, the reconstruction covers only $R_\mathrm{known}$ and the actual total is $R_\mathrm{known}+Δ$. A separately validated upper bound $0\leqΔ\leq U$ yields an honest interval $[R_\mathrm{known},R_\mathrm{known}+U]$. If $U$ is comparable to $R_\mathrm{known}$, it cannot rule out the factor-two counterexample. Acquiring a strong $U$, validating the response matrix across all relevant pathways, and detecting control-created chemistry are the substantive unsolved parts. The three-probe algebra by itself does not do them.

## Acquisition-inclusive comparison and next test

| Route with the same information access | What it can certify | Dominant charged resources here |
|---|---|---|
| Direct control-off Poisson observation | Native total and branching after enough events | Native exposure $\Omega(1/\varepsilon)$ for the two-world test; preparation, resets, detector efficiency |
| Exact native generator-row query | Native total immediately | Acquisition/validation of the full row and all outgoing support; in this toy, trivial if genuinely supplied |
| One controlled discovery setting, any feedback/cloning of its transcript | Controlled law and controlled pathways | Actuation and samples, but native rate nonidentifiable in the fixture |
| Complementary probes plus nuisance probe | Native total under the stated response/coverage model | Probe manufacture, $b$ and background calibration, exposure, 2816 expected events in the displayed fixture, reset/energy cost, error propagation |
| Native splitting/WE/FFS or correct likelihood-ratio control | Native path statistics under their respective conditions | Native propagation or complete weights/support, interface design and convergence; may dominate on structured multistep systems |

The strongest equally informed competitor for the proposed repair is ordinary calibrated rate-model fitting or likelihood-ratio/weighted-ensemble inference with exactly the same controls, native simulator and support information. It can prepend the same three-probe linear reconstruction. No new algorithmic or physical advantage over that comparator is established. The toy's statistical variance improvement is conditional on an especially favorable, **unverified** control family; the control energy, preparation duration, independent reset assumption, event-detection errors, pathway labeling and response-model drift were not measured.

The decisive next assay is a preregistered, blinded multichannel system with independently measurable control-off rates, one hidden native exit, and one control-created exit. First characterize whether physically realizable complementary probes yield a calibrated response matrix whose row space contains the native-rate target. Independently bound native flux through any missed channel, including controls that might erase one. Then compare native-rate error and pathway recovery against direct native observation, exact/native simulator queries where available, WE/FFS, and valid hyperdynamics/infrequent-metadynamics controls at equal *total* preparation, calibration, simulation/physical exposure, resets, energy and reliability budgets. A mere exponential waiting-time fit or many controlled events is not a pass. **No such assay was performed here.**

## Evidence and source scope

`python3 research/2026-10-15-operational-closure-v1/workers/s08_rare_adversary/exact_fixture.py` executed locally and checked the rational hazards, an unidentified null direction, the three-probe row combination and the Poisson variance comparison. It uses Python's `fractions.Fraction`; there is no Monte Carlo run. The coupling and row-space arguments above are original derivations for this report, internally reasoned but not independently peer reviewed. The local capital cards [N491](../../../../work/astra-capital-frontier-capability/frontier/review_cards/N491-chemical-rare-event-diagnostics-and-preprocessing.txt), [N492](../../../../work/astra-capital-frontier-capability/frontier/review_cards/N492-rare-event-certificate-acquisition-boundary.txt) and [N818](../../../../work/astra-capital-frontier-capability/frontier/review_cards/N818-acquisition-boundaries-for-rare-rates-remote-response-and-routing-repair.txt) were read as scoped, source-derived context, not as proofs of this fixture; prior campaign rare-event findings were also read. The relative local links in this paragraph are convenience locators; the exact capital files inspected reside at `/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-frontier-capability/frontier/review_cards/`.

Primary-source inspection was limited as follows: Voter's 1997 publisher abstract and 2013 author-authored local-hyperdynamics abstract/slides for the basin-bias and global dividing-surface condition; Tiwary and Parrinello's 2013 publisher abstract and Salvalaglio et al.'s 2014 original-paper abstract for the kinetic assumptions and Poisson diagnostic; Dupuis and Wang's full arXiv paper for dynamic feedback importance sampling; Giardinà et al.'s full arXiv paper, especially its original $U$, tilted $\tilde U$, and cloning steps; Zhang et al.'s original-paper abstract for weighted-ensemble exactness; Allen et al.'s original-paper abstract for FFS efficiency analysis. Full text for all molecular papers and any recent 2026 literature search were **not** established by this pass. Exact URLs are the links attached to the claims above. The CTMC, probe matrix, numerical values and native-exposure coupling are **this report's derivations**, not results from those publications.
