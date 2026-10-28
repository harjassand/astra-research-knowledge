**The main result is a constructive polynomial algorithm for a family of shared-variable Gram networks with growing, potentially crossing separators.** Its decisive invariant is the changing kernel inside the prescribed hub’s radical. The construction counts solutions, produces witnesses, and samples complete solutions exactly uniformly. A narrower compiler now acquires the required hidden structure directly from admitted ordinary Boolean circuits.

Both constructions have completed **version-bound internal reviews**, with no producer correction required in their final reviewed versions.

## Scientific destination and the barrier removed

I chose **exact inference in algebraic systems that reuse the same unknowns** as the overarching target. Success would let a compiler condition, count and generate interacting structured systems without enumerating every possible shared state. That would extend the usefulness of exact inference substantially beyond independent or read-once constructions.

I compared this with the materially different opening of **recovering hidden observation flags for large-codimension conditioning**. That branch also produced a completed construction, including protected subspaces and a reviewed unit-phase adapter. The shared-variable direction earned the main commitment because it attacks a compositional obstruction: individually tractable factors can become difficult when they constrain the same unknown.

### The completed principle

Let one unknown matrix \(U\) satisfy a prescribed alternating Gram equation
\[
U^{T}JU=A.
\]
Each satellite \(Y_j\) constrains a supplied portion \(UD_j\) of that **same** hub and has its own prescribed internal Gram matrix.

Write \(Z=\operatorname{rad}(A)\). For nonsingular ambient \(J\),
\[
K=\ker U\subseteq Z,\qquad
\dim\ker(UD_j)=\dim\!\left(K\cap(\operatorname{im}D_j\cap Z)\right).
\]

This identifies the information that must survive elimination. **Only the separators’ intersections with \(Z\) need to form a nested chain. Their complete spaces may cross.**

The algorithm counts and reconstructs actual admissible kernels through positive subspace extensions. Its kernel dynamic program has \(O((L+1)(h+1))\) states and \(O(L(h+1)^2)\) transitions, where \(h=\dim Z\) and \(L\) is the number of distinct radical traces. Coordinate acquisition within the supplied geometry, local Gram operations, integer arithmetic and output costs remain charged.

The resulting operations are distinct:

- **Count:** deterministic polynomial exact counting for the admitted supplied geometry.
- **Witness:** deterministic construction when the population is positive; the implementation computes counts first.
- **Uniform sampling:** exact sampling of the complete shared hub and all satellites, using positive mixtures and constructive conditional fibers.

A supplied jointly onto binary-affine original-input map can then restore original assignments with their exact multiplicity. Degenerate ambient forms are handled through a symplectic quotient and explicit radical lifts.

This unifies the earlier full-hub and nested isotropic constructions. In particular, when \(A\) is nonsingular, its radical is zero and **arbitrary supplied separator spaces** are admitted. The governing argument and executable construction are preserved in :chatgpt-content-reference{index="0"}[RADICAL_TRACE_GRAM_NETWORK.tex](producer-workspace/RADICAL_TRACE_GRAM_NETWORK.tex) and :chatgpt-content-reference{index="1"}[flagged_gram.py](producer-workspace/flagged_gram.py).

## What ordinary input now supplies

The separate raw compiler recovers the hidden ambient matrix factor, hub/satellite roles, and affine original-input map from an admitted Boolean gate DAG. It checks the complete acquired quadratic identity and counts **original independent inputs**; gate wires never become extra independent variables.

Its admission remains narrower: binary coefficients, the documented quadratic frontend, a certified full shared-hub observation space, and an onto acquired matrix chart. Acquisition is Las Vegas expected polynomial. Counting and witness construction are deterministic after acquisition.

The broader radical-trace theorem still receives its field, tensor chart and separator geometry explicitly. Recovering that broader geometry from raw partial observations remains an unresolved bridge.

The final independent raw audit checked a new 10-input circuit with repeated shared terminal layers against every original assignment. All **576 production sampling paths after acquisition** gave each of its 48 solutions probability exactly \(1/48\). The review also checked growing ambient acquisition, affine reconstruction, unsupported geometries and distinct emptiness cases. See :chatgpt-content-reference{index="2"}[RAW_GRAM_ACQUISITION_INDEPENDENT_REVIEW.tex](producer-workspace/RAW_GRAM_ACQUISITION_INDEPENDENT_REVIEW.tex).

## A useful failure changed the representation

Replacing the restriction with generic chordal overlap failed decisively. I proved an exact reduction from bipartite independent-set counting to Gram counting on **split graphs in a two-dimensional binary symplectic space**.

That failure motivated preserving actual radical-kernel information instead of relying on overlap topology or coarse ranks. The reduction also preserves the distinction between operations: the all-zero assignment always provides a witness in those instances, so its counting obstruction is not a witness-search obstruction. The proof is saved in :chatgpt-content-reference{index="3"}[CHORDAL_GRAM_BOUNDARY.tex](producer-workspace/CHORDAL_GRAM_BOUNDARY.tex).

The broader positive construction passed its own independent review, including dense coordinate changes, actual target pullbacks, conditional populations and the constructive sampling argument: :chatgpt-content-reference{index="4"}[RADICAL_TRACE_GRAM_INDEPENDENT_REVIEW.tex](producer-workspace/RADICAL_TRACE_GRAM_INDEPENDENT_REVIEW.tex).

## Equally informed comparison

The matched task was the **same original circuit’s exact count, one witness, and eight fresh exact uniform original-input samples**, including acquisition and output checking.

| Route | 17-input task | 12-input task |
|---|---:|---:|
| Acquired positive construction | 0.0551 s | 0.0151 s |
| Fixed-hub Gaussian method | **0.0481 s** | **0.0096 s** |
| Explicit adoption of the positive construction | 0.0503 s | 0.0186 s |
| Ordinary CNF + d4 | 4.7530 s | 0.0724 s |

These are single measurements with warm imports. **They establish no speed advantage over the informed Gaussian method.** Complete integer-ticket audits checked both conventional samplers on these cases. The adoption route explicitly reuses the construction; that does not establish historical precedence. Full accounting and qualifications are in :chatgpt-content-reference{index="5"}[FIXED_HUB_GAUSSIAN_COMPARISON.tex](producer-workspace/FIXED_HUB_GAUSSIAN_COMPARISON.tex).

The consequential addition is the proved representation: shared separators can grow and cross while exact constructive inference remains polynomial under the stated radical-trace condition. This is a reusable piece of the larger computational objective, with a separate acquired raw-input foothold. It does not establish unrestricted circuit counting or achievement of the civilisation-level mission.