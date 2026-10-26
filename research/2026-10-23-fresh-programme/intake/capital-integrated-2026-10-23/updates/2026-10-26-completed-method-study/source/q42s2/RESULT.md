# Stage 2: finite contact circuits retain reverse transfer

The stress stage preserves the first construction and strengthens its governing
limitations. **No mission-level advance is established.** The new completed
scientific object is a theorem for arbitrary finite reciprocal heat-contact
networks: whenever a finite periodic circuit transfers a DC temperature
perturbation from one terminal to another, its reverse DC transfer is also
strictly nonzero. I also attempted two stronger three-body mechanisms and
executed matched model comparisons. Neither establishes an advantage.

## The consequential failure mode and completed proof

The strongest tempting interpretation of the first-stage construction is that
more storage and better timing could turn it into a perfect selective heat
router. A small calculated reverse coefficient could then be mistaken for
zero. The completed proof in REVERSE_TRANSFER_PROOF.md rules out that ideal
operation throughout the following class: arbitrary finite graph, positive
constant scalar capacities, bounded reciprocal nonnegative periodic contacts,
fixed terminal temperatures, finite period and a stable periodic solution.

For distinct terminals i,j,

\[
 Y_{ji}<0\quad\Longleftrightarrow\quad
 \text{the union graph has an i-to-j path through internal nodes only}.
\]

Thus Y_ji=0 if and only if Y_ij=0. The nonzero values can be unequal; this does
not undo the first-stage circulation. The theorem carefully excludes paths
through a third clamped terminal, which absorbs the perturbation. Global union
connectivity alone would not justify a dense terminal response.

For a path with k internal nodes, conductance integrals W_e over a period P,
capacities C_v and maximum internal escape rate delta, both directions satisfy

\[
 \min(-Y_{ji},-Y_{ij})\geq
 e^{-k\delta P}\frac{\prod_e W_e}{P\prod_v C_v}>0.
\]

The proof uses nonnegative variation of constants and assigns successive edges
to successive repetitions of the schedule. Finite stores retain a positive
fraction while waiting. The result covers disconnected individual phases and
arbitrary phase ordering, not just a convenient complete graph. The explicit
floor is often weak and is not a practical isolation bound from aggregate
capacity and conductance alone.

The new theorem requires diagonal positive capacities. The original stage1
comparison allows a general constant SPD storage matrix. I separately stressed
that broader algebraic domain: its energy-gap, circle and reversal identities
survive, while some nonlocal SPD examples have positive off-diagonal responses.
Such a matrix cannot be silently treated as an ordinary positive thermal store.

## Withheld evidence and a false zero

Eighty fresh sparse schedules used one active edge per phase and varied node
counts, conductances, capacities, durations and contact order. They produced 680
terminal pairs: 318 connected by admissible internal paths and 362 separated by
terminal cuts. Every support prediction and quantitative reverse floor passed.
The smallest nonzero transfer was 5.13e-5 in this ensemble. The static gap
identity's largest absolute residual was 1.04e-15. These are diagnostics of the
implementation; the universal result comes from the proof.

The withheld slow-cycle cases expose a more consequential numerical issue. For
the original zero-leak three-contact body at z=800, C=G=1 and P=2400:

| Quantity | Actual local calculation |
|---|---:|
| Float64 reverse coefficient | 0 |
| Reverse coefficient at 100-digit precision | 1.528281076740703e-351 |
| Finite forward/reverse ratio | 2.726374572112567e347 |
| Hot-port cooling relative to matched static star | 0.001875 |

An apparent perfect isolator would therefore be an arithmetic-range error,
coupled to severely reduced heat throughput. No physical measurement is implied.

Sixty-four additional cases used nonlocal constant SPD storage matrices with
single-edge disconnected phases. The largest relative gap and reversal residuals
were 1.73e-15 and 4.56e-16; the circle bound's smallest eigenvalue was -2.15e-16,
consistent with roundoff. Two cases have positive off-diagonal responses above
1e-7, making the distinction in capacity hypotheses concrete.

## Stronger positive mechanisms attempted

I replaced the one-body mechanism with two explicit three-body designs:

- Fixed terminal contacts with cyclically switched internal ring contacts.
- Fixed internal ring contacts with cyclically switched terminal contacts.

Each uses total capacity one, total mean conductance one, three modulated contacts
with off/on=.001, and three additional fixed contacts. The extra connectors are
counted. Their summed maximum installed conductance is no larger than the
one-body comparator's, but geometric and actuator costs are not known, so this
is an ideal circuit-resource comparison, not a completed physical comparison.

Ordinary numerical design selection optimizes conductance allocation and period,
and may reverse the contact orientation. For directional throughput:

| Mechanism | Best directional excess / G found | Isolation at that point |
|---|---:|---:|
| Ordinary one-body controller | 0.1076333 | 6.3240 |
| Switched internal ring | 0.0148230 | 1.4846 |
| Switched ports, fixed ring | 0.0310877 | 5.7695 |

The latter isolation search hit its initial period boundary; I did not call that
a global negative. The explicit followup reoptimized at periods up to 10000.
At that endpoint it reaches isolation 69.7091, compared with the one-body
benchmark 69.7837, while forward transfer is only 0.000100262 G versus
0.0534974 G at the one-body isolation optimum. The search therefore supplies no
stronger positive mechanism. It does not prove global failure of every approximate
multi-body router or an asymptotic limit beyond the tested region.

## Established outcome and exact remaining operation

The original finite-isolation operation remains valid within its ideal model.
The first-stage ordinary optimizer reproduces its best directional throughput,
the static comparator still wins the specified cooling task, and the new proof
prevents perfect DC selection by adding finite passive storage and timing alone.

The theorem is not a claim about magnetic/coherent heat circulators, radiative
nonreciprocal primitives, capacity modulation, ideal zero-capacity resets,
infinite conductances or finite consumption of cold preparation. Those operations
are outside the stated positive contact class. Primary sources in SOURCES.md
make these boundaries explicit. Static Kron topology and positive-system
theory are established; novelty of the precise periodic theorem and quantitative
formulation remains unestablished.

A useful **finite-isolation** device is still possible in principle. What remains
unsupplied is a complete compatible contact architecture with measured actuator
work, clock and connector costs, added storage, leakage and preparation, which
demonstrates an advantage over competent conventional routing at those same
resources. These calculations do not supply that operation or justify a
civilisation-changing claim.

## Reproduction and artifacts

All new research is in stage2. Execute stress_support.py,
stress_matrix_capacity.py, architecture_search.py, ring_long_period.py and
plot_stress.py with /usr/local/bin/python3. The scripts read the unchanged stage1
solver with bytecode writing disabled. CSVs contain all tested cases; NPZs retain
the optimized matrices and one nonlocal-capacity example. RESEARCH_NOTES.md
preserves the incorrect broad topology idea, boundary followup and unsuccessful
positive mechanisms. Before/after content checks verify stage1 preservation;
that check has no scientific validation meaning.
