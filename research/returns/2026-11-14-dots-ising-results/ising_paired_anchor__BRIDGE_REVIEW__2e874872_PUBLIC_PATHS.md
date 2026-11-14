# Independent paired-column and continuation review

Independently reconstructed the two-column transfer rather than relying on the scalar result.

For each column with bottom plus and top minus, the vertical flip count is exactly1+2b, including counts0 andh. Hence the pair baseline division is epsilon^-2=t^-1. The count relation n01-n10=d2-d1 makes the fugacity extraction z^-Delta exact. Swapping column names when d1>d2 is only a symmetry in this pair calculation, not a physical permutation of the surrounding columns. Dropping inter-pair horizontal excess leaves a valid positive upper bound.

For w=(1,20epsilon,20epsilon,1), the four KDw/w ratios are those stated in RESULT.md. The first requires t<=z/20; the others have additional positive margins. K e11<=w and the initial e00 component of w equals1, giving the claimed transfer bound. There is no hidden fixed-count normalization or column independence assumption.

The paired fugacity penalty is bounded by c times the FULL sorted-height variation. Replacing theta by theta-c/2 must retain the two endpoint terms; the proof correctly pays exp[c(d1+dm)]<=exp(2ch). The inherited height-walk theorem applies with the improved positive delta_eff; bounding its denominator by1+R/8 is conservative. The unpaired column's exp(h epsilon) factor is paid.

For the sharper full-line continuation, the inherited native proof leaves one fixed essential axial wall and at least one other parallel primitive axial wall, with moving reference perimeter<=L+2 until first B. An all-walk directional tilt is valid: actual physical cycles are a subset of those walks, and displacementL extracts (epsilon/u)^L. The root/orientation factor100n is conservative. The full ordinary partition pressure retains ALL other loops; selecting one wall does not require assuming there is only one. The physical nonbacktracking3^p pressure is valid after zero-edge contraction. The factor exp(8(L+2)) cancels epsilon^L, leaving exp16 and u^-L<=exp(L/999). No extra free interface or discarded thermal entropy was found.

The new Q bound is increasing in h after the displayed relaxations and covers every smaller native prefix through the already proved partial-row comparison. That comparison uses physical theta4 and pays exp(2phi m); it is not altered by the auxiliary theta_eff. Terminal arrival domination is still nu<=Qw. The two stages use disjoint coordinates, and the displayed J_line upper bound exceeds exp(2phi m) at the retained instances. Thus the existing maximum-of-stage-loads join remains valid.

Reran check.py independently: the R10000 negative exponent33296 is reproduced. The first three paired bounds are weaker than prior anchor receipts and should not replace them. This review finds no gap in the stated finite construction. It does not establish a uniform growing-R estimate or capacity acquisition, and does not modify any frozen artifact.
