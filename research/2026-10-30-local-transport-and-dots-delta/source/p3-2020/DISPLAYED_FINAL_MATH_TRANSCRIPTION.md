# Normally visible2020final: text/formula projection

Visible-only source; no acquired manuscript/code/review originals or alternate transfer. Original TeX annotations replace duplicated rendered math glyphs.

ChatGPT said:ChatGPT
Constructive result
I constructed a local compiler that finds the positive potential and the physical controller together, in an explicit one-dimensional perturbative regime. The target is a sustained quantum process whose long-time recorded trajectories realize a prescribed exponential bias of a source process.
The result is a constructive tractability theorem with runnable prototypes. It does not yet establish a practical control advantage. The ordinary alternative receives the same information and can use the same compiler.
The previous locality, retention and adaptive-control files remain preserved. The completed checkpoint is    STATUS.md.
The central mechanism
Quantum Doob dynamics already supplies a formal way to make biased trajectories typical, and physical congruence constructions have precedents in quantum belief propagation. The missing step here was computing the required positive many-body object and turning it into executable local dynamics. Springer Nature Link+1
The mechanism I developed connects four operations:
Construct the positive eigenoperator  $F$  using a local Kirkwood–Thomas expansion.
Construct its ordered logarithmic derivative $D(t)=F'(t)F(t)^{-1}.$ An ordered-heap expansion retains the order of overlapping, noncommuting operators.
Integrate a physical congruence satisfying  $S^\dagger S=F$ .
Construct dressed jumps and their aggregate normalization, then assemble a trace-preserving Lindblad generator.
The underlying coupled-cluster and heap machinery is established. The working contribution is the constructive bridge from those representations to a local physical controller, together with the error and resource bounds. Priority remains unassessed. arxiv.org+1
This avoids an invalid shortcut uncovered during the investigation: the creation-operator logarithm is not an ordinary matrix logarithm. The physical controller also needs no global probabilistic filter, failure branch or rejection of complete trajectories.
What the theorem establishes
After a known independent-cell reference transformation, let  $\gamma$  be the reset gap and  $g$  the per-site perturbation strength in the specified centered coefficient norm. An explicit sufficient condition is $\frac{g}{\gamma}\le \frac1{4096}.$
This is a conservative proof constant, not an estimated physical phase boundary.
At perturbative order  $m$ , each dressed local operation can be computed on an  $O(m)$ -site interval. For continuous monitored implementations, the joint native-record/final-state approximation error over duration  $T$  is bounded by $C\,nT\,2^{-m}.$
Thus  $m=O(\log(nT/\epsilon))$  suffices. The one-dimensional compiler uses  $n\exp(O(m))$  arithmetic work. A subsequently completed and internally reviewed finite-bit argument supplies polynomial guard bits under explicit input-encoding, gap and conditioning assumptions. Generic whole-patch synthesis is consequently polynomial in this regime, with potentially prohibitive constants and exponents.
The compiler chooses a physical Doob gauge. Its long-time counting statistics agree with the conventional positive-square-root gauge; its finite-time instrument need not agree from an unchanged initial state. The approximation theorem compares the selected exact controller with its own truncation, using the same initial state.
The complete derivation is    perron_gauge_compiler.md.
Executed evidence—and its limits
The saved experiments distinguish theoretical guarantees, synthetic acquisition, floating calculations and exact rational identities.
Work completedResultWhat it establishes
Local calibrationSynthetic count archive representing 45,711,360 two-qubit device usesAcquisition and physical fitting were implemented; no laboratory observations occurred
Conservative phase checkAt coupling  $10^{-5}$ , a simultaneous 99% confidence calculation gives  $g/\gamma\le 7.98036\times10^{-5}<1/8192$ Phase membership with slack under the supplied structural promises; not stringent end-to-end accuracy
Four-cell compilationTested counting-function error fell from  $8.08\times10^{-3}$  at order zero to  $1.33\times10^{-8}$  at order fourUseful floating evidence outside the universal sufficient regime
Collective record checkNonzero adjacent count covariance was reproduced to approximately  $3.35\times10^{-10}$  at the tested finite-difference stepThe corrected example has an interacting record target
Local scalingOne central jump compiled on seven sites for nominal chains of 16, 128 and 2,048 sitesLocal coefficient construction; not operation or compilation of the entire 2,048-site system
Synthetic operation1,200 three-qubit trajectories, 68,967 jumps and 54,000 modeled qubit-time unitsAn operating simulation with its initial transient retained
Exact rational verificationEight coefficient identities through third order vanished exactlyFinite verification of gauge factorization and aggregate normalization, without floating tolerances
Calibration dominates the learned example. Its fourth-order controller has mean  $1.5333768010$ , essentially matching the fitted-model target  $1.5333768113$ . The actual-source target is  $1.5325405007$ , a discrepancy of about  $8.36\times10^{-4}$ . The tiny compilation residual is therefore not an unknown-device accuracy certificate.
The full resource ledger is    EXECUTION.md. The runnable implementations include   check_perron_gauge.py and   check_gauge_exact_rational.py.
Failures that changed the attack
The first example failed substantively: maximally mixed resets and unital interactions made its rewarded record exactly an independent Poisson thinning. An ordinary reweighted clock solved that observable task. I preserved that construction, changed the reset state, and executed the corrected interacting example.
The ordinary order-zero controller remains strong. Inside the conservative proved regime, its tested counting-function error is already about  $2.18\times10^{-6}$ . Higher orders improve fidelity to the specified interacting process, but most of the increased mean count comes from ordinary independent-cell reweighting. A larger count alone is not evidence of a stronger capability.
The actual enabling interface is also substantial: known reset cells and clocks, individually addressable local event instruments, fresh local probes, and calibrated synthesis of changed operations. The modeled acquisition alone requires approximately 91.4 million elementary qubit preparations and 73.1 million elementary qubit readouts.
Timing and initialization remain explicit costs:
Continuous-record guarantees require continuous monitored dynamics. The elementary digital implementation guarantees a time-binned record, not exact continuous timestamps.
Digital holding noise accumulates over actual laboratory time, including gates, preparation and readout.
The initial/terminal potential contributes an extensive  $O(n)$  boundary term. No transformed initialization or exact finite-horizon canonical tilt is free.
Completed internal reviews found no fatal error in the constructive core under these assumptions. The    core audit and    finite-bit addendum are saved; they are not external acceptance or formal verification.
The larger principle now available is constructive physical control through the local change of a positive many-body potential. Its consequential next test is whether that representation supports a collective capability under useful interaction strengths and realistic holding costs. The present work supplies a proved route and an executed mechanism; it does not yet establish that practical advantage.
STATUS.mdDocumentOpen file   perron_gauge_compiler.mdDocumentOpen file   EXECUTION.mdDocumentOpen file4 more
