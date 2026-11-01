# Independent conditional proof: stationary full-transition intensity

Date: 2026-11-01. Auditor: `producer-workspace/audit_sampled_clock_process`.

This receipt audits the proposed count identity supplied in the task discussion;
there was no frozen count-identity source file when it was assigned. It does not
approve any unfinished concrete global current, trial, model, or preparation.
No existing source was edited. No external retrieval, helper agents, numerical
evidence, or hardware claim is involved.

## Verdict and exact receiving interface

**PASS as the conditional theorem below.** Reversibility and a stationary base
law alone are not a license to omit the past-visit, energy-domain, or boundary
regularity premises. The proof is ordinary capacity/reactive-flux and Itô
machinery, not a novelty claim or an assumption of renewal statistics.

Let X be a continuous, conservative diffusion with invariant probability
`pi=m/Ztot`, Ztot finite, and generator G. Define its carré du champ by

    Gamma(g) = (G(g^2)-2g Gg)/2.

Let A and B be disjoint closed basins, separated by positive distance in the
concrete use, and set S=(A union B)^c. Assume:

1. A two-sided stationary reversible realization exists, and its past contains a
   visit to A union B almost surely before every finite observation time. It is
   enough to receive stationary ergodicity and positive pi mass for the basins;
   the two-sided ergodic theorem then gives past visits. An actual positive-Harris
   recurrence theorem can also supply this, but is not inferred merely from the
   words “finite invariant measure.”
2. The actual committor `q(x)=P_x(tau_B<tau_A)` is 0 on A, 1 on B, in [0,1],
   continuous, harmonic in S, and has finite energy

       cap_m(A,B) = integral Gamma(q) dm < infinity.

   Its identification as the global Dirichlet-form minimizer, if needed for a
   trial upper bound, must be independently received. No boundary condition at
   infinity or trial/current source certificate is silently supplied here.
3. The extended q has a localized semimartingale decomposition

       q(X_t)-q(X_0) = M^q_t + C^A_t - C^B_t,
       d<M^q>_t = 2 Gamma(q)(X_t) dt,

   where C^A and C^B are continuous locally finite-variation processes supported
   on times with X in the corresponding basin boundary. Localized means this
   holds before exiting each compact localization region. Their signs are not
   important to the cancellation below. A sufficient concrete route is smooth
   locally elliptic coefficients, regular disjoint smooth basin boundaries,
   q C2 in S with local C1 one-sided traces, and the generalized Itô formula for
   its constant extension into the basins. Boundary flux/local-time terms then
   have the stated support. A generic Fukushima zero-energy term is NOT
   automatically a finite-variation boundary local time; that receiving step
   must not be skipped for rougher models.

The identity to prove is

    E_stationary N_(0,T] = 2 cap_m(A,B) T / Ztot.

Here N counts completed transitions from the last-visited basin to the other,
not every interface contact and not raw-sign zero crossings. The factor 2 uses
the displayed Gamma/capacity convention; other capacity conventions must first
be converted.

## 1. Stationary augmentation and its actual law

On the two-sided stationary path define I_t=0 if the last basin visited at or
before t is A and I_t=1 if it is B. At a basin hit use the newly visited basin.
The past-visit assumption makes this well-defined. Its definition commutes with
time translation, so `(X_t,I_t)` is stationary. It is also a Markov augmentation
of the original Markov process: given current X and retained I, future updates
are determined by the future X path. No independent resets are inserted.

Under reversibility, conditional on X_t=x, the reversed past until its first
basin hit has the forward hitting-law distribution from x. Therefore

    mu(dx,0) = (1-q(x)) pi(dx),
    mu(dx,1) = q(x) pi(dx).

In particular, on A the retained label is certainly 0, and on B it is certainly
1. In S it is generally randomized under stationarity. Setting the retained
label to the sign of a state coordinate there does not in general produce this
stationary augmented law.

Reversibility is used for this explicit committor formula. The count proof below
uses the actual stationary augmentation and local committor decomposition, not
an unsupported claim that an arbitrarily initialized retained label is stationary.

## 2. Pathwise local finiteness before expectation bounds

On [0,T], every continuous nonexplosive X path is uniformly continuous and has
compact range. Consecutive completed transitions require travel between the
separated basins. There is therefore a positive path-dependent minimum time
needed for such travel, so N_(0,T] is finite pathwise. This argument alone does
NOT prove E N finite.

The retained label is a cadlag process with these finitely many jumps. Define

    F_t = (q(X_t)-I_t)^2.

It lies in [0,1]. At a completed A-to-B transition the left retained label is 0
and q=1, so F jumps from 1 to 0; at a B-to-A transition the left label is 1 and
q=0, again F jumps from 1 to 0. Each such transition contributes exactly -1.

## 3. Boundary cancellation, including switching instants

Apply the semimartingale square formula between and across the retained-label
jumps, using I_(t-) in predictable stochastic and finite-variation integrands.
The boundary contribution is

    2 integral (q(X_t)-I_(t-)) (dC^A_t-dC^B_t).

