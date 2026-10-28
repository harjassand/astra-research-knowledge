# Astra P2: passive causal erasure and a tested computing operation

Checkpoint: 28 October 2026 UTC / 29 October Australia–Brisbane. Previous tranches remain unchanged. This directory contains the new construction, executable work, genuine independent reviews, rejected inferences and source boundaries. It is not an export of the older packages.

## Main result

For a specified controlled-Weyl outgoing-field dilation, construct an exact causal passive receiver that erases the source-dependent field displacement while preserving the intended diagonal source operation, arbitrary references and the entire actual measurement record. The baseline field may be any normal state, including non-Gaussian and initially source-correlated states.

Given features f_(i,t) for n source labels and fixed incoming batches, define

    K_t=sum_(s<=t) Im Gram(f_s).

When K_T=0, a passive interferometer/homodyne compiler needs exactly rank(K_t)/2 retained bosonic modes after batch t. The maximum is at most floor(n/2); incoming modes are additional live width. A separately proved and independently reviewed lower bound shows classical adaptation cannot improve this count within passive optics, vacuum ancillary modes, destructive homodyne, source-independent displacements and local Z feedback. This is a canonical-mode theorem, not a finite Hilbert-dimension, photon-number, lifetime or finite-precision theorem. Non-Gaussian encodings, modular detectors and new source couplings have different resource contracts.

The decisive construction retires more than the radical of the feature span. For a real-orthonormal pair with <u,v>=i sigma, write

    v=i sigma u+sqrt(1-sigma²)w.

Retain physical mode u and homodyne the orthogonal w, whose source coefficients are real. The extra common record makes the construction passive; an earlier active Darboux representation had introduced a false divergent-gain requirement. Applying the split at every arrival preserves K_t and attains all cut minima in one compatible receiver. At the final cut all remaining relevant quadratures are measured. The measured field is destroyed; the source and reference retain the common baseline measurement assemblage.

**What this makes possible:** an actually specified emitted-field feature model can be compiled into a receiver schedule and an exact quantum-storage requirement without solving its arbitrary bosonic input state. It also implements jointly commuting field-quadrature measurements with refined records. Source feedback converts the measurement into an erasing instrument. The native field features, collection and control interface must still be acquired; bus closure alone does not supply them.

## Scientific decision and strongest comparisons

The initial route produced a rigorous 256-pulse bounded-sine ZZ gate. A strong exact bounded phase-winding kick comparator showed that boundedness and bus return alone were weak novelty targets. We moved to complete outgoing-field erasure, then to its causal realization. The exact state-uniform Weyl classification and optimal coherent isotropic completion are useful machinery, with close ancestry explicitly retained. The central advance of this tranche is the compatible passive receiver synthesis and its attained memory count.

A conventional coherent bright-span capture already stores at most n feature modes; the comparison is not merely against storing all time bins. The new receiver releases the measurable combinations into classical records and retains the prefix noncommutativity. Guo–Mueller–Liu's full Gaussian transformation compiler, Holevo's Gaussian-observable structure, ordinary Bell measurements and Bisio et al.'s classical-assisted quantum-memory theory are substantive starting points. Classical retirement and Gaussian Naimark dilation themselves are not new claims. Historical priority of the precise passive synthesis theorem remains unestablished.

## Constructed operation and a decisive adverse comparison

An explicit family with m peripheral qubits and one hub emits K=2m packets: first g(Z_j+iZ_hub), then g(-Z_j+iZ_hub). Its complex bright span has dimension m+1, but every unfinished prefix has symplectic rank two. A running-average interferometer uses one retained mode, two live modes, K-1 beam splitters and K homodyne outcomes. Four ordered conditional source displacements per edge produce the entangling phase; the receiver erases their remaining field information. A closed-form proof and rational algebra avoid numerical rank decisions.

The operation was then reconstructed for known pure memory loss, changing both source amplitudes and receiver mixing to maintain exact observed-output erasure. In a supplied independent-vacuum pure-loss model, all remaining inaccessible output channels are retained in a coherent-state Gram/Kraus description. A positive vacuum Kraus component bounds the complete source/reference/record error linearly in lost excitation; no-jump probability is not mistaken for total error. An opposite-label source superposition gives a matching first-order lower witness.

The equally informed comparator was strengthened during review. Three separate loss holds are not mandatory if each two-kick source block in the new operation is treated as lossless. A coalesced closed Weyl loop uses one hold, four kicks per edge, exact bus closure and no detector or fresh bus reset. At theta=pi/4, seven edges, per-hold transmissivity 0.999999, the long receiver schedule has actual half-diamond error >5.0697e-5 even with perfect detectors; the coalesced returning-bus workload has certified upper allowance <5.4978e-6. The conventional operation wins that compatible model comparison. At receiver efficiency 0.99999 the long schedule is enclosed between 0.0001606293 and 0.0001606487.

These are conditional model comparisons, not device error rates. The source-return permission, opposite packet routing, within-source-block losses, preparation, calibration, source memory/readout/reset and actual coupling delivery remain material. If source order is free, adjacent packet pairs shorten storage too, but their loss-matched amplitudes must be resynthesized using the m=1 formula; merely permuting the old tau^m pulses fails. The long accumulator is not selected as a superior gate architecture. Its role is an exact test of the broader receiver principle and its costs.

## Other completed assets and their exact scope

