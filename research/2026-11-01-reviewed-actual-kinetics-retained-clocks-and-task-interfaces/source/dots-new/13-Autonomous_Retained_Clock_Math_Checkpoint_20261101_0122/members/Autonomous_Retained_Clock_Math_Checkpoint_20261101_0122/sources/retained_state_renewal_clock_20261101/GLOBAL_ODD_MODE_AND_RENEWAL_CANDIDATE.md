# Reusable alternating rare-event clocks without angular reset

Status: new theorem candidate. The old one-passage results do NOT imply this
statement by renewal assumption. This file earns a global odd inverse form,
a finite-record comparison, a stationary transition-count identity, and a
cluster-to-continuous-path join. No executable or physical instrument is yet
received. Earlier freezes remain unchanged.

## 1. Actual task and class

Use the same ordinary reversible diffusion on R^(1+m):

 dY=-v'(Y)U(Z)dt+sqrt(2/beta)dW,
 dZ=-v(Y)M_z grad U(Z)dt+sqrt(2M_z/beta)dB,
 v(y)=1+kappa(1-y^2)^2.

Here m=4alpha, integer alpha>=4, beta,kappa,d0,mu>0,
U is a homogeneous quartic with U(z)>=d0||z||^4/m, and finite constant SPD
M_z>=mu I. The actual model has unit longitudinal mobility and zero cross
mobility. The already received positive-quartic raw program is an acquired
subclass; a generic unknown U does not automatically have a coercivity oracle.

Let A={y<=-1/2}, B={y>=1/2}, S={|y|<1/2}. Prepare the actual FULL Gibbs|A law
ONCE, as a mathematical initial-law premise. Do not reset or thermalize Z at
subsequent times. Define tau_1=first B hit, tau_2=first A hit after tau_1, and
then alternate. The actual clock label H_t is +1 until tau_1, -1 until tau_2,
etc. All return journeys and slab travel consume wall-clock time. There is no
added settling operation or claim that an entrance distribution equals Gibbs.

The target is a coupling on a specified finite horizon with the symmetric
continuous-time two-state chain, flip rate1/T0. Successful coupling means the
same number/order of hysteretic jumps, each timestamp within a specified mesh
Delta. It is NOT total variation of continuous timestamp vectors and NOT the
raw continuously observed sign of Y (which chatters near zero).

Normalize only the unknown transverse partition:
Z_U=int exp(-beta U)dz, w=exp(-beta vU)/Z_U, q(y)=v(y)^-alpha.
Then M=int_A w=int_(1/2)^infinity q, S0=int_S w, Ztot=2M+S0,
R=int_S q^-1, pi=w/Ztot, eta=S0/M, s=S0/Ztot, C=Ztot/M=2+eta.
Set T0=beta M R, lambda=1/T0 and k=2lambda.
The global diffusion and finite invariant law are already earned, not formal.
Its positive heat kernels/irreducibility make pi ergodic. Spectral gaps may be
zero. All following scalar quantities use the SAME unnormalized scale w.

## 2. The explicit global odd source, not a killed inverse transplant

Let h=1 on A,0 on B and h(y)=R^-1 int_y^(1/2)q(t)^-1dt in S. It is explicit
from the acquired scalar profile; no actual committor is computed. Put
psi=2h-1. Then psi(-y,z)=-psi(y,z), |psi|<=1, and

 2M<=N:=int psi^2 w<=Ztot, int psi w=0,
 E(psi)=4/(beta R).                                      (1)

Let f=1A-1B and r=psi-f. The new inverse operator is K=-L on the global
mean-zero subspace, not the old process killed on B.

Use the accepted well-current on the LEFT half-space y<0. Its normal flux at
0 is M*pi_(v*), v*=1+kappa, and its transverse component there is zero.
Reflect it to y>0 by keeping its longitudinal component and changing the sign
of its transverse component. Density and block mobility are invariant under
y->-y. The reflected divergence is -w1B; matching normal traces at0 create
no surface source. Thus the full current has distributional divergence w*f.
Its energy bound is

 B_f=beta[M^2 Rplus+2E_rest],
 Rplus=int_S [v*^2/(2v*-v)]^alpha,                       (2)

where E_rest is the explicit nominal non-slab bound from the received well
proof, WITHOUT beta:

 a=1+9kappa/16, d=1/alpha,
 G1=v*^2/(2v*-1), Gb=v*^2/(2v*-a),
 K0=alpha/[8mu sqrt(beta d0)],
 Dmax=4alpha max(kappa,1)/[mu sqrt(beta d0)],
 C_s=kappa/[2mu sqrt(beta d0)*a^(3/2)],
 E_rest=M^2(1/2+d)Gb^alpha
 +[v*^2/(128kappa^2(alpha-1)^2d^2)+K0*kappa^2]G1^alpha
 +(1+Dmax)/(16kappa^2(alpha-1)^2).

