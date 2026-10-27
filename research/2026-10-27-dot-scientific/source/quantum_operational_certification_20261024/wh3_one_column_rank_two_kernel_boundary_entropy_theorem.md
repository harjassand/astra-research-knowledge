# Full WH3 entropy theorem for the stable one-column rank-two-kernel boundary

2026-10-25. Exact theorem, with a finite rational certificate for its compact stationary receiver. The unrestricted one-column class with a faithful 3x3 correlated block remains open.

## 1. Entire source class

Choose distinct physical/reference labels i,j,k, a unit vector v=v_i|ii>+v_j|jj>, and any positive semidefinite 2x2 coefficient matrix T on span{|kk>,v}. Add arbitrary populations a|ik><ik|+b|jk><jk|, a,b>=0. Then

 Delta(A)=Tr A log A+Tr EA log EA-2Tr NA log NA >=0.

All coefficients and phases are arbitrary. In particular, this receives the previously stable boundary where the correlated rank-two block has kernel q supported on {i,j} and the only active population column is its missing index k.

By local diagonal gauges the coefficient matrix and v can be parameterized by h,d>=0, c complex with |c|^2<=hd, and x=|v_i|^2 in [0,1]. The audited shared-pair balancing theorem proves that, at fixed h,d,c,s=a+b, the deficit is minimized at x=1/2,a=b=s/2. Hence it suffices to establish the balanced receiver below.

## 2. Balanced receiver and compactness

Let q=s/2,

 T=[[d,c],[conj(c),h]],
 L=[[d+q,c/sqrt2],[conj(c)/sqrt2,h/2]],
 tau=h+d+2q.

The exact balanced deficit is

 D=Tr T log T-2Tr L log L+(d+2q)log(d+2q)
   +tau log(2/3)+d log2.                              (1)

Normalize tau=1. The domain h,d,q>=0, |c|^2<=hd is compact and D is continuous. Its boundary is paid:

* q=0 is the maximally-correlated theorem;
* c=0 is the physical-2+1 block theorem (not a classicality claim);
* |c|^2=hd is the rank-one-correlated-plus-population theorem;
* h=0 or d=0 forces c=0 and is included above.

Therefore a hypothetical negative minimum is faithful and coherent, with h,d,q>0 and 0<|c|^2<hd. Its normalized stationary equations are necessary.

## 3. Exact stationary reduction

The derivation in `one_column_shared_pair_balancing_theorem.md` gives common logarithmic divided difference ell(T)=ell(L)=ell>0. Scale coefficients by ell and write

 U=2theta coth(theta), D_T=(theta/sinh(theta))^2,
 V=2phi coth(phi),     D_L=(phi/sinh(phi))^2,

with theta,phi>0. Let r=h/2+q in scaled coordinates and m=d+2q. Every interior stationary source necessarily satisfies

 r=log(4D_T/D_L), delta=D/tau=r-log3,
 m=2V-U>0,        2logm-m=log D_T,
 r^2-(U-V)^2=4D_L-2D_T.                              (2)

The source inequalities imply |U-V|<r. If delta<0 then D_T<(3/4)D_L, so theta>phi, U>V. Put u=U-V. The logarithmic slope of D as a function of U obeys

 0< -dlogD/dU
   =(coth(theta)-1/theta)/(coth(theta)-theta csch(theta)^2)<=1.

The upper bound is equivalent to sinh(theta)>=theta. Integrating gives

 log(D_L/D_T)<=u<r.

Since log(D_L/D_T)=log4-r, every negative candidate therefore has

 log2<r<log3, 0<u<r.                                 (3)

## 4. Analytic exclusion outside a compact rectangle

The function f(m)=2logm-m has global maximum log4-2. Thus the moment equation in (2) requires D_T<=4/e^2. But D(theta) is decreasing and

 D(1)=1/sinh(1)^2>4/e^2,

so theta>1.

For theta>=3, U>=6. From (3), m=U-2u>U-2log3>2. Negative delta also gives u>log(4/3). Put a=2log(4/3), so 1/2<a<1. Then m<U-a and, because f is decreasing above two,

 f(m)>=f(U-a).

An exact calculation gives

 f(U)-log D_T=-E(theta),
 E(theta)=2[theta coth(theta)-log(2cosh(theta))]
         <=4theta/(exp(2theta)-1)
         <=12/(e^6-1)<1/10.

The middle function decreases for theta>=3. Also U-a>5, hence

 f(U-a)-f(U)=integral_(U-a)^U(1-2/t)dt
             >=a[1-2/(U-a)]>3/10.

Thus f(m)-log D_T>1/5, contradicting (2). All constants here have elementary rational witnesses: log(1+t) lies between t/(1+t) and t for t>0, log3<2, and the degree-five positive Taylor polynomial already gives e^6>121.

Every negative candidate consequently lies in

 1<theta<3, 0<phi<theta<3.                           (4)

## 5. Exact rational compact exclusion

The executable certificate `one_column_balanced_stationary_exact_certificate.py` exhausts the closed rectangle theta in [1,3], phi in [0,3]. It uses only Python Fraction arithmetic. Exponentials are enclosed by a positive Taylor sum with a rational geometric upper bound for the remainder. Logarithms are range-reduced to [1,2] and enclosed by the atanh series with its rational geometric remainder. Every rounded interval is rounded outward to a dyadic denominator 2^80.

U(theta) is increasing and D(theta) decreasing, so endpoint enclosures bound each rectangular box. Boxes are discarded only by a necessary condition from (2)-(3): theta>phi, the moment maximum, 0<r<log3, positive q/m, exclusion of zero from the moment equation, or exclusion of zero from the determinant equation. Otherwise a box is bisected. No floating-point sign or sampled point is used.

The saved receipt `one_column_balanced_stationary_exact_certificate.json` records PASS, 81 examined nodes, maximum depth10, and 41 rejected leaf boxes, covering the whole starting rectangle. Replaying the script reproduces the complete list of rational boxes and exclusion reasons. Thus no negative stationary candidate exists in (4).

Sections 2-5 rule out a negative global minimum of (1), proving the balanced inequality. The global balancing theorem then proves the entire source class in Section 1.

## Dependencies and scope

The balancing proof and physical output identity are in `one_column_shared_pair_balancing_theorem.md`, audited in `one_column_shared_pair_balancing_independent_audit.md`. Boundary receivers are `wh3_maximally_correlated_inputs_entropy_theorem.md`, `wh3_physical_two_plus_one_block_entropy_theorem.md`, and `wh3_rank_one_logcorner_anchor_theorem.md`. No uniqueness of stationary roots is assumed. Numerical root diagnostics are not part of the certificate or proof.
