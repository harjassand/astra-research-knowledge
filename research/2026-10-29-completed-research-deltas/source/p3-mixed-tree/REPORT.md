**I completed a broader raw-input chain-module construction and a separate construction for branching matrix-product trees.** Both now have governing proofs, executable implementations and completed version-bound internal reviews.

The main advance is **positive image compression without requiring exact length cancellation**. The earlier cancellation mechanism was sufficient, but it was unnecessarily restrictive.

## 1. Mixed inner modules and rectangular factors

The completed raw pipeline now acquires and solves a homogeneous right-factor space

\[
Y\in\operatorname{Hom}_{R}(R^b,U),
\qquad
R=\mathbb F_{2^a}[t]/(t^e),
\qquad
U=\bigoplus_i R/(t^{l_i}),
\]

where the inner module is faithful and may contain arbitrarily many different cyclic lengths. The right matrix may be rectangular. The target is the **complete prescribed product**, including targets with genuinely empty fibers.

Two restrictions have been removed from the earlier chain-ring consumer: the inner module need not be free, and the right factor need not be square.

The new recognition stage computes the entire paired equalizer

\[
\{(P,Q):PY=YQ\text{ for every acquired right-space element }Y\}.
\]

It uses that algebra to recover the chain-ring actions and actual coordinate transports, then verifies equality with the **whole** Hom space. It does not search for an invertible square member of the right space. The inherited ordinary-circuit frontend remains a partial recognizer; a declined encoding receives no counting claim.

The unrestricted left field matrix is identified bijectively with an \(R\)-linear map \(U\to R^p\). This adds no hidden left constraint. Returned factors are transported back through the corrected affine reconstruction, and every original gate and marked target is checked. Internal gate wires remain dependent quantities.

### Why the count stays compressed

Let \(\nu_j\) count the inner cyclic summands of length at least \(j\). For an actual image of conjugate type \(\kappa\), the number of onto left maps and compatible right lifts factors into adjacent positive terms:

\[
T_j(a,c)=
q^{\nu_jc+b(\nu_j-a)}
\prod_{h=c}^{a-1}(q^{\nu_j}-q^h).
\]

Combining these terms with the constructive submodule formula gives **\(O(ep)\) states and \(O(ep^2)\) scalar transitions**. Actual-coordinate linear algebra, local-factor computation, integer bit costs and output costs remain charged.

This extends the tractable class at unbounded codimension: the right Hom space has codimension \(bd(e-1)\) inside its ambient rectangular matrix space. The algorithm does not enumerate all characters, images or partitions as that codimension grows.

The operations remain distinct:

- **Counting:** deterministic polynomial computation after acquisition.
- **Witness search:** a separate deterministic feasibility test and construction, without initializing the count tables.
- **Exact uniform sampling:** an expected-polynomial construction of complete factor pairs, followed by the verified bijection to original assignments.

I also proved the reusable weighted-image corollary: explicitly computed nonnegative factors depending on adjacent type coordinates admit the same compressed partition sum and actual embedded-image sampling. Supplying those factors as an uncomputed oracle would not meet its assumptions.

The governing records are `MIXED_INNER_ALL_TARGET_PRODUCT_THEOREM.tex`, `RAW_MIXED_HOM_PRODUCT_CONSTRUCTION.tex` and `POSITIVE_IMAGE_CLOSURE_AND_BOUNDARY.tex`, with separate geometry, implementation and native-composition reviews.

## 2. Complete-output conditioning on matrix-product trees

A second completed construction handles independent rectangular matrices on a rooted tree, with every complete root-to-leaf product prescribed.

A subtree’s completion function has the form

\[
f(P)=
\mathbf 1[L\subseteq\operatorname{im}P]\,
w(\operatorname{rank}P),
\]

where \(L\) is the **actual span of its descendant target columns**. Branching combines these actual subspaces and multiplies rank weights; integrating an edge preserves the representation.

