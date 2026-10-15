# Physical adversary: hidden inventories, silent crossings, and actionable tests

15 October 2026, Australia/Brisbane. **Status: internal analytic audit and experimental designs; no laboratory work, new device, safety certification, novelty clearance, or capability advantage.** All writes are confined to this worker directory. Capital was not edited.

The leading separator proposal has a useful electrical inequality, but its physical inventory premise is unacquired. A conductive interlayer can miss a pore-following or SEI-insulated filament. Even after an alarm, electrical isolation does not bound how much pre-existing lithium can move into the remaining slab. Published experiments demonstrate mechanical shorting before electrochemical cycling in a high-pressure porous solid electrolyte, while also showing that this mechanism does not occur at every tested pressure. The right next step is a deliberately small set of geometry, pressure, and port-accounting falsification experiments.

This is a different failure explanation from computational operational closure. The obstacles are topology, mechanical transport, electrochemical contact selectivity, the location of stored material and energy, actuator authority, and the relationship between an electrical proxy and a thermal outcome. A competing inference algorithm cannot repair those physical interfaces.

## 1. The guard interface and the part of the bound that survives

The current decision-control candidate places a third-terminal guard at depth `a` of a separator of thickness `L`. The remaining slab has thickness `d=L-a`. The guard is held at a current-limited oxidizing bias relative to the anode. Its event triggers external charging interruption; a stripping pulse was considered, but the revised preventive bound does not rely on interpreting aggregate stripping current as metal removal.

For an Ohmic lithium region of volume `V` in the remaining slab, with conductivity at most `sigma_max` and an electronically insulating complement,

```
G_guard,cathode <= sigma_max V / d^2.
```

The Dirichlet trial potential `phi=z/d` proves this: its dissipation at unit voltage is at most `sigma_max V/d^2`; the actual potential minimizes that dissipation. A straight constant-area rod attains equality. Adding an ideal plane at anode potential cannot decrease anode-to-cathode conductance, so it can serve as a mathematical upper comparison. This argument does not require a minimum dendrite radius. I found no counterexample within that stated Ohmic geometry. The independent guard-bound worker is auditing the theorem separately.

The proposed physical continuation is

```
V(t) <= V0 + alpha Q_res,       alpha = M_Li/(F rho_Li),
G_short(t) <= sigma_max [V0 + alpha Q_res] / d^2.
```

The first line requires more than a current integrator. A conservative local material balance is instead

```
V_upper(t) <= V_upper(0)
              + alpha integral I_red,upper^+(s) ds
              + integral J_metal,in^+(s) ds
              + V_other_source^+(t).
```

`I_red,upper^+` counts all positive local lithium-reduction currents in that slab, including internal and guard-fed paths. `J_metal,in^+` is incoming metallic volume flux across its boundary, including creep and mechanically driven extrusion. Losses can be ignored for an upper bound. A net terminal current is not automatically an upper bound on the positive local reduction current; opposite local currents can cancel. Nor does a zero terminal current make the advective term zero. A valid `Q_res` must bound the relevant positive local electron supply or explicitly include all internally transferable inventory.

The theorem also needs a material boundary. For a passive linear electronic-conduction problem with leakage or non-lithium conductive inclusions, a more general trial bound is

```
G_electronic <= (1/d^2) integral_slab lambda_max[Sigma_e(x)] dx.
```

Here `Sigma_e` is the electronic conductivity tensor. Active electrochemical source terms and nonlinear breakdown require an additional model. A lithium-only volume certificate does not bound copper contamination, conductive carbon, electronically conducting interphase, or a changing current-collector geometry. Ionic conductivity is not electronic conductivity and must be measured separately.

Finally, `G_short <= G_h` is an electrical conclusion. A safe `G_h` must come from a specimen-specific thermal/chemical limit. At a bounded voltage `E_max`, total electrical bridge power is at most `E_max^2 G_short`, but a total-power bound does not itself bound peak temperature without thermal geometry. For fixed bridge resistance, concentrating a finite fraction of the resistance in a progressively smaller neck preserves its heat while reducing its thermal mass. Conductance alone therefore does not supply a universal harmless-short threshold. Direct chemical reaction, electrolyte decomposition, and already stored heat remain separate energy terms.

