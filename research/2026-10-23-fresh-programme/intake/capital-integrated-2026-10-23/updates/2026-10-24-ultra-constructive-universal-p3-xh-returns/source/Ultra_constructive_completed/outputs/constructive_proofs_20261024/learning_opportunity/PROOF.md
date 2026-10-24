# Acquiring nonlinear coordinates and the experiments for learning the next coordinate

24 October 2026. Internally derived theorem candidate. This is a complete written argument in the stated finite oracle model, with finite executable checks; independent external correctness and historical priority remain unknown.

The independent first question/construction is preserved verbatim in `FIRST_CONSTRUCTION.md`. The present argument incorporates the exact feasible-core cardinality and finite-grid corrections found independently by root and the bounded Luna checks. Four existing supports were used; none supplied the initial mechanism. No work from the fresh physical/material arm was read.

## 1. Contract and result

Write V=F₂ⁿ. An unknown bijection Q:V→V determines the oracle

    C(x,y) = 1{Q(x) <lex Q(y)}.

Q₁ is the most significant output bit. Each actual Qᵢ has Boolean algebraic degree at most two. The learner is supplied n and this quadratic-permutation promise, and receives exact chosen-pair comparisons. It does not receive Q, rank labels, output bit labels, a hidden basis, target code, significance flag, a fibre sampler or the rank/core size below. Raw input vectors and exact XOR/finite-field operations are available and charged. Equal submitted inputs are locally recognizable.

For a quadratic f define its polar form

    B_f(x,v)=f(x+v)+f(x)+f(v)+f(0).

This is an alternating bilinear form. For Fₜ=(Q₁,…,Qₜ), let

    Lₜ = intersection_(i≤t) rad B_Qᵢ,
    rₜ = n−dim Lₜ,              b(Q)=rₙ.

L₀=V, r₀=0. The computed rₜ are nondecreasing and bounded by b(Q); b(Q) is an **a posteriori complexity parameter**. It need not be supplied or cheaply certified from the unknown comparator.

**Theorem 1 (comparison-only quadratic acquisition).** For 0<δ<1, a randomized learner returns the exact Q₁,…,Qₙ on every input with probability at least 1−δ. It then compiles exact rank evaluation, inverse rank, and exact uniform sampling from every rank-prefix fibre, with zero further comparisons. Let

    Dₙ=1+n+binom(n,2),
    R=the least odd integer at least 8 ln(n Dₙ/δ).

A fresh-median implementation uses at most

    32,200 n Dₙ R

logical comparisons. With probability at least 1−δ, correctness and a classical computation bound of 2^b(Q) times a polynomial in n and log(1/δ) hold simultaneously, in addition to the declared source/comparator costs. The same successful branch has acquired raw ANF storage nDₙ coefficient bits; prefix-sampler tables use O(n2^b(Q)) numerical bits plus polynomial linear-algebra state. These are logical payloads, not allocator measurements. A compact final affine/core decoder has O(n²+n2^b(Q)) numerical bits before optional inverse preprocessing.

No polynomial bound in arbitrary b(Q) is asserted. On an erroneous acquired prefix, its computed radical can have codimension n even when true b(Q) is small. Thus the cap-n executable has an all-branch 2^n poly(n,log(1/δ)) bound, not an unconditional expected bound in true b(Q). A smaller acquired-rank or memory/time cap may stop with UNKNOWN before materializing a large core. Passing finite balance checks is not a proof of the quadratic-permutation promise. The confidence concerns the acquisition algorithm under that promise, not recognition of arbitrary orders.

## 2. Exact prefix preparation from acquired coordinates

Suppose the first t polynomials have already been acquired correctly. All objects in this section can now be computed from them alone. Form the stacked polar matrices, find their common nullspace L=Lₜ, and choose a linear complement x=Rz+v, where z∈F₂ʳ, v∈L and r=rₜ. Put

    A(v)=Fₜ(v)+Fₜ(0),   v∈L;       s=rank A.

