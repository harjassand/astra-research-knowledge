# Exact complementary-energy upper on the original pore cell

Producer continuation. Same original centered48-cube periodic image, same voxel size and Stokes convention as ../PROOF.md. No new pore image, crop, continuum discretization grid or physical assumption is introduced. Equilibrated H(div) stresses, complementary-energy bounds and pressure-robust Stokes error estimation are established ordinary methods; see Lederer–Merdon, arXiv:2008.05816v2, sections1-2. The aim is a finite executable upper using these methods, not a new variational principle.

## 1. Upper principle with pressure and boundary conventions

Use the lower package's whole-cell space V of periodic H1 divergence-free velocities zero in the ORIGINAL solid. Let sigma be a tensor with each row in periodic H(div,Q), satisfying div sigma=f in all original fluid cubes. Its divergence in solid cubes is unrestricted. This supplies the solid counterforce needed for the integral of a periodic divergence to vanish; setting div sigma=f everywhere on the torus would be impossible for nonzero f.

For every v in V, integration by parts gives

    f dot <v> = -<sigma:grad v>_fluid
              = -<dev(sigma):grad v>_fluid.

Here dev sigma=sigma-(tr sigma)I/3. There is no boundary traction assumption at a fluid/solid face: v has zero trace there. A globally H(div) extension makes all interior face terms cancel, and the outer terms cancel by periodicity. Normal tractions at pore walls need not vanish. Solid stress has zero pairing with v and is not included in the energy.

The energy convention is int|grad v|^2. Although it equals int2|sym grad v|^2 for admissible velocities, sigma is a NONSYMMETRIC pseudostress. Its antisymmetric part may NOT be discarded, and there is NO factor1/2 in the bound below. Cauchy plus 2ab-b^2<=a^2 yields

    f^T K f <= <|dev sigma|^2>_fluid.              (U1)

The pressure freedom is retained by the deviatoric projection. For three equilibrated fields sigma^(k) with div sigma^(k)=e_k, linear combination supplies every f and gives the full tensor upper

    K <= U,  U_kl=<dev sigma^(k):dev sigma^(l)>_fluid.  (U2)

A scalar-Poisson construction is a valid initial upper, but is not assumed tight. The continued optimization minimizes the deviatoric norm across all row-wise RT0 stress variables.

## 2. Original-grid row-wise RT0 stresses

Assign a unique oriented face variable q_(e,i) for row i at every voxel face adjacent to at least one ORIGINAL fluid cube. Faces with two solid neighbors have value zero. In a fluid or solid cube, component sigma_ij varies linearly in coordinate x_j between its incoming/outgoing face values a_ij,b_ij and is constant in the other coordinates. Shared normal traces agree. This is a global periodic row-wise RT0 H(div) field, with no smoothing or pore erosion.

Let D have +1 at a fluid tail cell, -1 at a fluid head cell, and no row for a solid cell. Then div sigma_i=(Dq_i)/h on each fluid cube. Work at h=1 with Dq_i=e_(k,i) for force k; the physical field is h times that field. Its integrated squared stress divided by total cell volume therefore scales by h^2.

Every fluid connected component has at least one fluid/solid face because the torus graph is connected and there is nonempty solid. Its source can leave through this unconstrained-traction face. This is not a divergence-free-current constraint with zero component sum.

## 3. Exact cell energy and finite tensor

Write m_ij=(a_ij+b_ij)/2 and d_ij=b_ij-a_ij. Exact integration over a unit cube gives

    int dev(sigma^k):dev(sigma^l)
      = sum_ij m_ij^k m_ij^l - tr(m^k)tr(m^l)/3
        +[sum_ij d_ij^k d_ij^l - sum_i d_ii^k d_ii^l/3]/12.  (U3)

The diagonal slopes depend on different coordinates, whose centered first moments vanish; no cross-coordinate slope terms are missing. This quadratic is positive semidefinite, with its hydrostatic mean direction free. The numerical optimizer uses the same formula, and the exact consumer independently integrates the affine components.

For dyadic stress numerators z with denominator 2^b, let S=a+b, Dlt=b-a and T=sum_i S_ii. The exact numerator cross-energy with denominator36 is

    G_kl=sum_fluid[9 sum_ij S_ij^k S_ij^l-3T^kT^l
                        +3 sum_ij Dlt_ij^kDlt_ij^l-sum_i Dlt_ii^kDlt_ii^l].

The certified matrix in voxel-squared units is U=G/[36M^3 2^(2b)], and in SI units it is multiplied by the SAME nominal h^2 used by the lower package. No large numerical inverse or residual estimate is trusted by this consumer.

## 4. Exact repair with solid counterforce

After rounding the nine face-stress fields, compute each fluid-cell residual r=Dz-2^bI. Choose a spanning tree in each fluid connected component, rooted at a fluid cell with a solid-neighbor face. Eliminate non-root residuals by tree-edge corrections exactly as in the lower package. At the root, correct its solid-neighbor face by -s*r_root, where s=+-1 is that face's incidence at the root. The source in the fluid is then EXACT. The induced solid divergence supplies the counterforce. Integer overflow is explicitly excluded; the independent consumer uses Python-integer force checks.

Any repaired stress gives a valid upper regardless of numerical convergence. A poor optimizer or aggressive cap may make it loose; it cannot turn the final verified equilibrium and exact energy into a point-prediction-only claim.

## 5. Finite lower/upper comparison and transfer scope

The exact lower L already belongs to the ORIGINAL domain's variational space, despite its internal support buffer. Once U is acquired, the same continuum satisfies L<=K<=U. Exact rational principal-minor checks of U-L are a useful consistency control; they are not the mathematical proof of the full continuum statements. A rational gamma with gamma L-U positive semidefinite gives a simultaneous all-force multiplicative interval.

The nominal upper transfers to a physical domain only with the OPPOSITE warranted inclusion Omega_physical subset Omega_upper. The lower uses an inner-pore inclusion. Thus a physical two-sided claim needs both, plus the same periodic-cell, continuum/wall-law and fluid calibration assumptions. Neither is implied by the segmented image. This continuation constructs an upper on the original mathematical cell, not an outer-geometry experiment or a physical permeability measurement.
