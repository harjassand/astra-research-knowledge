# Unflagged dilute sensors: closed weighted join and parameter-selection theorem

2026-11-01. Reconciles the parent's ROOT_DILUTE_SENSOR_POISSON_COMPILER.md with the weighted FLAG-XOR join. No collision flags, accepted-history records, or independent error-event assumption are introduced. The actual legal clock laws are independent because every phase instrument is TP and advances on all outcomes. Malformed native clocks remain the explicitly stated final conditional audit.

## 1. Actual own clock, including post-readout return phases

Clock states are 0 (idle),1,...,D (busy). Transition 0->1 occurs at r and performs preparation; every busy transition occurs at k, including D->0. Readout is q->q+1, with 1<=q<=D and destination0 when q=D. Thus D-q return phases are retained. Readiness r_s is armed only on phases1,...,q and killed at readout. Use r<=k/(4D).

For sensor restoring reward A>0, Boolean price epsilon, and cache sensitivity B, define h=epsilon B k at phase q, zero elsewhere. Put tau=1/r+D/k. The ACTUAL killed first-passage solution is
 t_0=A(1/r+q/k)+epsilon B,
 t_j=A(q-j+1)/k+epsilon B,                         1<=j<=q,
 t_j=A[(D-j+1)/k+1/r+q/k]+epsilon B,              q<j<=D.
In particular the POST-readout value is
 t_post=A tau+epsilon B,
and t_max=t_post. The accepted-readout reward is g=k t_post at phase q. Solving the armed reward equation for g+h gives the constant
 xi=A tau+2 epsilon B
on every armed phase and zero elsewhere.

For P_s=t e_s+xi r_s, the noncollision operator identity is
 L P_s=-A e_s-h(e_s+r_s)+epsilon_p r xi I_idle.
The Boolean cache-overwrite increase is at most h(e_s+r_s), so those terms cancel. The preparation impurity epsilon_p is physical and distinct from epsilon. The formula includes return waiting and never replaces t_post by t_source.

## 2. Direct collision charge without flags

Let I_pq project onto both own clocks being busy. For an ordered overlapping pair (p,q), the following are the only needed bounded-error estimates:

(a) A neighboring phase operation at total hazard at most k changes p's readiness projector by at most identity in operator order, supported on I_pq. Its price costs at most k xi_p I_pq. Preparation acts only on q's probe; a readout/reset is also bounded by this allowance if needed. No double-counting of mutually exclusive source-phase channels is required.

(b) At p's readout, the dressed check may differ from the bare check only if an overlapping neighbor is busy. Thus the readout mismatch is bounded by r_p+sum_q I_pq, and the cache-flip projector by e_p+r_p+sum_q I_pq. These are operator inequalities: outside the overlap projector the identities are exact, and inside it both discrepancy projectors are bounded by identity. No classical assumption on probes is used.

The readout gain and Boolean leakage therefore add k(t_post,p+epsilon B_p) I_pq=k xi_p I_pq. Together with (a), the combined source/Boolean remainder is bounded by
 sum_(ordered overlapping p,q) 2k xi_p I_pq.
This includes bad reports, rather than pretending accepted reports are clean. The exact factor2 uses the stated one-phase-outgoing-hazard convention; if an actual primitive list has additional independent channels, its summed hazard must replace k.

## 3. Actual pair-clock Poisson price, with an explicit uniform bound

For two identical independent cycle clocks the stationary busy fraction is
 f=Dr/(k+Dr),  pi(I_pq)=f^2.
Let Q_pair be their actual product generator and solve
 Q_pair H_pq=-I_pq+f^2.
Shift the solution by its minimum so H_pq>=0.

A quantitative bound follows without appealing only to continuity at r=0. Before hitting (0,0), let V_rem be the sum of remaining busy-phase transitions. Its value is at most2D. At least one busy clock advances at rate k; new departures from idle add at mostD each, at total rate at most2r. Hence
 Q_pair V_rem <= -k+2Dr <= -k/2
until the hitting time T_00. Therefore E_x T_00<=4D/k. The normalized centered Poisson solution has the hitting representation
 H_raw(x)=E_x integral_0^T00 [I_pq(X_t)-f^2]dt,
with H_raw(0,0)=0. Its magnitude is at most4D/k; centering the reward also enforces the Poisson equation at (0,0). Thus
 0<=H_pq<=8D/k.

Add the positive physical-clock price 2k xi_p H_pq for each ordered overlapping pair. Its generator cancels the pointwise collision charge exactly and leaves floor2k xi_p f^2. Bounds usable in the barrier budget are
 pair-price height <=16D xi_p,
 2k xi_p f^2 <= (5/2)D^2 A_p (r/k)
                         +4D^2 epsilon B_p (r^2/k),
because tau<=5/(4r). This is an actual occupation-potential identity at every clock state, not a marginal estimate over the full storage time.

## 4. Optional finite detector-error occupation price

For independent readout bit-flip probability eta<=1/2, the extra source-plus-Boolean floor is eta k xi I_(phase=q). Do NOT bound this by eta k xi at every instant if a useful dilute budget is desired. The actual stationary readout-phase probability is
 pi_q=r/(k+Dr).
Solve the own-clock centered equation Q H_q=-I_(phase=q)+pi_q and shift it nonnegative. Hitting idle gives 0<=H_q<=2D/k. Adding eta k xi H_q has height at most2D eta xi and replaces the floor by
 eta k xi pi_q <= eta r xi.
General detector/helper errors must instead be charged through their actual local generator; this independent-bit model is not universal.

