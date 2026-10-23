# Independent audit of the exact integer residual checker

Date: 21 October 2026. Author scope: the projection/Jacobi subagent's local implementation challenge, requested by the main investigator. This audit does not choose a new application, repeat the full experiment, or change `src/exact_residual.py`.

## Finding and disposition

The mathematical formulas in the audited checker are valid under the stated exact-integer, self-adjoint, dimension and nonnegative-input-error hypotheses. The first static review found that several of those hypotheses were not enforced at the public certificate boundary. The main investigator added the enforcement before the first dynamic adversarial probe ran.

The repaired source audited here has SHA256

`bd3bf12b28727a0cbc500221984269b6c2eccf5acec76885e632bb74b2041d78`.

The independent challenge suite is
`checks/challenge_exact_residual_projection_agent.py`; its receipt is
`results/exact_residual_projection_agent_audit.json`. It passed with Python assertions disabled (`python3 -O`). No eigensolver or solver status enters its exact admission tests. The separate small polar computations are floating diagnostics and are identified as such.

### Defects identified in the original boundary

The original public functions did not enforce that the sparse operator was exact integer data and symmetric, did not require a nonnegative original-input allowance, and converted proposed diagonal, off-diagonal and probe scalars with potentially lossy `int`/`int64` conversions. Probe lengths could be silently truncated by `zip`.

These are substantive certificate-boundary defects even though the intended loader and proposals already obeyed the relevant contracts. For example, before the patch, a one-column coordinate basis `vi=2^29 e1`, floating sparse numerator `ai[0,0]=2^-30`, zero Jacobi diagonal and exact probe `e1` pass the untyped arithmetic path. The product is `av[0,0]=1/2`, and conversion to Python `int` in the last Rayleigh product discards it. The reported completion error becomes zero although the represented matrix entry is `2^-62`. Similarly, a negative supplied `tau` could produce a negative total error allowance. These examples are algebraic reconstructions of the reviewed source; this audit does **not** claim that a pre-patch dynamic run was performed.

The main branch now requires an exact `int64` canonical CSR operator, exact symmetry, valid positive dimensions, an `int64` basis and probe with matching shapes, exact integer diagonal and sub-diagonal values before conversion, a positive exact integer probe denominator, and `tau >= 0`. Boolean and fractional integer surrogates are rejected. Both the initial eight-case probe and the full challenge observed the repaired version. The initial receipt is `results/exact_residual_initial_adversarial_probe.json`.

## 1. Exact decimal generalized operator to dyadic matrix

The target is the mathematical matrix

\[
A_{ij}=\frac{K_{ij}}{s\sqrt{m_i m_j}},
\]

where `K` and the positive diagonal masses are the exact rational values of the stored decimal source tokens, and `s` is the computed positive power of two. This statement covers the stored finite model; it does not assert a bound on physical model error.

For a nonnegative rational `x`, `sqrt_interval(x,bits)` computes

\[
a=\left\lfloor\sqrt{\left\lfloor 2^{2b}x\right\rfloor}\right\rfloor.
\]

The elementary identity `floor(sqrt(floor y)) = floor(sqrt y)` for `y >= 0` proves that `[a/2^b,(a+1)/2^b]` encloses the root. The interval collapses exactly when the rational squared-endpoint comparison is an equality. Every comparison and square root in this construction uses arbitrary-precision integers. Negative radicands are rejected.

If `[l,h]` encloses the positive denominator root, the numerator-sign branches correctly use `[K/h,K/l]` for nonnegative `K` and `[K/l,K/h]` for negative `K`. The reported scale is at least the largest enclosed absolute row sum. Thus the normalized exact symmetric target has operator norm at most one. This normalization is a bound on the source operator, not a supposition about the numerical spectrum.

For each enclosing coefficient interval `[a,b]`, the chosen dyadic numerator is nearest rounding of its midpoint. If that numerator is `z`, then

\[
|A_{ij}-z/2^{32}|\le\max(|a-z/2^{32}|,|b-z/2^{32}|).
\]

Summing these rational bounds by symmetric rows gives an operator-norm bound because the error matrix is symmetric and `||E||_2 <= ||E||_infinity`. The final upward dyadic rounding preserves the bound. Consequently the reported `tau` connects the exact original decimal operator to the exact dyadic surrogate; it is not merely a rounding statement about a separately constructed matrix.

The independent fixtures use both rational and irrational cross-mass roots, negative coefficients, explicit zero coefficients, and exact positive/negative half-way rounding. A separate rational bisection routine at 170 fractional bits derives a source enclosure and checks it against the published `tau`. It does not reuse the checker's integer-square-root implementation. The exact half-way fixture yields `tau = 2^-33`, as required.

The loader deliberately rejects positive masses too small for its fixed root precision to prove a strictly positive denominator lower bound. The tested masses `1e-100` exercise this valid-input precision rejection. It produces no certificate, and its execution cost is included. No claim of support for arbitrary dynamic range is made.

Source hashes in the receipt identify the files read. The integrating replay still must compare those hashes and the recomputed scale/allowance with the specified scientific inputs. This audit only uses synthetic local fixtures and does not independently establish the identity of the full NIST source pair.

## 2. Signed rounding and integer kernels

For every rational `x=p/q`, `q>0`, the nearest-integer rule

