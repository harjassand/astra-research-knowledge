# Unknown stationary Gibbs law: an all-target transfer and an earned path contract

Parent construction: `/root`. Independent derivation and audit:
`producer-workspace/computation_opening`. This note proves a parameter-transfer theorem
and specifies its computational observation contract. It asserts neither
historical novelty nor calibration of an actual physical source.

The reused Astra premise is the local-clamp/marked-refresh observation
contract in N1213, selectively read at Git revision
`51ce47ce39f976517d60e2f87bbe280b651f6056` of
`harjassand/astra-research-knowledge`, source
`research/2026-10-29-rare-means-and-finite-width/source/p1-final/ACQUISITION_SCIENCE.md`.
The accepted point-target theorem is not extended by assertion: the
coarse-target recrossing calculation and unknown-law transfer are supplied
separately below and in the parent's screened-lifetime proof.

## 1. All-target sensitivity for weights and positive cycle flows

Let Q be an irreducible generator on a finite state space, with strictly
positive, unnormalized invariant weights w. Set

    L=-Q,  D=diag(w)L,  Z=sum_x w_x.

The stationary directed edge flows F_xy=w_x q_xy are balanced. Thus D
has both zero row sums and zero column sums. Let nonnegative coefficients
a_c represent the directed flows as sums of directed cycle flows. The
cycle vertices can depend on the full outside configuration; no short
enumeration of all such cycles is assumed in this theorem.

For each cycle c, define

    B_c(f,g)=sum_(x->y in c) f_x (g_x-g_y),
    E_c(f)=B_c(f,f)=1/2 sum_(x->y in c) (f_x-f_y)^2.

Suppose every cycle has length between two and ell, so

    |B_c(f,g)| <= K sqrt(E_c(f) E_c(g)),
    K=csc(pi/ell) <= ell/2.

The formula for K follows by subtracting the cycle mean of f, applying
Cauchy--Schwarz and the ordinary cycle Poincare inequality. For lengths
two and three only, K=2/sqrt(3) is valid; K=7/6 is a safe rational choice
because (7/6)^2=49/36>4/3. The looser K=3/2 is valid as well.

Let a second model have positive weights what and cycle coefficients
ahat_c on the same cycle architecture. Assume

    exp(-u) w_x <= what_x <= exp(u) w_x for every x,
    exp(-v) a_c <= ahat_c <= exp(v) a_c for every c.

For every nonempty proper target A, put B=A^c and let

    M=E_(pi(.|B)) tau_A,
    Mhat=E_(pihat(.|B)) tauhat_A.

Then, simultaneously for every such A,

    exp(-3u)/F(v,K) <= Mhat/M <= exp(3u) F(v,K),

    F(v,K)=exp(2 asinh(K sinh(v/2))) <= exp(Kv).

In particular,

    |log(Mhat/M)| <= 3u+Kv.

The theorem does not need a spectral gap. A gap is separately needed for
the short-excursion computation and lifetime approximation.

### Proof: first compare flows at the same weights

Fix w, so the two balanced flows give generators with common pi=w/Z.
Let t,tstar be the true forward and adjoint hitting functions, let
mu=E_pi tau_A and C=1/mu. Let h=1-t/mu and hstar=1-tstar/mu.
Define hhat, Chat analogously for the fitted flow at these fixed weights.
All these potentials have pi mean zero and equal one on A.

The weak forward and adjoint equations on

    W={f:f|A=0, pi(f)=0}

give the exact identity

    Chat-C=<hstar,(Lhat-L)hhat>_pi.

The relevant energies are

    <hstar,L hstar>_pi=C,
    <hhat,Lhat hhat>_pi=Chat.

For each cycle, its coefficient ratio implies

    |ahat_c-a_c| <= 2 sinh(v/2) sqrt(a_c ahat_c).

