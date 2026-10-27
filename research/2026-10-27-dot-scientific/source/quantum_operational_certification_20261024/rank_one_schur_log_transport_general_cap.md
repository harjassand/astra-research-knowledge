# A sharp rank-one Schur logarithm comparison for every cap R >= 9

2026-10-25. Root extension of the exact baseline transport found for R=9 in the singular-boundary investigation. This is a scalar resolvent theorem with a noncommutative rank-one receiving consequence; not a higher-rank or full WH3 theorem.

Let beta >= 4 and W=beta(beta-2). For h,v >= 0 with h+v <= W, set

J_r(h,v) = integral_0^infinity h s / [(s+r)((s+r)(s+v)+h s)] ds.

Then J_1(h,v) >= 2 J_beta(h,v). The inequality is sharp: equality holds at h=0 and at v=0,h=W. For h>0,v>0 it is strict.

## Exact transport proof

Set R=(beta-1)^2, delta=W-h-v >= 0. For h>0,v>0 compare the two finite positive baseline measures

mu_1(ds)=ds/[(s+1)(s+R)],
mu_beta(dt)=2dt/[(t+beta)(t+beta+R-1)].

Their total masses agree because R-1=beta(beta-2) and log R=2log(beta-1). Match them by

z=sqrt((s+1)/(s+R)),
t=beta[(beta-1)z-1]/(1-z).

As s runs from zero to infinity, z runs from 1/(beta-1) to one, and t runs increasingly from zero to infinity. Direct integration of both measures proves this is an exact positive measure transport: their cumulative masses are equal, not merely comparable.

Writing N1=s(s+R), Nbeta=t(t+beta+R-1), the actual integrals become

J_1/h=integral N1/(N1-delta s+v) dmu_1,
2J_beta/h=integral Nbeta/(Nbeta-delta t+beta v) dmu_beta.

All denominators are strictly positive. At paired s,t, the first ratio exceeds the second exactly when

delta s t [t-s+beta-1]+v[beta s(s+R)-t(t+beta+R-1)] >= 0.

The two required expressions factor exactly as

t-s+beta-1 = beta z(beta-2)/(1-z^2),

beta s(s+R)-t(t+beta+R-1)
= beta^2 z(beta-2)(beta-z-3)((beta-1)z-1)
  /[(1-z)^2(1+z)^2].

Both are nonnegative on the stated domain because beta>=4 and z<1. Integrating proves the theorem. For h>0,v>0, the second term is strictly positive away from the endpoint, including beta=4, so the inequality is strict.

For h=0 both integrals vanish. For v=0 direct integration gives J_r=log(1+h/r). The desired inequality is equivalent to h<=beta(beta-2); equality occurs at h=0 or h=W. Thus no singular endpoint or dominated-convergence assumption is omitted.

## Rank-one matrix interpretation

Let P=|u><u| with ||u||=1 and let B>0 have Tr B<=1 and P<=R B, R>=9. The separate spectral-weight convexity reduction in strict_log_rank_one_singular_two_atom_reduction.md reduces the maximal survivor to a single feasible eigenvalue or two atoms with saturated harmonic constraint. The proof there is written for R=9; replacing 9 by R leaves the linear weight constraint and vertex argument unchanged.

In the two-dimensional cyclic subspace, saturation gives

B=(1/R)P+ww*, w=(sqrt(h/R),sqrt(v/R)), h+v<=R-1.

At p=1/(1+sqrt R)=1/beta and q=1-p, one has pP+qB=q[(beta/R)P+ww*]. The rank-one Schur resolvent gives

<u,log(rP+ww*)u>=log r+J_r(||w_1||^2,||w_2||^2).

After scaling by R, all baseline logarithms cancel because q^2 beta^2=R. Consequently

2<u,log(pP+qB)u>-<u,log B u>
=2J_beta(h,v)-J_1(h,v)<=0.

The one-atom case is the scalar inequality (p+q b)^2<=b for 1/R<=b<=1. Smaller p also obey the comparison: the function -<u,log(pP+(1-p)B)u> is convex, nonnegative since B<=I, and zero at p=1, hence nonincreasing on [0,1]. Therefore the log expectation increases with p.

This closes the rank-one singular survivor for every cap R>=9 and p<=1/(1+sqrt R). It does not supply exclusion for higher-rank singular survivors or for faithful active-cap matrices.

## Method boundary

For 2<beta<4, the factor beta-z-3 changes sign on part of the transport interval. This specific comparison therefore does not establish the theorem in that range. No counterexample or optimality claim is inferred from that failure.
