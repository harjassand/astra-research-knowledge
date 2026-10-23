# Focused integrated delta review

Reviewer: `/root/cycle11_entropy_drift_challenge`.
Date: 23 October 2026, Australia/Brisbane.

## Reviewed source and status

Principal source reviewed:

- `ENTROPY_DRIFT_AND_DEPTH_COST.tex`
- Final reviewed source: 35,221 bytes
- SHA256 `3afdc8e4b7028eac14317a8bb875b88698eb04201c8b36e8f4b8fa8d751fd2d8`
- Exact reviewed snapshot retained at `reviewed/ENTROPY_DRIFT_AND_DEPTH_COST_3afdc8e4b7028.tex`

The initial pass reviewed the 34,422-byte version, SHA256 `3dd135d05393550308dd05ff97502132eac23f146bf6180ed025444635fb54e7`. During review the principal added the recommended reference-identity clarification, explicit entropy notation and prefix definition, and corrected the included square notation. The final source above was then reread; the status below binds that final version rather than silently rebinding the initial pass.

**Status: PASS_AFTER_CLARIFICATION_AND_TYPOGRAPHIC_REPAIR. No outstanding requested correction in the examined scope.** No new computation or previous suite was rerun. This is a targeted source review, not external certification, a historical-originality assessment, or a delivery receipt.

The requested delta scope was the integrated all-normal operator theorem, finite-error input-entropy bound with a general CPTP encoder, the pure repeated-color input example, and the proposed reference-leakage frontier. I also read the new inherited-code depth-budget include to check how the operational lower is paired with the upper.

## 1. All-normal whole-bath theorem

The integrated proof correctly handles coherent bath depths, for which the compressed outgoing charge need not commute with input charge. It uses the valid operator inequality

\[
B^*(\log T)B\le\log(B^*TB),
\]

then trace-exponential monotonicity and finite-dimensional Golden–Thompson. It does not assume operator convexity or operator monotonicity of exponential.

The tilted map's sequential identity is correct in the written Kraus order. The exact root term

\[
\Psi_\lambda(I)=f_\lambda I-a(e^\lambda-1)P_0
\]

has the right sign for \(\lambda\ge0\). Positivity justifies iteration without an independent-channel replacement. Taking every normal bath vector state after the entropy bound correctly produces the full bounded operator lower bound. Infinite initial mean depth is harmless because the governing displacement remains bounded.

The theorem holds at both \(b=0\) and \(b=1\). At the identity endpoint the bound reduces to the input-dimension entropy bound. Its implication for one nonpositive bath expectation is valid and weaker in assumptions than a nonpositive full bulk operator.

## 2. Arbitrary-CPTP-encoder entropy bound

The finite-error lemma is correct as written. A full-diamond error \(\epsilon\le1\) gives half trace distance at most \(\delta_e=\epsilon/2\) for the decoded Bell state. Measuring the target ray gives overlap at least \(1-\delta_e\). Pinching into that ray and its complement yields

\[
S(R\widehat R)\le h_2(\delta_e)+\delta_e\log_2(K^2-1).
\]

The relevant entropy bound is increasing over the admitted error interval for \(K\ge2\), so replacing the actual infidelity by \(\delta_e\) is legitimate. The proof separately treats \(K=1\).

The untouched logical reference is exactly maximally mixed. Araki–Lieb therefore gives

\[
I(R:\widehat R)\ge2\log_2K-2S(R\widehat R).
\]

The physical channel and decoder act only on the encoded port state and an initially independent bath, so data processing applies to the actual mixed encoded joint state \(RA^N\). The estimate

\[
I(R:A^N)\le2S(A^N)
\]

does not require the encoder to be isometric. Thus the stated

\[
S(\rho_N)\ge(1-\epsilon_N)\log_2K-h_2(\epsilon_N/2)
\]

is valid for a general CPTP encoder. The full/half error conversion in the following theorem is correct. The phrase that no supplied system is initially correlated with the bath should continue to cover the logical reference and any retained encoder ancilla as well as the port marginal; that is already the intended channel contract.

Finite propagation correctly converts bounded displacement into a difference of means only when the initial mean is finite. At actual \(\tau_\pi\), the mean is \(1/2\), so the advertised rate–depth expenditure theorem is justified. No unbounded mean is subtracted in the all-normal statement.

The explicit optimized scalar cost envelope was also checked algebraically. The quadratic equation for \(z=e^\lambda\) is

\[
a(1+v)z^2+3bvz+2a(v-1)=0,
\]

