# Independent challenge: an epsilon-dependent logarithmic IMH prefix

Reviewer: `/root/prefix_literature`, 21 October 2026. This is a separate mathematical review after completion of the literature task. It targets the changing-prefix asymptotics and accounting, not the already reviewed fixed-prefix theorem or the old joint-KL gap.

## Verdict and dependencies

**Accept the proposed changing-prefix upper and lower asymptotics, conditional on the stated finite-time prefix inequality and low-tail estimate.** Their asymptotic use is uniform, the integer rule supplies a genuine fixed error margin, and the two-state lower construction survives a logarithmic prefix. No blocking gap was found in these steps.

One notation correction is necessary: the actual tail probability `b_h=q(W<h)` does not equal `b_*+O(h log(1/h))`. Its **uniform entropy upper envelope** has that expansion. The proof must use `b_h <= bar_b_h` and expand `bar_b_h`. This correction was sent to the owner before this report.

This review does not independently certify the finite-time inequality's derivation or the fixed-N residual floor. Those are separate proof obligations. The cost statement below is for a fixed number of lazy-mixture steps; it is not a theorem for stopping at an exact number of random-mixture global proposals.

## 1. Contract and proposed rule

Fix `K>0`, `0<alpha<1`, `beta=1-alpha`. Let `pi` and `q` be equivalent probability measures, `W=dpi/dq`, `D(pi||q)<=K`, `G` ordinary independence MH, and `L` any fixed pi-reversible kernel. Set

`C=(I+alpha G+beta L)/2`, `mu_N=q G^(N-1)`.

Thus `N` counts iid proposal candidates, including the initial draw; there are `N-1` prefix transitions. A reverse-KL budget is not needed for the claim reviewed here. The accepted original joint-KL theorem remains unchanged.

Define

`b_*=1-exp(-K)`, `lambda=-log(b_*)`,

`gamma=beta/(1-alpha b_*)`, `F_N=gamma b_*^N`,

`N(eps)=max(1, ceil(log(gamma/eps)/lambda)+1)`.

All constants are fixed as eps tends to zero. In particular `0<b_*<1`, `lambda>0`, and `beta<gamma<1`.

## 2. The ceiling rule has a fixed margin

Put `x=log(gamma/eps)/lambda`. If `x>0`, then `N>=x+1`; hence

`F_N=gamma exp(-lambda N) <= gamma exp(-lambda(x+1)) = b_* eps`.

If `x<=0`, then `eps>=gamma` and the maximum with 1 gives the same inequality. Consequently

`F_N <= b_* eps`

for every positive eps, not just asymptotically. Also

`N(eps)=log(1/eps)/lambda+O_(K,alpha)(1)`.

The additional candidate after the ceiling is important to this proof: it provides the nonvanishing relative error margin `1-b_*=exp(-K)`. A rule that only ensures `F_N<=eps` would not, by itself, absorb positive lower-order terms in a finite-time upper bound.

This is a sufficient rule, not a claim that its extra integer is always the smallest possible prefix. Equality at a fixed-N residual floor is a separate boundary question.

## 3. Uniform entropy bound on the low-weight probability

For `0<h<1/2`, write `b_h=q(W<h)` and `s=pi(W<h)`. Then `s<=h b_h<=h`. Binary data processing gives

`K >= s log(s/b_h)+(1-s)log((1-s)/(1-b_h))`

`  >= -H_2(s)-(1-s)log(1-b_h)`

`  >= -H_2(h)-(1-h)log(1-b_h)`.

Here binary entropy increases on `[0,1/2]`; the dropped term `s log(1/b_h)` is nonnegative. Therefore

`b_h <= bar_b_h := 1-exp(-(K+H_2(h))/(1-h))`.

With `h=eps^2`, expansion of this deterministic envelope yields

`bar_b_h = b_* + O_K(eps^2 log(1/eps))`.

This is uniform over all admitted pi,q. It is not an asymptotic equality for their actual low-tail probabilities.

## 4. Prefix tail estimate with changing N

Use the supplied finite bound, with `D={W<1/B}`, `b=q(D)`, `d=mu_N(D)`:

`d <= b_h^N + [b/(B h)] sum_(j=0)^(N-2) b_h^j`.

For `1/B<h`, `b<=b_h<=bar_b_h`. Since `bar_b_h` tends to `b_*<1`,

`d <= bar_b_h^N + O_K(1/(B eps^2))`.

Let `delta_h=bar_b_h-b_*`. Because `N=O(log(1/eps))`,

`N delta_h=O_K(eps^2 log^2(1/eps))=o(1)`.

Thus

`bar_b_h^N = b_*^N [1+O_(K,alpha)(eps^2 log^2(1/eps))]`.

For `kappa_b=beta/(1-alpha b)`, monotonicity gives

`kappa_b <= kappa_(bar_b_h) = gamma+O_(K,alpha)(delta_h)`.

Combining these estimates,

`kappa_b d <= F_N [1+O_(K,alpha)(eps^2 log^2(1/eps))]`

`              + O_(K,alpha)(1/(B eps^2))`.

In particular the dangerous tail is bounded by `b_* eps+o(eps)` once `B` grows at the specified exponential scale. No exchange of a pointwise limit and an instance supremum occurs: every displayed error has constants depending only on fixed parameters.

## 5. Main mixing scale and error budget

For any fixed `zeta>0`, choose

