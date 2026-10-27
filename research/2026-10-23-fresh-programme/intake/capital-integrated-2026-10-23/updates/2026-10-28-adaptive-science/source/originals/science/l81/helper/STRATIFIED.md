# Audit: independent stratified covariance-action times

The stratified variant is sound and keeps the proved general full-law upper bound. It changes the sine-family obstruction, so the iid-time matching lower bound must not be promoted to this variant.

## General construction and unchanged upper bound

For k action calls, independently draw T_j uniform on [(j-1)/k,j/k], use an independent Gaussian center C_j, and compose two fresh R22 heat actions at c_j=sqrt(T_j)C_j, s_j=sqrt(1-T_j). Let

    Sigma_j = k integral_((j-1)/k)^(j/k)
                   E[H_sqrt(1-t)(sqrt(t)C)^2] dt.

Then E[J_j(v)|v]=Sigma_j v, ||J_j(v)||<=L^2||v||, Sigma_j is PSD, and k^(-1)sum_j Sigma_j=Sigma. Consequently

    E[Jbar_k(Z)|Z]=Sigma Z,
    E[||Jbar_k(Z)-Sigma Z||^2 | Z]
       = k^(-2)sum_j E[||J_j(Z)-Sigma_j Z||^2 | Z]
       <= L^4||Z||^2/k.

The equality uses conditional independence of the nonidentically distributed calls given Z. Thus every step of the implemented-randomization proof is unchanged, as are the deterministic comparison, query cap n+4k and mean preservation. The parent's safe all-n bound therefore applies verbatim:

    TV <= [L^2 sqrt(d)/n^(3/2)+L^4 sqrt(d)/(4 tau^2 n^2)]/(2 eta^2)
          + L^4 d/(8 tau^2 eta^2 n^2 k).

No stronger general bound follows here merely from stratifying T. The internal secant/center randomness remains charged. Adaptive time choices would require a different unbiasedness argument.

## Exact sine-family time variance

For g_i(x)=sin(x_i), retain v=(1-exp(-2))/2 and q(t)=exp(-1)cosh(t). Let qbar=k^(-1)sum_j q(T_j). The stratified average is exactly unbiased: E qbar=v. If a_j=(j-1)/k,b_j=j/k, then

    E q(T_j)=k exp(-1)[sinh(b_j)-sinh(a_j)],
    E q(T_j)^2=exp(-2)[1/2+(k/4)(sinh(2b_j)-sinh(2a_j))].

Summing their variances gives the exact expression

    Var(qbar)=exp(-2){(1/2+sinh(2)/4)/k
                      -k[cosh(1/k)-1]
                      -(sinh(2)/2)tanh(1/(2k))}.

In particular,

    Var(qbar)=exp(-2)[sinh(2)-2]/(48 k^3)+O(k^(-5)).

A simple bound avoids cancellation in this formula. Since sup_[0,1] q'(t)=v, the independent-pair variance identity implies Var(q(T_j))<=v^2/(12k^2), hence

    Var(qbar)<=v^2/(12k^3).

Also, by monotonicity, every realized stratified average lies between the lower and upper Riemann sums, so

    |qbar-v| <= [q(1)-q(0)]/k.

This is a pathwise quadrature-error bound, not an expectation bias: the expectation bias is exactly zero. The iid-time proof used sqrt(k)(qbar-v)=>a nondegenerate normal; that step fails under stratification because the variance is O(k^(-3)). Therefore the previous iid-time d^(1/3) architecture lower bound does not cover this variant. This does not by itself prove a better general sampler.

## Residual covariance barrier after perfect first-order cancellation

For either time schedule, the actual covariance is

    Cov(Y)=sigma^2 I+E[Jbar_k(Z)Jbar_k(Z)^T]/(4 tau^2 n^2)
          >=sigma^2 I+Sigma^2/(4 tau^2 n^2).

The inequality is conditional Jensen using E[Jbar_k(Z)|Z]=Sigma Z. Covariance alone is not a TV lower bound. The sine family's coordinate-shell structure supplies the stronger law statement below.

In its coupled diagonal surrogate, conditional on all T_j the variance is

    sigma^2+(v-qbar)/n+Rbar/(4 tau^2 n^2),
    Rbar=qbar^2+k^(-2)sum_j[r(T_j)-q(T_j)^2],
    r(t)=[1+2exp(-2)+exp(-4)cosh(4t)]/4.

The conditional coordinate fourth moments are uniformly bounded. If k->infinity, n/k^(3/2)->0 and n=o(d^(1/4)), then

    n(v-qbar) -> 0 in L2,
    Rbar -> v^2 in probability,
    n^2[||Y||^2/d-sigma^2] -> v^2/(4 tau^2)>0 in probability.

