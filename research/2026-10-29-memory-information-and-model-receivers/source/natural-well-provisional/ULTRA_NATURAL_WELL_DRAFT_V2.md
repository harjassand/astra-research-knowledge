# Natural wells close to a harmonic oscillator: developing construction

29 October 2026. Root construction in progress; substantive peer challenge is
active. No novelty, physical implementation, efficient compiler or completed
universal coefficient table is claimed. The local smooth free-isometric-
embedding perturbation theorem is an explicit mathematical dependency.
Zergaenge1712.02766 Theorem1.1 has now been read in the primary source: a smooth
metric family through a given free isometric embedding has a smooth family of
isometric embeddings through that same map. This supplies every required
finite derivative norm. The computational implementation and priority question
remain separate from this mathematical existence dependency.

## Intended theorem and exact scope

Let M be a compact smooth manifold without boundary, Y a smooth vector field
and f_1,...,f_k smooth real observables. For every 0<eta<1 the proposed result
constructs a finite D, epsilon>0, and a C-infinity potential V on R^D such that

    ||D^2 V - I||_op < eta globally,
    V(q)=|q|^2/2 outside a compact annulus,

and the natural system q'=p, p'=-grad V contains the clock extension

    Z_epsilon = epsilon Y + partial_theta on M x S^1.

All embedded points have energy 1. Each f_j is recovered by a fixed quadratic
POSITION observable. This is not a claim about analytic/polynomial V, rational
initialization, a finite-precision/noisy universal computer or an efficient
trajectory algorithm. A computability corollary additionally needs effective
input data and a constructive version of the local embedding step.

In fact the construction gives a smooth family V_epsilon with a common compact
annular support for V_epsilon-|q|^2/2 and

    V_epsilon-|q|^2/2 -> 0 in every fixed global C^r norm, r finite.

Thus any prescribed finite collection of derivative tolerances can be met by
one sufficiently small positive epsilon. This does not assert a single
epsilon satisfying arbitrarily specified bounds in infinitely many norms, or
proximity in an analytic norm. The encoded physical clock slows as 1/epsilon.

## 1. A spherical free embedding with retained observables

Take a smooth free embedding h:M->R^r: in local coordinates the vectors
{h_i,h_ij: i<=j} are independent. One explicit ordinary way to obtain this
from any smooth embedding j:M->R^m is the quadratic lift
h=(j,(j_a*j_b)_(a<=b)). In a linear combination of its first and second
jets, the j coordinates first set the combined first jet of j to zero.
The quadratic coordinates then leave only the symmetric products of the
linearly independent j_i, forcing every second-jet coefficient to vanish;
the first-jet coefficients then vanish too. No local isometric-embedding
problem is needed just to acquire freeness. Fix a0=1/2 and a
positive delta so small that

    delta^2 (|h|^2 + sum_j f_j^2) < 1-a0^2

with a strict margin everywhere. Set

    Psi=(a0, delta h, delta f_1,...,delta f_k,
          sqrt(1-a0^2-delta^2(|h|^2+sum_j f_j^2))).

Then |Psi|=1 and Psi is an embedding. The vectors {Psi,Psi_i,Psi_ij} are
independent: the constant anchor kills the coefficient of Psi, and projection
onto the h coordinates then invokes freeness of h. The f_j coordinates are
exactly delta f_j, not reconstructed approximately.

Let L=dim Psi and define Q0:M x S^1 -> R^(2L) by

    Q0(x,theta)=(Psi(x) cos theta, Psi(x) sin theta).

The nonzero anchor recovers theta, and then Psi recovers x, so Q0 is an
embedding. Its induced metric is g0=gM+dtheta^2 with gM=Psi^*e, because
Psi.Psi_i=0. In the frame rotated by theta, its first and second derivatives
are grouped as

    first copy: Psi_i, Psi_ij, -Psi;
    second copy: Psi, Psi_i.

Both groups are independent by the preceding statement. Thus Q0 is free as
an embedding of the (dim M+1)-manifold. It is spherical, |Q0|=1, and
partial_theta^2 Q0=-Q0.

