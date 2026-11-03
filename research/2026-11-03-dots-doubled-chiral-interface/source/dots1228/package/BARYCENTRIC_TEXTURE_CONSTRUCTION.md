# Explicit local cochain-consistent SU(2) mass texture

This is a positive intermediate construction: a bounded, spatially Lipschitz, periodic and vector-covariant continuum mass texture whose integer degree equals the rotor cochain self-linking. It is **not** a proof that the corresponding finite Wilson slab has the correct occupied charge, and not a quantum interface gap theorem.

## Inputs

A branched oriented 3D triangulation, period-one vertex rotors phi_v, m_ab=round(phi_b-phi_a) for a<b, n=dm. Work away from half-integer walls, assigning any measurable convention on the walls themselves. Physical coarse edge scale is ell. Refine each tetrahedron barycentrically, using a fixed geometric subdivision independent of phi.

For rotor-generated n, each tetrahedron has either zero or two pierced faces n_f≠0. This can be seen from the affine complex map of the tetrahedron with vertex values exp(2 pi i phi_v): its generic zero set is empty or a line interval with exactly two boundary intersections. Shortest circle arcs and the corresponding chords are homotopic off zero, so the face winding agrees. The actual scalar vortex has sign −n. An exact finite chamber check uses all 48 four-vertex rotor chambers.

## Assignments on barycentric vertices

Write q=(z,w) in C². The SU(2) mass is U(q)=[[z,w],[-w*,z*]] after normalizing q.

For a nonempty vertex subset S of a tetrahedron, let a=min(S). Write delta_av=phi_v-phi_a-round(phi_v-phi_a).

* |S|=1 or 2: q_S=(exp[2 pi i(phi_a+sum_v delta_av/|S|)],0).
* An unpierced face or tetrahedron: use the same consistent-lift phase average in the z coordinate. All its vertex phases have a common lift in an interval of width strictly less than pi.
* A pierced face f: q_f=(0,exp[2 pi i phi_min(f)]).
* A pierced tetrahedron: let f,g be its two pierced faces and a=min(f),b=min(g). Set q_t=(0,exp[2 pi i(phi_a+delta_ab/2)]). Swapping f,g changes this expression only by an integer turn away from antipodal walls.

On a barycentric small tetrahedron with flag v⊂e⊂f⊂t, interpolate these four q values linearly in R⁴=C², then normalize. The implementation is piecewise_texture.py. It takes the original tetrahedron barycentric coordinates, sorts them descending, computes the corresponding flag, and uses mu_k=k(lambda_(k)-lambda_(k+1)) as subdivision barycentric coordinates.

## Exact symmetry and locality

Changing any phi_v by an integer leaves every q unchanged. A simultaneous global shift phi_v→phi_v+alpha multiplies BOTH z and w by exp(2 pi i alpha), hence U→diag(exp(2 pi i alpha),exp(-2 pi i alpha))U, the required vector covariance. The texture at a spatial point depends on only the four rotors of its coarse tetrahedron. Shared face, edge, and vertex assignments coincide, so spatial gluing is continuous. No global phase reference or spanning-surface solve is used.

Dependence on phi is deliberately piecewise and may jump at rounded-edge walls. That does not make multiplication by the mass unbounded on the rotor Hilbert space. It avoids the continuity obstruction found for smooth trigonometric mass families.

## Uniform nonvanishing and spatial scale

Within a nested flag, all z-coordinate phases lie in an interval of width at most 3 pi/4. (For an unpierced face inside a pierced tetrahedron the bound improves to 2 pi/3.) The reason is that every subset average contains the initial flag vertex, so even the four-vertex average differs from it by at most 3/4 of the available phase width; the difference between successive averages obeys the same bound.

The w-coordinate phases are either a single phase or the face phase and the tetrahedron midpoint, which differ by at most pi/2. Let Z,W be the sums of nonnegative interpolation weights of each type, so Z+W=1. With a=cos(3 pi/8), b=1/sqrt(2),

    |q|² >= a² Z²+b² W² >= a² b²/(a²+b²).

Thus |q| has an absolute positive lower bound (~0.3366), independent of rotor proximity to a wall. The code initially records the weaker safe bound cos(3 pi/8)/sqrt(2).

For a shape-regular coarse triangulation, the finitely many barycentric affine coordinate gradients are O(1/ell). Since vertex q values have norm one, |grad q| <= C_mesh/ell and |grad(q/|q|)| <= C_mesh/(c ell). This pays the spatial Lipschitz scale; the numerical constant C_mesh must be retained when translating to a rigorous continuum Dirac bound. There is no assertion that a small refinement factor already lies in the controlled continuum regime.

