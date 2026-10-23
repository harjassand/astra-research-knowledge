# Independent forward-state contraction verification

## Result

Independent 60-decimal-digit arithmetic reproduces the parent implementation's selected forward contractions and energy moments to maximum relative difference 1.334e-15. This validates the mathematical transcription of the supplied decimal coefficients, not the physical accuracy of the QCT fit or a compiled Fortran binary.

No parent files were changed. No reverse rates, flow trajectory, net chemistry, spending, or external outreach were performed.

## Source and independent method

Primary source: F. Esposito and I. Armenise (2017), supplementary interpolation routine, https://doi.org/10.1021/acs.jpca.7b04442.s002 ; downloadable PDF https://ndownloader.figshare.com/files/9083011 . Copied source PDF/text and SHA-256 checksums accompany the code/JSON receipt. S15 was independently rendered and visually inspected (seam_S15.png).

The independent script parses literal assignments line-by-line, requires unique entries, verifies 108 coefficients on each side, and evaluates the energy basis by nested scalar Horner evaluation with mpmath at 60 decimal digits. The parent instead uses long-double tensor contraction. Independent event sums use mpmath fsum. Parent output is read only after all independent results have been calculated.

Source S2 explicitly applies exp(a0+a1/T+a2/T^2)/3. Rates have source units cm^3 s^-1 per molecule pair, not molar volume units. The source energies are in eV relative to dissociation, not positive excitation above the vibrational ground state. Negative source energies must be retained in polynomial/inverse-energy evaluation. Excitation means instead subtract the respective molecular v=0 energy. NO(0)-N2(0) = 3.2485751 eV is ground-to-ground endothermicity under this source energy convention.

The rate loop includes N2 v=0..59 and NO w=0..47. The additional energy entries N2(60), N2(61), and NO(48) are not rate-loop states and were not included in the contracted population.

## Seam issue

The PDF genuinely prints aexchON2(i,lim_v(iw),iw+1) = a*En2(lim_v(iw)+1)+b. The literal variant reproduces the cross-product-index write and sequential iteration; the corrected_index variant explicitly proposes replacing its target by aexchON2(i,lim_v(iw)+1,iw). This is not an author-confirmed correction.

Although the comments describe interpolation of rates, actual code interpolates each exponent coefficient linearly in N2 energy. Therefore the fixed-temperature rate is log-linearly/geometrically interpolated, not arithmetically interpolated. Both independent and parent implementations implement the actual coefficient operation. At the selected 1700/2700 row the literal/corrected rate discrepancy is only approximately 0.0057%; that is not a bound on fit uncertainty.

## Selected results (corrected-index interpretation)

| T bath / T vibrational, K | Forward rate, cm^3/s | Own-QCT thermal enhancement | Event N2 excitation, eV | Event NO excitation, eV | Event mode change, kJ/mol |
|---|---:|---:|---:|---:|---:|
|1700 / 1700|2.34958360714e-20|1|0.831985865|0.073269496|-73.2050|
|1700 / 1959.5075393144|5.76269183085e-20|2.452643870|1.283600881|0.092469984|-114.9267|
|1700 / 2700|8.77511452797e-19|37.34753044|2.257623258|0.193130911|-199.1932|
|2700 / 2700|1.17389609738e-16|1|1.023876480|0.165572096|-82.8138|

At 1700 K the QCT thermal contraction is only 0.39960 times the separate 3e-10 exp(-38000/T) Arrhenius model. Thus the middle 1700/1959.5075 row gives 2.45264 times its own thermal population but only 0.98008 times the original Arrhenius rate. At 1700/2700 the corresponding ratios are 37.3475 and 14.9242. These ratios answer different questions and must not be conflated.

## Explicit non-preferential comparator

Define independent normalized bound-state Boltzmann populations for N2 and NO at a shared stipulated vibrational temperature Tv, with no reaction weighting and no rotational partition reweighting. This comparator is a modeling choice, not the predicted nascent NO distribution or a reverse-rate model.

| Tv, K | Mean N2 excitation, eV | Mean NO excitation, eV | Product minus reactant, kJ/mol |
|---|---:|---:|---:|
|1700|0.0468227243|0.0613465926|+1.40134|
|1959.5075393144|0.0640537676|0.0805040162|+1.58721|
|2700|0.1187310031|0.1391295558|+1.96816|

The contrast with the negative forward-event mode change directly demonstrates vibrationally preferential consumption under this fit/population definition. At 1700/2700 the event-reactant mean is approximately 19 times the mean of the stipulated N2 population. Assuming non-preferential consumption plus a Boltzmann product distribution would reverse the sign and greatly understate the magnitude of the mode-excitation term. Product mean at T bath instead of Tv is additionally recorded in the JSON, so an alternative explicitly declared comparator can be formed.

## Interpretive limits

