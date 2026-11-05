# BDL physical-check matroids: an extensive Fano obstruction

**Constructive comparator result, 5 November 2026.** This note leaves the accepted P1 full-syndrome history compiler, weighted extension, and unknown-input loading theorem at their earned scopes. It addresses the previously unresolved strongest-sampler gate using the *actual* random-embedding BDL replacement, including its subdivision parameter.

## 1. Result and consequence

Let `M_Z(i)` be the binary matroid whose elements are the physical Z checks of the BDL level-i code, represented by the columns of `H_Z(i)^T`. Its dual is represented by any full-row-rank generator of the physical check-dependency code `ker H_Z(i)^T`.

**Theorem.** For the main BDL alternating RX/RZ family, with any fixed allowed odd subdivision parameter ell>=3:

1. After RX–RZ–RX, `M_Z(3)^*` has an F7 minor, and `M_Z(3)` has an F7* minor. This uses a five-vertex wheel at a corner of the actual local complexes. It holds for arbitrary subdivision sizes in those three steps, not only for the computational probe ell=3.
2. At every sufficiently large even level L (indeed L>=6), there is a minor of `M_Z(L)^*` equal to a direct sum of `r_L = Omega_ell(N_L)` copies of F7. Dually `M_Z(L)` has a direct sum of r_L copies of F7* as a minor.
3. Consequently both the minimum graphic defect and the minimum cographic defect in Code Swendsen–Wang Definition 10 are at least r_L. Neither is O(log N_L). The physical Z-check matroid is nonregular.

This closes two previously open black-box comparator routes for this family:

- The regular-matroid positive Ising FPRAS cannot be invoked on the actual check matroid.
- The logarithmic-defect graphic/cographic sufficient condition for polynomial CSW mixing cannot be invoked in either orientation.

**It does not prove slow CSW mixing, hard Gibbs sampling, or necessity of our particular compiler.** A direct CSW mixing proof, another sampler, or a different efficiently samplable representation remains possible. The new result identifies a real structural obstruction rather than inferring one from metacheck weight, one logical qubit, or recursive construction.

The constants below depend on ell, which is extremely large in the published embedding proof. The statement is asymptotic at that fixed physical construction parameter; it does not claim practical runtime separation at modest N.

## 2. Primary governing definitions

BDL = Balasubramanian, Davydova, Lin, *A passive self-correcting quantum memory in three dimensions*, arXiv:2605.10943v1, 11 May 2026.

- https://arxiv.org/html/2605.10943v1
- §3.2.2, equations (60)–(72): local cellular complexes and restriction maps.
- §3.2.5, equations (94)–(96): the transposed RZ construction.
- Lemma 3.14: Tanner vertex degree at most 7 and edge-face degree at most 4.
- Equation (109): the alternating main family.

Write m=(ell-1)/2. RX subdivides each old square into m by m squares, doubles the local star at each X check, and joins the two boundary copies by a cylinder. The qubit-local complex is the doubled subdivided q–Z star; the Z-local complex is two points. The connecting maps are cellular restriction. The spatial perturbation changes the embedding, not these matrices.

CSW = Hangleiter, Ju, Vazirani, *Code Swendsen–Wang Dynamics*, arXiv:2510.08446v4, 5 October 2026.

- https://arxiv.org/html/2510.08446v4
- Definition 10 and Theorem 16 / Corollary 17 govern the sufficient criterion.

For h with physical checks as rows, Delta-graphic means `ker h^T` lies inside a graph cycle space with codimension at most Delta. Delta-cographic applies this condition to the dual check matroid. The published mixing bound is polynomial times `2^{O(Delta)}`. Physical check coordinates are retained throughout this note.

Goldberg–Jerrum, *A polynomial-time algorithm for estimating the partition function of the ferromagnetic Ising model on a regular matroid*, SICOMP 42 (2013), arXiv:1010.6231v2:

