# A received exit-time clock survives neutral internal processing — V2

**Status:** self-contained corrected statement and proof, 2026-11-01 UTC. The
original root is immutable. V2 makes the weak-domain and nonautonomous chronology
explicit and supplies an actual global transverse-stirring example. It does not
expand any accepted executable interface or certify physical controls.

The mathematical ingredients are ordinary energy-space projection/Schur
complements, neutral dissipative control, and passive L2 small gain. They receive
full prior credit. Historical novelty is unresolved. No special exclusion of
these ordinary explanations is intended.

## 1. Reference form and the received actual evolution

Let H be a real or complex Hilbert space, with inner product conjugate-linear in
the first entry. Let A be a nonnegative, injective, self-adjoint operator and let
E be its closed form, with V=D(A^(1/2)). Equip V with the form norm
(||f||^2+E(f,f))^(1/2). Choose a unit vector e in V such that

    a=E(e,e)>0,       q=||A^(-1/2)e||^2<infinity.                 (1)

The inverse is a FORM: neither Ae nor A^(-1)e is required to belong to H. The
spectrum of A may accumulate at zero; no positive global gap is assumed.

An admissible actual evolution, initially u(0)=e, is received through the
following explicit weak-energy conditions. Write

    u(t)=c(t)e+x(t),       x(t) perpendicular to e,
    c(0)=1,              x(0)=0,
    y(t)=-E(e,x(t)).

On every finite interval [0,T], require x in L2(0,T;V), c absolutely continuous,
the scalar identity

    c'=-a c+y                                                   (2)

a.e., and the integrated hidden-storage inequality

    (1/2)||x(T)||^2 + int_0^T E(x,x) dt
          <= Re int_0^T conjugate(c)y dt.                        (3)

The evolution must provide well-defined terminal H representatives and (3) for
every queried T. A standard continuous energy solution suffices. These are
assumptions about the FULL actual evolution, not consequences of the word
"control." For neutral contractive interventions, the same statement allows
nonpositive jumps of hidden storage while c remains unchanged, provided the
received causal non-Zeno evolution still earns (2)--(3).

For example, a common-domain nonautonomous form sum with a neutral skew term
satisfies (2)--(3) once its actual energy solution is earned. A genuinely
additional dissipative term annihilating e and its dual is treated in the same
way. Merely writing B_t^*=-B_t and B_t e=0 does NOT prove existence of an
unbounded operator/form sum, compatibility of weak domains, or global
wellposedness. No bound on processing strength or time derivative enters the
clock estimate AFTER (2)--(3) have been received.

## 2. Exact energy-space Schur complement

Let Q={x in H:<e,x>=0} and define

    sigma=sup_{0!=x in V intersect Q} |E(e,x)|^2/E(x,x),           (4)

with supremum zero if the subspace is zero. Then

    sigma=a-1/q,             0<=sigma<a.                         (5)

**Proof.** Complete V in the energy norm to obtain H_E. Injectivity of A makes
this a norm; coercivity in the original H norm is not needed. Finite q makes
ell(z)=<e,z> a continuous functional on H_E with squared norm q. The upper bound
is energy Cauchy--Schwarz. Equality follows from z_delta=(A+delta)^(-1)e:

    <e,z_delta> -> q,
    E(z_delta,z_delta)=int lambda/(lambda+delta)^2 dmu_e -> q.

The convergence uses int lambda^(-1)dmu_e=q<infinity. Therefore

    inf_{z in V, <e,z>=1} E(z,z)=1/q.                            (6)

The resolvent approximants can be normalized to satisfy the constraint exactly.
The energy closure of V intersect Q is ker ell: if z_n tends in energy to a
vector in ker ell, replace z_n by z_n-ell(z_n)e. The squared energy norm of the
projection of e onto ker ell is consequently a-1/q. It is also the squared dual
norm of x -> E(e,x) on this subspace. This proves (5), without assuming the
minimizer in (6) or A^(-1)e lies in H. In particular aq>=1. □

