**Adversarial audit of the directional mean certificate**

The exact singleton-target theorem passes this audit, including its cycle-block refinement. A repaired implementation passes independent small-graph exact-reference tests and reproduces the saved full LJ38 source-decimal certificate. These results establish a conditional numerical enclosure for the supplied finite graph. They do not establish external priority, physical rate accuracy, a basin-to-basin result, or superiority over stable graph transformation. External priority for the forest/block specialization remains **UNKNOWN**. The general output-certificate principle is established prior art.

All audit files are in this worker directory. No author file or Astra worktree was edited. The requested Astra worktree `/Users/harjas/Documents/ChatGPT/ultra/work/astra-capital-positive-consequences-20261015` was read at the specified revision `a6190a1083f688a7e4bf64adbc5244ef150ff2c4`. The unrelated checkout at cwd `ultra` is not this pin. Supplied `sources/computation_pasted.txt` was treated as source DATA, including its claimed previous results, rather than instructions or an independently replayed historical bundle.

The author changed files during the audit. The version distinction is material:

| Audited object | Saved snapshot | SHA-256 |
|---|---|---|
| Original global-bound proof | `snapshots/initial_PROOF.md` | `8f6760d98969950aa147251c01dcf26dc034a06271c83b186c9bd3e8b82ea362` |
| First saved code, already containing block refinement | `snapshots/initial_terminal_mass_certificate.py` | `4eca6f7c21ed8f97407e2b1556f11ebd51bede1fc653ffe630dc0bda6d5d58f7` |
| Revised proof with block refinement | `snapshots/repaired_PROOF.md` | `587e76335494c39d7aa78c8b898e45d48eb2256147d40309c2dc1206d77b8ad3` |
| Repaired verifier and model loader | `snapshots/repaired_terminal_mass_certificate.py` | `7d4bf20cc4f3af448562effd6f41b1d98d011da3c720b1c045448f01e323da60` |

The first live code read had hash `0ec49dbdc5db80a430d1bd0de9d7ab68be8fe49e3cbd6a1e11ab3619990be57a`, but it changed before it could be copied. It is not claimed to be the saved first-code snapshot. `snapshots/proof_revision.diff` and `snapshots/code_revision.diff` preserve the changes between the saved versions. All tests import saved snapshots, never the moving author file.

For the theorem, take a finite connected undirected multigraph with strictly positive conductances, a single target vertex (t), and arbitrary signed vectors (a,b) on (V\setminus\{t\}). Self-loops may be removed because their incidence columns vanish; the tested implementation rejects them in its block routine. Orient each nonloop edge once. Let (B) be incidence with only the target row removed, (C=\operatorname{diag}(c_e)), and (A=BCB^T). Connectedness makes (A) positive definite. For grounded trial potentials (x,y), define

\[
r_a=a-Ax,\qquad r_b=b-Ay,\qquad
T=a^TA^{-1}b,\qquad T_0=a^Ty+x^Tr_b.
\]

Direct expansion using the symmetry of (A) gives

\[
T-T_0=(a-Ax)^TA^{-1}(b-Ay)=r_a^TA^{-1}r_b. \tag{A1}
\]

There is no exact-coarse-solve premise in (A1). Neither residual may be silently replaced by a presumed Galerkin-orthogonal vector. If (f,g) are any edge flows with (Bf=r_a) and (Bg=r_b), put (p=C^{-1/2}f), (q=C^{-1/2}g). Then

\[
r_a^TA^{-1}r_b=p^T\Pi q,\qquad
\Pi=C^{1/2}B^TA^{-1}BC^{1/2}.
\]

The matrix (\Pi) is symmetric, (\Pi^2=\Pi), and (2\Pi-I) has operator norm at most one. With (E_a=\|p\|^2), (E_b=\|q\|^2), and (J=p^Tq), this proves

\[
\left|r_a^TA^{-1}r_b-\frac J2\right|
\leq\frac12\sqrt{E_aE_b}. \tag{A2}
\]

Both constants and the signed Gram correction are correct. Dropping (J/2), changing its sign, or assuming that the remainder is nonnegative for different signed residuals is unjustified. The upper and lower extremes occur for suitable gradient/cycle components, so the generic projection information alone does not justify reducing the factor (1/2). For general signed forcing the interval must remain signed: clipping its lower endpoint to zero is valid only when positivity of the requested functional is independently known. The production API is specifically for positive-mass MFPTs; it is not a general signed-forcing API.

