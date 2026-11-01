# One acquired resource certificate for predictable rate changes

**New author construction, whole review pending.** This is a mathematical
controlled count-process result. It asserts neither positive recurrence nor an
invariant law for a nonstationary/history-dependent controlled process. It makes
no physical calibration, actuator or operational claim.

## Result first

For the square-free reversible binary one-port architecture below and a raw
strictly positive rational channel-rate box, finite scalar formulas acquire a
single state function W, constants zeta>0 and C<infinity, and t>1 such that

    L_k W(x) <= -zeta W(x)+C

for **every state and every rate vector k in the box**. The same W works under
arbitrary predictable, possibly record-dependent selection of those rate vectors.
Consequently conditional exponential-count moments, finite-horizon maximum-count
tails and reaction-firing-count tails are controlled from any continuing-history
stopping time. No stationary-fiber law, reset, independent success trial or
unverified average service assumption occurs.

The acquisition uses ordinary common-Lyapunov reasoning, source-group convexity,
finite proper-subset absorption and conditional Dynkin/compensator arguments.
The new issue checked here is compatibility of all lower/upper channel bounds
in the actual face/inactive-state construction—not a deduction from separately
stable fixed-rate processes. Historical novelty is not asserted.

## 1. Model and actual admissibility obligation

Species are A and n>=2 satellites. There is a nonempty simple hub graph with E
edges. Every hub X_i+X_j has 2A<->X_i+X_j. Every other internal pair has form
A+X_k<->X_i+X_j; every satellite has at least one such arm. The only
nonconservative pair is 0<->A. All internal jumps conserve total count N.

For each directed channel r, the raw data contain exact bounds

    0 < lower_r <= upper_r < infinity.

Repeated channels may be combined by summing endpoints. At time s the predictable
rate coefficient k_r(s) must actually belong to this interval, almost surely
(ds times probability); the intensity is k_r(s)*(X(s-))_(source_r), using the
falling-factorial convention. Coefficients may depend on the entire observed
past, extra adapted randomness, state and time. No Markov or stationary policy,
independence between coefficients, or positive dwell time between choices is
required. Predictability excludes choosing using future random events.

These are *model-level* admissible actions: the exact intensity mapping earns the
bound when a requested vector is admitted. `RateGuard` starts at interval midpoints;
it admits a rational vector only if every coordinate is in its canonical channel
interval. A rejected request **keeps the previous admitted vector**—it does not
turn reactions off or stop the count dynamics. An arbitrary actuator label,
empirical estimate or calibration claim is not accepted as a bounded intensity.
If a different action-to-intensity mapping is used, its enclosure must separately
be proved. The guard does not infer predictability from a vector or certify
physical rates. Its code is an ordinary trusted in-process API, not a security
boundary against mutation of private implementation state.

Write lambda_-,lambda_+ for immigration bounds and mu_-,mu_+ for death coefficient
bounds. The strictly positive lower immigration bound is used at fully inactive
states; mu_- supplies drain dissipation. Lower channel bounds are not silently
allowed to be zero. Unsupported boxes are outside this certificate, not declared
unstable.

## 2. Worst-case constants, acquired without circular dependence

From the raw box acquire

    a+ = sum of forward 2A->hub upper rates,
    b- = min of hub->2A lower rates,
    s+ = max_hub sum of ALL outgoing hub upper rates,
    k- = min_satellite sum of outgoing A+X_i arm lower rates,
    k+ = max_satellite sum of outgoing A+X_i arm upper rates,
    S+ = sum of all directed internal upper rates.

All are positive and finite. Define, in this order,

    M=max(2,ceil(12s+/b-)), q=1+1/M, aw=2M, Ww=2M+2,
    g=k-*(1-q^-2)/(q-1), h0=b-/[4(q-1)],
    Cstep=(4M+4)*3^6,
    CA=Cstep*(a++k+)+18mu_+ M, CH=Cstep*s+,
    d=1/[8(3M+3)^2],
    T=max(1,ceil(4CA/g),ceil(4CH E/h0)),
    B=1+nT, R=(B+1)^2/d,
    K=max(2,ceil(4*2^n*CH*R/h0)), Pbar=(K+1)^n,
    RA=Pbar*CA*(B+1), RQ=Pbar*CH*(B+1)^2.

