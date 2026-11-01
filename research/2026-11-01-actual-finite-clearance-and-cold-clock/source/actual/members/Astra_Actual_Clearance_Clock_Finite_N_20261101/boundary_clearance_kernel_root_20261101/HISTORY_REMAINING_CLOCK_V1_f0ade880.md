# A bounded-sensitivity remaining-clock observable

Status: deterministic construction and candidate stochastic consumer. No finite-N stochastic clock or CLT is proved here. This uses the autonomous mesoscopic vector field, not a value function supplied for the actual count chain.

For l,e>=0, consider

 dl/ds=1+3l²e, de/ds=2l².

Let b(l,e) be its remaining time to blow-up. Cooperative comparison with the origin solution gives 0<b(l,e)<=s_*<=2 for finite initial values. The invariant-with-clock identity is d(l-3e²/4)/ds=1. For l>0, introduce v as the increasing e-coordinate, w0=l-3e²/4, and solve

 du/dv=1/[2(u+3v²/4)²], u(e)=w0.

Then b(l,e)=u(infinity)-w0. Along this inverse flow L(v)=u(v)+3v²/4 is positive and increasing; u remains bounded while the right side has an integrable v^-4 tail. Thus this is an actual scalar acquisition route for b, with startup and quadrature still to be validated computationally. It is not a hidden stochastic hitting-time oracle.

The inverse vector field has partial derivative -L(v)^-3 in u. Hence its flow sensitivity is

 J(v)=exp[-integral_e^v L(z)^-3 dz], J_infinity in(0,1).

Differentiating the actual inverse flow yields

 b_l=J_infinity-1, so -1<b_l<0,
 b_e=(3e/2)(1-J_infinity)-J_infinity/(2l²).

The moving lower endpoint contributes the second term in b_e; it cannot be dropped. These derivatives satisfy the exact transport identity

 (1+3l²e)b_l+2l²b_e=-1.

The bound |b_l|<=1 extends to l=0 by continuity and comparison; singular inverse formulas at l=0 should be evaluated by a separately verified forward startup, not literal division by zero. Higher derivatives and their usable suprema are still acquisition costs.

## Candidate actual-clock observable

For the actual rate2 count model, T=N^(1/5), l=[A+(C+D)/2]/T and e=E/T³. The candidate corrected remaining clock is

 b(l,e)+AE/(N T) b_l(l,e).

The full generator's AE identity can cancel the unresolved AE b_l/T term. If the full residual, jumps and bracket are charged, physical time/T plus this observable becomes an approximate martingale. This is the operation needed for a timing window; approximating every microscopic trajectory is unnecessary. The exact corrector derivation is a separate ongoing component, and all actual channels, imbalance, source preparation and exit events must be included.

## Deterministic candidate variance functional (not an actual-chain CLT)

If a justified diffusion limit had noise only in l with instantaneous variance 1+3l²e, its clock variance would be

 Sigma²=integral_0^{s_*} b_l(l(s),e(s))² [1+3l(s)²e(s)] ds
        =integral b_l² dl.

This integral is finite for a deterministic, explicit reason. On the orbit from(0,0), l=s+3e²/4. For e>0, the inverse sensitivity bound gives

 |b_l|<=1-J_infinity<=64/(135 e^5).

For e>=E>=1,

 dl/de=1/(2l²)+3e/2 <=8/(9e^4)+3e/2.

Consequently the remaining variance integral is at most

 (4096/18225)[(8/117)E^-13+(3/16)E^-8].

This is only a validated target for future scalar computation. The actual diffusion/CLT, its noise covariance, singular-boundary continuation, and finite-N error have not been earned. In particular the deterministic s_* clock cannot be advertised as a finite-N CDF solver: a continuous hitting law and a point mass have Kolmogorov distance at least1/2. A high-probability timing window and a distributional kernel are distinct deliverables.
