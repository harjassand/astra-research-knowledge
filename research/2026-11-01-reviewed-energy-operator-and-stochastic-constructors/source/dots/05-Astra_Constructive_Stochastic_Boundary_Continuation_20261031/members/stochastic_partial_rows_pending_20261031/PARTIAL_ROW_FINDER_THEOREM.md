# A raw-list sufficient finder for partially covered satellite faces

## Result and precise strength

The complete-hub-row assumption can be removed from the **sound certificate finder** by solving a coupled finite system over all low-count service configurations. No uniform activation clock, stationary fiber law, supplied Lyapunov patch, or favorable pivot is an input. A standard numerical LP proposes rationalizable head weights; every accepted result is checked against exact rational inequalities derived from the raw generator. Numerical success is not acceptance.

**Soundness theorem.** Every accepted certificate from the algorithm below gives a positive normlike V with LV<=-epsilon V+C on all integer states. The associated mass-action chain is nonexplosive and positive recurrent on each reachable class, and its invariant law has finite exp(theta N) moment for every theta<log T of the accepted certificate.

**Not a completeness theorem.** No proof that the LP search eventually succeeds for every recognized partial-row architecture is given. No all-exponent conclusion is inferred from one T. Unsupported raw lists, work-budget stops, floating infeasibility, numerical difficulties, or failed exact rational verification all mean UNKNOWN. They do not prove instability, exact LP infeasibility, or impossibility of a different Lyapunov representation.

This package is separate from the internally reviewed protected-token and complete-row constructions. Read its own independent receipt. All work is abstract count-process mathematics; no general weak-reversibility solution, historical priority, efficient complete algorithm, or operational chemistry is claimed.

## 1. Raw architecture acquired by finite enumeration

The finder enumerates a service subset S={Y_1,...,Y_m}, leaving nonempty satellites Z_1,...,Z_s. It checks the entire raw list against:

- A monomolecular service core strongly connected on {0,Y_1,...,Y_m}. Rates are lambda_i,k_ij,d_i. H is acquired from the nonzero star rows, and every h in H has d_h>0.
- Reversible star pairs 2Y_h<->Y_h+Z_j with rates alpha_hj,beta_hj. A pair may be absent; if present both rates are positive. Every satellite has at least one adjacent hub. **Rows need not be complete.**
- Remaining reactions preserve every service coordinate and the total count. They may have arbitrary finite degree. The complete raw graph is weakly reversible.

This version accepts no additional nonlinear service reactions. Null channels are discarded. Inputs are a trusted exact int/Fraction research API. The first recognized partition is used; no efficient or exhaustive search over all successful partitions is claimed.

## 2. Analytic tail acquired from the raw linear core

Let I=S\H. Solve finite single-particle equations

    sum_j k_ij(t_j-t_i)-d_i t_i=-1, i in I;     t_h=0.

Set

    L=max_h (1+sum_(i in I)k_hi t_i)/d_h,
    v_i=L+t_i, eta=(T-1)/L, q_i=1+eta v_i.

Then q_i>=T, q_h=T and Qv<=-1. Define

    delta=min_i eta/q_i,
    alpha=max_h sum_j alpha_hj,
    D=max_i d_i/q_i, B=sum_i lambda_i(q_i-1),
    c=min(1,delta/(4alpha)).

Let g(1)=1 and g(r+1)/g(r)=r/(r+c). For r>=1 set h0(y)=q^y g(r). Put V0=T^Z h0, where Z=sum_j z_j. Exactly as obtained by the linear conversion, immigration and death ratios,

    LV0/V0 <=B+2cD-(delta-c alpha)r
              -c/(r+c)sum_(h,j)beta_hj y_h z_j, r>=2.    (1)

This inequality does not require complete rows: missing star entries simply give zero terms. Acquire epsilon_tail=delta/4 and integer R0>=2 with B+2cD-(delta-c alpha)R0<=-epsilon_tail.

Outside a sufficiently large service ball, the constant/linear term in (1) is already negative regardless of which satellites are undrained. The problem is the finite service configurations whose fibers remain infinite.

## 3. The finite unknown head and exact generator forms

For a trial R>=R0, introduce one unknown h_y>0 for **every service composition** with r<R, not merely the all-hubs-empty states. There are binomial(R+m-1,m) unknowns. At all other service states use h0(y). Define V(y,z)=T^Z h(y).

Every nonneutral reaction changes r by at most1. Therefore patch effects are confined to service total r<=R. Enumerate every service composition in this finite set. For each one the raw generator has the exact affine-in-satellites form

    LV(y,z)/T^Z = A_y(h)+sum_j B_yj(h) z_j,               (2)

