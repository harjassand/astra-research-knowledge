# Ordinary physical suppliers for a prescribed invariant law

29 October 2026. Complementary physical-mechanism investigation within Astra P1.

This note establishes strong incumbent constructions and their actual interfaces.
The root's bounded excursion compiler is reviewed separately. None of the
ordinary time-change, trace-chain, Metropolis, or rejection-sampling principles
below is claimed as new. The useful comparison is exact capability under
specified actuation, observation, timing, and initialization resources.

## 1. Shared contract and the distinction being preserved

An actual native Markov kernel P on a standard Borel hidden state space is
reversible for a probability law mu. A finite visible label Y is noninvasively
readable. Apparatus memory affecting the next call belongs to the hidden state;
the contract is not inferred from equilibrium weights alone. The desired
endpoint law is nu(dx)=w(Y(x))mu(dx)/Z, Z=mu(w), with positive bounded w.
There is no granted microscopic copy, direct rollback, hold, or reinitialization
unless a construction explicitly adds it.

An invariant endpoint law does not supply an initial sample, convergence time,
or a law independent of the controller record. For repeated calls of a single
P, stopping rules alone leave the concatenated native path unchanged. The
selected macro endpoints can have law nu while raw native-step occupation has
law mu. This distinction is central, not an apparatus detail.

## 2. Particularly strong incumbent: marked endpoint acceptance

Scale w so a(y)=w(y)/w_max lies in [a_min,1], a_min>0. Starting at the current
physical state, take at least one native call. After each call, read Y and
accept the current endpoint with independent probability a(Y). If the mark
fails, continue P. Return the actual current hidden state at the first accepted
endpoint. No physical proposal is undone, no initial-state copy is needed,
and hidden memory may evolve arbitrarily subject to the reversible Markov
contract. Termination has the uniform tail Pr(tau>n)<= (1-a_min)^n.

Let A denote multiplication by a. The resulting endpoint kernel is

    K = P A + P(I-A)P A + P(I-A)P(I-A)P A + ... .

For a path x_0,...,x_n, the unnormalized starting flux under mu*a is

    mu(dx_0) a(x_0) P(x_0,dx_1) ... P(x_{n-1},dx_n)
       * product_{j=1}^{n-1}(1-a(x_j)) * a(x_n).

It is invariant under path reversal. Consequently K is reversible for
nu=mu*a/mu(a)=mu*w/Z. The sum is legitimate by the stated geometric tail.
This is also an immediate application of the ordinary watched-chain theorem
to the reversible augmented chain (X_n,U_n), U_n fresh uniform marks, watched
on U<=a(Y). The native state itself need not be observable.

In fact only native stationarity is needed for invariance: Kf=P(af)+P((1-a)Kf),
so integration against mu and subtraction give mu(aKf)=mu(af). This is exactly
Andral, Douc, Marival and Robert's 2024 Rejection Markov chain, Proposition1
and Theorem2. Their primary manuscript and the adjacent slice/correlated-mark
predecessors are recorded in PRIMARY_PREDECESSORS_AND_SCOPE.md. Reversibility
adds the stronger detailed-balance assertion but is not required for the
prescribed invariant law.

In a finite irreducible fixture, the mean native calls per accepted endpoint
at target equilibrium is 1/mu(a)=w_max/Z. More generally the same identity
holds for the invariant mixture obtained by weighting each closed component
by its acceptance intensity; arbitrary conserved-component initial weights
must be handled separately. Pointwise E_x tau<=1/a_min, but there is no finite
hard call cap. Per-call selectors, their exactness, reads and decisions cost
time and information. Exact real a(y) is not supplied by merely writing it.

For two equally weighted baseline labels, w_A=1,w_B=N, choose a_A=1/N,a_B=1.
The target-stationary mean is 2N/(N+1), exactly the mean of the root bounded
compiler. When N is a power of two, each A acceptance test has a literal
finite-fair-bit implementation. Its total number of tests/calls remains
unbounded. It works even when P cannot cross labels: it samples within each
unchanged component, and therefore does not manufacture the global target
component weights.

For an iid symmetric p-flip primitive its high-to-low and low-to-high
probabilities are

    K(A,B)=N p/[1+(N-1)p],
    K(B,A)=p/[1+(N-1)p].

The root bounded pair has K(A,B)=1-(1-p)^N, at least as large. The inequality
follows by representing this ordinary scheme's A horizon as a geometric H of
mean N and using E[(1-p)^H]>=(1-p)^N. This comparison is only the iid binary
case; no general spectral or efficiency improvement follows from it.

The root's general horizon/residual construction has an instructive relation
to this incumbent: geometric H has the same geometric residual law, while a
deterministic H=N uses the uniform equilibrium residual. The new scope to
assess is bounded stopping with full hidden detailed balance, not the broad
idea of programming an invariant law by selecting native endpoints.

## 3. Positive first-return mixture

