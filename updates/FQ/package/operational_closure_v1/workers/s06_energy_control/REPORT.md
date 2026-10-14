# S06 — Energy/control operation under hidden pathways

15 October 2026, Australia/Brisbane. **Candidate status: unbuilt; full-system net output and advantage UNKNOWN.** The strongest operation I can specify is a **thermally self-clocked, two-bank pyroelectric heat engine**: a thermal relay alternates each bank's contact with a metered hot stream and cold sink, while an electrical recovery circuit runs the charge cycle and delivers DC to a storage bus. The relay is a physical temperature measurement and actuator paid by the same heat flow. It does not require microscopic knowledge of domain switching or heat pathways; it does require measured *terminal* polarization loops, thermal response, leakage, relay thresholds and the complete energy ledger. The existing literature already contains watt-scale actively cycled pyroelectric output and microwatt passive-contact cycling. Combining them has no demonstrated positive net power or novelty-cleared advantage.

## Service and physical assembly

The useful service is sustained **net DC electricity at a specified bus voltage**, supplied from a declared hot stream and cold sink. A fair demonstration would fix their inlet temperatures, flow/pressure budgets, contact footprint, mass, and lifetime, then meter hot and cold enthalpy flows and every electrical input/output. The target of 1 W-class net DC is a *design target*, motivated by an existing 1 W generator report, not a prediction for this assembly.

Two characterized ferroelectric multilayer-capacitor banks (A and B) operate in antiphase. A thermally attached bistable strip or bellows changes over two thermal contacts/valves when its local temperature crosses upper/lower thresholds. An electrical contact on the same relay can request the high/low field transitions, but phase lag and electrocaloric kicks must be measured. An inductor and switches transfer rather than dissipate most of the large field energy between the two banks. A rectifier/converter delivers the remaining net electrical energy to storage. A finite thermal regenerator between the banks can exchange some sensible heat before each contacts its reservoir. The relay and the charge-transfer circuit are not free: their motion, leakage, switching, startup charge, calibration and standby draw are in the system ledger.

This co-design is meant to reduce active sensing and timing dependence under drift. The bimetallic relay responds to an actual thermal state, while the electrical port supplies a direct measure of cycle work. It cannot infer unobserved heat leakage, pump power or fatigue. Its alleged advantage is therefore lower complete-system overhead or greater reliability than active control, **not** a new source of work. A precharged capacitor is startup inventory; sustained output must be shown after many cycles with its stored energy nondecreasing or explicitly deducted.

## Derived operating conditions (original calculation)

Let the bank plus attached relay have measured thermal capacitance (C), intended contact conductance (G), off-state parasitic conductance (G_\ell), hot/cold reservoirs (T_H>T_C), and relay thresholds (T_\downarrow<T_\uparrow). A first thermal-port model gives

\[
C\dot T=G(T_H-T)+G_\ell(T_C-T)\quad\hbox{on the hot contact},
\]
\[
C\dot T=G(T_C-T)+G_\ell(T_H-T)\quad\hbox{on the cold contact}.
\]

Writing (T_H^*=(GT_H+G_\ell T_C)/(G+G_\ell)) and (T_C^*=(GT_C+G_\ell T_H)/(G+G_\ell)), sustained switching is possible in this model **only if**

\[
T_C^*<T_\downarrow<T_\uparrow<T_H^*.
\tag{1}
\]

This is a genuine coexistence test: a material may have a large polarization change and a relay may switch on a benchtop, yet the installed off-state thermal leak can make the two terminal temperatures unreachable. If (1) holds and switching is fast, the hot and cold dwell times are

\[
t_H={C\over G+G_\ell}\log {T_H^*-T_\downarrow\over T_H^*-T_\uparrow},\qquad
t_C={C\over G+G_\ell}\log {T_\uparrow-T_C^*\over T_\downarrow-T_C^*}.
\tag{2}
\]

