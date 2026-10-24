# A local unitary inelastic spin sorter and its reset resource

24 October 2026. Owned derivation in the stated finite Hamiltonian model.

**Status: frozen; full internal review passed.** Root completed a consequential read of the local Hamiltonian, exact cofactor witness, unitary accounting identity, fixed-kinetic thermal branch, finite-packet/timing completion, and finite smooth SWAP/spent-stock ledger. The four existing supports checked the bounded dependencies listed in Section 10; root also independently replayed the scattering point and its cofactor identity. These are internal model checks, not external certification, novelty clearance, a CISS explanation, material acquisition, or demonstrated hardware advantage. Quantitative packet bandwidth and operating rate remain unacquired.

## 1. The operation and the obstruction

The target operation is spatial spin sorting: send a normalizable, unpolarized electron packet from the left, obtain a nonzero spin imbalance in the transmitted beam, retain every reflected and internal-mode outcome, and restore the internal mode using an explicitly counted resource. No electron is absorbed in the scattering model. The entire outgoing electron, summing transmission and reflection, has zero net spin.

One elastic orbital channel per ordinary lead cannot supply this operation in the spin-conserving TRS setting. An internal energy channel can change that conclusion without a fictitious absorbing bath. The construction below uses a three-site spin-orbit ring and one scalar-coupled two-level system (TLS). It generates its scattering matrix from local Hermitian couplings rather than assigning an arbitrary multichannel unitary.

