# Actual-error minimax audit and finite-action distinction

Author: gc_control_adversary. Date: 2026-10-16. Internal analytic reconstruction. The minimax sandwich was communicated by the root from the peak-genesis worker; the audit and finite-action separation below were independently reconstructed here.

## Exact continuous-model minimax sandwich

Let U be the nonempty deterministic rate-control class 0<=lambda<=L, integral lambda=Lambda over [0,T]. Let H range over the unary exact finite-dimensional source class: H=H0(t)+V(t), [H0,Z]=0, {V,Z}=0, ||V(t)||<=J, with well-defined propagators and actual generator

    -i[H,.]+(lambda(t)/2)(Ad Z-Id).

The initial state is in the recorded Z=+ sector; arbitrary bath/reference input is allowed. Define p_lambda(H) as the operator norm of its final Z=- effect compressed to that initial sector, and

    R*=inf_(lambda in U) sup_(H in H) p_lambda(H).

The schedule is chosen before the unknown H, and H is independent of the random-unitary unravelling. Lambda is fixed, not an outcome-adaptive stopping budget. This is a unary endpoint risk, not logical memory error or a history-dependent decoder risk.

For the single fixed admissible witness H=JX with no bath, the physical random-unitary representation uses rate lambda/2 Z flips. Its sign xi starts at +1 and

    p_lambda(JX)=E sin^2(J integral_0^T xi(t)dt),
    E xi(t)xi(s)=exp(-integral_min(t,s)^max(t,s) lambda(v)dv).

Therefore C_lambda=J^2 E(integral xi)^2 is precisely the source exposure certificate. Starting xi at +1 does not change the covariance, so no missing stationary-seed assumption or factor of two occurs.

Write a=JT. Since |J integral xi|<=a and sin(x)/x decreases on [0,pi], for 0<a<pi

    sinc^2(a) C_lambda <=p_lambda(JX)<=C_lambda.

The source sharp endpoint theorem gives p_lambda(H)<=min(1,C_lambda) for every H in the class. If C* is the globally optimized certificate, it follows that

    sinc^2(a) C* <=R*<=min(1,C*).                         (M1)

For the incoming certificate optimizer lambda*,

    sup_H p_lambda*(H)<=min(1,C*),
    sup_H p_lambda*(H)/R*<=1/sinc^2(a)

whenever J>0 and the ratio is defined. As a->0 this is 1+a^2/3+O(a^4), uniformly over all feasible peak/intensity parameters. At J=0 both risks vanish and no ratio is needed.

Thus the source optimizer is asymptotically minimax for actual unary endpoint risk in the exact stipulated model. (M1) is not a finite-a solution of the unknown-H minimax problem, an actual-error lower bound for each H, or a hardware floor. The lower witness is in the class over which a supremum is taken.

The same argument for one finite random refresh grid gives C_grid=sum_r (J Delta t_r)^2, and hence

    sinc^2(a) a^2/(N+1)
       <=inf_grid sup_H p_grid(H)<=a^2/(N+1).

This conditional finite-count comparator has its own update primitive and is not constrained by a bounded continuous dephasing rate.

## An analytic finite-a counterexample to actual-error optimality for a known H

Take T=1, Lambda=2, finite cap L=100, and the admissible known Hamiltonian H=aX with a=3.1<pi. The certificate optimizer is cap inactive:

    lambda*(t)=4 on [1/4,3/4], zero elsewhere.

Under the physical telegraph representation its total mean flip count is one. The exactly-one-flip trajectories have density 2/e on that interval. A flip at time t gives signed time 2t-1. Their nonnegative contribution alone establishes

    p_lambda*(aX)
       >=(2/e) integral_(1/4)^(3/4) sin^2[a(2t-1)]dt
       =(1/(2e))[1-sin(a)/a]
       >0.1814.                                         (M2)

Consider the admissible competitor lambda=100 on [0.49,0.51], zero elsewhere. Its active width is delta=Lambda/L=0.02. On an odd-flip history the equal outer holds cancel, so the total signed time S satisfies |S|<=delta. On an even-flip history the outer holds add, and S lies in [1-2delta,1]. These are pointwise bounds for every telegraph history, regardless of its flip times or count. Consequently

    p_comp(aX)
       <=max{a^2 delta^2,(|sin a|+2a delta)^2}
       <0.0275.                                         (M3)

Equations (M2)-(M3) strictly separate the actual errors with elementary bounds. They prove that the certificate-optimal schedule need not minimize a known admissible Hamiltonian's actual endpoint error at finite action, even with a<pi and a finite peak cap.

This does not refute (M1). The known-H optimization has different quantifiers from inf_lambda sup_H; a schedule tailored to a near-return coherent rotation may be poor against a different unknown H. No finite-a global optimum, minimum actual logical error or physical implementation is claimed.
