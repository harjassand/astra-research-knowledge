# Candidate theorem: a sharp stochastic-explosion bifurcation at balanced conversion and immigration rates

**Date:** 2026-10-08 (Australia/Brisbane)  
**Astra source pinned:** `687dfc0640ee80654bcbdbe38cb13d6e1f1586ce`  
**Investigation:** one investigator, no parallel subagents. Independent derivation and numerical finite-generator tests.  
**Status:** internally derived full proof candidate, **not** externally reviewed, formally verified, or cleared for historical novelty. Not a field-breaking claim. This file lives on a research branch; do not silently upgrade immutable source-card statuses or merge without review.

## Motivation and prior capital

Astra `state/2026-10-08-stochastic-universality/RESULT_AND_RESTART.md` proved the unequal-rate cases of the base network
```
0 -> B           rate lambda
B -> A           rate mu * B
A + 2B -> 0      rate kappa * A * B * (B-1)
```
and its catalytic translations, but explicitly left the balanced line `mu=lambda` **unclassified**. Its deterministic permanence and strongly endotactic geometric claims are inherited, not independently fully reconstructed in this note. The stochastic balanced-rate return chain and explosion dichotomy below are the new candidate addition.

The general (1/x)-drift recurrence threshold is **classical**: J. Lamperti (1959), and modern Lo–Menshikov–Wade (Stochastic Processes and Their Applications 170, 2024, 104260, DOI 10.1016/j.spa.2023.104260). Strongly endotactic yet stochastic-explosive examples are **known**: Anderson–Cappelletti–Kim–Nguyen, *Tier structure of strongly endotactic reaction networks*, SPA 130 (2020), 7218–7259, DOI 10.1016/j.spa.2020.07.012. Exact priority of the following **specific network and parameter boundary** is **UNKNOWN**.

## Precise theorem candidate

Fix `lambda=mu>0`, `kappa>0` and integer `p>=0`. Translate each source and product complex above by `p A`, retaining the same rate constants. The translated network is

```
pA -> pA+B
pA+B -> (p+1)A
(p+1)A+2B -> pA .
```

Use **stochastic falling-factorial propensities** (no factorial denominators): respectively
`lambda*(A)_p`, `lambda*(A)_p*B`, and `kappa*(A)_(p+1)*B*(B-1)`.
Here `(A)_p=A(A-1)...(A-p+1)`, `(A)_0=1`.

For any finite initial state with `A>=p` and `B>=0`, let `T` denote the minimal CTMC's explosion time. Then the proposed **complete balanced-rate classification** is

```
                   P(T<infinity) = 1  iff  kappa < 2*lambda AND p >= 3;
                   P(T<infinity) = 0  otherwise.
```

States `A<p` (when `p>0`) are absorbing and do not explode. At the **borderline kappa=2*lambda**, nonexplosion holds for **every** p. In the un-translated base chain `p=0`, the embedded `B=0` return chain is transient if `kappa<2*lambda`, and **null recurrent** if `kappa>=2*lambda`. The `p=1,2` translated chains are nonexplosive even when their embedded chain is transient.

Every translated reaction graph is strongly endotactic by translation invariance; its deterministic mass-action vector field is `A^p` times the original vector field, and therefore has the same positive orbits and globally attracting equilibrium as the inherited original system. These deterministic assertions have an explicit provenance dependency on the earlier Astra result.

## Proof candidate, Step 1: exact return embedding and uniform tail

In the **base chain** write `a=A`, `b=B` and jump rates
```
(a,b) -> (a,b+1)       lambda
(a,b) -> (a+1,b-1)     lambda*b
(a,b) -> (a-1,b-2)     kappa*a*b*(b-1)
```
(the last only when enabled). Starting at `B=0`, define `tau_n` as successive visits to `B=0` separated by at least one birth event, and `X_n=A(tau_n)`.

Couple the `B` population **below** an immigration-death chain `B^*` with immigration `lambda` and independent per-particle deaths at rate `lambda`: couple births and conversions, and add the two-particle annihilation in the original only. From `B^*(0)=1` the return time to zero, and the number of jumps before return, have an exponential moment: the embedded nearest-neighbor walk has birth probability `1/(b+1)` at `b` and a strict geometric Lyapunov drift at large `b`; finite-state renewal then provides an exponential return-time moment. A Poisson exponential martingale bounds the number of immigration events before this return. Original conversion/annihilation counts are at most a constant times (one plus births). Including the initial `B=0` exponential holding time yields constants `epsilon,C>0`, uniform over every initial `a`, such that

