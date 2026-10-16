# Peak-cap certificate audit

Author: gc_control_adversary. Date: 2026-10-16. Internal analytic audit; external correctness, novelty and device capability UNKNOWN.

## Immutable contract and source

Pinned capital revision: `9dbe934e5475f415c2d160a6c0715534aafa546b`.

Incoming proof: `originals/shared_bath/pr104_bath_audit/PEAK_RATE_CERTIFICATE_ADDENDUM.md` in the current research directory. The earlier explicitly unresolved cap-infeasible case is in the pinned `updates/GB-dots-capital-genesis-20261016/package/derived/workers/gb_finite_rate_genesis/COST_AND_INCUMBENT.md`, section 1.

For fixed constant J>=0, duration T>=0, finite L>=0, and integrated latent-pinch intensity Lambda>=0, optimize

    C(lambda)=J^2 integral_[0,T]^2 exp(-|u(t)-u(s)|) dt ds,
    u(t)=integral_0^t lambda(s) ds,
    0<=lambda<=L a.e., integral lambda=Lambda.

The feasible class is nonempty exactly when 0<=Lambda<=LT. Lambda is twice the mean physical telegraph-frame flip count in that implementation. It is the mean actual measurement count only in an implementation using real full pinches.

## Global measure reduction, including plateaus

Assume L>0. Set a=JT and d=J/L. The pushforward measure mu=u_#(J dt) is positive, has mass a, and lies on [0,Lambda]. For every nonnegative Borel f, monotone absolutely continuous substitution gives

    integral f dmu = J integral_0^T f(u(t))dt
      >= (J/L) integral_0^T f(u(t))u'(t)dt
      = d integral_0^Lambda f(v)dv.

Thus mu>=d dv as a measure, not merely as a density at points where a differentiable inverse happens to exist. A positive-duration plateau contributes an atom; singular inverse components also remain in the positive remainder. No strictly positive lambda assumption is used. The objective is E(mu)=integral exp(-|v-w|)dmu(v)dmu(w).

It is valid to optimize over all positive measures of mass a satisfying this domination, even if not all are realizable: this supplies a lower bound, and a realizable minimizer will supply equality.

The exponential kernel has strictly positive energy on every nonzero finite real signed measure. For example its Fourier transform is 2/(1+omega^2)>0. Alternatively the source's Volterra square decomposition proves nonnegative energy; strictness follows from uniqueness of a signed measure with zero Laplace tails. Therefore for a candidate mu*, with potential V*=K mu*,

    E(mu)-E(mu*)=2 integral V* d(mu-mu*)+E(mu-mu*).

## Cap active: Lambda<=LT<=Lambda+2

Let q=(a-d Lambda)/2, so 0<=q<=d, and

    mu*=d dv+q delta_0+q delta_Lambda.
    V*(v)=2d+(q-d)[exp(-v)+exp(-(Lambda-v))].

The bracket is maximized at the endpoints. Since q-d<=0, V* is minimized at both endpoints. Write every feasible measure as d dv+nu, with nu positive and mass 2q. Then

    integral V* d(mu-mu*) = integral V* dnu-2q V*(0)>=0.

This proves global optimality, not just stationarity. For J>0 it is realized by endpoint holds of length h=(T-Lambda/L)/2 and central rate L for length Lambda/L. The exact minimum is

    C*=2d^2(Lambda-1+exp(-Lambda))
       +4dq(1-exp(-Lambda))+2q^2(1+exp(-Lambda)).

For Lambda>0 and J>0 the measure minimizer is unique by strict positive definiteness. When q<d its positive surplus can occur only at the endpoints. The associated monotone cumulative map is fixed up to null-set modifications by its occupation measure.

## Cap inactive: LT>=Lambda+2

Set c=a/(Lambda+2). The unconstrained minimizer

    mu*=c[dv+delta_0+delta_Lambda]

has constant potential 2c. It is feasible because c>=d. Thus it remains the global optimum, with C*=2a^2/(Lambda+2). It is attained by endpoint holds h=T/(Lambda+2), with central rate (Lambda+2)/T. The middle duration is T Lambda/(Lambda+2), so the integrated intensity is exactly Lambda.

## Degenerate cases and boundaries

- J=0: every certificate is zero; every admissible schedule is optimal. No division by J is needed.
- T=0: feasibility forces Lambda=0, and the certificate is zero.
- Lambda=0: lambda=0 a.e., the two named endpoint atoms coincide, mu=a delta_0, and C*=a^2. Both formulas reduce to this value.
- L=0: feasibility forces Lambda=0, and the previous case applies; do not form J/L.
- Lambda=LT: q=0, so constant maximal rate is forced, and C*=2J^2[T/L-(1-exp(-LT))/L^2].
- LT=Lambda+2: q=d=c; the two regimes agree at 2d^2(Lambda+2).
- Lambda>LT: no admissible schedule exists. This is a feasibility failure, not a value of the objective.

## Verdict and exact unresolved operation

No analytic defect found. The incoming result closes precisely the constant-J peak-cap optimization left unresolved by the earlier capital proof. It does not solve a variable-J or finite-width control optimization, minimize a capped error effect in every regime, or minimize an actual logical error probability.

Setting the deterministic intensity profile needs the known envelope J and control of the actual stipulated rate. It does not require observing the latent Poisson outcomes. The remaining implementation obligation is to qualify that rate control, its full joint dilation, controller independence, support, preparation, tracking, reset and total reservation cost. A latent rate bound is not a physical pulse spacing or bandwidth certificate.
