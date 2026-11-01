# Independent proof receipt: continuous raw sign versus finite-jump clock

Audit date: 2026-11-01. Auditor: `producer-workspace/audit_sampled_clock_process`.

Frozen target:
`sampled_clock_process_pending_20261101/CONTINUOUS_SIGN_RECORD_OBSTRUCTION_ROOT.md`.
Target SHA-256:
`a3ab4f6296e256bc85bc779e3ac9fcadebd057f6c0fd5b981790963a09560222`.

**Verdict: PASS under the stated actual diffusion premises.** The precise
measurable witness and stopping-time proof are supplied below. This is a scope
obstruction for continuous raw sign observation; it does not invalidate the
accepted finite deterministic sampled-path theorem, and it does not rule out a
hysteretic basin-return approximation. The frozen target was not edited.

## 1. Honest model assumptions

On the observation horizon, assume an adapted continuous nonexplosive process
whose scalar coordinate satisfies the actual Itô equation

    Y_t = Y_0 + integral_0^t beta_u du + sigma W_t,

where sigma is a nonzero constant and W is Brownian motion for the underlying
usual filtration. In the diffusion setting beta_u may be b(X_u), depending on all
coordinates. Assume the drift is pathwise locally bounded near each finite time
along every relevant nonexplosive sample path. It is enough that the state-space
drift be locally bounded and the full continuous path be nonexplosive: a path on
a compact time interval then has compact range and hence a finite drift bound.

Take Y_0<0 almost surely and deterministic 0<T<infinity. Let

    tau = inf{t>=0 : Y_t=0}.

Continuity and adaptedness make tau a stopping time. The conclusion uses the
actual driving Brownian motion and its stopping-time property; a formal marginal
diffusion equation or a scalar correlation curve alone would not supply this.
No equilibrium, global mixing, reversibility, or spectral gap is needed here.

The assumptions are conditional receiving requirements, not established facts
about any unspecified hardware or unfinished concrete model. If drift is
singular at the interface, noise vanishes there, or explosion is allowed, the
argument must be reconsidered; none is silently admitted by this receipt.

## 2. Stopping-time Brownian oscillations dominate bounded drift

Put theta=tau wedge T. This is a bounded stopping time. By Brownian strong
Markov, the shifted process

    B_s = W_{theta+s}-W_theta, s>=0,

is Brownian motion. Its local law of the iterated logarithm holds almost surely:

    limsup_{s downarrow 0} B_s / sqrt(2s log log(1/s)) = 1,
    liminf_{s downarrow 0} B_s / sqrt(2s log log(1/s)) = -1.

Only sufficiently small s, for which the denominator is defined and positive,
are used. The theorem is a basic Brownian path fact, used here as a theorem, not
inferred from numerical simulations. The stopping at tau wedge T avoids any
issue with applying strong Markov on paths where tau is infinite.

On {tau<T}, theta=tau and Y_tau=0. Local boundedness gives random M<infinity and
delta>0 such that

    |integral_tau^{tau+s} beta_u du| <= M s,  0<s<delta.

Since

    s / sqrt(2s log log(1/s)) --> 0,

the same normalized limsup and liminf for Y_{tau+s}, after division by
|sigma|, are +1 and -1. (A negative sigma merely interchanges Brownian extrema.)
Consequently, on {tau<T}, every sufficiently small interval
`(tau,tau+epsilon)` contains a time with Y>0 and a time with Y<0, almost surely.

This is an almost-sure path assertion on the hit event; conditioning on {tau<T}
does not require an independence assumption about a future label record. In
particular, assigning either sign at zero cannot give the raw sign a right-hand
limit at tau, because the strictly positive and strictly negative values already
accumulate there.

## 3. Countably measurable separating event

Let L_t be +1 when Y_t>0 and -1 when Y_t<0. At Y_t=0 choose either binary value by
a measurable convention. The argument below is independent of that convention.
Let D be the countable set of rational times in (0,T), and compare the laws of
the rational record `(L_q)_{q in D}` on the standard product space `{+1,-1}^D`.
For every positive integer m define

    E_m = union over q_0<...<q_m in D of
          intersection_{j=1}^m {L_{q_j} != L_{q_{j-1}}}.

Define `E_infinity = intersection_{m>=1} E_m`. Each E_m is a countable union of
finite cylinder events. Thus E_infinity is measurable and says that arbitrarily
long alternating subsequences can be read on rational observation times.

