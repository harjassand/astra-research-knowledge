# Physical-path investigation: isotope overwrite and event-conditioned selection

15 October 2026. **MISSION: NOT_ACHIEVED.** No laboratory operation was performed and no physical or technological advantage was established. The strongest surviving object is a precise experiment for event-conditioned isotope selection. Its decisive gate is acquiring a reliable single-site ejection/refill record and protecting accepted atoms through later operations. The broad energy-abundance and bulk-purification interpretation is stopped.

## Operation sought and why this substrate

The initial construction was a postgrowth isotope writer: preferentially eject light carbon from selected positions in intact graphene, fill the temporary vacancies using ordinary carbon, and repeat. The intended endpoint was a prescribed isotope pattern with the original covalent lattice restored. Temporary vacancies would be the material intermediate; acquired mass-sensitive kinetics and event feedback would provide the information and control. This direction was invented independently of the excluded manufacturing, native-instability, dissipation and DNA-repair routes.

An isotope pattern could be a useful scientific specimen if it separated a mass effect from a geometric or chemical alteration. That possible scientific use does not establish a new phonon device, quantum processor, or energy technology. Structural damage or residual catalyst can defeat precisely that endpoint.

## Primary evidence and the strongest comparator

[Susi2016](https://www.nature.com/articles/ncomms13040) reports isotope-sensitive ejections at 80–100 kV and one vacancy filled by the next 2.2-second frame at 95 kV. Thus displacement and filling coexist in one setup. Replacement identity, independent natural-feed exchange, missed-event rates and accepted-site protection were not measured. Supplementary Table 1 was downloaded and visually checked; its 95 kV central cross sections are 56.6 millibarn for light carbon and 2.1 millibarn for heavy carbon. The [2017 correction](https://www.nature.com/articles/ncomms15780.pdf) reverses Fig. 3c isotope labels and repairs Eq. 23; it does not replace this table.

The comparator is stronger than merely buying an isotope-pure bulk precursor. [Whiteway2020](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.102.235429) reports CVD isotope superlattices with 6–225 nm periods. [Senga2022](https://www.nature.com/articles/s41586-022-04405-w), inspected through its [author manuscript](https://arxiv.org/abs/2306.15861), fills a crack with a 1–2 nm by 10 nm isotope domain using residual carbon and a Si catalyst at 650 C: about 400 atoms in 3 minutes at 1.3e9 electrons/nm2. Its uncatalysed hole expands; high-temperature diffusion also limits pattern retention. These are existing local isotope-writing operations. A new protocol must win for a qualified final specimen, including the acquisition cost of any enriched starting sheet.

[Meyer2012](https://arxiv.org/html/1203.2372) identifies another coupled cost: a primary monovacancy leaves a neighbour vulnerable to a rapid second ejection. Hole growth from beam-driven chemistry also differs from clean-lattice knock-on. Adding carbon or a catalyst can change the very cross sections being used for selection.

## First construction fails as a high-purity blind writer

Let p=.01109 be the reservoir heavy fraction and let x be the repaired-lattice heavy fraction. Under independent, instantaneous refill and fixed pristine cross sections, the heavy fraction obeys

    dx/dD = p sigma_L(1-x) - (1-p) sigma_H x.

Its equilibrium is

    x_star = p sigma_L / [p sigma_L+(1-p)sigma_H].

At the acquired 95 kV central values, x_star=.23210059. Near-perfect repair does not make a pure heavy lattice. Reaching x=.20 in this ideal model needs 7.13405e12 electrons/nm2 and about 35.16 replacements per site. The incident kinetic energy is .108585 J for each uniformly irradiated nm2. This is neither absorbed specimen heat nor measured wall-plug energy. A per-atom energy needs an acquired beam profile, effective area and tails.

The independently authored [collateral diagnostic](COLLATERAL_MODEL.md) shows that random extra atom loss sharply degrades enrichment. One collateral removal per primary event gives only .02137044 heavy fraction at the same ratio; .1 gives .08683322. Sustaining .20 requires fewer than .01005573 unselected collateral removals per primary event in that explicitly well-mixed model. This is a measurable requirement, not a universal graphene theorem or an acquired value of the collateral rate.

The parent independently derived a stronger fixed-dose/open-loop scheduling bound using explicit heavy, light and vacancy states. Its bound is compatible with this elementary equilibrium. It must not be extended to event-conditioned stopping: selection can use the observed event history, which changes the admitted operation.

## Root mutation: select survivors, reset failures

The parent supplied a materially different protocol during this investigation. Start a site with an independent natural-feed atom. Irradiate it until the first observed ejection, or until an attempt fluence d is reached. Ejection means refill/reset and restart. Surviving the entire attempt means accept the atom and protect it permanently from further screening dose.

With exact event observation, no hidden replacement, isotope-dependent exponential ejection rates, and independent resets, accepted heavy probability is

    q(d)=p exp(-sigma_H d)
         / [p exp(-sigma_H d)+(1-p)exp(-sigma_L d)].

Thus q tends to 1 even though the blind writer has a finite equilibrium ceiling. This is a conditional change in operation, not evidence of a physical violation of the earlier restricted bound. The arithmetic was independently checked here; the parent owns the renewal derivation.

For target q, the attempt cap and acceptance probability are

    d = log[q(1-p)/(p(1-q))]/(sigma_L-sigma_H),
    a = p exp(-sigma_H d)+(1-p)exp(-sigma_L d).

Expected attempts are 1/a. Expected total fluence is

    {p[1-exp(-sigma_H d)]/sigma_H
       +(1-p)[1-exp(-sigma_L d)]/sigma_L}/a.

At the 95 kV central values:

| Nominal accepted heavy probability | Expected attempts | Expected total fluence, electrons/nm2 |
|---:|---:|---:|
| .90 | 105.009 | 1.95892e13 |
| .99 | 126.691 | 2.41098e13 |
| .999 | 139.753 | 2.70404e13 |

These are exact-model expectations with unbounded failure tails. They exclude waiting, switching, image acquisition, drift correction, preparation, repairs, failures and final qualification. At q=.99 the corresponding uniform-1-nm2 incident kinetic energy is .366967 J. They are not a lab throughput prediction.

## Decisive physical gate: what does a no-event record certify?

A frame showing an occupied site does not establish that its original atom remained there. Ejection followed by refilling between frames produces the same endpoint. The acquired source's visible vacancy is valuable positive evidence but does not give the missing-event probability. More image repetitions cannot correct an unknown record model.

Stage-separated supply is a possible test design: remove the carbon supply during screening, detect persistent vacancies, then enable feed only after rejection. It is not a solution already obtained. Residual adatoms, return of the same atom, reconstruction, chemical etching and source-on/source-off changes in bonding must be measured. Carbon supply independence and the isotope fraction of actual incorporated atoms must be qualified on the same specimen.

Rare acceptance amplifies unmodelled false acceptance. If a correct accepted component has probability a and heavy fraction q, and an additional unmodelled accepted component has probability at most epsilon and could be all light, the heavy fraction is bounded only by q a/(a+epsilon). Nominal q=.999 has a=.00715550. Guaranteeing .99 under this worst-case mixture requires epsilon<=6.5050e-5 per attempt. Zero failures in about 46,052 independently audited calibration attempts would be needed for a simple one-sided 95% binomial upper bound at that scale. This is one conservative planning calculation, not a universally necessary sample count or a measured instrument error.

Spatial protection is separate. Fluence-normalized cross sections measured with ~1 nm2 scans do not supply a single-atom beam profile. Irradiation tails on accepted neighbours accumulate over all later failed attempts and all subsequent sites. An atom that survives its own trial may later be overwritten. Protecting accepted atoms requires a measured cumulative exposure bound and acquisition-aware scan order, not merely a software flag.

[DECISIVE_EXPERIMENT.md](DECISIVE_EXPERIMENT.md) freezes a minimal admission sequence. It tests the event record and independent replacement before a pattern/device claim. If those gates fail, this candidate stops; it is not rescued by an ideal posterior.

## Separate Si-exchange-handle lead

A short targeted follow-up found a distinct, less destructive possibility: identify an isotope and route it using a temporary substitutional Si handle, exchanging Si with selected neighbouring carbon atoms, then park Si outside the qualified target region. This is preserved separately from renewal and is not counted as a completed operation.

[Tripathi2018](https://arxiv.org/abs/1712.08755) demonstrates 34 directed Si/carbon swaps without unwanted motion in one sequence and 150 ms feedback at 55 keV. Two unusually slow events are described as consistent with heavy carbon, but the isotope identity was not independently established. The source reports one knock-on damage event among its 55 keV series. This does not provide a calibrated isotope classifier or error-free transport.

The decisive experiment would compare inversion-time distributions on independently isotope-labelled, locally matched specimens, freeze the classifier, and transport one independently confirmed isotope while tracking all exchanges. Local strain and chemical surroundings can mimic rate changes. Direct vibrational isotope microscopy is the strongest readout comparator. This lead stops at the classifier/label-transfer gate; no isotope sorting, new capability or practical quantum use has been established.

## Full cost and claim ledger

| Requirement | What is actually obtained | Remaining cost or gate |
|---|---|---|
| Substrate acquisition | Public single-layer graphene experiments | Membrane growth/transfer, cleanliness, support, defects, specimen yield |
| Isotope-sensitive actuation | Source-reported pure-sheet cross sections | Actual feed-on/feed-off local cross sections, beam drift/profile and chemical state |
| Single-site event record | A visible vacancy/refill example | Hidden ejection/refill, false positive/negative rates, independent audit |
| Reset | Filling observed; isotope-domain crack growth reported | Independent incorporated-atom identity, same-atom return, reset time/yield |
| Control | Software can direct beams; Si feedback exists | Transfer to carbon ejection record, blanking latency, accepted-site protection |
| Material endpoint | None produced here | Atom-resolved isotope contrast, topology, contamination, long-term retention |
| Energy | Conditional incident-kinetic ledger | Wall-plug power, heating, vacuum, feed, detector, recovery and wasted runs UNKNOWN |
| Memory and computation | Small formulas and stdlib script | Image-stream storage/analysis, calibration and controller latency UNKNOWN |
| Scaling | Dose and retry expectations only | Failure tails, cumulative neighbour dose, specimen/process yield UNKNOWN |
| Competitor advantage | None | Same final pattern, geometry, damage, retention and complete resource budget |
| Novelty | UNKNOWN | Targeted searches are not exhaustive priority clearance |

The local capital checkout was read at 25fc24509a59aabee340b36b588c9e59a144253d: AGENTS.md, 00_START_HERE.txt, current navigation, and the N802 isotope-spectral dossier. N802's unqualified material/target-response bridge was retained as a warning, not a premise transferred to this graphene operation. The preceding campaign's root REPORT.md was read to avoid excluded/repeated routes. Current discovery workers' files were not read. No subagents were spawned.

The [calculation script](calculate.py) writes [calculations.json](calculations.json). It is a transparent arithmetic fixture, not a molecular simulation, laboratory replay, external proof audit or novelty check. Primary titles, dates, exact short excerpts, source-access limits and acquired bytes are in [SOURCES.md](SOURCES.md). Token use, pure inference time, inference energy and monetary cost are UNKNOWN. No paid compute, purchase, external message or physical experiment was executed.
