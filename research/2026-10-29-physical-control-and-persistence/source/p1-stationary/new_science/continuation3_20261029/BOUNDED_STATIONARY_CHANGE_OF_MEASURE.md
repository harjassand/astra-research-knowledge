# A bounded stationary change of measure on the current physical state

29 October 2026. Astra P1, root construction and governing proof.

## 1. Result and scope

An unknown stationary Markov operation can be turned into an actual endpoint
operation with a prescribed stationary reweighting, without learning its
transition probabilities or representing its hidden predictive state. A
finite counter supplies a deterministic cap on native calls. When the native
stationary law is unique, the construction attains the minimum possible mean
native-call count at stationarity; reducible sources require the componentwise
qualification below. Its universal cap is sharp as well.

Every output is the current physical state. The controller reads only its
visible weight; it does not copy a microstate, restore a stored state, or
select a hypothetical future. Hidden memory may evolve and the native
dynamics need not be reversible. If it is reversible, symmetrizing the
counter direction makes the compiled kernel reversible for the new law.

The result changes the invariant law at **operation-completion indices**.
It is not a reset from an arbitrary start, an independent sampler, a rapid
mixing theorem, or a change in the single native operation's physical-time
occupation. Sensing, timing, selection, preparation and actuation retain
their actual costs.

The closest ordinary incumbent is Bernoulli endpoint thinning, equivalently
watching an augmented chain on a subset. It has the same target and the same
stationary mean cost, but generally has an unbounded, geometrically dominated
native-call tail. It lacks a universal deterministic cap. The counter supplies
that cap without increasing the stationary mean.
Watched chains, importance thinning, occupation identities and Metropolis
are established mathematics. The candidate addition is this bounded physical
implementation, its matching limits, hidden-state scope and composition.
Historical priority for the complete assembly is not established here.

## 2. Actual interface

The microscopic state x is in a standard Borel space X. A fixed executable
native call has Markov kernel P and stationary probability measure mu:

    mu P = mu.                                      (1)

Neither P nor x need be known to the controller. A noninvasive label Y(x)
supplies a positive integer weight W(Y). Let m=min W, M=max W, Z=mu(W).
The intended invariant law is

    nu(dx)=W(Y(x))mu(dx)/Z.                          (2)

The extreme weights have positive mu mass for the sharpness statements.
Safe bounds suffice to execute the controller, but loose bounds need not be
optimal. Rational target weights can be scaled to positive integers.

Hidden bath/apparatus memory affecting the next call must be included in X;
the full operation must satisfy(1). Repeated calls use the same specimen.
There is no required hidden reset, mixing, finite state space, visible
Markov model, or independently prepared baseline between calls. Noninvasive
boundary sensing and compatible computation/switching must actually be
supplied or included in the native operation. Unknown evolution during
decision latency cannot be omitted.

The controller has the stated integer selectors, arithmetic and endpoint
reads. No physical hold, zero-call branch, rollback, microscopic readout,
direct output actuator or independent stationary initialization is assumed.
Stationarity in(1) is an exact premise, not established for an unrestricted
hidden system by finite equilibrium observations.

## 3. Literal controller and native-call cap

Starting at a visible weight w:

1. Draw C uniformly from {0,...,w-1}.
2. Choose d=+1, or choose an independent fair sign d in{+1,-1} if reversible
   output is wanted from a reversible native P.
3. Execute one actual P call and set C=(C+d*m) modulo M.
4. Read the new weight w'. Stop and output the current physical state if
   C<w'; otherwise repeat step3, with the same counter and direction.

All paths finish, with

    1 <= tau <= L=ceil(M/m).                         (3)

For the forward direction, the first wrap lands in{0,...,m-1}, which is
accepted for every state, within L calls. For the backward direction,
decrements reach that set within L calls, possibly after an initial wrap.
This is a pathwise bound, independent of hidden rates and memory.

Uniform integer selection is an actual resource. Fair-bit rejection sampling
for w>1 uses fewer than2ceil(log2 w) bits on average, but has unbounded worst
randomizer time when w is not a power of two. If every W is a power of two,
phase selection uses exactly log2 w bits; symmetrization adds one bit.
Counter storage needs O(log M) bits. Exact rational weights therefore have
a finite native-call cap, but not automatically a deterministic randomizer
or wall-time cap. The complementary unknown iid symmetric binary-source proof
supplies a separate, slower bounded-bit fallback for arbitrary rational ratios;
that fallback has not been transferred to arbitrary evolving hidden kernels.

To turn(3) into a physical-time deadline requires actual bounded native-call,
read, arithmetic and switching durations compatible with the kernel. All
intermediate labels, counter/selector values and completion times may be
retained. The endpoint theorem does not assert independence from them.

## 4. Stationarity proof

