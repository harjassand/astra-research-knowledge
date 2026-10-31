# Independent whole review: source-derived charges and centered creation

31 October 2026. Reviewer: challenge_graph_profile_compiler.

## Verdict and source binding

**PASS within the supplied finite-operator model and explicit static schedule interface.** I read the complete general-M receiving proof, executable specification, finder, independent certificate checker, schedule receiver and tests. I reran the supplied non-writing `run()` entry point: 152 checks pass. A separate independent exact/adversarial suite passes 86 checks. No author fixtures or frozen dependencies were rewritten. No new defect was found in these versions.

Sources in `centered_source_acquisition_20261031/`:

- `GENERAL_DRIFT_CLAMPED_RECEIVER.md`: `84ec35f0341ea677885ddff0960ec8132022134c86731a13e39da290922f29c7`.
- `CENTERED_SOURCE_ACQUISITION_SPEC.md`: `c5d7f4b6742dacda8e981f0637d8f7bc9bf985bac45798b55048362c92e97cdc`.
- `acquire_centered_certificate.py`: `f9b5dbc5f9c3047081f2a5b2549f2a3d67109aab209952ce9c415b2c7327b4e8`.
- `receive_centered_schedule.py`: `3ce26d413ee2fde44c7864f7e2ed033dd13be89a9a096d6bbc22dc7d0b243b47`.
- `test_centered_acquisition.py`: `17fbe762c96c83a6d423fdc981b3e3b5e8be7c1f70667fa2d0cfcdf82982bd78`.
- Independent `check_centered_independent.py`: `fcccf4be0a50a24f8f38166784a089aab1290f01a4cf0f0c04f6af63d2415b80`.
- Independent `centered_independent_checks.json`: `52b0bba1367f95609beb2589eaf5b046d63a03c1e04d0e3a865d6604714f39e6`.

The implementation hash-checks the repaired raw matrix component `35acdcdcc533f523cc78c558153f97fcb800711bbd4ff0f57b8a2ea50d60ee35` and frozen schedule component `a7bc4e513cb4de03a3ef5c504bae75b7b464cb4985a9a683cd560f9d439136f8`. Their previous scoped receipts remain dependencies, not silently strengthened claims.

## 1. General-M clamped proof

The input is an exact product-weight inequality for the ACTUAL full source generator, with M Metzler, both row and column margins at least kappa>0, and nonnegative activation at most a. Projectors may have arbitrary nonzero rank; no pure stationary reference is assumed. For each cell/location the TOTAL unwanted operator has PP compression zero and norm at most c, on the declared source cell and system patch. It need not annihilate P. Initialized Markov fields and the finite-register/common-control-support premises remain essential.

For unselected real creation, the operator Schur bound spends delta=kappa/4 times uQ and pays activation alpha=4c²/kappa times uV. Thus the free backward drift is M'=M+delta I, with row and column margins kappa'=3kappa/4. These allocations are valid for rectangular P/Q blocks, not only a scalar two-level decomposition.

At a selected clamped coordinate u_i=1, the ORIGINAL source coefficient satisfies (Mu)_i<=-kappa. The complex selected commutator has off-diagonal norm at most 3Rc and QQ part at most 4Rc. The proposed scalar cost 36R²c²/kappa plus kappa Q/4 covers the off-diagonal part; the cap R<=kappa/(16c) covers the QQ part with another kappa Q/4. The remaining original row margin is nonpositive. The proof correctly does NOT also subtract the outside-creation delta allocation at selected sites. Overestimating their scalar activation by a_eff remains harmless.

