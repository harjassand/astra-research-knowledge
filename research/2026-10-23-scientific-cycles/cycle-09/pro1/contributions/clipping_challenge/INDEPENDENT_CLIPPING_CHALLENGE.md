# Independent challenge of the Cycle9 clipped input

Reviewer: `/root/cycle9_clipping_challenge`. Date: 22 October 2026.

## Scope and source actually read

This review targets the new endpoint-moment and spectral-clipping construction. It does not repeat the entire inherited capacity audit. I read the native Cycle8 `NONLINEAR_ENDPOINT_RESPONSE.tex`, `INHERITED_OPERATOR_CODING.tex`, `INHERITED_COMPRESSION.tex`, and the actual Cycle7 three-case normal form and optimizer sections of `SHARP_TEMPORAL_GROWTH.tex` from the independently hash-verified starting source.

The new argument passes this internal challenge with the constants below. This is neither external certification nor a historical-priority assessment.

## 1. Moment counting is valid for the actual operator

Write `H=sum_{i<j} H_ij`. The native source gives Hermitian summands of norm at most two. Each summand changes exactly the two named binary charge bits, with zero action on equal endpoint charges. Input color permutations can be arbitrarily complicated; no locality claim about those color wires is needed.

In a product of `2p` summands, a nonzero diagonal binary-charge block requires every endpoint label to occur an even number of times. Since sigma is charge diagonal, every other product has zero sigma trace. Each remaining product has absolute sigma trace at most `2^(2p)`.

Orient each of the `2p` unordered edges. This gives `2^(2p)` distinct oriented endpoint lists for each edge list. Every even endpoint list admits a perfect matching of its `4p` positions whose paired labels coincide. There are `(4p-1)!!` matchings and at most `k^(2p)` choices of labels for a matching. Overcounting, including disallowed self-edges, only increases this upper bound. Therefore

`Tr(sigma H^(2p)) <= (4p-1)!! k^(2p)`.

For `|t|k<1/2`, expansion of cosh and
`(4p-1)!!/(2p)! = binom(4p,2p)/4^p <= 4^p`
give

`Tr(sigma cosh(tH)) <= 1/(1-4t^2 k^2)`.

Functional calculus gives `exp(t|H|)<=2 cosh(tH)` for `t>=0`. Thus

`Tr(sigma exp(|H|/(4k))) <= 8/3`.

The moment comparison does not replace the coherent bath dynamics by classical errors. It is an input spectral estimate. Commutation of sigma with H makes the later density construction particularly direct.

The moment statement has a useful stronger interface. Let P denote pinching into all complete binary charge patterns. The same word expansion bounds every diagonal block in operator norm, and positivity gives

`0<=P(H^(2p))<=(4p-1)!! k^(2p) I`.

Termwise summation and positivity of P then imply

`P(exp(|H|/(4k)))<=8I/3`.

Hence the exponential moment bound holds for any reference density that is block diagonal in every full charge pattern, regardless of within-pattern color correlations. Neither a product reference nor commutation of that reference with H is needed for this moment interface. Commutation is needed for the simple positive-density and scalar chi-square arguments used later with the actual sigma.

## 2. The proposed positive density is normalized and admissible

Put `l=ln 2`, `b=beta^2`, `v=Tr(sigma H^2)`,

`gamma=l/4`, `m=3lv/32`,

`L=I-gamma bH+(4m/k)b^2(Q-k/2)`.

All terms commute with sigma and Q; `Tr(sigma L)=1`. Let `N=L_-`, `M=L_+`, `epsilon=Tr(sigma N)`, and

`rho=sigma M/(1+epsilon)`.

This is a positive normalized charge-preserving input density. Zero eigenvalues are permitted. The inherited type/coding proof uses the positive eigenvalues only. Clipping is a mathematical choice of the average input, not an implemented postselection or filter. An existence claim does not provide an efficient algorithm for diagonalizing L or compiling the resulting code.

## 3. Tail cost and normalization

Assume `k>=2`, `r=bk<=1/64`. The diagonal correction has norm

`2mb^2=3lvb^2/16 <=3l r^2/128 <1/2`.

Joint spectral calculus therefore gives

`L_- <= gamma b (H-1/(2gamma b))_+`.

Integrating the positive spectral tail from the exponential moment,

`epsilon <= (32gamma/3)bk exp[-1/(8gamma bk)]`

`= (8l/3)r exp[-1/(2lr)]`.

The exact signed comparison `sigma L` has trace one, and
`||rho-sigma L||_1=2epsilon`. For the drift it is better to retain the positive correction `sigma N` explicitly rather than pay this doubled bound.

## 4. Entropy: the global chi-square bound is sufficient

Set `Z=L-I`, and use expectations with respect to sigma. The offdiagonal structure gives

`E Z=0`, `E Z^2=l^2 v b^2/16+9l^2 v^2 b^4/(256k)`.

For `f=M/(1+epsilon)`, `Ef=1` and

`E f^2=E M^2/(1+epsilon)^2 <= E L^2 <=1+E Z^2`.

Since `f ln f <= f(f-1)` (with the continuous value at zero),

`D_2(rho||sigma)<= E(f-1)^2/l <= E Z^2/l`.

This remains valid even when the operator norm of Z is large. No unproved Taylor remainder or Gibbs-response extrapolation is used.

The charge excess is exactly

`Tr[rho(Q-k/2)] = [mb^2+Tr(sigma(Q-k/2)N)]/(1+epsilon)`.

Since `mb^2<=k/2`, it is at least `mb^2-k epsilon`. Impose the sufficient clipping budget

`epsilon <= l v b^2/(256k)`.

Then charge excess is at least `23 l v b^2/256`. Also

