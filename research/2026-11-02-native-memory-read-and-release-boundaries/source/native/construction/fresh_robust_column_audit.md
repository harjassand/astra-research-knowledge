# Fresh adversarial audit: full-column perturbation construction

2026-11-02. Independent algebraic/combinatorial audit of `ROOT_FULL_COLUMN_CONSTRUCTION.md`, `EXACT_MIXED_SOURCE_ROD_FACTORIZATION.md`, `thermal_perturbation/PINNED_SIGNED_GAS_RATIO_LEMMA.md`, and `native_history_holder_lemma.md`. This is not an assumption of generic operator-log analyticity. The preceding native thermal closure is used only for its explicit scalar rod gas and KP bounds.

## Current verdict

**The exact mixed-column representation and the primitive activity estimate survive independent review, subject to the explicit compatibility repair below.** The pin-ratio lemma is valid for a genuinely scalar background. These facts do not alone prove the mixed KP criterion, local syndrome influence, or final perturbed Gibbs witness theorem. Those analytic steps must be stated and checked separately before announcing robust native memory.

A small but real definition issue: two sources sharing an elementary perturbation label must ALWAYS be incompatible, even when that label has empty marked support. Alternatively, remove pure scalar identity perturbations into a constant before expansion. Compatibility based only on intersection of actual marked sets misses empty-support identity labels; then the same used label can appear in several singleton sources and the claimed history bijection is false. For nonempty marked supports, this exclusion is already automatic. The constructor and root were notified promptly.

## 1. Exact assumptions required

- The native reference has the already-audited exact controlled-Pauli dressing and full-spectrum rod representation.
- The perturbation is a sum of bounded-support, bounded-range terms with a uniform local coefficient budget. After the fixed-depth dressing, the Pauli/matrix-unit expansion has fixed support size, dimension overhead, and bounded incidence. Arbitrarily many uncharged labels per site are not permitted; identical local supports can be regrouped before choosing elementary labels.
- All clocks explicitly acted on by an insertion are marked. All checks ANTICOMMUTING with its data Pauli are marked as clock columns. Data-support and bath-support overlap also join label components. Marking every check meeting the data support is a sufficient but unnecessary enlargement.
- Bath reference terms are onsite, finite-dimensional, and uniformly bounded. Their eigenbases define the worldlines. Bath density and interaction incidence are bounded, and finite bath volume is arbitrary. A genuinely interacting unexpanded bath reference would not satisfy the stated factorization.
- The code has an exact distance d, and its separately established polynomial stabilizer-filling statement applies to the connected support geometry of these sources. Distance alone does not give local syndrome dependence.
- Temperature and native couplings are fixed independently of volume. The eventual perturbation threshold may be extremely small in these fixed parameters; no positive threshold uniform as beta tends to infinity is claimed.

## 2. Why noncommuting Pauli words do not defeat source closure

Only V insertions change data syndrome; native closing hops contribute stabilizers. Every check affected by an insertion is an owned clock column. Compatible sources have disjoint owned clock sets, hence disjoint affected-check sets. Thus a globally closed diagonal-syndrome history necessarily has EACH source's net V word in the centralizer. Nonzero syndrome from one source cannot cancel against another.

Data supports of compatible sources are disjoint, so their V words commute term by term. A native stabilizer hop on a source-owned clock can anticommute with another source's V factor only if that other source also owns this check column, contradicting compatibility. Native stabilizers on exterior clocks commute with every V insertion by the same argument. Consequently regrouping data factors by source produces no unrecorded cross-source Pauli sign.

Inside a source, arbitrary ordering and complex Pauli phases are retained. Native stabilizer factors can be moved through its V factors with scalar signs charged internally. Its logical class is therefore that of the V product E_Gamma. Repetition of a label does not enlarge the UNION of its data supports. With m distinct labels this union has size at most b_D m; if b_D m<d, centralizer membership implies E_Gamma is a stabilizer up to phase. The activity is then a scalar on each logical sector. No assumption that individual V insertions commute was used.

Large sources retain logical operators rather than being scalarized. Compatible closed source words commute as physical operators, hence also as logical operators. There is no conflict between this statement and the existence of anticommuting logical Paulis: disjoint physical representatives cannot anticommute.

## 3. Arbitrary clock matrix units and pair factorization

A matrix unit may jump a clock between any two levels; it need not follow a native cycle edge. Since every such clock is owned for the entire circle, that jump is wholly internal. All native hops and all initial/final clock states on owned columns are summed there. No exterior excursion is allowed on an owned column. Thus a matrix unit does not cut an unowned rod or require an uncharged external boundary condition.

