# Independent challenge and refinement of the joint-KL upper bound

## Disposition

The principal investigator's proposed core-truncation bound is correct, including its spectral constant and its general measurable-space scope. Its first asymptotic coefficient `(sqrt(K)+sqrt(J))^2` is conservative. Two refinements of the same argument improve the established upper coefficient first to `K+J`, and then to `max(K,J)`.

The final result below is an upper bound, not a matching lower theorem or a historical novelty claim. In particular, the fixed mixture weight may matter to the sharp coefficient; the pure-global endpoint already shows why sharpness must not be inferred from this upper bound alone.

This note concerns only this new joint-KL construction. It does not repeat the previous Section 6 review or reexamine the completed B3 work.

## 1. Assumptions and notation

Let pi and q be equivalent probability measures on a measurable space, with positive finite ratio `W=dpi/dq`. Assume population bounds

`D(pi||q)<=K` and `D(q||pi)<=J`,

for fixed positive constants K and J. Let G be the independence-MH kernel using proposal q and target pi. Let L be an arbitrary fixed pi-reversible Markov kernel, and fix `0<alpha<1`. Define

`C=(I+alpha G+(1-alpha)L)/2`.

This is a self-adjoint Markov contraction with spectrum in `[0,1]`. For every measurable event A, set `g=C^t 1_A`. Then `0<=g<=1` and `pi(g)=pi(A)`.

For any `B,R>e`, put

`S={1/B<=W<=R}`, `a=pi(W>R)`, `b=q(W<1/B)`.

Binary entropy contraction gives

`a<=K/(log R-1)` and `b<=J/(log B-1)`.

Also

`q(S^c)<=b+a/R`, `pi(S^c)<=a+b/B`.

The second entropy bound uses the reciprocal likelihood ratio under q; its orientation is important.

## 2. Check of the original BR argument

Suppose `s=pi(S)>0` and let `m=E_pi[g|S]`. Since `integral_S pi(g-m)=0`,

`q(g)-pi(g)=integral_S q(g-m)+integral_(S^c)(q-pi)(g-m)`.

On S, q is at most B pi. Cauchy--Schwarz and `q(S)<=1` give

`|integral_S q(g-m)|^2 <= B integral_S pi(g-m)^2`.

The conditional variance pair identity and the independence-MH form yield

`integral_S pi(g-m)^2 = [1/(2s)] integral_(SxS) pi(dx)pi(dy)(g(x)-g(y))^2 <= (R/s) E_G(g,g)`.

Thus the proposed central term `sqrt(BR E_G/s)` is valid.

For a centered indicator u, spectral calculus gives

`E_C(C^t u,C^t u)=integral_[0,1] lambda^(2t)(1-lambda) d sigma_u(lambda)`.

The maximum of the scalar factor is at most `1/(2t+1)`, while `||u||_2^2<=1/4`. Therefore

`E_C(C^t 1_A,C^t 1_A)<=1/[4(2t+1)]`.

Since `E_C >= (alpha/2)E_G`,

`E_G(g,g)<=1/[2 alpha(2t+1)]`.

These are exactly the proposed constants. The original bound

`TV(q C^t,pi)<=q(S^c)+pi(S^c)+sqrt[BR/(2 alpha s(2t+1))]`

is consequently correct. The finite conditional mean m requires s>0, which is guaranteed by appropriately small chosen entropy-tail budgets. No finite-state or discrete-spectrum assumption is needed.

## 3. First refinement: tails cost a maximum

For any m in `[0,1]`, write

`T=integral_(S^c)(q-pi)(g-m)`.

Because `-m<=g-m<=1-m`,

`T <= (1-m)q(S^c)+m pi(S^c)`,

and

`-T <= m q(S^c)+(1-m)pi(S^c)`.

Both are at most `max(q(S^c),pi(S^c))`. Therefore the original bound improves to

`TV(q C^t,pi)<=max(a+b/B,b+a/R)+sqrt[BR/(2 alpha s(2t+1))]`.

One may allocate both a and b nearly epsilon, rather than requiring their sum to be nearly epsilon. In the BR bound this already improves the leading epsilon-log-time coefficient to K+J. No cancellation assumption is involved; this is a deterministic bound valid for every bounded test function g and every m in `[0,1]`.

