# Independent challenge: KL-controlled safe initialization

## Scope and verdict

I checked the root's proposed initialization lemma independently. Under the stated assumptions, all four claims hold with the stated constants:

- `M = exp(2K + 1)` gives `E_q min(W,M) >= 1/2`.
- The denominator failure probability is at most `delta_N = exp(-N/(16M))`.
- The successful output subprobability measure is dominated by `4 pi`.
- The whole output law has hockey-stick divergence `E_4(mu_N || pi) <= delta_N` and admits the claimed mixture decomposition.

The normalization-free implementation is valid. The externally supplied population KL bound is a substantial assumption; a finite empirical training loss does not supply it. This is a safe initialization construction, not a conclusion that the initialized law is within `delta_N` in total variation of the target.

I found no constant or normalization defect in the lemma. The direct SIR proof below also makes its scope on general measurable spaces explicit. A current primary theorem establishes that pure independence MH is no worse than SIR for every convex f-divergence at the same proposal budget on finite positive state spaces. Consequently, SIR should not be advertised as outperforming pure MH for this warm-start objective. The construction is a reusable consequence of elementary truncation/concentration and the published comparison, not a demonstrated novelty claim.

## Assumptions

Let `q` and `pi` be probability measures on a measurable space. Let `W = d pi / d q`, and assume `0 < W < infinity` q-almost everywhere, `E_q W = 1`, and

`D(pi || q) = E_q[W log W] <= K < infinity`, with `K >= 0`.

The strict positivity assumption prevents an all-zero candidate denominator. If zero weights are allowed, a specified fallback for the all-zero pool must be included in the bad event and its probability accounted for; the present proof should not silently omit that event.

Draw `X_1,...,X_N` independently from q, for a deterministic positive integer N. Conditional on this pool, select index J with probability `W(X_J)/sum_i W(X_i)`. Denote the selected state's law by `mu_N`.

All logarithms are natural. The hockey-stick divergence convention used here is

`E_C(mu || pi) = sup_A [mu(A) - C pi(A)] = integral (d mu - C d pi)_+`, for `C >= 1`.

## 1. Truncation mass: a shorter proof, including K = 0

Define `phi(w) = w log w - w + 1` for positive w. This convex nonnegative function satisfies `E_q phi(W) = D(pi || q)` because `E_q W = 1`.

For `M >= 1`, if `w >= M`, then

`phi(w) - phi(M) = integral_M^w log t dt >= (w-M) log M`.

If `w <= M`, the right hand side of `log(M) (w-M)_+` is zero and `phi(w) >= 0`. Therefore, everywhere,

`phi(w) >= log(M) (w-M)_+`.

For `M > 1` this yields

`E_q (W-M)_+ <= K/log M`,

and hence

`c_M := E_q min(W,M) = 1-E_q(W-M)_+ >= 1-K/log M`.

With the proposed `M = exp(2K+1)`,

`c_M >= (K+1)/(2K+1) > 1/2`.

This proves the requested weaker bound without dividing by K. In particular, the K=0 edge case is covered directly. The constants are conservative: for K>0, `M=exp(2K)` already suffices for `c_M >= 1/2`, but the root's stated choice is valid and avoids a separate endpoint convention.

## 2. Denominator concentration

Set `Y_i = min(W(X_i),M)/M`. These are independent variables in `[0,1]`. Their sum has mean

`m = N c_M/M >= N/(2M)`.

Let `G = {sum_i min(W(X_i),M) >= N/4}`. Its complement satisfies

`G^c subset {sum_i Y_i < m/2}`,

because `N/(4M) <= m/2`. The bounded-variable multiplicative Chernoff inequality gives

`P(G^c) <= exp(-m/8) <= exp(-N/(16M)) = delta_N`.

The first inclusion and the final inequality have the correct directions. No boundedness assumption is placed on W itself; only the proof's clipped variables are bounded. The candidates must be iid from q for this concentration argument as written.

## 3. Output submeasures and normalization

Define

`mu_G(A) = E[1_G sum_i W(X_i) 1_A(X_i) / sum_j W(X_j)]`.

On G, the actual denominator is at least the clipped sum, hence at least `N/4`. Thus

`mu_G(A) <= (4/N) E[sum_i W(X_i) 1_A(X_i)] = 4 pi(A)`.

Let `mu_B` be the same expression with `1_(G^c)`. Conditional selection probabilities sum to one, so

`mu_G(space)=P(G)=1-b`, `mu_B(space)=P(G^c)=b`, and `0 <= b <= delta_N`.

Therefore `mu_N=mu_G+mu_B`, and for every measurable A,

`mu_N(A)-4 pi(A) <= mu_B(A) <= b`.

Taking the supremum proves `E_4(mu_N || pi) <= b <= delta_N`.

Since `delta_N<1`, the good measure has positive mass. Put `nu=mu_G/(1-b)` and, when b>0, `eta=mu_B/b`. Then

`mu_N=(1-b)nu+b eta`, with `nu <= [4/(1-b)] pi`.

When b=0, eta can be any probability measure, since its coefficient is zero. The use of `4/(1-b)`, not 4, for the normalized good law is essential. The original root statement handles this correctly.

The event G need not be observed or checked by the algorithm. In particular, its definition using normalized W does not require the algorithm to know the target normalizer.

## 4. Algorithm access and complete relevant cost