Fix d and add the counter c in Z/MZ. The augmented native kernel is

    Q_d((x,c),dy dc')=P(x,dy)1_{c'=c+d*m mod M}.

It has stationary measure mu_tilde=mu times Uniform(Z/MZ). Let

    A={(x,c):c<W(Y(x))},       a=mu_tilde(A)=Z/M.

The normalized restriction to A is

    nu_tilde(dx,c)=mu(dx)1_{c<W(Y(x))}/Z.             (4)

Its x marginal is nu and its conditional counter is exactly the initial
phase draw. The loop is the positive first-return kernel R_d of Q_d to A.
Every counter orbit reaches the universally accepted interval within L calls.
Writing B=A^c, the killed block is nilpotent, Q_BB^L=0, and

    R_d=Q_AA+Q_AB(I+Q_BB+...+Q_BB^(L-1))Q_BA.        (5)

The finite trajectory sum is stochastic. The B-block stationarity equation
solves for mu_tilde|B using that finite inverse; substituting into the A
equation shows nu_tilde R_d=nu_tilde. This is the usual watched-chain
identity with a constructed set having a deterministic return cap.

Starting x at nu and drawing its conditional phase creates nu_tilde.
The loop preserves that law, and forgetting the phase returns an x with
law nu. A fresh conditional phase each macro yields a Markov kernel K_d on
the complete microscopic state. The visible process need not be Markov.
No actual microscopic enumeration or evaluation of(5) is required.

## 5. Reversibility and physical parity

If P is mu-reversible, Q_+^*=Q_- in L2(mu_tilde). Reversing each return path
in(5) gives R_+^*=R_- in L2(nu_tilde). Conditional phase sampling and
forgetting are adjoints for nu and nu_tilde. Therefore

    K_+^*=K_-,       K=(K_++K_-)/2 is nu-reversible.  (6)

Only the controller counter direction is reversed; the apparatus applies
the same actual P. For nonreversible P, invariance remains true but averaging
counter signs does not generally remove native currents.

If P^*=Theta P Theta for a mu-preserving microscopic involution Theta and
W is Theta-even, the same argument gives K^*=Theta K Theta. This generalized
reversal also requires a full actual kernel contract. Off-diagonal rate
ratios alone do not justify ignoring odd variables, escape rates or reversed
external controls. No actual Theta actuator is used in the construction.

## 6. Exact occupation and stationary mean cost

At a macro start distributed as nu, with its conditional phase, the expected
pre-call occupation measure on the augmented space is

    E[sum_{j=0}^{tau-1}1_{(X_j,C_j) in dz}]
       =mu_tilde(dz)/a.                            (7)

A is occupied only initially. B occupation is the initial restricted
measure times Q_AB(I-Q_BB)^(-1), which the B-block stationarity equation
identifies as mu_tilde|B/a. The inverse is a finite polynomial. Thus

    E_nu[sum_{j=0}^{tau-1}1_{X_j in dx}]=(M/Z)mu(dx),
    E_nu tau=M/Z.                                  (8)

These are stationary-epoch identities, not all-start mean bounds. The latter
are supplied only by the hard cap L. In a balanced binary baseline with
relative weight r, the stationary mean is2r/(1+r)<2. That does not remove
slow preparation, rare long runs, apparatus overhead or mixing barriers.

### Optimal stationary mean

Let P have unique stationary probability mu. Any causal stopped-current-state
controller using only successive P calls and independent seeds, with tau>=1,
finite E_nu tau and endpoint law nu when started at nu, has finite occupation
measure Lambda satisfying

    Lambda P-Lambda=Law(X_tau)-Law(X_0)=0.

This follows by the Markov property on{tau>j}, telescoping and finite expected
length. Uniqueness implies Lambda=c mu, c=E_nu tau. The mandatory first
pre-call state contributes nu, so Lambda>=nu. Hence

    E_nu tau>=ess sup_mu(dnu/dmu)=M/Z.               (9)

The compiler attains this lower bound exactly, even against a controller
that knows P. With multiple invariant components the bound is componentwise;
one may not infer this global optimality merely from one chosen invariant mu.
For example P=I, mu=(1/2,1/2), W=(1,2) permits a one-call identity costing1,
while this counter costs4/3. The target remains invariant in both cases.
A true zero-call hold, output overwrite, or another operation menu changes
the resource interface. Bernoulli thinning with acceptance W/M also attains
(9); the counter supplies the bounded tail at the same stationary mean.

## 7. Sharp universal call cap

Let Q be a finite irreducible stochastic matrix with stationary law mu.
The unknown family P_p=(1-p)I+pQ, p in an open subinterval of(0,1), shares mu.
Suppose the same controller, without p as input, always uses1..L calls and
preserves nu proportional to mu W for every p. Its endpoint K_p is a
polynomial of degree at most L. On the p=0 unchanged-state path let t_x be
its seed-averaged number of calls. Then1<=t_x<=L and

    K'_0=diag(t_x)(Q-I).                            (10)

