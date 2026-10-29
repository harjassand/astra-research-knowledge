# Uniform check soundness of the alternating replacement codes

## 1. Claim and exact imports

Work over F2. Let `C_k = (C_k^0 --d_k^0--> C_k^1 --d_k^1--> C_k^2)` be the alternating RX/RZ family of Balasubramanian–Davydova–Lin, **arXiv:2605.10943v1**, sections 3.2.2–3.2.6, starting with a constant planar surface-code seed. Use a fixed odd subdivision parameter `ell >= 3`, `t=(ell-1)/2`, and the natural cancellation squares. Every nonzero X/Z check overlap in this seed has size two. This property is preserved by the replacements below.

The source-proved inputs used here are:

* The total-complex definition, the cellular stars `Y_x,Y_q,Y_z`, and restriction connecting maps in equations (59)–(73).
* `Y_x` is connected and `H^1(Y_x;F2)=0`; `Y_q` is connected. These are the local cellular facts in the proof of Lemma 3.8, equations (76)–(80). They are hypotheses about the published replacement class, not consequences inferred from a passing finite computation.
* RZ is the dual replacement of section 3.2.5; reversing cochain degree exchanges X and Z and transposes the RX maps.
* Uniform Tanner vertex degree `D=7` and edge/face incidence `E=4` (Lemma 3.14), fixed `ell` independent of level, exponential size in level, and existence of a bounded-density, finite-range R3 embedding (Theorem 1.2 and section 3.2.7).

The contribution proved here is an explicit degree-one local retraction with two disjoint coordinate projections, its transpose, and the resulting **uniform polynomial check-soundness**. We then apply an established stability theorem. We do **not** equate this with perturbed finite-temperature storage, efficient initialization, physical interactions, or a practical error threshold.

Write `S_X(C)=im d^0` and `S_Z(C)=im (d^1)^T`. Let `f_k^X(M)` be the largest, over X stabilizers of weight at most M, of the minimum number of supplied X generators whose product is that stabilizer; define `f_k^Z` similarly. Set `f(0)=0`.

There are finite constants A,K,p, depending on ell and the degree bounds but **not on k**, such that

`f_{2k}^X(M), f_{2k}^Z(M) <= K M^p` for every integer `M>=1`.

Consequently the complete CSS stabilizer group has check-soundness function `2 K M^p`, uniformly in k, with no small-weight cutoff required for this combinatorial statement.

## 2. The RX bases and the repetition inclusion F

Use the source's shifted cellular bases. Fine degree zero consists of vertices of the disjoint `Y_x`. Fine degree one consists of:

1. edges of the disjoint `Y_x`, called X-edge qubits;
2. vertices of the disjoint `Y_q`, called Q-vertex qubits.

Fine degree two consists of faces of `Y_x`, edges of `Y_q`, and the two points of each `Y_z`. There are no identifications between these direct-sum vector spaces. Restriction maps connect them.

Define F by:

* `F^0 alpha` is the constant value `alpha_x` on all vertices of each `Y_x`;
* `F^1 c` is zero on X-edge qubits and the constant value `c_q` on all vertices of each `Y_q`;
* `F^2 b` is zero on the face/edge degree-two summands and equals `b_z` on both points of `Y_z`.

Cellular boundaries of constants vanish, and restriction preserves constants. Therefore

`d_f^0 F^0 = F^1 d_o^0`, `d_f^1 F^1 = F^2 d_o^1`.

This is the simple cochain inclusion already implicit in the source's diagonal duplication. Its transpose `(F^1)^T` is a coarse Z projection. Each fine coordinate contributes to at most one coarse q, so

`wt((F^1)^T z) <= wt(z)`.

This is a statement about the linear maps, without a stochastic or physical oracle.

## 3. Two disjoint projections p_b

For `b=0,1`, let `x_b` and `q_b` denote the old x and q vertices in layer b. The original x–q edge is subdivided into a ray of t edges in that layer. For a fine degree-one vector e, set

`p_b^1(e)_q = e_Q(q_b) + sum_{x adjacent q} sum_{edge in ray(x_b,q_b)} e_X(edge)`.

Let `p_b^0` evaluate a fine degree-zero vector at `x_b`.

Every Q-vertex selected here is used only for its own q. Every selected X-edge belongs to one old x–q ray and is used only for that q. Distinct rays share at most their root vertex, not any degree-one coordinate. The two layers have disjoint degree-one coordinates. Thus, on **every** vector e,

`wt(p_0^1 e) + wt(p_1^1 e) <= wt(e)`.

In particular one layer satisfies `wt(p_b^1 e) <= floor(wt(e)/2)`. The layer may depend on e; this is an explicit two-candidate calculation, not a uniform choice claimed in advance.

Telescoping each ray gives

`p_b^1 d_f^0 = d_o^0 p_b^0` and `p_b^1 F^1 = I`.

