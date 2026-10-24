# Observable frames connect localization to acoustic transport

The nonlocal kernel exposes a distinction between keeping masses within a cell together and controlling the motion between cells. This note gives a kinematic transport/fluctuation principle that uses a complete local displacement frame. It removes the rank-one, stiffness-budget and interaction-reach premises, at the cost of acquiring an additional intercell displacement bound. Earlier proofs remain unchanged.

## 1. General harmonic statement

Let D(q) be the finite-dimensional mass-normalized Hermitian Bloch dynamical matrix of a stable periodic harmonic system. It is analytic in q, has real mechanical time reversal D(-q)=D(q)^*, and has d>=1 zero eigenvalues at q=0. Positive-frequency normal modes have ordinary Gibbs covariance

c_T(omega)=hbar/(2omega)coth[omega/(2theta)],
theta=k_B T/hbar.

Fix any exact global zero modes on a finite ring and assume the local observables below have a finite thermodynamic Gibbs covariance in the specified physical frame. This is a genuine condition on those observables, not supplied by mere mechanical stability.

Define

a=max_q sqrt(lambda_min D(q)).

Suppose a collection of specified local linear displacement observables has a nonnegative quadratic form A(q) in mass-normalized mode coordinates. Suppose on a wave-number set S of normalized measure p>0 it obeys the frame inequality

v^* A(q) v>=alpha ||v||^2 for ALL v,
alpha>0,

and its equilibrium quadratic expectation is at most B. Then

B>=p alpha c_T(a),
a tanh[a/(2theta)]>=hbar p alpha/(2B).

Let rho_T solve rho_T tanh[rho_T/(2theta)]=hbar p alpha/(2B). The complete intrinsic right-moving channel count satisfies

J>=d integral_0^(rho_T) g_theta(omega)domega,
J/(d J_Q)>=1-Tail[rho_T/(2theta)],
J_Q=pi^2theta/3.

The constants p,alpha,B are actual properties/budgets of the observable frame. They are not free sensing or actuator assumptions. An observable family with a blind soft subspace may have alpha=0 and gives no such conclusion.

## 2. Proof: covariance and full channel counting

At every q a normalized lowest eigenmode has frequency at most a. On S, its contribution to the quadratic Gibbs expectation is at least alpha c_T(a), because c_T decreases. All other modal contributions are nonnegative. Integrating proves B>=p alpha c_T(a), and rearranging proves the cutoff inequality.

The multiplicity d in the conductance bound follows from spectral flow, not from labelling generic polarizations. Choose q_* in[0,pi] where lambda_min D(q_*)=a^2; time reversal permits this half-zone choice. At q_* ALL eigenvalues are at least a^2. For almost every0<omega<a, the number of eigenvalues below omega^2 is at least d at q=0 and zero at q=q_*. Along that path the net number of upward crossings of omega^2 is therefore at least d. Upward frequency crossings have positive group velocity, so the complete channel count has at least d right-moving modes at that omega. Critical frequencies and flat-band values are a null set; repeated analytic branches count with their multiplicity. Thus N_ch(omega)>=d almost everywhere on(0,a).

This argument keeps every nonmonotone and overlapping branch. Positivity of individual springs, a monotone pencil, a unique backbone, and a uniform bound on the interaction length were not used. What matters is a stable harmonic Bloch spectrum, its acoustic zero modes, the actual covariance frame inequality, and ideal intrinsic transport.

## 3. A concrete scalar displacement frame

Take arbitrary positive scalar point masses m_j in a cell, total M, with any stable time-reversal-symmetric harmonic interactions of finite reach per design. Pick one coordinate b as reference and define the physical local observables

r_j(l)=x_j(l)-x_b(l),
t(l)=x_b(l+1)-x_b(l).

Assume TOTAL quantum Gibbs variances of EVERY r_j and of t are at most d_0^2. Here d_0 is a displacement range, unrelated to the acoustic-zero count d above.

For a mass-normalized mode represented by physical x with sum m_j|x_j|^2=1, put

F_q(x)=sum_j m_j|x_j-x_b|^2
       +(M/2)|exp(iq)-1|^2|x_b|^2.

On the half-zone |q|>=pi/2,