Let R_y be the positive first-return kernel to the initial label set A_y.
When that return occurs almost surely, R_y is reversible for mu restricted
to A_y. This is ordinary trace/censored-chain theory. Choose before taking
any native path: execute one P call with probability b(y)>0; otherwise run
the positive first return R_y. Then

    K(x,.)=b(Y(x))P(x,.)+(1-b(Y(x)))R_{Y(x)}(x,.)

is reversible for mu/b(Y). For the P term, multiplying by mu/b cancels b.
Each R_y term is confined to A_y, where its coefficient is constant.
Thus b proportional to 1/w supplies the desired tilt. No hidden microscopic
restoration is needed. Finite stationary laws give almost-sure recurrence
for mu-almost every starting state; initial laws charging exceptional null
sets need their own premise. The bounded root construction needs no such
return assumption.

For a finite irreducible chain, Kac's formula gives

    E_{mu(.|A_y)} tau^+_{A_y}=1/mu(A_y).

Writing Z_b=sum_y mu(A_y)/b_y, the target-stationary mean native calls is

    [1 + sum_y (1-b_y)/b_y]/Z_b.

This can be small while pointwise cost is unbounded. For instance let native
states be a,b,c, with A={a,c}, B={b}, mu=(epsilon,1/2,1/2-epsilon), and
symmetric stationary flux epsilon/2 on edges a--b and b--c. The chain has
P(a,b)=1/2 and exit probability 2epsilon from b into A. Starting at a,

    E_a tau_A^+ = 1+1/(4epsilon),

although E_{mu(.|A)}tau_A^+=2. Stationary average cost is not a uniform
deployment guarantee.

## 4. Ordinary postproposal Metropolis repair: correct binary scope

Suppose the visible partition has exactly A,B, w_B>w_A, and r=w_A/w_B.
From A execute P. From B propose one P call. If it remains in B, stop.
If it enters A, accept with probability r; after rejection continue P until
the first return to B. Under almost-sure return the full microscopic kernel is

    K_AA=P_AA,                         K_AB=P_AB,
    K_BA=r P_BA,
    K_BB=P_BB+(1-r)P_BA(I-P_AA)^(-1)P_AB.

The last expression is the first-return path series, not a computational
inverse actuator. Every term in the B-return block is self-adjoint in mu_B.
The cross blocks balance after multiplying B mass by 1/r. Thus this ordinary
rejection repair is reversible for mu*w even with evolving hidden memory.
The rejected trajectory need not return to the original hidden microstate.

This corrects an initially attempted obstruction: 'only the visible bit
returns, so hidden memory necessarily invalidates Metropolis' is false in
this two-label reversible setting. Reversal of excursions is sufficient.
The premise also applies to an addressed binary site whose other visible
coordinates are truly fixed during its native excursion.

Its target-stationary mean is

    1+(w_B-w_A)mu(A)/[w_A mu(A)+w_B mu(B)].

For equal baseline masses this is 2w_B/(w_A+w_B)<2. In the frozen iid flip
model, the pointwise mean is at most2 and the endpoint mobility is the usual
p times Metropolis acceptance. In a general hidden model only the stated
stationary mean is controlled, and return tails can be arbitrarily long.

## 5. Actual failure of naive repair across more than two labels

Let mu be uniform on four native states 0,1,2,3. Native P has off-diagonal
probability1/4 on 0--1,0--2,2--3,3--1, and diagonal1/2. Visible labels are
A={0,1}, B={2}, C={3}; weights are w_A=3,w_B=2,w_C=1.

Try ordinary Metropolis acceptance after one actual proposal, followed on
rejection by first return to the original visible label. The induced kernel is

    [ 5/9    5/18   1/6   0    ]
    [11/36  11/18   0     1/12 ]
    [ 1/4    0      5/8   1/8  ]
    [ 0      1/4    1/4   1/2  ].

The desired nu=(1/3,1/3,2/9,1/9) obeys

    nu K-nu=(1/108,-1/108,0,0),

so is not invariant. The actual unique stationary law is
(183,168,120,58)/529. Its visible marginal differs from the desired marginal
by TV22/4761; hidden-state TV is82/4761. A rejected excursion leaving A through
B can return through C; its reversed path receives a different rejection
probability. The prechosen return mixture in Section3 and marked acceptance
in Section2 avoid this failure. The exact check reconstructs the algorithm
from first-hitting equations instead of assuming the displayed matrix.

## 6. Strong fixed-slot incumbent when a protected hold exists

Suppose an actual local P_i is mu-reversible and changes only visible bit i.
For target w(Y), write

    b_i(y)=min(1,w(y^i)/w(y)).

If an actual hold I of the same slot duration is available, prechoose P_i
with probability b_i(y) and I otherwise. The resulting

    K_i=b_i(Y)P_i+(1-b_i(Y))I

is reversible for mu*w: on each possible bit edge, w(y)b_i(y) is the same
at both endpoints. This implementation never makes a physical proposal that
must be rejected afterward. Unknown kinetics and evolving hidden memory are
allowed. It can program low-temperature or long-range Gibbs interactions
algebraically, while reads, energy evaluation, physical isolation, and mixing
remain real costs.

