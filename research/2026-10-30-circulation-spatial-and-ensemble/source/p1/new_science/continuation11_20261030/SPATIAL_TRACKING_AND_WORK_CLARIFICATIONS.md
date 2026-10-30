# Binding spatial tracking and work clarifications

30 October 2026. The actual physical-mechanism receiving review read
`JOINT_SPATIAL_TRACKING_AND_NONLINEAR_PROGRAM.md`, SHA256
`dd815be2bc16a734d377f8a141dc117383ff6c6357650a690e55f3d43a2d84ae`.
Its core stopped joint-volume proof was accepted; these scope clarifications
are binding. The separate original work note is preserved with this note.

## 1. Joint fresh noise, not fresh scalar marginals

Actual fresh thermal sources are independent across carriers, rows and
periods, conditional on the past. This also appears in the elastic-layer
correction. For the tracking estimate alone a uniformly bounded conditional
joint covariance operator would suffice for its Gaussian part, but the
product relative Gibbs argument uses the stronger actual product supplier.
One common fresh Gaussian in N identical rows has a covariance eigenvalue
of order N and leaves only a row-scale fluctuation exponent. It is an exact
failure of a scalar-marginal replacement.

## 2. Direct spatial interpolation and Fourier accuracy

The compact-set/exponential-tightness route in the original theorem is
valid. Its optional polynomial count-range sentence must not be read as
alone proving spatial sampling error after nonlinear composition. Instead,
for any fixed gamma in (1/2,1), the native conditional martingale bound gives

\[
 P\{\max_y\sup_{t\le T}|h_y(t)|>N^\gamma\}
 \le\operatorname{poly}(N)\exp[-cN^{1+2\gamma}].
\]

At this threshold the bounded-jump Bernstein denominator is dominated by
the row variance O(N^3) in physical counts, since gamma<1. The predictable
row drift contributes only O(1) after normalization. The exponent is
super-volume because gamma>1/2.

Off this event, smooth convolution and bounded derivatives of psi make the
vertical spatial sampling error O(N^(gamma-1)), which vanishes. The same
bound controls atom/step interpolation of the raw h term. A Fourier
truncation with O(log N) modes has error O(r^M N^gamma), meeting the evaluator
precision. Thus spatial sampling and evaluator accuracy are each paid and
proved, without changing the native current topology.

## 3. Work filtration and the separate observation-bias term

The complete actual force, including errors represented by eta, must be
constant over its declared held block and measurable with respect to the
record at the start of the **previous** block. Being selected before only
the upcoming block's sources is weaker and does not remove the preceding
block's innovation from the work correlation. An actuator with fresh
within-block force noise needs a separate work bound; it is not silently
included in the exact partial-refresh identity.

The bound O(N²+N K_N) for total mean carrier-force work includes O(N²) from
bounded target drift **and possibly observation bias**. The present
|eta|<=C/K_N allowance can cost O(N²) even unforced. O(N K_N) is the
contribution of the filtered current/thermal martingale term, not a general
noise-only operating-work promise. A sufficient smaller per-row normalized
observation scale for such a promise is O((N K_N)^(-1/2)), together with
vanishing target drift and the actual work filtration. No such improved
unforced promise is needed for the main theorem.

## 4. Which vorticity is programmed

For psi(y,t,z)=v(y)t the output's **row-mean horizontal** instantaneous
current is v(y). Its shear component has vorticity -v'(y). The full output
also retains the native horizontal zero-row-mean part and vertical current;
their vorticity is not overwritten by this architecture. All density-law
comparisons are at the same actual native load and initial law.