Applying the individual cycle form bound, then Cauchy--Schwarz over cycles,
therefore yields

    |Chat-C| <= 2K sinh(v/2) sqrt(C Chat).

Set y=sqrt(Chat/C). Solving

    |y^2-1| <= 2K sinh(v/2) y

gives y between exp(-asinh(K sinh(v/2))) and its reciprocal. Hence both
Chat/C and its inverse Mhat/M lie between 1/F and F. This bound remains
valid for all finite v; it requires no K eta<1 restriction. For K=1 it
reduces exactly to the ordinary reversible conductance factor exp(v).
Finally asinh(K sinh(t))<=Kt for K>=1 and t>=0, giving F<=exp(Kv).

### Proof: now change weights while fixing the fitted flow

The killed directed Laplacian D_B is a nonsingular M-matrix, so its
inverse is entrywise nonnegative. With W_B=sum_(x in B) w_x,

    M = w_B^T D_B^(-1) w_B / W_B.

Indeed the hitting equation is D_B t_B=w_B. At fixed balanced D,
replacing w by what gives a valid generator diag(what)^(-1)D with
invariant weights what. Entrywise inverse positivity bounds its numerator
between exp(-2u) and exp(2u) times the original numerator; the denominator
is between exp(-u) and exp(u) times W_B. This costs exp(3u) in either
direction. Apply this weight comparison after the fixed-weight flow
comparison above. It works for arbitrary A and entails no long-time
trajectory-total-variation error proportional to M.

## 2. A rational binary path model with an explicit acquisition contract

Let x in {0,1}^n and

    w(x)=product_i a_i^(x_i) product_(i=1)^(n-1) b_i^(x_i x_(i+1)),
    a_i,b_i in [0.9,1.1].

The baseline gauge is w(0,...,0)=1. The source has two kinds of marked
local channels, with a known absolute clock scale:

1. Unit-rate single-site heatbath refresh. For neighbors l,r, the odds
   at i are r_i=a_i b_(i-1)^l b_i^r, with absent edge factors omitted.
   The fresh bit equals one with probability r_i/(1+r_i).
2. On adjacent bits i,i+1, a directed three-cycle
   00->01->11->00, leaving 10 unchanged. Its transition rate at local
   state z and adjacent outside boundary xi is alpha_i/v_i(z;xi),
   where v_i contains exactly all Gibbs factors touching those two bits.
   The positive alpha_i have a supplied bounded range, and a known local
   proposal bound permits uniformization. The marked proposal is allowed
   to be null at 10; only actual transitions enter the generator and flow.

For every fixed outside configuration, the stationary flow of each
directed three-cycle edge is alpha_i w_outside. Thus it is balanced and
the whole nonequilibrium generator has invariant distribution w/Z.

The acquisition contract is local clamping plus identified refresh or
cycle attempts. It is substantially more informative than an unmarked
black-box trajectory. It must be an actual interface of the implemented
source, not silently assumed for an arbitrary physical system.

### Heatbath observations and compatible reconstruction

For every i, hold its neighbors at zero and record independent marked
heatbath outputs. Their success probability q_i0 has odds a_i. For every
edge i,i+1, use site i with right neighbor one and every other neighbor
zero. The new odds are a_i b_i. From the empirical probabilities set

    ahat_i = qhat_i0/(1-qhat_i0),
    bhat_i = [qhat_i1/(1-qhat_i1)] / ahat_i.

This constructs one globally compatible Gibbs law. Independently fitted
conditional tables need not be compatible, so do not substitute them for
this factor reconstruction. The fitted values are rational when the
counts are rational. Clip empirical probabilities to a known safe rational
interior interval to define the estimates even on a bad sample event.

Suppose, simultaneously, each empirical success and failure probability
has relative error at most eta, with 0<eta<=1/2. Put t=-log(1-eta). Then

    |log(ahat_i/a_i)|<=2t,
    |log(bhat_i/b_i)|<=4t,
    |log(what(x)/w(x))|<=u=(6n-4)t  for every x.

