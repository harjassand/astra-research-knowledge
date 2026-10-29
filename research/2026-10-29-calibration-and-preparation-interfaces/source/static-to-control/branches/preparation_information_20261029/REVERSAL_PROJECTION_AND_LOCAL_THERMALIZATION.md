# A stationary process has a nearest reversible Markov explanation

29 October 2026. Root construction, with the subsequent native-class resolution
linked below. This extends the preceding
physical-information results without changing their scope. All reversals below
are specified involutions; no observation is assumed to identify that involution.
Thermodynamic interpretation requires the source and bath conditions stated below.

## Scientific target

The orientation lift showed that a large stationary preparation divergence can
shield a small sustained reversal rate. A bound on that KL boundary is not the
only remedy. The relevant geometry for approximation by an equilibrium process
is a bounded Jensen--Shannon boundary. A bath need only control the modes that
change under reversal to make that boundary small; it need not erase all hidden
configurational memory. The intended result is a process-level stability and
identifiability principle, not a new fitted entropy estimator.

## 1. Finite Markov theorem with arbitrary specified parity

Let L be an irreducible row generator on a finite state set, with stationary
rho>0 and a specified involution theta. Write q_z=rho_{theta z},
mu=(rho+q)/2, and L^R=Theta L^* Theta, with stationary law q.
Let d(a||b)=a log(a/b)-a+b for rates, with its usual extended-value convention.
Define

    sigma = sum_z rho_z sum_{w != z} d(L_zw || L^R_zw).

This is the intrinsic stationary physical-path-reversal divergence rate.
The full stationary path divergence is B+T sigma, where
B=D(rho||q). B need not be small or finite in continuous-state extensions.

For z!=w put

    f_zw = rho_z L_zw,
    g_zw = f_{theta w,theta z},
    F_zw = (f_zw+g_zw)/2,
    Lbar_zw = F_zw/mu_z.                              (1)

Choose the diagonal of Lbar by zero row sums.

**Theorem 1.** Lbar is irreducible, has stationary law mu, and its stationary
path law is invariant under theta followed by time reversal. For every T>=0,

    D(P_L^rho[0,T] || P_Lbar^mu[0,T])
       = JS(rho,q) + T I
       <= JS(rho,q) + T sigma/4
       <= log(2) + T sigma/4,                         (2)

where I=sum rho_z d(L_zw||Lbar_zw), summed over offdiagonal edges.
Both the one-bit boundary and the coefficient 1/4 are optimal as uniform
constants, separately.

Moreover for every stationary theta-reversible irreducible finite generator H
on the SAME state set and SAME theta, with stationary nu, there is an exact
Pythagorean identity

    D(P_L^rho || P_H^nu)
      = D(P_L^rho || P_Lbar^mu) + D(P_Lbar^mu || P_H^nu). (3)

All path intervals in (3) are [0,T]. Thus (1) gives the nearest such Markov
path law in forward KL, for every positive horizon. This is not an optimization
over unknown hidden realizations, alternative parities, or a prescribed thermal
Hamiltonian/bath class. It is an existence/geometry theorem with L,rho,theta
supplied. It does not acquire them from a coarse record.

### Proof: stationarity and physical reversibility

The edge flux f has equal incoming and outgoing sums. So does g, since g is
the theta-reversed transpose of f. Hence F is divergence free, and mu is
stationary for (1). F_zw=F_{theta w,theta z}, mu=muTheta. The outgoing F sum
at z equals the outgoing F sum at theta z by divergence balance. Consequently
Lbar has equal escape rates at theta-paired states. These statements imply
stationary physical path reversal invariance, including the holding factors.
Its support includes that of L, proving irreducibility.

### Proof: the scalar rate inequality

For any p,q>0 and a,b>0, set m=(pa+qb)/(p+q). Then

    p d(a||m)+q d(b||m)
       <= (p d(a||b)+q d(b||a))/4.                    (4)

Here is an ordinary one-variable proof, included rather than relying on an
unidentified divergence-inequality convention. Set s=pa+qb,
alpha=p/(p+q), r=pa/s, and ell(r)=log(r/(1-r)). The left side divided by s is
the Bernoulli KL D_B(r||alpha). The right numerator divided by s is

    J(r)=(2r-1)(ell(r)-ell(alpha))
          +(1-2alpha)(r-alpha)/(alpha(1-alpha)).

