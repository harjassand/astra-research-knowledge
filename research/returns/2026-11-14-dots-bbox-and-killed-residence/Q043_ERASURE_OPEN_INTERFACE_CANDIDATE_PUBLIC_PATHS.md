# Candidate erasure reconstruction through a single open interface

Status: constructive proof interface under review, not an adopted congestion theorem.

For a selected ORIGINAL small component C in a box of widthW≤400, erase top rows, and each row left-to-right. At a current edge, the remaining portion R of C is known from the current state and geometric record. Original other components were nonadjacent to C; after deletion they remain nonadjacent to R. Hence their energies factor out of w(original)/w(current). This is different from an uncontrolled frozen-exterior resistance bound.

For an overwrite region U consisting of completed top rows, possibly plus a left prefix of the current row, sum all candidate erased sets A⊂U. The relative Gibbs weight is w(A∪R)/w(R). Ferromagnetic boundary monotonicity increases this partition sum if the known plus boundary below U is replaced by a completely plus row along the erase front. Side/top boundaries of the original component's bounding box may remain minus. Compatibility with original other components is discarded only after factorization, which increases the bound.

For a rectangular U, plus bottom boundary and minus sides/top create one open contour running between the bottom corners. Compared with the empty interior, its native Gibbs weight is exp(8W) times exp(−8 length+.04 enclosed added area). The remaining contours are bounded holes or disconnected plus components and may be paid by the existing positive/negative contour gases. No assumption that the original remaining shape R is rectangular is needed.

The confined magnetic resolvent used for prewrap growth also bounds this open contour. If T is the nonnegative widthW walk matrix and Rwalk=(I−T)^−1, then the open walk mass is at most Rwalk_0W. With LDL pivots p_i and off-diagonal b,
Rwalk_0W=b^W/(product_{i=0}^W p_i).

At W400, use the sameλdiscount for lengths≤12000 and pay the remaining tail by the finite area bound. The estimated relative log bound is around97, before root/record and auxiliary contour-gas factors. This numerical estimate is not yet a directed scalar certificate.

For the partial current row, the overwrite front is a one-step staircase. Its reference boundary length is at mostW+2 and its endpoints differ vertically by at most1; a corresponding open-walk representation should cost only a fixed factor exp16. This needs explicit edge-level checking before adoption. The general path record and original-component recovery must likewise be specified. Do not replace this candidate by a claim that a completed rectangle denominator automatically bounds a rough remaining component.