The path factors keep both conditional outcomes above a fixed positive
probability rho; for example rho=2/5 is safe for the supplied interval.
There are H=2n-1 heatbath contexts. With N independent trials per context,
multiplicative Chernoff and a union bound give failure probability at most

    4H exp(-N rho eta^2/3).

Thus N>=3/(rho eta^2) log(4H/beta_h) suffices. These are explicit local
trials and their known clock/proposal costs, not observations of the rare
global target. If the source only offers a global marked uniformization
clock, waiting for the selected local channel costs an additional O(n)
proposal factor; it is still polynomial and must be charged.

### Directed-cycle observations

At local state 00, all touching factors in v_i are one, irrespective of
outside neighbors. The marked cycle rate is therefore alpha_i directly.
Use known-bound uniformization, with local bound Lambda0>=alpha_max:
an identified local attempt succeeds with probability alpha_i/Lambda0.
Its empirical frequency times Lambda0 is a rational estimator alphahat_i.
If alpha_i>=alpha_min>0, the same Chernoff calculation uses probability
floor alpha_min/Lambda0 and O(eta^-2 log(n/beta_c)) attempts per channel.
An enforced local reset to 00 or a marked candidate-clock mechanism is
part of this observation contract and its cost; neither is a rare global
reset. It must be provided explicitly by the source implementation.

On the simultaneous relative-error event,

    |log(alphahat_i/alpha_i)|<=t.

### Error in full-state flow coefficients

For a heatbath flip at i, write w0=w(x_i=0) and w1=w(x_i=1). Its
two-cycle stationary flow coefficient is

    c=w0 w1/(w0+w1).

This function is increasing in each argument and homogeneous of degree
one. The full-state weight bounds exp(-u)w<=what<=exp(u)w therefore
imply exp(-u)c<=chat<=exp(u)c directly. This improvement was supplied
by the complementary control agent. It supersedes a valid but looser
bound u+10t obtained by separately comparing w0 and the local odds.

For a directed three-cycle, c=alpha_i w_outside. Its touching Gibbs
factors cancel exactly from the stationary flow, so the coefficient log
error is at most u+t. Therefore a single safe bound for all cycles is

    v=u+t.

With the rational cycle constant K=7/6, the all-target theorem gives

    |log(Mhat/M)| <= 3u+(7/6)v.

Thus eta of order desired relative error divided by n suffices. There is
no inverse target-probability factor in these local acquisition counts.
The degree-two path and finite positive parameter ranges are essential
to the constant probability floor used above. A bounded-degree tree
uses the same edge reconstruction, u=(6n-4)t, and the same homogeneous
heatbath flow comparison; its probability floor depends on degree.

### Concrete Poisson-count contract and rational quantization

The parent's executed construction uses an equivalent, more explicit
observation interface: hold the local source state and its context fixed,
and return the count of identified candidate transitions over a known
exposure T. Under the source contract, the count has law Poisson(T lambda).
Both heatbath directions are observed separately, so odds are estimated
as the ratio of their rates. The same two context ratios recover a_i
and b_i. At pair state 00 the directed-cycle candidate rate is alpha_i.
There are 2(2n-1)+(n-1)=5n-3 counted rates. This marked candidate-clock
contract, including local clamping, must actually be implemented; ordinary
unmarked state observations do not automatically provide it.

Every true rate has lower bound 2/5 when a,b are in [0.9,1.1] and alpha
is in [0.5,1]. The empirical rate count/T is rational for integer T.
With eta<=1, Poisson Chernoff gives joint failure probability at most

    2(5n-3) exp[-T (2/5) eta^2/3].

For n=80, eta=1/10000 and T=16*10^9 this is less than 5*10^-7.
The physical-equivalent exposure 397 T is a real part of this contract's
cost; aggregated simulated count generation does not establish access to
that much physical observation time.

