# A fully specified learned-throughput reference channel from the same holdout

27 October 2026. Local post-cutoff addendum to `full_qutrit_unentangled_holdout_verification.md`; independent receiving requested.

The original verifier certifies distance to G_a at the unknown ACTUAL average acceptance a. The same data can instead certify a fully specified classical reference channel G_ahat, without changing sample exponents.

For target0<nu<=1 and confidence beta, run that verifier with accuracy tau=nu/2 and confidence beta/2. Thus

 L=ln(8/beta), m=ceil(9216 L/nu^2),

with the same supplied acceptance floor and corresponding deterministic cap. On a completed run set

 ahat=m/N, epsilon=nu/8,

where N is the stopping time of the m-th accepted trial. Issue the strengthened certificate only when the original verifier certifies. The additional confidence analysis is simultaneous and does not use a new acceptance-dependent selection rule.

## Negative-binomial throughput confidence

Uniformly for any actual a>0,

 Pr[|ahat-a|>epsilon a] <=2exp(-m epsilon^2/16).       (1)

This refers to the hypothetical uncapped waiting time; a completed capped run is a subset, so its false-certificate probability is no larger. There is no assertion of a conditional confidence law after conditioning on completion.

For the upper deviation, N<m/[a(1+epsilon)] implies that at a deterministic time with expected acceptance at most m/(1+epsilon), at least m acceptances occurred. The binomial exponential bound at ln(1+epsilon) gives exponent

 m[ln(1+epsilon)-epsilon/(1+epsilon)]
 >=m epsilon^2/[2(1+epsilon)^2]>=m epsilon^2/4,

where epsilon<=1/8.

For the lower deviation use n=floor(m/[a(1-epsilon)]). Its mean is at least m/(1-epsilon)-1. Since m epsilon>=2, this is at least m(1+epsilon/2). The lower-tail Chernoff exponent at threshold m is at least

 m epsilon^2/[8(1+epsilon/2)]>=m epsilon^2/16.

These two estimates give (1). Here m epsilon^2/16>=9L, so this failure probability is at most2e^-9L<beta/2. Zero acceptance never yields a completed run.

## Fully specified complete guarantee

The original certificate is sound except on probability beta/2 and gives

 ||D_M-G_a||_diamond<=nu a/2.

On the throughput-confidence event, ||G_a-G_ahat||_diamond=2|a-ahat|<=nu a/4. Therefore

 ||D_M-G_ahat||_diamond<=3nu a/4
 <=[3nu/(4(1-nu/8))]ahat<=6nu ahat/7<nu ahat.         (2)

Thus with confidence at least1-beta every strengthened certificate specifies the known channel G_ahat and certifies complete error at most nu ahat. The actual acceptance still obeys the original lower confidence bound a_L; moreover ahat=3a_L/2 exactly. This does not identify ahat with a source's nominal signal probability p.

## Composition and costs

The sufficient small-mismatch completeness premise is now q<=nu^2/6144, because the invoked verifier accuracy is nu/2. For the received unknown-orthogonal-reset trained receiver, use nu_train=nu/16 and supply acceptance floor p0/2. The already received training bridge, with target nu/2, gives precisely this premise and preserves the nu^-4 training exponent. Holdout still has expected/high-probability cost O(log(1/beta)/(a nu^2)) and deterministic cap O(log(1/beta)/(p0 nu^2)). No extra source calls beyond this adjusted holdout are required for estimating ahat.

All original fixed-decoder, independent fresh holdout, memoryless-source, no-entangled-probe, and no-observable-training-failure guards remain in force. This is a learned-reference-channel certificate, not a hidden-decomposition certificate or a guarantee for nonstationary future behavior.