At r=alpha, J-4D_B and its derivative vanish, while

    (J-4D_B)''(r)=(2r-1)^2/[r^2(1-r)^2] >=0.

This proves (4); limits cover zero rates. The constant 1/4 is approached
when alpha=1/2 and a approaches b.

Apply (4) in each row with p=rho_z, q=q_z, a=L_zw, b=L^R_zw.
Then m=Lbar_zw. Stationary physical reversal is an involution, so the two
relative-entropy rates L versus L^R and L^R versus L are both sigma. Since
Lbar is reversal invariant, the rates from L and L^R to Lbar are both I.
Summation gives 2I <= (2sigma)/4. The path likelihood formula gives the
first equality in (2). Finally D(rho||mu)=D(q||mu)=JS(rho,q)<=log2.

### Proof: the exact projection identity

A stationary theta-reversible H has nu=nuTheta and theta-even escape rates.
Its stationary edge flux G_zw=nu_z H_zw has the same theta-transpose symmetry
as F. The difference between the two rate divergences on the left of (3) is

    sum f_zw log(Lbar_zw/H_zw)
      + sum_z rho_z (lambda_H(z)-lambda_Lbar(z)).

Write the logarithm as log(F_zw/G_zw)+log(nu_z/mu_z). The first term is
theta-transpose even, so its f average equals its F average. The second
is theta even, so balanced outgoing flux replaces rho_z lambda_L(z) by
mu_z lambda_Lbar(z). The escape term also has the same rho and mu averages.
The result is exactly the rate divergence from Lbar to H. The initial-law
identity D(rho||nu)=D(rho||mu)+D(mu||nu) follows because log(mu/nu) is even.
This proves (3). If a support mismatch causes infinity, use the extended
identity when meaningful, or restrict to finite cross divergences.

### Sharpness and interpretation

For Theta=identity and a nearly balanced biased ring, I/sigma tends to 1/4.
For the predecessor's slowly switching orientation lift, I tends to zero
with its switch rate, whereas JS tends to log2 as the orientation bias tends
to one. Thus a bound without any preparation term cannot hold uniformly.

The bounded JS term is neither the unbounded reversed-preparation KL B nor
an assigned physical work cost. The process and its reverse form a binary
statistical experiment; that is the origin of the one-bit ceiling. Lbar is
the local Markov projection of their equal path mixture. It is generally NOT
that mixture's full path law: the mixture retains a persistent orientation.

## 2. Local thermalization changes the preparation boundary

Let m be a reference probability invariant under Theta, Uu=u composed with
Theta, and E a closed symmetric conservative Dirichlet form commuting with U.
Suppose its reversal-odd spectral gap is lambda_odd>0:

    E(u,u) >= lambda_odd ||u||^2, whenever Uu=-u.

For rho=f^2 m, f>=0, ||f||=1, the odd part f_-=(f-Uf)/2 obeys

    2(1-A)=||f-Uf||^2 <= 4 E(f,f)/lambda_odd,
    A=int sqrt(d rho d rhoTheta).                     (5)

If the actual physical entropy/reversal rate satisfies sigma>=4E(f,f), then

    1-A <= sigma/(2lambda_odd),
    JS(rho,rhoTheta) <= 1-A <= sigma/(2lambda_odd).     (6)

For completeness JS<=1-A follows by comparing scalar f-divergences:
f_JS''(t)=1/[2t(1+t)] <= 1/(4t^(3/2))=f_H''(t),
with both functions and first derivatives zero at t=1.

Combining (2) and (6) gives a process-level bound

    D(P_L^rho[0,T] || P_Lbar^mu[0,T])
       <= sigma (T/4 + 1/(2lambda_odd)).              (7)

The right initial term can always be replaced by
min(log2,sigma/(2lambda_odd)). This controls the complete finite-window
path law and therefore every measurable coarse observation. It requires
no gap for even modes and no global hidden Dobrushin contraction.

This is a statement about the specific bath/reference form that controls
physical entropy. A freely chosen functional inequality detached from the
actual dynamics supplies no physical information. Necessity at the level of
the square-root inequality, native Langevin implementation, and counterexamples
to bounding B by E are developed independently in physical_frontier/.

