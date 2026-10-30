# Independent hostile review: all-small-reduced-error GPT active density

2026-10-30 UTC. Reviewed exact drafts:

* `GENERAL_ACTIVE_DENSITY.md`: `760e43ed233706c721b920bbf0a1f368de507bb4a1de167abb7b3ce56b47870c`
* `LOCAL_CASE3_DISCHARGE.md`: `1005e743f82f0a25a666447709a538967398666d077aee5d943304113dda1842`

Copies and `SOURCE_SHA256.txt` are retained here. Originals were not edited.

## Verdict

No mathematical defect found in the proposed active-hub-density derivation under the declared GPT code-family, robustness, expansion, reducedness, and small-error hypotheses. The localization of metastability/low-overlap is supplied by actual arguments, not inherited from an inapplicable global hypothesis. The resulting constant is conservative and positive for a fixed sufficiently large admissible degree.

This is scoped acceptance of the NEW density lemma and its local discharge. It is not a quotation of an existing multiplicity theorem, not inherited FGL acceptance, and not acceptance of an energy-token lift, D0/D1 transfer, weighted continuous-noise drift, or exp(cN) memory result. Those require their own interfaces.

## Primary-source cross-check

Read the actual [Gu–Pattison–Tang arXiv HTML](https://arxiv.org/html/2206.06557), identified there as arXiv:2206.06557v1: Definitions 16–28/31; Lemmas 19,22,29–33; and Section 4.2.2 through equation (119). The local-code and mixing ingredients match the draft's usage. For family parameters, choose the sufficient regime 0<eps<eps'<1/28 and delta<h^{-1}(rho), 0<rho<1/2, with simultaneous primal/dual robustness at exponent eps'. The paper supplies positive rate and linear distance: k≥(1−2rho)^2 n and d≥delta n/(4 Delta^(3/2−eps)). Its guaranteed correction radius is delta n/[6 Delta^(3/2−eps)(1+2Delta²)], smaller than the existence radius used here. Soundness U≥Delta^(-2)|e| for reduced errors is invoked only within the guaranteed correction radius. These distinctions must survive any subsequent memory lift.

## 1. Tie-sensitive local reversal

Let the chosen local corrections be minimum, with arbitrary nearest-codeword ties. At an inactive hub a, a face in both endpoint corrections would admit a strictly improving singleton. Therefore all correction incidences on Q(a) are unique, regardless of overlaps elsewhere.

For F⊆R∩Q(a), keeping each original c_v produces candidate new corrections R_v^+ XOR(F∩Q(v)). Summed candidate weights equal U(e), because each flipped face decreases one endpoint candidate by one and increases the other by one. Inactivity gives U(e XOR F)≥U(e), while local minimization gives the reverse inequality. Every individual minimum is bounded above by its candidate, and their sums are equal, so EACH candidate must attain the local minimum. This is the necessary tie-sensitive argument: no predetermined tie-breaking rule is assumed to remain invariant, but the old nearest codewords are valid consistent choices after the flip.

The total correction union stays unchanged: incidences on F reverse and all others remain fixed. Only uniqueness on F was needed. Remote correction overlaps are harmless. This proves the local replacement for the global R-flipping lemma rather than merely citing its stronger premises.

## 2. Inactive V1 hub implies full local low-overlap

For inactive v, first reverse all its outgoing correction incidences by flipping R_v^+. Its new local correction is empty and its nearest codeword remains valid. If a local codeword c overlapped R_v on more than half its weight, the second flip F'=R_v∩c would remove correction entries at the other endpoints. Their combined local potential decreases by |F'|, while v has a candidate correction of weight |c|−|F'|<|F'|. The combined mask lies inside Q(v), contradicting original inactivity.

This argument requires no global metastability and no claim that the intermediate error is globally inactive. It supplies exactly the full local low-overlap property needed for arbitrary single-row/column codewords in the later dense-edge argument.

## 3. Y and exceptional vertices without low-overlap

Minimum correction against the available zero codeword gives |R_v^+|≤|e_v| and hence |c_v|≤2|e_v|. Nonzero c_v has local weight at least delta Delta. Counting each erroneous face at its two V1 endpoints yields

|Y| delta Delta≤4|e|.

Substitution of the stated error radius and n=Delta²|V1|/2 gives exactly the draft's small-|Y| bound. This does not assume the false arbitrary-state lower bound on residual y-degree at every Y vertex.

A residual y face lies in e but in neither endpoint correction, so both endpoint c_v are nonzero. Thus exceptional residual degree can be compared with E(Y_e,Y) for arbitrary e. The displayed mixing upper bound leaves a gap (1/2−1/3)Delta^(3/2+eps)|Y_e|. Squaring the resulting inequality gives 24² Delta^(-1-2eps)|Y|, exactly q_e=576 Delta^(-1-2eps).

If an error face has neither endpoint in Y, both endpoint nearest codewords vanish and that face is an improving singleton. Such a face belongs to an active V1 local view. Covering all error faces by Y local views plus active local views gives |e|≤Delta²(|Y|+g), and U≤2|e|. This remains valid when Y is empty.

## 4. Restricting dense origins is sufficient

Under g<|Y|/4 and q_e≤1/4, at least half of Y consists of inactive normal origins. At each such origin, the preceding local low-overlap bound makes its nearest codeword small enough for robustness, so its row/column decomposition and a nontrivial dense slice are available. For sufficiently large Delta, the slice's approximating codeword cannot be zero. Applying local low-overlap to that row/column codeword also gives residual faces in the slice, so the edge satisfies the residual-incidence part of the dense-edge definition.

Every origin contributes at least one distinct V1–V0 edge. Thus |D_*|≥|Y|/2 and the maximum 2Delta endpoint degree gives |W|≥|Y|/(4Delta). The lower neighbor count at w uses only the one inactive normal origin, not low-overlap at all Y vertices. Its residual faces have other endpoints in Y. The mixing argument for W uses this lower neighbor count and the already established small |Y| bound, giving the stated 81/(delta² Delta) upper ratio for sufficiently large Delta.

Consequently mean D_*-degree is at least delta²Delta/162. With alpha=delta²/648 this is actually 4alpha Delta, stronger than the required 2alpha Delta. The claimed alpha/2 fraction above alpha Delta is therefore conservative.

For exceptional neighbors, |Y|/|W|≤4Delta and |Y_e|/|Y|≤576 Delta^(-1-2eps) bound the square-root mixing term by 192 Delta^(1/2−eps)|W|. The density term is ≤192 Delta^(-1/2−eps)|W|, absorbed by one additional Delta^(1/2−eps)|W| once Delta≥192. Markov with beta_exc=772/alpha removes at most alpha|W|/4. The remaining alpha|W|/4 special vertices are therefore justified without any global normality premise.

## 5. Actual local case-3 discharge

For a special w outside the closed neighborhood of active hubs, w and every V1 endpoint incident to its faces are inactive. This supplies unique correction incidence on Q(w), low-overlap on each neighboring V1 full view, and normal-view approximations on exactly the views subsequently used.

The row/column split is pointwise: off R_0, the two codeword bits both equal y_0; on R_0, exactly one endpoint codeword bit is one. Assigning that bit to the row or column yields the displayed disjoint decompositions. No information about correction overlaps outside Q(w) is required.

After F=e∩R_0 is flipped, the local reversal proof preserves nearest codewords, total R, residual y, and U. The error inside Q(w) is y_0. On every neighboring normal row/column, correction minimality and the unchanged codeword approximation bound the change under flipping its y_0 slice by the negative R_row/R_col slice weight plus Delta^(1/2+eps)/delta. Other affected views are exceptional or have zero slices. The full potential difference has no additional outside terms: every face of Q(w) has both V1 endpoints among these neighbors.

Inactivity of ORIGINAL w applies to the combined mask F XOR y_0; equality U(tilde e)=U(e) supplies the required no-improvement inequality from the intermediate configuration. It does not require that intermediate neighboring hubs remain inactive. Summing gives the stated |R_0|≤3t, row/column distance sum ≤10t, and—using good-origin dense edges only—the positive quadratic lower bound on |y_0|.

With simultaneous robustness at exponent eps'>eps, 10t is within its agreement radius for sufficiently large fixed Delta. The tensor agreement estimate gives the local stabilizer c_0, and |e_0+c_0|≤18t is smaller than the quadratic lower bound. The contradiction uses reducedness of the ORIGINAL e, not of tilde e. This discharges the otherwise load-bearing global-metastability localization step.

All needed degree inequalities can be imposed together: eps'>eps provides growing robustness slack; eps<1/2 gives the quadratic-vs-Delta^(3/2+eps) separation; eps>0 controls exceptional terms; alpha,beta_exc are fixed independently of Delta. Also impose the agreement theorem's weight range below half the product of local distances. This is another finite lower bound on Delta. Choose Delta along the admissible code/expander degrees with the simultaneous robustness properties, not an arbitrary unverified local code.

## 6. Charging special patches to active neighbors

Each face has four distinct hub corners. A hub shares faces with at most 3Delta² other hubs, hence K=1+3Delta² bounds a closed overlap ball. Any special w outside the union of active closed balls gives the preceding contradiction, so all special w belong to that union. Therefore

K g≥alpha|W|/4≥alpha|Y|/(16Delta).

This proves g≥c_Y|Y| in the g<|Y|/4 case; the complementary case is stronger because c_Y≤1/4. Combining with U≤2Delta²(|Y|+g) gives exactly kappa_GPT=c_Y/[2Delta²(1+c_Y)]. No adaptive counting, disjointness of closed balls, or injection from special vertices to distinct active hubs is assumed; the K multiplicity is explicitly paid.

## 7. Independent regression and scope of acceptance

`check_local_reversal.py` enumerates two small two-endpoint potential systems with all nearest-codeword choices, including ties. It checked 1,818 choice configurations, 1,196 inactive-hub instances, and 1,868 reversal subsets. In 408 inactive-hub instances, correction overlaps existed elsewhere. All local reversal, unchanged-codeword choice, union-preservation and inactive-hub low-overlap assertions passed. This is a toy algebra regression, NOT a finite-degree numerical proof of the Tanner density theorem.

The active-density result is for the GPT potential U and hubs in BOTH V0 and V1. It must not be relabeled as raw-syndrome SSF progress or applied to a different Tanner decoder without a new argument. Componentwise use requires a graph containing complete read neighborhoods, plus the reduced-subset and local-energy-separation checks. The smaller guaranteed decoding radius must be used when importing confinement. No exponential-lifetime upgrade follows from this receipt alone.

No tool or permission blocker occurred. No proof failure was repaired or hidden. No original file was changed.
