# An attainable quantum mass/range law for finite fractional suppression

FIRST_CONSTRUCTION.md proves for every finite single-link scalar positive harmonic network

(J_rigid-J)/J_Q <= gamma_B (ms^2/M) d^2 k_B T/hbar^2,
gamma_B=6C_B/pi^2,
C_B=sup_(x>0) x^5[2x coth(x)-3]/sinh^2(x),

whenever its internal-CM relative equilibrium rms displacement is at most d. A cap on every internal node relative to the backbone suffices. The present note gives an actual positive network family that attains the consequent mass/range/temperature RESOURCE ORDER. It does not solve the full bounded-range Pareto frontier or prove that its optimum deficit is linear in T.

## 1. Actual retuned family and its full transport spectrum

Choose any fixed mass ratio R=M/m>1 and any fixed a>0. Let ms=M-m and mu_red=m ms/M. At each positive T use ONE side mass and ONE positive spring

r=2theta a,
k=mu_red r^2=4mu_red theta^2 a^2,
theta=k_B T/hbar.

The only intercell spring is the same positive K. At each T every component is positive and finite. Its complete bands are[0,p] union[r,s], where

p^2+s^2=r^2+A,
p^2s^2=B r^2,
A=4K/m, B=A/R.

If r^2/A tends to0, then

p/r ->1/sqrt(R),
s/sqrt(A) ->1.

Assume also sqrt(A)/theta tends to infinity, which is equivalent here. The full optical band starts at r=2theta a and extends far beyond the thermal window. Dominated convergence in the Bose integral gives

J/J_Q ->1-sigma_R(a),
sigma_R(a)=(6/pi^2) integral_(a/sqrt(R))^a (x/sinh x)^2 dx>0,
J_Q=pi^2theta/3.

The same-M,K rigid comparator satisfies J_rigid/J_Q->1. Both statements include the full optical band; it is precisely the finite missing interval between the rescaled acoustic edge and optical start that supplies the limiting suppression.

At fixed m,M,K this gives a nonzero fractional suppression while k is proportional to T^2. Choosing a=x_R recovers the earlier optimum, but no optimality is needed for the present construction.

## 2. Actual Gibbs variance, rather than only its classical floor

The physical internal relative coordinate is Y=x_side-x_backbone. Its mass-normalized force vector is

w=(-1/sqrt(m),1/sqrt(ms)), ||w||^2=1/mu_red.

For Bloch wave number q let v_q=4K sin^2(q/2). Its two-mode matrix is

D_q=[ (v_q+k)/m         -k/sqrt(m ms) ]
    [ -k/sqrt(m ms)      k/ms         ].

The static contraction is exactly w^T D_q^+w=1/k, with the pseudoinverse needed only at q=0. At each fixed q!=0, as r^2/A tends to0 the low-frequency mode has

omega_low=r/sqrt(R)[1+o(1)],
|w dot e_low|^2=1/ms[1+o(1)],

while the high-frequency mode tends to the backbone mode. If m,ms vary proportionally at fixed R, the same relative statements hold. In particular the high frequency divided by theta tends to infinity.

For fixed masses the low mode then gives the pointwise limit

T Var_q(Y) -> hbar^2 sqrt(R)/(4ms k_B a) coth(a/sqrt(R)),

and the high-mode contribution to T Var_q(Y) tends to0.

The thermodynamic-limit local variance is the Bloch average. To justify passing the limit through that average, use for x>0

coth x<=1+1/x.

The mass-normalized quantum covariance therefore obeys

Cov_q <= (hbar/2)D_q^(-1/2)+k_B T D_q^(-1)

on its positive subspace. Spectral Cauchy-Schwarz gives

w^T D_q^(-1/2)w
 <=sqrt[(w^Tw)(w^T D_q^(-1)w)]
 =1/sqrt(mu_red k).

Thus for EVERY q, with translation removed at q=0,

Var_q(Y) <= hbar/(2sqrt(mu_red k))+k_B T/k
          = hbar^2/(4mu_red k_B T)(1/a+1/a^2).

