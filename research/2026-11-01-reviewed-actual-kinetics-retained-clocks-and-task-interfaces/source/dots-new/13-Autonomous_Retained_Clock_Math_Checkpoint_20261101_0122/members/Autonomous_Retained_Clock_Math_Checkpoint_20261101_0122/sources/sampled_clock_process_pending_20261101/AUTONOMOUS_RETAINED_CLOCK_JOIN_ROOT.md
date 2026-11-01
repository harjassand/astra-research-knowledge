# Root theorem join: autonomous internal circulation preserves the retained clock

Status: new joined theorem candidate, independent review pending. This joins exact separately reviewed mechanisms; it does not broaden the executable parser or claim a physical control service.

## Actual model and data to receive

Take the actual original quartic/homogeneous constant-SPD model and symmetric basins of GLOBAL_ODD_MODE_AND_RENEWAL_CANDIDATE.md, with all its positive parameters, coercivity, finite invariant probability pi and raw-model conditions. The reference global mean-zero form has its explicit odd trial psi=2h-1 and full inverse-form bounds, supplying epsilon, k=2/T0, s=pi(S), and C=1/pi(A)=2/(1-s).

Add any fixed smooth compactly supported transverse drift c(y,z), c_y=0, with div(pi*c)=0. Its amplitude may be arbitrary finite and may depend on the model dimension. This is an AUTONOMOUS actual diffusion. Use the compact drift/global form construction from AUTONOMOUS_NEUTRAL_CAPACITY_ROOT.md and its independent receipt. There is no time-varying, observed-state feedback or singular controller initialization hidden in this statement.

A simple explicit subfamily is c=(0,a*phi(y)*chi(U(z))*J*grad U(z)), with finite scalar a, constant skew J, and smooth compact cutoffs phi and chi. It fixes psi and h, is weighted divergence-free, and has compact support by the received coercivity. Other weighted-stream constructions require their own exact admission. Neither arbitrary descriptions of c nor a noisy physical realization are automatically verified.

## The independent joins

1. The common weighted measure and positive contracting actual propagation are earned by the compact drift Lyapunov/closed-form construction. Both chronological orientations have the symmetric reference energy plus a neutral skew term annihilating psi on both sides.

2. The accepted sharp neutral-vector theorem on the global mean-zero space therefore gives

 ||P_t psi-exp(-kt)psi||_L2(pi)
 <=||psi||_2 G(epsilon),
 G(epsilon)=0.5sqrt(epsilon(1+epsilon))+epsilon/EulerNumber.

The scalar correlation differs from exp(-kt) by at most(1/2+1/EulerNumber)epsilon, hence at most epsilon. No reversibility of the ACTUAL processed semigroup is used at this step.

3. The new actual forward committor q, not the old committor, is received by the bounded-domain weak-test/exhaustion argument. It obeys E(q)<=C0=1/(beta Rbarrier), because Ch=0. The actual stationary last-visited label exists. The nonreversible square-reset identity gives stationary transition intensity2E(q)/Ztot<=2C0/Ztot. The conditional last-label law uses the backward committor, but no equality of forward/backward committors is required.

4. For Z=sign(psi), the finite-record entropy proof needs only actual Markov conditional expectations, common invariant measure, the initial density bound C, and the received vector bound. It does not use detailed balance. Likewise the cluster argument needs the actual stationary count upper bound and scalar correlation upper bound, which are now both earned. Thus the original finite-mesh jump-matching proof applies with

 delta=G(epsilon)+2sqrt(s)

in place of sqrt(epsilon)+2sqrt(s), and the same conservative epsilon in the stationary odd-flip bound.

For x=Delta/T0 and n bins, a sufficient failure bound is

 sqrt[C*n*delta^2/(2(1-exp(-4x)))]
 +(C+1)*n*x^2/2 +C*n*epsilon/4 +(5/2)*n*(S_mass/M),

capped at1. On success actual hysteretic flips and a CTMC of flip rate1/T0 have the same count/order/direction, with every paired timestamp within Delta. Rational numerical-rate uncertainty must still be charged using a separately received corollary; the ideal-rate display above does not eliminate it.

## Consequence and limits

At fixed beta,kappa,d0,mu, the supplied epsilon=O(1/alpha) and exponentially small slab mass yield uniform finite-horizon retained-clock convergence over this entire received autonomous circulation class, using x of order epsilon^(1/4). Uniformity is in the mathematical error bound, not in apparatus force, action, implementation, calibration or computational input size.

Every actual return journey is retained; repeated A-to-B outputs consume the intervening B-to-A wait. No angular reset, hidden-state equilibration after entry, or free return is assumed. This is a finite-horizon timestamp-jitter/Skorokhod coupling, not exact iid finite-size waits or total variation of full continuous timestamp laws.

Arbitrary predetermined TIME-DEPENDENT neutral processing already has a different finite-grid/mean receiving, but does not inherit this stationary-count join. It remains outside the present continuous hysteretic theorem. Approximate controllers breaking weighted divergence or task neutrality also remain outside; their errors and energy injection are not absorbed for free.

The accepted Girsanov note prices a mathematical relative-path action proportional to integral c^T D^-1 c, where its assumptions hold. That can grow without bound even when the task-error constant is unchanged. It is not a joule or physical hardware certificate. This theorem alone does not show that an arbitrary useful computation can be implemented by the admitted internal circulation, nor claim a historical first for nonreversible metastability or Markov limits.
