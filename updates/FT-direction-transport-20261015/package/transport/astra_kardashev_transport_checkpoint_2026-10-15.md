# ASTRA Kardashev Genesis: boundary-controlled transport without host damage

**Research checkpoint — 15 October 2026, Australia/Brisbane**

**Status:** An internally derived, numerically checked conditional mechanism and its transport/resource obstructions. No new physical operation has been experimentally established. No named material has been shown to satisfy the coupled requirements. Historical novelty of the narrow mechanism is unresolved; its generic ingredients are already established prior art. This checkpoint is not a device performance prediction, externally reviewed theorem, or claim of civilisation-scale capability.

## 1. Selected task and scope

The selected target is control of useful ionic transport without simultaneously activating destructive host rearrangement, under one material, temperature, composition, loading, boundary condition, and accounting boundary. Fast ionic conduction itself is not a missing invention. The sought advance would be a new, independently usable control over the transport–damage trade-off where existing materials and controls cannot provide it.

The requested output is net useful transfer or accepted device output, not a local hop, a transient current, a small-signal impedance change, or an optical signature. Net transport requires a paid chemical-potential/electrical bias and charge-balanced reservoirs. A material-processing claim would additionally require the corresponding accepted, retained structural endpoint.

Independent opportunity screening preceded consultation of Astra. Capacitive ion ratchets, targeted phonon excitation, low-temperature electrochemical reduction, cold sintering, and local beam-driven atom manipulation were considered. This checkpoint records the transport branch in detail; it is not an exhaustive survey of those fields. Capacitive ratcheting and generic vibrational/mechanical gating were rejected as invention claims because of existing operation-level prior art.

## 2. Prior art and observations that must not be combined incorrectly

Kautz et al. report a nanoporous capacitive electrochemical ratchet for continuous ion separations in Nature Materials (2026). Capacitive ratchet pumping is not a new operation here [S1].

Minami et al. report single-cycle-THz-driven macroscopic ionic flow in sodium beta-alumina (2020). A proposal merely to use THz fields to move ions is therefore not new [S2]. Pham et al. combine experiment and calculation on phonon–ion coupling in LLTO. The reported factor of ten concerns differential impedance relative to other excitation conditions, not a demonstrated tenfold absolute device conductivity increase [S3].

Poletayev et al. study memory in ionic hopping, including back-hopping, using nonlinear optical probes. A launched hop is not equivalent to committed long-range transfer [S4]. McClellan et al. measure correlations between lattice responses to repeated UV excitation. Their approximately 1,500-shot correlation length is not a measured lifetime of enhanced dark DC conductivity. The UV lattice experiment cannot supply the missing dark-state lifetime for a separate THz conduction experiment [S5].

Mechanical control of ion binding and permeation is established prior art. Fang et al. study strain-sensitive crown-ether pores, and Sahu et al. study optimal electromechanically tuned transport in the same broad class [S6,S7]. Noh and Aluru study membrane fluctuations, vibrational coupling, and transport [S8,S9]. Thus, neither “stretch the pore,” “change flexibility,” nor “couple a vibration to an ion” is a new physical operation.

A 2026 preprint by Yang and Xie explicitly relates ionic free-energy landscapes to host-lattice response. Eliminating a harmonic host is already scientific machinery, not an invented primitive [S10].

**Search limitation:** These sources establish strong overlaps and disqualify broad novelty claims. The search does not establish priority or the absence of earlier work on the narrower stiffness-controlled, dual-pathway hypothesis below. Some publisher/PDF access failed. The checkpoint does not depend on unresolved THz power units or any inferred industrial efficiency for a published experiment.

## 3. Narrow hypothesis retained for testing

Add a passive mechanical constraint that suppresses a host displacement stabilising an occupied ion trap more than the useful transition state, while suppressing a displacement stabilising a destructive transition state still more.

The proposed physical action is a change in accessible mechanical boundary stiffness. It is not arbitrary freezing of selected atoms in a simulation, and it is not an unspecified control law. A real support must supply the assumed extra elastic energy without unacceptable changes in chemistry, aperture, contact resistance, electrical leakage, fatigue, or active area.

This is a narrower candidate than generic strain gating. Even so, fixed macroscopic reference geometry does not imply unchanged microscopic geometry: the operation intentionally changes local relaxation. A different fixture is not sufficient to establish a fundamentally new operation. Novelty and technological significance remain separate unresolved obligations.

## 4. Exact common-host harmonic calculation

Let s label an occupied initial state A, a useful constrained transition state U, or a harmful constrained transition state H. The unstable reaction coordinate is excluded from the stable host coordinates u. In the restricted model,

