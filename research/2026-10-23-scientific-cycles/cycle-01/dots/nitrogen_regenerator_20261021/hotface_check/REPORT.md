# Independent hot-face check: a valid restricted ceiling, not a universal regenerator closure

Date: 2026-10-21 UTC. Scope: sensible-heat transport and periodicity only. No reacting-flow calculation, material-property claim, hardware operation, purchase, or programme reopening was performed.

## Findings first

1. **The proposed 1900 K cold-outlet ceiling is correct under the stated local, equal-conductance, equal-duration assumptions.** The proof is a one-point periodic energy balance. It is independent of storage capacity and does not require a whole-bed numerical solution.
2. **It is not a universal ceiling for alternating ceramic beds.** Passive axial heat spreading invalidates the isolated-point balance. A closed-form, insulated-end continuum counterexample gives cold outlet **2304.209703 K**, effectiveness **0.715789180**, and maximum solid temperature **2436.844679 K**, with equal hot/cold flow, durations and convective conductance. The solid remains below 2500 K everywhere.
3. An independently solved boundary-value problem reproduces the analytic numbers; finite-volume spatial convergence and one finite-blow check support them. These are mathematical thermal-model receipts, not a validated nitrogen-fixation device.
4. Phase-dependent heat-transfer coefficients are a separate escape from the equal-h bound. Radiation can either add severe hot-face loading or provide axial redistribution; it must be resolved by mechanism. Exothermic surface recombination ordinarily adds heating and is not free useful recovery of preserved chemical product.

## 1. Exact local proof

Let x=0 be the fixed hot end: hot gas enters here at T_H=3100 K during the hot blow, and the cold stream exits here at T_o(t) during the reverse blow. The cold inlet at the opposite end is T_C=300 K. Let S(t) be the actual local material temperature at x=0, not the mean temperature of a finite first cell or a particle whose surface is hotter than its core.

Assumptions needed for this proof:

- The same material element returns to its complete initial energy state every cycle. A one-pass charge is not a periodic regenerator.
- It has no net heat exchange except the specified local gas-to-solid transfer: no axial or intraparticle conduction divergence, nonlocal radiation, external cooling/heating, or surface reaction source.
- The local heat-transfer law is q=h[T_g−S], with the same positive, constant h in both blows, and equal blow durations τ.
- Hot-side local gas is T_H; cold-side local gas equals the outlet temperature. Gas bypass or a downstream heater/mixing stage is not being included in T_o.
- S(t) ≤ M=2500 K at all times, including the true hottest surfaces.

The local solid equation can be written dU_s/dt = h[T_g−S]. Constant solid heat capacity is not needed for the integrated proof if the full energy state resets.

Integrate one cycle:

0 = hτ[T_H−⟨S⟩_h] + hτ[⟨T_o⟩_c−⟨S⟩_c].

Therefore

⟨T_o⟩_c = ⟨S⟩_h + ⟨S⟩_c − T_H ≤ 2M−T_H = 1900 K.

For constant gas heat capacity, equal constant mass flow and the stated inlet temperatures, the corresponding sensible effectiveness is

ε = [⟨T_o⟩−T_C]/[T_H−T_C] ≤ 1600/2800 = 4/7.

Equal mass flow and constant gas heat capacity enter this effectiveness interpretation, not the local temperature identity itself. Negligible gas inventory is part of the supplied whole-bed model; the local proof still works with gas inventory if the boundary gas temperatures and the local transfer law remain as stated. With strongly temperature/composition-dependent gas enthalpy, temperature effectiveness is not enthalpy recovery and a new enthalpy accounting is necessary.

### Finite storage and finite blow

The global peak is at least (T_H+⟨T_o⟩)/2, strictly greater if the material temperature varies for a nonzero duration. More storage can reduce cyclic swing, but cannot lower this floor.

For constant local heat capacity C_s and a=hτ/C_s>0, the exact hot-blow solution is S(t)=T_H−(T_H−S_0)e^(−ht/C_s). If its end temperature is at most M, the hot-blow average obeys

⟨S⟩_h ≤ T_H−(T_H−M)(e^a−1)/a.

Using only ⟨S⟩_c ≤ M gives the stronger necessary condition

⟨T_o⟩ ≤ M−(T_H−M)(e^a−1)/a < 2M−T_H.

