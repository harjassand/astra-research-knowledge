# Independent law analysis of the value-only covariance correction

Scope: mathematical challenge for l81. Read the frozen learning CASE and R22 Sections 8–11. No memory, other trajectories, active checkout changes, external service actions, descendants, or settings changes. All matrix derivatives below are proof objects, never runtime data. The target polylogarithmic compiler is not proved.

## 1. The covariance action is valid

Let X=g(G), mu=EX, Sigma=Cov(X), with globally L-Lipschitz conservative g. Write H_s(c)=E Dg(c+sZ). Brownian conditional expectation gives

    Sigma = integral_0^1 E[H_sqrt(1-t)(sqrt(t)C)^2] dt.

Conservativity makes H symmetric. Draw T uniform[0,1], C Gaussian, c=sqrt(T)C, s=sqrt(1-T). Compose two independent fresh R22 heat-Hessian actions at the same c,s. For each supplied v, the resulting J(v) has E[J(v)|v]=Sigma v and ||J(v)||<=L^2||v||. It costs four original whole-vector g queries, with no derivative or mean call. Conditional independence of the two action seeds, conditional on T,C, is essential. This uses the Brownian covariance identity, not the incorrect product of unconditional heat means.

## 2. A proved full-law bound for the actual positive random map

Fix tau,eta>0, tau^2+eta^2=sigma^2. Let n,m be positive integers. Generate independent X_1,...,X_n, Z,W standard Gaussian and m independent actions J_j, independent of X_i and conditionally independent given Z. Set

    Y = Xbar + tau Z - [1/(2 tau n)] Jbar_m(Z) + eta W.

This is an actual positive random-vector construction. Its deterministic query count is at most n+4m, and its surrounding work is O((n+m)d). Its mean is exactly mu.

Assume n>L^2/sigma^2 and put nu^2=sigma^2-L^2/n. Then

    TV(Law(Y), N(mu,sigma^2 I))
    <= [L^2 sqrt(d)/n^(3/2) + L^4 sqrt(d)/(4 tau^2 n^2)]/(sqrt(2) nu^2)
       + L^4 d/[4 sqrt(2) tau^2 eta^2 n^2 m].                 (1)

Constants here use TV=sup_A |P(A)-Q(A)|. A looser constant-factor version is equally valid.

Proof of deterministic part. The full Gaussian Stein kernel K_1 obeys delta_gamma K_1=g-mu and ||K_1||op<=L. For T_i=K_1(G_i)Dg(G_i)^T, Gaussian integration by parts gives a valid preconditioning Stein matrix for X_i, ||T_i||op<=L^2, and E T_i=Sigma. For U=Xbar-mu,

    T_U=n^(-2) sum_i T_i,
    E||T_U-Sigma/n||F^2 <= d L^4/n^3.

No pointwise derivative is acquired. R22 supplies the needed raw C^{1,1} kernel identity; weak chain rules suffice. Let E0=Sigma^2/(4 tau^2 n^2), and define an interpolation with Gaussian covariance

    Y_t=mu+sqrt(t)U+N(0,C_t),
    C_t=sigma^2 I-t Sigma/n+t E0.

All C_t>=nu^2 I. At t=0 this is the target; at t=1 its law is the deterministic-action version Xbar+(tau I-Sigma/(2 tau n))Z+eta W. For a measurable set A, differentiation and the Stein identity give

    d/dt P(Y_t in A)
      =(1/2) E[(T_U-Sigma/n+E0): Hess P_{C_t}1_A(mu+sqrt(t)U)].

For any fixed matrix R and Gaussian covariance C>=nu^2 I,

    |R:Hess P_C 1_A(x)| <= sqrt(2)||sym R||F/nu^2.

To see this, split C=nu^2 I+(C-nu^2 I), differentiate the first Gaussian, and use E[(W^T sym(R)W-tr R)^2]=2||sym R||F^2. Integrating the displayed derivative proves the first term in (1). Approximation by bounded smooth functions justifies the indicator calculation; uniform positive convolution covariance prevents an endpoint singularity.

