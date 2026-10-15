# Compact operator distributions: an independent constructive proof

Status: independent internal reconstruction, 2026-10-15. External correctness and historical novelty are UNKNOWN. No formal verification, finite-cost kernel compiler, or quantum advantage is asserted.

This proof was developed from the supplied pasted claim. The frozen PR94 producer proof was subsequently read and preserved in `sources/PR94_PRODUCER_PROOF.md`. Its stated Banach-cone and unital C*-algebra scope already includes the operator theorem below; its Section 9 already contains common-family sufficiency. Thus neither infinite Hilbert dimension nor common-family sufficiency is claimed here as an extension beyond that raw source. The physical-radius ramp construction and the explicit necessary-and-sufficient family formulation below are an independent reconstruction and an explicit consequence, respectively.

## 1. Exact theorem and conventions

Let m be a positive integer and H any complex Hilbert space. Let T be a compactly supported, norm-continuous, B(H)-valued distribution on R^m. Assume T(h) is self-adjoint for real h and T(1)=I. Evaluation on noncompact smooth functions means insertion of any smooth cutoff equal to one near supp T.

Choose finite data a>=1, N>=0, and C>=1 such that, for every smooth h,

    ||T(h)|| <= C max_{|alpha|<=N} sup_{|y|<=a}|partial^alpha h(y)|.       (1)

The support lies strictly inside the chosen ball. A compact distribution has such data after cutoff differentiation is absorbed into C. Put

    H_T(g) = T(exp(g.y)),       g in R^m.

The following are equivalent:

1. For every real g there is lambda_g>0 with H_T(g)>=lambda_g I.
2. Some scalar probability measure nu with integral exp(b|z|)nu(dz)<infinity for every b>=0 makes T*nu a positive operator-valued distribution.
3. For every epsilon in (0,1), there is a scalar probability density p=Z^{-1}exp(-V) such that V is smooth, radial and strictly convex, every derivative of p decays faster than every exponential and is integrable against every exponential, and

    (1-epsilon)p(x)H_T(grad V(x)) <= (T*p)(x)
          <= (1+epsilon)p(x)H_T(grad V(x))                         (2)

at every x. In particular T*p is a smooth pointwise coercive positive operator density, norm integrable with total integral I. Its every derivative is norm integrable against every exponential.

Positivity in condition 2 means (T*nu)(phi)>=0 for every real nonnegative compactly supported smooth phi. It automatically defines a normalized weakly countably additive POVM, as proved below. Norm countable additivity is not assumed. The noise is scalar and independent of the input state.

The term coercive means a positive lower spectral bound, not merely a strictly positive quadratic form on each nonzero vector.

## 2. Continuity and compact-tilt margins

Differentiating exp(g.y) on a fixed y-ball shows that g -> H_T(g) is norm continuous (indeed norm entire after complexification). For a bounded self-adjoint operator A, write ell(A)=inf_{||v||=1}<v,Av>. Then

    |ell(A)-ell(B)| <= ||A-B||.

Consequently condition 1 implies

    lambda_n = min_{|g|<=n+1} ell(H_T(g)) > 0,       n=0,1,... .     (3)

These numbers may decay arbitrarily quickly. The proof uses no predetermined lower envelope. It is qualitative unless certified lower bounds for them are supplied.

## 3. A local error estimate, including every derivative used by T

Set K=max(2,N) and B=m(1+a)^2. Suppose V is smooth and real, fix x, and assume

    max_{2<=|alpha|<=K} sup_{|z-x|<=a}|partial^alpha V(z)| <= eta,
    B eta <= 1.                                                  (4)

Put g=grad V(x) and

    F_x(y)=V(x-y)-V(x)+g.y.

Taylor's integral formula gives |F_x(y)| <= m a^2 eta/2. For a first partial derivative, the fundamental theorem of calculus gives

    |partial_{y_j}F_x(y)|
       = |partial_j V(x)-partial_j V(x-y)|
       <= sqrt(m)a eta.