Whenever X_t is on the A boundary, the current retained label is 0; whenever it
is on the B boundary, it is 1. Thus q(X_t)-I_t is zero on both boundary supports.
I_(t-) can differ from I_t only at the locally finite set of completed
transitions. The continuous finite-variation boundary measures have no atoms
and hence give this set zero mass. The entire displayed boundary contribution
vanishes. The fact that the coefficient at a first arrival is nonzero when
evaluated with the OLD label causes no leftover term: local time is continuous
and has no atom at that arrival.

Consequently the localized exact identity is

    F_t-F_0 = M_t + 2 integral_0^t Gamma(q)(X_u) du - N_(0,t],
    M_t = 2 integral_0^t (q(X_u)-I_(u-)) dM^q_u.

There is no unaccounted boundary-at-infinity term; all calculus is first carried
out on compact localizations and then unstopped as below.

## 4. Noncircular integrability and unstopping

Write `c=cap_m/Ztot`. Base stationarity and finite energy give

    E integral_0^T Gamma(q)(X_u) du = c T.

Stop the localized identity at T, the m-th completed transition, and a nested
compact exit/local-martingale localization. The stopped count is integrable,
the martingale has zero mean, and 0<=F<=1, so

    E N_stopped <= 1 + 2cT.

Nonexplosion, pathwise local finiteness of transitions, and exhausting
localization allow the stops to tend to T. Fatou gives

    E N_(0,T] <= 1+2cT < infinity.

This earns count integrability; it was not assumed to justify optional stopping.
Now count and energy terms converge by domination/monotone convergence, and the
bounded F terms converge as well. Passing the zero-mean stopped identities to
the limit yields

    E N_(0,T] = E F_0-E F_T+2cT.

Equivalently, the unstopped martingale is square integrable because

    E<M>_T
      = 8 E integral_0^T (q(X_u)-I_(u-))^2 Gamma(q)(X_u) du
      <= 8cT.

Actual augmented stationarity gives E F_T=E F_0, proving

    E N_(0,T] = 2 cap_m(A,B) T/Ztot.

As a check on the stationary endpoint term, the joint law in Section 1 gives
`E F_t = integral q(1-q) d pi`, independent of t.

This proof establishes finite expected count without circularly assuming it.
It uses no iid waiting times, no exponential first-hit law, and no independence
between bins or successive transitions.

## 5. Initial conditioning and deterministic-time jump atoms

Conditioning the stationary augmented law on X_0 in A yields exactly X_0 with
law pi(.|A) and I_0=0. Its density relative to mu is
`1_A(X_0)/pi(A)`. The induced full future-path law has the same domination, so
any already established stationary bad-event probability may be divided by
pi(A) for an upper bound under this initialization.

The stationary count E N=2cT is generally NOT an equality after that conditioning:
the endpoint term E F_0-E F_T no longer cancels. It must not be reused as if the
conditioned experiment were stationary.

Finite stationary count intensity also excludes deterministic-time jump atoms.
By stationarity the expected number in an interval of length h is 2ch. The
expected count at a single deterministic time is bounded by the counts in
arbitrarily short containing intervals and is therefore zero. This remains true
under any full-path law dominated by the stationary law, including pi(.|A).
It provides an alternative to separately invoking first-hit density theorems.

## 6. Exact per-bin inequality and its limits

For every nonnegative integer N,

    N-1_{N odd} >= 2 1_{N>=2}.

For a completed-transition count, parity is precisely the difference between
the two retained endpoint labels. Therefore

    P(N_bin>=2)
       <= [E N_bin-P(endpoint retained labels differ)]/2.

This is an exact combinatorial inequality. To get a small numerical bound one
must ALSO receive a sufficiently sharp lower bound for the retained endpoint
odd-flip probability and a matching intensity upper bound. A state-label grid
certificate does not automatically supply the retained-label probability:
their slab mismatch must be charged or an augmented-state certificate supplied.

Matched sampled labels plus at most one actual AND at most one comparison jump
per bin match jump counts, order, and directions. Corresponding jump times lie
in the same bin, hence differ by at most its width. Reference multiple jumps must
be excluded separately. This is a jump-time-error coupling, not total variation
of exact continuous jump-time distributions.

## 7. Blocker receipt

* **Action:** receive the actual two-sided stationary augmentation and almost-sure
  past basin visits. **Target:** concrete diffusion/initialization interface.
  **Reason:** invariant pi alone does not define a last-visited label on every
  invariant component. **Outcome:** conditional theorem proved; concrete
  augmentation not silently approved.
* **Action:** receive the actual finite-energy committor and its localized
  harmonic/boundary decomposition (or an equivalent rigorous Dirichlet-form
  argument). **Target:** concrete global-domain/current proof. **Reason:** a
  formal Fukushima symbol is not by itself finite-variation local time, and a
  killed local certificate is not automatically a global committor certificate.
  **Outcome:** conditional identity proved; these concrete receipts remain
  separate obligations.
* **Action:** use domination, not stationary equality, after Gibbs-on-A
  conditioning. **Target:** finite-horizon failure probability. **Reason:** the
  conditioning removes augmented stationarity. **Outcome:** exact R factor is
  available, without resets.

No permission denial or retry occurred.
