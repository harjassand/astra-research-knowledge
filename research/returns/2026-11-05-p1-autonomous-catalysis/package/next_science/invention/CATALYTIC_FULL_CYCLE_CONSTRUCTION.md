# Autonomous catalytic energy recycling: full-cycle construction and challenge

**Status.** Complete conditional stochastic construction, exact alternative explanation, and finite executions. These do not identify the real catalyst's mechanism or establish a new foundational principle. Unidentified physical parameters are explicitly synthetic. The thermodynamic and kinetic operations used have substantial prior art.

## Evidence and scientific question

The system is Liang et al., *Dynamic Vibration-Coupled Energy Transfer for Boosting ORR Catalysts in Fuel Cells*, JACS148,5115–5124(2026), [DOI10.1021/jacs.5c15936](https://doi.org/10.1021/jacs.5c15936). The source attributes improved PtCo oxygen reduction to oxygen-adsorption energy captured in a calixarene modifier and transferred to adjacent hydroxyl conversion. Simulations report0.126eV vibrational energy and a0.375→0.183eV barrier change. The SI annotates41ns storage, shows roughly3.1–3.5-fold TOF improvement, and fits66.1→60.2mV/dec Tafel slopes.

The full question is whether chemically captured excitation increases **completed net ORR cycles** beyond the same modifier's ordinary thermal, structural and transport effects, with capture, reverse reactions, relaxation and chemical completion all included. Detecting energy transfer is distinct from establishing that it causes the current enhancement.

The publisher abstract and official SI were acquired. The main-text derivation of41ns and the potential/elementary-step assignment of the barriers were not acquired. The SI gives41ns as a FigureS3 annotation. Its energy-utilization numerator is a molecular single-point energy change, which is not a measured nonequilibrium free energy. Identifying0.126eV with a two-state free-energy gap is an additional assumption.

## 1. Static reversible cycle reproduces the headline kinetic combination

Let a two-stage reversible chemical cycle have forward rates a,b and reverse rates qa,qb on its two distinct channels. The exact stationary cycle current is

\[
J=(1-q)ab/(a+b).
\]

For ORR overpotential eta, q=exp[-2eta/(kBT)] gives total affinity4eta/(kBT), using eV and volts. All rates are positive. Scaling b and qb together by r lowers one transition barrier while preserving chemical affinity.

For x=(1/b)/(1/a+1/b), the initial changed-step waiting-time fraction,

\[
F=1/(1-x+x/r),\qquad x=(1-F^{-1})/(1-r^{-1}).
\]

At298K, r=exp[0.192/(kBT)]=1766.466509. Whole-cycle gain F=3.3 requires x=0.6973644763; afterward x'=Fx/r=0.00130277181. An enormous elementary acceleration gives a modest cycle gain because another step takes control.

The logarithmic voltage sensitivity is the waiting-time-weighted sum of elementary sensitivities, plus dlog(1-q)/deta. Solving for the two elementary slopes gives60.189944707 and69.041988545mV/dec at eta=.3V. They exactly reproduce66.1 and60.2mV/dec, including the finite reverse-rate correction q=7.12518e-11. The equivalent effective whole-cycle barrier reduction is only kBTlog3.3=.0306595eV.

This is an identifiability witness, not a fit to all chemistry. The gain/Tafel/barrier combination does not uniquely diagnose retained adsorption energy. The source's own governing comparator, Hansen, Viswanathan and Nørskov, [JPC C118,6706–6718(2014), DOI10.1021/jp4100608](https://doi.org/10.1021/jp4100608), already predicts59mV/dec in an OH-covered regime and uses rate control and adsorption-energy scaling, with an optimum about.1eV weaker OH binding than Pt(111). This does not prove that model describes the modified catalyst; it establishes a strong ordinary baseline.

## 2. Fully reversible72-state construction

Each of two sites has stages E,O2*,OOH*,O*,OH*,H2O*. The four middle transitions consume proton/electron pairs; the second releases one water and final desorption releases another. The complete cycle is O2+4H+ +4e−→2H2O. A shared binary mode g adds2 states, giving6×6×2=72.

For every channel x→y receiving reservoir work w, its reverse rate satisfies

\[
\log(k_{xy}/k_{yx})=\beta[w-(F_y-F_x)].
\]

The rule applies even when both chemical and mode states change. This is ordinary local detailed balance.

### Capture and reference

At a cold mode, adsorption is split into (E,0)↔(O2*,0) and (E,0)↔(O2*,1), with forward rates(1-p)kads and p kads. Their total forward rate is fixed. At g=1 adsorption leaves the mode charged. Thermodynamic reverse capture/desorption is included. Comparing p=0 and p=1 changes capture routing without granting a larger total forward attempt rate.

Thermal mode down/up rates are b=1/tau and a=b exp(-beta DeltaF). Two energy-use mechanisms are separately implemented:

- **Modulation:** the OH reaction is faster while g=1; it does not consume the mode. Both forward and reverse OH rates are multiplied. The mode eventually dissipates its stored energy to the bath.
- **Consumption:** an extra (OH*,1)↔(H2O*,0) channel consumes the mode on forward reaction and recreates it on reverse reaction. This pays actual energetic assistance.

The generator is solved at55 decimal digits. Independent checks enforce equal net current through all six stages, mode balance, local detailed balance, and

\[
\dot S_i/k_B=\sum_e(p_xk_{xy}-p_yk_{yx})\log[p_xk_{xy}/(p_yk_{yx})]
=\beta(4\eta)J_{total}\ge0.
\]

At eta=0 the stationary distribution agrees with Gibbs equilibrium and chemical currents vanish; the largest equilibrium stationarity error is below4e-52 in the model's numerical units. This is a finite numerical check, not experimental validation or proof-assistant verification.

### Explicit parameter cases

Conditional source inputs are T298K, DeltaF.126eV, tau41ns, cold OH rate2.3e9exp[-.375/(kBT)]=1046.4659/s, and hot rate2.3e9exp[-.183/(kBT)]=1.848547e6/s. Using the Eley–Rideal prefactor here is conditional on the unidentified barrier assignment.

Synthetic state free energies are[0,-.95,-.70,-.40,-.20,-.10]eV. All non-OH forward rates are either100/s or10^6/s. These are not measured catalyst parameters and were not fitted to its data.

| Mechanism | Other rates /s | p=0 cycles/site/s | p=1 cycles/site/s | Capture-caused gain |
|---|---:|---:|---:|---:|
| Modulation |100|1.80413635293|1.80413635521|1.00000000126|
| Consumption |100|1.80413635139|1.80413636019|1.00000000488|
| Modulation |10^6|7589.649414|7756.570097|1.02199320|
| Consumption |10^6|7436.245991|7612.070031|1.02364419|

The consuming100/s case is a complete counterexample to equating captured energy with current benefit. Without capture, thermal excitation supplies3.332059845 mode consumptions per pair per second. With capture, net chemical capture supplies3.581776383 excitations/pair/s, mode consumption is3.332069639/s, and.249706744/s returns to the bath. Chemical input nearly replaces thermal input; completed current barely changes. Energy transfer can be substantial while causally irrelevant to a claimed rate enhancement.

At10^6/s, other steps are fast enough for more OH rate control, and capture gains about2.4%. The resulting thousands of cycles/site/s are not the observed TOF regime. This is a counterexample/stress-test family, not a theorem excluding all microscopic alternatives.

An additional completed lifetime sweep, retaining the consuming model and every chemical parameter of the10^6/s case, is saved in `catalytic_lifetime_requirements.json`:

| Mode lifetime | Capture off cycles/site/s | Capture on cycles/site/s | Gain |
|---|---:|---:|---:|
|0.41 microseconds|4969.234184|6348.815445|1.27762452|
|4.1 microseconds|1729.263079|6102.245051|3.52881243|
|41 microseconds|1034.578712|9525.504404|9.20713359|

This locates an actual finite positive regime in the supplied model. Its threefold example requires a lifetime100 times the source annotation and thousands of cycles per site per second. The capture-off baseline also changes as bath excitation slows: a large relative improvement does not establish an absolute advantage over the faster thermal catalyst. No material attaining these parameters or complete physical actuator is acquired.

## 3. Exact mode bookkeeping

With stationary charged-mode probability P1, net capture Jcap and net consuming-channel current Juse,

\[
J_{cap}+a(1-P_1)-bP_1-J_{use}=0,
\qquad P_1=(a+J_{cap}-J_{use})/(a+b).
\]

Modulation has Juse=0. Consumption requires separating thermal supply from chemical supply. Gross excitation counts are not recovered chemical work, and gross adsorption is not completed turnover. Reversible adsorption can be much faster than net ORR. Both gross adsorption and net current are reported.

This identity is specific to a binary mode. A coherent or multimode alternative needs a larger state and independently specified equilibrium comparison. The energy/entropy/free-energy distinction remains necessary.

## 4. Preparation bound independent of a binary gate

Condition on post-adsorption chemical configuration z. Let pi_z be the conditional thermal distribution of mode coordinates, p_z the actual excited distribution, under the same conditional Hamiltonian. Use the same chemical-state weights mu_z. Then

\[
\mathcal F_{extra}=k_BT\sum_z\mu_zD(p_z\Vert\pi_z).
\]

If subsequent physical dynamics are identical, for any specified binary event E, including completion by a fixed horizon,

\[
\mathcal F_{extra}\ge k_BT\,d_{Bern}(P_p(E)\Vert P_\pi(E)).
\]

Proof: joint initial relative entropy equals the displayed conditional sum; the common stochastic trajectory kernel cannot increase it; mapping the trajectory to E cannot increase it. The final entropy is binary. This is standard relative-entropy contraction plus established nonequilibrium free energy, not a new foundational result.

It makes phase/coherence proposals pay preparation. If entropy is unchanged, free-energy excess equals added energy. Entropy reduction and correlations require their own accounting. A coherent displacement of a thermal harmonic mode preserves entropy; its free-energy excess equals added energy, without an additional free coherence resource.

Illustration: a ready-OH baseline k0=1046.4659/s gives q=1-exp(-k0×41ns)=4.29042e-5. If an independently justified one-trigger renewal model required p=1-1/3.3=.696970, the binary bound is.164240eV, larger than.126eV if that is the complete free-energy budget. The p condition is not universal. Nor may q be replaced by unconditional Jtau when adsorption conditioning selects different chemical states. This is a conditional requirement, not an empirical exclusion.

Kuznets-Speck and Limmer, [PNAS118 e2020863118(2021), DOI10.1073/pnas.2020863118](https://doi.org/10.1073/pnas.2020863118), supplies a prior transition-rate amplification theory. Its heat-only bound uses forcing/noise independent of system state, explicitly precluding feedback, and does not directly cover self-pumping boundary-driven chemical NESS. General path-action relations retain kinetic/activity and initial-ensemble qualifications. The heat-only formula is not transferred here without those conditions.

## 5. Empirical alternatives already in the source record

The SI's titrated oxygen capacities are.079 and.04175mmol/g, ratio.528481. Its TOF equation divides current by a titration-derived active-site count. A TOF ratio3.3 with these counts at the same mass boundary corresponds to a current ratio1.74399. This does not invalidate improvement; it prevents conflating per-site and equal-mass gains. The written description calls TOF electrons/site/s whereas the equation divides by electron number n; the cycle/electron convention must be fixed before deriving a pumping rate.

The SI also reports35% lower pressure-independent oxygen transport resistance. EXAFS Co-O coordination changes1.7→4.0 and Co-Co3.2→1.0, with other structural changes. These are concrete changes to sites and transport, not hypothetical confounders. Their separate causal contributions remain unidentified.

Primary comparators:

- Genorio et al., [Nature Materials9,998–1003(2010), DOI10.1038/nmat2883](https://doi.org/10.1038/nmat2883): calix[4]arene patterning changes Pt selectivity and H/OH coverages. It is a different interface and can inhibit ORR; attachment is not a mechanically isolated intervention.
- Wang et al., [Science Advances7,eabb1435(2021), DOI10.1126/sciadv.abb1435](https://doi.org/10.1126/sciadv.abb1435): explicit water-adlayer and oxygen-access calculations correlate with activity across Pt structures and electrolytes. This does not identify the new catalyst, but supplies a consequential ordinary interfacial alternative.

Pressure, isotope, temperature or rigidity changes are not automatically selective interventions on energy transfer: they also affect adsorption, proton transfer, sites and transport. A causal comparison needs matched measured conditions and completed products/current.

## 6. Governing machinery and exact source conditions

Rao and Esposito, [PRX6,041064(2016)](https://doi.org/10.1103/PhysRevX.6.041064), equations48–61 and74–77, supplies established local detailed balance, entropy/current and nonequilibrium free energy. Wachtel, Rao and Esposito, [NJP20,042002(2018)](https://arxiv.org/abs/1709.06045), constructs thermodynamically consistent catalytic coarse graining. Its single-emergent-cycle flux-force relation is not automatically valid for each apparent channel when multiple emergent cycles remain. Full primary PDFs/texts were read; hashes are in `primary/catalytic_thermodynamics_manifest.json`.

Astra was consulted after empirical anchoring and the independent model, at commit `d5ac5437c8f953fc515f931fbcb1ef80b4e96dd7`. Exact governing originals read and retained:

- `updates/FL/synthesis/activation_audit/proofs/activation_bound.md`, SHA256 `f3cc65aa6f90bed16b8d24ec2a4fa53fbc44561c132c7a2f2e3e66f4b7e2d674`. The work floor assumes terminal outcomes, full loss, no terminal-branch recovery, survivor unloading and fixed renewal states. Its general ledger is ordinary renewal accounting. Neither its restricted floor nor a pooled hazard ratio is silently imported into reversible shared-mode catalysis.
- `updates/GC-peak-stability-genesis-20261016/package/derived/workers/gc_catalysis_genesis/PROOFS.md`, SHA256 `080648041fc39e060d340001c16438f4095ff302d42296340e8cf1db1f116fc8`. Randomized omission requires common read conditions, bounded assigned cohorts and sequential randomization. A41ns molecular intervention is not acquired by that theorem. Its counterexamples prevent inferring isolated-pulse causal effects from steady/periodic contrasts.

The packets remain source-derived and externally unreviewed. They supply neither a physical actuator nor mode distributions, calibrated reverse rates or validation.

## 7. Earned endpoint and remaining operation

The earned operation calculates whether captured energy increases net product current, substitutes for thermal input, or moves a bottleneck, given a physical generator and preparations. Reverse edges and actual cycle counts are included. A static countermodel reproduces the headline kinetic combination, and a reversible example exhibits captured energy without meaningful current benefit.

The unacquired operation is a matched physical or validated atomistic intervention on excitation distribution/coupling, holding chemical-state, structure and transport comparisons fixed, with complete-cycle current and energy measured. The accessible record lacks mode free energy/entropy, adsorption-conditioned preparations, a validated operating-bias/solvation reaction generator, and a counterfactual that suppresses transfer while preserving the other effects. These cannot be inferred from a barrier and lifetime alone.

A universal physical capability or new mechanism is not established. The construction preserves the strongest complete conditional science without promoting gating, renewal accounting or stochastic thermodynamics as a foundational discovery.

## Reproducibility

`catalytic_cycle72.py` generates `catalytic_cycle72_results.json` using mpmath. `solve_case(...,internal=True)` returns Q, stationary pi, channel tuples, states and beta for independent current-response audit. `CAPACITY_GEOMETRY_COMPLETION.txt` and the exact rational capacity code/results preserve the earlier completed alternative. Both rejected invention routes retain timestamped pre-literature checkpoints and precise prior-art reports.