To first order there is one use of the Q part: before it the controller
follows its unchanged-state prefix, and afterwards no further Q event moves
the state. This also counts Q self-transitions correctly. Polynomial identity
extends invariance from the physical interval to0, giving

    nu diag(t_x)(Q-I)=0.

Uniqueness of the left stationary vector of Q implies
nu(x)t_x=c mu(x), hence t_x=cZ/W(x). Therefore

    max W/min W <= L.                              (11)

A universal hard cap is at least ceil(M/m), attained by(3). Choosing Q
reversible proves sharpness even in that restricted class. The minimum
stationary mean and the minimum universal cap are attained simultaneously.

This is a one-unknown-kernel, endpoint-observation theorem. It is not a bound
for known-p control, arbitrary extra actuators, continuous between-call
observations, or the full source-B menu. Finite calibration selecting a fixed
controller does not prove an exact identity uniformly over unknown p;
approximate alternatives remain available.

## 8. Connection to the actual binary excursion

For W(A)=1,W(B)=N and forward direction, an A start stops at the first B
endpoint or N calls. From B, after the first step into A the remaining
budget is uniform in{0,...,N-1}; stop on return to B or budget exhaustion.
This is precisely the complete kernel in
BOUNDED_REVERSIBLE_EXCURSION_COMPILER.md, developed from the constructive
binary pair supplied by the existing record-geometry helper. Its block proof
and exact diagonal, clock and local-composition checks are retained.

The binary block proof needs only mu P=mu for invariance, using
mu_B P_BA=mu_A(I-P_AA); reversibility adds the adjoint conclusion. Uniform
phase makes the two counter directions give the same binary endpoint kernel.
For the preserved symmetric unknown iid flip p,

    K(A,B)=1-(1-p)^N,    K(B,A)=[1-(1-p)^N]/N.

Its ratio is fixed, while mobility remains unknown. This respects the
signed-continuation obstruction to a nonzero constant transition probability.
With p continuously distributed and frozen, covariance eigenvalue
(1+1/N)(1-p)^N-1/N gives positive Hankel matrices of every order. Exact target
invariance thus coexists with infinite linear predictive rank.

## 9. Interacting physical programs and acquisition

Supply local actual kernels P_i sharing stationary mu and preserving every
visible coordinate except i. In each fixed local context, compile using
the desired local relative weights. Every K_i preserves nu_W proportional
to W(Y)mu. Reversible P_i and symmetric counter signs give reversible K_i.
Prescribed scans or independent state-independent random scans preserve
nu_W; arbitrary history-selected schedules are not justified.

This implements positive rational local factor weights. Integer energies in
units log2 give literal power-of-two selectors, with native-call cap
2^(maximum local energy difference). With bounded local energy range this
does not grow with the number of sites. The square-lattice Ising weight at
coupling log2 uses local ratios1,16,256, at most8 phase bits and native-call
cap256. Its two-label special case needs no direction bit. Strong interaction
and phase coexistence do not break the invariant-law identity; they can
still make preparation exponentially slow.

Addressability, isolation, common stationarity, noninvasive reads, compatible
timing and selectors must be physically supplied. There is no apparatus
claim here. Frozen conserved-sector weights also remain unchanged. Common
baseline visible laws in each sector plus within-sector convergence can
give the same visible target without hidden mixing; otherwise correct target
sector weights or another actual intervention are required. The explicit
7/10-versus3/4 failure is retained in the excursion proof.

Kinetic calibration may select a faster member of a warranted common
stationary/reversible family and freeze that choice before deployment.
Estimation error then need not enter the target ratio, although the actual
conditional start, sector weights and throughput remain affected. The same
selected operation must respect each local context and both directions of
its edge. No preparation or confidence coverage is inferred from invariance.

The visible target is proportional to W(y)mu(Y=y). If that baseline measure
is estimated, compensation requires its actual finite confidence bound.
Finite data do not prove hidden stationarity or apparatus correctness.
A uniform full-operational-state/history per-call coupling error e gives
one compiled endpoint error at most Le, plus separately counted selector
and controller error. It does not supply long-time phase-observable accuracy.
Even coherent vanishing field errors can select a phase; energy-density
accuracy and magnetization accuracy are different objectives.

At stationary macro starts,(8) restores native-step occupation mu. Repeating
one P back-to-back has not changed its native path. A local network changes
the schedule of subsequent actuation but still has a distinct physical-time
law. A protected hold, isolated spectator, initialization, waiting and
per-device calibration remain strong real alternatives at their supplied
interfaces. All clock, apparatus and retained-record claims keep that scope.

