# Independent audit: direct K13 representation and finite-star certificate

Date: 2026-11-02. Scope: the intrinsic-page, skeleton-first completion already declared in `producer-workspace/ATLAS_NORMALIZATION.md`, together with the source's admitted box/edge geometric induction. This is a fresh audit; it does not replace the earlier thermal-contraction theorem/audit.

## Verdict first

**PASS for the declared source-compatible atlas and the unchanged vertex-generator coordinates.** The exterior capacity argument, complete boxed-star calculation, Shearer rank bound, path edge bases, and termwise Clifford/Gibbs identity establish

- maximum actual stabilizer weight at most 13;
- maximum X incidence per data qubit at most 12, Z incidence at most 4;
- check-overlap bound including self at most 196;
- at most three qubits per edge-frame Clifford block;
- no added data qubits and no source-temperature/energy overhead.

This is not merely ground-space equivalence: every named source Hamiltonian term, coefficient, syndrome projector, and full Gibbs state is conjugated exactly. The principal argument does **not** change the vertex-generator basis.

Two boundaries remain explicit. (i) Exact recursive rotated-template identity is supplied by the declared atlas, not proved merely by a source figure caption saying “nearly identical.” Consequently this audits that construction, not every unspecified alternative cellulation of the figures. (ii) The native two-body construction must be compiled again, and its actual footprint/contact/tail/imperfection constants checked. Exact source Gibbs conjugacy alone is not a native perturbation-admission proof.

## Governing strongest baseline: untouched source Hamiltonian already has K15 / D196

**The safest implementation result does not require even the edge Clifford.** The proved Q_v<=13 controls every old vertex generator in every existing edge basis. In an arbitrary old basis an edge stalk has dimension at most three, so each face Z term has weight at most 5·3=15. Consequently the **original Hamiltonian, with every original term, basis, coefficient, syndrome law, decoder input, and physical noise dictionary unchanged**, now has the certificate K<=15 and q_X+q_Z<=16.

The generic formula gives D<=226, but the same geometry proves **D<=196** without changing a basis. For an X check use 1+13(16−1)=196. For a Z check on a polygon of at most five edges, overlapping X checks lie only at its at most five boundary vertices, giving at most 5·6=30. Other overlapping Z checks lie on one of those edges: each has at most three other cofaces, giving at most 5·3=15. Include the check itself: its overlap count is at most 46. The common maximum is therefore 196.

At fixed effective J and eta, a new sufficient K15 native compilation has peak coefficient ratio (15/180)^3=1/1728 relative to the previous conservative K180 certificate. This is a sharper certificate of the same source Hamiltonian, not a claim that the old realized checks actually attained weight 180. Native recompilation/tail conditions still apply, but there is **zero new Clifford footprint conversion** in this baseline. The optional path-frame route lowers K15 to K13 with exact source Gibbs conjugacy; its possible factor-three data-word spreading means it cannot be advertised as generically noise-superior to K15 without the separate admission comparison. This K15 baseline is the governing large implementation gain.

## 1. Exterior capacity: double germs do not defeat the bound

Inspected the primary source `explicit_memory_witness_20261102/arxiv_src/paper.tex`, especially `claim:quantum_embedding_outside_boxes` (Claim 6.11; source lines approximately 5251–5313) and the earlier definition of simple local structures (approximately 4522–4549). It explicitly permits either:

1. one abstract edge occupying a lattice unit segment, with at most three incident faces; or
2. two abstract edges occupying that same segment, each with at most two incident faces.

For Rep_d, dimension is one (for d>=1); for Par_d it is d−1. The capacity per geometric direction is therefore at most two in **both** cases. It is immaterial whether coincident edge germs belong to the same abstract vertex or different ones: summing the whole geometric direction remains an upper bound for any one vertex. Six directions give Q_v<=12.

The proof needs the admitted geometric statement that collapsed-edge degeneracies are confined to the exceptional boxes. This is consistent with the listed T gadgets and the source's “only simple local structures” invariant; it must not be weakened to a statement only about the count of nonzero-length edges. The declared atlas adds no hidden interior cells, coordinate-driven identifications, or accumulating physical comparison subdivisions. With that premise there is no overlooked zero-length exterior contribution. Noninteger box boundaries keep every exterior lattice vertex a positive distance from every exceptional box, so applying the structure invariant to short incident germs is legitimate even when another endpoint is inside a box.

No assertion that exterior links are simple octahedral subgraphs is needed. In particular the earlier tempting identification of distinct edge germs by spatial direction has been avoided correctly.

## 2. Box membership and real collars

Inspected Example 6.8's literal polygon words and the source figures `quantum_example.pdf`, `quantum_doubling_T_junction.pdf`, `quantum_refinement_box.pdf`, `quantum_refinement_box-2.pdf`, and `quantum_doubling_free_cross.pdf`. Raster copies used for inspection are under `concrete_stars/audit_images/`.

### Newly doubled T

In the open box (-2/7,9/7) × (-2/7,2/7) × (-2/7,9/7), the named abstract vertices are precisely O,P,Q,R,D0,D1. P,D0,D1 coincide geometrically but are distinct abstract IDs. Completing the literal cylinder polygons with the original and copied sheet collars gives:

