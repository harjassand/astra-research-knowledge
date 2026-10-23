# Minimal trapped-water / pressure-pulse and iron-shell mechanics

**Status:** bounded model, not a prediction for an acquired specimen. No geometry, high-temperature strength, permeability, gas diffusivity, water-generation rate, or creep parameter is supplied here. All numerical values below are explicitly normalized toy inputs. The parent is checking material geometry and strength.

## 1. Gas stoichiometry is the first gate

Use the local reduction step

\[
\mathrm{FeO(s)+H_2(g)\longrightarrow Fe(s)+H_2O(g)}.
\]

For reaction extent rate \(r\) (mol s\(^{-1}\)), fixed pore volume \(V_g\), and ideal gas at temperature \(T\), let \(p_w,p_h\) be internal water and hydrogen partial pressures. A minimal equal-permeance model is

\[
\dot n_w=r-L(p_w-y_wP_e),\qquad
\dot n_h=-r-L(p_h-y_hP_e),\qquad y_w+y_h=1,
\]

where \(P_e\) is external total pressure and \(L\) is the species permeance (mol s\(^{-1}\) Pa\(^{-1}\)). Summing the balances cancels \(r\) exactly:

\[
\dot P_i=\frac{RT}{V_g}(\dot n_w+\dot n_h)
=\frac{1}{\tau_g}(P_e-P_i),\qquad
\tau_g=\frac{V_g}{RTL}.
\]

Thus the one-for-one conversion of H2 to H2O can change the internal composition without raising total pressure in a closed, fixed-volume pore. With equal permeance and steady reaction, \(p_w=y_wP_e+r/L\) and \(p_h=y_hP_e-r/L\), so the excess water partial pressure is offset by an H2 deficit and \(P_i=P_e\). A water partial pressure is not itself a pressure differential across the shell.

This is an intentionally minimal closure. Unequal H2/H2O permeances, solid-volume change, adsorption, condensation, another gas-producing reaction, or an independent net inflow can create a total-pressure source. Those must be measured or represented explicitly. In general,

\[
\dot P_i=\frac{RT}{V_g}(J_{\rm net}+\nu_g r)-\frac{P_i}{V_g}\dot V_g,
\]

where \(J_{\rm net}\) is non-reaction net molar inflow and \(\nu_g\) is net gas moles created per reaction event. Here \(\nu_g=0\). FeO reduction also contracts the solid phase; if that increases pore volume, the \(-P_i\dot V_g/V_g\) term lowers rather than raises gas pressure.

For a spherical pore of radius \(R_c\) venting through a porous shell of thickness \(h\), a simple diffusive estimate is \(L\simeq D_{\rm eff}A/(RT h)\), giving \(\tau_g\simeq R_ch/(3D_{\rm eff})\). This is only a scale model; tortuosity, Knudsen transport, cracks, and changing pore structure alter it.

### A downstep and return

Let external pressure step from \(P_0\) to \(P_0-\Delta P_{out}\) for duration \(t_p\), with \(y_w,y_h\) fixed, then return to \(P_0\). Start with \(P_i=P_0\). For the fixed-volume/no-extra-source model, \(\delta=P_i-P_e\) obeys \(\dot\delta=-\delta/\tau_g-\dot P_e\). Hence

\[
\delta(t)=\Delta P_{out}e^{-t/\tau_g}\quad(0<t<t_p),
\]

and immediately after return

\[
\delta(t_p^+)= -\Delta P_{out}(1-e^{-t_p/\tau_g}),
\]

after which it decays back to zero. The downstep creates at most the imposed \(\Delta P_{out}\) differential; it does not amplify it. For \(t_p\ll\tau_g\), the pore stays near its initial pressure throughout the low-pressure pulse and the return nearly cancels the differential. For \(t_p\gg\tau_g\), the pore equilibrates during the pulse; the return produces a transient external-over-internal differential of nearly \(\Delta P_{out}\). “Leaky” and “sealed” are therefore relative to \(t_p/\tau_g\), not absolute labels.

An upstep gives the opposite signs. The external total-pressure perturbation at fixed composition leaves the ideal-gas reaction quotient \(p_w/p_h\) unchanged at equilibrium, but scales both absolute partial pressures and therefore can change fluxes and dissolved-hydrogen concentration.