The native gauge sign at each native hop remains a product of two-clock signs, evaluated on the actual instantaneous states even in histories containing non-native jumps. Assigning each clock's complete trajectory to either a source or exterior rods groups these signs into symmetric source-source, source-rod and rod-rod factors. Cross-source V data phases were already excluded above. Scalar pair factors have modulus one, except forbidden configurations with factor zero. Their support is fixed by adjacent native clock columns or hard-core marked-set overlap, not by the possibly larger stabilizer-filling region.

The latter distinction is essential: a filling region records syndrome dependence of a scalar activity, not an additional physical interaction between trajectories. Adding that region to the hard-core support can destroy the intended linear source charge and is neither needed nor justified.

## 4. Bijection, time ordering, and normalization

A history with labelled V terms fixes the set of elementary labels used at least once. Its components are unique once the overlap graph and compatibility convention are fixed. Owned trajectories are full periodic paths with a fixed time origin. The exterior uses the established ordinary/wrap rod convention. Sorting all event times reconstructs the history uniquely outside null simultaneous-event sets.

For fixed repetition counts k_lambda>=1, the sum over chronological orders and their ordered simplexes has measure

    beta^(sum_lambda k_lambda)/product_lambda k_lambda!.

There is no extra factorial from clock-hop interleavings: these are already in the clock path propagation. There is also no second factor for source interleavings after their times have been assigned. The gas 1/N! only quotients the arbitrary ordering of its N source/rod objects. The special exclusion of shared labels prevents the USED-label decomposition from being represented more than once.

Onsite bath partition factors can be normalized sitewise. An owned bath site's trace is divided by its own unperturbed partition factor; untouched bath sites cancel globally. Shifting each onsite minimum to zero makes these denominators at least one. Therefore neither a bath-volume factor nor an arbitrary clock-vacuum probability enters.

## 5. Primitive activity bound independently checked

Fix an animal of m distinct elementary labels and all their insertion times. After taking absolute values, remove the positive clock penalties and all scalar signs. Matrix-unit entries are nonnegative and have operator norm one. The resulting clock path sum is bounded by the trace norm estimate on the K^c-dimensional owned space:

    K^c exp(2 beta t c),

where c is its number of owned clocks. This is valid with arbitrarily many prescribed matrix-unit insertions; each time gap contributes its share of beta, not a separate beta. The analogous onsite bath bound is d_B^h after shifting energies nonnegative. Summing repetitions gives

    integral |z_A| <= K^c d_B^h exp(2 beta t c)
                      product_(lambda in A)(exp(beta|c_lambda|)-1).

For c<=b_c m, h<=b_B m and bounded elementary coefficient magnitudes, this is q^m with the constructor's q. The local coefficient expansion overhead is fixed. In particular q tends to zero with perturbation strength at every fixed beta,t. Huge beta*t makes the sufficient threshold poor but introduces no volume dependence.

A bound of this kind is not yet a normalized thermodynamic statement. Summing every disconnected animal without cancellation would produce an extensive exponential and would not prove witness stability.

## 6. Scalar pin-ratio lemma independently checked

For fixed scalar pin factors k with |k|<=1, the interpolation k_u=(1-u)+uk remains in the unit disk. Hence the perturbed activity is dominated by the same absolute measure and obeys the same KP bound. Differentiating the absolutely convergent cluster series with respect to the measure produces one marked root with weight mu(k-1), not a division by k_u. The rooted estimate bounds its derivative by integral |mu||k-1| exp(a). Integrating and adding pins proves the two-sided modulus ratio in the receipt. Zeros of an individual activity factor cause no singularity, and the scalar partition functions stay nonzero by the cluster theorem.

For full-time clock columns, only O(|C|) neighboring clock species contribute to this root cost. Their ordinary start integration is beta, not total volume. The stated bound 16 beta t^2/Delta plus twice the charged wrap activity per affected clock is conservative and correct.

The large-column operator remainder can be bounded by expanding the SET of large columns first, pinning the scalar background, applying this ratio bound and bounding operator products by products of norms. This avoids any matrix logarithm. However the scalar mixed background, including all small columns, must first have its own KP bound. Applying the rod-only criterion while silently ignoring small-source response would be invalid.

## 7. Bath-volume and exceptional-source anchoring

A nonscalar source must have enough memory-supporting distinct labels to allow a centralizer word of weight at least d. In particular its total label count is at least d/b_D and it contains a memory-touching label. Anchor connected-label counting at such a label. Under bounded density and range there are O(n) possible memory anchors, regardless of total bath volume. Bounded-degree connected-set counting then gives a tail of the form C n lambda^(d/b_D) once the charged activity is small enough.

