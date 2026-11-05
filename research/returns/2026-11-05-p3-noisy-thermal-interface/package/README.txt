ASTRA: A NOISY INTERFACE TO A LONG-LIVED THERMAL QUANTUM REGISTER
Research construction and reproducible finite checks | 5 November 2026

START HERE
----------
Astra_Noisy_Thermal_Interface.pdf is the self-contained report. The new result
is a fixed-component-noise circuit construction, with an explicit compatible
thermal holding model. It is not a fabricated device, a practical resource
estimate, or a claim of universal energy/spacetime superiority.

The construction closes the noisy controller, thermal starting distribution,
unknown quantum input, noisy local delivery, and stopping-time read interfaces.
It proves independent boundary-noise compilation from correlated protected
syndrome histories, positive thermal precompensation at fixed temperature,
polynomial constrained sampling, and a common-bath obstruction for all
noninteracting holding Hamiltonians. It retains a paid nonlocal active fabric
and the accepted commuting Hamiltonian/Pauli-Davies bath assumptions.

THE OPERATION AND ERROR
-----------------------
Independent stationary Pauli component noise has a fixed rate p below a
positive sufficient threshold independent of size N, holding horizon T and
interior error budget epsilon. The fully acquired example uses one homogeneous
Pauli channel on every outgoing primitive wire, fixed preparation/measurement
templates, and selective isolation of actual check couplers for calibration.
Circuit lemmas admit broader specified independent Pauli laws; that does not
prove general gate-dependent hardware identification.

For R offered source/access opportunities and deterministic per-source
intrinsic-time caps summing to T, the process error has the form

  C n_raw p + epsilon_total + C [R N q + Gamma N T] b_N,
  q = O(p),       b_N <= C' exp(-c N^eta).

Rejected or selectively considered candidates count as offered opportunities;
in ordinary sequential use R is proportional to actual writes and reads. The
selected source is not assigned an equilibrium marginal for free.
The anytime-read proof first gives a sharper-tail term proportional to
N q (1 + Gamma N T_j); an explicit fixed Peierls slack absorbs its extra
polynomial factor. If only a total pathwise cap is provided across adaptively
refreshed sources, the conservative bound retains an extra reset-opportunity
factor. All references and pre-existing retained records are included jointly.
No uniform guarantee conditional on an arbitrarily rare record is asserted.

The raw-port term is real. A fixed number of unprotected unknown-input and
final-output cuts supports O(p)+epsilon. Encoded internal operations can reach
arbitrarily small epsilon. Every additional raw release/reacquisition can pay
another O(p); protected reuse does not repay the original input floor.

NEW PROOF NOTES (in noisy_interface_work/)
-----------------------------------------
operation_theorem.md
  Full campaign, actual seed extension, adaptive reads, source caps, physical
  accounting, and the noninteracting blackout boundary.
inverse_noise_theorem.md
  Signed inverse-noise polymers, all positive prefixes, local influence,
  constructive sampler, full Gibbs preparation, and free-energy bound.
endpoint_route/same_code_controller_bridge.md
  One Aharonov-Ben-Or code for quantum and noisy classical work; actual
  adjacent-level interfaces and local-stochastic raw fanout.
endpoint_route/endpoint_and_refresh.md
  Raw-port lower bound, Bell refresh, product Pauli output channels,
  calibration of the virtual comparison channel and synchronized deployment.
passive_route/static_tree_regenerator.md
  Mixed local-stochastic coupling that erases dependence on old errors with a
  static noisy majority tree. Exact reference leaves are a proof device only.
passive_route/history_erasing_bell_export.md
  Logical/gauge/reference composition and discarded internal records.
passive_route/soft_polymer_sampling_lemma.md
  Context-dependent heat bath and its weighted path-coupling proof.
passive_route/noisy_acquisition_and_control.md
  Noisy coefficient/channel acquisition, statistical precision, protected
  computation and the real additional selective-check access.

REPRODUCTION
------------
Requirements: Python 3, numpy, scipy, matplotlib, mpmath, Pillow, reportlab.
The PDF renderer uses the standard DejaVu TrueType fonts installed at
/usr/share/fonts/truetype/dejavu. No network or external full-text file is
required to reproduce the calculations or report.

From the unzipped package directory:

  python3 noisy_interface_work/run_all_checks.py
  python3 noisy_interface_work/build_report.py ./rebuilt_report

The check runner executes:
  verify_precompensation.py
  classical_tree_regenerator.py
  passive_route/check_static_tree.py
  endpoint_route/check_interface_identities.py
  verify_blackout_boundary.py

