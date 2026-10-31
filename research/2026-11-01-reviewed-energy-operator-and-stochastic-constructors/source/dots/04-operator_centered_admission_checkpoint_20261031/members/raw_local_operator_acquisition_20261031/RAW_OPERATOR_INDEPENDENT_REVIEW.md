# Independent review: raw finite local-operator acquisition

31 October 2026. Reviewer: challenge_graph_profile_compiler.

## Verdict and immutable scope

**PASS, after the complex-rational normalization repair described below**, for the finite supplied-operator drift certificate and its conditional mathematical receiving theorem. This is not a complete circuit-schedule certificate, experimental model validation, hardware guard construction, or threshold theorem. It does not establish optimal search, practical superiority, or historical novelty.

I read the entire mathematical source, acquisition implementation, and supplied test suite. I ran the suite through its non-writing `run()` entry point, preserving the author's saved fixture JSON, and constructed a separate exact/adversarial suite. The repaired supplied suite passes 113 checks; the independent suite passes 238 checks. Tests supplement, rather than replace, the proof and code inspection.

Bound sources in `raw_local_operator_acquisition_20261031/`:

- `RAW_OPERATOR_ACQUISITION_AND_RECEIVING.md`: SHA-256 `5fdd5bf94326e4715a4dc486a35bfe8bb939a456e44588c324ef491d0b9ba534`.
- Repaired `acquire_operator_certificate.py`: SHA-256 `35acdcdcc533f523cc78c558153f97fcb800711bbd4ff0f57b8a2ea50d60ee35`.
- Repaired `test_operator_certificate.py`: SHA-256 `a653b40243e6560328315e6e916e166e29058e4327e3ca1f81aad998aca021c2`.
- Independent `check_raw_operator_independent.py`: SHA-256 `adf47b79b1087f719a14d3706798c7a82293da7b88ad27583d8d41cf52e71d20`.
- Independent `raw_operator_independent_checks.json`: SHA-256 `78299e9c5214f3bde96f951eec9e564abec8c54877e0e153ca78a4d919815f82`.

Installed SymPy version independently checked: 1.14.0. No original author source was edited by this reviewer. The final source adds Section 8 describing a separate schedule wrapper and Section 9 preserving the normalization repair. I read both additions. This receipt binds the core theorem/code and Sections 1–7 and 9; it does not verify the new executable claims in Section 8. The separately appearing `receive_operator_schedule.py` and its tests/certificates are NOT reviewed or accepted by this receipt.

## 1. Common-kernel acquisition and actual access

For the supplied Hermitian coupling coefficients on each finite cell, the stacked nullspace gives their common kernel. If X spans it, X(X*X)^(-1)X* is its orthogonal projector, with exact complex-rational entries. Hermiticity gives both BP=0 and PB=0, hence B=QBQ. Empty coupling lists yield P=I; a zero-dimensional transparent sector is conservatively refused. This does not prove impossibility under another decomposition, cancellation, encoding, or physical redesign.

The repaired implementation explicitly normalizes computed complex-rational expressions and checks the projector and annihilation identities. Its coefficient norm upper bound, the maximum row sum of absolute real and imaginary parts, dominates the Hermitian operator norm. The actual supplied matrices, Pauli support, rates and external task are bound; spectator factors cannot be omitted and then inferred from this certificate. Subsequent location grouping must sum the relevant acquired coefficient bounds.

The program reads finite explicit local matrices, not matrices of the total tensor Hilbert space. Its cell dimension, local support and local matrix dimension caps are real restrictions. It still pays the full explicit graph/term input and uses a global cell-index matrix; this is not sublinear acquisition of an unknown large device.

## 2. Local positivity and global drift

The local generator adjoint is evaluated directly, with the correct Hamiltonian sign i[H,V] and rate-weighted dissipators. Source-creating terms are not discarded. The proposed right-hand side minus the adjoint has degree at most two in each weight coordinate. The tensor degree-two Bernstein conversion in the source and code is exact. PSD of every Bernstein coefficient is a sufficient operator inequality on the whole cube, not merely a test at its vertices.

The independent verifier checks Hermitian PSD by rational Schur complements, removing zero rows only when the corresponding zero diagonal has a completely zero row. A zero diagonal with a nonzero row is correctly rejected. Positive pivots preserve PSD equivalence. After the repair, all computed entries remain canonical complex rationals, including singular and non-real cases.

The finder uses a smaller, ordinary sufficient cone: each coefficient is diagonally dominant with diagonal at least the sum of the absolute real and imaginary off-diagonal parts. Its auxiliary linear inequalities and nonnegative activation objective correctly encode that cone. This is not a complete PSD finder or a new optimization method. The independent verifier does not require diagonal dominance. I exhibited and verified a rank-one non-diagonally-dominant Bernstein coefficient in a valid certificate that this verifier accepts.

Embedding a local inequality multiplies it by a positive commuting outside weight. Summing overlapping terms produces the declared global M and activation allocations; no independence of local trajectories is needed. Off-diagonal nonnegativity makes M Metzler. BOTH row and column margins at most -kappa are load-bearing: rows bound each coordinate, columns bound selected volume. The independent suite separately rejects a row-only and a column-only purported certificate. The activation cap cannot be discarded: even zero physical dynamics with a nonzero charge can satisfy an artificial negative-drift allocation only by paying compensating activation. Such a certificate is not free cooling.

## 3. Conditional amplitude receiving

