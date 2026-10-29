# A payable unexecuted calibration bridge and its exact-flow scope

30 October2026. Consumes the original qualified MODEL: dot x=-iKx+e u
whenever g=0, K Hermitian(real symmetric in the common real modal basis),
known metric, coherent phase clock, known finite input history and a qualified
linear realization Khat,ehat in the SAME Euclidean coordinates. Warrant
||K-Khat||<=dK, ||e-ehat||<=de, ||e||=1. Existing numerical values of dK,de
are qualified against the known synthetic source only, not an instrument.
All g=0/off-state, waveform, clock and readout assumptions remain explicit.
The first zero before calibration is retained; this removes only the second.

## 1. Exact finite calibration history and command

Write U(t)=exp(-iKt). The calibration uses u=1 for p=1/5, then zero drive
and ringdown for W=32. At that END time its actual state is

 x_cal=integral_0^p U(W+s)e ds.

Its predictor xhat_cal uses Khat,ehat. In acquired diagonal modal coordinates,

 xhat_cal,j=ehat_j exp(-i lambda_hat,j W)
                  [1-exp(-i lambda_hat,j p)]/(i lambda_hat,j),

with the continuous p limit at lambda0. This uses the input HISTORY, not a
hidden-state observation. Duhamel and unitarity give

 delta_cal=||x_cal-xhat_cal||
 <=p de+(pW+p^2/2)dK =de/5+(321/50)dK.                (B1)

The existing32 drive bins have width h=1/2 and total P=16. Let
B_l=integral_(bin_l) U(P-s)e ds and similarly Bhat. Then

 dB=||B-Bhat|| <=sqrt(32)h(de+P dK).                  (B2)

The stored floating pseudoinverse is merely a proposed finite matrix PB.
Outward arithmetic verifies ||Bhat PB-I||_F=rB<1, so
sigma_min(Bhat)>=(1-rB)/||PB||_F. The acquired lower bound is>.142057.
The proposed command is -PB Uhat(P)xhat_cal, rounded ONCE to48 fractional
bits per real/imaginary component. COMMAND.json supplies all32 exact complex
dyadics. No infinite precision command or impulse is granted.

For this ACTUAL finite coefficient vector v, certify

 eta_cmd=||Uhat(P)xhat_cal+Bhat v||,
 ||r0||=||U(P)x_cal+Bv||
 <=delta_cal+P dK||xhat_cal||+dB||v||+eta_cmd.          (B3)

The last line follows by adding/subtracting U(P)xhat_cal and the nominal
finite command response. No unknown error norm is absorbed. Outward Arb
uses the analytic finite rectangular-pulse integrals, not a flow solver.
It gives eta_cmd<1.990e-15 and the general residual<2.176e-11. Direct
evaluation on the known rational synthetic spectrum gives<1.021e-12;
that tighter number is also an ANALYTIC MODEL prediction, not a measured
reset. The command depends only on the acquired hats and known history.
The hidden true spectrum is used only to qualify the synthetic error bounds.

The extra cost is16 time units,32 finite complex constant-drive coefficients,
peak<.056901 and h sum_l|v_l|^2<.013647, with NO additional scalar readouts.
Ordinary comparators may use the same bridge. Physical gain/off-state/phase
and DAC errors would add their warranted state-error budget; none is measured
here. An initial state before calibration of norm e_init would add e_init
to(B1); the prototype does not acquire that stronger bootstrap contract.

## 2. Compile later resets rather than accumulate140 Gronwall factors

Use R=31/2 for the science readout interval and S=P+R. Let C be its actual
32-by-n linear readout matrix, PC a proposed finite left inverse of Chat.
Outward arithmetic verifies rC=||PC Chat-I||_F<1 and readout sigma_min>.291371.
The same unitary comparison gives

 dC<=sqrt(sum_l(de+t_l dK)^2),
 bB=rB+dB||PB||_F, bC=rC+dC||PC||_F.

The ideal linear feedback waveform is F=-PB Uhat(S) PC, acting on the RAW
post-pulse readout vector. Round this32-by32 complex matrix once to48
fractional bits, obtaining F48. COMMAND.json supplies the finite coefficients.
Their outward operator error is bounded by their Frobenius error dF.
Future finite raw detector numbers can be multiplied using exact dyadic
arithmetic, with the FINAL drive vector rounded to48 fractional bits. The
post-reset state error of that final rounding is at most

 a_R=sqrt(32)h *sqrt(64)2^(-49)<4.020e-14.             (B4)

The same bound a_P is available for rounding a finite preparation command.
This is a specified finite-command model resource; a physical DAC/noise
qualification is not supplied by the arithmetic certificate.

If z is the state just AFTER a science pulse, the actual state after its
readout and reset is

 r_next=A_R z+B F48 eta+epsilon_R,
 A_R=U(S)+B F48 C,
 ||epsilon_R||<=a_R.                                  (B5)

Factoring B PB=I+E_B and PC C=I+E_C gives

 alpha=||A_R||
 <=S dK+bB+bC+bB bC+sqrt(32)h sqrt(32)dF,
 gamma=||B F48|| <=(1+bB)||PC||_F+sqrt(32)h dF.         (B6)

