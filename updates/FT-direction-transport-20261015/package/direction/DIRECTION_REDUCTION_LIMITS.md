# Astra Meta-Genesis: what remains after global amplitude elimination

Research date: 15 October 2026.

## Status

The complete planar implication from rank-one convexity to quasiconvexity, including the full nine-coefficient left-SO(2)-invariant homogeneous quartic cone, is not established here. No negative compatible quasiconvexity gap is constructed.

This investigation establishes precise limitations of the preceding amplitude reduction:

1. The direction functional can be nonconvex **after global minimization over every amplitude**, even when the original integrand is the convex quartic `F(A)=|A|^4`. An explicit genuinely two-dimensional periodic example has a strict rational midpoint-convexity violation. A reduced-Hessian formula explains it.
2. For the unconstrained radial comparison, being a global amplitude minimizer about three suitably chosen target-translation centers is equivalent to the original vectorial Euler-Lagrange equation. This stronger collection of radial optimality conditions is not a global-minimum certificate.
3. A quantitative large-target-translation theorem identifies the actual limit of the fully amplitude-minimized affine-boundary problem. It is the original functional with one Cartesian output component minimized. The energy error is `O(R^-1)` and the component-minimizer error is `O(R^-1/4)`. This is not merely the observation that translating a map makes its phase small.
4. Keeping the previous fourth-mass constraint does not evade the limit: the constraint becomes a scalar mean constraint on the minimized Cartesian component.

The basic scalar convexity, perspective, Picone and Schur-complement operations are established mathematics. No historical novelty is claimed for those tools. The specific obstruction examples and quantitative comparison require their own priority review. Their analytic proofs are below. The accompanying script checks finite algebra only, not compactness, lower semicontinuity, or the implicit-function theorem.

The new script passed twelve groups of checks. The prior ten-group directional-density verifier was replayed. The prior million-cell interval certificate and the older long contact classifications were not rerun: none is a premise of the new conclusions.

## 1. Reconstruction of the load-bearing amplitude argument

Let `F:R^(m x d)->R` be C1, positively p-homogeneous, and rank-one convex. For a fixed sufficiently regular unit field `omega(x)`, write

    u=r omega,  rho=r^p,  A_r=Domega+omega tensor grad(log r).

For positive amplitudes,

    F(D(r omega))=rho F(Domega+omega tensor grad(rho)/(p rho)).       (1.1)

At each point, `a -> F(Domega+omega tensor a)` is convex because differences of its arguments have rank at most one. Its perspective is therefore convex in `(rho,grad rho)`. This proves the preceding fixed-direction convexity claim. No assumption that F is globally convex or nonnegative is involved.

For positive reference r and competitor s,

    Q=omega tensor grad(log(s/r))

is rank one, and homogeneity gives the exact identity

    F(D(s omega))
      -(1/p) DF(D(r omega)):D(omega s^p/r^(p-1))
    =s^p [F(A_r+Q)-F(A_r)-DF(A_r):Q] >=0.                       (1.2)

Indeed,

    D(omega s^p/r^(p-1))=(s^p/r^(p-1))(A_r+pQ),
    DF(D(r omega))=r^(p-1) DF(A_r),
    DF(A_r):A_r=p F(A_r).

For a homogeneous quartic, put

    mu=min{F(R): rank R=1, |R|=1}.

Rank-one convexity gives mu>=0. The scalar restriction

    f(t)=F(C+tQ)=At^4+Lt^3+C2 t^2+Dt+E

has globally nonnegative second derivative. For A>0,

    C2>=3L^2/(8A),
    A+L+C2-A/3=3(L+4A/3)^2/(8A)+C2-3L^2/(8A)>=0.

For A=0, nonnegative second derivative forces L=0, C2>=0. Thus the rank-one Bregman remainder is at least `F(Q)/3`. Equation (1.2) implies

    F(D(s omega))
      -(1/4)DF(D(r omega)):D(omega s^4/r^3)
      >= (mu/3) r^4 |grad(s/r)|^4.                             (1.3)

For positive regular reference r the integrated inequality extends to nonnegative W1,4 competitors by approximation. The admissible density domain is `{rho>=0: rho^(1/4) in W1,4}`, not all of an unspecified Sobolev space.

