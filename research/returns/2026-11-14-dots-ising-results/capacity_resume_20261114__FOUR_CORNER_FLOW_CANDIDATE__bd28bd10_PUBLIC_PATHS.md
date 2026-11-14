# Four fixed Ferrers-corner channels: candidate entropy-carrying native flow

STATUS: Constructive derivation and exact finite geometry/conservation tests. The overlap decoder and geometric inequalities below require independent review before any capacity certificate is adopted. Numerical R200 scalar is NOT outward-certified. No breakthrough claim.

## 1. Unchanged physical setup and computable channel law
Original torus L=8R, theta4, phi4/R, t=2phi, native per-site heatbath, original r5 core and kappa; target pluscount n/2. Work in units wminus=1. Choose d, K=2d+1, M=3R, with K<2R<M<L/2. A channel C consists of four independent Ferrers partitions lambda, each contained in a d-by-d corner square. Remove these four corner ideals from the occupied w-by-h rectangle; denote the resulting orthogonally convex, connected shape S_C(w,h). For w,h>=K, corner squares are disjoint, all bbox extremes are attained, physical perimeter is2(w+h), and area is wh-A_C, where A_C is total removed area.

q=exp(-t), Z= sum_lambda q^|lambda| = Gaussian-binomial(2d,d)_q, N=number of partitions=binom(2d,d). Choose p_C=q^A_C/Z^4. No sampler oracle: positive recursion Z(a,b)=Z(a-1,b)+q^a Z(a,b-1), boundary1, acquires the normalizer and sequential partition sampler in O(d²) arithmetic. The first term drops the row budget; the second removes a full first column. q is an elementary computable real; an exact-random-bit implementation has not been supplied. The proposed numerical test uses the explicit formula, not an opaque learned proposal.

## 2. Actual monotone physical path for each channel
Prefix: construct S_C(K,K) row by row. Start a new row in the overlap with the preceding row's interval, then extend left and right contiguously. The initial row is filled contiguously. Every prefix is connected and row/column convex.

Core: alternate growing right then up, from K-by-K to M-by-M. A right expansion adds exactly one cell in each row, at x=w-lambda_right(y). Process the top-right positive-cut rows from interior toward the outer corner, then bottom-right positive-cut rows similarly; skip zero-cut rows. Finally fill the contiguous central zero-cut interval from one end. Each positive-cut addition has exactly two occupied NN neighbors, because the inward row supports the first site of each plateau. The central interval has one one-neighbor birth, followed by two-neighbor additions. An upward expansion uses the same rule on the TRANSPOSED shape: top corner row partitions must be conjugated before obtaining column deficits. Omitting this conjugation is a real implementation error and was caught in the first finite test.

Thus the energy along each expanded side is at most the ordinary rectangular side path's corresponding energy plus t A_C. The exact endpoints are S_C(w+1,h) or S_C(w,h+1), respectively. In particular

R_core(C) <= q^(-A_C) R_bare_core <= q^(-A_C) R_bare_full.

Merge: at M-by-M, fill the four missing corner ideals from their inward boundaries, each addition with at least two NN neighbors, to reach the full square. Then use the ordinary balanced rectangular path to majority, with native winding energies. All paths start all-minus, use only physical additions, and reach majority for the first time at their last edge. All-minus is in the original core. Inject unit current along its reservoir edge of resistance kappa^-1. Other reservoir edges can carry zero current. No source redefinition is made.

## 3. Core edge overlap: proposed polynomial decoder
Core bboxes lie strictly inside L/2 in both coordinates, so a translated physical shape has a unique minimal torus bbox and its translation anchor is determined. Core shapes retain the bottom and left bbox extremes, even while a side is being added.

For right-growth stages, the unchanged height identifies the unique macro stage (because the core schedule alternates right/up). The left two corner labels are unchanged and recoverable. Before the central birth the physical bbox has the old width. A partially processed right corner has profile lambda'_i=lambda_i-1 on one contiguous interval [k,p) of its positive rows, and lambda'_i=lambda_i elsewhere. Hence at most(d+1)^2 possible original labels. A fully processed corner has lambda'_i=max(lambda_i-1,0), allowing at most(d+1) original labels (the number of terminal original ones). During the second corner's processing this gives at most(d+1)^3 possibilities for the active pair. During first-corner processing it is no larger. After central birth the bbox has its new width; the only ambiguity is original ones versus unfilled original-zero suffix rows, at most(d+1) choices per corner, hence at most(d+1)^2.

The flipped edge's location and old/new bbox dimensions identify which of these stages applies; the bounds are not multiplied by all stages. The same decoder applies to up growth after conjugating corner partitions, with the bottom two labels stationary. Given a physical bbox, at most one right and one up stage can contribute. Thus the proposed safe bound is

multiplicity per physical core edge <= B_d=2(d+1)^3,

including channel labels, directions and translations. The n translations do not multiply this number because the bbox fixes the translation anchor for each candidate channel.

Unweighted Cauchy-Schwarz at each physical edge, followed by summation, gives

R_core(mixture of channels and translations)
 <= B_d/n * sum_C p_C² R_core(C)
 <= B_d R_bare_full / (n Z^4).

The full Z^4 entropy is paid only after the polynomial overlap decoder; it is NOT justified by pretending channel paths are disjoint. If the decoder is false, this improvement is not established.

## 4. Prefix/merge/late path costs, without fictitious entropy gains
The exact count N of corner partitions is retained. Let
B_pre = 32K-t K²+tK,
B_M=32M-t M².
Every prefix has bbox dimensions<=K and occupied area at least bboxarea-A_C-K. Since K<2R, rectangular energy increases in each bbox dimension up to K. Orthogonal convexity gives energy<=B_pre+t A_C and path length<=K². Convexity of resistance under mixture, without taking a translation discount, therefore yields

