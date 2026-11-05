# Finite-record inference, preparation and observation costs

The [population theorem](README.md) bounds a stationary expectation. The [final report](package/reflection_report.tex) and [learning/finite-data audit](package/audit_notes/learning_audit.md) supply two distinct operational protocols. They do not justify substituting a raw empirical score into the population bound.

## One stationary uninterrupted recording

Prespecify an endpoint score `g`, nonnegative central weight `w`, lag `t` and validation count `n`. Consecutive blocks share boundary readings:

\[
Z_j=w(Y_{(2j-1)t})g(Y_{(2j-2)t})g(Y_{2jt}).
\]

For `|g|<=G`, put `B=G^2`. Under **every stationary equilibrium all-even hidden chain in the class**,

\[
P(\overline Z\le-z)
\le e^{-n\,kl((1+z/B)/2\,||\,1/2)}
\le e^{-nz^2/(2B^2)}.
\]

The tilted two-step transition operator has positive-semidefinite coefficient factorizations. Dropping negative odd terms in operator order yields the exponential-moment bound `E exp(-theta sum Z_j)<=cosh(theta B)^n`. This handles the shared-boundary dependence without hidden state count, a spectral gap or a mixing-time input. It does not make the blocks IID.

A separate additive-reversibilization/data-processing argument supplies a conservative quantitative rate interval. For total block duration `T=2t`, let `q(z)` be the first displayed exponential tail bound. Set

\[
L_\delta(z)=\begin{cases}
4\,kl(\delta||q(z))/(nT),&q(z)<\delta,\\
0,&q(z)\ge\delta.
\end{cases}
\]

Then `P(L_delta([-Zbar]_+)>sigma)<=delta`. Strong rejection of equilibrium can coexist with a weak numerical lower rate bound; these endpoints are not interchangeable.

In the [supplied fixed-seed synthetic run](package/simulation_results.json), `a=1,epsilon=.4,t=1`, score center `.37` and 750,000 consecutive blocks give empirical mean `-.01041134`, equilibrium tail bound `9.7436e-6` and conservative 95% rate floor `1.0092e-6`. It uses 1,500,001 binary readings and 1,500,000 modeled time units. The known synthetic initial state was drawn exactly from the uniform stationary law.

Stationary **microscopic** initialization is essential. Apparent stationarity or exponential visible correlation does not prove that premise. The score and sample count are fixed independently of validation. Learning on an earlier dependent path and applying the same bound conditionally, optional stopping or arbitrary postselection needs a new justification. A finite predeclared score family can be protected by a union bound.

## Arbitrary start with a supplied mixing envelope

The second protocol assumes the additional apparatus input

\[
\sup_x TV(P_s(x,\cdot),\pi)\le e^{-\kappa s}.
\]

Before each training or validation block, it waits `kappa^(-1) log[8(N+M)/delta]`. Sequential coupling controls the deviation from independent stationary blocks. Training chooses a center, frozen before validation. This route pays preparation/waiting rather than inferring hidden mixing from visible pair correlations.

For the explicit family, `kappa=a-2epsilon` follows from a uniform-refresh component. The executed run starts at hidden state 0 and never resets between blocks. At `a=1,epsilon=.4`, it uses 20,000 training and 750,000 validation blocks, 2,290,000 readings and a gap of about 93.15 time units before each block. Total modeled duration is 73,242,880.5. The 95% linear/nonlinear rate floors are `.00940259/.00943212`, against generating rate `.43944492`.

These durations are modeled physical time, not CPU benchmark times. Both protocols sample exact CTMC transition kernels at observation times in a synthetic model; this is not an Euler time-step approximation or an implemented laboratory apparatus. Hardware preparation, sensor energy, metrology and real-time access are not experimentally delivered.

## Weak-signal acquisition and calibrated readout

For independent triples at fixed `a,t`, set `r=e^(-at)` and `m=r^2(epsilon t)^2`. The exact chi-square divergence from the equilibrium telegraph triple law is `m^2/(1-r^2)^2`. Distinguishing with both error probabilities at most `delta<1/2` requires

\[
N\ge\frac{(1-r^2)^2}{m^2}(1-2\delta)
\log\frac{1-\delta}{\delta}.
\]

Bounded-score validation matches order `Theta(epsilon^(-4) log(1/delta))` for that **independent fixed-lag triple observation model**. It is not a lower bound for all continuous, adaptive-timing or intervention experiments. Power of the uninterrupted test on the constructed alternative is proved separately; its null guarantee itself still uses no mixing input.

The exact centered mean is `C(c)=((c-r)^2-m)/2`, so `O(epsilon)` centering accuracy suffices and costs `O(epsilon^(-2))` independent training samples at fixed `a,t`.

Independent calibrated observation flips with known probability `rho<1/2` can be inverted to an unbiased score, with conservative sample penalty `O((1-2rho)^(-6))`. The corrected central weight can be negative. That correction is covered by the preparation/validation route; the uninterrupted nonnegative-weight proof cannot be applied unchanged. Unknown sensor memory, backaction and timing uncertainty are outside the declared observation model.

All supplied [code and outputs](package/README.txt) are preserved without a new Capital simulation, inference run or audit.