```
E_a[exp(epsilon*(tau_1-tau_0 + |X_1-X_0| + J_1))] <= C,
```
where `J_1` counts reaction transitions in the excursion, after adjusting epsilon for units. In particular all `tau_n` are a.s. finite, the base process is nonexplosive (it spends independent Exp(lambda) times at B=0 between excursions), and the return chain is irreducible on nonnegative integers: `+1` occurs via `B=1 -> 0` conversion; `-1` occurs for `a>=1` via `B=1 ->2 ->0` annihilation.

**Audit point:** This is the crucial uniformity lemma. An explicit probabilistic coupling or a separate exponential Foster–Lyapunov proof should be checked by a Markov-process specialist. Merely asserting exponentially rare excursions is insufficient without this lemma.

## Step 2: an exact compensation observable and first two moments

Set `W(a,b)=a-floor(b/2)`. Annihilation leaves `W` **unchanged**. For `mu=lambda`, its exact generator is

```
L W(a,b) = 0                     b = 0 or 1
         = 2*lambda*b            b even >=2
         = lambda*(b-1)          b odd >=3.
```

The return cycle starts `(a,0)->(a,1)`. At `B=1`, conversion to zero or birth to `B=2` are equally likely. Conditional on reaching `(a,2)`, its first holding time has mean `1/(2*kappa*a+3*lambda)`. This first visit contributes exactly

```
4*lambda * (1/2) * 1/(2*kappa*a+3*lambda)
   = 2*lambda/(2*kappa*a+3*lambda)
   = lambda/(kappa*a) + O(a^-2)
```
to the drift of `W`, and hence to `E_a(X_1-a)` (both endpoints have B=0).

