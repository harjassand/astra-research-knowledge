# Exact mixed source–rod factorization for generic native perturbations

2026-11-02. Constructive algebraic/combinatorial lemma, following the supplied exact native-clock dressing. This note proves a mixed-gas representation and a source-activity bound. Its convergence/normalized-ratio consumer is being independently developed by audit_scalar_return_acquisition. It is not itself a completed lifetime theorem.

## 1. Reference and elementary perturbation labels

In the exact bounded-depth dressed frame,

 H_ref = direct_sum_s I_L tensor H_a(s) + H_B0,

where H_a has the audited native signed clock paths, and H_B0 is an onsite bounded-spin bath Hamiltonian. Diagonalize each onsite bath term and shift its minimum to zero; this only changes partition normalization.

Conjugate each generic finite-range perturbation by the fixed native U. Expand it into a finite sum

 V = sum_lambda c_lambda E_lambda tensor M_lambda,

where E_lambda is a physical data Pauli (including I), M_lambda is a tensor product of clock and bath matrix units on a bounded set, and sum of coefficient magnitudes per physical local term is bounded by a volume-independent constant times its norm. Complex c_lambda and non-Hermitian matrix units are allowed; only the sum V must be Hermitian. Remove scalar-identity labels first, as they contribute only an overall energy/partition-function constant. Every retained label then has a nonempty marked support. Sources sharing an elementary label are always incompatible (also implied by nonempty marked overlap). Bounded local dimension and the constant-depth circuit make this coefficient overhead, range, support, and overlap degree uniform. Write lambda for one elementary label and epsilon_d for an upper bound on |c_lambda| after incorporating this overhead.

For each lambda mark:
- its actual data support D_lambda;
- its bath support B_lambda;
- every clock explicitly acted on by M_lambda;
- EVERY check g whose support meets the expanded data support D_lambda (in particular, every check anticommuting with E_lambda).

The last two sets form C_lambda, the marked clock columns. This deliberately conservative definition includes commuting checks that meet the data support; bounded check incidence keeps its overhead constant. Each mark has bounded size, <=b. Make the label-overlap graph by intersection of any marked data/bath/clock sets. No additional optional edges are used: compatibility is exactly disjointness of these marked sets, ensuring the used-label connected-component decomposition is unique. No clock-neighbor adjacency is needed in this hard-core graph: neighboring disjoint columns interact by the native pair signs instead.

## 2. Unique compound sources

For a full finite Dyson history, take the set of elementary V labels USED at least once. Partition this set into connected components in the marked-overlap graph. Each component Gamma is a compound source. It contains:
- a connected set A_Gamma of m distinct labels;
- a positive number k_lambda of uses of every lambda in A_Gamma;
- all their times and matrix-unit transitions;
- the COMPLETE clock trajectories on C_Gamma=union C_lambda, including every native t hop and the initial clock states;
- the onsite bath paths on B_Gamma=union B_lambda.

All marked columns are full imaginary-time columns of circumference beta, even when the perturbation acts once. Compatible compound sources have disjoint marked data, bath, and clock sets. Native histories on unmarked clocks are split into the original ordinary/wrap rods. No ordinary rod is also retained on a source-owned column.

This is a bijection up to null coincident-time sets: from a full history the USED-label components and source paths are unique; conversely sort all source-insertion times and native-hop times and glue each clock path. Source sources are unordered with 1/k! convention; labels inside each source retain identity. Interleavings are reconstructed by sorting, not counted a second time. The same original fixed-origin trace convention applies to source-owned periodic clock paths, including never-zero paths.

## 3. Independent syndrome closure of compatible sources

Project the Gibbs operator onto initial/final data syndrome s. Every native dressed hop contains only identity or S_g, so only the V Pauli labels change syndrome. The total V product must have zero syndrome for this diagonal block.

Different compatible sources have DISJOINT sets of affected checks, because all meeting checks, hence all affected checks, were included in C_lambda. Consequently a nonzero syndrome created by one source cannot be canceled by another. Each source's total chronological Pauli product E_Gamma separately commutes with every check.

If a native S_g inside one source anticommutes with a V Pauli in a second source, g belongs to both marked-column sets, contradicting compatibility. Thus native data factors inside one source commute with every other source's V word. Data supports of different compatible sources are disjoint. Their Pauli labels commute, allowing data words to be grouped by source without extra cross-source phases. If |D_Gamma|<d, code distance implies E_Gamma is a stabilizer up to a Pauli phase. Therefore it acts on P_s as the scalar chi_Gamma(s), of modulus one. The existing polynomial filling theorem controls the syndrome neighborhood on which that scalar depends. This filling neighborhood is NOT added to C_Gamma: it is a dependence neighborhood of an activity, not a physical trajectory interaction support.

For large sources retain E_Gamma as a logical operator of norm one. Full-space trace or matrix estimates can be taken afterward. Bath-only sources have E_Gamma=I regardless of size and never require a distance cutoff.

## 4. Every remaining interaction is a scalar pair factor