Proof of implemented-randomization part. Condition on Xbar,Z and compare to the deterministic action. The additional shift is

    Delta=-[Jbar_m(Z)-Sigma Z]/(2 tau n),
    E[Delta|Xbar,Z]=0,
    E||Delta||^2 <= L^4 d/(4 tau^2 n^2 m).

For f=P_{eta^2 I}1_A, Gaussian differentiation gives |D^2f(x)[v,v]|<=sqrt(2)||v||^2/eta^2 uniformly in x. Taylor expansion with integral remainder cancels the first-order conditional term and bounds the expectation difference by E||Delta||^2/(sqrt(2)eta^2). This is exactly the second term in (1). It explicitly charges action variance and does not assert a realized matrix or Gaussian action law.

For fixed sigma/L, choose tau=eta=sigma/sqrt(2). Taking n and m both a sufficiently large constant times d^(1/3)epsilon^(-2/3) makes all three terms <=epsilon (plus a fixed small-d minimum for n). Thus the bound gives O_{sigma/L}(d^(1/3)epsilon^(-2/3)) deterministic g queries, rather than the independent-average O(sqrt(d)/epsilon) bound. Better allocation can choose m proportional to d/(epsilon n^2) once n is fixed. This remains far from polylog and does not beat the existing fixed-exponent machinery asymptotically at fixed epsilon. It is a finite implemented positive nonlinear correction, not a priority or practical-speedup claim.

## 3. Exact mean/covariance receipts

The implemented mean is exactly mu. Moreover

    Cov(Y)=sigma^2 I + E[Jbar_m(Z)Jbar_m(Z)^T]/(4 tau^2 n^2).

The cross covariance uses E[Z Jbar_m(Z)^T]=Sigma. Fixed-center R22 convex-order receipts imply E[J(Z)J(Z)^T]<=L^4I, and independent averaging also preserves this bound. Thus the covariance error is PSD and at most L^4/(4 tau^2 n^2)I. It is generally nonzero; covariance matching is not claimed. Affine g(x)=Ax+b gives J(Z)=A^2 Z exactly on every execution and

    Y~N(b,sigma^2 I+A^4/(4 tau^2 n^2)).

This affine check verifies signs and factors. Its d^(1/4) accuracy regime does not describe general g.

## 4. Single-action counterfamily: shared T creates a shell mixture

For each d use the genuine smooth conservative field

    g_d(x)_i=sin(x_i),  F_d(x)=-sum_i cos(x_i),  L=1.

Its mean is zero and Sigma=v I, v=(1-exp(-2))/2. Use one covariance action (m=1). Let T be its shared uniform parameter. For the heat action with input v and direction u=v/||v||, the exact component is

    J_s(c;v)_i=v_i cos(c_i+s xi_i-s(xi.u)u_i) sinc(Ru_i),
    R=s chi_3.

Since |J_i|<=|v_i| and |1-sinc(x)|<=x^2/6,

    E[||J_s(c;v)-diag(cos(c+s xi))v||^2 | c,v]
       <= (17/6) max_i v_i^2.

