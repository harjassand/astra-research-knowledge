# Independent challenge of the actual common-action certificate

Contributor: `/root/exact_kernel`, 21 October 2026.

**Verdict: PASS for the stated exact original-input transcript class.** No
blocking mathematical or implementation gap was found. This is an independent
source/proof challenge plus one execution of the producer's replay path, not a
second independent implementation of the full numerical checker. The contributor
previously authored the isolated integer-multiplication kernel and its tests;
the main common-action construction and pipeline were authored by the root.

## Source and contract

The immutable embedded owner archive has 6,330,093 bytes and SHA256
`f58b4f09eb259f0ac2d3962b955abd0fc7d603a7960a038257b72b1f00624115`.
The audit compared the actual imported `src/exact_residual.py`, saved Lanczos
NPZ, input-construction JSON and both NIST gzip files byte for byte against
that archive. They match. The imported residual module has SHA256
`bd3bf12b28727a0cbc500221984269b6c2eccf5acec76885e632bb74b2041d78`.

The inspected and replayed `src/common_action.py` has SHA256
`5324b9d584a1da54b9bd99ef8e1cb5421c1fe8a28e5b8e01a15a08a80b7dd9af`.
Its hash was unchanged across the replay. The main source itself checks the
source-file hashes, reconstructs the dyadic surrogate and compares the operator
scale, dimensions, allowance and norm bound to the pinned original receipt.

The intended operator is the original exact-decimal generalized matrix A, not
merely its dyadic surrogate. X concatenates all 512 stored basis columns, in
probe order, with denominator 2^29. The information class is

    {B=B^T : B X=A X, -(M+tau) I <= B <= (M+tau) I}.

This class is different from the eight independent scalar-J moment classes.
The original per-probe completion errors are not silently dropped: they are
irrelevant to this new direct-source action contract. The method pays for new
exact shared action on all 512 columns of its conditioned basis. It may not be
described as obtaining this action from the J coefficients alone.

## Change of coordinates and rank

The SVD only proposes a dyadic matrix C. The guarded integer kernel computes
Z=X C exactly, at denominator 2^61. W is the nearest dyadic coordinate matrix
at denominator 2^40. The exact integer discrepancy gives
`||Z-W||_F <= delta`, and the exact Gram gives
`||W^T W-I||_F <= gamma <1`.

The code checks `delta < sqrt(1-gamma)` with an outward lower square-root
bound. Thus Z has full column rank 512. Since X and C both have 512 columns,
this proves that X has full column rank and C is invertible. Consequently
`B Z=A Z` is exactly equivalent to the required `B X=A X`. No numerical rank
decision is trusted.

The recorded bounds are approximately gamma=2.6866965145e-6,
delta=1.9459816486e-10, sigma_min(W)>=0.99999865665, and
||Z||<=1.00000134355. These decimals are descriptive; the receipt stores the
rational bounds actually compared.

## Strict support

The signed symmetric surrogate has absolute row sums at most M. Every connected
component of its nonzero graph contains a row with a strictly smaller sum. If
an eigenvalue had modulus M, choose an eigenvector entry of maximum absolute
value. Equality in the row estimate would force that row to have sum M and all
its nonzero neighbors to have the same maximum magnitude. Propagation through
the component reaches the deficient row, a contradiction. Therefore
`||Abar||<M`. This argument handles signed entries and singleton components.

The exact source construction proves `||A-Abar||<=tau`. Hence
`||A||<M+tau`, giving the strict interior premise for both compressed inverses
and the global ambiguity count n-d. The checker found component sizes
1071,1,1,1 and a deficient row in every component. No positivity of the physical
stiffness matrix or unverified minimum eigenvalue is assumed.

## Exact-input pencil bridge

For b equal to either support endpoint and the exact threshold t, the target
pencil is

    P_b(A,Z)=Z^T [A^2-(b+t)A+b t I] Z.

Set E=A-Abar. Even when A and Abar do not commute,

    A^2-Abar^2 = Abar E + E Abar + E^2.

