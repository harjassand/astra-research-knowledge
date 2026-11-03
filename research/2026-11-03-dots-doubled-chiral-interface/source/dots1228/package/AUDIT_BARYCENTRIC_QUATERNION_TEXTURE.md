# Independent audit: barycentric quaternion texture

2026-11-03. Read `piecewise_texture.py`, `ROOT_CORE_PHASE_IDENTITY.md`, and the constructor's precise endpoint assignments. The earlier `ROOT_CELLULAR_TEXTURE_CONSTRUCTION.md` contains a more elaborate unfinished route; the barycentric construction supersedes its extension problem for the narrow fixed-configuration texture task.

## Verdict

**The proposed local texture construction works on generic rotor chambers**, with a uniform nonzero interpolation bound, shared-cell compatibility, individual-rotor periodicity, global phase covariance, and S3 degree equal to the cochain integer s under the conventions below. No fatal geometric obstruction found. Branch walls require a prescribed consistent one-sided chamber limit, not an arbitrary inconsistent tie rule. A sign qualification is necessary when identifying S3 degree with an SU(2) trace integral.

This proves a local continuous spatial texture and its degree. It does not identify the charge of a finite Wilson-lattice occupied state, construct a rotor hopping operator, or prove an interface gap.

## 1. Chamber geometry and consistent lifts

Write m_ij=round(phi_j-phi_i), n=dm, and alpha=dphi-m, with all edge differences non-antipodal. A triangle is unpierced exactly when its three phases admit a common real lift in an interval of width less than one-half turn. If every face of a tetrahedron is unpierced, all four phases admit such a lift: otherwise the origin lies in the convex hull of the four unit complex values and, by the planar convex-hull/Caratheodory argument, lies in the hull of a triple. Antipodal degeneracies are excluded here.

For a pierced tetrahedron there are exactly two pierced faces. One proof is the preimage of zero under affine interpolation of the four complex vertex values: generically it is the intersection of an affine line with a tetrahedron, hence an interval or empty. Its two endpoints correspond to pierced faces. Equivalently, the cyclic order of four non-antipodal circle points gives the same classification.

Each barycentric vertex is indexed by an actual simplex, not by an incident tetrahedron. Its assigned q therefore agrees between neighboring tetrahedra. For unpierced simplices the anchored shortest-difference mean coincides modulo integers with the mean in the consistent lift. This verifies that the code's formula is not silently using incompatible lifts on nested subsets.

The chamber data use only edge rounding. After a common-phase gauge phi_a=0 and other phases in [0,1), there are at most nine relevant affine half-integer walls in three variables, so the chamber enumeration is finite (a crude hyperplane bound is 130 regions). I do not claim that crude upper bound is the exact number of chambers. Independent grid enumeration found 26 distinct rounding patterns among the tested fixtures.

## 2. Angular span and uniform norm

In a barycentric flag S_1 subset S_2 subset S_3 subset S_4, averages of nested subsets of sizes k<l in a common real interval of width less than pi differ by at most (1-k/l)pi. Therefore all z-type flag values lie in an angular interval of width at most 3pi/4 when the tetrahedron is unpierced. If the tetrahedron is pierced but its flag face is unpierced, there are only three z-type values and the bound improves to 2pi/3. If the flag face is pierced, only the original vertex and edge midpoint are z-type, spanning at most pi/2.

The only possible w-type values in one small tetrahedron are its pierced face center and tetrahedron center. The latter is the shortest-angle midpoint of the two pierced-face anchors. Hence their angular separation is at most pi/2. The ordering used to choose the two face anchors does not matter away from antipodal walls.

Let t be the total interpolation weight of z-type vertices, a=cos(3pi/8), b=cos(pi/4). Rotating each complex coordinate separately to the middle of its phase interval gives

|z|>=a t, |w|>=b(1-t).

Consequently

||(z,w)|| >= min_{0<=t<=1} sqrt(a^2 t^2+b^2(1-t)^2)
             =ab/sqrt(a^2+b^2)
             =0.3365567705907775.

Thus normalized interpolation is well-defined uniformly, including chamber limits. The weaker bound printed by the current scratch code is also valid. Shape-regular fixed spatial simplices give uniform spatial Lipschitz bounds after normalization. No smooth dependence on rotor parameters across rounding walls is claimed.

## 3. Periodicity, covariance, compatibility and wall qualifications

Adding an independent integer to phi_j changes each affected rounded edge difference by that integer and leaves alpha and n unchanged. Every assigned phase is unchanged. A common real shift beta leaves alpha,n unchanged and multiplies both z and w by exp(2pi i beta). Linear interpolation and normalization preserve that covariance.

