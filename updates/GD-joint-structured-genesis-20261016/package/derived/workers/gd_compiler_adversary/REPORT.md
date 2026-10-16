# Compiler adversary report

16 October 2026. Independent worker `gd_compiler_adversary`; pinned source worktree revision `2688d7a383502df4fc1e64001d04bb76e6ec05e5`. No source/original bytes were edited. No installation, subagent, outreach, or Git mutation was performed.

## Decision

The supplied finite-rate Choi range criterion, optimized identity-shift signs, fixed signed-floor argument, and local four-Kraus correlated-edge construction survive this reconstruction. I did not find a decisive algebraic flaw in those claims. Their structured error class is correctly separated from the unrestricted `2ν/d²` fixed-baseline diamond-ball obstruction.

There is new, model-specific progress beyond reconstruction: a fixed floor for actual single-face unitary miscalibrations of the pair-correction jump, with an exact optimal clock rate among all fixed CPTP centers. A related Pauli-averaged floor remains exact when its conditional actions suffer the same common unknown single-face rotation. Both preserve 11-qubit support. These are conditional finite-dimensional synthesis results; the global memory proof, historical originality, apparatus assumptions, and practical usefulness remain unresolved.

## New claims and decisive evidence

1. **Sharp correlated-edge resource.** For the source edge class `|z|<=M`, every fixed center `N` with `N+E_z/Λ` CPTP for all admitted `z` requires `Λ>=4M`. A chosen phase gives normalized Choi eigenvalues `M,M,-M,-M`; requiring positivity for both signs forces the unit-trace center to carry at least `4M/Λ` trace. The source four-Kraus floor attains `4M`. This lower bound allows every fixed CPTP center and arbitrary Kraus rank, not only Pauli dephasing centers.

2. **Actual correction-unitary family.** Let `A=QΠ` be the source pair jump without its `sqrt(κ)` scale, and keep its inactive completion. Admit `A_actual=exp(-iθΣ_j u_jP_j)A`, `|θ|<=θ_0`, with real unit `u` over `m` selected single-face Pauli axes (`1<=m<=3`). This is a correlated physical correction-generator difference, rather than an arbitrary coefficient sample. With `q_0=sin²θ_0`, `t_0=sinθ_0 cosθ_0`, the exact minimax fixed rate is

   `Λ=κ[2sqrt(m)t_0-(m-1)q_0]`, for `θ_0<=arctan(1/sqrt(m))`,

   and `Λ=κ` for larger intervals.

   Install `α(C_0-Id)+βΣ_j(C_j-Id)` with `C_j` the completed action `-iP_jA`, `α=κ(q_0+sqrt(m)t_0)`, and `β=κ(t_0/sqrt(m)-q_0)`. Its rates sum to `Λ`. Positivity reduces to one explicit two-dimensional block, including singular endpoint cases. A projected active-input Choi matrix and signed-permutation symmetrization give the matching lower bound against every fixed CPTP center. The proposal needs at most `m+2` Kraus operators and the same 11-qubit patch.

3. **A floor with the same common actuator error.** The optimal weighted floor assumes its extra channels are implemented as specified. If every conditional action inherits the same unknown single-face postrotation, use the uniform average of all four conditional Pauli actions instead. Its active output is depolarized on the written face, so the common rotation cancels exactly. A floor rate `ν=4κsinθ_0` absorbs the actual correction difference for all unknown axes and angles in the admitted interval. It retains the original patch and does not estimate the rotation. Command-dependent errors, faulty checks, inactive-branch errors, and leakage remain outside this model.

Complete proofs, including the exact quantifiers, are in `PROOFS.md`, Sections 3–5.

## Overlap and resource accounting

One physical face lies in exactly 11 primal pair supports and 11 dual pair supports. A uniform rate `Λ` per pair therefore charges `12Λ` per vertex owner cell over both sectors and `22Λ` incident to a physical face. Guard rates count every proposal support intersecting the enlarged guard; a bound on an arbitrarily named patch is insufficient. A side-five torus enumeration checks the incidence, and the counting proof is `4·3-1=11` per sector.

