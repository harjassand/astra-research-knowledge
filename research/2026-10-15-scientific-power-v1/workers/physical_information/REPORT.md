# Physical information B — Meter the loss-making reaction itself

15 October 2026, Australia/Brisbane. **Status: physically unacquired candidate; novelty and practical advantage UNKNOWN.** No laboratory result was produced. The original results here are a finite-window conservation bound, two exact indistinguishability countermodels, and a proposed instrumented substrate. The accounting script checks illustrative arithmetic only.

The candidate is an **internally metered recombination element for an alkaline electrolyzer separator**. A gas-accessible, electrically insulated catalytic island is placed behind a liquid-excluding microcavity wall and inside a measured thermal boundary. It both consumes crossover hydrogen and meters the heat of that consumption. The resulting quantity is a lower bound on hydrogen destroyed in those islands in the *installed* device. It is not an estimate of the untouched membrane's permeability or an identification of all internal losses.

This is a narrower opportunity than a new hydrogen sensor, recombination catalyst, or separator. Those components and close combinations already exist. The potential scientific use is to separate the statement “little hydrogen exits in oxygen” from the statement “little hydrogen was wasted.” The decisive missing operation is a physically closed, sufficiently accurate thermal and chemical boundary inside an operating separator. Ordinary temperature measurement with heater pulses does not obtain that boundary.

## Current source-grounded opening