This is a necessary bound, not a sufficient design criterion. It quantifies why finite blow cannot rescue the restricted model. Equal-direction storage changes or latent heat do not evade the integrated bound unless their complete internal state or another heat/mass flux changes the balance.

## 2. Why coarse isothermal cells can falsely look better

A finite first cell has nonzero axial extent and is assumed internally isothermal. For cell NTU δ, hot gas is cooled across that cell; it does not remain at T_H over the whole cell surface. With the cell temperature S and cold-stream temperature T_i immediately before entering that cell:

q_h = Ċ(1−e^(−δ))(T_H−S),

T_o = S+(T_i−S)e^(−δ),

q_c = Ċ(1−e^(−δ))(T_i−S) = Ċ(e^δ−1)(T_o−S).

Thus, when expressed in terms of the external boundary gas temperatures, the cell has an apparent cold-to-hot conductance ratio e^δ. Its necessary bound is only

⟨T_o⟩ ≤ M−e^(−δ)(T_H−M),

which is weaker than 1900 K for any finite δ. This is not a counterexample to the continuum isolated-element result. It is the built-in internal heat redistribution of an isothermal lump. It disappears as δ→0. A real finite particle may also conduct heat internally, but then that physical transport and the hottest surface must be resolved rather than declaring its mean temperature the surface limit.

## 3. Variable conductance and unequal blow times

For constant phase coefficients h_h,h_c and durations τ_h,τ_c, set R_h=h_hτ_h/(h_cτ_c). The same balance yields

⟨T_o⟩_c = ⟨S⟩_c − R_h[T_H−⟨S⟩_h]

and therefore

⟨T_o⟩_c ≤ M−R_h(T_H−M).

So equal flow and duration do not by themselves imply the 1900 K ceiling if the heat-transfer coefficients differ. To admit a specified outlet T_*<M by this necessary condition, h_cτ_c/(h_hτ_h) must be at least (T_H−M)/(M−T_*).

If h varies within a blow, the exact statement uses h-weighted averages. Let A_h=∫_h h dt and A_c=∫_c h dt. Then

⟨T_o⟩_(h,c) ≤ M−(A_h/A_c)(T_H−M).

This is not automatically an unweighted time/enthalpy-average outlet bound. If the cold outlet is at most M and h_c(t)≤h_c,max, a conservative unweighted bound is

⟨T_o⟩_c ≤ M−[A_h/(h_c,max τ_c)](T_H−M).

A constructive rapid-cycle continuum example with no axial conduction, equal flows/durations and constant phase NTUs n_h=3,n_c=12 has combined conductance N=n_hn_c/(n_h+n_c)=2.4. Its effectiveness is N/(1+N)=0.705882353, cold outlet 2276.470588 K, and hottest solid 2441.176471 K. This proves that the equal-h assumption is substantive. It does not prove an actual bed can obtain the required fourfold conductance asymmetry at these temperatures and flow conditions.

## 4. Exact axial-conduction counterexample

Use x∈[0,1] from hot end to cold end and θ=(T−T_C)/(T_H−T_C). Let H(x) and C(x) be hot- and cold-blow gas temperatures in the rapid-cycle limit, and S(x) the cycle-independent leading-order solid temperature. Let n be each blow's total gas-solid NTU and

D = k_eff A/(Ċ L) = k_eff/(G c_p L).

Here k_eff is the axial effective solid-network conductivity under the chosen continuum model, G is mass flux and Ċ=ṁc_p. The averaged solid equation includes conduction throughout both blows, whereas each gas acts for half the cycle:

H′ = −n(H−S),

C′ = n(C−S),

D S″ + (n/2)(H+C−2S) = 0.

Boundary conditions are H(0)=1, C(1)=0, S′(0)=S′(1)=0. The solid ends are insulated: there is no external heat sink or external energy supply hidden in these boundary conditions.

Define

λ = sqrt[n(1+nD)/D],

R = n/[2(1+nD)] · [1+(2nD/λ)tanh(λ/2)],

ε = R/(1+R),

a = n(1−ε)/[2(1+nD)].

Then the exact solid solution is

S(x) = 1/2 + a(1/2−x) − [a/(λ cosh(λ/2))]sinh[λ(1/2−x)].

Its derivative is

S′(x) = −a + a cosh[λ(1/2−x)]/cosh(λ/2) ≤ 0.

Hence its hottest point is exactly x=0, not an unexamined interior or undersampled maximum:

S_max = 1/2+a[1/2−tanh(λ/2)/λ].

