# Independent subreview: raw compiler tokens and augmented weighted coverage

2026-10-30. Scope: V1 Sections 2, 4, 5, and the CSS-sector clarification. This is not a whole-controller, CP-similarity, or killed-basin verdict. All conclusions below were checked against the actual full-animal proof rather than inferred from prior acceptance language. Frozen inputs were not changed.

## Result

**No mathematical defect was found in this scoped raw-charge/coverage composition**, assuming the expressly imported small-reduced-error FGL confinement/active-hub interface and the fixed bounded footprint/incidence hypotheses. There is an important precision for the augmented container statement: `J(C) contains exactly sigma(C) among occupied vertices` is no longer true if “vertices” includes tokens. The needed and valid statement is “among occupied SYNDROME vertices.” Arbitrary occupied flag tokens can be in a container; they improve the completion lower bound and are never subjected to confinement. V1 does not explicitly make the false stronger statement, but this distinction should remain explicit in any rewrite.

## 1. Idempotent local rule and actual active hubs

The complete consulted syndrome includes every check the possible corrections can change. Enumerating subsets of the fixed generator support gives a fixed finite orbit. The channel first dephases distinct consulted-syndrome sectors; the chosen Pauli takes each measured sector to a local minimum; and every already minimal sector uses the identity correction, including ties. The second channel application therefore leaves the first output unchanged. Hence Phi_h^2=Phi_h as a CPTP superoperator, not merely on diagonal states.

Each nonidentity choice lowers global syndrome weight by at least one. If its changed set has cardinality at most k_data, beta_data=1/k_data is valid. A formerly permitted FGL strictly improving flip certifies that the source is not an orbit minimum, so the new hub is still active. Which minimum is selected is irrelevant to componentwise active-hub mass. The changed set remains inside the fixed full read/correction footprint. Inactive local measurement alone leaves the diagonal animal observable unchanged.

## 2. Why each raw reset is a genuine deterministic sector map

The explicit full excited-space unitary is the composition of (a) a syndrome-controlled XOR on the label and (b) a label-controlled Pauli. Each is a permutation of joint global syndrome/auxiliary-label sectors, with a unitary action inside each sector's degeneracy space. The guarded product retains this property. Conjugating a single physical auxiliary reset by that product gives a partial sector permutation, not a generic merging linear map. Its adjoint therefore preserves the joint diagonal algebra. For a fixed occupied source sector exactly one physical reset label is nonzero and the total reset rate is kappa.

The combined physical flag C_h=Q_h-G_h E_h is cleared at h by resetting h. A different previously unflagged occupied j was isolated and good. If it overlaps h, it could not have been unflagged while h was occupied; if it does not overlap h, the data/reset operation is disjoint. A ready j remains ready. Thus no reset creates a previously zero flag, as an exact source-subspace inclusion, not a probabilistic assertion. Gauge conjugation retains those inclusions.

Let K=R D_flag+k_reset and R>k_reset. On every bad-source sector the changed occupied-vertex set D contains all R own flag tokens, creates no flag tokens, and obeys

    removed(D)-added(D) >= R-k_reset,
    |D| <= K.

Thus beta_bad=(R-k_reset)/K>0. The declared D cliques make the existing full-animal charging proof applicable verbatim. With u=1-c and q=(1-theta)/2,

    D_h^bad >= q C_h sum_{B connected, D subset B} f_B.

For any connected A containing h's entire token bundle, B=A union D is connected, its weight obeys f_B>=theta^(u K)f_A, and for fixed B at most 2^K such A occur. Consequently the uniform explicit charge is

    D_h^bad >= q 2^(-K) theta^(u K) C_h
                 sum_{A connected, bundle(h) subset A} f_A.

The changed set D may depend on the local source pattern; the same constants work because its support and cardinality bounds are uniform. No independence of token copies or pinching is needed.

## 3. A noncircular augmented container construction

First fix the finitely many local data/read/reset/noise footprints and token multiplicity. For each data vertex x, choose a bounded vertex set J_x containing its own dummy, all incident syndrome checks, all possible changed-check sets for hubs whose full read footprint contains x, and whatever additional bounded token/reset neighborhood is required. These choices precede the component graph. Their cardinalities and incidence are uniformly bounded.

Next define the DATA graph G to include all declared local DATA support cliques and an edge x-y whenever J_x intersects J_y. In the animal graph include dummy G edges, connect x to its other J_x vertices, and include all possible reset/correction changed-set cliques. Every degree is bounded. For a G-component C of a minimum representative E, set J(C)=union_{x in C}J_x. Then:

- J(C) is connected because dummy G edges lie within it, and |J(C)|<=D0|C|.
- Different error components have disjoint J(C), by the defining overlap edges.
- Every occupied syndrome check in J(C) has an incident erroneous data vertex y. It belongs to J_y, so overlap forces y into C. Thus its occupied syndrome checks are exactly sigma(C), without cancellation between components.
- Arbitrary occupied token vertices may also occur in J(C), but no assertion about their confinement is needed.
- Every active hub reads an erroneous site. All erroneous sites in its full read footprint lie in one G-component because their J_x contain the same hub changed-check footprint. Its actual selected D_h lies in that component's J(C). Conversely a componentwise FGL active hub is globally active: all errors in the full read footprint are already in C.