Forcing the selected coordinate to stay one gives

    f_i=-(M'u)_i,  kappa'<=f_i<=D-kappa/4=F,

where D=max(-M_ii). The upper bound follows from nonnegative off-diagonal entries and nonnegative other coordinates. The lower bound follows from the row margin. Free coordinates remain in [0,1] by the first-boundary argument. At most gk backward upward clamps occur, each of size at most one, and the active forcing has instantaneous 1-norm at most Fgk and integrated 1-norm at most Fgk tau. Column contraction therefore proves exactly the two displayed impulse/forcing bounds. The diagonal-to-gap factor F/kappa' is necessary in this proof and is explicitly retained.

Backward upward clamps become forward DOWNWARD weight jumps. For the positive tilted density they can only decrease the weighted trace. Continuous free-coordinate derivatives cancel M' while selected coordinates use the original row-margin allocation above. Initial weight is bounded by exp(sum u(initial)); terminal weight dominates identity. Activation integrates against the total weight volume. Selected source-independent residuals add the stated 2R epsilon_ctl per location. These steps give the claimed common-dilation squared-norm bound with C0 and the 36R² term.

One fixed analytic jump-history family is used at every complex parameter, with the actual outside creating interactions on. The finite bounded-sector argument supplies operator-norm analyticity; no independently chosen Kraus phases or classical source paths are substituted. Multivariate Cauchy extraction then gives eta(R)^k for every finite selected set, with denominator (R-1)^k. Arbitrary finite initial source/system/reference correlations are allowed; arbitrary uninitialized incoming fields are not. System-only controls and common actual support bounds must satisfy the stated receiving interface.

This generalization is more than substituting a gap into the earlier qubit proof: both D and the entire actual generator inequality are paid. A large negative diagonal canceled by large positive transport can yield a poor bound despite a positive gap. The implementation's conditioned-M example correctly demonstrates that limitation.

## 2. Acquiring source-derived projectors

The source catalog uses only positive-rate ONE-CELL supplied jump matrices to propose common kernels. Empty subsets, zero kernels, failed compression tests and duplicate projectors are all treated explicitly and charged in the finite trial count. The order and caps are deterministic. A multibody jump is not automatically treated as a favorable one-cell loss.

Each projector is computed by exact rational complex nullspace and Gram inversion, using the repaired normalization routines. The catalog checks projector and annihilation identities for proposing jumps and PBP=0 for EVERY actual coupling coefficient. Hermitian B then has the required block form. It does not require BP=0, and it does not subtract an unpriced PP mean. Termwise centering is conservative if supplied terms could cancel; it is never more permissive.

Crucially, the proposing subset is NOT the subsequently verified generator. Every actual source Hamiltonian, raising channel, recycling channel and other supplied local term is included in the Bernstein drift inequality. The finder calls the inherited DD-cone LP with the newly proposed Q, not the old coupling-kernel projector. The checker independently reconstructs all local coefficients and tests their exact PSD plus the global margins and activation cap. The subset alone cannot authorize dropping unfavorable dynamics.

The verifier recomputes the catalog, provenance, selected indices, Cartesian position and bound external specification. It accepts valid allocations outside the finder's diagonal-dominant cone, subject to the same exact PSD checks. Catalog metadata describes a reproducible bounded search envelope; it is not an attestation that earlier candidates were actually run or failed. This distinction is explicit and does not weaken the accepted inequality.

UNKNOWN means no certificate was found in this bounded catalog/sufficient cone or within its budgets. It is not a general impossibility result. Full input inspection, catalog construction, exact coefficient growth and independent verification are paid outside the LP wall-clock timer. There is no exponential total Hilbert-space enumeration, but explicit input size, dense cell-index storage, subset trials and ordinary simplex costs remain.

## 3. Complete schedule and rational admission

The receiver first verifies the external centered certificate, then recomputes actual kappa, D and a from its allocations. The legacy component is used for full static gate/idle support coverage, source-to-location incidence, intended operation validation and rational grouped norm/control data. Its positive scalar coupling envelope sums ALL coefficient norm bounds at each cell/location. Thus c bounds the aggregate actual operator, including noncommuting source coefficients.

The internally constructed scalar source is bookkeeping, not a replacement channel or an assertion that arbitrary source cells are qubits. The legacy guarded error formula is NOT used for centered X-type couplings. The new clamped formula is evaluated independently with F=D-kappa/4 and kappa'=3kappa/4. Only if exact BP=0 holds for every coefficient is the separately labeled guarded alternative exposed. Its potentially much cheaper bound is valid and remains available without changing the centered status.

For c>0 the dyadic-radius loop checks all three rational caps exactly, refuses if R=2 fails or the explicit search cap is reached, and otherwise returns the largest admitted power of two. The exponent x is computed exactly. The upper (8/7)^ceil(8x) is valid because e^(1/8)<=8/7; its actual integer size is charged and capped. No online real square-root, logarithm or exponential oracle is assumed. The c=0 branch is handled as ordinary control-only error without dividing by c or a vanishing incidence count.

Full-record verification recomputes the result against caller-supplied external data and uses strict recursive type equality. A truthful NOT_ADMITTED record may verify but cannot pass the distinct admission check. CLI verification requires PASS. Task identifiers, threshold-contract hashes and control evidence identifiers bind inputs; they do not inspect or experimentally authenticate those external premises.

## 4. Independent execution and adverse cases

The 152 supplied checks passed without saved JSON mutation. They exercise source-derived X coupling, required two-jump intersections, omitted raising terms and paid activation, nonzero ground compression, zero-rate proposal exclusion, complex rotated sources, incomplete local proposal access, complete schedule failures, source fanout, all source-certificate integer aliases, exact CLI outcomes, fixed-diffusion nonvanishing bounds and poor D/kappa conditioning.

The 86 additional checks include all receiver integer-output bool/float substitutions; a rank-two transparent sector in a four-level source with FULL-RANK creating coupling and a complete admitted schedule; catalog-budget substitution with a rehashed certificate; external consumer budget substitution; zero-coupling control-only receiving; conservative refusal of uncombined PP cancellations; a tiny but nonzero creation component that correctly remains ineligible for the guarded alternative; and exact reconstruction of the chosen maximal dyadic radius, exponent ceiling, exponential rational and eta formula.

The mixed-rank example confirms that the implemented operation is not accidentally restricted to a pure-reference/rank-one loss model. It also does not prove completeness for arbitrary source-derived charges: the catalog remains deliberately limited to supplied jump-subset kernels.

## 5. Scientific and operational boundary

The earned capability is exact known-model acquisition of a useful charge from source dynamics even when the coupling has no annihilating kernel, followed by full-term drift verification and static scheduled centered-creation admission. Physical operator truth, undeclared interactions, hardware losses and activation, gate implementation evidence and the consumer gadget threshold remain external.

At fixed diffusion strength c proportional to sqrt(kappa), the leading c sqrt(g tau/kappa) contribution does not vanish. Neither this result nor its compiler claims that increasing loss erases the induced logical dissipator. Guarded modes are not silently reclassified, and a successful drift certificate is not automatically a small-error admission.

All algorithmic ingredients are ordinary exact linear algebra, bounded catalog search, LP/PSD certificates, schedule validation and rational inequality arithmetic. Stronger ordinary optimization may improve the certificate. This receipt establishes no optimality, historical novelty, practical hardware advantage, or quantum gate backend.
