# Separate source-current bounds and an acquired single exponential reference

Status: root corollary, source-bound independent review pending. This does not
modify either frozen MFPT engine or their accepted output task.

Use the explicit nonharmonic-trial theorem in
TRIAL_RESOLVENT_TO_SURVIVAL_ROOT_V2.md (SHA7d4d7f61...). Retain its actual killed
self-adjoint positive semigroup, finite measure, exact Gibbs-type A initialization,
trial h, M=m(A), S0=m(S), rho=S0/M, and energy upper C0. Replace the coupled
source hypothesis by SEPARATELY received bounds

  <1_A,K^(-1)1_A><=B_A,  <1_S,K^(-1)1_S><=B_S.

Then the same all-time survival conclusion holds with

  epsilon=C0(sqrt(B_A)+sqrt(B_S))^2/M^2-1,
  k0=C0/M,  d_init=rho+sqrt(rho(1+rho)).

Indeed positivity and inverse-form Cauchy--Schwarz give
<h,K^(-1)h><=(sqrt(B_A)+sqrt(B_S))^2; every remaining line of the spectral
and initial-law proof is unchanged. Valid premises imply epsilon>=0.

This matters when an improved A-current does not improve the S-current.
If B_S<=rho^2 B_old and B_A=B_new, one may use

  epsilon=C0(sqrt(B_new)+rho sqrt(B_old))^2/M^2-1.

It is INVALID to silently replace B_old by B_new in the S bound. For fiber
models with C0=1/(beta R), normalized b_new=B_new/(beta M^2 R) and
b_old=B_old/(beta M^2 R) give the equivalent expression
(sqrt(b_new)+rho sqrt(b_old))^2-1. Every root/rational operation in an actual
consumer requires outward receiving under the same total work budget.

Finally suppose exact arithmetic supplies 0<k_lo<=k0<=k_hi, and let
k_star=(k_lo+k_hi)/2. For every t>=0, the mean-value theorem and
sup_{t>=0} t exp(-a t)=1/(e a) give

 |exp(-k_star t)-exp(-k0 t)|
   <=(k_hi-k_lo)/(2e k_lo)
   <=(3/16)(k_hi/k_lo-1),

using e>8/3. Thus a SINGLE acquired Exp(k_star) reference has uniform absolute
CDF/survival error at most

 epsilon_upper + rho_upper + sqrt_up[rho_upper(1+rho_upper)]
       +(3/16)(k_hi/k_lo-1).

This is not relative extreme-tail accuracy, an exponential-moment bound, an
arbitrary-initial-state guarantee, or a physical preparation/calibration service.
The requested KS tolerance, rate interval, source bounds and arithmetic costs
must all be bound to the literal actual task by an independently checked receiver.
