# Retained-core acquisition: additional primary-literature challenge

This addendum supplements `MIXED_INTERFACE_PRIOR.md`. The target is an algorithm which, given only an alternating binary `B`, finds a small deleted coordinate set and an exact retained decomposition when some `B=A+S` has `rank_GF2(A)<=r` and at most `M` unordered nonzero entries in `S`. The proposed algorithm deletes `O(sqrt(rM)+r)` coordinates and uses an entropy-sized subset search plus `2^r` codeword enumeration. The promising regime is every `r=o(n)` when `M=O(n)`.

## 1. Closest additional acquisition ancestry: perturbed incidence matrices

**Fomin, Golovach, Misra, Ramanujan, “On the Complexity of Recovering Incidence Matrices,” ESA 2020, DOI 10.4230/LIPIcs.ESA.2020.50.** Section 3.2, Lemma 13 enumerates possible low-rank column spaces in `(mn)^{O(r)}` time when a binary matrix is a rank-`r` perturbation of a graph incidence matrix. Observation 15 enumerates `2^r` codewords to connect observed columns to possible incidence columns. Lemmas 19–20 then use matching; further graph classes use matroid intersection. Theorem 11 gives an enumeration algorithm with `(mn)^{O(r)}` delay.

Primary full paper: <https://drops.dagstuhl.de/storage/00lipics/lipics-vol173-esa2020/LIPIcs.ESA.2020.50/LIPIcs.ESA.2020.50.pdf>, pages 50:8–50:9. DOI page: <https://doi.org/10.4230/LIPIcs.ESA.2020.50>.

**Comparison.** This is genuine prior acquisition of a low-rank-plus-sparse description, with basis enumeration and binary-code membership as mechanisms. It deserves citation as ancestry. An incidence column has exactly two ones, whereas the retained-core problem allows arbitrary sparse support and symmetric adjacency matrices. More importantly, the stated `(mn)^{O(r)}` dependence is `2^{O(r log n)}` for square matrices, which is not subexponential for every `r=o(n)`. The paper does not give the coordinate-puncturing/unique-decoding guarantee under audit. Its exact full-incidence reconstruction is also a stronger output requirement than retaining an adequate core.

## 2. Graph rank editing: field and uniformity matter

The original proofs are available in **Syed Mohammad Meesum, “Matrix Editing via Multivariate Lens,” PhD thesis, 2017**, Chapter 2, based on the Meesum–Misra–Saurabh TCS 2016 paper.

Primary thesis record: <https://www.imsc.res.in/xmlui/handle/123456789/413>. Full PDF: <https://www.imsc.res.in/xmlui/bitstream/handle/123456789/413/HBNI%20Th126.pdf?isAllowed=y&sequence=1>.

PDF page 53, Theorem 5, explicitly uses matrices over the **reals**. Theorems 6 and 11 give minor-hitting branching algorithms with `2^{O(k log r)} n^{O(1)}` time for vertex deletion and edge editing. The fixed-r subexponential edge-editing theorem is Theorem 13. Its proof enumerates reduced target graphs. The footnote on PDF page 62 explicitly hides dependence on fixed `r` in the `O*` notation. These statements must not be silently promoted to a uniform growing-r GF(2) theorem. The elementary minor-hitting argument itself does transfer to GF(2), but its budget is the number of deleted vertices or changed edges needed to make the **whole** remaining matrix low rank.

### A concrete obstruction to using vertex deletion as a substitute

This is a direct calculation. Let `S` be the adjacency matrix of a perfect matching on even `n`. Then `M=n/2` and `rank_GF2(S)=n`. For any alternating `A` of rank at most `r`, `B=A+S` has rank at least `n-r`. Deleting `s` coordinate vertices deletes `s` rows and `s` columns, dropping rank by at most `2s`. Hence

`rank(B[R,R]) >= n-r-2s`.

Making this rank at most `r` requires `s >= (n-2r)/2`. For `r=o(n)` that is a linear number of deleted variables. The proposed compiler is allowed to retain the matching residual, so it does not encounter this requirement. This is a distinction between the targets, not a lower bound against other decomposition algorithms.

## 3. Column subset approximation has a different loss

**Dan, Hansen, Jiang, Wang, Zhou, “Low Rank Approximation of Binary Matrices: Column Subset Selection and Generalizations,” MFCS 2018.** Theorems 2–3 show that choosing `r` actual columns permits approximation factor

`r/2 + 1 + r/(2(2^r-1))`,

and the factor is asymptotically tight for that method on general binary matrices. Primary paper: <https://drops.dagstuhl.de/storage/00lipics/lipics-vol117-mfcs2018/LIPIcs.MFCS.2018.41/LIPIcs.MFCS.2018.41.pdf>, pages 41:4–41:5. DOI: <https://doi.org/10.4230/LIPIcs.MFCS.2018.41>.