\[
\left\lfloor\frac{2p+q}{2q}\right\rfloor
\]

has error at most one half and sends exact ties upward, including negative ties. The ceiling routine is the exact rational identity `ceil(2^b x)/2^b`; it remains an upper bound for negative values. The tests cover 2,771 signed nearest-rounding cases and 8,313 upward rounds.

Let `vmax` be the largest absolute stored basis integer, let `arow` be the largest absolute sparse operator row sum, and let `jrow` be the largest absolute Jacobi row sum. Every individual multiplication and every partial sum in `ai @ vi` has absolute value at most `arow*vmax`. Symmetry of the tridiagonal Jacobi matrix makes each of its column sums also at most `jrow`, so each intermediate in the explicit `VJ` construction has absolute value at most `jrow*vmax`. Requiring their sum to be at most `2^63-1` protects both kernels and the subsequent residual subtraction. Cancellation does not waive this guard.

For the Gram matrix, write `Nj=sum_r vi[r,j]^2`, computed with Python integers. Every absolute partial dot product is at most

\[
\sum_r |v_{ri}v_{rj}|\le\sqrt{N_iN_j}\le\max_jN_j.
\]

The guard `max Nj + 2^58 <= 2^63-1` therefore protects every Gram multiply/accumulate and subtraction of the dyadic identity. It is conservative at the signed negative endpoint, which is harmless. Subsequent squared norms and Rayleigh products explicitly convert each factor to arbitrary-precision Python integers before multiplication.

Sixteen small integer-kernel comparisons, including a case close to the signed integer limit, agree exactly with Python arbitrary-precision matrix products. Four separate tests verify rejection of unsafe operator multiplication, residual subtraction, Gram multiplication, and a deceptively cancelling sparse product.

These arguments assume normally constructed NumPy/SciPy arrays whose structure is not mutated concurrently with checking. The suite does not attempt to certify arbitrary corruption of a sparse object's internal buffers or cached format flags.

## 3. Polar and intended-probe budgets

The checker first bounds the Gram Frobenius norm by `gamma < 1`. If `Q` is the polar factor of the dyadic basis `V`, then

\[
\|Q-V\|_F^2
=\sum_i\frac{(1-\sigma_i^2)^2}{(1+\sigma_i)^2}
\le\frac{\gamma^2}{(1+\sqrt{1-\gamma})^2}.
\]

Thus the outward-rounded `d` bounds the **Frobenius** distance, which is strong enough for the first-column residual budget

\[
r\ge\|((\bar A Q-QJ)P)\|_F
\le r_0+(M+K)d.
\]

The last-diagonal allowance follows from

\[
|q_k^T\bar A q_k-v_k^T\bar A v_k|
\le M\|q_k-v_k\|(1+\|v_k\|)
\le Md(1+\sqrt{1+\gamma}).
\]

The code uses lower root endpoints in denominators and upper endpoints in numerators/norm allowances. The upward rounding directions are therefore correct. For `k=1`, `P=0`; setting `r=0` is valid. An exact two-column retained recurrence with a nonzero last omitted coupling `3/32` correctly reports zero completion error. That allowed omitted coupling is not confused with an error in an earlier recurrence column.

For the intended probe, the exact stored vector is `g=gi/gd`. Its positive norm is enclosed by `[gl,gh]`. If `v^Tg >= 0`, dividing by `gh` gives a lower bound on the normalized inner product; if `v^Tg < 0`, dividing by `gl` gives a lower bound. Hence the square root of `||v||^2+1-2*inner_lower` bounds the distance to `g/||g||`. The reported `start_error=min(1,start0+d)` is a **spectral-projector probability error**, as used by the main envelope. It is not a claimed bound on vector distance after clipping at one.

Three column-scaled coordinate frames have an exactly known polar factor and rationally checkable Frobenius and probe-distance bounds. Thirty-three additional small numerical polar computations are diagnostics. Their maximum floating overshoot in any checked scalar was `2.220446049250313e-16`, within the explicitly stated diagnostic tolerance `2e-12`. No floating diagnostic supplies an exact error bound.

The sharp completion theorem and the separate sorted-spectrum dense-comparator theorem have other assigned reviewers. This audit checks the scalar `gamma`, `d`, `r`, `z` and probe quantities on which the completion relies; it does not duplicate those full theorem reviews.

## 4. Observed cost and remaining scope

The full independent suite body took `0.08095949000016844` seconds wall time and `0.08009497199999993` seconds CPU. Peak process RSS was `50,458,624` bytes. Its tool-reported process invocation took `0.841865104` seconds, including startup/imports and receipt output. The earlier eight-case adversarial probe body took `0.0013240320004115347` seconds; its CPU time was not separately recorded. Both observed runs checked the repaired source.

The suite includes 27 malformed certificate-boundary rejections, six rejected loader cases (one a deliberate finite-precision limitation), and four overflow rejections. There were no failed suite runs. Source inspection, proof reasoning, code-writing and tool orchestration time are not included in the process-body timings and must not be presented as zero cost. No full matrix or scientific-data run was performed by this audit branch.

The repaired public entry points pass this bounded challenge. The source allowance remains conditional on correct input identity, and the scientific result still depends on the separately checked completion, quadrature, perturbation, sampling and comparator arguments. This local pass establishes neither a practical speed advantage nor an error contract for a different target.