For v,w∈L, polar vanishing gives A(v+w)=A(v)+A(w), so A is linear. For arbitrary z,v,

    Fₜ(Rz+v)=Fₜ(Rz)+A(v).                         (1)

Thus a specified prefix y is attained in core z precisely when the linear equation

    A(v)=y+Fₜ(Rz)                                  (2)

is consistent. Every feasible z contributes exactly 2^(n−r−s) points, a coset of ker A. Different z contribute disjoint inputs. Since Q is bijective, a t-bit prefix has exactly 2^(n−t) preimages. Therefore

    number of feasible z = 2^(r+s−t).              (3)

In particular this number is a power of two. Enumerate the 2ʳ core values, retain the feasible ones, choose a core with r+s−t fresh fair bits, and choose a uniform kernel element with n−r−s further fair bits. Every input in the fibre has probability 2^(−(n−t)); exactly n−t fresh bits are used. There is no rare-prefix rejection or hidden conditional sampler.

For repeated preparation, row-reduce A once. Bucket core z by the quotient syndrome of Fₜ(Rz) modulo im A. A requested prefix y selects its syndrome bucket; (3) makes every bucket equally sized. A right inverse on im A supplies a particular solution to (2), after which the kernel seed is added. Preprocessing enumerates 2ʳ cores once per stage. This is the executable implementation. Alternatively a scan can choose the indexed feasible core using polynomial working memory and exponential preparation time per sample.

All computations are exact binary arithmetic. Forming polar matrices, Gaussian elimination, complement/right-inverse construction, polynomial evaluations, table storage and each seed-to-input map are paid. A simple implementation costs 2ʳ poly(n,t) bit operations to prepare its reusable table and poly(n,t) per subsequent sample. No coefficient or microscopic coordinate is supplied by the oracle.

For t=n, A must be injective on L: a nonzero v with A(v)=0 would make Q(x+v)=Q(x), contradicting bijectivity. The output quotient by A(L) has dimension b(Q), and z↦Q(Rz) mod A(L) is a permutation of its 2^b(Q) quotient values. This gives a source-free inverse: identify the core z from the quotient, solve for v and return Rz+v. Decoder evaluation uses

    Q(Rz+v)=Q(Rz)+A(v),

so the acquired input basis, linear responses and 2^b(Q) core outputs suffice after compilation. `CompiledAffineCore` implements and verifies this operation without consulting the teacher.

## 3. Comparisons become averaged weak labels

Fix t<n and assume the correct prefix sampler. Write N=2^(n−t) and m=N/2. In every prefix fibre the suffix rank is a permutation of {0,…,N−1}; the next bit is 0 below m and 1 at or above m.

Given x, draw K=511 independent uniform same-prefix points and let M be their sample median. Label x by

    Lₜ(x)=1{Q(x)>Q(M)}=C(M,x).                    (4)

When N≤64, enumerate and sort the entire fibre instead, using its rank-(m−1) point for M. This label is then exact. The enumeration is paid and has a constant cap of 64 points.

For larger fibres, let J be M's suffix rank. If an independent X is uniform in that fibre, the conditional number of erroneous labels in (4) is exactly

    |J+1−m|,

including ties: the predicted upper set begins at J+1. To bound this, draw K iid continuous uniforms Uⱼ∈[0,1), set their discrete ranks to floor(N Uⱼ), and let U_* be their median. Sorting commutes with the floor operation, hence J=floor(N U_*). Therefore

    E[error fraction] ≤ E|U_*−1/2| + 1/N.

For odd K, U_* has the symmetric Beta((K+1)/2,(K+1)/2) order-statistic law, mean 1/2 and variance 1/[4(K+2)]. This follows directly by integrating its density proportional to u^((K−1)/2)(1−u)^((K−1)/2); the beta-integral recurrence gives the two moments. Cauchy–Schwarz yields

    e_N ≤ 1/[2 sqrt(K+2)] + 1/N.                  (5)

