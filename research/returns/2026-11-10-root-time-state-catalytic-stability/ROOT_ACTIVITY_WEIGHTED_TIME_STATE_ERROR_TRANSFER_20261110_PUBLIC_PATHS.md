Activity-weighted stability under unknown state- and time-dependent errors

Assumptions. Let Q be a conservative nonexplosive countable-state labelled jump generator on an irreducible actual class Gamma, with invariant probability pi. Let a(x) count ALL nominal labelled firings, including null firings. Write
 E(f)=1/2 sum_(x,e) pi(x)q_e(x)[f(x+nu_e)-f(x)]^2.
Assume the available nominal inequalities
 sum pi a(f-pi f)^2<=G E(f),
 Var_pi(f)<=C_P E(f),
 A=pi a<infinity,
 a(x)>=a0(1+|x|)^2, a0>0.
The actual reaction increments and number of labels are fixed and bounded, and rates are locally bounded on finite population balls. In the supplied universal catalytic construction, G,C_P,A,a0^-1 are bounded by explicit fixed-network powers of numerical input size W. Its nominal coefficients/table and computational costs are already constructed. No new physical species, clock or controller is introduced below.

Allow arbitrary unknown bounded measurable multipliers theta_e(t,x) satisfying |theta_e(t,x)-1|<=delta. Errors may depend on the population, the label and time; no distribution, independence or access to them is assumed. Define the actual minimal nonhomogeneous generator by q_e(t,x)=theta_e(t,x)q_e(x). Null firings use the same envelope. This is a broader error model than unknown fixed reaction coefficients.

Choose delta<=1/4 and delta sqrt(2G)<=1/4. Then, for initial density h0 in L2(pi), the actual law has density h_t and
 ||h_t-1||_L2(pi)^2
 <= exp(-t/C_P)||h0-1||_2^2+4 C_P delta^2 A.
For every finite horizon T and initial population u, the expected number of ALL actual firings is at most
 6G log(1/pi(u))+6AT,
after also imposing delta^2 G<=1/8. In particular, no admitted error schedule causes explosion. No stationary law is asserted for a genuinely time-varying generator.

Bounded-form proof. Let B_t=Q_t-Q. For real u,v with pi u=0, channelwise Cauchy-Schwarz gives
 |<u,B_t v>_pi|
 <=delta [sum pi a u^2]^(1/2)[sum pi q_e(Delta_e v)^2]^(1/2)
 <=delta sqrt(2G) E(u)^(1/2) E(v)^(1/2).
Also |<1,B_t v>|<=delta sqrt(2A E(v)). Nominal invariance, without reversibility, gives <e,Qe>=-E(e). Put e=h_t-1. The forward equation therefore yields
 (1/2)partial_t||e||2^2
 =<e,Qe>+<e,B_t e>+<1,B_t e>
 <=-E(e)+delta sqrt(2G)E(e)+delta sqrt(2A E(e))
 <=-(1/2)E(e)+2delta^2 A.
Here the last source term uses a sqrt(E)<=E/4+a^2, with a=delta sqrt(2A). The ordinary gap now gives
 partial_t||e||2^2<=-||e||2^2/C_P+4delta^2 A,
which proves the displayed estimate. No differentiability of the error schedule is needed.

Countable-state justification and firings. Use the accepted stationary-flux finite lumping: a finite population ball remains explicit and its complement is one proof-only state. Nominal pi, E and both inequalities are inherited exactly for functions constant on the tail. Its activity at the tail state is the conditional pi-average of a. Averaging arbitrary theta_e(t,x) with the nominal boundary flux leaves every aggregated off-diagonal rate in the SAME relative envelope. Finite nonautonomous forward equations are well-defined for bounded measurable rates.

For the finite density h and relative entropy H=pi h log h, the channelwise scalar entropy inequality used in the available transfer applies at each time and state. It gives
 H'<=-D(h)/2+2delta^2 E_(h pi)a,
where D(h)=-<h,Q log h> >=2 E(sqrt h). The weighted inequality and (pi sqrt h)^2<=1 imply
 E_(h pi)a<=G D(h)+2A.
Consequently H'<=-D(h)/4+4delta^2 A, and
 integral_0^T E_(h_t pi)a dt<=4G H(0)+4AT.
Multiplying by 1+delta<=3/2 proves the stated actual-firing bound. All constants are uniform in the finite ball. Up to its first exit the finite chain agrees with the actual minimal process. The firing bound passes through increasing stopping balls and prevents explosion (fixed bounded jumps cannot leave every ball in finitely many firings). The same argument counts null labels, rather than confusing spatial jumps with firings.

Finally take the finite-chain L2 bound through those nonexplosive limits. For a point mass at u, ||h0-1||2^2=1/pi(u)-1. Positivity of each atom makes this finite. Uniform L2 bounds and pi-tail tightness pass the law to the actual process and give the inequality by lower semicontinuity. The lower activity bound controls pi |X|^2<=A/a0.

Whole-law and absolute-mean guarantees. Set B=max(1,A/a0) and choose a rational tolerance satisfying
 delta^2<=epsilon^2/(16 C_P A B),
as well as the two smallness conditions above. Choose a rational time T with
 T>=C_P [log(1/pi(u))+log(2B/epsilon^2)].
Then for EVERY t>=T, ||h_t-1||2^2<=epsilon^2/B. Hence TV(Law(X_t),pi)<=epsilon/2 and
 |E X_i(t)-E_pi X_i|<=sqrt(E_pi X_i^2)||h_t-1||2<=epsilon.
The bounds hold simultaneously for every measurable state/time error schedule, even when it never settles. They are endpoint tracking of a FIXED pi, not convergence to pi for a fixed nonzero error and not an invariant-law statement for a nonautonomous process.

Effective resources. A rational upper bound for C_P,G,A,a0^-1 may replace each constant. All needed square-root constraints can be enforced conservatively by reciprocal-polynomial rational choices, without a square-root oracle. For the conditional-Poisson target,
 log(1/pi(u))<=sum_i lambda_i+sum_i [log(u_i!)-u_i log(lambda_i)],
because its class normalizer is at most exp(sum lambda_i). Bounding this above by finite polynomials in W uses u_i log(1+u_i), |log lambda_i| and fixed dimension; ordinary integer/rational upper bounds suffice. Thus T,delta^-1 and firing bounds are fixed-network polynomial in W, and the new tolerance/time arithmetic is polynomial in complete binary input length. The existing fixed family and precomputation are unchanged.

Scope. This proves a new robust nonautonomous/state-error consequence of the activity-weighted construction. It does not remove network-dependent constants, make variable-network compilation uniformly efficient, provide a physical experiment or strengthen an unrelated PDE theorem. It uses the accepted stationary-flux/entropy inequalities and the newly supplied universal nominal catalytic construction at their actual scopes; it does not independently reprove that construction.
