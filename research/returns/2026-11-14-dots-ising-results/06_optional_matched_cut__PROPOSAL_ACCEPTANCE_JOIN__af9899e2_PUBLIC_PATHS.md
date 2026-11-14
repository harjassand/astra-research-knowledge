# Optional matched-cut acceptance improvement

This is an energy-subset lower bound, NOT a capacity lower bound.

The exact coefficient construction and independently reviewed geometry give a genuine subset of the SAME native cut edges, with pure companions, perimeter <=1900 and full-domain inverse image all-minus. The truncated receipt proves W_good/Z_A >= exp(-6236). All these edges lie in the retained proposal image because all-minus belongs to the auxiliary core.

The exact marked rejection identity has per-attempt success W_aux/(Q Z_aux). Since Q Z_aux <= Q Z_M <= W_upper_bound <= exp(-6215) Z_A, the conservative bound is

    acceptance >= exp(-21), expected attempts <= exp(21).

This improves the capacity-based exp(234) rejection bound without improving W/C or physical decision time. It is still approximately 1.3 billion expected attempts as an upper guarantee, not a practical implementation. Approximate core/word/acceptance errors must be paid against this acceptance lower bound; full-versus-retained energy error still uses the capacity lower and omitted-energy bounds separately.

`receipt.py 100` regenerates exact coefficients using included `area.py`, then `truncated_receipt.py` explicitly keeps only perimeters <=1900. No assertion that excluded perimeters have zero weight is made. All 160 retained perimeter classes span 1582 through 1900.
