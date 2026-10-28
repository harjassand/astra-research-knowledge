**I completed a new acquired tractable class: arbitrary-target factorization over full chain-ring matrix images, with exact counting, witness construction, and exact uniform sampling of the original input assignments.** The mathematical core, raw-circuit composition, and same-task comparisons now have separate completed internal reviews.

The substantial barrier removed is the need for a unit phase within this new admission. A positive module-image representation handles an entire family of highly constrained right factors, including singular factors, without enumerating the exponentially large character space.

## The completed construction

For an explicitly represented ring
\[
R=\mathbb F_q[t]/(t^e),
\]
the core counts and uniformly samples every pair
\[
X_R\in R^{p\times s},\qquad Y_R\in R^{s\times s},
\qquad X_RY_R=Z_R
\]
for **every target \(Z_R\)** and arbitrary explicit depth \(e\). The right factor is square; the left factor can be rectangular. The theorem covers finite fields generally; the executable uses characteristic-two fields.

The decisive compression comes from conditioning on the actual image \(K=\operatorname{im}_R X_R\), which must contain the target module. Write \(d_K=\dim_{\mathbb F_q}K\) and let \(k\) be its minimum number of ring generators. The number of onto left maps is
\[
q^{s(d_K-k)}\prod_{j=0}^{k-1}(q^s-q^j).
\]
Each such map has \(q^{s(es-d_K)}\) compatible right factors. Multiplying cancels the entire image length:
\[
\boxed{W(k)=q^{s(es-k)}\prod_{j=0}^{k-1}(q^s-q^j).}
\]

This justified cancellation lets the positive Hall recurrence retain only two type coordinates, with **\(O(ep^2)\) states and \(O(ep^3)\) scalar transitions**. It enumerates neither partitions nor submodules. Sampling still retains actual coordinates: it constructs an actual image containing the target, chooses a uniform generating tuple, and solves the actual affine right-column equations. The multiplicities prove uniformity of the complete pair.

A separate literal control at right-image codimension **216** used **14 states, 19 transitions, and zero characters**, with witness and sample checked. That is a structural control, not an end-to-end performance benchmark.

*Governing records: theorem v1, SHA `90fac67d…`; literal implementation `e0185e83…`; independent literal review `2e11c4cd…`.*

## Acquisition and the three operations

The raw compiler starts from ordinary gates and declared independent inputs. It retains the checked terminal traversal, source-free bilinear split, field acquisition, affine matrix coordinates, and corrected original-input reconstruction.

The new stage then acquires and verifies the **whole right image**: its field-linear span, normalization to an algebra, center, nilpotent uniformizer, free natural module, and complete transported matrix span. Ring depth, matrix degree, and coordinates are not supplied as source metadata. All transports are checked before returning original assignments; internal gate wires remain dependent.

Recognition is a **sound randomized partial procedure**. Its bounded search for an invertible element can decline; a decline is never reported as a zero count. The inherited frontend’s admissions and costs remain explicit.

The operations are separately implemented:

- **Count:** the positive image-module recurrence.
- **Witness:** after acquisition, an affine section using an acquired invertible right element.
- **Uniform sample:** weighted actual-image selection followed by uniform onto maps and affine lifts.

The witness-only entry point succeeded with the counting constructor replaced by a function that raises on every call. It reported unknown population and refused uniform sampling. Thus the section does not conceal a counting dependency or imply a sampling law.

The native review independently solved **8,704 source-left affine fibers**, verified the original/source/acquired polynomial identities, and checked **52 fresh original outputs**. No producer correction was required.  
*Independent native review: SHA `01076c5f…`.*

## Same original tasks, equally informed comparisons

Each successful route below performed the same required task: exact count, one witness, and eight exact uniform original-input samples, including acquisition, reconstruction, original-gate checks, and output encoding.

| Control | Original inputs / gates | Exact count | Positive recurrence | XOR-aware route | Informed module route |
|---|---:|---:|---:|---:|---:|
| Depth 2, matrix degree 2 | 20 / 1,131 | 192 | 0.115 s | 0.109 s | 0.115 s |
| Depth 3, matrix degree 2 | 44 / 7,126 | 12,288 | 2.523 s | 2.541 s | 2.520 s |
| Depth 4, matrix degree 1 | 23 / 1,514 | 56 | 0.153 s | 0.137 s | 0.151 s |
| Synthetic ring transfer | 24 / 2,188 | 1,056 | 0.368 s | 0.352 s | 0.364 s |

These are single sequential warm runs. The full common native acquisition and compilation cost was charged to every algebra route, conservatively overcharging the alternatives.

The informed route independently rebuilds the older aggregate-length module recurrence, while explicitly sharing the complete-pair lifting construction. **These results establish no speed advantage. Sharing that construction also does not establish that the complete prescribed-target operation pre-existed.**

The ordinary unique-extension CNF route completed the 20-input task in **3.940 seconds**. All **192** compiled tickets were checked against the actual clauses and original gates, with distinct original projections. The same 44-input circuit did not complete compilation within **30 seconds**; its record makes no count or sampling claim.

The comparison review also checked all **108 saved algebra outputs** and disclosed the extra diagnostic output encoded by the algebra routes.  
*Independent comparison review: SHA `346e94bf…`; separate independent adapter review: `b8b36d77…`.*

The underlying Hall and matrix-generation formulas are classical. Finite-chain-ring matrix channels provide a scientific setting for these products. The transfer control uses a synthetic observation and a uniform unrestricted latent-factor model, including singular factors; it does not claim measured data or the cited paper’s full-rank transfer prior. [arxiv.org](https://arxiv.org/pdf/1304.2523v2?utm_source=chatgpt.com)

## Preserved boundaries and the next obstruction

At depth two, this completes every target at the regular dual-number **full zero phase**, a genuinely nonunit phase. At higher depth, the acquired complete ring-matrix image is a **different admission** from the older full-dual zero-phase complement.

The rank-one-socle/unit-phase construction retains its acquired full-tensor assumptions. The general faithful-module branch retains its own costs and admissions. The earlier affine-phase, prefix, and repaired sampler constructions remain distinct, with affected versions preserved.

The initial depth-three fixture still declines at the retained frontier. Its revised fixture adds only independent extra equations; that source change is preserved separately and does not enlarge the frontend by assertion.

General nonzero radical phases remain unresolved. Their retained identity
\[
X_RU+(\partial X_R)B=Z_R
\]
identifies the next substantial obstruction: the derivative term requires more information than the image module alone. Arbitrary original-bit conditioning and polynomial counting for unrestricted circuits remain unproved.

The completed capability is **exact conditional inference and generation for an acquired family of noncommutative matrix factorizations at arbitrary explicit ring depth**. The civilisation-level objective remains open.

Proofs, executable work, controls, reviews, and useful failures remain in the existing working directory. No upload, export, archive retry, or transfer was attempted; the older ZIP remains the earlier checkpoint.