Bath-only sources have E_Gamma=I for every size and remain scalar. They must stay in the background rather than being declared large exceptional sources merely because they have many bath labels. Pure clock sources can likewise remain scalar. Allowing arbitrarily large uncharged local bath dimensions, degrees, or numbers of contacts would invalidate this volume-independent counting premise.

For positive projected Gibbs weights W_s, a uniform operator comparison ||W_s/Z_small(s)-I||<=r<1 implies scalar trace comparisons within (1-r)|Z_small(s)| and (1+r)|Z_small(s)|. This produces multiplicative witness-ratio control, not an additive probability floor. Z_small need not be separately asserted positive. Establishing a sufficiently small r uniformly over all system sizes is still a quantitative tail condition.

## 8. Remaining analytic checks before full closure

1. Simultaneous source/rod KP, including source-source gauge-neighbor interactions as well as marked-overlap hard core.
2. Both contributions to syndrome influence: source activities whose stabilizer filling reaches the flipped bit, AND winding rods at that bit in source-containing connected clusters. The latter can be far from the original source and cannot be omitted.
3. Polynomial filling must enter only as a polynomial root-count/dependence factor, not an exponential of its volume.
4. The large-source pin cost must include response of the scalar SOURCES as well as rods.
5. The actual perturbed Gibbs diagonal weights must then be passed through the existing fixed-witness deletion and bounded-contact good-set enlargement. No generic operator-log analyticity or extensive partition-function comparison substitutes for these steps.

The exact-H logical-twirl/equilibrium-overwrite consumer is a separate supplied result. Its use here would still require the actual joint-Gibbs bound and its ideal correlated endpoint assumptions. This audit does not replace it with a discontinuous fully secular Davies argument or claim generic physical preparation/readout.

## 9. Verified correction and frozen representation binding

The constructor corrected the empty-support/shared-label issue before freezing `EXACT_MIXED_SOURCE_ROD_FACTORIZATION.md` at SHA256 `d6c5c78066af317d3c3e75fcdff64c3a9f6d77446c348140c23cbc8702d8f238`. I re-read the corrected definitions and verified this hash. The compatibility defect recorded above is therefore **resolved in that version**, not a remaining gap.

The corrected version additionally marks every check meeting the expanded data support (a safe conservative enlargement), and removes optional edges from the source-component graph. The latter is important: any edge used to merge USED-label components must also forbid two separated source objects joined by that edge; otherwise the purported bijection permits an extra decomposition. With the frozen graph defined exactly by marked-set overlap and compatibility by its negation, this consistency holds. The scalar auditor independently identified that optional-edge issue.

**Bound verdict for the frozen representation: PASS for the exact mixed-gas representation and primitive integrated activity bound under the stated assumptions.** The separate simultaneous-KP and local-influence gates listed in Section 8 remain to be independently checked when their receipt is available. No full robust-memory theorem is certified by this bound verdict alone.

## 10. Independent review of the mixed analytic consumer

I reviewed `thermal_perturbation/MIXED_GAS_ANALYTIC_CONSUMER.md` after the representation verdict. Its simultaneous-KP construction, source-strength comparison, two kinds of influence marking, and normalized exceptional-source estimate are mathematically sound, with the classification clarification below.

### KP constants and pointwise validity

The rod-only bound is at most (34/64)a_rod, since its length coefficient is at most one half of the chosen length charge. Adding source response <=a0/4 leaves slack for every ordinary duration, including the limit l down to zero, and for full-circle wrap roots. A source sees rods at cost L0 m<=A m/4 and other sources at cost <=A m/4. Counting potentially interacting sources through the enlarged label interaction graph is legitimate because that graph is only a counting majorant, not an alternative definition of compatible configurations. Bounded label incidence is indispensable here.

The integrated q0^m bound suffices to verify the criterion pointwise in a root trajectory: its interaction support is bounded by its marked columns and labels, independently of its detailed internal path and event count. Inflating every source by exp(alpha m) leaves an explicit summability margin for later polynomial factors.

### The O(v) influence bound does not hide an operator analyticity assumption

Scale elementary coefficients from v to an admissible reference v0. At the level of a fixed trajectory, the factor is exactly eta^k, with eta=v/v0 and k its number of V events. Each cluster contributing to Xi has k>=1, including clusters with only one source and arbitrary rod bridges. Absolute summability at v0 allows this direct comparison before regrouping trajectories.

