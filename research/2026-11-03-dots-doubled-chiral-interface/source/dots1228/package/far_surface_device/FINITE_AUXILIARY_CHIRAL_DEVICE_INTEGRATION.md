# Actual finite-auxiliary integration of the exposed ungauged chiral device

2026-11-03. Combines the audited global-norm open-device transfer with the actual symmetry disentangler and a newly proved compressed-rest gap. This is a finite-volume, volume-dependent-range construction. It does not claim a gauged continuum theorem or practical resource sizes.

## 1. Starting comparison and exact commuting factors

The audited physical bounded-rotor device satisfies, modulo a rotor-independent scalar C_ref,

 ||H_device-C_ref-(H_F+K_Q)||<=delta.

Throughout this note H_F=dGamma(h_F)-E_F,0>=0 is normal-ordered to its known free Fock ground energy E_F,0; that known scalar is included in C_ref. H_F is the explicit far free-CAR Hamiltonian, with all target modes below the static cutoff and the actual doubled canonical-copy multiplicity. K_Q is the exact canonical rest parent, with unique ground Omega_Q, ground energy0 and gap Delta. All high Wilson modes, decoration modes and rotor factors are retained in K_Q.

Add the required uniform theta-reset ancillas to both sides. Apply the ACTUAL anomaly-free shared-rotor disentangler D_g from the audited finite-auxiliary construction, to the entire Hamiltonian. D_g acts on interface rotors and decoration Majoranas; the free Wilson charges were already onsite and are not acted on. Therefore D_g acts trivially on the far CAR factor F. Its gates are parity even. The symmetric momentum cutoff P_N and K=sum_j L_j² act only on rotor factors in this frame, and likewise commute with F exactly.

The removed one-particle subspace includes complete multiplets and symmetric momenta, with conjugate/real-structure compatible canonical-copy and Nambu projections. Thus the CAR factorization and parity statement are genuine, not a formal splitting of incompatible BdG coordinates.

Unitary conjugation and compression are norm contractions. Adding the SAME kappa K to both sides does not change their bounded difference. Hence for every finite rotor cutoff P_L,

 || P_L[D_g^*(H_device+H_theta)D_g+kappa K-C_ref]P_L
       - [H_F+R_{kappa,L}] || <=delta,

where

 R_{kappa,L}=P_L[D_g^*(K_Q+H_theta)D_g+kappa K]P_L

acts only on the rest. K is added AFTER D_g conjugation; no unbounded differential operator is conjugated through a discontinuous rotor circuit.

## 2. Explicit Q-ground Fourier regularity

The projected static matrix obeys h_Q=QhQ with Q fixed in rotor configuration. Its derivative satisfies

 ||partial_j h_Q||_1<=||partial_j h||_1.

The uniform static rest gap gives

 ||partial_j sign(h_Q)||_1<=2||partial_j h||_1/g_fast.

The actual phase-fixed canonical Gaussian exponential therefore has vector derivative bound C_G||partial_j h||_1/g_fast, with C_G=4pi safely covering the copy/Majorana convention. Nonlocality of Q in space does not enter this trace-norm estimate. The elementary texture and decoration formulas supply the local derivative ranks and bounds already enumerated in the finite-auxiliary proof.

Apply the actual D_g inverse shears, floor phases and controlled Majorana rotations. Their finite local chamber enumeration gives derivative bounds B_j and wall counts R_j. No derivative is taken through a rounding wall. The resulting normalized vector has pointwise norm1. For m rotor coordinates, its rectangular Fourier tail obeys

 tau_N=||(1-P_N)D_g^*(Omega_Q tensor theta_uniform)||²<=A_Q/N,
 A_Q=sum_j(B_j+2R_j)²/(2pi²).

This is the actual interacting Q-ground, not an arbitrary eigenvector with an unspecified phase. The unchanged local trace-norm bounds make A_Q polynomial in volume, with the already paid microscopic constants.

## 3. New rest gap after cutoff and optional kinetic regulator

Let H_Q^g=D_g^*(K_Q+H_theta)D_g>=0. Its ground has energy0 and its gap is Delta, replacing Delta by min(Delta,1) if the added theta reset gap requires it. A safe finite-volume norm bound is

 B_Q=2 n_fast R_fast+m,

with the actual one-body copy count, all decoration constants and reset weights included. For tau_N<=1/2, normalize the Fourier trial chi_N=P_N Omega_Q^g/sqrt(1-tau_N). Since H_Q^g annihilates its exact ground,

 <chi_N,H_Q^g chi_N><=B_Q tau_N/(1-tau_N).

Choose a target energy e>0 and

 N0>=max(1,2A_Q,4B_Q A_Q/e),
 0<=kappa<=e/(2mN0²).

Then the trial belongs to every larger cutoff P_L, L>=N0, and its total energy is at moste. Positivity and min-max give

 0<=lambda0(R_{kappa,L})<=e,
 lambda1(R_{kappa,L})>=Delta,
 gap(R_{kappa,L})>=Delta-e.

Thus e<Delta gives a unique rest ground. This re-earns the gap for the NEW regulator. It does not claim that adding kappa K preserves the old excited rotor spectrum. Kappa=0 already gives a finite-dimensional compressed rest model; positive kappa additionally gives a coercive infinite-rotor completion if desired.

The same trial/min-max inequalities apply before compression when kappa>0, using its standard closed form. Its kinetic domain is nonempty and contains every finite Fourier trial, even if the original discontinuous canonical ground has infinite kinetic energy.

## 4. Finite device and low-energy content

Choose e<=Delta/8 and delta<=Delta/16. The actual finite-auxiliary Hamiltonian is globally delta-close, modulo C_ref, to

 H_F+R_{kappa,L},

