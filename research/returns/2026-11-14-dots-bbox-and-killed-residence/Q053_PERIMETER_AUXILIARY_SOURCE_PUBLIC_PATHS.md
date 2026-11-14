# Executable exact auxiliary thermal source via perimeter-coded polymers

## Result and precise scope

For the fixed R200 physical parameters θ=4,βh=.02,L1600, `PerimeterCore(L,box_sites,diag)` samples exactly the full Gibbs law conditional on every augmented plus component having a contractible lift in a box_sites×box_sites box. The graph is a SUPPLIED fixed one-diagonal-per-plaquette augmentation. For every explicit box_sites≤18, the rational proposal intensity is

Γ = n(10/27)^31 + n128^6(10/27)^46 / [1−128²(10/27)^15]
  =0.16262306109385385… .

Acceptance is at least exp(−Γ)>.84, so expected attempts<25/21. This is a finite acquired source operation, not a physical-transition sampler. In particular it can supply the auxiliary C16 interface once the governing site-count/span convention is selected (16 or17, with18 a conservative envelope). It does NOT silently identify a different box cutoff with original C16. It removes the need to wait for exponentially rare seed configurations in ordinary unconditional auxiliary acquisition; it does not close the weighted-walk proposal or physical decision/residence cost.

## Why area coding failed and perimeter coding works

A size-a DFS code grows exponentially in a, while low-temperature activity falls with perimeter. At a256-site auxiliary core, that envelope can be enormous. Instead encode every physical boundary edge of each plus component exactly once. Holes and diagonal contacts do not require flattening or omission.

For any finite plus setS fitting a b×b rectangle, a=|S| and physical nearest-neighbor perimeterP obey a/P≤b/4. In each occupied row there are at least2 horizontal boundary edges and at mostb sites; similarly for columns. Thus P≥4a/b, with no simple-connectivity assumption. For b≤18,

8P−a/25 ≥ (8−18/100)P = (391/50)P.

Every non-singleton finite set has evenP≥6. If P=6+2k, then (391/50)P≥46+15k. Since e^-1<10/27, a valid per-code rational envelope is

b_P=(10/27)^(46+15k).

For singletonP4 the sharper dedicated channel usesb1=(10/27)^31 and actual activityexp(−799/25). Treating all128^4 words as singleton candidates would waste a large constant; the singleton channel avoids that waste.

## Unique boundary-cycle code

Fix the polymer's anchor as its lexicographically minimum torus plus site. Use its unique contractible lift relative to that anchor at(0,0). Every cell coordinate lies in[-17,17]².

Represent each physical boundary edge as an oriented unit grid edge with the plus cell on its left. The oriented boundary is divergence-free at every dual vertex. Pair lexicographically ordered incoming and outgoing edges at each vertex. This defines a deterministic permutation of all boundary edges and hence directed cycles. Start each cycle at its lexicographically minimum edge and order cycles lexicographically. Cycles may touch; no simple-polygon assertion is needed. Each has length≥4 because the square grid is bipartite and a physical boundary cannot contain both orientations of one edge.

A seven-bit symbol (128-letter alphabet) stores:
-2 bits: edge direction;
-1 bit: cycle-end marker;
-4 bits: header payload.

Each cycle's first four symbols contain a16-bit header: the plus cell adjoining its first edge (35×35 possible anchor-relative positions) and its side (4 possibilities). There are4900 possibilities, below65536. Subsequent header payloads are0. Thus exactlyP symbols encode the entire polymer, including every hole boundary and any physically disconnected parts joined only by the supplied diagonals. No uncharged hole-placement record remains.

Decoding rejects short/malformed cycles, duplicated edges, inconsistent orientation, or out-of-range coordinates. A horizontal-ray winding computation reconstructs plus occupancy; it must be0 or1 everywhere and reproduce exactly the submitted boundary edges. The canonical encoding must match. Finally require anchor0, correct torus minimum, box membership, augmented connectivity and a consistent contractible lift for the supplied graph. These checks rule out all code multiplicities and invalid marks. Deterministic edge pairing is only a coding device, not the source's contour-resolution or an altered physical model.

## Poisson proposal and exact law

Let r=128²(10/27)^15=.0055457907… . A boundary mark chooses k≥0 with probability(1−r)r^k, then P=6+2k, a uniform torus root, and a uniform128-letter word of lengthP. Its total intensity is Γ_loop=n128^6(10/27)^46/(1−r), so each code has precisely intensityb_P. Codes with P>4b² are null because no valid polymer can have that perimeter. This is rejection of impossible marks, not truncation of the Gibbs distribution.

The singleton channel has intensityΓ1=nb1 and uniform root. Draw Poisson(Γ1+Γ_loop) marks and choose their channel by its exact rational intensity. Valid polymers are thinned using exact Bernoulli probabilityexp(−8P+a/25)/b_P (the singleton uses its ownb1). Unique encoding and Poisson thinning produce independent Poisson counts with intensity equal to every actual polymer activityz(S).