For a torus an explicit free h/Psi can instead be made from a constant anchor
and sin/cos pairs with frequencies e_i and e_i+e_j. At any torus point all jet
vectors are a fixed orthogonal rotation of those at zero. The anchor selects
Psi, sine e_i selects first jets, cosine e_i selects diagonal second jets,
and cosine(e_i+e_j) selects mixed second jets. This supplies an all-point
analytic freeness proof, not a finite rank diagnostic.

## 2. Make the slow flow geodesic, keeping the fast clock

For epsilon>0 define a smooth metric on M x S^1 by

    g_epsilon((v,a),(w,b))
      = a b + gM(v-epsilon a Y, w-epsilon b Y).

It is positive definite. For Z=epsilon Y+partial_theta,

    g_epsilon(Z,.)=dtheta,    g_epsilon(Z,Z)=1.

Since dtheta is closed and dtheta(Z)=1 is constant, the Koszul formula gives
grad_Z Z=0 for the Levi-Civita connection of g_epsilon. Hence Z trajectories
are unit-speed geodesics. The metrics tend to g0 in every fixed smooth norm
as epsilon tends to zero. This is an exact identity, not averaged dynamics.

## 3. Complete the metric without changing readout coordinates

Use s=3/5 and t=4/5, so s^2+t^2=1. The local perturbation input is:

    For a smooth free compact embedding Q0, every sufficiently small smooth
    one-parameter metric family g0+h_epsilon, h_0=0, admits a smooth family
    of isometric embeddings R_epsilon through R_0=Q0 for small epsilon.

Only this local near-Q0 assertion is used; a global C0-short approximation
theorem would not suffice. Smooth dependence follows from the primary
Zergaenge Theorem1.1, and is stronger than the C^4 proximity first required.

Apply it with h=(g_epsilon-g0)/t^2. Let R_epsilon be the resulting map and set

    Q_epsilon=(s Q0, t R_epsilon):M x S^1 -> R^(4L).

Then Q_epsilon^*e=s^2 g0+t^2(g0+h)=g_epsilon. It is an embedding even if R
were only an immersion, because its first block is the exact embedding sQ0.
Moreover Q_epsilon tends in C^4 to Qbar0=(sQ0,tQ0), which is spherical and
obeys partial_theta^2 Qbar0=-Qbar0.

The first block has not moved. If u0,v0 are its two anchor coordinates and
uj,vj the two coordinates of the retained delta f_j component, then

    O_j(q) = (u0 uj+v0 vj)/(s^2 a0 delta)

recovers f_j(x) EXACTLY along the embedded configuration manifold. It is a
fixed quadratic function of position alone, independent of epsilon and time.

## 4. Acceleration supplies a compatible potential jet

Let S_epsilon=Q_epsilon(M x S^1) and define the Euclidean acceleration field

    A_epsilon = Z(Z Q_epsilon).

Because Q_epsilon is isometric and Z is geodesic, A_epsilon is normal to
S_epsilon. It tends in C^2 to -Qbar0 as epsilon->0, since Q_epsilon is C^4
close and Z is C^3 close to partial_theta. In particular

    b_epsilon = -A_epsilon-Q_epsilon -> 0 in C^2.

Prescribe V|S=1/2 and grad V|S=-A_epsilon. These jets are compatible: the
specified gradient is normal, exactly as required by the constant value.

Relative to V0(q)=|q|^2/2 the required value and gradient are

    a_epsilon = 1/2-|Q_epsilon|^2/2,
    b_epsilon = -A_epsilon-Q_epsilon.

Their tangential compatibility is grad_S a_epsilon=projection_T b_epsilon.
Also a_epsilon->0 in C^2, b_epsilon->0 in C^2.

## 5. Small global extension and exact natural dynamics

For epsilon small, C^4 proximity to the fixed compact embedding Qbar0 gives
a common tubular radius and uniformly bounded needed derivatives of the
nearest-point projections pi_epsilon. Choose a fixed smooth cutoff chi equal
to1 near zero and supported within that tube. In normal coordinates
q=z+n, z=pi_epsilon(q), define

    W_epsilon(q)=chi(|n|^2)
                  [a_epsilon(z)+b_epsilon(z).n],

and set W=0 outside the tube. At n=0 its value is a_epsilon; its gradient is
the sum of the tangential gradient of a and the normal part of b, hence is b.
Consequently V=V0+W has the prescribed compatible jets.