## 4. Second refinement: a fixed anchor replaces BR by a sum

Choose the fixed threshold

`M=exp(2K+1)`

and the anchor set `A0={W<=M}`. The entropy-tail bound gives

`s0=pi(A0)>=1/2`.

For the current test function g, let `m=E_pi[g|A0]`. This m is still in `[0,1]`, so the tail-maximum argument remains applicable. The anchor does not depend on B, R, t or the event A; only its conditional mean does.

The exact independence-MH form is

`E_G(g,g)=(1/2) integral pi(dx)pi(dy) (g(x)-g(y))^2/max(W(x),W(y))`.

Restrict the second coordinate to A0. On that set, the denominator is at most `max(W(x),M)`. Jensen's inequality in y gives

`E_G(g,g) >= (s0/2) integral pi(dx) (g(x)-m)^2/max(W(x),M)`.

This is a weighted anchor inequality. It does not need a lower likelihood-ratio bound on A0, an ordinary spectral gap, or a finite state space.

Now center the entire signed-measure difference at the same m:

`q(g)-pi(g)=integral_S pi(1/W-1)(g-m) + integral_(S^c)(q-pi)(g-m)`.

Weighted Cauchy--Schwarz and the anchor inequality yield

`|integral_S pi(1/W-1)(g-m)| <= sqrt[(2 E_G(g,g)/s0) I]`,

where

`I=integral_S pi max(W,M)(1/W-1)^2`.

For `W<=M`,

`max(W,M)(1/W-1)^2 <= M(1/W^2+1)`.

On S, `1/W<=B`, so

`integral_(S intersect {W<=M}) pi/W^2 <= B integral pi/W <= B`.

This portion of I is at most `M(B+1)`. For `W>M>1`,

`max(W,M)(1/W-1)^2 = W-2+1/W <= W<=R` on S.

Its integral is at most R. Hence

`I<=M(B+1)+R`.

Combining with the established spectral smoothing estimate gives the refined general bound

`TV(q C^t,pi) <= max(a+b/B,b+a/R)`

`                 + sqrt[(M(B+1)+R)/(alpha s0(2t+1))]`,

with `s0>=1/2` and `M=exp(2K+1)` fixed over the whole admitted class.

This bound avoids division by pi(S). It remains meaningful even for choices where S is empty, although the chosen useful tail budgets ensure substantial retained mass anyway.

## 5. Uniform asymptotic consequence

For fixed K,J>0 and fixed alpha>0, let the supremum range over all pi,q,L satisfying the assumptions. Put

`B=R=t/(log t)^4`

for sufficiently large integer t. Then B,R>e. The tail maximum, multiplied by log t, has limsup at most `max(K,J)`; the cross terms a/R and b/B vanish faster. The central term is `O_(K,alpha)((log t)^(-2))`, uniformly over pi,q,L, because M is fixed and s0>=1/2.

Therefore

`limsup_(t->infinity) log(t) sup_(pi,q,L) TV(q C^t,pi) <= max(K,J)`.

For the corresponding worst-case proposal-start mixing-time envelope this implies

`limsup_(epsilon->0) epsilon log T_(K,J,alpha)(epsilon) <= max(K,J)`.

The usual harmless convention T>=1 avoids taking log 0. Markov contraction makes the fixed-chain error nonincreasing, and the uniform bound gives the inverse-envelope implication.

This is strictly stronger than the initially proposed `(sqrt(K)+sqrt(J))^2` upper coefficient. It is not a proof that the new coefficient is sharp.

## 6. An explicit finite budget, if required

For `0<epsilon<=1/2`, choose any `0<rho<1` and set `u=(1-rho)epsilon`. Let

`R=max(exp(1+K/u), 2/rho)`,

`B=max(exp(1+J/u), 2/rho)`,

`M=exp(2K+1)`, `D=M(B+1)+R`.

The tail bounds give a,b<=u, while `1/R,1/B<=rho/2`. Consequently

`max(a+b/B,b+a/R) <= u(1+rho/2) <= epsilon(1-rho/2)`.

Because s0>=1/2, the central term is at most `sqrt[D/(alpha(t+1/2))]`. It is therefore sufficient to choose the integer budget

