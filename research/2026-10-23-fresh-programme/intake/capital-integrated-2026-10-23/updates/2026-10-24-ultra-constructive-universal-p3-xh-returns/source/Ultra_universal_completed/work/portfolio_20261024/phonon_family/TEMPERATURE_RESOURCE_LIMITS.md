# Resource limits of the temperature-adapted optimum

This is a structural corollary of FAMILY_THEOREM_v3.md, not a temperature sweep and not a fixed-device performance claim. Keep A=4K/m0>B=4K/M fixed and define R=A/B=M/m0>1. Temperature is represented by theta=k_B T/hbar.

## 1. Exact low-temperature design law

Let r_*(theta) be the unique OPTIMIZED optical frequency, with p_*(theta)<r_*<s_*(theta). Define f(x)=(x/sinh x)^2 and C=integral_0^infinity f=pi^2/6.

Then as theta tends to zero,
r_*(theta)/(2theta) -> x_R,
where x_R is the unique positive solution of
sinh x_R=R^(3/4) sinh[x_R/sqrt(R)].

The complete optimized thermal conductance has the limit
J_opt(theta)/(pi^2 theta/3)
-> 1-(6/pi^2) integral_(x_R/sqrt(R))^x_R f(x)dx,
which lies strictly between zero and one for every fixed finite R>1.

Its required internal spring is
k_*(theta)
=4theta^2 x_R^2 m0(M-m0)/M [1+o(1)].
Thus the low-temperature family uses a RETUNED soft internal spring. Every fixed cell with fixed positive spring still has its usual leading single-channel quantum at sufficiently low temperature.

### Proof of the optimized limit

Put r=2theta x with x fixed. The attainable endpoint formula gives
p/(2theta) -> x/sqrt(R),
s/(2theta) -> infinity.
Uniformly on positive compact x intervals,
j(2theta x)/(2theta) -> Gamma_R(x)
=integral_0^(x/sqrt(R)) f + integral_x^infinity f
=C-integral_(x/sqrt(R))^x f.

The optimum's scaled x cannot tend to zero: the optical passband then recovers the full limiting integral C. It cannot tend to infinity either, because
p/(2theta)>=sqrt(B)/sqrt[4theta^2+A/x^2] -> infinity,
so its acoustic band recovers C. A fixed finite x has Gamma_R(x)<C, contradicting either escape for an optimizing sequence. Hence the minimizers lie in a compact positive x interval and every limit minimizes Gamma_R.

Its stationary condition is
f(x/sqrt(R))/sqrt(R)=f(x),
equivalent to the stated sinh equation. The ratio sinh x/sinh(x/sqrt(R)) increases strictly from sqrt(R) to infinity: its logarithmic derivative has the sign of
x coth x-[x/sqrt(R)]coth[x/sqrt(R)],
and t coth t is strictly increasing for t>0. Since R^(3/4)>sqrt(R), the positive root exists and is unique. Therefore all optimizing sequences converge to x_R.

The normalization pi^2theta/3 is the full single-acoustic-channel ideal Bose integral. The inequality does not violate it: the material parameters vary with temperature before taking the limit.

## 2. Large mass-ratio cost after that limit

In the subsequent limit R→infinity,
x_R=(1/4)ln R+ln ln R-ln2+o(1),
and
Gamma_R(x_R)
=[x_R+1/2+O(1/x_R)]/sqrt(R).
Consequently
J_opt/J_quantum ~ [3/(2pi^2)] ln(R)/sqrt(R)
in the iterated limit theta→0 first, then R→infinity.

Indeed x_R/sqrt(R) tends to zero, so the root equation becomes
exp(x_R)=2R^(1/4)x_R[1+o(1)].
The remaining low acoustic integral is x_R/sqrt(R) to leading order; the high-frequency Bose tail is[1/2+O(1/x_R)]/sqrt(R). Increasing suppression therefore spends increasing side mass, even in the ideal harmonic family.

No finite-R zero-conductance construction or uniform-in-both-limits statement is asserted.

## 3. A necessary displacement-range cost

For a finite harmonic mass/spring network with its global translation removed, the quantum thermal position covariance satisfies
Cov(u)>=k_B T K_elastic^+
as a quadratic-form inequality on translation-free coordinates. Diagonalizing the harmonic modes reduces it to
x coth x>=1
for each positive mode.

For the pendant coordinate y=x_side-x_backbone, static force-pair compliance is EXACTLY1/k: applying unit force to the side and opposite force to its backbone only stretches their joining spring, with no net backbone load. Therefore
Var(y)>=k_B T/k.

For the retuned low-temperature optimum, restore physical units and write the reduced mass
mu_red=m0(M-m0)/M.
Since r_phys~2(k_B T/hbar)x_R and k_*=mu_red r_phys^2,
Var(y) >= hbar^2/[4 mu_red k_B T x_R^2] [1+o(1)].

A fixed allowed rms displacement d_max therefore requires, necessarily,
mu_red T >= hbar^2/[4 k_B x_R^2 d_max^2] [1+o(1)].

Thus k_* proportional to T^2 is not a free physical resource: a fixed-mass, fixed-displacement harmonic implementation cannot follow the ideal retuned family indefinitely toward zero temperature. Larger moving mass or displacement range, additional confinement or a different physical contract is required. The inequality is necessary, not a fabrication sufficiency condition.

For a periodic chain this statement can be obtained on a finite ring with the zero translation removed and then passed to its limit; the relative pendant coordinate has finite static compliance1/k. It does not rely on the divergent absolute position of a free one-dimensional acoustic field.

## 4. High-temperature cost

As theta→infinity with K,M,m0 fixed, r_*(theta) must diverge and therefore k_*(theta) diverges.

If a bounded subsequence of r_* existed, passband endpoints would remain bounded, g_theta would tend uniformly to1, and j(r_*) would tend to a finite-resonator classical bandwidth strictly GREATER than the rigid width sqrt(B). But the optimum is always no greater than the rigid-chain finite-T conductance, which tends to sqrt(B). This contradiction excludes bounded r_*.

This explains compatibility with the classical lower bound: the optimizing family moves to unbounded internal stiffness; it does not give a fixed finite-resonator classical violation. No rate or uniform stiffness cap is hidden in the theorem.

## Scope

These laws concern design at each temperature, not active thermal retuning during a cycle. They do not price the work/control needed to change a spring in an existing device. They establish an explicit mass, stiffness and displacement boundary for interpreting the mathematical optimum. No equipment action, measured thermal effect or physical realization is inferred.