The contraction construction also checks out. Write (A_d) for the graph after deletion, require that retained graph to remain connected, and use (U) for the lift to constants on connected clusters, zero on the target cluster. The coarse matrix is (A_H=U^TA_dU). With exact coarse solutions (v,u) for (U^Ta,U^Tb), set (x=Uv,y=Uu). Then

\[
U^T(a-A_dx)=0,\qquad U^T(b-A_dy)=0.
\]

Every non-target cluster therefore has zero total residual, while the target cluster drains at the actual target (t). Root each cluster tree at its representative and the target-cluster tree at (t). Sending the signed subtree residual to the parent gives the required divergence at every non-root vertex. The zero-sum condition supplies the representative balance for each non-target cluster. A residual on vertices clamped to zero in the target cluster must still be retained and routed to (t); dropping those vertices' masses would change the task.

For a deleted edge oriented (i\to j), the added flow is (-c_e(x_i-x_j)), and likewise for (y). Its divergence is (-L_Dx), not (+L_Dx). Because these deleted-edge flows and retained cluster-tree flows have disjoint support,

\[
\begin{aligned}
E_a&=\sum_F f_e^2/c_e+\sum_D c_e(\Delta x_e)^2,\\
E_b&=\sum_F g_e^2/c_e+\sum_D c_e(\Delta y_e)^2,\\
J&=\sum_F f_eg_e/c_e+\sum_D c_e\Delta x_e\Delta y_e.
\end{aligned}
\]

For exact Galerkin solutions, (x^T(b-A_dy)=0) and (a^Ty=T_H). Consequently (T_0=T_H-\sum_Dc_e\Delta x_e\Delta y_e), with the minus sign in the author's proof. For inexact coarse solves, representative imbalances need an intercluster route. Extending the cluster forest by one retained original edge for each coarse-tree edge gives a full spanning tree; routing the complete original residual on that tree is sufficient. The verifier uses this latter construction, so its validity does not depend on whether the numerical coarse solve attained exact balance. A retained forest that is merely presumed balanced is insufficient.

The block refinement is valid for a specific graph-derived edge partition. Since there is one ground vertex, (\ker(B C^{1/2})) is precisely the weighted cycle space: deleting the one incidence row does not add any new divergence-free vectors. Every circulation decomposes into cycles, each simple cycle is contained in one vertex-biconnected edge block, and these blocks have disjoint edge supports. Hence the weighted cycle space is the orthogonal direct sum of the block subspaces. Its orthogonal projector, and therefore (\Pi=I-\Pi_{\mathrm{cycle}}), are block diagonal. For a bridge block the cycle subspace is zero and (\Pi_B=I). Applying (A2) only on cyclic blocks proves

\[
T=T_0+\sum_{B\text{ bridge}}J_B+
\frac12\sum_{B\text{ cyclic}}J_B+\varepsilon,
\qquad
|\varepsilon|\leq\frac12\sum_{B\text{ cyclic}}\sqrt{E_{a,B}E_{b,B}}. \tag{A3}
\]

This radius is no larger than the global radius, by Cauchy–Schwarz on the sequence of block norms. Its improvement can be enormous. Bridges are exact even when their conductance is tiny. Parallel edges must remain identifiable: two parallel edges form a cycle and must not be classified as two bridges. The iterative Tarjan implementation distinguishes parent edge IDs and passed exact parallel-edge and figure-eight tests. The figure-eight is especially useful: its two cycles meet at an articulation and belong to different blocks even though there are no bridges.

The partition in (A3) cannot be replaced by arbitrary contraction clusters. On the unit four-cycle (0\to1\to2\to3\to0), ground vertex 3 and take (f=(1,0,0,0)), (g=(0,0,1,0)). Grouping internal edges by clusters (\{0,1\}), (\{2,3\}) gives zero local products and (J=0), falsely suggesting zero remainder. In fact (B^TA^{-1}B) has the relevant off-diagonal entry (-1/4), so the remainder is (-1/4). This counterexample is saved in `audit_results.json`.

There is also a crucial grounding boundary. If several distinct target rows are removed without first identifying the targets, (\ker(B C^{1/2})) additionally contains paths joining different targets. The original graph's bridges then need not have (\Pi_B=I). For the unit path target (0)—source (1)—target (2), ground both endpoints. The grounded incidence is ([-1,1]), (A=[2]), and flow ((-1,0)) has source divergence one. Its bridge Gram correction is one, while the actual Green remainder and source MFPT are (1/2). To extend (A3) to a target set, first identify all target vertices into one ground and recompute the resulting multigraph blocks. The two path edges then form a parallel-edge cycle. This does not impair the present singleton (1\to7) run. Multiple zero-valued vertices in the coarse *trial* target cluster are also harmless when the original verifier still grounds only the actual singleton target and retains every other residual.