Assume the additional actual finite gate/idle schedule, source-to-location incidence, system patch support, intended system-only controls and integrated control-residual bounds stated in Section 5. In particular, each active unwanted term is supported on its declared cell and system patch, satisfies K=QKQ, and at most one selected active location is assigned to a cell at a time. These are not inferred by the acquisition program.

The product weight V=product(I+u_i Q_i) commutes with every such real unwanted term. On a complex contour, its imaginary part contributes at most 2Rc Q_i V, while source-independent control residuals contribute the scalar integrated potential. Using the backward equation u'=Mu+v(1+u), positivity follows from the Metzler property. At u_i=1, the row margin bounds the derivative by -kappa+4Rc, so R<=kappa/(8c) keeps the solution inside the cube. The column margin gives the positive-semigroup 1-norm bound exp(-kappa t).

For k selected locations, convolution and the incidence/duration bounds give initial total weight at most 4Rcgk/kappa and integrated total weight at most 4Rcgk tau/kappa. The derivative of V cancels the acquired drift contribution. Activation and control residuals remain, giving the stated common jump-history dilation squared-norm bound

    exp([4Rcg(1+a tau)/kappa + 2R epsilon_ctl] k).

The finite initialized-field dilation is the SAME analytic dilation for every contour point; it is not a collection of unrelated Stinespring choices. The finite-dimensional bounded-generator Dyson/jump-sector argument from the previously reviewed receiver applies. Multivariate Cauchy extraction of inclusive selected-location fault amplitudes therefore gives

    [ exp(R[2cg(1+a tau)/kappa + epsilon_ctl]) / (R-1) ]^k.

Arbitrary initial correlations among the finite source, system and reference are allowed; arbitrary uninitialized incoming Markov fields are not. Intended controls must respect the receiving interface. Any adaptive/coherently controlled implementation must pay a common actual support/incidence bound rather than substitute incompatible branchwise small supports.

The c=0 branch must be handled directly; a positive drift certificate does not itself imply that an admissible R>1 or a useful fault strength exists. This remains an initialized-isometry inclusive amplitude premise, not an automatic Pauli channel, marginal-probability statement, physical threshold, or arbitrary shared-bath theorem. Consumer contract hashes identify supplied obligations but do not authenticate or prove them.

## 4. Code boundary, verification and search

The parser enforces exact keys, canonical rational pairs, integer rather than bool/float metadata, finite matrix shapes, Hermiticity, nonnegative rates, ordered supports and finite resource limits. JSON duplicate keys, floats and nonfinite constants are refused. External model/task binding is recomputed from the caller's supplied specification. Merely editing a certificate's input digest cannot bypass the reconstructed local inequalities.

Successful certificates are checked independently of the optimizer. Optional acquisition statistics are checked by rebuilding the finite LP description, not trusted as scientific evidence. UNKNOWN is not accepted by the certificate verifier; CLI acquisition and verification distinguish successful certification from refusal and malformed input. UNKNOWN can mean no common kernel, failure of the restricted cone, resource refusal or unresolved optimizer behavior; it is not instability or impossibility.

LP size bounds apply after local polynomial construction; the wall-clock budget applies only to the optimizer call. They do not bound preprocessing, all rational bit growth, verification or I/O. The timer refuses unsupported/non-main-thread/already-active-timer situations rather than silently removing its budget. The ordinary exact simplex has no claimed polynomial worst-case runtime. Supplied proof size and rational arithmetic sizes remain part of verification costs.

The tests do not authenticate completeness or accuracy of the physical operator model, an external control evidence file, a gadget contract, or hardware calibration. The program is a known-model mathematical compiler, not a physical learning procedure.

## 5. Actual defects caught and preserved

The initial implementation, SHA-256 `c49faf3743da82019e762c21a562956ed2830ddce9dfa2f6f3750796e2d60147`, is preserved as `acquire_operator_certificate_pre_complex_normalization.py`.

I found two related valid-input defects:

1. A valid expanded complex-rational PSD Gram matrix could leave unsimplified expressions after Schur elimination. The final positivity comparison then raised TypeError instead of returning true; the outer verifier rejected the valid certificate.
2. The exact Hermitian rank-one matrix

       [[9, 9+9i, -6i],
        [9-9i, 18, -6-6i],
        [6i, -6+6i, 4]]

   has a two-dimensional common kernel, but charge acquisition crashed on an unsimplified projector identity assertion.

These were false rejection/crash defects, not demonstrated unsound PASS cases. The author repaired canonical real-plus-imaginary rational normalization in computed P/Q, identity products, matrix encoding, PSD input and every Schur complement. I read the diff and reran both failure families. I also exercised an actual complex rotated-loss model through acquisition and independent verification. The repaired suite includes the failures; the old bytes and failure history are not silently erased.

## 6. Evidence and limits

The 113 supplied checks passed via `run()` without rewriting saved results. The 238 additional checks include all integer-record bool/float alias substitutions, complex raw-kernel and actual complex-loss acquisition, 30 complex Gram PSD cases and 30 negative cases, genuine non-DD PSD verification, separate global margin tests, exact multivariate Bernstein reconstruction, rehashed external-model mutation, and strict JSON rejection.

The method combines ordinary common-kernel linear algebra, polynomial positivity certificates, Gershgorin/LP search, exact Schur verification and the already reviewed product-weight/Cauchy receiver. Stronger ordinary SDP/SOS methods may certify additional inputs. No exhaustive historical comparison or superiority claim follows from this review. The useful earned interface is supplied local operators to an exact independently checked drift inequality, with the full physical schedule and consumer premises still explicitly external.
