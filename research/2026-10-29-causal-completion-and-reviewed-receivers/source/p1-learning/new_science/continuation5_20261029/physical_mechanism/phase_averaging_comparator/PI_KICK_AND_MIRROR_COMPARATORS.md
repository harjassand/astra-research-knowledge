# Actual pi kicks and mirror rotation: strong ordinary averaging suppliers

29 October 2026. A separate continuation5 comparison. The completed transport
unit and all predecessor files remain unchanged.

## 1. Matched question and operation boundary

Let E_i be orthogonal visible heat-bath or exchange projections in L2(pi), and
D_i=I-E_i. Actual native rates are

    lambda_i = s_i(Y_outside) [1+alpha_i(Y_outside,Z) cos theta_i],
    |alpha_i| <= alpha < 1.                              (1)

The multipliers s_i and alpha_i commute with E_i. Z is arbitrary frozen
unknown memory. The target visible generator is

    a=sum_i s_i D_i.                                    (2)

Root's added independent phase-diffusion supplier has a finite-time compressed
semigroup estimate uniform in time, volume, and the visible spectral gap. This
note constructs the strongest ordinary alternatives I could justify and states
where their guarantees differ. A deterministic rotation, a pi kick, an absolute
phase setter, and a phase-only preparation mode are separate physical controls.
None follows from the mere availability of a diffusion kernel.

The operators below describe fixed-time endpoint observables. Uniformity over
all t is not a bound on a complete multitime record or on adaptive intervening
measurements. Unknown kinetic parameters still affect native paths and exposed
control/phase records.

## 2. Independent Poisson pi kicks match the general noise guarantee

Suppose an actual pulse flips theta_i -> theta_i+pi while leaving Y, Z and all
other phases fixed. Between pulses theta_i is otherwise fixed. Independently
flip each phase at Poisson rate gamma. Write the unknown original phase as
part of the frozen parameter and its orientation as sigma_i in {-1,+1}:

    lambda_i=s_i(1+beta_i sigma_i),
    beta_i=alpha_i cos(theta_i^original), |beta_i|<=alpha.

The signs are independent telegraph chains. Their product stationary law is
uniform, and their generator has spectral gap 2 gamma, independent of the
number of phases. Let P average these signs while retaining Y,Z and the original
phase offsets. The full self-adjoint positive generator is

    A_gamma=sum_i s_i(1+beta_i sigma_i)D_i
                  +gamma sum_i(I-F_i),                  (3)

where F_i flips sign i. It is the actual Markov generator, not an averaged
replacement of unknown native dynamics.

For f in the range of P,

    a=P A_gamma P=sum_i s_i D_i,
    b=Q A_gamma P=sum_i sigma_i s_i beta_i D_i,
    ||bf||²=sum_i ||s_i beta_i D_i f||²
            <= M_tel <f,af>,
    M_tel=max_i ess sup(s_i beta_i²) <= s_max alpha².    (4)

Independence of the stationary signs eliminates cross terms. Commutation with
E_i and D_i²=D_i give the last inequality. Native positivity and the telegraph
gap imply c=Q A_gamma Q >=2 gamma Q.

Consequently, if r_tel=M_tel/(2 gamma)<1,

    sup_(t>=0) ||P exp(-t A_gamma)P-exp(-ta)||
          <= r_tel/[2 sqrt(1-r_tel)].                   (5)

This covers arbitrary Y_outside-dependent beta_i and arbitrary frozen Z. It
does not need a finite hidden predictive model or visible mixing gap.
The worst-case ratio s_max alpha²/(2 gamma) equals the circle-diffusion ratio
s_max alpha²/(2 kappa) when gamma=kappa. This is a comparison of mathematical
control rates, not their energy, apparatus, or clock costs.

### A self-contained compressed-semigroup derivation

For a positive self-adjoint block operator A=[[a,b*],[b,c]], suppose
c>=kappa and b*b<=M a. Put r=M/kappa<1. Completing a square gives

    <(p,q),A(p,q)> >= (1-r)<p,ap>.

