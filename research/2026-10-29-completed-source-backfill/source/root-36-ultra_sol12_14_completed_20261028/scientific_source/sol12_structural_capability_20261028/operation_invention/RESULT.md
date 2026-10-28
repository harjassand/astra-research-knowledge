# Bounded operation result

**A conditional trace measurement without pose reconstruction was constructed and executed. Its ordinary Fourier comparator has identical information and noise. A finite-conductivity shortcut to enclosed-void certification was refuted, while its material-volume inequality survives. No practical powder capability or generic inference advantage was acquired.**

## Desired action

Acquire a covered upper bound on trace(polarizability)/mass for one moving, rotating conducting particle, without resolving its pose across fixed sign exposures. This could feed the existing one-sided closed-void certificate for manufacturing powder.

The selection used current task-first Astra source revision 8d51d60762b3ee28c10aaaa56e1b92da119dc1cc and T-powder-closed-void. The source already contains scalar Maxwell trace fields and an exact finite-body four-sign projection. Those were preserved as inputs rather than reintroduced as discoveries.

## Constructed and executed

Three uniform/gradient carrier pairs share difference frequency 17, with gradient frequencies 101, 173, 257 and uniform frequencies 118, 190, 274 per observation interval. Under a common instantaneous tensor law, exact periodic coefficient bandwidth 9, and the specified affine field model, their matched sideband is proportional to the trace even during unknown rotation. Charge, permanent dipole, arbitrary gradient response and supplied translation terms were included.

On 4096 samples with three complete rotations and true trace 7:

| Calculation | Result |
|---|---:|
| Common-beat receiver | 7.000000000000002 |
| Ordinary least-squares Fourier receiver | 6.999999999999999 |
| Equal carrier traces 7 with deliberately different tensors | 18 |
| Naive shortened-window receiver, real part | 6.995056681 |
| Ordinary full nuisance regression on that window | 6.999999999999992 |
| Added target-band nuisance .1 cos(Omega t) | 7.2 |

The ordinary methods receive identical samples, support promises and timestamps. On a coherent window the target statistic and noise are exactly the same. On the shortened window, equally informed ordinary regression corrects the leakage. Generic frequency mixing and lock-in detection are established prior methods; [Borgani et al.](https://arxiv.org/html/1408.5285) is a primary example.

This is an algebraic extension of the source's scalar trace basis to a supplied moving-coefficient model. It does not acquire common carrier response, exact bandwidth, sensor transfer, real kinematics or an electrode design. The simulated coefficient tensors have not all been realized by one physical body.

## A sharp restriction on the attempted material rescue

For homogeneous pure Ohmic susceptibility chi=i/tau, the exact depolarization spectral mass and first moment give
\[
 \operatorname{tr}(\Re\alpha+6\tau\Im\alpha)
 \ge9\epsilon_0 V_{\rm metal}.
\]
The right volume is metal, not the region filled across closed cavities. This valid inequality therefore cannot replace the physical-to-perfect-conductor premise of the void receiver.

An exact spherical-shell boundary calculation makes the distinction quantitative. At metal fraction 10^-6 and tau=.01, true void fraction is 0.999999. The measured loss-corrected response divided by the solid PEC mass scale is 1.444993969, which would give the invalid upper void estimate 0.307955589 if substituted into the static formula.

A connected smooth continuum family strengthens the restriction at the actual 1% gate: attach a closed, vanishing-metal balloon to a solid ball through a smooth thin neck. The full polarization equation and reciprocity give a response perturbation bounded by 9 epsilon_0 b V_S, linear in added metal volume. For tau=.01 and V_S/V_0<=10^-5, the normalized witness is at most 1.004079191<100/99 while the actual void remains at least 0.499995. Finite collections of finite-frequency dipole tensors converge to the ball's as well. Exact mass can be matched by dilation. A separate more conservative square-root bound and its exact numerical control are retained.

This family spends arbitrarily small geometry. For 15 micrometre radii, the sharper displayed volume ratio implies a wall scale about 50 pm, before accounting for the neck. A connected continuum film at atomic scale, and the contrast b=100 at actual powder measurement frequencies, are not physically qualified. This is not a manufacturing counterexample or a practical powder impossibility theorem. It proves that no uniform finite-contrast shortcut over the unqualified continuum class can dispense with a quantitative material/geometry/relaxation premise.

## Charged costs and status

The common-beat construction uses six calibrated carrier drives and signed, time-resolved sensing. At the same quadratic field budgets as the source's equal-time fields, a supplied nominal Al PEC sphere has target acceleration amplitude 9.838 m/s^2. In a 1 ms observation, the beat is 17 kHz and its displacement amplitude is only 0.862 nm. The source's illustrative 0.046% random-error target would require about 18 pm independent position noise per sample under a simplified known-phase model with 4096 samples. At 10 ms, those conditional scales are 1.7 kHz, 86.2 nm and 1.80 nm. Photon rate, colored noise, initial-motion regression, material response, drive peaks and coverage were not acquired.

Computation used the existing local Python environment. The sideband calculation, including the 729-column ordinary nuisance regression, took about 0.11 s; the exact shell, reciprocal identity and bound arithmetic took about 0.18 s. Timings are local receipts, not physical measurement costs or general algorithmic speedups.

| Claim | Status |
|---|---|
| Conditional pose-independent trace encoding | CONSTRUCTED; executed supplied-model control |
| Generic new heterodyne method or priority clearance | NOT_CLAIMED; priority UNKNOWN |
| Advantage over equally informed ordinary regression | NOT_ESTABLISHED; identical coherent statistic |
| Loss-corrected material-volume lower bound | PROVED in the specified Ohmic continuum model |
| Filled-volume substitution or 1% rescue over arbitrary continuum geometry | REFUTED |
| Physical per-particle response/bandwidth/geometry admission | NOT_ACQUIRED |
| Practical powder device, useful yield, industrial coverage or throughput | NOT_ACHIEVED |

Proofs: PROOF.md and FAILED_LOSS_BRIDGE.md. Executed inputs and outputs: code/ and results/. Acquisition, comparator and physical cost boundaries: COSTS_AND_REPLAY.md. The old conditional PEC certificate and its existing device limitations remain unchanged.

Internal review: root whole-read the original proofs and independently reconstructed the strengthened bilinear-reciprocity bound, accepting those mathematical scopes. It did not replay the numeric controls or a boundary mesh. REVIEW_RECEIPT.md preserves the precise acceptance and physical limits.