The actual period adds valve travel, thermal lag and any regeneration dwell. These equations follow by solving the linear heat-balance ODE; they are not a claim that real ferroelectric thermal response is single-exponential. They show why a relay that follows local temperature cannot promise 0.2 Hz without acquiring (C,G,G_\ell) and the contact delays. The explicitly hypothetical values in [calculation output](CALCULATIONS.json) give about 0.039 Hz despite 80 K reservoir span; they are a sensitivity example, not device data. Electrocaloric temperature jumps at field changes can also drive relay chatter unless the post-switch state remains inside the hysteresis band.

For a measured electric-displacement loop (D(E,T)), the *signed electrical work delivered by the bank* is the cycle integral (w_e=-\oint E\,dD) per active volume, with the sign fixed by measured terminal voltage/current. In a rectangular small-signal approximation with cold-to-hot polarization decrease (\Delta P>0), high/low fields (E_H>E_L), and active volume (V_a), the available work is approximately

\[
W_{\rm loop}\simeq V_a(E_H-E_L)\Delta P,
\tag{3}
\]

before leakage, hysteretic loss, switching, rectification and mechanical work. The exact signed loop, not an assumed favorable \(\Delta P\), must be acquired at operating frequency and temperature. Antiphase charge transfer reduces gross charging loss but does not change the cycle's heat-to-work exergy limit. For hot heat (Q_H>0), the net electrical work of a periodic device obeys (W_{\rm DC}\le Q_H(1-T_C/T_H)) for ideal fixed-temperature reservoirs; finite stream temperatures and other exergy inputs need a stream-exergy ledger. A more operational accounting is

\[
P_{\rm exported}=fW_{\rm bank,measured}-P_{\rm field\ electronics}
-P_{\rm pump}-P_{\rm relay/valves}-P_{\rm standby}-P_{\rm conditioning},
\tag{4}
\]

where the bank's measured signed work already includes field charge returned to storage; each term must be measured once, avoiding double counting. If the relay/valve is driven directly by thermal motion, its cost appears as reduced (Q_H)-to-electric conversion and heat rejection, not as a fictitious zero-work port.

For two equal lumped banks initially at (T_H,T_C), direct passive contact transfers at most (C(T_H-T_C)/2) from the hot bank to the cold bank before they meet at the mean temperature. Thus one lumped equalization can recover at most half of the sensible heat of a full temperature swing; finite-time transfer recovers less. A staged counterflow regenerator could do better, but adds contact area, heat capacity, pressure drop and cycle time. Regeneration changes hot heat demand, not the source of electrical work.

## Quantitative power coexistence screen

The 2026 *Joule* primary paper reports GEN3 at **1 W electrical output**, **0.2 Hz**, 255 PST multilayer capacitors and 4.3 cm³ active material; this is **5 J per cycle at the reported electric output port**. It uses a two-fluid-loop hot/cold switching system and high voltage (350 V at GEN3). Its separate Stirling-cycle demonstrator powers communication electronics, but its published 1 W headline is not evidence that *this passive relay assembly* delivers 1 W net after fluid handling and voltage conversion. The 2022 *Nature* paper reports 54 mW for a 57 s actively pumped/valved Olsen cycle and a best reported module heat-to-electric efficiency of 1.43% at its own operating point. The 2012 bimetal/pyroelectric primary paper reports 4.4 µW at 0.19 Hz across 96 K. These are **three different devices/conditions**; combining their best numbers is invalid as a performance estimate.

The potentially fatal complete-system term is fluid handling. If a water-like fluid carries hot heat (\dot Q_H=\rho c_p\dot V\Delta T_f) and a pump overcomes pressure drop (\Delta p) at efficiency (\eta_p), then

\[
{P_{\rm pump}\over\dot Q_H}={\Delta p\over \rho c_p\Delta T_f\eta_p}.
\tag{5}
\]

