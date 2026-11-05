# Joint exposure bounds and the shared-wait counterexample

[Return guide](README.md) · [Complete native source](P2_AUTONOMOUS_CLASSICAL_OUTPUT_20261106_RETURN.txt) · [Missing positive operation](receiver-and-unfinished-operation.md)

## Fixed windows retain the common physical burst

For each actual exposure window `W_i=K_i x I_i`, let `E_i` be the marked Poisson source points whose time lies in `I_i` and whose spatial ball intersects `K_i`. Controls, buffers, data and waiting must be included in the footprint/time. Define `b_S=mu(intersection_(i in S) E_i)`.

The supplied proof gives exact inclusion–exclusion for all windows being hit and the useful upper bound

```
P(all windows in J hit) <= sum_(pi in Part(J)) product_(B in pi) b_B.
```

Assigning one incident source point to each hit and grouping equal points produces the set partitions; Poisson factorial moments give the products. For two windows the bound is `b_1 b_2+b_{1,2}`. The intersection term retains one burst hitting both operations. Fixed geometric windows require no additional causality condition on arbitrary allowed CPTP fault values.

## Causally selected windows need a stronger premise

For predictable indicators `H_i`, let `N_i=integral H_i dN`. The source must retain its declared Poisson compensator in the filtration choosing the windows, and every nonempty set must have a deterministic pathwise budget `integral product_(i in S) H_i dmu<=b_S`. Under those conditions, for nonnegative `a_i`,

```
E exp(sum_i a_i N_i)
 <= exp(sum_(nonempty S) b_S product_(i in S)(exp(a_i)-1)).
```

The source's predictable exponential-supermartingale argument then yields a joint Chernoff bound. Past faults/outcomes may guide exposure; advance future geometry conveyed by fault values is not covered by that premise. Mean exposure bounds do not replace pathwise budgets.

If one physical source point belongs to at most `K` selected sets and each individual budget is `b<1`, the specified-set corollary is `(b exp(1-b))^(m/K)` for `m` windows. This is a joint bound, not independence. Unrestricted Pareto marks have no uniform bounded multiplicity `K`; large-radius intersections must stay explicit or be separated and charged.

For a footprint inside radius `cH`, duration at most `tau` and marks of radius at least `H`, the hit probability is at most `C_(d,alpha,c) lambda tau H^-r`, `r=alpha-d`. Here `tau` is real elapsed exposure, including stalled clocks, retained data, occupied buffers and delayed messages. Nominal circuit depth cannot replace it. These estimates do not construct the required exposure witnesses for an autonomous controller.

## Finite mean repair does not imply a recursive joint fault law

Take `k` independent rate-`q` damaging sources, all exposed until one shared completion time `S~Exp(v)` independent of those sources. Each marginal hit probability is `q/(q+v)`. Nevertheless, with `a=q/v`,

```
P_k = E(1-exp(-qS))^k
    = Gamma(1+1/a) Gamma(k+1) / Gamma(k+1+1/a)
    = k! a^k / product_(j=1..k)(1+ja).
```

For fixed `a>0`, this decays polynomially as `k^-1/a`, rather than as any fixed `p^k`. At `a=0.05`, `k=100`, the source reports `P_k~3.39e-23`, versus a false marginal product of about `6.00e-133`.

This counterexample has no spatial correlations at all: shared waiting alone defeats the inference. A finite mean, exponential completion tail or small marginal hazard therefore does not supply the joint condition needed for recursive fault tolerance. It does not prove autonomous computation impossible, refute the strongest finite-neighborhood repair design or revive naive marching-rule deadlock. Jointly local, controlled delay witnesses remain the missing requirement.
