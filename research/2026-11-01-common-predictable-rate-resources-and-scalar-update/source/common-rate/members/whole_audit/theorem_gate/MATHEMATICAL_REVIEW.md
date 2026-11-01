# Independent review: common predictable positive-box construction

## Verdict, dependencies and scope

**PASS, theorem and mathematical receiving joins only.** The accepted new source
is `COMMON_PREDICTABLE_BOX_THEOREM.md`, SHA256
`d53758d6f0a7f311e4a3d06e38882b113680ea5604f74f4e4132d17b8542c7de`, bound by author
manifest `16c0b44e613b2b779422ac81c7356d6b31ed61f47180d8ad177154527bfe9a44`.
All 22 manifest-listed file hashes matched. Exact input snapshots and separately
accepted base-theorem/Pbar receipts are recorded in `INPUT_BINDINGS.json`.
The fixed-rate and Pbar proofs are dependencies, not a prior acceptance of this
controlled result. I independently checked the new endpoint choices and the
conditional, resource, risk-ledger and observation joins below.

No author module or test was imported/run. Reading implementation declarations
and checking frozen bytes does not approve the parser, guard, ledger, serializer,
receiver or whole executable. This receipt concerns their mathematical contracts,
not whether those contracts are correctly implemented or physically realized.

The process means the usual pure-jump reaction counting construction: a firing
uses one listed channel and its listed increment; the stipulated predictable
intensities are compensators relative to the full working filtration. No extra
unmodelled state jumps, simultaneous batches with a different generator, or
anticipating access to future driving events are added by this verdict. Merely
assigning individual marginal rates to a different joint-jump process would not
earn L_k. Rate changes themselves are not reaction firings. These are the
ordinary generator/intensity premises of the source, made explicit here.

## 1. One common source inequality really follows from the box

The function, its face weights and every scalar through the final tilt are fixed
from the whole raw box, not recomputed on each policy/state. The graph and positive
lower bounds stay fixed. Its actual independent-face sum is the same finite sum
as in the accepted base theorem; Pbar is only a scalar ceiling.

For a selected bulk arm, every enabled arm has the required resource increment
and the actual sum of forward coefficients is at least k_-. Thus the lower g is
valid without choosing a favorable individual arm. At a selected hub, favorable
amplification has coefficient at least b_-, while the sum of all potentially
adverse reverse-arm coefficients is at most s_+. With M>=12s_+/b_- and M>=2,

  q^M>=2,  s_+(q^2-1)<=5s_+/(2M)<=5b_-/24.

The grouped favorable margin is at least b_-/2-5b_-/24>b_-/4. Source-group
convexity may therefore be applied separately to *each actual vector* with the
same lower margin and the same integral profile. This earns g and h0 uniformly;
it is not an inference that stability of endpoints implies a common function.

All discarded/unselected positive terms instead use upper rates: a_+, k_+, s_+,
and mu_+. The death-profile jump is still -2M, including last-copy death; its
positive cost is at most 18mu_+ M A D_J. The remaining tilted death baseline is
nonpositive. Immigration uses the actual monotone profile increment and is at
most lambda_+ eps Z_J. Hence the displayed local inequality has exactly the
required lower/upper split.

The accepted subset-transfer proof is then uniform because every coefficient
in it is the just-established *common* coefficient. Its negative reserve S
uses g,h0; its positive costs use CA,CH. T and K pay the same quarter budgets.
The transfer reaches a strictly smaller independent set; no state-dependent
face is inserted into Psi. Its terminal positive sums use P<=Pbar. The actual
face cover and sstar are unaffected by the choice of rates within the box.

## 2. Death and inactive-state compatibility

For B0=1-e A/(N+1), death's negative tilted baseline is at most
-(1-e)mu_-(1-1/t)A=-(1-e)DA, while its positive angular contribution is at most
e mu_+. Forward internal losses cost at most e Fwd A and reverse amplification
supplies at least 2e b_- Q/(N+1). Since e<=1/4 and
 e Fwd <=D/4, the remaining A dissipation is at least D/2. Also

  e mu_+ <= mu_- mu_+ eps/4 <=mu_+^2 eps/4.

