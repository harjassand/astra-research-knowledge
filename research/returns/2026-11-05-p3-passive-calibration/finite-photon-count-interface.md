# Finite local-oscillator photon counting, detector service and timestamp costs

This supplies the actual classical optical operation used by [passive Hamiltonian calibration](README.md). Read the preferred [matched-LO proof](package/next2_continuous_quantum/OUTPUT_ONLY_CLASSICAL_CALIBRATION.md), [independent implementation review](package/next2_alternatives/finite_lo_implementation_review.txt), [timing/scope addendum](package/next2_root/TIMING_AND_SCOPE_ADDENDUM.txt) and [general finite-LO derivation](package/next2_root/finite_lo_photocount_acquisition.txt). Earlier conservative formulas in the last file are preserved; they are not substituted for the final evaluated allocation.

## Actual measurement and all-outcome variance

After known balanced loss, mix each actual Pauli output with a finite coherent oscillator and count both arms. For detected LO photons mu in a window, the integrated difference D has exact finite-LO mean `E[D/sqrt(mu)]=X_matched` and second moment `E[D^2/mu]=X_matched^2+N_total/mu`. N_total includes **all** signal temporal modes, not only one fictitiously stored mode. No infinite-oscillator or temporal-mode storage primitive is assumed.

Preferred matching sets `q=rw`, `mu=kappa q/4`, `R=kappa r/2` and mean total window count `m=Rw`. Signed jumps are the calibrated Pauli projectors, and `D/m` has the normalized quadrature mean. Products on s distinct physical ports have conditional second moment at most `(1+1/m)^s`; the forward/reverse odd average retains that bound without claiming those products independent. Empty windows are observed. Counter clipping returns zero locally when a selected total exceeds K, with Poisson tails paid. Unrelated-port overflow does not throw away an entire shared block.

The LO photon **rate** is finite and independent of window width in the matched schedule. Continuous illumination through paid source burn-in avoids an instantaneous switch but pays `3n kappa r T_wall/4` detected LO photons; incident photons additionally pay actual LO attenuation. Gating is an alternative only with real ramps, slew, service and ramp-photon costs. Parallel observation pays O(n) optical channels and classical processing, not a fixed aggregate optical interface.

## Fixed deadtime and growing detector arrays

Split each mixed arm into L equal labelled detector rails. The service model has bounded recovery deadtime d0, missed-count-only error, no unbudgeted afterpulsing/crosstalk or source feedback, and calibrated efficiencies. Same-rail predecessor pairs give `E C<=R^2(w+d0)d0/L`; the predecessor interval before the window matters even with continuous illumination. An initial guard removes arbitrary initial detector blindness.

Compare **unclipped** products first. Missed-count/product telescoping gives mean bias at most `s R d0(1+d0/w)/L`, avoiding the old unnecessary clipped-amplitude multiplier. Clip actual observed totals afterward and allocate the independent overflow budget. Detector hardware, optical routing, real propagation and recovery are paid. This construction treats busy time; it is not an exactly calibrated arbitrary response-filter inverse.

## Timestamp precision remains a different resource

If every actual window endpoint differs by at most tau, its normalized kernel differs in L1 by at most `2tau/w`. Tensor telescoping bounds the response bias by `2s(tau/w)(1+2tau/w)^(s-1)`, at most `4s tau/w` in the allocated regime. Apply this before clipping and budget counter tails separately. The joint timing/deadtime formula includes the enlarged incident window and its cross term, as specified in the addendum.

Timing offsets must be source/count-mark independent and bounded, or come with the admitted deterministic bound; arbitrary outcome-dependent timing is not covered. Constant calibrated propagation delay shifts labels; residual uncertainty, actual path length, LO envelope coverage and all ramp photons remain costs. Pad the source discard interval so its promised burn precedes the earliest accepted true event.

A detector array does **not** create accurate timestamps from a fixed unknown latency/jitter floor. A direct clock pays frequency of order `1/tau`, bits of order `log(T_total/tau)` and detector latency/bandwidth supporting that precision. Further service/reference calibration can add accuracy-dependent work. The inverse-square statistical exposure comparison is not a claim of optimal total hardware or a fixed-bandwidth device.

Unmixed intensity can estimate r only with known efficiency and paid Poisson exposure. Unknown r and unknown kappa cannot be separated from those counts alone, and intensity does not certify Pauli operators, phases, pure vacuum inputs or model completeness. Actual filter distortion, phase/gain/loss drift and correlated background need response-bias allowances.

This classical calibration permits known nonzero loss. It does not acquire an arbitrary quantum payload through its count record or weaken the [first-ingress loss converse](../2026-11-05-p1-bounded-component-acquisition/loss-and-spectral-access.md). Deferred recovery retains the coherent archive, its ingress and protected waiting. Original event-driven simulations on the [main page](README.md) omit the physical service models; no new Capital program, hardware experiment or audit was run. [Original package and hashes](SOURCES.json).