Since C is a subset of a minimum representative it is reduced. Assuming |C|<ell, imported confinement gives |sigma(C)|>=h|C|, hence |J(C)|<=b0|sigma(C)| with b0=D0/h. FGL hub mass gives g_C>=kappa_A|sigma(C)|. Enlarging G does not require a new expansion theorem: the imported theorem is for all reduced small errors, not only errors connected in the old graph. It does require recomputing D0 and the basin's component definition, exactly as V1 says.

## 4. Full augmented coverage with explicit entropy accounting

Let s_A count occupied syndrome vertices and b_A occupied tokens. Choose 0<eta<u. Partition all connected animals into total-sparse, flag-dense, and the remaining syndrome-dense class.

**Total-sparse:** if s_A+b_A<eta|A|, then f_A<=theta^((u-eta)|A|). If A0 bounds rooted animal counts, taking A0 theta^(u-eta)<1 gives sum_sparse |A|f_A<=C_vac N. The graph has O(N) vertices since R and hub incidence are fixed.

**Flag-dense:** if b_A>=eta|A|/2, at least eta|A|/(2R) distinct bad bundles meet A. Divide |A|f_A equally among those bundles. For any assigned h, completing just its own bundle gives connected B with f_B>=f_A, because all added tokens are occupied. Fixed h,B has at most 2^R sources. Therefore

    sum_flag-dense |A|f_A
      <= [2R 2^R/(eta c_bad)] sum_h D_h^bad.

**Syndrome-dense remainder:** s_A>=eta|A|/2. The original covered/poor proof may be repeated with k_A=s_A, counting ONLY syndrome occupancy. For covered A, complete by one active D_h meeting A; the ratio f_B/f_A>=theta^(u k_data) is unaffected by spectator tokens. For an uncovered A, poor components carry at least half s_A. A poor C has at least kappa_A|sigma(C)|/2 active D_h disjoint from A. Bounded incidence nu gives

    |sigma(C) outside A| >= kappa_A|sigma(C)|/(2nu)
                            >= alpha |J(C)|,
    alpha=kappa_A/(2nu b0).

For B=A union J(C), let j=|J(C)|. Added occupied syndrome vertices alone give

    f_B/f_A >= theta^(-(alpha-u)j).

Any added occupied tokens increase this ratio. For fixed C,B there are at most 2^j source A. Taking u<alpha and 2 theta^(alpha-u)<=1 pays all preimages. The charge coefficient |A intersect sigma(C)| is at most |sigma(C)|<=g_C/kappa_A. For fixed B, summing g_C over containers wholly contained in B counts distinct active hubs whose actual D_h are contained in B. There is no uncontrolled component factor and no simultaneous completion of many components.

Thus sum_syndrome-dense |A|f_A<=C_data sum_h d_h, using the strict per-move bound d_h>=q sum_{B containing D_h}f_B and |A|<=2s_A/eta. Combining the three classes proves exactly

    W_ext <= C_cov (sum_h d_h + sum_h D_h^bad) + C_vac N.

All animal sums must remain untruncated. The parameters are compatible: first fix R and augmented graph/constants; choose u positive below the beta-move and alpha-completion margins; choose eta<u; then theta sufficiently small for finite move/preimage/counting inequalities. No choice depends on N.

## 5. CSS sector sum

Use separate syndrome/dummy/token graphs for the two CSS sectors. The same physical flag contributes R identical combinatorial copies in each; no new registers or independent random bits are introduced. Choose R larger than both sectorwise reset syndrome-flip bounds. Every bad reset then has a strict charge in each graph, and its decrement of the sum is the sum of the two decrements under the SAME physical rate kappa. This does not double the reset rate.

An X-type accepted correction changes only its corresponding check sector and leaves the opposite raw potential fixed, and conversely for Z. Thus all per-move, data-coverage, and bad-reset inequalities add with common worst-case constants. Containers need be disjoint only within a given sector's chosen minimum representative. No disjointness of X- and Z-error containers in a common mixed graph is assumed or needed.

## Exact input hashes (SHA-256)

- FULL_SIMPLE_COMPILER_MANUSCRIPT_V1.md: `27cf4facafb16e35e6f6206c18e972b4fa7ce6b41431390de6b89ce2c66b25f6`
- FULL_SIMPLE_COMPILER_V1_CSS_CLARIFICATION.md: `a1de9c36528876bee8e9f5afe33f5dd93e922196028a1282ccbd6fb16a131deb`
- AUGMENTED_FLAG_COVERAGE.md: `e3f241884488c40a9453664bfdb1c6d58c1d65c7dd6b2de9a549e481025ed520`
- MONOMIAL_BAD_RESET_CHARGE.md: `e1ef5f188554c4dd698aad58a312dd2c1485dc2cefa241d328720e0f2f3de948`
- MONOTONE_COMPILER_FLAGS.md: `36f8ee93a3ab61c116da919cc70dad41d127219694decbb150c2d1b849a897d3`
- WEIGHTED_PROGRESS.md: `eb73f1a44736fd20cad9039ea711fbc549cd4ae53e90c769c619da02eb882702`
- FULL_ANIMAL_KILLED_BASIN_CANDIDATE.md: `b2981ef69f958aa461a3cb0d4753fa0fbc1e27bb9430c0bffd7f8687b09436ff`

No whole-theorem conclusion is implied by this subreview. In particular CP similarity on the basin, cross-mask correction terms, dressed noise transfer, and canonical logical action require their own checks.
