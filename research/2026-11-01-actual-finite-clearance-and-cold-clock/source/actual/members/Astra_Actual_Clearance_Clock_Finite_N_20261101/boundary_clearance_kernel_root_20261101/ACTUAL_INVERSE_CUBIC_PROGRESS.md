# Actual inverse-cubic progress inside a moderate admitted cone

Status: root full-generator component, pending independent review. It receives neither the cone nor the final population-clearance state.

Use the exact rate2 count model, fixed reference N>0, L=A+(C+D)/2, Z=C-D, and R=E²/(NL). Define U=E-A/2. Admit pre-stop states satisfying

 B>=100, E/B<=1/5, L/B<=1/10,
 A<=L/10, |Z|<=L/10, CD>=4, U>=100, R<=2.

All inequalities concern the actual current state, not a supplied conditional equilibrium. One-step successor values remain in every generator calculation.

## Exact drift and noise

The literal twelve-channel generator gives

 GU=(5/2)A²-2A-1/2+A[(B-C-D)/2-2E]+CD/2,
 q_U=1/4+A/4+(11/4)A(A-1)+A(C+D)/4+(5/2)AE+(3/4)CD+AB/4.

Every U jump has magnitude at most3/2. Since

 CD=(L-A)²-Z²/4 >=(323/400)L² >=(4/5)L²,

and E<=B/5, the A-source bracket is at least A(B/10-L). Also AL<=L²/10<=CD/8. Integer A gives (5/2)A²-2A>=0. Finally CD>=4 pays the remaining1/2. Therefore

 GU>=AB/10+CD/4.

For the bracket, A<=B/100, B>=100, C+D<=B/5 and E<=B/5 imply

 q_U<=(83/100)AB+(13/16)CD<=9GU.

Thus both progress and fluctuations are received from the same actual source groups. In particular both E-consuming AE channels have been included; E is not assumed monotone.

## An actual physical-time budget

For U>=100, Taylor's theorem on all actual jump segments gives

 G(U^-3)<=-3GU/U^4+6q_U/(U-3/2)^5
          <=GU/U^4[-3+54U^4/(U-3/2)^5]
          <=-2GU/U^4.

The last scalar inequality follows, for example, from
27*200^5<50*197^5 and U>=100. Since U<=E, CD>=4L²/5 and R<=2,

 G(U^-3)<=-CD/(2U^4)<=-(2/5)L²/E^4<=-1/(10N²).

Define the globally positive bounded extension

 Psi(x)=10N²/[max(U(x),50)]³.

At every admitted state and all one-step targets, U>=98.5, so the extension changes none of the preceding calculations. Consequently G Psi<=-1 throughout the admitted pre-stop domain.

Let tau_E be a declared macro-E target and sigma_adm the first other admission failure, including all required state/denominator/ratio gates. Stop at sigma=tau_E wedge sigma_adm. Nonexplosion and finite-horizon Poisson domination justify localized Dynkin; Psi is bounded and nonnegative. Thus

 E_x[sigma]<=Psi(x), P_x[sigma>d]<=Psi(x)/d.

If a separate construction supplies
P_x[sigma_adm<=min(tau_E,d)]<=delta_adm,
then

 P_x[tau_E>d]<=10N²/[U(x)^3 d]+delta_adm.

A simultaneous adverse gate exit is included as failure. This is not a claim that the target is reached without a received admission bound.

For T=N^(1/5), if the actual entrance has E=e0 T³ and U>=.99E, then

 E_x[sigma]<=11T/e0³.

Choosing d=epsilon T gives a stopped-duration contribution at most11/(epsilon e0³). This offers a concrete alternative to an enormous inherited amplification cutoff, but only if the moderate cone, A/imbalance caps, total-count margins and exit-state handoff are actually earned. For example U>=.99E follows from R>=1/2, E<=N/10 and A<=L/10; it is not implicit in the basic upper-R gate.

No physical state is reset, no reaction is deleted, no independent attempt count or Poisson fiber law is assumed, and no final removal-time/CDF algorithm is supplied by this component.