Thus the different endpoints in D, CA, Cbirth and the baseline inequality are
compatible; substituting one rate endpoint everywhere would not establish this.

At Z0, neither source nor target of an internal reaction permits an entry/exit:
all sources are disabled there and every internal target is active. Immigration
is the only enabled transition. Keeping its **same actual coefficient** on both
terms gives

  L_k^t h <=lambda_actual[eps(1+Psi)-H]
          <=lambda_actual[eps(1+Pbar)-H]
          =-lambda_actual <=-lambda_-.

This cancellation is essential. Separately bounding the positive term by
lambda_+ and the negative term by lambda_- would generally be too weak. The
source explicitly avoids that invalid step.

Only true A=1 death can enter Z0. The actual independent support face, present
in the unmodified sum, gives S>=g(N-1)dA. The threshold uses mu_+ H, not mu_- H,
and pays the whole adverse mu_actual H/t. The dA bound is the accepted uniform
integral lower bound 1/[8(3M+1)^2]; acquiring it does not evaluate q^M.

The remaining Nstar thresholds pay RA, RQ and the two interior cover alternatives
with D and b_- exactly as displayed. The face alternative has upper drift
 eps*Cbirth-sstar/4 <=-3sstar/16. Therefore nu=min(lambda_-,1,sstar/8)>0 is a
common negative constant on N>=Nstar. Since 3/4<=h<=Htot,
L_k W<=-zeta W there. Inside N<Nstar, all possible destinations have N<=Nstar
and the total intensity is at most lambda_++mu_+ Nstar+S_+ Nstar^2. The displayed
C, with its additional factor t, conservatively bounds L_k W+zeta W.
All these are pointwise inequalities for every k in the box.

## 3. Nonexplosion and conditional receiving after a stopping time

Bounded immigration intensity gives finitely many immigration events on each
finite horizon, by thinning or stopped compensator expectation. Pathwise,
 N(s)<=N(0)+I(s). All internal jumps conserve total count and true death lowers
it. On a finite random count sublevel, finitely many channels have uniformly
bounded intensities. Stopping first at that sublevel and then at the m-th firing,
compensator expectation rules out infinitely many firings in finite time.
Infinitely many predictable changes of rate coefficients do not change this
argument; their computational cost is outside the firing-count contract.

For an a.s. finite stopping time tau, shift the counting-process compensator
identities to (tau,tau+u]. The shifted coefficients are predictable for the
shifted filtration, and their bounds are unchanged. The common drift inequality
therefore holds after conditioning on F_tau. One can first restrict to events
where tau and N(tau) are bounded, localize at count/firing sublevels, and then use
conditional Fatou. No Markov or strong-Markov assumption is needed.

For a fixed finite u, the convenient nonnegative integrating-factor process on
0<=s<=u is

  exp(zeta*s) W(X(tau+s))
       +(C/zeta)[exp(zeta*u)-exp(zeta*s)].

Its localized drift is nonpositive. Its initial value and its value at u give
exactly (A), including the factor 1-exp(-zeta*u). Taking the lower bound
W>=3t^N/4 and the upper bound W(tau)<=Htot*t^N(tau) gives (B).
Conditional statements hold almost surely for the stated stopping time/history,
not as assertions about arbitrary conditional laws on null histories. An
unconditional finite initial moment yields the stated unconditional bound; a
finite realized count state still makes the conditional right side finite even
when the unconditioned initial exponential moment is infinite.

For a finite horizon T, W(X(tau+s))+C(T-s) is nonnegative with nonpositive
localized drift on [0,T]. Stop also at sigma=inf{s>=0:N(tau+s)>=R}. On sigma<=T,
W is at least 3t^R/4. Optional stopping plus Fatou gives (C). If the initial count
already reaches R, the clipped bound is 1, as it must be. This is not a bound on
the maximum over an infinite future.

