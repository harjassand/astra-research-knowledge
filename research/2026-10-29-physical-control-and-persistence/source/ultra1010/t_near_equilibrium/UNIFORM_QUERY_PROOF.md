# A subcritical hard-sphere query and positive finite-observation output

29 October2026. Consumes the full-domain radial operator certificate, not its
finite preview. This is a restricted actual-hard-sphere operation with ideal
real/random primitives. Continuous full-velocity iid output and finite-bit
implementation are NOT claimed. Signed marks are only an intermediate;
Section7 gives an actually positive normalized observation consumer.

## 1. Acquired source class

M(v)=(2pi)^(-3/2)exp(-|v|^2/2), beta=3/4. Supply a radial nonnegative f0,
its exact density evaluator, mass1, mean0, energy3 and a warranted

    ||(f0-M)/M^beta||_infinity <=D=1/3200.

The ordinary comparator receives the same density, sampler and symmetry.
One explicit source is f_delta from POSITIVE_RESIDUAL_BARRIER.md, with
delta=2^-14. Its source bound is <=5delta M(0)^(1-beta)<5/16384<D.
All source parameters and sampling are explicit; no evolved density or
norm bound is an input. Other sources must actually qualify these premises.

## 2. Controlled mild equation

Let h=(f-M)/M^beta. Let Kc be the radial, mass/energy-controlled linear
kernel in RADIAL_OPERATOR_PROOF.md, and nu the known Maxwellian collision
frequency. The acquired coefficient is

    int |Kc(V,ds)| <=eta nu(V), eta=99/100.

Let Z_beta=int M^beta=(2pi)^(3/8)beta^(-3/2). Collision energy conservation
gives M^beta(p)M^beta(q)=M^beta(v)M^beta(w). Therefore the nonlinear term is

    N(h,h)(v)=int M^beta(w)|v-w| E_sigma
                    [h(p)h(q)-h(v)h(w)]dw.

Write nu_beta(v)=int M^beta(w)|v-w|dw. Gaussian scaling and radial convexity
give nu_beta/nu <=C_beta=Z_beta/sqrt(beta)<4. The last strict constant is a
plain rational/pi bound, not an unknown kinetic norm.

Use the mild equation with diagonal loss nu. For ||h||<=D, its nonlinear
term has norm at most2C_beta D^2 nu, and Lipschitz constant at most
4C_beta D nu. Hence the controlled map preserves the D-ball because

    eta+2C_beta D < eta+8D <1,

and is a contraction there because

    eta+4C_beta D < eta+16D=199/200.                    (U1)

These bounds hold on every time horizon, with the same constants, since
the diagonal exponential integral has mass at most1. They construct a
unique global bounded controlled mild solution; no future oracle or mixing
assumption is used.

## 3. Identification and positivity, without importing a future bound

Moment control changes the physical equation only by

    -M(v)[a(|v|) m0(t)+c(|v|) m2(t)],
    mj=int |v|^j M^beta(v)h_t(v)dv, j=0,2.

The ordinary quadratic collision term conserves mass and energy even for
signed integrable Gaussian-decaying densities. Thus (m0,m2) satisfies a
finite homogeneous linear ODE with zero initial value. Coefficients are
finite integrals of M times the bounded compact-head controls. Consequently
m0=m2=0, the controlled solution solves the ORIGINAL hard-sphere equation,
and its moments match M. Radial symmetry pays momentum automatically.

One must also prove positivity, since a signed solution alone is insufficient.
Here is a self-contained local identification argument. The uncontrolled
weighted linear row tends to zero relative to nu at large V, by the analytic
tail bound already proved. It is bounded on every compact speed region.
Choose a ball of radius2D around an already positive initial f=M+M^beta h.
Then nu_f<=nu+2D nu_beta<=(1+8D)nu. Put lambda=(1+8D)nu. The original
gain/loss Picard map for f is

    e^(-lambda t)f_initial+
    int_0^t e^(-lambda s)[Q^+(f,f)+(lambda-nu_f)f]ds.

For positive f in this2D-ball its integrand is nonnegative. In h variables,
the added diagonal lambda-nu is O(D); nonlinear Lipschitz size is O(D).
Split speeds at R: the raw linear row is arbitrarily small beyond R,
while on[0,R] its integral is O(t) since nu is bounded there. Thus for a
sufficiently small, explicit-in-principle time interval this map is a
contraction and maps the2D-ball into itself (start with the D-ball source).
Its iterates can be chosen positive throughout. The controlled global
solution, having zero moments, solves this same map and lies in its smaller
D-ball; local uniqueness identifies it with the positive solution. Repeating
the argument from each endpoint proves positivity for all finite times.
All integrals are justified by the D M^beta Gaussian domination. This
does not assume the standard positive solution already has that domination.

## 4. Bounded subcritical marked query

Scale z=h/D. At speed V with remaining time t draw Exp(nu(V)). If it
exceeds t, return z0(V). Otherwise, with remaining time reduced by the wait:

* Linear branch: with probability L(V)/nu(V), where L=int|Kc|, draw the
  child from |Kc|/L and multiply its answer by the kernel sign.
* Nonlinear gain: with probability D nu_beta/nu, sample w from
  M^beta(w)|v-w|/nu_beta, perform the actual elastic sphere collision,
  and multiply two independent answers at p,q.
* Nonlinear loss: with the same probability, sample that partner and return
  minus the product of independent answers at v,w.
* Otherwise return0.

