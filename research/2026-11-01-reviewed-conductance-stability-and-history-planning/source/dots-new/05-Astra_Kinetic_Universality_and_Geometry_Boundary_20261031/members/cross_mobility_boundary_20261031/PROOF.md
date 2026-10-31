# Cross mobility can destroy a fixed-potential capacity guarantee

Status: independently reviewed PASS, exact receiver and replay PASS. Date: 2026-10-31.
No older source or consumer freeze is modified. All coordinates are the fixed
physical Euclidean coordinates (y,z); this is not a coordinate relabeling.

## Statement

Let

    v(y)=1+(1-y^2)^2=y^4-2y^2+2,   F(y,z)=v(y)z^2/2,
    A={y<=-1/2}, B={y>=1/2},       beta=1,
    Z=integral_R2 exp(-F),         mu=Z^-1 exp(-F) dy dz.

For each integer k>=1 and rational 0<epsilon<1, receive the actual constant SPD
matrix

    D=[[1,k],[k,k^2/(1-epsilon)]].

The conservative reversible diffusion with generator

    Lf=mu^-1 div(mu D grad f)
      =tr(D Hess f)-(D grad F).grad f

exists for every initial point, has invariant probability mu, and has the same
macroscopic diffusion entry D_yy=1 for every member. Its normalized Dirichlet
capacity and capacity/mass conductance satisfy

    max{epsilon/16, exp(-k^2/2)/16}
      < cap_mu,D(A,B)
      <=36 epsilon + (1200/k) exp(-k^2/128),                  (1)

    0 < cap_mu,D(A,B)/mu(A)
      <=144 epsilon + (4800/k) exp(-k^2/128).                (2)

Strict lower inequalities may freely be weakened to non-strict ones in a finite
certificate. In particular epsilon=1/n,k=n (n>=2) is an entirely rational,
explicit family with capacity and conductance tending to zero, while F, both
full-fiber basins, beta, invariant law and D_yy are unchanged.

This disproves any strictly positive capacity lower bound from the fixed
potential and marginal D_yy alone over all constant SPD full mobilities. It does
not refute the no-cross block-mobility theorem. It does not posit a novel
Dirichlet principle, generic rate hardness, arbitrary-start MFPT, or any physical
realization.

## 1. Normalization and basin mass are globally received

For all y,

    v(y)>=1,  v(y)-y^4/2=(y^2-2)^2/2>=0.

Integrating the Gaussian z fiber gives

    m(y)=sqrt(2*pi)/sqrt(v(y)),    Z=integral_R m(y)dy.

On |y|<=1, v<=2, hence Z>=2sqrt(pi)>3. For |y|<=2 use
m<=sqrt(2*pi), and for |y|>2 use m<=2sqrt(pi)/y^2. Thus

    Z<=4sqrt(2*pi)+2sqrt(pi)<16.

In particular mu is an actual probability measure; the zero-energy line z=0
does not invalidate integrability. The tails in y are proportional to y^-2;
finite second moments are neither claimed nor needed.

The density is even in y. Write Z_A=integral_A exp(-F) and
Z_mid=integral_{|y|<1/2} exp(-F). On |y|<=1/2, v>=25/16, so
Z_mid<=(4/5)sqrt(2*pi). On -1<=y<=-1/2, v<=25/16, so
Z_A>=(2/5)sqrt(2*pi). Consequently

    Z=2Z_A+Z_mid<=4Z_A,        1/4<=mu(A)<1/2.               (3)

Every matrix entry, the potential, and the basin descriptions are fixed known
mathematical inputs, rather than inferred from equilibrium samples.

## 2. The global process for EACH D

D has positive leading entry 1 and determinant

    det D=k^2 epsilon/(1-epsilon)>0.

Its coefficients are finite for each admitted parameter pair. The SDE is

    dX_t=-D grad F(X_t)dt + sqrt(2D)dW_t.

Its drift is polynomial and hence locally Lipschitz; the constant diffusion is
nondegenerate. The unique maximal strong solution is nonexplosive. To see this,
let x=(y,z) and

    V_D(x)=1+x^T D^-1 x.

For each fixed SPD D, V_D is coercive. Euler pairing gives

    x.grad F=(3y^4-4y^2+2)z^2,
    L V_D=4-(6y^4-8y^2+4)z^2,
    6y^4-8y^2+4=6(y^2-2/3)^2+4/3.

Therefore L V_D<=4. With tau_R the first exit from the Euclidean ball of
radius R, stopped Ito and nonnegativity yield

    P_x(tau_R<=t)
      <= [V_D(x)+4t]/[1+R^2/lambda_max(D)] -> 0.

The stopped stochastic integrals are bounded-coefficient local martingales,
so this application of Ito requires no stationary second moment. The coercive
comparison constants depend on the actual D; no uniform mixing or uniform
starting-point time claim is made.