`u=vb^2/k <= r^2/(8k) <=1/65536`,

so the relative entropy is at most `17 l v b^2/256`. Using `-log_2 sigma=kI+Q` yields

`S(rho)-3k/2 >=3 l v b^2/128 >= l v b^2/64`.

Thus the parent construction's stated entropy constant is conservative.

## 5. Exact operator drift survives clipping

The source's exact diagonal cancellation and all-order response give, on the whole bulk prefix,

`D_b(sigma L)=gamma b^2(1-b)[(3v/4)I-F_k(b)]`.

The inherited bound `||F_k(b)-vI||<=8b(k-2)v` and `bk<=1/64` imply `F_k(b)>=7vI/8`. Hence

`D_b(sigma L)<=-l v b^2(1-b)I/32`.

The added positive input correction has trace epsilon. The full physical bounded displacement obeys `||G_beta||<=k`, even on the infinite bath. Consequently

`D_b(sigma N)<=k epsilon I`.

For `b<=1/256`, `1-b>=1/2`; the stated epsilon budget and `epsilon<=1` give

`D_b(rho) <= -l v b^2(1-b)I/128`

on initial bath depths at least k. This is a full operator inequality over all coherent/entangled prefix states. The clipped input has many-endpoint coherences, but their total effect was bounded by its trace-class correction. The pair lemma was applied only to the signed linear comparison where it is valid.

No inward sign is imposed at the root. Charge preservation ensures the homogeneous-increment lemma still applies, and the inherited finite root remainder is retained.

## 6. Uniform block choice and coding consequence

For `0<beta<=1/16`, set `b=beta^2`, `B=ln(e/b)`,

`k=floor[1/(16bB)]`.

Because `bB` is increasing on `(0,1)`, its largest value in this range occurs at `b=1/256`; direct elementary comparison gives `1/(16bB)>2`. Thus `k>=2`, `k>=1/(32bB)`, and `bk<=1/(16B)<1/64`.

The tail bound gives

`epsilon <=(8l/3)bk exp[-8B/l] <=(8l/3)bk b^8`.

Since `b^7<=3/65536`, this is at most `l b^2 k/8192`, which is no greater than `l v b^2/(256k)` by `v>=k^2/32`. The clipping budget therefore holds uniformly, including the floor in k.

The exact positive rho has charge preservation, finite input rank at most `3^k`, and strict inward operator drift. These are precisely the inherited operator-coding theorem's hypotheses. It yields one initializer-independent deterministic unassisted code sequence, pointwise vanishing full-diamond error for every fixed normal initializer, and the actual tau_pi coherent-information limit `S(rho)/k`. Beta, k and rho remain fixed before the coding horizon. No terminal bath return is added.

The entropy lower gives

`S(rho)/k >=3/2+l b^2 k/2048 >=3/2+l beta^2/[65536 ln(e/beta^2)]`.

The inherited code proof continues to pay the r-squared positivity factor, auxiliary CPTP normalization, polar repair, and all physical calls. Half-diamond errors are exactly half the stated full-diamond errors. These are unchanged inherited obligations, not a fresh-channel coding reduction.

## 7. Counterexample to a genuinely load-bearing omitted premise

Total-charge preservation, input offdiagonality and individual norm bounds alone do not imply the even-endpoint moment bound. On the native qutrit input let

`T=sum_{a=1,2} (|0a><a0|+|a0><0a|)`

act on sites 1 and 2, with identity on the others. Then `||T||=1`, T is input-offdiagonal and commutes with total Q and sigma, and `Tr(sigma T^2)=1/2`. Falsely label every pair summand as `H_ij=2T`. Their sum is `H=k(k-1)T`, so

`Tr(sigma H^2)=k^2(k-1)^2/2`.

At k=4 this is 72, exceeding the proposed moment upper `3k^2=48`. Each term changes the same two bits rather than its named endpoints. This isolates exactly the grading premise used by the proof; it is not a counterexample to the actual H.

## Status and resources

The mathematical derivation above is an independent source-based challenge. No asymptotic spectrum fit, finite-cutoff stationary state, Gibbs response assumption, or numerical count is used as proof. No new hardware/paid compute, external outreach, bath initialization, or reset is involved.

The mathematical review and inference costs were not instrumented and remain unknown. File-reading tool calls returned in under one second each. Those timings do not measure discovery or review cost. Historical originality and external expert acceptance are not established by this internal review.

## Integrated-manuscript follow-up

Read the complete new main argument through comparison in `SPECTRAL_CLIPPING_CAPACITY.tex`. The mathematical constants, fixed-before-horizon contract, spectral obstruction witness, moment interface and two omitted-premise examples match the construction reviewed above. One exported-interface omission was found: the general positive-part lemma needed `[sigma,Q]=0` before concluding charge preservation. The actual input already had this property. The main source now states it explicitly and includes the `B=I` counterexample; this correction was read and verified. The scalar diagonal-correction norm is now named `eta0`, distinct from the physical reference eta. No concrete mathematical issue remains in this inspected version. Exact version binding is in `INTEGRATED_MANUSCRIPT_REVIEW.json`; later edits are not silently included.

### Final numerical/comparison delta

Checked only the two subsequently added fixed-angle and resource paragraphs against the actual `representation/transfer_comparison.json`. All displayed values agree to their reported precision, including the beta=1/512 block length, susceptibility, both certified lower bounds, their ratio, input-dimension logarithm, and Lyapunov constants. The beta=1/16 and 1/64 comparisons correctly retain the stronger predecessor. Rank is explicitly only bounded above, and the evaluations are not described as measured capacities or practical performance. No theorem rerun was needed and no further concrete issue was found. The final source identity and JSON identity are recorded in the `final_delta_review` entry of the version-preserving receipt.
