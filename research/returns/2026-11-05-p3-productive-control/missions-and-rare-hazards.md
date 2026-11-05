# Useful missions and attained rare-evidence boundaries

Mean useful-work optimality, mission survival and exact policy certification are distinct outputs. The [main report](package/report.tex), [boundary construction](package/independent/boundary_constructor_notes.md), [independent intervention proof](package/independent/intervention_constructor/constructor_notes.md), and [final qualifications](package/STATUS.txt) preserve the following scopes.

## Finite mission without equilibrium preparation

Under the deployed rule, suppose conditional transitions satisfy `p_i<=p_i^+` and `q_i>=q_i^-`, even when they depend on the whole history. Set

```text
b0=1, bi=(q_i^-/p_i^+) b_(i-1),
H(i)=sum_(j=0)^(i-1) bj.
P_x(T_N<=t)<=[H(x)+t p0^+]/H(N).
```

Nonpositive conditional drift of H at positive states proves the bound without equilibrium preparation or full path-law prediction. This is a survival guarantee under earned conditional envelopes, not an optimal-policy theorem for every changing environment.

For the example, `R=q_B^-/p_B^+>1`. From zero,

```text
P_0(T_N<=t)<=t p0^+(R-1)/(R^N-1).
```

Survival through t cycles completes at least 2t useful units. The full failure budget also includes

```text
delta_cal+eta_init+t p0^+(R-1)/(R^N-1)+t eta,
```

where eta bounds additional catastrophic interface failure per cycle. At N=8 the internal bound for 1,000 cycles is about 0.0132634; at N=16 it is about 6.99e-7. Neither removes the 0.01 calibration allowance. A much smaller total risk needs stronger calibration, preparation and interface budgets.

Every-safe-start mean optimality does not make a near-failed starting state suitable for a low-risk mission. Initial reserve must be physically prepared and paid. The earlier all-safe-start mean theorem remains at its original scope.

## A decision whose information lies only in rare hazards

Two controls have the same useful rate u>0 and bounded power. Their hazards are `(epsilon,2epsilon)` in one world and swapped in the other; every other observation has the same conditional law. Choosing correctly doubles mean useful work, yet any adaptive or parallel experiment needs the following worst-case aggregate exposure for reliable identification (0<delta<1/2)

```text
E T_aggregate>=kl(1-delta,delta)/[(2 log(2)-1)epsilon].
```

Parallel hardware can reduce elapsed time but does not reduce aggregate specimen exposure. Unlike the stable local policy family, this decision has no frequent distinguishing information.

An attaining finite operation is included. With the hazard scale supplied, hold each specimen for `h=1/(2epsilon)` and compare endpoint survival. Nominal probabilities are exp(-1/2) and exp(-1). Relative timer error omega and endpoint bias beta leave contrast

```text
g=exp[-(1+omega)/2]-exp[-(1-omega)]-2beta.
```

For fixed positive g, `m>=2 g^-2 log(1/delta)` paired trials suffice, using at most `m(1+omega)/epsilon` total hold exposure plus 2m resets and endpoint reads. Reset fidelity and shared metrology failures have separate budgets.

Failure must remain observable until readout, through deferred repair or a protected retained first-failure flag. Reading only whether the specimen works now is insufficient if it can fail and recover. This persistent-failure/readout requirement is one of the final independently checked qualifications.

## An exponentially rare omitted bypass changes exact policy certification

A second pair has a nominal unique optimum always A. B has useful-work mean

```text
M_B(N)=24(1.5^N-1)-8N.
```

For N>=3, add only to A a direct catastrophic transition with per-cycle probability `h=10/M_B(N)`. Always A then earns at most M_B/10 while B retains M_B. Exact optimal-policy certification across these two models requires

```text
E K>=M_B(N)/20 * kl(1-delta,delta).
```

Reset-to-zero probes attain the exponential dependence: a direct jump from zero to failure is impossible nominally and has probability h in the alternative. It is an exact-policy obstruction; no lower bound for every approximately optimal adaptive controller is inferred.

The boundary is therefore specific: action inequalities may be settled by finite local data while excluding a consequential rare mechanism remains expensive. A support-completeness premise cannot be replaced by a short trace with no observed bypass. The [repair companion](productive-repair-and-resources.md) separately prices indispensable physical support and long operation.
