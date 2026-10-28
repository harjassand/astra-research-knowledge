**Completed a broader polynomial counting and exact-sampling construction: faithful modules with rank-one socle action, including nonfree modules and non-chain algebras.** This removes the \(2^{as^2}\) residue-character factor on that class, allowing unrestricted matrix degree \(s\) and growing full affine codimension \(aes^2\).

The literal construction, raw-input integration and comparison have completed internal reviews against frozen versions.

## The new representation

Let \(A\) be a split local Frobenius algebra of dimension \(e\), acting faithfully on an \(m\)-dimensional module \(V\). Let \(N\) be the **actual acquired action of a socle generator**, and require \(\operatorname{rank}N=1\). The module need not be regular or free.

For the complete tensor \(M_s(A)\), a prescribed **unit phase**, and any product target \(Z\in F_q^{p\times ms}\), the exact count is

\[
\boxed{
q^{(2m-e-1)s^2}
C_q\!\left(p-r_0,(m-1)s,(m-1)s,r-r_0\right)
}
\]

where

\[
r=\operatorname{rank}Z,\qquad
r_0=\operatorname{rank}\!\left(Z(N\otimes I_s)\right).
\]

Here \(C_q\) is the explicit positive Gaussian formula for ordinary matrix-product fibers, with its constructive sampler. No new counting oracle is assumed. The governing arguments are saved in `SOCLE_RANK_ONE_UNIT_PHASE_THEOREM.tex` and `RAW_SOCLE_RANK_ONE_CONSTRUCTION.tex`.

The construction acquires a labelled basis \(H\) satisfying \(HNH^{-1}=E_{0,m-1}\). This turns the residue constraints into one prescribed identity corner. The positive rectangle machinery counts and samples that entire weak fiber. After undoing the transport, a full-phase map with exactly \(q^{(e-1)s^2}\) preimages per final pair gives **exactly uniform final samples**.

This removes the previous regular-module restriction without requiring a module decomposition. It includes \(A\oplus W\) whenever \(W\) is annihilated by the socle generator. Algebra dimension \(e\) and module dimension \(m\) remain separate throughout.

The operations now have distinct admissions:

| Operation | Completed scope and cost after acquisition |
|---|---|
| Count and exact uniform sampling | Rank-one socle action: polynomial in the explicit descriptions, without a residue-character budget |
| Count and exact uniform sampling on any faithful module | Preserved general branch: \(2^{as^2}\operatorname{poly}\), with its documented native admission gate |
| Witness construction on any faithful module | Separate polynomial section; constructs no counted weak engine and reports no invented population |

The raw recognizer remains **commutative, characteristic two, full tensor, acquired parent and unit phase**. The mathematical theorem has broader field/algebra scope than that implemented raw admission.

## Verification and the full original-input pipeline

The new raw entrypoint acquires the field, algebra, actual module, phase and target geometry from the ordinary circuit. It verifies both coordinate transports, reconstructs the original independent variables, and evaluates the original gates. Internal wires never become independent counting variables.

The completed reviews establish several concrete checks:

- Independent literal controls exhausted **2,048 weak pairs**, obtaining 1,024 final pairs with exactly two preimages each, and checked **12,384 additional actual-left fibers**.
- A matrix-degree-five control completed count, witness and sample while the character-counter constructor was forbidden. It made **zero calls**; the generic residue expansion would have contained \(2^{25}\) terms.
- The raw delta review reused the **explicitly identified, hash-verified prior censuses** of 1,024 and 4,096 source-left matrices. It checked **26 fresh original outputs and conditional right fibers**, plus a separate section-only witness. Those censuses were not presented as newly rerun experiments.

These results and their exact version bindings are retained in `SOCLE_RANK_ONE_INDEPENDENT_REVIEW.tex`, `RAW_SOCLE_RANK_ONE_INDEPENDENT_REVIEW.tex` and the associated executable audit records.

The target geometry matters: independent controls with the same target rank but socle-image ranks \(0,1,2\) gave different counts. Thus ordinary target rank alone is insufficient. The repeated-module example with socle rank two correctly **declines this polynomial branch**; its earlier general faithful-module count remains separate and valid.

## Equally informed comparison

Five routes performed the same original task: exact count, one witness and eight exact uniform samples, including raw acquisition, representation, original reconstruction, gate checks and output encoding.

Selected complete-task timings from `compare_socle_rank_one_routes_results.json`:

| Original circuit | Exact count | Positive corner route | Algebra/XOR route | Equally informed Schur route |
|---|---:|---:|---:|---:|
| 34 inputs, 3,631 gates | 1,966,080 | 0.873 s | 0.832 s | 0.852 s |
| 44 inputs, 6,873 gates | 251,658,240 | 2.795 s | 2.780 s | 2.764 s |

The full-phase prefix and informed residue-prefix routes also agreed. These are single warm sequential measurements; common acquisition conservatively includes native compilation work for every route.

**No advantage over equally informed algebra was established.** The direct Schur route can use the same acquired socle representation and has the same polynomial guarantee. The substantive gain is the reusable representation and completed count/search/sample operation, with an exponential dependence removed under precise hypotheses. The comparison and its limitations have a separate completed review.

Higher socle rank, nonunit phases and arbitrary original-bit conditioning remain unresolved by this polynomial branch. The phase-dependent map also does not automatically preserve final-row-prefix conditions. Earlier affine-phase, row-prefix, section and two-carrier results retain their own admissions and reviews.

All proofs, executable work, data, corrections and reviews remain in place. No upload or export was attempted; the older ZIP remains only the earlier checkpoint. The civilisation-level objective remains open, and polynomial counting for arbitrary circuits remains unproved.