## 3. Uniform correlation theorem and proof

Every evolution satisfying section 1 obeys

    sup_{t>=0}|c(t)-exp(-at)| <= (aq-1)/2.                        (7)

For sigma>0, (4) and (3), on a finite interval [0,T], give

    ||y||_2^2/sigma <= int E(x,x)
                    <= ||c||_2 ||y||_2,
    ||y||_2 <= sigma ||c||_2.                                   (8)

The zero-output case is included. Variation of constants in (2) gives

    c(t)=exp(-at)+int_0^t exp[-a(t-s)]y(s) ds.                    (9)

The causal exponential convolution has L2 gain at most 1/a, and
||exp(-at)||_{L2(0,T)}<=1/sqrt(2a). Since sigma<a,

    ||c||_{L2(0,T)} <= sqrt(a/2)/(a-sigma).                      (10)

Cauchy--Schwarz in (9) then gives

    sup_{0<=t<=T}|c(t)-exp(-at)|
       <= ||y||_{L2(0,T)}/sqrt(2a)
       <= sigma/[2(a-sigma)] = (aq-1)/2.                        (11)

This is first a finite-horizon proof, so it does not assume infinite-time
integrability to establish small gain. Arbitrary T proves (7). If sigma=0,
(4) forces y=0 a.e., and (9) is exact. No spectral mixture representation,
stationary processing, hidden-mode basis, or global gap was used. Q is a proof
subspace, not an oracle, acquired model reduction, or simulated trajectory.

## 4. Trial/current clock certificate

Now let A be a positive self-adjoint reference killed generator in L2(D,m),
where m is finite and D is the disjoint union of a basin A_set and a slab S.
Put M=m(A_set)>0, S0=m(S), rho=S0/M. Let the explicit killed-form-domain trial h
satisfy h=1 on A_set and 0<=h<=1_D. Its extension is zero on the killing set B.
Put N=||h||^2, so M<=N<=M(1+rho), and e=h/sqrt(N).

Suppose reference energy and inverse-form certificates earn

    E(h,h)<=C0,        <h,A^(-1)h><=B_total,
    k0=C0/M,          epsilon=C0 B_total/M^2-1.                 (12)

All inverse quantities denote inverse forms/monotone zero-resolvent limits.
Valid premises imply epsilon>=0, because
E(h,h) * <h,A^(-1)h> >= N^2 >= M^2. Moreover

    a<=k0,
    k0 q<=C0 B_total/(MN)<=1+epsilon,
    aq-1<=epsilon,
    k0/a-1<=epsilon,                                           (13)

where the last implication uses aq>=1. For a<=k0, the mean-value estimate is

    sup_t |exp(-at)-exp(-k0t)|
       <= (k0-a)/(exp(1)a) <= epsilon/exp(1).                   (14)

Thus (7) gives the normalized actual trial correlation bound

    sup_t |c(t)-exp(-k0t)|
       <= (1/2+1/exp(1))epsilon <= (7/8)epsilon.                (15)

Here exp(1) is **Euler's number**, not the Euler--Mascheroni constant and not the
unit trial e. The final rational bound follows from exp(1)>8/3.

### Separate source-current bounds

If the reference killed resolvent is positivity preserving, then independently
received bounds

    <1_A_set,A^(-1)1_A_set><=B_A,
    <1_S,A^(-1)1_S><=B_S

give B_total=(sqrt(B_A)+sqrt(B_S))^2. Indeed 0<=h<=1_D and positivity imply
<h,A^(-1)h><=<1_D,A^(-1)1_D>, and inverse-form Cauchy--Schwarz gives the stated
sum bound. This can first be done at positive resolvent parameter and then
passed monotonically to zero. An improved B_A does NOT automatically improve
B_S. The two source bounds and every numerical outward operation remain
separate receiving obligations.

## 5. Actual positive Markov propagation: chronology and initial law

