# Nonunital thermal products: a legal CP coverage comparator
2026-10-29. Separate constructed extension; independent receiving review pending. No trace-preserving whitening is assumed.

## Thermal channel and explicit self-compatible realization
Let 0<q<1, 0<gamma<=1, eta=1-gamma, and sigma=diag(q,1-q). Define generalized amplitude damping by

 Phi([[p,z],[z*,1-p]])=[[eta p+gamma q,sqrt(eta) z],[sqrt(eta) z*,1-eta p-gamma q]].

It is CPTP and fixes sigma. It is the convex mixture of ground-state amplitude damping with weight q and excited-state amplitude damping with weight1-q. For gamma>=1/2 it is self-compatible by a direct finite construction: with two output qubits B,C and an environment qubit E,

 V|0>=|000>,
 V|1>=sqrt(eta)|100>+sqrt(eta)|010>+sqrt(1-2eta)|001>.

Trace E. Both B,C marginals are ground-state amplitude damping with parameter gamma. Conjugate the input by X and both output qubits by X for the excited-state version, then mix those two broadcast maps with weights q,1-q. This is a full-domain CPTP extension of Phi, not a capacity or implementation assumption.

## Exact CP decomposition preserving the thermal state
Let Delta be energy-basis dephasing, A=1-gamma(1-q), B=1-gamma q, and, for gamma<1,

 alpha=1-sqrt(eta/(AB)).

Since AB=eta+gamma^2 q(1-q)>eta, one has 0<alpha<1. In the unnormalized Choi matrix the only nondiagonal entries are a sqrt(eta) coherence between |00> and |11>; that2×2 block has diagonal A,B. The Choi matrix of Phi Delta is precisely the diagonal of Phi's Choi. Thus J(Phi)-alpha J(Phi Delta) has coherent block

 [[(1-alpha)A,sqrt(eta)],[sqrt(eta),(1-alpha)B]],

which is positive with determinant zero by construction; the other two diagonal entries are nonnegative. Therefore

 R=[Phi-alpha Phi Delta]/(1-alpha)

is CP, trace preserving, and fixes sigma. This is an actual decomposition

 Phi=alpha Gamma Delta+(1-alpha)R, Gamma=Phi,              (T1)

where BOTH Gamma and R preserve sigma. At gamma=1, Phi is the replacement channel sigma and is already EB; set alpha=1 and omit the residual branch. No assertion is made at zero temperature q=0 or1, where this particular alpha vanishes.

For gamma>=1/2,
 alpha=1-sqrt(1-gamma^2 q(1-q)/(AB))
       >=gamma^2 q(1-q)/(2AB)>=q(1-q)/8.                 (T2)

These constants are sufficient, not sharp. At q=1/2 the phase-covariant factor2 theorem is much better than(T2).

## Complete entropy comparator for arbitrarily correlated thermal products
Consider any number of sites with channels Phi_i, stationary sigma_i, and alpha_i from(T1). Let sigma_A=product_i sigma_i, Phi=product_i Phi_i, Delta=product_i Delta_i and alpha*=min_i alpha_i. For arbitrary finite reference R, any faithful omega_R, and arbitrary rho_AR, put tau=sigma_A tensor omega_R. Then

 D(rho||tau)-D((Delta tensor id)rho||tau)
 <=alpha*^(-1)[D(rho||tau)-D((Phi tensor id)rho||tau)].    (T3)

Proof. Expand the product CP decompositions. A branch is Psi_S Delta_S, where Psi_S is a product of local Gamma_i or R_i, and therefore fixes tau. Joint convexity of relative entropy and DPI give

 D((Phi tensor id)rho||tau)<=E_S D((Delta_S tensor id)rho||tau).

The resulting loss f(S)=D(rho||tau)-D(Delta_S rho||tau) equals S(Delta_S rho)-S(rho), because every Delta_i fixes log(tau). This is the same normalized monotone submodular function proved in the main manuscript using binary-unitary Holevo increments and commuting dephasing. Each site belongs to S with probability alpha_i. The fixed-order chain bound gives E f(S)>=alpha* f(all), proving(T3). Correlated input states and quantum references are not replaced by independent states; no independent-output premise is used.

The physical comparator is simply the product energy-basis projective measurement and preparation, not the nonlinear relative-entropy recovery map. Gamma and R are proof devices whose legal CP/TP structure was established explicitly.

## Actual-prior consequence
For any finite ensemble E with barycenter sigma_A, Holevo loss delta=chi(E)-chi(Phi E) obeys

 sum_x p_x T(rho_x,Delta rho_x)<=sqrt(delta/(2alpha*)).    (T4)

The prior may be arbitrarily correlated across sites. Use(T3), average, and the identity D(rho||Delta rho)=S(Delta rho)-S(rho), then Pinsker and Jensen. This applies to a fixed product thermal barycenter; it does not require product ensemble members or independent labels. A complete-reference version follows under a stationary common ensemble barycenter, with consistent reference conditions.

For an arbitrary nonstationary barycenter bar_rho, the visible correction is

 kappa=D(bar_rho||sigma_A)-D(Phi bar_rho||sigma_A)>=0,
 sum p_x T(rho_x,Delta rho_x)<=sqrt[(delta+kappa)/(2alpha*)].

It cannot be silently deleted. This is not the unrestricted N371 delta-only result. Temperatures approaching zero can make the displayed constant diverge, and arbitrary nonfactorable channels are outside this theorem unless a matching CP coverage decomposition is supplied.

## Executed checks and scientific scope
check_thermal.py checks the explicit single-excitation broadcaster,20 thermal Choi decompositions across gamma=.5,.6,.9,.999 and q=.01,.2,.5,.8,.99, and100 correlated two-qubit/reference2 relative-entropy comparisons. Marginal residual<=1.12e-16; worst computed Choi residual eigenvalue -8.33e-17 is floating error around the exact zero eigenvalue. The tests are finite diagnostics; the algebraic proof governs. No native circuit, measured thermal device, new primary algorithm or historical novelty is claimed.

This extension is a concrete response to the N371 nontracial obstruction: known thermal channels admit a reference-preserving CP decomposition, avoiding unphysical congruence/whitening maps. It establishes a size-independent, though temperature-dependent, entropy-loss-to-classicalization law for an explicit nonunital correlated-input class. The remaining challenge is intrinsic nonfactorable or low-temperature dimension-free comparison, not another fitted encoder.