## 4. Exact Poisson comparison, including the stopped exit jump

Stop the reaction firing count at sigma, including a firing at sigma if one
causes the exit. Up to that firing its pre-jump count is below R, so its total
intensity is bounded by
 Lambda_R=lambda_++mu_+ R+S_+ R^2.
The stopped predictable intensity can be written using 1_{s<=sigma}; no
independence between exit and count is assumed. On the event sigma>T, the full
and stopped firing counts agree.

Here is a direct proof of the exact Poisson-tail comparison in (D), which avoids
any informal independence or coupling premise. Let J be the stopped simple
counting process with intensity a_s<=Lambda_R, and for a fixed integer m put

  f(s,j)=P{j+Poisson(Lambda_R*(T-s))>=m}.

This is a bounded increasing function of j and solves
 partial_s f=-Lambda_R[f(s,j+1)-f(s,j)].
Its predictable drift along J is
 (a_s-Lambda_R)[f(s,j+1)-f(s,j)]<=0.
Conditional optional stopping (or bounded localization) therefore gives

  P{J_T>=m | F_tau}<=P{Poisson(Lambda_R*T)>=m}.

Thinning is another valid proof. An exponential-mgf supermartingale alone gives
the dyadic Chernoff cap below, but **mgf order by itself is not an inference of
all exact Poisson-tail inequalities**. The source's parenthetical shorthand is
read with the valid thinning route, or with the explicit bounded-function proof
above; this receipt does not use that invalid inference.

The union for actual firings is contained in {sigma<=T} union {J_stopped>=m},
which proves (D). The joint count/firing violation in (E) has this same union,
so the exit probability is charged once, not twice. Identically labelled copies
of the same reaction have total intensity equal to the summed intensity and
one firing per actual channel event. Their labels need not be discarded in the
count: aggregation does not turn several events into a single counted event.

## 5. Actual integer caps and their bit cost

Let beta=alpha/2. With a received integer U>=N(tau), write C=c0*t^(Nstar+1) and
L=max(U,Nstar+1). The two numerator terms in (C) are at most
 [Htot+c0*T]t^L. For block=ceil(1/eps), Bernoulli gives t^block>=2. Choosing the
least nonnegative k with
 2^k >= (4/3)(Htot+c0*T)/beta
and R_F=L+block*k makes the count-exit bound at most beta. No huge power is
expanded. When T=0, the vanished C*T term permits L=U; k is retained, so this
does not mistakenly set R_F=U and charge an event that already occurs at time 0.

For v>=0, exp(v)<=2^(2ceil(v)), because 2 log(2)>1. Markov's inequality for
2^Poisson(v) gives the displayed threshold
 m(v,beta)=2ceil(v)+ceil_log2(1/beta)
with P{Poisson(v)>=m}<=beta. The same cap follows directly for the stopped
count from its exponential compensator. Because beta<1/2, these thresholds are
strictly positive even for v=0.

Pathwise N<=U+immigration count gives the independently valid R_P. Both R_F and
R_P are fixed from the history at tau, so selecting their smaller value selects
one valid bound; it neither incurs a union penalty nor differentiates a minimum
of Lyapunov functions. The firing intensity bound is then recomputed at this
selected R. One beta for exit and one beta for stopped firings prove (E).

For an explicit ordinary binary input box, all common expanded scalars retain
the polynomial-bit argument of the accepted Pbar corollary. A lower endpoint may
be 2^(-L) and M may be exponentially large, but M has O(L) bits and dA is
fixed-degree rational. Pbar has O(L^2) bits; the remaining fixed formulas,
including c0, have polynomially many bits. C itself remains a factored power.

Add the bit lengths of U, rational T and alpha to the input cost. Ratios for k
have polynomially many bits; k is obtained with bit lengths and one dyadic
comparison. Its numerical value is bounded by those bit lengths. The integer
block can have huge numerical value but polynomial bit length. Thus R_F, R_P,
Lambda_R and the firing threshold all have polynomial bit length and can be
acquired with ordinary polynomial-time integer/rational arithmetic. This does
not charge a unit-cost huge real operation, expand t^U, or enumerate faces.
It does not assert practicality of the resulting numbers.

