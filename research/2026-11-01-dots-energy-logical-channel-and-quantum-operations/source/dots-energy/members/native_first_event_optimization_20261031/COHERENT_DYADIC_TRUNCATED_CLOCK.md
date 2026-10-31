# Coherent truncated exponential clocks with constant success

Status: candidate acquired operation. This supplies a truncated exponential for a COHERENT remaining duration, not only a classically fixed window. It is an ordinary geometric-product preparation plus bounded-gap polynomial amplification. No scalar conditional acceptance P(t) is evaluated. The numerical law is discretized explicitly and its cost is paid.

## 1. Inputs and positive geometric preparation

Fix an acquired positive rate q and a common time mesh h>0 for the current physical first-event call. Both are classical parameters with certified finite arithmetic. Supply a coherent integer N in [1,Nmax], representing duration t=N h. Choose Bmax large enough for all integers below 2*max(1,Nmax). N is preserved as an input/output register.

Let l=ceil(log2 N), M=2^l, so N<=M<2N (N=1 gives l=0). Compute l reversibly from the leading bits of N. For j<l prepare a bit with

    p_j=e^{-q h 2^j}/(1+e^{-q h 2^j}),

and set higher bits to zero. These rotation angles depend only on q,h,j, not on N or l, and can be precomputed CLASSICALLY once per physical call. A controlled j<l condition selects the appropriate prefix of the same list. Thus no table indexed by all N is used. The resulting integer m has probability proportional to z^m on [0,M), z=e^{-q h}.

Compute the success flag m<N. Its success probability is

    P_N=(sum_{m<N}z^m)/(sum_{m<M}z^m)>=N/M>=1/2.

The first inequality uses decreasing nonnegative weights. N=1 succeeds deterministically. Conditional on success, the m-probabilities are exactly

    (1-e^{-q h})e^{-qhm}/(1-e^{-qNh}), m=0,...,N-1,

the INTEGRATED bin probabilities of Exp(q) conditioned on falling in [0,Nh]. The rate-zero limiting operation, if admitted, is uniform and obeys the same success bound; in the actual positive-rate bridge only q>0 is needed.

Return the left endpoint m h, not a midpoint, so all recursive durations stay on the same grid. Coupling to the exact conditional exponential inside the selected bin gives absolute time error <=h. A reflected increasing exponential returns N h-m h, with the same error. Zero times are allowed and retain the chronological operator word; the received stable hierarchy already specifies the t=0 limiting bridge. For an input N=0, use that caller-specified zero-time convention rather than dividing by a zero conditional probability. The N=0 branch is controlled around the polar circuit and is OUTSIDE its admitted block and its minimum-singular-value claim; it is not silently amplified as another successful conditional exponential.

## 2. Explicit bounded odd amplification polynomial

The good block of this proposal is B|N>=sqrt(P_N)|N>|phi_N>, where phi_N is the normalized accepted clock state. Thus every singular value on the admitted N>=1 domain is >=1/sqrt(2). No value of P_N is required to implement the following uniform polynomial.

Let c_k=binom(2k,k)/4^k and

    p_m(x)=x sum_{k=0}^m c_k(1-x²)^k.

This is an odd polynomial of degree2m+1. For x in [0,1], its terms are nonnegative and the infinite series equals1 for x>0, so 0<=p_m(x)<=1; by oddness it is bounded on [-1,1]. For x>=1/sqrt(2), using c_k<=1,

    0<=1-p_m(x)<=sum_{k>m}(1-x²)^k<=2^{-m}.

Choose m>=ceil(2 log2(16/eta)). Scaling p_m by 1-eta²/256 gives strict margin if useful for numerical phase factorization. Ordinary rectangular-block singular-value transformation implements this bounded odd polynomial using degree2m+1 calls to the proposal unitary/inverse and fixed projector reflections, with the phase preprocessing and precision paid. The coefficients are acquired rationally from c_(k+1)=c_k(2k+1)/(2k+2); their binary lengths and expansion cost are polynomial in m. This is not an assumption of a normalization-one exponential oracle: the polynomial and its gap are explicit.

On the admitted singular interval the transformed good amplitudes differ from1 by O(eta²), and coherent failure norm is O(eta). The polar output direction is exactly |N>|phi_N>. Hence the full source-preparation isometry is within O(eta) of the desired conditional clock, uniformly for coherent superpositions of N and external reference registers. The classical polynomial/phase-factorization stage must approximate the target GOOD polynomial to O(eta²), for example eta²/1000, so its ideal coherent failure remains O(eta), not O(sqrt(eta)). Allocate eta/2 to this resulting source-isometry error and eta/2 to subsequent actual unitary/phase synthesis. Actual gate synthesis is compared in full circuit operator norm and may have total error O(eta). No normalized physical postselection, amplitude estimation, or expected-query stopping is used.