All listed probabilities sum to at most eta+2D C_beta<1. Every result lies
in[-1,1]. First-event conditioning gives exactly the controlled mild map,
so contraction identifies the expectation with z_t(V). The expected number
of children is <=eta+4D C_beta<=199/200. Standard comparison with a
subcritical Galton--Watson process proves almost-sure finite tree and

    expected visited nodes <=200, uniformly in V and finite t.  (U2)

Short-circuiting a zero product only saves work. The signed mark is bounded,
not an unbounded importance mass. It is not itself a velocity output.

## 5. No hidden row or partner sampler

The kernel is explicitly computable; L need not be supplied as an integral
oracle. Use a positive envelope for the controlled radial kernel. Its gain
splits at s=V. For s<V omit only erf(s/sqrt2); sample squared radius from
the reversed truncated exponential proportional to exp[(1-beta)y/2] on
[0,V^2]. For s>=V the exact gain law is a tail-Rayleigh:
s^2=V^2+(2/beta)Exp(1). Their envelope masses, including the weighted
prefactor, are respectively

    E_low=4[1-exp(-(1-beta)V^2/2)]/[(1-beta)V],
    E_high=4erf(V/sqrt2)/(beta V),

with continuous limits at0. Loss is bounded by V+s and controls by
|a|+|c|s^2. Their Gaussian radial proposals are chi3,chi4,chi5 at variance
1/beta, with known masses. Native envelope rejection uses only
|k-a-cs^2| divided by this known positive envelope.

These samplers require only uniforms, exponentials, normals and elementary
functions. Half-integer chi laws are normal-square plus independent chi2
exponentials, so no new distribution oracle is hidden. For the certified
table the complete envelope mass E(V) obeys E/nu<48 uniformly; a separate
scalar bound checks the finite control maxima and analytic tail.

To choose the linear branch without knowing L, first choose the two
nonlinear events of total probability pQ=2D nu_beta/nu<=1/400. On their
complement use Huber's GENERAL linear Bernoulli factory. A native envelope
coin of mean L/[E+2nu(1-pQ)] is amplified by

    C=2+E/[nu(1-pQ)]<51,
    epsilon=1-eta(V)/(1-pQ)>=3/400.

This produces the required conditional probability L/[nu(1-pQ)]. Its
input coin samples the envelope or a known dummy-reject component; it uses
no evolved law. C>=2 keeps auxiliary geometric means bounded by2. The
ordinary Huber mean bound gives at most64,600 base coins per branch call.
After a linear branch is chosen, independently envelope-reject to sample
its child. The possibly small L does not cause hidden total infinite work:
branch probability L/nu times conditional mean E/L is E/nu<=48.

Nonlinear partners are sampled by a mixture of V times the beta Gaussian
and its speed-weighted law, accepting |v-w|/(V+|w|). Its mean proposals
are <=2. The actual incoming/outgoing cosines pay the hard-sphere angular
law, rather than replacing the rate by a Maxwell clock. Thus total ideal
primitive work per query has an explicit finite bound independent of t.
The conservative factory bound is large; practical superiority is not implied.

## 6. A paid equilibrium comparison from this same tree

The native nu(V)>=nu0=2sqrt(2/pi). The dominating time-oriented branching
process has expected offspring<=199/200, so its mean number of descendants
alive at age t is <=exp[-nu0 t/200]. A nonzero query must have some
descendant reaching the initial time boundary. Therefore

    |h_t(V)|<=D exp[-nu0 t/200],
    TV(f_t,M)<=D Z_beta exp[-nu0 t/200]/2.              (U3)

This supplies an actually paid ordinary approximate-equilibrium alternative.
The exact-observation consumer below must not claim a practical advantage
over simply using M at tolerances already paid by (U3).

## 7. Positive normalized finite-observation completion

Let a FINITE supplied partition (C_i) have known

    A_i=int_(C_i) M, B_i=int_(C_i) M^beta,
    A_i>D B_i for EVERY cell.                          (U4)

Also acquire conditional sampling of M^beta on each cell. These are initial
Gaussian/instrument calculations, not evolved-density values. Propose i
with probability (A_i+D B_i)/(1+D Z_beta). Draw V from M^beta restricted
to C_i, obtain the bounded query H_t(V), and accept with probability

    (A_i+B_i H_t(V))/(A_i+D B_i).

It lies in[0,1] on EVERY realization by (U4). Its expected numerator is
the TRUE cell probability int_(C_i)f_t. Accepted outputs are therefore
normalized iid observations of the exact hard-sphere solution. Expected
proposal count is1+D Z_beta<1.001. No evolved pointwise lower bound,
signed final output, self-normalized estimator or unpaid equilibrium
tolerance is used. This is an integrated positive completion, not a
claim that the intermediate signed density mark was already sufficient.

The executed source uses three radial cells[0,1],(1,2],(2,infinity). All
A_i,B_i and their positive margins are outward-certified Gaussian integrals.
Conditional beta radii are sampled by ordinary chi3 rejection; their
known probabilities pay every failed draw. More generally (U4) admits
arbitrary finite measurable detector partitions with acquired Gaussian
masses/conditional sampling; target information and source-smallness must
be supplied and charged.

## 8. Exact boundary

This closes uniform-time normalized iid output for the declared finite
OBSERVATION LAW. It does NOT close continuous full-velocity sampling or
every countable fine grid: tail cells can fail (U4). A sufficiently warm
global Gaussian lower envelope or a different positive representation
remains necessary for that stronger target, and is not granted here.
Only the source, radial model, smallness certificate, finite control table,
native kernel primitives and finite detector contract are consumed.
Finite-bit/validated ODE/physical model acquisition, historical novelty
and practical all-incumbent advantage are distinct, unacquired claims.