## 5. Closed legal-clock generator join

Let E=sum_i w_i e_i^B be Boolean consistency, delta_i=w_i-sum_child w_child>0, and let the actual circuit provide R_i/R_s as in the accepted FLAG-XOR proof. Let D_W bound a flag actuation's |Delta W| and B_act bound its |Delta E|. Use actuator rate a (distinct from the source departure r) and choose
 epsilon=a/k,
 a/k <=1/(2B_act),
 A_s=a[(1+D_W)R_s+1],
 gamma_i >= k[((1+D_W)R_i+w_i)/delta_i].
Then a0=1-epsilon B_act>=1/2. The identity a0+(D_W+epsilon B_act)=1+D_W makes these rate choices explicit. The Boolean gate rates need not be imposed on the quantum source.

Let V=W+Z, where Z includes epsilon E, all own-source prices, all ordered pair prices, optional detector prices, and the separately audited small clock-inversion penalties. On legal clocks, combining all actual terms gives
 L V <= -(a c_0/2) W -a E -a sum_s e_s
         +sum_s epsilon_p,s r xi_s
         +sum_s eta_s k xi_s pi_q
         +sum_(ordered p,q) 2k xi_p f^2,
where c_0 W is the accepted witness lower bound on true improving moves. Dropping the additional negative terms gives LV<=-cW+b n with c=a c_0/2.

Native malformed-clock operations contribute R_malformed. They are not included in the displayed legal identity. The parameter theorem below is conditional on the concrete audit showing that the chosen clock-inversion repair dominates R_malformed without adding an unpriced positive floor. Additional hardware noise gives its actual bound nu_V n; include it in b. Miscalibrated jump cross terms are part of that bound.

## 6. Fully explicit density constants and existence hierarchy

Let N_sensor<=C_s n, at most Delta overlapping neighbors per sensor, E<=C_E n, B_s<=B, and A_s<=C_A a with C_A=max_s[(1+D_W)R_s+1]. Let epsilon_p,s<=p and eta_s<=eta<=1. For r<=k/(4D), the nonclock part of Z is bounded by
 Z_nonclock <= C_z (a/r) n,
where the following conservative finite constant suffices:
 C_z=C_E+C_s[(5/2)C_A+3B
             +Delta(20D C_A+32D B)
             +2D((5/4)C_A+2B)].
The last bracket covers detector occupation prices. Let clock penalties contribute at most z_clk n. Thus z=C_z a/r+z_clk satisfies 0<=Z<=z n.

Set
 C_p=C_s[(5/4)C_A+2B],
 C_col=C_s Delta D^2[(5/2)C_A+4B].
The intensive mean floor satisfies
 b/a <= C_p(p+eta)+C_col(r/k)+nu_V/a.
Consequently
 z+b/c <= C_z a/r+z_clk
             +(2/c_0)[C_p(p+eta)+C_col(r/k)+nu_V/a].

For any positive interior allowance theta below the protected barrier density, sufficient EXPLICIT choices are
 C_z a/r <=theta/5,
 z_clk<=theta/5,
 p+eta<=theta c_0/(10C_p),
 r/k<=min{1/(4D),theta c_0/(10C_col)},
 nu_V/a<=theta c_0/10,
together with a/k<=1/(2B_act) and the gamma_i choices above. Then z+b/c<=theta and
 LV<=-cV+(b+cz)n,
with an equilibrium mean scale no larger than theta n.

There is a nonempty FIXED intensive parameter region: fix k; choose r/k sufficiently small; choose a/r sufficiently small; set epsilon=a/k and the finite classical gamma_i; choose a small clock-penalty height and then the finite sorting rate demanded by the malformed-clock audit; finally require finite preparation/detector impurity and actual hardware-noise strength below the stated positive bounds. No parameter depends on total n.

This is an existence hierarchy, not a claim about a prespecified noise rate. High-rate sorting hardware has actual noise: nu_V must be evaluated AFTER selecting its rate and all price/support constants. Slowing a indefinitely cannot tolerate fixed nu_V, and if a given device fails nu_V/a<=theta c_0/10 the theorem does not apply. All constants may be prohibitively large.

## 7. Protected interface and exact remaining condition

The readiness projectors commute with the dressed true stabilizers by the Pauli-sign cancellation used in the source construction; cache/Boolean/occupation terms do as well. Thus this construction uses the dressed W barrier, not a bare-check substitution. Readiness terms need not commute mutually on colliding configurations; the global exponential step must use the noncommuting local estimate, not the commuting special case.

The new derivation removes the former reliable-collision-flag premise and does not assume collisions never happen. Conditional native mean closure now depends on the actual malformed-clock transition audit and on its sorting/noise budget, not on an ideal collision-free full source. A complete memory result still requires the parent's protected-component, exponential and boundary-bandwidth interface checks. Mean drift alone is not claimed as an exponential lifetime theorem.

The active comparator gets these same sensors, physical clocks, local gates, connectivity, impurities and rates. No practical advantage is asserted.

## 8. Finite-generator verification

`check_dilute_prices.py` directly constructs the own and product clock matrices. It verified 180 readout/return cases with D=1,...,8, including slow-start ratios down to10^-4 and the r/k=1/(4D) boundary: exact killed t/xi solutions, product stationarity, pair centered Poisson equations, detector centered equations, and both stated uniform height bounds. Results are in `check_dilute_prices_results.txt`. This is a generator/algebra check, not a test of malformed native clock transitions or the quantum collision operator identities.