If a character changes at g, either a source dependence footprint contains g or some winding rod on g occurs. Marking the former uses the rooted e^(Am) estimate and polynomial anchor counting. Marking the latter uses the rooted multi-object e^(a_rod)-1 estimate because a source-containing winding-rod cluster has at least two objects. The eta factor applies to the selected source-containing subset BEFORE replacing that subset by all multi-object rooted clusters at v0. Hence overcounting source-free reference clusters does not invalidate the O(v) factor. I independently checked this order of operations; it avoids an otherwise plausible but incorrect differentiation of a norm bound.

The 1/beta factor and root start-time integral are handled correctly. Arbitrarily many clock wraps and repeated source insertions remain covered. This is a local influence estimate, not a globally extensive estimate.

### Normalized exceptional-source estimate

The same KP criterion applies to a large source as a test pin even when it is excluded from the scalar background. Its pin cost includes BOTH rod and scalar-source response and is bounded by A m. Anchoring its connected label set at a memory/clock label gives O(n), not total bath-volume, possible roots. The minimum size d/b_D and charged geometric-series tail then give R_n<=C n lambda^(d/b_D). To infer a vanishing remainder, the actual family must supply its stated growing distance, sufficient to dominate log n; the stronger polynomial distance bound used by this construction suffices.

Expanding large sources first and using the scalar pin ratio proves an operator remainder relative to Z_small. No logarithm of an operator-valued partition function is taken. Actual projected Gibbs traces are positive, so the 1±r_n modulus comparisons give an ordinary positive probability-ratio comparison. For r_n<=1/2 the additive correction to a two-weight logarithmic ratio is bounded by 4r_n. This term does not become an additive floor in bad-event probability: the witness injection is charged multiplicatively.

### Required classification clarification

The receipt's phrase 'all SCALAR sources' needs a precise cutoff convention if the earned filling theorem only guarantees local filling for small centralizer words. A safe convention is:

- keep sources with b_D m<d in the scalar background;
- also keep sources of any size whose V data word is the identity up to phase (their remaining flux dependence is only on their owned columns), including genuine bath-only sources;
- place every other source with b_D m>=d in the exceptional set, even if its word happens to be a stabilizer rather than a nontrivial logical.

All exceptional sources then still have the size and memory-anchor properties used in the tail. This conservative convention removes any need to assert local filling for an arbitrary large stabilizer. Alternatively the stronger all-size filling theorem must be stated and justified explicitly. I reported this clarification to both the scalar auditor and root before certifying the combined static gate.

## 11. Independent audit of the actual-Gibbs and physical-time join

I reviewed `ROOT_ROBUST_NATIVE_MEMORY_JOIN.md` and the exact finite-bath consumer in `bath_gate/SECULAR_TEST_AND_POSITIVE_CONSUMERS.md`. The static-to-dynamic join is valid under the explicit actual-code witness/filling premises and endpoint assumptions, once the scalar cutoff clarification in Section 10 is implemented.

### Positive Gibbs weights to the original decoder

The scalar gas controls diagonal syndrome weights of the ACTUAL perturbed Gibbs operator; it does not claim that this Gibbs state is block diagonal in syndrome. Off-diagonal coherences do not enter the expectation of a syndrome projector. The small-source log influence and 1±r_n comparisons yield the displayed positive-weight ratio with error Lambda_beta(v)|D|+4r_n. For fixed witness tau, the original valid-syndrome translation is injective and deletes exactly its occupied checks. Its probability bound acquires a reduced tension and the fixed factor exp(4r_n). This factor is not repeated once per volume or per defect. It does not create a probability floor.

Conditioning on the other CSS syndrome is still legitimate because the allowed syndrome set is an algebraic product even though its weights are not independent. Enlarging the bad event by all bounded-weight Pauli prefixes changes its probability only by a fixed polynomial and fixed ratio constants. It uses the original decoder, not a V-dependent replacement decoder. Consequently arbitrary bath matrix coefficients and all actual dressed local data operators are protected on this same good subspace.

### Logical twirl and physical time, checked directly

Let rho be the actual total Gibbs state and Q one of its reference decoder logical Paulis. The reference H_ref commutes with Q. Each actual Hermitian memory-touching interaction has [Q,V_j]P_good=0. Anti-Hermiticity and [Q,P_good]=0 imply both [Q,H] and QHQ-H have two-sided bad support. Their norms are at most 2vn, with no pure-bath terms charged.

The exact Gibbs identity gives

    D(rho || Q rho Q) = beta Tr rho(QHQ-H) <=2 beta v n p.

Pinsker and convexity of the logical twirl yield

    ||rho_bar-rho||_1 <=2 sqrt(beta v n p),
    rho_bar=I_L/2 tensor Tr_L rho.

