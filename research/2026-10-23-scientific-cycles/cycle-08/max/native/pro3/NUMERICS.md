# Exact finite evidence and reproducibility limits

The finite checks test newly changed algebra and interfaces. They are not
numerical evidence for an asymptotic limit. Every probability, transition,
matrix product, comparison and positivity certificate is rational. No
floating-point normalization or tolerance certifies any scientific inequality.

## Frozen first execution

EXPERIMENT_CONTRACT.md and evidence/DIAGNOSTIC_FREEZE.json precede the first
run of code/reciprocal_checks.py. The 7-state fixture is nonreversible at the
proposal level and has a large incoming column. Its q masses are (i+1)^4/4676,
i=0,...,6; pi numerator vector is (1,1,1,1,100,1000,5000), normalized by
6104. Native reciprocal support, stochasticity, detailed balance of the actual
target kernels and a rational KL admission bound are checked.

Six parameter/weight cases and all eight hit-set subsets exercise interior,
endpoint and positive-defect energy regimes. Exact LDL decompositions certify
the resulting quadratic forms for every vector on those finite fixtures.
Absorption is independently computed by first-hit decomposition; original
post-hit propagation is also compared with the full chain.

An 18-state many-to-one fixture tests the new counterconstruction and its
same-input corrected-screen and pure-IMH controls at horizons 2,4,8,16.
The failed old counting-column premise is visible exactly: the absorbed
conjugated local column has sum 5>2. The reverse-proposal energy bound holds.

First execution: PASS. Observed body wall time 0.6461982050022925 seconds;
CPU 0.646119439 seconds; peak RSS 13,440 KiB. Serialization and discovery are
excluded. Full stdout and body-resource records are preserved.

## Separately frozen opposite geometry

FANOUT_CHECK_CONTRACT.md and evidence/FANOUT_FREEZE.json freeze the additional
code/fanout_checks.py before its first run. This is a new 18-state one-to-many
fixture for eta=1/4 and kappa=1/2 versus the matched kappa=1/4 control. It
computes per-vertex ratios, native transitions and the exact three-block
quotient. The complete leaf block retains same-block global moves; its escape
is explicitly distinguished from a single leaf's diagonal. Four horizons
check each hybrid and the ordinary comparator.

First execution: PASS. Body wall time 0.04379089300346095 seconds; CPU
0.043791112 seconds; peak RSS 13,696 KiB. No prior source, frozen input or
result was modified to add this check.

## Total executed finite checks

| Check | Count |
| --- | ---: |
| Local all-vector exact LDL certificates | 49 |
| Mixture all-vector exact LDL certificates | 49 |
| Absorption/first-hit identities | 147 |
| Original full-return identities | 4 |
| Native quotient and hybrid sandwich checks | 24 |
| Pure-IMH sandwich checks | 8 |

These counts describe the bounded producer executions, not independent
theorems or discovery productivity. The largest explicit matrix has 18
states. No asymptotic graph, long Monte Carlo simulation, favorable target
search, numerical fit, external compute job or old scientific suite was run.

## Deterministic replay identities

| File | SHA256 |
| --- | --- |
| EXACT_INPUTS.json | 0e5cbb797882d83d2b35c66b6174d72b923db46b36a17f01f19e804e0d9d5a66 |
| RECIPROCAL_CHECKS.json | 8824791cbae98d164cb2ed2073ec1346196cfdb6b6aad79d236f0221fb8c18f8 |
| FANOUT_INPUTS.json | 0e9a0145d7611d076bc00916a544d6e858b47976bbb008618a9776029708bf6d |
| FANOUT_CHECKS.json | 3ab8e68b39b5c1093024a2e0bee1e96d42c46e750a3a925dd52fab16e44225f8 |

The portable replay verifies the archive manifest and runs only these two
scripts in a fresh temporary directory. It compares all four files byte for
byte and records its own resource observations. Its actual result is in the
external delivery receipt; elapsed replay time is not research-discovery cost.

## What remains outside this evidence

The analytical universal statements rest on their full proofs and accepted
dependencies, not these finite examples. Formal verification, external
acceptance, historical originality and useful implementation are unknown.
Native index, probability-evaluation, precision and target-call costs of the
asymptotic families are not replaced by the quotient's tiny replay time.
