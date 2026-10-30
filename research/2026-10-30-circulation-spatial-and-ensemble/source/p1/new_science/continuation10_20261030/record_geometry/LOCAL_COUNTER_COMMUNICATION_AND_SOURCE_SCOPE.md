# Local counter communication and source scope

**Status.** Conditional sensing/communication schedule for the delayed queue. The jump case closes at the displayed detector and logical-channel interfaces. The finite-duration interacting extension has an additional energy envelope. No equilibrium data supply these operations automatically.

## 1. Synchronized snapshots before causal collection

At declared times \(t_m\), local detectors sample and hold their cumulative signed counts. Actual sample times differ from \(t_m\) by at most a fixed \(\delta_s=O(1)\). Collection and broadcast take \(O(N)\) time but do not change these timestamps. Clock preparation, synchronization, distribution and reliability are charged. A bounded-speed graph does not itself supply synchronized clocks.

Reading running counters successively along a traveling message is different: \(O(N)\)-separated timestamps can destroy the cancellation that gives an \(O(1)\) total background drift. The held-count protocol avoids that inference. It combines

\[
\widehat E_1=\widehat A_1+(\widehat B_1-\widehat B_2)/2,
\qquad \widehat E_2=\widehat A_2-(\widehat B_1-\widehat B_2)/2.
\]

The factor \(1/2\) is exact fixed-point arithmetic. Commands take effect at a declared later boundary. Snapshot-to-use delay, force ramps and the maximum age before the next update all enter \(D_N\). Epoch spacing \(CN\) gives \(D_N=O(N)\) with the supplied communication primitive below.

## 2. Finite-response jump-current pickup

A sufficient local pickup at an oriented section, with signed crossing count \(Q_i\), is

\[
\tau_sdr_i=-r_i\,dt+dQ_i,\qquad dC_i=r_i\,dt,
\qquad r_i(0)=C_i(0)=0.
\]

Thus \(C_i(t)=Q_i(t)-\tau_sr_i(t)\). The response time \(\tau_s>0\) is fixed. Noisy differences of readings are not repeatedly accumulated. This interface supplies linear response, dynamic range, noninvasive pickup and a reliable stored integral. It is not a claim that every finite-bandwidth detector does so.

Read the held integral with centered independent Gaussian errors of uniformly bounded variance, then quantize at resolution \(q_N\). A uniform conditional joint sub-Gaussian bound can replace independence. Reading does not corrupt the stored integral. Overflow is detected rather than wrapped.

For the bounded-rate background and independent walkers, total absolute crossing activity has conditional intensity at most \(CN\), since \(R_N=o(N)\). Separate tracks have \(O(NR_N)\) detector positions but only \(R_N\) added moving charges. Whole-horizon activity is Poisson-dominated with mean \(O(N^3)\); range \(N^5\) overflows only superexponentially rarely at speed \(N\).

Sum the absolute pickup errors and split the exponential filter convolution at a sufficiently large multiple of \(\log N\). The old tail is at most \(N^{-2}\) times total activity. The recent part is dominated by activity in an \(O(\log N)\) window. Poisson exponential moments and a polynomial union over epochs give

\[
\Pr\{\max_m\sum_i|\tau_sr_i(t_m)|>N^{3/2}\}
\leq\operatorname{poly}(N)e^{-cN^{3/2}\log N}.
\tag{1}
\]

The same bound holds for individually skewed times in the fixed snapshot window. The additional count discrepancy is at most total absolute activity in a fixed-width window about each epoch. Timing is therefore controlled by actual activity, not inferred from small aggregate drift.

With \(O(NR_N)\) readouts, aggregate noise variance is \(O(NR_N)\), so

\[
\Pr\{\max_m|\text{aggregate read noise}|>N^{3/2}\}
\leq\operatorname{poly}(N)e^{-cN^2/R_N}.
\tag{2}
\]

This is superexponential at speed \(N\). Unit quantization contributes at most \(O(NR_N)=o(N^2)\), enough for tracking. For rare arming at \(N^{3/2}\log N\), take \(q_N=1/N\): deterministic quantization error becomes \(O(R_N)\), and (1)--(2) are negligible on the arming threshold. Extra converter resolution is charged; it still needs only \(O(\log N)\) bits over the specified range. Read noise remains order one per detector: fine quantization does not claim noiseless analog precision.

Thus the queue receives an \(o(N^2)\) observation envelope with superexponentially small failure, before adding the separate communication error. One shared lane with \(O(N)\) pickups has a smaller burden.

## 3. Bit-serial local addition and broadcast

On the no-overflow event each held value fits in \(w_N=O(\log N)\) bits. A nearest-neighbor chain adds words least-significant-bit first. Each node keeps one carry, combines its local word bit with the incoming prefix bit, and emits the next prefix bit after a fixed logical step. With fixed-width sign extension and enough high bits reserved for the final sum, the entire sum arrives after \(O(N+w_N)\) time. Word bits stream while the pipeline advances; the latency is not \(O(Nw_N)\).

For separate tracks, first combine their \(R_N\) held words at each longitudinal site through a local bounded-degree transverse chain. This takes \(O(R_N+w_N)\), followed by the longitudinal chain. Since \(R_N=o(N)\), collection still takes \(O(N)\). It uses \(O(NR_N\log N)\) memory and bit transmissions per snapshot, up to fixed architecture factors. A single shared physical lane instead needs \(O(N\log N)\).

