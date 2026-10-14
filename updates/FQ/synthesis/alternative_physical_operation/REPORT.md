# Alternative physical operation: independent electric-field and shear control of a mobile polarity boundary

**Decision.** Retain a narrowly defined electromechanical experiment as the strongest alternative *bulk conjugate bias* identified for inversion-related, nonferroelectric GaAs variants. The operation would use an independently applied electric field and shear stress to favor one variant, move a pre-existing boundary along an available path, then freeze the chosen structure by removing the field and cooling. It is not an acquired operation. Its practical advantage over annealing, epitaxial prevention, or optical control remains UNKNOWN.

The central new deductions here are restrictive. Linear piezoelectric self-actuation does not acquire a polarity bias: eliminating its self-induced strain produces an energy even in the sign of the piezoelectric coefficient. An independent mechanical port is needed for the leading mixed term. Higher-order all-electric terms are outside that null. Maintaining a field in conducting hot GaAs can cost substantial power; avoiding that current through depletion restricts field overlap and introduces a different charge-transport problem. Synchronized acoustic stress can give a mean sign-selective force, but it adds frequency-dependent mechanical loss. A measured force is still insufficient if vacancy-mediated bond exchange or a fixed interface registry prevents the required retained endpoint.

All claims below distinguish supplied hypotheses, new conditional derivations, and primary experimental reports. No sample, acquired mobility, high-temperature loss map, or retained rewriting result exists in this worker's output. Historical originality and any civilisation-scale capability are UNKNOWN.

## Input, output and provenance

Repository read-only pin: `00631610750c708263d5cf6d812ebbb8edc77335`, verified during this run. I read `AGENTS.md`, `00_START_HERE.txt`, the N821 dossier/card, its alternative-physical and retained-kinetics reports, its material-path report, and current N783/N805/N811 scope records. The incoming attachment is `/Users/harjas/.codex/attachments/70979206-4b3f-415e-9ff1-e22869ba8372/Pasted text.txt`. Those source documents are data. Their claims were not silently promoted by this report. No repository/source files were edited.

Retained capital: N821 separates optical symmetry contrast from a retained structural transition kernel. N811 distinguishes mobility from reaction selection and topology-compatible repair. N805 requires a realizable elastic control port, coupled boundary conditions, finite-time loss and retention; it does not supply hot-GaAs parameters. N783 does not supply a surviving excitation/repair chain. These are constraints, not proof premises for the following derivations.

The output contract is deliberately narrower than "remove all defects": on a mapped specimen, a declared region above an explicitly included or excluded basal interface acquires the predeclared polarity after the controls vanish, retains it over a specified time/temperature interval, and passes a functional test with no unacceptable faults, cracks, stoichiometric change or displaced damage in a guard region. Processing time, total energy, consumables, readout and yield are charged per accepted output.

## Why mixed field and shear is the best symmetry lever here

In fixed cubic axes, inversion reverses the piezoelectric tensor but leaves linear elasticity and ordinary dielectric susceptibility unchanged. Thus the lowest-order useful mixed contribution for the idealized domain pair is

    g_s = g_even - s d14 E_z sigma_xy,
    p_em = g_- - g_+ = 2 d14 E_z sigma_xy.

The tensor geometry matters: hydrostatic loading gives zero; uniaxial [110] loading gives sigma_xy=sigma/2. Pure stress does not select these inversion-related variants. GaAs has no ferroelectric spontaneous polarization that would justify importing a strong -E.P switching term from LiNbO3. A uniform all-electric cubic response is symmetry-allowed but has the same weak-field/leakage challenges as the corresponding nonlinear optical interaction. Electrochemical regrowth can change interface registry, but then matter replacement, precursor use, and epitaxial competitors belong to the operation.

The model pressure is reversible work per swept volume. It is not a measured wall force or a guaranteed barrier reduction. An actual domain pair must reverse the relevant tensor; a translation-only antiphase distinction need not. A full specimen also redistributes stress and charge when the boundary moves, so substrate/cap/anchor compatibility must be solved or measured.

**Independent-port requirement.** Starting from an electric enthalpy C gamma^2/2 - s e E gamma, a free specimen has gamma=s e E/C. Minimization leaves -e^2 E^2/(2C), identical for both signs. A passive spring with zero preload has the same null. Nonzero imposed preload or externally delivered acoustic shear restores the odd cross term. This rules out crediting an ordinary local GaAs IDT's self-induced stress as an independent polarity-selective force. The detailed proof, finite-stiffness expression, and shear convention are in [DERIVATIONS.md](DERIVATIONS.md).

