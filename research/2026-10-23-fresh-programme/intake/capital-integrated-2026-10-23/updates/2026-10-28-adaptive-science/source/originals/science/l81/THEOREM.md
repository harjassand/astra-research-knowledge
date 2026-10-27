# A finite value-only covariance correction, with its implemented law

This is an internally derived intermediate construction for N687. It is not the requested polylogarithmic compiler and is not a priority claim. It combines frozen R22's two-value action with standard Gaussian martingale and Stein identities. The authorized helper independently reconstructed the law bound and challenged the single-action version; its detailed argument is retained in `helper/CHALLENGE.md`.

Throughout, TV(P,Q)=sup_A |P(A)-Q(A)|. Matrix norms are operator or Frobenius as indicated. Exact Gaussian vectors, scalar square roots, arithmetic and whole-vector g values are the runtime primitives. All Hessians, covariance matrices and Stein kernels below are analysis objects, not algorithm inputs.

## 1. Class and acquired covariance action

Let g=grad F:R^d -> R^d be globally L-Lipschitz, F in C^{1,1}; nonconvex fields are allowed. Let mu=E g(G), Sigma=Cov(g(G)). Gaussian Poincare gives 0<=Sigma<=L^2 I. Define H_s(c)=E Dg(c+sZ), using the weak derivative in the proof only.

The R22 heat action on a supplied v!=0 is

    u=v/||v||,
    Zperp=Z0-(u.Z0)u,
    R=s sqrt(A1^2+A2^2+A3^2),
    J_s(c;v)=||v|| [g(c+sZperp+Ru)-g(c+sZperp-Ru)]/(2R).

It costs two g values and satisfies E[J_s(c;v)|c,v]=H_s(c)v and ||J_s(c;v)||<=L||v|| on every execution. For v=0 return zero. Null events R=0 can be assigned zero. The proof is the line-segment derivative identity and the classical representation U chi_3 ~ N(0,1) for independent U uniform[-1,1]. No limiting difference quotient is used.

Draw T uniform[0,1], C standard Gaussian, put c=sqrt(T) C and s=sqrt(1-T), and compose two independent heat actions at these SAME c,s:

    J_Sigma(v)=J_s^{(2)}(c; J_s^{(1)}(c;v)).

Uniform T can be generated from three scalar Gaussians by (1+A/sqrt(A^2+B^2+C^2))/2. The event T=1 is null. This operation uses FOUR g values.

**Covariance-action theorem.** For every supplied v independent of the fresh seeds,

    E[J_Sigma(v)|v]=Sigma v,
    ||J_Sigma(v)||<=L^2||v||.

To prove it, let B_t be Brownian motion. The martingale E[g(B_1)|B_t] has integrand H_sqrt(1-t)(B_t), so Ito isometry gives

    Sigma=integral_0^1 E[H_sqrt(1-t)(sqrt(t)C)^2]dt.

Conservativity makes H symmetric. Conditional expectation of the two fresh actions is H^2v. This is not a product of unconditional heat means. Freshness of the second action remains valid after observing the first vector.

For fresh standard Gaussian v, R22's fixed-center convex-order word bound also gives E[J_Sigma(v)J_Sigma(v)^T]<=L^4 I. It does not give a realized common matrix or a Gaussian output.

## 2. Actual positive sampler

Choose positive integers n,k, sigma>0, and tau,eta>0 with tau^2+eta^2=sigma^2. Draw independent G_1,...,G_n,Z,W standard Gaussian vectors. Use k independent covariance actions conditionally on retained Z. Return

    Y=(1/n) sum_i g(G_i) + tau Z
        -(1/(2 tau n k)) sum_{j=1}^k J_Sigma,j(Z) + eta W.       (A)

All action seeds are fresh, independent of G_i, and independent between calls conditional on Z. W is reserved until the final addition and unused by every query.

This is a finite positive random-vector map. It has a deterministic cap of n+4k whole-vector queries on EVERY execution. It uses O((n+k)d) vector arithmetic and O(d) streaming storage, outside the g oracle. No mean, matrix, derivative, potential-value, density, rejection, or stopping oracle is used.