This replaces enumeration of complete prefix matrices with **\(O(np)\) rank states and \(O(np^2)\) scalar transitions**, for \(n\) vertices and root dimension \(p\), plus the paid matrix operations. It supports unbounded depth and branching, exact counts, an independent deterministic witness construction, and exact joint uniform sampling of **all edge factors**.

The traversal visits shared prefixes once. The proof also keeps the terminal distinction explicit: a leaf requires its precise target matrix, so its contribution is an affine lift count, without an extra image or rank multiplicity.

**This result has literal-coordinate admission.** The tree, field and edge-variable interpretation are supplied and checked. Hidden arbitrary-depth tree acquisition from an ordinary Boolean circuit is not established.

Its governing source is `MATRIX_PRODUCT_TREE_THEOREM.tex`, with a separate completed implementation review.

## 3. Decisive checks and equally informed comparisons

The completed reviews include:

- **4,672 independently solved source-left fibers** for the raw mixed-module controls, producing counts \(128,64,0,4608\).
- Exact original polynomial, Hom-space, transport and affine-reconstruction checks, plus **39 fresh original-gate witness/sample checks**.
- Exact conditional sampler-law audits covering **768** complete pairs in a mixed-length case and **192** in a rotated-field case, with the required uniform probability for every pair.
- For the tree sampler, **320 accepted decision paths** aggregating to **170 complete tuples**, each with probability exactly \(1/170\).

These probability checks are finite exact audits, not frequency tests.

The same-original-circuit comparison requested an exact count, one witness and eight uniform samples, including acquisition, reconstruction, gate checks and output encoding:

| Original inputs / gates | Count | Positive construction | XOR affine-fiber route | Equally informed forward route |
|---|---:|---:|---:|---:|
| 18 / 996 | 128 | 0.084 s | 0.075 s | 0.087 s |
| 32 / 3,899 | 64 | 0.799 s | 0.785 s | 0.805 s |
| 36 / 3,694 | 4,608 | 1.072 s | 1.048 s | 1.068 s |

These are single warm sequential measurements. Every algebra route is charged the common acquisition and native representation/count work; alternatives additionally pay their own work. That conservatively overcharges the alternatives. **There is no demonstrated speed advantage over the equally informed routes.**

The forward route independently computes its recurrence and type selection while sharing the new actual-image and factor-lifting construction. Its successful adoption does not establish that the complete construction previously existed.

The ordinary CNF route completed the 18-input task in **1.020 seconds**, with all 128 sampling tickets independently checked. The configured 32-input compilation timed out after 30 seconds, yielding no count or sampling claim. This is a result for that solver configuration, not a lower bound on conventional methods. The saved comparison and its independent accounting review bind the exact sources and outputs.

Classical image/flag disintegration is a relevant antecedent, including Huang’s treatment of rectangular matrix products. I have preserved that relationship without assigning historical priority to the present composition. :chatgpt-content-reference{index="0"}

## 4. The remaining obstruction is now more precise

For a nonfree output module, the total image of the left map loses necessary information. Lifting depends on the nested actual images

\[
K_j=\phi\bigl(U[t^j]\bigr).
\]

I proved and saved the exact fixed-left lifting formula using these spaces. It gives ordinary affine-fiber counting and sampling once the left map is fixed. **A compressed global sum over those filtered images remains unresolved.**

The two 60-input encodings retain their separate acquisition failures. Neither is recorded as an empty fiber or a successful larger example. The geometric proof’s earlier nonfaithful obstruction was corrected in version 2; the affected version remains preserved. Earlier complementary constructions and repaired samplers retain their separate admissions.

All proofs, executable work, data, corrections and reviews remain in place under:

`producer-workspace/chain_extensions`

No upload, export or archive operation was performed.

The completed advance is an enlargement of Astra’s proved constructive classes: mixed-module factorization through an acquired raw pipeline, and complete conditional generation on branching matrix products. The civilisation-level objective remains open, as do arbitrary-circuit polynomial counting and unrestricted affine conditioning.