## 3. Diffusion extension and its physical limitation

For smooth stationary diffusions with common diffusion matrix 2D, specified
linear parity Theta, and an absolutely continuous physical reversed process
with drift b^R, put q=rhoTheta and

    mu=(rho+q)/2,
    bbar=(rho b+q b^R)/(rho+q).                       (8)

Subject to well-posedness, integrability, and the Girsanov range condition,
this diffusion is stationary and physically reversible, and is the same
Markov projection of the forward/reverse mixture. Its stationary KL rate
satisfies I<=sigma/4. Indeed the sum of its two directional squared drift
costs is

    (1/4) int [rho q/(rho+q)] |b-b^R|^2_(D^-1),

whereas the sum of forward/reverse rate costs is

    (1/4) int (rho+q) |b-b^R|^2_(D^-1).

Use rho q/(rho+q)^2<=1/4 and equality of the two reversal-related rates.
For degenerate diffusions use the inverse on the diffusion range and require
drift differences to lie in that range. A formal Fokker--Planck calculation
alone does not certify existence/nonexplosion; these remain explicit analytic
conditions on this continuous-state extension.

For standard kinetic Langevin dq=M^-1 p dt, both b and b^R have exactly the
same position drift, so (8) preserves this kinematics and the noise covariance.
It generally introduces a momentum-dependent force and a non-Maxwell even
stationary density. Consequently it need not preserve the original physical
class 'velocity-independent force plus calibrated linear Maxwell friction'.
Equation (7) then supplies proximity to a reversible path model in the broader
specified-parity kinetic class, NOT a native same-bath equilibrium realization.
No thermodynamic interpretation of the surrogate's drift is silently added.

## 4. Consequence and next hard obligation

If a model class has a warranted common positive lambda_odd and the above
rate/form domination, every sequence with sigma tending to zero approaches
stationary physically reversible path models on every finite time window.
The orientation obstruction is excluded because maintaining a parity-biased
stationary preparation now consumes rate in the locally thermalized odd modes.
Arbitrarily slow even configurational memory is allowed.

For an even coarse readout and observable path reversal TV Delta_T,
Pinsker and reversal invariance of the surrogate give

    Delta_T <= 2 TV(P_obs,Pbar_obs)
             <= sqrt(2 sigma [T/4+1/(2lambda_odd)]).

This corollary is only a consequence; it is not the main scientific target.
The stronger content is the exact projection and the complete-path stability
mechanism with the required physical information exposed.

The next genuine obstruction is whether, and under which additional physical
conditions, the nearby reversible path model can be chosen inside the SAME
calibrated thermal source class. Small entropy controls momentum Fisher
information but does not directly control the spatial force mismatch to a
Gibbs surrogate. This was the open step at the original reviewed version.
It is now resolved in three different, precisely scoped directions:
THERMAL_STABILITY_DEPENDS_ON_OBSERVATIONAL_RESOLUTION.md gives a native
counterexample to unrestricted strong path approximation;
physical_frontier/NATIVE_EQUILIBRIUM_TOPOLOGY_OBSTRUCTION.md supplies full
path-TV closure under both amplitude and Lipschitz caps; and
BOUNDED_FORCE_FINITE_RESOLUTION_EQUILIBRIUM.md removes the Lipschitz cap for
weak and fixed-resolution record laws. GENERAL_THERMAL_MEMORY_METRICS.md
gives an exact, acquired-record route in a separately specified one-way class.
None of these physical gates is inferred from a fit.

## 5. Antecedents and scope of addition

Ordinary additive reversibilization and its information projection are known:
Wolfer--Watanabe, Information Geometry 4 (2021), 393--433,
doi:10.1007/s41884-021-00061-7. Standard convex divergence inequalities,
Gaussian Poincare, Girsanov, and the momentum-current entropy formula are
ingredients, not claimed discoveries. Kim--Lee--Jeong (2022) and
Degunther--van der Meer--Seifert (2024) already explain the odd-parity boundary.
The proposed assembly is the arbitrary-parity, parity-asymmetric stationary
projection with its exact finite-horizon identity and one-bit boundary,
combined with local reversal-sector thermal coercivity. Priority is not
established. A strong equally informed optimizer may improve particular
entropy lower bounds; no algorithmic or experimental advantage is claimed.
