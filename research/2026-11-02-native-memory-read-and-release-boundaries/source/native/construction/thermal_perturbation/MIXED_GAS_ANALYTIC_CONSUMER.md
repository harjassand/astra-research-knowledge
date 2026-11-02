# Independent mixed-gas convergence, local influence, and exceptional-source consumer

2026-11-02, revision 2 (explicit safe cutoff). This is a proved analytic consumer of the exact compound-source/rod representation. It assumes the source factorization and the q^m activity estimate stated in `../EXACT_MIXED_SOURCE_ROD_FACTORIZATION.md`; their exact compatibility convention must forbid every cross edge used in forming connected USED-label components. It does not use an operator logarithm.

## 1. Fixed admissible majorant

Keep the exact clock model inside a STRICT rod-KP region. In the preceding rod audit one may use

    a_rod(l)=a0+b l,
    a0=64 Dbar (t/Delta)^2, b=32 Dbar t²/Delta,

with a0≤log2, Delta−2t−b≥Delta/2, and charged wrap fugacity at most (t/Delta)^2. Its rod-only KP integral is at most max(1/2,34/64) times a_rod, leaving uniform slack. Any needed fixed per-rod spatial weight is included in Dbar.

Let a source have m distinct V labels, at most b_c m marked clock columns, bounded data/bath support per label, and integrated absolute trajectory measure at reference perturbation strength v0 at most q0^m. The primitive-source label graph has bounded degree. Enlarge an auxiliary LABEL INTERACTION graph to connect labels whose marked supports overlap or whose clock columns are adjacent in the native clock graph. This graph is still bounded degree; it is used for upper bounds, not to alter the exact source partition.

There exist volume-independent constants C_an,B_r,B_s such that:

- connected source-label sets of size k containing a fixed label number at most C_an^(k−1);
- sources interacting with a fixed ordinary/wrap rod can be rooted at at most B_r elementary labels;
- sources interacting with an m-label source can be rooted at at most B_s m elementary labels.

These follow from bounded local dimension, range, density and label incidence. A source with no marked clocks does not interact with rods; its data/bath hard-core interactions are still counted by B_s.

Give each source charge a_src=A m. The rod contribution seen by a source is at most L0 m, where a safe fixed choice is

    L0=b_c D [16 beta t²/Delta + 2 Wcharged],

with the weighted-majorant version if rod activities were inflated. Choose A≥4L0+4. Let alpha>0 be a spare per-label weight. Define

    G(q0)= q0 exp(A+alpha) /
           [1−C_an q0 exp(A+alpha)].

Select the reference perturbation strength v0 so small that the denominator is positive and

    2 B_r G(q0) ≤ a0/4,
    2 B_s G(q0) ≤ A/4.                              (K)

This is possible because the source estimate has q0→0 linearly as v0→0, despite its fixed factors K^(b_c), bath dimensions and exp(2 beta t b_c). Every constant may be extremely unfavorable in beta, but is independent of memory/bath volume.

The mixed KP criterion now holds with slack: a rod sees its old rod integral plus at most a0/4; a source sees at most A m/4 from rods and A m/4 from other sources. The charge and spare exp(alpha m) apply to complete trajectory labels, not to already averaged phases. The complex-measure continuum theorem therefore supplies an exact absolutely convergent scalar logarithm for rods plus all memory-touching sources with m<d/b_D, and arbitrary-size bath-only sources. Here memory-touching includes sources using native data OR clock perturbation labels, including clock-only perturbations whose dressing creates a data Pauli. Every large memory-touching source m≥d/b_D is excluded from the scalar background and treated as exceptional, even when its particular data word happens to be scalar. Large bath-only sources remain allowed and have no data or clock dependence. No source-independent assumption of positive activities is made.

## 2. Why source strengths produce O(v), without differentiating an operator log

For any actual perturbation V of local strength v≤v0, set eta=v/v0 and scale its elementary coefficients up by eta^−1 for a majorant reference of strength v0. Preserve their phases and supports. A concrete source trajectory containing k V events has its activity multiplied by exactly eta^k, with k≥m≥1. Pair factors and all native hopping measures are independent of this scaling.

Consequently every mixed cluster containing at least one source has absolute weight at most eta times its corresponding reference-majorant weight. This remains true with arbitrarily many zero-hop thermal wrap rods. It is a direct monomial comparison of absolutely convergent trajectory integrals, not differentiation of a norm estimate and not a claim of a volume-uniform operator-log Taylor series.

## 3. Local syndrome influence

Each scalar source trajectory has one syndrome-character factor. Its support consists of native closing-hop fluxes on its O(m) columns, together with a chosen actual stabilizer filling of its closed V Pauli word. The accepted polynomial filling theorem gives a dependence footprint F_gamma in a polynomial-radius neighborhood of its data support. The number of candidate elementary source anchors whose m-label footprint can contain a fixed syndrome check is at most C(1+m)^p, for fixed p, times the ordinary connected-label animal count. This uses bounded-density physical geometry. NO expansion into 2^(filling volume) truth-table coefficients occurs: each trajectory is already ONE monomial.

Let Xi(s)=log Z_small(s)−log Z_clock(s), with the known bath product factors canceled. In the mixed cluster series every contribution to Xi contains a source. For a syndrome bit g there are only two ways such a cluster character can depend on g:

(A) g belongs to the footprint of one of its sources. Mark that source. The rooted bound gives

    (1/beta) integral_(source: g in F_gamma) d|nu0|(gamma) exp(A m).

This is uniformly finite by polynomial anchor counting, q0^m and the spare exp(alpha m). Call its uniform bound C_src.

(B) The cluster has a winding ordinary rod on g. Mark that rod. Since the cluster also contains a source, it has at least two polymers. The rooted bound after deleting the singleton is exp(a_rod)−1. Thus its majorant is at most

    C_wind := integral_0^beta A_w(l)[exp(a0+b l)−1] dl,

where A_w is the exact winding density from the rod audit. Its start-time integral beta cancels the free-energy factor. This is finite and volume independent. It is harmless to overcount source-free multi-rod clusters at the reference majorant when bounding this subset; the factor eta was already established for the actual selected mixed clusters.

Hence, for any two valid syndromes differing on a set T,

    | Re Xi(s) − Re Xi(s') |
       ≤ 2 beta eta (C_src+C_wind) |T|.              (I)

The same bound holds for the absolute complex logarithm difference. Triangle inequalities and marking can overcount but do not miss a character that changes. This establishes O(v) local influence, not an extensive O(nv) error. Pure-clock clusters give the previously earned F_beta(s); pure-bath far-away clusters cancel from Xi differences.

## 4. Large logical sources and positive actual weights

Every retained memory-touching source has m<d/b_D, so its closed V data word has support below d and is a stabilizer. We declare ALL memory-touching sources with m≥d/b_D exceptional, including accidentally scalar ones; no locality assertion about a large stabilizer word is needed. Repeated use of a fixed local label does not evade the support bound b_D m because m counts DISTINCT labels. Background clock rods and their bridges are stabilizers and do not enlarge the support of the V word. This conservative cutoff may overcount harmless exceptions but preserves the estimate below.

Use the separately proved pinned signed-gas ratio lemma. The mixed KP bounds are valid for any source as a test root, including every excluded large memory-touching source, so its external pin cost is at most A m. Such a closed source is represented by its bounded logical operator, whether scalar or not. Expand the full projected Gibbs operator by its set of exceptional sources. The relative matrix remainder is bounded by

    r_n ≤ exp[R_n]−1,
    R_n ≤ C n sum_(m≥d/b_D) C_an^m q(v)^m exp(A m)
        ≤ C' n lambda^(d/b_D),                     (E)

for lambda<1 after reducing v0 if necessary. Scalar bath-only sources of any size stay in the background. Exceptional sources are anchored to a native data OR CLOCK perturbation label: clock-only native noise can acquire a data Pauli after the dressing. There are O(n) such anchors. Bath-only labels need not be counted by total bath volume; they are counted only within connected animals attached to a memory/clock anchor.

Actual projected Gibbs traces W(s) are positive. With the one-logical-qubit multiplicity, the norm remainder implies |W(s)/(2 Z_small(s))−1|≤r_n, after canceling the common bath normalization. Therefore 2|Z_small(s)|(1−r_n)≤W(s)≤2|Z_small(s)|(1+r_n). We use Re log Z_small=log|Z_small|; no separate positivity of the signed truncated scalar partition function is assumed. For r_n≤1/2, the two-syndrome logarithmic correction is bounded by log[(1+r_n)/(1−r_n)]≤4r_n. This is a multiplicative witness-ratio correction, not an additive r_n contribution to the bad-syndrome probability. The bound is uniform in s and in bath volume.

Combining (I), (E), and the exact clock free-energy influence gives the positive witness comparison with only a small O(v) loss of tension and a vanishing multiplicative large-source correction. The previously earned syndrome-translation/shrunken-stable-set arguments can then be applied to the dressed local operator support.

## 5. Exact boundary of this consumer

The result depends on the EXACT compound-source factorization, including independent syndrome closure and scalar modulus-at-most-one pair factors. It cannot be applied to pointlike V pins that ignore the syndrome-defect interval. It also assumes finite fixed beta, bounded local dimensions/density/range, and sufficiently small fixed perturbation strength. The source activity estimate charges all unrestricted clock/bath trajectories and decomposition overheads.

The logical-twirl/physical-time consumer remains a separate join: the reference native Hamiltonian must commute with the chosen decoded logical algebra, and actual local perturbations must commute with it on the admitted good sector. Nothing here replaces that condition with mere geometric locality. This construction is not an operator-log locality theorem, an arbitrary-time-dependent-noise theorem, or an efficient physical loader.

## Revision record

Revision 1 is preserved as `MIXED_GAS_ANALYTIC_CONSUMER_V1.md`, SHA256 `3077290b18531e15c9cf10ee4afe18c8e611db56cfe788c8a7a0e38a840c0654`. Revision 2 explicitly retains only memory-touching sources below the distance cutoff plus arbitrary-size bath-only sources in the scalar background. All large memory-touching sources are exceptional, irrespective of accidental scalarity. It also spells out the positive actual W(s) ratio through Re log Z_small. No KP constants, activity estimates, or physical hypotheses change. This revision supersedes any broader scalar-background classification in the companion structural receipt.
