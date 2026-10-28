# Conservative image flows to a continuous Stokes permeability certificate

Producer derivation; not yet independently reviewed. The target is a reusable lower-certificate operation for image-defined porous materials, not an acquired physical permeability or a new Stokes variational principle. Closest primary operations were recovered BEFORE implementation: divergence-conforming B-splines (Evans–Hughes, 2012/2013), FFT variational permeability upper bounds (Bignonnet–Dormieux 2014; Bignonnet 2020), and conforming variational bounds generally. The operation below uses this established mathematics and makes its data/rounding/support interface explicit. Historical priority is UNKNOWN.

## 1. Continuous target and supplied geometry

The periodic cell Q has M^3 cubes of side h, M>=6, volume M^3h^3. A supplied Boolean mask F defines the open pore Omega as the interior of the union of its closed pore cubes, on the three-torus Q. There is a nonempty open solid region. Define

    V={v in H^1_periodic(Q;R^3): div v=0, v=0 a.e. in the solid}.

This whole-cell definition avoids free assumptions about boundary corner regularity. Positive solid measure supplies a Poincare inequality. For viscosity one the periodic Stokes permeability K is defined by

    f^T K f = sup_(v in V) {2 f dot <v> - <|grad v|^2>}.   (1)

Here <.> is divided by TOTAL cell volume. This convention gives <u>=Kf. With viscosity mu, <u>=Kf/mu. For divergence-free periodic fields vanishing in the solid, the integrated energies 2|sym grad v|^2 and |grad v|^2 agree. We do not substitute a Darcy coefficient for the pore-scale continuum problem.

For a measured material, an independent warranted pore inclusion Omega_model subset Omega_physical is required before transferring a lower bound to physical no-slip Stokes flow. An ordinary segmented image by itself does not prove such an inclusion. A periodized cropped image is a declared mathematical cell, not a proven representative volume of the rock.

## 2. Exact discrete currents, INCLUDING winding flows

Let A be the one-cell Chebyshev erosion of F, with periodic neighbors: a cube is active only if all its 27 neighboring cubes, including itself, belong to F. Make one directed edge for every adjacent active pair in each positive coordinate direction. A current q_e is a mean normal VELOCITY coefficient, not a flux integral. D has +1 at the tail cell and -1 at the head. Require Dq=0 exactly.

For an x-face at x=(i+1)h, between cells (i,j,k) and (i+1,j,k), define its lowest-order Raviart–Thomas basis

    b_e^RT(x)=e_x beta_1(x/h-i-1) beta_0(y/h-j-1/2) beta_0(z/h-k-1/2),

with periodic sums understood. beta_0 is the centered unit box and beta_1 the centered tent. Analogously for y,z. The field w=sum_e q_e b_e^RT has continuous normal traces, zero normal trace on the boundary of the active cubes, and distributional div w=0 exactly when Dq=0. It need not be H^1 because tangential traces may jump. Its mean is

    <w>=(Cq)/M^3,  C_(a,e)=1 if edge e has direction a, else 0.  (2)

Conserved currents must NOT be represented only as curls of globally periodic potentials: those have zero mean and would remove the very transport to be measured. Dq=0 retains noncontractible cycle currents. A spanning forest with lifted integer cell coordinates computes the winding vectors of all graph cycles; their real span equals C ker D. This is ordinary periodic graph topology, not a newly invented percolation invariant.

## 3. Compact smoothing, exact no-slip and mean preservation

Convolve w periodically with the normalized cube box k_h(x)=h^-3 product_a beta_0(x_a/h). Then v=k_h*w has, for an x-edge,

    b_e(x)=e_x beta_2(x/h-i-1) beta_1(y/h-j-1/2) beta_1(z/h-k-1/2), (3)

where beta_2 is the centered quadratic cardinal B-spline. This is the lowest smooth member of the established divergence-conforming tensor-product spline complex.

Each component is H^1. Convolution commutes with distributional divergence and preserves the integral; hence div v=0 and <v>=Cq/M^3. Equivalently beta_2'=beta_1(.+1/2)-beta_1(.-1/2), so div v is a sum of product tents with coefficients Dq/h.

The box convolution expands raw support by at most h/2 per coordinate. Every active cube has a full one-cell certain-pore buffer, so the resulting support lies within the union of F cubes, with zero trace on the solid boundary. Thus v belongs to V. No finite-band Fourier field is incorrectly asserted to vanish on an open solid; no Brinkman penalty or infinite-contrast limit is used. Arbitrary rough active-cell topology is allowed because the proof uses whole-cell distributional identities and support.

There is a useful ROBUST GEOMETRY admission, stronger than exact nominal-image membership. Let Fbar be the closed union of nominal pore cubes and Abar the closed union of active cubes. The erosion rule proves

    Abar + [-h,h]^3 subset Fbar,
    supp(v) + [-h/2,h/2]^3 subset Fbar.          (3a)

