# Local preparation island: interface and cost audit

2026-10-24. Independent bounded audit of `../FIRST_CONSTRUCTION.md`. This is
source-free mathematical/interface review, not a literature-priority finding
or physical validation.

## Main boundary

The construction avoids a global state identifier and global Hankel-rank
promise, but it does not learn that the supplied local variables are complete.
Known binary cells, their known interaction graph, bounded-range Markov
sufficiency, and conditional independence of local update noise are strong
physical structure. The noisy sensors then provide paid approximate access to
the complete state of each measured neighborhood. This is not a global
full-state oracle: only a finite guard and its causal cone are read. It is,
however, a local state-observation/Markov-completeness contract, and finite data
cannot certify that no unrepresented local memory exists.

For example, augment one observed cell by a hidden finite shift register that
is not read and that changes a transition only after a particular long control
history. A fixed finite calibration and validation transcript can be identical
with or without the register, yet a later continuation can differ. Thus “no
unrepresented local memory” must remain supplied. A finite-horizon version is
more modest and useful: the specified native variables suffice for all allowed
histories through the stated acquisition and target horizons. It is still an
assumption about the physical interface, not something established by a fit.

## Minimum honest contract and acquisition

For the stated local influence argument, the physical contract needs all of
the following:

* A known bounded-degree graph, interaction radius, and binary native cell
  variables; no omitted local degrees of freedom that affect the permitted
  update or target readout during the certified horizon.
* A synchronous transition kernel that factorizes across updated cells
  conditional on the complete current configuration and selected local
  modes. The update-noise draws are not exposed to the controller or future
  policy. If they are logged, the result is not a guarantee conditional on
  that log.
* Site-selective legal modes and a pre-read/act/post-read timing boundary. The
  controller can apply a chosen mode when the measured local context is the
  desired one. Sensor measurements do not change the cell, and each repeated
  read has independent conditional error, or a separately validated
  concentration guarantee. A bare marginal error ceiling below one half is
  insufficient if repeated errors can be perfectly correlated. The sensor
  error ceiling or confusion model must be calibrated and included in the
  failure budget.
* Independent full-process starts, each charged in cost. The initializer
  supplies no context labels or context sampler. Each required context/mode
  must occur often enough under those starts, or be reached through an
  explicitly paid local preparation protocol. Otherwise acquisition returns
  `UNKNOWN`.
* A finite target horizon and future controls restricted to the same local
  graph/range and control interface. No unmodeled global feedback, broadcast
  readout, or faster-than-local channel may carry distant state into the
  target transcript.

Let `L = sum_i |A_i| 2^{|N_i|}` count site/mode/context response cells in the
guard (or use the smaller explicitly visited model). To estimate every
Bernoulli response within `epsilon_p` with failure at most `delta_p`, a
conservative simultaneous Hoeffding count is

    n_cell >= ceil(log(2 L/delta_p)/(2 epsilon_p^2)).

If `N_read` binary sensor decisions are used and the conditional sensor-error
probability is at most `eta_s < 1/2`, majority repetition count

    r_sensor >= ceil(log(2 N_read/delta_s)/(2 (1/2-eta_s)^2))

