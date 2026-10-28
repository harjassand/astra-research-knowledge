# A replenished liquid-metal anode for aluminum scrap: construction and failed gate

The proposed operation is a continuous Al-transfer anode. It would feed contaminated solid aluminum into a liquid Ga intermediary, expose that liquid to an electrorefining electrolyte, and collect Al on a separate cathode. The intended enabling consequence is continuous scrap upgrading without a passivating solid-scrap/electrolyte front or bulk remelting.

This is a new branch, distinct from the completed powder-polarizability work. No response/volume bound, Fourier receiver, or old quantum/thermal construction is used here.

The actual result is a mathematical transport construction and a failed qualification of the simple architecture. It is not a measured or acquired physical scrap-refining capability. The strongest ordinary alternative remains directly renewed solid-anode electrorefining. The numerical countermodel below disproves an onset-only purity argument, not every possible Al–Ga process.

## 1. Two genuinely competing operations

**Candidate A: a liquid-Ga supply layer.** A feed-contact region replenishes Al dissolved in a liquid-metal reservoir or supported layer. A distinct electrically controlled liquid/salt interface oxidizes Al into the electrolyte. Ga returns to the feed contact. Source residue and product harvesting are separate streams. Three claims would have to be paid: sustained dirty-scrap-to-liquid Al admission, sufficient selective anodic flux, and retained host/product purity through many inventory turnovers.

**Alternative B: directly renewed solid-Al electrorefining.** Ultrasound, stirring, or another qualified surface-renewal operation acts on the scrap anode in the refining electrolyte. It incurs no added Ga host. The comparison is not against unrefined scrap, dilution alone, or an artificially unagitated anode.

Primary results already make B a strong contender. The source screen found laboratory high-purity low-temperature Al electrorefining as early as 2003, a 2022 solid-state molten-salt scrap-upgrading process, and a 2026 pulsed-ultrasound process. Source observations and missing common-regime parameters are separately recorded in sources/PRIMARY_INPUTS.json. None is a full industrial or full-cycle validation.

Evidence discriminated against advancing A as a presently acquired operation: rapid metal-side transport does not supply the electrolyte-side transport, while the Ga intermediary adds a reducible contaminant pathway. The independent alternative was retained through the calculation.

## 2. Thermodynamic convention: dilute liquid is not an ideal-mixture penalty

If liquid Al–Ga is locally equilibrated with its actual Al-rich feed phase, the chemical potentials of Al in the two phases coincide. Its mole fraction can be small without the liquid's Al activity being equal to that mole fraction. Charging RT log(x_Al) relative to pure solid Al would therefore be unjustified without the actual phase/activity model.

Conversely, coexistence does not automatically make the activity relative to pure Al equal to one. Ga can enter the Al-rich solid. The correct reversible electrode potential is referenced to the chemical potential of the actual admitted source phase. That activity, its relation to concentration, and its changes as impurities accumulate have not been acquired.

Electrochemical removal at the downstream interface creates undersaturation and requires renewed feed admission. A finite initial dissolved-Al charge does not prove continuous operation. Gallium-induced grain-boundary penetration, nanoparticles in a Ga–Al composite, or an Al-water reaction do not by themselves measure a selective dirty-scrap-to-liquid Al flux in a dry refining electrolyte.

## 3. Why a visible Ga oxidation onset is not a purity guarantee

The relevant Ga dissolution can produce Ga(I), rather than a three-electron Ga(III) product. Primary work also electrodeposits Ga from chloroaluminate liquids. It is therefore incorrect to infer zero Ga contamination merely because the liquid-metal anode is below a visibly reported Ga dissolution onset.

In a supplied reversible Ga(I)/Ga model, let E_G be the formal potential in a declared concentration convention and E_a the anode potential in the same reference. With the Ga-metal activity absorbed into c_star,
\[
 c_{\rm eq}(E_a)=c_\star
       \exp\!\left[\frac{F(E_a-E_G)}{RT}\right].
 \tag{1}
\]
At every finite E_a this concentration is positive. A more cathodic Al collector can remove those ions and sustain a Ga countercurrent. A cyclic-voltammetry onset at finite current resolution is not a bound on that countercurrent at a declared product impurity level.

