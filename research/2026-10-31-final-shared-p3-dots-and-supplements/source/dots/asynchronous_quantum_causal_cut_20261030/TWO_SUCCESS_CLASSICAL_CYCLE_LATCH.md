# Physical two-SUCCESS latch for the observe-delay-commit cycle

2026-10-30. Refinement of NATIVE_CLASSICAL_OBSERVE_DELAY_COMMIT.md. This closes one finite-state freshness detail, not the global strong signed-noise theorem.

## Why the refinement is necessary

The first successful snapshot after an arbitrary cut can belong to an inherited partial attempt. Merely saying that the next visible commit starts a new cycle is insufficient unless the physical commit also resets a freshness counter, and the next commit cannot reuse an old snapshot. The source's choice of the SECOND visible switch after a rational start is useful only after this actual finite-state sequencing has been supplied.

## Colocated hardware and leaves

Group at site x the visible X_x, snapshot S_x, local resource tag, observer hub, a counter c in {0,1,2}, and an n-stage timer. This is one fixed finite-dimensional hardware site. Neighbor labels remain remote read-only controls. Every transition described below is an onsite resolved leaf except the already compiled two-site snapshot edges.

* The observer LOAD remains unconditional. Its locked attempted payload copies the full neighborhood into S_x when c<2; when c=2 it is identity on S_x and all visible DATA. This preserves nominal all-state attempt service rather than parking the native machine indefinitely.
* Its actual SUCCESS leaf increments c from 0 to 1, or from 1 to 2. In the latter case it also initializes the timer to stage 0. At c=2 it leaves the counter/timer unchanged. These are explicit resolved onsite leaves, not a counter attached to fictitious records of a perturbed generator.
* The timer advances only when c=2. A state with c<2 cannot commit. All finite timer labels are in {0,...,n}; arbitrary initial timer state with c=2 therefore has no more than n remaining forward stages.
* The visible COMMIT leaf requires c=2, completed timer, and local tag FREE. It writes Tr(S_x) plus the fresh Rand leaf and atomically resets c=0 and the timer to 0. It does not bypass a neighbor's read lock.

The actual SUCCESS/counter coupling is a fixed alteration of the nominal hardware. The CP cavity keeps these specific onsite leaves identifiable where needed. One does not claim that the same leaves remain a separate instrument in the unrestricted actual perturbed generator.

## Second-switch freshness

Let sigma_1 be a visible commit in a nominal clean interval. Immediately afterward c=0. A later visible commit sigma_2 requires two subsequent actual SUCCESS leaves. At most the first of those can complete an attempt already partially underway at sigma_1. The second follows the first attempt's SUCCESS/cleanup/new LOAD and full ownership acquisition. Its copied neighborhood is therefore a new serializable snapshot after sigma_1. Its SUCCESS is the one that starts the timer.

A stale old SUCCESS with a malformed initial terminal phase may count as the first event, but cannot alone enable sigma_2. A stale timer cannot do so either, because COMMIT reset c to zero. A late cached operation cannot bypass this requirement: the snapshot, c and visible commit share the same site/ownership footprint, and the native SUCCESS leaves are the only nominal increments of c.

The usual good-history/forest condition still covers competing inherited owners. A compromised neighboring partial transaction is not made harmless just by this local counter; it must be included in the same marked native neighborhood used by the exact compiler's clean semantics.

Thus, on that clean semantic event, the snapshot used at sigma_2 lies strictly after sigma_1 and at least the timer duration before sigma_2. With a timer lower duration T/2, it satisfies the primitive medium's required look-back separation for T_low=T/2. The first commit after an arbitrary cut may remain stale, exactly as permitted by the source's second-switch computation condition.

## Service accounting

Use the new channel/counter alphabet to reconstruct the finite monitored path and witness. The original generic two-SUCCESS theorem is structural input, not a license to reuse its old numerical constants.

From c=0 or 1, two actual successes suffice to enable the timer; from c=2 no successes are needed. The timer has at most n remaining stages. After it is finished, clearing the finitely many incident readers and taking the actual tag-free COMMIT leaf gives a finite all-state path to a visible switch. This establishes the structural basis of a uniform upper-dwell tail. The good full-cycle lower dwell comes from the freshly initialized timer, independently of snapshot waiting. The future joint timer/commit/snapshot tests must all live in one compatible CP cavity family.

This refinement makes the second-switch claim a physical finite-state statement. It does not yet prove adaptive-window product bounds for the broad continuous joint-bath noise class.
