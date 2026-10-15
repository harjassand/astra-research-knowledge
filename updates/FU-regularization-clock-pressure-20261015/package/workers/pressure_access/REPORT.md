# Pressure-write access audit

Decision: **no acquired same-state post-extraction high-temperature current/field/retention operation**. The physical performance, retention under useful load, comparative advantage and Astra novelty remain **UNKNOWN / NOT ACHIEVED**. This is an independent documentary and mathematical audit, not a physical experiment or an independent replication.

The principal useful acquisition in this tranche is the **published supplement**, obtained from the official Europe PMC supplementary archive beyond arXiv. The absent `astra_pressure_write_audit.zip` remains absent; its alleged contents were not reconstructed or treated as evidence. The supplied pasted text was DATA.

## Evidence contract and acquired source facts

Main reference: [Deng et al., PNAS 123 e2536178123 (2026)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12993975/), DOI [10.1073/pnas.2536178123](https://doi.org/10.1073/pnas.2536178123). Published XML and a nine-page SI were acquired from [Europe PMC full text](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12993975/fullTextXML) and [supplementary archive](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12993975/supplementaryFiles).

The following compact source ledger preserves the relevant distinctions:

| Observation / method | Source scope |
| --- | --- |
| Maximum retained transition | 151 K **resistive onset**, inside DAC; not qualified zero resistance |
| Current perturbation | S2, 0.2–50 mA, inside DAC; SI S3 has finite resistance on an ohm scale; authors discuss heating/relaxation artifacts |
| Aging | S3, at least three days stored at 77 K inside DAC, with temperature scans; not a high-temperature loaded hold |
| Extracted specimen | S2, magnetic onset about 140 K; SI S6 plots its signal multiplied by ten |
| Shielding estimate | About 78%, calculated at **70 K**, using `|M|/H=1.9e-8 emu/Oe`, `r=42.5e-4 cm` |
| Mechanical protocol | Room-temperature ruby/Raman pressure calibration; screw release at 4.2 K; cBN medium; Van der Pauw contacts |
| Specimen / structure | Square diagonal 80–120 micrometres, thickness about 20 micrometres; broader diffraction peaks and slightly expanded quenched lattice |
| Computational interpretation | Pressure-dependent Lifshitz crossing; proposed trapping barrier unmeasured |

The official supplementary ZIP contains the SI PDF plus article JPG/GIF figures. It contains **no raw numerical V/I/T/time records or diffraction frames**. The XML links no separate data repository. Bounded searches of exact DOI/title, GitHub and named data repositories found no publicly retrievable raw traces or independent post-extraction transport replication; this is not an exhaustive absence proof. Receipts, search results and exact read ranges are saved in `sources/` and `READ_RANGES.json`.

The SI sharpens, rather than closes, the missing physical interface. A temperature-dependent resistance drop can identify a superconducting contribution while other regions, interfaces or current paths still dissipate. The current scan does not establish a finite-current zero-voltage interval. Its changes can also involve temperature and time: a current reversal cancels an additive thermoelectric offset, but **does not cancel Joule heating or a changing specimen**. A temperature scan with an onset marker is not an isothermal I–V curve.

The extracted magnetic trace is valuable evidence of a surviving superconducting response. However, the low-temperature shielding estimate cannot identify the fraction responsible for the enhanced-temperature tail. A specimen containing ordinary superconducting material and a smaller enhanced region fits that distinction. Neither volume fraction nor magnetic shielding guarantees a percolating transport path; neither gives a positive lower bound on its weakest cross-section. No favorable measurements from different samples or preparation histories are joined here.

## Reconstructing and limiting the residual-stress argument

Let `tau` be Cauchy stress relative to uniform ambient pressure. For a static body, `div(tau)+b=0` and boundary traction `t=tau n`. Multiplying the balance equation by `x_j` and integrating gives

`integral_Omega tau_ij dV = integral_boundary x_j t_i dA + integral_Omega x_j b_i dV`.

Thus negligible body forces and **zero traction on the entire boundary** imply `<tau>=0`. The stress is a spatial volume average; homogeneous density, isotropy and linear elasticity are not required. Contacts, mounting, gasket support and surface forces must appear in the boundary term. At finite acceleration there is an additional inertia term. During loaded service, electromagnetic body forces can matter, so the unloaded free-body identity cannot simply be carried into a high-field current test.

Define hydrostatic compression `p=-tr(tau)/3`. Suppose a volume fraction `f` has `p>=p_star>0`, and the complement's mean pressure is at least `-S`. Then

`0=<p> >= f p_star-(1-f)S`, hence `f<=S/(S+p_star)`.

If an independently bounded mean compression is `p_bar<=p_bar_max`, the generalized bound is `f<=(S+p_bar_max)/(S+p_star)`, capped at one. A uniaxial tensile-strength number is not automatically the required bound on mean hydrostatic tension.

**No numerical fraction exclusion follows here.** The required residual pressure `p_star`, the relevant complement tension bound `S`, and the enhanced-state volume fraction are unacquired. The writing pressure is not `p_star`. The shielding estimate is not `f`. The argument rules out only a uniformly retained external-pressure stress throughout a truly liberated unloaded body. It does not rule out eigenstrain, oxygen rearrangement, local self-equilibrated stresses, structural defects, electronic order or metastability. In particular, average stress zero does not imply average strain zero: `tau=C:(epsilon-epsilon_star)` admits changed stress-free geometry. The paper already discusses strain/defects and expansion, so the identity is not a refutation of its actual proposed explanation.

An XRD line width alone does not provide the missing stress field: instrumental width, domain size, defects and microstrain must be separated, with a specimen-specific constitutive calibration. Do not refine guessed moduli or strengths to rescue this gate.

## Reconstructing and limiting the occupation-convexity argument

For fixed one-electron energies and positive temperature,

`F(n)=sum epsilon_k n_k + k_B T sum[n_k log n_k+(1-n_k)log(1-n_k)]`.

On `0<n_k<1`, `d2F/dn_k2=k_B T/[n_k(1-n_k)]>=4 k_B T`. Restriction to a fixed-number affine subspace preserves strict convexity. This occupation-only equilibrium model has a unique minimizer. A pressure-dependent band crossing alone therefore supplies neither two minima at the same final Hamiltonian nor a kinetic lifetime.

The limitation matters as much as the calculation. It is not a theorem excluding memory in the full coupled material. With two levels of energies `+gq` and `-gq`, total occupation one, and a structural/order coordinate `q`, consider

`F(n,q)=gq(2n-1)+2 k_B T h(n)+K q^2/2+lambda q^4/4`, `lambda>0`,

where `h(n)=n log n+(1-n)log(1-n)`. The occupation block is strictly convex. Eliminating it nevertheless gives

`F_eff(q)=K q^2/2+lambda q^4/4-2 k_B T log[2 cosh(gq/(2 k_B T))]`,

with `F_eff''(0)=K-g^2/(2 k_B T)`. For `0<K<g^2/(2 k_B T)`, the joint system has a double-well effective potential. This is a mathematical counterexample to an overextension of the convexity claim, **not fitted Hg1223 coefficients or a material prediction**. Conserved or kinetically isolated occupations also require a dynamical analysis. The decisive task is to measure a history-storing coordinate and its relaxation together with useful current, not infer a barrier from an equilibrium band plot.

## Strong primary competitors

These are separate existing capabilities, not properties of the pressure-written specimen:

| Primary source | Verified comparator and qualification |
| --- | --- |
| [Gapud et al., Phys. Rev. B 56, 862 (1997)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.56.862); [author-posted paper](https://www.researchgate.net/publication/230822693_Effects_of_1-MeV_proton_irradiation_in_Hg-based_cuprate_thin_films) | Hg1223 transport bridge: pre-irradiation zero-resistance transition 123.6 K and `Jc=0.27 MA/cm^2` at 100 K; electric-field criterion `1 microvolt/cm`. Low-dose pinning improvement competes with superconducting degradation. Primary paper text verifies the pasted numerical comparator. |
| [Moriwaki et al., Physica C 303, 65–72 (1998)](https://www.sciencedirect.com/science/article/pii/S0921453498002470) | Publisher abstract: (Hg,Re)-1223 film, zero-resistance transition 127.5 K; transport `Jc=1.5 MA/cm^2` at 77 K self-field and `0.12 MA/cm^2` at 1 T parallel to c. Film active area is not packaged engineering area. |
| [Li et al., Supercond. Sci. Technol. 39, 055021 (2026)](https://doi.org/10.1088/1361-6668/ae6c9c); [acquired author version](https://arxiv.org/html/2605.05800v1) | Publication status is corrected from “preprint”: journal metadata verified; full publisher PDF blocked. Author-version details: Bean-model magnetic inference, proton-treated single crystals, current enhancement with a transition-temperature tradeoff and appreciable relaxation. The `77 K` self-field result supplies no `140 K` pressure-state transport or lifetime. |
| [Hartwig et al., IEEE Trans. Appl. Supercond. 34, 0600316 (2024)](https://doi.org/10.1109/TASC.2023.3332613); [published PDF at KIT](https://publikationen.bibliothek.kit.edu/1000166953/151963422) | Representative-scale REBCO coil: 20.1 T peak field on conductor at 40.5 kA, nominal 20 K operation; first campaign included a five-hour full-current hold. A distinct 31.5 kA, 24 K campaign included a 24-hour flat top. Published diagnostics include joints, current sharing, cooling and mechanical response. Intentional quench produced localized damage; protection is not a solved universal property. |

The main same-task high-field comparator is the measured coil, not an ideal material critical temperature. The two coil campaign results are deliberately not presented as one simultaneous operating point. The useful power operation already demonstrated by REBCO is controlled large field and current with measured thermal and mechanical response. Its costs and quench limits still matter.

The acquired irradiation author version reports an optimum-dose self-field magnetic `Jc` exceeding `0.5 MA/cm^2` at 77 K and a pristine irreversibility field of approximately `1.2 T` at that temperature. It derives current from magnetization hysteresis and studies relaxation for about an hour. These are informative constraints on pinning and creep, not sustained transport qualifications. Raising onset, adding defects, resisting vortex motion and retaining the written state under load are coupled obligations; maximizing one independently does not close the others. No depairing-current estimate or irradiation result is inserted into a pressure-state calculation.

## Concrete arithmetic and complete-resource boundary

`calculate.py` reproduces `calculations.json`; all material performance inputs remain unknown.

The supplied proposed bridge target gives `I=1.2 A`, `Vcrit=5 nV`, `Rcrit=4.167 nOhm`, and segment electrical loss `6 nW`. The current is 24 times the largest current in the source perturbation scan, and 6,000 times its smallest. These ratios do not estimate the source's critical current. Van der Pauw geometry does not justify treating the nominal area as a uniform transport-bar area.

At that current density, an infinite uniform-sheet estimate gives about `12.6 mT` self-field at a broad face. This is an approximation, not an edge-field calculation, and shows why externally applied field alone does not describe the coupled operating point. A transverse `0.1 T` gives a force of `6 microN` over the proposed voltage segment. Mounting, self-field, temperature, current distribution and creep must coexist in the same test.

For one contact, `P=I^2 R_contact`: a hypothetical `1 microOhm` contact would dissipate `1.44 microW`, 240 times the segment criterion loss; `1 milliOhm` gives `1.44 mW`. These are sensitivity examples, not acquired contact resistances. Noise and offsets require calibration on the actual wired specimen. Johnson-noise calculations alone cannot certify nanovolt measurement precision.

For a matched useful electrical output, use

`P_wall,loss = P_electrical,loss,total + (Q_parasitic,cold + P_electrical,loss,cold + Q_other,cold)/COP_actual + P_aux + E_preparation_per_qualified_unit/t_service`.

Define the boundary to avoid counting the same auxiliary twice. Cold electrical loss is correctly counted as electrical input loss and as refrigerator heat load. If preparation energy is per attempt instead, qualification yield must divide it before amortization. Include unsuccessful growth/writes, containment, tooling, gas handling, initial cooling, extraction/contact damage, qualification, stabilizer/insulation, protection, rewrites and replacement. No defensible total energy or cost advantage can be computed without these data.

With 300 K rejection, Carnot minimum work per removed watt is `2.896` at 77 K and `1.143` at 140 K: a factor `2.534` at **identical heat load**, not an actual system saving. A hotter state may require more conductor or lose current under field. The cold writing/handling path and service lifetime remain separate obligations.

The source specimen geometry gives `0.064–0.144 nL`, with a midpoint volume ratio of ten million specimens per cubic centimetre. This is a scale gap, not a manufacturing architecture. `10 GPa` over `1 cm^2` requires `1 MN`; it is not an energy estimate. Measure actuator `integral F dx`, sample `integral P(-dV)`, losses and equipment energy separately. The source's slow growth and annealing schedule alone corresponds to about `391–511 hours` using a 25 C room-temperature ramp endpoint, before setup, pressure writing, failures and qualification. That arithmetic is a process-time accounting, not an energy measurement.

## Decision and narrow continuation

The ambitious joint target is still only a proposed acceptance test. For the extracted state, placing a transport target at a magnetic onset gives no demonstrated current or temperature margin. The best next experiment is the **smallest post-extraction transport screen above the pristine transition**, using the already demonstrated warm extraction route, followed by controlled release/thermal comparisons only if the screen finds a conducting enhancement. The exact protocol and failure scope are in `ASSAY.md`.

Do not launch a defect/pinning optimization or fit retention coefficients before this gate. If it fails, preserve the pressure-quench result as state-retention physics and redirect high-field energy work to the demonstrated REBCO operation and its measured current-sharing/quench bottleneck. No invented device is required to rescue this candidate. Scientific access to a surviving extracted state can still be valuable for microscopy/spectroscopy, but it does not establish a superior conductor.

Astra capital was used only after source selection, through pinned N654 and its exact conservation-budget ranges. Its applicable lesson is the requirement for useful loaded output and an inventory in the same experiment. It supplies no superconducting material property. Pin: `0c789ca775808e23e57138b56a393ad1e58cb15c`.
