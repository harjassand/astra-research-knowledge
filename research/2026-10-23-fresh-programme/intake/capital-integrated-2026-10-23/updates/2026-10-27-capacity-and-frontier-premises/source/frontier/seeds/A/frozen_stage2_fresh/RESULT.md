# Fresh continuation result

27 October 2026. **The full all-copy qutrit Werner target is unresolved.
No negative rank-two witness for the original functional was obtained.**
This continuation preserves a completed conditional local theorem and
decisive obstructions to extending its proof globally. It does not mark
the scientific mission complete.

The frozen first-stage files were read and left unchanged. The continued
target remains every finite number of copies and every complex matrix of
rank at most two, with no restriction to real, normal, product, graph, or
selected support families.

## Completed mathematical continuation

`local_transfer.md` proves the following implication, including all
degenerate kernel directions and all orders:

\[
 \big[q_m(Z)\ge0\ \text{for every complex rank-two }Z\big]
 \Longrightarrow
 \big[\operatorname{diag}(uv^*,uv^*,0)\text{ is a local minimum of }q_{m+1}
      \text{ for every nonzero }u,v\big].
\]

Together with the already supplied exact lift, the reverse implication
also holds. Thus full local stability of this entire family is **exactly
equivalent to the global lower-copy target**. This is not a free induction.

The proof introduces a physical Gram slice. A local unitary selects the
lowest physical Gram line, removing the common-plane transverse null
directions. The transverse form is then coercive. A finite six-dyad
separable decomposition of the binary first-site form makes the remaining
binary term nonnegative using only lower-copy rank-two positivity.
An explicit factor-neighborhood bound is supplied: if its binary factors
are within \(2^{-m}/10\) of the normalized base, the transverse term is at
least \(2^{-m-1}(\|U_2\|_F^2+\|V_2\|_F^2)\).

This resolves the frozen handoff's local compatibility obligation
conditionally on precisely the lower-copy premise already required for
the Hessian: when \(Q=0\), the cubic real coefficient vanishes and the
constrained same-copy quartic \(q_{m+1}(XY^*)\) is nonnegative. Arbitrary
same-copy rank-two quartics are not assumed positive. Nearby zeros must
retain a common physical binary plane at the distinguished site.

## Full global obligation and opposition

`global_obligation.md` gives the exact arbitrary-factor splitting
\(q_{m+1}(C(t))=a+t^2T+t^4d/2\). Assuming lower-copy positivity,
\(a,d\ge0\), so the entire next-copy target is equivalent to
\(T\ge-\sqrt{2ad}\) for all unrestricted complex factor blocks. This sharp
global discriminant inequality remains unproved.

The following attempts to avoid that obligation fail rigorously:

- Globally nonnegative \(T\), even in the lowest-Gram-line slice, is false
  already at two copies. Exact rational factors give \(T=-147605/3362\).
  Their full two-copy value is positive, so they are not a target witness.
- A sliced \(T\) need not have only one negative direction. A rational
  two-plane has a negative-definite restriction with determinant
  \(892762964\).
- Lower-copy rank-two positivity, a positive crossed operator, its strict
  rank-one lower bound, and the norm bound do not suffice as black-box
  hypotheses for a global induction. A reconstructed known PPT activation
  model has all these properties (even matching the numerical bounds after
  embedding) but its product with the qutrit factor has an exact
  Schmidt-rank-two expectation \(-15/31\). This model is **not** the actual
  Werner tensor power and is not a counterexample to the task.

## Verification and limits

`check_local_transfer.py` checks the six-dyad identity with exact SymPy
arithmetic. Nine arbitrary complex identity/coercivity diagnostics for
one through three remaining sites passed; direct partial-trace residuals
were below \(2\times10^{-15}\). They validate the formulas, not the
lower-copy positivity premise.

`exact_opposition.py` uses exact rational arithmetic, including 6,561
entrywise partial-transpose comparisons for the PPT countermodel. It
passes under `python -O`. Receipts are in the corresponding JSON files.
An initial JSON serialization error in the added integer-factor receipt
was corrected; retained receipts are from the complete successful run.

`discriminant_probe.py` performs two unrestricted complex local descents
at three total copies after analytically eliminating the third-row scale.
Both approached the zero boundary \(T/\sqrt{2ad}=-1\) from above to
rounding accuracy; no negative target witness was obtained. Their direct
same-copy checks, iteration limits, and objectives are retained in
`discriminant_probe.jsonl`. Neither search certifies a global optimum.

The public CT/BD sources, frozen Hessian and exact lift, and pinned Astra
BQ projection-completeness text were read as prior work. The auxiliary
PPT activation mechanism is prior mathematics from Vollbrecht--Wolf,
[quant-ph/0201103v2](https://arxiv.org/pdf/quant-ph/0201103), reconstructed
here with exact coordinates. Historical novelty, a formalization,
independent external correctness audit, all-copy positivity, and NPT bound
entanglement are not established by this block.