The cross term bB bC is retained. The actual receipt gives
alpha<6.747e-10, gamma<3.433. No opaque norm of a floating inverse or assumed
perfect cancellation is used. In particular the reset suppresses the next
cycle's state dependence; a product of140 unconstrained pulse-growth bounds
would be the wrong composition operation.

## 3. Explicit target/norm/noise contract

Require supplied desired linear-preparation vectors of norm<=1.500001,
at most32 readout values per block, each complex additive error<=1e-9,
48bit output rounding as above, science g=7/20 and duration<=13/10.
The actual new flow must satisfy the declared norm-preserving Kerr model;
unmodelled loss/process noise/actuator drift needs a separate budget.

Given reset norm r, the next prepared/pulse initial norm is at most
r+(1+bB)1.500001+a_P. Exact Kerr pulses conserve that norm. Therefore

 r_bar=max{r0,[alpha((1+bB)1.500001+a_P)
                 +gamma sqrt(32)1e-9+a_R]/(1-alpha)}

is invariant. The receipt gives r_bar<2.043e-8 and all exact science-pulse
norms<1.500002<8/5. The8/5 cap is thus an explicit derived CONTRACT of this
qualified model/input, not a claim about arbitrary stored solver outputs.

On that ball an exact Kerr flow has difference Lipschitz bound

 L=exp[3|g|(8/5)^2(13/10)]<32.931.

For two EXACT-flow protocols using the SAME compiled controller, same target
commands and the same additive readout-noise word, their reset differences
satisfy

 d_(i+1)<=q d_i+2a_R, q=alpha L<2.222e-8.              (B7)

One may share the exact final rounding perturbation too, removing2a_R;
the receipt conservatively keeps it. For DIFFERENT bounded noise words,

 d_(i+1)<=q d_i+b,
 b=2gamma sqrt(32)1e-9+2a_R,
 d_i<=q^i d_0+b(1-q^i)/(1-q).                         (B8)

The reported3.883e-8 floor is b/(1-q), NOT a replacement for the transient
q^i d0. This pays time/state/error correlations and the complete finite
science sequence without granting a reset after each shot for free.
For reconstructed endpoints of those exact protocols, the initial/readout
matrices also give

 dX_i<=(1+bC)d_i+||PC|| ||Delta eta_pre,i||,
 dY_i<=(1+bC)L d_i+||PC|| ||Delta eta_post,i||.

Common additive words remove the noise differences; different bounded words
use2sqrt(32)1e-9 for each. These are exact-protocol DATA bounds, not bounds
on an unvalidated ODE solver's endpoints.

## 4. What this does NOT transfer from the old executed data

The old run used TWO separately zero-initialized calibration/science segments.
Its science ODE and floating controller arithmetic were not validated.
Its small stored ENERGY defect cannot bound trajectory error: constant-energy
surfaces contain different states/phases, and even different times on a true
trajectory can share energy. Equations(B7)--(B8) compare exact flows and do
NOT certify a distance to those unvalidated stored endpoints.

Consequently we do NOT infer the proper unexecuted protocol's actual design
rank, tensor/K error, ordinary-fit score or measured execution cost from the
old array receipt. A future proper run must consume its OWN measured design
conditioning/error warrants. Alternatively an independently validated bound
from old arrays to the exact zero-reference protocol, including nonlinear
flow AND linear-controller arithmetic, would permit the following transfer.
That additional bound is currently UNKNOWN and was not acquired by a rerun.

For clarity, let dXi,dYi bound total reconstructed-endpoint changes between
old data and a prospective proper exact protocol, including any such old
numerical error. On a warranted endpoint ball of radius Rdata, set
E=sqrt(sum_i(dXi+dYi)^2). Feature telescoping gives

 ||Delta A||<=4Rdata^3 E,
 ||Delta b||<=4||Khat||Rdata E/|g|.                   (B9)

Thus old design sigma lower s0 transfers only if4Rdata^3 E<s0; its source
tensor residual then gains sqrt(n)||Delta A||+||Delta b||. This is a
conditional algebraic receiver, not an acquired proper-rank certificate.
The old s0=.0255975 remains a valid certificate of the OLD finite arrays.
It does not pay the missing E. The global two-radius analytic-family theorem
and exact finite-pulse energy identity remain unchanged, at their existing
model/access scope.

## 5. Scope and evidence

construct_bridge.py performs no ODE/source/science/fit run. It reads stored
linear coefficients, constructs finite dyadics and proves outward linear/
scalar bounds at192bits. COMMAND.json is UNEXECUTED. CERTIFICATE.json labels
source-specific analytic predictions and unchanged original hashes. The
prospective protocol time is9010.9045 rather than8994.9045; extra control
power is additive. Original benchmark times/scores remain separate-segment
diagnostics. No empirical/physical, whole-ODE, new finite-noise performance,
novelty or advantage claim is added. The first bootstrap zero and native
global-control/readout qualification remain explicit resources.
