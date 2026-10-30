# Synchronous analog centering with unknown passive memory

The first-return obstruction showed that passive memory can hide an incremental
response behind a bounded ADC for a paid finite service horizon. Its positive
certificate reduced probe amplitude to control clipping bias. With fixed
nonzero quantization step, that sufficient certificate contains an
epsilon^{-3} acquisition term.

This continuation asks a different, concrete question: can a bounded signed
analog reference convert clipping bias into loss of sensitivity at an unknown
root, and what precision resource does that operation require? The answer is
yes under an explicit measurement contract. Ordinary interval identification
then obtains a finite-confidence epsilon^{-2} window bound, up to logarithms,
while retaining unknown passive memory and a fixed finite-level ADC. A
calibration indistinguishability result shows why reference accuracy cannot be
treated as free. No advantage over ordinary methods with the same reference
operation is claimed. The original fixed-ADC minimax rate remains unresolved.

The first-return scientific artifacts remain unchanged.

## 1. Two failed attacks determine the mechanism

Keep the first-return scalar physical interface

\[
 y_t=a u_t+h_t,\quad |a|\leq1,\qquad
 \sum_{t\leq n}y_t^2\leq E_0+\sum_{t\leq n}u_t^2.                  \tag{1}
\]

The unknown old field h_t is predictable before the fresh current sign.
Neither mixing, dimension, a decay law, nor a reset is supplied. The ADC
contract remains conditional unbiased stochastic rounding of its clipped
input, bounded by R, with rounding variance at most Delta^2/4 and
Delta=2R/(L-1). The complete conditional measurement chronology matters.

Digitally forming a residual after clipping fails. For signed input
u=eta*sigma, a candidate c, and Q measuring C_R(y),

\[
 \mathbb E[\sigma(Q-c\eta\sigma)/\eta\mid\mathcal H]
 =a\theta(h,a\eta)-c.                                               \tag{2}
\]

Even c=a is generally not a root. In the executed exact scalar counterexample,
R=1, eta=.125, a=c=.6 and h=2. Both input signs saturate. The expected digitally
formed score is -.6 at the true gain.

Now supply an analog reference r=c*u **before** the clipping element, and
measure C_R(y-r). At c=a its sign-demodulated mean is zero, including when it
clips. In that same example the expected analog-centered score is exactly
zero. But a second attack also fails: zero score alone is not a stopping rule.
With the wrong candidate c=0 and the same h=2, both signs still saturate and
the mean score is again zero. A known energy budget must guarantee enough
sensitive windows before a zero score has information content.

This rules out both a digital fix to the existing record and an unqualified
analog nulling claim. The construction below accounts for the missing
sensitivity explicitly.

## 2. The enabling operation and its costs

During a block, choose candidate c before drawing any of its fresh signs.
Apply u_t=eta*sigma_t to the specimen, and send the following residual to the
ADC:

\[
 v_t=y_t-(c+\zeta_t)u_t
     =h_t+(a-c-\zeta_t)\eta\sigma_t,\qquad |\zeta_t|\leq\rho.       \tag{3}
\]

The gain-reference error zeta_t is predictable before the current sign. The
analog reference is therefore a synchronous signed feedforward quantity; it
is not an unobserved arbitrary current-sign-correlated rounding error. The
measurement device must warrant its range, accuracy, loading, and conditional
ADC contract. Its summing/readout stage must preserve the fixed specimen
response and the physical passivity contract in (1).

In a differential electrical or optical readout this is a reference supplied
at the detector, after the specimen response. A new calibrated summing channel
and its power, loading, noise and timing are real enabling resources. No such
apparatus has been built here. The algorithm requires at most reference
amplitude eta*(1+rho), and a gain-reference accuracy rho. If a reference DAC
alone supplies that error budget by nearest-level rounding, it needs step at
most 2 eta rho across approximately [-eta,eta], or at least ceil(1/rho)+1
levels. Extra transfer/calibration error consumes part of the same rho budget.
The code uses a finite reference grid and certifies using its error bound.

For the two-level ADC execution, conditional stochastic rounding has the
equivalent mathematical implementation of one comparator with a fresh uniform
random threshold in [-R,R]. Its threshold generation and complete conditional
calibration are inherited measurement assumptions, not free physical facts.
A finite-precision threshold generator must supply an adequate mean-error
bound; an arbitrary sign-correlated comparator error is not covered.

