# Exact diagnostics and measured costs

The full mathematical argument is CRITICAL_ENDPOINT_THEOREM.md. The fixed
diagnostic contract was written before execution in EXPERIMENT_CONTRACT.md.
The new code uses Python's standard library only:

    python code/absorbed_checks.py --output result.json --inputs inputs.json --resources resources.json

The inputs are one genuine six-state native chain with two alpha choices,
all eight subsets of its safe set as the absorbed boundary, and four finite
first-hit horizons. They are not a search for adverse mixing and not a
replacement for the class supremum. All normalized q,pi,Q,G,L and the exact
parameters are in evidence/EXACT_INPUTS.json.

## What was checked exactly

Fraction arithmetic verified positivity, normalization, symmetry of Q,
detailed balance of G,L,C, KL<1 through max W=91/50<2<exp(1), actual killed
row masses, and the separate local and global weighted column bounds.

For every absorbed matrix, the p=2 energy inequality was checked for ALL
vectors: an exact rational LDL factorization with strictly positive pivots
certifies Gamma I minus (D P^E D^-1)(D P^E D^-1)^T is positive definite.
This produced 16 certificates. Absorbed mass and separately accumulated
first-B-hit mass agreed exactly in 64 checks; each squared Holder bound held.
Two complete first-hit decompositions with original full propagation after
each hit agreed exactly with direct C^16, at N=5. No floating positivity or
normalization was used.

Results: evidence/ABSORBED_CHECKS.json, 41,219 bytes, SHA256
`06ccdbb28c5d92890aa6d3fcca20e8fe3319991290a69d172028203142cba6c7`.
The exact diagnostic passed on its first execution.

## Theorem-defined illustrative constants

At K=1 and alpha=1/2, 80-digit Decimal bisection gives

    c_* = 0.648419527440700180703395351103758319...
    s_cross = log(1-exp(-1))/c_* = -0.7073740471658282132684308339...

The exact limiting amplitude from the theorem, with pure IMH amplitude one,
has the following illustrations:

| Critical offset s | Hybrid limiting amplitude | Pure IMH amplitude |
|---:|---:|---:|
| -2 | 2.31211781948 | 1 |
| -1 | 1.20894053126 | 1 |
| 0 | 1 | 1 |
| 1 | 1 | 1 |

These are evaluations of the proven formula, not fits to matrix powers.
Decimal outputs are not outward-rounded interval certificates. No additional
precision run is needed to support the exact analytic conclusion; no practical
runtime comparison is inferred from the table.

## Observed resource boundary

The first successful diagnostic body took 0.127882274 seconds wall,
0.127884421 seconds CPU, with peak RSS 11,776 KiB as reported by Python
resource.getrusage. It includes native construction, rational certificates
and Decimal constants, and excludes JSON output writes/interpreter startup.
The two independent contributors ran no numerical jobs in this allocation.

The portable replay has a separate measured receipt. These short runtimes
are not discovery costs. Active model inference, token, monetary and complete
historical research costs are unknown. Wall-span records include reading,
reasoning, tools, reviews and delivery, not a measured active-thinking budget.
No large graph, long trajectory, old search campaign or paid compute was run.