This is the usual bounded-gap polar/fixed-point amplification operation. Its O(log(1/eta)) query cost must be compared honestly with three-call preparation PLUS scalar acceptance arithmetic, not declared automatically superior.

## 3. Actual circuit and finite-precision costs

One proposal unitary computes l, applies at most Bmax controlled rotations, compares m<N, and uncomputes ancillary arithmetic while retaining m,N and success. All inverses exist. Leading-bit extraction and integer comparison use polynomial, in fact standard linear/quasilinear finite-register circuits; their actual gates and work registers are paid. Neither coherent QRAM nor a range-enumerating amplitude table is assumed.

For D=2m+1 amplification degree, allocate each elementary proposal rotation/operator implementation error at most eta/[100 D(1+Bmax)] and phase errors by the same capped circuit hybrid. Since N is retained, the exact proposal is block diagonal in N and the error bound is uniform, not amplified by sqrt(Nmax). Acquire tiny probabilities with squared absolute probability tolerances as needed to synthesize angles in operator norm. Evaluate the fixed coefficients e^{-x}/(1+e^{-x}) with nonpositive exponentials and certified clipping; a clipped amplitude costs its amplitude, not merely its probability.

The resulting quantum operation cost is O(D) calls to an explicit O(Bmax)-rotation/comparison proposal, plus its acquired synthesis costs. Classical acquisition prepares O(Bmax) angles for each fixed rate q; it is polynomial in input lengths, Bmax and precision bits. There is no online exponential, inverse logarithm, square root of a random uniform, or coherent P_N normalization evaluation. Rates s,d,nu,2c can have separate precomputed lists; their number is constant for the one-chain source.

The grid h must still satisfy the received physical/source timing error budget, and all clock values are converted to the physical time register with actual finite arithmetic. Large q is paid through the required grid bits and angle acquisition, not ignored. Every unused source seed and amplification failure flag is retained until inner unprepare, and SELECT is zero on any failure flag.

## 4. Receiving and limits

This operation may replace each truncated exponential component in the already acquired elementary bridge. Its exact finite bin law differs from the continuous conditional time only by the coupled O(h) bin displacement; state-preparation error O(eta) is subdivided across the capped number of uses. The stable hierarchical remaining-time argument and chronological ordering remain necessary. A grid-positive remaining duration is N h; a rounded zero duration uses the explicit limiting bridge, not an undefined conditional clock.

This does NOT remove the source's atom/mixture probabilities or its other acceptance arithmetic automatically. It does not imply that all coherent exp/log arithmetic is gone from the full first-event simulator. It supplies one paid bounded-success conditional operation and a legitimate alternative to direct inverse-CDF evaluation. The fixed-window outer clocks and unconditioned QQ waiting clocks can use the simpler unamplified product construction and should not pay this extra normalization machinery.

No gate benchmark, practical crossover or novelty claim is made. Both legitimate normalization options—few proposal calls with acquired scalar P, versus O(log(1/eta)) cheap proposals without P—must be priced in the eventual integrated audit.

## 5. Ordinary primary implementation used

The polynomial receiver is exactly the real-polynomial rectangular singular-value transformation of Gilyén–Su–Low–Wiebe, Corollary18: real parity-matching polynomials bounded by1 on [-1,1] are implemented as projected blocks, with one additional control for the real part. This supplies the normalization-one polynomial block used above, not an unpriced scalar sign oracle. Primary statement inspected: https://arxiv.org/html/1806.01838v1 .

Finite phase acquisition is paid using Haah's bounded-precision product-decomposition construction, Section4.3: for degree D its classical preprocessing is O(D^3 polylog(D/epsilon)) bit operations, with arithmetic precision O(D log(D/epsilon)). Our rational coefficient list is explicitly available at that accuracy; here the polynomial target tolerance passed to that preprocessing is epsilon=O(eta²), while subsequent actual circuit synthesis is budgeted in operator norm at O(eta). This addresses numerical phase acquisition rather than assuming exact real arithmetic. Primary Section4.3 inspected: https://arxiv.org/html/1806.10236v4 . These are strong established components, not new phase-synthesis results.