For completeness, invariance does not rest only on a formal density. In each
bounded smooth exhaustion domain, the killed diffusion has the symmetric
Dirichlet realization of L on L2(mu), because integration by parts gives

    -integral f Lg dmu = integral grad f^T D grad g dmu

for smooth compactly supported f,g. Local uniqueness identifies these killed
semigroups with the stopped SDE. Exhaustion and nonexplosion give the conservative
semigroup P_t and retain symmetry by monotone convergence on nonnegative test
functions. Thus P_t1=1, and symmetry plus finite mu gives

    integral P_t f dmu = integral f P_t1 dmu = integral f dmu.

This is the required global reversible invariant process for each actual D,
including the cross terms. There is no assumed fast equilibration and no
block-diagonal Lyapunov being applied outside its hypotheses.

## 3. A smooth, exactly admissible full-fiber boundary patch

Here is a concrete C-infinity step with the stated numerical derivative bound.
Let

    psi(t)=exp[-1/(1-16t^2)] for |t|<1/4, and 0 otherwise,
    I=integral psi(t)dt,      u(t)=I^-1 integral_{-infinity}^t psi(s)ds.

Then 0<=u<=1, u=0 on t<=-1/4, u=1 on t>=1/4, and

    I >= (1/4)exp(-4/3),
    ||u'||_infinity <=4exp(1/3)<6.

Define

    chi(y)=1-u(4(|y|-7/16)).

The absolute value causes no nonsmoothness at zero because chi is identically
1 in a neighborhood of zero. Thus chi is C-infinity, equals 1 on |y|<=3/8,
equals 0 on |y|>=1/2, takes values in [0,1], and ||chi'||<=24.

Put alpha=(1-epsilon)/k and s=y-alpha z, and take

    h(y,z)=chi(y)u(s)+(1-chi(y))u(y).                       (4)

This is a C-infinity bounded trial with h=0 on ALL of A and h=1 on ALL of B,
not merely on a typical fiber or except on a small tail. It is also in the
weighted energy domain: the following estimate proves finite energy; smooth
spatial cutoffs then approximate it in weighted H1 for each fixed finite D.
(The derivative of a radius-R cutoff contributes at most C_D/R^2 times the
finite mass.) No boundary-violating trial is used at any intermediate limit.

Core |y|<=3/8: chi=1, and

    grad h=u'(s)(1,-alpha),
    (1,-alpha)^T D(1,-alpha)=epsilon.

Hence the entire core contributes at most 36 epsilon Z to the unnormalized
energy. Outside |y|<1/2 the gradient vanishes identically.

Patch P={3/8<|y|<1/2}: here u'(y)=0. Let

    a=chi u'(s),   b=chi'[u(s)-u(y)].

Then grad h=(a+b,-alpha a), and EXACTLY

    grad h^T D grad h =epsilon a^2+2epsilon ab+b^2
                     <=(sqrt(epsilon)|a|+|b|)^2<=900.       (5)

If either a or b is nonzero, |s-y|>=1/8, because y is separated from the
transition interval [-1/4,1/4] by at least 1/8. Consequently

    |z| >= k/[8(1-epsilon)] >= k/8.                       (6)

This is the sole tail suppression used: derivative errors are supported in an
exactly identified Gaussian tail. P has total y length 1/4, and v>=1. The
standard elementary Gaussian bound

    integral_{|z|>=R}exp(-z^2/2)dz <=(2/R)exp(-R^2/2)

follows by replacing 1 with |z|/R on each tail and integrating. Taking R=k/8
therefore gives

    E_unnormalized,patch(h)
      <=900*(1/4)*(16/k)exp(-k^2/128)
      =(3600/k)exp(-k^2/128).                              (7)

Divide core+patch by Z>3 and use the variational definition of capacity to
obtain the upper inequality in (1). Equation (3) gives (2).

The alternative variable-shear trial u(y-alpha chi(y)z) also works, but its
patch derivative contains z chi'(y); the blend (4) avoids that unnecessary
weighted-tail cost. Both are ordinary admissible test functions, not claims
about the true committor.

## 4. Positive lower bounds and the cost of collapse

For any smooth admissible h,

    grad h^T D grad h
      =epsilon h_y^2 + [k^2/(1-epsilon)](h_z+alpha h_y)^2
      >=epsilon h_y^2.

On each fixed z, weighted Cauchy-Schwarz across -1/2<=y<=1/2 gives

    integral exp(-F)h_y^2 dy >=1/[integral exp(F)dy].

The interval has length 1 and v(y)<=2 there, so its denominator is at most
exp(z^2). Integration in z gives cap>=epsilon sqrt(pi)/Z>epsilon/16.
Density/trace approximation extends this bound to the capacity domain.
In particular every actual SPD member has strictly positive capacity.

