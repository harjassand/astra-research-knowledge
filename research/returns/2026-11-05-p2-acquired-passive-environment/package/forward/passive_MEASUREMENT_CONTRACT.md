# Concrete finite-trap / finite-bin passive-kernel acquisition

## Main conclusion

Raw force and position box meters suffice; an extra net-restoring-force channel is unnecessary. During each hold, subtract the paid known value V'(commanded hold position). The resulting nonlinear subtraction error is bounded by the known force-law modulus at the certified tracking tolerance. Two adjacent position box averages give the integrated derivative term exactly under a triangular test. All force weighting is implemented from finitely many force boxes, with a bounded-force quadrature error. There is no point-position, velocity, instantaneous-clamp, rate-cutoff, or hidden-reset oracle.

Both random-sign repeated probes and one aged-baseline probe are available. The latter gives a deterministic old-memory drift allowance and can remove the random-offset sample bill.

## Source and declared meter model

x'+V'(x)+m=f, z_lambda'=-lambda z_lambda+x', m=integral z_lambda dnu, f=k(q-x). V is known C1 and mu-strongly convex; nu is a positive finite measure on [0,infinity), total mass<=B, with no rate gap/order/upper bound/moment. Initially (1/2)integral z0^2 dnu<=E0. Let G=sqrt(2BE0). The drag coefficient is known and normalized to one. This is a deterministic passive bath with noisy readouts, not an undeclared thermal force model.

Meters return true finite-bin time averages plus deterministic calibration/quantization errors bounded by epsilon_f,epsilon_x and centered random errors. For disjoint bins and channels, those random errors are conditionally sub-Gaussian with known proxies sigma_f^2(d),sigma_x^2(w), independent of future fresh signs and with no measurement backaction on the source. For white instrument readout, use sigma_f^2(d)=v_f/d and sigma_x^2(w)=v_x/w. A correlated or sign-dependent bias belongs in the deterministic error budget; it is not assumed away by averaging.

## Finite trap command and global tracking

Use x_cmd=c+u(t), u(0)=0, |u|<=A, |u'|<=U, and q=c+V'(c)/k+u. Write kappa=k+mu,

F_V(A)=max(|V'(c+A)-V'(c)|,|V'(c-A)-V'(c)|),
D=G+2BA+U+F_V(A),
delta=max(|x(0)-c|,D/kappa).

Then |x-x_cmd|<=delta for arbitrarily many cycles. At a new extremum of e=x-x_cmd the derivative-memory term has the favorable sign:

