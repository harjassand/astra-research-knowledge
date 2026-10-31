# Factorized many-mode first-event compiler: new construction

31 October 2026. Unreviewed extension of the fixed-two-mode candidate. This does not silently enlarge any accepted theorem. It removes the exponential endpoint enumeration only if the operator-valued block-encoding argument below survives whole review.

## 1. Shorter windows buy a bounded row normalizer
Let E(t)=tensor_i exp(Mi t), Mi=[[0,gi],[gi,-2lambda_i]], gi=sqrt(Gamma_i lambda_i), Gamma_i=gamma_i ai^2, Gamma=sum_i Gamma_i. For a single factor, write its entries as [[a,b],[b,d]]. Since a>=d,

max row sum=a+b <=exp(Gamma_i t/2)[1+sqrt(Gamma_i t/2)].

Indeed a<=exp(si t), while b<=min(gi*t,gi/(2lambda_i))*exp(si t), and the minimum is at most the geometric mean sqrt(Gamma_i t/2). Hence

R_product(t)<=exp[Gamma*t/2+sqrt(r*Gamma*t/2)].

Choose every window tau<=1/(4r Gamma) when Gamma>0. Then R_product(t)<2 for all t<=tau. There are O(1+r Gamma*T+p) windows after splitting at prescribed controls. Gamma=0 is handled directly. The extra factor r is paid; it replaces an exponential 2^r endpoint normalization.

## 2. Operator-valued row/column preparation
For a symmetric nonnegative matrix E with row sums at most R, ordinary row/column state preparation embeds E/R as an overlap of two isometries. Here retain both endpoint strings in the common workspace. The right isometry on input endpoint i prepares j with amplitude sqrt(E_ji/R). The left isometry on output endpoint j prepares i with the same amplitude. Use orthogonal left-failure and right-failure flags for the unfilled row/column probability so their overlap contributes zero.

E is a tensor product of two-by-two factors, so both preparations factor into r constant-size preparations controlled on the corresponding endpoint bit. For t<=tau use each factor's row bound at tau; their product is below two, and an additional flag can rescale to the fixed R=2. This does not enumerate endpoint strings. The two-state probabilities and rotation amplitudes are computed to certified finite precision; tiny probabilities are clipped only with a charged amplitude error.

Conditioned on the pair (i,j), append an identical uniform random-word register on BOTH preparation sides and compute the same finite conditional virtual bridges. Put a SELECT of the chronological system-operator word and its (-i)^k phase between the preparations. The SELECT leaves endpoint and bridge labels untouched; product block-encoding work flags are projected only at the final good block. The overlap for matrix entry (j,i) is

(E_ji/R) E_bridge[chronological normalized system word],

which is K_ji/R. Thus the whole block is K/R, not a sum over all endpoint pairs. Fresh operator-block ancillas ensure the selected product is the product of blocks. Any failure/default bridge branch receives the previously budgeted mean-block error. The private virtual random words are unprepared; they are not a physical noise record.

This is a matrix-of-operator-expectations use of standard row/column block encoding. The identity must be checked at the circuit/isometry level, including its failure flags; it is not a free matrix-entry oracle assertion.

## 3. Actual jump rows remain factorized
For a jump of color i, the positive majorant is E_other tensor Wi, where

Wi(t)=2sqrt(lambda_i)|0><1| exp(Mi t)
     =[[2sqrt(lambda_i)b_i,2sqrt(lambda_i)d_i],[0,0]].

Its maximum row and column sums are bounded by the same scalar 2sqrt(lambda_i)(b_i+d_i). The earlier single-factor bounds and R_other<2 imply a constant C times

sqrt(lambda_i)exp(-2lambda_i*t)+sqrt(Gamma_i)

for the full positive majorant's row and column sums. The nonsymmetric row/column preparation works with one rank-one two-state factor and r-1 symmetric factors. The bridge's pre-jump endpoint bit is one, while its physical output bit is zero; retain that distinction in both preparation circuits. When Gamma_i=0, cancel the shared decay factor analytically in the normalized row; when lambda_i=0 omit the zero event arm.

A sufficiently generous squared envelope remains
w_i(t)^2=4096 exp(Gamma*tau)[lambda_i exp(-4lambda_i*t)+Gamma_i].
The sum of its integrals is O(r+Gamma*tau). Together with K's fixed normalizer two, the complete first-event isometry has normalizer O(sqrt(r)), not O(2^r). Pad to an explicit known larger normalization, for example a power of two above 256sqrt(r+1), and charge the resulting polynomial amplification cost.

The outer event-color distribution is acquired by finite arithmetic over the r elementary component weights; a linear scan or controlled tree of cumulative sums is polynomial in r. Each event time is again a mixture of truncated exponential and uniform. No arbitrary state-preparation oracle is assumed.

## 4. Conditional source complexity for many modes
All r virtual bridges are independent conditional on their endpoint bits. Before conditioning, their combined transition count is at most 2Poisson((sum_i si)*tau)+r. Conditioning divides tail bounds by the product of endpoint probabilities. Its logarithm is the SUM of the r logarithmic endpoint costs. Thus a deterministic virtual-event cap polynomial in r, input bits, log switching rates and log inverse error remains possible. Do not sample endpoint strings by rejecting against their exponentially small joint probability.

The global boundary/tie exclusions divide by that same product. Their probabilities may require a very fine timing mesh, but its bit length is polynomial in r and the input lengths. Sort the polynomially many sampled virtual events coherently. Preserve the exact noncommuting order outside the priced tie set. Recursive duration stability and the separate no-event atom remain mandatory.

The independent actual-event MGF bound is still exp[Gamma*T(exp(theta)-1)] from ground ancillas. Actual-jump caps, prescribed-control windows, private remaining-time comparisons, complete CPTP defaults, common-uniform isometry errors and the zero-coupling cancellation all carry over with polynomial r factors. The physical ancillas are retained throughout.

## 5. Intended consequence and unresolved status
If these finite-preparation and amplification details close, the full simulator can have polynomial cost in r, 1+alpha0*T+Gamma*T+p, the input sizes, log(2+sum_i lambda_i*T) and log(1/epsilon), with all controlled H0/Ai block-encoding costs charged. If only individual Ai encodings are supplied, coherently selecting their index can be implemented with O(r) controlled calls and that cost must be counted.

This would treat a variable number of independent, noncommuting telegraph couplings, without processing their fast classical switch lists or assuming a time-ordered noise-frame oracle. It remains a construction under review, not an implemented compiler, practical speedup or novelty claim. The accepted finite two-mode representation and count bound do not depend on acceptance of this extension.