Equation(1) is not asserted as a validated law for the proposed liquid Al–Ga interface. Real Ga activity, its oxidation-state/complex speciation, equilibrium standard, kinetics, deposition nucleation, and bath composition must be acquired. Its use here constructs an admissible screening countermodel to the onset-only argument.

## 4. Exact trace-species transport with ordinary boundary controls

For a dilute Ga species in a fixed one-dimensional transport layer,
\[
 N=-D_G c'(x)+v c(x),\qquad 0<x<L,\quad N'=0.
 \tag{2}
\]
The effective drift v is a supplied parameter; charge/speciation and electrolyte electric-field effects are not silently set from oxidation state. Put Pe=vL/D_G. Exact integration gives
\[
 N=K_Ac(0)-K_Cc(L),\qquad
 K_A=\frac{D_G}{L}\frac{\mathrm{Pe}}{1-e^{-\mathrm{Pe}}},
 \quad K_C=K_Ae^{-\mathrm{Pe}}.
 \tag{3}
\]
At Pe=0, both coefficients are D_G/L.

Allow finite source and collector transfer rates,
\[
 N=k_a(c_{\rm eq}-c(0)),\qquad N=k_c c(L).
 \tag{4}
\]
Solving(3)–(4) yields
\[
 N=
 \frac{K_A c_{\rm eq}}
      {1+K_A/k_a+K_C/k_c}.
 \tag{5}
\]
The perfectly reversible source and absorbing collector are the limits k_a,k_c to infinity. Slow real Ga kinetics could reduce leakage; that possibility is retained, not excluded by the model.

The code independently solves the ordinary boundary-value problem(2),(4), using a generic numerical collocation solver rather than the closed expression(5). At Pe=-3,0,+3, nontrivial finite transfer coefficients and positive concentrations, flux relative errors are below5e-13. This verifies the implemented transport algebra, not a material law or a new general transport algorithm.

## 5. All electron and atom counts

Let j_Al be the current density used only for Al production, on the same geometric area as the Ga transport. Then
\[
 \dot n_{\rm Al}=\frac{j_{\rm Al}}{3F},\quad
 r=\frac{\dot m_{\rm Ga}}{\dot m_{\rm Al}}
   =\frac{3F M_{\rm Ga}N}{M_{\rm Al}j_{\rm Al}},\quad
 w_{\rm Ga}=\frac{r}{1+r}.
 \tag{6}
\]
The Ga(I) current is F N. Treating that leakage as a three-electron Ga(III) current would undercount Ga mass per charge.

For the simplified active-Al-complex transport comparison, the balanced reaction is
\[
 4\mathrm{Al_2Cl_7^-}+3e^-
       \longrightarrow \mathrm{Al}+7\mathrm{AlCl_4^-}.
 \tag{7}
\]
If that complex is supplied by a single-species stagnant film with concentration C_Al and diffusivity D_Al, its scenario current ceiling is
\[
 j_{\rm Al,max}=\frac{3F}{4}
                  \frac{D_{\rm Al}C_{\rm Al}}{\delta}.
 \tag{8}
\]
This is explicitly a simplified transport model. A real chloroaluminate bath has coupled speciation, migration, activity and electroneutrality; an apparent voltammetric diffusivity does not automatically validate(8). It is not a rigorous ceiling for the actual multicomponent electrolyte.

## 6. The executed countermodel

The following inputs intentionally combine source-inspired scales with explicit unacquired assumptions:

| Parameter | Countermodel value | Acquisition boundary |
|---|---:|---|
| T |303.15K |supplied |
| E_G |.437V |primary-reported formal value; full standard/reference/T convention not acquired |
| c_star |1000mol/m^3 |supplied activity-to-concentration convention |
| D_G |9.12e-11m^2/s |primary-reported Ga(I) value in60/40 AlCl3–EMIMCl |
| D_Al |3.25e-12m^2/s |reported in a different BMIM liquid at343K |
| C_Al |3000mol/m^3 |supplied |
| each boundary-layer thickness delta |10micrometres |supplied |
| effective Ga length L |2delta |two supplied film resistances |
| Ga source/collector kinetics |reversible/perfect sink |supplied |
| effective Ga drift Pe |0 |supplied |