The previous fixed-fourth-mass existence argument is also sound under its hypotheses. If omega is smooth with bounded derivative and mu>0, polynomial growth and Young's inequality give

    F(omega tensor grad r+r Domega)
      >= (mu/2)|grad r|^4-C_F ||Domega||_infinity^4 r^4.

Fixed fourth mass therefore bounds minimizing sequences in W1,4. Strong L4 convergence of amplitudes, weak convergence of their gradients, and scalar convexity in grad r give attainment. This is a convex conditional problem. It is not a sign theorem for its minimum and not joint convexity in direction and density.

### Attribution

Brasco and Franzina [1], notably Sections 2 and 3, discuss scalar hidden convexity, kinetic-energy perspectives, Picone inequalities and their equivalences. The vectorial application above is obtained because the normalized-gradient differences are rank one. Neither the inherited note nor this continuation should treat the perspective or ground-state substitution as newly invented mathematics.

## 2. Exact nonconvexity after global amplitude minimization

### 2.1 Definition of the fully reduced functional

On the square 2pi-periodic torus use probability-normalized averages. Let theta have a periodic unit field `(cos theta,sin theta)`; a real lift of theta may have integer winding. Define

    J(theta)=min { E |D(r exp(i theta))|^4 :
                   r>=0, r in W1,4, E r^4=1 }.                (2.1)

Existence follows directly from coercivity of `|D(r exp(i theta))|^4` in grad r at fixed mass. The admissible amplitudes may depend on both coordinates. The minimum is not restricted to a trigonometric ansatz.

With rho=r^4,

    E |D(r exp(i theta))|^4
     = E [rho |grad theta|^4
       + |grad rho|^2 |grad theta|^2/(8rho)
       + |grad rho|^4/(256rho^3)].                            (2.2)

At `theta_0(x,y)=y`, the first term is `E rho=1` and the other terms are nonnegative. Therefore

    J(theta_0)=1,

with unique normalized amplitude r=1.

### Theorem 2.1: a strict midpoint violation for the globally reduced energy

Set epsilon=1/100 and

    theta_plus=y+epsilon sin(x+y),
    theta_minus=y-epsilon sin(x+y).

Then

    J((theta_plus+theta_minus)/2)=1,

but

    J(theta_plus)=J(theta_minus)
      <= 486519245657/486680000000 <1.                        (2.3)

Thus J is not convex, even in a smooth local chart of a fixed winding class, although F itself is convex.

**Proof.** Translation of x by pi takes theta_plus to theta_minus and preserves all amplitude competitors, so their global minima agree. Their midpoint is y.

For theta_plus use the admissible density

    rho=1-8epsilon cos(x+y) >=23/25,
    E rho=1.

Put `c=cos(x+y)` and

    K2=|grad theta_plus|^2=1+2epsilon c+2epsilon^2 c^2.

Then `|grad rho|^2=128epsilon^2(1-c^2)`. The trial energy is exactly the average of

    (1-8epsilon c)K2^2
      +16epsilon^2(1-c^2)K2/(1-8epsilon c)
      +64epsilon^4(1-c^2)^2/(1-8epsilon c)^3.                  (2.4)

The three numerator averages are

    1-12epsilon^2-(45/2)epsilon^4,
    8epsilon^2+4epsilon^4,
    24epsilon^4.

Using `1-8epsilon c>=1-8epsilon=23/25` in the two positive rational terms gives

    trial <= 1-12epsilon^2-(45/2)epsilon^4
          +(8epsilon^2+4epsilon^4)/(1-8epsilon)
          +24epsilon^4/(1-8epsilon)^3
          =486519245657/486680000000.

The deficit below one is the positive rational `160754343/486680000000`. The global minimum is at most this trial value. No approximation to the minimizing amplitude is used. QED.

For orientation only, the exact trial value is

    50880491/40000000 - (7241/220800)sqrt(69)
      =0.99960166181435788040... .

The rational upper bound, not this decimal, proves (2.3). The trial amplitude is not asserted to be the exact minimizer.