If water is liquid and fills a hydraulically confined pore, a different model applies. Let \(q=P_\ell-P_e\), \(C_V=dV_{\rm accommodated}/dq\) (m\(^3\) Pa\(^{-1}\)) be total fluid-plus-shell compliance, \(G_\ell\) hydraulic leak conductance (m\(^3\) s\(^{-1}\) Pa\(^{-1}\)), and \(Q_w=\bar V_w r\) the retained liquid-water generation rate after filling. Then

\[
C_V\dot q=Q_w-G_\ell q-C_V\dot P_e,\qquad \tau_\ell=C_V/G_\ell.
\]

Before pressure builds, generation must first fill available pore volume \(V_{free}\), taking at least \(t_{fill}=V_{free}/Q_w\) if none escapes. This branch requires a liquid-filled or capillary-locked connected phase; it does not follow from generating steam. Condensation state, pore saturation, and hydraulic leak rate are open inputs.

## 2. Pressure-to-fracture necessary condition

For a thin spherical shell (mean radius \(R\), thickness \(h\ll R\)) under a uniform internal-over-external differential \(\Delta P=P_i-P_e>0\), membrane force balance gives tensile hoop stress

\[
\sigma_\theta\simeq \frac{\Delta P R}{2h}.
\]

An ideal strength threshold is therefore

\[
\Delta P_{crit}\simeq \frac{2\sigma_{eff}h}{R}.
\]

Units: Pa on both sides; \(h/R\) is dimensionless. For the no-source pressure step above, a necessary idealized condition for pressure-driven tensile failure is \(\Delta P_{out}\ge 2\sigma_{eff}h/R\). This is not sufficient: flaw geometry, porosity, stress concentration, loading time, and fracture toughness matter. If \(h/R\) is not small, use thick-shell mechanics. For high-temperature iron/oxide, \(\sigma_{eff}\) must reflect temperature, strain rate, creep/yield, and shell microstructure; no such number is assumed here.

Use the measured differential across the shell, not absolute \(p_{H_2O}\), in this criterion. Using the parent-supplied PRL2023 scale comparison (about 0.5 MPa water pressure versus about 1 GPa transformation stress) only as context, those quantities are not like-for-like: 0.5 MPa would be the mechanical load only if it were actually an internal-minus-external total-pressure differential. The quoted water pressure does not establish that such a differential exists. I did not independently retrieve that paper in this bounded derivation.

## 3. Transformation eigenstrain can load iron even without trapped pressure

For an isotropic spherical layer with displacement \(u=Ar+B/r^2\), uniform eigenstrain \(e^*\), and bulk/shear moduli \(K,G\), tension-positive stresses are

\[
\sigma_r=3K(A-e^*)-4GB/r^3,\qquad
\sigma_\theta=3K(A-e^*)+2GB/r^3.
\]

Impose displacement and radial-traction continuity at bonded interfaces and zero radial traction at the outside surface. The next formulae assume equal \(K,G\) in Fe and FeO to isolate signs; they do not represent acquired material constants. Let Fe→FeO stress-free volume expansion be \(\beta>1\), and for a small-strain toy set \(e^*=\beta^{1/3}-1\). Actual transformation strain may require finite-strain/multiphase mechanics.

### Two layers: dense Fe core plus outside-only oxidized skin

Let Fe occupy \(0<r<a\), and FeO occupy \(a<r<R\), with oxide eigenstrain \(e>0\), Fe eigenstrain zero, equal moduli, perfect bonding, and a traction-free outer surface. The exact solution gives

\[
\sigma_{core}=\frac{12KG}{4G+3K}e\left(1-(a/R)^3\right)>0,
\]

uniform hydrostatic tension in the Fe core. In the oxide skin,

\[
\sigma_{\theta,skin}(r)=
-\frac{6KG a^3e(R^3+2r^3)}{R^3r^3(4G+3K)}<0.
\]

So outside-only oxidation can mechanically load an unreacted dense Fe region even when reaction-water pressure is absent: the Fe core is pulled hydrostatically while the oxide skin is hoop-compressed in this ideal bonded model. Hydrostatic tension is not limited by a von-Mises shear-yield criterion; void formation, debonding, diffusion, or high-temperature relaxation would need their own models. This sign result does not infer cracking from a Pilling–Bedworth ratio alone.