Suppose the ACTUAL process has a globally received killed transition propagator
on observables

    P_{s,t}f(x)=E[f(X_t) 1_{tau_B>t} | X_s=x],

positive and L2-contracting with respect to the SAME measure m. For a process
started at time zero this notation uses the corresponding survival interval;
subsequent conditional propagators are defined on the unkilled state space D.
Take

    u(t)=P_{0,t}^*e.                                           (16)

This is the chronological forward-density evolution: where generator notation
is legitimate, partial_t P_{0,t}=P_{0,t}L_t and u'=L_t^*u. We do NOT assume
P_{0,t}e solves u'=L_tu, which would generally reverse the required ordering for
time-dependent generators. Require that (16) actually earns (2)--(3).

For real positive functions the scalar c(t) equals
<h,P_{0,t}h>/N. The actual survival probability from the EXACT initial law
m(.|A_set) is

    S_actual(t)=<1_A_set,P_{0,t}1_D>/M.                         (17)

Write r=h-1_A_set and d=1_D-h. Both are nonnegative, supported in S, and at
most one. With P=P_{0,t},

    <1_A_set,P1_D>-<h,Ph>
       =<1_A_set,Pd>-<r,Ph>.                                  (18)

Both right-hand terms are nonnegative. Contraction bounds them respectively by
sqrt(M S0) and sqrt(N S0); hence their DIFFERENCE has absolute value at most
sqrt(N S0), not their sum. Positivity and contraction also give 0<=c(t)<=1.
After division by M and conversion from N/M to one,

    |S_actual(t)-c(t)| <= rho+sqrt(rho(1+rho)).                  (19)

Combining (15) and (19) proves the received clock theorem:

    sup_{t>=0}|P_{m(.|A_set)}(tau_B>t)-exp(-k0t)|
       <= (7/8)epsilon +rho+sqrt(rho(1+rho)).                   (20)

Probability envelopes may of course be clipped to [0,1]. Self-adjointness is
required of the REFERENCE A, not of the actual propagator. The latter can be
nonreversible and time inhomogeneous.

### Acquired rate interval

If a separate numerical receiver earns 0<k_lo<=k0<=k_hi and selects
k_star=(k_lo+k_hi)/2, add

    (k_hi-k_lo)/(2 exp(1) k_lo)
       <= (3/16)(k_hi/k_lo-1)                                  (21)

to the right side of (20) to use the single Exp(k_star) reference. This follows
by integrating the rate derivative t exp(-kt) and maximizing over time. A
midpoint is not automatically the exact k0. Bounds for epsilon, rho and every
root, exponential or interval operation require their own outward receiving;
this proof is not an implementation of that receiver.

## 6. A concrete globally received neutral-stirring class

This example is on the original whole-space constant-SPD Langevin model. It is
not merely a bounded-domain analogy and does not add an unreceived mobility.
Use F(y,z)=v(y)U(z), v(y)=1+kappa(1-y^2)^2, beta,kappa>0, where U is a smooth
positive coercive homogeneous polynomial of degree p. Let the transverse
dimension be d, alpha=d/p>=4, and M_z>=mu I be fixed SPD. The reference SDE is

    dY=-v'(Y)U(Z)dt+sqrt(2/beta)dW,
    dZ=-v(Y)M_z grad U(Z)dt+sqrt(2M_z/beta)dB.                  (22)

Its finite Gibbs measure is proportional to exp(-beta v U); scaling gives y
marginal proportional to v^(-alpha). Kill at Y=b, and use a trial h=h(y).

Choose any constant skew d-by-d matrix J and smooth compactly supported scalar
cutoffs phi, psi, and set

    chi(y,z)=phi(y)psi(U(z)),
    c_field(y,z)=(0,chi(y,z)J grad U(z)).                        (23)