To see that a hit gives this event, Section 2 supplies strictly positive and
strictly negative values arbitrarily close to tau from the right. Recursively
choose an alternating sequence of such values with times decreasing to tau.
For any finite initial portion, reverse its order to obtain an increasing
alternating list of times in (tau,T). At each selected time continuity gives an
open interval of the same strict sign. Choose ordered rational times in these
disjoint small intervals. Their labels alternate regardless of the value assigned
at zeros. This proves

    P_actual(E_infinity) >= P_actual(tau<T).

In fact, with Y_0<0 and the stipulated raw sign off zero, a path with no hit before
T has only negative rational labels, so this event has probability exactly
P(tau<T), up to the null set in the Brownian path theorem. The lower bound alone
is all the root needs.

This event avoids an uncountable union over random hit times and does not depend
on a disputed definition of a jump for the non-cadlag raw sign path. “Infinitely
many sign changes” is made precise by the alternating rational witnesses.

## 4. Finite-rate comparison and total variation

A homogeneous two-state CTMC with finite exit rates a and b has at most finitely
many jumps in [0,T] almost surely. For example, uniformization by rate
Lambda=max(a,b) bounds its actual jumps by a Poisson(Lambda T) event count; if
Lambda=0 there are no jumps. Its usual cadlag path with N jumps has at most N
alternations along any increasing sequence of observation times. Therefore

    P_CTMC(E_infinity) = 0.

The same conclusion holds for any comparison process separately known to have
finitely many jumps on compact intervals; merely saying a time-dependent rate is
finite at each individual time would not by itself prove nonexplosion.

With `TV(P,Q)=sup_E |P(E)-Q(E)|`, the rational record laws satisfy

    TV(actual rational sign record, CTMC rational record)
       >= P_actual(tau<T).

Any common full-record observation space whose sigma algebra includes rational
evaluations inherits this lower bound by projection/data processing. One must
not claim both records live in the usual cadlag path space D([0,T],{+1,-1}): on
the hit event the raw diffusion sign is not right-continuous and has no right
limit at tau. A common product-coordinate observation space, or just the
countable rational record space used above, is sufficient and fully rigorous.

No matching initial label law is necessary for this lower bound; the separating
event already has zero probability for every finite-jump comparison law.

## 5. Exact scope and retained distinctions

* If a separately earned estimate gives P(tau<T)>=c>0, the continuous-record TV
  error is at least c. This audit supplies no numerical lower bound for that hit
  probability and makes no hardware, timescale, or barrier-calibration claim.
* A fixed finite deterministic grid cannot witness E_infinity. Its projected
  distribution can therefore be accurately approximated even while the full
  record has the stated TV obstruction. Projection decreases TV, not the other
  way around. The accepted finite sampled-path theorem is unchanged; its
  resolution-dependent error is not a continuous-record certificate.
* A hysteretic last-visited-basin label with A={Y<=-b}, B={Y>=b}, b>0, is a
  different retained-state observable, requiring an initial retained label if
  the starting point lies in the slab. Consecutive label switches require
  coordinate travel of at least 2b. Uniform continuity of each continuous Y path
  on [0,T] then gives a positive pathwise minimum time needed to travel that
  distance; hence only finitely many such switches occur on the horizon. The
  raw-sign infinite-alternation obstruction does not transfer to this label.
  This proves neither exponential holding times nor independent renewals nor a
  Markov approximation for the hysteretic process.
* Positive-width slab omission, adaptive sampling after settling, and first-hit
  records likewise change the observable and need their own proof. They are not
  counterexamples to this raw-sign statement and are not certified by it.

## 6. Disposition and blockers

* Root obstruction: **no mathematical blocker** with the stated nondegenerate
  constant-noise, adapted continuous diffusion, locally bounded drift, and
  nonexplosion premises.
* Common observation space: **action** interpret the comparison on the countable
  rational record product space, or another space containing those evaluation
  events; **target** the full-record TV claim; **reason** raw sign is not cadlag
  after a hit; **outcome** the precise lower bound above is valid. This is a
  formalization of the root's “rich enough” observation-space clause, not a
  repair requiring an extra mixing hypothesis.
* Concrete order-one horizon: **action** separately establish the actual
  P(tau<T) bound and diffusion/model receipts; **target** any future numerical or
  physical application; **reason** the theorem is a conditional obstruction,
  not a hitting-probability computation; **outcome** left unclaimed here.

The earlier conditional finite sampled-path theorem remains frozen at SHA-256
`d1eb7f96cd68e1c681baa4907f888265dbd16a233096d9a345a53003d53e4979`.
No external retrieval, numerical evidence, helper agents, permission escalation,
denial, or retry was needed.