The exact common multiplier contains ALL nonempty independent satellite sets I:

    J_I=2M*A+(2M+2)*NearMass_I+(M+1)*FarMass_I,
    Z_j=(1-q^(-(j+M)))/(j+M), D_j=Z_j-Z_(j+1),
    w_I=K^(n-|I|), Psi=sum_I w_I Z_(J_I).

Near means graph neighbors of I; Far is outside I and Near. Only independent I
are used. The binomial upper bound sum_I w_I <=Pbar avoids enumerating them for
scalar acquisition; it does not replace the actual sum by profiles on non-independent
sets. Evaluation may still enumerate up to 2^n-1 sets.

Use the already acquired finite face-cover constants

    delta=1/4, eta=delta/(4n), hh=eta^(n-1)/(2n),
    epsC=min(1/4,hh^2/2,hh/8), gamma=delta*hh/8,
    sstar=min(g,h0)*d*epsC/4.

Only now choose the tilt and final constants:

    Cbirth=lambda_+*(1+Pbar)+mu_+^2/4,
    eps=min(1,sstar/(16*Cbirth)), t=1+eps,
    D=mu_-*(1-1/t), Fwd=2a++k+,
    e=min(1/4,D/[4(Fwd+1)]), H=1+eps*(1+Pbar),
    dA=1/[8(3M+1)^2].

Choose Nstar as the ceiling of the maximum of

    2,
    4RA/D,
    RQ/(e*b-),
    1+4mu_+ H/(g*dA),
    4(Cbirth*eps+1)/(D*gamma),
    2(Cbirth*eps+1)/(e*b-*gamma^2).

Finally set

    nu=min(lambda_-,1,sstar/8), Htot=1+Pbar+H,
    zeta=nu/Htot,
    C=(zeta+lambda_++mu_+ Nstar+S+ Nstar^2)*Htot*t^(Nstar+1).

These formulas are acyclic. In particular e uses mu_- for dissipation, CA and the
last-death threshold use mu_+, and inactive negativity uses lambda_- rather than
incorrectly substituting lambda_+ everywhere. Scalar rational bit costs are
polynomial in the explicit input length by the same fixed-formula/binomial
argument as the bound Pbar. C is an exact **factored power**, not a polynomial-
size expanded numerical constant. No numerical usefulness of this enormous bound
is claimed merely because its expression is compact.

## 3. Uniform source and subset inequality

For a fixed admissible vector k, write L_k^t f=t^-N L_k(t^N f). All bounds below
are uniform in that vector. At a bulk arm A+X_i with i in I, every destination
increases J_I by at least 2, with total forward coefficient at least k-. At a
hub having one I endpoint, or both endpoints Far, its source resource is 2M+2.
Amplification increases J by 2M-2>=M with coefficient at least b-; only reverse
arms to I can lower J, and their decrement is 2. Their total adverse coefficient
is at most s+. Since q^M>=2 and s+(q^2-1)<=5s+/(2M)<=5b-/24, every such
source group has the same positive gap >=b-/4. Thus the completely monotone
integral Z_j=integral_[1/q,1] z^(j+M-1) dz gives the negative reserves g and h0
uniformly over the entire channel box. No individual reverse channel is assumed
favorable.

All other internal increments obey |Delta J|<=4M+4 and are bounded using Cstep,
a+,k+,s+. Actual death contributes at most 18mu_+ M A D_J after discarding its
negative tilted baseline. Immigration satisfies Z_(J+2M)<=Z_J and costs at most
lambda_+ eps Z_J. Thus, with U_I=A+outside-I mass, F_I=inside-I mass,

    L_k^t Z_I <= lambda_+ eps Z_I-r_I
                 +CA*A*(U_I+1)*D_I+CH*Qbad_I*D_I,
    r_I=[g*A*F_I+h0*(Qcross_I+Qfar_I)]*D_I,
    d/(U_I+1)^2 <= D_I <= 1/(U_I+1)^2.

