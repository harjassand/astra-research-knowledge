# Polynomial preparation of the finite-volume ungauged gapped regulator

2026-11-03. This closes state acquisition for the finite auxiliary Hamiltonian, using its explicit high-overlap trial and the acquired term block encoding. It is not a preparation theorem for a low-energy state of the dynamical gauged theory.

## 1. Known target, gap and trial

Use the actual finite-volume D†-frame regulator from FINITE_AUXILIARY_COERCIVE_REGULATOR.md. Let V_R=H_R+delta I and optionally H_kappa=V_R+kappa sum_j L_j² with the EXPLICIT kappa=e_target/(4mN²). Its finite Fourier compression at L>=N has

 0<=E0<=e_target,  lambda1>=Delta,

and the normalized explicit trial

 chi_N=P_N Omega'/||P_N Omega'||,
 Omega'=D†[W_G(phi)Bell tensor uniform(theta)],

has energy at most e_target. The actual phase-fixed combined-fast Gaussian W_G and the corrected shared-rotor D are already constructed. The unnormalized Omega'(angles) has pointwise norm1. The angle-space amplitude is given by reversible cochain arithmetic, a controlled Gaussian unitary, and the exact integer shear, not an unknown interacting eigenvector.

Let H_alg be the Hermitian charge-pinched compiled Hamiltonian, ||H_alg-P_L H_kappa P_L||<=epsilon_H. Then

 -epsilon_H<=E0_alg<=e_target+epsilon_H,
 lambda1_alg>=Delta-epsilon_H.

Choose e_target<=Delta/8 and epsilon_H<=Delta/16. A known separator E_cut=Delta/2 lies strictly between the unique ground and every excitation. No ground-energy oracle is required.

## 2. Vector-valued Fourier quadrature with no tensor-dimension loss

Write d_N=2N+1. On every coordinate j the actual amplitude Omega' has a uniform slice total-variation bound V_j, including its finitely many cochain/shear/matching walls. The finite-resource note acquires V_j from chamber derivatives and wall counts; at fixed microscopic stack those bounds are independent of total volume. Bounds polynomial in volume would also suffice here.

For one coordinate the n-th Fourier coefficient trapezoid error is at most

 [V_j+2pi N]/S, |n|<=N.

Stacking d_N coefficient vectors gives norm error at most sqrt(d_N)[V_j+2pi N]/S. For all coordinates telescope the continuous/discrete Fourier maps. In EACH difference term, commute the differing coordinate map to act FIRST on the original amplitude. Its error is uniformly bounded for every remaining coordinate value. All remaining Fourier projections, whether continuous or discrete, are contractions in their corresponding normalized L² spaces. Thus

 ||P_N Omega'-v_S|| <= rho_grid,
 rho_grid <= (sqrt(d_N)/S) sum_j[V_j+2pi N].                (1)

There is no d_N^m factor and no assumption of L-infinity-valued bounded variation across moving walls. This proof uses the slice bound before other transforms, not a false assertion that an intermediate transformed function has the same BV norm.

Here v_S is the low-Fourier part of the EXACT sampled grid state after identification with the continuous cutoff basis. A common power-of-two grid S>2N suffices; the shared shear is exactly reversible modulo S. Initial uniform grid amplitudes and unitary coefficient gates ensure exact grid normalization. Equation(1) applies directly to the final D†-transformed amplitude, so no assumption that D preserves the cutoff is made.

## 3. Actual preparation circuit and success probability

1. Allocate all rotor/ancilla grid registers in uniform phase superpositions, and prepare the onsite even Gaussian Bell reference.
2. Given the grid angles, evaluate the actual finite-volume one-body h(phi) reversibly, using exact integer floor decisions. Compute its grouped spectral polynomial and apply the controlled Gaussian purification unitary. A conservative implementation uses a global f_tot-mode quadratic Trotter circuit with f_tot=O(V); its cost is polynomial, even though much larger than a local-patch preparation.
3. Apply the explicitly declared D† circuit: inverse output-matching rotations, corrected cochain phase, and inverse shared integer shear, in the proved order. All integer shears/floor decisions are exact on the common grid. Smooth phases and Gaussian rotations have a separately certified uniform circuit error rho_circ.
4. Apply the inverse phase-grid QFT, test |n_j|<=N for every rotor, and map accepted labels into the physical |n_j|<=L Hamiltonian registers. Use explicit valid-code isometries and reject invalid/padding labels.
5. Compute the TOTAL onsite integer gauge-subgroup charge and retain charge0. This is an exact integer projection, not a continuous-phase approximation and not a local Gauss-law projection.