Why are all remaining contributions `O(a^-2)`? An excursion has uniformly exponential event-count tails. On the event that fewer than `a/2` reaction events occur, `A>=a/2` throughout. Thus the **first non-annihilation escape from B=2** has probability `O(a^-1)`. It is needed both for subsequent visits to B=2 and for any visit to B>=3. By the strong Markov property, the expected number of subsequent visits is bounded uniformly, and each visit of a B>=2 state lasts `O(a^-1)` in expectation (after weighting by B's at-most-exponential tails). Paths with at least `a/2` events contribute exponentially little. This gives the stated `O(a^-2)` error.

On the complement of the rare `O(a^-1)` event, `X_1-a=+1` with probability `1/2`, or `-1` with probability `1/2+O(a^-1)`; the remaining path contribution has uniformly bounded conditional second moment by the same exponential-tail/Markov argument. Therefore

```
E_a[X_1-X_0]       = (lambda/kappa)/a + O(a^-2);
E_a[(X_1-X_0)^2]   = 1 + O(a^-1);
sup_a E_a exp(epsilon*abs(X_1-X_0)) < infinity.
```

Also `E_a[X_1-X_0]>0` for every finite a, since the generator of W is nonnegative and with positive probability the process spends time at B=2.

## Step 3: classify the embedded chain, including the critical equality

Put `c=lambda/kappa`. Taylor expansion against the uniform exponential moments gives, for smooth f with controlled derivatives,

```
E_a[f(X_1)-f(a)] = (c/a+O(a^-2))*f'(a)
                     + (1/2+O(a^-1))*f''(a)
                     + controlled third-order error.
```

If `c>1/2`, choose `theta in (0,2c-1)`, and use `f(a)=(a+K)^(-theta)`. Then for sufficiently large a,

```
E_a[Delta f] = -theta*(2c-1-theta)/2 * a^(-theta-2)
                         + O(a^(-theta-3)) < 0.
```

A positive function tending to zero with this negative drift implies **transience** by the usual stopped-supermartingale hitting-probability argument. Irreducibility gives `X_n -> infinity` a.s.

If `c<1/2`, use `f(a)=(a+K)^r`, `0<r<1-2c`. Its drift is
`r(2c+r-1)*a^(r-2)/2 + O(a^(r-3))<0`, while `f(a)->infinity`. The stopped-supermartingale criterion implies **recurrence**.

If `c=1/2`, use the borderline function `f(a)=log(log(a+K))` for sufficiently large K. Direct derivatives give

```
E_a[Delta f] = -1/(2*a^2*(log a)^2)
                 + O(1/(a^3*log a)) < 0
```
for all large a. Therefore the **critical boundary is recurrent**, not an unresolved equality case.

The recurrent cases are **null recurrent**, not positive recurrent: suppose the chain had a stationary probability pi. The strictly positive bounded conditional drift `m(a)=E_a Delta X>0` would yield, by the stationary ergodic theorem and the martingale strong law using uniformly bounded second moments, `X_n/n -> E_pi m(X)>0` a.s. But under stationary pi, `X_n/n ->0` in probability. Contradiction.

## Step 4: catalytic clock and exact explosion boundary

Let `A_phys=p+a` on the active component `A_phys>=p`. All translated stochastic rates equal the corresponding base rates multiplied by

```
q_p(a)=(a+1)(a+2)...(a+p),  q_0=1.
```

Hence the translated CTMC is exactly the base jump chain with continuous clock

```
T = integral_0^infinity [q_p(A_s)]^-1 ds.
```

On each B=0 holding interval, its physical clock contribution is an independent Exp(lambda) variable divided by `q_p(X_n)`. Conditional on the embedded trajectory `(X_n)`, the sum of these independent weighted exponentials diverges a.s. exactly when `sum_n [q_p(X_n)]^-1` diverges.

* If the return chain is recurrent (c<=1/2), it visits a finite state infinitely many times. Thus the clock diverges for **every p**.
* If the return chain is transient (c>1/2) but `p<=2`, the clock still diverges. Indeed if `sum_n (X_n+1)^-2<infinity`, then the conditional drift and quadratic variation of `log(X_n+K)` would both be summable. Its martingale decomposition would converge a.s., contradicting `X_n->infinity`. Since `q_p(a)<=C(a+1)^2` for p<=2, this forces clock divergence.
* If c>1/2 and p>=3, choose `0<theta<min(2c-1,p-2)`. The negative drift of `(a+K)^-theta` from Step 3 yields
  `E[sum_n (X_n+1)^(-theta-2) * 1_{X_n>R}]<infinity`, by telescoping the Lyapunov inequality. The expected number of visits to the finite set `[0,R]` is finite by irreducible transience. Since `p>theta+2`, `E sum_n (X_n+1)^-p<infinity`. The uniform exponential excursion bounds in Step 1, plus the fact that `A` moves by at most the excursion event count, show
  `E[physical time in excursion n | X_n=a] <=C_p (a+1)^-p`. Therefore **E[T]<infinity**, and T is finite a.s.

These cases exhaust the statement. For a finite initial `B>0`, there is a.s. a first return to `B=0` in finite time, so the same dichotomy holds.

## Independent deterministic and structural reconstruction

The network really is **strongly endotactic** without relying on the earlier card. Its source complexes are `(0,0),(0,1),(1,2)` and reaction vectors `(0,1),(1,-1),(-1,-2)`. For any nonzero linear covector `w=(u,v)`, inspect which source maximizes the dot product: if source 0 maximizes, then `v<=0`, so its edge is not outward; if `v=0`, source 1 ties and its edge has strictly negative projection `u<0`. If source 1 maximizes, then `v>=0`, `u+v<=0`, and its edge has strictly negative projection `u-v<0` unless w=0. If source 2 maximizes, then `u+2v>=0`, and its edge projects `-u-2v<=0`; in the zero case source 0 ties and its edge projects `v<0`. This is precisely the maximal-source endotactic requirement. Translation by `pA` adds the same `(p,0)` to all sources and products, leaving these inequalities unchanged.

The original deterministic ODE at `mu=lambda` is
```
a' = lambda*b - kappa*a*b^2,
b' = lambda*(1-b) - 2*kappa*a*b^2 .
```
The unique positive equilibrium is `(a*,b*)=(3lambda/kappa,1/3)`. Here is an explicit boundedness argument. After an initial interval `b<=Bmax` since `b'<=lambda(1-b)`. Choose `c0^2=lambda/(16*kappa)`, `eps0=kappa*c0^2/(2lambda)=1/32`, and large `A0`. On `a>=A0`: (i) if `b<c0/sqrt(a)`, then `b'>lambda/2` while `a'<=lambda*c0/sqrt(a)`; (ii) if `c0/sqrt(a)<=b<=eps0`, then `a'<=lambda*eps0-kappa*c0^2<0`; (iii) if `b>=eps0`, then `a'<=lambda*Bmax-kappa*a*eps0^2<0`. Thus the locally Lipschitz barrier `V(a,b)=a+(c0/sqrt(a)-b)_+` has strictly negative upper directional derivative throughout `a>=A0` (on the kink use both one-sided derivatives), so `a` remains bounded. The vector field points inward at `a=0` when `b>0` and at `b=0` (where `b'=lambda`); a bounded trajectory has no boundary omega-limit. The divergence `-kappa*b^2-lambda-4*kappa*a*b` is strictly negative, eliminating periodic orbits by Bendixson. Poincare-Bendixson with a unique interior equilibrium gives global attraction for every positive initial state. The translated deterministic ODE is the original right-hand side times the strictly positive factor `a^p`; it therefore has the same positive trajectories, just different clock parametrization, and inherits global attraction.

## What is new and what is not

**Potential new internal result:** complete, exact **rate/clock phase diagram** `kappa<2*lambda AND p>=3` for a three-channel, strongly endotactic, deterministic-permanent family at balanced immigration/conversion. This closes a *named open case* in the pinned Astra stochastic-universality record and shows a rate-controlled stochastic explosion bifurcation inside a fixed reaction-graph class.

**Established borrowed results:** Lamperti's near-critical drift philosophy and optional stopping; known existence of strongly endotactic explosive networks; standard stochastic time changes; familiar deterministic mass-action permanence principles. This is not a solution of a globally famous open problem, an algorithmic complexity lower bound, or physical finite-fuel explosion. Its historical uniqueness and a specialist-level proof check are not established.

## Reproducible independent computation

`verify_return.py` solves a finite killed-generator Dirichlet problem for `B>=1` until hitting `B=0` or artificial truncation boundaries. It computes the **unnormalized** first two hitting increments plus probability of truncation escape; small escape probability is a diagnostic, not a rigorous bound on omitted unbounded payoffs.

For `lambda=mu=1`, a=300, Bmax=9 and `|A-a|<=13`, the outputs are

| kappa | a*E Delta A | E (Delta A)^2 | predicted a*drift |
|---|---:|---:|---:|
| 0.5 | 1.991156540 | 1.004989774 | 2 |
| 1 | 0.997782107 | 1.002497418 | 1 |
| 2 | 0.499444643 | 1.001249351 | 0.5 |
| 4 | 0.249861050 | 1.000624837 | 0.25 |

The finite-solver evidence is numerical and *does not* establish recurrence or explosion. Replicate with `python verify_return.py` (numpy/scipy), optionally vary truncation windows and compare the limits.

## Adversarial obligations and high-value continuation

1. Specialist check of **uniform exponential excursion moments**, including Poisson-birth event counts until immigration–death return, and rigor of the `O(a^-2)` drift remainder with unbounded B.
2. Review the **borderline log-log Lyapunov expansion** and the supermartingale proof of `E sum (X_n+1)^-p<infinity`, especially arbitrary overshoot jumps.
3. Verify exact **stochastic time-change normalization** (falling factorial, no extra `p!` factors) and all-active-initial-state quantifiers.
4. Fully independently reprove the inherited deterministic global attraction, strongly endotactic reaction geometry, and uniform excursion-to-clock expectation bound.
5. Full historical priority search in stochastic reaction networks, Lamperti modulated chains, catalytic time changes and Lamperti–Bessel explosion criteria. The narrow direct-query scan did not find an exact antecedent, but absence in search is not priority proof.
6. Seek more consequential downstream implications: rate-dependent classification of stochastic explosion under syntactic permanent/endotactic promises, complexity of deciding explosion with variable graph inputs, and possible extension to more general fast-return phase-dependent reaction systems. None of these is proved here.

This candidate is a rigorous research target but not an independently validated field-breaking discovery.