1=||x||_Mass
 <=sqrt(M)|x_b|+||x-x_b1||_Mass
 <=sqrt(M/2)|(exp(iq)-1)x_b|+||x-x_b1||_Mass
 <=sqrt[2F_q(x)].

Therefore this observable family has p=1/2 and alpha=1/2. Its Gibbs quadratic expectation is bounded by

B<=M d_0^2+(M/2)d_0^2=3M d_0^2/2.

The general theorem gives the explicit fully quantum bound

a tanh[a/(2theta)]>=hbar/(12M d_0^2),
a>=hbar/(12M d_0^2).

There is no K_aff, K_eff, backbone-mass-floor or link-length threshold. In a classical Gibbs model the corresponding covariance argument instead gives

a^2>=k_B T/(6M d_0^2).

For scalar connected cells d=1. The quantum possible deficit below the intrinsic acoustic quantum is bounded by Tail[hbar/(24M d_0^2 theta)] and hence is exponentially small in1/T at fixed M,d_0. Extra channels can increase conductance, so equality with one quantum is not asserted for arbitrary retuned graphs.

## 4. Vector coordinates require an actual vector range cap

The same norm argument works for vector positions if the caps are on the full Euclidean relative displacement,

E||x_j-x_b||^2<=d_0^2,
E||x_b(l+1)-x_b(l)||^2<=d_0^2,

with scalar masses weighting all components. These expressions are invariant under a fixed orthogonal change of spatial coordinates. They control displacement in the chosen physical reference frame, not just strain or relative orientation.

If D(0) has d independent acoustic zeros, the spectral-flow proof in Section2 supplies the d-fold channel coverage under this SAME genuine frame cap. This does not assign a vector cap to an ordinary free beam by assumption. Torsional or rotational Goldstone fields can give divergent within-cell laboratory displacement variance even after global translation is removed; fixing a global orientation does not in general remove the thermodynamic fluctuation. In that case the stated cap fails and this theorem gives no finite localization bound. A local strain cap is not automatically a bound on these vector observables.

## 5. An attaining resource order and the Fejer boundary

QUANTUM_COST_ATTAINABILITY.md constructs a passive one-pendant family with fixed mass ratio R, M=Q_M/T, spring k=4mu_red theta^2a_0^2 and constant nonzero fractional heat suppression. It has a fixed bound on the within-cell relative variance. It can satisfy the additional adjacent-reference cap too.

For this family's backbone link t, static compliance on an N-cell periodic ring is(N-1)/(NK), tending to1/K. Its mass-normalized force-pair norm squared is2/m. The covariance upper bound coth x<=1+1/x and spectral Cauchy-Schwarz therefore give

Var(t)<=k_B T/K+(hbar/2)sqrt[2/(mK)].

With m=Q_M/(RT), this tends to0 as T tends to0. Therefore the actual mass-proportional-to1/T construction meets BOTH types of range cap at sufficiently small T while retaining finite fractional suppression. The necessary M T d_0^2 resource order is thus attained; no claim about optimal constants follows.

The positive Fejer kernel in NONLOCAL_KERNEL_CONSTRUCTION.md has no within-cell r_j but its adjacent-reference variance grows at least as hbar/(M Omega_N). That is exactly the missing observable t. It therefore does not evade this frame theorem. It does evade a contract that gives unbounded interaction reach and prices only K_eff,M and an empty within-cell range budget.

This identifies which physical information changes the design conclusion. A real structure must acquire an appropriate displacement/strain-frame bound; the theorem does not grant it. Conversely, a conventional network that actually pays increased moving mass or displacement range can use the same positive construction.

## Scope and conventional explanation

The oscillator covariance, uncertainty/localization ingredient and Landauer channel count are established. The added result is a uniform statement over changing harmonic graphs and their retunings, conditional on a counted observable frame. It is consistent with the Lindemann/quantum-stability ancestry examined in MELTING_COMPARATOR.md. Historical priority remains UNKNOWN.

The theorem concerns intrinsic periodic harmonic transport. It does not rule out thermal insulation by contact reflection, disorder, dissipation with additional reservoirs, anharmonic scattering or other operations outside this contract. No material-frame range, finite-contact transmission or fabricated device has been supplied by the proof.
