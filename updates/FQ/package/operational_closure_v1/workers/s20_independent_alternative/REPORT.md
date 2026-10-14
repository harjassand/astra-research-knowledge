# Independent alternative: a persistent inductive reserve for a quenching magnet

15 October 2026, Australia/Brisbane. **Status: conditional circuit construction; no new operational capability established.** This is an intentionally non-information-first investigation. The magnetic field, coil geometry, current, and even the fault location may be supplied exactly. A superconducting magnet can still destroy its own winding after one section becomes resistive because hundreds of megajoules of stored magnetic energy must go somewhere before the local conductor overheats. The limiting quantities are inductive geometry, current margin, hot-spot enthalpy, induced voltage, AC loss, and mechanical stress. Better state inference alone cannot change those quantities.

The consequential task would be to survive one local winding quench *and keep the useful field operating* long enough for an orderly shutdown or recovery. The proposed operation is a geometrically interleaved, independently insulated superconducting reserve loop, left closed at zero transport current after startup. On a quench in the active winding, the rising resistance drives current out of it. Flux conservation in the cold reserve induces a current in the same field direction. The transfer uses the low-leakage differential electromagnetic mode, whereas dumping the useful field must change the high-inductance common mode. No controller needs to discover where the fault is before that initial transfer; diagnostics are still required to verify it and to trigger a safe fallback. This is a conditional design, not a demonstrated magnet.

## What was tried, and the redesign forced by prior art

The first idea was simply to add a tightly coupled secondary winding to absorb energy. That is established territory. The ESC authors explicitly derive a current-change gain proportional to `1/(1-k^2)` for coupled coils and simulate energy shifting into normal-conducting auxiliaries. Bifilar winding work uses a low-inductance differential mode to generate rapid current changes and reports a small REBCO experiment. Older passive secondary and quench-back work is also acknowledged in ESC. Thus magnetic coupling, energy transfer, and differential-mode speed cannot be claimed as new here. See the primary-source ledger below.

The substantive redesign is to make the secondary a **persistent superconducting reserve** with the separate objective of retaining the task field after the faulty loop goes to zero. This changes the end state: energy remains in a surviving winding instead of being promptly dumped or intentionally spread as heat. It also creates a new physical cost: the reserve needs nearly full post-fault current capacity and must survive the induced ramp. The literature on self-coupled protection of multiple HTS coils is especially close; I have not inspected its full paper, so priority for this narrower field-retention variant is **UNKNOWN and plausibly absent**. Its usefulness requires a matched physical test, not a lexical distinction.

## Exact ideal-circuit mechanism (my rederivation, not a novelty claim)

Take two separately closed loops with positive-definite inductance matrix

```
Lmat = [[L1, M], [M, L2]],  k = M/sqrt(L1 L2),  0 < k < 1.
```

The active loop starts at `i1(0)=I0`; the superconducting reserve starts at `i2(0)=0`. After a local quench, let the active-loop resistance be any nonnegative `R1(t)`. Grant a lossless, perfectly superconducting reserve (`R2=0`), linear time-independent inductances, closed loops, and no external power during transfer. Kirchhoff's equations are

```
L1 i1' + M i2' + R1(t) i1 = 0,
M i1' + L2 i2' = 0.
```

The second equation conserves reserve-linked flux: `M i1 + L2 i2 = M I0`. Hence

```
i2(t) = (M/L2) [I0 - i1(t)],
Leff i1' + R1(t) i1 = 0,
Leff = L1 - M^2/L2 = L1(1-k^2).
```

If the accumulated resistance integral diverges, the active current reaches zero. The heat produced *in the active resistive path* then obeys the exact ideal-model identity

```
Q1 = integral_0^infinity R1(t) i1(t)^2 dt
   = (1/2) L1(1-k^2) I0^2
   = (1-k^2) E0,
E0 = (1/2) L1 I0^2.
```

This is not a claim about maximum hot-spot temperature: the spatial distribution of `Q1`, transient heat transfer, and AC/eddy losses are absent. If `R1=R` is constant, `i1=I0 exp(-t/tau)` with `tau=L1(1-k^2)/R`; its initial hot-spot power remains `R I0^2`, and high coupling compresses this power into a shorter interval. Final reserve current is `(M/L2)I0`. For equal windings with identical field maps and `L1=L2=L`, this is `k I0`, so the ideal useful field finishes at `k` of its starting value. Energy conservation gives `E_final=k^2 E0`. The small residual field loss and small local Joule fraction come from the same geometry. A nonzero reserve resistance eventually dissipates the retained energy; a resistive auxiliary cannot supply long-lived field continuity.

The exact multiwinding version makes the design bottleneck transparent. Partition an inductance matrix around failed loop `j` into `Ljj`, coupling vector `m`, and the surviving-loop matrix `LSS`. Suppose the survivor loops are closed and lossless, and start at zero current. Their final currents are