The first two scripts regenerate their JSON and scientific plots; the runner
also saves the two stdout-only finite-check outputs as JSON. Monte Carlo is
explicitly separated from rigorous algebra and the uniform coupling proof.
The blackout check tests matrix identities and broadcasting extensions; it
does not simulate a macroscopic BDL memory or measure its lifetime.

The package contains already generated result files. SHA256_MANIFEST.json
records each distributed file, except the manifest itself. build_package.py
documents the whitelist used to create the archive and needs the workspace
predecessor archive when run in its original location.

SCOPE AND RESOURCES
-------------------
All elementary gates, controls, waits, resets, raw measurements and final
corrections are noisy. The source, compiler and decoder are actual protected
computations. The final local classical controls and quantum outputs arrive
at a common prescribed clock. The classical regenerator uses a polynomial
number of protected copies in inverse accuracy, in addition to the ordinary
fault-tolerance overhead. This is not merely polylogarithmic preparation cost.

The complete resource ledger includes fabrication and coupler precision,
nonlocal links, component/SPAM acquisition, actual-check calibration, cold
preparation, all quantum/classical occupied spacetime, gate/reset/link energy,
static interactions, cooling and record maintenance, and each paid refresh.
The BDL existence constants, large conservative computational code, cold
temperature and small sufficient p threshold remain explicit disadvantages.

The blackout theorem uses an unobserved independent isotropic Pauli Davies
bath, with g_beta(omega)=2 nu/(1+exp(-beta omega)), and no quantum helper
outside the holding channel. Arbitrary pre-hold encoding, classical side
records, local gaps/cooling, and final decoding are allowed. Monitoring the
purifying bath record, an interacting autonomous correction device, or an
off-model protected quantum helper changes this target.

This is not a derivation of finite-speed, bounded-density, strictly local
three-dimensional active routing. It does not tolerate general noncommuting
fabrication error, unrestricted drift, correlated bath bursts or arbitrary
hidden failure of switching hardware. No finite calibration campaign can
certify the declared noise model for all future times.

A state free-energy excess is bounded by O(N q^2 exp(w beta J_max)); this is
not the energy consumed by the preparation algorithm or a reversibly
attaining work protocol. Ordinary active fault tolerance receives the same
controls, cooling, reset, metrology, routing and input access. A competitor
given the same passive protective hardware may use it. No universal total
resource advantage follows from the passive lifetime.

PRESERVATION
------------
predecessors/Astra_Thermal_Register_Research_Package.zip is copied unchanged:
  bytes: 9131625
  sha256: fcc57d7e78d9561e87a8bb557347bc9d8bb106dd318d51971d16ef393bf39394

It preserves the accepted reusable-register process, source-conditional
loader and bath inputs, once-paid classical syndrome source, intrinsic-time
coupling, reference/record guarantees, paid syndrome-preserving access,
separate coherent TFD and central-sector constructions, and earlier direct
prevention, productive-control/repair, burst-loss and first-event machinery.
Those results are not reproved, broadened, or reduced to one physical class
here. Named actual-check sampler obstructions remain obstructions to those
specific sufficient routes; no general sampling-hardness claim is made.

PRIMARY SOURCES
---------------
Aharonov and Ben-Or, measurement-free fault tolerance:
  https://arxiv.org/pdf/quant-ph/9906129
  https://doi.org/10.1137/S0097539799359385
Christandl, Fawzi and Goswami, quantum input/output, v3:
  https://arxiv.org/pdf/2408.05260v3
Christandl, Fawzi and Goswami, qLDPC interfaces, v2:
  https://arxiv.org/pdf/2602.16948v2
Zhang et al., quantum error pre-compensation:
  https://arxiv.org/pdf/2309.01434
Kotecky and Preiss, abstract polymer expansion:
  https://doi.org/10.1007/BF01211762
van Enter et al., Gibbs evolution and connected flip islands:
  https://arxiv.org/pdf/math-ph/0105001
Balasubramanian, Davydova and Lin, passive 3D quantum memory:
  https://arxiv.org/html/2605.10943v1
Dunnweber, Styliaris and Trivedi, autonomous 2D correction/computation:
  https://arxiv.org/html/2601.20818v1
Horodecki, Shor and Ruskai, entanglement-breaking channels:
  https://arxiv.org/pdf/quant-ph/0302031
Gottesman, local-gate fault tolerance:
  https://arxiv.org/pdf/quant-ph/9903099
Christandl and Muller-Hermes, noisy communication interfaces:
  https://arxiv.org/pdf/2009.07161

Full proofs, source attribution and limitations are in the report and notes.
Standard threshold, error-precompensation and cluster-expansion ideas are
credited; no exhaustive priority claim is made. Third-party full texts and
private upload helpers are not distributed.