The actual SIR operation only needs iid samples from q and unnormalized importance weights `u(x)=tilde_pi(x)/q(x)` at those sampled points. The unknown normalizer multiplies every weight by the same constant and cancels from all conditional selection probabilities.

For a desired bad-component bound `delta in (0,1)`, the displayed proof permits

`N = ceil(16 exp(2K+1) log(1/delta))`.

This requires N independent proposal draws, N evaluations of the unnormalized importance ratio (or equivalent recorded weights), and linear scalar selection work. Ordinary weighted reservoir selection gives the same conditional law with one retained candidate and one running sum, plus N-1 uniforms. Batch storage is optional. Exact numerical selection is an ideal-arithmetic statement; finite precision, underflow and errors in evaluating q or the unnormalized target require separate accounting. Log-space implementations reduce arithmetic problems but do not by themselves certify a prescribed total variation error.

K is a certified bound on a population quantity under pi. It is not computable from arbitrary finite q-candidate observations with a distribution-free guarantee merely because those observations have a small empirical loss. The lemma must not be advertised as solving that certification problem. It also does not eliminate the exponential dependence on K.

The proof provides an approximately warm law. It does not prove that `TV(mu_N,pi) <= delta_N`: the normalized good component may still differ substantially from pi while having bounded density.

## 5. Transfer to subsequent stationary kernels

For any pi-invariant Markov kernel P, positive measure order is preserved:

`mu_G P <= 4 pi P = 4 pi`.

The bad component retains total mass b. Thus `E_4(mu_N P || pi) <= b` for any deterministic sequence of pi-invariant kernels, including a fixed local/global hybrid. The same mixture decomposition survives with transformed good and bad laws.

This preservation is not a mixing-rate theorem. A later convergence result still needs its own assumptions on the hybrid kernel. In particular, adding local steps does not automatically preserve pure IMH's special finite-budget ordering relative to q-started SIR; the warmness argument is a different, valid mechanism.

## 6. Existing pure-IMH dominance and attribution boundary

Primary source: Alexey Kurennoy, Ramil Yarullin and Fergal Reid, *Metropolis-Hastings Dominates Importance Resampling for Policy Composition*, arXiv:2610.03480v1, 2 October 2026.

URL: https://arxiv.org/html/2610.03480v1

Theorem 1 compares N-candidate SIR with independence MH initialized at the first of the same N iid proposals and run for N-1 updates. For finite positive state spaces and positive importance weights, MH has no larger convex f-divergence from the target. The theorem is not restricted to autoregressive proposals. Choosing `f(t)=(t-4)_+` gives the E_4 comparison directly.

Hence, in that source's finite-state scope, the root's bound implies

`E_4(H_N || pi) <= E_4(S_N || pi) <= delta_N`.

Pure IMH therefore supplies the same certified approximate warm start at the same proposal/weight budget. It also has a constant-storage implementation. The SIR calculation is useful as a transparent proof device; a claim that this initialization is superior to ordinary pure IMH is contradicted by the cited theorem.

The source does not explicitly state the root's particular forward-KL-to-warmness constants in the passages inspected. I do not claim a new theorem from that absence: the ingredients are elementary and the MH consequence is immediate once the SIR lemma is written. Its defensible status is an internally proved, constructively reusable warm-start guarantee with published comparison machinery correctly attributed.

## 7. General-space extension of the needed E_4 comparison

The direct SIR proof above already holds on the root's general measurable space. The cited theorem itself explicitly uses finite support. If the root wants to apply its MH consequence generally, the following approximation supplies the missing extension for E_4 without asserting that the source stated it.

Take an increasing sequence of finite partitions of the positive weight W, with dyadic resolution tending to zero and the upper truncation level tending to infinity. Let `F_m` be their sigma fields and `W_m=E_q[W|F_m]`. Then W_m is finite-valued, positive, has mean one, and converges to W almost surely and in L1. Define `pi_m=W_m q`.

On each finite weight partition, both SIR and IMH using W_m preserve the conditional q-law within a cell. Their comparison reduces exactly to the cited finite-state theorem on the cells. Therefore `E_4(H_(N,m)||pi_m) <= E_4(S_(N,m)||pi_m)`.

For fixed N, couple all algorithms using the same iid candidate states and uniforms. SIR's normalized candidate weights converge almost surely because all limiting weights are positive and finite. Its output laws therefore converge in total variation. Each of the finitely many IMH acceptance probabilities also converges; an independent uniform equals a limiting threshold with probability zero. Thus the selected index agrees eventually almost surely, and the MH output laws converge in total variation. Also `TV(pi_m,pi) = E_q|W_m-W|/2 -> 0`.

Finally, the variational definition gives

`|E_4(mu||pi)-E_4(mu'||pi')| <= TV(mu,mu') + 4 TV(pi,pi')`.

Passing to the limit proves the required E_4 dominance on the general measurable space. This argument extends only the needed finite, continuous hockey-stick functional here; it does not silently assert convergence of every unbounded f-divergence.

## Final independent disposition

The proposed constants and mixture normalization are sound. The safe initializer can be used as an explicit prephase before a separately justified pi-invariant hybrid. Use pure IMH as the strongest ordinary matched-budget initializer, or present SIR as a proof mechanism with its dominance relationship disclosed. Keep the population-KL certificate, finite-precision assumptions and subsequent kernel's mixing obligations explicit. No standalone novelty or practical speedup is established by this lemma.