Independent reconstruction from the frozen raw fixture obtains count level 24
and firing level 116462 at U=10,T=1,alpha=1/100. Immigration still wins at
T=2^1121; the common-Foster candidate wins at T=2^1122. These neighboring dyadic
checks reproduce the reported comparison, not a claim about an exact continuous
crossover or operational usefulness. An enormous time horizon is still enormous
when its binary representation is short.

## 6. Adaptive overlapping episodes and exact risk accounting

For rational, finite F_tau-measurable horizon/confidence choices and an integer
received count bound, parameter tuples have countably many values. The fixed-
parameter conditional inequalities therefore extend by restriction to the
corresponding F_tau events; no independence, reset or new stationary sample is
needed. Later rate choices may continue using the entire record as long as their
actual intensities remain predictable and inside the same box.

For each actual episode j, P(E_j|F_(tau_j))<=alpha_j. The stopping times need not
separate episode intervals; overlapping episodes are allowed. Tower, countable
subadditivity and Tonelli for nonnegative allocations give

  P(union_j E_j)<=sum_j E alpha_j=E(sum_j alpha_j)<=alpha_total.

The pathwise sum premise is crucial. A risk reservation made only after seeing
future violation is not a history-measurable start-time allocation. Nor does a
rejected reservation authorize an episode. A ledger invariant spent<=total,
with only positive accepted rational increments, proves the required sum bound
for every finite prefix and then by monotone convergence for countably many
reservations. Rejection must leave that invariant intact. The arithmetic
contract is sound; I have not approved the supplied class as its implementation.
Memory/time to maintain an unbounded ledger is not free, and finite-horizon caps
may grow across episodes. No finite cap on the infinite-future maximum follows.

## 7. Narrow observation contract is sufficient, but must be real

The proof uses the current state only to establish the model's actual drift.
The external budget interface can replace W(X(tau)) by Htot*t^U for any actual
F_tau-measurable U>=N(tau); it need not evaluate Psi or observe all coordinates.
Since internal reactions conserve N and true death decreases N,
 N(tau)<=U0+I(tau0,tau]
pathwise from a valid initial bound. Ignoring deaths is conservative. The count
I must cover **actual successful** immigrations through the episode start,
including appropriate boundary-time coverage; a received upper bound is enough.
Commanded injections or incomplete detection are not a proof of this inequality.
An unmodelled externally forced state jump is not a rate selection in the stated
model. If the observation enclosure itself fails with positive probability, that
failure would need a separate risk charge; the present theorem assumes the
received enclosure is true, rather than earning sensor/calibration guarantees.

The same distinction applies to actions: an interval-checked numeric vector does
not certify a physical intensity mapping or future predictability. Rejected
commands retaining the previous admitted vector preserve the mathematical rate
box, but no claim about actual hardware follows from that API rule.

## 8. Evidence and exclusions

`independent_box_checks.py` imports no author code and runs no simulation. It
checks exact worst-rate endpoint suprema of the local-source and B0 inequalities
on two independently generated small models; actual inactive cancellation;
separated positive endpoint formulas through 2^(-512) and 2^512; all payment
thresholds; independent resource-cap arithmetic from the frozen raw fixture;
exact rational log ceilings; and finite path-dependent risk-allocation branches.
`CHECK_RESULTS.json` records **4,046 successful assertions**. The uniform proof
above, not these finite tests, earns arbitrary states, histories and horizons.

No invariant distribution, recurrence under arbitrary nonstationary control,
all-tilt moments, infinite-future maximum, independent trials, actuator calibration,
sensor completeness, controller/observation cost, operational use, or novelty is
accepted. No external retrieval, denied-source retry, escalation or physical
chemistry/biology occurred. No mathematical blocker was found. Whole executable
acceptance remains a separate boundary.
