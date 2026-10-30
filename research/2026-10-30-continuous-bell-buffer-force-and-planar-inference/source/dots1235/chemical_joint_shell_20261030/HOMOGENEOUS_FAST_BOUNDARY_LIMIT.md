# Uniform factorial boundary limit for homogeneous conservative fast reactions
Status: personally derived lemma, awaiting audit. Supports the modified-fast extreme-composition check, not general boundary closure.

For fixed nonnegative integers a,b and 0<alpha<1, define

    h_ab(m)=(m)_a [(m+b-a)!/m!]^alpha  if m>=a,
    h_ab(m)=0                         if m<a.

When a=b=0 this is identically1. Otherwise p=(1-alpha)a+alpha b>0. Fixed-shift factorial asymptotics give h_ab(m)=m^p[1+O(1/m)] as m->infinity. Treating the bounded m remainder separately yields, uniformly over integers 0<=m<=N,

    N^(-p) h_ab(m) = (m/N)^p + O(N^(-min(p,1))).

The estimate includes infeasible sources: there m<a is bounded and the approximating term is O(N^-p).

For any fixed conservative reaction y->y' with |y|=|y'|=D and x_1+...+x_d=N, its actual primal factorial gain divided by N^D converges UNIFORMLY on all integer compositions to

    product_i (x_i/N)^((1-alpha)y_i+alpha y'_i).

The loss similarly converges to product_i(x_i/N)^y_i. Therefore the full homogeneous fast generator of V0=product_i(x_i!)^alpha, divided by N^D V0, converges uniformly to the continuous simplex function

    E_alpha(t)=sum_(y->y') k_yy' [t^((1-alpha)y+alpha y')-t^y].

No lower bound on any individual count is required.

For the modified two-composition cubic triangle on 3C,A+2C,3A, E_alpha(0,1) is minus the total positive outgoing rate constant from 3C, and E_alpha(1,0) is minus that from3A. Other source contributions vanish at the corresponding endpoint. By continuity there are two fixed extreme-composition cones with E_alpha<=-c. Uniform convergence gives actual fast drift <=-c N^3(B)_4 V0 for all large N in these cones, including bounded or zero minority coordinates.

At B>=4, the connector-adjusted F equals V0 at every fast target. Its only nontrivial clearing-return correction is independent of C after cancelling C!^alpha. The prior low-B calculation bounds its positive part by C(1+A^(3-delta))(B)_4 F, with delta>0, uniformly in C; bounded A is covered by finitely many ratios. Immigration/activation positive terms are bounded by C(B)_4[1+A^(1+2alpha)]F. Since alpha<1, both are o(N^3)(B)_4 F. Thus the negative extreme-composition F drift needed in HOLEY_HEAD_ACTUAL_RETURN_CLOSURE_CANDIDATE.md is earned for the modified graph.

Balanced high-B states are handled by the existing finite-complex bulk theorem with a graph-dependent sufficiently small alpha. This lemma does not replace that theorem or the actual low-B return calculation.
