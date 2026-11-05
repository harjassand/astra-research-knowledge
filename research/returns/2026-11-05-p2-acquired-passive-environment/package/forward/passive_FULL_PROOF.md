# A finite-actuator, finite-bin acquisition theorem for arbitrary passive memory

## Outcome and scope

A scalar strongly convex passive-memory system can be probed through a finite moving harmonic trap to acquire a certified positive filtered memory kernel. The true unfiltered kernel is then within an explicit L1 allowance. The construction needs no hidden reset, no bath gap, no upper bath rate, no known number of modes, no instantaneous clamp, and no velocity or endpoint-position measurement.

This is an acquisition theorem within a specified calibrated measurement model. It does not infer unknown sensor gains, force-law errors, bath-energy bounds, or the overdamped source model from uncalibrated data. Fixed stiffness, force, sensor resolution, and bandwidth impose the displayed feasibility limits. The physical output is a finite collection of rounded force/position bin averages with a simultaneous error contract, not an oracle for K(t).

The accepted Astra passive residual theorem and its no-reset predecessors remain prior machinery. The present work closes a finite physical measurement route to the nodal information that theorem requires; it does not claim priority for random-sign cancellation, positive exponential kernels, or generalized-Langevin learning.

## 1. Source, controls, and measured quantities

Normalize a known positive drag coefficient to one. The physical equations are

x'(t)+V'(x(t))+m(t)=f(t),
z_lambda'(t)=-lambda z_lambda(t)+x'(t),
m(t)=integral z_lambda(t) dnu(lambda),
f(t)=k[q(t)-x(t)].

The known potential is C1 and mu-strongly convex, mu>0. The unknown measure nu is positive on [0,infinity), with mass b<=B. Neither its order nor any positive rate bound is specified. The initial bath energy obeys (1/2)integral z_lambda(0)^2 dnu<=E0. Thus

G0:=sqrt(2BE0) >= integral |z_lambda(0)| dnu.

Zero-rate modes are allowed. They need not relax at any time. Infinite first rate moment is also allowed.

Meters return actual averages of f and x over declared finite time bins, with bounded deterministic calibration and quantization errors epsilon_f,epsilon_x, plus conditionally centered sub-Gaussian errors. Noise proxies for a force bin of duration d and a position bin of duration w are denoted sigma_f^2(d),sigma_x^2(w). Distinct nonoverlapping bins and the two channels are independent conditional on the source history in the simple model used below. A more general calibrated covariance bound can replace this assumption. White instrument readout gives sigma_f^2(d)=v_f/d and sigma_x^2(w)=v_x/w.

These are readout noises, not an additional thermal force driving the source. Such a thermal model would require an additional prediction theorem. Measurement backaction is absent in the stated classical meter model.

## 2. A maximum principle that keeps the memory sign

Let K(t)=integral exp(-lambda t)dnu. It is continuous, nonnegative, decreasing, and has total variation at most B, even if K'(0) is infinite. Elimination of the hidden state gives

