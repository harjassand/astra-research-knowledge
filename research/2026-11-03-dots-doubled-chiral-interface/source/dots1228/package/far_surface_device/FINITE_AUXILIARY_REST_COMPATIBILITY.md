# Finite auxiliary/coercive completion of the exposed far-surface device

2026-11-03. This is a joint compatibility proof, conditional on the audited bounded global-norm transfer and fixed-Q static gap. It is not a transfer of arbitrary low-energy states of the infinite-degeneracy reset model.

## 1. Exact assumptions and the symmetry frame

Use the global comparison, with the energy-zero convention explicitly recorded,

 ||H_device−C_ref I−(H_F tensor I+I tensor K_Q)|| <= delta.

Normalize H_F>=0 by subtracting its known free Fock vacuum energy. K_Q>=0 has a unique canonical ground Ω_Q, rest gap Delta>0, and bounded norm B_Q. F contains complete species/canonical copies and conjugate-hole partners. Q is a FIXED valid CAR/BdG complement, independent of rotor configuration. These are the hypotheses audited in GLOBAL_NORM_REST_PARENT_TRANSFER.md, including near-mass leakage and the dummy-gap convention.

Add theta ancillas with bounded reset Hamiltonian H_theta and uniform ground, on both sides. Apply the actual anomaly-free-stack disentangler D†, with PLUS cochain phase and output-matching integer-projector dressing as proved in ../joint_gap/SHARED_ROTOR_DOUBLE_DISENTANGLER.md. For the concrete two-base doubled stack it uses bosonic weights(2,−8), vector shears(2,1), and fermion-copy weights(1,−4). There is one shared rotor per doubled base and one theta per boundary vertex. K decorations use the declared normal ordering Σ n_pair, vacuum charge zero.

D acts only on rotors and decoration fermions. All its gates are fermion-parity even. Hence it commutes with the far CAR algebra and preserves its exact graded tensor factorization. The transformed chosen U(1) is onsite: theta angular momenta plus the original free onsite charges. Product physical Fourier cutoffs P_L commute with that onsite symmetry and with the F factor. They do NOT need to commute with the disentangler itself.

Put R_Q=D†(K_Q+H_theta)D and Ω=D†(Ω_Q tensor uniform_theta). Then R_Q>=Delta_0(1−|Ω><Ω|), with Delta_0=min(Delta,1). Below we rename Delta_0 as Delta. A conservative bounded norm is B=2 n_fast R_fast+m, counting all fast modes and all bounded resets, including theta. Increase this bound if the adopted one-body normalization requires it. No full Fock dimension enters.

## 2. Actual Q-canonical Fourier tail

The Q-canonical Gaussian rotation is an explicitly phase-fixed exponential, including the graded conjugate copy. Its covariance is sign(Q h(phi) Q) on the fixed Q space. On each smooth rotor chamber,

 ||partial_j sign(QhQ)||_1 <=2 ||Q(partial_j h)Q||_1/g
                          <=2 ||partial_j h||_1/g.

Thus the canonical many-body vector derivative is bounded by C_G ||partial_j h||_1/g, with conservative C_G=4pi in the adopted Gaussian normalization. Compression to nonlocal Q does not spoil the trace-norm bound: Q is fixed and Schatten compression is contractive. Local rank of partial_j h bounds its trace norm without a total-volume/Fock amplification. The extra constant F dummy block contributes no derivative.

The barycentric texture has a positive normalization floor c_*, finitely many local pair-difference walls, and chamberwise angle derivatives bounded by2pi/c_* in period-one units. The corrected D consists of integer shears, explicit cochain phases and periodic local integer-projector rotations. Pulling back these walls through its bounded-depth circuit gives finitely many slice jumps. Let R_j be their exact local count, including the periodic endpoint, and B_j the chamberwise vector derivative bound, including shear coefficients and local phase/rotation derivatives. These constants are computed from the same fixed local stencil formulas as in the finite-auxiliary theorem, now replacing h by QhQ in the derivative inequality above. Moving walls in spectator coordinates are handled slice by slice almost everywhere.

With m total rotor coordinates and

 A=sum_j(B_j+2R_j)^2/(2pi²),

