# Universal attainable-spectrum design theorem for a passive phonon backbone

Status: owned internal mathematical construction; root whole-proof review found no substantive gap. Version2 clarifies zero coefficients in the root-count argument; the original6092 proof remains preserved unchanged. Earlier governing proof99f7440a and all prior certificates are preserved unchanged. This file generalizes its single engineered point. Historical novelty, material realization and mission-level physical capability remain unestablished.

## 1. Physical model and exact output

Fix K>0, total unit-cell mass M, a positive backbone-mass lower bound m0 with0<m0<M, and finite theta=k_B T/hbar>0. A finite passive connected internal network of positive scalar point masses and positive springs attaches within each cell to one backbone coordinate of mass m>=m0. The only intercell link connects that coordinate to its counterpart in adjacent cells with spring K. Internal topology, number of nodes, stiffnesses, and dark modes are otherwise unrestricted.

Mass normalization gives
D(q)=D0+4K sin^2(q/2) vv^T,
D0>=0 with exactly one rigid-translation nullmode,
||v||^2=1/m, and squared overlap of v with that normalized nullmode=1/M.

The output is full ideal-contact harmonic BALLISTIC thermal conductance, including every acoustic and optical pass band. Apart from k_B/(2pi),
J_theta(chi)=integral_0^infinity g_theta(w) chi(w)dw,
g_theta(w)=[w/(2theta)/sinh(w/(2theta))]^2.
It is a strictly positive, strictly decreasing function of w>0, equals1 at zero, and decays exponentially at infinity.

No full3D conductivity, electronic power factor, contact transport, finite-modulus fabrication or anharmonic material operation is supplied.

## 2. Main theorem

For EVERY such quadruple(K,M,m0,theta), the conductance minimum over ALL finite internal passive networks and all allocations m>=m0 is attained by a cell with:
- backbone mass exactly m0;
- ONE side mass M-m0;
- ONE finite positive internal spring k_*.

Its full passband spectrum and active driving-point response are unique. Distinct isospectral networks or additional dark modes can represent the same response, so physical topology is not asserted unique.

The unique internal spring is found from one scalar stationarity equation below. Its construction does not require an unconstrained indicator relaxation to be physically realizable. It uses exactly the two positive masses and two spring types displayed above.

## 3. Exact necessary spectral resources

Let alpha_j and beta_j be the ordered eigenvalues of D0 and D0+4Kvv^T. Rank-one interlacing makes the passbands
[sqrt(alpha_j),sqrt(beta_j)]
disjoint in their interiors. Alpha_0=0; zero-width dark intervals can be cancelled.

For every admitted finite network:
T(chi)=integral 2w chi(w)dw=4K/m;
L(chi)=integral [chi(w)-1_[0,Omega](w)]/w dw=0,
Omega=2sqrt(K/M).

The trace gives T. The determinant lemma gives
prod(t+beta_j)/prod(t+alpha_j)
=1+4K v^T(D0+tI)^(-1)v,
whose t→0 residue is4K/(M t). Consequently
prod beta_j/prod_(j>0)alpha_j=4K/M=Omega^2,
equivalent to L. These are identities of the full spectrum.

The classical total-bandwidth lower bound remains
integral chi(w)dw>=Omega,
with equality approached by rigidly binding the full mass M. The finite-temperature theorem below does not violate it.

## 4. An explicit attainable curve for ANY resources

Define
A=4K/m0, B=4K/M, so A>B>0.

Use r>0 for the q=0 optical frequency of a one-side-mass cell. Let
Delta(r)=sqrt[(r^2+A)^2-4Br^2],
p(r)^2=[r^2+A-Delta]/2,
s(r)^2=[r^2+A+Delta]/2.

Then0<p(r)<r<s(r), and its passbands are
[0,p(r)] union [r,s(r)].
They satisfy
p^2+s^2-r^2=A,
p^2 s^2/r^2=B.

They are physically realized by
m=m0, M_side=M-m0,
k(r)=r^2 m0(M-m0)/M.
Indeed the internal two-mass matrix has eigenvalues0,r^2, while adding4Kvv^T changes its trace to p^2+s^2 and determinant to p^2s^2.

Thus the entire r-curve is an actual positive passive network family.