- The N2 distribution is p_v proportional to exp[-(E_v-E_0)/(kB Tv)] over v=0..59. Calling Tv=T bath a thermal-population comparator is valid for this definition. It is not a proof of full rovibrational equilibrium: a v-dependent rotational partition factor may be needed for that stronger claim. The interpolation routine itself contains no explicit rotational partition weights that could independently verify the parent's rotational-averaging description.
- A negative event mode-change does not mean the entire reaction is exothermic or that this quantity is direct translational heat. Adding source ground-state endothermicity leaves positive combined bath energy demand: +240.235, +198.513, +114.247, and +230.626 kJ/mol for the four rows. The unresolved rotational/translational split must not be invented.
- The printed driver generates 1000..20000 K values. This alone is not validation of physical accuracy at 1700 K or an uncertainty interval.
- Exact source decimal mathematical interpretation is verified. The printed Fortran uses many unsuffixed real literals (including 1./3.), so default-kind rounding can prevent bitwise equality with a compiler execution; no author executable or compiler reference has been tested here.
- No statistical factors sufficient for a justified reverse-state model were supplied by this routine. No reverse rate, net NO production, or total nitrogen-chemistry conclusion follows from these forward moments alone.

## Follow-up: independent linear-program bound certificate

At supplied mean excitation 0.06417802570979354 eV and bath temperature 1686.4595074210936 K, scaled scipy HiGHS LP independently verifies the parent's two-point enumeration. Minimum supports v=0,1 with p1=0.22113539777442856 and forward rate 9.035890851704081e-21 cm^3/s. Maximum supports v=0,50 with p50=0.006853970903801243 and forward rate 3.841448670189442e-12 (literal) or 3.817898040771379e-12 (corrected-index) cm^3/s. Affine dual lower/upper envelopes have nonnegative signed slack over all 60 tabulated states; parent objective disagreements are below 4.7e-15 relative. The independent rate implementation, not parent rate arrays, supplies the LP coefficients. See check_moment_lp.py and moment_lp_receipt.json.

This check takes the caloric temperature and mean supplied by the parent as inputs; it does not independently rederive the NASA/finite-ladder caloric split or the global entropy pass. The extreme distributions demonstrate only that one mean energy does not fix a forward-event rate for this finite mathematical table. They do not establish attainability from the initial distribution, maintenance against relaxation/dissociation, an achievable gain, net NO production, or a physical upper bound.

High-v applicability is especially material here: N2(v=50) has source energy -0.39464689 eV relative to dissociation, or 9.36362681 eV excitation above v=0. It is bound in the stated vibrational ladder, not itself an above-threshold pseudolevel, but a vibrational-only population does not establish survival/occupancy of its rotational manifold. The separate source SI3 explicitly lists N2 quasibound (j,v) lifetimes using WKB, with stated typical accuracy within one order of magnitude and particular emphasis on lifetimes below 1 ps. That source is evidence that j-dependent lifetime restrictions matter; it is not proof the fitted high-v rate is reliable for an arbitrary optimized population. Its text is copied as quasibound_lifetimes_source.txt. Treat the extreme-population result as static information insufficiency only.

## Corrected published thermal-fit distinction

Parent reports a separately sourced corrected thermal fit from DOI 10.1021/acs.jpca.0c00869: 1.2686e-13 T^0.874 exp(-36899/T). Parent-calculated ratios of the declared equal-temperature vibrational-only contraction to that fit are 0.74258 at 1700 K, 0.74594 at 2000 K, 0.76574 at 2300 K, and 0.79889 at 2700 K. These figures are parent-supplied, not independently recomputed or source-verified here. They are NOT disagreement between the two contraction implementations. Rotational weighting and source/fit approximation conventions may contribute. Consequently use “defined equal-temperature population comparator,” not “exact full QCT LTE recovery.” Do not rescale state rates to erase the discrepancy without an explicit, independently justified model change.

## Algebraic challenge: explicitly synthetic reversible completion

For forward N2+O -> NO+N define Kc(T)=[NO][N]/([N2][O]) at equilibrium in the chosen NASA bulk thermochemistry. The proposal

kb(w,v;T) = kf(v,w;T) pN2_eq(v;T) / [Kc(T) pNO_eq(w;T)]

is algebraically consistent as a DECLARED synthetic reversible comparator if both finite-ladder equilibrium populations are normalized and use the same bath T, ladder truncation and energy convention. It is not a source-identified reverse-QCT model. Both sides have two particles, so Kc is dimensionless and no net concentration-standard-state factor remains; kb has the same cm^3 molecule^-1 s^-1 units as kf. Concentrations must use a compatible number-density convention. No additional factor of 1/3 or an independently guessed degeneracy may be applied.

A fully state-resolved thermodynamic completion must subtract the equilibrium finite-ladder energy and entropy and add actual-population energy and entropy for BOTH N2 and NO. With NO constrained at bath equilibrium its correction cancels in the bulk state, but any interpretation of nascent-NO energy partition must separately account for instantaneous relaxation to that constraint. State chemical potentials can be written mu_s,v=mu_s,NASA(T,n_s)+RT ln[p_s,v/p_s,v_eq]. The non-equilibrium Gibbs correction per mole of species is RT times the relative entropy D(p||peq). Pairwise detailed balance then yields nonnegative isothermal reaction entropy production. This is an algebraic property of the declared closure, not evidence that its reverse branching is physically correct.

For the proposed trial with pNO=pNO_eq, contraction gives kb_bulk=kf_equal_temperature/Kc and net forward formation rate [N2][O] kf_equal_temperature [enhancement-Q/Kc], where Q=[NO][N]/([N2][O]). This explicitly separates forward enhancement from composition/equilibrium driving. A fixed-composition, fixed-bath-temperature scan that changes Tv also changes stored energy; it is not an equal-energy process comparison. No net process yield, reachability or all-closure conclusion follows from the one-state synthetic diagnostic. No numerical reverse calculation was performed in this independent check.
