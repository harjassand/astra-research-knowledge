# Reversible random scenery: full preparation and finite-precision cost

29 October 2026. Astra P1, existing record-geometry complementary role.
This is independent of root's directed-shift/baker preparation proof.

## 1. A stationary reversible microscopic source

Let X={−1,+1}^Z, with product fair-sign measure mu. Write omega_k for the
kth microscopic coordinate and let theta translate the scenery by one site.
The actual native kernel is

    P=(theta+theta^(−1))/2.

At each native call the entire scenery is translated by one independent
fair random-walk step. The controller sees Y(omega)=omega_0. The product
law is stationary; theta's adjoint is its inverse, so P is reversible.
The source is ergodic under mu: a P-invariant square-integrable function
has zero Dirichlet energy, hence is shift invariant, and the Bernoulli
shift is ergodic. There is no positive-mass conserved-sector mismatch.

Take the nontrivial positive target

    nu(domega)=(1+a omega_0)mu(domega),  0<|a|<1.

The full scenery is the microscopic state. Selecting the correct current
sign alone is not enough to prepare this law, because all other coordinates
must retain the corresponding product conditional distribution.

## 2. No finite-mean exact stopped-current-state preparation

This assertion holds even if the controller knows P and sees the complete
scenery, provided its only state-changing action is another P call and its
output is the current physical state. Arbitrary independent randomization
and zero-call stopping branches are allowed.

Suppose X_0~mu, tau is almost surely finite, E tau=C<infinity, and X_tau
has target law nu. Extend the native Markov path after stopping if needed.
Every fixed-time state still has law mu. The finite pre-stop occupation
measure

    Lambda(A)=E sum_(j=0)^(tau−1) 1_{X_j in A}

is absolutely continuous relative to mu and has mass C. Write Lambda=u mu,
where u>=0 and u is integrable. The stopped occupation equation gives

    Lambda P−Lambda=nu−mu,
    (I−P)u=−a omega_0.                              (1)

For k in Z, set c_k=mu(u omega_k). Integrability gives |c_k|<=C. Pairing
(1) with omega_k and using reversibility and independent centered signs,

    c_k−(c_(k−1)+c_(k+1))/2=−a 1_{k=0}.             (2)

Away from zero, c_k is affine on each half-line. Boundedness forces it to
be constant on each half-line. The equations at k=1 and k=−1 identify both
constants with c_0, making the left side of (2) at zero equal to zero. This
contradicts a!=0.

Thus no such exact preparation can have finite mean native-call count.
This conclusion is about the actual stopped endpoint, not an estimator or
a two-sided-path independence demand. It already holds with a known kernel
and full state observations. The four-state theorem in the adjacent file
is a separate, stronger universality obstruction under rapidly mixing
finite hidden memory and only visible observations.

## 3. A finite-precision lower bound of order epsilon^(−2)

Suppose now that tau has finite mean C and its endpoint law rho satisfies
TV(rho,nu)<=epsilon. Write J for the net spatial displacement of the scenery
at the stopping time. The underlying spatial steps are independent fair
signs even conditional on the initial scenery and controller seed. The
stopped random-walk martingale isometry therefore gives

    E J²=E tau=C,       E|J|<=sqrt(C).               (3)

The isometry is valid without a second moment of tau: the stopped sums are
Cauchy in L2, with squared tail norm E[(tau−N)_+], which tends to zero.

Here is the required mass-transport bound, stated with its full proof. Run
the same relative-coordinate controller from every integer origin of a
fixed scenery, averaging over its independent random seed and walk. Let
t_omega(i,j) be its probability of stopping at absolute site j when started
at i. This is a translation-covariant random transport with row masses one.
Stationarity shows that the density h=d rho/d mu is its incoming column
mass at zero. Indeed, shifting the integral for each possible displacement
turns E[f(X_tau)] into mu[f(omega) sum_i t_omega(i,0)].

For a block I of n consecutive sites, total incoming minus outgoing mass
equals sum_(j in I)(h(theta^j omega)−1). Internal transport cancels. Its
absolute expectation is at most the expected mass crossing the boundary
in either direction. Stationarity gives

    expected outgoing mass = E min(n,|J|),
    expected incoming mass = E min(n,|J|).

For a fixed displacement j, exactly min(n,|j|) starting sites in the block
are carried outside; the same counting identity applies to incoming sites.
All sums are justified by nonnegativity and finite expected incoming mass.
Consequently

    E|sum_(j=1)^n (h(theta^j omega)−1)|
       <= 2 E min(n,|J|) <= 2 sqrt(C).              (4)

Let S_n be a sum of n iid fair signs. Because mu|h−(1+a omega_0)|<=2epsilon,
the triangle inequality applied to (4) proves the exact finite-n constraint

    2 sqrt(C)+2n epsilon >= |a| E|S_n|,  n>=1.       (5)

Equivalently,

    C >= (1/4) sup_(n>=1) [|a|E|S_n|−2n epsilon]_+². (6)

This is an explicit bound without an unspecified asymptotic constant.
For n=2m,

    E|S_(2m)|=2m binom(2m,m)/4^m.

Using its asymptotic sqrt(2n/pi) and choosing n near a²/(8pi epsilon²)
gives, as epsilon decreases to zero,

    C >= (1−o(1)) a^4/(64 pi² epsilon²).             (7)

Equation (7) is a lower bound only. No matching reversible-scene upper
bound or practical advantage is established here. It is stronger than the
directed-shift cost lower bound because native random-walk displacement is
diffusive: sqrt(C), rather than C, bounds its mean absolute displacement.
The controller can know the entire scenery and still cannot bypass (5).

The cost is native calls. Physical-time conclusions require an actual
duration per call. A hypothetical ability to command a chosen spatial
direction, teleport to a matching site, restore an earlier state, or output
a stored state changes the operation interface and does not fall under
this theorem.

## 4. Scope and ordinary alternatives

This source is an infinite-dimensional reversible environment process. Its
states have conserved translation orbits of zero mu mass; ergodicity above
does not claim Harris irreducibility. The four-state theorem avoids this
potential distraction and is the main universality result.

The argument in Section 2 uses the classical occupation identity. Section 3
uses the usual stationary mass-transport bookkeeping and the stopped
random-walk isometry; their application to full microscopic preparation is
derived here. Extra-head and unbiased-shift primary predecessors are listed
separately. No novelty claim is inferred from deriving these equations.

Root's measure-preserving baker representation is a possible way to express
a reversible mixture of forward and inverse shifts on a smaller coordinate
space, if both directions are part of the actual native source. Its physical
receiver assumptions remain separate; no such apparatus is asserted here.