Therefore

    ||P_b(A,Z)-P_b(Abar,Z)||
      <= ||Z||^2 tau [2M+tau+|b+t|].

For R=(Abar-bI)(Abar-tI), `||R||<=(M+|b|)(M+|t|)`. Expanding Z=W+D gives

    ||Z^T R Z-W^T R W||
      <= delta (2||W||+delta) (M+|b|)(M+|t|).

These are exactly the two allowances in the source. The compressed surrogate
pencil is assembled from exact integer `W^T W`, `W^T Abar W` and
`(Abar W)^T Abar W`, with the correct denominators. Its dyadic quantization
error is bounded by an exact Frobenius sum. All three allowances are added
outward. The numerical diagonalization supplies only proposals; the inherited
integer residual/Gram checker then bounds the eigenvalues of the ORIGINAL
target pencil using the full accumulated allowance.

An independent rational recombination of the saved receipt confirmed the two
allowance formulas, their sum, the rank inequality, the exact threshold and
the count arithmetic. No additional numerical precision sweep was run.

## Counts and endpoint attainment

The lower-endpoint pencil has inertia (negative,zero,positive)=(47,0,465).
The upper-endpoint pencil has inertia (465,0,47). The checked sign margins,
after all eigenvalue, coordinate and original-input allowances, exceed
2.4395e-7 and 2.6544e-7 respectively. Both pencils therefore have no eigenvalue
at zero; the inclusive convention is resolved.

For the exact feasible extremal completions from the independently supplied
Schur-complement proof, the correct count formulas give

    min_B N_B(t) = n_+(P_U) = 47,
    max_B N_B(t) = n-d+n_-(P_L) = 1074-512+47 = 609.

Both endpoints are attained by the specified exact completion operators.
The width is 562/1074=281/537, and it equals the global maximum ambiguity
(n-d)/n. The result concerns the exact interval hull of attainable CDF values;
it does not assert that every real number between the endpoints is attained.
An empirical CDF takes values on the 1/1074 grid.

## Scope limitations that remain material

The endpoint matrices need not preserve the source matrix's sparsity, detailed
entries, physical interpretation, exact trace or any stronger unprovided prior.
The ambiguity is for the stated action-plus-support class. It is not an
impossibility theorem about computing the already known A, or about every
method using the full input.

The competing completions depend on the realized basis block X. This proves a
deterministic consistency-class statement; it does not yield a lower bound for
a fixed input selected independently of random probes. It also gives no
probe-weighted CDF monotonicity under Loewner order.

The exact extremal operators are specified by source-bound algebraic formulas.
The checker certifies their needed compressed inertias without materializing
their dense n-by-n entries. This is a valid exact representation, not a claim
that rounded floating endpoint matrices themselves are the witnesses.

## Replay and resources

Exactly one complete `--replay` was run. It returned PASS with counts 47 and
609 and reproduced the producer's source identities, coordinate bounds,
pencil hashes, witness hashes, sign margins and endpoint widths. It made no
new random draw, SVD, eigensolver call or Krylov step. The source imports the
eigensolver function but the replay branch never invokes it.

The replay body took **39.30656651499885 seconds wall**, **39.506364305 seconds
process CPU**, with **239,243,264 bytes peak RSS**. The enclosing subprocess
took **39.75867776499945 seconds wall**, including interpreter/import costs.
The existing main replay receipt was absent before this invocation; the newly
created `results/common_action_replay.json` is preserved unchanged. Additional
audit receipts are `common_action_audit_invocation.json`,
`common_action_audit.json`, and `common_action_independent_replay.log`.

Source inspection, analytical checking, the small rational recombination,
authoring and model inference are not fully metered. The wrapper time includes
the replay body and must not be added to it as a second independent expense.
No failed full replay, new optimization, or alternative full construction was
performed in this audit. Computational usefulness remains defeated by the
retained dense comparator; this correctness verdict does not reverse that cost
comparison.