The unitary-action synthesis installs a different regularized completed-pair generator. Its exact decomposition retains ideal correction clocks at rate `κ` and declares the floor/error combination a rare arbitrary local proposal at rate `Λ`. The source's schedule-uniform Kraus-span interface can consume this decomposition if its charged local ceiling holds. All envelope, LSS, HT, finite-torus replay, homology, encoding and decoding obligations are inherited; this worker did not independently establish them. The original active-only generator gains no theorem from this argument.

The optimum floor can require up to four additional completed conditional action streams per pair, or `m+1` for an `m`-axis catalog. At small three-axis angle, their total rate is approximately `2sqrt(3)κθ_0`. The common-error-invariant alternative uses four streams totaling approximately `4κθ_0`. These are mathematical implemented-generator costs, with no acquired physical implementation or useful numerical threshold.

## Adversarial boundaries retained

- The source rate criterion fails permanently if the residual drift has any component outside the noise range. A singular generalized inverse cannot repair it. Amplitude damping provides a negative principal minor at every finite rate.
- A signed difference of two correction dissipators need not be Lindblad. Its physical correlation constraints can be useful, but positive-semidefinite assumptions cannot be imported silently.
- Known sparse coefficients, a known action error, and an arbitrary operator-norm or diamond-norm patch ball are different inputs. In particular, a per-instance Pauli one-norm bound from Parseval does not give a fixed coefficientwise box of the same summed size. Section 6 of `PROOFS.md` preserves this distinction.
- Bounded body count does not imply bounded geometric diameter. A distant weight-two correlation violates the fixed guard premise even if its incident count is bounded.
- The unrestricted diamond-ball minimax result holds for fixed affine centers and fixed rate. It is neither contradicted by these restricted families nor a no-go theorem for all memory designs.

## Bounded independent tests

Run `python3 independent_checks.py` from this directory. It uses existing NumPy and writes `CHECK_RESULTS.json` only in this worker directory. The current run passed:

- Gauge/Kraus generator reconstruction: maximum error `1.78e-15`; a rate below the optimum has a negative Choi eigenvalue. Four amplitude-damping minors match their analytic negative values.
- 45 commuting/anticommuting complex-edge cases, including boundary singularities: maximum error `8.33e-17`; all three sharp edge witnesses have Choi trace norm exactly `4M` to floating precision.
- 48 signed coefficient samples under one fixed floor, with seven zero-floor directions and exact cancellation: minimum numerical Choi eigenvalue `-9.54e-17`, null-space residual at most `1.26e-17`.
- 360 actual correction-unitary instances across one/two/three axes, small angles, critical angles and larger intervals: maximum map/trace-preservation error `2.78e-13`; worst coefficient eigenvalue `-2.27e-16`. The active-input Choi family is orthonormal to `2.22e-16`. Smaller endpoint clock budgets yield negative witnesses.
- The common-postrotation floor identity holds to `2.78e-17`; its worst coefficient eigenvalue is `-1.63e-16`.
- A side-five 4D torus has 3,750 physical faces; each has primal incidence 11. Actual 11-qubit trace orthogonality is also checked symbolically from stabilizer supports.

These checks test algebra and geometry; they do not certify asymptotic memory correctness, historical originality, physical fault tolerance, or device advantage.

## Provenance and remaining work

`PROVENANCE.json` records the exact read paths, byte hashes, source-manifest verification, pinned worktree revision, and execution scope. `FROZEN.json` hashes the final worker artifacts. The source compiler and regularization audit were read completely. The pair theorem and completion/envelope interface were read for applicability; their other imported lemmas remain outside this worker's verification scope.

The next consequential check is independent verification of the physical-family minimax proof and the common-error-invariant floor, then apparatus qualification of the single-face action-error model. Repeating the supplied sparse-compiler tests would add little. Prior-art clearance remains open; `PRIOR_NOTES.md` records the limited primary search and nearby standard frameworks.