Trying unordered column subsets and all `2^r` coefficients can have the desired entropy-sized search. However, the cited guarantee enlarges the sparse error budget from `O(M)` to `O(rM)`. For polynomially growing `r` and `M=Theta(n)`, this need not be a near-linear number of local phase factors. This comparison does **not** assert that their tight examples are symmetric or that every extension of column selection fails. It identifies why the published guarantee does not by itself subsume the new counting regime. The puncturing method instead sacrifices a small coordinate set to preserve an `O(M)` residual.

## 4. Robust subspace recovery does not remove the sparse residual

**Dahiya, Fomin, Panolan, Simonov, “Fixed-Parameter and Approximation Algorithms for PCA with Outliers,” ICML 2021**, Theorem 1.4, solves robust subspace recovery in `2^{O(k(log r+log k))} n^{O(1)}` time. Its model uses real vectors and at most `k` nonzero **rows** of corruption; all other rows lie exactly in the low-dimensional subspace. Primary paper: <https://proceedings.mlr.press/v139/dahiya21b/dahiya21b.pdf>, pages 1–3.

The matching example above has a corruption in every row. A nearly linear number of changed entries is not a small number of outlier rows. Neither the output requirement nor the field is the same. The paper's geometric noisy-inlier results use additional separation assumptions and also do not directly apply.

**Candes, Li, Ma, Wright, “Robust Principal Component Analysis?”, JACM 2011**, Theorem 1.1, is also not a direct comparator in the required algebra: it uses real low rank, singular-vector incoherence, and uniformly random sparse support. Primary preprint: <https://arxiv.org/pdf/0912.3599>, Sections 1.3–1.4. The proposed retained-core theorem assumes none of these distributional or incoherence conditions.

There is a sharp field mismatch even without noise. Index rows and columns by `x,y in GF(2)^d`, with even `d`, and set `A_xy=x^T J y` for an invertible alternating `J`. This alternating binary matrix has GF(2)-rank `d`. As a real matrix, its rank is `2^d-1`: writing `A=(1-H)/2`, the character matrix `H_xy=(-1)^{x^T J y}` is a Walsh matrix, and the sole null direction of `A` is the coordinate indexed by zero. Therefore small GF(2) rank need not imply small real rank. This calculation is not attributed to the PCA papers.

## 5. Sparse residuals can force large rank width, even after acquisition

**Lee, Lee, Oum, “Rank-width of random graphs,” Journal of Graph Theory 70(3), 339–347 (2012)**, Theorem 1.1(iii), proves that for each fixed `c>1`, `G(n,c/n)` has rank width at least `gamma(c)n` with probability tending to one. It also has `O(n)` edges with probability tending to one. Primary full preprint: <https://discovery.ucl.ac.uk/id/eprint/10120245/1/rankwidth.pdf>. DOI: <https://doi.org/10.1002/jgt.20620>.

The following transfer is elementary and useful here. If `B=A+S` and `rank(A)<=r`, then for every cut `(X,Xc)`,

`|rank(B[X,Xc])-rank(S[X,Xc])| <= r`.

Taking the maximum cut in a fixed decomposition, then minimizing over decompositions, gives

`|rw(B)-rw(S)| <= r`.

Thus a rank-`o(n)` dense perturbation of such a sparse random graph still has linear rank width. Deleting `s` vertices can decrease rank width by at most `s`: extend any decomposition of the remaining graph by attaching those leaves, increasing each relevant cut rank by at most `s`. Consequently even after the proposed `s=o(n)` deletion, the complete retained matrix can have rank width `Omega(n)`.

This defeats a claim that the mixed family is merely small-rank-width in disguise. It does not prove counting hardness or exclude another polynomial-time representation.

## 6. Phase-evaluation caveat and final scope

A phase that is entirely a binary quadratic sign is already exactly evaluable by Gaussian elimination, regardless of graph width. The comparison becomes meaningful only in the presence of a nonlinear/non-Clifford local foreground, such as a linear number of cubic signs, or appropriate non-Clifford unary phases. Linear rank width is then a limitation of a width-based evaluation bound, not an unconditional running-time lower bound.

For a **supplied** low-rank-plus-sparse decomposition, Walsh expansion of the low-rank part followed by the local phase theorem is already the direct algorithm. The retained-core acquisition is the substantive extra step under audit. The strongest exact general GF(2) competitor remains Fomin–Golovach–Panolan 2020 plus the explicit alternating-core repair in the preceding note. This additional focused search found mechanism-level ancestry, but no primary theorem that supplies the full retained-core guarantee and covers every `r=o(n)` at `M=O(n)`.

