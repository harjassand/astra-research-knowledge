# Finite-LO receiving: exact instrument closure, not a detector construction

31 October 2026. Author continuation, not yet independently reviewed. This material is OUTSIDE the accepted qualified bus package. It consumes the separately accepted beta=8 vacuum bus/filter model. The root candidate `FINITE_LO_ERASER_ROOT_CANDIDATE.md` is reproduced unchanged (SHA256 1afefa1ad8bffd4f9a922e7a562ac0c8a437ccaca61ab2b049e8fcfd59f3581b). The mechanism is ordinary weak-field homodyne with photon-number-resolving detection, not a new erasure principle.

## 1. Exact finite optical instrument

The accessible signal is the single-mode coherent state |b sqrt(S)> for b in {-2,0,2}. Introduce |i sqrt(n_LO)> in exactly the same mode and mix on a balanced beam splitter, with output amplitudes (b sqrt(S) +/- i sqrt(n_LO))/sqrt(2). Both output modes are photon-number measured. For counts (m,n), the phase of the diagonal Kraus amplitude is

    (m-n)pi/2 - (m-n)b theta,
    theta=atan(2sqrt(S/n_LO))/2.

This identity is exact on those three B eigenvalues. Applying exp[i(m-n)theta B] is two local Z rotations. It removes that phase but not the total-count information about B². Summing the positive corrected amplitudes gives the exact adjacent-sector factor

    v=exp[-(sqrt(n_LO+4S)-sqrt(n_LO))²/2],

while the +2/-2 factor is one. With lost vacuum signal energy ell, the three-sector kernel has adjacent value t=exp(-2ell)v and extreme value d=exp(-8ell). The already-proved Schur-channel diamond calculation applies with w=1-t and q=1-d:

    error=q                     if q>=2w  (equivalently 2t>=1+d),
          4w²/(4w-q)            otherwise.

No infinite local oscillator or ideal quadrature projection is used. In the first branch it equals the unrestricted post-gate minimax lower bound from the lost extreme-pair coherence. Perfect erasure is not obtained at finite n_LO and zero lost energy, except in trivial zero-signal cases. For general B with additional distinct eigenvalues, atan(b sqrt(S/n_LO)) is not linear in b; the same local correction does not apply.

## 2. Constant unequal detector efficiencies are receivable

Let signal/LO amplitudes *before* detector loss be A0,L0, both real, and let the two output efficiencies be eta_+,eta_-. Assume ordinary mode-independent passive attenuation, no dark counts or number misassignment, and the same temporal mode in both arms. Put eta_bar=(eta_++eta_-)/2. The observed positive-amplitude kernel is the preceding formula with

    S=eta_bar A0², n_LO=eta_bar L0²,

and lost signal energy is (1-eta_bar)A0² plus previously uncollected signal. Unequal attenuation also produces a deterministic local-B phase

    chi_loss=A0 L0 (eta_+-eta_-)/2.

This follows directly by taking the coherent-state overlap of both lost output modes. Their imaginary overlap is chi_loss(b-c), while their real distinguishability depends only on eta_bar. Pay the additional correction exp(-i chi_loss B). The count-difference angle is unchanged because S/n_LO=A0²/L0². This result does NOT receive mode-dependent losses, detector phase shifts, drifting imbalance, correlations, dark counts or a generic uncalibrated instrument. Symmetry cannot substitute for their actual instrument.

## 3. Finite counter and local controls

Require the actual number instrument to agree with the declared instrument on all true outcomes m+n<=M. On overflow any stated fallback correction is allowed; there is no postselection. Total count is Poisson with branch mean n_LO+b²S, so uniformly over arbitrary data/reference input its overflow probability is at most the Poisson tail at lambda_max=n_LO+4S. For lambda_max<M+2,

    p_over <= exp(-lambda_max) lambda_max^(M+1)/(M+1)!
              /[1-lambda_max/(M+2)].

The first tail term times a geometric series bounds the tail. Changing the conditional correction only on overflow costs at most 2 p_over in complete norm: the two bad-outcome CP maps each have trace bounded by p_over on every input. This is not a claim that a saturated physical detector is automatically faithful below M.

The certificate chooses M=20, a *total* count cap. This is conservative for two detectors each able to report 0 through 20. It constructs a finite table of 41 local correction angles for count difference -20,...,20, wrapped modulo pi. Exact arithmetic bounds the table-computation error below 1e-8 radians. The physical local controls must deliver each requested qubit phase within 1e-6 radians, contributing <=4e-6 in complete norm. Duration remains tau_Z=0.01 and required coefficient is at most pi/(2tau_Z), as in the accepted bus. This is an actual local correction, not a free frame for later noncommuting gates.

The new budget adds a finite PNR readout/decision latency of **one normalized time unit** before those corrections. Continuing dephasing gamma=0.0001 per qubit is charged through that latency. The old ideal-homodyne ADC and Gaussian-saturation terms are removed, not counted as evidence for this different instrument. The remaining 0.001 complete-error allowance is still an explicit SUPPLIED bound; it must jointly cover force/optical calibration, LO preparation and phase, number misassignment, other controls and residual couplings. For example an arbitrary number-misassignment probability epsilon_num uniformly bounded per operation contributes at most 2 epsilon_num, but no such probability was experimentally acquired here.

