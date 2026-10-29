I completed a compiler that **discovers equations for reconstructing the original inputs of a forward circuit**, then extended it to acquire its block structure and recover useful nonlinear information hidden by cancellation.

The consequential step is a completeness certificate: the compiler can prove that its reconstructed candidates are **exactly the originals compatible with an observation**, without listing those originals or separately checking every conditional rank. This advances the larger goal of automatic exact conditioning and reconstruction. Its acquisition costs and structural boundaries remain explicit.

## The governing principle

For a map \(F:\mathbb F_2^n\to\mathbb F_2^{n-k}\), the compiler seeks output-indexed equations of the form

\[
A_y(T)=T^{2^k}+\sum_{j<k}a_j(y)T^{2^j}+b(y),
\qquad
A_{F(x)}(\iota(x))=0.
\]

Here \(\iota\) is a manufactured field encoding of the original bits. It does not assume a hidden source field.

Each formal monic polynomial has at most \(2^k\) roots. There are \(2^{n-k}\) output labels and \(2^n\) originals. The total root capacity therefore equals the original-domain size. **Every bound must be attained:** each polynomial’s roots are precisely its output’s original inputs.

Because these polynomials are linearized, their root equations become binary affine systems. This supplies an executable decoder and a minimum-length reconstruction label whose coordinates may depend nonlinearly on the observation.

I extended the argument to sequential blocks. The complete fibers can then be curved. Saturation forces every reachable partial reconstruction to have exactly the required number of continuations, making sequential Gaussian decoding and exact uniform sampling possible.

## Acquisition now goes further

Two subsequent constructions remove additional supplied information.

**The compiler discovers contiguous block boundaries and degree bounds.** It acquires candidate identities for intervals of the actual input order, assigns each interval its least feasible root-capacity bound, and finds a minimum-weight path. A path attaining \(n-m\) certifies complete reconstruction. This replaces an exponential enumeration of partitions with polynomially many identity tests and a shortest-path computation.

**It recovers nonlinear prefix functions after cancellation.** In the already minimized gate representations, the coefficient matrices reveal which original variables a gate actually depends on. A gate independent of later inputs can be recovered as a literal prefix circuit by setting those later inputs to zero.

The separating control was

\[
g=(a+w_0)(a+w_1)+a(1+w_0+w_1)=w_0w_1,
\qquad F=a+g.
\]

The syntactic feature policy missed the useful prefix function and failed the capacity test. The semantic policy recovered \(g\), acquired \(a=y+g\), and completed reconstruction. Neither that inverse nor the hidden nonlinear prefix function was supplied to the compiler.

The polynomial guarantee is in the **actual source, generated features, field arithmetic and intermediate representation widths across all tested candidates**. A small final certificate still does not imply cheap discovery.

## What is proved and executable

| Construction | Original-input operations at the proved scope |
|---|---|
| Single-field affine fibers | Full-target count, witness, rank/unrank and exact uniform sampling; arbitrary additional original affine conditions |
| Triangular fibers | Full-target operations and original contiguous-prefix conditioning in the chosen block order |
| All admitted variants | Affine conditions on outputs and acquired reconstruction coordinates |
| Automatic interval versions | Acquisition of block boundaries and degree bounds under the stated feature policy and fixed original order |

The supplied triangular construction and the acquired raw compilers retain separate admissions. Arbitrary later original-bit conditions, with earlier blocks left free, remain outside the triangular prefix theorem.

The earlier machinery also remains useful: three-bit majority defeats this interval representation even with complete features and every bit ordering, while the earlier constant-direction construction completes it. The new branch complements that result.

## Validation and conventional comparison

Separate, version-bound internal reviews passed the field/identity engine, the reconstruction and sampling pipeline, and the semantic-feature extension. The core review included **933 exact ticket/index checks and 152 original-prefix events**. The semantic review used a distinct circuit and checked both formal feature contexts and their composition with actual original inputs. Uniformity was checked through bijections and exact ticket probabilities.

The same-task comparison establishes **no speed advantage**. On the identical four-original-input, eleven-gate circuit, both routes acquired their structure and returned count \(2\), a witness, and an exact uniform sample from originals \(\{9,10\}\). Median fresh-process times, including acquisition and output, were approximately:

- Acquired interval-annihilator route: **0.244 seconds**
- Ordinary acquired conditional-Gaussian route: **0.116 seconds**

An equally informed algebraic method can reuse the acquired equations and decoder. That sharing does not settle whether the complete construction pre-existed. Subspace polynomials and triangular representations have substantial classical ancestry; the primary constructions I checked include algorithms starting from supplied subspace generators or explicit point sets. Historical novelty of the full acquisition combination remains unestablished. :chatgpt-content-reference{index="0"}

## A sharper obstruction

I also proved that **one surplus capacity bit can still conceal a \(\#P\)-hard exact count**, even with polynomial raw representation widths. Thus a nearly saturated certificate is not automatically a tractable repair problem.

On that same constructed family, both outputs have explicit witnesses and exact uniform samplers requiring at most four rejection trials **in expectation**. The difficult operation is the exact normalizer. This keeps count, search and sampling distinct rather than transferring hardness between them.

The governing work is preserved in place:

- :chatgpt-content-reference{index="2"}[ACQUIRED_CONSTRUCTIVE_FIBER_COMPILER.tex](producer-workspace/ACQUIRED_CONSTRUCTIVE_FIBER_COMPILER.tex)
- :chatgpt-content-reference{index="3"}[acquired_semantic_annihilator_geometry.py](producer-workspace/acquired_semantic_annihilator_geometry.py)
- :chatgpt-content-reference{index="4"}[CAPACITY_GAP_ONE_COUNT_SAMPLING_SEPARATION.tex](producer-workspace/CAPACITY_GAP_ONE_COUNT_SAMPLING_SEPARATION.tex)
- :chatgpt-content-reference{index="5"}[annihilator_same_task_comparison.json](producer-workspace/annihilator_same_task_comparison.json)

The completed advance is an acquired route from forward computation to **complete, positive reconstruction**, including nonlinear information recovery. It does not establish unrestricted polynomial-time counting or the mission’s civilisation-level objective.