- https://arxiv.org/html/1010.6231v2

Their positive weighted q=2 FPRAS applies to regular matroids. The accepted prior comparison gives its deletion/contraction sampling reduction and then unknown-input syndrome loading. The obstruction here concerns its structural hypothesis, not that reduction.

## 3. Exact RX dependency coordinates

This section is the main algebraic bridge. It keeps physical check coordinates rather than replacing them by a homological basis in the Hamiltonian.

The BDL Tanner complexes have the following property: an X/Z pair shares either zero or two qubits, with one corresponding Tanner square in the latter case. The seed has it. It is preserved by RX: a new Z check is either a local face, a qubit-local edge, or an old-Z point. Its overlap with a new local X vertex is respectively the two incident face edges; one local edge and one qubit-local vertex; or the old X/Z pair's two qubits. RZ is the transpose. Subdivision preserves these cases.

For an old X check x define its **link graph** L_x:

- vertices are old qubits q adjacent to x;
- each Tanner square `(x,q,z,r)` gives one edge q–r, labelled by z.

Let D=ker H_Z(old)^T, the old physical Z-check-dependency space. All the following variables are independent:

- `d in D`;
- one free bit `s_z` for every old Z check;
- an even vector `(a_qz : z~q)` for every old qubit q, so `sum_{z~q} a_qz=0`;
- a cycle `F_x` in the binary cycle space of L_x, independently for each x. Its value on the square f is `F_xf`.

Every new Z-check dependency, and only such a dependency, has the following coordinates. When m>1, the stated value is repeated on all subcells of that coarse cell.

| Physical new Z-check coordinate | Dependency value |
|---|---|
| old-z point, copy 0 | `s_z` |
| old-z point, copy 1 | `s_z+d_z` |
| q–z horizontal branch, copy 0 | `a_qz` |
| q–z horizontal branch, copy 1 | `a_qz+d_z` |
| vertical q-local edge at z | `a_qz+s_z` |
| x-local face f, copy 0 | `F_xf` |
| x-local face f, copy 1 | `F_xf+d_z` |
| x-local cylinder face on boundary q–z of f | `F_xf+a_qz` |

All additions are in F2.

### Proof of completeness

The relation equation is the zero-sum condition at each physical qubit. First consider a q-local doubled star. Write the values on its two horizontal branches as a0_qz,a1_qz and on its vertical z edge as b_qz. The endpoint equations give

`a0_qz + b_qz + z0 = 0`,

`a1_qz + b_qz + z1 = 0`.

Put s_z=z0, d_z=z0+z1, and a_qz=a0_qz. Then b_qz=a_qz+s_z and a1_qz=a_qz+d_z. The two centre equations give even parity for a_q and `sum_{z~q}d_z=0`. The latter is exactly d in D.

For an x-local doubled star, let F_xf be the copy-0 face value. The two equations along a boundary q–z edge force the cylinder value to be F_xf+a_qz and the copy-1 face value to be F_xf+d_z. Equations on x–q edges say that F_x is a cycle of L_x. The remaining vertical-edge equations follow from the same two parity identities. Conversely, substitution verifies every qubit equation.

At m>1, an interior edge of a subdivided x face has exactly two incident face checks and no external restriction term, so their relation coefficients agree. This propagates over the connected m by m grid. An interior vertex of a subdivided q branch likewise forces equality along the branch. Cylinder faces and restriction incidences match these subdivisions. Therefore the same coordinate table is exhaustive, with repeated coefficients. No unproved change of Hamiltonian check basis is being used.

The implementation `rx_relations.py` independently generates this table and verifies that its rows are relations of the literal cellular matrix and have the full nullity. On the third minimal-subdivision replacement the independent parameter counts are d=3, s=588, a=1432, F=968, totalling 2991.

## 4. Series extension and minors, with explicit physical access to the parameters

### The unchanged sector is a series extension