Broadcast epoch-tagged commands back locally in \(O(N+R_N)\) time. They retain the original snapshot timestamp and specify a future actuation boundary. On the \(TN^2\) horizon there are \(O(N)\) epochs. The separate-track implementation therefore uses \(O(N^2R_N\log N)\) bit operations, besides \(O(NR_N)\) actual track hardware. Clock distribution, sensing and source preparations are additional.

The algorithm presumes an actually supplied reliable logical primitive: either exact operations in the declared model, or a whole-horizon corruption probability superexponentially small at speed \(N\). Finite bandwidth alone does not imply that reliability. Fixed per-word or per-bit error cannot be dropped. A noisy implementation must pay for its actual coding, recovery, protected logic or energy barriers and verify both error and delay. The queue theorem uses the resulting \(D_N\); this tradeoff has not been solved for free.

## 4. Finite-duration interacting carriers: local readout extension

The exact center-of-mass supplier permits arbitrary relative energy; that alone does not bound skewed local readings. The following additional envelope closes this particular detector implementation without identifying the interaction. Let

\[
\mathcal E_{\rm rel}
=U-\inf U+\tfrac12\sum_l(V_l-P/R_N)^2
+\tfrac12\sum_l(Y_l-Y/R_N)^2.
\tag{3}
\]

Require \(\mathcal E_{\rm rel}(0)\leq C R_NN^2\), except on a superexponentially rare event. This is a weak but real preparation/interaction bound. For example a uniformly bounded pair-potential range \(O(R_N^2)\), arbitrary initial positions, and the supplied Gaussian velocities and thermal coordinates satisfy it for \(R_N=o(N)\). An arbitrary unknown interaction of unbounded scale need not.

Common forces cancel from the relative equations. During transport, (3) is conserved. During a bath exchange its increase is at most half the squared norm of the incoming Gaussian coordinates; the same bound covers the intermediate rotation by retaining the incoming-coordinate energy. Consequently, on \(O(N^2)\) periods,

\[
\sup_t\mathcal E_{\rm rel}(t)
\leq\mathcal E_{\rm rel}(0)+\tfrac12\sum_k\|\xi_k\|^2.
\tag{4}
\]

Chi-square concentration bounds the right side by \(C_TR_NN^2\), except with probability at most \(e^{-cR_NN^2}\), after changing constants. Combine this with the supplier's exact aggregate-momentum bound to obtain

\[
\sup_{t\leq TN^2}\sum_l|V_l(t)|
\leq |P(t)|+\sqrt{2R_N\mathcal E_{\rm rel}(t)}
\leq C_TR_NN
\tag{5}
\]

outside a superexponentially rare event. This bound is deliberately coarse; no hidden relative mixing is used.

Put local pickups at the \(N\) lattice sections of the physical continuous ring. If \(Q_i\) counts actual signed crossings of section \(i\), then

\[
\left|\sum_iQ_i(t)-\sum_l[X_l(t)-X_l(0)]\right|\leq R_N.
\tag{6}
\]

Indeed each particle's summed crossing count is the change of its integer part. The bounded remainder is actual fractional displacement, not discarded transport.

For one particle and an interval \(I\), the sum over sections of the maximum absolute net crossing count from a fixed time in \(I\) is at most \(1+\int_I|V_l|dt\). To see this, bound each section's net crossings by the difference between its integer crossing indices at the maximum and minimum unwrapped positions; summing those differences telescopes to the change of the ordinary integer part. This also controls rapid back-and-forth motion, without counting every oscillation as irreversible flow. Summing over particles and using (5) bounds skewed-count errors over fixed-width windows by \(O(R_NN)\).

Applying the same net-interval bound inside the exponential filter convolution gives total absolute pickup error \(O(R_NN)\). Thus bounded skew, finite pickup response and the crossing/displacement conversion together contribute \(O(R_NN)=o(N^2)\). Gaussian read errors and quantization are as above, now with only \(O(N)\) fixed pickups. Whole-horizon counter magnitudes are at most \(O(R_NN^3)\) on the energy event, so the same polynomial register range suffices.

This closes the queue's observation envelope for tracking. It does not automatically close a much smaller rare-arming threshold: the coarse \(R_NN\) error must also be smaller than that threshold, or a sharper detector/energy argument is needed. For example \(R_N=\lceil N^{1/3}\rceil\), \(a_N=N^{-1/6}\) simultaneously gives \(R_Na_N\to\infty\), \(R_N/N\to0\), \(O(N)\) delay, and \(R_NN=o(N^{3/2}\log N)\). Exact synchronized summed pickup is another, stronger timing interface because the relative currents then cancel in the sum. No such exact synchrony is inferred from bounded skew.

## 5. Supplied function evaluation and resource boundary

For the root's nonlinear cumulative-current target, synchronized held native counts can feed a fixed function evaluator. Its actual error and execution time must enter the same observation envelope and delay. Merely specifying an arbitrary mathematical \(C^2\) map does not make it a computable physical operation. Explicit polynomial, trigonometric or other supplied finite-precision evaluators are straightforward examples at their paid runtime/precision interface.

The finite-rate walker implementation and the finite-duration interacting implementation remain distinct. The former uses a point-process rate contract and, on separate tracks, larger track/sensing hardware. The latter uses local finite-frequency rotations and \(O(R_NN^2)\) fresh thermal preparations, plus the present energy envelope when this skew-tolerant detector is used. Neither construction establishes a practical speedup or a complete apparatus cost advantage. Current-error regulation itself has the direct Brandes and Wagner predecessors cited in the supplier file.