This bound is uniform in q. It proves dominated convergence after multiplying by T for fixed masses. The exceptional q=0 point has zero weight in the thermodynamic limit. Consequently the ACTUAL quantum variance satisfies

Var_infinity(Y)
 = hbar^2 sqrt(R)/(4ms k_B T a) coth(a/sqrt(R)) [1+o(1)]
 = [k_B T/k] [ (a/sqrt(R))coth(a/sqrt(R)) ] [1+o(1)].

Both the lower bound from FIRST_CONSTRUCTION.md and this upper/asymptotic calculation include quantum zero-point motion. Therefore a constant fractional suppression with Var of order1/T is actually attained in the ideal model; it is not merely suggested by a static compliance calculation.

Here Var_infinity(T) is the limit of the local relative-coordinate variance on finite periodic rings at each T, with only the global translation removed. Absolute one-dimensional acoustic displacement is not used. The finite-ring variance obeys the same uniform upper bound at every T.

## 3. A bounded-range family that pays the necessary mass order

Now allow total moving mass to be a priced resource. Keep R,K,a fixed and let

M(T)=Q_M/T,
m(T)=Q_M/(RT),
ms(T)=Q_M(1-1/R)/T,
mu_red(T)=Q_mu/T,
Q_mu=Q_M(R-1)/R^2>0.

Then k(T)=4Q_mu(k_B/hbar)^2 a^2 T, and

r^2/A is proportional to T ->0,
Omega/theta is proportional to T^(-1/2) ->infinity.

Thus this family has the same strictly positive limiting fractional suppression sigma_R(a), but the uniform quantum variance bound becomes the T-independent value

Var(Y)<= hbar^2/(4k_B Q_mu)(1/a+1/a^2).

Choose

Q_mu >= hbar^2/(4k_B d^2)(1/a+1/a^2)

to guarantee the fixed rms cap d for EVERY T in the ideal model, not just asymptotically. There is only one internal mass, so its individual relative-coordinate cap is exactly the CM cap. No uncounted dark displacement is needed.

The actual thermodynamic-limit variance tends to the finite value

hbar^2 sqrt(R)/[4Q_M(1-1/R) k_B a] coth(a/sqrt(R)),

as follows by the same uniform bound and pointwise mode limit. The backbone high-mode contribution tends to0; its frequency is of order sqrt(T), while its observable weight is of order T.

Combining necessity with this construction gives a resource-order statement: for fixed R and a nonzero limiting fractional suppression in the regime Omega/theta->infinity, the product M T d^2 must remain bounded below by a positive constant. Mass proportional to1/(T d^2) is sufficient, with a positive finite network at each T. The constants above are not a sharp Pareto frontier.

For a simple exact natural-unit object set hbar=k_B=K=1, R=4, a=2, Q_M=4. Then

m=1/T, ms=3/T, M=4/T,
r=4T, k=12T,
Var(Y)<=1/4,
lim Var_infinity(Y)=coth(1)/12,
lim (J_rigid-J)/J_Q=(6/pi^2) integral_1^2 (x/sinh x)^2 dx>0.

Every quantity here is specified, and the variance cap is analytic. No temperature grid is a premise.

## 4. Interpretation and scope

The necessary mass/range cost now applies away from the exact thermal optimum, and an equally informed conventional one-resonator network attains its order. Extra topology is not needed for that operation. A fixed-mass design cannot retain the same suppression merely by approaching the optimum imperfectly or adding more finite modes while keeping all relative rms motion bounded.

This does not price the work of retuning an existing device. It is a family of separately specified passive harmonic designs, with mass, spring stiffness and equilibrium variance counted. Connector material, contact transport, additional polarizations, geometry/strain, damping and anharmonic stability have not been acquired. The growing mass is explicit; it is not a finite-material construction or a zero-cost way around the range bound. Multiple-intercell-link models require separate analysis because the indicator/moment argument used for necessity can fail there.