Write
j(r)=integral_0^p(r) g_theta(w)dw
     +integral_r^s(r) g_theta(w)dw.

All endpoints are smooth for r>0. If t=r^2 and d=Delta,
d(p^2)/dt=(B-p^2)/d>0,
d(s^2)/dt=(s^2-B)/d>0.
In particular p'(r)>0 and s'(r)>0.

## 5. A finite interior global minimum exists

At r→0,
p~r sqrt(B/A), s→sqrt(A),
so j(r)→integral_0^sqrt(A)g_theta
> integral_0^sqrt(B)g_theta=J_rigid.

At r→infinity,
p^2=B-B(A-B)/r^2+O(r^-4),
p=sqrt(B)-sqrt(B)(A-B)/(2r^2)+O(r^-4),
s=r+(A-B)/(2r)+O(r^-3).

The missing acoustic tail gives
integral_p^sqrt(B)g_theta
=g_theta(sqrt(B))sqrt(B)(A-B)/(2r^2)+O(r^-4).
The compensating optical contribution is at most
(s-r)g_theta(r)=O(r exp[-r/theta])=o(r^-2).
Therefore
j(r)-J_rigid
=-g_theta(sqrt(B))sqrt(B)(A-B)/(2r^2)+o(r^-2)<0
for all sufficiently large finite r.

A continuous function with a limit above J_rigid at zero, limit J_rigid at infinity, and a finite value strictly below J_rigid attains a global minimum at some finite r_*>0. This establishes existence without any temperature sweep or unconstrained-spectrum compactness assumption. It also proves a strict rigid-chain advantage at every finite theta, though the size can become arbitrarily small near limits.

## 6. Every stationary member supplies a three-root dual

At any stationary r, abbreviate its endpoints by p<r<s and define
h(w)=w g_theta(w),
F(w)=h(w)+lambda+2mu w^2.

Choose the unique lambda,mu with F(p)=F(r)=0:
2mu=[h(p)-h(r)]/(r^2-p^2),
lambda=-h(p)-2mu p^2.

Differentiate both fixed spectral moments along the attainable r-curve:
p'/p+s'/s-1/r=0,
2p p'+2s s'-2r=0.

Hence
0=j'(r)+lambda L'(r)+mu T'(r)
  =[F(p)/p]p'+[F(s)/s]s'-F(r)/r
  =[F(s)/s]s'.
Since s'>0, stationarity forces F(s)=0. The dual therefore has THREE distinct positive roots p,r,s.

## 7. Three roots force the correct dual signs

The following elementary cases exclude all other quadrants.

If lambda>=0 and mu>=0, F(w)>0.

If lambda>=0 and mu<0, then
F(w)/w^2=g_theta(w)/w+lambda/w^2+2mu
is strictly decreasing on w>0, so it has at most one positive root.

If lambda<0 and mu<=0, put x=w/(2theta),
L=lambda/(2theta)<0, P=4mu theta<=0.
The positive-root-equivalent entire function is
Q(x)=[F(2theta x)/(2theta)]sinh^2(x)/x^2
=L+x+sum_(n>=1)c_n[P+4L/((2n+2)(2n+1))]x^(2n),
c_n=2^(2n-1)/(2n)!.
Every even coefficient is negative, hence Q''<0. Rolle's theorem gives at most two positive roots.

Thus THREE positive roots necessarily imply
lambda<0, mu>0.

## 8. Universal all-frequency root bound in the proper quadrant

For lambda<0,mu>0, the bracket
P+4L/((2n+2)(2n+1))
increases strictly with n and tends to P>0. Its signs can change at most once from negative to positive.

If ALL coefficients of Q'' are NONNEGATIVE, then Q''>0 on x>0 and it has no positive zero (there are strictly positive tail coefficients). Otherwise let e be the exponent of the first STRICTLY POSITIVE term in Q'', ignoring zero coefficients. Divide Q'' by x^e. Every negative coefficient is at a power below e and therefore acquires a negative exponent; its derivative is positive. Positive terms have nonnegative exponents and nonnegative derivatives. Because at least one negative term exists in this case, the resulting derivative is strictly positive. Thus Q''/x^e is strictly increasing and has at most one positive zero.

