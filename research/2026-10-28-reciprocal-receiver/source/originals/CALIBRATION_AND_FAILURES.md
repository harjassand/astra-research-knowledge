# Physical construction, calibration and important failures

28 October 2026. No equipment was operated, purchased or contacted.

## Reciprocal one-feed collection

For a reflectionless reciprocal mesh, the forward/reverse matrices are U,U^T.
Its full scattering [[0,U^T],[U,0]] is symmetric and unitary for unitary U.
Drive feed e1, prepare u=Ue1 and match all unused feed ports. The returning
field T(z)u reaches the same feed as u^T T(z)u. A calibrated directional
separator and a passive 50:50 reference combiner feed one power detector.
Other return modes are dumped, not falsely counted as measured total power.
The separator must not introduce an unmodelled loop; insertion loss, leakage,
detector gain and incident normalization are calibrated or bounded.

There is a stronger per-configuration observation: **any fixed passive
reciprocal front end** with one source/return feed, one tagged target and all
other ports matched reduces to a reciprocal two-port plus loss. Its scalar
return is beta+z a/(1-s_eff z), with a=h^2, where |h|^2 is the actual matched
target power per upstream feed power. Thus front-end reciprocal insertion
loss/reflections do not require knowing microscopic parameters for this
per-configuration metrology. However, changing unknown reflections with the
command can change the effective source: the O(n) fixed-Gram control theorem
still requires a calibrated fixed linear mode map or a justified perturbation
bound. It cannot treat arbitrary programmable cavities as a fixed input basis.

## Three physically simple target states

At real reference impedance Z0, z=(Z-Z0)/(Z+Z0). The target states
0,+1/2,-1/2 correspond to positive resistances Z0,3Z0,Z0/3. A switch among
these terminations is an explicit passive narrowband tag. Phase stepping is
performed locally at the receiver, not at the hidden load. Calibration of the
assembled switch/leads/terminations at the target reference plane is required
before embedding or through an available calibration connection. One-port
calibration and public implementations such as scikit-rf provide an established
route; this continuation did not execute a hardware calibration.

Component labels or DC tolerances alone do not characterize RF parasitics.
Retain actual complex load intervals, drift and switching time. For a real
resistance perturbation dR, exact subtraction gives

    |z(R+dR)-z(R)|=2 Z0 |dR|/(|R+Z0||R+dR+Z0|).

For actual and nominal |z|<=rmax<1, passivity of the original source gives

    ||T(z)-T(z_nom)||<=|z-z_nom|/(1-rmax^2).

This bounds the matched receiver amplitude error for unit input, including an
imperfect nominal matched state. Non-port changes caused by tag actuation
need their own error/model bound. Calibration access is therefore constructed
as a finite pre-embedding operation, and its residual uncertainty is charged;
it is not silently declared to exist on an uninstrumented hidden target.

## A passive reference receiver and finite local calibration

A 50:50 combiner with reference amplitude R>0 produces

    I_theta=|h+R exp(i theta)|^2/2,
    theta in {0,pi/2,pi,3pi/2}.

The second output is terminated. Normalize powers to a signal feed unit;
the reference adds R^2 units of optical/RF power. The exact reconstruction is

    h_hat=[(I_hat_0-I_hat_pi)+i(I_hat_pi/2-I_hat_3pi/2)]/(2R).

Four simultaneous calibrated errors <=eta give complex error <=sqrt(2)eta/R.
An unknown common reference phase throughout the twelve-reading block is
irrelevant to p=|a|. Unknown phase changes between loads are harmful.

A finite local calibration uses a traceable local power standard for detector
gain/dark offset; reference-only readings; and known test fields in two
independent quadratures at the signal input. No hidden target measurement is
involved. Under the physical fixed-linear-optics/square-law-detector model,
retain an interval for the real response d=B x+b, where x=(Re h,Im h) and
d is the pair of opposite-phase power differences. If

    ||B-B0||<=eB, ||b-b0||<=eb, sigma_min(B0)>=s0>0,

then x_hat=B0^{-1}(d_hat-b0) obeys

    ||x_hat-x|| <= (e_d+eb+eB)/s0

because |h|<=1. The matrix inverse/norm certificate, test-field uncertainties,
reference amplitude/phase errors and drift must be retained. Finite calibration
fits do not prove stationarity or the physical detector law. Unequal signal
coefficients or residual nonlinear detector response must be bounded separately.