The phase and amplitude depend on x+y in addition to the carrier y. The corresponding gradient is not confined to one rank-one matrix line. Nevertheless all original energies in this example are nonnegative because `F(A)=|A|^4`. A negative second difference of J is not a negative quasiconvexity gap.

### 2.2 The exact reduced second variation

This calculation locates the surviving interaction after minimization. Let k be a nonzero integer wavevector and theta_0=k.x. At rho=1, vary

    rho=1+t eta,  theta=k.x+t h,  E eta=0.

The full quadratic form obtained from (2.2) is

    Q(eta,h)
      =E[(|k|^2/4)|grad eta|^2
          +8|k|^2 eta(k.grad h)
          +4|k|^2|grad h|^2+8(k.grad h)^2].                 (2.5)

The density block is a positive multiple of the Laplacian on mean-zero functions. Its minimizer for fixed h solves

    Delta eta=16 k.grad h,
    eta=16 Delta^(-1)(k.grad h).

Therefore the Hessian of the fully minimized functional is

    D^2J(k.x)[h,h]
      = E[4|k|^2|grad h|^2+8(k.grad h)^2]
        -64|k|^2 <k.grad h,(-Delta)^(-1)(k.grad h)>.          (2.6)

The final pairing uses normalized integration and the inverse on mean-zero functions. The Fourier multiplier on a nonzero frequency xi is

    Lambda_k(xi)
      =4|k|^2|xi|^2+8(k.xi)^2
       -64|k|^2 (k.xi)^2/|xi|^2.                           (2.7)

For k=(0,1), xi=(1,1), and h=sin(x+y),

    D^2J(y)[h,h]=-8,
    eta=-8 cos(x+y),
    J(y+epsilon h)=1-4epsilon^2+o(epsilon^2).                (2.8)

This is not obtained by minimizing over only one density Fourier coefficient. Translation invariance of the quadratic form makes Fourier modes orthogonal, and all density modes have been eliminated in (2.6).

**Justification of differentiating the true minimum.** Work in a C^(2,alpha) neighborhood of rho=1 and of the affine phase. The mass-constrained density Euler equation has linearization `-(|k|^2/4)Delta` on mean-zero densities, with the multiplier accounting for constants. This is an isomorphism between the relevant periodic Holder spaces. The implicit-function theorem gives a positive smooth critical density near one. Fixed-direction convexity makes it a global density minimizer, not merely a local critical point. The positive-reference Picone comparison proves uniqueness at fixed mass. The reduced functional is consequently smooth on this neighborhood, and differentiating its stationarity equation gives (2.6).

One need not invoke this implicit-function argument to prove nonconvexity: the exact trial-and-symmetry proof of Theorem 2.1 is independent of it.

The same calculation for `F(A)=|A|^p`, p>1, gives

    D^2J_p(k.x)[h,h]
      = p|k|^(p-2) E|grad h|^2
        +p(p-2)|k|^(p-4)E(k.grad h)^2
        -p^3|k|^(p-2)<k.grad h,(-Delta)^(-1)(k.grad h)>.

On one spatial coordinate this becomes

    p(p-1)|k|^(p-2) E|h'|^2
       -p^3|k|^p E|h-Eh|^2.

Thus the issue is not special to one quartic coefficient choice. No priority claim is made for this nonlinear-eigenvalue stability calculation.

### 2.3 What convex elimination generally does

For a smooth functional E(rho,theta), suppose the density Hessian A is coercive on its constraint tangent space and the critical density can be solved smoothly. In block form write its second variation as

    [[A,C],[C*,D]].

The reduced direction Hessian is

    D-C* A^(-1) C.                                         (2.9)

The identity

    <A eta,eta>+2<C h,eta>+<D h,h>
     =<A(eta+A^(-1)Ch),eta+A^(-1)Ch>
       +<(D-C*A^(-1)C)h,h>

shows that the negative index is retained in the reduced block. Eliminating a positive block subtracts a nonnegative response term; it does not make the remaining block more convex. This is standard Schur-complement/Lyapunov-Schmidt analysis [2], not a new general principle.

## 3. Radial global optimality about many centers is exactly stationarity