makes all decisions correct with probability at least `1-delta_s` under the
stated independent-read model. These are paid reads before and after the
update; choose an odd integer at least this large for an unambiguous majority.
On the joint good event, form

    C_ij^{a,U} = max_{c,c' differ only at j}
                 ( |p_hat_i^a(c)-p_hat_i^a(c')| + 2 epsilon_p ).

The selected mode is certified only if the sum of these upper bounds is at
most `q<1` for every trained cell. Finite counts cannot replace this margin:
if a true row sum exceeds `q`, the procedure must reject that mode.

Coverage has a separate cost. Let `pi_min` lower-bound the probability, on one
independent start, of obtaining a usable sample for each required
site/context/mode entry (thus including any mode-scheduling probability). Then
independent starts need on the order of

    N_start = O((n_cell + log(L/delta_cov))/pi_min)

to obtain the required count for all entries, with constants fixed by a
binomial lower-tail bound. The bound is not uniform as `pi_min` tends to zero.
If a context has zero initializer probability and no paid local actuation can
create it, its transition row is unidentified and the Dobrushin certificate
cannot be issued. Each start also incurs local reads (up to
`(|N_i|+1) r_sensor` per sampled site), controlled update events, data
storage, fitting, and validation. Synchronous hardware may collect responses
at many sites in one round, but only where their required modes can actually
be selected simultaneously; no free context oracle or parallelism should be
assumed in the cost ledger.

## Check of the spatial bound and timing

Under the supplied product-kernel model, couple each local Bernoulli update
with a common uniform draw. The probability of disagreement at site `i` is
bounded by `sum_j C_ij D_t(j)`. For trained sites, the row sum is at most `q`.
Treat the influence coefficients as a substochastic, possibly time-varying
path kernel: total weight of any one additional dependency step is at most
`q`. The contribution from arbitrary initial disagreements inside `B` is at
most `q^k`; a path from `i` to an uncontrolled exterior state requires at
least `d(i,B^c)` local dependency steps, so its total first-exit weight is at
most `q^{d(i,B^c)}`. The two contributions add, giving the stated

    D_k(i) <= q^k + q^{d(i,B^c)}.

This argument needs the row-sum bound over *all* local contexts, including
contexts involving exterior neighbors at the guard boundary. It also needs
the graph-distance/interaction-radius convention to be explicit. If each
update has radius `r`, an `H`-round future observation on `A` has a backward
cone `F` of radius at most `rH`; a guard of radius `R >= rH` gives distance at
least `R-rH+1` from `F` to `B^c`. Coupling the future run with common local
noise and the same policy then gives

    TV <= sum_{i in F} D_k(i)
       <= |F| [q^k + q^{R-rH+1}].

For radius one this recovers the written exponent `R-H+1`.

This causal claim is naturally a *parallel synchronous-round* statement. If
“one round” instead means a sequential sweep of updates, a long sweep can
carry a dependency across many graph edges before the next round boundary.
Then `R>=rH` in wall-clock rounds is not sufficient. Count causal update
events along the longest within-sweep path (or time-expand the actual
schedule); the guard must exceed that event-depth times the local radius.
Likewise, instant global observation of remote sites followed by adaptive
control is an extra communication channel and invalidates the locality claim.

## Strongest matched controls and cost test

An equally informed local model-based controller receives the same sensor
records and intervention counts, fits the same response tables, selects the
same modes, and proves the same coupling bound. It ties the mathematical
operation; the theorem is not an algorithmic advantage over that controller.
An external initializer can bypass the acquired guard only if it can prepare
the same target state directly; that target-preparation ability is an extra
comparator premise, not implied by the existence of an initializer for
response trials. If it can, it can prepare the target on each future trial
without first paying for table acquisition. If it can only reproduce the
acquisition-start distribution, the fair comparison is to apply the same
guard `S` after those starts, making that per-use `S` cost common. Let `C_A` be all
acquisition cost, including full starts, reads, updates, coverage failures,
computation/storage and confidence/precision overhead; let `C_prep` be the
per-use guard cost; and let `C_full` be a full initialization to the matched
target. Any cost advantage requires

    T (C_full - C_prep) > C_A,

with the future experiment and certified visible-law tolerance held fixed.
If the comparator prepares the reference and applies the same `S`, subtract
that common `S` cost from both sides; the learned route still must recover its
calibration cost. If `C_full <= C_prep`, this route cannot win on operation
cost. The actual initializer cost and reachable context probabilities are
therefore decisive, not implementation details.

The credible changed capability is narrower than “learns an unknown system”:
from noisy local transition observations, it can certify a finite guard that
makes a finite-horizon local experiment insensitive to arbitrary remote and
initial configurations, under an explicit native-variable/Markov contract.
It neither recognizes that contract from finite data nor provides a global or
unbounded-horizon reset. These are the physical and informational promises to
keep visible in any continuation.