**Implemented full-law theorem, all n,k>=1.**

    TV(Law(Y), N(mu,sigma^2 I))
       <= L^2 sqrt(d)/(2 eta^2 n^(3/2))
        + L^4 sqrt(d)/(8 eta^2 tau^2 n^2)
        + L^4 d/(8 eta^2 tau^2 n^2 k).                         (B)

The constants in (B) are rounded upward from the proof. In particular, with tau=eta=sigma/sqrt(2), r=L/sigma,

    TV <= r^2 sqrt(d)/n^(3/2)
          + r^4 sqrt(d)/(2n^2) + r^4 d/(2n^2k).               (C)

No n>L^2/sigma^2 assumption is needed. This is a full-law inequality, not an inference from moment diagnostics.

### 2.1 Stein matrix of the ordinary average

The full Gaussian resolvent K=K_1 from frozen R22 satisfies delta_gamma K=g-mu and ||K||op<=L. Weak Gaussian integration by parts and the Lipschitz chain rule give a valid Stein matrix for X=g(G):

    T(G)=K(G)Dg(G)^T,
    E[(X-mu).f(X)]=E[T:Df(X)],
    ||T||op<=L^2,  E T=Sigma.

For a direct weak derivation independent of higher kernel regularity, let P_t be the Gaussian OU semigroup, P_t f(y)=E f(exp(-t)y+sqrt(1-exp(-2t))Z). Set K(y)=integral_0^infinity exp(-t)P_t[Dg](y)dt. Gaussian integration by parts gives d/dt E[(P_t g_i)f]=-E[grad(P_t g_i).grad f], while grad(P_t g_i)=exp(-t)P_t[grad g_i]. Integrating from zero to infinity proves E[(g_i-mu_i)f]=E[K_i.grad f]. The bound ||K||op<=L follows by integration. Gaussian mollification and dominated convergence extend the identity to the raw Lipschitz field. Thus this proof uses no unproved high-order kernel regularity and never acquires K or Dg.

Only sym(T) matters for scalar Hessians. For U=(1/n)sum_i g(G_i)-mu, use

    T_U=n^(-2)sum_i T(G_i).

Independence and the Frobenius operator bound give

    E||sym(T_U)-Sigma/n||F^2 <= L^4 d/n^3.                   (D)

The weak chain rule is legitimate for bounded smooth tests; Gaussian convolution next supplies regularity for arbitrary measurable events.

### 2.2 Deterministic-action comparison

Temporarily define an unimplemented comparison variable

    Y*=mu+U+MZ+eta W,
    M=tau I-Sigma/(2 tau n),
    Q=Sigma^2/(4 tau^2 n^2).

Sigma is NOT supplied to (A). It is used only to compare laws. For t in [0,1] interpolate

    X_t=mu+sqrt(t)U+N(0,C_t),
    C_t=sigma^2 I-t Sigma/n+Q.

Since Sigma is PSD,

    C_t=C_1+(1-t)Sigma/n >= C_1=M^2+eta^2 I >= eta^2 I.

At t=0 the law is N(mu,sigma^2 I+Q); at t=1 it is Law(Y*). For each measurable A, Gaussian differentiation and (D) imply

    d/dt P(X_t in A)
      =(1/2)E[(T_U-Sigma/n):Hess P_Ct 1_A(mu+sqrt(t)U)].

For every symmetric R and C>=eta^2 I, the centered indicator and Gaussian quadratic-form variance identity give

    |R:Hess P_C 1_A(x)| <= ||R||F/(sqrt(2) eta^2).             (E)

Indeed split C=eta^2 I+(C-eta^2 I), differentiate the first Gaussian, and use E[(Z^TRZ-tr R)^2]=2||R||F^2 with ||1_A-1/2||infinity<=1/2. Integrating gives TV(Y*,N(mu,sigma^2 I+Q)) <= L^2 sqrt(d)/(2sqrt(2)eta^2 n^(3/2)). A Gaussian covariance interpolation gives TV(N(mu,sigma^2 I+Q),N(mu,sigma^2 I))<=||Q||F/(2sqrt(2)sigma^2). Replacing sigma^2 by eta^2 and rounding constants upward gives the first two terms of (B).