- original upper O−R−A0, right O−D0−C0, lower O−B0;
- copied upper Q−A1, right Q−C1, lower Q−D1−B1.

Every rib segment has two sheet-side faces. At the book root the two along-seam germs are common across retained pages; intermediate path vertices have separate page-side germs. These are the actual scaled edge-book collars, not boundary closures invented for an isolated polygon fixture.

The extra Q−R germ in the upper cylinder page must be retained. Its degree-two stalk is the extra contribution responsible for Q_v=13 at all-red Q. Without it the calculation would undercount. The script does retain it.

### Recursive T residual

The open box (-2/7,16/7) × (-2/7,2/7) × (-2/7,2/7) contains precisely O,P,Q,C0,C1 in the listed local coordinates. R=(2,0,1) and B4=(2,1,0) are outside, as are the other upper/lower side ports. The collar meeting this box is the original sheet book with paths O−A0, O−C0−C1−C2, O−B0. There is no basis for adding a second copied book at Q to this residual template. The script correctly does not do so.

Thus truncated unknown cofaces at R or B4 cannot invalidate the finite list of **inside-box** stars; those exterior vertices use the six-direction argument instead. O has a K_(3,d) link; P and Q have theta page paths (2,2,2) and (1,2,3), respectively; C0/C1 are the corresponding K_(2,3) attachment stars.

### Crosses

A newly doubled glued-cross box contains only the two endpoints of its degree-four cylinder edge. The full endpoint link is a four-cycle plus a center joined to all four outer vertices. A free-cross box contains separate abstract single-rib attachment stars even where their images overlap; each is K_(2,3). Gluing these free-cross IDs would be a different construction and would require a new certificate. The next refinement leaves no residual cross box, so the exterior invariant, not an unverified split-cross endpoint guess, controls its output.

### Executable checks

Reran `boxed_link_geometry_certificate.py` and independently checked every output in `audit_k13_regression.py`. All 252 cases pass independent GF(2) rank, generator-validity/independence, dimension, Q_v, and twice-covered entropy-bound checks:

| class | cases | max Q_v | max dim F_v |
|---|---:|---:|---:|
| doubled T | 132 | 13 | 4 |
| recursive T | 116 | 12 | 4 |
| glued cross | 2 | 11 | 4 |
| free cross | 2 | 7 | 2 |

The regression also tests membership of all named coordinate vertices using exact integer inequalities. Enumeration verifies the stated finite input; it does not by itself prove that those inputs are the physical collars. The source/atlas binding above is the separate geometric argument.

## 3. Recursive closure and its exact evidentiary scope

The primary source states: types 1/2 refine to only type-2 residual boxes; types 3/4 leave none; boxes are disjoint; W0 has no ribs and carries inherited residual boxes in separate original/copied sheets; other regions produce only named T/glued/free boxes. With the atlas's explicit page-deletion and rotation/reflection generators, this closes a finite local class from the square seed. No global enumeration of all large codes is required for this induction.

**Scope caution, not a new obstruction for the declared construction:** the source caption for `quantum_refinement_box-2.pdf` says the rotated structure is “nearly identical,” and Example 6.8 says other nonsquare words are obtained analogously. These phrases alone are not an exact combinatorial port map. The needed exact identity is generator 3 of the already declared atlas: rotations/reflections and recursive repetitions of the two specified page words with relabeled ports and the same ordered exterior port word. If a later claim is instead about every literal/uncompleted source drawing independently of that definition, the exact gate is: supply the second-type-2 polygon words and port gluing (or a germwise capacity certificate) and verify that they are covered. Merely observing the two pictures look alike would not discharge it.

## 4. Rank, incidence and path-basis algebra

For a complete regular polygon star every face coordinate occurs in two distinct edge-germ restriction sets. Uniform A in F_v gives, by the twice-covered entropy inequality,

 2 dim F_v <= Σ_e H(A restricted to e) <= Σ_e dim F_e = Q_v.

No independent face-bit assumption is involved; the standard conditional-entropy chain-rule proof applies equally to dependent coordinates. Degenerate embedding does not destroy regular **abstract** polygon boundaries. Hence Q_v<=13 implies dim F_v<=6. Two endpoint stalks give q_X<=12 in any vertex basis. This bound counts rows conservatively and does not require an optimized basis.

A single globally fixed ordering of abstract face IDs at each red edge gives its path basis. Every face belongs to at most two path columns. A polygon has at most five abstract edges, so w_Z<=10; an edge has at most four cofaces, so q_Z<=4. There are twelve unoriented Hamiltonian paths on four labeled faces, and the bound is uniform across all twelve. No endpoint chooses a private basis. Thus K<=13 and D<=1+13(12+4−1)=196 are valid conservative certificates.

## 5. Exact full-Gibbs conjugacy, and what it does not prove

With E_new=E_old A, d0_new=A^(-1)d0_old and d1_new=d1_old A. The computational-basis linear permutation U_A|x>=|Ax> implements

 U_A X(u) U_A^† = X(Au),
 U_A Z(v) U_A^† = Z(A^(-T)v).