For RX, an X-check relation restricts to a zero coboundary on every connected Y_x. It is therefore constant, b_x, on that local vertex set. The qubit-local restriction equation is `sum_{x~q} b_x=0`. Hence

`ker H_X(new)^T = repeat(ker H_X(old)^T)`.

Thus the dual check-matroid representation repeats each old column. It is a parallel extension on the dual side, equivalently a series extension of the physical check matroid. The RZ/Z statement follows by transposition. This holds at every subdivision size.

### The other sector contains the old matroid as a minor

In the RX relation table, actual physical columns supply generators of the independent s, a and F parameter spaces:

- copy-0 terminal columns supply each s_z;
- copy-0 q-branch columns span each even-star a_q parameter space;
- copy-0 x-face columns span each cycle-coordinate F_x parameter space.

Contract bases of these spaces in the dual matroid. The remaining copy-1 terminal columns are exactly d_z, representing the old dual check matroid. Delete all other columns. This proves `M_Z(old)^*` is a minor of `M_Z(new)^*`; by duality the same holds for the primal matroids. Together with the unchanged-sector series extension, both old physical-check matroids survive as minors through every replacement.

This argument also justifies all later parameter elimination: we always contract spans generated by actual check columns. We never arbitrarily project away a direction and silently call it a matroid minor.

## 5. A wheel supplied by an actual BDL corner

Take any old Tanner square `(x,q,z,r)`. At RX output consider the copy-0 x-local vertex at the old corner z. Call it u. The link graph at u is the wheel with five vertices A,B,C,D,E and edges

`AB, AC, BC, AD, BE, CD, CE, DE`.

The five qubits are:

- A,B: the two copy-0 x-local boundary edges ending at z;
- C: the x-local vertical edge at z;
- D,E: the q-local and r-local copy-0 vertices at z.

For m>1, A and B are the last small boundary edges, and AB is the corner small face. The incidence list is unchanged.

The eight neighboring Z checks and their dependency values are:

| Link edge | Actual check type | Value in RX dependency coordinates |
|---|---|---|
| AB | x-local copy-0 corner face | F |
| AC | x-local q–z cylinder face | F+a_qz |
| BC | x-local r–z cylinder face | F+a_rz |
| AD | q-local copy-0 horizontal edge | a_qz |
| BE | r-local copy-0 horizontal edge | a_rz |
| CD | q-local vertical edge at z | a_qz+s_z |
| CE | r-local vertical edge at z | a_rz+s_z |
| DE | copy-0 terminal z point | s_z |

The next RZ step has a terminal X check v corresponding to u, copy 0. Its link is exactly the same wheel: the connecting squares at a terminal corner reproduce the old link. By the series-extension result, the dependency value on each neighboring new Z check is the same as on its old Z check.