which gives the root written in the source. The transition to \(\lambda=0\) occurs at \(v=a/3\), because \(f'_0/f_0=-a/3\). The \(b=0\) comparator is the ordinary charge-entropy expression stated there.

## 3. Pure-push depth/entropy counterexample

This is a correct actual-device counterexample to replacing reference leakage by a bare depth lower bound.

For each pure input \(|1\rangle\), the two bath Kraus operators are \(\sqrt a S_1\) and \(i\sqrt b I\), with distinct emitted symbols. Every length-\(N\) output word with \(j\) pushes therefore induces the same bath map \(S_1^j(\cdot)S_1^{*j}\), apart from its scalar amplitude. Tracing distinct output words and collecting equal \(j\) gives exactly the binomial mixture in the principal source. This argument retains all coherent amplitudes before the output trace and does not require bath branches with different \(j\) to be orthogonal.

The actual isometry \(S_1\) increases depth by one even at vacuum. Thus the mean is exactly \(1/2+aN\) from \(\tau_\pi\). Each shifted bath density has the same finite entropy as \(\tau_\pi\), so the finite-mixture entropy upper is valid.

More strongly, if \(EF_0\) starts in a purification of \(\tau_\pi\), each branch

\[
(S_1^j\otimes I)|\Omega_{\tau_\pi}\rangle
\]

is a normalized pure state. The joint final \(EF_0\) state is therefore a mixture of at most \(N+1\) pure states, and

\[
S(EF_0)\le H(\operatorname{Bin}(N,a))\le\log_2(N+1).
\]

At \(b=0\), its entropy is zero, while the bath marginal retains exactly \(S(\tau_\pi)\). All these claims are consistent with one another. The input is a fixed pure word, so no logical reference information is present. The source correctly says that this does not demonstrate high-rate reliable communication or refute a reference-aware converse using the code entropy.

## 4. Proposed next leakage inequality

For a purification \(R\) of the physical input \(\rho_N\), and a purification \(F_0\) of the independent initial bath, the post-interaction state on \(R B E_NF_0\) is pure. Therefore

\[
S(\rho_N)-I(R:E_NF_0)=S(B)-S(E_NF_0)
=I_c(\rho_N,\mathcal N_N^{\tau_\pi})
\]

is exact. All entropies in this identity are finite: the finite dimensions of \(R\) and \(B\) bound the entropy of their complementary joint system, even though its Hilbert space is infinite.

The candidate inequality is explicitly marked unproved, and no settled capacity conclusion is drawn from it. The pure-push example has zero right-hand side in that candidate and therefore does not refute it.

**Continuation clarification, now incorporated in the final reviewed source:** a purification of the physical input is not automatically the original logical reference when the encoder is a general CPTP map. Turning an input-purification coherent-information upper into a converse for every admitted code still needs an encoder reduction or a corresponding inequality formulated directly for the actual encoded reference state. The present finite-error theorem does not have this problem because it works directly with the actual logical reference and mutual information. This is an explicit remaining obligation for the proposed next programme, not a gap in any theorem currently claimed.

## 5. Operational lower and typography

The inherited-code depth-budget proof uses the actual encoder's uniform joint overflow bound, the finite propagation interval for the low-depth component, and the exact geometric initial tail. It correctly avoids multiplying the initial tail by the spectral-type probability. Its conclusion is uniform over logical inputs; decoding on emitted outputs cannot change the unconditioned bath marginal. The resulting \(O(\log N)\) final mean depth is a valid additional property of the retained lower code at actual \(\tau_\pi\).

**Typographic repair, completed:** the initial included `INHERITED_CODE_DEPTH_BUDGET.tex` printed `r_{A_n}^{,2}` in the depth inequality, positive-block estimate, and definition of \(\delta_n\). The final include uses `r_{A_n}^2`. The surrounding argument, later scalar estimate, and inherited lemma already used the correct square; this was a display/notation error rather than a mathematical gap. The corrected include is 7,228 bytes, SHA256 `dddc42af6fa44d8e486d7dec806f9ec1ba6c0f7deda663950c7e51850d9b04a2`.

## Final assessment

No substantive gap was found in the examined integrated theorems or the pure-input counterexample. The main new result is stronger than the original bulk-pressure operation: it supplies an all-normal entropy/displacement inequality and a finite-error operational resource bound. It still preserves the necessary distinction between sublinear-depth capacity and unrestricted capacity. The chosen reference-leakage continuation is scientifically justified and has a genuine unproved obligation.

No new test run was necessary for this delta review. Inference and total review costs are unknown. This review binds the exact principal hash stated above and must not be silently rebound to a later version.