Compute all raw factor ratios first. Then clip a,b to [0.9,1.1] and alpha
to [0.5,1], and round each independently to the nearest multiple of
1/100000. Clipping cannot increase log error relative to a true parameter
inside the interval. Nearest rounding costs at most

    q=1/50000

in absolute log error, uniformly over these intervals. Form raw b from
the two raw context odds before quantizing a; otherwise b inherits an
extra quantization error from its denominator. Set the rational bound

    t=eta/(1-eta)=1/9999 >= -log(1-eta).

The final model then satisfies

    u=(6n-4)t+(2n-1)q,
    v=u+t+q,
    |log(Mhat/M)|<=3u+(7/6)v.

For n=80 the last rational quantity is approximately 0.21174318,
strictly below log(5/4). An elementary positive Taylor bound on exp of
that rational can certify the comparison without treating a floating
evaluation as the premise. Hence the learned source mean is within a
factor 5/4 for every nonempty proper target, on the single parameter
confidence event. The screened Monte Carlo and screening bias have their
own additional factors and failure probabilities.

Explicit rational arithmetic gives

    u=25389841/499950000,
    v=35347/694375,
    E=3u+(7/6)v=35287001/166650000.

The rational bound

    exp(E) <= sum_(j=0)^8 E^j/j! + [E^9/9!]/(1-E/10) < 5/4

was evaluated exactly; its numerical value is approximately 1.23583046.
For the data confidence, the rational lower Taylor sum
sum_(j=0)^32 (64/3)^j/j! in the denominator bounds
794 exp(-64/3) by less than 4.364*10^-7, hence less than 5*10^-7.

## 3. Exact rational counting and initialization for cylinder targets

Let A fix any specified subset S of bits to a specified pattern. This is
a cylinder event, not an arbitrary membership oracle. Define a mask
m_i(s) equal to one if bit s satisfies the pin at i, otherwise zero.
Forward messages on a path are

    F_1(s)=m_1(s) a_1^s,
    F_i(s)=m_i(s) a_i^s sum_(r=0,1) F_(i-1)(r) b_(i-1)^(r s).

Then Z_A=F_n(0)+F_n(1); remove the masks to obtain Z and p=Z_A/Z.
Sample the last bit proportional to F_n, then recursively sample the
previous bit r proportional to F_(i-1)(r)b_(i-1)^(r x_i).
This produces an exact sample from pi(.|A) in O(n) arithmetic operations.

All fitted parameters are rational. With parameter bit length B0,
message numerators and denominators have polynomial, O(n B0+n), bit
length after common-denominator representation. Their possibly
exponentially small normalized probabilities therefore do not require
an exponential number of bits. Exact sampling from a rational probability
uses ordinary random-integer generation/rejection with polynomial expected
bit cost. No rejection with success probability p is used.

For a tree, replace the path recursion by the ordinary two-state
sum-product messages from leaves to a root and sample downward. A single
count or pinned sample still uses O(n) arithmetic. Bounded degree and
bounded-size local moves keep the pattern enumeration below polynomial.

### Earn the stationary exit-flux law

For every local marked transition channel r, enumerate the bit pattern
sigma on its updated block and its neighboring boundary. The pattern
size is at most three for heatbath and four for an adjacent-pair cycle
on a path. Keep only patterns that are compatible with A before the
move and violate at least one target pin after the move.

For each retained descriptor d=(r,sigma), form the cylinder

    C_d=A intersect {local pattern=sigma}.

The channel rate q_d is constant on C_d. Its total stationary outward
flux weight is exactly

    W_d=q_d Z_(C_d)/Z.

Compute every Z_(C_d) by pinned sum-product. Choose d with probability
proportional to q_d Z_(C_d), sample x from pi(.|C_d), then apply the
specified transition to obtain y outside A. The resulting law is

    nu(y)=[sum_(x in A) pi(x)q_xy] / J,
    J=sum_d W_d.