### 2.3 Implemented nonlinear randomization

Condition on U,Z and define

    Delta= -[Jbar_Sigma(Z)-Sigma Z]/(2 tau n).

Conditional unbiasedness gives E[Delta|U,Z]=0. Independence of k calls and the deterministic action bound give

    E||Delta||^2 <= L^4 d/(4 tau^2 n^2 k).                    (F)

Apply Taylor's formula to P_{eta^2 I}1_A at mu+U+MZ. Its first-order conditional term is zero. Equation (E), for R=Delta Delta^T, bounds the integrated second-order remainder by E||Delta||^2/(2sqrt(2)eta^2), hence by the last term of (B) after rounding upward. This charges the actual nonlinear action's randomization, rather than replacing it inside an exponential by its mean.

## 3. Accuracy, query and exact covariance scope

At fixed positive sigma/L, n,k of order d^(1/3) epsilon^(-2/3) make (C)<=epsilon, with constants depending on the ratio. A less wasteful k is of order d/(epsilon n^2) after n is chosen so the first two terms are below epsilon. All schedules are deterministic. Thus a simple sufficient query bound is

    O_{sigma/L}(d^(1/3) epsilon^(-2/3)).

For an explicit schedule choose n at least the ceiling of the maximum of 1, (3r^2 sqrt(d)/epsilon)^(2/3), and (3r^4 sqrt(d)/(2epsilon))^(1/2); choose k at least max(1,ceil(3r^4 d/(2epsilon n^2))). Each term of (C) is <=epsilon/3. For 0<epsilon<1 and fixed ratio this has the displayed asymptotic order. Query count is n+4k on every seed realization, with polynomial arithmetic/storage.

Exactly, E Y=mu. With V=E[J_Sigma(Z)J_Sigma(Z)^T]-Sigma^2>=0,

    Cov(Y)=sigma^2 I+[Sigma^2+V/k]/(4 tau^2 n^2),
    0<=V<=L^4 I-Sigma^2.

Covariance is generally too large; exact matching is not claimed. Affine g(x)=Ax+b, A symmetric, gives J_Sigma(v)=A^2v pathwise and the EXACT output law

    Y ~ N(b, sigma^2 I+A^4/(4 tau^2 n^2)).

Rounding the exact output and target by the same map preserves the TV upper bound by data processing. The NumPy implementation is a floating-point diagnostic of the exact-real program; it does not prove uniformly bounded bit lengths for arbitrary oracle reals. Secant constant offsets cancel algebraically; large offsets can require explicit centering in numerical work.

## 4. Competitors and consequence

The same Stein/smoothing interpolation gives the ordinary independent-average sampler gbar_N+sigma Z a bound L^2 sqrt(d)/(2sigma^2 N), hence sufficient cost O_{sigma/L}(sqrt(d)/epsilon). Formula (B) improves this simple query bound using the same legal source information.

This does not establish a best available N687 sampler: frozen R16 is an asymptotically stronger arbitrary-fixed-positive-exponent proof candidate, under its recorded candidate/audit status. Cloud/FORS mechanisms in frozen R21 have their own contracts and can be stronger in their regimes. This construction uses no supplied covariance or exact expectation oracle. The supplied-Sigma comparison is analysis only. The numerical sin and affine examples have analytically easy means: they validate implementation and expose defects, and cannot establish practical advantage over algorithms exploiting those formulas.

The target requires poly(log d,log(1/epsilon)) values, rather than polynomial dimension and accuracy dependence. The present map removes the leading covariance effect of averaging but leaves averaged Stein fluctuation, covariance-squared error and implemented randomization. It does not implement a Newton iteration or prove a superlinear update that can be reapplied to its own output.