For u(t)=exp(-tA)(f,0), energy dissipation therefore yields

    integral_0^infinity ||a^(1/2)p(t)||² dt
          <= ||f||²/[2(1-r)].

The forced omitted component is
q(t)=-integral_0^t exp[-(t-s)c] b p(s) ds. The L1 norm 1/kappa of its
convolution kernel and Young's inequality give

    ||q||_(L2(time)) <= sqrt(M)/kappa * ||a^(1/2)p||_(L2(time)).

The visible error paired with g is

    -integral_0^t <b exp[-(t-s)a]g,q(s)> ds.

The integrated a-energy of exp(-ta)g is <=||g||²/2. Cauchy-Schwarz proves
r/[2 sqrt(1-r)]. There is no lower bound on the nonzero spectrum of a.
Kernel vectors are annihilated by b, so the same argument covers conserved
visible quantities. This is the same relative-form mechanism as root's
compressed theorem, instantiated with an ordinary telegraph supplier.

### Initial signs, retained data, and burn-in

Exact P initialization can be supplied by fresh independent fair pi-kick
choices conditional on the complete deployment record and frozen parameters.
The orientation outcomes must not remain in the retained record against which
that conditional guarantee is requested. Forgetting a variable in a formula
does not remove an apparatus copy of its value.

If the phase actuator can run ALONE while Y and Z are actually held fixed,
fresh unrecorded telegraph evolution for time u prepares N signs from any
known initial sign pattern within

    TV <= min{1, (N/2) exp(-2 gamma u)}                 (6)

of independent uniform signs, jointly with the old retained record. This
coupling bound adds directly to an appropriate later law comparison. It
requires u >= log[N/(2 epsilon)]/(2 gamma) when that logarithm is positive.
The signs are the two-point phase orbits; their unknown original cosines are
retained in the frozen parameters. Exact independent fair private choices cost
N fresh bits plus the actual pulses and disposal/isolation of their outcomes.

If native Y motion runs during burn-in, (6) for the signs alone does NOT imply
the joint product P premise: Y can become correlated with the signs. An actual
phase-only/holding supplier or a separate joint correlation estimate is needed.
Likewise, exposing the bath kicks and their timing prevents simply invoking
unrecorded-bath conditional initialization. The endpoint norm estimate (5)
does not itself control all exposed kick records.

Poisson kicks cost N gamma expected physical flips per unit time. A global
clock can select a site uniformly, but its event rate then scales as N gamma.
The pulse duration and accuracy, site addressing, sensing if used, and real
phase displacement all remain physical costs. If the pulses are not effectively
instantaneous relative to the declared model, their actual waveform must be
included. A one-site telegraph correlation decays at 2 gamma; that numerical
factor is not a free thermodynamic advantage over diffusion.

## 3. Deterministic echo is exact in the commuting family

If a and all native modulation operators commute, flipping every phase by pi
reverses the entire modulation B. Evolve for h under a+B and h under a-B.
Then

    exp[-h(a-B)] exp[-h(a+B)] = exp(-2ha).              (7)

This is exact for every unknown phase/amplitude and every volume at cycle
boundaries. Independent heat-bath sites with rates depending only on frozen
parameters are an example. No random seed or phase reset is needed for the
stroboscopic assertion; the deterministic pulse schedule may be retained.
Finite-time fluctuations and native records inside the cycle are different.

Exchange modes on neighboring SSEP bonds do not commute. Neither do general
state-dependent heat-bath modes. Equation (7) is not valid there. Increasing
the switching rate supplies a conventional product-formula approximation,
whose uniform-time and volume scope must be proved rather than assumed.

## 4. A constructive uniform-time mirror theorem on a bounded sector

Let H_0 be a finite-dimensional common invariant Hilbert sector of ALL native generators being
compared. On that sector suppose

    a>=0, ||a||<=L, B=B*, -alpha a <= B <= alpha a,
    A_+=a+B, A_-=a-B, c=1+alpha.                      (8)

L is an upper bound, not the visible spectral gap. No positive gap is needed.
B may contain arbitrary fixed unknown parameters. An actual global pi pulse
changes B to -B without changing the visible specimen or hidden Z.

