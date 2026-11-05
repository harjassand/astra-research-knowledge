# Independent audit of the BDL physical-coordinate matroid obstruction

## Conclusion

The algebraic and combinatorial bridge in `sampler_route/sampler_obstruction.md` passes this independent audit. At fixed allowed odd refinement parameter \(\ell\ge5\), the physical Z-check matroid at all sufficiently large even BDL construction depths has a direct-sum minor of \(\Omega(N)\) copies of \(F_7^*\). Consequently the rank defect to every regular quotient or regular lift on the physical coordinates is \(\Omega(N)\). This excludes the quoted near-graphic/near-cographic sufficient conditions with logarithmic defect and exact regular-matroid sampling. It is not a claim that every implementation of CSW is slow, nor a Gibbs-sampling lower bound.

The audit uses the exact local RX/RZ definitions of [BDL 2605.10943v1, Sections 3.2.2 and 3.2.5](https://arxiv.org/html/2605.10943v1). It does not substitute the informal tensor-product construction. A complete local copy of the primary text is `bdl_2605_10943v1_full.txt`.

## 1. The Lawrence identity is exact, including redundant old checks

Let \(A\in\mathbb F_2^{n\times m}\) have the old physical Z checks as columns. Define

\[
L(A)=\begin{pmatrix}A&0&I_n\\0&A&I_n\end{pmatrix}.
\]

Its kernel is exactly

\[
\ker L(A)=\{(u,u+r,Au):u\in\mathbb F_2^m,\ r\in\ker A\}.
\]

Using a basis for \(\ker A\), a dual representation restricted to upper-check and bridge columns is \([I_m\mid A^T]\), with extra zero rows. Hence contracting the lower-check columns of \(L(A)\) gives the dual of that augmented matroid. The lower-check columns need not be independent. Their contraction rank is \(\operatorname{rank}A\), as required by the dimensions.

The physical RX contraction that produces \(L(A)\) is also valid. Contracting all x-local face columns passes from each edge space to its quotient by local face boundaries. BDL's \(H_1(Y_x)=0\) identifies that quotient with the image of edge-to-vertex boundary. The inclusion maps commute with boundary. Therefore its extra x-vertex rows equal the inclusion of q-vertex rows. The terminal old-Z point columns also satisfy this equality because old CSS commutation makes their x-side image vanish. Removing these redundant rows leaves the disjoint \(Y_q\) graph incidences and the terminal point columns. Contract the two star arms to two vertices per old qubit and retain one bridge: this is precisely \(L(A)\). All these are physical Z-check elements.

## 2. Arbitrary subdivision, verified independently of the diagnostic generator

The new script `audit_matroid_subdivision.py` constructs the local two-square gadget without importing `bdl_matrices.py`. For each old x-square, it uses two \(s\times s\) grids, \(s=(\ell-1)/2\), and the two boundary-cylinder strips. Its q-blocks are the two subdivided arms with one terminal bridge. The resulting augmented matrix has

\[
r_s=4s^2+10s+5
\]

check rows and \(8s^2+18s+8\) physical-qubit columns, plus \(r_s\) identity columns.

Define the row projection \(Q_s\) by merging all subface rows of one original layer face, all subfaces of one original side strip, and all subedge rows of one original q-arm. The projection has rank 19. Its kernel is spanned by actual qubit columns:

* A dual spanning tree within each layer grid supplies differences of neighboring subface coordinates.
* Internal vertical edges within each side strip supply the analogous differences. They do not belong to \(Y_q\), so no additional q-check entry appears.
* Internal q-arm vertices supply differences of neighboring q-edge coordinates. They are not old-Z leaves, so no terminal point entry appears.

The supports of these trees lie in separate row groups. Their union is independent of rank \(r_s-19\), exactly \(\ker Q_s\). Contract them. Keep one identity column per group, one appropriate boundary-edge qubit per coarse edge, the endpoint bridge qubits, and the q-root/leaf qubits. The projected columns are **exactly** the 53-column \(\ell=3\) augmented matrix. Thus the finite Fano projection pulls back for every integer \(s\ge1\).

The independent script verifies this identity and the final quotient ranks for \(\ell=3,5,7,9\). The check-row counts are 19, 41, 71, 109, and the final contraction ranks are 16, 38, 68, 106. In all four cases the retained seven columns are exactly the vectors 1 through 7 of \(\mathbb F_2^3\). `matroid_subdivision_audit.json` records the results. The proof above, rather than finite testing, supplies the all-\(\ell\) statement.

## 3. Local extraction and the intervening dual step

For the two-square strip \((x_0,q_0,z,q_1)\), \((x_1,q_1,z,q_2)\), its chosen cells form a closed subcomplex inside the corresponding blocks of the full RX construction. In the augmented matrix, contracting identity columns outside those check cells projects away all other rows. Deleting physical-qubit columns outside the selected cells leaves precisely the strip matrix, even if the full old Tanner complex has extra incidences between some of the selected old vertices: those incidences use unselected faces or branch-cell labels.

For vertex-disjoint strips, there are no remaining cross-block entries. A retained x-edge qubit couples only to x-face cells of its own old x and q-edge cells bearing its selected q/edge label. A retained q-vertex qubit couples only to its q-edge cells and matching old-Z point label. Distinct selected old vertices therefore yield a literal direct sum. This is stronger than merely having disjoint Fano witnesses without controlling their spans.

For RZ, contracting physical qubit columns on a spanning tree of each connected \(Y_z\) identifies all new check-row coordinates in that block. Retaining one identity per block and one q-root vertex per old qubit produces \([I\mid h_Z]\). Hence augmented minors survive the intervening RZ step. At the physical-check level, the internal edge rows force a dependence coefficient to be constant throughout each \(Y_z\) vertex block; the q-root equations are exactly the old dependence equations. Thus RZ is a series extension of the old physical Z-check matroid and preserves its minors.

These observations validate the four-step pipeline from a packed strip family to a physical direct-sum \(F_7^*\) minor.

## 4. The packing is extensive in the actual family

The purity count can be made explicit. The base has every physical qubit adjacent to at least one X and one Z check. RX preserves this: every x-local edge has its two X endpoints and lies in a local face; every q-local vertex lies on a local q-edge and receives X incidence from an old X neighbor. The dual argument applies to RZ. By CSS commutation and the prescribed Tanner pairing, every pair of an X and a Z incidence at a qubit belongs to a Tanner square. Therefore

\[
2|T(2)|=\sum_q\deg_X(q)\deg_Z(q).
\]

Both degrees are at least one and uniformly bounded at fixed \(\ell\), so \(|T(2)|=\Theta(N)\).

Every old Tanner square contributes a distinct subdivided layer-square in the next RZ \(Y_z\) block. For \(s\ge2\), choose one internal edge of this patch and an endpoint at which its two adjacent faces have distinct other incident edges. The vertex is a physical Z check, the faces are two physical X checks, and the three edges are the qubits of the two-square strip. Bounded Tanner degree bounds the overlap graph of these constant-size candidate neighborhoods. Greedy selection retains a constant fraction. Fixed-\(\ell\) size growth then gives \(\Omega(N)\) vertex-disjoint strips at the required preceding even level, and \(\Omega(N)\) physical \(F_7^*\) summands four steps later.

The same density argument validates the bounded-weight relation packing used in `central_quotient_and_recent_decoding.md`: internal-edge qubits of the preceding RZ layer grids have exactly their two endpoint Z checks, and disjoint old radius-two neighborhoods give disjoint RX local relations. The final RZ repeats relation coordinates through its series classes.

## 5. Independent proof of the rank-defect lower bound

Suppose \(M\) has a direct-sum minor \(N_1\oplus\cdots\oplus N_L\), every \(N_j\) nonregular. Let \(R\) be a regular quotient of \(M\), with rank defect \(\Delta\). Use a linear quotient \(\phi:V\to W\) on their column representations. Common deletion and contraction induce a quotient on the minor with kernel dimension at most \(\Delta\): after contracting a column span \(U\), its kernel is \((\ker\phi+U)/U\); restriction can only reduce its dimension.

Now the source minor span splits as \(V=\bigoplus_jV_j\). If \(\ker\phi\cap V_j=0\), the quotient is injective on that summand and the corresponding restriction of the regular minor remains \(N_j\), impossible. Every intersection therefore has dimension at least one. They lie in direct-sum subspaces, so

\[
\Delta\ge\dim\ker\phi\ge\sum_j\dim(\ker\phi\cap V_j)\ge L.
\]

For a regular **lift**, dualize: duality reverses lift/quotient and preserves regularity and rank defect. The dual of the direct-sum minor is a direct sum of the nonregular \(N_j^*\), so the same bound applies.

Equivalently, the cycle-space proof in the sampler note is valid: if \(C\subseteq D\) and \(D\) is regular, each \(D\cap\mathbb F_2^{E_j}\) must strictly extend \(C_j\). The resulting block-supported vectors are independent modulo \(C\), giving codimension at least \(L\). This explains why one global extra constraint cannot repair a direct sum of independent nonregular obstructions.

## Limits of the conclusion

This audit establishes the sufficient-condition boundary for the actual physical matroids. It does not rule out a different nonregular-matroid algorithm, a different dynamically tailored CSW proof, or the accepted history-polymer sampler. The latter already constructs the required cold syndrome law. The new obstruction makes that comparison substantive without changing BDL's Hamiltonian, bath, random embedding, paid writing/reading, or one-time initialization-error convention.