For the code's SU(2) matrix U=[[z,w],[-conj(w),conj(z)]], this common spinor phase is **left multiplication** U -> diag(exp(2pi i beta),exp(-2pi i beta)) U, not scalar multiplication of an SU(2) matrix.

On a shared barycentric face, all vertex values are the same simplex-indexed values, so affine interpolation agrees exactly. Equal barycentric coordinate ties only select between neighboring small tetrahedra whose common face has identical interpolation.

At half-integer edge walls, independent nearest-integer choices can violate the generic two-pierced-face logic. Define the wall value through a specified globally consistent infinitesimal perturbation/one-sided chamber limit. The rule must be compatible on shared simplices and preserve integer periodicity/common-phase covariance. The generic construction and the uniform norm bound alone do not justify arbitrary separate tie choices. Jump discontinuity in rotor parameter space is allowed in this texture statement; its later quantum rotor operator domain remains separate.

## 4. Zero link and degree, including the signs

The positive half-plane estimate shows that z cannot vanish if any z-type interpolation weight is nonzero. Thus, inside a pierced tetrahedron, its zero set is exactly the two barycentric edges joining each pierced-face center to the tetrahedron center. Unpierced tetrahedra have no zeros. These arcs glue into the resolved dual vortex link; the zero positions do not approach original edges when a phase approaches a rounding wall.

On a pierced face, the boundary z phase follows the shortest arcs, subdivided at the edge midpoints. Its winding is integral alpha=-n on that face. The transverse index of the fixed face-center zero is therefore -n. The glued zero link carries this physical scalar-vortex orientation, not the opposite n orientation.

On an ordered tetrahedron [a,b,c,d], the pierced-face anchors are a unless the pierced face is [b,c,d], whose anchor is b. The full core phase path through the tetrahedron center follows the shortest arc between these two anchors. Along the n-oriented dual arc its increment in turns is n_bcd alpha_ab. Along the actual z-vortex orientation it is -n_bcd alpha_ab. Summing with tetrahedron orientation yields

wind_core(w)=-integral alpha cup n
            =-integral (dphi-m) cup dm
            =integral m cup dm=s,

because the manifold is closed and dn=0. The core w values never vanish; interpolation follows the intended shortest phase path, so normalization does not alter the winding.

Orient S3 as the boundary of C^2 with real coordinate order (Re z, Im z, Re w, Im w). At z=0,w=1 the positive tangent orientation is (Re z,Im z,arg w). Therefore the degree of the normalized spinor is exactly the oriented winding of w on z=0, hence **deg_S3=s**. The PL bends at tetrahedron centers do not alter this intersection calculation; equivalently use an arbitrarily small generic spatial perturbation/homotopy preserving the nonzero norm.

### Important SU(2) trace convention

For the specific code matrix [[z,w],[-w*,z*]], the tangent generators at (z,w)=(1,0) in the positively oriented S3 coordinates (Im z,Re w,Im w) are (i sigma_3,i sigma_2,i sigma_1). Their triple trace is negative. Thus

(1/(24pi^2)) integral tr[(U^{-1}dU)^3] = -deg_S3

with that trace convention and spatial orientation. Using a minus sign in the winding definition, or a different standard spinor-to-SU(2) convention, restores +s. Do not silently identify this sign with a microscopic slab axial charge; that transfer has not been proved.

## 5. Optional spatial smoothing

A continuous spatial texture is enough to define degree. If smooth spatial mass fields are wanted, the raw q has a uniform Lipschitz bound on a fixed shape-regular triangulation and a uniform positive norm. A local linear spatial smoothing with uniform error less than half the norm lower bound, followed by normalization, is homotopic through nonzero fields and keeps the degree. Linear smoothing preserves the global spinor phase covariance. This does not smooth the family across rotor rounding walls and does not establish rotor-domain or lattice-charge statements.

## 6. Independent scratch check

I separately enumerated phi=(0,x/11,y/11,z/11), x,y,z in {0,...,10}, and all 24 barycentric flags for each fixture. Results: 671 tetrahedra with zero pierced facets, 660 with two; no other count. Largest sampled z span was 0.3409091 turns, below 3/8; largest w span was 0.2272727 turns, below 1/4. These numerical checks corroborate but do not replace the proofs above.

**Earned component:** a cell-local, periodic, globally covariant, uniformly nonvanishing barycentric spinor texture whose standard S3 degree equals the exact cochain self-linking integer. **Still separate:** free-lattice occupied-charge equality, finite-refinement convergence, coherent local reconnection operators, and a many-body symmetric interface gap.