This section concerns unconstrained radial comparison with fixed boundary values. It is deliberately stronger than imposing one fixed fourth-mass constraint.

### Theorem 3.1: translated radial optimality criterion

Let F be a rank-one-convex homogeneous quartic and let u be a smooth map on a bounded connected domain. Choose target translations c for which |u+c| is bounded away from zero. Put

    r_c=|u+c|,  omega_c=(u+c)/r_c.

If u is a weak solution of

    -div DF(Du)=0,                                         (3.1)

then for every such c and every nonnegative W1,4 amplitude s having the same boundary trace as r_c,

    integral F(D(s omega_c))-integral F(Du)
      >= (mu/3) integral r_c^4 |grad(s/r_c)|^4 >=0.          (3.2)

Conversely, if u has this global radial-minimum property for m+1 target translations c_0,...,c_m whose differences c_i-c_0 span R^m, then u solves (3.1). In the planar target, three noncollinear centers suffice. Centers avoiding zero can always be chosen for a bounded u.

**Proof of the forward implication.** Apply (1.3). The test field

    xi=omega_c(s^4/r_c^3-r_c)

has zero boundary trace. Stationarity gives

    integral DF(Du):D(omega_c s^4/r_c^3)
      =integral DF(Du):Du
      =4 integral F(Du).

Substitute into (1.3). Approximation gives the stated competitors.

**Converse.** Use the small variations `s=r_c(1+t eta)` with eta smooth and compactly supported. Both signs of t are admissible. A radial minimum implies

    integral DF(Du):D[eta(u+c)]=0.

Subtract the identities for c_i and c_0. This gives

    integral DF(Du):[(c_i-c_0) tensor grad eta]=0.

Since those constant target vectors span the target space, every component of div DF(Du) vanishes distributionally. QED.

This theorem does not claim that a nonglobal stationary point exists for the particular planar cone. It proves that requiring global amplitude optimality about all centers adds no condition beyond the original Euler equation in this unconstrained setting. It therefore cannot, without further information about vectorial stationary points, certify global quasiconvexity.

### 3.2 The remaining angular equation is the original tangential equation

For left-SO(2)-invariant F, write u=r exp(i theta), S=DF(Du), and let J be the target quarter-turn. Rotation invariance gives

    S:JDu=0.

The direction variation delta u=h Ju has first variation

    delta E=integral j.grad h,
    j_i=S_i.Ju.                                           (3.3)

On a smooth positive branch of mass-constrained amplitude minima, the envelope derivative is still (3.3): the induced amplitude variation has zero mass derivative and contributes zero by radial stationarity.

The radial equation is

    -omega.div S=4lambda r^3.

Moreover

    div j=(div S).Ju,

because the remaining term is S:JDu=0. Together, radial and angular stationarity give exactly

    -div S=4lambda |u|^2u.                                 (3.4)

Thus the reduced direction equation is the tangential part of the original constrained vectorial Euler-Lagrange system. At zeros or nonsmooth minimizers, this calculation must be replaced by a weak/subdifferential formulation; no blanket regularity claim is made.

## 4. An ordinary Cartesian scalar minimization already eliminates one component

This is standard scalar convex minimization, recorded explicitly so the translation limit has a definite target.

Let Omega be a bounded connected Lipschitz domain in R^2. Let g_1,g_2 be affine functions. Let F be a homogeneous rank-one-convex quartic with

    mu_1=min_{|xi|=1} F(e_1 tensor xi)>0.

For a fixed scalar second component v in `g_2+W0^(1,4)(Omega)`, define

    I_v(a)=integral F([grad a; grad v]),
    a in g_1+W0^(1,4)(Omega),
    R_F(v)=min_a I_v(a).                                   (4.1)

The bracket denotes matrix rows, not columns.

### Proposition 4.1: unique scalar minimizer and global remainder

There is a unique minimizer a_v. For every admissible a,

    I_v(a)-I_v(a_v)
      >=(mu_1/3)||grad(a-a_v)||_4^4.                       (4.2)

The same statement holds after also fixing the scalar mean integral a=m_0.