(K*e')(t)=K(t)(e(t)-e(0))+integral_[0,t](e(t)-e(s))[-dK(t-s)].

This bounded-variation identity requires no moment of lambda. It proves the scalar maximum principle directly. The actual force is bounded by Fmax=|V'(c)|+k delta. The hidden L1 force envelope at every future cycle start is bounded by

Gstar=G+2B(A+delta).

A known actuator force error epsilon_act adds to D and Fmax. A center-position calibration error epsilon_q produces epsilon_act=k epsilon_q. Fixed stiffness or fixed center-resolution therefore creates an explicit precision floor; it is not erased statistically.

For repeated positive excursions u in [0,A], tighten 2BA to BA and Gstar to G+B(A+2delta). All statements below remain valid with the looser symmetric bounds.

## Smooth cycle and finite slew

S(v)=10v^3-15v^4+6v^5. Ramp u from 0 to sigma A as sigma A S(t/h), hold, and return using the reversed ramp. The center is C2; speed <=(15/8)A/h and acceleration <=(10 sqrt(3)/3)A/h^2. Thus fixed speed and acceleration caps permit small h by reducing A proportionally to h^2, with the explicit metrological/statistical costs below.

## Exact finite-bin observable

Choose arbitrary rational starts t_i in [0,T], i=1,...,M, and let t_max=max_i t_i. For each start, use a triangular test psi_i on [t_i,t_i+2w], height one, rising for w and falling for w. The readout width w is independent of the spacing between starts. During a hold at x_cmd=c+sigma A, position box averages X_left,X_right satisfy exactly

(1/w)integral psi_l x'=(X_right-X_left)/w.

Subdivide each w into n force boxes, d=w/n. Midpoint coefficients a_r=psi_l(mid_r)/n, r=0,...,2n-1, are nonnegative and sum to one. Their weighted force average differs from (1/w)integral psi_l f by at most Fmax/n, irrespective of force bandwidth. Define the measured force residual

R_jl=sum_r a_r F_jlr - V'(c+sigma A) -(X_right-X_left)/w.

The nonlinear force mismatch is bounded by

Omega(delta)=max_{s in {0,+1,-1},r in {+1,-1}} |V'(c+sA+r delta)-V'(c+sA)|.

Only finitely many force-law evaluations are required. A certified force-law evaluation error epsilon_V is added separately. No nonlinear function of a noisy position reading is used.

The one-residual deterministic error, excluding tracking-memory error, is

b_meter=Omega(delta)+epsilon_V+epsilon_f+2epsilon_x/w+Fmax/n.

Its random-noise proxy is

v_meter=sigma_f^2(w/n)*(4n^2-1)/(6n^3)+2sigma_x^2(w)/w^2
       <=2v_f/(3w)+2v_x/w^3  [white instrument readout].

Different kernel nodes may share position and force bins; the bounds do not assume their independence.

## Positive filtered kernel and horizon-uniform bias

Let r_h(s)=S'(s/h)/h and

c_h(lambda)=integral_0^h r_h(s) exp[-lambda(h-s)]ds,
d_w(lambda)=((1-exp(-lambda w))/(lambda w))^2, d_w(0)=1.

The measured signal is Kstar(t)=integral exp(-lambda t)c_h(lambda)d_w(lambda)dnu. This remains a positive exponential mixture of total weight<=B. Its finite-ramp and finite-box filtering obeys

||K-Kstar||_L1(0,T)<=B(h/2+w).

Proof: c_h d_w is the Laplace transform of a nonnegative delay with mean h/2+w; integrate 1-exp(-lambda delay) over t and use (1-exp(-lambda delay))/lambda<=delay. Frozen modes lambda=0 are transmitted exactly.

## Random-sign acquisition, no hidden reset

Choose arbitrary distinct rational starts t_i in [0,T], i=1,...,M, and put t_max=max_i t_i. At each cycle start choose a fresh Rademacher sign before the ramp. Let Y_jl=sigma_j R_jl/A. Splitting the state at cycle start gives signal Kstar(t_l), retained initial force sigma_j H_jl/A with conditional mean zero and |H_jl|<=Gstar, and tracking-memory error <=2Bdelta/A. Consequently for N cycles and M nodes, with probability >=1-alpha simultaneously at all nodes,

|mean_j Y_jl-Kstar(t_l)| <= (2Bdelta+b_meter)/A
 +sqrt(2(Gstar^2+v_meter) log(2M/alpha)/(N A^2)).

This is a martingale bound, not an independent-hidden-state assumption. The observed position is returned only within delta of c; the latent state is never reset.

## Aged-baseline acquisition: one probe can suffice

After alignment, hold u=0 for H>2w. Measure one baseline triangular residual on [H-2w,H]. Then perform one positive ramp of duration h and hold through all nodes. Estimate Kstar(t_l) by (R_post,l-R_base)/A.

For the initial hidden force g(t)=integral exp(-lambda t)z0 dnu,

|g'(t)|<=G/(e t), t>0.

The difference between the two positive weighted averages has old-force drift at most

D_age=G(h+t_l+2w)/(e(H-2w)).

The formula uses the mean separation of the two tests, not a hidden spectral gap. The two tracking-memory terms total at most 4Bdelta. Thus with M nodes and R independently metered repetitions (R=1 allowed), uniformly with probability >=1-alpha,

|estimate-Kstar(t_l)| <= [D_age_max+4Bdelta+2b_meter]/A
 +sqrt(4 v_meter log(2M/alpha)/(R A^2)).

Here D_age_max=G_use(h+t_max+2w)/(e(H-2w)), t_max=max_i t_i<=T. For a single probe, G_use is the initial post-alignment G. For repeated aged probes, use the uniform cycle envelope Gstar. Fresh signs are optional in this aged-baseline variant. Baseline noise is shared among nodes and is already included in the variance; union bounds remain valid.

## Complete physical and computational bill

Random-sign mode: time guard+N[2h+t_max+2w], at most 2NM requested position bins of width w, 2nNM requested force bins of width w/n, N fresh signs. Position restoration is a finite reverse ramp.

Aged mode: time guard+R[H+2h+t_max+2w]. Only the last 2w of the long guard needs metering for baseline subtraction. Including the baseline, each repetition needs at most 2(M+1) requested position bins and 2n(M+1) requested force bins, plus any separately acquired prediction-initialization window. The sum of requested integration durations is 2w(M+1) per channel; overlapping windows share a continuous integrated record. Actual source occupancy includes the full R H wait. Merge all rational endpoints and accumulate cumulative meter increments; O(Mn) endpoint updates and O(M) accumulators suffice, plus O(Mn log M) scheduling, or use conservative O(M^2 n) overlapping-window bookkeeping. Pay the minimum endpoint separation/clock resolution, or round endpoints and include the timing errors proved in passive_FULL_PROOF.md. Node independence is never assumed.

Force and slew are Fmax, (15/8)A/h, (10 sqrt(3)/3)A/h^2. Trap travel is 2A per probe. Absolute stage work is bounded by 2A Fmax per probe (apart from initial stored trap energy and any moving-center preparation). Arithmetic is linear in the number of meter bins and can stream into M averaged outputs. All stiffness, calibration, quantization, readout noise, force-law evaluation precision, and bandwidth parameters must satisfy the displayed inequalities; they are not free oracles.

## Initial alignment without a hidden reset

If the trap already has center q0, choose the unique c satisfying c+V'(c)/k=q0, using the known strongly monotone force law. Let d0 bound initial |x-c|, including position measurement error. Hold q=q0. Set R0=max(d0,G/kappa), Gprep=G+2B R0. The maximum principle gives |x-c|<=R0 and therefore

|x(t)-c|<=d0 exp(-kappa t)+Gprep/kappa.

To reach delta0>Gprep/kappa, take t_guard>=(1/kappa)max(0,log[d0/(delta0-Gprep/kappa)]). At guard end, bath energy is at most (sqrt(2E0)+2sqrt(B)R0)^2/2, so use Gprep in the acquisition formulas. The guard force bound |V'(c)|+kR0 is paid explicitly and must fit the hardware cap. No lambda-dependent mixing or microscopic reset occurs. Numerical solution error for c is another calibrated actuator/reference error, not exact root-finding access.

## Arbitrary-node handoff correction

The observation starts are the fitter's arbitrary rational times, not a w-spaced lattice. The triangle width w and the maximum fitting mesh gap Delta are separate parameters. If endpoints 0,T are observed, a monotonicity-only final certificate is ||K-Khat||_1<=B(h/2+w)+2B Delta+T(eta_acq+eta_fit). For cumulative-meter implementation, precision errors epsilon_Yf,epsilon_Yx yield residual error <=2epsilon_Yf/w+4epsilon_Yx/w^2; this replaces the per-average epsilon_f+2epsilon_x/w allowance.