Overlapping descriptors cause no error: they represent distinct outgoing
channel contributions, whose rates add in Q. Patterns with inconsistent
pins have zero weight and are discarded. There are O(n) descriptors on
a path, at most a fixed number per local channel. Naively computing all
their counts takes O(n^2) arithmetic; each later sample costs O(n).
For a bounded-degree tree the same procedure has
O(n^2 2^O(d)) preprocessing and O(n) sampling. All operations use the
fitted model and explicitly computed rational counts.

This earns the rare-target exit initialization required by the short
recrossing procedure. It is computational conditional initialization of
the acquired model, not experimental preparation of a rare physical state.

### Recrossing can be simulated with rational choices alone

The fitted factors remain inside the supplied ranges after clipping and
nearest rounding. Give each heatbath refresh channel proposal rate one
and each adjacent-pair directed channel proposal rate two. This bounds
the directed rate because alpha/v_local<=1/(0.9^5)<2. Add an independent
killing channel with rational rate s. The total proposal rate is

    Lambda= n+2(n-1)+s=3n-2+s.

Choose channels with their rational rate divided by Lambda. A heatbath
proposal samples the exact rational conditional bit law. A directed
proposal accepts its intended transition with probability
alpha/(2 v_local), respecting its null state. A killing proposal terminates
the recrossing with success. An actual transition into A terminates with
failure. Membership in a cylinder is directly evaluable.

Uniformization proves that the returned Bernoulli variable has exactly
the required probability P_nu(Exp(s)<tau_A). No floating exponential
waiting-time draw is required. The number of proposals is stochastically
bounded by a geometric variable with success probability s/Lambda, so
its expectation is at most Lambda/s. A cap of order
(Lambda/s) log(1/beta) gives an explicit rare runtime-failure event if a
strict finite runtime is required. The bit cost of every rational choice
is charged along with the proposal count.

### Boundary of the computational claim

The sensitivity theorem holds for every target A. The polynomial counting
and initialization claim holds for cylinder targets (or separately
specified target representations with efficient exact weighted counting
and conditional sampling). Arbitrary known membership is insufficient:
even uniform independent bits and a Boolean-circuit membership predicate
already contain general satisfying-assignment counting. Merely evaluating
membership does not earn either Z_A or the exit law.

## 4. What an executed fixture can and cannot establish

An executable simulated source may expose exactly the local marked
experiments above while withholding its parameters from the learner.
The learner can reconstruct rational factors and cycle coefficients from
returned counts, compute the cylinder partition and exit law, and run
the screened estimator. Full hidden parameters may then be used only by
a separate validation computation. That is a concrete test of the
acquisition/computation composition.

It does not establish that an external material, biological system or
device obeys this Gibbs/local-cycle model, permits these interventions,
has known clocks, or has the promised mixing bound. Those remain source
conditions. Ordinary methods receiving the same acquired local model can
reuse its rational messages, flow decomposition and certified recrossing
operation. No universal advantage over such an equally informed method
is claimed.

## 5. Independent exact finite checks

`verify_unknown_weights.py` checks the sharpened cycle perturbation and
the separate weight transfer on every nonempty proper target in twelve
finite examples of three through six states. The examples contain
positive two- and three-cycle flows with independently changed
coefficients and independently changed stationary weights, including
weights reduced by 2^-20. All 336 target checks passed in exact rational
arithmetic; results are in `unknown_weight_checks.json`.

The code avoids testing transcendental numbers as premises. For a
rational coefficient-ratio bound R>=1 and rational K=7/6, the fixed-weight
flow comparison is exactly equivalent to

    (Mhat/M-1)^2 <= K^2 (R-1)^2/R * (Mhat/M).

It checks that inequality rationally, then checks the inverse-positive
weight bounds separately. These finite checks support, rather than
replace, the all-target proof.