**Proof.** At fixed grad v, varying grad a is a rank-one variation. Hence the scalar integrand is convex. Its quartic remainder obeys (1.3)'s univariate bound in the constant output direction e1:

    F([xi;eta])-F([zeta;eta])-F_1([zeta;eta]).(xi-zeta)
       >=(mu_1/3)|xi-zeta|^4.                              (4.3)

Taking zeta=0 and using quartic growth for F_1 yields

    F([xi;eta]) >= c|xi|^4-C|eta|^4.

Poincare's inequality after subtracting g_1 gives coercivity. Convex weak lower semicontinuity yields attainment. The scalar Euler equation, or the multiplier equation when the mean is fixed, makes the linear term in integrated (4.3) vanish for feasible comparisons. This proves uniqueness and (4.2).

No new numerical complexity theorem is claimed. The point is that one globally solvable scalar component is already present in the original Cartesian representation.

### A checkable error bound for an approximate scalar solve

For a trial a, let the residual functional on W0^(1,4) be

    res(h)=integral F_1([grad a;grad v]).grad h,
    d=sup{|res(h)|: ||grad h||_4<=1}.

Then

    0<=I_v(a)-R_F(v)
       <=(3/4)(3/(4mu_1))^(1/3) d^(4/3).                  (4.4)

Indeed (4.3) gives `I_v(a+h)>=I_v(a)-d t+(mu_1/3)t^4` with t=||grad h||4. Maximize `d t-(mu_1/3)t^4` exactly. This is a standard strong-convexity residual estimate. Computing the dual norm d rigorously remains a required step in any numerical certificate; it is not replaced by sampled residual values.

## 5. Quantitative translation limit of the fully amplitude-minimized problem

This theorem is the main test of whether the amplitude reduction genuinely removes the remaining direction difficulty.

Let F, Omega, g_1,g_2 be as in Section 4. Fix v in `g_2+W0^(1,4)`. Since 4>2, W1,4 functions are bounded and have continuous representatives; Omega is assumed to have the usual Lipschitz extension property.

For R large enough that d_R=R+g_1>0, define

    q_R=v/d_R,
    omega_R=(d_R,v)/sqrt(d_R^2+v^2).                        (5.1)

For a in `g_1+W0^(1,4)`, put h=a-g_1 and

    u_R[a]=(R+a, v+h q_R)
           =(R+a, (R+a)v/(R+g_1)).                         (5.2)

If R+a>=0, this is precisely `r_R[a] omega_R`, with

    r_R[a]=(R+a)sqrt(1+q_R^2).                             (5.3)

Every nonnegative amplitude with the prescribed boundary is represented this way. On the boundary,

    u_R[a]=(R+g_1,g_2).

Thus the affine boundary is exact, not asymptotic. Its gradient is

    Du_R[a]=[grad a;
              grad v+q_R grad h+h grad q_R].               (5.4)

Define the global radial minimum without a mass constraint by

    m_R(v)=min_{a-g_1 in W0^(1,4), R+a>=0}
                     integral F(Du_R[a]).                 (5.5)

The mass-free minimum is used first to expose the limit; Section 6 restores exactly the constraint used in the previous investigation.

### Theorem 5.1: the reduced direction problem contains Cartesian row minimization

For all sufficiently large R, (5.5) has a minimizer a_R, its amplitude is strictly positive, and

    |m_R(v)-R_F(v)| <= C/R,                                (5.6)
    ||a_R-a_v||_(W1,4) <= C R^(-1/4).                      (5.7)

The constants depend on F, Omega, the boundary data, and v, but not on R. Every global minimizer has these bounds.

The direction fields satisfy

    ||omega_R-e_1||_(W1,4) <= C/R.

If v and the boundary data are smooth, convergence to e1 is O(R^-1) in each fixed C^k norm. Nevertheless their fully minimized energies converge to the unrestricted original scalar-component minimum R_F(v), with v arbitrary.

### Proof

#### 5.1 Uniform energy comparison on bounded W1,4 sets

Because W1,4 embeds into L-infinity in the planar domain,

    ||q_R||_infinity+||grad q_R||_4 <= C/R.

For h with zero trace,

    ||grad(h q_R)||_4
      <=||q_R||_infinity||grad h||_4
          +||h||_infinity||grad q_R||_4
      <=(C/R)||grad h||_4.                                 (5.8)