Consequently v is an admissible no-slip trial for ANY other coercive periodic pore domain Omega' containing the interior of Fbar eroded by [-h/2,h/2]^3. The same tensor (6) therefore lower-bounds ALL such domains, without solving them separately. For a designed periodic material, a warranted maximum solid invasion of h/2 in this precise signed-distance/inclusion sense would transfer the certificate despite boundary uncertainty. Hausdorff proximity of arbitrary sets alone is not substituted for the inclusion; extra tiny internal barriers would violate it. A segmented micro-CT image does not itself warrant this condition. The executed data acquire the nominal model, not the manufacturing/measurement tolerance. At the supplied nominal h=5.345 micrometres, the conditional buffer is 2.6725 micrometres.

## 4. Finite exact energy stencils

Set M_p(k)=int beta_p(t) beta_p(t-k)dt and S_p(k)=int beta_p'(t)beta_p'(t-k)dt. Their nonzero values are

    M1(0)=2/3, M1(+-1)=1/6;
    S1(0)=2, S1(+-1)=-1;
    M2(0)=11/20, M2(+-1)=13/60, M2(+-2)=1/120;
    S2(0)=1, S2(+-1)=-1/3, S2(+-2)=-1/6.

Distinct velocity components have no cross terms in int |grad v|^2. For x-edges with index displacement k,

    E_x(k)=S2(kx)M1(ky)M1(kz)
           +M2(kx)S1(ky)M1(kz)+M2(kx)M1(ky)S1(kz). (4)

The y,z stencils permute coordinates. Only 45 offsets per orientation occur, all rational with denominator dividing 2160. Periodic assembly gives

    int_Q |grad v|^2 = h q^T E q.                 (5)

These are exact integrals of compact polynomial basis functions. There is no omitted Fourier tail, numerical quadrature debt or collocation derivative assumption. The companion exact consumer independently integrates the piecewise polynomials before evaluating the currents.

## 5. Solver-independent certificate and exact rounding

Take any k columns Qc of discrete currents with DQc=0 exactly. They can be generated by any floating solver, surrogate or hand construction. Let G=Qc^T E Qc and J=CQc. Remove dependent columns until G is positive definite. Optimizing (1) over this finite trial span gives the full tensor inequality

    K >= K_lower = (h^2/M^3) J G^-1 J^T.         (6)

This is Loewner order, so it certifies every real force simultaneously. No reliable solve of the large floating linear system is assumed: any supplied currents satisfying the finite checks yield a valid bound. Only a matrix of size at most three is inverted for the executed three-force construction.

For the executed image-derived cell, exact Sylvester tests also show K_lower/h^2-(1/100)I is positive definite. Thus it certifies the concrete model-side design requirement K>=(h^2/100)I, including every domain admitted by (3a). This threshold is a derived algebraic consequence after computation, not a preregistered empirical comparison. A physical material has not been admitted by an acquired tolerance/flow-law certificate here.

To convert approximate currents to exact ones: round every edge current to a dyadic integer numerator, compute its exact divergence r=Dq, and correct tree edges in reverse forest order. For child c and parent edge e let s=D_(c,e) in {+-1}; set q_e <- q_e-s*r_c and r_parent <- r_parent+r_c. Every component has sum r=0, so roots finish at zero. Non-tree currents and all supports are retained. Overflow must be excluded by integer bounds, not assumed. Python-integer evaluation of (4)-(6) then certifies the corrected field. Poor approximate currents merely yield a weaker valid lower bound; they do not invalidate it.

The exact-rational energy and mean may be stored without the common dyadic denominator, which cancels from JG^-1J^T. Three trial columns require O(number_of_edges) exact arithmetic because the stencil support is fixed. Bit costs include rounded-current magnitudes, tree sums and rational 3x3 inversion. This is not a uniform accuracy or optimality bound for the floating solve.

## 6. Equal-information comparison and meaningful limits

An equally informed ordinary spline-Stokes Galerkin solver uses the SAME geometry, active basis and force vectors. It may solve the saddle system [E D^T;D 0] and report Cq/M^3 as a point estimate. This operation adds exact divergence repair, exact support/energy integration and a full continuous lower certificate to its approximate output; no generic speedup over that solver is claimed. A direct FEM/FFT bound with comparable rigor is a strong existing comparator, not a strawman.

The first local six-face bubble lift was rejected: although conforming, it enforces artificial tangential zeros on every internal grid face and caps its permeability by O(h^2) under fixed physical refinement. FAILED_LOCAL_LIFT.md preserves that general obstruction. Smoothing the RT field avoids those artificial internal walls. It still pays a buffer: erosion may destroy narrow image connections. No universal bound on the fraction of true permeability captured, no arbitrary-resolution convergence rate, no physical subvoxel pore guarantee, and no RVE or laboratory agreement is asserted. These are substantive limits to a discovery-multiplier claim.

The executed public-image calculation is a model-side construction. If the numerical result is far below the ordinary prediction or its enclosure is too loose to decide a task, it must not be promoted as a practical improvement merely because the certificate is exact.