The strongest equally informed ordinary competitor can use exactly (3) and the
interval estimator below. Analog nulling and bisection are ordinary methods.
The new claim is the scoped passive-memory confidence construction, not the
invention of those methods or a separation from them.

## 3. A block theorem with nonzero reference error

At the start of a block, suppose the controller's retained record already
gives an interval I=[l,h] containing a, of width w, and choose c=(l+h)/2.
Let E be a warranted upper energy budget for the block. E can conservatively
be E_0 plus all earlier incident specimen energy. Even without observing the
current stored state, the global prefix inequality (1) gives the required
block output-energy bound with this E.

Use N input packets of amplitude eta. Define

\[
 q_{\max}=w/2+\rho,\quad M=R-q_{\max}\eta>0,\quad
 H=2E+4N\eta^2,\quad \beta=H/(NM^2),\quad\kappa=1-\beta,            \tag{4}
\]

\[
 \widehat z=\frac1{N\eta}\sum\sigma_tQ_t,\qquad
 x=\log(2/\delta_b),                                                \tag{5}
\]

\[
 \nu=\frac{\sqrt{2(H+N\Delta^2/4)x}}{N\eta}
     +\frac{2(R+q_{\max}\eta)x}{3N\eta},\qquad e=\nu+\rho.          \tag{6}
\]

**Block theorem.** Conditional on any past for which a is in I and the stated
energy/measurement contracts hold, with probability at least 1-delta_b,

\[
 |\widehat z-(a-c)\tau|\leq e
 \quad\text{for some}\quad\tau\in[\max(0,1-\beta),1].               \tag{7}
\]

This is a uniform-in-old-state theorem; no favorable warm trajectory is
selected for its probability guarantee.

*Proof.* The true physical field, before the downstream reference is added,
obeys the same pathwise bound as the first-return proof:

\[
 \sum h_t^2\leq2E+4N\eta^2=H.                                      \tag{8}
\]

For s=a-c and d_t=s-zeta_t, fresh signs and conditional ADC rounding give

\[
 m_t=\mathbb E[\sigma_tQ_t/\eta\mid\mathcal H_t]
 =\frac{C_R(h_t+d_t\eta)-C_R(h_t-d_t\eta)}{2\eta}
 =d_t\theta_t,\quad0\leq\theta_t\leq1.                            \tag{9}
\]

Because |d_t|<=q_max, the attenuation loss is bounded by

\[
 1-\theta_t\leq\mathbf1\{|h_t|>M\}\leq h_t^2/M^2.                 \tag{10}
\]

When d_t=0, theta_t may be set to one. Averaging gives tau=mean(theta_t)>=kappa
and mean(m_t)=s*tau-mean(zeta_t*theta_t). The final term has magnitude at most
rho. The energy argument gives sensitivity, not direct access to h_t.

For X_t=sigma_t Q_t/eta and D_t=X_t-m_t, |D_t|<=R/eta+q_max. Clipping cannot
increase distance from the point sigma_t*d_t*eta, which lies inside [-R,R].
Fresh rounding therefore implies

\[
 \operatorname{Var}(D_t\mid\mathcal H_t)
 \leq\mathbb E[(X_t-d_t)^2\mid\mathcal H_t]
 \leq(h_t^2+\Delta^2/4)/\eta^2.                                   \tag{11}
\]

The two-sided bounded-martingale Bernstein/Freedman bound, with the
conservative 2/3 linear term as in the first-return proof, yields
|mean(D_t)|<=nu with probability at least 1-delta_b. Combining with (9)-(10)
proves (7). The reference can be changed using earlier blocks' records without
invalidating freshness within the next block. QED.

## 4. A computable confidence interval and finite progress

Suppose beta<1/2. Let z_l=z_hat-e and z_h=z_hat+e. The confidence interval for
s=a-c has endpoints

\[
 s_l=\begin{cases}z_l/\kappa&z_l<0\\z_l&z_l\geq0\end{cases},
 \qquad
 s_h=\begin{cases}z_h/\kappa&z_h>0\\z_h&z_h\leq0.\end{cases}        \tag{12}
\]