The conditional-coordinate error is O(n^2/sqrt(d)); the actual-versus-surrogate error is O(n sqrt(log(2d)/d)) in L1, both vanishing. Under the target Gaussian the same scaled shell tends to zero. Thus TV->1 in this parameter regime. With perfect qbar=v the same positive n^(-2) variance defect remains, provided Rbar tends to v^2. For balanced n=k=N->infinity, this proves a d^(1/4) obstruction when N=o(d^(1/4)), rather than the iid-time d^(1/3) obstruction.

This is a scoped lower bound for the first correction, and does not exclude removing the n^(-2) term with a further acquired positive correction. It also does not establish that d^(1/4) queries suffice for arbitrary conservative g.

## Final audit: all deterministic allocations below d^(1/4)

The parent proposed a stronger stratified lower bound, verified here. For this exact stratified first correction on the sine family, ANY deterministic positive-integer allocation

    Q(d)=n(d)+4k(d)=o(d^(1/4))

has TV error tending to one. This is an architecture-level obstruction only. The general proved upper bound is still d^(1/3), so this does not close the gap between the upper and lower bounds for stratification.

For k->infinity, define

    W_k=k^(3/2)(qbar-v),
    c_star=exp(-2)[sinh(2)-2]/48>0.

The exact variance calculation gives Var(W_k)->c_star. Moreover

    W_k=sqrt(k)sum_j[q(T_j)-E q(T_j)],

with independent centered summands bounded by sup|q'|/sqrt(k). Thus the triangular-array Lindeberg condition holds and W_k=>N(0,c_star). Also Rbar->v^2 in probability. Write gamma_d=n/k^(3/2).

If gamma_d tends along a subsequence to gamma_0<infinity, use the shell normalization n^2. Then

    n^2 delta=-gamma_d W_k+Rbar/(4 tau^2)
       => -gamma_0 N(0,c_star)+v^2/(4 tau^2).

The limit is a positive constant when gamma_0=0, and otherwise is a nondegenerate shifted normal with no atom at zero. If gamma_d->infinity, normalize instead by a_d=n k^(3/2)=n^2/gamma_d<n^2. Then

    a_d delta=-W_k+Rbar/(4 tau^2 gamma_d)=>N(0,c_star).

At either normalization, the target shell fluctuation and conditional-coordinate error vanish because n^2/sqrt(d)<=Q^2/sqrt(d)->0. The actual-versus-surrogate error is bounded by its n^2-normalized value O(n sqrt(log(2d)/d)), also vanishing. A shrinking shell event separates every continuous limiting law from the degenerate target, or separates the positive constant directly. Convergent subsequences in the compact extended interval [0,infinity] cover arbitrary gamma_d.

If k stays bounded, pass to a fixed k. For n->infinity, the n-normalized variance defect tends to v-qbar and has no atom at zero. For fixed n,k the defect is analytic and not identically zero on the open product of stratum intervals. To check nonidentity rigorously, the same analytic expression extends to the connected cube (0,1)^k. If it vanished identically on the stratum rectangle, analytic continuation would force it to vanish throughout that cube; taking all T_j down to zero contradicts q(0)<v and the positivity of the quadratic term. Its zero set therefore has measure zero. This completes the subsequence audit.

## Final audit: Loewner monotonicity of the covariance integrand

Let B_t be standard Brownian motion and use the bounded self-adjoint matrix martingale

    H_t=E[Dg(B_1)|F_t],   M(t)=E[H_t^2].

This M(t) is precisely the covariance integrand used above: the conditional heat Hessian is evaluated at B_t with remaining scale sqrt(1-t). For 0<=t<u<=1, the martingale property and self-adjointness give

    M(u)-M(t)=E[(H_u-H_t)^2] >=0.

The cross terms vanish after conditional expectation, without a commutativity assumption. Also 0<=M(t)<=L^2 I. For arbitrary T_j in the jth stratum, both the realized matrix average and its integral lie between the same Loewner lower and upper Riemann sums. Those brackets differ by the telescoping matrix

    [M(1)-M(0)]/k <= L^2 I/k.

Therefore, pathwise,

    ||k^(-1)sum_j M(T_j)-Sigma||op<=L^2/k.

This receipt uses no derivative continuity beyond the bounded terminal weak Hessian; the martingale and its terminal limit justify endpoints. It is useful analysis of the shared-time component. It does not acquire M(t), remove the random Gaussian centers or secant action variance, or improve the stated general full-law bound by itself.