Here Qcross is the sum of products for I--Near edges; Qfar is Far--Far; Qbad
contains the remaining hubs, outside I with at least one Near endpoint.

For completeness, the global absorption is unchanged but is now common to all
k. At each state put J={i in I:x_i>=T(U_I+1)}. If J is nonempty, own capture
pays the CA term with <=g*A*F_I*D_I/4. Bad hubs touching Near(J) charge cross
hubs with product ratio <=1/T and multiplicity at most E, costing at most
h0*Qcross_I*D_I/4. These two payments together consume at most r_I/4. The remaining bad hubs have both endpoints Far(J). When nonempty they
transfer to a STRICT subset J of I, with U_J<=B(U_I+1) and D_I<=R D_J. A
receiving J has at most 2^n strict supersets, each of weight <=w_J/K, so all its
incoming transfers consume <=w_J*r_J/4. When J is empty, N<=B(U_I+1); residuals
are bounded by CA(B+1)A/(N+1)+CH(B+1)^2 Q/(N+1)^2. Summing therefore gives

    L_k^t Psi <=lambda_+ eps Psi-S/2
                +RA*A/(N+1)+RQ*Q/(N+1)^2,
    S=sum_I w_I*r_I.

This is one actual global inequality. Analysis selects a subset to prove it;
the multiplier itself has fixed weights, with no switching selector or cutoff.

The finite prefix-gap cover yields either A>gamma N, a hub with both endpoint
counts>gamma N, or an independent I with U_I=0 or
A F_I+Qcross_I+Qfar_I>=epsC U_I^2. Briefly, a ratio-gap prefix at scale eta
has minimum >=hh times the relevant available mass; an internal edge already
gives the bulk alternative. Otherwise the prefix is independent. Failure of
activation forces most outside mass into Far, where another ratio-gap prefix
must be independent, or its edge contradicts failure. Add this Far prefix. Its
outside-to-minimum ratio stays <=3delta/8. Each failure adds a vertex, so at
most n stages finish. This is the same finite selector proved in the byte-bound
base theorem. On an active face state, integer U_I>=1 and hence S>=sstar.

## 4. Death, immigration and the common inactive join

Let Z0={A=0,Q=0} and B0=1-e*A/(N+1). A direct channel calculation gives, uniformly,

    L_k^t B0 <=lambda_+ eps+e*mu_+ -(D/2)A
               -2e*b-*Q/(N+1).

Death's negative baseline is at least -(1-e)D A; its positive angular term is
<=e*mu_+. A-decreasing forward internal channels cost <=e*Fwd*A, absorbed by
the chosen e. Reverse amplification supplies the displayed Q term. Immigration's
angular increment is nonpositive. Finally

    e*mu_+ <= mu_-*mu_+*eps/4 <=mu_+^2*eps/4.

Set h=B0+Psi+H*1_Z0 and W=t^N h. Then 3/4<=h<=Htot. Internal jumps can neither
enter nor leave Z0: every product is an active binary complex and every source
is disabled on Z0. Immigration leaves Z0. At such a state it is essential to
keep its ACTUAL coefficient through the cancellation:

    L_k^t h <=lambda_actual*[eps*(1+Pbar)-H]
             =-lambda_actual <=-lambda_-.

Using unrelated upper/lower endpoints on the two terms separately would lose
this valid cancellation. The only positive indicator entry is A=1 death with
independent satellite support. That support is one included face, J_I=2M and
A F_I=N-1. Thus S>=g(N-1)D_(2M)>=g(N-1)dA, which pays its full cost
mu_actual H/t<=mu_+ H with S/4 once the stated head is exceeded.

After residual absorption, active states N>=Nstar obey

    L_k^t h <=eps*Cbirth -(D/4)A-e*b-*Q/(N+1)-S/4.