To give the remaining cochain map explicitly, the row of `p_b^2` for an old z is the sum of:

* the fine Z point `(z,b)`;
* all Q-edge degree-two checks on each layer-b subdivided q–z ray, for q adjacent to z;
* all layer-b X faces in the subdivided old squares incident to z.

For each old x,z pair with nonempty overlap, the unique natural square has its two shared q vertices. The boundary of its subdivided square is exactly the two x–q rays and the two q–z rays. Summing these boundaries proves

`p_b^2 d_f^1 = d_o^1 p_b^1`, `p_b^2 F^2 = I`.

The size-two overlap property is invariant: in RX, a fine X vertex and a fine X-face check share the two incident edges of that face; with a Q-edge check they share the restriction edge and its endpoint Q vertex; with a Z-point check their overlap is inherited from the old x,z pair. No other check pair overlaps. RZ is dual. Thus this face-based p2 formula applies at every level of the surface-seed family, rather than assuming an arbitrary Tanner-face pairing has the required parity.

## 4. A bounded local degree-one homotopy

For each x choose a spanning tree of `Y_x`, rooted at `x_b`, that contains all the prescribed layer-b x–q rays. Their union is a subdivided star and can be extended to a tree. Define `h_b^1 e` at a vertex to be the sum of e_X along its tree path from the root.

For a closed cochain e, the local X-face syndrome vanishes. Since `H^1(Y_x)=0`, integration gives `e_X=d_X h_b^1 e` throughout each block. Removing this coboundary leaves a Q-vertex field constant on each connected `Y_q`. Its value is precisely `p_b^1 e`. This proves the cocycle identity

`e = F^1 p_b^1 e + d_f^0 h_b^1 e` when `d_f^1 e=0`.

We need the full homotopy, because its transpose will supply the opposite CSS sector. It can be built locally as follows.

For an arbitrary e let `a=h_b^1 e` and `R_X=e_X+d_X a`. For an X edge, the corresponding row of R_X is its fundamental tree cycle. `H_1(Y_x;F2)=0`, so fill that cycle with faces of the **same** `Y_x`. This defines a face-check linear factorization of each row of R_X; no global solving is involved.

Next set `e'_Q=e_Q+g^0 a`. The commuting-square identity gives

`d_Q e'_Q = (d_f^1 e)_Q + g^1 R_X`.

For a vertex v in `Y_q`, integrate this equality along any graph path from `q_b` to v. The difference `e'_Q(v)+e'_Q(q_b)` is a sum of Q-edge syndrome coordinates plus the already filled X-edge residuals from the at most D adjacent X blocks. This constructs a linear `h_b^2` with

`I - F^1 p_b^1 = d_f^0 h_b^1 + h_b^2 d_f^1`.

All signs are plus in F2. Each row of h2 uses only Q-edge checks of one q block and X-face checks of its neighboring x blocks. Taking transposes gives

`I - (p_b^1)^T (F^1)^T = (h_b^1)^T (d_f^0)^T + (d_f^1)^T (h_b^2)^T`.

In particular, for a Z cycle z,

`z = (p_b^1)^T (F^1)^T z + (d_f^1)^T (h_b^2)^T z`.

This proof uses only explicitly bounded local cell complexes. It does not assume a local homotopy of the entire recursively grown code, an inverse geometric embedding, or a finite-dimensional global state.

## 5. Uniform literal costs

There are at most `F_*=D E=28` old squares in an x or z star; this deliberately weakens the bound obtainable by counting both incident edges. Counting cells in the doubled, subdivided stars gives:

`V_* = 2 F_* (t+1)^2` vertices in any `Y_x`;

`F_x* = 2 F_* t(t+1)` faces in any `Y_x`;

`E_q* = D(2t+1)` edges in any `Y_q`.

An F0 column and an h1 column have at most V_* entries. A p2 row has at most `1+D t+F_* t^2` entries. An h2 row has at most `E_q*+D F_x*` entries: repeated face terms cancel in F2, so this counts the whole permitted local pool, not an unjustified bound on accumulated path multiplicity.

Use the single explicit constant

`A=max{V_*, 1+D t+F_* t^2, E_q*+D F_x*, 1}`.

Every local correction and lifted old check in the preceding construction therefore costs at most A fine generators per input coordinate/check. These bounds are independent of replacement depth. The finite consumer checks the full maps at ell=3; there A=805. That number does **not** replace the much larger ell required by the primary random embedding. The all-level argument uses the formula for the source's fixed ell.

## 6. Check-soundness transport

If e is an X stabilizer then `p_b^1 e` is an old X stabilizer by the first cochain identity. Choose the layer with weight at most `floor(M/2)`, fill the old stabilizer, lift with F0, and add h1 e. Thus an RX step satisfies

`f_X,new(M) <= A M + A f_X,old(floor(M/2))`.

