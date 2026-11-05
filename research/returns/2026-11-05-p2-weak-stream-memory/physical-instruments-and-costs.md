# Physical candidate instruments, exact final readout and paid implementation costs

The supplied [pure-initialized construction/status](package/schur/PURE_BASELINE_AND_FINAL_STATUS.md) and [fusion theory](package/schur/FUSION_THEORY.md) specify physical growing-spin instruments for the [fixed weak stream](README.md). Receiver memory is an auxiliary qubit times a spin irrep, retaining adjacent-spin coherence plus classical outcomes. Small invariant matrices describe each known policy/history; this is not a simulation or compression theorem for an arbitrary 43,462-qubit output state.

The pure version starts in an invariant singlet, mixes the two total-spin multiplicity copies with a covariant unitary and measures a branch while retaining its quantum spin representation. A tested policy spends its initial purity to retain the first two outputs exactly, then loses most of the recoverable information. At `theta=.3`, N=600, one stored history has optimal final entanglement fidelity `.48206991236142`, while the full-bath decoder exceeds `.99`. This is a **conditional-history diagnostic**, not an averaged policy theorem or a no-go for initialized/nonmyopic receivers. [Actual history receipt](package/schur/pure_adaptive_theta0.3_N600_seed1729_joint_firstupper.json), [other policy receipts](package/online/adaptive_fusion_optimal_0p3_600_20.json).

The immediate pinching-loss minimizer and pure-state policy use the known channel/history, not a measurement of the hidden arbitrary input. Numerical local policy optimization is not certified global or horizon-optimal. Large-spin rotor diagnostics lack the required physical intertwiner; ordinary integrable fusion requires spectral shifts absent from the fixed homogeneous real-angle source. Coherent flags have separate [unresolved recovery/compression steps](virtual-statistics.md).

## Exact optimal final decoder for the declared spin memory

The [readout theorem](package/schur/OPTIMAL_SPIN_READOUT.md) removes final-decoder approximation for a covariant channel into `C^2 tensor Q_J`. For J>=1, its time-reversed invariant Choi blocks are scalars a,c on total spins J-1,J+1 and a positive 2x2 block B on spin J, with normalization `(2J-1)a+(2J+1)Tr(B)+(2J+3)c=1`. Put `d_-=2J`, `d_+=2J+2`. The all-decoder optimum is

```text
F_opt=(1/2) max_(0<=x,y<=1) {
 d_- a(1-x)+d_+ c(1-y)+d_- B_-- x+d_+ B_++ y
 +2sqrt(d_- d_+)|B_-+|sqrt(xy) },
epsilon_opt=1-F_opt.
```

At most six elementary corner/edge evaluations suffice, with separate J=0,1/2 rules in the proof. For an unnormalized classical history it returns probability-weighted fidelity; sum histories before taking one minus fidelity. The explicit coherent CG dilation retains the relative phase between memory sectors rather than measuring it, uses logarithmic initialized work space and finite-precision rotations, and pays discarded environment, calibration, protection and implementation error. Acquisition-model error eta and decoder error delta add to `1-F_opt`. This is an attained final-readout operation for the declared memory state, not an attained acquisition policy. [48-state finite decoder checks](package/schur/covariant_spin_readout_receipt.json).

## All-output benchmark and physical routing

The accepted all-output operation has N inverse interactions before routing. In its **specified fixed-junction nearest-neighbour layout**, capture requires `R_c=N(N-1)/2` routing swaps and decode `R_d=N-1`. Including source and inverse encounters, `G=2N+R_c+R_d=(N^2+5N-2)/2`; N=43,462 gives 944,581,376 counted gates. Collection alone costs 944,450,991 encounter-intervals of qubit-time. These are layout bills, not universal lower bounds.

For source encounter time tau_s, inverse time tau_d, routing time tau_w and control interval tau_ctl,

```text
T_capture=N tau_s+R_c tau_w+(N+R_c)tau_ctl,
T_decode=N tau_d+(N-1)tau_w+(2N-1)tau_ctl.
```

The N+2 operating cells, factory initialization, inaccessible tracial preparation records, reset, protection over those times, calibration and accumulated gate error remain paid. The ideal `.1`, one-percent point leaves almost no implementation margin. Reserving half that error budget for the ideal channel gives N=50,440 and 1,272,222,899 gates in this layout; no protected hardware/factory was simulated.

For a compressed spin proposal the internal encoded register may be logarithmic, but an update of compiled depth G_step at local clock Omega_R needs service time of order `G_step/Omega_R`. Faster arrivals create an additional coherent carrier backlog. Delaying acquisition avoids it only if the source interface permits the delay, with wall time/protection charged. Small internal matrices do not erase physical buffering or gate work.

A direct source full SWAP is simpler if action pi/2 is actually available; the stipulated weak encounter does not provide it. Strong receiver controls after emission cannot extend that earlier source encounter. Standard Schur/CG, pure-family coherent gathering, mixed-i.i.d. and integrable machinery remain credited at their premises. [Complete TeX report](package/weak_stream_memory.tex), [original package/hashes](SOURCES.json). No new Capital execution, compilation or audit occurred; the general acquired memory/processing endpoint remains unresolved.