Full microscopic identity is stronger than needed. A rejected-slot kernel R
that preserves the entire visible label and is mu-reversible is sufficient.
Label preservation alone does not imply this conditional reversibility.
An isolated spectator device can supply a useful logical hold only if the
combined real operation has this required effect on the target device and
the full hidden contract. Extra hardware and isolation cannot be priced at0.

With dyadic energy ratios, selection uses finitely many known fair bits;
one native call or a real hold occupies each fixed slot. An empty word is
not a positive-duration hold. This incumbent removes the root's mandatory-
positive-call odds budget because the rejected branch makes zero target
native calls while real physical time still elapses.

## 7. A finite-rate physical gate gives a wall-clock stationary target

There is an elementary supplier when genuine on/off actuation is available.
Let Q be a native continuous-time generator reversible for mu; scale w>=1.
Introduce an observed controller gate g in {on,off}. In on, use Q; in off,
hold the physical system. Switch on->off at alpha(Y), off->on at beta(Y),
with alpha/beta=w-1. Then the joint generator is reversible for

    rho(dx,on)=mu(dx)/Z,
    rho(dx,off)=(w(Y)-1)mu(dx)/Z.

The x marginal is exactly mu*w/Z at arbitrary stationary wall time.
Native edge balance holds on the on layer; vertical gate balance holds by
the prescribed ratio. An off-layer mu-reversible generator preserving Y can
replace the full hold. Unknown Q rates never enter the selector calibration.

One bounded-rate choice is alpha=gamma(1-1/w), beta=gamma/w. Both are at most
gamma, but mean off durations w/gamma can be enormous. Values w=1 give zero
stationary off mass at those labels; scaling strictly above1 avoids that
degeneracy at additional holding cost. Gate generation, exact rates, sensing,
switching latency, and isolation are actual supplier requirements. This is
a direct physical time-change/auxiliary-state detailed-balance construction,
not a claimed new principle or a free improvement over the excursion method.

## 8. Actual baseline initialization remains a legitimate route

If an actual initializer supplies independent X~mu on each trial, rejection
with acceptance w(Y)/w_max gives an actual nu endpoint. Expected trials are
w_max/Z. This requires the stated fresh conditional sampling property, not
only an unconditional equilibrium marginal that may remain correlated with
old retained information. Initialization/replacement time, available locality,
hidden-sector change, actuator/sensor use, and randomization all count.

The accepted sample in ordinary iid rejection sampling is independent of
the number of failed trials and their values, but not of every possible
accepted-trial mark or sensor record. Marked-record claims must state which
record is compared. An initializer used for warranted baseline calibration
does not automatically have the deployment locality/latency required by a
local physical Gibbs program. Its existence is nevertheless not excluded by
a theorem about a smaller native menu.

## 9. Conserved hidden classes and conditional histories

If all available operations preserve a hidden class C, its initial weights
remain unchanged. A class with baseline mu_c converges, if it converges, to
mu_c*w/mu_c(w). Global mu*w instead assigns class weights proportional to
mu(C)mu_c(w). Equal initial class weights generally do not become those
weights. This limitation applies to hold, gating, marked acceptance, and
return constructions as well as to the root bounded compiler.

Example: two unchanged equal-weight classes have baseline Pr(Y=1)=1/4,3/4.
Their aggregate visible baseline is uniform. With w(1)/w(0)=3, the separate
tilted means are1/2,9/10, giving7/10 under unchanged equal class weights.
The desired global tilt has mean3/4 and needs class weights3/8,5/8.

A useful sufficient condition is a common baseline visible distribution
in every accessible class. Then every class has the same visible tilted
target, so conditional class weights selected by an old record do not matter
after appropriate within-class convergence. That convergence, its uniformity,
and its timing are additional hypotheses. Calibration-dependent selection of
individually valid kernels does not make the initial law conditional on the
calibration record stationary. Retaining controller records never erases this
distinction.

## 10. Comparison received by the bounded compiler

The incumbent closest to the bounded compiler at its stated coarse interface
is marked endpoint acceptance: it already tolerates arbitrary reversible
hidden memory, needs neither hold nor return to a microscopic state, and has
the same target-stationary native-call mean in the binary example. Its missing
property is the deterministic native-call cap. Positive first-return mixtures
and binary rejected-excursion Metropolis are further exact ordinary choices
with potentially small mean cost and unbounded tails. Protected holds, actual
rate control, and fresh initializers add real resources and can be preferable.

The root's bounded construction has a specific mathematical advantage over
those no-hold incumbents: every actual branch finishes within N native calls,
without sacrificing microscopic reversibility of the prescribed tilt, while
not claiming autonomy of timing, full records, physical-time occupation, or
finite-time preparation. The separate odds-budget proof shows that a ratioN
is sharp for one unknown iid symmetric source when every branch must take
between1 andN native calls. Exact-equilibrium control is a useful task even
though it does not learn or cancel the native kinetic dependence.

Primary-source comparisons and exact rational checks are saved beside this
note. No hardware experiment, broad priority claim, or practical speedup has
been established.