Intersect [c+s_l,c+s_h] with I. It contains a on the block confidence event.
If

\[
 \nu+\rho\leq\frac{w(2\kappa-1)}4,                                \tag{13}
\]

the intersection has width at most w/2. To see this, when the score band has
one sign its width is at most

\[
 \frac{w(1-\kappa)}{2\kappa}+\frac{2e}{\kappa}\leq w/2.            \tag{14}
\]

Here |z_hat|<=w/2+e was used. When the score band crosses zero, its width is
2e/kappa, which also satisfies the bound. Intersecting with I only reduces
width. Padding that interval inside I to exactly w/2 preserves coverage and
makes the next experiment budget deterministic.

Start at [-1,1], use K=ceil(log2(1/epsilon)) blocks, and allocate delta/K failure
probability to each. Stop after K half-width reductions. Except on an event
of probability at most delta, every update contains a and the final gain
radius is at most epsilon. If a computed intersection is empty or fails its
required progress bound, the executable retains the earlier interval and
returns its actual larger radius; it does not manufacture a successful stop.

For the scalar control task u*(a)=ab/(a^2+lambda), map the final gain interval
through that function, checking its endpoints and any included points
plus/minus sqrt(lambda). The midpoint and half-width of its image are the
exact minimax command and distance certificate for that uncertainty interval.
The generic task radius is at most |b|*epsilon/lambda.

## 5. A closed finite-service upper bound

The executable minimizes each block size over the explicit inequalities
(4), (6) and (13). A simpler conservative analytic budget demonstrates the
precision exponent without numerical optimization.

Take 0<eta<=R/8 within the warranted actuator limit, 0<epsilon<=1/2,
rho=epsilon/32, K=ceil(log2(1/epsilon)), and x=log(2K/delta). Set

\[
 n_1=\left\lceil\max\left\{\frac{128E_0}{R^2},
                   1024(R/\eta)^2x,1\right\}\right\rceil,
 \qquad n_k=4^{k-1}n_1.                                            \tag{15}
\]

Then all K confidence intervals can be halved with the declared failure
allocation. In particular,

\[
 N_{\rm total}=n_1(4^K-1)/3<\frac{4n_1}{3\epsilon^2}.               \tag{16}
\]

*Verification.* Before block k, earlier drive energy is at most
eta^2*n_k/3. Thus H/n_k <= 2E_0/n_k+(14/3)eta^2 <= 17R^2/192.
Throughout the construction q_max<=2, so M>=R-2eta>=3R/4. Consequently
beta<=17/108<1/4, kappa>3/4, and the right side of (13) is at least w_k/8.
Also Delta<=2R. Equation (6) is bounded by

\[
 \nu_k\leq (R/\eta)\sqrt{(209/96)x/n_k}
             +5Rx/(6n_k\eta).                                    \tag{17}
\]

Since w_k=2/2^{k-1}, the second term of (15) makes each term in (17) at most
w_k/32. Finally rho<=w_k/64, so nu_k+rho<=5w_k/64<w_k/8. This proves (13).
QED.

For a fixed amplitude fraction eta/R, (16) is an epsilon^{-2} window bound
up to log(K/delta). The finite ADC level count is fixed. The extra resource
is reference accuracy rho proportional to epsilon, requiring order
epsilon^{-1} calibrated reference levels over fixed reference range. Probe
energy and reads both scale as epsilon^{-2} in this conservative construction.
This removes the epsilon^{-3} term from the **first-return sufficient
certificate**. It is not a lower-bound separation from every fixed-ADC
estimator, including methods using known dither records or adaptive thresholds.

The reference-squared sample sum is separately recorded. It can be converted
to joules only with a physical waveform, impedance, summing architecture and
duration. The full service time also includes ADC, reference switching and
digital computation. No advantage is asserted before those costs are known.

If the reference apparatus injects a known cumulative energy J back into the
specimen, H in (4) must become 2E+4N eta^2+2J. A powered reference or detector
bath is not exempt from this accounting. A large enough continuing injection
can make beta>=1/2 and invalidate the progress condition. Downstream placement
is not itself evidence that backaction, loading and noise are negligible.

## 6. A calibration floor with actual indistinguishable passive instances

The reference accuracy requirement is not merely a proof artifact for a
centered-only receiver with unknown input-coherent reference leakage.