For an illustrative 1.43% conversion fraction (borrowed from the **different 2022 point**), \(\rho c_p=4.2\times10^6\) J m⁻³ K⁻¹, \(\Delta T_f=10\) K and \(\eta_p=0.30\), pumping alone consumes the entire gross output if \(\Delta p\ge180\) kPa. At 100 kPa, the hypothetical 1 W gross output would need about 70 W hot heat and 0.555 W pump input, leaving 0.445 W before all other costs. At 200 kPa with a 5 K fluid temperature change, pumping would consume 2.22 W. The arithmetic is in [calculations.py](calculations.py) and [CALCULATIONS.json](CALCULATIONS.json). None of those pressure drop, efficiency, flow or heat numbers was acquired for the 2026 generator; the screen says exactly what must be met, **not** that its full system fails.

One redesign is a gravity/thermosiphon loop plus a small thermally switched valve, avoiding powered pumping. It still requires two complete heat-exchanger loops, a finite buoyancy head, check-valve losses, and reliable alternation; a passive heat pipe's continuous hot-to-cold transport is not automatically alternating contact to the ferroelectric. The 2012 bimetal experiment proves only µW output from a directly moved small element. The 2026 thermomagnetic self-oscillator gives a useful independent warning: it reports 0.8 µW peak AC and 1.25 µW cm⁻² DC after rectification, with simulated heat intake 180–800 mW across its geometries and dominant mechanical/impact damping. Its self-tuning temperature window is real, yet sensorless oscillation alone did not create high conversion power. A heat-driven relay must therefore be measured with the high-throughput bank and fluid path; low-power self-oscillation and high-power loop output cannot be spliced into a successful device.

## Strongest equally informed competitors and substantive fallback

**Closest incumbent:** The active fluid-cycled PST Olsen generator of Song et al. (2026), with the *same* characterized capacitors, reservoirs, flow path, electrical recovery, and field limits. Give its controller access to the same local temperatures and terminal power. It can use thermocouples or terminal-based extremum seeking to adjust phase and field, including thermal drift. The proposed relay wins only if it exports more net DC, or the same service at lower total lifetime cost/failure rate, after its extra relay and losses are charged. Standard inductor charge transfer between antiphase ferroelectric capacitors was demonstrated in 2018; it is not an invention credit here. A same-footprint thermoelectric generator (TEG), with its own optimized heat exchangers and converter, is the alternative service competitor.

The failure mode prompted a substantive simpler fallback: **direct TEG with a fixed, uncertainty-robust electrical load**. If its acquired terminal characteristic over the *actual thermal boundary* is Thevenin (V=E-rI), (E>0), (r\in[r_-,r_+]), choose a passive load (R=\sqrt{r_-r_+}). Then (P=E^2R/(r+R)^2), while the instantaneous ideal matched power is (E^2/(4r)), so

\[
{P\over P_{\max}}={4rR\over(r+R)^2}
\ge {4\sqrt\kappa\over(1+\sqrt\kappa)^2},\qquad
\kappa=r_+/r_-.
\tag{6}
\]

For a fourfold acquired resistance range the guaranteed fraction is 8/9; for sixteenfold it is 0.64. This is a complete elementary circuit derivation under its stated port model, not a discovery or a guarantee that unknown thermal contacts leave a linear Thevenin source. It shows that hiding microscopic pathways need not prevent positive power if the *port response* is acquired. It also removes the relay, thermal cycling, high-voltage bias, and active timing. A 2015 primary TEG MPPT study already reports 1.87% average deviation from maximum-power output, so the fixed-load theorem gives no evident matched advantage. The TEG's low-grade efficiency and heat-exchanger burden must still be measured at the service terminals.

## Fatal experiment and acquisition ledger

