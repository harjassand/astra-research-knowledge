# Full-fiber conductance without the internal partition function

Status: constructed and author-tested; independent whole review pending. This is
an abstract diffusion theorem and executable sufficient input grammar. It is not
an originality, universal complexity, physical application or MFPT claim.

## 1. Actual task, inputs and acquired structure

Input is the complete rational coefficient dictionary of a polynomial F on the
actual Euclidean R^(m+1), m>=2. No coordinate, decomposition, graph, sampler or
partition function is supplied. The current consumer accepts exactly an aligned
sufficient family, finding a physical coordinate y and verifying every coefficient:

    F(y,z) = v(y) U(z),       v(y)=1+kappa(1-y^2)^2, kappa>0,
    U(z)=sum_i d_i z_i^4 + sum_(i<j) J_ij z_i^2 z_j^2,
    d_i>0, J_ij>=0.

Omitted couplings mean zero. The lowest degree-four part is (1+kappa)U. All fiber
coordinates occur in positive z_i^4 terms, so exactly one coordinate is absent:
y. A top/base coefficient ratio t=kappa/(1+kappa) acquires kappa=t/(1-t).
The consumer checks 0<t<1, every monomial/sign of U, all positive diagonals, then
the ENTIRE degree 4/6/8 dictionary F=vU. It does not merely recognize a few terms.
The unknown generic rotated grammar returns UNKNOWN, not a Euclidean transform
with uncharged metric. Permutations and a nonfirst y axis are accepted.

Set d_min=min_i d_i. The identity

    m sum_i z_i^4 - (sum_i z_i^2)^2
      = sum_(i<j) (z_i^2-z_j^2)^2

certifies U >= (d_min/m)||z||^4. Neither convexity nor a mixing hypothesis is used.
For example U=x^4+y^4+20x^2y^2 has Hessian eigenvalue 12-40<0 at (1,1).

The process is the ACTUAL isotropic diffusion

    dX_t=-grad F(X_t)dt+sqrt(2/beta)dW_t, beta>0.

Basins A={y<=-1/2}, B={y>=1/2} contain whole fibers and are acquired FROM this
grammar; they are not arbitrary user-selected basins. The observable is the
reversible capacity divided by equilibrium basin mass, cap_mu(A,B)/mu(A).
It is not an arbitrary-state expected first-hit time, a finite-time crossing
probability, angular relaxation time, or a Markov model for the projected y_t.
Indeed the actual y drift -v'(y)U(z) depends on z.

## 2. Scaling cancels an unknown angular partition constant

More generally let U be positive homogeneous degree p>=2 with U>=a||z||^p.
Its partition constant Z_U=integral exp(-U(z))dz is finite. Exact scaling gives

    integral exp[-beta v(y)U(z)]dz = (beta v(y))^(-m/p) Z_U.

Thus take q(y)=v(y)^(-m/p), Q=integral_R q(y)dy and the conditional density rho_y.
The joint probability density is q(y)rho_y(z)/Q. Neither Z_U nor any angular
integral is needed by the algorithm. Z_U cancels in this normalized marginal and
in the capacity/mass ratio. This is a proof, not a partition oracle.