vector-valued Fourier integration by parts and Parseval give

 tau_N=||(1−P_N)Ω||² <= A/N.

There is no assumption that Ω has finite bare kinetic energy. Its jumps can make that energy infinite.

## 3. New compressed rest gap with an explicit scalar ledger

Let e>0 be the allowed rest-vacuum energy uncertainty, choose integer

 N>=max(1,2A,4BA/e),

and let chi_N=P_NΩ/sqrt(1−tau_N). Then

 <chi_N,R_Q chi_N> <= B tau_N/(1−tau_N) <=e/2.

Define K_rot=sum_j L_j² in the NEW physical onsite frame, not by conjugating an unbounded kinetic operator through D. Choose

 0<kappa<=e/(2mN²).

For every L>=N, define

 R_kappa,L=P_L(R_Q+kappa K_rot)P_L.

By positivity and minmax,

 0<=lambda0(R_kappa,L)<=e,
 lambda1(R_kappa,L)>=Delta,
 gap(R_kappa,L)>=Delta−e.

The same inequalities hold for uncompressed R_Q+kappa K_rot, defined by its closed quadratic form. The trial bound is explicit because <chi_N,K_rot chi_N><=mN². Both rest ground states have overlap squared with Ω at least1−e/Delta. This earns the NEW rest ground/gap; it does not reuse the old reset gap after an unjustified kinetic modification.

At kappa=0 the same ground/gap conclusion holds with energy bound e/2, but the infinite-rank low-energy reset obstruction and divergent thermal trace remain in the uncompressed model. For kappa>0, the finite-volume rest operator has compact resolvent and finite thermal trace by comparison to kappa K_rot. The excited UV spectrum has deliberately changed.

## 4. The actual physical device and the rest theorem now combine

Let H'_device=D†(H_device+H_theta)D. Define the implementable finite auxiliary device

 H_device,kappa,L=P_L H'_device P_L+kappa P_L K_rot P_L.

Compression is norm contractive. Adding precisely the same kinetic term on both sides cancels it from the difference, so

 ||H_device,kappa,L−C_ref I−(H_F tensor I+I tensor R_kappa,L)||<=delta.

This remains valid despite the unbounded uncompressed kinetic term: the difference of the two closed-form Hamiltonians is the ORIGINAL bounded perturbation of norm<=delta, and on the finite cutoff it is an ordinary bounded matrix. No bare-domain invariance of D is used.

This proves that the near finite auxiliary sector is gapped while the exposed free far sector survives, at the paid global resolution. If E_rest=lambda0(R_kappa,L), then E_rest lies in[0,e]. Relative rest excitations cost at least Delta−e. Actual physical eigenvalues differ by at most delta from comparison eigenvalues before further ground-energy alignment. A safe full-device unique-ground criterion is delta<min(p_min,Delta−e)/2, where p_min is the explicit smallest positive free far excitation (if the chosen finite-volume spin structure removes exact zero modes).

For a low-energy threshold below Delta−delta, no excited-rest comparison levels occur. To claim equal spectral-projector ranks, the threshold must additionally be separated by more than delta from the comparison free energies shifted by E_rest. Without computing E_rest, use the certified intervals [E_F_level,E_F_level+e] and choose thresholds outside their delta-neighborhoods. This does not require enumerating all free many-body levels when the target observable/sector supplies a simpler threshold, but arbitrary exponential-spectrum enumeration is not claimed polynomial.

## 5. Offsets, dynamics and useful initial states

C_ref must be a certified numerical scalar if an absolute QPE threshold is requested. Its uncertainty delta_C simply adds to delta in such thresholds. Computing reference fast energies uses the explicit fixed-reference one-body/BdG matrix and its specified normal-ordering constants, not an interacting-ground oracle. The companion integration worker owns the exact sign/offset formula. If C_ref is omitted, the theorem remains about gaps and relative/dynamical quantities only. The additional E_rest is NOT presumed known: either budget its interval width e or separately acquire it.

For any even far observable O_F and any initial density matrix on the finite device, Duhamel gives

 |<O_F(t)>_device−<e^{itH_F}O_F e^{-itH_F}>_same_initial_F_marginal|
 <=2|t|delta ||O_F||.

