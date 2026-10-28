# Root receipt: weighted decoder positive-cost interface

28 October 2026. Scope: Sections 2–4 mathematical reduction and counterexample received; no new rounding algorithm and no change to k^6 source rate.

Source SHA256: `553188e262bc4bdc8d919650983ca293354f9cec7aa6e14463bc1bfdd3839fcb`.

I independently read the dual pair and verify equality Tr(UD)=Tr(Y)+Tr((U-Y tensor I)D) on every actual TP decoder. Primal center I/2 and sufficiently negative scalar dual give Slater feasibility. For a certified feasible dual within tau/2 of optimum, m>=tau/2 and W>=0 hold exactly, with the stated bounded-domain norm estimates. Finite inward shift/mixing must retain the reserved objective slack, as the source says. No source oracle is introduced.

The expectation contract is sufficient only for existence of an action with the stated ratio: E numerator>=alpha S and E denominator<=beta cost imply the ratio lower bound, since denominators are strictly positive. An algorithm needs an additional success-probability/repetition argument, explicitly not supplied.

For identity noise the Bell overlap of replacement is1/4, hence the six-state mismatch mean is1/2. With t=1/2, s=tau=2^-e, the repaired/original ratio is exactly6/(2^e+5). Exact Fraction checks at e=2,4,8,16 confirm its decay. This refutes fixed interior-shrink repair, not the oracle task or a generic lower bound.

This root receipt does not independently re-review the quoted Naor–Regev–Vidick primary theorem; Section1 remains source attribution by the author. The reduction/obstruction above is self-contained and does not need that theorem.