The exact conditional continuity field is w_y(z)=-(v'(y)/(p v(y)))z. Indeed
partial_y log rho=(m/p)v'/v-beta v'U, div w=-(m/p)v'/v, and
w.grad_z log rho=(beta v'/p)z.grad U=beta v'U by Euler homogeneity. Their sum is 0.
The density/current is an analytical object, not something the algorithm samples
or evaluates in high dimension.

Integration by parts, justified by coercive polynomial tails, or differentiation
of the scaling identity gives E_y U=m/(p beta v). Hence Jensen and coercivity give

    E_y||z||^2 <= [m/(p beta a v)]^(2/p),
    K(y):=E_y||w_y||^2
      <= m^(2/p) v'^2/[p^(2+2/p)(beta a)^(2/p)v^(2+2/p)].       (1)

Angular nonconvexity, correlations, interaction strength and conditional mixing
do not appear in this valid moment bound. They are not being assumed small.

## 3. Conditional transport controls the FULL Dirichlet capacity

For an admissible smooth h=1 on A and 0 on B, put hbar(y)=E_y h(y,z). Continuity
and integration by parts imply

    hbar'=E_y[partial_y h+w_y.grad_z h].

Cauchy-Schwarz yields

    E_y(|partial_y h|^2+||grad_z h||^2) >= hbar'^2/(1+K(y)).

The one-dimensional weighted Cauchy inequality, with hbar(-b)=1,hbar(b)=0,
gives full Dirichlet energy >=1/(beta Q R1), where b=1/2 and

    R0=integral_-b^b 1/q,    R1=integral_-b^b (1+K)/q.

The trial h depending only on y and h' proportional1/q gives the upper capacity
bound 1/(beta Q R0). These statements extend from the smooth admissible core by
weighted Sobolev approximation (or equivalently use the unit current
J=(rho,rho w) on the slab, whose divergence is 0 and dual energy is R1).
The fiber boundary terms vanish by coercivity and finite polynomial moments;
there is no reflecting fiber truncation. Since q is globally even,
mu(A)=MA/Q with MA=integral_b^infinity q. Therefore

    1/(beta MA R1) <= cap_mu(A,B)/mu(A) <= 1/(beta MA R0).      (2)

If global evenness is absent the actual left basin mass must replace MA. The
present family is globally even, not merely even inside the slab.

## 4. Dimension-free quartic resistance bound, with no f' overestimate

Write W=1/q=v^(m/p), s=1+2/p and

    C_m=m^(2/p-1)/[p^(1+2/p)(beta a)^(2/p)],
    v_min=1+9 kappa/16.

On 0<=y<=b, -v'=4kappa y(1-y^2)>=0, v>=v_min and
-W'/W=(m/p)(-v'/v). Equation (1) gives, including its continuous endpoint at 0,

    K W <= C_m (-v')v^(-s)(-W')
        <= [4kappa C_m/v_min^s] y(-W').

The crucial sign is -W'>=0. Integration by parts retains the negative boundary:

    integral_0^b y(-W') = -bW(b)+integral_0^b W <= integral_0^b W.

Evenness gives R1<=(1+4kappa C_m/v_min^s)R0. For p=4 and the acquired
a=d_min/m, C_m=1/[8 sqrt(beta d_min)], exactly independent of dimension.
Combining with (2), define

    k_free=1/(beta MA R0),
    C=1+kappa/[2 sqrt(beta d_min) v_min^(3/2)].

Then

    k_free/C <= cap_mu(A,B)/mu(A) <= k_free.                 (3)

For beta=d_min=kappa=1, v_min=25/16 and C=157/125 exactly. The earlier root
candidate in sources/ used a valid but looser bound through f'; it is preserved
unaltered. This direct comparison replaces that step, not the task or model.

## 5. A consequence: rate-insensitivity to unknown angular interactions

Fix m, beta=kappa=1, and impose d_i>=1. Every admitted nonnegative interaction
graph and every finite choice of its weights has the SAME q and k_free. Every
full conductance lies in [125 k_free/157,k_free], even if the graph, diagonal
coefficients and unknown Z_U differ. Therefore any two such conductances differ
by at most 157/125. Input checks still have to be paid for each changed model.

This does not assert identical full conductances or that the unknown partition
functions are hard. It identifies microscopic details that cannot materially
change this specified equilibrium full-fiber observable, within a proved factor.
It says nothing about changing interactions in time, angular relaxation,
nonequilibrium preparation, arbitrary-start hitting times or restricted basins.

## 6. Global process, finite Gibbs law and explicit unbounded tail

For y>=T>1, v(y)>=kappa y^4(1-T^-2)^2, so for p=4

    integral_T^infinity q
      <= kappa^(-m/4)(1-T^-2)^(-m/2) T^(1-m)/(m-1).         (4)

This is finite for m>1, exactly the implemented dimension requirement. Coercivity
makes each fiber partition finite, hence the full Gibbs law is normalizable.
For nonexplosion take V=1+y^2+K0||z||^2 with K0=1+kappa/p. Then

    grad V.grad F=2[yv'+K0 p v]U,
    yv'=4kappa y^2(y^2-1)>=-kappa, v>=1,
    LV<=2(1+K0m)/beta.

A stopped Lyapunov argument with V coercive and smooth local coefficients proves
nonexplosion. Integration by parts and the finite Gibbs law yield the conservative
reversible diffusion used in(2). No global Lipschitz drift or barrier crossing
simulation is assumed. The quartic zero locus z=0 at large y does not invalidate
this argument: it has finite total Gibbs mass by the explicitly charged fibers.

## 7. Exact scalar execution and receiving

At rational y, v^m is rational. q^4=v^-m and W^4=v^m. For any rational a>=0,

    k=floor_root4(floor(2^(4P) a))

satisfies k/2^P <= a^(1/4) <=(k+1)/2^P, with equality of endpoints detected by
k^4 den(a)=2^(4P)num(a). floor_root4 is isqrt(isqrt(integer)); it is exact.
The same construction with one isqrt provides the square-root factor bound.
Perfect rational squares use their exact rational roots, hence157/125 is exact.

q is increasing on[1/2,1], decreasing on[1,infinity], and W decreasing on[0,1/2].
Endpoint minima/maxima give outward Darboux bounds. Tail pieces[1,2],[2,4],...,
[T/2,T] each have N uniform cells, avoiding an unnecessarily uniform mesh over a
long tail when m=2. Equation(4) is added only to the upper mass endpoint.
A positive certified seed on[1,5/4] sets the paid tail cutoff. Failure to resolve
the seed is UNKNOWN, not an infinite loop. T and N double under explicit caps;
point cache caps total distinct points across all attempted grids.

Admission requires positive lower mass/resistance and

    M_upper R_upper <=(1+delta) M_lower R_lower.

Thus the output exact rational interval is

    [1/(beta M_upper R_upper C_upper),
     1/(beta M_lower R_lower)],

where C_upper is a rigorously rounded upper bound on C. In the unit parameters,
its width ratio is <=(157/125)(1+delta), however small the rate.

The receiver takes ORIGINAL raw input plus external beta/tolerance/budgets,
reacquires every identity and reruns the bounded exact calculation. It strictly
binds types recursively, including nested graph data, all task fields, basin and
observable, factor/tail/grid/precision and every exact interval endpoint.
Optional timings, float displays and diagnostic operation counts are not proof
fields. They cannot change an admitted exact interval. Float overflow/underflow
is represented by null; excessive exact serialization becomes UNKNOWN.
This is sound but incomplete receiving, not a proof assistant or a general
positive-quartic solver. All source hashes are separately frozen for review.