\[
E_s(u;\kappa)=E_s^0+\frac12u^T K u-f_s^T u+\frac\kappa2(b^T u)^2,
\qquad K\succ0,\quad\kappa\ge0.
\]

The vector b specifies a **physically accessible** support displacement, expressed relative to a fixed support reference. It cannot be selected as an arbitrary ideal per-atom actuator. Common K, common masses, harmonic relaxation, well-defined constrained states, and an adequate separation of host equilibration from activated transport are assumptions, not material observations.

Set

\[
c=b^TK^{-1}b>0,\quad p_s=b^TK^{-1}f_s,\quad
R_s=\frac{p_s^2}{2c},\quad \chi=\frac{\kappa c}{1+\kappa c}.
\]

Classical integration over u gives

\[
F_s(\kappa)=E_s^0-\frac12f_s^T(K+\kappa bb^T)^{-1}f_s
+\frac{k_BT}{2}\log\det(K+\kappa bb^T)+C(T).
\]

The determinant term is common to the states in this model. Sherman–Morrison therefore yields

\[
F_s(\kappa)-F_s(0)=\chi R_s+\frac{k_BT}{2}\log(1+\kappa c),
\]

and, for the activation barrier B_s=F_s-F_A,

\[
\boxed{B_s(\kappa)-B_s(0)=\chi(R_s-R_A).}
\]

One shared control lowers the useful barrier and raises the harmful barrier if

\[
\boxed{R_U<R_A<R_H.}
\]

This ordering is a conditional coexistence requirement, not three independently adjustable performance assumptions. The proof does not demonstrate that any material realises it.

### Accessibility ceiling

Even an infinitely rigid implementation of this one boundary coordinate cannot lower the useful barrier by more than

\[
B_U(0)-B_U(\infty)=R_A-R_U.
\]

For a target local rate multiplier g, with unchanged kinetic prefactors, a necessary condition is

\[
\chi(R_A-R_U)\ge k_BT\log g.
\]

At 300 K a tenfold multiplier needs about 0.05953 eV of barrier lowering. A support with only 1 meV of useful differential relaxation cannot supply that result, regardless of control precision or external spring stiffness. The conclusion applies only to the stated model and accessible coordinate.

### Beyond the common-K approximation

For a fixed constrained ensemble and an actual added energy \(\kappa q^2/2\), differentiation of the partition function gives

\[
\frac{\partial B_s}{\partial\kappa}
=\frac12\left(\langle q^2\rangle_s-\langle q^2\rangle_A\right).
\]

This suggests what must be acquired in an anharmonic system: the response contrast between the occupied ensemble and relevant transition ensembles. A well-state phonon spectrum alone does not supply transition-state statistics. State-dependent force constants, changes in the dividing surface, reaction pathways, quantum vibrational free energies, friction, and recrossing must be treated rather than silently omitted. The common-K barrier formula survives only within its assumptions; the classical determinant expression is not a generic quantum free-energy model.

## 5. A faster escape rate is not sufficient for transport

A two-state single-occupancy pore gives an exact countercheck. Let a_L,a_R be entry rates from left and right reservoirs, and b_L,b_R be exit rates. Put A_r=a_L+a_R and B_r=b_L+b_R. The stationary occupied fraction is

\[
p_1=\frac{A_r}{A_r+B_r},
\]

and the net left-to-right particle current is

\[
J=\frac{a_Lb_R-a_Rb_L}{A_r+B_r}.
\]

Raising the occupied-state energy can accelerate escape but also decrease occupancy. Raising the useful transition-state energy relative to the empty pore additionally slows entry.

Assume that the two entry transition states have the same support response, both exits have the same multiplier, and the empty state E has R_E=0. These are model restrictions. Define

\[
\alpha=e^{-\beta\chi R_U},\qquad
q=e^{\beta\chi(R_A-R_U)}.
\]

Then a'_L=alpha a_L, a'_R=alpha a_R, b'_L=q b_L, b'_R=q b_R and

