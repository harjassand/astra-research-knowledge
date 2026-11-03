# Root reconciliation of the explicit barycentric mass texture

2026-11-03. This supersedes the need for the unfinished general handlebody phase-extension algorithm in ROOT_CELLULAR_TEXTURE_CONSTRUCTION.md for the rotor-generated configurations considered here. It is a candidate geometric construction being independently audited. It is not yet a free-lattice index or interface-gap theorem.

Let m=round(dphi), n=dm. Generic tetrahedra have zero or two pierced faces. On the barycentric subdivision assign a unit spinor q=(z,w):
- Original vertex i: (exp(2 pi i phi_i),0).
- Edge center: (shortest-arc phase midpoint,0).
- Unpierced face: (phase average of its three consistently lifted rotors,0).
- Unpierced tetrahedron: (phase average of its four consistently lifted rotors,0).
- Pierced face: (0,exp(2 pi i phi_min(face))).
- Pierced tetrahedron: (0,shortest-arc midpoint of its two pierced-face phases).
Interpolate q affinely inside each flag simplex and normalize to U=q/||q||, with the usual SU(2) completion of the spinor.

Consistent lifts exist for an unpierced simplex because m is a closed integer 1-cochain there and hence exact. Their adjusted rotor differences all lie in (-1/2,1/2). Every pair lies in that interval, so the adjusted values fit in an interval of length <1/2. Integer changes of representatives alter the common lift by an integer; the exponentiated average is unchanged. A common rotor rotation multiplies every assigned z and w by the same phase. Shared faces use the same assignments irrespective of which tetrahedron contains them. Branch changes at shortest-arc walls are allowed and explicit.

Uniform nonzero bound:
In a nested flag, z-type phases are averages over nested subsets containing the same original vertex. For an unpierced tetrahedron the phase range of these averages is at most 3 pi/4: for sizes r<s, the mean difference is at most (s-r)/s times the full rotor phase range (<pi). If the tetrahedron is pierced but its flag face is unpierced, the z-type range is at most 2 pi/3. If that face is pierced, only vertex and edge are z-type and their difference is at most pi/2. The w-type phases, when there are two, are a face phase and the shortest midpoint, differing by at most pi/2.

Let Z and W be total barycentric weight of z-type and w-type vertices. Set a=cos(3 pi/8), b=cos(pi/4). Then |z|>=a Z and |w|>=b W, with Z+W=1. Thus

  ||q|| >= a b / sqrt(a^2+b^2) > 0.336.

The normalized map is uniformly Lipschitz in SPACE on a fixed shape-regular subdivision, with a computable O(1/ell) bound from the affine vertex gradients and this normalization floor. It need not be continuous as a function of the rotor PARAMETERS across rounding walls; that departure is essential to the previous failed smooth-family charge test.

The z sum cannot vanish unless all z-type weights vanish. Consequently z=0 is exactly the barycentric resolved-dual arc from pierced face center through pierced tetra center to the other pierced face center. On each such arc, w follows its assigned shortest phase path. ROOT_CORE_PHASE_IDENTITY.md gives its total winding s when oriented as the physical scalar vortex -n. Degree can be evaluated at target (z=0,w=exp(i theta)) with theta avoiding node phases; its preimages lie on arc interiors. The transverse degree is the face vortex orientation, and the longitudinal count is core phase winding. This is the pending explicit sign/PL degree audit, rather than an assumed fermion response formula.

For later quantum construction, bounded piecewise mass multiplication on the rotor Hilbert space is a well-defined bounded operator. Bounded local integral/hopping kernels could likewise avoid imposing a bare angular-momentum domain. That does not supply their locality, amplitudes or gap. The remaining central gates are: actual UV-regulated slab occupied-charge/index equality, a usable local partial-transfer family, and a symmetric trivial thermodynamic interface gap. The geometric map alone establishes none of those.
