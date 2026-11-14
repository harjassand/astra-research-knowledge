# Physical-step contour encoding:3^P rather than4^P

## Exact representation lemma
Use precisely the source convention inherited in `n1722_thermal_transport_20261113/THERMAL_CORE_CAPACITY_LOWER.md`: the fixed lattice triangulation has a trivalent dual, every dual vertex is incident to exactly one zero-coupling diagonal-crossing edge, and a resolved contour is a nonbacktracking dual loop. Physical perimeter P counts only positive-coupling nearest-neighbor edges. If the underlying source instead includes BOTH crossing diagonals as independent edges, this lemma requires re-establishing the planar representation; do not silently apply it there.

The zero-cost dual edges form a perfect matching. Starting just after a physical edge, a nonbacktracking walk can choose:
1. the other physical edge at its present dual vertex; or
2. the zero-cost edge, then either of the two physical edges at the matched vertex.

There are exactly three physical-step continuations. The next physical edge determines which continuation occurred; no geometric label is erased. Closing the loop after its final physical edge offers at most one compatible zero-edge closure or immediate closure. Choose a canonical directed physical starting edge, of which there are at most4n on the square torus. Hence the number of resolved contours of physical perimeter P is at most4n3^(P-1), and in particular at most6n3^P. Self-avoidance or nonwinding restrictions only reduce the count. This proof holds for arbitrary fixed choices of one diagonal per plaquette, not only a translation-invariant triangulation.

It is the ordinary nonbacktracking walk bound after contracting a perfect matching, not a new contour theory. The older4^P estimate counted up to2P separate dual decisions and unnecessarily treated both as unconstrained binary choices.

## Executed finite diagnostic
`check.py/json` enumerates self-avoiding loops up to physical perimeter9 on the9-by9 periodically triangulated lattice, with a fixed initial directed physical edge. Counts are2,6,32,1 at perimeters4,6,8,9; the last includes a winding loop. It also checks every local incoming physical edge has exactly three compressed continuations and confirms zero collisions between distinct full contour paths sharing the ordered physical-edge signature. This is a finite representation check, not a proof of a global Ising residence theorem.

## Consequence for the existing direct occupation baseline
Replace4^P by3^P in compute's `ising_band_occupation/RESULT.md`. At theta4 the entropy-relaxed mass threshold moves from
(4-2log4/4)^2=10.9352756
to
(4-2log3/4)^2=11.9072881.

For the actual intermediate band M11\M5, set q=3exp(-8) and
u11=6n[(1/600)^(2r)/(1-1/600)+(4/5)^(R+1)/(1-4/5)].

The same full-domain thermal-spin-flip injection and two-scale split yield, whenever u11<1 and the inherited topology/core conditions hold,
Z_M11/Z_A <=1/(1-u11),
N_(M11\M5)/Z_A <=66nR² exp(-3.5216R)/[(1-q)(1-u11)].

The scalar constants follow from3exp(-7.5)<1/600;3exp(-8+2sqrt11)<4/5; log3<1.1; sqrt11>3.316. The area exponent4(8-log3)sqrt(t)-8t is concave on[5,11], and both endpoints exceed3.5216. Thermal interiors are retained by the inherited injection; no pure-phase assumption or source-current/Gibbs substitution is introduced. v<=1 alone transfers mass to actual voltage occupation. These stated decimal inequalities can be replaced by rational/Taylor certificates before external theorem packaging; this note's executed scalar diagnostic uses floating math.

## Scope and limitation
This extends a baseline from M10 to M11, not the full beyond-M10 problem. At area16R² even a perfect zero-entropy square has zero Peierls energy relative to all-minus in this scaling; better contour counting cannot control arbitrary larger domains by Gibbs mass. Winding states and the full residence numerator remain unresolved. Do not present this modest standard entropy improvement as a breakthrough or a replacement for the phase-gas coverage theorem.