Use the symmetric physical cycle

    + for h/2, pi pulse, - for h, pi pulse, + for h/2.

Its duration is 2h and its endpoint operator is

    T_h=exp(-h A_+/2) exp(-h A_-) exp(-h A_+/2).        (9)

It is a positive self-adjoint contraction. Define

    x=2hcL,
    R_3(x)=exp(x)-1-x-x²/2,
    epsilon_h=R_3(x)/[h L (2-exp(x))].                 (10)

Assume x<log 2 and epsilon_h<1. The a=0 sector is trivial.

### Theorem 1: deterministic stroboscopic bound

The positive effective generator a_h=-log(T_h)/(2h) satisfies

    -epsilon_h a <= a_h-a <= epsilon_h a,

and therefore

    sup_(n>=0) ||T_h^n-exp(-2nh a)||
        <= epsilon_h/[2 sqrt(1-epsilon_h)].             (11)

For small h, epsilon_h=(4/3)c³L²h²+O(h³L³). The bound is independent of volume
whenever the invariant-sector bound L is, and independent of how small a's
nonzero eigenvalues are. It holds for each fixed B; the initial phase and
deterministic pulse schedule can be retained at these cycle boundaries.

**Proof.** Work on the complement of ker a and define the form norm
||D||_a=||a^(-1/2)D a^(-1/2)||. Because A_±=a^(1/2)C_±a^(1/2) with
||C_±||<=c, any word of k such factors has form norm at most c^k L^(k-1).
The exponential product in (9) agrees with exp(-2ha) through degree two.
Bounding all remaining ordered words by their absolute series coefficients,

    ||T_h-exp(-2ha)||_a <= (2/L) R_3(x).               (12)

Let D=I-T_h and E=I-exp(-2ha). The same series estimates give
||D||_a, ||E||_a <=[exp(x)-1]/L. Therefore both similarity norms
||a^(-1/2)D a^(1/2)|| and ||a^(1/2)D a^(-1/2)|| are at most q=exp(x)-1<1;
the analogous bounds hold for E. The telescoping identity for D^k-E^k,
followed by the absolutely convergent log series, yields

    ||log T_h+2ha||_a
       <= ||T_h-exp(-2ha)||_a sum_(k>=1) q^(k-1)
       <= (2/L) R_3(x)/(2-exp(x)).                     (13)

Dividing by 2h proves the relative-form estimate. To compare the semigroups,
use Duhamel and Cauchy-Schwarz in the a-energy. The integrated a-energy of
exp(-t a_h) is at most 1/[2(1-epsilon_h)] on a unit vector, while that of
exp(-ta) is at most 1/2. The relative error epsilon_h then gives (11).
Both generators annihilate ker a, so its inclusion causes no difficulty. QED.

### Theorem 2: all physical times after mean-zero phase averaging

Let the fixed unknown B be drawn from the actual conditional initial phase
law with E B=0, while a and the bound (8) are unchanged. A fresh unretained
global fair pi-kick orientation can also provide this symmetry for arbitrary
fixed original phases; it flips the entire B. Then the actual compressed
endpoint propagator U_bar(t) satisfies

    sup_(t>=0) ||U_bar(t)-exp(-ta)||
      <= epsilon_h/[2 sqrt(1-epsilon_h)]
                         +2 alpha² L² h².              (14)

**Proof.** Write t=2nh+u with 0<=u<2h. The actual propagator is a partial-cycle
contraction V_B(u) times T_(h,B)^n (or the reverse-order adjoint convention;
the norm proof is identical). Replace the latter by exp(-2nh a), using (11)
uniformly in B before averaging. For the remaining partial-cycle error write
Duhamel twice. The single-B term averages to zero because E B=0. Every
remaining term is bounded by ||B||² times the two-time simplex volume u²/2,
using the contraction of all intervening native and mean propagators. Since
||B||<=alpha L and u<2h, its norm is at most 2 alpha² L² h². QED.