This proof neither assumes [H,P_bad]=0 nor that the perturbed Hamiltonian is logically degenerate. It only uses bad-supported logical commutators and the actual small Gibbs probability.

Replacing the decoded logical factor by an arbitrary reference-entangled input retains the actual joint gauge/clock/bath marginal. The system marginal is bounded by 2rho_bar. Exact unitary evolution with the SAME H fixes rho and preserves this operator domination. Using the equal-trace effect bound gives, for all physical times,

    p_bad(t)<=2p+||rho_bar-rho||_1.

For each logical Pauli, reference trace-norm duality bounds the derivative coefficient by 2vn p_bad(t). The Pauli expansion of a qubit channel has three such coefficients, so integration gives

    error(T)<=6vnT[2p+2sqrt(beta v n p)].

Thus the constants quoted in the root join are conservative and correct. The stretched-exponential error scale survives the square root after reducing the allowed storage exponent. There is no finite-order simulation error multiplied by T, no bath mixing requirement, and no secular or weak-coupling time rescaling.

### Resource and endpoint boundary

All bath-bath interactions in the STATIC theorem must be small expanded terms in V; only bounded onsite bath terms may remain in H_B0. The dynamic argument alone is broader, but it cannot enlarge the static bath class for free. Finite bath volume is arbitrary under bounded density/dimension/range/incidence. The norm budget vn covers only actual terms touching native memory, including clocks. This is consistent with the O(n) exceptional-source anchoring.

A compact finite beta interval with strict original margins permits a common positive perturbation threshold: all explicitly charged constants can be bounded over that interval and v chosen below the resulting fixed minimum. This is not a threshold uniform to zero temperature.

Initialization is an ideal overwrite of the decoded logical subsystem of the ACTUAL interacting equilibrium state. It retains gauge/clock/bath correlations. The operation uses the fixed U and decoder, not knowledge of V; it does not require manipulating the external bath directly once the actual equilibrium state exists. However supplying that equilibrium state, executing the decoder/overwrite, and terminal decoding with clock access remain ideal endpoint resources. Product-bath initialization, arbitrary nonequilibrium input noise, or noisy/efficient preparation is not established.

The result is an open-region exact finite-spin Hamiltonian statement with fixed qudit hardware. It is not a bosonic-reservoir theorem, qubit-only two-body construction, practical tolerance claim, or historical novelty certification.

## 12. Final bound verdict and resolved cutoff

I verified revision 2 of `thermal_perturbation/MIXED_GAS_ANALYTIC_CONSUMER.md`, SHA256 `160cf7c1f0fe86bea69db1c0447ac6b135687bb48af458d11781672c21d33bda`. It explicitly uses the conservative cutoff: only memory-touching sources below d/b_D and arbitrary-size genuinely bath-only sources remain in the scalar background; ALL large memory-touching sources are exceptional, even accidentally scalar ones. This resolves the classification issue in Section 10. Its explicit one-qubit multiplicity, positive W(s) comparison through |Z_small|, and multiplicative 4r_n correction are correct. No new assumption about arbitrary large stabilizer filling is needed.

**FINAL VERDICT: PASS for the integrated robust-native static Gibbs estimate and exact finite-spin physical-time retention statement, under the exact assumptions enumerated in this audit and the root join. No unresolved mathematical gap was found in the audited component interfaces.** This is an internal independent audit, not a historical novelty claim or external peer-review certification. The underlying actual-code witness and polynomial filling theorems remain stated inputs; this audit checks their use rather than redoing the entire code construction.

Bindings:

- Exact source representation/activity: `EXACT_MIXED_SOURCE_ROD_FACTORIZATION.md`, SHA256 `d6c5c78066af317d3c3e75fcdff64c3a9f6d77446c348140c23cbc8702d8f238`.
- Mixed analytic consumer revision 2: SHA256 `160cf7c1f0fe86bea69db1c0447ac6b135687bb48af458d11781672c21d33bda`.
- Integrated root join reviewed: `ROOT_ROBUST_NATIVE_MEMORY_JOIN.md`, SHA256 `d833625e8a392a291071499b3d32d8f52161aeb12754a430ad9f5429f79eda8c`.

The root join may replace its audit-pending status by internally reviewed and explicitly spell out the safe cutoff without changing the mathematics certified here. Any stronger bath, endpoint, hardware, temperature-uniformity, or novelty claim is outside this verdict. In particular all bath interactions beyond the onsite reference must remain in the sufficiently small V, the initial state must be the actual joint Gibbs equilibrium before ideal logical overwrite, and the SAME total Hamiltonian must govern physical-time storage.