The required C^2 extension estimate is

    ||W||_C2 <= C [||a||_C2 + ||b||_C2],

with C uniform over the small C^4 family of embeddings. A second tangential
derivative of b.n occurs away from n=0, which is why b must be small in C^2
and the embedding is required to be close in C^4. Local smooth metric
perturbation is invoked at that stronger norm, not only at C^0 or C^1.
With these norms W->0 in C^2.

More generally the parameter-dependent tubular maps and cutoff can be chosen
smooth with support in one fixed annulus for epsilon in a compact short
interval. Since a_0=b_0=0, W_0=0. Smooth parameter dependence and compact
support imply ||W_epsilon||_Cr=O_r(epsilon) for each fixed finite r. This
proves the stronger C-infinity-topology assertion without exchanging a
finite-r bound with an infinite list of independently specified tolerances.

Choose epsilon so ||D^2W||<eta. Its tube lies near the unit sphere and avoids
the origin. V=|q|^2/2 near the origin and outside a compact set, and global
uniform convexity gives its unique minimum0 at the origin. The Hamiltonian
vector field is globally Lipschitz and complete. On the embedded phase state

    iota(x,theta)=(Q_epsilon(x,theta),Z Q_epsilon(x,theta)),

Hamilton's equations agree exactly with Z, since q'=ZQ and
p'=A=-grad V. Speed is1, V=1/2, so every encoded state has energy1.
The first position block makes iota injective. No approximate trajectory
or long-time error estimate is being substituted for this exact invariant
embedding. The map contains a slow copy of Y plus a fast clock; no infinite
computation is compressed into a finite time.

## 6. Relation to the existing constructions

Tao1707.02389v3 Theorem1.6 provides ordinary potential-well universality from
a strongly adapted form; Proposition1.8(v) covers arbitrary flow x circle.
Its stated coercivity modification does not by itself assert global uniform
convexity or closeness to a fixed harmonic well. Local Nash/Gunther tools are
established. The conjectured new conjunction is the near-harmonic NATURAL
potential, exact readout-preserving completion and fixed quadratic position
observable. A primary-prior comparison is active; historical novelty UNKNOWN.

N716's Sections3--5 provide a different exact mixed-momentum resonant lift,
not this natural-potential theorem. Its full source has been read. Its compact
torus/latch construction plus the published CMP21 polynomial simulator gives
a prospective convergent-bit corollary after the geometric theorem and
effective construction interfaces are settled. N675 and its stated internal
dependencies remain CORRECT AND ACCEPTED by standing instruction; no part of
this construction purports to re-audit them or to follow automatically from
their quantum-channel order theorem.

## 7. Explicit torus dimension and readout

For M=T^d take the frequency set A={e_i:1<=i<=d} union
{e_i+e_j:1<=i<j<=d}; its size is m=d(d+1)/2. With rational
kappa=1/(m+1), put

    a=(1-m*kappa^2)/(1+m*kappa^2),
    c=2*kappa/(1+m*kappa^2),
    Psi=(a, (c cos(alpha.x),c sin(alpha.x))_(alpha in A)).

Here a>0 and a^2+m*c^2=1 exactly. No extra square-root coordinate is needed.
At x=0 the anchor removes Psi, the sine e_i coordinates remove all first
derivatives, cosine e_i removes all diagonal second derivatives, and cosine
(e_i+e_j) then removes all mixed second derivatives. At every x the same
derivative frame is an orthogonal rotation of this one. This proves augmented
freeness at every point. The induced gM is a constant positive metric.

Thus L=1+2m and the natural configuration dimension is

    D=4L=4d(d+1)+4.

This bound is independent of the velocity field's Fourier degree, number of
monomials, or description length. Those costs remain in the potential and
infinite convergent isometry construction. Each sine/cosine input coordinate
already has a retained position-only quadratic readout. Extra general smooth
observables can instead use the original construction in Section1.

If one uses the 17-dimensional tracking simulator described in CMP21
Remark3.4, N716 Section6 adds one halting-coordinate circle, one clock circle
and two latch circles, giving d=21 and D=1852. This is a conditional explicit
dimension bound on that stated source interface, not an expanded universal
coefficient table or a practical mechanical design. The absorbing halting
state and exact computable initialization remain part of the simulator input.

