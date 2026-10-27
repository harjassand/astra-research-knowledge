# Conditional regression budget and an explicit global 2x2 receiver

26 October 2026. These are conditional posterior statements, NOT a separator for the cosine source and NOT a solution of Morrey's conjecture.

Write q(z)=uv+uw+vw=z^T Jz, J=(ee^T-I)/2. A source-supported posterior sigma has mean m and D=E q(Z)-q(m)=0. Put X=Z-m and choose a minimizing delta=E(q(X)-a.X)^2 (a constant is unnecessary since both terms have mean zero). Singular covariance is allowed; any minimizing a can be used.

## 1. A regression budget for actual posterior splits

For a finite posterior decomposition sigma=sum p_i sigma_i with means m+v_i, require D_i=0 and q(v_i)=0. Then E_i q(X)=q(v_i)=0, and the parent residual e=q(X)-a.X has E_i e=-a.v_i. Child optimal affine regression is invariant under translation and is no worse than the parent affine predictor with its child mean removed. Consequently

    delta - sum p_i delta_i >= sum p_i (a.v_i)^2.

If gamma=inf{|a.d|: |d|=1,q(d)=0}>0, this is at least gamma^2 sum p_i |v_i|^2. Thus if EVERY subsequent node retains gamma>=gamma_*, total future mean-variance gain is at most delta/gamma_*^2. There is no assertion that this margin survives: zero-displacement observations can change posterior geometry.

With A=a^T J^{-1}a=(sum a)^2-2|a|^2>0,

 gamma=(|sum a|-sqrt(6|a|^2-2(sum a)^2))/3
      =A/(|sum a|+sqrt(6|a|^2-2(sum a)^2)) >= A/(5|a|).

This follows by resolving a into its e and e-perpendicular components and using the null-cone angle. For a bounded observation h preserving E h=E[q(X)h]=0, v=E[Xh] null, the simpler bound |v|^2<=delta E h^2/gamma^2 follows from a.v=-E[e h]. Neither estimate is an exhaustion theorem.

## 2. Coefficient-space global null-convex bump

Let r=gamma/4, phi(X)=(1-|X|^2/r^2)_+^3, and b=gamma^4/192. The global function

    f(z)=(q(z-m)-a.(z-m))^2+b phi(z-m)

is C2 and null-convex. On the bump support |grad e.d|>=gamma-2r=gamma/2 for unit null d. Thus D2(e^2)[d,d]>=gamma^2/2, whereas D2 phi>=-6I/r^2. Outside the bump, e^2 is null-convex globally. A strict conditional gap occurs if delta<b(1-E phi).

A moment-only sufficient test uses |X|^2<=D_m^2=3+|m|^2+2||m||_1<=12 and

    1-E phi >= E|X|^2 / max(D_m^2,r^2).

All moments and gamma in this test must be received for the actual posterior, not Monte Carlo.

## 3. Explicit globally rank-one-convex full-matrix extension

Use B(u,v,w)=[[u+w,w],[w,v+w]], so det Bz=q(z). Define symmetric L by
L11=a_u, L22=a_v, L12=(a_w-a_u-a_v)/2. Then L:Bz=a.z and det L=A/4>0; L is definite. Let lambda be its least absolute eigenvalue, R=lambda/4, b=lambda^2 R^2/48, and kappa(X)=(X12-X21)/2. Set

 P(A)=(det X-L:X)^2+4 det(L) kappa(X)^2
      +b(1-|X|_F^2/R^2)_+^3,  X=A-Bm.

This is an explicit GLOBAL C2 rank-one-convex function, without an unproved cutoff extension. For unit rank-one D=u v^T, |u|=|v|=1,

 (u^T L v)^2+det(L)(u cross v)^2
   =(u^T L u)(v^T L v)>=lambda^2.

The square root of the two-square expression after replacing -L:D by (cof X-L):D is at least lambda-|X|_F. Since det is affine along rank-one lines, the Hessian of the first two terms is therefore >=2(lambda-R)^2=9lambda^2/8 on the bump. The bump's negative Hessian is at worst 6b/R^2=lambda^2/8. Outside it both squares are rank-one-convex globally. This also handles negative-definite L because the product on the right is positive.

For a symmetric posterior, the skew term vanishes and the gap test is delta<b(1-E phi(BX)). Physical and coefficient norms MUST NOT be interchanged.

## 4. Concrete non-source example and a quantitative failed source route

For uniform mass on the four elliptope vertices, m=0,a=(1,1,1), e=q-sum z=0, L=[[1,-1/2],[-1/2,1]], lambda=1/2, R=1/8, b=1/12288. All four Bz lie outside the bump; EP=0<P(0)=b. This is an explicit nonlaminate four-point measure, NOT a gradient-law counterexample.

For the actual cosine source mu and m=0, this conservative bump family cannot separate. Exactly

 E e^2=3/4-(sum a)/2+|a|^2/2,  E|BZ|_F^2=3.

Since 1-(1-t)_+^3<=3t, the bump loss is at most 3lambda^2/16. Definiteness gives |a|^2>=6lambda^2: for positive L=lambda I+Q, Q>=0, a_u,a_v>=lambda and a_w=L11+L22+2L12>=2lambda; negate L for the other case. Hence

 EP-P(0) >= 3/4-(sum a)/2+(15/32)|a|^2 >= 7/20.

Adding a constant to e changes neither this expected-square difference nor the Hessian proof. Thus this explicit full-matrix conditional receiver is NOT a hidden source counterexample: the entire stated conservative family has a strict positive source gap. A conditional bad posterior, even if received, does not imply that every source decomposition encounters it.

## 5. Exact application to the received strong first split

`verify_first_split_regression_budget.py` integrates actual polynomial source posteriors exactly. At the root delta=3/8, gamma=1/2, V=3/2. For the child density 1-h/4 (probability1/3),

 a=(57/82,209/328,209/328), delta=509/1312,
 gamma=76/123, V=87/64.

Here delta/gamma^2 is approximately1.01617144, strictly below V=1.359375. Therefore a continuation that retains this gamma as a lower bound at every future nonterminal node cannot exhaust that posterior's variance. This is not a posterior obstruction: the necessary escape is to change the regression geometry, possibly through zero-mean-displacement labels. The other child density1+h/8 has gamma385/1084 and delta5381/17344, and does not satisfy this particular budget deficit. The exact average regression loss is3453/88888, exceeding the guaranteed root margin payment9/512. These are exact source moments, not the earlier finite-grid diagnostics.

## 6. Larger admissible heights (separate from the 7/20 exclusion)

The same global physical proof permits ANY 0<R<lambda and

    0<=b<=R^2(lambda-R)^2/3.

Indeed the baseline rank-one Hessian on the bump is at least2(lambda-R)^2, and its worst negative bump Hessian is6b/R^2. The conservative source exclusion7/20 in Section4 applies ONLY to that section's smaller height/radius, not this larger family. A bounded sampled search is preserved in `probe_maximal_global_bump.py`; it is a gate for receiving, not an integral certificate or an all-parameter family exclusion.
