# Independent review: full plus row/column occupation theorem

Reviewed n1722_thermal_monotone_congestion_20261113/ONE_LINE.md, full_line_scalar.py, and fluid's ising_full_corridor_20261113/TOPOLOGY_AUDIT.md. Reran the scalar receipt successfully. No defect found within the stated finite-parameter model and inherited capacity assumptions.

## Checked details
- The original core is decreasing, heatbath attractive, B increasing, and shared accepted rate-kappa clock gives decreasing original v. Coordinate current budgets charge actual source current including the harmless A/B overlap. No reflected or restarted process is substituted.
- A fixed plus column has magnetization L. After k prescribed sites (including skipped plus sites) are processed, total M>=2k+2L-n. First B is reached by ceil((n-2L)/2), leaving the opposite last column untouched. At both endpoints the processed set is full columns plus one consecutive partial column. Skips do not create an extra label.
- For each source assignment on the overwritten prefix, all untouched bits are fixed by the physical edge. Replacing unknown exterior neighbors by minus increases the source/reference weight ratio, while the full plus column stays plus. This comparison needs NO initial minus collar, no core exterior law, and no physical boundary pinning during the real dynamics.
- The favorable field factor is dropped on the original prefix before contour constraints are relaxed. This avoids a hidden enlarged positive-field partition.
- In the actual fixed triangulation, the opposite interface is a fixed closed dual cycle of physical length L. The full wall set has trivial total mod2 homology, so after removing that nontrivial cycle another nontrivial cycle remains, of physical length at least L. Reference remaining perimeter<=L+2. Full walls, including nested and additional winding loops, determine spins once the plus column is fixed.
- The loose100n4^s cycle count is safe: root an oriented physical edge, total dual length<=2s because zero-edge crossings cannot be consecutive, and degree-three nonbacktracking continuation has at most two choices. Summing lengths/root orientations fits the constant100. Every contractible physical wall has length>=4; winding ones have length>=L>=8. Dropping compatibility only enlarges the positive product bound.
- The upper endpoint's forced-original-minus site may be dropped to enlarge its fiber; both heatbath endpoint terms are paid. First-B restrictions remove sources, not add them.
- Paying2L line labels explicitly handles overlap. The scalar code's floating logarithm is used only to propose an integer; a separate exact rational positive-Taylor assertion certifies that integer, so the reported upper bounds do not rely on floating rounding.

Finite occupation bounds remain e^-596,e^-1836,e^-10234,e^-105199 at the four imported capacity instances. The capacity proof itself is an inherited dependency, not independently reconstructed here. The exact clock and r parameters must remain the same in any package.

## The actual complementary sector is NOT 'no winding'
At L=8R define plus spins by

 0 <= (x-y mod L) < 4R-1.

This is a diagonal winding band. It contains a physical nearest-neighbor staircase winding once in both torus directions. Every row and column has exactly4R-1 plus spins, so it contains no full plus row or column. It is outside B because its area is(4R-1)L<n/2. Its physical perimeter is4L, and at theta4,phi4/R

 log[w(x)/w_minus]=-2theta·4L+2phi·(4R-1)L=-64.

This log weight ratio to the all-minus state is independent of R. For the four PACKAGED finite parameter instances, the inherited ALL-domain-wall pressure bound gives Z_A/w_minus<=2exp(S0), with S0<.01 at R80,200,1000 and S0<1 at R10000. Therefore this uncovered state's weight relative to Z_A is at least exp(-64)/3 in the first three instances and exp(-64)/6 in the fourth. These lower bounds are far larger than the new full-line occupation upper bounds at those instances. This uses the LOCAL previous-package pressure receipt, not an optional external density calculation. No uniform thermodynamic-limit lower bound relative to Z_A is asserted.

This is NOT a lower bound on its actual voltage-weighted occupation and does not refute a future current argument. It identifies a real remaining high-area winding geometry. diagonal_gap.py checks the exact lattice counts and physical staircase for several sizes. The formulas above establish the general example.

Possible next step: cover diagonal winding anchors while preserving their homology through a sweep. Their natural interface length is2L, and3^P contour counting would cost2L log3 rather than2L log4. This may fit the finite capacity margin, but a complete path/partition/label proof has not been supplied here.