Uniform convergence on every positive compact interval justifies differentiating the entire series termwise. Therefore Q'' has at most one positive zero, Q' at most two, and Q at most THREE. An extra multiplicity at one of three distinct roots would create too many derivative zeros, so all three are simple.

Because F is negative at zero and positive at infinity, the stationary curve member has exactly the global sign pattern
F<0 on(0,p) union(r,s),
F>0 on(p,r) union(s,infinity).

This step is analytic over the whole frequency axis; it does not rely on a frequency grid.

## 9. Global optimum over every internal network

Let chi_* be a stationary curve member's actual two-band spectrum and define
R(w)=g_theta(w)+lambda/w+2mu w=F(w)/w.

Its indicator is exactly1 where R<0 and0 where R>0. For ANY admitted finite network chi,
integral R(w)[chi(w)-chi_*(w)]dw>=0
pointwise.

The log moments cancel. The trace moment of a competitor with m>=m0 is no larger than the candidate's:
T(chi)-T(chi_*)=4K/m-4K/m0<=0.
Thus
J_theta(chi)-J_theta(chi_*)
=integral R(chi-chi_*)dw
 -mu[4K/m-4K/m0]
>=0.

The apparent1/w singularity causes no problem: both finite connected spectra have a nonzero acoustic interval, so their indicator difference vanishes near zero; they also have bounded frequency support.

The finite minimum from Section5 is stationary, hence this dual proves it globally optimal over every passive internal topology, every finite number of resonators and every permitted backbone-mass allocation.

Equality forces m=m0 and the same passbands except sets of measure zero. Two different r values have different optical starts and cannot have the same spectrum. Consequently the stationary point r_* is unique, its spring k_* is unique, and the active scalar response is unique. Arbitrary dark-mode/isomorphic realizations are still possible.

## 10. An analytic global inverse design map

At fixed theta, consider ANY proper dual pair(lambda<0,mu>0) with three simple roots x_1<x_2<x_3. Define
ell=ln x_1+ln x_3-ln x_2,
A=x_1^2+x_3^2-x_2^2.
Then B=exp(2ell) and A>B>0.