If the orientation is retained and one conditions on it, the cancellation
does not apply. The valid bound for each key at arbitrary times is instead

    epsilon_h/[2 sqrt(1-epsilon_h)] +2 alpha L h.        (15)

All-time quadratic error can also be averaged over an actually independent
uniform phase ensemble. Marginally uniform phases correlated with a retained
record do not supply the needed conditional mean-zero initialization. The
theorems compare single-time operators; they do not claim a joint total-
variation guarantee for the pulse key, complete native path, or multiple
adaptive reads.

### Finite-speed mirror rotation, without instantaneous pi pulses

Suppose an actual actuator can rotate every phase at a prescribed angular
velocity Omega while leaving Y,Z unchanged, reverse that velocity, and keep
unmodeled diffusion/drift absent during this protocol. Set h=2pi/Omega.
Rotate forward through one full turn during [0,h] and retrace it during [h,2h].
For every unknown original phase, the coefficient path A(t) is palindromic,
its time average is a, and 0<=A(t)<=c a.

The complete propagator is W*W, hence positive self-adjoint. Palindromicity
makes its second-order ordered integral equal to one half the square of its
first-order integral. The ordered-word bounds used in (12)–(13) are unchanged.
Thus (11) holds, and (14) also holds if the actual initial ensemble has
E[A(t)-a]=0 for each t, for example independent uniform original phases or a
fresh unretained global mirror orientation. This avoids an ideal instantaneous
pi pulse, but it supplies a stronger deterministic phase-motion actuator.

If an uncontrolled Brownian phase process remains active, the actual phase
path is not palindromic. Retracing the deterministic control does not reverse
fresh noise. That different protocol requires its own bound; it is not
silently included in the mirror theorem.

## 5. Consequential SSEP density-mode receiver

On a bounded-degree graph, let E_e=(I+swap_e)/2 for an exclusion exchange on
bond e. Let s_e be supplied known positive constants and beta_e arbitrary
functions of frozen parameters, neither depending on the particle configuration.
Then every native generator preserves the
linear density-observable sector

    f_v(eta)=sum_x v_x(eta_x-rho).

On coefficients v the mean generator is the weighted graph Laplacian with
bond conductance s_e/2. Its norm obeys

    ||a|| <= Delta s_max = L,                           (16)

where Delta is maximum graph degree. Under product Bernoulli pi, or the
uniform canonical exclusion law restricted to mean-zero v, the observable
inner product is a scalar multiple of the Euclidean coefficient inner
product. Thus (16) and the mirror norm bounds have the intended L2(pi) meaning.

For the nearest-neighbor ring, L<=2s_max at EVERY system size. Equations
(11) and (14) therefore control density modes at t=N² tau with no loss as N
grows or the diffusive spectral gap vanishes. The deterministic error scales
as O((s_max h)²), compared with the inverse-noise-rate bound for diffusion or
telegraph control. A concrete conventional mirror supplier can consequently
match, and asymptotically improve the frequency dependence of, the density-
mode consequence in this matched subfamily. This does not compare their
physical energy costs or establish a practical speedup.

If alpha_e depends on Y_outside, the native generator can send a linear density
observable into a nonlinear observable. That sector is then NOT invariant,
even when the averaged generator is exactly SSEP. Replacing the full a by its
one-particle norm in (16) would be invalid. The full many-body generator norm
can grow with volume. Root's general local-variance/diffusion bound covers
that larger family; this deterministic bounded-sector theorem does not.

## 6. Sharp failure of a quadratic all-time, all-volume echo claim

Even commuting independent sites defeat the tempting extension of (14) to
the full many-body observable space with a volume-independent L.

Take N fair independent spins y_i in {-1,+1}, E_i the fair heat-bath projection,
s_i=1, and lambda_i=1+alpha cos theta_i. Initial phases are independently
uniform. The normalized all-spin character F_N=product_i y_i is an eigenvector
of the mean generator a with eigenvalue N. During the initial + segment of a
mirror cycle, at time t before its first pulse,

    P exp(-t A_theta)P F_N
       = exp(-Nt) I_0(alpha t)^N F_N,                  (17)

