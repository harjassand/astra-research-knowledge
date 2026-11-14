# Independent paid-join review

Reviewed the source, rectangle partition, partial-row bound, terminal domination and coordinate accounting against the original open-anchor proof.

1. The anchor here already has m plus sites, so no endpoint-acquisition B0 factor is necessary.
2. At the terminal m-by-(L-1) rectangle, its physical upper boundary is the original anchor. Replacing only those upper boundary incidences by minus increases each source/all-plus-reference weight ratio. It need not correspond to a physical globally consistent boundary configuration. Bottom anchor incidences remain plus. The displayed Q bound therefore still applies under periodic identification.
3. Skipping initially plus sites is deterministic. For a fixed terminal state, summing the original weights of all preimages is at most Q times that terminal state's weight. Early-B exclusions only decrease this sum. This is a pointwise unnormalized pushforward, not an assumption of thermalized arrivals.
4. The second-stage fixed-column flow is linear in its source weights. Domination by Q times the Gibbs weight transfers its pointwise edge load with one Q factor, not two.
5. Stage one uses only the width-m band; this entire band is plus at the join and upward stage two cannot flip it. Thus their coordinate sets are disjoint. The maximum of stage bounds, followed by the original coordinate-current inequality, is legitimate.
6. Paying 2n possible oriented anchor labels and n coordinate cuts gives the stated 4n^2 Q J_line C, provided the inherited one-line constant is used exactly as stated. The displayed upper J_line is larger than exp(2 phi m) on all four numerical instances.

No algebraic or periodic-boundary gap was found. This is a restricted occupation inequality, not an acquired exit-time algorithm. A filled droplet does not imply a solid anchor of this length. No new high-mass source family beyond earlier results has been established by this review, and the R10000 scalar is vacuous.

Executable scalar check was rerun independently: certified floors 513, 1497, 3760 at R80,200,1000, and negative/vacuous floor -503023 at R10000. No empirical dynamics was run.