A quartic polynomial satisfies

    |F(A+E)-F(A)|<=C_F(|A|+|E|)^3|E|.

Applying Holder to (5.4) and (5.8) gives, for all admissible a and all sufficiently large R,

    |I_R(a)-I_v(a)|
      <=(C/R)(1+||grad(a-g_1)||_4^4),                       (5.9)

where `I_R(a)=integral F(Du_R[a])`. This comparison holds before imposing positivity of R+a.

#### 5.2 Uniform coercivity and existence

Section 4 gives

    I_v(a)>=c||grad(a-g_1)||_4^4-C.

For sufficiently large R, (5.9) therefore gives the same type of coercive bound for I_R, uniformly in R. The admissible comparison a=g_1 has bounded energy independent of R. Thus every minimizing sequence and every minimizer is uniformly bounded in W1,4.

For a sequence weakly converging in W1,4, pass to a subsequence converging uniformly and strongly in L4. In (5.4), the lower-order term `h grad q_R` then converges strongly in L4. For frozen h, changing grad a changes the matrix by `(1,q_R) tensor delta grad a`, a rank-one difference. The integral is therefore weakly lower semicontinuous in that gradient. Quartic growth controls the error from the strongly converging lower-order term. The constraint R+a>=0 and boundary trace are closed. This proves attainment.

The uniform W1,4 bound gives a uniform L-infinity bound on a_R. Hence R+a_R>0 for every sufficiently large R. The radial positivity constraint is inactive at these minima. The preceding fixed-direction density formulation consequently applies without a mass constraint, and it is a convex formulation of the same minimum.

#### 5.3 Values and minimizers

The unique Cartesian minimizer a_v is bounded; thus R+a_v>0 for large R. It is an admissible comparison in (5.5). Equation (5.9) gives

    m_R(v)<=I_R(a_v)<=R_F(v)+C/R.

Conversely, the uniform bound on a_R and (5.9) give

    m_R(v)=I_R(a_R)>=I_v(a_R)-C/R>=R_F(v)-C/R.

This proves (5.6). It also yields

    I_v(a_R)-I_v(a_v)<=C/R.

Use the global scalar remainder (4.2) and Poincare's inequality to obtain (5.7). QED.

### Why this is stronger than a pointwise small-phase observation

The direction omega_R is constructed from the arbitrary second component v and the *prescribed affine first boundary component* g_1. It does not use the unknown minimizing first component. The amplitude is minimized globally. The minimum and its minimizers are then compared quantitatively with a definite Cartesian problem. The result is not obtained merely by translating a preselected map and noting that its angle is small.

No computational hardness theorem follows from an equivalent limit. A representation equivalent to the original problem could still admit a new useful inequality. What is disproved is the inference that small direction variation, together with solved amplitude optimization, by itself excludes any of the original global sign difficulty.

## 6. The previous fourth-mass constraint survives as a mean constraint

Choose any reference `a_ref in g_1+W0^(1,4)` and prescribe exactly

    M_R=integral (R+a_ref)^4(1+q_R^2)^2.                    (6.1)

Let m_R^mass(v,a_ref) be (5.5) with the additional condition

    integral (R+a)^4(1+q_R^2)^2=M_R.                        (6.2)

### Theorem 6.1: fixed-mass translation limit

For all sufficiently large R the mass-constrained radial minimum is attained, all its minimizers have positive amplitudes, and

    m_R^mass(v,a_ref)
       -> min { I_v(a): a-g_1 in W0^(1,4),
                         integral a=integral a_ref }.      (6.3)

The value error is O(R^-1), and the minimizers converge in W1,4 at rate O(R^-1/4) to the unique minimizer of the mean-constrained Cartesian problem.

### Proof

On uniformly bounded W1,4 sets, hence uniformly bounded amplitudes, expand

    R^(-4) (R+a)^4(1+q_R^2)^2
      =(1+a/R)^4 [1+v^2/(R+g_1)^2]^2.

Subtract the corresponding expression for a_ref and divide by 4/R. Uniformly after integration,

    [M_R(a)-M_R(a_ref)]/(4R^3)
      = integral(a-a_ref)+O(R^-1).                         (6.4)