The face case is <=-3sstar/16. The two interior alternatives give <=-1 using the
corresponding head thresholds. Together with inactivity,

    L_k^t h <=-nu for all N>=Nstar and ALL k in the box.

Therefore L_k W<=-zeta W outside the head. Inside it, every possible destination
has total at most Nstar and total channel intensity is at most
lambda_++mu_+ Nstar+S+ Nstar^2. The displayed factored C safely bounds
L_k W+zeta W there. This proves the common global inequality.

## 5. Controlled-process receiving without a stationary or reset premise

Use any filtered probability space carrying the counting-process construction
with the predictable intensities in Section1. Immigration is dominated pathwise
by a homogeneous rate-lambda_+ Poisson clock through thinning. Hence
N(s)<=N(0)+B_+(s). On every finite horizon, this bounds N on a finite random
sublevel; all channel rates there are bounded. The process is nonexplosive even
if the controller makes arbitrarily many predictable coefficient changes. We
are bounding reaction firings, not the computational cost of controller decisions.

For localized stopped processes, the conditional compensator identity gives
Dynkin's formula with L_(k(s)) W. The common drift inequality holds for every
predictable choice. Applying the integrating factor and then conditional Fatou
along finite-sublevel localization gives, for every a.s. finite stopping time tau
and every deterministic u>=0,

 E[W(X(tau+u)) | F_tau]
 <= exp(-zeta*u) W(X(tau))+(C/zeta)*(1-exp(-zeta*u)).       (A)

No strong-Markov property is used: apply the same predictable compensator and
localization after tau, condition on F_tau, and use tower/conditional Fatou. For
random initial distributions, the unconditional bound holds when E W(X0)<infinity;
otherwise the corresponding extended conditional inequality remains the useful
finite-state statement. Because W is finite at every finite count state, (A)
works from the continuing realized history, including a history-selected tau.

In particular

 E[t^N(tau+u) | F_tau]
 <=(4/3)*[Htot*exp(-zeta*u)*t^N(tau)
           +(C/zeta)*(1-exp(-zeta*u))].                  (B)

This supplies a uniform-in-time moment bound, not an invariant distribution.
A nonstationary controller need not have one; none is asserted. A moment bound
for each time is not a bound on the maximum over all future time: even an
unbounded irreducible positive-recurrent autonomous specialization may eventually
visit arbitrarily large count levels.

For deterministic Htime>=0 and integer Rlevel>=0, stop additionally at the first
time N>=Rlevel. Since L W<=C, the process W(s)+C*(Htime-s) up to this bounded
horizon is a nonnegative local supermartingale, hence a supermartingale after
localization/Fatou. At the exit W>=3*t^Rlevel/4. Optional stopping yields

 P{sup_(0<=u<=Htime) N(tau+u)>=Rlevel | F_tau}
 <= min(1,(4/3)*t^(-Rlevel)*[Htot*t^N(tau)+C*Htime]).     (C)

This is a conditional finite-horizon resource tail with linear horizon cost. It
is not a time-uniform infinite-horizon maximum bound. It remains valid after
any previous accepted action or prior threshold crossing; no state reset occurs.

Let J_H count reaction firings during (tau,tau+Htime]. Before the above exit,
total intensity is bounded by the acquired scalar

    Lambda_R=lambda_++mu_+*Rlevel+S+*Rlevel^2.

A further stopped thinning clock (or the exponential counting-process
supermartingale) gives stochastic domination of the stopped firing count by
Poisson(Lambda_R*Htime), conditionally on F_tau. The stopping time may depend on
that clock; independence of the exit event is NOT assumed. A union bound gives

 P{J_H>=m | F_tau} <= min(1, RHS_unclipped(C)
                          + P{Poisson(Lambda_R*Htime)>=m}). (D)