where A and B are linear affine forms in the unknown head weights, with rational fixed tail values. Explicitly,

    A_y(h)=sum_(core y->y') rate(y,y')[h(y')-h(y)]
            +sum_h alpha_h* y_h(y_h-1)[T h(y-e_h)-h(y)],

    B_yj(h)=sum_h beta_hj y_h[h(y+e_h)/T-h(y)],            (3)

and alpha_h*=sum_j alpha_hj. A forward star creates one satellite, hence its factor T; a reverse star removes one satellite, hence its factor1/T. The actual service core is used, and every exit outside the unknown head uses the exact tail value. Neutral reactions vanish because they preserve service and satellite total.

A service state y is **covered** if for every satellite j some occupied hub h has beta_hj>0. If y is not covered, at least one satellite can diverge without any direct negative coefficient from its stars. This is the face the earlier complete-row construction could not ignore.

## 4. Coupled finite inequalities

Choose rational epsilon=delta/500, so epsilon<epsilon_tail. Choose positive rational gamma; the implementation uses

    gamma=min(epsilon,c beta_min/[2(R+c)]),

where beta_min is the smallest nonzero reverse-star rate. Impose:

- For every **uncovered** y with r<=R:

      A_y(h)+epsilon h(y)<=0,
      B_yj(h)<=0 for every satellite j.                  (4)

- For every **covered** y with r<=R:

      B_yj(h)+gamma h(y)<=0 for every satellite j.        (5)

No constant-drift inequality is required in (5), since all satellite directions then have strictly negative coefficients. Positivity of every unknown head weight is checked separately.

All inequalities are affine and rational. They couple neighboring face corrections rather than choosing an independent Dirichlet solution and hoping it is monotone. In particular a reverse-star coefficient is checked even when its destination crosses the chosen head boundary.

The numerical proposer uses SciPy/HiGHS on this explicitly built matrix, with a positive strict proposal margin and a positive proposed weight lower bound. It rationalizes each floating candidate with a declared denominator limit, then evaluates **every exact rational inequality** and weight sign. Only those exact checks can accept. Floating infeasibility, solver failure or an exact violation merely advances the declared radius search or yields UNKNOWN. No Farkas certificate is claimed for a numerical infeasibility report.

The trial radii double from R0. The default trial-count and head-state budgets are explicit. Neither numerical optimization nor rationalization is treated as complete for this class. Costs include all attempted LP dimensions and the exact rational residuals.

## 5. Global soundness of any accepted finite certificate

At uncovered states, (2) and (4) give LV/V<=-epsilon for **all** satellite populations.

At covered states, put H_y=A_y(h)/h(y), a_yj=-B_yj(h)/h(y)>=gamma. Then

    LV/V=H_y-sum_j a_yj z_j.

Let a_y=min_j a_yj>0 and acquire integer

    Z_y=max(-1,ceil((H_y+epsilon)/a_y)).

For total satellite count greater than Z_y the drift is at most -epsilon V. On the remaining finite satellite head, an explicit sufficient exception constant is

    C_y=h(y) T^Z_y max(0,H_y+epsilon)

when Z_y>=0, and zero otherwise. Set C=max_y C_y over covered service configurations. This bound need not be tight; its value and bit cost are recorded.

If r>R, no one-step reaction reaches the patched head r<R. Equation (1) therefore gives LV/V<=-epsilon_tail<=-epsilon there. Together with the finite covered/uncovered service layers, this covers every integer state and proves

    LV<=-epsilon V+C.                                    (6)

Because c<=1, g(r)>=1/r. The tail dominates T^(r+Z)/r. The finite service head has strictly positive coefficients times T^Z. Thus V is positive and normlike. Stopped Dynkin and finite sublevels give full-process nonexplosion, including high-degree neutral motion. Weak reversibility supplies feasible reverse paths and closed communicating classes; the Foster bound gives classwise positive recurrence.

Stopped exponential Dynkin implies P_tV<=aV+b with a=exp(-epsilon t)<1, b=C(1-a)/epsilon. Invariance and concavity of min(V,n), followed by Fatou with lower bound -b, imply pi(V)<=C/epsilon without assuming integrability. For every theta<log T, exp(theta N) is bounded by a finite multiple of V. No conclusion about larger exponents is obtained unless a separately accepted larger-T certificate is acquired.

## 6. Executed partial-row, non-complex-balanced example

The four species are B,D,C,F. The service core consists of

    0->B at1/10; 0->D at1/5;
    B->0, D->0, B->D, D->B at1.

Stars are 2B<->B+C and 2D<->D+F, all four rates1. Neutral satellite conversions are C<->F at rates1,1. Thus B has no F-star and D has no C-star. The raw scan acquires S={B,D}, H={B,D}, satellites{C,F} after5 partition trials.

The example is not complex balanced. The monomolecular linkage forces b=2/15,d=1/6. The star linkages force c=b and f=d, while the neutral linkage forces c=f, a contradiction. Compatible product-Poisson factors are therefore not silently available. The core conversion and neutral satellite conversion also prevent describing this example as two independent pivot chains.

At T=2, the actual numerical proposal attempts R=2 and R=4 return infeasibility statuses, retained only as UNKNOWN. At R=8 it returns a rationalizable candidate. All89 rational inequalities for36 unknown head weights pass exactly, with a strictly negative largest residual. There are45 service configurations at r<=8, of which28 are covered and17 uncovered. The exact epsilon is1/1000. The recorded Foster constant is large (948-character rational representation), not suppressed as a practical bound.

The search paid LP shapes(3 variables,11 inequalities), (10,29), (36,89), totaling3527 dense matrix entries. Head weights reach37-bit numerator/denominator size. The original generator challenge checked1056 exact count states, including satellites at0,1,10,100. These tests supplement the all-state proof, not replace it.

An earlier differently parameterized partial-row search exhausted its radius budget; one large-radius floating success failed exact rational verification. Such a candidate is rejected, not rounded into a theorem. The corresponding diagnostic is separate from the accepted example and does not establish mathematical infeasibility.

## 7. Scope and remaining obstruction

This result crosses multiple partially covered satellite faces by **acquiring** a coupled finite correction from the raw list. It is a sufficient finder, unlike the prior complete-row family where an unbudgeted termination theorem was proved. A compatible LP point is not an input: the recorded algorithm constructs its matrix, calls a conventional numerical proposer, and exact-verifies the returned point. Nonetheless, no theorem guarantees success or a finite radius on all recognized partial-row networks.

The method retains a monomolecular service core, direct hub deaths, reversible star shapes, and a common exponential satellite weight. More general service cores or nonlinear satellite coupling require additional analysis. Existing LP, Foster, queueing/comparison, tier and decomposition machinery is given full credit; the exact proof/certificate acquisition is not a priority claim. General weak-reversibility recurrence remains outside scope.
