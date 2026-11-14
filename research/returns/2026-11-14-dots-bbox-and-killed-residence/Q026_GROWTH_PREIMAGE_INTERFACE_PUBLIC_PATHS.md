# Conditional preimage bound for the post-bootstrap growth segment

This is a proved reduction, NOT a complete congestion theorem.

Let R be a contractible rectangle of width400 and height h<L, full current plus on R, with arbitrary fixed exterior eta. Let x agree with current z outside R, and x_R subset R. In energy E=8P-.04A,
E_eta(x_R)-E_eta(R) = E_minus(x_R)-E_minus(R)+16 * number of bonds from an exterior eta-plus to a missing interior site.
Hence w_eta(x_R)/w_eta(R) <= exp[E_minus(R)-E_minus(x_R)]. Exterior thermal companions therefore HELP this weight-ratio bound and require no enumeration.

A growth-only canonical segment can preserve an original augmented-connected seed C0 spanning exactly400 columns, in a box of height<=400. Fill its box by two-neighbor additions, then extend only the height of the filled rectangle until winding. During the completed-rectangle portion all initial x_R contain C0 and thus contain some augmented component of horizontal span400. Outside R remains unchanged, hence is reconstructed from the current edge. It is NOT necessary that all of x_R be connected.

For every connected nonwinding component C in width400 box, with bbox dimensions w,h_C,
E(C)>=16(w+h_C)-.04*w*h_C.
If w=400 this equals6400, independently of h_C; E(R)=6400 too. All other components have positive energy. Consequently the weighted preimage sum for a fixed full rectangle is bounded by
 exp(6400) * Z_R^{contains width400 component},
where Z is the standalone minus-exterior polymer partition function. A usable bound can be obtained by a marked width400-polymer activity times the unrestricted polymer gas, provided both are paid quantitatively. The magnetic-hull entropy machinery is relevant here with widths<=400 and heights<=1600; no claim is made that existing <=400-square tables already prove it.

At a partial added-row edge, z_inside is the previous full rectangle plus the active prefix, within the one-row enlarged rectangle R1. Its isolated energy is <=6415.96. Every compatible original x_inside is a subset of z_inside and still contains the seed. The same exterior-bond identity holds for deleting z_inside minus x_inside. Enlarging the preimage sum to all subsets of R1 containing a width400 component therefore costs at most exp(6415.96) times their isolated partition mass. This pays the partial row by exp(15.96), without any denominator replacement in the wrong direction. A complete edge reconstruction must retain position, height, orientation and prefix length; these polynomial records have not yet been fully enumerated.

OPEN: (1) the initial bootstrap filling segment is not covered: its current shape is not a full rectangle and replacing its denominator by full-rectangle weight is invalid; (2) wrapping and subsequent strip thickening need a cylindrical partition bound retaining first-majority stopping; (3) exact global deterministic path assignment and edge-record multiplicities; (4) quantitative marked polymer activity. No duration/congestion claim follows yet.