Every non-enumerated fibre has N≥128. With K=511,

    7e_N ≤ 7/[2 sqrt(513)] + 7/128 < 1/4.         (6)

The label bound is an **average under uniform raw X**, including conditional preparation and median randomness. It is not a high-accuracy label for each arbitrary X. Using it as such would be an invalid shortcut. The local-correction step below converts this averaged information into exact-coordinate requests.

## 4. Acquiring an exact next coordinate

For any quadratic Boolean f and any a,b,c,

    xor_(S subset {a,b,c}) f(x+sum S)=0.           (7)

One proof expands each monomial: a third additive difference annihilates degree at most two. Thus f(x) is the xor of the values at the seven nonempty-offset vertices. For three independent uniform a,b,c, every nonempty sum of them is uniform on V, even though the seven vertices need not be mutually independent. This remains true if offsets coincide or some vertices repeat.

For a desired f(x)=Qₜ₊₁(x), replace those seven values by seven labels (4), using fresh conditional-median experiments. A union bound over the seven marginally uniform vertices and (6) bounds one correction trial's error by <1/4. No independence of the seven vertices is assumed. Repeat with fresh offsets and preparations R times and take the majority. The trials are independent conditional on the correct previous coordinates, so Hoeffding gives

    P[incorrect recovered value] ≤ exp(−R/8).      (8)

The values at 0, each eᵢ, and each eᵢ+eⱼ determine a quadratic uniquely:

    constant = f(0),
    linear_i = f(eᵢ)+f(0),
    quadratic_ij = f(eᵢ+eⱼ)+f(eᵢ)+f(eⱼ)+f(0).

There are Dₙ such value requests. Once acquired, the next polynomial's polar form becomes available and updates the next conditional preparation table. This is the actual bootstrap:

    experience -> leading polynomial -> acquired preparation -> next polynomial.

It does not invent the quadratic model class; that promise remains supplied.

For sequential error accounting, couple the implementation to an ideal run using the true prefix at every stage. The two runs coincide until their first incorrect acquired coordinate. In the ideal run (8) holds for each of nDₙ value requests; a union bound gives total error at most nDₙ exp(−R/8)≤δ. This avoids conditioning future trials on an event involving their own unrevealed randomness. No semantic zero-error/Las-Vegas claim is made: a wrong decoder can be returned on the stated failure event.

## 5. Complete resource boundary

A merge sort of K=511 points uses at most K ceil(log₂K)=4,599 comparisons, plus one comparison for (4). Sorting an exact fibre of at most 64 points costs at most 384, plus one. Thus every weak label costs at most 4,600 comparisons, a correction trial at most 32,200, and the stated nDₙR bound follows. Repeated identical comparisons may be retained, but the bound does not require that optimization. Source rank evaluations or a hardware comparator's internal work are additional, never free.

The median-preparation randomness is exactly n−t bits per sampled input. A conservative total fresh-bit bound is

    nDₙR [3n+7·511·n],

covering offsets and median samples; exact short fibres need no sample randomness. The finite model has no real-valued precision oracle. Each physical comparison sends two n-bit inputs and returns one bit. Chosen-input preparation, reset/settling if an actual source requires them, repeated-query legality, comparator noise/calibration, and source computation have not been acquired on a physical platform. In the deterministic mathematical oracle there is no evolving hidden experimental state or reset operation.

The learner uses raw ANFs plus its acquired linear algebra and 2ʳ core tables. Interpreter/dictionary overhead, source caches and final exhaustive validation are separately reported by the executable. The logical payload is not a peak resident-memory measurement. All validation work is paid and occurs after acquisition; no teacher truth or hidden rank enters the learner's decisions.

For unrestricted quadratic permutations, b(Q) can equal n, making the preparation/computation exponential. Conversely b(Q)=O(log n) gives polynomial classical time jointly with correct acquisition on the high-probability successful event, or with an appropriate explicit resource cap and UNKNOWN on cap failure. This is an information/computation separation in the legal interface, not evidence of a generic efficient quadratic-system solver.