For an *incremental* outside-skin oxidation step on a pre-existing oxide-core/Fe-shell particle, set the already-existing core's eigenstrain to zero in the incremental reference state. With the equal-modulus assumption, the region inside the new skin is then mechanically one substrate: replace \(a\) by the Fe-shell outer radius \(b\) in the two-layer formula. The newly added skin increment gives the Fe shell a uniform hydrostatic tensile increment \(12KG e(1-(b/R)^3)/(4G+3K)\). The three-layer formula below instead describes the total constrained state when both core oxide and outer skin carry eigenstrain relative to the same Fe reference; it can therefore have a deviatoric Fe-shell field.

### Three layers: oxide core / Fe shell / oxidized outer skin

Let FeO core be \(0<r<a\), an unreacted Fe shell be \(a<r<b\), and an FeO outer skin be \(b<r<R\). Give both oxide regions eigenstrain \(e>0\), the Fe shell zero eigenstrain, equal \(K,G\), and assume perfect bonding and elastic equilibrium. The exact Fe-shell stresses are

\[
\sigma_{r,Fe}(r)=\frac{12KG e}{R^3(4G+3K)}
\left(R^3+a^3-b^3-\frac{R^3a^3}{r^3}\right),
\]

\[
\sigma_{\theta,Fe}(r)=\frac{6KG e}{R^3(4G+3K)}
\left(2(R^3+a^3-b^3)+\frac{R^3a^3}{r^3}\right).
\]

The Fe-shell hoop stress is tensile throughout this toy; radial stress is compressive at \(r=a\) and tensile at \(r=b\). The oxide core is hydrostatically compressed, while the outer oxide skin is hoop-compressed. Thus an outer oxidized skin can load a dense intermediate Fe shell, and it produces a deviatoric shell stress field, but actual stress magnitude and crack outcome depend on moduli, radii, plasticity/creep, pores, and interface conditions. The formula is a bonded-layer upper-constraint idealization, not a fracture prediction.

The executable exact fixture uses normalized \(K=G=1\), \(e=0.01\), \(R=1\), \(a=0.5\), \(b=0.9\) for the three-layer case. It returns positive Fe-shell hoop stresses with exact rational values at sampled radii, but those values are in normalized stress units. A separate two-layer toy uses \(a/R=0.9\), also with normalized moduli/eigenstrain. Neither fixture uses measured PBR, dimensions, or strength.

## 4. Non-identification and falsifier

A rate change during the total-pressure pulse does not identify fracture. At fixed H2O/H2 ratio, changing \(P_e\) scales absolute \(p_{H_2}\). A simple transport rival is

\[
J_{H_2}=k_g(p_{H_2,e}-p_{H_2,i})+\text{solid uptake},\qquad
C_H=S_H\sqrt{p_{H_2}}
\]

for gas-film plus pressure-dependent dissolved-H storage (the latter is a candidate model, not a measured law for this sample). Both can change reduction rate while reaction affinity based on \(p_{H_2O}/p_{H_2}\) is unchanged. The same pulse may also alter gas diffusivity/viscosity, boundary-layer transport, pore pressure, and conversion front location. Rate-only observations are non-identifying.

A useful falsifier must record: (i) particle/shell radii and thickness distribution \((R,h,a,b)\), pore/free volume and connectivity; (ii) external and, if feasible, internal total pressure versus time; (iii) H2/H2O fractions, conversion and integrated water formed/escaped; (iv) temperature and pulse duration; and (v) pre/post-return crack/porosity imaging and baseline gas permeability after a standardized equilibration. The pressure-fracture explanation fails for a fixture if the measured peak \(P_i-P_e\) is below the geometry/strength threshold by a clear margin, or if a claimed durable permeability benefit appears without any persistent post-return structural/permeability change. A rate gain that occurs without stress-threshold crossing and tracks absolute H2 pressure/uptake is consistent with transport or hydrogen-storage effects instead.

The tight future discriminator is a matched pulse comparison with measured internal pressure and post-return structure, alongside a nonreacting/pre-reduced Fe-shell control under the same external total-pressure and H2/H2O history. That control can reveal pressure-dependent H uptake/transport without reaction-water generation. It is a proposed falsification protocol only; no experiment or hardware operation was performed.