If z is a Z stabilizer, `(F^1)^T z` is an old Z stabilizer by the transposed F cochain identity. Fill it, lift its generator coefficients with `(p_b^2)^T`, and add `(h_b^2)^T z`. Hence

`f_Z,new(M) <= A M + A f_Z,old(M)`.

RZ exchanges X and Z. For `g_k=max(f_X,2k,f_Z,2k)` a paired step consequently obeys

`g_k(M) <= A(1+A) M + A^2 g_(k-1)(floor(M/2))`.

For the constant seed let m0 bound the number of checks needed for any seed stabilizer (m0=4 is safe for the supplied seed). Choose

`p=ceil(log_2(2 A^2))`, `K=max{m0, 2 A(1+A)}`.

Since `A^2/2^p <= 1/2`, induction proves `g_k(M)<=K M^p` for every k and positive integer M: the recurrence's first term is at most `K M^p/2`, and the second at most `K M^p/2`. The zero word has the empty representation. Odd levels also have a polynomial bound, but only the even family is needed here.

A Pauli stabilizer with both X and Z parts has each part of weight at most its own full support size. Applying the two sector bounds gives the complete function `f(M)=2 K M^p`.

Binary words suffice for these support bounds: pure X and pure Z generators have fixed positive phases, and the valid CSS stabilizer group contains no minus identity. Two generator products with the same binary Pauli vector therefore have the same group phase. No independent arbitrary phase choice is inserted by the filling algorithm.

The argument is also an executable filling algorithm. It compares two explicit projected weights, recurses on the selected coarse word, and lifts/adds the saved local corrections. The halving is an acquired map identity, not an assumed energy-barrier or mixing property.

## 7. Distance and the precise stability consequence

The identities `p_b F=I` and `I-Fp_b=d h+h d` make F and each p_b inverse on first cohomology; their transposes give the analogous homology statement. For a nontrivial X logical word both p0 and p1 remain nontrivial, so the disjoint inequality gives `d_X,RX>=2 d_X,old`. The Z projection F^T is nonexpanding and preserves the nontrivial class, giving `d_Z,RX>=d_Z,old`. Dualizing and pairing proves

`d_(2k) >= 2^k d_seed`.

The source's constant-factor size growth then gives a distance which eventually exceeds any fixed multiple of log n.

The second ordinary input is **Yin–Lucas, arXiv:2411.01002v2 / PRX Quantum 6, 030329 (2025)**. Its Appendix B Lemma 24 permits any fixed polynomial check-soundness function when interaction-graph shells grow polynomially; its formal stability theorem is in Appendix C. We use this theorem, not a new general stability argument.

The physical embedding hypothesis is paid as follows. If graph edges join qubits that share a Hamiltonian check, their Euclidean length is at most a fixed R_c. A graph-distance-r ball lies in a Euclidean ball of radius r R_c. The primary bounded-density embedding therefore gives at most `c(1+r)^3` qubits. The shell bound can safely be taken as `gamma(r)<=c'(1+r)^3`, corresponding to a dimension parameter **4** in the ordinary lemma. We do not require an inverse-Lipschitz embedding or silently use a Euclidean shell-area bound for an arbitrary graph shell.

Thus, for every fixed primary-qualified ell and its bounded-density embedding, the unperturbed commuting-projector family has a positive, size-independent perturbation threshold in the **exact weighted local norm** of the Yin–Lucas theorem. Beyond a size-independent onset, sufficiently small perturbations in that norm leave a ground doublet separated from the rest of the spectrum by a constant gap, with exponentially-in-distance small doublet splitting and the theorem's quasi-local dressing conclusion.

A fixed-range, bounded-incidence physical perturbation can be put into that norm with a fixed constant loss: enlarge its support by the checks it touches and decompose into the finitely many local check syndromes. The enlarged support, number of pieces and exponential support weight are bounded independently of n. The numerical native threshold, however, is **not** acquired by this argument; the constants may be extremely poor at the primary's large ell.

This closes a **zero-temperature spectral-stability** gate using check soundness. It does not establish the strict spatial TQO-2 condition as phrased in the original paper, does not justify a perturbed Davies generator, and does not prove a finite-temperature perturbed memory lifetime.

## 8. What the finite consumer establishes

`compile_complex.py` independently constructs the finite total complexes from the primary definitions; it imports no source scientific code. `check_retraction.py` constructs F, both p's, h1 and a local h2, and checks all cochain, retraction and degree-one homotopy matrix identities over F2 on **all vectors**, by matrix equality. It checks coordinate disjointness and the literal generator-cost bounds. The finite ranks and local-neighborhood queries are exploratory antecedents, not the all-level theorem's premise.

The all-level claims above rest on the symbolic telescope/local-face-fill proof and the explicit uniform cell counts. The public source's geometry, thermal-lifetime theorem and the ordinary gap-stability theorem remain separately named imports. No finite rank experiment certifies those imports or a physical device.