The LO mean quoted in the certificate is observed mean after loss. With equal efficiency .999 the input LO energy is greater by 1/.999, with further preparation/filter losses paid separately. Its actual phase and temporal/spectral/polarization mode relative to the signal are supplied calibration. The optical filter and finite readout window are those of the accepted bus; their unobserved signal tail is already in ell. Both number detectors must implement the stated finite-window instrument. A slow calorimeter which cannot distinguish late photons does not automatically implement it. A smooth LO can continue to ring down after the observation window, but detector recovery and late-photon contamination of later service calls still need receiving. The earlier ideal-homodyne warm-apparatus theorem is NOT inherited by this finite coherent-signal construction.

## 4. Exact numerical receiving, with failures retained

The imported accepted certificate supplies at beta=8

    S about 0.07805864803433685,
    ell about 0.00048116830540799.

The exact new grid uses observed LO means {1,2,3,4,6,7,8,13,16}, M=20, the extra unit readout latency, physical local-angle tolerance 1e-6, and the same remaining 0.001 allowance. All pi, square roots, exponentials, Poisson-tail bounds and correction-table angles are enclosed using rational/dyadic arithmetic. The controlling code is `certify_finite_lo.py`; imported `accepted_certify_bus.py` is a byte-identical copy of the previously accepted certifier.

At mean **4 LO photons**, exact complete-error upper is **0.009134838999948075**. It is below the target 0.01 with finite LO, finite count range, finite readout time, bounded local correction and continuing declared data noise. Means 1 and 2 fail because finite-LO B² information is too large. Means 13 and 16 reach the old lost-field minimax in the ideal unbounded counter but fail this M=20 service because overflow is too frequent. Mean 3 passes narrowly; it is not a robust hardware recommendation.

Thus “make the LO large enough to recover the homodyne optimum” is not the best ordinary receiver choice under a finite counter. A weaker finite LO can satisfy the actual gate target with much less dynamic range. This closes a mathematical ideal-measurement limit, not the harder physical high-efficiency detector service.

## 5. Why binary click detection is not the same service

For comparison, split the same two coherent output pulses into N equal-energy bins, give each bin an ideal on/off detector, and use one phase increment per reported click. No-click and click overlap factors are respectively c0 and c0(exp(h)-1), with

    c0=exp[-(lambda_b+lambda_c)/(4N)],
    h=[bc S+n_LO+i(c-b)sqrt(S n_LO)]/(2N).

After the one-click phase correction, the two ports give the exact factor

    K_click(b,c)=|c0[1+exp(i theta(b-c))(exp(h)-1)]|^(2N).

Multiply the independent lost-signal overlap afterward. This diagnostic models an actual ideal on/off-bin instrument, not a faithful number measurement. It loses the unknown extra phase increments of multiple photons in a bin. Equal-energy bins require their own timing or spatial multiplexing and rearming; fixed-duration bins generally have unequal energy. Using only the mean photon count cannot certify a detector bandwidth.

The diagnostic at mean4 illustrates the distinction: N=512 gives bus-only error about 0.006056, while N=1024 gives about 0.005600; adding the stated other/readout costs leaves the former above and the latter below 0.01. These are floating checks of this stipulated bucket model, not a physical lower bound on detector speed or a claim that these bins have been built. The simpler collision bound 2p_collision<=lambda_max²/(2N) is valid but much looser. An ordinary calibrated number-resolving calorimeter uses another physical resource instead of simulating every photon-time event.

## 6. Primary precedent and stopping boundary

[Thekkadath et al., Phys. Rev. A 101, 031801 (2020)](https://arxiv.org/html/1908.04765) already implement weak-field homodyne using balanced mixing and two photon-number-resolving TES detectors. Their intrinsic detector range/efficiency, total optical-system efficiency, mode overlap and readout cadence are distinct quantities: reported system efficiencies around .274/.354 are far below the .999 stipulated here, and the experiment uses 10-microsecond acquisition windows. No reported performance is transplanted into this gate budget. Under the simple constant-loss model with average efficiency .314 and this same bus/filter, lost-field distinguishability alone gives a gate-error lower bound above .35, regardless of LO strength or decoder. The cited hardware is precedent for the measurement type, not evidence that our high-efficiency reliable-observation service exists.

The strong ordinary construction has now removed both a full trajectory record and an infinite-LO requirement. Remaining consequential work is acquiring the actual low-loss, calibrated, mode-matched interaction/observation/control service—or using an ordinary architecture that avoids it. Tunably suppressing bus loss during a closed trajectory, coherently reusing the emitted field, encoded operation, squeezed input, or variable-B/multi-mode gates alter resources and must be compared fairly. None is excluded by the restricted fixed-B lower bound. There is no reason to keep refining this receiver fixture unless a physical platform makes its unobserved loss unavoidable and supplies the requisite force. The next selection should identify that necessary physical operation, not append another abstract source class.
