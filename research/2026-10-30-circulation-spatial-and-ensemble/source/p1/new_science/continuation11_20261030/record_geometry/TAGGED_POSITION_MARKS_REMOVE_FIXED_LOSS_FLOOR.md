# A richer emitted record removes the fixed-loss current floor

30 October 2026. Existing record_geometry role. This is a constructive
strengthening of the downstream readout comparison, at a different
explicit record interface.

## 1. Native physics and extra observable information

There are at most C N^2 native particles on N horizontal circles of
circumference N. Each particle remains in its row. A native elementary
move is one lattice step clockwise or counterclockwise. Interactions,
hidden states and time-dependent kinetics are allowed, provided the total
conditional native event intensity is at most Lambda N^2.

The actual outgoing event port is one way and already part of the native
reference, as in DOWNSTREAM_EVENT_READOUT_AND_VOLUME_PRECISION.md.
Now a detected event additionally identifies the native particle and its
wrapped position immediately after the event. Its emission time or
causal ordering is available. Detection is independent across emissions
conditional on the complete native path, with efficiency at least a
fixed eta_0>0. The efficiency need not be known and need not tend to one.

Static particle tags, distinguishable position labels, timing and a
nonreturning output channel are real extra observable resources.
They are not inferred from an anonymous current pulse or from a native
Markov generator. In particular, the count-only fixed-loss obstruction
does not apply to this richer record.

## 2. A causal estimator requiring no initial microscopic position

For each particle, discard its motion before its first detected position.
Retain that position. Whenever its next position is detected, add the
shortest signed lattice arc from the previous detected position to the
new one to the estimated physical current. Use a fixed convention for
an exact half-circle tie.

The estimator is causal in the ordered detected record. It does not
simulate a missing native future or require a native rate estimate.
It also does not need an initial position measurement: the omitted
initial segment is accounted for below.

Let K be the number of actual native steps between two successive
detected positions. If K<N/2, the actual unwrapped endpoint displacement
has magnitude less than N/2 and is recovered exactly. If K>=N/2, the
difference between the true endpoint displacement and the short-arc
choice is a multiple of N, with magnitude at most 2K.

For a one-dimensional row the same statement controls the entire
integrated spatial current. The actual path's signed edge-current vector
and any short arc joining its endpoints differ by an integer circulation:
the same integer on every edge of the ring. Its total variation is the
absolute unwrapped winding displacement and is at most 2K. Backtracking cancels exactly
in this signed integrated current.

The unobserved initial and final path segments each have current total
variation at most their respective number of actual steps.

## 3. Exact pathwise error bound

Let G_a^0 denote the number of native steps of particle a up to its first
detected event, truncated if the observation horizon comes first.
Let R_a(s) be the number of its steps since its last detection, or zero
if its entire unresolved segment has already been charged to G_a^0.
Let K_{a,j} be completed detection-interval lengths.

For true and reconstructed integrated current measures, normalized
with N^{-3} per physical edge crossing,

\[
\sup_{s\le N^2T}\|Y_N(s)-\widehat Y_N(s)\|_{\rm TV}
\le N^{-3}\left[
\sum_a G_a^0
+\sup_{s\le N^2T}\sum_a R_a(s)
+2\sum_{a,j}K_{a,j}{\bf1}_{\{K_{a,j}\ge N/2\}}
\right].                                                     \tag{1}
\]

Every quantity on the right counts actual native moves. The reconstructed
short arcs are an estimator, not a declaration that the missing particle
followed that arc.

## 4. Fixed efficiency gives superexponential volume accuracy

For every epsilon>0 there are constants such that

\[
\Pr\left\{\sup_{s\le N^2T}
\|Y_N(s)-\widehat Y_N(s)\|_{\rm TV}>\epsilon\right\}
\le e^{-cN^4}
+{\rm poly}(N)\exp[-c_\epsilon N^3+C N^2+o(1)].                \tag{2}
\]

Consequently the error is superexponential at speed N^2. This is stronger
than convergence in the negative-Sobolev current topology.

Here is a proof conditional on the complete unchanged native path.
Its total number Q of events satisfies
Pr(Q>K_0N^4)<=exp(-cN^4) for a sufficiently large fixed K_0,
by the intensity bound.

Detection decisions can be coupled to independent guaranteed successes
of probability eta_0. Each actual detection interval lies inside a
guaranteed-success interval. A geometric variable G with success
probability eta_0 has an exponential moment at some theta>0.

