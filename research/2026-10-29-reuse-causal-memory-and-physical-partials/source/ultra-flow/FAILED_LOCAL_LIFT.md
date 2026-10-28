# Failed first construction: local face bubbles create grid-scale walls

For each cube let phi(t)=6t(1-t), Phi(t)=3t^2-2t^3, and face-normal coefficients a_i,b_i. The local velocity

    v_i=[a_i+(b_i-a_i)Phi(x_i)] product_(j!=i)phi(x_j)

has exact div v=(sum_i(b_i-a_i)) product_j phi(x_j). Conserved face currents therefore yield a global continuous, divergence-free, no-slip field. Exact integration gives, per opposite-face pair,

    E_pair=[10872(a^2+b^2)+3456ab]/875.

This includes turning/junction cost and provides a legitimate variational lower bound. For a one-voxel straight square duct its resistance 144/5=28.8 is close to the exact square-duct value. That attractive control is misleading at higher resolution.

The construction forces tangential velocity to zero on EVERY internal grid face. For each component i, every line in a transverse coordinate is cut into intervals of length h on whose endpoints v_i=0. The one-dimensional Dirichlet Poincare inequality gives int v_i^2 <=(h/pi)^2 int |partial_j v_i|^2 for any j!=i. Thus, globally,

    <|v|^2> <= (h/pi)^2 <|grad v|^2>.

By Cauchy, optimizing 2f dot <v>-<|grad v|^2> over this entire lift space gives f^T K_lift f <=h^2|f|^2/pi^2. For a fixed physical channel as h->0 this tends to zero while the actual permeability stays positive. No grid tuning or larger numerical solve repairs this representation ceiling. The near-exact one-cell duct control was therefore not an adequate discriminator.

The continued construction uses a compact mollification of a globally conservative RT field, producing established divergence-conforming B-spline fields. This preserves global mean/winding currents while allowing tangential flow across interior faces. Its support buffer and any loss of narrow channels remain explicit.