For completeness, the gas difference obeys H−C = (1−ε)+2D S′, which is not spatially constant when conduction is present. The gas sum follows H+C = 1+nD+n(1−ε)/2 −n(1−ε)x−2nD S. These expressions verify the gas boundary conditions and provide the full field.

At n=8,D=0.1:

- λ=12.
- ε=0.7157891795804793.
- T_c,out=2304.209702825342 K.
- T_s,max=2436.844678670807 K.
- Cold outlet exceeds the no-axial ceiling by 404.209703 K while every solid point remains below 2500 K.

The hot-end average convective input is n[1+ε−2S(0)]/2=0.7578862078 in the nondimensional local source normalization. It is balanced by negative D S″, meaning heat export to other axial locations. Insulated ends do not force S″(0)=0; they force S′(0)=0. Conflating these conditions would incorrectly retain the isolated-point proof.

The D→0 limit recovers ε=n/(n+2) and S_max=(1+ε)/2. The D→∞ limit becomes an almost isothermal bed: S→1/2 and ε→(1−e^(−n))/2. Consequently conduction can reduce effectiveness at fixed NTU while improving the maximum achievable recovery under an imposed material-temperature ceiling. There is no contradiction with the familiar statement that axial conduction is generally an effectiveness penalty when maximum solid temperature is not the binding design constraint.

Physical translation: D=0.1 would require k_eff=12 W m^−1 K^−1 for G=1 kg m^−2 s^−1, c_p=1200 J kg^−1 K^−1, L=0.1 m. This is only dimensional translation. No measured zirconia conductivity, radiative transport coefficient, packed-bed geometry, pressure drop, or survivability has been established by this calculation.

### Independent numerical receipts

The attached script uses three independent checks of the analytic case, not a design-parameter grid:

- scipy.solve_bvp applied directly to the four first-order continuum equations converges at tolerance 10^−9 with 1989 nodes and reproduces ε and S_max to printed precision.
- Conservative finite-volume rapid-cycle solves at N=100,200,400 give ε=0.7157492751,0.7157792062,0.7157866864 and Tmax=2436.525882,2436.764935,2436.824740 K, converging to the analytic result.
- One exact matrix-exponential periodic finite-blow solve at N=160,n=8,D=0.1,b=Ċτ/C_s,total=0.001 gives ε=0.7157734237402, cold outlet 2304.165586 K and sampled peak 2438.274885 K. Periodic reset residual is 4.44×10^−16 and whole-cycle energy residual is −6.73×10^−13.

For the latter finite-volume system, the unsampled peak is also safely bounded: at a spatial maximum the conduction term cannot heat that maximum, and dθ_max/dt≤n. With 100 intervals per blow, the peak is no larger than the sampled maximum plus n b/100, or **2438.498886 K**. This controls temporal sampling, not spatial discretization error. The analytic continuum result establishes the limiting counterexample; these finite-blow and mesh tests are supporting numerical evidence.

The rapid-cycle solution is a limit, not a claim of a literal zero-duration heat engine. A small but nonzero blow is possible in the model, and the checked finite-blow case has substantial margin. Valve operation, gas inventory, carryover, thermal stress, pressure drop and material response remain outside this receipt.

## 5. Radiation: distinguish loading from redistribution

For an illustrative local grey reservoir law q_r=κ(T_g^4−S^4), identical κ in both phases, equal durations and no other transport, periodicity gives

⟨T_o^4⟩_c = ⟨S^4⟩_h+⟨S^4⟩_c−T_H^4 ≤ 2M^4−T_H^4.

At T_H=3100 K,M=2500 K the right-hand side is negative: −1.42271×10^13 K^4. Thus no such purely radiative local periodic element can satisfy the cap even with a zero-temperature cold radiation reservoir. Its necessary peak floor is T_H/2^(1/4)=2606.778887 K. With an otherwise identical linear convection term, this symmetric local radiation adds a net positive heat load under the 2500 K cap and tightens, rather than relaxes, the linear bound.

This is a mechanism test, not a radiation model for nitrogen/oxygen/NO. Actual gas spectral participation, optical depth, view factors, reactor irradiation, surface emissivity and directional shielding must be specified. Equal symmetric grey coefficients must not be assumed merely because the same bed alternates direction.

