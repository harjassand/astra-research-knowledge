# Independent audit: killed finite-phase factorial certificate

Reviewed 2026-10-30. Source: `KILLED_FINITE_PHASE_FACTORIAL_CERTIFICATE.md`.

**Verdict: passes at child-audit level under the two stated graph hypotheses.** This is a local killed-generator construction. It does not control incoming forcing after extension by zero or growing-head constants.

## 1. Cofactor weights, shifts, and the exact quadratic identity

For sufficiently large count, every nonzero channel polynomial is positive. Projected reachability to killing makes Q_0 a transient finite subgenerator, even without mode irreducibility. Its inverse has positive diagonal and nonnegative entries, so tau=(-Q_0^T)^-1 1 is strictly positive. Positive forest expressions show that each entry is a rational function with an integer leading exponent beta_j and positive leading coefficient.

Replacing each source rate by k_e(r-beta_j)_a does not change any channel's leading degree or coefficient. In every positive forest expression it therefore preserves the numerator and denominator leading degrees and coefficients. Recomputing tau for Q(r) really retains the same beta vector; this is not an assumed fixed point of a signed determinant calculation.

The equation Q^T tau=-1 gives incoming_internal_j-outgoing_internal_j=K_j-1. Expanding the quadratic form then gives exactly

    u^T diag(tau)Q u
      = -1/2 sum_e F_e(u_k-u_j)^2 -1/2 sum_j(K_j+1)u_j^2.

Internal same-mode reactions cancel in Q, have zero difference energy, and cancel from the flux imbalance. They must remain in the tilted generator, as the source explicitly does. There is no omitted same-mode loss or artificial stationary measure.

## 2. Tilted energy absorption

For a downward edge the displayed completed-square identity is exact. Eventually t<=1/2, so its endpoint-square sink is uniform and also controls the mode difference, regardless of the vanishing t-weight on its own difference term. For an upward edge, writing u_j=u_k-(u_k-u_j) and applying Young gives exactly the claimed bound with retained -F_e/4 difference energy and positive (b+b^2)F_e u_k^2. At large r the latter is O(r^(2alpha delta))F_e u_k^2.

Choose a return-or-kill complex path and stop at the first complex of height <= the original source height, or at killing. Before that terminal event, all source heights are integers strictly above the original source height; hence their fluxes have at least one power of r advantage over the original upward-edge flux. If the path reaches the original height, the terminal edge is downward and provides its source endpoint sink. If it reaches killing first, the killing source has the same height advantage and supplies a term in K_j. Telescoping mode values along the preceding path bounds the original target-mode square by its differences and that final sink square.

Repeated modes do not invalidate telescoping. A same-mode downward edge still gives an endpoint-square sink. A same-mode upward edge has no initial difference energy, but its burden is controlled by its return-or-kill path in exactly the same way.

After splitting a fixed fraction of each negative resource among the finitely many chosen paths, every positive burden is smaller by O(r^(2alpha delta-1)). Thus 2alpha max(delta_+)<1 suffices. All burdens can be absorbed while retaining the extra -1/2 sum_j u_j^2. This proves strict negative definiteness of the weighted symmetric part and hence Hurwitz stability of the Metzler G. The argument does not need per-mode first-up bias or stationary flux balance.

## 3. Exact lift and stopped consequences

For rational alpha, all entries of G and v=(-G)^-1 1 are rational functions of r^(1/q), with real fixed coefficients. Hurwitz/Metzler positivity makes every v_j strictly positive. A nonzero eventually positive rational-Puiseux function has a leading power times a positive coefficient, so each fixed-shift ratio is 1+O(1/r), including when its leading exponent is negative or fractional.

At source residual r, the actual destination residual is exactly r+delta. The gamma ratio times the v-target ratio is r^(alpha delta)[1+O(1/r)], and the fixed factor 1+epsilon absorbs this for every nonzero jump. At delta=0 there is exactly no argument shift. Killing has value zero and its original loss is retained. Consequently the actual generator satisfies LV/phi<=Gv=-1 in the large-count region.

Choose the positive finite extension below a threshold and then enlarge the region of the asserted inequality by the maximum physical jump size. This ensures no large-count source used in the comparison has a target in the arbitrarily extended part. Factorial growth dominates every profile power, giving normlikeness. Standard stopped localization yields nonexplosion and finite expected phi-cost until killing or entry into the finite low-count set, without assuming recurrence beforehand.

## 4. Finite truncations of a weakly reversible network

The lifting argument checks out. For a source internal population z and source complex y, fix the nonnegative residual w=z-y. Along an original complex return path, the internal population is w+y_i, and each next reaction is enabled there. Either all these populations stay in the chosen finite S and the lifted complex path returns to its source, or its first departure is an actual killing edge. This proves the return-or-kill property for each retained internal edge.

Mode reachability to actual exit is a separate hypothesis and cannot be inferred from weak reversibility: closed internal components may remain. The source correctly retains this obligation. Similarly, zero exterior extension creates genuine incoming forcing in the unrestricted physical generator. The local certificate does not bound that forcing, nor the profile exponents/thresholds as the finite set grows.

## Conclusion

No mathematical defect was identified in the stated local theorem. Its new cofactor-flux imbalance legitimately replaces the stationary tree vector for a transient killed projection. Growing-head matching and physical return feedback remain open exactly as stated.

## Reviewed source hash
527d038f87bd42599a0b2fd22512604f449037cd62318c49836dd2062cb18624  chemical_joint_shell_20261030/KILLED_FINITE_PHASE_FACTORIAL_CERTIFICATE.md