One can use the clipped probability bound from (C) in (D) as well. This controls
actual reaction firings, including separately labelled identical channels before aggregation;
it does not bound arbitrary controller computations, observation overhead or
physical resource use not represented by these counts. Poisson tails are standard
one-dimensional quantities and can be evaluated with rigorous numerical budgets
or left as exact distribution expressions. No hidden fiber calculation occurs.

## 6. Acquisition, receiving, comparisons and limits

`common_box.py` performs a raw positive-box shape scan and acquires all scalars
without independent-set enumeration. It includes a same-author canonical
receiver, the admitted-rate guard, a finite sum evaluator with separate mask,
exponent and rational-power-bit budgets, and an exact statewise maximizer over
the channel box. The latter uses linearity in rates: each channel coefficient
chooses its upper endpoint when positive and lower endpoint when negative.
Thus endpoint testing need not enumerate 2^(number of channels) vectors, and
its witness is an actual admitted adversarial state-dependent action.

The common inequality is analytic, not inferred from a simulation or finite
corner tests. A rejected quantitative evaluation preserves structural admission;
a request outside the box is rejected and the previous valid rates stay active.
The raw support and rates are mathematically acquired, not supplied as a useful
Lyapunov/decomposition oracle. Full multiplier evaluation may still be exponential
in satellite number and enormous in count/rate bit complexity. Factored tail
expressions do not imply a small practically useful numerical bound.

Common Foster functions for switching processes and conditional drift/optional
stopping are ordinary strong comparators. A fixed-rate invariant law, pointwise
recurrence theorem, queue stationary law or independently chosen per-policy
Lyapunov function would not by itself establish the single inequality used here.
This construction supplies it for the explicit class and box. No claim is made
for switching reactions off, changing architecture, unbounded rates, unverified
actuators, arbitrary weakly reversible networks, all exponential moments, or
historical novelty. An identified autonomous Markov specialization may separately
receive recurrence conclusions; this controlled theorem does not assign them.

The underlying face theorem dc96226443a99ee0a8541f03cce5af28ff735a95c6855053d223cf87d5001327
and separate Pbar corollary are retained as reusable proof capital, not edited.
Their independent acceptance status and this new extension's status are separate.
No external source retrieval, upload, operational chemical/biological work, or
previously blocked-source retry was used in this extension.

## 7. Actual integer budget acquisition, and the ordinary stronger short-horizon cap

The tail expressions need not be left as unevaluated formulas. For rational
failure probability alpha in (0,1), assign alpha/2 to maximum count and alpha/2
to firing count. Let C=c0*t^(Nstar+1), where c0 is the computed rational
`CF_prefactor`. For any received F_tau-measurable upper bound N0>=N(tau), and
Ttime>=0, put

    L=max(N0,Nstar+1),
    block=ceil(1/eps),
    k=ceil_log2( (4/3)*(Htot+c0*Ttime)/(alpha/2) ),
    R_F=L+block*k.

Use a nonnegative logarithm ceiling (zero when its argument is <=1); it is
computed by rational bit lengths and a power-of-two comparison. Bernoulli's
inequality gives t^block>=1+block*eps>=2. Hence (C) is <=alpha/2 at R_F without
expanding t^L or the huge final bound. When Ttime=0, L=N0 is enough.

**Ordinary comparator retained:** immigration alone gives
max_(u<=Ttime) N(tau+u)<=N0+Poisson(lambda_+*Ttime). This generally provides a far
sharper short-horizon bound than the enormous Foster constants. For v>=0,
E[2^Poisson(v)]=exp(v)<=2^(2ceil(v)); therefore the acquired integer

    m(v,beta)=2ceil(v)+ceil_log2(1/beta)

has upper-tail probability <=beta. Set R_P=N0+m(lambda_+*Ttime,alpha/2) and
choose R=min(R_F,R_P). Each candidate is separately justified, so selecting the
smaller numerical cap preserves the guarantee. This is not an unjustified
minimum of state Lyapunov functions. The common Foster cap grows logarithmically
in horizon after its large fixed head; the immigration cap grows linearly.
Neither dominates numerically for every instance/horizon.