On an UNMARKED clock g, no V matrix unit acts and every E_lambda commutes with S_g. Therefore its flux is the constant initial s_g for the whole time circle. Its trajectory splits into exactly the audited native rods with their original single-rod flux factors.

On a source-owned clock, flux may change in time when a source Pauli flips that check. All such changes are internal to the SAME source, because no other compatible source affects that check. Native closing-hop flux factors and all data reorder signs are included in the source's internal measure.

The remaining native hopping signs are precisely the previously proved pairwise clock-trajectory signs. Group them as:
- rod–rod signs for unmarked clocks;
- source–rod signs, multiplying all native pair contributions between the complete source clock paths and the given outside rod;
- source–source signs, multiplying all native pair contributions between their complete clock paths.

Each is +/-1. Forbidden overlaps give zero: an outside rod cannot occupy a source-owned column, and sources cannot have intersecting marked sets. The product of all native pair signs is unchanged by grouping. Thus every pair factor h is in {0,+1,-1}, with |h|<=1 and |h-1|<=2.

Arbitrary matrix-unit coefficients introduce NO extra outside dependence: every clock/bath argument of M_lambda is marked by definition. Their coefficients and internal transition constraints stay in the source measure. The representation is therefore an exact continuum complex-measure gas with the SAME modulus-one pair-factor structure as the original rod gas, augmented by compound source objects. No matrix-valued connected cumulant is needed for small closed sources; their data word has already reduced to a scalar. Large sources can be handled as bounded logical operator insertions in the scalar background.

## 5. Absolute activity bound: all beta*t allowed

Let source Gamma use m distinct labels, with c=|C_Gamma|<=b_c m and h=|B_Gamma|<=b_B m. Fix all V insertion times and counts. Drop all clock-pair signs, all flux signs, and the nonnegative clock penalties. The positive native hopping matrix on each K-cycle has norm at most 2t. Each prescribed tensor matrix unit has norm one. Schatten/operator norm bounds on the resulting positive path sum give

 total absolute clock path weight <= K^c exp(2 beta t c).

This remains true with arbitrarily many matrix-unit insertions: the time gaps sum to beta and their norm-one factors do not multiply the bound by K per insertion. For onsite baths shifted nonnegative, the corresponding bound is d_B^h. Dividing by the unmarked product bath partition functions does not worsen this because each onsite partition function is >=1.

For fixed repetition counts k_lambda>=1, summing all time orders and integrating gives beta^(sum k_lambda)/product k_lambda!, including all interleavings exactly once. Hence

 integral |z_Gamma| over histories with this distinct label set
 <= K^c d_B^h exp(2 beta t c)
    product_(lambda in A_Gamma) [exp(beta |c_lambda|)-1]
 <= q^m,

 q = K^(b_c) d_B^(b_B) exp(2 beta t b_c)
     [exp(beta epsilon_d)-1].

A bounded number of extra local data/bath states or decomposition conventions is absorbed into q. No bath-volume or total-clock-volume factor occurs. The bound deliberately sacrifices the clock gap Delta inside source columns. At fixed beta,t,dimensions it still tends to zero linearly with epsilon_d. Thus even beta*t>>1 is not a conceptual obstruction: it may demand a fantastically small but FIXED imperfection threshold.

For a label-overlap graph of bounded degree D_V, the number of connected distinct-label sets of size m containing a specified label is at most C_V^(m-1), with C_V depending only on D_V. Their marked column count and number of neighboring possible rod columns are O(m). These are the quantitative inputs needed by the independent mixed-KP analysis.

## 6. Precisely remaining analytic interface

This representation plus the activity bound is not yet the local syndrome-potential estimate. One must apply the mixed-gas cluster theorem with:
- the established rod endpoint/length charges;
- an O(m) charge for a full-time m-label compound source, large enough to pay all rods meeting its O(m) columns during beta;
- sufficiently small fixed q to pay the reverse source contribution seen by each rod and source.

For scalar sources, the resulting rooted influence estimate must count the polynomial filling neighborhood when a syndrome bit is flipped. Large memory-touching sources have m>=d/b_D and must be bounded RELATIVE to the scalar partition function, anchored to O(n) memory labels rather than all bath labels. Scalar bath-only sources remain in the background even when large.

Important distinction: the label-component source is formed BEFORE adding background rod bridges. Its individual syndrome closure holds because affected-check sets are disjoint, even when rods later connect sources in the Mayer expansion. This is why the scalar reduction is valid without demanding all thermally occupied ancillary paths be independent.

## 7. Audit cautions

- Do not forget data/bath supports in the label-overlap graph; affected checks alone do not ensure disjoint Pauli/matrix words.
- Include every check meeting the expanded data support in the full columns; omitting even affected checks would let an outside rod see time-varying flux and invalidate factorization.
- Do not expand a source into separate little time pins and then assume its syndrome closure locally; the full USED-label component is the closed object.
- Do not count filling neighborhoods as physical interaction support: that would introduce unnecessary superlinear source charges.
- Do not remove wrapping paths or insist all source clocks reach zero.
- The absolute activity bound is intentionally weak in beta; no practical hardware constant or zero-temperature-uniform threshold is claimed.
