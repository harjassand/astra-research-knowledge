# Exact common-seed time change and the next genuinely graph-level profile problem
Status: algebraic representation and scoped research consequence, not a new recurrence theorem. Separate from all frozen proofs.

Suppose every homogeneous degree-m fast complex contains at least a0 A, 1<=a0<m. Set A'=A-a0 on the active region A>=a0, v=m-a0, and subtract a0 A from every fast complex. The resulting graph is homogeneous of degree v. For a source with A multiplicity a0+u,

    (A)_(a0+u)=(A)_a0 (A-a0)_u.

Thus the fast generator is EXACTLY the residual degree-v mass-action generator, multiplied by the common positive state-dependent factor (A)_a0 (and the common B catalyst). Clearing at (A)_m similarly factors as (A)_a0 (A')_v. Removing the common clock factor preserves the entire fast/clearing embedded path and clearing-output distribution. It does not preserve physical time or occupation integrals.

If the original graph contains mA and a0 A+vX_i for every reservoir, the residual graph contains EVERY pure vX_i, including vA'. Its strong connectivity is unchanged. Therefore the already-earned pure-source accessibility/clearing machinery applies to its operational-time fast/clearing process when v>=2, WITHOUT requiring that every reservoir pure source have an immediate A-producing outgoing edge.

The physical clock is recovered by occupation weights:

    physical T = E int_0^tau_op 1/[(A'+a0)_a0 (B)_q] ds,
    physical U = E int_0^tau_op (A'+a0)/[(A'+a0)_a0 (B)_q] ds.

This explains why the clearing-output law can be strongly concentrated away from low A while the physical time/occupation ratio stays nonvanishing at low-A starts. It also identifies the true remaining information: profile transport through the whole connector cycle, not operational-time fast mixing.

The current incoming-moment proof requires immediate A-production from each source a0 A+vX_i; it uses a pointwise sign for Q f_s(A). Weak reversibility alone supplies paths, not that sign. For example, a residual pure-complex chain vC->vD->vA'->vC started with C large, D=0 and small A' has no immediate A'-production. A scalar inverse-A drift can fail even though the graph is strongly connected and operational-time clearing is fast.

The next structural profile must therefore retain reserves in upstream species or phases along reaction paths, not only A. An exact killed-fiber resolvent can define such a profile, but its shift/comparison bounds across actual connector additions cannot be assumed: earlier pointwise resolvent-ratio obstructions remain failures. A graph-derived multi-coordinate reserve profile with controlled connector shifts would remove the immediate-production premise. This is the next consequential graph-level obligation, rather than further increasing a0 or q inside the already favorable directional class.
