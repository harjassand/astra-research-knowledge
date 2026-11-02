# Robust native thermal memory with an exact local spin environment

2026-11-02. Root integrated theorem, independently internally reviewed under the stated assumptions. This is a theoretical open-region construction with ideal equilibrium endpoints, not practical hardware or arbitrary-noise fault tolerance.

## 1. Precise capability and resources
Start with the actual hierarchical 3D CSS code and the exact native K=7 clock implementation from Delivery82. At sufficiently low fixed nonzero temperature and fixed t/Delta, it has a full-spectrum traced syndrome free energy with positive witness tension. No auxiliary clock is assumed frozen in its vacuum.

The new statement permits generic sufficiently small, fixed local Hamiltonian imperfections and microscopic interactions with a bounded-density local spin environment. The SAME interacting Hamiltonian governs initial equilibrium and all subsequent physical-time storage. No Davies limit, adjustable frequency resolution, refreshed reservoir, or time-dependent correction is invoked.

Native code hardware consists of data qubits and seven-level clock spins, geometrically local onsite/two-body terms, bounded degree/density/range, and fixed strengths. Perturbations may be generic native two-body terms; the proof actually permits bounded-body finite-range terms of bounded local incidence. After the fixed bounded-depth U they have a larger but still fixed support. This is not a qubit-only or restricted-exchange implementation.

Let n denote native memory size, including clocks (within a fixed factor of data size). The environment is any finite set of bounded-dimensional spins in the same bounded-density geometry, with bounded onsite H_B0. Let

 H_tot=H_nat+H_B0+V.

V may contain memory/clock calibration errors, memory–bath contacts and bath–bath interactions. Its local interaction strength is at most v_*; all support, decomposition and overlap constants are fixed. Bath-only interactions are small parts of V, not arbitrary uncharged interacting reference terms. The sum of norms of terms touching native memory is at most v n. Constants are independent of n and bath volume.

Fix a compact finite inverse-temperature interval with strict original witness/rod margins. There exists a positive v_* independent of volume for which the conclusion holds. The open region is within this fixed local-dimension, geometry, range/body and local-strength parameter class. Its sufficient value can be fantastically small; no realistic engineering tolerance is claimed. The threshold need not be uniform as beta tends to infinity.

## 2. The new static construction
In the fixed dressed frame H_ref=H_anc(S)+H_B0 commutes exactly with the original full-space decoder logical algebra. Expand U†VU into bounded-support data Paulis times clock/bath matrix units, with explicitly bounded coefficient overhead.

The used perturbation labels form compound sources. Each source owns COMPLETE imaginary-time paths on every clock/bath column it touches, including all checks meeting its expanded data support. Exterior clocks remain the exact ordinary/wrapping rod gas. Compatible sources have disjoint marked supports and must close their data syndrome separately. A source with m distinct labels has data word weight at most b_D m, regardless of repeated events. Below code distance it is a stabilizer, with a syndrome dependence neighborhood supplied by the previously proved polynomial filling theorem.

Native clock trajectory interactions are scalar pair signs of modulus at most one. Arbitrary matrix-unit insertions are internal to owned columns. The exact source measure has an absolute bound

 q(v)^m,
 q(v)=K^(b_c) d_B^(b_B) exp(2 beta t b_c)[exp(beta C_local v)-1],

up to stated fixed decomposition constants. The exponential penalty charges full unrestricted clock histories; it is not silently discarded. Identity constants and shared-label exclusion are handled explicitly. No point-event replacement of a syndrome-changing interval is used.

The mixed source/rod gas satisfies a simultaneous KP criterion at sufficiently small fixed v. An exact event-count majorant gives O(v) local syndrome influence, while source footprints and winding-rod roots account for every syndrome character. Remote free energy cancels through the convergent scalar gas. The scalar background keeps memory-touching sources only for m<d_n/b_D and all bath-only sources. ALL larger memory-touching sources, even accidentally scalar ones, are exceptional and yield only a relative matrix remainder

 r_n<=exp[C n lambda^(d_n/b_D)]-1,  lambda<1,

uniformly in bath volume. Large bath-only sources remain in the scalar background. The normalization uses a proved pinned signed-gas ratio, not an unproved operator-log theorem or a global exp(beta*n*v) estimate.

Governing files: EXACT_MIXED_SOURCE_ROD_FACTORIZATION.md; thermal_perturbation/MIXED_GAS_ANALYTIC_CONSUMER.md; thermal_perturbation/PINNED_SIGNED_GAS_RATIO_LEMMA.md. The independently derived Schatten-Hölder history bound is retained as additional machinery, not a substitute for the exact component factorization.

## 3. Actual positive Gibbs witness bound
Let W_V(s) be the trace of the ACTUAL Gibbs operator in data syndrome s after U. The scalar reference free energy is F_0(s) from Delivery82, with

 F_0(s)=c-J0 sum_g s_g+R_0(s),
 sup_g sum_(A contains g)|r_A|<=epsilon_0 J0, epsilon_0<1.