Build the candidate and the active PST incumbent with identical banks, heat exchangers, inlet streams, coolant pressure budget, power electronics and storage. Randomize time blocks across control modes: (i) thermal relay, (ii) active controller with the **same** local temperature/terminal information, and (iii) a fixed schedule. Include a commercial/optimized TEG assembly at matched footprint, streams and sink as the service comparator. Meter simultaneous (Q_H,Q_C), bank (V,I), storage (V,I), pump/valve/controller power, pressure and flow, relay position/temperature, and failure/downtime. Run long enough to separate startup charge depletion and fatigue from sustained output. The decisive pass condition is positive storage-bus energy growth under load over many steady cycles, no external unmetered clock/field/pump supply, and a statistically resolved net/lifetime advantage at the same service. An equally informed active controller reaching the same or higher net output at comparable cost kills the claimed control advantage even if the passive cycle works. If (1) fails in operation, if the relay phase differs from the terminal optimum, or if (4) is nonpositive, the operation fails its own physical gate.

Acquisition and cost items that must remain explicit: ferroelectric batch yield and frequency-dependent full (D(E,T)) loops; latent/sensible heat and hysteresis; (C,G,G_\ell) including contacts and valves; local temperature relay lag and electrocaloric jumps; field supply and dielectric breakdown; electrical charge-transfer loss; hot/cold stream enthalpy and exergy; pump/thermosiphon hydraulic loss; cold-side heat rejection; insulation, leakage, pressure sealing and fouling; startup inventory; sensor/meter calibration used to *certify* output; footprint and active-material manufacture; and cyclic fatigue of both relay and capacitors. The controller may use fewer electronic sensors, but the bench must still instrument all energy ports to verify the claim.

## Claim/source ledger

| Claim | Status |
|---|---|
| Thermal relay oscillation iff thresholds lie between the two effective thermal equilibria, under the declared first-order port model | Original derivation, exact within model; physical parameters unacquired. |
| Equation (5) pump threshold and equation (6) robust fixed-load fraction | Original arithmetic/elementary circuit derivation; conditional, reproduced by local script. |
| 1 W at 0.2 Hz from a fluid-cycled PST generator | Source-reported measured **electric generator output**, not integrated candidate net DC. |
| Passive bimetal/pyroelectric output and thermomagnetic self-actuation | Published separate experiments at µW scale. |
| Two-bank thermally self-clocked regenerative device exports sustained net power and beats a matched active controller or TEG | **UNKNOWN; no integrated device or matched test.** |
| Originality of the combination or exceptional consequence | **UNKNOWN.** The components and proximate combinations have substantial prior art. |

Primary sources actually inspected: [Song et al., *Joule* 10, 102340 (2026)](https://doi.org/10.1016/j.joule.2026.102340), publisher search-indexed abstract, introduction, prototype description and reported GEN1–GEN3 points (direct publisher open was not available in this session; supplement and raw Zenodo data were not reanalyzed); [Lhéritier et al., *Nature* 609 (2022)](https://doi.org/10.1038/s41586-022-05069-2), accessible main text including pump/valve methods, 54 mW point, 1.43% best efficiency and autonomous two-MLC demonstration; [Ravindran, Kroener and Woias, *Procedia Engineering* 47 (2012)](https://doi.org/10.1016/j.proeng.2012.09.077), accessible primary full text and 4.4 µW bimetal result; [Torelló et al., *Nature Communications* 9 (2018)](https://doi.org/10.1038/s41467-018-04027-9), accessible circuit and charge-transfer results; [miniature PZT/Ni-Mn-Ga thermomagnetic generator, *Scientific Reports* (2026)](https://doi.org/10.1038/s41598-026-59705-2), accessible methods and measured AC/DC output; [TEG MPPT experimental study, *Energy Conversion and Management* (2015)](https://www.sciencedirect.com/science/article/pii/S019689041501047X), publisher search-indexed abstract reporting 1.87% average MPP deviation. The prior Astra heat audit and N720 resource dossier were read as scoped campaign context, not used as a proof premise or evidence for this candidate.