Particle-to-particle or wall-mediated radiation can instead move heat axially. If represented by a defensible positive axial k_eff, it belongs to the redistribution mechanism in Section 4 and can relax the hottest-point constraint. If radiation escapes to ambient, it cools the bed but sacrifices recovery. If photons heat the cold gas through another route, that route must be included explicitly. No scalar statement that “radiation helps” or “radiation kills it” is warranted without separating these channels.

## 6. Chemical recombination and product preservation

Add q_add(t), positive into the hot-face solid, to the local no-axial equation. Then the equal-h identity becomes

⟨T_o⟩ = ⟨S⟩_h+⟨S⟩_c−T_H−[1/(hτ)]∫cycle q_add dt.

Net exothermic reaction heating of the solid therefore tightens the bound; net export or an endothermic sink relaxes it, but introduces a separate energy/material term. Surface atom recombination is experimentally known to contribute significant heat flux on ceramic thermal-protection materials, with sensitivity to surface composition, condition and temperature [2–4]. Those experiments establish the need for coupled surface chemistry, not the rate for this proposed packed bed.

In particular:

- Recombination of N or O atoms is not by itself proof of NO destruction. Heterogeneous NO decomposition and the homogeneous reverse nitrogen-oxidation network need their own kinetics and species balances.
- A thermal model without composition cannot establish whether the NO product survives the hot-bed residence time, wall area, temperature history, reversal carryover or downstream reheat.
- Heat recovered by destroying the desired chemical product cannot be credited as recovery while also retaining that product's full chemical-energy/yield credit.
- A genuine endothermic or reversible thermochemical storage route is a different coupled chemical cycle, not a storage-capacity escape from the local sensible-only proof.

No new chemical mechanism, rate integration or yield claim is made in this check.

## 7. How to use the result

Close only the **equal-conductance, equal-duration, no-axial-transport local sensible-bed branch** if its required cold-outlet temperature exceeds 1900 K under the 2500 K material limit. Do not close alternating-contact heat recovery as a class. An axial/radiative heat-spreading branch has a valid mathematical path above that bound, but requires measured or independently justified transport, actual peak-surface temperatures, gas/solid chemistry, pressure drop, flow switching and losses before it can be promoted into a device claim.

## Sources and provenance

The inequalities and closed-form counterexamples above are original derivations in this check, not claims attributed to the cited papers. Published sources support model provenance and the identified omitted mechanisms only.

1. T. E. W. Schumann, “Heat transfer: A liquid flowing through a porous prism,” Journal of the Franklin Institute 208(3), 405–416 (1929). DOI: https://doi.org/10.1016/S0016-0032(29)91186-8 . Publisher search result and abstract inspected. Classical porous-solid/fluid heat-transfer formulation; not a source for the new 1900 K ceiling or axial counterexample.
2. M. Balat-Pichelin, L. Bedra, O. Gerasimova and P. Boubert, “Recombination of atomic oxygen on α-Al2O3 at high temperature under air microwave-induced plasma,” Chemical Physics 340, 217–226 (2007). DOI: https://doi.org/10.1016/j.chemphys.2007.09.019 . Publisher search result includes the abstract and conclusion, reporting oxygen recombination and heat-flux measurements for alumina at 900–2400 K and 300 Pa. Direct subsequent full-page retrieval returned HTTP 403; full text was not inspected. These conditions must not be transplanted into the proposed reactor.
3. P. Kolodziej and D. A. Stewart, “Nitrogen recombination on high-temperature reusable surface insulation and the analysis of its effect on surface catalysis,” AIAA 87-1637 (1987). NASA record: https://ntrs.nasa.gov/citations/19870057566 . Search result contains the NASA abstract: nitrogen/oxygen energy-transfer catalytic coefficients on borosilicate glass and recombination diffusional heat flux. NASA's record has no downloadable paper; a later direct fetch returned 403. No quantitative coefficient from it was imported into this calculation.
4. “Thermal and chemical approaches for oxygen catalytic recombination evaluation on ceramic materials at high temperature,” Applied Surface Science (1997). DOI: https://doi.org/10.1016/S0169-4332(97)00238-9 . Publisher abstract inspected through search results. Its reported surface-dependent recombination heating illustrates why “ceramic” does not specify catalytic behaviour; no coefficient was adopted here.

Receipt files: verify.py (reproducible bounded calculation), results.json (machine-readable results and timing), run.stdout, run.stderr, source_receipts.json, and SHA256SUMS.txt. No parent file was overwritten.