Let two memoryless reciprocal passive one-port specimens have gains a=-rho
and a=+rho. Their outputs are y=a*u. Each dissipates (1-rho^2)u^2, so both have
E_0=0 and satisfy (1) for all time. Suppose the actual analog reference in
these two worlds is respectively (c-rho)u and (c+rho)u. Both calibration errors
obey the same advertised bound rho. The centered signal is exactly -c*u in
both worlds for every possible input and candidate, including adaptive ones.

Thus their complete centered ADC records, warnings and known random numbers
coincide for all time. Even a full-precision centered readout cannot distinguish
the physical gains. Their task optima are

\[
 u^*_\pm=\pm\frac{|b|\rho}{\rho^2+\lambda}.                        \tag{18}
\]

A deterministic worst-case command radius cannot be smaller than the positive
quantity in (18); the same 1-2delta certificate argument as in the first-return
twins applies. For rho=.02, b=.4 and lambda=.5, the radius is .01598721023.
The code replays 256 adaptive windows, while the algebra proves the all-time
statement. These specimens need no hidden memory or initial stored energy.

The scope is essential: a separately calibrated reference-bypass channel or a
measurement of the leakage is an additional observation that breaks this
equivalence. The floor is not asserted for a controller granted that extra
channel. It shows why an unknown coherent feedthrough cannot be silently
called independent measurement noise.

Likewise analog centering does not defeat the first-return finite-service
masking theorem. If the reference magnitude is bounded by V, prepare that
lossless delay-line construction with h>R+V+a_0U. Both centered outputs still
saturate for every allowed command throughout the paid horizon. The new
operation supplies neither an unbounded dynamic range nor an uncharged erasure.

## 7. Executed results and the ordinary alternatives

The standalone local command is `python3 -B centered_adc_experiment.py`.
It reads the first-return simulator and writes CENTERED_RESULTS.json in this
directory. No external files, services or equipment are used. The analytic
proof applies to arbitrary old fields satisfying the stated contracts; the
simulated specimens are the first-return reciprocal lossless delay-line
realizations, with an additional unchanged dark energy of 9.

The main experiments retain the four first-return gain/delay choices. Declared
E_0=64, R=1, eta=.075, b=.4, lambda=.5. The ADC has **two** output levels.
Each task requests a gain radius .0625 with failure probability .01. Four
blocks, selected using public budgets and intervals, use 987286 physical
windows and the same number of scalar ADC reads. Specimen incident energy is
5553.48375 normalized units. There are no resets or zero-input waits.

The reference error budget is rho=.001953125. Half is reserved for unknown
calibration error, so the nominal reference uses full span .15, step
.000146484375, and 1025 levels including endpoints. The required range including
the complete error allowance is .15029296875. These reference levels are an
additional resource to the two-level ADC. The execution includes both that
finite grid and an unknown coherent calibration leakage of magnitude rho/4.
The controller receives the digital DAC code and the total error bound; the
actual analog output and its leakage are audit-only quantities. The confidence
envelope is conservative and does not claim to use the known code optimally.

| Gain (audit only) | Delay | Certified gain interval | Certified task radius | Actual task error (audit only) | Saturated reads retained | Reference squared sample sum |
| ---: | ---: | :--- | ---: | ---: | ---: | ---: |
| .01 | 1 | [-.0776889,.0473111] | .04954502 | .01986320 | 1 | 6.504152 |
| .3 | 1 | [.2421743,.3671743] | .02897871 | .00101095 | 2 | 356.027384 |
| -.6 | 127 | [-.6843208,-.5593208] | .00372411 | .00010282 | 6 | 1952.006753 |
| .95 | 32768 | [.875,1] | .00493827 | .00066020 | 0 | 3855.682430 |

Every stage made its warranted half-width progress, and all four gain and task
intervals covered in their simulated runs. The long-delay specimen still has
stored energy 185.872633 after learning, including its unchanged dark energy.
Thus the result does not depend on clearing the specimen. These are individual
99 percent mathematical guarantees under the contracts, not a joint 99 percent
empirical assertion for four runs. Numerical energy residuals and the exact
per-block confidence constants are retained in the results file. One hundred
thousand additional random interval-geometry checks verified containment and
half-width progress as numerical diagnostics, not as a replacement for proof.