## Exact topological degree

Inside a barycentric flag, z-type contributions cannot cancel. Consequently z=0 is precisely the fixed resolved-dual curve composed of segments from pierced face centers to the tetrahedron center and onward to the other pierced face. The nonzero w phase along each such arc follows the shortest interpolation between its endpoint anchor phases.

Orient the arcs by the scalar vortex sign −n. On tetrahedron (a<b<c<d) of orientation epsilon, the net core phase increment in turns is

    −epsilon * n_bcd * [(phi_b−phi_a)−m_ab].

All faces other than bcd have anchor a; this gives the formula directly. Summing over a closed manifold, the dphi cup n term is exact and integrates to zero. Hence

    winding(w along z=0)= integral m cup dm = s.

For a normalized C² map into S³, its degree is this core winding, with the transverse orientation supplied by z. Therefore deg U=s. The sign is checked separately by integrating the S³ volume form in texture_degree.py.

On the actual cubic reconnection endpoints in cubic_move.npz, s is 0 and −1. The core rule gives −1.7e−16 and −1.0000000000000002 numerically. All 78 vortex segments per endpoint are retained. Random tests on 50,000 local samples yielded minimum unnormalized norm .47826 and maximal periodicity/vector-covariance errors below 5e−15; these are checks, not substitutes for the algebraic bounds.

## Physical costs and still-missing conclusions

This texture supplies a finite-range, bounded rotor-dependent mass on a refined Wilson boundary by sampling U at UV sites. With refinement r=ell/a_UV, a coarse region of N_c³ sites and slab thickness L uses 16(r N_c)³ L single-particle orbitals for the four-species charge-conjugated representation. The rotor factor remains L²(S¹) per coarse vertex. It does not truncate the rotor charge spectrum.

A continuum derivative-bound regime needs M ell large compared with the actual geometric constant while M remains small compared with the UV/bulk scales. This hierarchy cannot be obtained by simply sending M above the slab hopping, which relocates mirrors.

The correct lattice occupied axial charge has not been proved from the mass degree. Neither has a local charge-transfer amplitude between endpoint full slab ground states, consistency of overlapping quantum moves, absence of unwanted interface states, or a thermodynamic quantum gap. These remain separate requirements.

## Independent volume-form check

For each barycentric small tetrahedron with four real quaternion vectors q_0,...,q_3, the exact pullback of the S³ volume form for normalized affine interpolation is

    det(q_0,q_1,q_2,q_3) / |sum lambda_i q_i|^4

in standard simplex coordinates, with the domain orientation supplied by the parent tetrahedron and flag permutation. Tensor Gauss quadrature after a Duffy transform gave:

 order     endpoint a degree       endpoint b degree
 4          -.00243111797           -1.00780569884
 8           .00000022150            -.99999399797
12          -.00000000270           -1.00000000454

Only 468 small tetrahedra have nonzero determinant in either endpoint. This separately checks the geometric map, gluing, and sign rather than only verifying the algebraic core-phase formula.

## Rotor operator convention

The covariance above is a statement about the numerical fiber family H(phi). If the rotor symmetry sends |phi> to |phi+alpha>, multiplication operators transform by f(phi)→f(phi−alpha). Thus the mass-function covariance H(phi+alpha)=G_f H(phi) G_f† is precisely what the complete rotor–fermion Hamiltonian needs. One must not read the plus sign in the numerical texture function as assigning a second same-sign charge to a creation operator.

## Optional smooth spatial version, still strictly local

If a continuum index estimate requires more than spatial Lipschitz regularity, mollify the normalized C² field q(x) with a positive smooth compactly supported unit-integral kernel K_rho, then normalize again. Choose rho times the established Lipschitz constant below 1/2. Then ||K_rho*q-q||<=rho Lip(q)<1/2, so the convolution is nowhere zero and straight interpolation followed by normalization gives an explicit homotopy preserving degree. A standard bump K_rho(x) proportional to exp[-1/(1-|x|²/rho²)] inside |x|<rho and zero outside suffices. This adds only a fixed finite spatial neighborhood to the rotor dependence, preserves exact periodicity and vector covariance, and gives finite higher-derivative bounds with explicit rho dependence. It does not smooth across rotor-configuration walls. No global elliptic solve is introduced.