Assume q has at least two Z neighbours. We can retain one a_q mode w whose coordinate is w at z and at one other chosen neighbour z', and zero elsewhere. Algebraically, contract the q-branch columns for all neighbours outside `{z,z'}`. The remaining even-parity relation makes the two uncontracted values equal. Retain s_z=u, kill a_r and F, and remove other parameters as described next. The eight inherited wheel values become

`d_AB=0, d_AC=w, d_BC=0, d_AD=w, d_BE=0, d_CD=w+u, d_CE=u, d_DE=u`.

These are **local independent variables produced by RX**, not a pair of global inherited dependencies. This is the feature that permits extensive packing.

## 6. The third replacement produces F7, explicitly

Apply RX once more. In the new dependency representation, the wheel at v supplies an independent cycle F' on the wheel. Contract the final-step s and a spaces; contract the F' spaces at unselected X checks. Actual columns now include:

- all inherited d_z columns, from copy-1 terminal checks;
- for each wheel edge e, both F'_e and F'_e+d_e, from the two copies of its x-local face.

Parametrize the wheel cycle by

`x=F'_AB, y=F'_AC, zeta=F'_BC, t=F'_DE`.

The vertex parity equations give

`F'_AD=x+y`, `F'_BE=x+zeta`,

`F'_CD=x+y+t`, `F'_CE=x+zeta+t`.

Contract the three actual columns

`u+w`, `F'_AC=y`, `F'_BC=zeta`.

The first is available as an inherited CD check column. In the quotient, u=w, y=zeta=0. Retain these seven actual columns:

| Retained column | Quotient value |
|---|---|
| inherited w | w |
| copy-0 AB face | x |
| copy-1 AD face | x+w |
| copy-0 CD face | x+t |
| copy-1 CE face | x+t+w |
| copy-0 DE face | t |
| copy-1 DE face | t+w |

They are precisely the seven nonzero vectors in the three-dimensional binary space spanned by x,t,w. Their matroid is F7. This is the complete local certificate.

For completeness, F7 is nonregular without needing a recognition package: choose three independent elements as a basis. The Fano lines force compatible nonzero representations of their pairwise sums and the triple sum. Over a field of characteristic not two, the line through the three pairwise sums requires one relative sign reversal, whereas the three lines through the triple sum require all three signs to agree. This is impossible. In particular F7 has no real representation. Regular matroids, and their graphic/cographic subclasses, exclude it and its dual as minors.

### Killing inherited parameters using actual columns

The coordinate eliminations above can be made in the full final dual matroid. After the final s,a spaces have been contracted, every intermediate physical dependency column d_z is available through a copy-1 terminal check. RZ repeats every preceding physical column, so these intermediate columns include copies of every first-RX column.

Within these inherited columns:

1. Contract all first-RX F spaces using first-copy face columns.
2. First-RX second-copy face columns are then old d_z. Contract a basis of the entire old dependency space. Every old Z check participates in a Tanner square, so all d_z are available.
3. Contract unwanted first-RX s_z using copy-0 terminal columns.
4. Contract all unselected a_q spaces using copy-0 q branches. For each selected q retain exactly the mode supported on `{z,z'}` by contracting the other branch columns.

The remaining inherited parameters are exactly the selected independent pairs (u,w). This establishes the global minor operation rather than only a formal substitution in the local equations.

The [[5,1,2]] seed has a square with q adjacent to two Z checks, so the first three replacements already yield one Fano minor. More generally the packing below does not depend on that particular seed labelling.

## 7. Extensive packing

Choose a collection of **vertex-disjoint** coarse Tanner squares `(x_i,q_i,z_i,r_i)` with each q_i having at least two Z neighbours. Vertex-disjointness gives distinct q_i,z_i and ensures r_i is never a selected q_j. Apply the preceding construction simultaneously.

- The first-RX s_{z_i}=u_i are independent because the z_i are distinct.
- The selected even-star modes w_i are independent because the q_i are distinct.
- Each selected first-RX corner gives a different terminal X check after RZ.
- At the third RX step, its wheel cycle space F'_i is independent of all other local F' spaces.
- The global contractions just described remove all other parameters. They leave a direct sum of these six-dimensional wheel parameter spaces.
- Contracting u_i+w_i, y_i and zeta_i independently in each space leaves a direct sum of F7 minors.

This is stronger than merely finding many overlapping Fano minors: the surviving quotient spans are independent.

### Number of qualifying squares

Consider an even coarse level j>=2, just after RZ. Split its qubits into E, the 1-cells of the local Y_z complexes, and V, the vertices of the qubit-local Y_q complexes.

Every E qubit has exactly two Z neighbours, its endpoints. It also belongs to an X check: every local edge is in a face or a restriction subcomplex. Thus it occurs in a Tanner square and qualifies as q.

Every old q has at least one old Z neighbour, and Y_q embeds as a subcomplex of Y_z at each such incidence. There are at most seven q neighbours per old z. Each Y_z is connected and has an edge, so its vertex count is at most twice its edge count. Therefore

`V <= sum_z sum_{q~z} |Y_q(0)| <= 7 sum_z |Y_z(0)| <= 14 E`.

Hence `E >= N_j/15`. Choose one incident Tanner square per E qubit. Each square contains two qubits, so at least `N_j/30` distinct qualifying squares occur. A Tanner vertex is incident to at most 14 squares, because it has at most seven edges and each edge belongs to at most four squares, with each square counted twice at that vertex. A chosen square can therefore conflict with at most 56 candidate squares at its four vertices. Greedy packing gives at least

`r >= N_j/1680`

vertex-disjoint qualifying squares (rounding can only improve this real-valued lower bound).

### Comparing the coarse and final sizes

For an explicit loose bound put m=(ell-1)/2 and `C_ell=100 m^2`. Each replacement has `N_{i+1} <= C_ell N_i`:

- There are at most 7N old Tanner squares.
- The doubled subdivided x-star edges contribute at most `12m^2` per old square, after summing over all x.
- The q-local vertices contribute at most `2N+14mN <=16m^2N`.

The same estimate holds for RZ by transposition. The estimates deliberately overcount shared edges.

For any even L>=6 choose j=L-4. Apply RX–RZ–RX, obtaining the direct sum of F7 minors in the dual Z-check matroid at level L-1, and then use the RZ series extension to preserve the minor at L. Consequently one explicit bound is

`r_L >= N_L / (1680 C_ell^4)`.

The coefficient is tiny for the embedding theorem's ell, but strictly positive and independent of L. This proves the asserted Omega_ell(N_L) obstruction for the actual fixed-ell family.

## 8. Why packing lower-bounds both CSW defects

The following elementary rank-loss lemma is useful beyond this application.

**Lemma.** Let M be represented over F2. If M has a minor equal to a direct sum of r nonregular matroids, then any linear projection of its representing space whose image matroid is regular loses at least r ranks.

**Proof.** Realize the minor by contracting a set C and deleting the unused elements. A projection P induces a map after contracting C in its domain and P(C) in its image. The induced kernel has dimension at most the original rank loss. In the contracted domain, the r minor blocks span a direct sum of subspaces W_i. If the induced map were injective on W_i, its image would contain the same nonregular restriction. This contradicts minor-closed regularity of the image matroid. Thus the kernel intersects every W_i nontrivially. Choosing one nonzero vector from each intersection gives r independent vectors. ∎

A Delta-graphic certificate for h is exactly a projection from its physical row matroid to a graphic matroid losing at most Delta ranks: the relation-space inclusion ensures the map is well-defined, and the codimension equals the rank loss. A Delta-cographic certificate is the same statement for its dual.

Apply the lemma to `M_Z(L)`, which has r_L F7* blocks as a minor, and to `M_Z(L)^*`, which has r_L F7 blocks. Both defects are at least r_L. This establishes the two orientations separately; nonregularity alone would not have done so.

## 9. What this says about direct hierarchical dynamic programming

The coordinate formula gives a useful exact factorization, but not independent blocks. In the high-temperature expansion of the code partition function, each physical check contributes its own positive factor on its relation coordinate. The cylinder checks contain `F_xf+a_qz`, the vertical checks contain `a_qz+s_z`, and the second-copy faces contain `F_xf+d_z`. These are actual interactions between local cycle, qubit-star and inherited variables. Summing over one family generates functions of its neighbours.

A homological direct sum therefore does not supply a fixed-size interface for an exact sampling recursion. The extensive minor theorem also rules out the particular claim that all this coupling can be absorbed into only O(log N) additional dimensions above a graphic or cographic sampler. It does **not** exclude bounded-width tensor algorithms without further width analysis. Nor does it show that the accepted history compiler is already the fastest method.

The honest next opening for P1 is consequently stronger than its earlier unresolved comparator status: construct the promised low-temperature sampler or a direct mixing theorem on matrices with this extensive nonregular structure. A general request to analyze the hierarchy does not itself implement that operation.

## 10. Exact computational receipts

All computations are binary and exact; none is a quantum-device simulation.

- `bdl_matroid_probe.py`: literal §3.2.2 cellular RX at m=1, dualized for RZ, including the three types of induced Tanner squares and complete check incidences.
- `rx_relations.py`: independent coordinate-table construction; proves equality computationally at level 3 by nullity and composition checks.
- `wheel_minor.py`: a 19-column, rank-six local wheel representation; finds the displayed Fano contraction without relying on CMR.
- `verify_wheel_packing.py`: finds three vertex-disjoint squares in the actual level-2 cellular complex, verifies their level-3 corner wheels and independent inherited (s,a) patterns, and verifies the final direct sum of three rank-three Fano blocks.
- `matroid_certificates/wheel_packing_verification.json`: deterministic exact receipt from that run.
- `matroid_certificates/wheel_Fano.json`: local contraction certificate.
- `bdl_subdivision_check.py`: independently constructs the subdivided cellular complexes at ell=3,5,7. It verifies the complete first-RX relation space, the actual corner-wheel incidence, and preservation of that wheel and its inherited values through RZ. The level-2 sizes are respectively 1336, 8144 and 27752 qubits. All exact checks passed; the all-ell theorem still rests on the cell-propagation proof rather than extrapolation from these cases.
- `matroid_certificates/subdivision_verification.json`: the corresponding three-subdivision receipt.

The earlier broader diagnostics are retained but not needed for the theorem:

| Level | Qubits | X checks / rank | Z checks / rank |
|---|---:|---:|---:|
| 0 | 5 | 2 / 2 | 2 / 2 |
| 1 | 60 | 24 / 24 | 38 / 35 |
| 2 | 1336 | 840 / 750 | 588 / 585 |
| 3 | 36624 | 15824 / 15734 | 23880 / 20889 |

At levels 1 and 2 both dual check representations have independently verified graph certificates. Level-3 X still does. A reduced level-3 Z representation has the fundamental submatrix

```
1 1 0 1
1 0 1 1
0 1 1 1
```

beside an identity block. Its Fano certificate first suggested the local wheel proof. This is useful evidence that the implementation detects the actual onset instead of merely testing an arbitrary parity-history toy.

CMR v1.4.0, official source commit `0c42a44deb8262a1f2a400add5d6be80e90eda3c`, was used only for discovery/diagnostics:

- https://github.com/discopt/cmr/tree/0c42a44deb8262a1f2a400add5d6be80e90eda3c
- https://discopt.github.io/cmr/binary_regular.html

Returned positive graph certificates were checked independently by exact equality of GF(2) row spaces. Failed recognition and regularity timeouts are not premises of any theorem above.

## 11. Comparison with P2 and P3 at their achieved scopes

P2 has already composed whole-campaign entropy losses and built amortized thermal waiting. Its quadratic sufficient wait is not a universal optimum, and the useful response duration can dominate preparation in slow harmonic examples. Observation-dependent selection and real reset must be accounted for before a broad intervention resource lower bound is earned. This note supplies no additional P2 lower bound.

P3 has a rigorous causal-cone catastrophe obstruction and a refined uniform finite-horizon target whose input-dependent seed radius is independent of the horizon. Its positive half needs actual finite-speed local correction and a finite readout; declared immutable schedules do not themselves correct data. A matching constructive threshold, if completed with those costs, would be a stronger foundational outcome than merely closing the sampler-comparison gate here.

P1 retains the accepted exact loading/history machinery. The new extensive Fano theorem removes two strong generic-sampling shortcuts, improving its scientific specificity. It does not produce the useful thermal loading endpoint by itself. Thus it should be preserved as completed reusable mathematics while selection turns on whichever programme actually completes its central operation.
