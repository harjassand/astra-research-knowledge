# Central construction: canonical doubled Gaussian preparation and symmetry averaging

Root derivation, 2026-11-03. This is a collective-gap construction under explicit outstanding locality/representation checks. It is not yet a completed strictly bounded-range single-interface theorem.

## 1. Use the actual static model, with both faces gapped

The audited two-massed-face Wilson construction has two independent, covariantly transforming textures U0(phi0), U1(phi1). It is NOT a slab with a fixed identity mass at its remote face. Its full one-body gap is at least M/3, uniformly in lateral volume, and the same bounds extend uniformly over normal lengths L>=2. Add the actual decoration on each face with the opposite signed self-linking charge. The fast ground state psi_phi is Gaussian, nondegenerate, has exactly zero combined axial charge and hence even fermion parity. The occupied-count proof is the actual Wilson/localizer bridge, not assumed anomaly matching.

Take two copies related by matrix conjugation while retaining the same axial eigenvalues, not negating them. The conjugate copy has reversed free V charges; these simply interchange the +/-1 flavors. Alternatively identify it with an identical free copy by the explicit onsite real-structure matrix. Its free Weyl chirality and A V^2 anomaly coefficient are unchanged. The conjugate decoration retains the SAME scalar self-linking term and K_phi is replaced by K_phi*. This is not the inverse-anomaly dual-fiber comparator.

## 2. Canonical Gaussian preparation has no ground-state phase oracle

For a number-conserving pure projector P_phi, particle-hole transform the second copy for calculation. Its desired doubled covariance is diag(P_phi,1-P_phi). The onsite Bell covariance is (I+tau_x)/2. With F_phi=2P_phi-I, the explicit one-body rotation

 R_phi=exp(i pi tau_y tensor F_phi/4)

sends the Bell covariance to diag(P_phi,1-P_phi). F_phi=-sign(h_phi) is acquired from the actual uniformly gapped finite-range one-body Hamiltonian.

A Majorana version covers the superconducting decoration. For pure covariance Gamma (Gamma^T=-Gamma,Gamma^2=-I), an orthogonal pi/4 rotation with off-diagonal blocks +/-Gamma maps an intercopy Bell covariance to diag(Gamma,-Gamma), with the second-copy basis convention fixed explicitly. The lifted quadratic fermion unitary is defined by its exponential, so no independently chosen eigenvector phases or global Slater determinant phase are inputs.

Fermionic convention check is essential: a product of local Gaussian Bell pairs differs from ordinary copy-ordered vectorization by (-1)^{N(N-1)/2}. On the fixed even-parity COMBINED fast sector this is i^N, an onsite Gaussian phase on the conjugate copy. One must either purify the whole free+decoration covariance in this convention or explicitly keep the separate parity correction. Exact small-mode checks and the complete representation contract are being independently worked out.

## 3. Joint locality is acquired by spectral polynomials

Uniform gap and bounded local one-body norm give exponentially convergent polynomial approximants to sign(h_phi). Their errors are uniform over every rotor configuration. The difference of successive polynomial approximants has bounded norm and finite hopping radius, and depends only on rotor values in that radius. A telescoping series therefore supplies an exponentially quasilocal JOINT rotor–fermion interaction for the controlled quadratic generator, not merely a matrix whose entries depend on distant rotors.

Concretely a degree-n term connects at most polynomially many sites within distance n; the polynomial volume factor is dominated by the exponential approximation error. Rotor coefficients are bounded multiplication operators. Differentiability across rotor rounding walls is not required. The controlled unitary W=int dphi |phi><phi| W_phi is thus finite-time quasilocal with volume-independent bounds when both endpoint faces are gapped.

## 4. Exact collective parent and gap

Let H0 be the sum of independent rotor reset projectors and onsite Bell-pair penalties. Its normalized ground is the rotor product |+> times Bell reference, with gap1. Define Hpar=W H0 W†. It has exactly the same unique ground and gap. The ground wavefunction is the canonical doubled Gaussian family, so its arbitrary fast-state phases cancel.

The V action is covariant on that family and on the reference Bell/rotor state. Each fast fiber has axial charge zero. Therefore the full ground Psi is invariant under the ACTUAL axial symmetry U_A(beta). The latter is a finite-depth controlled local circuit: onsite free charge rotations, controlled disjoint decoration-pair rotations, and bounded local scalar cochain phases.

