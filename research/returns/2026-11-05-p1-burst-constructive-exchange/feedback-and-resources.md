# Exact affine intervention without learning the hidden force

This companion answers the primary P2 challenge within its calibrated affine constant-force Langevin family. The [full proof](package/p2_bypass.md) and [final smooth-meter completion](package/p2_c1_meter_completion.md) govern; the latter supersedes older rectangular and piecewise-linear switching fixtures. It does not settle the [universal intervention-stream resource law](../2026-11-05-p2-intervention-stream-opening/README.md).

## Exact cancellation and useful arms

The plant is

\[
dx=(p/M)dt,\quad
dp=(-kx+F-\gamma p+u)dt+\sqrt{2\gamma\sigma^2}\,dW,
\quad \sigma^2=M/\beta,
\]

with unknown constant `F` and `k=M lambda_s(gamma-lambda_s)`, `0<lambda_s<=gamma/2`. Position sensing and an additive force actuator are explicit access premises. No force identification, pinning or spring-stiffness control is assumed.

A finite linear instrument gives `O=GU+nu`; the prospective endpoint is `HU+(N_x,N_p)`. Here `U` includes the old state and frozen hidden variables with arbitrary correlations to the old reference. Fresh instrument/bath noises are jointly Gaussian and independent of that whole old system. Select `G^T w=h_p^T`, the momentum endpoint row. Then

\[
p_T^0-w^TO=N_p-w^T\nu=:Z_p
\]

has zero gain from every old variable, including the hidden force. This removes dependence without identifying which hidden sector was present.

Let `V=Var(Z_p)` and `r=sigma^2-V`. Suitable position feedback decorrelates the final position noise from `Z_p`; a second constraint eliminates initial-position gain from the feedback displacement. For a fresh fair arm `A=+-1`, use independent dither

\[
f_A(d)=G_r(d)[1+A a\sin(\sigma d/r)],\qquad
a=\eta e^{V/(2r)},\quad \eta=1/2.
\]

When `a<=1`, Gaussian convolution produces exactly the original useful arms

\[
q_A(p)=G_{\sigma^2}(p)[1+A\eta\sin(p/\sigma)],
\]

and the complete joint endpoint is

\[
\mathcal L(A,p_T,x_T,Z,R_{old})
=\tfrac12q_A(p_T)\mathcal L(x_T,Z,R_{old}).
\]

The hidden marginal is the **contemporary prepared marginal**, which preparation may change. Fine meter records and dither seeds must be isolated, disposed of or reset before reuse; retaining them as extra references would generally invalidate this factorization. Arbitrary non-Gaussian old laws are covered; second moments enter expected control-cost bounds.

## Final finite instrument and supplied certificate

Eight canonical pointers have normalized mass 100, `Var Q=10^-6`, `Var P=10^-2` and coupling `g(t)xP`. Pointer drift and force backaction on the source are included. Coupling has `C^1` cubic smoothstep edges, peak one and normalized slew at most 96. Two finite smooth force pulses implement the displacement.

The final [100-piece directed interval certificate](package/p2_c1_direct_sine_arm_interval.json) covers the continuum `0<=k/(M gamma^2)<=1/4`, with

\[
V/\sigma^2\le0.542831311,\qquad a\le0.905327083<1.
\]

The feedback-constraint determinant is bounded away from zero. This is supplied interval evidence, not extrapolation from a numerical grid. An [independent full-state calculation](package/p2_smooth_meter_validation.json) checks the smooth-meter representation. The nominal meter-plus-force schedule is `1.1/gamma`; the separate Gaussian replacement fixture is `1.2/gamma`.

Useful bare harmonic response occurs on the fast scale `1/gamma`, while hidden-sign distinguishability tends to zero on that scale as `lambda_s -> 0`. Waiting `1/lambda_s` would dominate the useful response. Thus an inference-time lower bound cannot serve as a universal intervention-time lower bound against this route. The previous thermal waiting and marking certificates remain correct for the operations they analyze.

## Complete bill and limits

The nominal duration assumes observations reach the controller before the force window. Actual ADC/computation latency, extra readout noise and a causally shortened force window need their own acquired parameters and certificate. Eight fresh cold pointers, reset/disposal, randomness, range, actuator limits, response sensing and repeated trials all count. A thermal pointer realization uses temperature `10^-4` of the source temperature; quantum uncertainty and a safe classical regime constrain that choice. Source-position width grows as `lambda_s^(-1/2)`, so the construction does not have fixed range as the soft mode vanishes.

Point fixtures at `D_0=1` have normalized expected squared-force integral about 13,324–23,324. These are control-action figures, not mechanical work or a uniform optimality certificate. The interval candidate controller is distinct from those point predictors. Calibration error has a moment-dependent campaign cost; under appropriate nondegenerate margins, coefficient tolerance can scale as `epsilon/sqrt(n)`. No calibration experiment establishes that accuracy or acquisition time here.

The source credits ordinary Gaussian output-feedback covariance steering. Its supplied bridge is arbitrary-reference/unknown-force cancellation, finite canonical sensing with backaction and the non-Gaussian arm endpoint. There were zero hardware trials. This is a completed calibrated affine construction, not the original universal nonlinear campaign interface or a sharp total-resource optimum.

All supplied [code and receipts](package/README.txt) are preserved without execution by Capital.
