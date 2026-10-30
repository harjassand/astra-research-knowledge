# Two-good source/capture composition: independent algebra
2026-10-30. Conditional receiving lemma, not proof of a joint quantum capture implementation.

## Exact premises
Let rho be the actual completed source state in its ideal toggling frame, V the fixed ideal frame-restoring unitary channel, and Pi_s the virtual good-pattern projector in that input-defect basis. V is not a second execution of the noisy source. Suppose its positive tail is at most delta_s uniformly in the allowed retained bath/reference. Let J be the actual pointer-Z recording instrument, retaining a historical classical outcome m in the analysis and placing the physical raw latch in |m>. J must preserve the established source pointer-component identity; an arbitrary instrument merely producing a genuine classical label does not suffice. Any measurement-label errors need their own incorporation in the error pattern or an instrument-level module proof.

Let C be the actual capture channel after J. Conditional on every m, assume its final physical ports obey the uniform positive subset effect bound relative to m, including arbitrary conditional DATA/bath states. This is the contract supplied by the stated classical port theorem, not an independence premise. For this algebra assume C acts as identity on quantum DATA tensor a channel on capture/gauge/bath. More generally replace this with an explicit proven preservation/intertwining law for the source modules. A classical port effect alone does not provide such a law.

Let Q_c be the final diagonal projector selecting port-error patterns g=m'+m that are capture-good. It is diagonal jointly in final physical ports and the historical classical m reference. This reference is a mathematical record of an actually executed instrument, not additional protected hardware.

## Exact subnormalized comparison
Set rho_s=Pi_s rho Pi_s and sigma=C J V(rho_s), retaining m. The first gentle estimate and complete contractivity give

    ||C J V(rho)-sigma||_1 <= 2 sqrt(delta_s).

The uniform capture effect applies separately to EVERY conditional positive state in J V(rho_s), irrespective of how virtual projection changed its bath correlations. Thus Tr[(I-Q_c)sigma]<=delta_c Tr(rho_s)<=delta_c. The second gentle estimate gives

    ||sigma-Q_c sigma Q_c||_1 <= 2 sqrt(delta_c).

The total actual-to-good comparison is at most 2sqrt(delta_s)+2sqrt(delta_c). No source/capture marginal probabilities are multiplied. No source-pattern measurement is executed. No normalization by a good probability is taken. These are positive CP restrictions rather than signed fault flags.

## Deterministic union criterion
For a graph witness W of size s, if both support covers F and G contain fewer than s/8 vertices of W, then |(F union G) intersect W|<s/4. This is sufficient for the original quarter-occupied completed/repair witnesses and the half-occupied bridge witnesses. Use precisely the same rooted-union witness families as in the corrected source certificate: every component contains at least one selected root. Terminal-baseline support budgets must also be split between F and G, with selector multiplicity paid. Physical boundary defects remain source-only in a DATA-identity capture channel.

Capture-good is imposed on the ACTUAL final error support G=supp(g), not on hypothetical internal classical fault flags. Its bad-event probability follows by ordinary graph-witness union counting from the final positive port law. The stronger one-eighth occupancy pays p_port^(s/8), not the original quarter-occupancy p_port^(s/4); geometric constants and thresholds must be chosen accordingly. Source-good is imposed on its virtual support cover F. They need not be independent or admit a joint local-stochastic distribution.

## Common output frame
For each initial defect-basis component and actual historical m, write f for its effective source outcome flip, so its ideal graph branch label is s=m+f. For a final physical port component m'=m+g, the SAME branch has label

    s=m'+(f+g).

Consequently the deterministic ATG recovery identity with fixed decoder/tie rule, applied at final record m', yields residual Rep(f+g), up to a scalar phase, after the single frame P(m'). Since supp(f+g) is contained in F union G, the strengthened separate good conditions imply the original good certificate. The quantum boundary then lies in the prescribed small-radius module (including source boundary defects).

Record/gauge/bath-only capture may arbitrarily correlate or mix its registers. It cannot move DATA out of its initial componentwise span. Resolving final m' and using linearity gives the same common-span statement for all coherent defect coefficients and every retained bath. The historical m label can subsequently be forgotten. The fixed-baseline discrepancy is D(m')=b(m')+sigma(P(m')); on every surviving component it equals b(f+g)+sigma(Rep(f+g)), so the density bound holds for one common diagonal function of the actual final ports.

## Why the quantum-side premise is necessary
A channel can capture every port perfectly and independently replace all DATA by |0...0>. It then has port error probability zero but generally destroys the encoded Bell source and its allowed low-radius module. Even a theorem allowing arbitrary quantum DATA/bath in classical effect estimates does not imply preservation of that DATA. Joint DATA noise during O(log n) capture likewise needs a real quantum-memory/intertwiner estimate; this derivation does not silently set it to zero in the claimed physical model.
