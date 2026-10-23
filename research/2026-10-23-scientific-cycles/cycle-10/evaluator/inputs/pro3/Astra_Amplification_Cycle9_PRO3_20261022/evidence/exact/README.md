# Frozen Cycle9 finite checks — one admission failure preserved

The input is the unchanged `../PREEXECUTION_FREEZE.json`, SHA256
`357cb63fb78fa1fe0fe627e84c0cf58942cd64261834805224635028736e0253`.
The first complete execution used `../../code/exact_checks.py`, SHA256
`c78a5576bc5861501a9f936e495e84d03a0b7f8dffbf80799455c9b814b91711`.
No fixture, horizon, probability, depth, power or information budget was
changed after freezing or after execution.

## Decision

Every requested native kernel identity, quotient identity, exact finite
capture inequality and ordinary-IMH comparison passed on both fixtures.
However, the coalescence fixture is **not admitted under its frozen K=1**.
A rigorous rational enclosure proves its KL divergence exceeds one.
The suite therefore deliberately returned exit status **1**, and records
`all_frozen_gates_pass: false`. This failure is not reclassified as a pass.

The coalescence results remain useful algebraic checks of the kernel,
lumping, actual hazards and retained terminal union. They are not evidence
of an admitted K=1 minimax instance. The analytical growing-depth theorem
proves eventual admission independently; a finite n=128 example is not
guaranteed to have reached that asymptotic regime.

| Frozen fixture | Native states | KL diagnostic | Rigorous admission | Conservative TV lower | Original full-law TV |
|---|---:|---:|---|---:|---:|
| Expansion | 32 | 0.7871982548836166 | Upper enclosure <1 | 0.02153477531169968 | 0.04917383575018947 |
| Coalescence | 5,462 | 1.103836351039874 | Lower enclosure >1 | 0.004108528887207315 | 0.04237325886901944 |

Displayed decimals are diagnostics. All kernel entries, evolved laws,
inequalities and the KL admission decision were evaluated with exact
Python `Fraction` arithmetic. The JSON files record numerator/denominator
strings for compact rationals and SHA256 hashes plus bit sizes for large
ones; the complete q, pi, quotient matrices and final laws are stored as
exact numerator/denominator arrays. No floating comparison determines a
pass or failure.

## What was checked

For both orientations, the code enumerated every native proposal edge,
checked both reciprocal proposal directions and every native row, proved
the frozen screen equals one by its positive exact square, retained the
true rejection diagonal, and checked local target detailed balance and
native-to-level lumping. The expansion has 60 directed off-diagonal
native edges; the coalescence has 10,920.

For the 32-state expansion only, full native G and C matrices were built.
Their rows lump exactly, and their first four evolved laws agree with the
quotient laws and remain uniform within each level. For the 5,462-state
coalescence, no dense native G or C matrix was built: all sparse native
Q/local edges were checked, and G was obtained from its proved level
formula, since every native state in a level has the same importance
ratio. The actual scientific law is always the native law; the quotient
is a verified calculation, not a replacement sampler.

The exact global hazard counts only actual moves out of the current
level. Global rejection and movement inside the level are holds. The
marked local forward event is separate from a global move to the same
next level. A marked absorbed chain checks the selected first-hit event;
the full original C law at n=64 or n=128 is then computed independently,
including all post-hit exits and returns. The retention calculation uses
the entire terminal union.

The rational finite certificate uses the slightly stronger timing factor

`[1-(1-c-alpha*q_star/2)^H]^J`,

where `H=floor(n/(2J))`, instead of its weaker exponential lower bound.
The exact level-dependent window capture is also computed and checked
against both the conservative product and the marked horizon capture.
This change was authorized before execution and does not alter inputs.

## Rigorous KL enclosure

For each positive rational x, exact binary range reduction writes x (or
1/x) as `2^j y`, with `1<=y<2`. The code evaluates 24 terms of

`log(y)=2 sum_{k>=0} t^(2k+1)/(2k+1)`, `t=(y-1)/(y+1)`.

The omitted nonnegative remainder is at most

`2 t^49/[49(1-t^2)]`.

The same calculation bounds log 2, and inversion reverses the interval.
Multiplication by each exact positive pi mass and summation yields exact
rational lower and upper bounds for the *single* complete KL divergence.
The expansion's upper endpoint is below one; the coalescence's lower
endpoint is above one. The JSON retains endpoint hashes and exact gate
booleans. Floating logarithms are reported only as a readable diagnostic.

## Same-input ordinary controls

| Fixture | Pure-G steps | Exact TV, displayed as decimal | Proved finite bound, displayed as decimal |
|---|---:|---:|---:|
| Expansion | 16 | 0.0016607431847831926 | 0.08660018198763972 |
| Expansion | 64 | 0.0010506261144886892 | 0.08659255259310847 |
| Coalescence | 32 | 0.0013700822713556902 | 0.3371584416745472 |
| Coalescence | 128 | 0.00006502364876652282 | 0.3371584415581319 |

These are actual finite-law comparisons on the same q, pi and disclosed
analytic input. The deterministic smaller count is `floor(alpha*n/2)`;
it is not an assertion of equal wall time or target-evaluation cost.
The bounds are conservative at these small horizons, especially because
the coalescence has z=1/4. Direct sampling of the disclosed analytic
target remains allowed. Neither these calculations nor an adverse finite
hybrid comparison proves the asymptotic theorem.

## Observed resources and reproduction

The scientific calculation ran once, from 2026-10-22 09:09:51.641999 UTC
to 09:09:56.908168 UTC. Recorded process CPU was 5.262211834 seconds,
wall time 5.266222576 seconds, and peak process RSS 19,968 KiB on Linux.
This includes both fixtures and output serialization. Inference, coding,
proof discovery, total scientific time, monetary and energy costs are
unknown. No external or paid resource was used.

Run into a new empty output directory:

```sh
python code/exact_checks.py --output-dir /tmp/astra-cycle9-fresh-check
```

The script refuses to overwrite nonempty evidence directories. Its
expected exit status for the frozen inputs is **1**, reflecting the
preserved coalescence admission failure; the expected model-check result
is true for both fixtures. Successful reproduction means matching those
scientific outcomes and exact fraction hashes, not changing the frozen
failure to obtain a zero process status. Resource timings will vary.