With Lambda_R from (D), acquire m=m(Lambda_R*Ttime,alpha/2). Then

 P{max_(u<=Ttime) N(tau+u)>=R OR J_Ttime>=m | F_tau}<=alpha. (E)

The union is charged only once: on the event of no count exit, the full firing
count equals the stopped firing count. Hence its probability is bounded by the
count-exit probability plus the stopped-firing tail, not twice the exit cost.
The Poisson bound for stopped firings can equivalently be proved directly by
the exponential compensator E[2^J_stopped]<=exp(Lambda_R*Ttime), so (E) does not
require an independent stopping clock or a hidden conditional distribution law.
The count/event budgets are actual binary integers. Their lengths and the scalar
arithmetic to compute them are polynomial in the raw box input, N0, rational
horizon and rational confidence input lengths. They may have astronomically large
values. Computing them enumerates no independent sets and expands none of the
profile powers or t^(Nstar+1). Exact full W/drift evaluation remains separately
costed and potentially exponential. `resource_budget` reports which count cap
was used and the Bernoulli/dyadic receipts for independent checking.

## 8. Repeated adaptive episodes: no reset and no free repeated risk budget

A fixed per-episode confidence alpha must not be reused indefinitely while
claiming the same all-history failure probability. Let tau_j be an actual sequence
of a.s. finite stopping times. At tau_j choose a finite rational horizon T_j and
rational alpha_j>0, both measurable from the history then available, and acquire
(E)'s budget from the current count N(tau_j). For such history-measurable choices,
the conditional proof applies by conditioning/approximation; it does not require
a reset or a fresh stationary draw. Let E_j be that episode's stated budget
violation. If the admitted risk allocations satisfy

    sum_j alpha_j <= alpha_total <1   almost surely,

then tower and the countable union bound give

    P(union_j E_j) <= sum_j E[P(E_j | F_tau_j)]
                    <= E[sum_j alpha_j] <=alpha_total.

Episodes may overlap and rates may use the entire earlier record; independence
is not needed. `RiskLedger` earns the allocation inequality in the model API by
reserving positive rational risk before an episode and refusing an overspend
without changing the prior ledger. It does not infer that an external episode
actually used an admitted allocation. The physical/model controller must keep the
same admitted rate-box obligation throughout every episode. There is no bound on
unreceived episodes or on controller overhead. Across infinitely many episodes,
the acquired count levels need not remain bounded: nothing here implies a finite
cap on the infinite-future maximum of an unbounded irreducible chain.

## 9. Narrow resource-observation interface

Budget acquisition needs only an actually received, history-measurable bound
U_tau>=N(tau), because W(X(tau))<=Htot*t^U_tau. Replace t^N(tau) by t^U_tau in
(B),(C), and use N0=U_tau in Sections7–8. It need not evaluate Psi, observe the
full species vector, or observe every fast internal firing. The controlled model
still has its actual hidden state and the stipulated mass-action intensities;
partial observation by the controller does not change that model contract.

There is a particularly narrow mass-accounting route. From a received initial
bound U0>=N(tau0), let I(tau0,tau] count ACTUAL successful immigration events.
Internal channels preserve N and death lowers it, so pathwise

    N(tau)<=U0+I(tau0,tau] .

A received upper bound on I suffices as well. An observation ledger must cover
all such arrivals through the claimed start time tau; missing a real arrival can
make its bound invalid. Commanded injections, detected-but-incomplete streams,
or a bare integer labeled an observation are not automatically actual-count
receipts. Instrumentation, detection completeness, timestamps/coverage and any
action-to-rate enclosure are separate obligations. This mathematical package
does not certify them. The API field is explicitly `initial_total_upper_bound`,
and its same-author arithmetic receiver validates the resulting budget, not the
truth of an external observation. Unobserved deaths only improve a valid upper
bound. Thus full fast-reaction monitoring is not an implicit cost or premise,
but the much narrower immigration-count/initial-bound contract is not free.
