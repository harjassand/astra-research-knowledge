# Local noisy factories: exact geometry, robust compilation and sharp boundaries

Research note, 2026-11-05. Convex reachability and channel inversion are standard; the useful deduction is an explicit actual-apparatus interface for a constructive many-body ensemble sampler. The conditions below preserve the final physical noise and do not assert unrestricted acquisition.

## 1. Exact local range and an attaining routine

Six actual local settings j=(a,s), a in {x,y,z}, s in {+,-}, output sigma_j=(I+v_j.sigma)/2. Each complete routine includes final reset, selector, switching, preparation and delivery noise. Independent fresh noise and no unmodeled memory are assumed. Classical randomization attains exactly the Bloch polytope P=conv{v_j}.

All radius-r Pauli states (I +/- r sigma_a)/2 are reachable exactly iff every +/-r e_a belongs to P. Six linear programs find the setting distributions, or certify failure by a separating hyperplane. This distinguishes positivity of a formal inverse from an implementable local mixture.

If ||v_(a,s)-s e_a||_2<=delta, then

(1-sqrt(3) delta) O subset P,

where O=conv{+/-e_x,+/-e_y,+/-e_z} is the unit octahedron. Proof: h_P(u)>=||u||_infinity-delta||u||_2>=(1-sqrt(3)delta)||u||_infinity. Support-function domination gives the inclusion. This allows asymmetric, biased and nonunital perturbations as long as the actual measured vertices obey the bound.

For an invertible affine qubit map v -> A v+t applied after ideal Pauli settings, P=t+A O. The exact radius criterion is

max_(a,s) ||A^(-1)(s r e_a-t)||_1 <=1.

For isotropic contraction kappa this gives r<=kappa, sharply. For amplitude damping gamma it gives r<=1-2gamma when 0<=gamma<=1/2. If gamma>1/2 then even the origin is outside the full output ellipsoid, so I/2 cannot be produced from any input under that final channel.

## 2. Smooth positive rational compiler

Let V_0=[e_x,-e_x,e_y,-e_y,e_z,-e_z], B=V_0^T/2 and u=(1/6,...,1/6)^T. Given target x=r v_(0,j), set

w^0=r e_j+(1-r)u,      A=VB,
w=w^0+B A^(-1)(x-Vw^0).

Then 1^T w=1 and Vw=x. Indeed 1^T B=0 and VB=A. Also V_0B=I. If each column perturbation has norm <=delta, then

||A-I||_2 <=sqrt(3)delta,
|w_k-w^0_k| <= delta/[2(1-sqrt(3)delta)].

The first bound follows from ||V-V_0||_2<=sqrt(6)delta and ||B||_2=1/sqrt(2). For the second, ||x-Vw^0||_2=||(V_0-V)w^0||_2<=delta because w^0 is a distribution, and each row of B has norm 1/2.

Consequently every weight is positive whenever

delta/[2(1-sqrt(3)delta)] < (1-r)/6.

For r=1/2 and delta<=1/32 the minimum weight is greater than 0.066. The formula is rational in the actual Bloch vectors and strictly positive on a neighborhood. If those vectors are rational functions of finitely many observable physical assay probabilities, the separate positive-rational sampler implements it with fresh probes and only logarithmic accuracy overhead. This last observable-oracle condition is substantive, not supplied by the formula.

## 3. Independent local factories cannot produce entangled targets

Any operation that only classically correlates independent one-site output routines produces a fully separable state. No amount of precision in classical mixture weights removes this boundary.

Consider M disjoint qubit dimers with H=-J sum_l Phi_l, where Phi is a maximally entangled rank-one projector. Each thermal pair is

rho_t=(1-t)I/4+t Phi,
t=(exp(beta J)-1)/(exp(beta J)+3).

