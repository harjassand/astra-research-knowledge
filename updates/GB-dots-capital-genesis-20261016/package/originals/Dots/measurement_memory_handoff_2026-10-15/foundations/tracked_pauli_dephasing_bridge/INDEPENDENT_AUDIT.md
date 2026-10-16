# Independent audit: tracked full-Pauli refresh and actual error-label effects

Date: 2026-10-15. Verdict: valid on the explicitly restricted interface below. This is an exact physically corrected random-control model and a mathematical doubled-space proof, not the original autonomous stabilizer-dephasing memory generator.

## 1. Audited scope

There are finitely many identity-target pulses i with mutually disjoint physical data patches D_i of n_i qubits. Pulse intervals may overlap or nest. A common arbitrary finite persistent bath B is allowed. During interval I_i=[s_i,e_i], pulse i has a fixed-laboratory-frame Hermitian coupling V_i(t) supported on D_i tensor B, with ||V_i(t)||<=g_i; outside I_i it vanishes. Other terms are bath-only or commute with all selected checks in the proof. No Hamiltonian term simultaneously touches two pulse patches. Initial data and bath may be arbitrarily correlated.

Each pulse applies an independent uniform full-Pauli initial frame F_{0i}, independent of the initial data/bath and all other randomness. Independent Poisson X and Z updates on each data qubit are tracked exactly throughout its interval. At its end, the exact inverse of its entire current frame is applied. The laboratory coupling is independent of the chosen frames and records; fixed-frame conjugation is an actual physical relation, not a calibration assumption inferred from isolated average fidelities. Frame gates, updates, tracking, and final inversion remain exact resources.

For this audit, patches are mutually disjoint throughout the experiment, not merely nonoverlapping while simultaneously active. Reusing one physical patch in later pulses requires an additional virtual-history/support proof. No such reuse extension is silently supplied by the global conjugation below.

## 2. Initial twirl: actual correlated-input Kraus identity

Let eta_i(t) be the cumulative relative update frame, starting at identity at s_i and frozen after e_i. Moving the exact wrappers through operations on disjoint data patches gives the corrected joint unitary

 U_{F0,eta}=F_0^dagger W_eta F_0,

where F_0=product_i F_{0i} and W_eta has toggling Hamiltonian H_B+sum_i eta_i^dagger V_i eta_i, independent of F_0. Global Pauli phases of cumulative frames cancel; no phase convention on eta is required.

Expand in the orthonormal data-Pauli basis,

 W_eta=sum_p P_p tensor B_{p,eta},
 B_{p,eta}=d_D^(-1) Tr_D[(P_p^dagger tensor I)W_eta].

Averaging the independent full initial frames exactly kills all distinct Pauli characters. Thus the actual corrected channel has the Kraus representation

 rho -> E_eta sum_p (P_p tensor B_{p,eta}) rho
                            (P_p tensor B_{p,eta})^dagger. (1)

This is an equality for ALL joint data-bath inputs, including correlated inputs. It is not a reduced-channel twirl that assumes a fresh bath at each pulse. Trace preservation gives sum_p B_{p,eta}^dagger B_{p,eta}=I_B for every eta.

The frame independence is essential. Conditional postselection on a bath state which has already interacted with the selected initial frames does not establish (1); the derivation starts before their independent initialization and keeps all bath dynamics inside W_eta.

## 3. Correct doubled-space lift, including Y and phases

Use |A>>=(A_D tensor I_R)|I>> with normalized |I>>=d_D^(-1/2)sum_x|x>_D|x>_R. Conjugation by a unitary g is represented by

 C_g=g_D tensor g_R^*,
 C_g|A>>=|g A g^dagger>>.

For a Hermitian Pauli P, P^*=P^T, so the proposed expression C_P=P_D tensor P_R^T is correct. In particular C_Y=-Y_D tensor Y_R. Replacing it by +Y tensor Y would give the wrong Bell eigenvalue. For a cumulative non-Hermitian Pauli phase, use g tensor g^*, not an unqualified g tensor g^T.

All Pauli conjugation lifts C_P commute and fix |I>>. Each Bell-Pauli vector |P_p>> is their simultaneous eigenvector. Global phases cancel in C_g.

For any bath vector psi, define the pathwise error-state isometry

 A_eta psi=(W_eta tensor I_R)(|I>> tensor psi).

Its Bell coefficients are exactly B_{p,eta}psi. Now conjugate by the CURRENT relative frame,

 chi_eta=(C_eta tensor I_B) A_eta psi.

Between updates, the Hamiltonian of chi is the FIXED laboratory V_D+H_B, acting on D,B and trivially on R. At an update by P it jumps by C_P. Therefore its trajectory average is exactly the lifted Lindblad dynamics

 rho_dot=-i[H_B+sum_i V_i(D_i,B),rho]
             +sum_{i,q,a=X,Z} gamma_{iqa}(C_{a,iq}rho C_{a,iq}-rho). (2)

