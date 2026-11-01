# Two separately derived corollaries of the reviewed survival proof

These are theorem-only additions by the reviewer. They do not edit the root source, accept an executable, or claim historical priority.

## 1. An explicit trial function is enough; no actual committor is needed

In the reviewed abstract theorem, replace the actual equilibrium committor by ANY h in the killed quadratic-form domain such that h=1 on A, 0<=h<=1 on D=A union S, and E(h,h)<=C0<infinity. Retain the source inverse-form bounds Q_A<=B_A and Q_S<=rho^2 B_A, with M=m(A)>0 and rho=m(S)/M. Then the SAME conclusions hold with

    k0=C0/M,
    epsilon=C0 B_A(1+rho)^2/M^2-1,
    d_init=rho+sqrt(rho(1+rho)).

Proof: Every use of h in the root proof involves only its range/support values, its norm M<=N<=M(1+rho), its form energy upper bound, and inverse-form positivity domination. In particular

    EX=E(h,h)/(N k0)<=1,
    E(1/X)=k0 Q_h/N<=1+epsilon.

No harmonicity, minimizing property, capacity equality, committor equation or pointwise hitting-probability identity is used. The exact initialization difference remains the same because h=1_A+e and 1_D=h+d with e,d supported in S and lying in [0,1]. Form/inverse-form Cauchy implies epsilon>=0 exactly as before.

For the fiber models an explicit choice is the scalar optimal transition profile

    h(y)=1, y<=-b;
    h(y)=R^-1 integral_y^b q(s)^-1 ds, -b<y<b;
    h(y)=0, y>=b,
    R=integral_(-b)^b q(s)^-1 ds.

It has no transverse derivative, lies in [0,1], matches the target trace, and has form energy C0=1/(beta R). It belongs to the killed form domain: its boundedness supplies L2 integrability under the finite reference measure, its derivative is supported on the slab and has the displayed finite energy, and the inherited smooth weighted form admits cutoff approximation. Thus this concrete application can dispense with the actual committor even as an existence object. Source-current admission and exact initialization remain necessary. This is a simplifying strengthening, not a flaw in the frozen committor-based theorem.

## 2. Uniform arithmetic-midpoint rate uncertainty

Let 0<lo<=k0<=hi, and k_star=(lo+hi)/2. For every t>=0, the mean value theorem in the rate gives

    |exp(-k_star t)-exp(-k0 t)|
       <= |k_star-k0| t exp(-lo t).

The supremum of t exp(-lo t) is 1/(e lo). Since |k_star-k0|<=(hi-lo)/2,

    sup_t |exp(-k_star t)-exp(-k0 t)|
       <= (hi/lo-1)/(2e)
       <= (3/16)(hi/lo-1).

The rational constant follows from e>1+1+1/2+1/6=8/3. The strict inequality holds when hi>lo; equality is harmless at zero width. No finite time grid is used.

If a received survival theorem gives absolute error delta about exp(-k0 t), then the same law has uniform absolute CDF/survival error at most

    delta + (3/16)(hi/lo-1)

about the declared midpoint-rate exponential. If T0 is enclosed in [T0_lower,T0_upper], use lo=1/T0_upper and hi=1/T0_lower: arithmetic midpoint in rate is not reciprocal arithmetic midpoint in time.

All interval endpoints, delta, and their input/model bindings still require finite outward receiving. The corollary does not accept a claimed numerical KS value or any numerical exponential evaluation.