The following budgets are calculated from the two analytic certificates at
the same per-task failure level and E_0. The fixed-ADC column optimizes the
first-return dense ordinary signed-regression bound over a 20000-point public
amplitude grid. The centered column uses eta=.075 and charges the reference
accuracy rho=epsilon/32. Entries other than the main centered .0625 tasks are
**computed budgets**, not additional simulated learning trajectories.

| ADC levels | Gain radius | Fixed ADC: windows/reads | Fixed ADC: incident energy | Centered: windows/reads | Centered: incident energy | Added reference levels |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2 | .125 | 187730 | 1480.447 | 236155 | 1328.372 | 513 |
| 2 | .0625 | 1377969 | 5908.787 | 987286 | 5553.484 | 1025 |
| 2 | .03125 | 10463334 | 23762.301 | 4071927 | 22904.589 | 2049 |
| 2 | .015625 | 80906979 | 95671.626 | 16690895 | 93886.284 | 4097 |
| 257 | .0625 | 30208 | 60.290 | 41905 | 235.716 | 1025 |
| 257 | .015625 | 317656 | 123.610 | 480448 | 2702.520 | 4097 |

At the two finer two-level settings, centering reduces the sufficient window
budget by about 2.57 and 4.85 times while requiring the calibrated reference.
This is a comparison of sufficient certificates, not a speedup theorem against
the best fixed-ADC method. At the displayed 257-level settings the earlier
ordinary certificate is better in both window and specimen-energy costs. The
new architecture therefore does not establish an improvement for the inherited
257-level execution or a universal benefit from replacing its ADC.

An ordinary sparse method also changes the resource comparison. From the
first-return sparse bound, charge both binomial count tails with total
failure delta/2, and the two martingale tails with delta/2. If
z=x=log(4/delta), use count interval

\[
 M_- =\lfloor Np-\sqrt{2Np z}-2z/3\rfloor,\quad
 M_+ =\min(N,\lceil Np+\sqrt{2Np z}+2z/3\rceil).                    \tag{19}
\]

With K=2E_0+4M_+U_s^2, substitute M_- in the denominators of the first-return
sparse beta and nu, and M_+ in K. Their sum is a valid uniform gain-radius
bound on the joint event. The code searches a public grid for low expected
reads, using the original two-level ADC and no analog reference. For gain
radius .0625 and failure .01 it obtains:

| Calendar/physical windows | Expected ADC reads | Expected incident energy | Probe amplitude | Bound on gain radius |
| ---: | ---: | ---: | ---: | ---: |
| 2000000 | 259436.5 | 5876.696 | .1505051 | .0624691 |
| 4000000 | 41662.6 | 5094.829 | .3496970 | .0624855 |
| 8000000 | 19348.4 | 4720.558 | .4939394 | .0623530 |

Those are analytic resource plans with expected reads/energy and explicit
high-probability count intervals, not executed trajectories or exact bills.
They show why fewer dense windows cannot be promoted into a complete apparatus
advantage: ordinary idling can save most readout operations, and the detector,
waiting, specimen and reference costs have not been priced. No global
optimality of either grid is asserted. An ordinary method supplied the new
centering operation can also copy or improve the centered estimator exactly.

## 8. What remains unresolved

The reusable mathematical observation is that synchronous reference centering
makes clipping attenuate the **estimation error**. At the exact root, its
conditional bias vanishes even with arbitrary predictable old fields.
Passivity supplies a paid lower bound on accumulated sensitivity. This is
stronger than assuming a visually quiet field or ignoring saturated samples.

The physical obligation is still to supply a stable, accurately calibrated
reference/summing operation with bounded backaction, detector mean error,
complete energy and service-time costs, and warranted initial energy. The
calibration twins establish a real obstruction if coherent leakage is left
unknown. The original saturation twins still apply with the enlarged bounded
reference range.

The information-theoretic obligation remains a sharp lower/upper comparison
for the original fixed-ADC oracle, including all retained dithers, adaptive
threshold operations actually supplied, and ordinary set-membership methods.
The epsilon^{-2} result is proved for the enlarged centered oracle. Neither
its priority nor a separation from the strongest equally informed ordinary
approach has been established. No hardware capability or practical advantage
is claimed.