Define Hsym=int_0^{2pi} U_A(beta) Hpar U_A(beta)† d beta/(2pi), with V averaging included only if its exact covariance has not already been established. Each conjugate is positive, has the SAME ground Psi, and obeys H>=I-|Psi><Psi|. Thus their average has unique ground and gap>=1. This is a collective extensive-system proof, not a single avoided-crossing extrapolation. Axial averaging preserves quasilocality because the symmetry has bounded circuit depth. The path from Hpar to Hsym shares its exact ground and gap. W is a finite-time quasilocal unitary, so the ground has no intrinsic topological order.

## 5. Remaining physical gates, not supplied by this note

- Verify all fermionic Choi/Bell conventions and exact doubled representation. Same chirality is essential; accidentally using the inverse anomaly would trivialize the task.
- Establish the parent on uniformly gapped two-interface slabs for arbitrary L and take a controlled half-space limit. The untreated far Weyl boundary cannot be spectrally flattened and called the original target. It must be introduced later, after isolating the gapped interface, or joined to original free bulk through a paid local gapped interpolation.
- Prove quasilocal-to-strictly-bounded-range truncation stability with exact symmetry. Generic gapped Hamiltonians are not automatically stable. Product-parent/locally gapped frustration-free machinery is being examined explicitly.
- Preserve free-SPT bulk rather than replacing it by an unrelated inverse layer. Deep-bulk canonical preparation should yield the two conjugate-matrix free projectors; local changes near the interface and their tails must be charged.
- Finite rotor/qubit resources and the actual anomaly-free stack/disentangler/gauging contract remain later gates. The current existence-scale UV constants are astronomical.

The point of the construction is that phase-free Gaussian doubling, an actual charged static endpoint, controlled local preparation, and common-ground symmetry averaging might join the previously separate operations. No completed bounded-range regulator or practical capability is claimed before these checks close.

## 6. Strengthening: preserve the ORIGINAL free bulk exactly

The unit-weight conjugated Bell parent above is not necessary. Use instead

 Hpar_actual = Hfast(phi) - E0(phi) + W Hrot W†,

where Hfast is the ORIGINAL quadratic Wilson plus decoration Hamiltonian for both copies, and Hrot is the sum of product rotor resets. In the reference frame Kref(phi)=W_phi†[Hfast(phi)-E0(phi)]W_phi is a positive quadratic Bell-quasiparticle Hamiltonian with

 g N_Bell <= Kref(phi) <= R N_Bell.

Consequently Kref+Hrot has unique product ground and gap>=min(g,1), even though its coefficients depend on phi. The actual fast part is already exactly A/V invariant, so axial averaging changes only the dressed rotor-reset terms. The original nearest-neighbor quadratic bulk is retained, not replaced by a flattened bulk.

E0(phi) is constructively available as a quasilocal scalar interaction: for a number-conserving block, local density e_x=tr[(h-sqrt(h²))/2]_{xx}. Uniform gap gives polynomial approximants of sqrt on [g²,R²]. Each polynomial diagonal is a finite closed-walk stencil; the telescoping interaction has exponentially decaying range. The per-site trace factor is the fixed onsite orbital dimension, not total volume. Decoration constants and any Nambu factor must be kept explicitly. Deep-bulk constants may be subtracted. The phi-dependent part is localized near the rotor interfaces. Its finite-range approximation is a genuine additional error in the stability ledger.

A further exact algebraic improvement: Qref(phi)=W_phi†Q_A(phi)W_phi is quadratic and has the fixed Bell vacuum as a charge-zero eigenvector. Therefore its pair-creation/annihilation coefficients and scalar vanish in Bell quasiparticle variables. It commutes with the SAME N_Bell for every phi. Thus R_beta=W†U_A(beta)W preserves N_Bell and is identity on N_Bell=0. The averaged reference rotor resets are positive, preserve N_Bell, and equal the bare Hrot on N_Bell=0. This gives the same collective gap directly by sectors.

For stability, each difference R_beta hrot_x R_beta†-hrot_x annihilates the Bell vacuum for ALL rotor states. Product conditional-expectation shells yield |Krot-Hrot|<=C N_Bell. Therefore N_Bell+Hrot <= Krot+(C+1)N_Bell <= max(1,(C+1)/g)(Kref+Krot). This is the required product-excitation coercivity, not merely a global spectral-gap assertion.

The finite-range proof must retain the NORMAL direction as explicit lattice sites when L tends to infinity. Absorbing an entire L-layer slab into one onsite factor would hide L-dependent local norms. Fixed UV/coarse refinement may have enormous constants but is independent of lateral volume and L. The uniformly gapped two-interface sequence and uniform locality then permit an actual half-space interface limit.

Independent Gaussian checks: root's15 random even states on1–3 fast modes and the other constructor's2/4-mode checks agree with the graded canonical target to ~1e-15, including no uncontrolled phase. These checks support the exact covariance/Clifford algebra; they are not the collective gap proof.