For 2<=|alpha|<=N, the corresponding derivative of F_x is, up to sign, partial^alpha V(x-y), hence is at most eta. Therefore

    ||F_x||_{C^N(B_a)} <= B eta <= 1.                             (5)

Let b_j be the j-th Bell number, the number of partitions of a set of j labeled elements, with b_0=1, and let b_*=max_{0<=j<=N}b_j. For j>=1 the chain rule in its partition form is

    partial_{i_1}...partial_{i_j} exp(-F)
      = exp(-F) sum_{pi partition of {1,...,j}}
          product_{A in pi}(-partial_{i_A}F).

Every product has at least one factor and is bounded by B eta because B eta<=1. The undifferentiated difference obeys |exp(-F)-1|<=e|F|. Thus, including order zero,

    ||exp(-F_x)-1||_{C^N(B_a)} <= e b_* B eta.                    (6)

This remains valid when N=0 or N=1; the second derivative in K is what supplies Taylor's estimate.

The exact identity

    p(x-y)=p(x)exp(g.y)exp(-F_x(y))

then gives

    (T*p)(x)/p(x) = H_T(g)+E_x,
    E_x=T(exp(g.y)(exp(-F_x(y))-1)).                              (7)

Leibniz's rule bounds each derivative of the product by

    exp(a|g|)(1+|g|)^N ||exp(-F_x)-1||_{C^N(B_a)}.

With the explicit scalar constant

    A_0=C e b_* B,

we obtain

    ||E_x|| <= A_0 exp(a|g|)(1+|g|)^N eta.                       (8)

E_x is self-adjoint. If ||E_x||<=epsilon ell(H_T(g)), then

    ||H_T(g)^(-1/2) E_x H_T(g)^(-1/2)|| <= epsilon,               (9)

which proves (2). The inverse-conditioning factor is included in (9); a small absolute error alone would not suffice in a remote tail.

## 4. Explicit constants for Cartesian derivatives of radial functions

The construction below is in physical radius. This section supplies the angular derivative bounds.

For k>=1 define the computable positive rational number

    A_k = sum_{pi: partition of {1,...,k}, every block size <=2}
             |(1/2)_{|pi|}| 2^{|pi|},                           (10)

where (t)_j=t(t-1)...(t-j+1) is a falling factorial. Since r(x)=sqrt(sum x_j^2), the partition chain rule, |partial_j(r^2)|<=2r, |partial_j partial_k(r^2)|<=2, and all higher derivatives of r^2 zero give

    |partial_{i_1}...partial_{i_k}r(x)| <= A_k r^{1-k}, r>0.       (11)

Exactly the same argument gives

    |partial^alpha sqrt(L^2+|x|^2)|
          <= A_{|alpha|}(L^2+|x|^2)^{(1-|alpha|)/2}.              (12)

For 1<=ell<=j put

    B_{j,ell}=sum_{pi partition of {1,...,j}, |pi|=ell}
                    product_{A in pi} A_{|A|}.

For every one-variable smooth u and r>0, (11) and the same chain rule yield

    |partial_{i_1}...partial_{i_j}u(r)|
       <= sum_{ell=1}^j B_{j,ell}|u^{(ell)}(r)|r^{ell-j}.         (13)

All constants here are finite explicit partition sums. Mixed coordinate derivatives are included; no Hilbert basis or Hilbert dimension enters.

Choose one fixed C-infinity nondecreasing step theta, zero on (-infinity,0] and one on [1,infinity). A concrete choice is the normalized integral of

    b(t)=exp(-1/[t(1-t)]),  0<t<1,       b(t)=0 otherwise.

Let d_k=sup_t|theta^{(k)}(t)| for k>=1. These are finite constants of one fixed explicitly given scalar function. They can be bounded numerically with certification if a numerical compiler is required; no unknown input margin is hidden in them.