The constants follow by bounding the two terms by 2(xi.u)^2 max_i v_i^2 and (R^4/18)max_i v_i^2, with E R^4<=15. Applying this twice and using |J_1(Z)_i|<=|Z_i| shows that the actual covariance action differs in squared L2 norm by O(log(2d)) from

    Jtilde_i=Z_i B_i,
    B_i=cos(sqrt(T)C_i+sqrt(1-T)xi_i)
        cos(sqrt(T)C_i+sqrt(1-T)xi'_i).

Conditional on T=t the approximate output coordinates are iid. Their variance is exactly

    sigma^2 + [v-q(t)]/n + r(t)/(4 tau^2 n^2),
    q(t)=exp(-1)cosh(t),
    r(t)=[1+2exp(-2)+exp(-4)cosh(4t)]/4.

Conditional fourth moments are uniformly bounded in d,n,t. Consequently, if n=n(d)->infinity and n=o(sqrt(d)),

    n[||Y||^2/d-sigma^2] => v-q(T).

The action-approximation error in this statistic is O(sqrt(log(2d)/d)) in L1; the conditional-coordinate fluctuation is O(n/sqrt(d)) in L2; the r/n term vanishes. The limiting random variable v-q(T) is continuous with no atom at zero. Under the target Gaussian the same statistic tends to zero. A shrinking shell event therefore proves

    TV(Law(Y),N(0,sigma^2 I_d)) -> 1.

For completeness, choose delta_d=n/sqrt(d)+1/n+sqrt(log(2d)/d), threshold a_d=sqrt(delta_d), and event |n(||y||^2/d-sigma^2)|>a_d. The target probability tends to zero; the candidate probability tends to one by the preceding bounds and the atom-free limit.

This is a counterexample to the ONE-action dimension-improvement claim, not a lower bound for the main compiler target or for the batched algorithm in (1). Fixed m leaves a nontrivial shared-parameter mixture too. Batching is therefore mathematically substantive, rather than a cosmetic variance reduction.

## 5. Exact remaining gap

The estimate still spends a polynomial number of values. The randomization term d/(n^2m) is real, as the shared-parameter shell mechanism demonstrates. A polylog upgrade would require an acquired positive correction that removes or recursively squares this implemented full-law defect without recursively producing polynomially many covariance actions. Neither the unbiased action identity nor its convex-order bound supplies that operation.

## 6. Growing action batches: a matching dimension obstruction for this map

The same sine family proves more than the fixed-m case. Let m=m(d) tend to infinity, with n=n(d) satisfying

    n sqrt(m)/sqrt(d) -> 0,     sqrt(m)/n -> 0.

Then the implemented batched map still has TV distance tending to one from its Gaussian target. In particular, n=m=N(d)->infinity with N=o(d^(1/3)) fails. This shows that the dimension exponent 1/3 of the balanced upper-bound allocation cannot be improved for this particular first covariance-action correction simply by a better dimension-only analysis.

Proof. Use independent T_j and the coupled diagonal surrogates above. Conditional on (T_1,...,T_m), approximate coordinates are iid and their variance equals

    sigma^2 + (v-qbar)/n + Rbar/(4 tau^2 n^2),
    qbar=(1/m)sum_j q(T_j),
    Rbar=qbar^2+(1/m^2)sum_j[r(T_j)-q(T_j)^2] <=1.

The fourth moments are uniformly bounded. Jensen applied to the action-approximation errors retains E||Jbar-Jbartilde||^2<=C log(2d). Consequently the actual-versus-surrogate error in the scaled shell statistic n sqrt(m)(||Y||^2/d-sigma^2) is O(sqrt(m log(2d)/d)) in L1. This vanishes under the two displayed conditions: they imply m=o(n^2) and n^2 m=o(d), hence m=o(sqrt(d)). The conditional coordinate fluctuation is O(n sqrt(m)/sqrt(d)), and the quadratic correction is O(sqrt(m)/n); both vanish. The bounded-variable central limit theorem therefore gives

    n sqrt(m)(||Y||^2/d-sigma^2)
       => N(0, Var[q(T)]),
    Var[q(T)]=exp(-2)-1/8-(3/8)exp(-4)>0.

Under the target Gaussian the same statistic tends to zero. A shrinking shell event yields TV->1, just as in Section 4. This is a lower bound only for the specified implemented first correction on a smooth legal field, not a target-complexity lower bound, and not a lower bound against a different higher-order positive compiler.

## 7. Parent's independently checked all-n strengthening

The parent found a useful refinement of (1), checked independently here. Keep E0 fixed and use C_t=sigma^2 I-t Sigma/n+E0. Since Sigma is PSD,

    C_t=C_1+(1-t)Sigma/n >= eta^2 I

for every n>=1. At t=0 the law is N(mu,sigma^2 I+E0); at t=1 it is the deterministic first-order correction. Compare the t=0 Gaussian to the target in a separate covariance interpolation. Centering indicators at 1/2 improves the Gaussian Hessian bound to ||sym R||F/(sqrt(2)eta^2). Safe rounded-up constants then give the all-n bound

    TV <= [L^2 sqrt(d)/n^(3/2)+L^4 sqrt(d)/(4 tau^2 n^2)]/(2 eta^2)
          + L^4 d/(8 tau^2 eta^2 n^2 m).

Thus no small-n cutoff is actually necessary. Section 2 is retained as the initial independently derived conservative bound.

## 8. Sharp iid-time architecture dimension exponent for all deterministic allocations

The growing-batch argument strengthens to the following iid-time statement. Every action time here is an independent uniform draw on [0,1]; stratified schedules are excluded. Fix sigma,tau,eta>0 with tau^2+eta^2=sigma^2. For the sine family and this exact first covariance-action map, let deterministic positive integers n=n(d),m=m(d) satisfy

    n+4m=o(d^(1/3)).

Then TV(Law(Y),N(0,sigma^2 I_d))->1. Thus the d^(1/3) dimension exponent of the proved upper bound is sharp within this iid-time deterministic-allocation architecture at fixed accuracy. This says nothing about other value-query algorithms, higher-order corrections, adaptive batch selection or the main polylog target.

Proof. Write Q=n+4m. The conditional-diagonal surrogate from Sections 4 and 6 has uniformly bounded coordinate fourth moments. Its conditional variance defect is

    delta=(v-qbar)/n+Rbar/(4 tau^2 n^2),
    Rbar=qbar^2+(1/m^2)sum_j[r(T_j)-q(T_j)^2].

First suppose m->infinity. With a_d=n sqrt(m), the actual-versus-surrogate shell error is O(sqrt(m log(2d)/d)) in L1, and the conditional sampling fluctuation is O(a_d/sqrt(d)) in L2. Both vanish since m<=Q and a_d<=Q^(3/2)=o(sqrt(d)). The target shell statistic also tends to zero. Let

    S_m=sqrt(m)(qbar-v),  b_d=v^2 sqrt(m)/(4 tau^2 n).

By the bounded-variable CLT, S_m=>N(0,Var q(T)). Expanding Rbar around v^2 gives

    a_d delta = -[1-v/(2 tau^2 n)] S_m + b_d + o_P(1/n).

If b_d has a finite subsequential limit, n->infinity and the limit is a nondegenerate normal law shifted by that limit. If b_d->infinity, the statistic diverges positively in probability, because S_m is tight and its displayed coefficient stays bounded. Either way a shell test separates it from the target with probability tending to one. Apply this argument to convergent subsequences of b_d in the compact extended interval [0,infinity].

If m stays bounded along a subsequence, pass to fixed m. If n->infinity, normalize the shell by n; its limit is v-qbar, with no atom at zero because q(T) is a nonconstant strictly increasing continuous function of a continuous uniform variable. If n also stays bounded, pass to fixed n,m. Then the unscaled variance defect delta(T_1,...,T_m) is a real analytic function on (0,1)^m and is not identically zero: by continuity at T_j=0 for all j, qbar=exp(-1)<v and both terms defining delta are positive. Hence its zero set has Lebesgue measure zero. Conditional shell concentration again separates the candidate and target with probability tending to one. These cases cover a further subsequence of every subsequence, proving the claim.

A numerical diagnostic supports, but is not used to establish, the shell mechanism. With d=262144,n=8,m=1, tau=eta=1/sqrt(2), and 256 independent runs, a target two-standard-deviation radial band was violated by 0.64453125 of candidate outputs and 0.0390625 of target outputs. The event-probability difference was 0.60546875, and the conditional-shell prediction correlation was 0.92990095. These are finite Monte Carlo frequencies, not a certified numerical TV lower bound. The script and CSV retain the seed and all tested dimensions.


Update: `STRATIFIED.md` audits a legal stratified-time alternative. Its general upper bound is unchanged, while the iid-time matching lower bound above does not transfer. The sine example instead has an explicitly quantified n^(-2) covariance/shell obstruction in a d^(1/4) regime.
