# Reversible singular-explosion regularization: exact observation law and first-passage bifurcation

**Date:** 2026-10-08 (Brisbane)  
**Read-only prior Astra revision:** `b5824d0fcbfe0688980788da2722270a2f068fb0`  
**Classification:** internally proved mathematical example/candidate synthesis; finite rational tests; **external expert correctness, formal verification, historical originality, experimental relevance UNKNOWN**. Single investigator; no parallel subagents. This review branch does not change the canonical card status.

## Selection and prior evidence

Read `00_START_HERE.txt`, selective `01_CORE.txt`, `frontier/PRIORITIES.md`, `agent/UPSTREAM_ENTRY.txt`; compared stochastic universality, log-valuation permanence, square-root collective-bath and family-197/Rokhlin candidates. Chosen because the precise stochastic information experiment admits closed exact formulas. Existing Astra `state/2026-10-08-stochastic-universality/RESULT_AND_RESTART.md` has stronger **fixed-parameter, deterministic-permanent / stochastic-explosive** examples. The present positive-parameter model does **not** explode. Do not claim a new counterexample to complex-balance nonexplosivity.

## Reusable rate-independent stopped-path lemma

Let `l>=2`, `K>l`, and let `lambda_n>0` be any rates for `l<=n<K`. Start a birth-only chain `P0` at `l`, moving `n -> n+1` at rate `lambda_n`. Compare to `Peps` with *the same* births and additional `n -> n-1` deaths at rate `mu_n=eps*lambda_n*(n-l)`, `eps>0` (zero at the lower boundary). Observe the **entire continuous-time path up to first hitting K**, including all holding times and transitions. Write `L=K-l` and `Q=product_{j=0}^{L-1}(1+eps*j)^(-1)`. Both first hit K a.s. Then exactly

```text
TV(P0,K, Peps,K) = 1-Q
KL(P0,K || Peps,K) = eps*L*(L-1)/2
KL(Peps,K || P0,K) = +infinity     if L>=2
TV(P0,K^m, Peps,K^m) = 1-Q^m
KL(P0,K^m || Peps,K^m) = m*eps*L*(L-1)/2.
```

For equal prior probabilities, the optimal decision is "positive eps" if **any downward jump** occurs across m full stopped paths, and "pure birth" otherwise, with exactly `Q^m/2` Bayes error. These *path* identities are **independent of the numerical size of the upward rates** `lambda_n`. At `eps*L^2->c` and `L->infinity`, `TV->1-exp(-c/2)`; if `eps*L^2->infinity`, `TV->1`. For m independent paths the relevant parameter is `m*eps*L^2`.

**Proof from path likelihood, not an information heuristic.** P0 is supported only on the strictly upward event sequence `l,l+1,...,K`. Conditional on this sequence with holding times `w_n`, the density of P0 over that of Peps is `exp(sum_n mu_n*w_n)>=1`. Under P0 the `w_n` are independent exponentials `Exp(lambda_n)`. Integrating its log gives `sum mu_n/lambda_n=eps*L*(L-1)/2`. Under Peps the probability of no reverse event is `prod lambda_n/(lambda_n+mu_n)=Q`. The P0 density dominates on that support and is zero off it: TV is exactly `1-Q`. The product case repeats the argument; log expansion establishes the scaling. The reverse divergence is infinite because Peps has positive mass on reverse-jump paths for L>=2.

## Concrete weakly reversible detailed-balanced mass-action specialization

Take the one-species reaction pair

```text
l A  -- rate constant 1 --> (l+1) A
(l+1) A -- rate constant eps --> l A.
```

At volume one use stochastic falling-factorial propensities `lambda_n=(n)_l`, `mu_n=eps*(n)_(l+1)=eps*(n)_l*(n-l)`. For each `eps>0`, the deterministic ODE `a'=a^l(1-eps*a)` is globally attracted, from every `a>0`, to `a*=1/eps`. The stochastic chain on its **closed irreducible class n>=l** is nonexplosive, positive recurrent, reversible, with

```text
z=1/eps;
pi_eps(n) = (z^n/n!) / sum_{k=l}^infty (z^k/k!),  n>=l.
```

States `n<l` are absorbing and excluded from claims of irreducibility. Directly, `pi_(n+1)/pi_n = z/(n+1)=lambda_n/mu_(n+1)`. For `V(n)=n`, `QV=(n)_l[1-eps(n-l)]` has finite upper bound, giving nonexplosion by stopped Dynkin; normalizable detailed balance and irreducibility give positive recurrence. The deterministic scalar phase line proves global attraction.

At `eps=0` the chain is pure birth with independent `Exp((n)_l)` holding times and almost-sure explosion at time `T_l`. Telescope `1/(n)_l=[1/(n-1)_(l-1)-1/(n)_(l-1)]/(l-1)` to obtain

```text
E[T_l] = 1/[(l-1)*(l-1)!],
E[T_l-T_(0,K)] = 1/[(l-1)*(K-1)_(l-1)].
```

Coupling the forward exponential clocks up to K, and introducing independent eps-death clocks, yields for each delta>0

```text
P(|tau_(eps,K)-T_l|>delta)
  <= 1-Q(eps,K-l) + 1/[delta*(l-1)*(K-1)_(l-1)].
```

