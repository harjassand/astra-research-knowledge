Finite radii: exact balance, dilute equilibrium error and contact geometry

Scope. The completed inhomogeneous point-particle compiler does not yet
describe mutually excluding particles of positive radius. The following
pays three interfaces for that different model. None is a quantitative
mixing or actual collision-work theorem for a many-body reflected gas.

1. A geometry with no impossible all-population packing promise

For a fine species s put d_s=|P_s|_1>=1 and give it radius rho*d_s.
Conserved weighted mass<=N0 implies sum_i d_s(i)<=N0 and n<=N0.
Only configurations in this invariant mass cap are physical states of
the new finite-container problem. Abstract chemical decoder graph
equivalence may still hold on all fine counts; positive spatial support
cannot be demanded for arbitrarily many fixed-radius particles in a
finite box. That stronger demand would be impossible for a trivial
packing reason, unrelated to kinetic compilation.

Require every closed particle ball to lie inside Omega, so its center
satisfies n_f.x<=b_f-rho*d_s in unit-normal facet notation. Require pair
distances>=rho(d_s+d_t). These are finite algebraic inequalities from the
original rational facets, a rational rho and integer payload sizes.
Choosing rho*(1+N0+max d_s)<=min(kappa,r)/2^16 ensures a large interior
parking region. Every fine count within the cap has a strictly feasible
placement: arrange its balls along a diameter of the inball, with total
occupied diameter2rho sum d_s<<kappa. This is an existence construction,
not an emitted list of N0 particles or a path-connectivity assertion.

2. Exact nominal chemical balance survives geometric rejections

Use the unnormalized hard-core grand-canonical reference
 product_s[(a_tilde_s/V)^n_s/n_s!] *1_feasible * product_i dx_i,
restricted to conserved mass<=N0 or to an actual invariant class.
No configuration-volume or class normalizer is computed.

For binding A+B->C keep the point rule: ordered eligible pair x,y,
attempt coefficient c_e*V*K_r(y-x), product anchored at x. Execute it
only when the product configuration is feasible. Otherwise emit a hidden
binary null attempt A+B->A+B. Reverse C->A+B draws z from K_r, anchors
the first product at x and second at x+z, and succeeds only if the new
configuration is feasible. Invalid releases are hidden unary null marks.
Apply the analogous success/rejection rule to a unary species conversion
whose new radius is larger. Original true null marks remain observed.

The successful pair is supported on EXACTLY the same pairs of feasible
configurations in both directions. Its Jacobian is1. The source Palm
factor c_e*a_A*a_B/V equals c_reverse*a_C/V by the old activity identity.
Ordered pairs retain the stipulated no-1/2 convention. Geometric
rejection is a diagonal flux and is self-reverse for every configuration.
One fixed hidden rejection branch per base channel suffices structurally;
the branch list need not depend on radius, geometry or population.

For a fixed count the nominal divergence-form diffusion has uniform
Lebesgue measure on its feasible configuration domain as invariant
measure, PROVIDED the conormal reflected realization is established.
At a contact, with e=(Qi-Qj)/|Qi-Qj|, the prescribed pushes are
 +D_i(t,Qi)e*dLij on i and -D_j(t,Qj)e*dLij on j.
This is conormal reflection in the block nominal matrix. It is not an
independent-particle process. At a wall use -D_i*n_f*dL_if at the shifted
face. The variable D intrinsic drift is still div D_i. Nominal form
symmetry and local reaction flux balance require no unknown mobility
value in a chemical coefficient.

3. A paid all-count equilibrium estimate without a3N-volume oracle

Fix any count in the mass cap. Under independent uniform center positions
in the ORIGINAL Omega, let E be feasibility. Eroding Omega by s removes
at most3s/kappa of its volume fraction: it contains the homothety
 c+(1-s/kappa)(Omega-c).
Thus the wall union bound is<=3rho N0/kappa.

The pair-overlap probability is at most
 [rho(d_i+d_j)/kappa]^3,
since V>=4pi*kappa^3/3. Also
 sum_(i<j)(d_i+d_j)^3
 <=(sum_i d_i)^2 sum_(i<j)(d_i+d_j)
 =(n-1)(sum_i d_i)^3<=N0^4.
Consequently
 p_bad=P(E^c)<=3rho N0/kappa+rho^3 N0^4/kappa^3.