The mass/leaf cases are correct. For reversible rates (q_{ij}=c_{ij}/w_i), the backward equation for a singleton-target mean is

\[
\sum_j c_{ij}(u_i-u_j)=w_i\quad(i\ne t),\qquad u_t=0.
\]

Thus (a=e_s,b=(w_i)_{i\ne t}) gives (T=u_s=\mathbb E_s\tau_t). The target's own mass is absent because time after arrival is not part of the first-passage time. If (v=A^{-1}e_s), then (C_G=1/v_s) and (h=C_Gv) is the source-before-target committor, giving (T=\sum_iw_ih_i/C_G). Scaling all (w,c) by the same positive factor leaves the rates and (T) invariant. Scaling conductances alone by (k) divides (T) by (k). A normalized equilibrium partition sum is unnecessary.

A one-articulation appendage containing neither terminal in its interior has constant source Green potential. Contracting it at its attachment while retaining its total mass is therefore exact for this selected mean whenever the remaining source solution is exact. In particular, a heavy weak leaf attached to (s) contributes (M) to the mean in the supplied unit-edge example, while the same leaf attached to (t) contributes nothing. A weak internal connection on the source-to-target route is different: with (c_{sz}=d,c_{zt}=k,w_s=1,w_z=M), the mean is ((M+1)/k+1/d). Preserving only quotient mass and conductance loses the unbounded (1/d) term. The bridge correction in (A3) recovers it exactly. No first-passage variance, CDF, or tail certification follows from a mean certificate.

The numerical verifier's repaired binary64 scope is coherent. An input coefficient without bands is converted with `Decimal.from_float(float(z))`, enclosing exactly that binary64 graph, not an exact decimal value that happened to be used to generate the float. Arbitrary finite grounded binary64 trial potentials are permitted; sparse assembly, equilibration, pivoting, approximate solves, and mass summation may be inaccurate without making the residual identity false. Their errors are exposed by the original-graph residual pass. The verification must use original individual coefficients, including parallel edges, rather than trusting rounded coarse aggregated coefficients. It does so.

Every residual subtraction, subtree sum, Gram sum, energy upper bound, and final endpoint operation uses an explicit directed Decimal context. Products with signed factors examine all interval corners. Energy upper bounds use the larger exact endpoint magnitude and the positive conductance lower endpoint. `Decimal.copy_abs()` matters: ambient-context `abs()` could round a magnitude inward. The saved code uses `copy_abs()`. Square roots and exponentials receive outward neighboring representable values, covering the documented correctly rounded result even where the operation itself uses round-to-nearest. This argument is conditional on Python/libmpdec's documented arithmetic and ordinary faithful execution, not a mechanically verified implementation. The [Python Decimal documentation](https://docs.python.org/3/library/decimal.html) is the arithmetic contract consulted.

For coefficient bands, the exact true residuals and subtree flows for every positive coefficient choice lie in the computed intervals. Repeated occurrence of a coefficient creates interval overestimation, not a loss of enclosure. For each choice, the same topological block theorem applies; using upper energy bounds and a (J) interval therefore gives a uniform enclosure over the whole input box. The actual physical parameters may be correlated; covering their box remains sufficient. Coefficient uncertainty must be supplied in those bands to be certified.

No false cancellation was found in the repaired directed path. With exact zero source and mass residual on a cyclic triangle, `sqrtup(0)` returns a tiny positive neighbor, causing an outward last-digit width rather than a fabricated exact zero. The test at 80 digits encloses (7/8) by endpoints ending in `...99999` and `...00001`. This harmless conservatism could be removed with an exact-zero branch, but is not a correctness defect. A catastrophic-cancellation stress test correctly returned a useless interval ([0,6\times10^{292}]), rather than reporting success. Another test used the smallest positive binary64 conductance and a mass (2^{1023}), producing an enclosed mean around (1.819\times10^{631}); conversion to ordinary floating-point output would be inappropriate.

The long-double diagnostic is materially weaker. In the saved heavy-leaf test, (w_3=2^{80}), (c_{03}=2^{-80}), core conductances are (c_{01}=c_{02}=1,c_{12}=3/2), and the exact mean is (6044629098073145873530887/8). The global energy product radius is about (1.306\times10^{24}), while the directed block radius is (1.8811\times10^{-12}). Long-double residual arithmetic loses additive unit terms in the large mass cancellation and displays block radius zero and relative width zero. The Decimal certificate gives a nonzero valid enclosure. Therefore a diagnostic's `accepted` appearance cannot certify arithmetic. The repaired adaptive wrapper gates its final `accepted` field on the outward certificate.