Define

    D = 1 + max_{2<=j<=K}
          ( A_j + B_{j,1} + sum_{ell=2}^j B_{j,ell}d_{ell-1} ).   (14)

## 5. Delayed ramps: a complete construction

For a specified epsilon in (0,1), choose the nonincreasing positive tolerances

    beta_n=min(1/B,
       epsilon lambda_n/[A_0 exp(a(n+1))(n+2)^N]), n>=0.          (15)

Choose

    L_0 >= max(1, max_{2<=j<=K}A_j/beta_0),
    L_n = max(1,4D/beta_n), n>=1.                               (16)

Choose finite starting radii recursively:

    R_1=max(2a+2, 2a+4D*2/beta_1),
    R_n=max(R_{n-1}+L_{n-1}+4a+2,
            2a+2, 2a+4D(n+1)/beta_n), n>=2.                    (17)

Increasing any radius or width further is harmless provided the separation condition is retained. In particular one may impose any additional finite radius lower bounds.

Set

    q(r)=r/sqrt(L_0^2+r^2)
                + sum_{n>=1} theta((r-R_n)/L_n), r>=0,
    V(x)=sqrt(L_0^2+|x|^2)-L_0
                + sum_{n>=1} integral_0^{|x|}theta((t-R_n)/L_n)dt. (18)

The sums are locally finite because the radii strictly escape to infinity. Every ramp vanishes near the origin; the base potential is smooth on all R^m. Hence V is C-infinity. Its radial derivative is q. For r>0,

    q(r)>0,
    q'(r)=L_0^2/(L_0^2+r^2)^(3/2)
                     + sum_n L_n^(-1)theta'((r-R_n)/L_n)>0.      (19)

The radial and tangential Hessian eigenvalues are q'(r) and q(r)/r, respectively. Both are positive, and the Hessian at zero is L_0^(-1)I. Thus V is strictly convex everywhere, including every plateau between ramps.

After ramp n is completed q(r)>=n. Therefore q(r)->infinity and

    V(r)/r -> infinity.                                        (20)

For example, for any J choose a finite r_J after J ramps. For r>=r_J, V(r)>=J(r-r_J), so liminf V(r)/r>=J. This proves (20) without a rate assumption.

## 6. Uniform local jets, including every remote tail

First suppose |x|<R_1-a. For |z-x|<=a one has |z|<R_1, so there is no ramp contribution. Equations (12) and (16) give the bound (4) with eta=beta_0. Also |grad V(x)|<1.

Otherwise there is a unique n>=1 with

    R_n-a <= |x| < R_{n+1}-a.                                  (21)

For |z-x|<=a,

    R_n-2a <= |z| < R_{n+1}.                                   (22)

The lower radius is at least 1. All ramps before n have finished there by the separation in (17), and all ramps after n have not begun. Thus at most the n-th ramp has nonzero derivatives of its slope in this entire neighborhood. The sum of ramp slopes is at most n. Using (12), (13), r=|z|>=1 and L_n>=1 gives, for 2<=j<=K,

    max_{|alpha|=j}|partial^alpha V(z)|
      <= A_j/r^{j-1} + B_{j,1}n/r^{j-1}
           + sum_{ell=2}^j B_{j,ell}d_{ell-1}
                         L_n^{-(ell-1)}r^{ell-j}
      <= D[(n+1)/r+1/L_n]
      <= beta_n/2 <= beta_n.                                  (23)

The term n/r in (23) is the angular contribution. Increasing ramp width alone would not control it; the lower bound on R_n is essential. Arbitrarily remote neighborhoods are covered by (21), with no truncation radius.

At x in this band, |g|=q(|x|)<n+1. Combining (8), (15) and (23),

    ||E_x||<=A_0 exp(a(n+1))(n+2)^N beta_n
            <=epsilon lambda_n<=epsilon ell(H_T(g)).            (24)