\[
\boxed{\frac{J'}{J}=
\frac{\alpha q(A_r+B_r)}{\alpha A_r+qB_r}.}
\]

For q>1 and 0<alpha<1, improvement requires

\[
\boxed{\frac{A_r}{B_r}>
\frac{q(1-\alpha)}{\alpha(q-1)}.}
\]

In the dilute entry-limited limit A_r/B_r -> 0, the current ratio tends to alpha, not q. The current can fall even though escape is much faster. In the strongly occupied, escape-limited limit it tends to q, provided the changed entry process remains sufficiently fast.

The especially optimistic R_U=0 case has alpha=1. Even then, a large local escape gain vanishes in the dilute limit. With fixed entry, unlimited escape can improve current by at most (A_r+B_r)/B_r. This is a transport-network bound, not a universal materials theorem.

The cycle affinity is unchanged:

\[
\log\frac{a'_Lb'_R}{a'_Rb'_L}
=\log\frac{a_Lb_R}{a_Rb_L}.
\]

The operation is not an equilibrium ion pump and supplies no free chemical affinity.

## 6. Fully declared numerical example — synthetic, not material data

Take T=300 K, R_A=0.12 eV, R_U=0.02 eV, R_H=0.20 eV, R_E=0, and kappa*c=1. All values are invented model inputs chosen to test coexistence and cancellation. They are not values for LLTO, hBN, graphene, or any real specimen.

The shared clamp raises the occupied-state energy by 0.06 eV, the useful transition-state energy by 0.01 eV, and the harmful transition-state energy by 0.10 eV, each relative to the empty-state response. Thus the useful barrier falls by 0.05 eV and the harmful barrier rises by 0.04 eV.

Assuming unchanged attempt and transmission factors, entry is multiplied by 0.6792, useful escape by 6.9177, and harmful escape by 0.21283. The useful-to-harmful local branching ratio improves by 32.5037. These are rate-model calculations, not measured rates.

With b_L=b_R=1 per second, the same clamp gives:

| Regime | a_L | a_R | J before (ions/s) | J after (ions/s) | Current ratio |
|---|---:|---:|---:|---:|---:|
| Dilute | 0.001 | 0.0001 | 0.000449753 | 0.000305630 | 0.67955 |
| Partly blocked | 10 | 1 | 0.692308 | 1.984698 | 2.86679 |
| Highly blocked | 1000 | 100 | 0.816697 | 5.557048 | 6.80430 |

The finite-control threshold for A_r/B_r is about 0.55210. Absolute rates are arbitrary and have no inferred physical throughput meaning. The example establishes that the local advantage can coexist with either a global gain or a global loss.

### Explicit first-passage damage accounting

Add an absorbing failure transition from the occupied state at rate h. There is no empty-state damage in this restricted illustration. Starting empty, the exact mean lifetime and expected net right-port transfer before failure are

\[
\mathbb E[T]=\frac{A_r+B_r+h}{A_rh},\qquad
\mathbb E[N]=\frac{a_Lb_R-a_Rb_L}{A_rh}-\frac{a_R}{A_r}.
\]

The second expression counts a right-reservoir entry as -1 and a right exit as +1. With a_L=10,a_R=1,b_L=b_R=1,h=0.001 per second, and h'=0.21283 h under the same clamp, expected net transfer before failure rises from about 818.09 to 26,593.89 ions, a factor of 32.507. Mean lifetime rises from about 1,181.91 to 13,399.64 seconds. These values were checked against the absorbing-generator linear equations. Other damage channels, multi-ion occupancy, chemical degradation, and electrode failure are absent and could reverse the conclusion.

## 7. Conservation and full resource costs

A passive constraint is not free to establish. In the fixed-A classical model, reversible quasistatic stiffness insertion costs

\[
W_A=\int_0^\kappa\frac12\langle(b^Tu)^2\rangle_{A,\kappa'}d\kappa'
=\chi R_A+\frac{k_BT}{2}\log(1+\kappa c).
\]

For the synthetic finite-clamp example this is 0.06896 eV per model subsystem. It is not a measured actuator cost. Population changes, support manufacture, switching losses, hysteresis, leakage, contact friction, solvent changes, reset, waste, and conditioning can add costs. A passive held support has no obligatory ideal continuous actuation power, but a real device's holding and maintenance costs must be measured. No work extraction from a single equilibrium bath is proposed.

For a conductivity-improvement claim at fixed current density j and thickness L, the maximum electrical saving for a change sigma_0 -> sigma_1 is

\[
p_{\rm saved}=j^2L\left(\frac1{\sigma_0}-\frac1{\sigma_1}\right).
\]

As an explicitly assumed screen, j=10 mA/cm^2, L=100 micrometres, sigma_0=1 mS/cm and sigma_1=10 mS/cm give 1 mW/cm^2 baseline ohmic loss and 0.9 mW/cm^2 saving. Any added optical/electrical control and net extra utilities must fit within that benefit for this task boundary. This is not an efficiency measurement or criticism of a particular published experiment.

For a uniform through-thickness series conductor, improving only a depth delta can eliminate at most delta/L of the original bulk resistance, even with infinite local conductivity. This geometric bound must not be applied to a different, in-plane measurement geometry. Interface-dominated systems need their actual equivalent transport problem.

## 8. Physical implementation and acquisition boundary

A supported versus suspended ultrathin ionic membrane is a plausible experimental class because its atomic transport sites may couple to a nearby support. Defect-engineered hBN has been investigated for Li-ion conduction and is one possible screening platform [S11]. That work does not provide the required transition-state compliance ordering, the chosen support law, or a demonstrated transport–damage improvement.

An independently adjustable or mechanically latched support could change stiffness while a transport aperture remains open. It would have to be implemented at an appropriate length scale; a remote macroscopic clamp need not constrain the relevant local atomic motion. Holding mean applied strain approximately fixed is a useful control, not proof that microscopic geometry is unchanged. A backing contact might change charge, bonding, solvation, or transport area more strongly than it changes the desired mechanical response.

The first material-specific calculation must include the actual support, pore chemistry, solvent/electrodes where relevant, occupied state, empty state, useful entry and exit paths, and credible damaging pathways. Compare the same geometry/regime with and without the proposed control. Arbitrary atom-freezing or hand-chosen favorable force projections cannot qualify this step.

Required inputs and acquisition paths:

- **Accessible stiffness and displacement coordinate:** characterize the real fixture and membrane response; obtain a validated mechanical/atomistic boundary model, not just a bulk elastic constant.
- **Occupied/empty free energies and transition ensembles:** use electronic-structure and finite-temperature rare-event calculations with validated chemistry and actual boundaries; constrain these by measurable occupancy, residence-time and transport data. A reactant phonon spectrum alone is insufficient.
- **Net transport and carrier identity:** measure DC transfer in a charge-balanced cell, separate electronic and displacement currents, and use collected material or tracer accounting where needed. A tracer identifies the carrier but does not itself establish the actuator mechanism.
- **Destruction and useful lifetime:** measure irreversible structural/chemical change and accepted output over time under the same loading, not in a separately gentler experiment.
- **Resources:** measure net source work, support establishment, heat handling, consumables, active-area loss, fabrication yield, reset, and product conditioning under a matched useful-output boundary.

No full same-regime acquisition is supplied in this invocation.

## 9. Exact continuation decision

Do not launch a complete apparatus programme from this checkpoint. The next useful result is one material-plus-support calculation or experiment that either satisfies or rejects the coupled inequalities with uncertainty estimates.

Reject or reclassify the route if the physically accessible overlap is too small; the useful and harmful transition responses have the wrong ordering; another damage pathway becomes dominant; slower entry or lower occupancy cancels escape improvement; prefactors/recrossing overturn barrier estimates; the device loses more area/energy/yield than it gains; or the mechanism and capability reduce to established strain/binding control without a new operation.

A reasonable initial diagnostic target is a clearly resolved useful barrier change together with an opposite-sign harmful-pathway change, followed by net transfer and damage measurements. A tenfold local target corresponds to 59.53 meV at 300 K, but no universal threshold makes an operation technologically transformative. The threshold must ultimately come from a declared device task and its strongest matched comparator.

Comparators include optimized composition/defect engineering, static strain or pore chemistry, reduced transport thickness, better contacts, and thermal operation at matched useful output. These are not straw-man untreated controls.

## 10. Astra capital consulted after independent selection

Repository revision read: `846f185763ed3a27310fad4ce9471ba324d1e5f4`.

Read the entry guide, N814 and N832 dossiers, and the full N832 alternative-operation derivations at `updates/FR-capital-mining-20261015/synthesis/alternative_physical_operation/DERIVATIONS.md`.

N832's explicit spring-supported electric/shear calculation reinforces that boundary control and specimen response must be solved together. Its zero-preload inversion-symmetry null is not an obstruction to all passive transport control: an occupied trap and its saddle are not assumed to be inversion-conjugate variants. The corresponding null in the present model is exact: if f_U = -f_A, then p_U squared equals p_A squared, R_U = R_A, and the clamp gives no useful barrier shift. A difference in deformation magnitude, not merely reversed sign, is essential. No GaAs pressure, wall mobility, hot-material coefficient, or loss law is imported into the ionic model.

N814's molecular work-return discussion reinforces complete resource accounting. Its conditional survivor-return floor is not a universal bound on a supported ionic membrane. Only the dossier was consulted for N814; its underlying molecular proofs were not re-audited here.

The inspected records explicitly retain open material-acquisition/capability obligations. Repository claims and same-team derivations are not independent experimental validation. No files were uploaded or committed to the repository.

## 11. Computational check receipt

`astra_transport_checks.py` performs 1,000 seeded random positive-definite matrix checks of the rank-one barrier identity and finite-difference checks of its response derivative. Maximum absolute errors in this run were approximately 3.16e-13 and 3.20e-9 respectively in synthetic numerical units. It also evaluates the coupled occupancy/entry model, checks unchanged cycle affinity and equilibrium zero current, and solves the explicit absorbing damage process.

`astra_transport_check_results.json` contains exact inputs and outputs. The scripts do not run molecular dynamics or electronic-structure calculations, acquire material parameters, establish novelty, or certify a physical effect.

## 12. Primary-source register

Sources are paraphrased, not reproduced. Access depth is stated to avoid treating an abstract as a full experimental audit.

**S1.** Kautz et al., *A nanoporous capacitive electrochemical ratchet for continuous ion separations*, Nature Materials 25, 1037–1044 (2026). DOI: 10.1038/s41563-026-02511-y. Preprint: arXiv:2309.00951. University/publisher records and preprint inspected; supports operation-level prior art, not an industrial efficiency conclusion.

**S2.** Minami et al., *Macroscopic Ionic Flow in a Superionic Conductor Na+ beta-Alumina Driven by Single-Cycle Terahertz Pulses*, Physical Review Letters 124, 147401 (2020). DOI: 10.1103/PhysRevLett.124.147401. Primary abstract inspected.

**S3.** Pham et al., *Correlated terahertz phonon–ion interactions control ion conduction in a solid electrolyte*, Materials Horizons 13, 3355–3375 (2026). DOI: 10.1039/d5mh01990g. Preprint arXiv:2305.01632v4, revised 25 December 2025. Preprint abstract and accessible publisher text inspected. No full experimental power budget certified here.

**S4.** Poletayev et al., *The persistence of memory in ionic conduction probed by nonlinear optics*, Nature 625, 691–696 (2024). DOI: 10.1038/s41586-023-06827-6. Primary HTML and relevant methods/transport discussion inspected.

**S5.** McClellan et al., *Photoinduced correlations in stochastic dynamics of a solid-state ionic conductor*, Nature Communications 17, 6552 (15 May 2026). DOI: 10.1038/s41467-026-72663-7. Primary HTML, acquisition protocol and correlation interpretation inspected.

**S6.** Fang et al., *Highly mechanosensitive ion channels from graphene-embedded crown ethers*, Nature Materials 18, 76–81 (2019; online November 2018). DOI: 10.1038/s41563-018-0220-4. NIST primary research abstract inspected.

**S7.** Sahu et al., *Optimal transport and colossal ionic mechano-conductance in graphene crown ethers*, Science Advances 5, eaaw5478 (2019). DOI: 10.1126/sciadv.aaw5478. NIST primary research abstract inspected.

**S8.** Noh and Aluru, *Scaling of ionic conductance in a fluctuating single-layer nanoporous membrane*, Scientific Reports 13, 19813 (2023). DOI: 10.1038/s41598-023-46962-8. Relevant primary HTML simulation and vibrational-mode sections inspected. Related work: *Ion transport in two-dimensional flexible nanoporous membranes*, Nanoscale 15, 11090–11098 (2023), DOI: 10.1039/d3nr00875d; bibliographic/abstract-level access.

**S9.** Noh and Aluru, *Activation of atomic transport via vibrational coupling-induced force fluctuations*, Applied Physics Letters 123, 091601 (2023). DOI: 10.1063/5.0160780. Primary abstract inspected; molecular-dynamics study, not experimental actuator qualification.

**S10.** Yang and Xie, *Lattice-renormalized geometric frustration drives fast ionic transport*, arXiv:2606.22345v2 (2026). Selected theory sections inspected. Preprint evidence; not independent experimental validation of the proposed boundary operation.

**S11.** Wu et al., *Defect-Engineered Hexagonal Boron Nitride Enables Ionic Conduction for Lithium Metal Batteries*. Preprint arXiv:2510.27021; publisher metadata also located for Nano Letters 26(30), 9791 (2026). Preprint abstract inspected. No numerical battery performance is transferred to the proposed clamped geometry.

## Bottom line

The retained question is whether one realizable passive boundary response can jointly reduce useful transport barriers, raise destructive barriers, and improve the full transport-and-lifetime process after entry, occupancy and resource costs are included. The exact model shows conditional coexistence and explicit failures; the material regime and distinct physical operation remain unestablished. This is a bounded research intermediate, not a new physical power claim.