The next pointwise term is `(3/(2R))(a^2-a_ref^2)`; the common v^2 term cancels.

Uniform coercivity follows from Section 5, and a_ref is a feasible comparison, so all minimizing sequences are uniformly bounded. Compact convergence in L-infinity and L4 makes the mass constraint closed. Existence and eventual positivity follow as before. Every limit has the mean required in (6.3).

For recovery with the *exact* mass, fix a smooth nonnegative zero-boundary bump zeta with integral one. If a has the required limiting mean, equation (6.4) makes the scaled mass error O(R^-1). The derivative of the left side with respect to t in a+t zeta tends uniformly to one. The intermediate value theorem therefore supplies t_R=O(R^-1) for which a+t_R zeta has exactly the prescribed mass. Its energy changes by O(R^-1).

Apply this correction to the Cartesian constrained minimizer for the upper bound. For the lower bound, (6.4) gives an O(R^-1) mean error for a_R. Correct that error by an O(R^-1) multiple of zeta, compare with the constrained Cartesian minimum, and use (5.9). This proves the O(R^-1) value bound.

The constrained scalar Euler equation makes the linear term in (4.3) vanish between exactly mean-feasible competitors. Its quartic remainder, applied after the O(R^-1) correction, proves the O(R^-1/4) minimizer convergence. QED.

The fourth-mass normalization is therefore not an additional source of global positivity. In this translation limit it fixes only the mean of the eliminated Cartesian component. No replacement of the original mass constraint by a different one was made without proof.

## 7. Consequence for a putative quasiconvexity counterexample

Suppose a smooth compatible affine-boundary test u=(a,v), with boundary `(g_1,g_2)=Bx`, has

    integral F(Du) < |Omega|F(B)-epsilon.

Fix omega_R by (5.1), using g_1 and v, and, for the fixed-mass version, choose a_ref=a. The Cartesian mean-constrained minimum in (6.3) is no greater than the energy of this original a. For all sufficiently large R, the globally amplitude-minimized map along omega_R therefore satisfies

    integral F(Du_R^*) < |Omega|F(B)-epsilon/2.               (7.1)

It has exact affine boundary `Bx+R e_1`, is a genuine W1,4 map, and its direction approaches the constant e_1. Subtracting the target translation preserves its gradient and produces the same kind of quasiconvexity test as the original one.

Conversely, if F is quasiconvex, every such actual map has nonnegative gap. Thus a universal claim of positivity for all these asymptotically constant, globally amplitude-minimized directions is equivalent to the original affine-boundary positivity problem, not a consequence of conditional amplitude convexity.

The amplitudes grow like R, and their fourth masses grow like R^4. Normalizing them to mass one rescales both the energy and affine boundary but preserves the sign, because F is homogeneous. This observation does not keep the affine matrix B fixed during that additional normalization; the universal problem already ranges over all B.

This is a statement about the full obstruction being retained. It is not a proof that all possible analysis of the reduced functional must fail, nor a complexity-theoretic impossibility result.

## 8. The remaining functional and a more honest computational use

The translate-free residual problem is already

    R_F(v)=min_a integral F([grad a;grad v]),

with the correct affine traces (and a mean constraint when inherited from fixed mass). Its sign relative to |Omega|F(B) is unresolved.

At a sufficiently regular nondegenerate solution branch a_v, write the blocks of D^2F at the actual gradient A_v as F_11,F_12,F_22, with row indices. The second variation of the reduced scalar-component energy is

    R_F''(v)[h,h]
      = inf_eta integral D^2F(A_v)
                    [[grad eta];[grad h]],[[grad eta];[grad h]].     (8.1)

Equivalently it is the operator Schur complement of the scalar elliptic first-row block. This formula needs the stated regularity and coercivity for differentiation of the minimizing branch; it is not asserted at every degenerate minimizer.

The missing positive estimate is a bound for the mixed block relative to both diagonal blocks along nonaffine compatible minimizers. Pointwise rank-one convexity does not by itself sign this variable-coefficient vectorial quadratic form. Writing (8.1) is not a new positivity theorem. It identifies why another conditional minimization can return the same coupled obstruction in a nonlocal operator.