With ideal relative phase spacing, estimated Rhat and |Rhat-R|<=eR<Rhat,
the simple formula instead has field error <=sqrt(2)eta/Rhat+eR/Rhat.
A phase-step chord deviation ephi changes I by at most R ephi for |h|<=1.
Unknown load/reference gain supplies a calibration floor that more photons
cannot remove. Absolute source-to-target phase is unnecessary. These are
conservative separate-error charges; SHARED_CALIBRATION.md gives a stronger
relative bound for calibration shared across the three target states.

## Exact failures that prevent free calibration

**Uncalibrated remote-load scale.** For c>0 preserving passivity,

    t'=c t, s'=c^2 s, z'_j=z_j/c^2, S0'=S0

preserves every complex accessible response for every input, but p'=c^2 p.
A rational witness is S1=[[0,1/4],[1/4,0]] with loads z_j and
S2=[[0,1/2],[1/2,0]] with loads z_j/4. Both are symmetric contractions and
return z_j/16, while matched target powers are 1/16 and 1/4. This proves an
all-command ambiguity, not merely a finite-data failure. A known matched state
alone does not remove it.

**Nonreciprocal coupling.** The original forward/return scaling gauge remains:
scaling t_out by c and t_in by 1/c preserves every accessible field while
changing delivered power. The new receiver needs reciprocity in compatible
power-normalized ports; fitting reciprocal data is not a proof of it.

**Fixed partial aperture.** A target may couple entirely to an uncollected
controlled mode. The same-feed construction removes this by using the actual
reciprocal return of the prepared mode. A random fixed receiver does not.

**Unknown dynamics.** Quiet accessible power does not prove that hidden energy
has decayed. The original finite-memory/independently bounded-tail assumption
is retained. A stationary scattering matrix supplies no generic settling time.

## Time and photons

Each oracle uses three target states and four local phases each, twelve powers.
For Q scalar queries this is 12Q detector integrations and 3Q target-setting
blocks if local phases are grouped. Include all actual reset and switch events.
For the original finite-memory realization with maximum |z|=1/2, after j
certified flush blocks from reset the signal RMS error is <=d_j=2^(1-j)
over a following complete T block or an integer number of such blocks.
T includes added path and load delays. Take each detector integration window W
to be an integer multiple of T. For a shorter arbitrary window replace d_j
by sqrt(T/W)d_j: stored energy can emerge in a short pulse.
Reference interference changes the detector transient bound to

    |I_transient-I_stationary| <= (1+R)d_j+d_j^2/2.

Choose j against this bound, charge jT signal illumination per new load, four
integration windows and local phase settling, and a T matched reset whenever
the schedule uses a reset. Local reference illumination during these waits is
also charged if it is left on. More efficient schedules need separate proofs.

For stationary independent coherent-state Poisson readout, mean intensity is
<=M=(1+R)^2/2 per signal photon unit. A conservative sufficient exposure for
K pre-budgeted readings and simultaneous raw error eta with failure <=beta is

    N >= [2M/eta^2+2/(3eta)] log(2K/beta).

This is the Poisson Bernstein/union bound, not an optimal statistical rate or
lower bound. Reference photons add R^2 N per equal-duration reading. Include
transient mean allowance in M when needed. Larger R also increases M, reference
energy and detector dynamic range; it is not a free infinite-gain resource.
For the original dark source, direct return counting and reference detection
can both need order p^(-2) photons for fixed relative p precision. The new
linear bounded-absolute-error modulus does not prove universal photon advantage.

## Selected current Astra reuse

Read-only snapshot: b2adf267d6341d66a643102658fbadeb01518301. N997's actual
uncertain-history proof supports retaining justified enclosures and checking
numerical proposals; its full-vector query theorem is not imported. N996's
native vector/transpose actions are unavailable here. N1050's active-shunt
gauge proof is a useful analogy for shared instrument parameters and harmful
gain drift, not a wave-scattering theorem. N1061's same-loop reciprocal fixture
proof and hidden-motion counterexample reinforce operating-loop/timing scope,
not mechanical-loss laws for this wave source. Packet acceptance labels do not
confer acceptance on this continuation or an audit of the supplied P1 archive.