This gives the claimed conjugacy of corresponding **individual** X and Z terms with coefficients unchanged; term dependencies, zero-weight identity terms, and redundant named rows do not invalidate it. All spectra, partition functions, Gibbs states, and named-syndrome projectors follow at every beta. Dual-sector compatibility is automatic because the same Clifford implements both actions.

The independent regression checks both Pauli actions on all 175 invertible binary frames of dimensions 1–3, for all binary Pauli vectors and computational states: 172,816 exact action identities pass. This is a check of conventions in addition to the symbolic proof.

A new single-qubit Pauli maps to at most three old data qubits in the same edge stalk. A native prefix of at most 13 new data Paulis maps to at most 39 old data qubits. Full-trace/readout transport is available in the old frame, but claims about **physical noise strength** must account for that bounded spreading/contact load. In particular one must not silently reuse a pointwise local-stochastic exponent without checking its dictionary. The direct source thermal syndrome law itself has no such loss, because it is exactly identical.

Recompiling is necessary: directly conjugating an old two-body data-clock coupling could produce a multi-data coupling. The stated K13 native route correctly recompiles and does not claim native whole-spectrum equivalence to the old compiled device. At fixed effective Pauli coefficient J and eta, the sufficient resonant coefficient certificate is reduced by (13/180)^3 = 0.00037671467764060346; that is a comparison of sufficient designs, not proof the previous 180 bound was attained or optimal. New clock tail and admitted-perturbation constants remain the explicit downstream check before any laboratory-tolerance claim.

## Files and reproducibility

- Audited derivation: `DIRECT_K13_GIBBS_CERTIFICATE.md`.
- Audited geometry: `concrete_stars/FINITE_BOX_AND_EXTERIOR_GRAMMAR.md`.
- Finite producer: `concrete_stars/boxed_link_geometry_certificate.py`.
- Independent regression: `concrete_stars/audit_k13_regression.py`.
- Regression output: `concrete_stars/audit_k13_regression.json` (PASS_ALGEBRA_AND_LISTED_COORDINATES).

Run from any working directory with Python 3. The scripts only read the specified scientific fixtures and write their result JSON files in this package.

## Final narrow audit: explicit native dictionary and uniform thermal admission

Inspected `UNTOUCHED_K15_AND_NATIVE_DICTIONARY.md` §§3–4 and `DIRECT_K13_NATIVE_RESOURCE_LEDGER.md` against the earned heterogeneous formulas in `resonant_clock_compiler_20261102/resonant_rod_bound.md` and the ordinary-tail estimate in `temperature_uniform_protection_20261102/FRESH_NATIVE_SYNDROME_HOLE_AUDIT.md`. **PASS; no formula correction required.**

For one microscopic term with d data, c clock and b bath sites, the initial Pauli/matrix-unit expansion has at most 4^d M^(2c) d_B^(2b) coefficients of modulus at most its operator norm. In W(q')† E W(q), unchanged prefixes cancel up to Pauli phases; only intervals from the at most c changed check prefixes remain. Thus the untouched-source word has support at most d+15c. An unchanged clock can affect the phase only if its check touches E or has edge-block overlap with a changed check. There are at most 16d+195c additional controls. Their diagonal matrix-unit expansion gives the displayed conservative

 C_dict = 4^d 15^(16d+197c) d_B^(2b).

Including the originally acted-on clocks gives b_c<=16d+196c, and a one-neighborhood enlargement gives d_c<=196b_c. Diagonal control functions commute with the prefix gauge, so no second or iterated light cone is missing. The relevant graph is the enlarged **edge-block** graph, whose D<=196 bound is valid in both edge frames; physical-qubit overlap alone would not justify frame-independent controls. For the optional K13 frame, the output data word is at most 3d+39c in the old decoder frame, while the same clock/contact bounds and the dictionary with 13 in place of 15 remain safe. These are deliberately loose but explicit norm/support bounds, not asserted optimal noise tolerances.

For x=Dbar eta²<=1/64, beta J>=1 and M>=3, the heterogeneous choice gives mu_a>=2JM/eta² and b=16Dbar JM, hence mu_a−b>=(7/4)JM/eta². The sufficient wrap expression M(M−1)exp[−(7/4)(beta J)M/eta²] decreases with M on this domain; at M=3 it is at most 6exp[−21/(4eta²)]<=eta². This discharges the full-circle wrap condition uniformly, rather than borrowing monotonicity of an old M180 design. The winding tail is at most exp[2/9−3/(2eta²)]. For the ordinary tail, c_a=t_a/K_a²<=mu_a/4 gives M0,a(c_a)<=(4/3)JK_a, and monotonicity of s exp[−s/(2eta²)] for s=(beta J)M>=3 gives

 beta delta_bar <=4exp[−3/(2eta²)]<=4exp(−96).

The separate event-pressure and generic-activity inequalities remain required exactly as stated; the audit does not replace beta J Dbar eta² admission by an all-temperature assertion. This closes the requested finite locality/tail ledger for applying the already admitted native theorem to the new compilation. No further optimization is used.
