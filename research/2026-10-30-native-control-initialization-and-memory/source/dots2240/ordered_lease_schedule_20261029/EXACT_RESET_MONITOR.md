# Exact finite-rate clock measurements from label-resolved one-site resets

This implements the projected-path mechanism using only explicitly calibrated on-site Hamiltonians and on-site reset transitions, without direct Markov dephasing or a limiting argument.

## Physical alphabet and channels

Append a two-level monitor to each monitored physical qudit. For its CLOCK-POSITION/epoch/ownership labels c, let P_c be mutually orthogonal complete projectors. They are identity on quantum data and syndrome/Kraus workspace. Set

 H_mon=Omega I_clock,data,workspace tensor X_mon,
 M_c=sqrt(kappa_m) P_c tensor |0><1|_mon,

with Omega,kappa_m>0 fixed. All existing site Hamiltonians/jumps act as identity on the monitor. These M_c are DISTINCT, label-resolved decay channels. Replacing them by the single unresolved reset I_clock tensor |0><1| would NOT measure the clock.

The enlarged site dimension doubles. The number/selectivity of reset transitions scales with the fixed clock alphabet. Both are explicitly priced fixed resources under the finite-qudit one-site-transition convention.

Since sum_c M_c^*M_c=kappa_m I tensor n_mon, no-monitor-emission evolution factors between the clock/data dynamics and the monitor. A resolved emission c exactly applies P_c to the current clock and resets the monitor. Thus, once monitors are product factors, their emission times are independent damped-Rabi renewal processes even while clocks are moving. These are exact projective events, but their times are NOT Poisson.

Each P_c commutes with the clean history dressing. Adding these monitor operations therefore changes scheduling but preserves exact completed-data-channel semantics. Workspace-resolving measurements would not have this justification and are excluded.

## Uniform isolated-monitor window probability

Write A=-i Omega X-(kappa_m/2)n. The first-emission effect in a positive-length interval [0,u] is

 E_u=integral_0^u kappa_m exp(A^*s)n exp(As) ds.

E_u is strictly positive. Indeed a vector in its kernel would satisfy <1|exp(As)v=0 throughout an interval. Analyticity, evaluation at zero, and its first derivative imply v_1=0 and Omega v_0=0, hence v=0.

For EXACTLY one emission in the interval use

 F_u=integral_0^u kappa_m exp(A^*s)n exp(As)
                 ||exp(A(u-s))|0>||^2 ds.

Thus alpha(u)=lambda_min(F_u)>0 and is computable from a 2x2 matrix integral. The no-emission survival from every state is >=exp(-kappa_m u).

## Local monitor flush and finite measurement windows

Let n be the number of monitored sites in the fixed local proof patch. Divide a window epsilon into n slots. In slot i require exactly one emission from monitor i and no emissions from the others. Uniformly over initial monitor states, the probability is at least

 w_mon=alpha(epsilon/n)^n exp[-kappa_m (n-1)epsilon]>0.

The exact unresolved timing-record effect is I_clock tensor the isolated-monitor record effect: adjoint evolution on I_clock tensor A_mon closes autonomously because sum_c P_c=I. This remains true despite moving clocks. Consequently this bound also applies with monitor-monitor/clock entanglement: at each step the selected isolated-monitor event effect is >=alpha I and the other silence effects have the displayed scalar lower bounds. Main clock dynamics never couples Hamiltonianly to monitor degrees of freedom.

Use one such window as a FLUSH, with no restriction on the clock-label outcomes. Every monitor has then reset once; conditioned on the full local record, all monitors are known pure factors independent of the remaining clock/data state. Subsequent no-emission evolution preserves that factorization. The flush itself need not imitate a simultaneous clock measurement.

After the flush, every later selected window has a clock-independent timing density. Conditional on any allowed timing pattern, its clock instrument is a sequence of exact P_c projections separated by total main-clock evolution epsilon. Consequently the SAME 4B epsilon approximation to an ideal simultaneous joint clock measurement used in FINITE_RATE_PROJECTED_PATH.md applies, irrespective of how small w_mon is. No division of the error by w_mon is needed: first condition on the independent monitor timing pattern, bound its normalized clock instrument, then integrate the timing density.

## Transfer of the finite-path bound

Use delta,epsilon,L,p_0,B from FINITE_RATE_PROJECTED_PATH.md. After the flush, select L+1 measurement windows and no monitor events during the L transition windows. A safe completion bound is

 c_monitor=(p_0^L/2) w_mon^(L+2) exp[-kappa_m n L delta]>0,
 T_monitor=L delta+(L+2)epsilon.

The additional power/window accounts for the flush. All parameters are fixed finite constants; alpha is an explicit finite-dimensional Gramian eigenvalue. This is a genuine reset-only implementation of the alternate monitored scheduler, not an infinite-rate classicalization or effective-generator approximation.

The same legal-sector and repair limitations as FINITE_RATE_PROJECTED_PATH.md apply.

## Independent audit

The independent challenge worker checked the monitor factorization, strictly positive event Gramian, ordered-slot bound, flush argument, and final probability factors; no defect found. The direct finite-rate projected-path proof has a separate audit in FINITE_RATE_PROJECTED_PATH_AUDIT.md. These are mathematical audits of the stated ideal model, not experimental validation.