R_pre <= 2K² exp(B_pre) (N/Z)^4.

Corner filling has length<=4d² and never exceeds its initial energy B_M+tA_C, giving

R_merge <= 8d² exp(B_M) (N/Z)^4.

The common late balanced path has energy<=B_M+16; a deliberately loose bound is

R_late <= 2n exp(B_M+16).

Merge and late edges occupy disjoint pluscount ranges. Prefix/core/merge phases can overlap across channels; rather than omit this congestion, apply the universal squared-sum inequality:

R_physical <= 3(R_pre+R_core+R_merge+R_late).

A sharper Minkowski bound is available but not used in the saved headline scalar. Add the shared kappa^-1 without dividing it by n. Finally multiply by the full original ZA/wminus, whose separately derived finite upper is exp(10^-6). This explicitly accounts for Q=Z^4, all phase mixing, original source, and all thermal-core configurations. The source normalization is not a product Gibbs approximation.

## 5. Executed tests and candidate R200 value
Two tests were run: native q=exp(-8/R) with floating weights, and exact integer common-denominator weights at diagnostic q=1/2 to check conservation independently of transcendental arithmetic.

R2,d1:16 full channels,359 distinct physical edges; exact source outflow81/81, zero interior divergence; maximum core edge label multiplicity2 versus bound16.
R4,d2:1296 full channels,78167 distinct physical edges; exact source outflow1500625/1500625, zero interior divergence; maximum core multiplicity6 versus bound54. Every emitted spin was unoccupied, every core neighbor count was1 or2, every macro endpoint equaled its independently reconstructed shape, every prefix energy bound passed, all corner fills existed with>=2 neighbors, and every path ended at exact majority.

These are anchored full-graph tests. The q=1/2 test is a rational conservation/geometry diagnostic, NOT the native R4 importance law; its native energy was still computed separately. The native-q test is separately saved. The torus-translation decoder is justified above, not exhaustively tested over all large-instance translations.

At R200,d132,K265,M600:
log Z=38.3440688872, log N=179.9761427962.
log R_pre bound6259.98090;
log R_core bound6270.00432;
log R_merge bound5378.37334;
log R_late bound4831.44866.
Including phasefactor3 and thermal multiplier gives candidate log inverse-capacity upper6271.10298. Relative to retained Wcut/ZA<=exp(-6215), candidate W/C upper is exp56.10298. This would be a major finite certificate improvement over exp187, but still far from a practical or uniform polynomial predictor. It is conditional on the proof obligations above and is currently a scalar floating diagnostic, not an adopted theorem or outward certificate.

Artifacts: corner_channel_check.py/native-weight result; corner_channel_exact.py/exact-weight result; corner_bound_scalar.py/results. No large channel ensemble was enumerated and no large sampler was run.

## 6. Independently suggested quadratic decoder tightening
An independent active-corner enumeration tested d1..5, up to63504 active-corner pairs and698544 emitted edges. One-direction maximum multiplicities were2,6,12,20,30. These do not prove an asymptotic bound, but revealed a lost endpoint in the cubic count.

At an edge during positive-cut processing, the flipped row index z is part of the physical edge. Processing order is d-1 down to0, skipping zero original rows. Thus previously processed positive rows are exactly[z+1,p), where p is the original partition's positive support length. The start of the interval is no longer unknown. There are at mostd+1 possible original active labels. The earlier fully processed corner has at mostd+1 choices. Hence the safe per-direction bound improves to(d+1)^2; postbirth already had that bound. Old/new bbox, flipped x coordinate and disjoint top/bottom corner regions determine the applicable stage. Including both growth directions gives **B_d=2(d+1)^2**. This is independently proposed and independently re-derived; review should check it rather than infer it only from finite data.

The potentially sharper d(d+1) per-direction count is NOT used in the saved certificate.

## 7. Fully specified directed arithmetic, conditional on geometry
`certify_four_corner_scalar.py` now produces two independent receipts, one with cubic and one with quadratic overlap. It uses no floating log or exponential primitive. Exact Fraction Taylor sums through degree32 at |x|/2^s<=1/8 give lower exp values; the omitted tail is bounded by its first term divided by1-x/34. Values are converted outward to80-digit Decimal and squared with the appropriate rounding direction. Negative exponent bounds use reciprocals with reversed endpoints. The Gaussian-binomial normalizer uses the positive17424-cell recurrence rounded DOWN with q rounded down. Every resistance term, inverse normalizer and final sum is rounded UP.

The known directed bare-path upper exp6423 is used, not its non-certified floating improvement. Source kappa^-1<exp2593.6 and full-core exp(10^-6)<=1/(1-10^-6) are explicitly added. The common source is never divided by n.

Cubic receipt: normalized flow resistance/exp6272 <=0.5122460478; conditional C/ZA>exp(-6272), W/C<exp57.
Quadratic receipt: normalized flow resistance/exp6267 <=0.5742731505; conditional C/ZA>exp(-6267), W/C<exp52.

These are arithmetic certificates of stated formulas, NOT substitutes for the general geometric proof. Scalar calculation and partition acquisition took approximately0.009seconds per receipt; no enumeration of the enormous channel ensemble was performed. Constructing a sampled complete channel path still requires n/2 physical additions at R200, plus the partition sampler. The original full-output importance sampler and its stopping/residence costs remain separate obligations.