m(t)=g0(t)+(K*x')(t),
g0(t)=integral exp(-lambda t)z_lambda(0)dnu,
|g0(t)|<=G0.

For any C1 scalar e, integration by parts in bounded-variation form gives

(K*e')(t)=K(t)[e(t)-e(0)]+integral_0^t [e(t)-e(s)] [-K'(t-s)]ds,

with the last expression interpreted as a positive Stieltjes integral when needed. At a new maximum above e(0), this is nonnegative. At a new minimum below e(0), it is nonpositive.

Consequently, for a scalar equation

e'+k e+[V'(a(t)+e)-V'(a(t))]+K*e'=r(t),

with |r|<=D, the first-exit argument and strong convexity imply

|e(t)|<=max(|e(0)|,D/(k+mu)).

This is a scalar order argument. No analogous coordinatewise assertion is being made for a general vector-valued noncommuting bath.

A second useful identity is the hidden-state solution

z_lambda(t)=exp(-lambda t)z_lambda(0)+v(t)-exp(-lambda t)v(0)
            -lambda integral_0^t exp[-lambda(t-s)]v(s)ds,

where v=x-c for any constant c. The last two terms together are a weighted average of earlier v, with total weight one. If v stays in an interval of width W, its driven contribution has magnitude at most W. Hence integral |z_lambda(t)|dnu<=G0+BW for every t, independently of experiment count or duration.

## 3. Explicit initial alignment with fixed stiffness

An initial observed-coordinate bound is needed to price centering. It may come from a calibrated physical travel range or a sound observed-state enclosure; a finite time average alone should not silently be treated as an exact endpoint reading.

Suppose the trap initially has center q0 and fixed stiffness k. Compute the unique c solving

V'(c)+k(c-q0)=0.

Strong monotonicity gives uniqueness and a finite bisection bracket around q0 of radius |V'(q0)|/(k+mu). Certified evaluation and bisection errors are retained as an actuator/reference error. Let d0 bound |x(0)-c|. Hold q=q0, so no center motion or slew is required. Write kappa=k+mu and

R0=max(d0,G0/kappa),
Gprep=G0+2B R0.

The maximum principle gives |x-c|<=R0 throughout this guard. The hidden-state identity gives |m|<=Gprep. Direct scalar comparison then gives the stronger time-dependent enclosure

|x(t)-c|<=d0 exp(-kappa t)+Gprep/kappa.

For any requested initial tolerance delta0>Gprep/kappa, the finite guard

t_guard >= max(0,log[d0/(delta0-Gprep/kappa)])/kappa

ensures |x-c|<=delta0. At that point the bath energy is bounded by

Eprep <= (sqrt(2E0)+2sqrt(B)R0)^2/2,

and its L1 hidden-force envelope is Gprep. This does not erase frozen modes. It aligns only the observed coordinate. Use G=Gprep for the subsequent acquisition formulas; if alignment was already supplied, use its corresponding certified G.

For a finite-precision reference, keep the actual center program q=q0+u+u'/k and certify epsilon_root>=|V'(c)+k(c-q0)| from paid force evaluations. This avoids any center jump at the guard/probe join. In the guard formulas replace G0/kappa by (G0+epsilon_root)/kappa and Gprep/kappa by (Gprep+epsilon_root)/kappa; include epsilon_root in the subsequent actuator-error budget.

The guard force is bounded by |V'(c)|+epsilon_root+kR0 and must be included in the hardware bill. Increasing stiffness can make this initial peak large. If that bound exceeds a fixed external force cap, this particular preparation does not establish feasibility; a supplied aligned state or an independently justified lower-force preparation is needed.

Optional stiffness ramping is a different actuator capability and is not assumed here. In a y=x-z centering argument, any favorable damping term k+mu+b uses the true mass b. A supplied upper bound B cannot replace b in that favorable term; using only k+mu is uniformly safe.

## 4. Two finite trap programs

Let x_cmd=c+u(t), with u(0)=0, |u|<=A. Define

F_V(A)=max(|V'(c+A)-V'(c)|,|V'(c-A)-V'(c)|).

The simplest program is q=c+V'(c)/k+u. If |u'|<=U, its tracking allowance is

D_plain=G+2BA+U+F_V(A),
delta=max(delta0,D_plain/(k+mu)).

A stronger programmed variant feeds forward the known command velocity:

q=c+u+[u'+V'(c)]/k.

This uses no measured or hidden-state velocity. It removes the U term from the tracking forcing, giving

D_ff=G+2BA+F_V(A),
delta=max(delta0,D_ff/(k+mu)).

Indeed, substitution with e=x-x_cmd gives exactly

e'+k e+[V'(c+u+e)-V'(c+u)]+K*e'
=-[V'(c+u)-V'(c)+g0+K*u'].

The bounded command has |K*u'|<=2BA for arbitrarily many cycles. Apply the maximum principle. A known additive actuator-force error epsilon_act adds to D. A center error epsilon_q contributes k epsilon_q, so finer tracking requires corresponding calibrated stage resolution.

For velocity feedforward, the actual force and hidden envelope satisfy

Fmax=|V'(c)|+U+kdelta+epsilon_act,
Gstar=G+2B(A+delta).

The actual position speed is bounded by

W_x=U+kdelta+F_V(A+delta)+Gstar+epsilon_act.

No lambda moment is needed for this speed bound. For positive-only excursions u in [0,A], 2BA can be sharpened to BA and Gstar to G+B(A+2delta); the symmetric bounds are retained for convenience.

## 5. Explicit smooth ramp, slew, range, and work

Use the septic smoothstep

S(s)=35s^4-84s^5+70s^6-20s^7, 0<=s<=1.

It has S'=140s^3(1-s)^3>=0, unit displacement, symmetry S(s)+S(1-s)=1, and its first three derivatives vanish at the endpoints. Its derivative bounds are

C1=35/16,
C2=84/(5sqrt(5)),
C3=105/2.

A ramp u=sigma A S(t/h), a hold, and the reversed return give

U=C1 A/h,
U2=C2 A/h^2,
U3=C3 A/h^3.

The velocity-feedforward center is C2 across all joins, with

|q'|<=U+U2/k,
|q''|<=U2+U3/k,
|q-c|<=A+(U+|V'(c)|)/k.

For specified positive speed and acceleration caps Smax,amax, one simple sufficient choice is k>=1/h and

A<=min[Smax h/(C1+C2), amax h^2/(C2+C3), allowed amplitude].

Every quantity is finite. Small h is paid through smaller A, larger stiffness, and a more demanding signal-to-noise and calibration bill.

The total center travel for one complete velocity-feedforward probe is at most 2A+4U/k. Its absolute actuator work is at most Fmax(2A+4U/k). Plain moving-center control has travel exactly 2A. Initial stored trap energy and centering forces are counted separately.

## 6. A genuine finite-bin force balance

During a hold at x_cmd=c+sigma A, use a triangle psi of height one and support [t,t+2w]. It rises linearly for w and falls for w. Let phi=psi/w, so integral phi=1. If X_left and X_right are the two position box averages over the adjacent w intervals, then

integral phi x'=(X_right-X_left)/w

exactly. This identity uses measured time averages, not endpoint positions.

Split each w interval into n force boxes of duration d=w/n. For each of the 2n force boxes use coefficient a_r=psi(midpoint_r)/n. They are positive, sum to one, and satisfy

sum a_r^2=(4n^2-1)/(6n^3).

Because |f|<=Fmax and psi is linear between the joins,

|sum a_r F_box,r - integral phi f|<=Fmax/n.

No derivative or bandwidth bound on the true force is used. The bound applies even if arbitrarily fast hidden modes create a sharp force transient.

Compute the measured residual

R=sum a_r F_box,r - V'(c+sigma A) -(X_right-X_left)/w.

The only nonlinear force evaluation inside this measurement is at a known commanded hold position. Its error relative to the true V'(x) is bounded by

Omega(delta)=max_{s in {0,+1,-1},r in {+1,-1}}
 |V'(c+sA+rdelta)-V'(c+sA)|.

Monotonicity of V' makes these finitely many evaluations a sound bound. Continuity makes Omega(delta) tend to zero as delta tends to zero. A numerical evaluation allowance epsilon_V is also charged. No nonlinear transformation of noisy position data occurs.

One residual therefore has deterministic metrology/potential allowance

b_m=Omega(delta)+epsilon_V+epsilon_f+2epsilon_x/w+Fmax/n.

Its random-noise proxy is

v_m=sigma_f^2(w/n)(4n^2-1)/(6n^3)+2sigma_x^2(w)/w^2.

For the white readout model,

v_m<=2v_f/(3w)+2v_x/w^3.

Overlapping triangles may share bins. The simultaneous confidence bound below uses a union bound over nodes and does not require node independence.

If an instrument has an additional calibrated positive normalized causal signal filter with mean delay tau_f or tau_x, this can be paid separately. Shifting the test function gives a force error <=2F_history tau_f/w because ||phi'||_1=2/w. Here F_history must bound the entire force history contributing through the filter, including earlier centering or release peaks unless finite filter support or certified sensor clearing excludes them. Position filtering similarly gives <=2W_history tau_x/w using a speed bound over its contributing history. Add those terms to b_m. The filtered-force quadrature cap must also cover the filtered signal; using F_history is safe unless a smaller local cap is certified. The frontend linear range must cover the admitted physical force history. This extension needs no upper bath rate. A fixed sensor response time creates a precision floor; a faster finite sensor is a paid resource, not an ideal-bandwidth assumption.

## 7. Exactly which kernel is acquired

Let r_h(s)=S'(s/h)/h and define

c_h(lambda)=integral_0^h r_h(s)exp[-lambda(h-s)]ds,
d_w(lambda)=((1-exp(-lambda w))/(lambda w))^2,

using d_w(0)=1. A ramp of signed amplitude sigma A followed by the triangular readout produces the signal sigma A Kstar(t), where

Kstar(t)=integral exp(-lambda t)c_h(lambda)d_w(lambda)dnu.

Both factors lie in [0,1], so Kstar is a positive exponential mixture with total height at most B. The factor c_h is the Laplace transform of the ramp delay h-s, whose mean is h/2 by symmetry. The factor d_w is the Laplace transform of the sum of two uniform [0,w] delays, with mean w.

Thus c_h d_w=E exp(-lambda D) for a nonnegative delay D of mean h/2+w. Since K-Kstar>=0,

||K-Kstar||_L1(0,T)
=integral E[(1-exp(-lambda D))(1-exp(-lambda T))/lambda]dnu
<=B E D=B(h/2+w).

At lambda=0 the integrand is zero, and the formula is read by its continuous limit. Frozen modes are transmitted exactly. No identification or resolution of the fastest modes is required because their missing integrated influence is bounded.

For tracking error e, integration by parts gives |K*e'|<=2Bdelta, including a nonzero initial e. This remains true over each local cycle after splitting off its initial hidden state.

## 8. Random-sign retained-device acquisition

At each deterministic cycle start, choose a fresh independent sign sigma_j before the ramp. Let Y_jl=sigma_j R_jl/A for node l. Conditional on the previous complete history, the retained hidden state is already fixed. Its freely decaying force contributes sigma_j H_jl/A with conditional mean zero and |H_jl|<=Gstar. The trajectory tracking correction contributes at most 2Bdelta/A and need not be centered.

Choose any M distinct rational observation starts 0<=t_1<...<t_M<=T; they need not form a lattice and need not be separated by w. Put t_max=max_i t_i. For N cycles and failure probability alpha, the standard conditional sub-Gaussian calculation gives simultaneously

|(1/N) sum_j Y_jl - Kstar(t_l)|
<= (2Bdelta+b_m)/A
 +sqrt[2(Gstar^2+v_m)log(2M/alpha)/(N A^2)].

The formula is a martingale result. It assumes neither independent hidden trajectories nor matched hidden preparations. Returning the commanded position to c only restores the actual position within delta.

## 9. Aged-baseline acquisition and its precise constant

A second mode avoids the random hidden-offset variance. After alignment, hold u=0 for H>2w. Measure a baseline triangular residual on [H-2w,H]. Then ramp positively during [H,H+h] and measure post-ramp node t on [H+h+t,H+h+t+2w]. Estimate Kstar(t) by

(R_post,t-R_base)/A.

The initial hidden force satisfies, for t>0,

|g0'(t)|<=integral lambda exp(-lambda t)|z0|dnu<=G/(e t).

The first inequality is justified even without a rate moment, since lambda exp(-lambda t)<=1/(et). Comparing the two positive weighted averages and using their mean time separation gives

|g_post_average-g_baseline_average|
<=G(h+t+2w)/(e(H-2w)).

The numerator uses mean separation, not the most distant support endpoints. The two memory tracking errors cost 4Bdelta. The two potential/meter residual errors cost 2b_m.

Use the same arbitrary rational starts t_i and put t_max=max_i t_i<=T. The probe hold lasts t_max+2w. For R independently metered repetitions of this aged experiment, a simultaneous bound is

|estimate(t_l)-Kstar(t_l)|
<= [D_age+4Bdelta+2b_m]/A
 +sqrt[4v_m log(2M/alpha)/(R A^2)],

where

D_age=G_use(h+t_max+2w)/(e(H-2w)).

For one probe, G_use is the envelope at the start of its quiet hold. For repeated probes, G_use=Gstar bounds every cycle start. The baseline measurement is shared across nodes, but the variance of each baseline difference is at most 2v_m; the union bound is still sound. The sign can be fixed positive. A long guard makes the old force nearly constant, not small; zero-rate offsets are measured and subtracted rather than erased.

## 10. A constructive finite parameter choice

For a desired nodal allowance eta>0, select h,w to fit the permitted smoothing bias, and choose A>0 satisfying the physical speed/acceleration limits. In aged mode, the following sufficient allocation makes the total displayed nodal error at most eta:

4Bdelta+2Omega(delta) <= A eta/4;
2epsilon_V+2epsilon_f+4epsilon_x/w <= A eta/8;
n >= 16Fmax/(A eta);
H >= 2w+4G_use(h+t_max+2w)/(e A eta);
R >= 64v_m log(2M/alpha)/(A^2 eta^2).

Round n and R upward and take R>=1. Add optional sensor-response terms to the deterministic metrology allocation. Choose k and initial centering so the stated tracking delta actually holds. With fixed instruments that do not meet the calibration/noise/force/stiffness requirements, report the larger achieved bound instead of asserting the desired accuracy.

Because V' is continuous on the bounded operating interval, the delta condition can be met by finite halving and paid force-law evaluations, provided stiffness and metrology resources can be increased. No polynomial bound on those evaluations follows from strong convexity alone. If V' has a supplied local Lipschitz constant, an explicit delta=O(A eta/(B+L)) suffices.

For orientation only, with fixed T,B,G, local force Lipschitz constant and fixed slew caps, choosing h,w=Theta(epsilon), A=Theta(epsilon^2), eta=Theta(epsilon) permits delta=Theta(epsilon^3), k=O(epsilon^-3), n=O(epsilon^-3), an optional lattice of M=O(epsilon^-1) starts, and aged H=O(epsilon^-3). This is a finite resource construction, not an optimality claim. With fixed white position-noise density, v_m grows like w^-3 and the repetition bill can be as large as O(epsilon^-9); an aged protocol that repeats that many long guards is then unattractive. The random-sign mode may be cheaper. A one-probe aged experiment instead requires correspondingly precise readout. The formulas make that tradeoff explicit.

## 11. Full execution bill and finite readout bits

Random-sign mode requires source time

t_guard+N[2h+t_max+2w],

at most 2NM requested position boxes, 2nNM requested force boxes, and N fresh signs.

Aged mode requires source time

t_guard+R[H+2h+t_max+2w].

Only the final 2w of each quiet hold needs to be read. Including its baseline triangle, the conservative requested-meter bill is 2R(M+1) position boxes and 2nR(M+1) force boxes. Any additional future-initialization window is counted separately. The sum of requested window durations per channel is 2Rw(M+1); overlapping windows can share one integrated meter record, so actual metered occupancy is the length of their union. Source occupancy still includes the full R H. No independence between overlapping nodes is assumed.

All requested endpoints are known rational numbers: each force triangle uses t_i+r w/n for r=0,...,2n, and its position boxes use t_i,t_i+w,t_i+2w. Merge the endpoints and read cumulative integrated meters there. The weighted sums can be accumulated by coefficient jumps at the corresponding endpoints, using O(Mn) endpoint-update operations and O(M) accumulators per probe, plus scheduling/sorting. A heap merge of the already sorted per-window lists costs O(Mn log M) comparisons. A simpler implementation that scans all active windows is conservatively O(M^2 n). This operation count does not claim that 2nM requested averages are independent experiments.

The exact merged schedule has a finite minimum nonzero endpoint separation that can be computed from the rationals. Its clock resolution and bit representation are paid resources. Alternatively, round all endpoints to a calibrated common finite clock grid, merge coincidences, and include the explicit endpoint-timing allowances described below. There is no need to execute all ticks of a potentially fine common denominator grid. Stiffness, peak force, center range, slew, stage resolution, and work have already been displayed.

The force coefficients are rational: their ascending half is a_r=(2r+1)/(2n^2). With rational chosen A,w and rounded meter reports, the weighted sums and divisions can be executed by exact finite integer/rational arithmetic. Evaluation of the known V' is separately certified to epsilon_V. This avoids silently assigning exact-real arithmetic to the data reduction.

Finite ADC range is also possible. If there are L_f force readings, allocate overflow probability alpha_ADC and choose a force range exceeding

Fmax+calibration allowance+sqrt[2sigma_f^2(d)log(2L_f/alpha_ADC)].

Use the corresponding position range |c|+A+delta plus its noise allowance. A quantization step 2epsilon_quant then has bounded rounding error epsilon_quant whenever unsaturated. Its bit count is the ceiling of the logarithm of range divided by step, plus a sign bit. Any overflow must be flagged; the overall confidence loses at most the allocated overflow probability. This avoids treating Gaussian readout as an infinite-range, infinite-precision number.


### Cumulative readout precision and finite clock error

If cumulative force and position integrals have bounded per-reading deterministic errors epsilon_Yf and epsilon_Yx, the corresponding one-residual allowance is at most 2epsilon_Yf/w+4epsilon_Yx/w^2. This replaces, rather than duplicates, the per-average metrology allowances. It follows because the total absolute coefficient of the cumulative force readings is at most 2/w and that of the three cumulative position readings is 4/w^2. This accounting prevents the arbitrary-node implementation from silently changing the meter precision model. For cumulative ADC range, replace the bounded average Fmax by Fmax L_int (and Xmax by Xmax L_int), where L_int is the longest active integration duration between meter resets; the white-noise proxy is v_f L_int or v_x L_int. The meter integrator may reset between acquisition windows without resetting or perturbing the hidden bath. Charge its resulting bit range and precision accordingly.

Suppose each intended endpoint is executed within tau_clk, using a deterministic or noise-independent calibrated clock. For the physical signal, add 2Fmax tau_clk/w+4Xmax tau_clk/w^2 per residual, where Xmax=|c|+A+delta bounds position over the relevant windows. The integrator readings at displaced endpoints still have Gaussian white-noise variances, but their covariance is computed at the actual endpoints. A safe proxy, allowing even rounded endpoint coincidences, is

v_m,clock <= v_f[ sqrt(2/(3w))+2sqrt(tau_clk)/w ]^2
           +v_x[ sqrt(2/w^3)+4sqrt(tau_clk)/w^2 ]^2.

The proof bounds the L2 change of each step-function integration weight by sqrt(tau_clk) times its total coefficient variation. Use this proxy in place of v_m. Apply the force and position bounds on the enlarged measurement windows. The comparison is to the nominal finite-bin observable, so these timing allowances already cover an endpoint that shifts slightly into a ramp; no instantaneous force derivative is used. Ensure H-2w>tau_clk and keep the controlled source running through the final shifted endpoint. If the entire readout is deliberately padded by an additional known delay instead, that positive delay adds at most B times its duration to the L1 filtering allowance. Thus the fitter's rational nodes do not imply an unpriced ideal timing oracle.

## 12. Interface to the unfiltered nonlinear prediction certificate

Suppose the finite positive fitter returns Khat with total mass at most B and residual at every reported node at most eta_fit, while acquisition supplies a simultaneous sound eta_acq. Both Kstar and Khat are decreasing. If the observed starts include 0 and T, let Delta=max_i(t_{i+1}-t_i) be their actual maximum mesh gap; Delta is independent of the triangle width w. Then

||K-Khat||_L1(0,T)
<=B(h/2+w)+2B Delta+T(eta_acq+eta_fit).

For a monotonicity-only certificate, include endpoint observations 0,T, or explicitly price the uncovered end intervals. More sophisticated positive fitting certificates may use the arbitrary nodes directly. The first term is the proved finite-control/readout filtering cost. The remaining terms are the accepted positive-kernel mesh certificate. This is a bound on the original kernel K, not merely on a convenient filtered target.

The accepted passive residual theorem can then use this kernel allowance multiplied by ||xhat'||_2, together with the separately acquired current hidden-force mismatch and numerical execution residual. Kernel acquisition does not initialize the future bath. Returning the observed coordinate and measuring a current baseline are separate paid operations; no zero hidden-force assumption should be introduced at the prediction start.

## Verification and limitations of the present artifacts

`passive_verify_bounds.py` checks the exact triangular weight variance, septic derivative constants, and the filter/aging inequalities on 182 positive modes including one frozen mode and rates from 10^-12 to 10^12. Its results are in `passive_bound_checks.json`. `passive_verify_arbitrary_nodes.py` additionally checks the merged cumulative-meter reduction in exact rational arithmetic for overlapping nonuniform nodes, verifies the nonzero cross-node noise covariances, and checks the finite-clock signal and variance allowances. Its results are in `passive_arbitrary_node_checks.json`. The root programme is building the independent joined nonlinear fixture; it is not duplicated here. Numerical ODE quadrature is not presented as an interval-validated physical experiment or as the actual fine-bin record count.

The completed claim is the finite acquisition operation and its exact analytical error contract under explicit source and calibrated-instrument assumptions. Unknown sensor gains, an unspecified measurement-noise law, unknown thermal forcing, a missing initial observed-range bound, or hardware that fails the displayed feasibility inequalities remain genuine limitations rather than hidden oracle calls.

## Finite physical deployment handoff

The acquisition port alone does not provide instantaneous release or a free untrapped force input. The separate `RELEASE_HANDOFF.md` proves a finite stiffness ramp to zero, a physically programmed additive drive through an independently movable local viscous support, the updated delta_rel and gamma_rel initialization bounds, and the associated actual force, slew, work, power, calibration, and query-programming costs. Switchable stiffness and selective viscous-support motion are explicit additional resources. A fixed-trap predictor instead includes that trap in the known physical potential and is a different operation.
