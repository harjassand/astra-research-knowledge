# Isotope replacement: a blind ceiling and an information-driven escape

15 October 2026. Root-authored mathematical construction. Internal derivation; independent same-team audit pending. Historical priority, physical realization, and practical advantage are UNKNOWN. This is a controlled stochastic model, not measured isotope enrichment.

## Interface

A target lattice site has isotope H, isotope L, or vacancy V. A beam gives fluence D and ejects an occupied isotope at constant cross section sigma_H or sigma_L, with sigma_L > sigma_H >= 0. The exponential waiting-fluence law is supplied. A fresh refill is an independent H draw with probability p, otherwise L. All repeated replacements preserve the same lattice geometry and cross sections. No collateral loss, same-atom return, hidden replacement, beam tails, detector error, or readout damage is included. These ideal grants favor the proposal and must not be called acquired capabilities.

The candidate physical substrate is graphene with 12C=L and 13C=H. Susi et al., Nature Communications 7, 13040 (2016), DOI 10.1038/ncomms13040, measured isotope-dependent knock-on statistics and observed an ejection followed by refill at 95 kV. Their supplementary Table 1 central cross sections at 95 kV are 56.6 millibarn for 12C and 2.1 millibarn for 13C. These are estimates on isotope-labelled specimens, not qualified rates for a repeatedly repaired site. The table errors are not treated as simultaneous confidence bounds. Natural feed p=0.01109 is an explicitly chosen planning composition, not a measured composition of their refill atom. The Fig. 1 refill does not identify the incoming atom. The 2017 correction concerns Fig. 3c labels and Eq. 23, not proof of isotope exchange.

## Blind replacement at fixed per-site fluence

Start with H probability p and L probability 1-p. In fluence coordinates, let H,L,V also denote unconditional occupancy probabilities, O=H+L<=1, and z=(1-p)H-pL. Isotope-neutral refill leaves the expectation of z unchanged, even if refill timing depends on the preceding vacancy history. Beam ejection gives

    dz/dD = c O - b z <= c - b z,
    c = p(1-p)(sigma_L-sigma_H),
    b = p sigma_L + (1-p) sigma_H.

For a common deterministic cumulative fluence D at every target, with no selection or isotope-dependent beam steering, the integrating-factor bound is

    z(D) <= (c/b)(1-exp(-bD)).

After an isotope-neutral final refill makes every site occupied, q=H=p+z, hence

    q <= q_star-(q_star-p)exp(-bD),
    q_star = p sigma_L / [p sigma_L+(1-p)sigma_H].

Instantaneous independent refill attains equality in the ideal model. Delaying refill or splitting an otherwise common fixed dose cannot improve it. For sigma_H>0, obtaining a blind equilibrium ceiling q_star>=q requires

    sigma_L/sigma_H >= q(1-p)/[p(1-q)].

This statement MUST NOT be extended to arbitrary adaptive stopping. Vacancy history carries isotope information through the survival time. Root initially considered a broader schedule claim, then constructed the counterexample below before publication. The correction changes the operation and its information contract.

If an exactly occupied endpoint is reached after finite expected counts, heavy-atom balance gives an additional necessary bound:

    E[number of fresh refill draws] >= (q-p)/p.

It counts fresh reservoir atoms, not returning sputtered atoms. It follows from q-p=p E[refills]-E[heavy ejections]. It is not a fabrication-yield estimate.

## Adaptive renewal screening

For each site independently, begin with a fresh draw from the same reservoir. Irradiate until the first ejection or a screening fluence d. On ejection, stop, refill with a fresh independent draw, and restart the screening clock. On surviving all of d, stop irradiation permanently and accept that site. Every site eventually produces an output; rejected attempts and their dose are charged. No final-site postselection is hidden.

Write

    a(d)=p exp(-sigma_H d)+(1-p)exp(-sigma_L d).

An attempt succeeds with probability a. Bayes' rule gives the final isotope probability

    q(d)=p exp(-sigma_H d)/a(d).

For p<q<1, choosing

    d=log[q(1-p)/(p(1-q))]/(sigma_L-sigma_H)

achieves q exactly in the admitted model. Thus a finite selectivity ratio does not impose the blind ceiling once a complete ejection history and per-site stopping are supplied.

The attempts are iid renewal cycles. Their number is geometric with mean 1/a, the mean number of failed ejections/refills is (1-a)/a, and mean total fluence is

    E[D_total] = {p[1-exp(-sigma_H d)]/sigma_H
                  +(1-p)[1-exp(-sigma_L d)]/sigma_L}/a.

For a zero cross section the associated quotient has continuous limit d. The formula follows by integrating the survival probability to get one attempt's expected fluence, then solving the renewal recursion E[D_total]=E[min(T,d)]+(1-a)E[D_total]. It does not assume cost is independent of attempt success. Attempt count and dose are unbounded random variables; only their expectations are finite. A fixed deadline needs an explicit abort probability and the charge for aborted sites.

If at most M independent attempts are allowed, failure probability is (1-a)^M. The accepted outputs still have composition q in the ideal model; the unaccepted sites must be retained in the yield ledger. The acceptance event is not a measured isotope label. Any relation between isotope composition and a final quantum/thermal/device function requires a separate experiment.

## Actual physical gate

The operation needs a reliable statement that the SAME atom survived a complete screening interval. A vacancy that ejects and refills between imaging frames can look like no ejection and invalidate q(d). A known bound on missed events must be propagated into the final isotope posterior. Staging beam exposure, vacancy readout, and a controlled carbon supply could provide the interface, but it has not been demonstrated here, and changing adatoms/bonding/temperature can change the very cross sections used by the calculation.

Neighbor atoms with dangling bonds can have lower displacement thresholds. The ideal site clock ignores this measured mechanism. Frame rate, readout dose, beam tails, same-atom returns, isotope-dependent refill, cumulative nonhexagonal defects, support compatibility, and accepted-site protection are decisive coupled requirements. A calibrated renewal flag cannot be replaced by an apparently filled lattice image.

Direct isotope analysis by knock-on damage is already prior art. Isotope-controlled CVD, post-growth hot-Cu etch/regrowth, and the 2022 Senga et al. isotope-domain writing/imaging experiment are serious incumbents. No novelty claim is made for survival selection as a general statistical principle. The only possible distinct operation is endpoint-matched, local post-device isotope rewriting using natural feed and a qualified renewal interface. Its advantage is NOT_ESTABLISHED.

## Decisive experiment

First qualify the information channel, before any device claim. On labelled 12C and 13C reference regions, run a frozen exposure/readout/refill protocol with a separately tagged refill source used only for calibration. Independently assay atom exchange and lattice quality, including same-atom return and replacement events hidden within one readout interval. Measure the full primary/neighbor displacement and healing race under the exact operating conditions. If the acquired flag and rate model cannot support a covered posterior, stop.

Only then run blinded natural-feed trials at predeclared doses and attempt caps; report all failed sites, damage, dose, current/time, vacuum/heating, feed use, readout, reset and assay costs. Compare the same local isotope endpoint and lattice/device function against optimized isotope growth/exchange and direct isotope identification/selection. No experiment was performed in this campaign.
