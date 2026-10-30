# Nonlinear relaxation of a warm memory moment
2026-10-30. Root derivation candidate. This is an in-basin moment law, NOT trace-norm mixing of the logical register.

## 1. What the full animal sum contains beyond W>=V
Let B_A=f_A G_A>=0 be the actual animal-local positive summands, with ||B_A||<=exp(c1 |A|) and at most C N A0^m animals of size m. These follow from theta<1 and the bounded per-vertex activity-circuit norm. Define V_G=sum_A B_A and W_G=sum_A |A|B_A.

For every positive integer r,

    V_<r<=C' N K^r I,
    W_G>=r V_G-C' N r K^r I,                         (1)

for a fixed K>1. This uses positivity of each summand and an elementary geometric sum, not commutation between different G_A.

Let T be the accepted unital CP proof circuit and F=T(V_G). Applying positivity/unitality to (1) gives

    T(W_G)>=r F-C' N r K^r I.

For ANY positive subnormalized state rho, put x=Tr(F rho), y=Tr(T(W_G)rho). Optimizing the scalar integer r after taking expectation yields fixed constants a,C0>0 such that

    y>=a x log_+(x/(C0 N)).                           (2)

One can take r=floor(log(x/(C'N))/(2log K)) for x sufficiently large, and enlarge C0 to cover the small range. This is NOT a forbidden operator supremum over noncommuting inequalities and does not use Jensen on a noncommuting W.

## 2. Actual noisy/killed moment contraction
The accepted drift has the stronger form

    d x/du<=-lambda y+b N Tr(rho).

Combining with (2), and choosing C2>=C0 so the additive bN is absorbed at x>=C2N, gives

    x(u)<=C2 N exp[log_+(x(0)/(C2N)) exp(-kappa u)],    (3)

with kappa>0 fixed. Below C2N the same scalar comparison keeps x bounded. All rates are those of the actual accepted apparatus; no new recovery operation is performed.

If x(0)<=exp(gamma N), constant time reduces the extensive logarithmic moment coefficient by a fixed factor. Time O(log N), with a potentially very poor constant 1/kappa, returns it to O(N). This is stronger than discarding W and using only W>=V, which would suggest O(N) time from such an initial moment.

## 3. Logical safety during warm relaxation
Assume the initial channel already has identity logical action in the canonical gauge, is supported in the common component/potential basin, and has x(0)<=exp(gamma N) below its exponential boundary M=exp(mN), gamma<m. This initial condition must be earned by an input/gate/preparation interface; it is not implied by an arbitrary low-energy state.

The killed state stays positive. Its boundary mass is at most C x(u)/M, so the actual-to-killed Duhamel comparison is bounded by

    C N integral_0^u sqrt(x(s)/M) ds.

For example, split after O(log N) warm time. Before that, the bound is at most a polynomial/logarithmic factor times exp[-(m-gamma)N/2]; afterward x=O(N) supplies the ordinary exponentially long lifetime estimate. Noise acts throughout warm relaxation.

This is a warm-start stability statement with explicit logical and basin premises. It does not by itself supply reusable gate sequencing, a physical decoder, a stationary distribution, or an input-independent global mixing theorem. Its purpose is to make the next operation earn a composable input contract rather than assuming perfectly clean controllers/errors each time.