A second lower bound exposes a necessary cost that the Schur bound alone misses:

    D=(1,k)(1,k)^T + diag(0,k^2 epsilon/(1-epsilon)).

Thus its energy dominates (h_y+k h_z)^2. In the unit-Jacobian coordinates
(y,w) with z=w+ky, apply the same one-dimensional inequality along each tilted
line. Both full-fiber boundary values remain exact on every such line. This
produces

    cap >= Z^-1 integral_R dw /
              [integral_{-1/2}^{1/2}exp(F(y,w+ky))dy].

On the slab,

    F(y,w+ky)<=(w+ky)^2<=2w^2+k^2/2,

and hence

    cap >=sqrt(pi/2)exp(-k^2/2)/Z>exp(-k^2/2)/16.          (8)

More generally, for EVERY constant SPD D=[[1,b],[b,c]], c>b^2,

    cap >=(1-b^2/c)sqrt(pi)/Z,
    cap >=sqrt(pi/2)exp(-b^2/2)/Z.                         (9)

Consequently any sequence in this fixed-F/full-basin family with capacity->0
must have BOTH its longitudinal Schur complement 1-b^2/c->0 and |b|->infinity.
Bounded cross coefficients, or bounded transverse mobility c, forbid collapse
even when the matrices approach singularity. In fact these two conditions are also jointly sufficient for every sequence in
this fixed-F two-dimensional family, not just a specially tuned one. For b!=0
put delta=1-b^2/c and alpha=b/c. Use the same smooth blended trial (4) with this
alpha. Its core quadratic form is delta, the patch bound is still 900, and its
nonzero patch derivatives require |z|>=|b|/[8(1-delta)]>=|b|/8. Therefore

    cap_D <=36delta+(1200/|b|)exp(-b^2/128).              (10)

This works for either sign of b and every nonzero real b; integrality and
rationality are restrictions of the finite receiver, not of the analytic
theorem. Combining (9) and (10) proves the EXACT classification

    cap(D_n)->0  IFF  delta_n->0 AND |b_n|->infinity.     (11)

The same equivalence holds for cap(D_n)/mu(A), because mu(A) is fixed.
Degenerating Schur complement alone or diverging transverse mobility alone is
not sufficient. The two conditions together are sufficient in precisely this
fixed-potential, fixed-full-basin, constant-mobility class.

For our D, writing gamma=k^2/(1-epsilon),

    gamma <=lambda_max(D)<=gamma+1,
    gamma epsilon/(gamma+1)<=lambda_min(D)<=epsilon,
    gamma/epsilon<=condition_number(D)<=(gamma+1)^2/(gamma epsilon).

Since gamma>=1, the eigenvalue condition number lies between gamma/epsilon and
4gamma/epsilon. Noise covariance per unit time is 2D: y variance rate is always
2, but transverse variance rate diverges like 2k^2/(1-epsilon), cross covariance
rate is 2k, correlation is sqrt(1-epsilon), and the conditional longitudinal
noise scale tends to zero. These are real geometric/dynamic costs, not an
unadvertised uniform physical resource budget. Whitening D would change F and
the basin geometry, so is not a valid fixed-physical-coordinate comparison.

## 5. Finite, rational receiver and explicit failure costs

The executable receiver reads k and epsilon as exact integer/rational inputs,
checks k>=1,0<epsilon<1, receives every matrix entry, verifies Sylvester's exact
SPD condition and the Schur complement, and emits rational bounds. Since e>2,

    exp(-k^2/128)<=2^(-floor(k^2/128)).

Since e<3,

    exp(-k^2/2)>=3^(-ceil(k^2/2)).

It can therefore report, with no numerical quadrature or PDE solver,

    cap lower =max(epsilon,3^(-ceil(k^2/2)))/16,
    cap upper =36epsilon+(1200/k)2^(-floor(k^2/128)),
    conductance upper =4*cap upper.

The exponential estimates are deliberately loose rational certificates, not
estimates of the true capacity. The program also exposes matrix entries,
determinant, Schur complement, and proven condition-number enclosure.

The theorem consumes a fixed analytic potential grammar and exact constant
mobility entries. Its input validation rejects nonintegral/negative k,
epsilon outside (0,1), unknown/extra schema fields, and noncanonical rational
inputs. It does not read arbitrary potentials or infer reversibility, constant
mobility, or fluctuation-dissipation from data. Exact SPD checks here are O(1)
rational operations; producing the tail certificate uses integers with
O(k^2+input-bit-length) bits in this simple implementation, so large k is not
being counted as constant cost. No random failure probability is hidden: the
reported interval is deterministic conditional on the stated model.

Receiver hardening: raw JSON duplicate keys are rejected. Before constructing
expanded integer powers, the receiver enforces a configurable positive exponent
budget (default 1,000,000). A budget rejection is a declared computational limit,
not a counterexample to the analytic theorem. It occurs before large power
allocation; all displayed examples fit the default budget.