whose rest factor is unique and separated by at leastDelta-e. Therefore its resolved low spectral content consists only of the explicit free far-Fock excitations, with the rest in its new ground. At an absolute cutoff belowDelta-delta and separated by more thandelta from the comparison spectrum, the actual low spectral projection has the same finite rank. Relative to the respective ground energies, spectral errors are at most2delta and the rest threshold is at leastDelta-e-2delta.

The new rest ground energy E_rest lies in[0,e]. It is not silently set to zero. If an absolute energy window must be known without solving the interacting rest, allow the whole interval[0,e], or make e smaller than the requested energy accuracy. Relative excitation energies do not need that offset.

For a unique FULL finite-device ground, also resolve the far AP level spacing p_min,lattice: the sufficient condition is2delta<min(Delta-e,p_min,lattice). No volume-independent device gap is claimed.

The actual canonical device has two same-chirality fast copies. Its exposed far content is correspondingly doubled relative to the original four-Weyl root. This construction removes no physical copy.

## 5. Real-time operation for the new finite model

Since all regulator and cutoff operations commute with F, the comparison dynamics on target CAR observables remain exactly those of H_F. Bounded-perturbation Duhamel gives

 ||{c(f,t),c(g)^*}-<exp(it h_F)f,g>I||
 <=4|t|delta ||f||||g||,

for ANY state of this NEW finite-auxiliary device. This is not inferred from approximation of old-model thermal or low-energy states. It follows directly from the new global comparison. A continuum-Weyl dispersion comparison, if requested, still separately costs |t|a²Lambda³. No dynamical gauge-field statement is included.

## 6. Energy-zero acquisition and resources

C_ref is a fixed one-body reference energy plus explicit decoration/copy normal-ordering constants. It can be certified by constructing the known fixed-texture compressed matrix and using a polynomial sign-trace approximation or a certified one-body eigensolver, with the correct BdG factor. This is a finite explicit calculation, not an interacting-ground-state oracle. Its numerical error must be added to energy-window budgets if QPE is used. The new E_rest is bracketed by[0,e]; a QPE protocol must use that interval or perform an energy search, not reuse an old zero-energy promise.

The physical fermionic Hamiltonian retains the audited finite patch radius and normal thickness O(log²(n/delta)) with the enormous endpoint constants stated in GLOBAL_NORM_REST_PARENT_TRANSFER.md. The symmetry circuit increases range by its fixed light cone. Rotor local dimension is2L+1, with L>=N0. For m rotor coordinates and F_phys physical fermionic modes, logical qubit count is

 F_phys+m ceil(log2(2L+1)).

The full Hilbert dimension remains exponential. Since A_Q=O(volume) and B_Q=O(volume) at fixed microscopic resources, N0 is polynomial in volume and1/e. Choosing kappa<=e/(2mN0²) is likewise explicit and may be very small. These are finite-resource, ungauged existence and quantum-compilation contracts, not a practical classical simulation claim.

The structured compiler evaluates the polynomial/finite-patch Gaussian formulas rather than storing dense local matrices. Its already audited finite-grid, Hermiticity, valid-code and symmetry-twirl corrections must remain in the combined error budget. A fresh compilation error eta_comp simply enlarges the final bounded comparison error to delta+eta_comp.

Symmetry scope: exact Fourier-cutoff symmetry is asserted for the actual integer onsite subgroup earned by D_g, together with any additional generators separately verified to commute with those projectors. It is not inferred for an arbitrary other subgroup merely from global anomaly cancellation. The ungauged far-CAR factorization itself is independent of this extra gauging question.


### Explicit reference-energy convention

For an actual number-conserving block c^* h c+C, its ground energy is C+Tr(h-|h|)/2. For an actual Majorana block(i/4)gamma^T A gamma+C, with real antisymmetric A, it is C-Tr|iA|/4. Equivalently a redundant Nambu expression(1/2)Psi^* H_BdG Psi+C_BdG has ground energy C_BdG-Tr|H_BdG|/4; C_BdG must include its actual normal-ordering constant. These formulas must not be mixed or applied twice.

Compute the fixed-texture Q-rest reference energy by summing these expressions over the actual canonical copies and decoration blocks, with the constant dummy-F contribution removed. This gives the C_ref in the reference-subtracted counterterm comparison. The free far energy E_F=Tr(h_F-|h_F|)/2 is also explicit. When the low-energy statements normalize H_F to have ground energy0, replace the total comparison offset by C_ref+E_F. No unknown interacting quantity enters that scalar. The new regulated rest energy remains separately bracketed by[0,e].

The trace can be certified to tolerance eta_ref by a finite sign/absolute-value polynomial with error <=eta_ref/(nR), or by a certified finite one-body eigensolver. The matrix Q and its geometric mode basis are explicit, so this calculation needs no spectral-state oracle. Complexity is polynomial in n and the requested bit precision at fixed gap/norm ratios.

For a claimed polynomial finite-energy cutoff of the optional coercive infinite-rotor completion, choose an explicit inverse-polynomial value, for example kappa=e/(4mN0²), rather than an arbitrarily smaller number satisfying only the upper bound. The bounded-part norm and standard estimate (2+T B_bounded)sqrt(E/kappa)/(L+1) then give a polynomial cutoff for that NEW model. Kappa=0 is reserved for the already finite compressed construction, not a finite thermal-trace claim for infinite rotors.

The Fourier/min-max component was independently derived by the finite-auxiliary worker in FINITE_AUXILIARY_REST_COMPATIBILITY.md. The global-norm component is independently audited in AUDIT_GLOBAL_NORM_REST_TRANSFER.md. This note supplies their actual common factorization, copy/parity conditions and energy-zero ledger, rather than treating the certificates as unrelated.