Its Phi probability is F=(1+3t)/4. Every product state on a pair has Phi overlap <=1/2. Thus for beta J>log 3, no one-site factory can attain even a single pair. Measuring each disjoint Phi projector yields independent Bernoulli outcomes inside each product component, each with mean <=1/2. Mixing components preserves stochastic domination by Bin(M,1/2). The target gives Bin(M,F). Thresholding at M(F+1/2)/2 and applying Hoeffding gives

inf_(sigma fully separable) (1/2)||sigma-rho_t^(tensor M)||_1
  >= 1-2 exp[-M(F-1/2)^2/2].

The global error approaches one exponentially at fixed temperature below this threshold, although every Hamiltonian term is local and commuting across dimers. This is a physical capability boundary, not a computational hardness statement.

## 4. Exact two-qubit depolarizing floor, and attainment

Use the singlet projector Psi^- for a Heisenberg dimer and write

rho_t=(1-t)I/4+t Psi^-,       0<=t<=1.

Let each final qubit undergo depolarization D_lambda with Bloch contraction 0<=lambda<=1. Then for arbitrary two-qubit input sigma,

min_sigma (1/2)||rho_t-(D_lambda tensor D_lambda)(sigma)||_1
   = (3/4) (t-lambda^2)_+.                                (5)

Proof: the U tensor U twirl T fixes rho_t, commutes with the two equal depolarizers and contracts trace distance. Therefore an optimum may be taken Werner, sigma=rho_s with -1/3<=s<=1. The final state is rho_(lambda^2 s). Since

(1/2)||rho_t-rho_u||_1=(3/4)|t-u|,

the closest reachable parameter is u=min(t,lambda^2). If t<=lambda^2 and lambda>0, the attaining preimage is rho_(t/lambda^2). If t>lambda^2, a singlet input attains the floor. If lambda=0 the sole output is I/4. The statement also holds for isotropic Phi states using U tensor conjugate-U twirling.

This is sharper than an inverse-positivity test because it gives the exact best achievable error even allowing arbitrary entangled input, quantum computation, cooling and optimal precompensation before the compulsory terminal channels. It remains a terminal-channel model; active protection after or replacement of that channel changes the problem.

For H=J(X X+Y Y+Z Z), J>0, the singlet energy is -3J and each triplet energy J. Thus

t=(exp(4 beta J)-1)/(exp(4 beta J)+3).

Exact delivery under the terminal depolarizers is possible precisely when t<=lambda^2, equivalent for lambda<1 to

4 beta J <= log[(1+3lambda^2)/(1-lambda^2)].

The state rho_(t/lambda^2) can be prepared as singlet with probability t/lambda^2 and maximally mixed otherwise (for t>=0). This requires a paid actual entangling two-qubit factory or the already earned finite noisy interface; one-site product factories cannot implement it in the entangled region. A fully ideal singlet generator is not silently supplied by the attaining mathematical input.

For any terminal channel K and observable H, the minimum delivered energy is lambda_min(K^*(H)), attained by a ground state of K^*(H). This elementary convex-duality identity is useful for choosing a task weaker than full-state accuracy. For transverse-field Ising H and product Pauli channels, K^* rescales local fields and bonds and preserves the free-fermion class. The endpoint energy optimum is thus constructively accessible with the same paid preparation controls, while full Gibbs delivery need not be.

## 5. Scope and comparators

Quantum error pre-compensation (https://arxiv.org/pdf/2309.01434) already provides general inverse-positivity and optimization viewpoints. No claim is made that the convex-range criterion, the affine inverse or twirling is new. Their combined use specifies exactly what an actual noisy local factory must supply to support an independently earned constructive interacting-state sampler, and identifies temperatures and tasks it cannot cover. A comparison may grant the same sampler, classical machinery and terminal channels to any stronger active method.

An arbitrary simultaneous rotation of all preparation and meter axes is observationally invisible internally. Hence the physical target must use an identifiable control frame, and unknown arbitrary SPAM is not solved by local convex geometry. Model validation, acquisition, record reset, independent refresh, detector costs and any entangling control remain charged. No practical resource advantage is inferred from polynomial dependence with unfavorable constants.