The exact Omega' is neutral, and P_N commutes with the onsite charge. Let tau_N=||(1-P_N)Omega'||² and rho=rho_grid+rho_circ. Contractivity of the charge0 projection implies that the resulting unnormalized accepted vector differs from P_N Omega' by at most rho. Its success probability is at least

 (sqrt(1-tau_N)-rho)².

After normalization its distance from chi_N is at most 2rho/sqrt(1-tau_N), provided rho<sqrt(1-tau_N). With the already paid small tau_N and, for example, rho<=1/100, success is bounded below by a constant close to1. Repeat-until-success has constant expected repetition count; a prescribed failure probability costs only logarithmically many attempts. There is no exponentially unlikely postselection hidden here.

The total-charge projection removes numerical symmetry leakage. It does not assert a low-energy gauge-field state. The normal-ordering/background convention in the charge arithmetic must be the actually fixed integer convention; if it labels the target by a known q0 rather than0, subtract that known offset before the test.

## 4. No interacting ground-state oracle: a known spectral filter

For the ideal trial chi_N, the energy/gap bounds give ground weight at least

 1-(e_target+2epsilon_H)/(Delta-e_target-2epsilon_H).

The finite grid/circuit normalized error decreases that weight by at most twice the state-norm error. Thus with the choices above the prepared accepted trial has a constant ground overlap bounded safely away from zero; by tightening the existing trial parameters it can be made close to1.

Use the acquired alpha-normalized block encoding of H_alg to perform phase estimation with energy resolution substantially smaller than Delta/4. The known threshold Delta/2 accepts only the ground band. Shift and scale energies using the known norm alpha to avoid phase aliasing. Coherent repetition/median amplification suppresses false acceptance/rejection to eta_f using O(log(1/eta_f)) fixed-resolution phase-estimation repetitions. Each repetition requires total simulated evolution time O(1/Delta), up to fixed safety factors. Controlled Hamiltonian simulation uses the already acquired block encoding and its inverse.

Conditioned on acceptance, the normalized output has excited-state weight O(eta_f/p0), where p0 is the initial constant ground weight. Choose eta_f=O(epsilon_out² p0) for trace/vector error O(epsilon_out). Acceptance probability remains Omega(p0), so preparation succeeds with constant probability and logarithmic repetition overhead. The algorithm discovers no unknown ground energy: the certified interval and threshold above suffice.

The approximate target ground remains in charge0: the exact target is neutral and unique, the compiled operator is exactly charge conserving, and an error smaller than the gap cannot replace it by an orthogonal charge sector without violating the spectral/overlap bound. All accepted physical Hamiltonian blocks preserve the valid cutoff code. Phase-estimation gate errors receive a separate norm budget.

## 5. Explicit polynomial cost

Take

 S >= max(2N+1, C rho_grid^-1 sqrt(2N+1) sum_j[V_j+2pi N]).

This is polynomial in V,N,1/rho_grid. Its quantum register cost is m log S, not S^m. The global one-body polynomial degree is O((R/g)² log(poly(V)/rho_circ)). Reversible dense one-body arithmetic costs O(k f_tot³ poly(bits)), and the deliberately conservative quadratic Trotter preparation costs O(f_tot^7/rho_circ) pair/string gates. The controlled coefficient derivatives/errors are bounded on one-body matrices and unitaries, never by Fock dimension. D† costs polynomially many local integer arithmetic and matching-rotation gates. Total-charge calculation costs polynomial integer additions.

The final filtering uses polynomial(alpha/Delta,log(1/epsilon_out)) queries/gates to the explicitly compiled Hamiltonian oracle. Multiplying by POLYNOMIAL_QUANTUM_TERM_COMPILER.md's per-query cost preserves polynomial dependence on V, the finite cutoffs, inverse requested errors, and inverse certified gap. For the fixed microscopic family Delta is volume independent in the fully gapped test system. If applying a different finite device whose full gap includes a desired far-surface finite-size energy, that smaller proved gap must replace Delta; no constant full gap is silently claimed for an intentionally gapless boundary.