## 2. Exact adversarial models and the experiment that distinguishes each

### 2.1 A porous guard is not a geometric cutset

Let the guard cover the plane `z=a` except for an open pore disk of radius `R`. A straight lithium cylinder of radius `r<R` can run from anode to cathode through that disk without intersecting the guard. Its guard current is exactly zero in the ideal model and its final electronic conductance is positive. Interconnected metal in the plane is compatible with this counterexample: electrical continuity of a mesh does not make it a separating surface in three dimensions. Staggering porous layers does not establish a cutset if a tortuous connected void path remains.

**Decisive test:** fabricate an intentionally registered pore or edge seam at the proposed manufacturing tolerance. Grow or position a known conducting filament through it while monitoring guard current, guard potential, and independent anode-cathode conductance. Image its three-dimensional path. A bridge preceding any qualified alarm refutes universal interception for that geometry. A successful tested pore does not cover smaller, untested paths; a positive contract needs a certified lower filament size, a truly dense barrier, or a reactive interception mechanism that covers those voids.

The passive copper detector is close prior art. Wu et al. used a 50 nm copper coating between two 12 micrometre separators while retaining porosity. Their full paper describes contact-induced potential collapse and explicitly notes that connection opens copper surface to lithium deposition, reducing electrode separation. That is evidence for a working contact alarm in their specimens and for a possible back-action, not a proof that every crossing is detected. [Wu et al., Nature Communications 5, 5193 (2014)](https://doi.org/10.1038/ncomms6193).

### 2.2 A mechanically touching filament can be electrically silent

Take a metallic lithium core of radius `b`, covered by an electronically insulating shell of thickness `h`. Its tip is electrochemically accessible, while its side contacts the guard through the shell. For an ideal cylindrical shell of electronic conductivity `kappa`, contact length `ell`, and bias `U`, the radial conductance is

```
G_shell = 2 pi kappa ell / log[(b+h)/b],
I_guard = U G_shell.
```

For any finite detector threshold and finite bias, this model admits a sufficiently small `kappa` so that the core passes with no qualified event, while retaining high axial metallic conductance. This is a counterexample to an unspecified minimum signal, not evidence for a particular shell conductivity in the intended cell. A dense hard guard might prevent passage or fracture the shell; that mechanical fact must be acquired rather than presumed.

**Decisive test:** use bare and deliberately electron-insulated conducting microprobes of independently measured axial conductance and shell leakage. Bring them to, and if mechanically possible through, the exact wetted guard under qualified pressure. Record the minimum alarm charge before independent terminal connectivity. Include a bare-metal positive control and an insulating non-metal probe. Destructive cross-sections must determine whether the shell was breached. The contract needs an observed contact-transfer floor over the admitted shell/pressure family, not just sensitivity to bare lithium.

### 2.3 Hidden distal metal defeats an alarm-based initial-volume inference

Before the first guard contact, put a detached lithium rod of radius `b` in the upper slab, extending from `a+epsilon` to `L-epsilon`. After the first alarm, two short connecting segments, each of length `epsilon`, make a nearly full-length conducting rod. Their new plating charge tends to zero with `epsilon`, while the final conductance tends to `sigma pi b^2/d`. The initial distal volume is not small merely because the guard has not yet alarmed. The `V0` term correctly covers this model **if it is independently bounded**; the alarm record alone cannot supply that bound.

Internal nucleation is a real material possibility. Han et al. used operando neutron depth profiling and reported lithium deposition inside bulk LLZO and Li3PS4, contrasting it with their LiPON cells; they attribute the difference largely to electronic conduction. This is substrate-specific evidence, not proof that the proposed guard material nucleates lithium. [Han et al., Nature Energy 4, 187–196 (2019)](https://doi.org/10.1038/s41560-018-0312-z), acquired author PDF, pp. 1–6.

**Decisive test:** put a quantified distal metal inclusion into otherwise matched test slabs. Measure first-event time and the additional charge required for terminal connection. Separately section aged but never-alarmed guard specimens using a calibrated metal-sensitive method. A batch distribution can support a probabilistic `V0` specification; it is not a universal per-device volume bound unless the manufacturing inspection covers every relevant region.

### 2.4 Stored metal and pressure can cross without new plating charge

Put a finite metallic lithium reservoir below the guard and a permeable pore/crack through or around it. After electrical isolation, use a mechanically loaded piston to extrude metal into the upper slab. The upper volume increases by the displaced reservoir volume while `Q_res=0`. Mechanical work, previously stored elastic energy, or applied stack pressure pays for the motion. This violates the charge-only volume cap without violating the conductance-volume inequality. Choosing `V0` to include all movable lithium in the cell restores a bound but may make it too large to be useful.

This mechanism has unusually direct published support. Doux et al. report a Li|Li6PS5Cl|Li cell shorting mechanically at 75 MPa before plating/stripping, with creep through a porous pellet. Their same text explicitly says that at 25 MPa zero applied current did not produce shorting over prolonged times; cycling was required. Thus high-pressure zero-charge shorting is demonstrated, while rapid failure at ordinary guard pressures is **UNKNOWN**. [Doux et al., Advanced Energy Materials, 1903253 (2020)](https://doi.org/10.1002/aenm.201903253), [acquired preprint](https://arxiv.org/abs/1910.02118), PDF p. 6, printed p. 5.

**Decisive test:** with all electrical ports opened and their leakage measured, apply the admitted post-alarm pressure/temperature history to a preloaded metal reservoir and exact guard stack. Track mechanical displacement, load, transferred metal volume, and terminal conductance. Repeat with pressure released after the simulated alarm. This directly measures or refutes the missing `J_metal,in` cap. A pressure-release actuator is useful only if it reduces transfer while retaining the interface and mechanical integrity needed for safe storage.

### 2.5 Local redistribution can grow upper metal at zero net terminal current

Connect a high-chemical-potential lithium region below the guard to a lower-chemical-potential metal seed above it through an internal electronic and ionic circuit. With effective driving voltage `Delta_mu/F`,

```
I_internal = (Delta_mu/F)/(R_e+R_ion),
dV_upper/dt = alpha I_internal,
I_external = I_guard = 0.
```

The lower region dissolves while the upper seed grows. Stress, curvature, or concentration differences can supply the finite free energy. This idealized internal galvanic circuit is a separate countermodel from physical extrusion. A terminal integrator sees no net charge, but the positive local reduction current is nonzero. The intended physical material may block the electronic path; if so, that blocking is the acquired premise.

**Decisive test:** isolate terminals, impose independently calibrated pressure/chemical-potential differences on two spatially resolved metal regions, and track local metal inventory rather than only total lithium. Measure electronic leakage across the proposed gate before and after aging. A null result bounds this specified internal circuit at the achieved resolution; it cannot exclude every unknown chemical reservoir.

### 2.6 Guard current and a stripping command do not establish metal removal

A direct metallic contact can carry electronic shunt current without oxidizing the dangerous branch. In general,

```
I_guard = I_electronic_shunt + I_Faradaic + I_capacitive + I_background.
```

A current-limited clamp of `I_max` facing contact conductance `G_c` cannot hold more than `I_max/G_c` across that contact. For the illustrative circuit `I_max=1 mA`, `G_c=1 S`, the supported voltage is only 1 mV; holding 50 mV requires at least 50 mA before parasitic loads. These values are circuit examples, not measured electrochemical thresholds. If the clamp collapses, the connected layer can become an extension of the anode rather than an oxidizing trap. If a stripping pulse removes a narrow proximal neck first, a distal metallic fragment can survive while the current falls to zero.

**Decisive test:** record actual guard potential with a sufficiently fast Kelvin/reference measurement during contact; measure current at every port and distinguish capacitive/background charge using identical no-filament controls. Quantify remaining distal metal after the pulse. Compare active bias, floating guard, current-limited saturation, and deliberately failed electronics at equal initial geometry. A higher alarm current with more surviving distal metal is a falsifier of the assumed charge-to-removal interpretation. The revised volume theorem wisely does not rely on that interpretation.

## 3. Nominal scales: what a useful latency contract would have to beat

The reference calculation uses lithium resistivity `9.28e-8 ohm m` at 293 K, density `534 kg/m^3`, molar mass `0.006941 kg/mol`, and `F=96485.33212 C/mol`. The first value is in Chi's recommended table; its uncertainty and purity qualifications must be retained. These are nominal bulk references, **not a certified upper conductivity for the proposed filament**. [Chi, Electrical Resistivity of Alkali Elements, Table 3 (1979)](https://doi.org/10.1063/1.555598), [NIST density](https://physics.nist.gov/cgi-bin/Star/compos.pl?matno=003&mode=text), [NIST molar mass](https://webbook.nist.gov/cgi/cbook.cgi?Formula=Li&NoIon=on).

They give `alpha=1.34716e-10 m^3/C`. A straight rod with `G=1 S` saturates the nominal volume inequality:

| Remaining thickness | Rod radius | Metal volume | Plating charge | Same charge at 1 A |
|---|---:|---:|---:|---:|
| 10 micrometres | 0.5435 micrometres | 9.28e-18 m^3 | 68.89 nC | 68.89 ns |
| 20 micrometres | 0.7686 micrometres | 3.712e-17 m^3 | 0.27554 microcoulombs | 275.54 ns |
| 50 micrometres | 1.2153 micrometres | 2.32e-16 m^3 | 1.7221 microcoulombs | 1.7221 microseconds |
| 100 micrometres | 1.7187 micrometres | 9.28e-16 m^3 | 6.8886 microcoulombs | 6.8886 microseconds |

`1 S` is an illustrative electrical target, not a universal danger threshold. At `d=20 micrometres`, assigning all of `1 A x 10 microseconds` to upper-slab plating yields only the loose nominal bound `G<=36.29 S`. At `1 mA x 100 microseconds`, the corresponding bound is `0.3629 S`. Initial metal, movable metal, guard supply, charged circuit elements, and internal redistribution make the cap larger.

These scales do not prove the concept impractical. They identify regimes worth separating: a small-current microcell, larger remaining thickness, or a directly qualified local current-routing fraction might satisfy a useful cap. A total-current bound at ampere scale is much more demanding. There is no measured detector latency, local plating fraction, conductivity maximum, or safe conductance threshold in the present packet.

Arithmetic and exact countermodel scores are saved in `audit_calculations.py` and `CALCULATION_RESULTS.json`. They are calculations on declared models; no synthetic trajectories were passed off as observations.

## 4. A different high-consequence operation: finite-horizon ionic quarantine

The alternative physical action is to suppress **ionic transport inside the cell** after a precursor, rather than merely disconnect the charger. The operational output would be a finite, verified quarantine interval during which internal electrochemical discharge cannot exceed a stated heat/charge budget. This would change the storage/removal decision after an alarm. It would not certify permanent safety or reverse damage.

The actuator class is established. Gonzalez et al. demonstrated a third-terminal PPy:PDA iongate separator, with reduced state limiting ion transport; its measured added areal resistance changed from 255 to 2443 ohm cm^2 after baseline subtraction. Their main text distinguishes fast polymer charge switching from full-cell shutoff taking tens of seconds. Pinholes and on-state resistance trade off against off-state blocking. These results do not establish nanosecond interception or perfect isolation. [Gonzalez et al., Advanced Functional Materials, 2102198 (2021)](https://doi.org/10.1002/adfm.202102198), [full author PDF](https://liugroup.ucsd.edu/wp-content/uploads/2021/07/adfm.202102198.pdf), pp. 3–6.

The proposed decision contract is new analysis here; the iongate mechanism is not claimed as new. If all relevant ionic paths cross a gate whose **damaged-state** conductance is bounded by `K_off`, cell EMF is at most `E_max`, and a lumped positive-resistance circuit is qualified, then

```
I_internal <= E_max K_off,
E_electrochemical(T) <= E_max^2 K_off T.
```

A sufficient quarantine condition would be

```
E_local_reactive + E_switch + E_residual_before_off
 + E_max^2 K_off T + E_other_exotherm(T) <= E_thermal_margin(T),
```

with uncertainty included. `E_local_reactive` covers metal already on the cathode side and direct local reaction that does not need cross-gate ion transport. The contract fails if a mechanical puncture opens an ionic bypass, the gate switches nonuniformly, its bias creates a new electronic path, or the chemical/thermal margin is unbounded. All of those are measurable interface questions. The published order-of-magnitude resistance increase is not automatically enough for a large-area cell: total conductance scales with area.

**Decisive comparison:** use the same precursor record, cell chemistry, active capacity, initial SOC, pressure, cooling, computation, and permitted removal time. Compare (A) external charger isolation, (B) active metal guard, (C) known passive current-limiting interception, and (D) alarm-triggered iongate. Impose matched, characterized internal electronic contacts and separately matched mechanical punctures. Measure internal discharge, all guard/gate electrical work, local temperature, calorimetric heat, capacity loss, and failure to switch. The primary outcome is heat and residual energy over the predeclared quarantine interval, not a voltage drop or a nominal off-state resistance measured before damage.

A particularly strong existing comparator is the partially electronically conducting Janus separator. Gonzalez et al. explicitly designed it to intercept a dendrite, raise short resistance, and drain charge slowly, with laboratory cycling and abuse comparisons. It should receive the same capacity, thickness, temperature, and fault-family budget; a bare separator is too weak a baseline. [Gonzalez et al., Draining Over Blocking, Advanced Materials, 1906836 (2020)](https://doi.org/10.1002/adma.201906836), [full author PDF](https://liugroup.ucsd.edu/wp-content/uploads/2020/02/Gonzalez_et_al-2020-Advanced_Materials.pdf), pp. 1–6.

**Disposition:** this is a consequential alternative intervention to investigate, with direct physical precedent and substantial prior art. No new combination, improved switching material, safe quarantine interval, superiority, or historical novelty was established. If existing Janus/iongate designs win under matched fault and energy budgets, they close the invention claim while remaining useful technology.

## 5. Independent countermodels for the earlier physical claims

### A finite hidden reservoir can mimic sustained energy production over a finite run

An initially charged capacitor with energy `E0=C V0^2/2` and regulated converter can deliver constant reported power `P` for any specified finite observation interval `T` if `E0>=PT/eta`. A chemical or elastic reservoir supplies the same construction. Consequently, finite positive bus output alone does not identify the energy source. The issue is source identifiability and resource depletion, not computational closure.

**Discriminator:** bound the full initial electrostatic, chemical, elastic and thermal inventory; measure every electrical/thermal/fluid port; perform source removal/reversal and loaded steady cycling. Show exported energy beyond the independently bounded initial inventory plus uncertainty, with reset/recharge costs included. If reservoir capacity is unbounded or unmeasured, longer operation is evidence of endurance, not a logical exclusion of a hidden reservoir. This is an explicit finite-run countermodel, not an allegation about any particular experiment.

### Joule heat and sensor nonlinearity can imitate a buried electrochemical gate

For pulse input `u(t)`, let `dot theta=-lambda theta+c u^2` and let magnetic readout state obey `dot m=-b m+(a+k theta)u`. The hidden variable is temperature, but the equations have the same even-in-current gate followed by odd readout structure as a proposed interfacial state. An amplitude/order statistic that rejects an affine response can retain this cubic response. Separately, a linear physical field `B=B0+kU` read by `f(B)=B+epsilon(B-B0)^3` gives an odd cubic contrast without nonlinear electrode physics. Changing pulse amplitude alone does not distinguish these models.

**Discriminator:** vary thermal conductance or impose a matched heater waveform while holding electrical pulse shape fixed; use independently calibrated coil-only field waveforms and full raw NV spectra; vary optical duty cycle at matched readout precision. Then require a registered local chemical outcome under a held-out waveform. A measured thermal control changes the model family; merely fitting a better cubic curve does not. The earlier packet's embedded-NV and nonlinear-response sources were inspected as prior campaign context; no new NV result is claimed here.

### Detector back-action can be the actual drive

An equilibrium specimen coupled to a biased detector need not remain equilibrium. The relevant countermodel has a detector excitation channel `k_det(V_det)` feeding specimen transitions while terminal specimen bias is zero. Observed transitions or inferred dissipation can then be real but paid by the detector. Primary experiments report phonon-mediated back-action from biased charge detectors. [Granger et al., Nature Physics 8 (2012)](https://doi.org/10.1038/nphys2326). Joint DQD/QPC theory explicitly accounts for both charge channels. [Golubev et al., Physical Review B 84, 075323 (2011)](https://doi.org/10.1103/PhysRevB.84.075323).

**Discriminator:** independently randomize detector bias/power and duty cycle, while matching achieved state-classification accuracy and bandwidth as closely as physically possible; add a second readout channel and detector-off evolution followed by readout. Record detector electrical power and specimen transition statistics. The extrapolation to zero detector disturbance needs a qualified model and uncertainty; an apparently insensitive range of detector settings alone is not proof of passivity.

## 6. A physically explicit equilibrium negative-snapshot model

This preserves an independent opening identified before the separator follow-up; it does not refute the prior all-even finite-CTMC theorem.

Take a harmonic oscillator `x=A cos theta`, `v=-A omega sin theta`, with uniform phase. Physical time reversal maps `(x,v)` to `(x,-v)`. At gap `Delta=2pi/(3omega)`, threshold `Y=1[x>-A/2]` produces the equally weighted words `011,110,101`, apart from zero-measure boundaries. Therefore

```
E[Y0(Y_- - r)(Y_+ - r)] = -(2/3)r(1-r) < 0.
```

There is no dissipative hidden cycle; mechanical momentum is a real odd coordinate. For a canonical oscillator with threshold `x>0`, the six possible sign words other than `000,111` have equal probability, giving

```
E[W] = r(3r-2)/6,
E[W] at r=1/3 = -1/18.
```

The alternative survives finite friction and a single equilibrium bath. In mass-normalized form,

```
dx = v dt,
dv = -omega0^2 x dt - gamma v dt + sqrt(2 gamma kBT/m) dB_t.
```

Its canonical stationary distribution and momentum reversal give zero stationary entropy production. Position is stationary Gaussian with normalized correlation

```
c(t)=exp(-gamma t/2)[cos(omega_d t)+gamma sin(omega_d t)/(2omega_d)],
omega_d=sqrt(omega0^2-gamma^2/4).
```

Let `c1=c(Delta)`, `c2=c(2Delta)`. Central symmetry and the two-variable Gaussian sign-angle identity give

```
P111 = 1/8 + [2 asin(c1)+asin(c2)]/(4pi),
P11  = 1/4 + asin(c1)/(2pi),
E[W] = P111 - 2r P11 + r^2/2.
```

At `omega0=1`, `gamma=0.1`, `r=1/3`, `Delta=2pi/(3omega_d)`, the saved analytic-formula calculation yields `E[W]=-0.0448978286`. Strict negativity near zero friction also follows by continuity, without relying on the floating-point number. The physical odd-coordinate distinction is established in stochastic thermodynamics; the oscillator witness above is direct analysis here. [Spinney and Ford, Physical Review E 86, 021127 (2012)](https://doi.org/10.1103/PhysRevE.86.021127), [inspected full text](https://arxiv.org/html/1204.4822v2).

**Discriminator:** resolve signed velocity and phase; fit the measured position correlation over multiple lags; apply a calibrated momentum-reversal impulse at fixed position with its work recorded. The equilibrium oscillator predicts reversal of subsequent phase motion. A dissipative all-even ring predicts its driven orientation unless the intervention also reverses its physical drive. A damped oscillator with finite measurement back-action is an experimental model to test, not a zero-energy hardware claim. A binary snapshot record cannot by itself establish which physical description applies.

## 7. Acquisition, comparators, and the precise continuation gate

The highest-value first experiment is the **electrically isolated, pressure-controlled metal-transfer test on the exact guard stack**, accompanied by the engineered-pore and SEI-contact challenges. It can decisively reject a charge-only inventory contract before a full high-energy prototype. If no transfer is detected, the result is a pressure/temperature/time/geometry-specific upper bound whose imaging and current resolution must be stated.

Every comparison must charge patterned-layer fabrication and yield, extra separator thickness and inactive mass, lead/feedthrough reliability, electrochemical window, ionic impedance, contact/background calibration, initial-metal inspection, pressure/load calibration, detector bandwidth, timing jitter, independently qualified reset, gate/guard power, thermal conditioning, failure trials, computation, and sample disposal. True reset of distal metal or SEI cannot be inferred from terminal voltage recovery. Token and inference energy telemetry are unavailable and remain **UNKNOWN**.

The strongest equally informed comparator receives every raw guard waveform, timing, pressure trace, image, chemical assay and energy record. It can implement the same alarm and inequality, or use a better model. The intended advantage must therefore be a physically demonstrated intervention or a better finite-cost decision, not an information advantage over an identical-data analysis. Hardware controls include the passive third-terminal detector, passive resistive Janus interception, iongate actuation, and an appropriate physically partitioned cell design at equal delivered energy and size.

The decisive unresolved obligation is to obtain **all three** of: (i) an admitted-path and contact specification that actually guarantees or quantifies detection, (ii) a useful bound on initial plus post-alarm conductive material from every electrical and mechanical source, and (iii) a calibrated link from that bound to a finite thermal/chemical hazard budget. None has been acquired for the proposed substrate. Until then, the result is a conditional electrical certificate and a falsification program.

## Source inspection and provenance

Downloaded primary PDFs, extracted text and selected rendered pages are in `sources/`; `DOWNLOAD_LOG.json` records downloads. Visual checks confirmed the lithium-resistivity table, pressure-zero-current distinction, and porous-copper construction. Some direct publisher web opens failed; author-hosted PDFs supplied the stated full-text evidence. The NRC download initially labeled as a creep paper is actually a 2020 conference abstract, not the 2021 journal full article; the log records this distinction.

- Wu 2014: full six-page PDF inspected, especially fabrication/contact discussion. No source data reanalysis.
- Doux 1910.02118: full preprint and supporting information acquired; pressure and pre-cycling shorting passages checked. No claim that its high-pressure result transfers quantitatively to a new guard.
- Han 2019: full author PDF acquired; internal-deposition, electronic-conduction and measurement-method passages inspected. No raw neutron data reanalysis.
- Chi 1979/NIST: recommended table and uncertainty/purity qualifications checked. Nominal scales, not a new material measurement.
- Ding et al., [Journal of Power Sources 488, 229404 (2021)](https://doi.org/10.1016/j.jpowsour.2020.229404): publisher abstract/introduction inspected; a separate NRC conference abstract was downloaded. The journal full methods were not acquired here. It supports measurable creep/extrusion as a concern, not an assigned guard's transfer rate.
- Gonzalez 2021: full author PDF acquired; resistance, pinhole tradeoff and switching discussion inspected. Gonzalez 2020: full author PDF read through primary web extraction, particularly architecture and abuse comparison. Neither experiment was independently replicated.
- Spinney/Ford: full HTML inspected for physical reversal/odd coordinates; oscillator derivation is original analysis. Granger: primary publisher abstract inspected; Golubev: primary abstract inspected. Those support back-action/channel accounting, not a detector-specific correction.

The prior operational report and the s09/l04/l03 dossiers were read as preserved campaign context. Memory supplied workflow/evidence-tier guidance only. No inherited claim was promoted to laboratory evidence. Novelty of the new analysis, external proof correctness, laboratory feasibility, scalable reliability, and practical superiority are **UNKNOWN**.
