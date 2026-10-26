# Second-stage development and rejected interpretations

I began with the exact algorithm, data and limitations preserved from stage1.
The original files were inventoried by SHA-256 before imports. Python bytecode
writing was disabled so importing the preserved implementation would not
change its directory. Stage2 uses fresh fixed seeds and reports every case.

The strongest apparent escape from the depth barrier was transient drive:
perhaps a small DC difference hid a transient peak, a frequency-selective
mode or a beneficial time-varying shunt schedule. I constructed the difference
system as a positive cascade instead of subtracting two almost equal impulse
responses. This made the comparison meaningful even on the n=18 path where
the gain is around 1e-18. The time-varying kernel is entrywise bounded by the
unloaded one. SVD of the unloaded finite-horizon operator is the conventional
optimal input, rather than an arbitrarily weak constant pulse.

Primary literature showed that DC determination of the gain of a positive
LTI system is already known in Rantzer's Theorem 3. I did not promote that
rediscovery as a new control law. The additional positive-cascade and
time-varying comparison give a complete scoped derivation for this fault task.

I then attacked the fixed-noise assumption instead of extending it by fiat.
Low-frequency Johnson-Nyquist voltage noise changes with the port resistance.
Absolute fault signal alone is insufficient for this comparison. Passing to
input admittance shows that the *relative* fault signal also decreases in
every positive load, which proves both KL directions decrease for the stated
quasistatic noise model. An additional full-frequency Gaussian-bin surrogate
was evaluated on the same fixtures. It found no gain, but does not prove a
universal colored-noise theorem. I left that boundary explicit.

The positive route was to break the calibration gauge with independent
capacity standards. Normalizing by unknown actuator gain turns the observed
two-point network into a matrix affine in the real Laplace parameter. Its
known capacity slope identifies the gains. The construction works exactly
without generic spectral assumptions. The introduced information is n known
capacity values; it is not discovered calibration from unanchored data.

I executed 15 exact rational cases and then 12 noisy same-information ordinary
joint-fit comparisons. The noiseless construction works, but all eight noisy
direct reconstructions either reject or leave the passive physical class.
The conventional joint fit is substantially stronger under noise. Its own
large internal parameter errors despite small withheld port errors are also
retained. Neither good prediction nor an optimizer's successful termination
was labeled correct identification.

Because a Laplace value is not a free physical observation, I completed a
finite rectangular-pulse and weighted-integral protocol with a truncation
bound and white-readout variance. Sixteen finite-duration examples verify the
bound. Truncation and inverse amplification still spoil most physical
reconstructions. Repeated cycles, finite source amplitude, reset, calibration,
bandwidth and noise resources cannot be omitted from an advantage claim.

The physical data stream may contain more information than the two summaries;
an ordinary estimator can retain and fit the full history. No loss of that
information is imposed on the incumbent to manufacture a win. The all-input
dynamic bound is the stronger comparison in its declared noise/budget model.

During execution the runtime emitted warnings from matmul and matrix
exponential squaring. Every saved finite-horizon operator was finite and its
comparisons passed. I wrote an independent nonnegative-series exponential
audit using einsum arithmetic rather than the warning-producing BLAS path.
Eight comparisons agreed to at most 6.72e-15. This checks those numerical
exponentials; it does not identify the warning's runtime cause or turn the
finite diagnostics into a proof. The original warning and scope are recorded
in the result.

No intervention used negative conductance, active gain, local detectors or
removal of unknown losses without explicitly changing the resource model.
Those remain possible future physical routes rather than operations this
trial claims to have supplied. The final verdict remains a complete scoped
mathematical object and decisive limitations, without mission-scale success.