First, sum_a G_a^0 is dominated by a sum of O(N^2) such variables.
Chernoff's inequality at epsilon N^3 gives
exp[-c_epsilon N^3+C N^2].

Second, at each fixed native event time, the unfinished runs R_a are
independent truncated geometric tails conditional on the native path.
The same bound applies to their sum. There are at most K_0 N^4+1 event
times on the retained event, so a union gives the second term in (2).

Third, for theta small enough,

\[
\mathbb E\exp[\theta G{\bf1}_{\{G\ge N/2\}}]
\le 1+C e^{-cN}.                                             \tag{3}
\]

The completed long-interval sum is dominated by the corresponding sum
over at most Q+C N^2 independent guaranteed-success intervals. One may
oversample that many geometric intervals separately for each particle;
the number of native events of each particle is fixed in the conditional
argument. On Q<=K_0N^4, the log moment in (3) is at most
C N^4 exp(-cN)=o(1). A final Chernoff bound proves (2).

No independence of the native particles is assumed. What matters is
unchanged native dynamics, fresh detection decisions conditional on that
path, local unit moves, and the row topology.

## 5. Why the count-only impossibility and this theorem coexist

In the count-only Poisson example, the entire detected record contains
event times, signs and row labels, but not the intermediate wrapped
positions. Missed positive and negative streams are then independent of
that record, so their winding contribution cannot be inferred.

A tagged position record contains information about the missed events.
The endpoint displacement of every short missed run is recovered even
though its individual event counts are not. The rare ambiguity is a run
long enough to wind around the entire circle. Its length threshold grows
with N, and that geometric protection produces (2).

The distinction is actual recorded information, not a more favorable
analysis of the same estimator. If a proposed detector already exposes
emitter positions or identities, those records must be retained in
assessing a sensing lower bound.

## 6. Finite delay, communication and resource limits

The estimator assumes the actual source ordering of each particle's
records. A fixed bounded delay, an actual timestamp, or a FIFO tagged
channel can supply this order. Variable propagation times are not
silently treated as exact emission times. A downstream latency o(N)
can be charged by the recent-event-window estimate in the companion
readout proof.

The later spatial collection delay is a different issue. The record can
be reconstructed for a held past epoch and then delivered as a stale
record with a declared age. That is compatible with a separately proved
delayed controller. It does not establish a zero-age global measurement.

This richer port sends O(log N) identity/position bits per detected event,
and the native horizon contains O(N^4) events. An uncompressed record
therefore has O(N^4 log N) bits. Running reconstruction can retain only
the last position and current counter for each of O(N^2) particles, but
records appearing at different physical sites still have to reach the
same causal state or be merged by a distributed protocol.

A central processor for each row needs order N event updates per unit
physical time at ordinary interior activity, with corresponding tagged
communication. Fixed-range propagation takes order N time across a row.
Increasing bandwidth, additional parallel channels, local tracking
memories, timestamp distribution and queue storage are paid possible
suppliers. This note does not assert that a bounded-bandwidth prefix
adder for anonymous aggregate counts already performs that tagged merge.

Thus (2) supplies an exact causal record statistic, not a completed
same-hardware communication implementation. A full receiver must either
provide its timestamped ordered stream with an actual finite delay and
reliability bound, or prove the distributed reconstruction protocol.

The outgoing photon energy and source-isolation costs from the companion
note remain. Fixed efficiency removes the need for progressively longer
absorption or increasingly small intrinsic loss, but it does not remove
the marked output, static tag, range, timing or power requirements.

## 7. Exclusions and useful consequence

This theorem is for row-confined particles. For unrestricted
two-dimensional trajectories, endpoints do not determine the spatial
integrated current: missed closed loops can carry nonzero circulation
inside a small region. Their scale need not grow with N. Extending (2)
to that setting requires a topology-appropriate extra record, a new
estimate, or finer observation; it is not asserted here.

The theorem does not reconstruct every native microscopic history or
heat record. Many different short excursions have the same observed
endpoints and the same net one-dimensional current.
It also does not supply an initial density measurement. The actual native
density law remains unchanged because the source port is one way.

Within its class, this is a stronger ordinary alternative: a fixed-loss
readout can recover the complete integrated native current at
super-volume accuracy by retaining particle identity and wrapped position.
The earlier vanishing-loss requirement is therefore a property of the
count-only interface, not a universal measurement limitation.