Two actual API defects were found and repaired by the author after they were reported through the parent. Both exact failed outputs are preserved under the first saved code:

| Input | Incorrect first-code result | Truth | Repaired behavior |
|---|---|---|---|
| Two-state unit graph, (x=(0,0),y=(1,1)), target vertex 1 | `[2,2]` | (T=1) | Rejects nonzero trial ground |
| Unit triangle, zero trials, falsely cached singleton block for every edge | `[3,3]` | (T=1) | Recomputes blocks and rejects mismatch |

The repaired verifier also rejects nonpositive/nonfinite graph coefficients, invalid/incorrect-count coefficient bands, and malformed spanning-tree witnesses. `repair_results.json` records those rejection messages and 60 fresh independent-reference enclosures. A remaining metadata issue in pinned repaired snapshot `7d4bf20c` is separately recorded: if only `w_bounds` is supplied, the computation uses the mass bands but `coefficient_scope` tests only `c_bounds` and labels the result `exact_binary64_input_graph`. The concrete unit-edge example with nominal mass one and mass band ([2,3]) returns ([2,3]) under that label, excluding the nominal binary64 mean one. The mathematical band enclosure is valid; the label must indicate bands when either kind is present. The executed LJ38 route supplies both kinds, so it is unaffected. Later author corrections must be checked against a new pin rather than silently replacing this receipt.

The decimal-versus-float boundary is also concrete. With one edge constructed as the binary64 number `0.1`, the 50-digit certificate encloses (36028797018963968/3602879701896397), about (9.999999999999999444888\ldots). It excludes the exact-decimal-model answer (10). That is consistent with the explicitly binary64 scope. It would become an invalid scientific claim if reported as a certificate for exact decimal conductance (1/10). Signed masses similarly require the signed theorem without MFPT clipping; the old API accepted a negative mass and returned inverted endpoints `[0,-1]`, while the repaired positive-MFPT API rejects it.

The independent tests use Fraction Gaussian elimination and an independently assembled incidence/projection matrix. They do not use SciPy or the author's exact solver as a numerical reference. They establish the tested identities and examples, not arbitrary implementation correctness:

| Executed check | Result |
|---|---|
| Exact (HC H=H), cross-block zeros, bridge identity, general signed forcing and residual identity | 128 cases passed |
| Arbitrary grounded trial vectors, positive multigraphs, independent exact MFPT reference | 120 interval enclosures passed |
| All coefficient corners for a three-edge graph with two relevant masses | 32 corners enclosed |
| Ambient Decimal precisions 2, 7, 28, 100 | Same verification endpoints |
| Repaired API, fresh independent-reference graphs | 60 enclosures passed |
| Source/target leaves, huge pendant mass, exact-zero residual, binary64 extremes | Enclosures passed; diagnostic failure retained |
| Incorrect arbitrary-cluster localization and unmerged multiple grounds | Explicit exact countermodels retained |

The audit also replayed the new actual LJ38 result. `lj38_replay.json` reloaded the public source-decimal model at exact decimal temperature `0.2`, generated outward coefficient bands at precision 80, checked the saved NPZ's graph arrays and singleton source/target against that loader, and reproduced every numerical certificate field. `topology_ingress.json` independently checked all 277,776 transition-state endpoint fields: all are integral, in range (1,\ldots,100000), and exactly representable as binary64, so the float-based endpoint parser does not change topology on this actual dataset. All symmetry orders are positive integers no larger than 48. Source files have hashes `614033913e955c51f9896a1059f03a9e353c60fa09ce9ad0417b1ce056906f45` and `64ab017dfa6bc9affa4b51ac9bc4d342d1cef183e9bf4e706ce6b70acf7e0935`. The saved witness hash is `5bed8c4764fac1d52d169e8b9d00660087a1f73cb15dcf5f7f3a8751400dd88c`.

The retained connected component has 71,887 states and 122,971 individual nonself transition-state edges. For singleton source row 1 and target row 7, the reproduced raw interval is

\[
[78136.25510524738014894734912363313655943445\ldots,
\ 78296.72321314222115860672586887771251746859\ldots],
\]