Choose rho so p_bad<=1/4. The conditional feasible uniform law differs
from the independent product in TV by exactly p_bad; bounded observable
errors therefore have paid polynomial coefficients.

For a chemical attempt, represent the source and offset using at most
one extra point. The local placement density relative to independent
uniform positions is bounded by V/v, v=(2r)^3. Feasibility of BOTH source
and target can be tested on this extended sample space; its total payload
size is at most2N0. The same union bound gives a conservative error
 C(1+V/v)*p_bad(2N0)
for an averaged success/rejection kernel, after dividing by a source
feasibility probability>=3/4. This is a fixed polynomial times rho for
rho<=1, with r^-1,kappa^-1,N0 charged. The old EXACT point normalizer
q, computed in dimension6, can still be used: hard-core average-rate
errors can be made small with polynomial rho^-1 rather than computing
new count-dependent normalizers. The flux equality in2 is exact even
though this effective count-rate approximation is only approximate.

These are equilibrium observable estimates. They do not put an arbitrary
actual initial placement at equilibrium or prove a conditional occupation
bound after a chemical event. They also do not justify replacing the
interacting process by independent particles for its whole run.

4. A rationally conditioned common inward direction for contact clusters

Assume rho*N0<=kappa/16 and rho<=kappa/16. Form the graph of touching
balls. Every connected component has diameter<=2rho N0. For a component
C choose its center of mass z_C and let
 v_i=(c-z_C)+(Qi-z_C), i in C.
The first term moves the component toward the certified inball; the
second dilates it. For any contact i,j in C,
 e_ij.(v_i-v_j)=|Qi-Qj|=rho(d_i+d_j)>=2rho.
For any shifted active outer face of particle i,
 -n_f.v_i>=(Qi-c).n_f-2|Qi-z_C|
 >=kappa-rho*d_i-4rho N0>=kappa/2.
Moreover ||v||<=4sqrt(n), enlarging a fixed constant if necessary.
Thus the normalized configuration vector has positive scalar product
with EVERY inward unit active normal, with margin at least
 rho/[16(1+N0)].

For a neighborhood version, form components using pairs within a small
extra gap and walls within that gap. Taking the gap at most a fixed
constant times rho^2/(1+N0)^2 preserves the same diameter and half the
angular margin: a pair normal varies at rate O(rho^-1). This supplies
polynomially conditioned local cone compatibility without a constant
exponential in particle number or facet count.

In particular no nonzero positive combination of active normal vectors
vanishes. For the block nominal conormal pushes multiply a putative zero
combination by the inverse block matrix, then test against v. Hence wall
and pair-clock decompositions cannot acquire arbitrary cost by adding a
positive zero-force circulation. The positive-cone margin bounds their
sum against the regulator variation with paid rho^-1,N0,d0^-1 factors.
It does NOT yet bound that regulator variation in expectation.

5. The missing dynamic operation

The old convex metric-projection potential projects onto a contracted
CONVEX set. The many-body hard-core configuration set is nonconvex and
its dimension grows with population. Pair-contact terms have additional
curvature signs. Applying a3N-dimensional heat bound with exponent3N/2
does not pay a universal numerical exponent, even though the cone
constants in4 are polynomial. A quantitative dilute-gas conditional
contact comparison from EVERY feasible placement, and actual wall/PAIR
push bounds under the whole predictable fault box, remain to be built.

Small equilibrium excluded volume alone does not bound nonequilibrium
collision work or provide a density-independent spectral gap. Starting
from touching clusters invalidates a claim that a first collision is
automatically a rare event. The point conditional-clock/channel machinery
can be reused after the needed occupation estimates are actually paid;
it is not itself an interacting-gas theorem. No atomic or energetic
validity follows from a positive hard radius in this ideal model.

Primary scope actually read after completed local hold checks: Fradon,
https://arxiv.org/pdf/0910.5394v1, Theorems2.2/2.4 and Proposition3.4,
the contact-cluster geometry in Proposition4.1. These are finite globules
with normal reflection, bounded Lipschitz coefficients and their specified
radius/gradient-interaction constraints. Their geometry is an opening,
not the present time-dependent conormal/reaction/compiler/cost theorem.
No cited held original, Tanaka theorem, alternate version or archive was
followed or recovered. The root calculations above concern this different
finite-radius interface directly.