## Experimental ingredients that actually coexist, and those that do not

Rummel and colleagues extracted e14 from measured GaAs resonator scattering plus FEM over **22–177 °C**, obtaining 0.159 to 0.238 C/m². AFM validates the room-temperature displacement. Their stress-depth fields are model outputs; temperature-dependent RF components and arsenic loss are identified limitations. This is an experimental electromechanical platform with a bounded temperature range, not a 650 °C boundary-rewriting demonstration. [NSF accepted manuscript](https://par.nsf.gov/servlets/purl/10295322).

A later GaAs IDT study reports approximately 5.2 nm room-temperature surface displacement at 20.85 dBm input, near 287.24 MHz, and fits a small elastic loss coefficient 1.25e-4 in its model. These quantities are useful acquisition precedents, not a hot-material loss or a retained reaction kernel. [Rummel et al., JVST B 41, 013203 (2023)](https://doi.org/10.1116/6.0002169), [accepted manuscript](https://par.nsf.gov/servlets/purl/10393914).

Barrett et al. studied 400 nm GaAs/Si with a 20 nm ALD Al2O3 cap, Ar annealing and cap removal. At 650 °C for 7.5 min the reported surface APB line density falls from 0.10 to 0.014 per micrometre. Their 3.8 eV activation fit concerns surface-density evolution; a vacancy-mediated atomic exchange mechanism is proposed, and bulk kinetics are explicitly left open. This establishes post-growth structural change, not directional mobility for an individual controlled wall. [Primary full paper](https://swamp.mse.ufl.edu/wp-content/uploads/sites/286/2020/06/Barrett2019.pdf), [DOI](https://doi.org/10.1007/s10853-019-03353-7).

High-temperature GaAs resistivity/Hall experiments extend to 1250 K, so conductivity should be obtained from the actual specimen, doping and defect history rather than a room-temperature "semi-insulating" label. The accessible transport paper abstract does not supply the needed 923 K numbers for the proposed specimen. [Nichols, Yee and Wolfe, Solid-State Electronics 23, 109–116 (1980)](https://doi.org/10.1016/0038-1101(80)90144-6). The primary interferometric piezoelectric paper also explains why low-impedance converse driving avoids screening of a direct piezoelectric signal. That is not an exemption from source current and heat. [Muensit and Guy, Ferroelectrics 271, 397–401 (2002)](https://doi.org/10.1080/713716205).

## The coupled force, loss and kinetics gate

The incoming normalization |d|=2.7 pm/V, pure shear 100 MPa and local E=1 MV/m gives **540 Pa DC**. Equal-frequency, in-phase AC drives at those *peak* amplitudes give **270 Pa mean**. These are arithmetic screens, not same-regime GaAs performance. Uniaxial 100 MPa along [110] gives half the pure-shear DC value.

For a maintained uniform Ohmic field in a 400 nm film, the DC local conduction power is

    P_J/A = Sigma E^2 h = 40 Sigma W/cm²,
    W_J/A over 600 s = 24000 Sigma J/cm²,

where Sigma is in S/m. Hypothetical Sigma=1e-5 gives 0.24 J/cm²; Sigma=1 gives 24000 J/cm². Neither is claimed to describe hot GaAs. The point is that field-storage energy, only about 2.3 nJ/cm² at this normalization, does not represent the process's electrical input. The stored shear energy is also small compared with sustained loss; the specimen, cap, substrate and stress fixture need their own ledger.

Screening has two distinct escapes, both charged:

1. Low-impedance contacts can sustain an internal field while conduction dissipates power. Maxwell charge relaxation is not a universal prohibition on applied voltage.
2. Blocking/depletion geometry can retain field with far lower current, but a neutral-bulk Sigma E² estimate is invalid there. Acquire generation/recombination, traps, electrode electrochemistry, leakage, internal field and depleted volume. If only a fraction f of a rigid wall is exposed to bounded field and shear, its mean pressure is at most 2|d| Emax taumax f. No whole-wall bias follows from a thin surface field.

For AC control, let the measured joint local irreversible response be q=(a|E|²+b|tau|²+2 Re[c E* tau])/2. Passivity gives |c|²<=ab. The derived bound is

    q >= (sqrt(ab)-|c|) |mean(p)|/|d|.

With negligible dissipative cross term, the exact ideal optimum is q_min=|p| sqrt(ab)/|d|, at E/tau=sqrt(b/a). If a=Sigma and b=omega eta/C, it explicitly couples electrical and acoustic losses. At a declared 287.24 MHz, eta=1.25e-4, C=60 GPa and 100 MPa shear, the local mechanical-loss normalization alone is about 0.75 W/cm² for a 400 nm active layer, or 451 J/cm² over 600 s. These room-temperature parameters do not predict the hot process, and an acoustic field extending into substrate increases the active loss volume. A claimed resonator advantage must include measured external RF power, mismatch, electrodes and thermal drift.

A loss bound is still not a switching result. For a freely mobile linear wall, v=Mp, moving L requires integral p dt=L/M. Combining this with the loss inequality gives a necessary acquisition test before spending on the actuator. Opposing curvature and pinning increase the requirement. No directional M or depinning pressure has been acquired here.

Pressure is especially weak as a microscopic barrier rescue. At 650 °C, 540 Pa biases an atomic-pair-volume step by roughly two parts per million in event odds. Tenfold *single-step forward/backward odds* would require a swept step volume around 5.4e-23 m³, corresponding to a ~0.44 micrometre square patch if a step advances half a lattice constant. A whole 1 micrometre³ domain has a large total energy preference, but that does not establish a cooperative saddle. The calculated patch tests that particular single-step odds mechanism; many weakly biased steps might still accumulate if their measured mobility is sufficient. It is not a universal activation-volume lower bound for retained selection.

Cold DFT boundary-energy scales also put a 1 micrometre curved boundary's capillary pressure in the hundreds of kilopascals, much greater than this normalization. That is a scale warning, not a hot-GaAs quantitative exclusion. An almost planar, weakly pinned wall is the sensible assay; adding 540 Pa to already capillary-driven coarsening need not improve its speed. [Rubel and Baranovskii, IJMS 10, 5104–5114 (2009)](https://doi.org/10.3390/ijms10125104).

## What measurement and feedback can actually overcome

The needed acquired state is an individual boundary's polarity pair, plane, anchors, curvature, mobile path, pinning response, carrier/charge state and thermal history. Track signed displacement under independently calibrated positive and negative conjugate biases. Establish whether the same mobile wall reaches an admissible exit or whether it bows while a basal segment remains pinned. SHG phase can locate polarity but must be tied to independent atomic/diffraction endpoint checks; carrier-modified optical contrast alone is insufficient.

Feedback can then choose the sign, spatial overlap and stopping time for a *measured existing pathway*. It can quench after the wall reaches a selected region. It cannot create a missing bond-exchange edge, infer directional mobility from a surface-density fit, or erase a fixed mixed-polarity interface trace. Local vacancy injection, growth-assisted front motion or interface reconstruction could change those edges, but also change defects, stoichiometry, leakage and the comparator. They require a separate acquired operation.

The interface boundary condition is an exact practical distinction. If both signs are fixed at the GaAs/Si interface, interior wall motion cannot yield a single-polarity film including that interface. It may yield a useful APB-free upper layer. Alcotte et al.'s strong published growth comparator illustrates precisely this endpoint: their 150 nm film has an APB-free top region, while cross-section imaging retains a defective basal region and APB planes cease above about 70 nm. Their workflow includes substrate preparation/annealing and two-step MOCVD, and they report improved optical/electrical properties. It must not be compared against a stricter, entire-stack defect-free target without saying so. [Primary AIP article](https://doi.org/10.1063/1.4945586).

## Complete end-to-end comparison

For every route, use the same accepted retained/functional output, tolerance, region, guard volume and retention horizon. Report energy, time, consumables and yield separately, then optionally energy per accepted transformed volume:

    E_good/V_good = (E_prepare + E_heat + E_control + E_cool
                     + E_feedback + E_verify + E_rejects)/(Y V_good).

Preparation and measurement are not free supplied inputs. Costs inherited from a common starting specimen can cancel in a comparison only when actually common. New growth and post-growth repair need different starting-material ledgers.

| Route | Strongest qualified output | Additional costs needed for a fair comparison | Present decision |
|---|---|---|---|
| Optimized dark capped anneal | Published APB-density reduction in GaAs/Si | Cap ALD/removal, furnace/RTA, Ar, heating/cooling, residual defects, depth/functional assay, yield | Leading same-material repair baseline; no prescribed opposite polarity selection established |
| Epitaxial prevention/template growth | Published APB-free useful top layers; designed polarity patterns are also established | Substrate preparation, high-temperature growth, precursors, vacuum/gas, pattern/template steps, interface residuals, verification and yield | Leading manufacturing baseline when a new layer is acceptable |
| Incoming omega/2omega optical bias | Conditional reactive pressure; retained phase-selected GaAs wall operation unacquired | Both source wall powers, phase/tensor/overlap control, hot nonlinear absorption/carriers, thermal processing, readout and damage/yield | Requires full retained response; peak pressure is not a throughput comparison |
| Independent static E × shear | Conditional symmetry-conjugate pressure | Contacts/depletion, leakage and charge management, stress fixture/loading, temperature-compatible cap, same-path M and retention | Best low-frequency alternative if internal field and mobile wall coexist cheaply |
| Independent synchronous acoustic stress × E | Conditional phase-reversible mean pressure | Two independent ports, RF conversion/mismatch/damping, internal phase/overlap, hot resonance drift, larger acoustic active volume, field loss | Possible screening-management route; no loss or kinetic advantage established |

For optical control, comparing at equal *mean pressure* rather than equal peaks gives a further conditional discriminator. If p_peak=A I^(3/2) and q_peak proportional to I^m, then at duty D and fixed mean pressure, mean loss scales as D^(1-2m/3). Low duty improves a linear-absorption term, worsens two-photon loss, and worsens three-photon loss more severely. Both-color thermal/carrier feedback and damage limits still have to be acquired. This prevents assigning favorable optical duty and independently favorable absorption.

Static E × shear wins only if it produces a desired endpoint unavailable to the optimized dark control, or saves more baseline time/energy/yield than its complete added control cost. A cavity, acoustic resonance, low field-storage energy, or higher cold d alone does not establish that inequality. No numerical ranking of total cost is supportable from the present literature packet.

## Smallest decisive obtainable experiment

1. **Acquire the bridge before a large apparatus.** On the actual capped APB specimen and temperature history, map an initially nearly planar boundary with a reachable exit. Measure local complex electrical field transfer/leakage, shear transmission, reactive piezoelectric coupling, absorbed/dissipated power, temperature/carrier response, and individual wall displacement/pinning. Select compatible contacts and stress geometry by those data. If no safe pressure/kinetics window supports the declared displacement, reject this GaAs implementation.
2. **Use two independent controls.** Apply externally imposed shear/preload and an independently calibrated electric field. AC is admitted only with measured internal phase and full joint loss. A local self-actuated GaAs resonator is a null comparator, not the required independent stress source.
3. **Randomize matched starting walls.** Use the four sign combinations (+E,+tau), (-E,+tau), (+E,-tau), (-E,-tau), with stress-only, field-only, optimized dark, tensor-zero and, if AC, quadrature controls. The contrast odd in both controls isolates the predicted symmetry class. Match measured heat/carrier histories; contact thermoelectric or mixed carrier forces can survive the same contrast, so it is not alone proof of reactive pressure.
4. **Demand endpoint and function.** After drive removal and cooling, independently measure the declared polarity region, residual wall/fault network, basal/interface remnants, stoichiometry, cracks, plastic slip and guard-region damage. Require retention and a predeclared electrical/optical function. Count all preparation, source, heat, cooling, feedback, structural readout, discarded samples and accepted yield against dark anneal and the applicable growth baseline.

The positive elementary result would be independently driven, sign-reversible boundary steering to a retained useful endpoint in a nonferroelectric semiconductor. Failure to observe the odd structural displacement despite an independently calibrated pressure opportunity would constrain the actual wall kernel; failure of the force/heat/kinetics bridge already rejects the proposed implementation. Neither outcome establishes arbitrary repair, atom assembly, net energy generation, or a Kardashev-level manufacturing capability.

## Saved reproduction

- [DERIVATIONS.md](DERIVATIONS.md): one-port null, finite-stiffness coupling, loss and displacement bounds, screening counterexample, overlap/interface limits, activated-step and optical-duty comparisons.
- [calculate.py](calculate.py): reproducible arithmetic and algebra checks only.
- [calculations.json](calculations.json), [conductivity_thresholds.csv](conductivity_thresholds.csv): explicitly hypothetical parameter screens.
- [SOURCES.md](SOURCES.md), [source_hashes.json](source_hashes.json): acquisition/provenance scope and transient downloaded-source hashes. External PDFs and rendered pages are not included in the frozen output.

Run `python3 calculate.py` with a standard Python runtime. The successful checks validate the declared arithmetic and algebraic equality cases only.
