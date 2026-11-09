# Exact fixed-batch categorical coupling

This is the finite-alphabet fixed-batch premise inherited from Astra N1691, stated and proved here so the hard-cap comparison can be read without another archive. It is not a new claim of this package.

## 1. Setup

There are r>=1 independent P records, the first being the actual supplied X, and s>=1 independent Q records. The positive integers r,s are fixed before sampling. An algorithm may use all ordered records and independent auxiliary randomness. It must output Y with exactly law Q for every pair P,Q. It cannot query further source records or use the unknown probabilities.

Let A=(A_1,...,A_d) and B=(B_1,...,B_d) be the two count vectors. Conditional on A=a,B=b, all compatible ordered P lists are equiprobable, and likewise for Q lists. The conditional distribution of the records therefore does not depend on P,Q. In particular

    Pr(X=j | A=a,B=b)=a_j/r.

Write g_j(a,b)=Pr(Y=j | A=a,B=b), averaging the algorithm's auxiliary randomness and all compatible ordered lists.

## 2. Universal exactness forces the empirical target marginal

For every P,Q in the interiors of their simplexes, universal exactness says

    sum_(a,b) Mult_r(a) Mult_s(b) P^a Q^b g_j(a,b) = q_j,

where |a|=r, |b|=s and Mult_r(a)=r!/(product_i a_i!). The homogeneous Bernstein representation of q_j at degrees (r,s) is

    q_j = sum_(a,b) Mult_r(a) Mult_s(b) P^a Q^b (b_j/s).

For completeness, this representation is unique. If the difference vanishes on the product of simplexes, homogeneity makes it vanish on every pair of strictly positive vectors: scale each vector by its coordinate sum and multiply by the corresponding sum to powers r and s. A polynomial zero on this open set has every monomial coefficient zero. Thus

    g_j(a,b)=b_j/s

for every pair of count vectors. Boundary distributions follow by the same polynomial identity or by continuity. No assumption about a preferred ordering, linear algorithm or deterministic decision rule was used.

## 3. Optimal disagreement and a matching operation

Conditional on the count vectors, (X,Y) is a coupling of a/r and b/s. Therefore

    Pr(X != Y | A=a,B=b) >= TV(a/r,b/s).

A maximal categorical coupling of those empirical histograms attains equality while retaining the actual X as its first coordinate. Let

    u_i=a_i/r, v_i=b_i/s, h_i=min(u_i,v_i),
    R=1-sum_i h_i.

When X=i, retain i with probability h_i/u_i. If it is not retained, draw from the residual weights v_j-h_j normalized by R. The impossible u_i=0 conditional input is never used. If R=0, retain X always. These are rational probabilities from integer counts and have exact fair-bit implementations by ordinary integer rejection. The conditional output is v; averaging gives Q. Hence the minimum possible unconditional disagreement is exactly

    E TV(P_hat_r,Q_hat_s).

Only histogram construction and rational categorical selection are needed. A generic dense optimal-transport solver is not the appropriate implementation baseline.

## 4. Uniform upper bound

For a multinomial empirical distribution based on m draws,

    E ||P_hat_m-P||_1
      <= sum_i sqrt(p_i(1-p_i)/m)
      <= sqrt((d-1)/m).

The last step is Cauchy-Schwarz and sum_i p_i(1-p_i)=1-sum_i p_i^2<=1-1/d. With r=s=m, the triangle inequality and the factor 1/2 in total variation give

    E TV(P_hat_m,Q_hat_m)
      <= TV(P,Q)+sqrt((d-1)/m).

Thus m=ceil((d-1)/eta^2) supplies the stated deterministic-batch comparator using 2m-1 new calls. The companion fixed-allocation moment calculation supplies a nonasymptotic lower bound at equal uniform sources. This upper bound is deliberately simple and is not an assertion of optimal finite constants.