`t=ceil(exp((K+zeta)/eps))`, `B=R=t/(log t)^4`, `h=eps^2`.

For sufficiently small eps, `B,R>e`, `1/B<h<1/2`, and

`log t=(K+zeta)/eps+o(1)`.

Take the supplied anchor `M=exp(2K+1)` and `s0=pi(W<=M)>=1/2`, and set

`U_N=M(N^2 B+1)+N^2+R`,

`Delta_N=sqrt(U_N/[alpha s0(2t+1)])`.

Then

`Delta_N=O_(K,alpha,zeta)(N/(log t)^2)`

`       =O_(K,alpha,zeta)(eps^2 log(1/eps))=o(eps)`.

For `a=pi(W>R)`, the forward-KL tail bound gives

`a <= K/(log R-1)` and `a/eps <= K/(K+zeta)+o(1)`.

The prefixed low tail satisfies `d=O(eps)`. The remaining supplied terms obey

`d[alpha(Delta_N+a/R)+eta_t]/(1-alpha b)=o(eps)`,

`b/B=o(eps)`, `N a/R=o(eps)`.

The denominator is at least `beta>0`, and `eta_t=O(t^(-1/2))`. The injection remainder `1/(B eps^2)` is exponentially small compared with every fixed positive power of eps.

Consequently the stated finite-time inequality implies

`TV(mu_N C^t,pi)/eps <= max(K/(K+zeta),b_*)+o(1)`.

Both entries of this maximum are strictly less than one. This proves one common sufficient integer time for every admitted instance, for all sufficiently small eps. Therefore, defining the worst-case first sufficient post-prefix time by `T_safe(eps)`,

`limsup_(eps->0) eps log T_safe(eps) <= K`.

The same coefficient holds if the deterministic prefix length `N-1` is included in total transition count. This argument does not require a uniform rate in K, alpha or zeta; they are fixed. Such an additional claim would need separate estimates.

## 6. Matching two-state lower bound

Fix `ell>1`. For small eps let

`p=ell eps`, `delta=exp(-K/p)`, `r=p delta`,

`pi=(p,1-p)`, `q=(r,1-r)`, `L=I`.

The pair is equivalent, and

`D(pi||q)=K+(1-p)log((1-p)/(1-r))<K`.

The reverse divergence is at most `-log(1-p)`, hence tends to zero; the same family is also compatible with any fixed positive reverse-KL budget if one is retained.

The nontrivial eigenvalues of G and C are respectively `1-delta` and `1-alpha delta/2`. Thus the exact TV distance after the prefix and t hybrid steps is

`(p-r)(1-delta)^(N-1)(1-alpha delta/2)^t`.

Since `N=O(log(1/eps))`, `(N-1)delta->0`; the prefix does not change its leading amplitude. Choose any fixed `0<c<log(ell)` and set

`t=floor(2c/(alpha delta))`.

Then the exact TV divided by eps tends to `ell exp(-c)>1`, while

`eps log t -> K/ell`.

TV is nonincreasing in t under the pi-invariant C. This insufficient time therefore gives `liminf eps log T_safe(eps)>=K/ell`. Letting ell decrease to one yields

`liminf eps log T_safe(eps)>=K`.

Together with the upper bound, the proposed logarithmic-prefix operation has coefficient exactly K. The lower instance depends on eps; it does not claim that a single fixed target/proposal pair realizes this coefficient.

## 7. Resource and implementation interpretation

For t deterministic mixture steps, the full operation uses N prefix candidates, then an expected `alpha t/2` additional global candidates and `beta t/2` local-kernel calls. The number of actual additional global proposals is binomial, and is bounded above by t. Thus both expected proposal count and the elementary deterministic upper bound have logarithmic coefficient K. They are not the same finite resource contract.

Stopping when a prescribed number of global proposals has occurred creates another random-time operation. No guarantee for that operation follows merely by substituting its expected t into this proof.

At fixed K the prefix is logarithmic in precision. Its coefficient is not uniformly modest: `1/lambda` grows like `exp(K)` when K is large. The proof establishes neither lower wall time than pure IMH nor finite-time dominance. The costs of evaluating q, target ratios and L remain application-dependent and unmeasured here.

All theorem formulas are in ideal real arithmetic. A numerical implementation of the ceiling rule must avoid rounding downward near an integer boundary; otherwise the explicitly proved error margin can disappear. The population K budget and alpha are assumed, not inferred from finite training loss. The diagnostic below uses exact rational arithmetic for its special parameter choice; it is not a validation of arbitrary floating-point MH transitions.

## 8. Targeted exact calculation and limits

`prefix_scaling_boundary.py` checks candidate/update accounting at K=log(2), alpha=1/2, where `b_*=1/2` and `gamma=2/3`. It tests eps at, immediately below and immediately above `gamma*2^(-r)` for r=1,2,10,100,1000. All 15 exact Fraction checks passed, including `F_N<=b_* eps` and the expected ceiling jump.

Observed run: approximately 0.00848 seconds wall, 0.00848 seconds CPU, peak RSS 8832 KiB. These are the script's own observed process measurements, not the total research cost. The output is `prefix_scaling_boundary_results.json`.

No old funnel plots, old matrix suite, B3 or R3 operation was rerun. The universal asymptotic conclusion rests on the analytic argument above and its explicitly named finite-time dependencies, not on the integer diagnostic.