## 6. Cached-median executable variant

The executed code uses one cached median per encountered prefix at each stage, and retains repeated weak labels/comparisons. It is a distinct implementation of the same bootstrap. A fresh-median independence proof must not be copied to it unchanged.

Fix ε=1/64. Conceptually preassign an independent K-point median to every prefix of every stage, independently of all correction-offset tapes. There are fewer than 2ⁿ such medians. Hoeffding's binomial tail bound for the sample median gives

    P[|U_*−1/2|>ε] ≤ 2 exp(−2K ε²).

Consequently all those conceptual medians are within ε of half except with probability at most 2^(n+1) exp(−2Kε²). They need not actually be generated; independent lazy materialization when a prefix is first requested has the same joint law. Exact-enumerated fibres are automatically good.

On this simultaneous event, (5)'s deterministic quantile argument bounds the now-fixed label function's uniform error by ε+1/128=3/128. For every desired x a random-offset correction errs with probability at most 21/128. Conditional on the whole fixed median collection, fresh offset trials are independent, including when label/comparison results are retained. Their majority error is at most

    exp[−2R(43/128)²].

The code sets odd K,R so that

    2^(n+1)exp(−2Kε²) ≤ δ/2,
    nDₙexp[−2R(43/128)²] ≤ δ/2.

This establishes its stated confidence without claiming fresh medians at each label call. Median selection and sampling occur only for encountered prefixes and are explicitly counted. A conservative comparison bound adds the K=O(n+log(1/δ)) median-preparation factor; the executable is not represented as a direct measurement of the fresh-K=511 algorithm. Both algorithms use the same information interface. Python PRNG runs are finite diagnostics of implementation, not certification of ideal independent randomness.

## 7. General reduction, and the remaining computational difficulty

The same reasoning gives a broader **query-only** statement. For a bijection whose output coordinates have fixed Boolean degree d, an acquired prefix can always be sampled by enumerating all 2ⁿ raw inputs, filtering with the learned prefix and choosing a uniform index in its known power-of-two fibre. A (d+1)-offset cube supplies q=2^(d+1)−1 uniform-marginal correction queries. Choose a constant K=O(q²) and enumerate fibres of size O(q) so that qe<1/4. Interpolate D_(n,d)=sum_(j≤d)binom(n,j) coefficients per coordinate and repeat corrections O(log(nD_(n,d)/δ)) times.

Thus every fixed-degree Boolean permutation is exactly acquirable with a number of comparisons polynomial in n and log(1/δ), while raw preparation can still take exponential classical time and memory. The quadratic radical sampler is the enabling efficient preparation operation for its acquired-small-core regime. This extension neither removes the supplied degree/permutation promise nor makes general fixed-degree inversion efficient.

## 8. Genuine class extension and the strongest comparator

Use F₈=F₂[α]/(α³+α+1), z=a+bα+cα². Direct exact multiplication yields

    z³=(a+b+c+bc)+(b+ab+ac)α+(c+ab)α².

The cube permutes F₈ because gcd(3,7)=1. Its three coordinate quadratic parts are linearly independent, and their common polar radical is zero. Every nonzero linear combination of these three output coordinates is non-affine. Therefore the 3-bit map has no affine leading output coordinate under invertible affine input/output changes; it cannot have a complete scalar triangular flag. Cube×identity has affine combinations from the identity factors: the no-affine-combination statement is about the residual cube, not the whole n-bit product. The executed affine-hidden products whose first acquired bit is nonlinear are already outside the archived scalar-triangular theorem in their fixed significance order. This is checked from the acquired ANFs, then against teacher truth after return.