The initial band has exactly the same estimate with n=0. Equation (9) proves the global relative inequalities (2). This completes the positivity part of sufficiency.

## 7. Exponential decay, derivatives, normalization and integration

The construction gives q(r)<=1+r: before R_1 the base slope is at most one, while in the n-th radial band q<=n+1 and R_n>=n+1. Equations (12)-(13), L_n>=1 and R_n>=n+1 also show, for every fixed j>=2, that

    sup_x max_{|alpha|=j}|partial^alpha V(x)| < infinity.         (25)

For j>K the constant can depend on j and the fixed step theta, but not on n. This conclusion follows from the same expression as the first three lines of (23), replacing D by the analogous finite D_j; no tolerance beta_n for j>K is needed.

The partition chain rule now gives, for every multi-index alpha,

    |partial^alpha exp(-V(x))|
          <= C_alpha(1+|x|)^{|alpha|}exp(-V(x)).                 (26)

Since V(r)/r->infinity, (26) proves both

    exp(b|x|)|partial^alpha p(x)| -> 0 as |x|->infinity,
    integral exp(b|x|)|partial^alpha p(x)|dx < infinity           (27)

for every b>=0 and alpha. In particular 0<Z=integral exp(-V)<infinity, and p=Z^{-1}exp(-V) is an everywhere positive radial strictly log-concave probability density.

The map x -> (y -> p(x-y)) takes values continuously in C^N(B_a), and its C^N norm is integrable against every exp(b|x|). To see this directly, use (26), (20) and |x-y|>=|x|-a. The same argument works with any extra x derivatives. Hence applying T is legitimate under the Bochner integral, using the bounded extension of (1) to the closure of smooth restrictions in C^N(B_a). For each y,

    integral p(x-y)dx=1,
    integral partial_y^alpha p(x-y)dx=0 for |alpha|>0,

with the latter justified by (27). Therefore

    integral (T*p)(x)dx = T(1)=I.                              (28)

All derivatives of T*p are norm integrable against every exponential by the same bound. This argument does not use finite-dimensional truncations or scalarization to prove normalization.

## 8. Necessity with arbitrary all-exponential probability noise

Here is an elementary smoothing proof that avoids unbounded exponential tests until absolute weighted bounds have been established.

First, a positive distribution S=T*nu is automatically normalized. Take smooth radial cutoffs chi_R, equal to one on B_R and zero outside B_{2R}, increasing to one. On B_a,

    integral chi_R(y+z)nu(dz) -> 1 in C^N.

For order zero the error is at most nu(|z|>R-a); higher derivative errors are at most fixed constants times R^{-|alpha|}. Equation (1) yields S(chi_R)->I in norm. Each scalar distribution <v,S(.)v> is positive and thus is a Radon measure mu_v. Monotone convergence gives mu_v(R^m)=||v||^2. Polarization produces a normalized weakly countably additive POVM M representing S.

Choose a nonnegative compactly supported C-infinity probability density rho, supported in B_b. The positive smoothing

    F(x)=integral rho(x-z)M(dz)

exists as a bounded operator, is positive, and has integral I. Convolution associativity gives F=T*q with q=nu*rho. This equality may first be read distributionally; both sides are norm-smooth functions, so it is pointwise.

For |alpha|<=N define the compactly supported nonnegative envelope

    k_alpha(w)=sup_{|y|<=a}|partial^alpha rho(w-y)|.

Then

    sup_{|y|<=a}|partial^alpha q(x-y)|
           <= integral k_alpha(x-z)nu(dz).                     (29)

For each real g, the exp(g.x)-weighted integral of the right side is

    m_nu(g) integral exp(g.w)k_alpha(w)dw < infinity.             (30)

Consequently T may be interchanged with the exponential integral in Banach norm, and

    integral exp(g.x)F(x)dx=m_nu(g)m_rho(g)H_T(g).               (31)

