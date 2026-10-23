# Numerical evidence and its limits

The analytic proof determines the theorem. The frozen numerical contract is
`EXPERIMENT_CONTRACT.md`. Complete exact inputs are in
`evidence/exact_tree_inputs.json`; principal code is `code/branching_checks.py`.
Only Python's standard library is required.

## Exact checks before numerical propagation

All five principal cases construct normalized positive rational q,pi and the
exact quotient G,L,C. They check row sums, nonnegativity and detailed balance
with Fraction arithmetic. Per-vertex ratios select each MH branch exactly.
The analytic inequality
`KL <= log(1/q_star)+p log(W_leaf)` is certified below one by exact Taylor
and rational bounds. The lower certificate also uses only fractions; its
waiting correction follows from `(1-D0)^H <=1/(1+D0 H)`.

The cases use W_leaf=n*(log2 n)^2 and rational p determined by that identity.
These are finite members of the same native class, not a substitution into
the main asymptotic selection p=(log n)^-M. Keeping that distinction prevents
a finite pattern from being presented as a proof of an asymptotic exponent.

## Actual finite law comparisons

For alpha=1/2, the hybrid at n iterations has n/4 expected global attempts.
The table compares its actual TV, calculated from its exact quotient, with
ordinary IMH at n/4 global iterations. Both begin at the same q and target
the same pi. Full IMH at n is also preserved in the result files.

| D, depth | n | Native states | Proved finite TV lower | Hybrid TV at n | Pure IMH TV at n/4 |
|---|---:|---:|---:|---:|---:|
| 4, 2 | 2^16 | 22 | 0.07737472079 | 0.07747751863 | 9.603653387e-6 |
| 64, 2 | 2^20 | 4,162 | 0.1004623159 | 0.1004707806 | 1.501098565e-5 |
| 64, 3 | 2^48 | 266,306 | 0.04016346675 | 0.04016347138 | 1.351686668e-6 |
| 64, 4 | 2^200 | 17,043,522 | 0.01604164374 | 0.01604164378 | 5.867295549e-6 |
| 64, 6 | 2^680 | 69,810,262,082 | 0.002561209341 | 0.002561209341 | 6.468422298e-11 |

Numbers in the last two columns are high-precision diagnostics, not outward
interval enclosures. Their input normalization and KL admission are exact.
All examples were frozen before root execution. No cases were selected after
looking at these errors. They supply no performance advantage and none is
claimed. Target-query latency, cache misses and implementation maintenance
costs are not measured by matrix exponentiation.

The quotient has only depth+2 states. Tree automorphisms are transitive on
each level; q,pi and the transition kernel are invariant under them. Thus
qC^n stays uniform within levels and full TV equals quotient TV. The main
proof separately establishes the needed exact level transition law. No
69-billion-state array was created. Matrix squaring computes the finite law
at 2^680 without executing that many random steps.

The independent challenger constructed a full 22-state rational tree and
its quotient directly, checking all laws through twelve steps, including
the equality of final TV. Its exact KL certificate is 39767/40000<1. That
case has a distinct finite parameter selection from the principal's 22-state
row and is recorded in `reviews/tree_lumping_exact_check.py` and its JSON.

## Precision and exact scalar separation

Principal successful runs used 80 and 120 reserved digits plus
`ceil(log10(n))+30` guard digits. The 145 compared numerical values agree
to better than 1e-70 relative; maximum difference was about 7.46215e-80.
Mass errors were separately below 10^-reserve. The matrices remain
nonnegative in both propagations. `evidence/precision_comparison.json`
records the comparison. This resolves the concrete rounding risk for these
finite examples, not an ideal-real implementation guarantee over the class.

The constants are

    c_* = 0.648419527440700180703395351103758319...
    1/c_* = 1.542211419737745110564407530431280310...

For b=.63, increasing D from 2,4,16,64,256 to 4096 yields sufficient adverse
multiplier suprema approximately 1.22770, 1.34891, 1.48098, 1.52212, 1.53303
and 1.53650. Keeping b=.63 stops short of the entropy boundary; this table
is not the proof of the limiting coefficient. The theorem uses strict
approximation in both b and D.

An exact illustrative adverse multiplier 1.5 at b=.63,D=64,v=log4 uses
`801^3=513922401 < 16*320^3=524288000`. The exact margin is 10,365,599.
No decimal positivity or optimized finite matrix norm is needed for it.

## Observed calculation costs and failure

| Run | Body wall seconds | CPU seconds | Peak RSS KiB | Matrix / row products |
|---|---:|---:|---:|---:|
| Principal, 80 reserved digits | 2.883281844 | 2.880651839 | 13,056 | 2,882 / 15 |
| Principal, 120 reserved digits | 3.598622908 | 3.597590567 | 12,032 | 2,882 / 15 |
| Challenger, exact lift | 0.023068317 | 0.023065342 | unknown | exact finite check |
| Challenger, same case plus KL certificate | 0.024186383 | 0.024187892 | unknown | exact finite check |

The first principal execution reached output serialization and failed at
Python's 4,300-digit conversion limit. It completed all mathematical checks
and wrote the result file; that partial output is preserved and byte-identical
to the later 80-digit output. The repair grants a finite 100,000-digit limit
for generated fractions. Its unrecorded runtime/RSS are unknown. The original
source and traceback summary remain in `evidence/`.

These timings exclude the scientific construction, source reading, reasoning,
review, interpreter startup, packaging and private delivery. Total model
inference, tokens, money and historical discovery costs are unknown. Portable
replay gets its own receipt and must not be substituted for discovery cost.