The slab price is counted ONCE and each well price TWICE. This distinction is
essential; the original killed A-source bound cannot simply be reused globally.

The residual r is supported in S, odd, nonnegative on its left half and bounded
by1 in magnitude. J_r(y)=int_(-1/2)^y q(t)r(t)dt in S and0 outside satisfies
0<=J_r<=S0/2 and returns to zero at the right boundary. The explicitly received
conditional dilation current J_r*pi_v*(1,-v'z/(4v)) has divergence wr and
energy at most

 B_r=beta(S0/2)^2 R(1+C_s).                             (3)

Normal traces vanish at both boundaries. The existing weighted slab integration
inequality supplies C_s; no generic pointwise slab bound replaces it.

Both sources have zero full-space mean. Finite current energy bounds their
compact-core energy functionals by Cauchy. Positive resolvent/exhaustion (or
the spectral variational identity on the mean-zero space) then gives finite
GLOBAL inverse forms Q_f<=B_f,Q_r<=B_r. Constants are the only zero modes and
are orthogonal to these sources. Infinity is controlled by the already finite
full well-current energy, not an assumed pointwise flux limit. Consequently

 Q_psi=||K^-1/2 psi||^2 <=(sqrt(B_f)+sqrt(B_r))^2
       <=beta M^2 R(1+epsilon),                        (4)

where a convenient completely scalar choice is

 b_f=B_f/(beta M^2 R),
 1+epsilon=(1+eta/2)[b_f+(eta/2)(1+C_s)].               (5)

This is weighted Cauchy, not an unproved common-source bound. Since Rplus>=R,
epsilon>=0. The accepted asymptotics show epsilon->0 uniformly over the class
at fixed beta,kappa,d0,mu, with epsilon=3/(4alpha)+O(alpha^-2) plus exponentially
small terms. The coefficient describes this witness, not actual kinetic error.

## 3. A whole-vector slow mode

Let e=psi/sqrt(N). The spectral probability of K relative to e, scaled by k,
has X=K/k with

 E X=E(psi)/(kN)=2M/N<=1,
 E(1/X)=k Q_psi/N<=1+epsilon.

The previously received scalar spectral lemma therefore gives

 exp(-kt)<=c(t):=<e,P_t e><=exp(-kt)+epsilon.

Self-adjointness upgrades it to the WHOLE vector estimate

 ||P_t e-exp(-kt)e||^2
   =c(2t)-2exp(-kt)c(t)+exp(-2kt)<=epsilon.             (6)

No gap, hidden-mode basis, committor oracle or angular mixing bound is used.
The reference k=2/T0 is a correlation decay; the two-state FLIP rate is k/2.
Other independently received stronger vector lemmas may improve constants,
but(6) alone is sufficient for every theorem in this file.

For the total binary partition Z(y)=+1 on y<=0,-1 on y>0, the only difference
from psi lies in S, with |Z-psi|<=1. In L2(pi), for r_t=exp(-kt),

 ||P_t Z-r_t Z|| <=sqrt(epsilon)+(1+r_t)sqrt(s)
                  <=delta:=sqrt(epsilon)+2sqrt(s).     (7)

This proves a task-specific approximate invariant observable, not a Markov
property of the full projected coordinate or its derivatives.

## 4. Entire sampled records with retained state

Observe at deterministic times t_0=0<...<t_n. Let the reference chain have
transition Q_i(z,z')=(1+r_i zz')/2, r_i=exp[-k(t_i-t_(i-1))], starting +1.
The actual Gibbs|A initial density relative to pi is1A/pi(A)<=C. Positivity and
invariance preserve that upper bound at EVERY deterministic later time.

For a complete observed past, the next actual Bernoulli probability differs
from Q_i by the conditional expectation of
(P_(Delta_i) Z-r_i Z)/2. Bernoulli relative entropy is at most the squared
probability difference divided by Q_i(+)(1-Q_i(+))=(1-r_i^2)/4. Conditional
Jensen, then the density bound, and the entropy chain rule give

 KL(actual sign record || reference record)
       <=C sum_i ||P_(Delta_i)Z-r_i Z||_L2(pi)^2/(1-r_i^2).

Pinsker yields

 TV_sign<=sqrt[(C/2) sum_i delta_i^2/(1-r_i^2)],        (8)
 delta_i=sqrt(epsilon)+(1+r_i)sqrt(s).

There is no2^n word union. The proof is also valid for the joint law with an
initial nonanticipating classical record R0 generated conditionally on X0:
condition the entropy chain rule on R0 (even X0 itself), and the unconditional
marginal bound is unchanged. The comparison record is independent of R0. This
is an averaged joint-law statement with the fixed Gibbs|A marginal, not a
uniform guarantee after selecting an arbitrarily rare initial state/history.
Future noise must be independent of R0 given X0; no feedback acts on the model.

At a sampled point the actual hysteretic H can differ from sign Z only if X is
in S. Since P_A(X_t in S)<=C*s=eta, a union bound adds n*eta. Thus(8)+n*eta
bounds TV of the entire sampled H record, while all angular state is retained.
No reset or assertion about the boundary entrance density is made.

Schedules may be chosen from the model certificate before observing the path.
Arbitrary adaptive observation times or interventions do not inherit the
marginal density bound. A causal selection from an already received finite
deterministic record is a data-processing operation, not that broader claim.

## 5. Stationary count identity: earn rather than assume rare-cluster control

This section uses the ACTUAL committor q_B=P_x(tau_B<tau_A), only as a proof
device. It is0 on A,1 on B, harmonic in S, and has finite capacity
cap=E(q_B)<=C0=1/(beta R) by the supplied scalar trial. No q_B evaluation is
needed by the certificate.

Take the two-sided stationary diffusion. Ergodicity and positive pi(A),pi(B)
ensure visits to both basins arbitrarily far in the past. Hence its last-visited
label L_t in{0,1} (A=0,B=1) is well defined and jointly stationary with X_t.
The corresponding H=1-2L is cadlag. Its number N_t of label changes in(0,t]
is finite pathwise: continuity of Y on each compact time interval and the
unit separation of A and B preclude infinitely many full crossings.

The equilibrium potential belongs to the global closed form, is smooth in S
and up to each flat boundary locally. Its distributional generator has positive
boundary charge on A and negative charge on B. These are the standard
conormal/Revuz measures. Each has finite total charge cap: test against q_B
and1-q_B with compact cutoffs, using finite energy and1 in the conservative
finite-mass form. Thus Fukushima/Itô--Tanaka gives, first under compact/energy
localization,

 q_B(X_t)-q_B(X_0)=M_t+A^A_t-A^B_t,
 <M>_t=2 int_0^t Gamma(q_B)(X_u)du,
 Gamma(q_B)=beta^-1 grad q_B^T diag(1,M_z) grad q_B.

The A and B additive functionals are continuous and supported on their own
boundaries. At such a boundary the last-visited label equals q_B, except at an
opposite first hit itself; the local time has no atom at that instant. Thus
(q_B-L)d(A^A-A^B)=0. Visits/leavings of the same basin do NOT generate a reset
term. At an opposite hit q_B is continuous, while L switches to its new value;
(q_B-L)^2 jumps from1 to0, contributing exactly -1.

Applying the continuous-plus-jump square rule therefore gives

 (q_B(X_t)-L_t)^2-(q_B(X_0)-L_0)^2
   =2 int_0^t(q_B-L)_(u-) dM_u
       +2 int_0^t Gamma(q_B)(X_u)du -N_t.              (9)

There is no reflecting boundary or killing term in this full stationary model.
For removal of localization, |q_B-L|<=1 and stationarity imply the expected
martingale bracket is at most8t*cap/Ztot, finite. The martingale is L2 after
localization and passes in L2; the nonnegative energy integral passes in L1 by
its exact finite expectation. The square terms are bounded. Identity(9) then
also earns integrability of N_t (one may first stop its count and use Fatou,
then pass using the identity). Nonexplosion ensures compact exit localizers
increase to infinity. Taking stationary expectations gives the EXACT identity

 E_pi N_t =2t*cap/Ztot <=2t*C0/Ztot <=lambda*t.         (10)

This is the ordinary equilibrium transition-frequency/capacity relation,
not a substitution of inverse capacity for the Gibbs|A first-passage mean.
The boundary reset, infinity and initial-law distinctions are the point of
spelling out(9). Unbounded full fibers do not require an unreceived compact
boundary assumption: finite form energy/charge is the global control.

## 6. Suppress unseen clusters and couple TRUE continuous return clocks

Use a uniform analysis mesh Delta>0, n intervals; write x=lambda*Delta,
r=exp(-2x). Let D_i indicate that H differs at the two endpoints of interval i.
Its parity equals N_i modulo2. Thus

 1{N_i>=2}<=(N_i-D_i)/2.                              (11)

Under stationary pi, sign-flip probability is(1-<Z,P_Delta Z>)/2. The L1,
not L2, slab comparison and positivity give

 <Z,P_Delta Z> <=r+epsilon+2s.

The two endpoint H-versus-Z errors cost at most2s. Hence
E_pi D_i >=(1-r)/2-epsilon/2-3s. Combining this with(10) and
x-(1-exp(-2x))/2<=x^2 gives

 P_pi(any bin has >=2 ACTUAL full-basin transitions)
       <=(n/2)[x^2+epsilon/2+3s].                    (12)

The whole forward path law from Gibbs|A is the stationary forward path law
conditioned on X0 in A, with Radon--Nikodym bound C. Its label at0 is then
certainly A. Therefore the entire bad event(12), not a fictitious restarted
entrance law, is bounded by C times its stationary probability.

The symmetric reference chain has Poisson(lambda) jump times, independent
exponential holding times, and its probability of >=2 jumps in any mesh bin is
at most n*x^2/2. Couple its grid record to actual H using(8) and the slab union.
On success, if both paths have at most one jump per bin, equal grid endpoints
force the same number and direction of jumps in every bin. Pair these jumps;
their timestamps differ by at most Delta. No deterministic mesh endpoint is a
jump almost surely (the actual diffusion has a density and the separating
surfaces have zero Lebesgue mass). Linear interpolation between paired times
then gives an increasing time change fixing0,n*Delta, displacing times by at
most Delta, under which the two cadlag labels agree exactly.

A sufficient overall failure probability is therefore

 E_n(x)=sqrt[C*n*delta^2/(2(1-exp(-4x)))]
          +(C+1)*n*x^2/2 +C*n*epsilon/4 +(5/2)*n*eta,  (13)
 delta=sqrt(epsilon)+2sqrt(s).

The bound may be clipped at1. It is a coupling with time jitter, NOT continuous-
path total variation and NOT exact conditional renewals. If the finer delta_i
from(8) is used, the first term can be sharpened without changing the mechanism.
The same coupling may retain an initial nonanticipating classical R0, with the
reference chain independent of R0; all cluster/slab probabilities are still
unconditional bounds under the fixed actual Gibbs|A marginal.

## 7. Actual reusable-clock consequence and paid limits

For fixed dimension-free beta,kappa,d0,mu, accepted scalar asymptotics give
epsilon=O(alpha^-1), eta exponentially small. Fix any finite scaled horizon H.
Choose integers n tending to infinity so x=H/n is of order epsilon^(1/4).
For x<=1/4,1-exp(-4x)>=2x, so every term of(13) tends to zero uniformly over
admitted angular U and M_z, while Delta/T0=x tends to zero. Hence the ACTUAL
hysteretic process H_(T0*t), t in[0,H], converges by the explicit coupling to
the two-state unit-flip-rate chain, with retained full angular state and no
post-crossing equilibration assumption. This is a uniform Skorokhod time-change
statement on finite horizons; no global gap exists or is needed.

For the first j alternating waits, choose H and pay the Poisson truncation
P(Poisson(H)<j). On the successful event with at least j reference jumps,
|tau_i/T0-S_i|<=x for all i<=j. Thus wait increments differ by at most2x
(first by x) from j independent unit Exponential variables. For a joint wait-CDF,
a conservative additional threshold-boundary error is2j*x. This proves the
finite-j renewal limit rather than assuming independence after a boundary hit.
At fixed finite alpha it is only the quantitative received error, not exact iid.

The return direction is part of this alternating clock. If only A->B events
are exposed, each output-to-output cycle includes a B->A return too: the
reference wall-time interval is a sum of TWO exponentials, not an exponential
with free reset. One may report the active A->B waits separately, but actual
return/settling/exposure time cannot be erased from the ledger.

All physical horizons n*Delta=H*T0 are huge when the event is rare. This is an
analytic prediction/coupling certificate, not actual exposure, physical
preparation, sensor bandwidth or a simulated long trajectory. The mesh in
Section6 is a proof device; true event detection is a separate physical
obligation. Numerical receiving must pay raw input reading, the old three
scalar integrals, roots/exponentials, all finite search/refinement and external
horizon/accuracy conjunctions. Future deterministic finite-record queries may
reuse the certificate but their own computation is not free: a fixed FINITE
J-state accumulator costs O(nJ) arithmetic; arbitrary predicates, bounded real
accumulators, optimizations or samples require their actual costs.

An independently established TV preparation error adds ONCE by full path-kernel
contraction, not once per tick. No such preparation is supplied here; discrete
approximations are not automatically TV-close to continuous Gibbs. No stronger
unbounded-moment guarantee follows from the finite-path error, and relative
rare-transcript/tail or arbitrary adaptive-control guarantees are excluded.