No first-priority, optimality, or practical speed claim is established by this audit. No new executions were performed for this literature addendum.

## 7. Free diagonal completion: an important already-solved boundary

The strengthened promise is `B = D + diag(v) + S`, where `B` is alternating, `D` is symmetric of GF(2)-rank at most `r`, and `S` has at most `M` unordered off-diagonal edges. This changes the appropriate graph parameter from adjacency rank to minimum rank with a free diagonal. The following primary results must be included when describing the scope.

**Eugene Kogan, “On the rank of Z_2-matrices with free entries on the diagonal,” arXiv:2104.10668 (2021).** <https://arxiv.org/pdf/2104.10668>. Define `R(B)=min_v rank(B+diag(v))`. Theorem 2 and Remark 3 construct an actual completion `D` in `O(n^4)` time with

`R(B) <= rank(D) <= 2 R(B)`.

It chooses an invertible completion `B'` and returns `B'+I`; Lemma 7 proves the guarantee. Thus **`M=0` already has polynomial acquisition with rank at most `2r`**, sufficient for subexponential rank-dependent expansion whenever `r=o(n)`.

Theorem 1 displays exact-completion time `O(n^{r+4})`. Its proof actually enumerates diagonal changes having at most `r` zero entries. Consequently its uniform bound is `poly(n) sum_{j<=r} binom(n,j)`, also subexponential for every `r=o(n)`. The factor-two algorithm is preferable when exact minimum rank is unnecessary.

**Buchanan, Purcell, Rombach, “Subgraph complementation and minimum rank,” Electronic Journal of Combinatorics 29(1), P1.38 (2022).** Primary full text: <https://arxiv.org/pdf/2101.06180>; published DOI: <https://doi.org/10.37236/10383>. The paper defines `mr(G,F_2)` as minimum rank of a symmetric matrix whose off-diagonal zeros are exactly the graph's nonedges. Since the only nonzero field element is one, this is exactly the free-diagonal parameter above. It relates this minimum rank to the least number `c_2(G)` of clique edge sets whose symmetric difference is `E(G)`, proving

`mr(G,F_2) <= c_2(G) <= mr(G,F_2)+1`.

This gives representation ancestry for unknown diagonal freedom and sums of clique phases. It does not in the inspected theorem provide the new sparse-error retained-core guarantee. Avoid conflating this graph minimum rank with index-coding minrank, whose constraints on diagonal and edge entries differ.

The complete graph illustrates why diagonal freedom broadens the former alternating-rank promise: its adjacency matrix is `J+I`, whereas choosing all diagonal entries one gives rank-one matrix `J`. This example is already covered by Kogan's algorithm; it is an illustration of scope, not evidence of new algorithmic content.

### Updating the Fomin–Golovach–Panolan comparator

For the strengthened promise, `B` is entrywise within `K=2M+n` of the symmetric rank-`r` matrix `D`. Fomin–Golovach–Panolan's Theorem 6 therefore provides a rank-`r` matrix `X` at entry distance at most `K` in

`2^{O(r sqrt(K log(rK)))} poly(n)`

time. It need not return a symmetric `X`. The threshold/row-basis support-cover argument in `MIXED_INTERFACE_PRIOR.md` applied to `X+X^T` deletes `O(sqrt(rK)+r)` coordinates and makes the retained `X` symmetric. In the strengthened setting its diagonal can simply be retained and handled by the proposed Z4 quadratic refinement, so the additional diagonal-removal lemma is unnecessary. The retained off-diagonal residual has at most `K/2` unordered edges. This budget may exceed the original `M`, but is still `O(M+n)`, which is enough for the near-linear-factor counting consequence. This is a concrete adequate competitor even though it is bicriteria with respect to the requested edge budget.

When `M=O(n)`, this published runtime is guaranteed subexponential, for example, for `r=o(sqrt(n/log n))`. It does not give the proposed guarantee for every `r=o(n)`. Applying Kogan directly to a corrupted `B` does not close that gap: a sparse matching already has linear free-diagonal minimum rank, so a sparse residual need not preserve a small value of `R(B)`.

### Revised defensible comparison

The scientifically useful acquisition claim is the **unknown sparse off-diagonal perturbation together with unknown low rank and arbitrary diagonal**, while deleting a sublinear set of coordinates and retaining only a near-linear number of residual local factors. Free-diagonal completion without sparse errors is already solved strongly enough. The field-specific and rank-width distinctions in Sections 3–5 continue to apply: diagonal entries do not change any cross-cut matrix, so the linear-rank-width example is unchanged. The inspected primary results do not supply the proposed retained-core guarantee throughout `r=o(n), M=O(n)`, but this focused audit is not a first-priority claim.