Coercivity of U makes this a smooth compactly supported, bounded, globally
Lipschitz vector field. Choose nonzero cutoffs/J if nontrivial stirring is
wanted. Let s(t) be predetermined, measurable and locally essentially bounded;
there is no common numerical cap on its amplitude, frequency or derivative.
Add s(t)c_field to the drift of (22).

### Neutrality is exact

Skewness gives grad U dot J grad U=0 and
trace(J Hess U)=0. Also grad_z chi is parallel to grad U. Consequently

    div c_field=0,       c_field dot grad F=0,
    div(m c_field)=0,    c_field dot grad h=0.                  (24)

The vector field has no y component, so is tangent to the killing boundary.
There is no infinity boundary term because it is compactly supported. The
transport C=c_field dot grad is therefore antisymmetric in L2(m) at the form
level and annihilates h on both sides, including its weak form-domain version.
One can also see genuine skew-adjoint receiving from the complete ODE flow of
this bounded smooth field: (24) makes that flow m-preserving, and composition
with it is a strongly continuous unitary group fixing h.

### Global SDE existence is earned

Set K=1+kappa/p and use the proper function

    V_lyap=1+y^2+K z^T M_z^(-1)z.

The reference generator satisfies

    L0 V_lyap=2(1+Kd)/beta
               -2[yv'(y)+Kp v(y)]U(z)
              <=C_lyap:=2(1+Kd)/beta,                          (25)

because yv'>=-kappa and v>=1. Compact support gives the finite constant
D_lyap=sup |c_field dot grad V_lyap|. Thus

    L_t V_lyap<=C_lyap+D_lyap|s(t)|.                           (26)

Local time-measurable SDE existence and pathwise uniqueness follow from local
spatial Lipschitz coefficients. Stopped Ito and (26) give, for a point start,

    E V_lyap(X_{T wedge tau_R})
       <=V_lyap(X_0)+C_lyap T+D_lyap int_0^T|s(t)|dt,

where tau_R is first exit from {V_lyap<R}. The right side is finite on each
finite horizon, and division by R proves nonexplosion as R tends to infinity.
This extends to probability mixtures of finite point starts. In particular the
exact Gibbs basin law is admissible. Killing cannot create explosion.

### Actual positivity, common measure and common weak domain are earned

For the full process let E_full be the reference form. Its conservative
symmetric diffusion has invariant finite m and contains the constant 1 in its
form domain with zero energy. The transport form satisfies

    |<f,Cg>| <=||c_field||_infinity sqrt(beta/mu)
                              ||f||_2 sqrt(E_full(g,g)).        (27)

It is bounded on the SAME form domain equipped with the H-plus-energy norm;
its real diagonal part is zero. On finite horizons s is bounded, so the usual
nonautonomous variational construction applies to E_full plus the
antisymmetric transport form. Its energy estimate gives uniqueness. The
constant density 1 is an exact solution because E_full(f,1)=0 and C1=0. The
resulting evolution therefore preserves m. Its smooth local generator agrees
with the globally unique diffusion already received above; this identifies the
variational evolution with the actual SDE, not merely a formal operator.

Equivalently, preservation of m can be checked constructively by alternating
the invariant reference diffusion with the complete m-preserving transport
flow, localizing with (26), and passing to the SDE splitting limit. Step
approximations to any locally bounded measurable s converge in L1 on finite
intervals. Stopped locally-Lipschitz SDE stability plus (26) passes invariance
to their limit. This does not infer invariance from finite Gibbs mass alone.

The killed transition propagator is positive and sub-Markov. Jensen and
domination by the full process yield

    int |P_{r,t}f|^2 dm
       <=int P_full_{r,t}(|f|^2) dm=int |f|^2 dm.               (28)

The same bound (27) holds on the reference killed form domain because the
transport is tangent to the killing boundary. The actual adjoint density
solution belongs to L2(0,T;V), is H-continuous, and satisfies

    (1/2)d||u||^2/dt <=-E(u,u).                                (29)

Testing against e=h/sqrt(N) is legitimate; its transport term vanishes by
(24). This gives (2). Subtracting the scalar identity
(1/2)d|c|^2/dt=-a|c|^2+Re(conjugate(c)y) from (29) gives precisely (3).
Thus the example earns all actual-process premises of (20).

Existence estimates may depend on the finite-horizon amplitude norm. The
clock-error constant does not. Local boundedness is a sufficient receiving
condition for THIS example, not a necessary hypothesis added to the abstract
port theorem. No extension to merely formal, singular or arbitrarily
unbounded drift/mobility is implied.

This stirring need not be a dynamically irrelevant rigid rotation. For
U=z1^4+2z2^4+sum_{i>=3}zi^4 and J(a,b)=(-b,a) in its first two coordinates,

    (J grad U) dot grad |grad U|^2
       =768 z1^3 z2^3(-z1^2+2z2^2),                            (30)

which is generally nonzero. It moves along energy levels while changing
coefficients governing subsequent transverse-energy dynamics. No claim about
the sign or size of its survival change is needed for the theorem.

## 7. Strict scope and nonclaims

- This is uniform ABSOLUTE CDF/survival accuracy. It is not relative accuracy in
  an extreme tail, an exact exponential law, an exponential-moment theorem,
  or a bound on the processed mean. The reversible reference MFPT theorem must
  NOT be transferred to the actual nonautonomous process merely from (20).
- The initial law is the exact full m(.|A_set), for the same m used by the
  reference form and actual L2 contraction. This is not a physical sampler,
  preparation, calibration or hardware guarantee.
- Predetermined protocols are included when their actual propagation is
  received. Independent external random protocols can be conditioned on and
  averaged if their paths earn the same bound. Source-dependent record
  feedback is NOT automatic: branchwise invariance does not imply invariance
  after a state-dependent branch selection. A joint source/controller model
  must earn the actual energy, positivity and common-measure premises.
- General extra reversible transverse diffusion/jumps can fit only when their
  common-measure invariance, neutrality, dissipation, weak domain and global
  actual process are separately proved. State-dependent mobility needs its
  divergence drift. Finite Gibbs mass does not prevent explosion for an
  arbitrary unbounded mobility.
- Mathematical neutrality means preservation of this task's trial on both
  sides. It does not mean zero work, free actuation, free switching/readout,
  or unlimited physically valid exposure. All actual acquisition, control,
  waiting, release and calibration obligations remain unpaid here.
- No quantum all-selected fault theorem, physical computing separation,
  equipment claim, historical novelty claim, or new executable acceptance is
  supplied. The ordinary Schur/passivity/control explanation is retained.

## 8. Provenance

Original immutable root:
`PASSIVE_PORT_CLOCK_ROOT.md`
SHA-256 `487a37d2d7d0c15ee756ccda3717bb47c5bd9aa4b1e0bec5ea7201c435950a6d`.

Independent original-root audit and proposed precision patch:
`audit_neutral_processing_process_20261101_0034/`.
V2 is the consolidation by that reviewer, so a V2 source-bound recheck is not
misrepresented as a new second-author independent review.

Accepted background used only for the existing reference certificate/model:

- `TRIAL_RESOLVENT_TO_SURVIVAL_ROOT_V2.md`, SHA-256
  `7d4d7f61e03860e11e0e550ab850714497acc6f395b5179e4f318a1739434e83`.
- `SEPARATE_CURRENT_SURVIVAL_COROLLARY_ROOT.md`, SHA-256
  `5a98beb1d277777aa03016e6d56b76f29ebe52188c5fe981b0cf95c050dee7f4`.
- `POISSON_CURRENT_CONSTANT_SPD_MFPT.md`, SHA-256
  `bf9e83e1f39f25758dc02b10a06d06a955b98e61de172f633ba5d4f341a7d8e0`.

The proofs of the port estimate, normalization, initial-law transfer and concrete
process receiving are contained above; no patch reconstruction is required.
