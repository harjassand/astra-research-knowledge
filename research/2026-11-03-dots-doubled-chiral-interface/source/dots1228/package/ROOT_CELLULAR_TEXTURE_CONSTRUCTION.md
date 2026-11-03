# Local cellular texture construction to test

Root proposal, 2026-11-03. This is a constructive route with identified unfinished geometric checks, not an earned slab-interface theorem.

The smooth-mass charge failure requires cochain-consistent branch changes. An arbitrary solid-angle field has nonlocal tails. A different route builds a finite set of local cell templates.

1. On each ordered edge, z follows the unit-modulus shortest arc between exp(2 pi i phi_i) and exp(2 pi i phi_j). The phase increment is 2 pi(dphi-m). This is periodic in each rotor and covariant under a common phase rotation. It has an explicit branch switch at dphi=m+1/2. Around a triangular face, its winding is -dm.

2. On a face with winding n=0, extend the boundary phase without a zero. For winding ±1, put a vortex of that degree at the FIXED face center, rather than using a linearly interpolated zero that approaches an edge near a rounding wall. In a smoothed disk parameterization let a(theta) be the boundary phase lift, degree n. Set z=r^|n| exp(i[n theta+chi(r)(a(theta)-n theta)]) for a radial chi that is zero near the center and one near the boundary. Constants and the boundary reference phase transform covariantly. Geometry/derivative bounds are fixed per template, with phase increments bounded. Check actual sign conventions against s=m cup dm.

3. In a tetrahedron, pair the signed face-center vortex endpoints using the prescribed resolved-dual geometry. dn=0 gives signed balance. Remove fixed-radius tubes about these arcs. The complement is a fixed handlebody. Its S1 phase-extension problem is an elementary integral-cohomology problem: the boundary meridian periods must have equal/opposite values at endpoints of each arc. This is the actual compatibility check for a proposed pairing, not merely total charge balance.

Given compatible boundary data, an explicit finite-cell algorithm is available: triangulate the fixed complement; extend its integer closed 1-cochain from the boundary by solving the fixed relative integer coboundary system (a Smith-normal-form computation can be precomputed per template). On each face the zero winding then allows a real phase lift and interpolation; on each 3-cell pi_2(S1)=0 removes further extension obstruction. Boundary phases are the actual face functions, not arbitrary independent constants. Tube phases and endpoint jets must be joined using collars. This requires explicit implementation; it is not yet supplied by this note.

4. Smooth fixed collars, preserving the zero link and its orientations, to obtain z with this link as regular zero set. Let n_frame be the actual cup-product/Morse framing of the resolved link. Along the link define w=D_{n_frame} z and extend it into a fixed tube, vanishing outside. Nonvanishing w on the link guarantees U=(z,w)/sqrt(|z|^2+|w|^2) is an SU(2) spinor texture. Global vector covariance follows if z and w both transform by the same phase.

The degree identity can then be checked geometrically: deg(U) is the signed winding of arg w along z=0, because preimages of (0,1) count exactly that winding. A small push-off of the link in n_frame has z approximately epsilon w. Therefore the winding is the linking of that push-off with the whole zero link. If the chosen framing is exactly the cup-product framing, this is the required cochain self-linking (up to the explicit orientation sign). The framing identity and matching to the primary Kasteleyn resolution still need verification on the actual simplicial templates.

Essential unfinished checks:
- Existence and explicit integer-cochain solutions for every rotor-realizable local endpoint pattern, with one common rule on shared cells.
- Individual-rotor periodicity and common-phase covariance of the whole template family, including changes of lifts and branch walls.
- Uniform bounded spatial derivatives after compatible collar smoothing, including vertices/edges and all chamber boundaries. Discontinuity in parameter phi across a branch wall is allowed here but its quantum rotor domain must later be earned.
- Exact degree test on the saved S3 and cubic moves.
- Complete Wilson-slab occupied-charge matching at paid UV refinement, not a continuum anomaly substitution.
- Local partial reconnection operators, consistent overlapping moves and a joint thermodynamic gap remain separate central obligations.

The fixed cellwise cohomology solve is not a global Seifert-surface oracle. Nevertheless it only becomes a local algorithm after boundary compatibility and shared-cell conventions are explicitly constructed. No completed interface or novelty claim follows from this proposal.