The mixed gas gives, for valid s,s' differing on D and sufficiently large n with r_n<=1/2,

 |log[W_V(s)/W_V(s')]+beta[F_0(s)-F_0(s')]|
 <=Lambda_beta(v)|D|+4r_n,

where Lambda_beta(v)=O(v), with fixed-temperature constants independent of memory and bath volume. Positivity here is positivity of actual projected Gibbs traces; an intermediate signed scalar gas need not be treated as a probability law.

For the actual source's removable witness tau contained in the occupied syndrome, the ratio is at most

 exp[-(2beta J0(1-epsilon_0)-Lambda_beta(v))*|tau|+4r_n].

Choose v_* so the reduced tension stays above the actual source's strict Peierls threshold. Condition on the other CSS syndrome rather than assuming X/Z statistical factorization. The existing injective witness surgery and entropy count then yield

 p_1(n)<=poly(n) exp(-c n^eta).

The actual polynomial distance ensures r_n tends to zero, without an extensive bath-volume penalty. General syndrome-translation ratios allow the good set to be shrunk by every Pauli prefix on every enlarged local perturbation footprint. This costs only a polynomial prefactor and fixed constants. Let the resulting projector be P_good, P_bad=I-P_good. For the true joint Gibbs state rho_beta,

 p(n)=Tr(P_bad rho_beta)<=poly(n) exp(-c n^eta).

All projectors and logical observables are understood in the fixed dressed frame, or conjugated back by U in native coordinates.

## 4. Fixed decoder algebra and actual physical-time storage
Let Q_X,Q_Y,Q_Z be the original decoder's exact full-space logical Pauli algebra. Then [H_ref,Q_mu]=0. The enlarged good-set admission ensures

 [Q_mu,V_j] P_good=0

for every actual memory-touching interaction term, including arbitrary bath coefficients. Hermiticity makes the commutator supported on P_bad on BOTH sides. This is stronger than merely asserting local support.

Use the previously independently reviewed thermal logical-twirl argument. Relative entropy and Pinsker give

 delta_tw=||rho_bar-rho_beta||_1<=2 sqrt(beta v n p(n)),
 rho_bar=I_L/2 tensor tau_GB.

Initialize the ACTUAL interacting Gibbs state and coherently overwrite its fixed decoded logical qubit with any incoming input xi_LR initially independent of the supplied joint Gibbs state, retaining the joint gauge/clock/bath marginal tau_GB. This ideal operation can be defined without knowing V once the actual equilibrium state is supplied. It is not an efficient physical thermalizer or noisy encoder theorem.

The encoded system marginal is at most 2rho_bar. Exact unitary evolution under H_tot preserves rho_beta, hence for ALL physical times,

 Tr[P_bad rho_MB(t)]<=2p(n)+delta_tw.

The reference-safe decoded channel obeys

 error(T)<=min{2,6 v n T [2p(n)+2sqrt(beta v n p(n))]}.

Thus for a sufficiently reduced positive exponent, stretched-exponential physical storage time has vanishing logical error. The environment volume does not enter the memory-touching norm budget. No Markov, secular, rotating-wave, or weak-coupling time-limit approximation is used in this conclusion.

## 5. What was actually removed, and what remains
This extends the exact native Hamiltonian construction to an open fixed-temperature region of generic local Hamiltonians and weak microscopic spin-environment couplings. It removes exact calibration and fully secular bath modeling as mandatory assumptions of that theoretical retention result.

It does NOT remove the ideal actual-Gibbs initialization and ideal terminal decoding, including clock access. It does not cover arbitrary nonequilibrium noise, controls injecting uncharged energy, arbitrary strong/interacting bath references, unbounded-dimensional bosonic reservoirs, or time-dependent adversarial perturbations. It is not an infinite-temperature or zero-temperature-uniform statement. Clock dimensions and allowed interactions remain explicit. Sufficient code and perturbation constants can be prohibitive; the result is not a practical quantum hard drive.

A minimal two-qubit example in bath_gate documents why robustness cannot simply be inferred by continuity of a fully secular Davies generator. That example is an order-of-limits warning, not a no-go for the native code or finite-coupling physical dynamics. The exact joint-equilibrium consumer avoids that inference.

## 6. Prior machinery and scientific judgment
The native clock mechanism, signed continuum cluster theorem, original 3D code, and thermal logical criterion are credited in Delivery82 and the attached dependency proofs. Ocko–Yoshida and HPWL are serious native-interaction comparators, not straw alternatives. The present new construction is the full-column generic-perturbation representation, its normalized local Gibbs control, and the resulting binding of the native model to the already-earned exact-environment consumer. Historical novelty beyond this scoped comparison has not been established.

The north-star connection is a stable physical principle for reliable quantum information, with an actual many-body implementation obstacle removed. A proof with fixed but extreme constants is protected intermediate work; it is not sufficient evidence of a civilisation-changing usable device. The next consequence gate should address an indispensable physical resource or a stronger foundational implication, rather than simply widening an already expensive model catalogue.