Therefore if `K->infinity`, `eps*(K-l)^2->0`, reversible finite-threshold hitting times converge **in probability under a coupling** to the irreversible explosion time, although the eps>0 system never explodes. Balancing terms at `K~eps^(-1/(l+1))` gives the explicit `O_delta(eps^((l-1)/(l+1)))` bound. The statistical distinction scale `K-l~eps^(-1/2)` is much smaller than the equilibrium population `1/eps`.

## Exact first passage and sharp supra-equilibrium times

Let `tau_K` be the reversible process' first hitting time of K starting at l. Define `S_l=1` and for `n>l`, `S_n=1+eps*n*S_(n-1)`. The backward-generator equation `lambda_n*t_n-mu_n*t_(n-1)=1` for step time `t_n=E_n tau_(n+1)` gives exactly

```text
E_l[tau_K] = sum_{n=l}^{K-1} S_n/(n)_l,
S_n = n! * z^(-n) * sum_{m=l}^n z^m/m!,   z=1/eps.
```

For fixed `alpha>0`, `K=floor(alpha/eps)` as eps->0:

* `0<alpha<=1`: `E_l[tau_K]->E[T_l]`.
* `alpha>1`: `eps*log E_l[tau_K]->I(alpha)=alpha*log(alpha)-alpha+1>0`, and in fact
  `E_l[tau_K] ~ alpha/(alpha-1) * exp(z) * z^(-(K-1)) * (K-1-l)!`.

For `0<alpha<1` there are also exact first-order expansions, with `gamma_E` Euler's constant:

```text
l=2:
E_2[tau_K]=1+eps*[log(1/eps) + log(alpha/(1-alpha))
                       + gamma_E - 1 - 1/alpha]+o(eps).

l>=3:
E_l[tau_K]=1/[(l-1)*(l-1)!]
              + eps/[(l-2)*(l-1)!] + o(eps).
```

**Proof of phase transition.** The recurrence follows by first-step analysis. For `n<=alpha*z,z=1/eps`, `S_n<=1/(1-eps*n)` when alpha<1; dominated convergence proves the finite limit. At alpha=1, `S_n=sum_{j=0}^{n-l}(n)_j/z^j<=C*sqrt(z)` for n<=z (use `prod_{k<j}(1-k/n)<=exp[-j(j-1)/(2n)]`), which makes the n>=delta*z contribution `O_delta(z^(3/2-l))->0`; the lower-n tail is dominated. For alpha>1, for n/z on compact subsets of (1,infinity), the Poisson partial sum in `S_n` is asymptotic to `exp(z)`; the terms `S_n/(n)_l~exp(z)*z^(-n)*(n-l)!` have backward ratio approaching `1/alpha` at the terminal end. Earlier levels contribute exponentially less by Stirling and the strict increasing rate `I(u)` on u>1. Terminal geometric summation gives alpha/(alpha-1); Stirling gives I(alpha).

For `l>=3,alpha<1`, `S_n=1+eps*n+O_alpha(eps^2*n^2)` for n>l; summation divided by `(n)_l` gives an `o(eps)` remainder and the telescoping coefficient `1/[(l-2)*(l-1)!]`. At l=2 compare `S_n` to `g_n=1/(1-eps*n)`: at n=2 the difference contributes exactly `eps+O(eps^2)`; from n>=3 the summed remainder is `O_alpha(eps^2 log(1/eps))`. Decompose `1/[n(n-1)(1-eps*n)]=1/[n(n-1)] +eps/[(n-1)(1-eps*n)]`; harmonic/Riemann sums yield the stated constant.

## Reproducibility, prior art, and restrictions

The accompanying `verify.py` contains finite rational backward-generator cross-checks, exact balance and TV/KL identities, and floating-point convergence tests. An initial test run passed 180 exact rational identities, with the ell=2, K=6, eps=1/10 case yielding TV=179/429 and KL=3/5. Finite tests do not prove the general claims.

**Established concepts:** product-Poisson equilibrium: Anderson--Craciun--Kurtz 2010; Cappelletti--Wiuf 2016 https://arxiv.org/abs/1507.02195; complex-balanced nonexplosion: Anderson--Cappelletti--Koyama--Kurtz 2018 https://pubmed.ncbi.nlm.nih.gov/30117084/; reversible reaction limits: Gorban--Yablonsky 2011; standard birth-death first-passage / large-deviation potential methods (e.g. Doering--Sargsyan--Sander--Vanden-Eijnden 2007). The precise combined observation identity and logarithmic correction may be elementary consequences of old results: **historical novelty NOT ESTABLISHED**.

**Unresolved:** expert proof review, full priority search (including birth-death statistical tests), Lean formalization of the exact statements/asymptotics, snapshot-only/noisy/deadline observation alternatives, finite-volume calibration, realistic reaction implementation. No new transformative algorithm or field-breaking theorem is certified.

**Important exclusions:** no claim of positive-eps explosion; no inference from finite stopped-path results to complete infinite-path TV; no all-state stochastic irreducibility; no detector-cost-free promise; no symmetric KL; no empirical validation. Rate-agnostic lemma is an elementary identity, and should be advertised as such until priority is settled.
