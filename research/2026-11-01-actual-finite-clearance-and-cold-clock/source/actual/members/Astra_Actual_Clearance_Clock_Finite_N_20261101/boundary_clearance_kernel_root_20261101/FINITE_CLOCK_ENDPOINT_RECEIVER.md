# From an acquired clock budget to an actual clearance interval

Root conditional construction, awaiting independent review. This receives explicit error/bracket budgets; it does not assert they are already assembled or economically useful.

Use the actual corner, N=T^5>=10^20, original horizon4T, and admitted startup L=400 by time800 with A<=2,Z=0,E<=Ebar=8*400^3. All gates and first failures are charged separately, with adverse simultaneous exits taking priority. After entrance require A/L<=1/100, |Z|/L<=1/100, R=E²/(NL)<=2 and the existing count/macro caps.

Let b be the accepted remaining deterministic clock and

 q=b(L/T,E/T³)+AE b_l(L/T,E/T³)/(NT).

Suppose the ACTUAL stopped Dynkin decomposition from entrance sigma has

 q(X_t)=q(X_sigma)-(t-sigma)/T+D_t+M_t,
 sup|D_t|<=r,
 predictable bracket of M <=v, and all jumps |Delta M|<=j,

up to the first macro cap, original4T, or other admission failure. The budgets' own exit probabilities must be included in delta_adm. Use two-sided bounded-jump Freedman with Ldelta=log(2/delta), giving

 m=j Ldelta/3+sqrt(2v Ldelta+(j Ldelta/3)^2).

Then sup|M|<=m except probability delta. This is conditional on actual entrance data and deterministic uniform ceilings, not on future successful admission.

## Exact endpoint geometry

The inverse-flow representation gives

 0<=b(l,e)<= integral_0^infinity dw/[2(l+3w²/4)^2]
             =pi/(4sqrt(3) l^(3/2)) < l^(-3/2).

Also b_l is in [-1,0], and on e²<=3l, |b_e|<=6. Write l=L/T. Post-startup the corrector has absolute magnitude at most

 AE |b_l|/(NT)
 <=sqrt(2)/(100 T²) l^(3/2) min(1,l^(-5/2))
 <=1/(70T²).

Thus q>=-1/(70T²) everywhere in the admitted domain, without imposing a lower ratio. These estimates concern actual endpoint coordinates.

At startup, join (0,0) to (400/T,0) then to (400/T,E/T³). Every segment used for b_e stays in the padded cone because the endpoint has R<=2. Since both first derivatives are nonpositive,

 s_*-400/T-6Ebar/T³-1/(70T²) <=q(X_sigma)<=s_*.

Consequently sigma/T+q(X_sigma) differs from s_* by at most

 beta=800/T+6Ebar/T³+1/(70T²).

This deliberately conservative enclosure charges startup time and its actual state. It does not replace the random startup by a deterministic initial condition.

At a successful macro cap, either L>=N/5000 or E>=ceil(N/100). The latter and R<=2 imply L>=N/20000. Thus l>=T^4/20000>1. The displayed inverse-clock estimate and the sharper l^-1 corrector estimate give

 |q(X_tau_cap)|<=3*10^6/T^6 =c_cap.

Indeed 20000^(3/2)+sqrt(2)*200<3*10^6. A gate violation on the cap jump is charged as failure, not accepted using these endpoint bounds.

## Forced hit and final clearance

If

 s_*+beta+r+m+1/(70T²)<4,

then on the successful admission and martingale events, a non-hit at original4T contradicts q>=-1/(70T²) and its actual Dynkin identity. Hence a macro hit is earned by that horizon; it is not assumed in optional stopping. Its physical time satisfies

 |tau_cap/T-s_*|<=beta+r+m+c_cap.

Before macro cap the received count band has S>=N-12T. For N>=10^20 this is strictly above 15(N+2)/16. Therefore the actual first population-clearance time tau_clear at that threshold cannot precede tau_cap on the same event. The separately received entropy service gives tau_clear<=tau_cap+5 with its explicit delta_5. Hence

 tau_clear/T in [s_*-epsilon, s_*+epsilon+5/T],
 epsilon=beta+r+m+c_cap,

with total failure at most delta_adm+delta+delta_5. Use outward rational enclosures of s_* in an executable answer, and charge their acquisition and precision. No variance approximation, finite-N Gaussian CDF error, microscopic trajectory generation, or advantage over strongest retained ordinary computation is inferred from this interval alone.
