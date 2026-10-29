# Tracking a predictable drifting symmetry frame: finite fixed-share construction
2026-10-29. New working proof, not yet receiving-reviewed. Uses accepted gap-free feedback and robust v4 loss geometry. This file is separate from all frozen accepted sources.

## What changes
Allow the hidden true relative frame C*_{i,t} to change with time and actual causal history. It must be fixed before the current private probe/candidate/role choices; its source operations at that round commute with its current twisted star swaps. No single frame is required to explain all past calls. The source retains arbitrary memory. Outer good branches remain identity in the CURRENT encoder's logical coordinates, so the logical outer register is unchanged by candidate-frame changes.

A prescribed predictable comparator path is different from retrospectively minimizing a path using future random outcomes. The latter is not covered by the unbiasedness step below. Current role/key privacy and the full source boundary are unchanged. The complete pre-role scheduling in robust_gapfree_oracle_20261029/FINITE_SAMPLER_SCHEDULING_CLARIFICATION.md is required, including all prospective role keys and their candidate-independent ranges; candidate-only cap neutrality is insufficient. Guarded accepted soundness remains model-free; only readiness uses drift/defect promises.

## Exact finite fixed-share update
Fix one rational SO3 net of sizeM, probe probabilityp, rational eta<=p/2 and share alpha=A/B in[0,1/2]. Use the same shifted feedback ell_t(j)=1_probe fhat_t(j)/p, in[0,1/p]. First form v_j=w_j(1−eta ell_t(j)), then
 w'_j proportional to (1−alpha)v_j+(alpha/M)sum_k v_k.
The share transition is applied on EVERY active round, including service/validation rounds with zero feedback. After stopping, the proof may continue hypothetical zero-feedback share transitions; unlike ordinary MW, these need not preserve weights. No physical calls or computation after stopping are required.

This is the forward update for a prior on expert paths with uniform first expert and transition Q(j|i)=(1−alpha)1[j=i]+alpha/M. With common integer loss-update factorsF_j, all weights can be kept as integers:
 W'_j=(B−A)M W_j F_j + A sum_k W_k F_k.
The common denominator cancels. Bit widths gain only O(log(BM)) per update beyond the prior finite learner; the implementation remains polynomial but expensive. Capped exact weighted sampling is a candidate-independent neutral stop, as in robustv4.

For any expert path j_1,...,j_T with at mostS switches, the deterministic potential argument yields
 sum_t <w_t,ell_t>−sum_t ell_t(j_t)
 <= K(S,alpha)/eta+eta sum_t ell_t(j_t)^2,
 K(S,alpha)=lnM+S ln(M/alpha)+(T−1−S)ln[1/(1−alpha)].
For alpha=0 use only constant paths andK=lnM. The displayedK bounds minuslogprior; the true stay probability is larger and only improves the result.

This deterministic inequality holds simultaneously for paths. If j_t is predictable before its current probe, conditional unbiasedness applies to its chosen feedback even if the path depends on earlier actual records. Thus expected true-delta regret is at most
 45[K(Sbar,alpha)/eta+eta T/p]
for a deterministic almost-sure bound S<=Sbar. No expectation of a hindsight minimum is substituted. Gamma_t/frames may depend on the actual stopped history; sampler-abort rounds have zero loss/feedback for every expert.

For1<=Sbar<=T−1 choose alpha=min(1/2,Sbar/(T−1)). Since alpha<=1/2, K is increasing inS, justifying Sbar. When Sbar<= (T−1)/2,
 K=(Sbar+1)lnM+(T−1)h(Sbar/(T−1)),
whereh is binary entropy in natural logarithms. A rational eta within a constant factor ofmin(p/2,sqrt(pK/T)) gives O(sqrt(TK/p)+K/p) regret. This is distinct from share1/T, whose unnecessary SlogT term cannot alone establish the full sublinear-variation statement.

## Predictable variation budget and net approximation
Let a deterministic boundPbar cover the actual path variation
 P_T=sum_{t=2}^T max_i ||C*_{i,t}−C*_{i,t−1}||_F.
Only active rounds are counted; after stopping extend frames constantly and losses byzero. Build a predictable segment anchor: start at the current true frame; replace it whenever any current star frame is more thanepsilon from its anchor. Distinct replacement segments each consume more thanepsilon variation, so there are at mostmin(T−1,ceil(Pbar/epsilon)) switches. Round each anchor to one fixed nearest rational-net point of radiusepsilon, with deterministic ties. Current true frame and rounded anchor differ by at most2epsilon. Under exact current symmetry,
 sum_{t,i} delta_{i,t}(rounded anchor) <=18(n−1)T epsilon².
The learner never needs to know the anchors or hidden frames. They are predictable comparators in the proof; the numerical design uses only the declared drift bound and net radius.

Consequently total expected selected star loss is bounded by
 18(n−1)T epsilon²
 +45(n−1)[K(Sbar,alpha)/eta+eta T/p]. (D1)
Here common segment switches bound each edge path. If current symmetry has additional comparator defectGamma, replace the first term by (sqrtGamma+sqrt(18(n−1)T epsilon²))², provided the comparator path remains predictable. This is a direct conditional-expectation extension, not a hindsight selection.

## When the average loss vanishes
For fixedn,p and a declared boundPbar_T=o(T), take an accurately rounded rational epsilon on the order of
 max(T^(−1/4),(Pbar_T/T)^(1/5)), capped at a constant.
IfPbar=0 use the static path. Then Sbar/T→0, lnM=O(ln(1/epsilon)), and K/T→0; the entropy term usesh(Sbar/T), notlogT times the switch rate. Therefore(D1)/T→0 for every sublinear declared variation budget. For moderate nonzero Pbar, the explicit order is
 O(T^(3/5) Pbar^(2/5) sqrt(log(T/Pbar)))
plus static/horizon rounding terms; the nonasymptotic bound(D1), not this abbreviated order, governs endpoint regimes.

This construction is budgeted: it knows a valid variation envelope for choosingepsilon,share andlearning rate. It does not yet claim adaptation to unknown drift budgets or arbitrary fast drift. Exactly computable rational conservative bounds for all parameters suffice; no irrational sampling oracle is introduced.

## Operational transfer
Insert(D1), or its defect extension, for total lossG in the same readiness bound
 Pr[ready]>=1−a(D/d)G/(b+1)−exp(−sT/8)−delta_sampler.
The matching/outer-code soundness is unchanged. Positive fixed-port asymptotic rate additionally requires the separate fixed-port outer-code compiler; growing-port and fixed-port statements must not be conflated. No future-frame extrapolation follows from low past variation.