- **Bounded nonlinear gate:** 16 cells, 256 bounded-sine pulses, one initially independent vacuum oscillator retained throughout. Complete source/reference/bus half-trace allowance <0.000801379000384. Exact integer/rational arithmetic, Galerkin error and phase fitting are included. Independent replay and a different tail calculation accepted the result. The separate fresh-vacuum comparison is <4.019055856e-8 in reduced-source half-diamond distance and consumes 16 independent preparations/resets. Neither bound includes physical delivery or loss.
- **All-state Weyl erasure:** relative unitaries must commute. For the finite qubit alphabet, omega(f_i,f_j) in (pi/4)Z is exact, with a residual CZ cocycle that must be retained or paid. Ordinary homodyne uses the isotropic case. An all-input approximate eraser obeys ||[R_i,R_j]||<=16epsilon; its Weyl witness is not a finite-energy device lower bound.
- **Coherent isotropic completion:** H*=|iOmega|-iOmega attains minimum added feature norm Tr|iOmega| and rank(Omega)/2 added modes for this route. A 2n-1-kick palindrome preserves the intended source phase. The added source coupling is real extra machinery; an uncoupled detector ancilla is insufficient. Opposite-symplectic completion has direct Gaussian Naimark ancestry.
- **Two-bin complete instrument:** a passive Bell receiver with balanced loss gives an exact Pauli noise channel tensor its actual vacuum record. Calibration bounds retain records and therefore can be linear in mismatch even when reduced-source noise is quadratic. An explicit direct-homodyne comparator has independently reviewed complete-diamond and rigorous record witnesses; it is not claimed optimal over all receivers.
- **Analytic pulse compiler:** the larger finite-word construction remains preserved with author checks. The 345,000-pulse existence bound and free-word executable have not received the same independent executable audit as the 256-pulse certificate; do not promote their status by co-location.

## Proof, executable and actual-review map

| Result | Construction / executable | Actual review |
|---|---|---|
| Passive causal eraser | causal/PASSIVE_STREAMING_ERASER.md; passive_streaming.py; exact_feature_algebra.py; passive_streaming_results.json | reviews/causal_review/INDEPENDENT_REVIEW.md and receipt |
| Adaptive passive necessity | causal/ADAPTIVE_PASSIVE_NECESSITY.md | reviews/causal_review/ADAPTIVE_NECESSITY_REVIEW.md and receipt |
| Weyl criterion / coherent completion | eraser/CONTROLLED_WEYL_ERASURE.md | reviews/erasure_challenge/ROOT_PROOF_REVIEW.md |
| Approximate all-input obstruction | reviews/erasure_challenge/INDEPENDENT_DERIVATION.md, Section 6 | ROOT_REVIEW_APPROXIMATE_OBSTRUCTION.md alongside it |
| Same-bus nonlinear gate | schur/CERTIFIED_ANGULAR_CELL.md; certify_angular_cell.py; angular_exact.py | reviews/pulse_review/INDEPENDENT_REVIEW.md and independent_audit.py/json |
| Two-bin receiver / calibration | eraser/TWO_BIN_OPERATION.md; two_bin_checks.py/json | reviews/erasure_challenge/TWO_BIN_REVIEW.md and receipt |
| Full-record direct comparator | reviews/erasure_challenge/NO_MEMORY_COMPARATOR.md; no_memory_checks.py/json | ROOT_REVIEW_NO_MEMORY_COMPARATOR.md alongside it |
| Star source operation / complete loss comparison | star/STAR_OPERATION.md; star_checks.py/json | reviews/erasure_challenge/STAR_REVIEW.md and independent loss-Gram checks |
| Energy-restricted approximate compilation | eraser/ENERGY_RESTRICTED_COMPILATION.md | See reviews/causal_review/ENERGY_RESTRICTED_REVIEW.md for current verdict |

Proof headers preserve their status at authorship; later version-pinned reviews supply the current verdict. The star reviewer contributed the stronger comparator and lower-witness challenge, which are disclosed as collaborative ingredients rather than two independent origins. The independent Gram construction and exact replay are separately recorded.

Executed: all seven causal compiler cases; exact non-saturated/saturated pair and refinement audits; exact 256-pulse replay; 12 star parameter cases and strong conventional comparisons; 18 independent rational loss-Gram cases with 378 source-label patterns; outward two-bin/direct-record certificates. The causal compiler's <=2.13e-15 floating residuals are diagnostics, not physical error certificates. Its exact input ranks/algebra and theorem are separate. Scalar star/two-bin enclosures use exact rational arithmetic, integer square roots and rigorous series.

The exact certificate scripts use Python's standard library. The general floating receiver compiler additionally uses NumPy/SciPy. Reviews already contain independent replays. Preserve frozen files when rerunning: use an alternate output path where supported or a temporary working copy. No computation or download is promised after this checkpoint ends.

## Frontier retained for the next attack

The exact rank theorem now has a constructive energy-restricted approximation interface: project actual features onto a delivered receiver's real measured subspace, retain the controlled Weyl phase, and bound the full instrument using a common number moment. This prevents tiny nonzero symplectic singular values from being mistaken for hard finite-error storage requirements. A small two-bin feature can be measured with zero retained quantum modes at a quantified nonzero error, while its exact rank still demands one. At fixed interaction-generated gate angle, shrinking that feature can increase the other coupling and loss/calibration costs; no free capability is inferred.

The strongest next opening is to make receiver design depend jointly on admitted state/energy, required operation, collection and storage loss, rather than exact rank alone. This is a research frontier, not a claim of execution in the background. The current tranche has already constructed and tested the exact principle, a finite-error interface, a compatible source operation and its adverse strongest conventional comparison.