On the other hand, positivity allows Tonelli after scalarizing, without presupposing a moment of M:

    integral exp(g.x)<v,F(x)v>dx
       =m_rho(g) integral exp(g.z)mu_v(dz).                     (32)

Equations (31)-(32), and m_rho(g)>0, show that the original POVM has bounded exponential moments in every direction and

    Q(g):=integral exp(g.z)M(dz)=m_nu(g)H_T(g),                  (33)

where the original integral is the bounded positive weak integral. For a unit vector v, Cauchy-Schwarz in the scalar probability measure mu_v gives

    <v,Q(g)v><v,Q(-g)v> >= 1.

As <v,Q(-g)v><=||Q(-g)||, it follows that

    H_T(g) >= [m_nu(g)m_nu(-g)||H_T(-g)||]^{-1}I.               (34)

The denominator is finite and positive. This proves coercivity on arbitrary H and completes necessity. Only finite moments at g and -g were used for this last estimate. Normalization and positivity were derived from the distributional convolution rather than assumed for an arbitrary weak POVM.

## 9. Exact common-family criterion and dimension uniformity

Let {T_omega} be any indexed family, with possibly different Hilbert spaces H_omega. Assume all T_omega satisfy (1) with the same m,a,N,C and are self-adjoint with T_omega(1)=I_omega. Then the following are equivalent:

1. For every finite t,

    inf_{omega, |g|<=t} ell(H_{T_omega}(g)) > 0.                 (35)

2. One scalar probability measure nu having every exponential moment makes every T_omega*nu positive.
3. For every epsilon in (0,1), one scalar smooth radial strictly log-concave probability density p with (27) makes (2) hold simultaneously for every omega and every x.

For sufficiency replace (3) by the infimum over omega as well and use exactly the same construction. Its constants do not depend on Hilbert dimension or the cardinality of the family.

For necessity, (1) gives

    ||H_{T_omega}(-g)|| <= C exp(a|g|)(1+|g|)^N.

Applying (34) separately but with the common nu yields the explicit uniform bound

    H_{T_omega}(g) >=
       [C exp(a|g|)(1+|g|)^N m_nu(g)m_nu(-g)]^{-1}I_omega.       (36)

For |g|<=t, both noise moments are at most integral exp(t|z|)nu(dz), so (35) follows. This proves the exact common-family criterion.

Under the common data, (35) can equivalently be replaced by uniform coercivity separately at each fixed g, namely inf_omega ell(H_{T_omega}(g))>0. Indeed, for |g|,|h|<=t, differentiate along the line segment. Leibniz's rule applied to y_j exp(k.y) and (1) give

    ||H_{T_omega}(g)-H_{T_omega}(h)|| <= L_t |g-h|,
    L_t=sqrt(m)C(a+N)exp(at)(1+t)^N.                            (37)

This bound is uniform in omega. Thus g -> inf_omega ell(H_{T_omega}(g)) is L_t-Lipschitz on the tilt ball. If it is positive at every point, compactness gives a positive ball minimum. Equation (37) also explains what a finite tilt-net certificate would require; positivity recognition is not supplied by the theorem.

This family result is already implicit in the frozen producer's general Banach-cone theorem: use the Banach space of bounded self-adjoint operator families with the sup norm and its product positive cone. It is presented explicitly because it identifies the precise uniform obstruction and the required data, not as a newly cleared theorem.

For a compact parameter space Omega and a fixed Hilbert space (or a fixed common Banach ambient algebra), a continuous family in the common C^N operator-seminorm topology has norm-continuous H_{T_omega}(g) jointly in omega,g. Pointwise coercivity then gives (35) by compactness. Thus a compact continuous parameter family admits one regularizer. Mere pointwise coercivity without compactness or a uniform margin does not suffice.

## 10. Sharp scope checks

### Strict quadratic positivity does not imply coercivity