```
iS(final) = LSS^{-1} m I0,
Qj = (1/2) I0^2 [Ljj - m^T LSS^{-1} m].
```

The bracket is the Schur complement of `LSS` and must be positive. In magnetic-field language, it is the energy in the failed loop's field component that the reserve windings cannot reproduce. A useful task field with linear map `Btask = bj ij + BS iS` survives only if `BS LSS^{-1}m` approximates `bj` in the *actual region and harmonics of interest*. If surviving windings start at nonzero currents `iS0`, the same ideal heat formula holds and their current **increment** is `LSS^{-1}m I0`; the task-field change is `(BS LSS^{-1}m-bj)I0`. This is the form needed for a multiwinding magnet already operating with several energized loops.

Here is an exact geometry counterexample to using coupling factor alone as the task-field certificate. Represent two normalized field profiles in an abstract two-mode magnetic-energy space by `f1=(1,e)` and `f2=(1,-e)`, with `0<e<1`. Then `L1=L2=1+e^2`, `M=1-e^2`, and `k=(1-e^2)/(1+e^2)` tends to one as `e` tends to zero. The second, weak harmonic initially equals `+e I0`, but after passive transfer it is `-k e I0`; its sign reverses despite arbitrarily good total-energy coupling. At `e=0.01`, `k≈0.99980002`, the ideal Joule fraction is only about `0.00039992`, and the weak harmonic is nearly the opposite of the target. This is a mathematical mode example, not a fabricated physical coil. It shows why small global magnetic-energy residual alone does not certify a clinically usable MRI field, accelerator optics, or fusion confinement field. The distinction between energy coupling and task-field geometry is the core design condition.

The first single-reserve architecture fails immediately as a general solution if its field shape differs from the failed winding, if `iS(final)` exceeds its critical-current margin, or if a common cryogenic/mechanical event quenches both. An overcomplete array of interleaved reserve loops is the redesign for a specified one-loop fault set: design `L`, `BS`, and current capacities so that the Schur complement, task-field error, and induced peak current are all bounded for **each** candidate failed loop. This is a concrete min-max coil-design problem, but no feasible high-field layout has been constructed here. It cannot be promoted by the algebra alone. The passive derivation directly fits persistent-mode magnets; series-powered magnets need an added isolation/crowbar operation whose delay and reliability must be charged.

## Scale check actually executed

`verify_transfer.py` computes the identities and checks finite-time energy conservation in dimensionless two-loop trajectories. At `k=0.97`, the ideal Joule fraction is `0.0591` and the field-retention fraction is `0.97`; at `k=0.999`, the fractions are `0.001999` and `0.999`. To force the ideal Joule fraction below `10^-6` would require `k >= 0.9999995`. These are calculations under the stated circuit assumptions. The bifilar primary paper reports `k=0.97` on a **small** co-wound REBCO test coil; it does not measure this proposed passive-reserve transient. Its conductor, dimensions, parasitics and operating regime cannot be transferred to a full-size magnet.

For a pure scale illustration, Ren and Gao describe a proposed superconducting test magnet with `436.6 MJ` stored energy. Applying the *hypothetical* two-loop fractions to that energy gives `25.803 MJ` local-path heat at `k=0.97`, `0.873 MJ` at `k=0.999`, and `873 J` even at `k=0.999999`. That magnet did not contain this reserve, and these numbers are **not predicted temperatures or experimental results**. They show why a coupling factor that looks very close to one can still be insufficient at large stored energy. A local enthalpy limit, resistance-growth profile, conductor geometry, and thermal model are needed before any safe threshold can be stated.

## Closest equally informed comparator and full cost

The strongest incumbent is an optimized protection architecture given the *same* coil geometry, conductor budget, coupling matrix, diagnostics, cryogenic capacity, and field tolerance. It can combine local bypass or no-insulation current sharing, heaters/CLIQ, an ESC or self-coupled secondary, sectionalized dumps, and a controlled shutdown. A design with two nearly identical superconducting windings and enough current margin could also make the same passive current transfer; that is not a separable advantage of the proposal. In the comparison, field continuity must be valued explicitly, and the incumbent may use redundant windings if those are in the resource budget.