With endpoint signs epsilon=(+1,-1,+1),
dx=-(d lambda+2x^2d mu)/F'(x).
Put u_x=(1/x,2x)^T. The Jacobian is exactly
D_(lambda,mu)(ell,A)
=-sum_(x=x1,x2,x3)[epsilon_x x/F'(x)]u_x u_x^T.

All weights are positive by the alternating signs, and distinct x give linearly independent u_x. The Jacobian is therefore symmetric STRICTLY NEGATIVE DEFINITE. It is nonsingular everywhere in the three-root region.

Sections4–9 show this moment map reaches EVERY A>B>0. Strict dual equality makes it injective: two pairs with the same resources have the same unique optimal spectrum, and two distinct quadratics lambda+2mu w^2 cannot agree at three distinct positive roots. The local inverse theorem therefore upgrades the map to a global analytic bijection onto
{(ell,A): A>exp(2ell)>0}.

This is a complete structural family, not an isolated point or a collection of temperature runs. The desired(K,M,m0,theta) determine a unique dual and a unique attainable one-resonator optimum.

## 11. Constructive scalar algorithm and actual resources

Given K,M,m0,theta:
1. Compute A=4K/m0 and B=4K/M.
2. For any trial r>0 compute s^2 from the plus quadratic root and p^2=B r^2/s^2 (the latter avoids subtraction cancellation).
3. Evaluate the derivative WITHOUT numerical quadrature:
j'(r)=g_theta(p) r(B-p^2)/(p Delta)
     +g_theta(s) r(s^2-B)/(s Delta)
     -g_theta(r).
4. Bracket its unique zero and bisect with certified function evaluations. The derivative is negative before the zero and positive after it because there is exactly one stationary point and it is the strict global minimum.
5. Return backbone m0, side mass M-m0, external spring K and internal spring
k_*=r_*^2 m0(M-m0)/M.

All mathematical components are finite and positive at every finite nondegenerate resource tuple. Exact algebraic formulas define the attainable spectra once r_* is specified; transcendental root-finding precision must be paid. Scalar evaluation/bisection avoids any internal-topology search. No uniform conditioning bound is asserted near M=m0, theta limits, narrow spectral gaps or extreme stiffness ratios.

The allowed internal stiffness is not free in a real material: k_* is an explicit output cost. If a fabrication/stiffness/strain or frequency cap excludes it, this unconstrained theorem supplies a lower benchmark but does not solve that modified design problem.

## 12. Complete inverse realization of arbitrary finite spectra

This second result makes the finite attainable-spectrum language exact. It is classical Foster/Stieltjes-type passive network synthesis specialized to this bulk-band problem, not asserted as a new synthesis principle.

Let a prescribed strict squared-endpoint list obey
alpha0=0<beta0<alpha1<beta1<...<alpha_(n-1)<beta_(n-1).
Fix S=4K>0 and form
q(t)=[prod_j(t+beta_j)/prod_j(t+alpha_j)-1]/S.

At each pole -alpha_j its residue is
c_j=prod_l(beta_l-alpha_j)/
     [S prod_(l!=j)(alpha_l-alpha_j)]>0.
Numerator and denominator each have exactly j negative factors. Thus
q(t)=sum_j c_j/(t+alpha_j)
is a positive Stieltjes sum. Its limits give
sum c_j=1/m=(sum beta-sum alpha)/S,
c0=1/M=prod beta/[S prod_(j>0)alpha].

q has exactly one simple zero -sigma_j between each pair of successive poles:
alpha_(j-1)<sigma_j<alpha_j.
Its derivative is negative away from poles. Therefore
1/[tq(t)]=m+sum_j rho_j/(t+sigma_j),
rho_j=1/[-sigma_j q'(-sigma_j)]>0.

Build an actual star:
backbone mass m;
side mass m_j=rho_j/sigma_j;
spring k_j=rho_j.
Because1/[tq(t)] at zero is M,
sum_j m_j=M-m.
Eliminating these side coordinates gives exactly q(t). Every pole is visible and the star has exactly n degrees of freedom; the determinant lemma then reproduces the desired alpha and beta, hence the complete desired passbands.

Consequently, among finite strict passband unions, the trace/log constraints plus their implied positive m,M are SUFFICIENT as well as necessary. No more general connected internal topology creates additional active scalar band spectra beyond a positive star. Touching/zero-width intervals can be simplified by cancelling common endpoint factors; dark modes are not inferred from an active scalar spectrum.

## 13. Precision and physical costs

For n desired bands, the minimal active star uses n-1 side masses/springs. Residue products are explicit. Its n-1 simple zeros have known interlacing brackets; algebraic root isolation or certified bisection gives finite-precision parts. Narrow pole/zero gaps can require high precision, very small branch masses or high frequencies; neither robustness nor material affordability is implied.

The star also preserves the backbone incident internal stiffness. If
E=sum(beta_j^2-alpha_j^2), A_band=sum(beta_j-alpha_j), S=4K,
its total star spring constant is
sum_j k_j = S[E-A_band^2]/(2 A_band^2).
This follows by expanding q(t) at infinity. For any original positive-spring network the same quantity is its backbone incident stiffness; other internal edges can add further spring cost. For the universal optimum it equals the explicit k_* above.

These are ideal point-mass/spring costs. Connector mass, finite specific modulus, extra polarizations, geometry, anharmonicity and actual contact transport remain separately owned interface questions. No equipment action, specimen or measurement was acquired here.

## 14. Prior-art boundary

Positive alternating-pole/zero network realization is classical Foster/Cauer/Stieltjes synthesis. Foster's1924 primary theorem explicitly addresses finite lossless reactance networks and uses a frictionless mechanical-oscillation analogue; inverse two-spectrum Jacobi/spring-mass reconstruction is also established, including Nylen–Uhlig1997.

The mathematical candidate under examination is the specialized UNIVERSAL full-Bose minimizer, its proper-quadrant/root-count proof and analytic resource inverse in this precise single-backbone mass/stiffness contract. A bounded search has found no directly matching thermal extremal theorem; this is not novelty clearance. The framework must not be described as the first passive resonator, first local-resonance insulator, or new invention of passive network synthesis.

Primary sources and their access limits are retained in sources_support/PHONON_FAMILY_PRIOR.md. The proof above is self-contained and does not rely on an inaccessible source theorem as a premise.