A scalar component solver can still be useful in a counterexample search. It has a unique global minimizer and the residual bound (4.4), without target-translation size, phase charts, winding or an artificial mass parameter. This is standard convex elimination, not a claimed fundamentally new method or a complexity guarantee.

No new low-frequency alternating search or positive fixed-phase certificate is presented as progress in this run. The compatible constructions executed here are exact countertests to claimed reduced convexity. They do not have negative quasiconvexity gaps. The previously retained positive multidirectional witnesses are not relabelled as new outputs.

## 9. Verification record and research decision

Run:

    python verify_direction_obstruction.py

The script uses SymPy and Python standard-library exact arithmetic. It reads no optimizer output or prior verification file. Its twelve check groups reconstruct: all-35 quartic Euler/Picone identities; the rank-one remainder and residual-dual constant; the density/phase Hessian; general-p spectral square completion; exact rational and algebraic trial energies; the two-dimensional reduced-energy countertest; the actual boundary-preserving translation gradient; all-35 quartic perturbation identities; the fixed-mass expansion; translated radial-test differences; and Schur square completion.

`audit/verify_directional_density.py` is a copy of the previous supplied verifier. Its execution completed with ten groups passing. The new results do not assume the correctness of the prior interval implementation or the earlier contact classifications. They use the directly reconstructed perspective and Picone argument and the explicit positive rank-one-value hypothesis.

The following are analytic, not certified by finite algebra: the convex direct method, compact embedding, lower semicontinuity, implicit-function theorem, the identification of its local critical density as the global minimizer, and the O(R^-1) variational comparison. Complete arguments and assumptions are given above. No external review or formal validation is claimed.

### Assessment

The amplitude reduction is correct and useful as a conditional convex solve. The present theorems show that it has not removed the global sign difficulty:

* the true reduced direction energy can be nonconvex;
* complete radial optimality across translation centers is equivalent to the original Euler equation;
* arbitrarily flat directions, even after global amplitude optimization, retain arbitrary Cartesian residual fields and their original minimized energy.

Accordingly, concentrated inference on further fixed-direction certificates or the same alternating amplitude/phase iterations is not presently justified as a route to the complete theorem. This is a judgment about the evidence and representation studied, not about the age or open status of the mathematical problem.

A justified reopening would require an actual coupled stress/Schur estimate along nonaffine compatible minima, a different global structure not obtained merely by eliminating one convex block, or an independently rank-one-convex integrand with a rigorously negative compatible field. No such mechanism is supplied here. The current branch should be preserved for independent verification rather than presented as converging to a foundational breakthrough.

## Sources and provenance

[1] L. Brasco and G. Franzina, *Convexity Properties of Dirichlet Integrals and Picone-type Inequalities*, arXiv:1403.0280v2 (2014), especially Sections 2 and 3. The primary HTML text was read. Hidden convexity, perspectives and Picone equivalences are prior mathematics. https://arxiv.org/html/1403.0280v2

[2] A. Levitt, *The many disguises of the Schur complement*, author-hosted note, especially Sections 1, 4 and 6. The PDF was read and its second page rendered. Schur elimination, inertia and reduced-Hessian structure are standard. https://www.imo.universite-paris-saclay.fr/~antoine.levitt/schur.pdf

[3] G. Bruno and F. Pasqualotto, *Quasiconvexity for the Dacorogna--Marcellini Energy*, arXiv:2608.06367v1 (2026), Theorems 1 and 2. The latter requires both left and right rotational invariance. No theorem for the complete left-invariant cone is imported. https://arxiv.org/html/2608.06367v1

[4] Supplied prior artifact `PHASE_DENSITY_COMPATIBILITY.md` and its exact verifier. Read in full; the load-bearing perspective, Picone and scalar-existence claims were reconstructed.

A further primary partial-optimization webpage fetch failed, and targeted searches did not establish priority for the specific examples or the quantitative translation comparison. Absence of a matching retrieved theorem is not evidence of novelty. No claim about another research problem's relative success probability is made. No third-party manuscripts are redistributed and no repository was modified.
