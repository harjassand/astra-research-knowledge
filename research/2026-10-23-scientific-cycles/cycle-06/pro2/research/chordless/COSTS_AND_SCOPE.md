# Chordless contribution costs and scope

## Actual new computation

| Execution | Body wall seconds | Body CPU seconds | Peak process RSS bytes |
|---|---:|---:|---:|
| Exact theta boundary, free comparator and cap-obstruction diagnostic | 0.015369859000202268 | 0.015355758000000004 | 11,010,048 |
| Exact separator-profile receiving diagnostic | 0.0011043940030504018 | 0.001102510999999997 | 10,616,832 |

Total recorded bodies:0.01647425300325267 seconds. Both first executions passed.
No retuning, precision sweep, graph search or old fixture replay was performed.
The first script covers12 explicitly listed path-length vectors and all16
terminal-color assignments:188 extensions accepted,4 equal-terminal K_(2,4)
states rejected for the exact combinatorial reason. It also exhaustively counts
four-color assignments on K_(2,r), r=2,3,4, checks the free three-color comparator,
and saves the cap-obstruction witnesses for K=2,6,17,64.

The second script consumes the actual saved Theta(2,2,2,13) fixture. It compares
sequential exact boundary-profile joins with the direct profile of the whole
graph, then verifies the exact duplicate-channel rejection of a fourth short
path. The resulting actual maximum component order is4. This is an author
receiving calculation, not an independent proof review.

Source import/Python startup, serialization after the recorded body clocks,
tool/service overhead and the complete discovery/authoring cost are excluded
from these body figures and remain unmetered. Measured peak RSS is per process,
not simultaneous memory or total resource use.

## Source and research work

The first recorded clock was2026-10-22 00:08:37 UTC. The actual Cycle5 structural
note, long-strip proof and focused literature note were read. Two primary-source
open calls for Trotignon–Vuskovic reported rounded service latencies2.3s and2.2s.
A focused three-query search reported2.6s. These sum to7.1s of reported source
service latency, not total reading/reasoning time. The search's acyclic edge
coloring result was not substituted for the vertex-coordinate problem.

Proof development, unsuccessful structural reasoning, code authoring, messages,
review, inference/token cost, total scientist CPU/wall, energy and money totals
are unknown or unmetered, not zero. No purchase, installation, paid compute,
public upload, Page edit or outreach was performed by this contributor.

## Operation-level work

For a supplied theta-path representation, constructing the coloring and its
terminal signature costs O(n+m) work and storage. Validating the representation
must check unique internal vertices, complete edge coverage and stated lengths;
the supplied generator constructs that representation exactly. Recognizing an
arbitrary graph as a more general atom or finding its decomposition is not an
implemented free input to this operation.

The profile builder traverses each color-pair forest and takes O(q^2(n+m))
work; q=4 is fixed here. Each abstract two-terminal profile join takes constant
arithmetic work, but its masses are input-dependent integers requiring their
actual bit cost. Iterating the exact mass formulas does not cap those integers.
The code assumes pieces share only the two designated nonadjacent terminals
and agree on colors; receiving use must validate that graph interface.

For matrix recovery, construct the full-support coordinate decoder after any
coloring/composition. The original action cells contain all incident terms.
The four or three actual matrix actions, preparation, observation reading,
decoding arithmetic, input conversion, residual certification and downstream
spectral work still have to be charged. This contribution claims no application
timing or superiority to an ordinary solver.

## Rejected or incomplete mechanisms

1. Universal arbitrary-terminal reset is false: equal terminal colors on
   Theta(2,2,2,L), L>=3, force all three color channels despite unbounded order.
2. Universal arbitrary-terminal extension is false already on K_(2,4).
3. Keeping only a component-size cap is insufficient for no-recolor degree-two
   reinsertion, for every cap K>=2, even on cycles and away from a boundary edge.
4. Coloring the degree-at-least-three induced forest alone leaves constraints
   through short degree-two threads. A favorable local forest coloring does
   not settle those terminal states or their masses. No global theorem was
   promoted from this incomplete idea.
5. Four edge colors of a chordless graph are not four vertex-query coordinates;
   no reduction satisfying the free-diagonal norm contract was established.

These are scoped failures, not impossibility of four coordinates for the
whole class and not a reason to retire the scientific mission. Historical
originality remains unassessed; finite exact checks establish their own saved
instances, while the all-size claims rest on the written proofs.