The strongest conventional comparison is already multichannel TRS filtering, not a universal two-terminal prohibition. Utsumi, Entin-Wohlman and Aharony give a unitary two-orbital helical-junction construction with spin/orbital flips and nonmagnetic leads. Thus the broad extra-channel filtering operation is established. Our narrower result is an explicit spin-conserving, energy-exchanging realization and a resource identity charging its transmitted spin imbalance against reflected internal excitation. An elastic multiorbital incumbent has no such TLS reset requirement. No superiority to it follows. [Phys. Rev. B 102, 035445 (2020)](https://doi.org/10.1103/PhysRevB.102.035445), [primary manuscript](https://arxiv.org/abs/2005.04041).

## 2. One compatible Hamiltonian and its inputs

Set hbar=1 for evolution and restore hbar in the spin readout below. A single electron occupies sites 1,2,3, two leads, and a conserved spin label sigma=+1 or -1. An independent spinless TLS A has states n=0,1, gap Delta>0, N=|1><1|, and real tau_x. In either electronic lead the TLS remains present and free. It is not an additional electronic lead.

The central Hamiltonian in spin sector sigma is

\[
 H_{{\rm mol},\sigma}=h_\sigma\otimes I_2+I_3\otimes\Delta N
       +\eta |3\rangle\langle3|\otimes\tau_x,
\qquad
 h_\sigma=\begin{pmatrix}
 \epsilon_1&t&t e^{-i\sigma\phi}\\
 t&\epsilon_2&t\\
 t e^{i\sigma\phi}&t&\epsilon_3
 \end{pmatrix}.                                                    \tag{1}
\]

All epsilon_j,t,eta,Delta are real. The TLS coupling is scalar in electron spin. This is an exact two-level, Holstein-type local coupling; it is not a derivation of a particular molecular vibration or a truncation error bound for a harmonic oscillator.

Two spin-independent semi-infinite nearest-neighbor leads, with hopping t_l>0 and zero band-center energy, attach site 1 to L and site 2 to R with real contact hopping v. Contacts preserve n and sigma. Each lead has one electronic orbital at a fixed electron kinetic energy. The additional asymptotic label is the state of the same physical TLS.

The hopping e^{i phi sigma_z} is a specified TRS spin-orbit link, not an electromagnetic flux or a Zeeman term. With Theta=i sigma_y K and the real TLS basis, H_- = H_+^* and the complete Hamiltonian is TR invariant. Spin is conserved. The loop holonomy e^{i phi sigma_z} remains as a model resource; no material realizing the chosen large phase is acquired here.

For comparison, on an electronic tree, static mode-independent SU(2) link matrices can be removed by site spin frames along unique paths. Scalar on-sites and scalar internal-mode couplings remain spin independent; the mode kinetic Hamiltonian is unaffected by a mode-independent frame. The constant frame in either lead preserves an unpolarized input. This familiar gauge argument is conditional on those couplings: it does not cover mode-dependent spin frames, onsite spin/orbital structure, or arbitrary spin-flip devices. The ring in (1) evades this particular tree reduction.

The ideal benchmark input is a ground-state TLS and an unpolarized left electron. Section 6 replaces the monochromatic benchmark by a finite-band product beam and finite-temperature TLS stock. A pure ground-state stock is not silently supplied by a finite-temperature, finite-time reset.

## 3. Flux-normalized unitary scattering at fixed total energy

At total electron-plus-TLS energy E, channel n has electron energy E_n=E-n Delta. If |E_n|<2t_l for both n, define

\[
 \Sigma_n(E)=\frac{v^2}{2t_l^2}
       \left(E_n-i\sqrt{4t_l^2-E_n^2}\right),\qquad
 \Gamma_n=-2\operatorname{Im}\Sigma_n>0.                            \tag{2}
\]

Place Sigma_n on electronic contact sites 1 and 2 in TLS block n, and put zero on site 3. Let G_sigma=(E-H_mol,sigma-Sigma)^(-1). In contact order (L0,R0,L1,R1), let W embed each contact into its central site with coefficient sqrt(Gamma_n). Then

\[
 S_\sigma=I_4-iW^\dagger G_\sigma W.                                \tag{3}
\]

This normalization includes the different channel group velocities. The identity
G-G^dagger=-i G W W^dagger G^dagger proves unitarity of S. There is no omitted TLS bath or imaginary loss term.

All central inverses are regular whenever both channels are open in this model. If (E-H-Sigma)x=0, the positive imaginary part forces both contact components in each TLS block to vanish. The site-2 equations, with hopping t=1 in the witness, then force both site-3 components to vanish. Thus x=0. In particular, no real scattering pole occurs on the open-channel intervals used below.

Transpose, not complex conjugation of the retarded self-energy, gives

\[
 G_-=G_+^T,\qquad S_-=S_+^T.                                       \tag{4}
\]

The identical diagonal retarded self-energy is unchanged by transpose. Equation (4) is the appropriate two-spin reciprocity relation in this channel convention.

## 4. An exact spin/excitation identity

For ground-left input define

\[
 T_\sigma=\sum_{n=0,1}|S_{\sigma,Rn,L0}|^2,\quad
 \bar T=(T_++T_-)/2,\quad
 P_T=\frac{T_+-T_-}{T_++T_-},\quad F=\bar T P_T=(T_+-T_-)/2.          \tag{5}
\]

F is the dimensionless signed transmitted spin flux per incident electron; its angular spin is (hbar/2)F. An unpolarized input weights the two incident spins by 1/2.

Let U=S_+ and name a=L0,b=R0,c=L1,d=R1. Column a unitarity gives
T_+=1-|U_aa|^2-|U_ca|^2. Row a unitarity, together with (4), gives
T_-=1-|U_aa|^2-|U_ac|^2. Therefore

\[
 T_+-T_-=|U_{ac}|^2-|U_{ca}|^2.                                    \tag{6}
\]

The spin-averaged reflected excitation probability for this same input is

\[
 P_{{\rm exc,ref}}=\tfrac12(|U_{ca}|^2+|U_{ac}|^2).
\]

Consequently

\[
 \boxed{|F|=\bar T|P_T|\le P_{{\rm exc,ref}}\le P_{{\rm exc,total}}.  \tag{7}
\]

Here total excitation includes transmitted and reflected outcomes. For a ground TLS its mean gained energy is Delta P_exc,total, at least Delta |F|. This is an excitation/restoration-energy accounting statement, not a universal lower bound on heat or work for all spin sorters. It uses spin conservation and the specified channels; no coefficient-one generalization to arbitrary spin-flip TRS scattering is claimed.

Each spin has T_sigma+R_sigma=1, so the reflected angular spin is -(hbar/2)F. The complete outgoing electron remains unpolarized when both leads and both internal outputs are included. The sorter redistributes spin spatially.

The bound is algebraically sharp in the abstract four-channel class: the three-cycle a->b->c->a, with d fixed, and its transpose partner give Tbar=1/2, P_T=1 and P_exc=1/2. This is only a unitary sharpness check. It does not prove that (1) reaches that limit; the actual local witness below does not saturate it.

## 5. A nonzero witness from the local Hamiltonian

Choose the following single dimensionless point, without a parameter search:

\[
 t_l=v=t=1,\quad E=\tfrac12,\quad\Delta=1,\quad
 (\epsilon_1,\epsilon_2,\epsilon_3)=(0,\tfrac3{10},-\tfrac15),\quad
 \eta=\tfrac25,\quad\phi=\tfrac\pi2.                               \tag{8}
\]

The electron energies are E_0=1/2 and E_1=-1/2, both strictly inside the lead band. They are energies relative to a band center; a negative channel value here is not a negative absolute-energy premise.

There is an elementary analytic nonzero proof. Let
G_n=[E_n-h_+-diag(Sigma_n,Sigma_n,0)]^(-1), P_3=|3><3|. The rank-one mode coupling gives

\[
 G_{10}=\frac{\eta G_1 P_3G_0}
                    {1-\eta^2(G_0)_{33}(G_1)_{33}}.                \tag{9}
\]

Thus, in the plus sector,

\[
 r_{10}=-i\sqrt{\Gamma_0\Gamma_1}
 \frac{\eta(G_1)_{13}(G_0)_{31}}{D},\quad
 r_{01}=-i\sqrt{\Gamma_0\Gamma_1}
 \frac{\eta(G_0)_{13}(G_1)_{31}}{D},\quad
 D=1-\eta^2(G_0)_{33}(G_1)_{33}.                                   \tag{10}
\]

Their squared-modulus difference is (6). For an explicit cofactor evaluation set d_jn=E_n-epsilon_j-Sigma_n for j=1,2, and d_3n=E_n-epsilon_3. At phi=pi/2,

\[
 D_n=\det G_n^{-1}=d_{1n}d_{2n}d_{3n}-d_{1n}-d_{2n}-d_{3n},\quad
 C_n=d_{1n}d_{2n}-1,
\]
\[
 (G_n)_{13}=(1-i d_{2n})/D_n,\quad
 (G_n)_{31}=(1+i d_{2n})/D_n,\quad (G_n)_{33}=C_n/D_n.              \tag{11}
\]

Writing y=sqrt(15)/4 gives d_20=-1/20+iy, d_21=-11/20+iy. The two product numerators differ by
4y[(11/20)^2-(1/20)^2]=3sqrt(15)/10>0. Including the broadenings and common denominator,

\[
 T_+-T_-=\frac{9\sqrt{15}}
 {50|D_0D_1-(4/25)C_0C_1|^2}>0.                                   \tag{12}
\]

In exact arithmetic, with d=413583083,

\[
 |r_{10}|^2=\frac{3000(1489-375\sqrt{15})}{d},\quad
 |r_{01}|^2=\frac{3000(1489+375\sqrt{15})}{d},
\]
\[
 F=\frac{1125000\sqrt{15}}d=0.0105350205160\ldots,\quad
 P_T=\frac{2000\sqrt{15}}{713843}=0.0108510788681\ldots,             \tag{13}
\]
\[
 \bar T=0.970873094198\ldots,\quad
 P_{{\rm exc,ref}}=\frac{4467000}d=0.0108007319052\ldots,\quad
 P_{{\rm exc,total}}=\frac{61692000}d=0.149164708461\ldots.           \tag{14}
\]

The exact replay verifies (3),(4),(7),(9),(10), not only floating-point transmission values. Root's independent full-resolvent replay agrees. In this particular model eta=0, phi=0 or pi, or Delta=0 removes the signed difference; removing a ring edge also removes the spin holonomy by the tree gauge. These controls are not universal claims about other Hamiltonians.

The nonzero point is not a sizable or optimized performance result. Its large spin-orbit phase and all coupling values are specified model inputs, not calibrated material parameters.

## 6. A finite-band product beam and a finite-temperature mode

Let F_0(E) be (5) for a ground TLS at total energy E. For an excited left TLS at the SAME total energy, row/column c unitarity gives F_1(E)=-F_0(E). This is not an unconditional cancellation for a thermal mode.

For an independently prepared electron of kinetic energy K and a thermal TLS with
p_beta=[1+exp(beta Delta)]^(-1), the excited input has total energy K+Delta. Its actual spin flux is

\[
 F_\beta(K)=(1-p_\beta)F_0(K)-p_\beta F_0(K+\Delta).                \tag{15}
\]

Only an ensemble conditioned to have the same total energy in both TLS branches permits a factor (1-2p_beta)F_0(E). In general that is not a product beam, and no tanh reduction is used here.

At (8), a kinetic interval inside (1/4,3/4) keeps every required shifted channel K-Delta,K,K+Delta inside the lead band. Section 3 proves regularity. Continuity therefore supplies a nonzero subinterval around K*=1/2 on which F_0(K)>3F*/4, where F*=F_0(K*) is (13). Choose a normalized h in C_c^infinity supported in that subinterval. Its nonzero finite bandwidth is fixed before preparation; no numerical width is asserted. Asymptotic energy orthogonality gives

\[
 F_{{\rm packet},\beta}=\int |h(K)|^2
 [(1-p_\beta)F_0(K)-p_\beta F_0(K+\Delta)]\,dK.                    \tag{16}
\]

The conservative bound |F_0|<=1 and p_beta<F*/8 imply F_packet,beta>F*/2>0. For orientation, the sufficient condition is beta Delta>about 6.63, not a Kelvin temperature or a practical operating window. It uses a finite-temperature mixed stock and finite-width normalizable beam, not an exactly ground TLS or a monochromatic physical state.

For an excited input the analogue of (7) charges the spin flux to reflected DE-excitation. A thermal mixture is bounded by the probability of internal transitions, with the appropriate branch energies. Its net mode-energy change can contain cancellation between excitation and de-excitation; there is no inference that Delta times net population change always bounds |F_packet,beta|.

The source supplies one unpolarized single electron with a specified finite-energy spectral state per use. A source implementation, its efficiency, a calibrated spin-resolved collector, and a useful packet bandwidth/rate are not acquired by this mathematical existence statement.

## 7. Finite departure and reset timing

Equations (3)-(16) use asymptotic scattering, not an assertion that a smooth finite-band packet is exactly absent from the central region at a finite time. The finite-time completion is an approximation with an error charged against the strictly positive margin in (16).

A packet assembled from the regular scattering states with h in C_c^infinity has no bound-state component. Its amplitude in any fixed finite interaction region is an integral of smooth, compactly supported energy coefficients times exp(-iEt); integration by parts makes it tend to zero. The incoming/outgoing lead pieces have the corresponding traveling phases. Nonstationary-phase estimates on the wrong-direction half-line give norm convergence to the free incoming packet in the distant past and to the free outgoing packet in the distant future. This also permits a product free incoming packet prepared far from the ring at a finite starting time: its error from the scattering incoming state can be made arbitrarily small. Any bound-state admixture caused by that finite approximation is included in this error, not discarded.

For clarity, fix a finite reset duration tau. Compare the actual Hamiltonian during reset with the asymptotic free-electron Hamiltonian plus the same reset on the TLSs. Their difference V_loc is bounded and supported on a finite electronic region (including lead endpoints). For the ideal outgoing state, let ell(T) be the maximum probability in that region during [T,T+tau]. It tends to zero. Purification and Duhamel give an additional vector error at most

\[
 \|V_{\rm loc}\|\,\tau\sqrt{\ell(T)},                              \tag{17}
\]

in addition to the scattering norm error at T. A TLS-only SWAP leaves the electronic marginal, hence ell(T), unchanged in the comparison dynamics. Consequently a finite wait and finite reset can approximate the asymptotic operation to any prescribed nonzero accuracy. Bounded spin/lead effects change by at most their operator norm times the trace-norm state error. Choose that error below the positive margin in (16).

This argument is existential. It supplies no numerical dwell time or uniform rate as the packet bandwidth narrows. It assumes the packet's scattering-state preparation and regular open-channel support just specified. It neither uses a finite exact departure nor postselects away a surviving central component. It also does not claim exact indefinite repeated operation with a fixed nonzero per-shot error.

## 8. An explicit finite reset, with every stock/output retained

After departure in the ideal comparison operation, supply TLS B with the SAME gap Delta and independent state tau_beta. Set

\[
 H_A+H_B=\Delta(N_A+N_B),\quad
 W_{\rm sw}|i\rangle_A|j\rangle_B=|j\rangle_A|i\rangle_B,
\quad H_{\rm sw}(t)=J(t)W_{\rm sw}.                               \tag{18}
\]

W_sw is Hermitian, W_sw^2=I, and [W_sw,H_A+H_B]=0. A smooth finite pulse with zero endpoint values, |J|<=J_max, and integral Jdt=pi/2 gives

\[
 U=e^{-i(H_A+H_B)\tau}(-iW_{\rm sw}),\qquad
 \tau\ge\pi/(2J_{\max}).                                          \tag{19}
\]

The target A returns exactly to tau_beta and is uncorrelated with the electron. Its old state AND its electron correlations move to the spent B. This works even when the old A marginal is coherent. The outgoing electron marginal is unchanged. Free evolution does not change tau_beta.

In this declared reset Hamiltonian, <W_sw> is constant, so the NET coupling work is

\[
 W_{{\rm switch,on}}=\int\dot J\langle W_{\rm sw}\rangle dt=0.        \tag{20}
\]

This is not zero hardware control cost: the exchange coupling, maximum strength, pulse area, finite time, finite controller, and thermal stock are additional inputs. Pulse-area error, imperfect stock, and the finite-departure error in (17) remain operational errors. The work correction from a vanishing state error is bounded by integral |Jdot| times that error, for this fixed smooth pulse.

Let p_in,p_out be the target populations before/after scattering. The exact static-scattering ledger is

\[
 \Delta E_{\rm electron}=-\Delta(p_{\rm out}-p_{\rm in}),\qquad
 \Delta E_A=\Delta(p_{\rm out}-p_{\rm in}).                         \tag{21}
\]

For the thermal operation p_in=p_beta. SWAP transfers Delta(p_out-p_beta) to B. A then returns to its original energy; the spent ancilla remains an output. If B is passively rethermalized with no work recovery, this energy is heat exported in the complete rethermalization limit. With energy recovery and correlations retained, heat and work partition differently. For a general reset with decoupled endpoints, positive outward heat and extracted work obey

\[
 Q_{\rm out}+W_{\rm out}=\Delta(p_{\rm out}-p_{\rm in}),             \tag{22}
\]

provided all auxiliaries other than the named heat/work outputs are returned. For an exact ground input and passive ground restoration, the released energy is Delta P_exc,total>=Delta|F|; it is exactly bath heat only under that passive/no-recovery convention.

One thermal ancilla is consumed/exported per exact model reset, or its rethermalization must be supplied. The spent B contains entropy and correlations not determined by p_out alone. A finite-rate finite-temperature bath generally only approximates tau_beta in finite time; its residual error and reused-stock error must be counted. No free perfect ground reset, free growing ancilla supply, correlation erasure, or closed autonomous finite-resource perpetual cycle is asserted.

Maintaining the incoming electron distribution is also a source resource. Energy lost by the electron is not replenished by declaring A reset. The static Hamiltonian does no work during scattering; its source energy, mode energy, spent-ancilla energy, potential bath/recovery streams, and every electron output together close the energy ledger. A real controller and readout can add costs absent from this ideal model.

## 9. What is established and what the strongest prior already supplies

The construction supplies a local, nonmagnetic, fully unitary single-packet spatial sorter with a nonzero analytic witness. Finite bandwidth and a low but nonzero thermal occupation preserve a positive model flux, and a finite reset with counted thermal stock returns the target mode. A finite-time implementation approaches that operation without discarding packet tails. The excitation bound (7) is exact in its spin-conserving ground-input contract. It does not claim a useful polarization, optimality, a calibrated physical TLS/SOC realization, or an advantage over elastic multiorbital filtering.

Vibrational spin-selectivity ancestry is strong. Fransson's model uses SOC-derived spin-dependent electron-phonon terms and, for the transport selectivity calculation, a magnetic analyzer configuration; it does not furnish this closed single-electron/TLS channel accounting. That difference is a model distinction, not a priority conclusion. [Phys. Rev. B 102, 235416 (2020)](https://doi.org/10.1103/PhysRevB.102.235416), [primary author copy](https://www.diva-portal.org/smash/get/diva2:1521748/FULLTEXT01.pdf).

Upadhyay and Levy's self-consistent weak-coupling NEGF/SCBA calculation reports negligible energy-integrated CISS in its helical transport setting with a magnetization-reversal analyzer and thermal phonon occupations. Our finite prepared-mode packet, large specified SOC phase, and exact TLS scattering problem do not test that steady-state weak-coupling claim. A one-energy unitary example is not evidence for explaining molecular CISS or producing a bias-driven spin current after thermal/spectral integration. [J. Chem. Phys. 164, 164303 (2026)](https://doi.org/10.1063/5.0324706), [primary manuscript](https://arxiv.org/abs/2601.15063).

## 10. Bounded support and reproducibility

The central derivation belongs to this source; support checks have narrower scopes. They are not external reviews.

- `luna_resolvent_algebra/UNITARY_INELASTIC_SORTER_AUDIT.md` and `check_spin_scattering.py`: exact SymPy transpose, unitarity, rank-one reflection identity, exact probabilities and inequality. `SECTION6_PRODUCT_BEAM_AUDIT.md` separately checks the excited-input identity, kinetic-energy shift and finite-band thermal margin.
- `luna_boxcar/LOCAL_RING_TLS_SCATTERING_AUDIT.md` and `spin_sorter_check.py`: local Hamiltonian/TRS/flux-normalization and independent numerical replay/controls; no physical calibration.
- `luna_single_port/FULL_CYCLE_ENERGY_AND_FINITE_ERROR_AUDIT.md`: energy, entropy and reset accounting. Its single-energy thermal notation is superseded for the product-beam contract by `THERMAL_SWAP_AND_KINETIC_BRANCH_ADDENDUM.md`, which checks (15),(18)-(22) and finite-error boundaries.
- `luna_random_lag_sources/PRIMARY_PRIOR_NOTE.md`: the three named primary comparisons and their model/operation limits.
- Root's independent full six-state resolvent replay agrees with (13)-(14) and independently obtains the nonzero radical in (12). This supports the algebra, not a material or hardware claim.
- Boxcar's subsequent Section 7 readback checks the finite-support Duhamel estimate and scattering norm asymptotics; finite-start bound-state admixture remains in the separate norm-error budget. Root's full read also covers this finite-time interface.

No parameter sweep, laboratory action, purchase, external outreach, dissemination, or acquisition claim is part of this unit.