This earns preparation of the UNGAUGED finite-volume gapped regulator (and its explicitly chosen weak-kinetic completion) from simple local reference states. It is not an efficient classical description of its full wavefunction, and not a practical resource claim: the Wilson refinement, spectral condition ratio, patch sizes and conservative Trotter constants remain enormous. It also does not prepare a controlled-energy dynamical-gauge state by merely tree-dressing the output.

Executed small pipeline check: check_trial_ground_filter.py uses one discontinuous rotor and an even-pair two-state Gaussian sector, exact canonical parent, Fourier compression N=3 and kappa=1e-4. It finds cutoff success0.99610, trial ground overlap squared0.999967, compressed gap0.99259, and exactly one eigenstate below the PREDECLARED threshold0.5. Ideal spectral filtering has success0.999967 and fidelity1 to numerical precision. This checks the preparation/filter algebra on a finite toy, not the astronomical Wilson construction; results are in trial_ground_filter_results.json.

## Reference-energy accounting for the open-device variant

The zero-energy bracket in Section1 uses the positive-parent convention H_fast-E0(phi), with its full scalar constant retained. A reference-subtracted open-device Hamiltonian can instead equal C_ref I plus that positive-parent convention. One must NOT use threshold Delta/2 on that Hamiltonian without restoring its energy offset.

The finite-device worker supplies an explicit fixed constant-texture one-body reference and explicit finite compressed rest projection. Compute C_ref by building that finite one-body matrix and summing its negative energies, including both canonical copies, decoration offsets and correct Nambu/BdG factors. This is polynomial classical matrix arithmetic in the finite number of modes; it is not interacting ground-state preparation. A certified sign-trace polynomial gives an absolute trace error bound by the finite one-body dimension times its approximation error, which is allowed in this GLOBAL finite-volume scalar computation. Choose precision so |C_hat-C_ref|<=epsilon_C<=Delta/16 and charge epsilon_C together with epsilon_H in the separator budget. Either subtract C_hat I or use the threshold C_hat+Delta/2. The gap and overlap claims are invariant under this scalar shift. If the chosen reference/projection is not explicitly available, the threshold argument is pending until this acquisition or an independently proved energy-search procedure is supplied.

## Accuracy to the intended compressed Hamiltonian, not only H_alg

Filtering to error epsilon_out produces the ground of H_alg. To identify it with the ground of the intended P_L H_kappa P_L, also pay its eigenvector perturbation. Let g_target>=Delta-e_target be the target gap. Projecting the perturbed ground eigenvalue equation onto the target excited space gives

 sin(angle(ground_alg,ground_target)) <= epsilon_H/(g_target-epsilon_H).

Their phase-aligned vector distance is at most sqrt(2) times that bound. Thus the unqualified final error is epsilon_filter+O(epsilon_H/g_target), not merely epsilon_filter. For an overall requested epsilon_out choose, for example, epsilon_filter<=epsilon_out/2 and epsilon_H<=epsilon_out g_target/16, as well as the previous gap/threshold budgets. These stronger compiler tolerances remain polynomial. Comparison to an infinite-rotor H_kappa ground requires the separate finite-cutoff error budget too; the filter itself does not erase that error.

## Open-device full ground versus gapped-rest preparation

The desired far chiral band has levels BELOW Delta_rest. A threshold Delta_rest/2 therefore does NOT isolate the full device ground and must not be described that way. It can at most exclude rest excitations within a separately certified low-energy window.

For the unique finite OPEN-device ground, use the audited actual full gap g_device=min(Delta_rest,p_min), reduced by the global transfer/compilation error, and choose those errors much smaller than p_min. Replace every separator, overlap and eigenvector-accuracy gap above by this smaller g_device, and use the corresponding acquired C_ref. Include the explicit filled negative-energy far-band Gaussian state in the trial. QPE cost grows as alpha/p_min, still polynomial in volume when the paid AP far-band lower bound is inverse polynomial. This route requires that actual lower bound and trial-charge/reference ledger; the rest-gap theorem alone is insufficient.

Alternatively prepare only the gapped K_Q rest state and a separately specified far Fock state. Then claim the audited approximate initial state and finite-time dynamics under the global-norm transfer, not exact preparation of the full device ground. These two output contracts are distinct.