Reject a collection if retained polymers overlap or are adjacent in the SUPPLIED augmentation. Compatible collections may nest: an island inside a ring's hole is retained when the actual plus sets are nonadjacent. The whole physical energy is additive between distinct augmented components because nearest-neighbor adjacency is a subset of augmentation. Conditioning the thinned Poisson family on compatibility therefore gives exactly the full core Gibbs law, including thermal holes and nested plus components. Duplicate polymers are incompatible and supply no erroneous factorial factor.

The empty *envelope* proposal alone ensures acceptance≥exp(−Γ)>.84. This is a simple bound; it does not rely on measured all-empty samples. No target filter, source-flux tilt, majority exclusion, or perimeter-tail omission is made.

## Arithmetic and actual costs

All proposal probabilities and intensities are rational. Geometric sampling uses integer comparisons; Poisson inversion and activity thinning use rational Taylor exponential enclosures with lazy random bits inherited fromsource.py/source8.py. There is no fixed numerical precision cap or floating accept/reject decision. `secrets` represents the ideal random-bit interface assumption, not a claim of a formally verified runtime entropy source.

Per envelope mark expected perimeter is6+2r/(1−r)<6.012. Impossible large marks can be rejected immediately. Boundary reconstruction scans at most35² candidate cells; all finite membership/compatibility checks are charged. For the fixed tuple the expected rejection count is<25/21, and the exact arithmetic and random-bit comparisons have finite expected work. No uniform growing-r or all-temperature complexity claim is made; Γ scales with n and this fixed-width construction does not establish large-volume uniform polynomial rejection complexity.

## Executed evidence

`test_perimeter_core.py` checks every65,535 nonempty4×4 subset, including disconnected physical sets, holes and diagonal contacts: code roundtrip and exact boundary length pass. Extreme-coordinate tests include a full18×18 box and an18×18 hollow ring. Rational comparisons certify Γ<.163,exp(−Γ)>.84 and every exponent envelope through the maximum324-site perimeter1296.

10,000 unconditional auxiliary draws accepted first try and were all empty; this is expected dilution, not an empirical validation of rare-polymer probabilities. The law/cost argument is the encoding/thinning proof above. `perimeter_core_tests.json` records the run. Additional pinned-component and wrapped-graph tests are recorded separately when executed.

This construction is a new executable specialization of standard polymer Poisson rejection, not a claimed new general sampling principle or North Star breakthrough. It is separate work completed after the frozen bbox/flow v2 ZIP.

## Further implemented refinement: compact channels and relative normalizer

`CompactPerimeterCore` implements the SAME law with explicit P4,P6,P8 channels and keeps every P≥10 boundary word. This reduces the rational envelope to

Γcompact = n(10/27)^31 +2n(10/27)^47 +8n(10/27)^63
          + n128^10(10/27)^78/[1−128²(10/27)^15]
         =7.947236839014245e-7.

The small-perimeter classification is exhaustive, not a model approximation. P4 is one singleton type. P6 consists of two nearest-neighbor domino orientations. P8 consists of six connected triomino orientations, a2×2 square, and one permitted diagonal pair per plaquette. Across both possible graph orientations there are two diagonal geometric shapes; a fixed one-diagonal-per-plaquette graph has precisely one of them at each plaquette. Shapes not fitting the explicitly chosen core box are rejected. Uniform translations/type choices give each small polymer exactly one code. Valid activity is bounded by the listedb31,b47,b63; for remaining P=10+2k the common bound(391/50)P≥78+15k proves the stated geometric envelope.

Consequently, for the full thermal auxiliary core,

1 ≤ Z_aux/w_minus ≤ exp(Γcompact) ≤1/(1−Γcompact)<1.000001.

This is now a directly acquired relative-normalizer enclosure for every supported box convention≤18, independent of the original uncollected thermal-core archive. It is not a statement about the exponentially tilted physical source-flux normalizer. Unconditional rejection acceptance is also at least exp(−Γcompact), near1.

Conditioning the ENVELOPE count on≥1 and rejecting empty retained output yields the exact full core conditioned on nonempty. Its acceptance is at least

n exp(−799/25) exp(−Γcompact)/(1−exp(−Γcompact))>.04,

so expected attempts<25. Executed2000 conditional draws each for uniformNE and alternating diagonals, all singleton; attempts47573 and48126. `test_compact_perimeter.py` also verifies every remaining perimeter exponent and all small channel activity bounds with exact rationals. It exhaustively checks all4×4 subsets, finding precisely1,2,9 translation-normalized connected-in-king-graph shapes at P4,P6,P8; the last9 are7 NN shapes and2 possible diagonal shapes. Receipt:compact_perimeter_tests.json.

The earlier baselinePerimeterCore remains available and its receipt remains historical. Recommended caller API is now `CompactPerimeterCore(1600, chosen_box_sites, supplied_diag)`. Both methods sample the same explicitly selected law; only the proposal envelope differs. No perimeter truncation or source approximation was introduced.