The starting state on every unused D_i R_i is |I>>, independent of the other registers, even when a pulse starts later. Earlier other-patch dynamics acts only on their registers and the bath. Bell-label projectors commute with every C_eta, so their endpoint probabilities in (2) equal the coefficient effects from (1). After a patch finishes, later disjoint-patch/bath operations preserve its Bell labels.

The R registers and their dissipators are a mathematical error-operator representation. They are not additional physical devices or assumed unmeasured responses. Equation (2) is justified by the explicitly tracked physical data controls and final inversions, not by adding dephasing to the original memory by fiat.

## 4. Positive error-label subset effect

For each marked pulse i, a nonidentity n_i-qubit Pauli label anticommutes with at least one of the 2n_i generating X/Z checks. Select one such lifted check Z_i=C_{a,iq} per marked pulse. Because physical patches are disjoint, V_j commutes with Z_i for j!=i. Split

 V_i=V_i^even+V_i^odd,
 V_i^odd=(V_i-Z_i V_i Z_i)/2,
 ||V_i^odd||<=g_i.

The odd term flips only its selected Z_i. All even terms and unmarked-pulse terms commute with every selected Z_i and can enter the baseline. Other randomizer trajectories can be conditioned on: they commute with the selected lifted checks, preserve the parity signature/norm, and are independent of selected clocks. This reduces exactly to the independently audited simultaneous endpoint-subset theorem, with the initial Bell state in the +1 sector of every selected check.

The selected coupling and selected dephaser act during I_i only. The paired-time integrals contain only times inside I_i, so the same proof uses its duration tau_i=e_i-s_i. Different overlapping/nested intervals do not add factorials; summing chronological word orders still partitions the product of the per-species ordered domains. Deterministic endpoint Bell labels of completed patches are unchanged afterward.

With gamma_i the minimum X/Z update rate on patch i, let

 B(g,gamma,tau)=1/2{exp(-gamma tau)
       [cosh(d tau)+(gamma/d)sinh(d tau)]-1},
 d=sqrt(gamma^2+4g^2).

Union over one generating check per marked pulse gives the actual joint coefficient EFFECT inequality

 E_eta sum_{p:p_i!=I for all i in S} B_{p,eta}^dagger B_{p,eta}
 <= product_{i in S} q_i I_B,
 q_i=min{1, 2n_i B(g_i,gamma_i,tau_i)}.                    (3)

The factor 2n_i is a simple union bound, not an assumption that the check changes are independent. Individual caps can be justified by discarding indices with uncapped q_i>1 and applying the same subset theorem to those retained. A looser expression is q_i<=min{1,n_i[exp(2g_i^2 tau_i/gamma_i)-1]}.

The endpoint theorem initially bounds a probability for every bath vector. Since the coefficient effect is positive and its quadratic forms obey the same bound, (3) follows as an OPERATOR inequality on B. The corresponding physical branch effect from (1) is I_D tensor that operator, and thus holds for arbitrary data-bath correlations and references. There is no conditioning on a favorable future bath state.

## 5. What the bridge does and does not buy

Unlike terminal stabilizer syndrome alone, p_i here is the FULL data-Pauli error label of a twirled identity pulse. Its zero label is identity on that entire patch, and a nonzero label is supported on that patch. Thus this is a potentially valid replacement for a per-clean-pulse action-squared effect budget in a suitable support theorem.

Composition still requires all of the following:
- Actual initial and final full-Pauli frames and exactly tracked updates.
- Fixed laboratory-frame coupling independent of seeds and no uncharged controller access to them.
- All data interactions during the pulse included in the permitted patch, and the required correction/pulse scheduling or reservation cleanliness.
- Separate justification for changing correction target operations, moving memory factors, reusing a patch, incomplete pulses, or overlapping physical supports.
- Noisy wrappers, record corruption, controller noise, leakage, and finite-duration updates qualified separately.

The construction uses private full-Pauli initial frames and exact pulse endpoints. It does not remove all external timing/controller assumptions or turn the earlier scheduled qualified-core memory result into a fully autonomous noisy-controller theorem. Nor does a covariant correction dissipator automatically fit the parity-preserving baseline of the endpoint proof.

## 6. Audit verdict and checks

Under Sections 1-4 the exact lift and positive coefficient-effect upgrade are valid. The transpose/Y issue is resolved by C_g=g tensor g^*. The effect bound is uniform in the persistent bath and arbitrary joint inputs, with explicit generating-check multiplicity. The main restrictions are physical frame tracking, disjoint patch incidence, and pulse/support composition.

The companion check_bridge.py verifies the lifted/classical telegraph Bell-label effects, full initial-frame correlated-input twirl, and Kraus completeness with noncommuting bath interactions. The independently written check_direct_fourier.py additionally tests the stronger direct Fourier effect theorem with reused support and a noncommuting baseline. These are interface checks, not a device or memory-lifetime experiment. See DIRECT_FOURIER_INDEPENDENT_AUDIT.md for that stronger route, which does not require a parity-preserving baseline or disjoint physical supports at the algebraic effect-bound level.
