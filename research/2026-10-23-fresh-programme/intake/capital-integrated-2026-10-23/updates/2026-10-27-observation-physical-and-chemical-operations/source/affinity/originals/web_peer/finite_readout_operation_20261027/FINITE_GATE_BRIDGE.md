# Exact finite gate bridge, and why it is not yet a useful new instrument

This is a conditional finite readout construction, not physical acquisition. It removes one real mathematical gap from the previous infinite-frequency argument. It does not make the full readout/independence contracts free.

## Required experiment/record contract

1. A joint physical record has T synchronized samples of definite-parity observables. Its initial observation/noise map commutes with physical record reversal. Memoryless static measurement with reversal-compatible noise is sufficient; spatially correlated noise can qualify. A known symmetric exposure can also be part of this map. Unknown history-dependent localization is not granted this property.
2. A controlled gate sets that observation sequence to zero outside the T-sample window **before every unknown temporal channel filter**. Ordinary cropping after the filter does not qualify. The gate is common/synchronized and symmetric under reversal of the physical window.
3. Channel i has an unknown real causal FIR h_i of length at most L+1, fixed across trials. Capture all T+L output samples, including the tail. Initial filter state is zero. An IIR analogue needs an acquired initial-state/tail envelope; a finite settling interval is not exact merely because it is long.
4. Noise produced after the unknown filter is absent or transported by an acquired full error/reversal contract. It cannot silently be moved to the input. Genuine independent physical trials require an acquired preparation/return law and its actual time, energy and failure cost.

Choose a DFT length M>=T+L and pad the captured sequences with zeros. Because the complete gated linear convolution is captured, at every DFT bin

`Y_i^r(m)=H_i(m) Z_i^r(m)`

holds exactly for trial r. No narrow-band approximation, deconvolution or unknown frequency-smoothing phase is used. The known pre-filter gate and full tail are doing the work.

## Three-trial closure waveform

For independent trials a,b,c define at each bin

`W_Y=Y1^a Y2^{a*} Y2^b Y3^{b*} Y3^c Y1^{c*}`.

Then `W_Y=|H1 H2 H3|^2 W_Z`. The multiplier is real, nonnegative and even in frequency. Thus the inverse DFT is an even-filtered circular closure waveform. Its phase, with an explicit fixed symbol for zero, is invariant under every nonzero channel gain. Filter zeros can erase information and are not assumed absent for free.

Reversing one T-sample physical record gives `Z_i^R(m)=epsilon_i exp[-2pi i m(T-1)/M] Z_i(m)^*`. The common origin phase cancels within every same-trial edge; each parity appears twice. Reversing all three trials consequently sends W to its conjugate, irrespective of individual definite parities. This is an exact finite-record reversal transport theorem.

Any measurable bounded or categorical test of the complete phase vector now has a valid conjugation null under physical reversibility. If the full physical trial law supplies a finite-record path-KL budget, data processing supplies the corresponding three-trial information bound. This does not require Gaussianity or replacing the law by its covariance. A full-law test is not intrinsically capped by the elementary second-moment inequality's 2/(3T).

## A stronger ordinary alternative appears before three trials

For only two physical channels in a single trial, define `theta=arg(Y1 Y2*)`. Under the same gate/filter contract it is the unfiltered relative phase plus the unknown constant `arg(H1 H2*)`. Physical reversal is therefore reflection of theta about an unknown circular axis (the parity shift is absorbed into that axis). Testing reflective symmetry about an unknown axis is established circular statistics: Pewsey2002 DOI10.2307/3316098; Ameijeiras-Alonso, Ley, Pewsey & Verdebout, arXiv1707.09272 and its published version.

These ordinary methods receive the same finite gated records and can test non-Gaussian phase-law asymmetry without a separately calibrated sensor phase or three dedicated source copies per statistic. Pooled U-statistics can likewise reuse all trials for closure estimates; a naive factor-three saving is not a universal comparison. Unknown-axis symmetry tests and higher-order/invariant polyspectra must be included before claiming a closure-method advantage. Their asymptotic assumptions are not silently converted into finite confidence.

The first nonzero relative-phase trigonometric moment can always be rotated to real; ordinary two-point phase cannot witness the unknown-axis obstruction. Higher-order circular symmetry can. For example, a phase law on an equally spaced triangle with three distinct positive weights has no reflection axis; this is a general observation-class separation, not evidence of a new test or a real instrument.

## Finite error and cost boundaries

If a captured DFT value has a certified complex error disk of radius d_i^r, its phase error is at most `asin(d_i^r/|Yhat_i^r|)` when the disk misses zero. Summing the six terms bounds closure phase error; two terms bound relative phase error. A zero-containing disk requires a full phase uncertainty/explicit missing symbol. Selecting only large observed amplitudes needs a reversal-even selection law or conservative treatment of uncertain membership. No rare event or reset is discarded from the acquisition bill.

For N trials the direct time bill is at least `N*(T+L+preparation/return time)` in sample units, plus obtaining the support/tail/noise/reversal promises. Readout gating must occur at the specified location in the chain. A generic old archive lacks this guarantee; software zero-padding cannot supply it retrospectively. When an actual common-camera reversal-equivariant map is already qualified, ordinary path/KL tests get that stronger contract too and may need no closure filtering at all.

## Endpoint of this candidate

The finite gate theorem is a positive conditional bridge, but no presently acquired instrument/record supplies its entire contract. The full-law statistical alternatives are established, and no acquisition advantage over those alternatives has been demonstrated. This is therefore not promoted into a discovery multiplier or a new physical capability. It is retained as useful exact capital, while the scientific question is replaced below rather than tuning its moment constant or the old PS500 spectrum.