where I_0(z)=(1/2pi) integral exp(z cos theta)dtheta.
Choose t=h/2=1/N. Since I_0(z)=1+z²/4+O(z^4),

    ||[P U(t)P-exp(-ta)]F_N||
       ~ alpha²/(4eN) = alpha² h/(8e).                (18)

Thus this mirror sequence cannot have an O(h²) error bound uniform in BOTH
all times and volume, even though it is EXACT at every completed cycle in
this commuting example. The initial phases here are the same independent
uniform phases used by the diffusion compression; the failure is not caused
by a mismatched phase prior.

For synchronous deterministic rotation, the integrated cosine has amplitude
R_t=2 sin(Omega t/2)/Omega. Replace alpha t by alpha R_t in (17). At t=c/Omega
and N asymptotic to Omega/c,

    error ~ [alpha² sin²(c/2)/(e c)] / Omega.           (19)

Any c>0 with sin(c/2)!=0 gives an inverse-frequency lower bound. The same
initial segment occurs in a forward-then-reverse rotation. This does not
exclude a uniform inverse-frequency upper bound for broader deterministic
protocols; no such general theorem is claimed here.

One global fair orientation bit is even weaker than N independent phase
orientations on the full many-body space. With all original cosines equal to
1, the corresponding multiplier is exp(-Nt) cosh(alpha Nt). At t=1/N its
deviation from exp(-1) is exp(-1)[cosh(alpha)-1], independent of pulse speed
when N is increased with it. This does NOT contradict the root diffusion
theorem: a single common sign is not its independent stationary phase
initialization. It shows why the convenient global-bit initialization in
the bounded-sector theorem cannot be promoted to a general full-space result.

## 7. Stronger actuators and physical cost boundaries

An actual absolute phase setter with a compatible hold can set every theta_i
to pi/2, making cos theta_i=0 and lambda_i=s_i exactly. It defeats averaging
entirely, without learning Z. An unknown phase translation or a pi flip does
not supply an absolute phase setter; each preserves the original offset.
Actual phase readout plus calibrated rotations and a hold may supply one, at
their sensing/actuation/preparation costs.

Mirror pi cycling requires two synchronized global pulses per duration 2h.
At most this is a constant number of broadcast control events, not a claim
that manipulating N physical phases has volume-independent energy or hardware
cost. Independent Poisson kicks require N gamma expected local events per
unit time. Continuous diffusion and deterministic rotation have their own
actuator and dissipation costs, not determined solely by kappa or Omega.

The deterministic bounds allow arbitrary retained frozen Z and old data only
under their actual conditional phase initialization. They do not use calibration
to learn the hidden kinetics. An expectation bound transferred from an L2(pi)
operator estimate also retains the real L2 norm of the incoming visible
density; it is not automatically a dimension-free worst-state TV statement.

## 8. Disposition

Independent telegraph pi kicks supply the same general uniform-time/volume
relative-form estimate as circle diffusion when the pi actuator and proper
conditional initialization are real. Symmetric deterministic cycles give a
stronger second-order ordinary comparator on a genuinely invariant bounded-
norm sector, including SSEP densities with configuration-independent bond
disorder. They are exact stroboscopically for commuting modes. Neither result
licenses claiming that a noise-only phase interface already contains kicks,
controlled rotations, phase setting, or conditional phase preparation.

The full many-body all-time quadratic claim fails in an explicit commuting
family. The broad inverse-frequency deterministic comparison under arbitrary
Y_outside-dependent amplitudes remains unresolved here. The sources and checks
are recorded separately; no historical novelty claim is made for telegraph
motional narrowing, Strang symmetry, or dynamical decoupling.

Primary sources and their actual read scopes are in
`PRIMARY_PHASE_AVERAGING_COMPARISON.md`. The mirror mechanism is conventional
[Strang symmetry](https://doi.org/10.1137/0705041), and randomization-based
decoupling has substantial [primary predecessors](https://arxiv.org/pdf/quant-ph/0511120).
Neither source is used as a substitute for the explicit dissipative form and
record-scope proofs above.