The pinned N780 governing proof (`updates/FA/package/decoder_continuation/COMPARISON_DECODER_THEOREM.txt`) learns exact coordinates, inverse and all prefix samplers from the same comparison oracle on a complete affine-hidden scalar-triangular class. It has expected D+6·binom(n,2) comparisons, and must be retained as the stronger incumbent wherever its promise applies. Our proof does not improve it there. Its partial-flag counterexample is an additional joint-polar-rank-2 target outside its stated leading-affine class; the present executable also recovers that target.

Low-degree interpolation and local correction are established machinery, not newly invented primitives. Schapire–Sellie exact polynomial learning uses labelled membership/equivalence feedback; [the author's paper](https://www.schapire.net/papers/SchapireSe93.pdf) is the governing source. [Rubinfeld–Sudan](https://epubs.siam.org/doi/10.1137/S0097539793255151) studies polynomial testing/correction. [Booth et al.'s lexicographic-order learning paper](https://www.lamsade.dauphine.fr/~lang/papers/bclms09.pdf) starts from visible attributes. Those results cannot be credited with or compared against a free hidden-coordinate/fibre oracle here. Conversely an equally informed conventional learner may retain every acquired prefix, use this same preparation operation, and choose any standard polynomial-recovery procedure. No strict advantage over that comparator is established.

[Kane–Lovett–Moran–Zhang (2017)](https://www.ias.edu/sites/default/files/math/csdm/2017-2018/KaneLoMoZh2017.pdf) is a stronger comparison-learning framework: its inference-dimension theorem permits both label and comparison queries, with concrete low-query examples for halfspaces. Within an acquired fibre our comparator is a suffix-score comparison, but the next-bit labels are still unavailable except through the averaged median simulator. No applicable inference-dimension or robustness theorem for that simulator was established by the focused check. It remains a strong conditional post-label comparator, not a demonstrated subsumption of this acquisition loop.

The distinctive operation being investigated is the closed comparison-to-acquired-prefix-to-next-experiment reduction, with runtime charged to a core computed from acquired data. A focused primary-source audit has not established its historical novelty; absence of a matching search result is not novelty evidence.

## 9. Recognition is still exponentially expensive in the exact arbitrary-order contract

For n≥4, consider the identity order and, for each a∈F₂^(n−1), the adjacent-pair swap

    Q^(a)(z,b)=(z,b+1{z=a}).

The identity is quadratic. The swap's final bit has degree n−1>2, hence it is outside the promised class even after invertible affine input changes. Every comparison except the mutual comparison of (a,0),(a,1) agrees with identity. Therefore a deterministic exact recognizer must query all 2^(n−1) special pairs on identity.

For a randomized recognizer accepting identity with probability at least 1−α and each nonmember with probability at most β, couple its tapes on both orders. Acceptance can differ only if the special pair is queried. Its identity-run probability for each special pair is at least 1−α−β; summing gives expected comparison count at least max(0,1−α−β)2^(n−1). This is the same scoped recognition obstruction already derived in N780's governing `RECOGNITION_AND_NOISE.md`, specialized to the current quadratic class. It is not a new lower bound and does not rule out approximate/far-from-class testing.

## 10. What this checkpoint establishes

The written construction closes a real restricted acquisition loop: useful later experiments are generated from previously acquired coordinates, without rank labels or a latent sampler being supplied. It gives a broader same-oracle class than the complete scalar flag, a computed runtime parameter, and exact reusable nonlinear rank/inverse/fibre operations. Source-free finite implementations are available.

It does not establish general representation acquisition, autonomous discovery of the class, a noisy physical interface, practical advantage, universal learning acceleration, historical novelty, external proof acceptance, or a civilisation-level capability. The executed strongest full-sort comparator wins on the small finite targets. Processor energy has not been measured, and no physical economy is asserted. A separately derived stronger quotient-rejection preparation and inverse operation is proved in `QUOTIENT_PREPARATION_SUPPLEMENT.md`; it is not the algorithm measured by the finite core-table runs. The remaining question is efficient preparation when its acquired quotient deficit is large; no general solver or hardness conclusion is claimed.
