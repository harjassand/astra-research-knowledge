# Primary comparison and actual capability disposition

[Sutherland, *Micropipelines*, CACM1989](https://arc.cecs.pdx.edu/wp-content/uploads/2023/04/Sutherland_Micropipelines_TuringAward_ACM_1989.pdf)
is the controlling primary architecture. Its event-driven elastic FIFO,
two-phase request/acknowledgement, safe capture/hold/overwrite and series
composition were read directly, especially printed pp722--727. It already
explains backward propagation of empty spaces. None of these are a new
invention here. Its physical bundled-data implementation has timing and
initialization conditions; our atomic measured neighbour-copy channel is
a specified model primitive, not an acquired transistor realization or a
proof of every implementation's hazard tolerance. The nominal Muller/
handshake core is an equally informed ordinary alternative and can reproduce
the exact FIFO used here.

[Dolev--Dubois--Potop-Butucaru--Tixeuil, *Stabilizing Data-Link over non-FIFO
Channels with Optimal Fault-Resilience*, 1011.3632v2](https://arxiv.org/html/1011.3632)
was read at its actual model, lower bounds and protocol scopes. It treats
bounded-capacity unreliable non-FIFO channels, weak fairness, arbitrary
initial corruption and bounded duplicate/ghost/reordering metrics. Its
Theorem4 is a(0,1,1,1) stabilizing link, stronger initial-message metrics
than our raw FIFO's M-ghost allowance. Counters, repeated acknowledgements
and processor/application interfaces are actual parts of that incumbent;
they are not denied to the ordinary comparator. A theorem after a last
transient corruption does not itself give our displayed sustained-noise
Poisson deadline, but its bounded-effect perspective is already prior.
We do not claim a new generic data-link no-go from the initial ghost
indistinguishability argument.

The ordinary asynchronous-circuit literature includes Muller C-elements,
dual-rail completion and four-phase protocols. A primary author-level
[Cambridge four-phase note](https://www.cl.cam.ac.uk/~djg11/wwwhpr/fourphase/index.html)
was acquired. These designs do not turn a noisy ack bit into an infallible
certificate. Conversely, the port lower bound in PROOF(18) does not rule
out a redundant consumer, a paid noisy verifier or temporal coding.

Gacs's corrected2024 asynchronous reliable-computation construction is
an even stronger broad conventional alternative; its actual rate-
perturbation/medium scope was read in the preceding frozen package. We
do not silently upgrade it to a ready all-future-labelled quantum-control
threshold, nor assert that such an admission is impossible. The present
FIFO avoids that import: its invariants hold on EVERY physical state
and its Poisson good-schedule bound is simultaneous over fault labels.

The workload proof is standard Lindley/coverage/queueing analysis, with
ordinary Finner/read-q for the specified independent primitive streams.
The latter named import has its exact primary formulation already cached
and visually checked in the frozen c_classical_eroder source package.
It is not an inferred independence of completed transactions.

## What was changed rather than assumed

A population Schmitt-latch/encoded-ack proposal was considered, but no
completed reliable mutable-register compiler is claimed. In particular,
the old copy's density and independence premises cannot simply be reused
at an adaptive acceptance time. Parent's separate root_async_restart
work pays a simultaneous sparse RESTORING restart and a fixed-catalogue
Palm union; its original asserted clean-copy extension to a future-selected
source pattern required an additional argument. Our read identified that
source-to-destination future-coin gap, and parent preserved/corrected it.
The present queue theorem does not depend on that disputed extension.

Instead EVERY tag pattern is a valid bounded queue. The only relevant
state-restoring quantity is a bounded prefix workload, so a deterministic
worst-case comparison handles future-selected initial patterns and
acceptance times directly. This removes persistent phase/history damage
for this actual open-line protocol, without claiming its noisy native
notifications are error-free.

## Consequence and limitation

The completed operation is a reusable, causal, bounded-local classical
FIFO with an UNLOCATED packet-edit budget per physical fault and a paid
deadline-or-edit tail. No clock, perfect register, state reconstruction,
fixed external copy interval or history rewind runs the controller.
Its source can change after an actual local capture/ack, and stages compose
by concatenation. It is nearest-neighbour on a line of fixed-size cells,
so the previous expander wiring is not being relabelled as3D locality.

It is NOT yet an exponentially reliable encoded acknowledgement,
interactive logical stream or autonomous quantum decoder. Raw noise can
create a packet at an idle output. The receiver is not told which packets
are wrong. A closed feedback ring can also fill/empty and deadlock; actual
hole/token restoration is a separate requirement. Constant-cell recovery
does not imply a size-independent noise threshold for a growing pipeline.

The original stronger mutable-logical-register interface therefore remains
unbuilt. What survives is a concrete fault-contained streaming primitive
and an explicit reduction of its remaining reliability problem to
unlocated edits plus deadline violations, not arbitrary permanent
controller phase corruption. The core architecture/methods are ordinary;
no world-priority, native hardware, practical advantage or quantum-memory
claim is made.