## 8. Nearly round convex hypersurfaces

There is a geometric consequence in addition to the natural Hamiltonian.
Let Sigma_epsilon={q:V_epsilon(q)=1/2}. Global uniform convexity, V(0)=0,
and properness make this a smooth closed strictly convex hypersurface,
diffeomorphic to S^(D-1). The gradient is nonzero there because the origin
is the only critical point. Smooth dependence and the radial implicit function
theorem make Sigma_epsilon tend in every fixed C^r norm to the unit sphere.

Every encoded q(t) lies on Sigma_epsilon, has Euclidean speed1, and obeys
q''=-grad V(q). Its acceleration is normal to the WHOLE hypersurface, so it
is a unit-speed geodesic of the induced Euclidean metric. Consequently

    (M x S^1, epsilon Y+partial_theta)

embeds exactly into the unit tangent geodesic flow of an arbitrarily nearly
round strictly convex Euclidean hypersurface, with the same quadratic position
readouts. The second fundamental form is positive definite. By the Euclidean
Gauss equation every sectional curvature is positive, and for fixed finite
norm tolerances it can be made uniformly close to1. This does not say that
the whole geodesic flow is conjugate to Y, or that positive-volume invariant
sets or transverse stability have been obtained.

Generic chaotic geodesics of convex hypersurfaces and generic universality
near elliptic periodic points are established prior directions. The stronger
conjunction here is exact arbitrary smooth-flow embedding with a clock,
near-round extrinsic geometry and fixed position readout. Its historical
priority remains UNKNOWN; those generic chaos results are not evidence of
newness, and neither do their stated abstracts supply this exact conjunction.

## 9. An explicit tubular radius for the torus construction

This supplies a constructive interface, not just an appeal to compactness.
Let d_flat be the standard shortest Euclidean angular distance on T^(d+1),
and D0=|Q0(x,theta)-Q0(y,phi)|. The anchor and retained e_i pairs give

    |exp(i theta)-exp(i phi)| <= D0/a,
    |Psi(x)-Psi(y)| <= (1+1/a) D0,
    d_flat((x,theta),(y,phi)) <= C D0,
    C=(pi/2)*sqrt((1+1/a)^2/c^2+1/a^2).

Because the first block sQ0 never changes, Q_epsilon is globally
co-Lipschitz with lower constant s/C. A rational lower constant is

    m=s/[2*((1+1/a)/c+1/a)] > 0.

Let B>0 be an upper bound on the operator norm of the flat-coordinate Hessian
of Q_epsilon; a coefficient absolute-sum derivative bound suffices. For any
shortest angular displacement v from z to z', Taylor's formula gives

    |projection_(normal at z)(Q(z')-Q(z))| <= B |v|^2/2.

Together with |Q(z')-Q(z)|>=m|v|, this shows that for normal n at Q(z),

    |Q(z)+n-Q(z')|^2-|n|^2 >= (m^2-|n|B)|v|^2.

Thus every |n|<m^2/B has Q(z) as its UNIQUE closest point on the whole
embedded torus. Choosing a rational r<min(1/8,m^2/(4B)) yields a certified
normal tube. The Hessian of the normal projection's implicit equations is
bounded below there by m^2-rB, so differentiation of those equations bounds
the needed projection derivatives using m,r and C^3/C^4 bounds on Q. These
are finite algebraic upper bounds. For small epsilon the tube also remains
away from the origin, because Q_epsilon tends uniformly to a unit sphere.

For a finite-Fourier velocity field, the Fourier contraction constructed in
../b_conventional/periodic_gunther.py gives computable upper bounds on every
fixed derivative of its limit, with a geometric approximation tail. The
fixed analytic strip is a regularity and computability tool for Q, not a
claim that the globally cut-off V is analytic. The tube above, a computable
smooth cutoff and implicit normal projection make the global potential
computable. One can halve rational epsilon until the explicit C^2 extension
upper bound is below eta. This terminates by the O(epsilon) estimates.
No efficient complexity bound, whole universal coefficient expansion or
laboratory preparation is supplied by this existence algorithm.
