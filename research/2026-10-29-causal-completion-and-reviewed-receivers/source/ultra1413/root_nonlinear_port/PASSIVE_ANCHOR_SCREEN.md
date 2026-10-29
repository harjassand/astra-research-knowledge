# Can ambient noise replace the distributed nonlinear actuator?

29 October 2026. Root's bounded alternative-mechanism screen. This is a
resource/identifiability observation, not a new reconstruction algorithm,
novelty claim, executed experiment or qualified apparatus.

The costly resource in the pulse constructions is a known physical-coordinate
anchor: globally switching an onsite law while retaining the calibrated
quadratic network. A nonlinear element only at the measured port cannot
replace it, by the exact orthogonal-equivariance argument in PROOF.md.
Could passive local fluctuations supply the anchor instead?

For the stable linear model

    dx=-(gamma I+iH)x dt+sigma dW,  y=e0^T x,

with gamma>0 and isotropic circular complex Gaussian W, the answer is no.
For every real orthogonal Q with Qe0=e0, replacing H by QHQ^T and x,W by
Qx,QW preserves the complete port-process law. The stationary covariance is
sigma^2 I/(2gamma); all time covariances are determined by the scalar return
e0^T exp[-(gamma I+iH)t]e0. Gaussianity makes these determine every finite
port distribution. Port-adapted feedback preserves the same equivalence.
More recording time or higher Gaussian moments does not break this gauge.

Known independent NON-Gaussian physical-site sources can break it. Their
higher joint cumulants can contain the physical impulse-response columns,
rather than only their Gram sums. That changes the input contract: independence,
nonzero cumulants, temporal statistics, amplitudes and sufficient separation/
conditioning now need acquisition. The statement does not prove that an
arbitrary single-port Hamiltonian is stably reconstructible from such data.

This broad strategy is already an ordinary blind-identification approach.
I read the primary Fernandes--Comon--Favier ICASSP2007 paper's model and
cumulant equations (pp1--2, Eqs1--5): independent temporally iid non-Gaussian
sources, nonzero kurtosis, a bounded FIR memory, one measured output, and
fourth-order cumulant matching. Its actual theorem/algorithm treats at most
two sources with different channel lengths; it does NOT establish the
general coherent-network operation considered here.

Primary source:
https://www.gipsa-lab.grenoble-inp.fr/~pierre.comon/FichiersPdf/FernCF07-hawai.pdf

A second primary thesis PDF was too large for the web reader (HTTP400,
17549015 bytes); its search extract was not treated as a read proof.
Search-result-level traffic-tomography and MISO tensor work were not treated
as governing theorems either. No absence claim follows from this bounded
screen. No model run or additional worker was used.

Decision: preserve as a potentially different physical anchor, but do not
promote it as a free passive replacement or a new generic discovery. Without
a concrete qualified source/noise platform and a paid finite-data receiver,
it does not currently earn development priority over the completed operations.