[Liu et al., Nature Energy (2026)](https://www.nature.com/articles/s41560-026-02094-7) explicitly distinguish outlet hydrogen from hydrogen consumed chemically at the alkaline anode; the latter is corrected using an apparent kinetic model. Their internal HOR probe requires an extra AEM that changes crossover. Their recombination catalyst is already a successful functional comparator, not our invention. These observations motivate a direct consumption meter; they do not validate the proposed meter.

The strongest electrochemical incumbent is [Gawas et al., Energy & Environmental Science (2025)](https://pubs.rsc.org/en/content/articlehtml/2025/ee/d5ee00048c?page=search): online GC plus measured HOR current at high differential pressure. It directly addresses hydrogen consumed electrochemically before the outlet. The new candidate must be compared against this method, complete two-exhaust molar accounting, and conventional calorimetric hydrogen sensors. It cannot claim advantage merely by comparing with outlet GC alone.

## The physically changed interface

The starting embodiment is a small laboratory alkaline cell near ambient pressure and approximately 80 C. It is not a pressurized industrial-stack proposal. A separator has an anode-side array of side pockets with the following proposed structure:

1. A hydrophobic gas-accessible wall admits dissolved H2/O2 into a gas microcavity while excluding liquid KOH. Candidate materials include a supported PTFE microporous wall; compatibility under compression, hot concentrated KOH and aging is unacquired.
2. An electrically floating Pt catalyst on a suspended island inside each cavity catalyzes recombination. A dielectric separates it from heater/thermometry conductors. The device has no electrochemical collector connection to the main anode or cathode. Electrical leakage and insulation are measured and bounded, rather than assumed absent.
3. Instrumented suspension legs conduct heat to a known bath. A surrounding guard is maintained at the island temperature. All remaining thermal paths require measured bounds; a temperature-controlled heater alone is insufficient.
4. The ionic current travels through the separator around the pockets. The gas pockets, supports, leads and guard modify ionic resistance, gas transport and mechanical behavior. All claims concern this modified substrate.
5. Anode exhaust H2 is measured with calibrated molar-flow and species measurements; electrolyte mixing, intentional H2 feeds, dissolved H2 inventory and potential H2 generation elsewhere are accounted for.

A schematic functional path is:

    cathode H2 source -> separator -> anode-side gas pocket
                                         |
                                insulated Pt island
                                H2 + O2 -> H2O
                                         |
                             instrumented heat boundary

    ionic current -> connected liquid paths around the pocket
    unconsumed H2 -> anode control volume -> measured exhaust

The readout is integrated reaction heat in joules, with a conservative error interval and chemical closure ledger. The representation is a conserved mole count obtained from a thermochemical upper bound per consumed H2 molecule. It does not require a fit of an internal reaction-rate law, diffusion coefficient, hidden site count, or supersaturation model.

This arrangement is co-designed measurement and intervention: the reaction that mitigates the unwanted gas creates the information signal. It deliberately adds a loss-making reaction rather than claiming to passively observe an untouched specimen. Whether it is a useful instrument after paying for that intervention remains open.

## Exact finite-window consequence

Let T be an acquisition interval. For a metered island, define Q as the net thermal energy exported across its audited thermal boundary, minus its measured electrical heater energy, with sensible stream enthalpy handled at specified reference conditions. A conservative calibration gives Q >= Q_minus.

Write the local energy balance as

    Q = sum_k h_k N_k + e.

Here N_k >= 0 is the number of moles of H2 consumed through admissible reaction k, h_k is its released heat per mole at the actual stream/product reference conditions, and e contains non-H2 reaction heat, residual chemical/thermal storage changes, unmetered heat paths, electrical leakage, and measurement error. Require the acquired bounds

    h_k <= h_max  for every admissible H2-consuming channel,
    |e| <= B.

Then, without an assumed kinetic model,

    N_rec := sum_k N_k >= max(0, (Q_minus - B)/h_max) =: L_rec.       (1)

**Proof.** Q_minus <= Q <= h_max N_rec + B. Rearranging and imposing nonnegativity yields (1). For multiple independently budgeted islands, sum their individual lower bounds. Their error budgets must jointly cover shared systematic errors.

The requirement is an upper enthalpy bound, not an assumption that every molecule forms liquid water. Vapor-water and peroxide channels can be included if their maximum heat per consumed H2 is bounded. Other combustible contaminants can create heat without consuming H2; they must be excluded or included in B. Catalyst reduction/oxidation, hydrogen adsorption, condensation, water uptake, support chemistry and finite inventory changes also belong in B. Calling the catalyst “inert” does not establish those bounds.

The [NIST liquid-water formation enthalpy](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7732185&Mask=2) is 285.830 kJ/mol in magnitude at its standard reference conditions. That value gives an illustrative scale of 1.481 V when divided by 2F. It is not automatically h_max for hot KOH, water vapor, a changed catalyst or contaminated gas.

Now choose a complete anode-side control volume. Let N_cross be the signed net H2 feed entering it across the cathode-to-anode separator cut; N_exit the H2 leaving in measured exhaust; N_unmetered >= 0 other irreversible H2 consumption; N_gen internal/external H2 supplied other than through that cut; and Delta N_A the final-minus-initial molecular-H2 inventory in the volume. Atom/species balance gives

    N_cross = N_exit + N_rec + N_unmetered + Delta N_A - N_gen.

If N_exit >= L_exit, Delta N_A >= -I_A and N_gen <= G_A, then

    N_cross >= max(0, L_exit + L_rec - I_A - G_A).                   (2)

The outer max(0,.) is licensed only when net cathode-to-anode feed is known nonnegative in the admitted operating regime. Without that premise, the unclipped expression is still the valid signed lower bound. Initial dissolved H2, trapped gas, intentional calibration injection and anode-side H2 production cannot be omitted. Unobserved consumption only increases the required feed; unobserved generation can invalidate (2).

Equation (2) concerns net feed supporting consumption and escape. It does not count gross forward crossings, rapid recrossings, or all molecules that ever entered an unresolved membrane pore. Inferring those quantities requires another interface.

The immediate decision change is falsification of any installed-device claim that total H2 loss is below L_rec, or that net anode feed is below the right-hand side of (2). A low exhaust H2 concentration plus a positive L_rec would certify that at least some apparent gas-purity improvement came with directly measured H2 destruction. It would not establish that the separator is inefficient overall: lower voltage or other benefits may outweigh that loss, and total cell energy must still be measured.

## Exact adversary 1: global composition, charge and heat do not identify the loss

This reaction-network countermodel does not assume a particular electrolyte actually realizes the rates. It shows the interface is insufficient over a physically ordinary admitted class of charge-carrying redox cycles.

Let i=Q_terminal/(2F) be terminal electron-pair equivalents over an interval, p the amount of water split, r the amount of H2 recombined with oxygen, and s the amount of a closed redox shuttle cycle transporting an electron pair between terminals without net material change. Thus

    i = p + s,
    net H2 = p - r,
    net O2 = (p - r)/2,
    net water consumed = p - r.

For any 0 < ell < i, compare:

| Realization | Water splitting p | Recombination r | Shuttle s |
|---|---:|---:|---:|
| A | i | ell | 0 |
| B | i-ell | 0 | ell |

Both have the same terminal charge and the same net chemical streams. Set the same terminal electrical work W and return all hidden inventories to their initial states. The first law then forces the same total heat,

    Q_total = W - h_water (i-ell),

at common reference conditions. Endpoint atom-isotope inventories also agree when no label-resolved reaction history is separately measured. Heat adds no independent mechanism equation once complete terminal energy and material balance already fixes it.

The local metered reactor breaks this equivalence by measuring where a specified class of reaction occurred behind a restrictive boundary. Merely adding whole-cell calorimetry or an isotope concentration to the same terminal interface does not do so. This does not defeat the stronger HOR-current incumbent: HOR is precisely an additional, reaction-specific interface.

## Exact adversary 2: heater pulses cannot validate an unknown thermal cut

An island with temperature theta, bath temperature theta_b, heat capacity C, measured heater power P, unknown thermal conductance K, and reaction heat q obeys the lumped balance

    C dtheta/dt = P + q(theta) - K(theta-theta_b).

For any delta K for which the alternative model is admissible, set

    K' = K + delta K,
    q'(theta) = q(theta) + delta K (theta-theta_b).

The equation and every temperature response to every heater waveform remaining within the admitted operating envelope are unchanged. For example, with nonnegative heater power, theta >= theta_b, q >= 0 and delta K >= 0, the alternative reaction heat remains nonnegative. Positive reaction heat can be exchanged exactly for an unknown heat shunt. At a single held temperature, the ambiguity is even simpler: P = K Delta theta - q.

An inert reference or a pre/post electrical calibration does not automatically remove the ambiguity: reacting and nonreacting islands may differ in wetting, gas composition, adsorption and thermal paths. In-situ heater modulation measures a coupled thermal/reaction response if the reaction changes with temperature. It does not magically identify K.

The proposed repair is a physically audited heat boundary: measured suspension-leg heat flux plus an isothermal guard, with bounded residual gas, liquid, radiation and lead paths. A sufficient residual-shunt bound has the form

    B_shunt <= integral sum_j K_j,max |theta_j-theta_guard| dt + B_other.

Both K_j,max and the relevant spatial temperature mismatches must be acquired. This includes heat flowing in from ordinary anode reactions: island-local heat cannot be assigned from the local temperature of a strongly thermally connected cell. Without these bounds, a finite B is UNKNOWN and (1) cannot be reported as a certificate. This is the principal technical gate, rather than sensor sensitivity alone.

A finite list of calibration trials also does not prove B for arbitrary future conditions. B requires engineering limits over an explicit operating envelope or a stated statistical coverage claim with its sampling assumptions. Moving to higher pressure, wetting, a new contaminant or an unqualified current transient leaves that envelope; the meter must return UNKNOWN until requalified.

## Exact back-action adversary: a good sink can raise crossover

For steady diffusion through a slab, c(0)=c0, c(L)=0 and diffusivity D give unmodified flux J0=D c0/L. Add a perfect absorbing reaction plane at x=a. The cathode-side feed becomes J_installed=D c0/a. At a=L/2, the installed sink receives twice the original flux.

Consequently, a recombination measurement cannot be extrapolated back to the untouched membrane even with a perfect heat meter. The islands change the H2 boundary condition, and gas cavities/ionic bypass paths also change the substrate. The theorem deliberately reports installed-device loss. An optimized uninstrumented recombiner, a lower-permeability separator or a different electrode architecture may be better for the technology.

For the proposed liquid exclusion, a capillary criterion such as

    Delta P_max < min_pores[-2 gamma cos(contact_angle)/pore_radius]

would be necessary under a simple cylindrical-pore description, but it is not sufficient evidence for a real aged compressed wall. Surface chemistry, pore-size tails, defects and local water films matter. A wetting event can add an unmetered thermal path, ionic current and electrochemical reactions simultaneously. Failure of liquid exclusion invalidates the restrictive reactor boundary until these effects are bounded; a plausible PTFE label is not a receipt.

## Consequence and cost scale, explicitly synthetic

[verify_accounting.py](verify_accounting.py) and [ACCOUNTING_RESULTS.json](ACCOUNTING_RESULTS.json) contain exact rational arithmetic for these examples and both indistinguishability constructions. They contain no laboratory data.

Using the standard liquid-water enthalpy only as a scale:

| H2-loss equivalent current density | Recombination heat per cm2 |
|---:|---:|
| 0.1 mA/cm2 | 0.148 mW |
| 1 mA/cm2 | 1.481 mW |
| 10 mA/cm2 | 14.812 mW |
| 100 mA/cm2 | 148.118 mW |

A one-hour hypothetical observation with Q_minus=60 J, B=12 J and independently validated h_max=300 kJ/mol would give L_rec=0.00016 mol, equivalent to at least 8.576 mA on a 1 cm2 cell. If escaped H2 were at least 0.00010 mol and initial inventory at most 0.00002 mol with no other H2 source, (2) would give 0.00024 mol minimum net feed. These numbers illustrate the required measurements; they are not predicted performance.

If a fixed chemical-storage budget is B0 and residual error grows at rate b, waiting longer only helps when the minimum useful reaction heat rate q exceeds b. A sufficient acquisition duration is T > B0/(q-b). A systematic error larger than the target heat rate cannot be overcome by more averaging. These are sufficient certification conditions; no lower bound on the best attainable acquisition cost or estimation precision has been established.

An idealized obstruction illustrates hardware cost. If otherwise identical ion-conducting area is reduced by fraction f, R_A'=R_A/(1-f). With R_A=0.1 ohm cm2, j=1 A/cm2 and f=1%, the added ohmic power is about 1.010 mW/cm2. A 1% pocket area sampling only 1% of a 1 mA/cm2 H2 loss would release about 0.0148 mW/cm2 of sensor heat. Thus even small hardware obstruction can exceed the directly sampled loss signal. Lateral gas collection may improve capture but is not free, and no unmeasured collection-efficiency factor may be used to turn a local lower bound into total loss.

## Strongest incumbents and novelty boundary

* **GC plus HOR currents.** Gawas et al. already combine gas and reaction-specific charge measurements. Give this comparator the same cell I,V, gas flow, pressure, temperature, conditioning, species assays and any admissible auxiliary electrodes. If HOR and complete balances resolve the relevant loss at lower total cost, our candidate has no demonstrated advantage.
* **Full two-exhaust mole balance and product assays.** Optimized whole-cell accounting can identify net lost H2 within an acquired reaction class, including cathodic Faradaic losses and leaks. It can suffer a small-difference precision problem, but no precision advantage of local calorimetry has been acquired. It also gives more direct technology-level efficiency information.
* **Established calorimetric recombination.** [Lalik et al. (2015)](https://doi.org/10.1016/j.apcata.2015.04.029) measured H2/O2 recombination with gas-flow microcalorimetry and studied humidity-dependent catalyst behavior. The core heat-to-reaction idea is established.
* **Established hydrogen calorimetric sensors.** [US20220113271A1](https://patents.google.com/patent/US20220113271A1/en), with a 2019 priority claim, explicitly describes catalytic heater/thermopile sensors in electrolyzer gas paths. [Zhu et al., ACS Sensors (2026)](https://doi.org/10.1021/acssensors.6c00697) reports a room-temperature catalytic MEMS thermopile. Its reported air/gas performance does not transfer to hot KOH or an internal separator.
* **Functional recombination separators.** Liu et al. already supply this mechanism. [Shin et al., Small Methods (2026)](https://doi.org/10.1002/smtd.202502412) reports a mid-plane Pt recombination separator. Neither source inspected here establishes the exact internal, thermal-boundary-counted measurement arrangement; a targeted search is not a historical-priority audit.

Any analysis competitor receiving the same raw calorimeter, thermal-boundary and chemical records can compute (1) and use the rest of the data. A deterministic scalar bound cannot confer information advantage over that same-data competitor. The possible advantage is the *physical boundary and acquired raw record*, with costs included, not an exclusive statistic.

Historical novelty of the full internal metered arrangement is UNKNOWN. Its scientific value is incremental until a meaningful decision is shown to improve against these incumbents. No new recombination chemistry or universal physical-information principle is claimed.

## Decisive acquisition, rather than another conditional simulation

The first required construction is one currentless gas-accessible island with a quantitatively closed thermal boundary that remains intact inside a working alkaline cell. Demonstrating a thermopile signal is insufficient.

Before any membrane-loss claim, blinded controlled gas feeds must establish an acquired conservative B under the actual cell temperature, compression, electrolyte, flow and main current. Include no-H2 trials with deliberate thermal-gradient changes, humidity steps, flooding, main-current steps, known heater inputs, and bounded combustible contaminants. Apply a known external heat source at the ordinary-anode location while the island receives no H2; this directly challenges spatial heat cross-talk. A positive certified L_rec in a true no-H2 window immediately falsifies the bound or the closure ledger. Known H2 input and independently measured output establish whether the bound is valid and usefully tight without an assumed catalyst-rate law. Isotope challenges can test inventories and contamination, but D/H or oxygen exchange must not be silently interpreted as preserved molecular ancestry.

Only then operate on actual crossover with unchanged installed hardware. Compare time- and resource-matched GC+HOR, complete mole balance, and optimized conventional thermal sensing. The primary decision is a predeclared minimum destroyed-H2 threshold relevant to choosing between two installed separator designs at measured cell power and gas purity. The proposed method passes a capability gate only if it obtains a reliable decision the incumbents cannot obtain at comparable total cost and perturbation. A validated local heat count alone is an instrumentation result, not a breakthrough in hydrogen efficiency.

The full ledger includes separator and microcavity fabrication, Pt/support mass, microfabricated heat sensors and guards, wiring, insulation, stack assembly and failed parts; capillary/pressure/aging validation; gas and chemical standards; actual electrode conditioning; all baseline heater/guard/cold-bath power; electrolyte pumping and gas handling; I,V and both-exhaust instrumentation; thermal calibration and contamination tests; storage bounds; sampling and destructive analysis; downtime and reset; interpretation compute and operator time; and the extra membrane resistance, gas transport, catalyst consumption and mechanical failure risk caused by the instrument itself. Every candidate-specific value is currently UNKNOWN. Token and inference energy telemetry was not acquired.

## Routes stopped during this investigation

1. **D2O assay for Li0 versus LiH.** This is already explicit in [Fang et al., Nature (2019)](https://www.nature.com/articles/s41586-019-1481-z) and [Tao et al., Communications Materials (2022)](https://www.nature.com/articles/s43246-022-00273-z). No invention credit is taken.
2. **Stable/isotopic crossover tags alone.** Atom labels can count transfer but do not preserve electron-transfer history. Vanadium radiotracer membrane crossover is established [2019 primary article](https://www.sciencedirect.com/science/article/abs/pii/S0376738819303692); isotope-resolved redox self-exchange is also old [Kozerski et al. (1997)](https://experts.nau.edu/en/publications/determination-of-aqueous-fesupiiiiiisup-electron-self-exchange-ra/). The latter is an author-institution abstract, not a full text acquired here.
3. **H2/D2 pulse plus water isotope inventory.** Proton/isotope exchange does not preserve molecular-H2 ancestry. No protected tag that bypasses that problem was acquired. Such data may be useful under a validated exchange model but do not justify a model-free H2-loss count.
4. **Whole-cell calorimetry as a hidden-reaction identifier.** The exact shuttle/recombination countermodel above defeats it at the stated terminal interface.
5. **Self-calibration from heater pulses only.** The exact K/q transformation defeats this claim. The corrected candidate explicitly requires a separately audited thermal cut.

## Delivery and continuation judgment

The exact conservation inequality is simple and internally derived. Its premises expose what the hardware must actually create. The concrete substrate proposal remains unbuilt. The adjacent prior art is strong, and no current result supports a consequential efficiency gain, a unique new sensing principle, lower total cost, or mission completion.

The one useful followup is a combined thermal/chemical/pressure feasibility audit of a **complete internal heat boundary**. Root has assigned a separate adversary for that purpose. If no realistic bound B can stay below the target reaction heat while preserving useful separator operation, stop this candidate. If it can, the next work is a narrowly scoped physical metrology prototype and detailed prior-art search, not another hidden-rate simulation or Capital promotion.

## Evidence categories and inspected sources

**Internal derivations:** equations (1)–(2), terminal-interface countermodel, thermal K/q equivalence, diffusion back-action example and ideal area-blocking arithmetic. These have not had an independent specialist proof audit. **Executed calculation:** standard-library rational accounting in the accompanying script/JSON. **External laboratory evidence:** only results attributed to cited primary articles. **Proposed laboratory evidence:** all island, guard, capillary, species-closure and comparative-performance results; none was obtained.

The source inspection log is [SOURCES.md](SOURCES.md). The campaign brief and prior operational-closure report were read to exclude repetition of the snapshot theorem and NV pulse-order nonlinearity assay. No Capital or other worker directory was edited.
