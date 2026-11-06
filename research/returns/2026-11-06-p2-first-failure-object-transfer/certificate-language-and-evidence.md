# Unconditional generator failure, a one-split bypass and evidence

The direct family identity prompted a candidate certificate language: nonnegative finite sums of affine squares, integer-affine consecutive products `ℓ(ℓ−1)` including integer shifts, and nonnegative functions of at most two original bits, modulo`x_i²=x_i`. The [returned report](package/RESEARCH_REPORT.txt) refutes unconditional completeness even with unlimited terms and coefficient magnitude.

Its six-bit nonnegative quadratic is

`F=3x₅+x₆+Σ_(1≤i<j≤4)x_ix_j−2x₅(x₁+x₂+x₃+x₄)−x₆(x₁+x₃)+x₅x₆`.

This is the established Grishukhin`Gr₇` cut inequality in six-bit form, credited to Avis–Ito, not a claimed new inequality. Its minimum is0 at the all-zero assignment. Two restrictions prove nonnegativity directly. With`U=x₁+x₃−x₆` and`S₄=x₁+x₂+x₃+x₄`:

- At`x₅=0`, `F=Σ_(i<j≤4,{i,j}≠{1,3})x_ix_j+(1/2)U(U−1)`.
- At`x₅=1`, `F=(1/2)(S₄−2)(S₄−3)+x₆(1−x₁)+x₆(1−x₃)`.

Every term is nonnegative on binary inputs. A single split on`x₅` therefore certifies it immediately. Multiplying the two identities by`1−x₅` and`x₅` and adding makes cubic terms cancel. Those conditional multipliers lie outside the unconditional quadratic language being refuted.

The supplied [rank witness](package/GRISHUKHIN_WITNESS.json) contains all21 zeros, the22 degree≤2 multilinear features, their`21×22` evaluation matrix and coefficient vector. Deleting the final`x₅x₆` column gives an integer determinant`−1`, proving rank21 and a one-dimensional quadratic nullspace spanned by`F`. In any nonnegative-generator sum for`F`, each weighted summand must vanish at every zero, hence be a nonzero positive multiple of`F`. Affine squares/consecutive products have off-diagonal structure proportional to`v_i v_j`; `b₁₂=1`, `b₁₆=−1`, `b₂₆=0` rules that out. A two-bit function cannot be a nonzero multiple of this multi-bit quadratic. Thus no finite certificate in the specified unconditional cone exists. This is not merely a failed search for a short certificate.

That cone failure does not preclude conditional certificates, higher-degree/global inequalities or arbitrary optimisation. Full coordinate branching makes the conditional language complete through constant leaves, but the obvious construction can have`2^n` leaves. No polynomial bound is supplied on branch/piece count, coefficient bit lengths, certificate discovery or verification cost. Existence of short certificates and deterministic construction of assignments/certificates are different obligations; neither can be hidden in advice or preprocessing.

The source notes conditional complexity consequences: a sound, complete polynomially bounded and efficiently verifiable system for arbitrary quadratic nonnegativity would imply`NP=coNP`; a uniform polynomial-time constructor with known timeout and sound verifier would imply`P=NP`. These are implications, not impossibility proofs. An unrestricted exact optimiser is not required to use this language. Energy bounds from the sum of absolute binary coefficients keep the requested minimum/value and`n`-bit minimiser polynomial in output size.

| Producer-reported exact evidence | Scope |
|---|---:|
| Odd-family exhaustive assignments | 10,920 across odd`n=3,…,13` |
| Symbolic direct-certificate identities | 50 odd values through101 |
| Formal-moment parameter cases | 9,455 `(p,q)` pairs |
| Forced-frontier recurrence cases | 30 values of`m` |
| Six-bit object | All64 assignments |
| Zero-set determinant | Exact`21×21` minor`−1` |
| Signed-binary fixture round trips | Both explicit instances |

The general family proofs come from algebra/counting, not passing bounded tests. For the fixed six-bit object the supplied nonzero determinant is a complete finite witness for the stated rank. [AUDIT_RESULTS.json](package/AUDIT_RESULTS.json) is the producer's exact finite-check record, not a new Capital or external audit. The [checker](package/verify_continuation.py) includes bounded exponential enumeration and is not an unrestricted polynomial solver. Capital ran none of it.

[RECEIVED_TRANSFER.json](package/RECEIVED_TRANSFER.json) records the incoming P1 family and says the peer archive was not retrieved. [The new failure objects](package/FAILURE_OBJECTS_ONLY.json) omit preferred repairs/proof narratives and were retained without a further outgoing exchange. The actual transfer episode and completed new science are documented; no controlled feedback or coordination-policy benefit follows from their temporal sequence. The earlier independent packet and all its accepted restrictions remain unchanged.
