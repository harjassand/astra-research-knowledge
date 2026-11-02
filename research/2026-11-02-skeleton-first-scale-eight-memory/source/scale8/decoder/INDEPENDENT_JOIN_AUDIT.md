# Independent joined trace/duality review

Reviewer: `producer-workspace/audit_component_contour_proof`, 2026-11-02.

Reviewed `FULL_TRACE_REMOVABLE_EXTENSION.md` together with `producer-workspace/REMOVABLE_TRACE_EXTENSION.md`.

## Core conclusion

The join is sound under the explicit full-trace interfaces and the native local-ratio hypothesis. The physical prepass must be included in the fixed ambient graph and in the two-run whole-component/matching construction, not treated as a separately uncharged map.

For every row of F², retaining a zero-output gate whenever it has an occupied contributor is essential and sufficient for the selected-component property: all occupied contributors in that row belong to one augmented trace component, even if their XOR vanishes. Hence F² tau equals the selected dual input. Restriction of the dual full trace gives d_B r_C = F² tau before assuming tau valid. The all-vectors top-degree identity then gives d_A(G¹r_C+H²tau)=tau. Kernel-only prepass components are covered by H²tau and do not require a nonzero dual output.

Selected dual input mass is bounded by the column norm of F² times selected physical input mass. Complete selected dual trace components therefore have total size proportional to all selected physical leaves. Completing the trace need not preserve the mass of a smaller ancestor skeleton; the correct mass is the leaf set after completion. The text makes this distinction explicitly.

The G image of fully lifted corrections belongs in the physical support estimate, not the entropy animal. Its bounded column norm changes support constants, while expanding that image into physical trace vertices could introduce a scale-dependent factor. H is similarly applied algebraically and has bounded single-fault discrepancy support.

## Two precision requirements to make explicit

1. **Match the entire augmentation in the two-run graph.** Add matching-site edges for all corresponding active/stencil vertices, including physical base leaves and prepass gates. Then every occupied physical leaf outside the fault set selected in one run is selected in the other, yielding |tau'| <= |tau|+k. The companion theorem's matching rule already has this form when applied to the augmented graph, but the local extension describes the transfer implicitly as “two-run indexing.” A direct sentence would prevent an implementation that only matches dual trace vertices.

2. **Specify the Gibbs syndrome measure or assume its ratio.** Additive excitation energy alone does not imply the displayed probability ratio if syndrome-sector multiplicities vary. It suffices that pi(s) is proportional to exp[-beta E(s)] over the valid syndrome space, as for equal-degeneracy commuting Pauli stabilizer sectors, or that the native local-ratio theorem supplies the stated inequality. The conditional join already permits the latter route. This is a measure-identification clarification, not a counterexample under the explicitly assumed native ratio.

Both points were reported to the local-duality auditor. Neither changes the abstract full-trace proof or supplies missing concrete family geometry. The remaining map, stencil, terminal, and native-ratio hypotheses must still be verified in the actual application.