| Resource or failure | Charge to the persistent-reserve operation |
|---|---|
| Acquisition | Pre-measured `L`, mutual coupling, field maps/harmonics, critical-current surfaces, thermal limits, joint resistance, fault-set distribution; quench/field sensors to verify transfer. The ideal equations grant all of these. |
| Preparation | Fabricate electrically separate interleaved windings, insulating joints and current paths; charge the primary while the reserve is open, then close a persistent switch at zero reserve current. Commission all fault configurations. |
| Conductor, volume, cooling | A reserve that ends near `I0` needs near-full current capacity and space, plus cryogenic supports and insulation. Two equal half-current windings would each need to tolerate nearly the full current after the other fails. |
| Energy and time | At least the leakage fraction is deposited in the faulty path in the ideal passive circuit. AC/interstrand/screening and structural eddy losses, switch/lead losses, cooldown energy and recharge are additional. A faster differential transfer creates larger `di/dt` and may quench the reserve. |
| Control and reliability | Monitor reserve current, temperature and field harmonics, and keep an independent dump fallback. Internal turn voltages, Lorentz-force redistribution, common-cause damage, and a second fault are not covered by the one-fault model. |
| Scaling | Magnetic energy scales with magnet size and field; a fixed `1-k^2` leaves growing absolute local energy. Achieving extreme coupling while preserving insulation, margin and structural separation is the central geometry question. |

The key tradeoff is not hidden information: even an oracle that announces the quench at `t=0` cannot make the Schur complement or the heat capacity vanish. The proposal would buy reduced local heat and field continuity by supplying a physically redundant current path. It has no established full-resource advantage over a well-designed, equally redundant incumbent.

## Decisive test and failure criterion

First, build a co-wound two-loop demonstrator with independent persistent loops and measured `L1,L2,M`, field maps, critical-current surfaces, and thermal budget. Precharge the active loop, close the unpowered reserve, and trigger blinded local faults at varied turns and operating currents. Measure both currents with enough bandwidth to test `i2(t)=(M/L2)[I0-i1(t)]`; measure the spatial hot-spot temperature, deposited energy, transient field/harmonics, induced turn and ground voltages, reserve AC losses, strain and any secondary quench. Repeat under a second-fault and common-cooling-fault condition. Compare against optimized no-insulation/current-sharing, ESC/CLIQ plus dump, and self-coupled protection using the same conductor mass, cryogenic capacity, usable field specification and fault distribution. No such experiment was done here.

The ideal mechanism is falsified as an operational protection route if the measured reserve cannot remain superconducting at the required transferred current/ramp, the task field leaves tolerance, or the measured peak hot-spot/voltage/stress exceeds safety limits even though the circuit's ideal integrated heat is small. The *advantage* claim fails if the same-resource incumbent has equal or better survival/field continuity after counting added conductor, preparation, cooldown and failures. Passing a small-coil circuit identity alone would leave full-size mechanical, thermal, cost, and novelty gates open.

## Primary sources and precise use

1. [Ravaioli, Verweij, Wozniak, *Energy Shift with Coupling* (2024), full arXiv HTML](https://arxiv.org/html/2409.05446v1). Inspected introduction and Sections 2/2.2: existing heaters, CLIQ, secondary circuits, ESC's resistive auxiliary, circuit equations and `1/(1-k^2)` gain; Section 2.2 also identifies transient losses and nonconstant inductance. This supports comparator and missing physics, not the proposed field-retaining reserve.
2. [Krave and Marinozzi, *Bi-Filar Coil Winding for Fast Quench Protection* (2024), full PDF](https://arxiv.org/pdf/2406.02467). Inspected pp. 1-5: co-wound differential mode; small REBCO coil measured `k=0.97`; the authors report rapid current injection, parasitic losses, lead heat and force concerns. Its objective is to induce a broad protective quench, not demonstrate field-preserving passive failover.
3. [Kim et al., *Self-Protection Characteristic Comparison Between No-Insulation, Metal-as-Insulation, and Surface-Shunted-Metal-as-Insulation REBCO Coils* (2023), MIT repository abstract](https://dspace.mit.edu/entities/publication/e05dd261-35a5-447b-bf24-06b914d57612). Inspected abstract only: turn-to-turn bypass and resistance/strength tradeoff are real physical comparators. No claim that its tests apply to this reserve architecture.
4. [Ren and Gao, *Electromagnetic, stress and thermal analysis of the Superconducting Magnet* (2015), arXiv abstract](https://arxiv.org/abs/1512.00845). Inspected abstract only for the proposed `436.6 MJ` system; used solely as a hypothetical energy-scale multiplier.
5. [Yang et al., *A Dynamic Self-Coupling Fast Discharge Method for High Temperature Superconducting Magnets* (2023), DOI](https://doi.org/10.1109/TASC.2023.3332406). The title and author abstract were located in search results, but the publisher full text was inaccessible in this run. The abstract describes transfer of energy from a quenched coil into nonquenched coils in a seven-coil design. This is a serious proximity flag, not a verified detailed comparison or novelty judgment.

The mathematical derivation, dimensionless calculation and design synthesis above are my work in this task. The circuit principle and differential-mode gain are already present in prior literature. Physical feasibility, measured advantage, full cost, and novelty remain **UNKNOWN**.