The Ga and Al numbers are **not a measured common-regime dataset**. No transfer between EMIM and BMIM liquids or between temperatures is qualified. The purpose is to test a logical architecture claim under an explicit conventional model, not forecast a real Al–Ga cell.

Equations(5)–(8) give j_Al=70.5549A/m^2 and Al production0.0236763kg/m^2/h. The Ga results are:

| Model E_a relative to Al | Ga mass concentration in collected product |
|---:|---:|
|0V |2.626ppm |
|.05V |17.806ppm |
|.10V |120.713ppm |
|.15V |817.871ppm |
|.20V |5519.145ppm |
|.25V |36263.422ppm |

In particular .20V is below the separately reported visible Ga onset near.325V, yet the explicit countermodel exceeds the entire0.1% impurity budget of99.9% Al. This comparison does not assert that the two different source experiments share their potential/activity regime.

Solving for an admitted Ga mass-fraction gate w gives
\[
 E_a\le E_G+\frac{RT}{F}
  \log\!\left[
  \frac{w}{1-w}
  \frac{M_{\rm Al}j_{\rm Al}}
       {3F M_{\rm Ga}K_{\rm eff}c_\star}
  \right],
 \tag{9}
\]
where K_eff is(5)'s effective transfer coefficient.

The countermodel's gates are:

- 1ppm Ga: E_a<=-.025224V;
- 100ppm Ga: E_a<=.095082V;
- 1000ppm Ga: E_a<=.155257V.

These are declared design gates, not universal Al-alloy standards. The1ppm gate leaves no positive Al anode overpotential in this particular fast-Ga model. It does not prove that real Ga kinetics, surface activity, a selective barrier, or an added Ga collector cannot change the conclusion.

At E_a=.20V, meeting the three respective gates requires Ga transport/activity suppression by factors5549.77,55.49,5.54. With an absorbing collector and all suppression assigned to source kinetics, the maximum Robin k_a values are8.22e-10,8.37e-8,1.00e-6m/s. These are concrete measurement thresholds. The Ga(III)/Ga(I) kinetic constants reported on tungsten or glassy carbon cannot be substituted for the needed Ga(I)/Ga-metal rate at an Al–Ga surface.

## 7. Faster mixing does not fix composition in this model

For equal source/collector Ga layers and Pe=0, K_eff=D_G/(2delta) in the fast-interface limit. If Al reaches(8),
\[
 r=
 2\frac{M_{\rm Ga}}{M_{\rm Al}}
 \frac{D_G}{D_{\rm Al}}
 \frac{c_{\rm eq}}{C_{\rm Al}}.
 \tag{10}
\]
Delta cancels. Thinning both films raises both throughput and contaminant transport proportionally; it does not improve their ratio. The code verifies the same ratio over a100-fold range of common layer thickness.

This does not forbid a selective change in relative mass transfer, source activity or interfacial kinetics. Those would be different acquired operations. Merely granting the Ga architecture ordinary agitation for free does not supply such selectivity.