`t >= ceil(4D/(alpha rho^2 epsilon^2))`.

This makes the central term at most `rho epsilon/2`, yielding total TV at most epsilon. Taking `rho=sqrt(epsilon)` recovers the leading coefficient `max(K,J)` for fixed positive K,J.

The theorem counts lazy-kernel applications. In the natural implementation, the expected later global and local updates are respectively `alpha t/2` and `(1-alpha)t/2`, plus one initial q draw. Actual running time also includes each kernel's own proposal, target-evaluation and numerical costs.

## 7. Endpoints and limitations

- If either K=0 or J=0, the corresponding zero KL forces pi=q. Proposal initialization is then stationary, so the exact endpoint is trivial. The nonzero formula need not be optimized there.
- The asymptotic statement keeps K,J and alpha fixed. If these depend on epsilon, additional uniformity analysis is needed; an exponentially small alpha can change the leading cost coefficient.
- Alpha=0 is excluded: an arbitrary local kernel may be the identity. At alpha=1 the direct pure-global result has coefficient K, so the displayed max(K,J) bound need not be sharp.
- L must be a fixed pi-reversible Markov kernel. State-dependent mixture weights or uncontrolled adaptation are not covered merely because each component is invariant separately.
- The proof works on general measurable spaces using the Hilbert-space spectral theorem for bounded self-adjoint operators. No diagonalization of a finite transition matrix is assumed.
- Exact kernel implementation and externally certified population KL bounds are assumptions. Finite training losses, approximate ratios and floating-point MH decisions require separate error accounting.
- The result is a conditional mixing guarantee for the specified sampler, not a universal lower bound for sampling pi from every representation and not an observed application speedup.

The most immediate unresolved mathematical obligation is a matching lower bound or a sharper upper constant with its alpha dependence. The anchor proof establishes only the stated upper envelope and should be presented with that scope.

## 8. Check against the principal's integrated source

I read the completed `JOINT_KL.md` once on 21 October 2026 at 11:52 UTC. Reviewed snapshot: 8,826 bytes, SHA256 `2655f172b4d419811cea6595fd91a0b05d9072adb69b0753089b0c4b6011bd44`.

Its final bound, explicit all-epsilon budget, time-domain asymptotic and general-space qualifications correctly transcribe the checked argument. Its displayed explicit budget uses the simpler choices `R=exp(1+3K/epsilon)`, `B=exp(1+3J/epsilon)`, `t=ceil(4U/(alpha epsilon^2))`, with `U=M(B+1)+R`. This is valid: the tail contribution is below epsilon/2 and the central contribution is at most epsilon/2. That finite budget is conservative; the later time-domain argument separately supplies the optimal upper coefficient claimed in the source.

One nonmathematical editing remnant was reported to the principal: the standalone line `because integral_S (dq/dpi)^2 dpi <= B q(S)<=B.` after the outside-mass paragraph belongs to the superseded product-core argument and should be removed or relocated. It is true but unconnected in the integrated anchor proof. Removing that line does not change any reviewed assumption or argument.

The principal's q-measure presentation of the low-weight part of (2.5) is also valid. On the clipped core, `integral q/W <= B`, `integral qW <= 1`, and the term `-2 integral q` can be dropped for an upper bound, giving `M(B+1)` exactly.

For the combined conclusion I also read `JOINT_KL_FUNNEL_NOTE.md`: 13,282 bytes, SHA256 `c5002daf81f177c0c180248d482fbca7800be2833b935cd2ac631e41b578225e`. The fixed skew-edge proposal gives entrance mass `(1-alpha)rho b`, local escape `rho s/p`, and a valid reverse-KL lower exponent `(1-alpha)rho J`. Every fixed rho<1 is admissible, so the supremum class permits the limiting lower coefficient `(1-alpha)J`. The binomial-subordination formula preserves that coefficient under laziness. The ordinary two-state family with L=I supplies K while its reverse KL tends to zero.

Consequently the principal's integrated bracket

`max(K,(1-alpha)J) <= liminf epsilon log T <= limsup epsilon log T <= max(K,J)`

is supported by the supplied arguments. In particular its exact coefficient K for `0<J<=K` follows. The gap when `J>K` remains explicit; neither this review nor the principal's statement claims it has been closed.