with upper/lower ratio minus one (0.002053695914639048096444099157405558\ldots), about (0.20537\%). This replay took about 13.52 seconds, including band reload and verification, and did not repeat the author's adaptive selection or a full exact solve. The complete result in `lj38_replay.json` is conditional numerical evidence for the source-decimal finite model, not an independent 71,887-state rational reference solve.

The HTST normalization was checked against the pinned PyGT `io.py` formula. Its rate from minimum (i) through transition state (e) is

\[
q^{\mathrm{HTST}}_{ij}=
\frac{o_i}{2\pi o_e}
\exp[-\beta(E_e-E_i)+(S_i-S_e)/2].
\]

The new loader uses (w_i=\exp[-\beta(E_i-E_0)-(S_i-S_0)/2]/o_i) and the analogous transition-state conductance, omitting the common (1/(2\pi)). Thus (q^{\mathrm{raw}}=2\pi q^{\mathrm{HTST}}), and **HTST times are raw times multiplied by (2\pi)**. A common energy/entropy shift in (w,c) cancels. The repaired helper encloses (2\pi) using exact alternating-series remainders in Machin's identity, then multiplies with directed interval arithmetic. Its reproduced time interval is approximately ([490944.57003532629,491952.82089312207]) in reduced LJ HTST time, not seconds. The finite source-decimal energies, Hessian fields, symmetry orders, and model convention are certified numerically; uncertainty of physical energies, transition-state completeness, recrossing effects, or the HTST approximation is not enclosed.

The selected task is narrower than the database's basin task. The actual `min.A` contains states 1–5; `min.B` contains states 6–400. Singleton (1\to7) is a definite valid output but is not the basin (A\to B) MFPT. A basin mean requires its initial distribution and target-set convention, followed by the target identification needed for the block theorem. The target row is a minimum with its own supplied model data; membership in a stored funnel set does not convert a selected singleton first-passage time into a material lifetime.

Prior art changes what may be claimed. [Parés, Nguyen, Díez and Peraire (2021), Theorem 1, equations (10)–(12)](https://arxiv.org/html/2106.10945v1) already gives guaranteed two-sided linear-output bounds from primal/adjoint potentials and equilibrated fluxes, with a computable half correction and half product-of-norms remainder. The present (A1\)–(A2\) is a finite graph realization of this complementary-energy structure. The [Prager–Synge reconstruction review by Bertrand and Boffi](https://arxiv.org/abs/1907.00440) documents its hypercircle lineage. These are direct, primary-source reasons not to present the general certificate as a new computational principle. The author's additional 2015/2023 DOI citations are not needed for that conclusion; their full texts were not independently inspected in this audit.

Existing graph transformation addresses the actual requested quantity. [Trygubenko and Wales (2006)](https://arxiv.org/abs/cond-mat/0603830) gives an exact transition-probability/waiting-time approach assuming the full finite network is supplied. [Sharpe and Wales (2021)](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.103.063306) explicitly treats robust MFPT computation in metastable finite Markov chains. The locally inspected PyGT snapshot retains waiting times and branching probabilities and computes selected MFPTs after elimination. Its stability fallback is substantive competition, not a generic sparse-solver straw baseline. Local inspected hashes are `724658303c878a474aee2a8ab7ba2722116deb1f8595052cf4de90092b3b8446` for GT, `717892c14047f70e501d2777852de56b953c2cd4bdbc83fa1314db572183f0c1` for MFPT, and `615177413a230b2e6b0ec2d6fe55e9a8dbb9a6ca81ccc1356c720035f7c4441e` for IO.

The forest route and cycle-block decomposition are useful structure, but an externally checked priority result for that specialization was not established. Nor does a smaller solve automatically imply lower complete cost: all masses and conductances are read, the original graph is scanned for residuals, blocks and a routing tree are built, and source-decimal exponentials can dominate runtime. There is no worst-case small-core guarantee, and the same certificate can verify a full incumbent solution. Author-reported candidate-versus-full-sparse timings were not independently benchmarked by this audit, and no independent stable-GT timing comparison was run here. The defensible result is therefore a tested supplied-graph directional-mean enclosure using established goal-oriented error analysis, with a valid structural refinement and explicitly retained failure modes.

To reproduce the audit in the supplied runtime, run `audit_checks.py`, `repair_checks.py`, and `replay_lj38.py` from this directory with `R/.venv/bin/python` and `PYTHONDONTWRITEBYTECODE=1`. These scripts write their receipts only here. The saved snapshots, counterexamples, exact results, full-source replay, and revision diffs are the reviewable evidence; their existence and hashes are not substitutes for the stated mathematical and arithmetic premises.