An equally informed ordinary hydrodynamic model must also be allowed unequal species film thickness. For standard rotating-disk mass transfer,
\[
 k(D)=.62D^{2/3}\nu^{-1/6}\omega^{1/2}.
 \tag{10a}
\]
This familiar law is used and experimentally checked, for example, in the primary study [Additively Manufactured Rotating Disk Electrodes and Experimental Setup](https://pubs.acs.org/doi/10.1021/acs.analchem.2c02884). Granting the same ideal law to both candidate and ordinary electrodes changes D_G/D_Al in(10) to (D_G/D_Al)^{2/3}. The common rotation-rate factor still cancels from composition.

With supplied nu=1e-5m^2/s and omega=100rad/s, the revised Al current is201.198A/m^2 and output.0675167kg/m^2/h. At the same model E_a=.20V, Ga is1822.968ppm, rather than5519ppm. Thus this stronger comparator materially improves the candidate's prediction but still misses the1000ppm gate.

Its1ppm gate is E_a<=+.003812V: a narrow positive window exists, unlike the equal-film model's negative threshold. The corresponding100 and1000ppm limits are.124117 and.184292V. This correction is retained explicitly; no global claim that a1ppm receiver is impossible follows. The code does not qualify a rotating liquid-Ga layer, its wetting/support, actual viscosity or a common-bath diffusivity.

## 8. Pulsing is not a free rescue under the supplied laws

Suppose the fixed bulk transport operator has reversible boundary concentration(1), an absorbing collector and a periodic settled state. Averaging its linear transport equation over one period makes the mean Ga flux K_eff times the mean boundary concentration. No quasistatic pulse-frequency limit is required under that fixed operator.

If the Al current additionally obeys a supplied positive-current Tafel law with slope B_Al volts per decade,
\[
 j_{\rm Al}=j_0\exp(\log(10)E_a/B_{\rm Al}),
 \quad \overline{N_G}=C\overline{j_{\rm Al}^{p}},\quad
 p=\frac{F B_{\rm Al}}{RT\log(10)}.
 \tag{11}
\]
For p>1, Jensen's inequality says constant potential/current minimizes mean Ga leakage at fixed mean Al throughput and elapsed time. A supplied B_Al=.09031V/dec at343K gives p=1.32695. A two-level current(.2,1.8) with equal duty has the same mean as constant one but14.98% greater normalized leakage. The instantaneous boundary concentration is a power of current; an instantaneous flux law is not assumed in a rapidly pulsed system.

This is a conditional control comparison. Actual Ga kinetics, a time-varying electrolyte drift, an Al mass-transfer plateau or a changing interface can violate the premises. The published ultrasound duty cycle is an acoustic operation, not the voltage pulse in(11); this result is not a criticism of that experiment.

## 9. Metal-side speed, finite host and full material balance

Grant the candidate favorable but unacquired liquid-metal values: density6000kg/m^3,1wt% dissolved Al, D_metal=1e-9m^2/s and thickness100micrometres. A simple diffusive supply ceiling is6436.76A/m^2,91.23 times the equal-film ionic current and31.99 times the stronger rotating-disk current. Thus fast Al transport inside Ga does not remove the modeled electrolyte bottleneck.

That layer contains.6kg host and.006kg dissolved Al per square metre. At the modeled output, one Al inventory turns over in912s. Demonstrating100 turnovers would require25.34h of genuinely replenished output, not consumption of a preloaded composite.

At an illustrative feed with90wt% Al, at least.111kg non-Al material must be accounted for per kg Al product before recovery losses. If all of it entered the host, a1wt% debris inventory relative to the Ga layer would be reached in2.28h. If it stays in a feed basket or is continuously filtered, those paths and their Al/Ga losses must be measured. The calculation does not assume all impurities actually enter Ga.

At the equal-film ionic throughput,1t/h would need42236m^2 of active area and25.34t of the assumed100micrometre host. The stronger rotating-disk scenario reduces this to about14811m^2 and8.89t. These are scenario extrapolations, not lower bounds on every design. A thinner stable host, stronger electrolyte transport or different geometry can change them, and each needs its own material/interface qualification.

## 10. The matched ordinary alternative and decision

Directly renewed solid-anode electrorefining gets the same electrolyte transport improvements and cathode optimization. It need not transport Al through a Ga host and introduces no additional Ga pathway. It still owes its own feed/preprocessing, anode residues, side reactions, cathode harvesting, heat, bath lifetime and full-cycle costs.

The2026 primary source reports a specific laboratory regime with99.90wt% Al,98.90% cathodic current efficiency,.65V and20% ultrasound duty at343K. The reported energy1.958kWh/kg is numerically consistent with the cell-charge expression
\[
 E_{\rm cell}=\frac{3FV_{\rm cell}}
        {M_{\rm Al}(3.6\cdot10^6)\eta_F}
        =1.95853\ {\rm kWh/kg}.
 \tag{12}
\]
That equality is not proof that the paper omitted all auxiliaries. Their full measured heat/ultrasound/handling ledger was not acquired. Neither route has an established full-cycle advantage here.

**Decision:** do not promote the liquid-Ga architecture as a feasible acquired scrap-upgrading operation or as a demonstrated improvement over the ordinary alternative. The simple fast-liquid/onset-only argument fails; explicit purity/flux gates and source-complete mass balance replace it. A real capability remains NOT_ACQUIRED. This is a bounded candidate failure and a concrete transport construction, not a universal impossibility theorem for liquid-metal electrorefining.
