# Independent reconciliation of the local core-phase construction

2026-11-03. Root independently verified the constructor's positive combinatorial operation.

For ordered tetrahedron [a,b,c,d], let m_ij=round(phi_j-phi_i), n=dm. Orient its boundary facets with alternating signs. For generic rotor phases, exactly zero or two facets have n≠0. One proof uses affine interpolation of the four complex vertex values exp(2 pi i phi): the inverse image of zero is the intersection of a line with a convex tetrahedron, hence empty or a single segment. Its boundary endpoints lie on exactly two faces. The winding of the triangular edge phase equals origin containment of that complex triangle, because shortest-angle edge arcs are homotopic off zero to straight chords when endpoints are not antipodal. Degenerate coincident/antipodal cases require prescribed limits; they are not counted as generic chambers.

Give each pierced face f the core phase exp(2 pi i phi_min(f)). Inside each tetrahedron interpolate between its two core phases by the shortest angle along the resolved vortex arc. All faces except [b,c,d] have anchor a. Thus the local increment for an n-oriented arc is

  n_bcd * (phi_b - phi_a - m_ab).

If the opposite face is not pierced, both anchors are a and the increment is zero, agreeing with the formula. Orientation n fixes the sign when it is pierced. Summing over oriented tetrahedra gives integral (dphi-m) cup n = - integral m cup n, since dn=0 and the manifold is closed. The physical complex scalar vortex has orientation -n (its edge phase increments are dphi-m), hence its core-phase winding is +s, s=integral m cup dm.

This rule is strictly cell-local, periodic under individual integer representative shifts, and covariant under simultaneous global rotor rotation. It explicitly changes branch at shortest-angle walls. It does not require a globally selected Seifert surface, nor assign a fractional local Chern-Simons density to an integer onsite charge.

Root exact-rational check: phi=(0,x/11,y/11,z/11), all x,y,z in {0,...,10}. Of 1331 tetrahedra, 671 had zero pierced facets and 660 had two. The local phase-increment identity held exactly in every case. The constructor also tested the actual cubic reconnection and obtained total winding 0 and -1, equal to its two self-linking values.

What is earned: the core phase and its winding identity, not yet a complete smooth spatial SU(2) texture or lattice ground charge. To transfer this to deg U for U=(z,w)/sqrt(|z|²+|w|²), construct z with precisely this oriented zero link and extend w from the prescribed phases along it into compatible tubes. Tube smoothing, bounds uniform in chamber parameters, actual Wilson occupied-charge matching, partial-transfer amplitudes and the many-body interface gap still remain.