On ell^2(N) define the diagonal compact signed-measure distribution with scalar entries

    T_n=[(1/16)delta_2+delta_{-2}+(-1/2+1/n)delta_0]/(9/16+1/n).

Each has total mass one and total variation at most 25/9, so their diagonal sum is a norm-continuous operator distribution of order zero, with common compact support {-2,0,2}. Its real Laplace entries are

    H_n(g)=[sinh^2(g-log 2)+1/n]/(9/16+1/n)>0.

Every nonzero vector has a positive quadratic form at every real g. But

    H_n(log 2)=16/(9n+16) -> 0.

Thus the operator transform is not coercive at log 2. No common all-exponential regularizer exists for all scalar entries; equivalently the infinite diagonal distribution has none. Every finite truncation does have one. This is the supplied counterexample, independently verified algebraically here.

### The uniform distribution bound in the family theorem matters

The scalar family T_A=delta+A delta'', A>0, has H_A(g)=1+A g^2>=1, common support {0}, and common order two, but no common finite seminorm constant C. There is no common probability noise, even if arbitrary nonsmooth noise is allowed. Otherwise smooth it by rho as above to obtain an integrable smooth probability density p with p+A p''>=0 for every A>0. Letting A->infinity gives p''>=0. An integrable nonnegative convex function on R is identically zero, a contradiction. Therefore uniform compact-tilt margins alone cannot replace the full common-data hypotheses.

## 11. A bounded-slope localized consequence

For any fixed radius c>0, the same physical-radius construction has the following variant. If H_T(g) is coercive for every |g|<c, there is an everywhere positive smooth radial strictly log-concave scalar density p whose exponential-moment domain is exactly the open ball |g|<c, and T*p is a positive normalized operator density. Conversely, existence of such a scalar noise implies coercivity throughout that ball.

To adapt the construction, choose base terminal slope c/2 and positive ramp increments alpha_n=c/2^{n+1}, n>=1, whose total with the base is c. Replace the base potential by (c/2)(sqrt(L_0^2+r^2)-L_0) and each ramp term by alpha_n times the corresponding term in (18). On band n the slope is at most s_n=c(1-2^{-(n+1)})<c. Use compact-tilt margins on |g|<=s_n and replace the n in (23) by the sum of the first n increments. Choose radii and widths by the same inequalities, increasing them when necessary. The local error proof is unchanged. The slope q(r) is strictly increasing, remains below c, and tends to c.

Hence V(r)/r->c, giving every interior exponential moment. Moreover V(r)<=cr (since V(0)=0 and q<c). For any unit u and x=tu+z with z perpendicular to u, |z|<=1 and t>=1,

    exp(c u.x-V(x)) >= exp(-c),

because |x|<=t+1. Integration over this infinite fixed-radius cylinder shows that every boundary moment |g|=c diverges; exterior moments diverge as well. The same reasoning gives weighted derivative integrability on strictly smaller moment balls. Necessity uses (29)-(33) at interior g and -g only.

This is a routine bounded-slope consequence of the mechanism, not a historical-priority claim. It localizes the positivity obligation to the chosen noise moment domain; the all-exponential theorem is its unbounded-slope endpoint.

## 12. What remains unestablished

The proof is explicit conditional on a valid finite-order seminorm bound and certified positive compact-tilt lower bounds. It supplies no efficient way to recognize those bounds, compute the necessary infinitely many radii, sample the resulting density, optimize its variance, compile a POVM, or invert its smoothing stably. Distribution estimates and the family construction are independent of Hilbert dimension, but can depend strongly on m, N, C, support radius, and the entire margin profile.

No external mathematical review or formal proof checker has certified this reconstruction. The source's absent full ZIP/manuscript was not recovered; only the supplied pasted text and the named frozen PR94 proof were used. Historical novelty, exact predecessor exclusion, and practical capability remain UNKNOWN.