The scalar C_ref cancels. Because the comparison is an exact tensor sum, no rest-ground oracle is needed for this dynamics statement; even an entangled initial state is covered through its far marginal. For a low-energy prepared input, the explicit state rho_F tensor |chi_N><chi_N| has comparison energy at most E_F+e, and actual energy at most C_ref+E_F+e+delta. A certified polynomial circuit preparing chi_N is an additional interface, now approachable through the canonical controlled Gaussian/grid construction; it must not be confused with Hamiltonian compilation.

For real-time comparison to the uncompressed NEW coercive device, subtract C_ref and use H'_device+kappa K_rot−C_ref >=kappa K_rot−delta. An initial energy expectation <=E therefore gives a conserved kinetic tail bound

 ||(1−P_L)psi(t)||<=sqrt((E+delta)/kappa)/(L+1).

If B_dev bounds the bounded part's norm, the compressed-evolution error is at most

 (2+T B_dev) sqrt((E+delta)/kappa)/(L+1).

This is an energy-capacity theorem for the new coercive model, not uniform approximation of every low-energy state of the original bounded-reset model.

## 6. Resources and remaining scope

For each boundary vertex in the concrete stack, the rotor factor is(2L+1)^3. Total finite Hilbert dimension is2^F(2L+1)^m, and logical qubits are F+m ceil(log2(2L+1)). N,kappa and the dynamical L above have paid polynomial dependence on volume, time, energy and inverse accuracy at fixed microscopic resources. Hamiltonian coefficient/gate compilation uses ../joint_gap/POLYNOMIAL_QUANTUM_TERM_COMPILER.md with its independently audited valid-code, variation and Hermiticity corrections.

The far-device construction needs volume-dependent range and thickness O(log²(n/delta)), with the already enormous Wilson/sign-polynomial constants. The Fourier/kinetic step preserves its spatial support and the actual gaugeable onsite symmetry. This is a finite-volume finite-auxiliary exposed-mode device theorem. It is not a fixed-dimensional thermodynamic regulator, a gauged-continuum theorem, a single-copy undoubling result or a practical simulation estimate.

## Explicit state-vector grid estimate for the low-energy trial
A useful input-state route need not prepare the unknown rest ground. For the explicit normalized pointwise vector Ω(phi), let Ω_S be its value at the center of each tensor-grid cell, held constant throughout that cell. With uniform coordinate bounds B_*=max B_j and R_*=max R_j, coordinate telescoping gives

 ||Ω−Ω_S||_L2 <= m sqrt(4R_*/S+B_*²/S²).

For one coordinate only cells containing a jump contribute the4R_*/S term; all other cells use the derivative bound. The bound is uniform in spectator angles, so replacing other coordinates by their sampled values does not introduce a tensor-product dimension factor. The actual deterministic floor conventions must retain these uniform branch bounds also at grid ties.

Prepare the normalized finite-grid vector S^(−m/2) Σ_grid |phi_grid> Ω(phi_grid) with the explicit controlled Gaussian rotation and corrected D†. A tensor QFT gives discrete Fourier coefficients. Centered-cell integration shows that the continuum Fourier coefficients of Ω_S are those coefficients multiplied by product_j sinc(pi n_j/S). On the retained |n_j|<=N box, the multiplier differs from1 by at most C m N²/S². Consequently the retained discrete vector differs from P_N Ω in norm by at most

 eta_grid = m sqrt(4R_*/S+B_*²/S²)+C mN²/S².

A polynomial S achieves any requested eta_grid. Postselecting the physical cutoff succeeds with probability at least1−tau_N−2eta_grid−eta_grid², and normalization changes the error by only a constant when tau_N,eta_grid are small. Uniform arithmetic/Gaussian-gate errors add directly. The fixed-Q Gaussian and fixed CAR basis have explicit finite one-body data; an audited arithmetic/basis compiler is still required for a final gate statement. The state estimate itself supplies the missing no-exponential-dimension quadrature bound. For a low-energy guarantee, budget normalized state error eta_state so 2(B+kappa mN²)eta_state fits the spare energy allowance. For far-observable response, its trace-distance error simply adds to2T delta.
