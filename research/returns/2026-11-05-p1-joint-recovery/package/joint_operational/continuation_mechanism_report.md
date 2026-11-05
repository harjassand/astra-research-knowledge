# Operational continuation: finite-memory controls, feedback, and initialized frames

## Outcome

This continuation supplies executable causal CPTP control families and a reproducible optimization of their actual input-reference recovery channel. It does not establish the requested optimal joint memory law. The controls tested so far improve several small-memory benchmarks, but none approaches high-fidelity recovery at the quartic collection horizon. The numerical results below are attainable finite-model policies, subject to the stated numerical precision, rather than converse bounds or certified global optima.

The exact inverse-buffer construction and its routed physical implementation remain the complete recovery benchmark. They are described in `operational_report.md`, with independent density-matrix validation in `verify_routed.py` and `routed_verification.json`. This continuation does not replace that benchmark's guarantee with a source-forgetting criterion or with joint source-plus-memory preservation.

## 1. Exact terminal objective and causal control optimization

The simulated object is the normalized Bell-input state on the inaccessible input reference R, inaccessible source S, and retained receiver memory M. The receiver map at step j acts only on M and the newly emitted carrier E. Preparing the independent memory in a known pure or mixed state is allowed. The source action is always the prescribed partial SWAP, with the same angle on every fresh tracial carrier.

For a memory dimension m, a nonselective stage is represented by its Choi matrix J, of size 2m² by 2m², using the convention

    J[i,α;j,β] = Λ(|α><β|)[i,j],
    J >= 0,   Tr_output J = I_(2m),

where α,β index the actual M⊗E input. The propagated joint state and a backward terminal cost make each individual map update a semidefinite program. The final M→Q decoder is itself optimized by SDP. Forward and backward sweeps optimize one stage at a time while keeping the other stages fixed.

The objective is the final Bell entanglement fidelity after discarding S. Neither S nor R is physically measured or made available. They appear only in the offline model used to select an input-independent receiver policy. The matrices can be stored before the unknown input arrives and executed using only the time index and permitted classical record.

Source covariance gives an exact operational conversion from this objective to diamond error. Pick a single random Clifford g, apply it to every incoming carrier before the chosen receiver, and undo g on its final qubit. Keep g as a classical label. The resulting logical channel is depolarizing, has the same Bell fidelity F_e, and has half-diamond error exactly 1−F_e. Thus each reported Bell fidelity is an achievable twirled-channel error, not just a state-fidelity surrogate. This twirl also applies to asymmetric initialized frames and feedback instruments.

The search is nonconvex in all stages together. Coordinate ascent, with monotonicity checked to numerical tolerances, supplies feasible policies; it does not certify the global optimum or rule out another initialization, larger memory, more classical outcomes, or a more general channel class.

### Numerical checks

`control_search.py` checks the adjoint and Choi objective against direct density-matrix evaluation. With one carrier and m=2 or m=4, it reproduces the exact optimum

    F_e = 1/4 + (3/4) sin² θ.

With two carriers and m=4, it matches a separate unrestricted decoder on the entire two-carrier output. The tests cover θ=.3 and .7. Their discrepancies are below 10⁻⁷. The physical line inverse decoder was separately checked in sixteen cases, with maximum Choi-entry residual 2.78×10⁻¹⁶.

Every SDP proposal is projected onto the positive cone and normalized to restore exact trace preservation at the mathematical matrix level. Its objective is reevaluated after this correction. A materially decreasing update is rejected. Final files record trace-preservation residuals, Choi eigenvalues, state trace and positivity, and reference-marginal checks. Solvers sometimes report reduced numerical accuracy; the repaired policies and direct objective, rather than the raw solver objective, are used. Decimal results should be interpreted as numerical diagnostics to roughly 10⁻⁶, not interval-arithmetic certificates at a sharp threshold.

## 2. Nonselective one- and two-qubit controllers

The unrestricted nonselective m=2 search was run from both a first-carrier capture policy and random near-identity unitary channels. At θ=.7,N=12 both converge to F_e≈.741656403. The recovered policy from the symmetric capture initialization is a full initial capture followed by partial-SWAP readers with decreasing angles:

    1.570796, .634383, .376100, .234594, .146312, .090013,
    .054553, .032660, .019384, .011438, .006724, .003943.

For every stage after the initial capture, the adjoint maps the output Pauli vector to

    α σ_M + β σ_E + γ (σ_M × σ_E),

with α+β=1 and (α−β)²+4γ²=1 to numerical precision. This identifies an executable unitary partial-SWAP channel. It is consistent with the known restricted tracial-reader obstruction; it is not a new unrestricted lower bound.

At quartic-scale horizons, the same initialization produces recovered Bloch visibilities approximately 1.85 sin²θ at θ=.5, 2.14 sin²θ at θ=.3, and 2.27 sin²θ at θ=.2. This is evidence of failure of these optimized basins at weak angle. It does not prove that all initialized or measured one-qubit receivers share that scaling.

For m=4, the full Choi SDP reaches F_e≈.818789 at θ=.7,N=12 from a random initialization. Other starts reach .816132 and .814445. These improve on one-qubit memory, but remain well below the full-output inverse-buffer fidelity. Their distinct final values also demonstrate that the coordinate method should not be treated as a global optimizer.

## 3. Explicit finite classical-state feedback

`feedback_control.py` extends the search to a receiver with m-dimensional quantum memory and C classical controller states. At each step, for each current label x, it chooses an instrument with CP maps

    J_(x→y) >= 0,   Σ_y Tr_output J_(x→y) = I_(2m).

The exact unnormalized RSM state is propagated separately for every retained classical label. The backward cost is also label dependent. Each instrument update is one SDP, and the final decoder is optimized separately for each final label. Classical labels are never silently treated as coherent quantum memory.

This is a real physical feedback architecture. A map selected after outcome y can differ from the map selected after another outcome. The implemented class intentionally uses only the retained label x and time j; it may forget other historical information. It therefore lies inside, rather than exhausts, the allowed unlimited-record model. The C=1 limit reproduces the nonselective implementation, and C=1,2,4 all reproduce the exact one-carrier optimum.

Two classical states improve the one-qubit-memory fidelity to approximately .763939 at θ=.7,N=12, .579979 at θ=.5,N=37, and .393048 at θ=.3,N=262. Four classical states reach .597247 at θ=.5,N=37 and .404685 at θ=.3,N=262. These are exact average-channel calculations over all classical outcomes, not Monte Carlo trajectories. The weak-angle runs do not show a recovery mechanism approaching identity.

The feedback maps are not merely re-labeled nonselective readers. Some optimized branches have single Kraus operators, while others use higher-rank CP maps or suppress a transition. A simple universal unitary policy was not extracted from them. Their finite matrices nevertheless define executable CPTP instruments.

## 4. Payload qubit times a spin gauge

The prior Schur work already introduced coherent qubit×spin memory, its small invariant-state representation, and its physical CG implementation. Both prior files were read before extending that family: `joint_root/inputs/FUSION_THEORY.md` and `joint_root/inputs/PURE_BASELINE_AND_FINAL_STATUS.md`. The extension here is the terminal Bell-cost optimization with a final optimized decoder, not the claim that qubit×spin memory or the representation is new.

The retained system is

    M = C²_payload ⊗ Q_J,   dim M = 2(2J+1).

The stage channel class is SU(2) covariant and has Stinespring environment spin 1/2, with arbitrary multiplicity. It includes every SU(2)-covariant unitary on M⊗E followed by discarding E, and also irreversible channels implemented with independent ancillary systems. For J≥1 its Choi operator is fully specified by one positive 6×6 multiplicity matrix, subject to linear trace-preservation constraints. For J=1/2 the matrix is 5×5.

`rep_control.py` constructs the physical irreducible basis, exact Kraus operators, and minimal trace-preservation constraints. Forward propagation, adjoint propagation, and the SDP objective are evaluated from these Kraus operators; no formal operator compression is substituted for carrier erasure. `spin_gauge_control.py` applies this representation to the actual collision model. Dense-map, adjoint, objective, and trace-preservation tests pass at J=1/2,1,2, with residuals below 10⁻¹⁰.

The first carrier is captured into the payload factor. The gauge was tested both tracial and independently pure. For the asymmetric variants, the final decoder is unrestricted rather than forced to be covariant. Pure north-pole states, a coherent extremal-state superposition, and a generic pure state are supported by the implementation. The executed large-frame tests used north-pole and generic pure states; no claim is made that this exhausts useful initialized resources.

At θ=.5,N=37, optimized fidelities include .680136 for J=1 tracial, .674551 for J=2 tracial, and .689547 for J=2 initially pure north. At θ=.3,N=262, J=2 gives .472572 tracial and .477099 pure north. Raising the tested pure gauge to J=4 did not improve the .5-angle results. These experiments do not establish a uniform J bound. In particular, the earlier approximation of a large invariant spin register by a classical orientation cannot be applied without its invariance premises to a large asymmetric pure initialization.

## 5. Coherent regular frame and matched pure cascade

Two further starts were tested after exchanging actual constructions with the other researchers.

The regular-frame test retains the integer-spin sectors j=0,1 and their right multiplicities:

    M = Q_0 ⊗ C¹  ⊕  Q_1 ⊗ C³,   dim M=10.

Both spin-sector coherence and right-multiplicity coherence are kept. The independent pure frame is localized near the identity by amplitudes proportional to 2j+1 on the maximally entangled left/right vector in each sector. This is a finite regular SO(3) frame, not a lone spin or a measured J label. It is narrower than an unrestricted large SU(2) rotor.

The initial receiver gate is the physical matched collective interaction

    exp[i θ (J_left · σ_E + I/2)].

The subsequent optimization again uses the actual terminal Bell fidelity and an unrestricted decoder. Each stage is a covariant CPTP map in the environment-spin-1/2 class, now with a 25×25 multiplicity cone. `rotor_control.py` implements it. A one-carrier optimization approaches the known one-carrier bound. At θ=.5,N=37 the six-sweep run reaches F_e≈.611760. This is recovery from M alone after S is discarded; it is not a statement that the frame merely protects a relative state on S⊗M.

The matched-cascade start was supplied by the independent channel constructor. Memory consists of k physical receiver qubits in |0,+,(+i)> and each outgoing carrier undergoes the same-angle partial SWAP with each memory qubit in order. It is then discarded. This source-specific pure initialization has a nonzero weak-angle limiting signal, so the θ² signal behavior observed in the capture-start experiments cannot be generalized to all initialized receivers.

`cascade_control.py` reproduces that fixed policy before optimizing it. Its complete source-plus-memory Pauli signal agrees with the independent channel-power code to below 2.4×10⁻¹⁵ for k=2 and k=3 in the validation case. The final decoder remains unrestricted. For k=3 the physical covariant stage class has a 14×14 environment-half multiplicity cone. The k=2 control run at θ=.3,N=262 reaches F_e≈.338696; k=3 at θ=.5,N=37 reaches .477874. The k=3 weak-angle run at θ=.3,N=262 reaches .432724 after ten sweeps. No high-fidelity trend was established in these searches.

## 6. The positive loss ledger identifies what fails in the tested policies

The root's exact general acquisition ledger was evaluated independently on the saved states. Let a_j be acquired balanced-Petz visibility and q_j the remaining source-traceless norm. With b=sin⁴θ and r=1−b, actual receiver losses obey

    a_j = a_(j−1) + b q_(j−1) − ellP_j,
    q_j = r q_(j−1) − ellQ_j,

and

    a_N = 1−r^N−Σ_j[ellP_j+(1−r^(N−j))ellQ_j].

`policy_ledger.py` evaluates the balanced norms from the full Choi states, including nontracial receiver averages. For classical feedback, the norms are evaluated on each unnormalized label block and summed, as required by the direct-sum reference state. The exact ledger residuals and loss nonnegativity agree to about 10⁻¹⁵ in the checked examples.

At θ=.3,N=262:

- The one-qubit nonselective capture-start policy has final a≈.03477. Its q falls below 1/2 by step 6 and below 1/10 by step 17.
- The two-label one-qubit feedback policy has final a≈.03638, with the corresponding steps 7 and 17.
- The J=2 tracial-gauge policy has final a≈.08807, with steps 13 and 42.
- The J=2 pure-north gauge has final a≈.09182, with steps 14 and 44.

The full-output quartic acquisition process would still have q≈.9 after such short prefixes. These receivers spend their remaining joint source information much too early. This is the failure mechanism of the tested policies. It is not a general lower bound on arbitrary coherent frames or histories.

For the best unrestricted m=4 run at θ=.7,N=12, a≈.576088. The ledger's all-final-decoder lower error is about .180746, while the optimized decoder achieves .181211. Thus that example's main deficiency is its retained channel, not an obviously poor final readout.

## 7. Paid operation and resource account

All policies above use one fresh emitted carrier at a time. Their retained quantum space is exactly the specified memory M; a classical controller label or global Clifford choice is classical. A numerical map is made concrete by a Choi eigendecomposition, Kraus realization, and a Stinespring isometry. The hidden source and reference used in offline optimization do not enter that physical realization.

For a generic m-dimensional memory and C classical outcomes, the total number of refined Kraus outcomes at a stage is at most 2 C m². A direct dilation must count its environment and independent initialized ancillas. An alternative binary measurement-tree realization uses the memory, current carrier, and one measured ancillary qubit. Each final branch has rank at most m, so a physical unitary compresses it back to M before releasing the carrier. For m encoded in q=ceil(log₂m) qubits, this gives q+2 live qubits before routing or additional arithmetic workspace. Subspace padding is extended by an arbitrary CPTP operation off the known code space. No input carrier is erased merely because a tensor description is small.

Dense generic controls have nontrivial synthesis cost. A conservative direct dilation has polynomial cost in m and C per stage; serial binary implementation trades coherent environment space for measured steps and classical lookup. The finite time-dependent tables contain O(N C² m⁴) complex coefficients in the generic feedback representation. This is classical data and offline work, not free quantum processing. The alternating SDPs are also an offline computational cost, and may become prohibitive as m,C or the horizon grow.

The restricted qubit×spin channels have a more structured implementation. Their Stinespring intertwiner has an environment spin 1/2 and at most six multiplicity copies. Adding or removing the few spin-1/2 factors uses CG transforms; the intervening multiplicity isometry has constant dimension. Binary-encoded spin arithmetic and controlled rotations therefore give a definite implementation without granting native arbitrary-spin Hamiltonians. Arithmetic registers, a carrier, and all unmeasured ancillas still count. The reported scripts simulate these operations as matrices; they are not compiled device circuits.

The regular-frame experiment retains growing right multiplicities. At larger cutoff its arbitrary optimized multiplicity controls would grow with the cutoff. No polylogarithmic synthesis cost or near-linear overall processing theorem is claimed for that extrapolation.

Let the arrival interval be Δ and a compiled update take τ. If τ≤Δ, the small-memory receiver can service the stream with its stated workspace. If τ>Δ, it cannot parallelize successive updates to the same unknown memory without changing the protocol. An input queue accumulates, of order N(1−Δ/τ) carriers at the end of collection in the deterministic-clock model. Those carriers are quantum memory. Finishing the computation after the stream does not remove that storage obligation.

Independent frame preparation must finish before the relevant arrivals or pay for that queue. The product-frame preparations are simple single-qubit rotations. The north-pole spin state is a known computational basis state of the encoded spin. A generic pure frame may need order its dimension in synthesis work; it is not free. The regular left/right-entangled frame requires the stated superposition and entanglement preparation.

A conservative implementation budget is

    εideal + εpreparation + εsource-calibration + εcontrol + εstorage + εdelivery ≤ ε.

If each physical stage, including its classical outcome, is approximated in half diamond norm by δ, the adaptive composition error is at most Nδ. Choosing δ=O(ε/N) is sufficient when an ideal policy leaves a margin. The same hybrid reasoning gives an O(N|η|) worst-case source-angle mismatch bound. This is a sufficient precision prescription, not an assertion that calibration exposure or arbitrary control synthesis is free. Gate-set compilation, arithmetic precision, resetting and reading flags, and policy lookup must satisfy the service-time premise.

Protection costs require a noise and hardware model. Under a specified threshold architecture the memory-time and gate locations of these circuits can be converted to physical qubits and code cycles. The ideal CPTP input specification alone cannot supply a universal protection or routing cost. In particular, constant retained logical memory is not by itself a complete physical memory claim if the controller cannot keep up.

## 8. Scope of the completed result

This continuation has operationalized three previously distinct issues: fully general nonselective finite-memory controls; genuine finite-state measurement feedback; and initialized coherent frame controls evaluated against the actual source-to-output channel. It has also identified where the tested policies lose acquisition potential using the exact positive ledger.

It has not earned a new asymptotic memory or processing law. Small-memory numerical successes are feasible benchmarks; failures of local searches are not obstructions. The large-frame, large-history, low-loss control problem remains open here. The exact passive inverse construction supplies the full-recovery upper bound, while the accepted all-decoder and prefix converses retain their stated scopes.

The completed-result tables and file manifest below contain exact run parameters and paths. The saved NPZ policies are replayable numerical CPTP specifications. Multiplicity-coordinate policies also store their explicit physical Kraus bases, so a different SVD/null-space convention cannot change the implemented channel. `materialize_replay_bases.py` checks those physical bases against the saved state evolution; `replay_policy.py` executes the policies directly from the saved arrays, with positive projection and input normalization giving a defined CPTP realization. The accompanying JSON files contain objective histories and physicality residuals.

<!-- COMPLETED_RESULTS -->

## Completed numerical results

| Receiver | θ | N | m (qubits) | C | F_e | Twirled error | Passive-buffer F_e |
|---|---:|---:|---:|---:|---:|---:|---:|
| Unrestricted nonselective; capture start | 0.7 | 12 | 2 (1) | 1 | 0.74165640 | 0.25834360 | 0.92238903 |
| Unrestricted nonselective; capture start | 0.5 | 37 | 2 (1) | 1 | 0.56826868 | 0.43173132 | 0.89933315 |
| Unrestricted nonselective; capture start | 0.3 | 262 | 2 (1) | 1 | 0.38984508 | 0.61015492 | 0.89909665 |
| Unrestricted nonselective; capture start | 0.2 | 1283 | 2 (1) | 1 | 0.31714303 | 0.68285697 | 0.89852587 |
| Unrestricted nonselective; capture start | 0.7 | 12 | 4 (2) | 1 | 0.81613152 | 0.18386848 | 0.92238903 |
| Unrestricted nonselective; random start | 0.7 | 12 | 4 (2) | 1 | 0.81878897 | 0.18121103 | 0.92238903 |
| Unrestricted nonselective; second random start | 0.7 | 12 | 4 (2) | 1 | 0.81444523 | 0.18555477 | 0.92238903 |
| Two-state feedback; capture start | 0.7 | 12 | 2 (1) | 2 | 0.76393894 | 0.23606106 | 0.92238903 |
| Two-state feedback; random start | 0.7 | 12 | 2 (1) | 2 | 0.75960312 | 0.24039688 | 0.92238903 |
| Two-state feedback | 0.5 | 37 | 2 (1) | 2 | 0.57997948 | 0.42002052 | 0.89933315 |
| Two-state feedback | 0.3 | 262 | 2 (1) | 2 | 0.39304809 | 0.60695191 | 0.89909665 |
| Four-state feedback | 0.5 | 37 | 2 (1) | 4 | 0.59724658 | 0.40275342 | 0.89933315 |
| Four-state feedback | 0.3 | 262 | 2 (1) | 4 | 0.40468521 | 0.59531479 | 0.89909665 |
| Payload × spin-1/2 gauge, tracial | 0.7 | 12 | 4 (2) | 1 | 0.81628860 | 0.18371140 | 0.92238903 |
| Payload × spin-1/2 gauge, tracial | 0.5 | 37 | 4 (2) | 1 | 0.62432141 | 0.37567859 | 0.89933315 |
| Payload × spin-1 gauge, tracial | 0.5 | 37 | 6 (3) | 1 | 0.68013567 | 0.31986433 | 0.89933315 |
| Payload × spin-2 gauge, tracial | 0.5 | 37 | 10 (4) | 1 | 0.67455136 | 0.32544864 | 0.89933315 |
| Payload × spin-2 gauge, pure north | 0.5 | 37 | 10 (4) | 1 | 0.68954708 | 0.31045292 | 0.89933315 |
| Payload × spin-4 gauge, pure north | 0.5 | 37 | 18 (5) | 1 | 0.64299496 | 0.35700504 | 0.89933315 |
| Payload × spin-4 gauge, generic pure | 0.5 | 37 | 18 (5) | 1 | 0.58967601 | 0.41032399 | 0.89933315 |
| Payload × spin-2 gauge, tracial | 0.3 | 262 | 10 (4) | 1 | 0.47257248 | 0.52742752 | 0.89909665 |
| Payload × spin-2 gauge, pure north | 0.3 | 262 | 10 (4) | 1 | 0.47709943 | 0.52290057 | 0.89909665 |
| Coherent regular SO(3) frame, j=0,1 | 0.5 | 37 | 10 (4) | 1 | 0.61176045 | 0.38823955 | 0.89933315 |
| Two-qubit pure matched-cascade start | 0.3 | 262 | 4 (2) | 1 | 0.33869552 | 0.66130448 | 0.89909665 |
| Three-qubit pure matched-cascade start | 0.5 | 37 | 8 (3) | 1 | 0.47787402 | 0.52212598 | 0.89933315 |
| Three-qubit pure matched-cascade start | 0.3 | 262 | 8 (3) | 1 | 0.43272419 | 0.56727581 | 0.89909665 |

Here m counts the retained coded quantum space. The generic serial physical realization additionally counts the current carrier and a measured ancillary qubit; arithmetic, routing and queues can add more. C is the number of retained classical controller labels. Frame and cascade searches have C=1 and are restricted covariant-control searches with the stated initial states.

All selected runs completed. The largest selected trace-preservation residual is 6.15e-13; the smallest selected repaired CP eigenvalue is -1.54e-15.

## Reproducibility and file map

- `numerical_summary.json`: complete selected-run parameters, fidelities, physicality residuals, and exact paths to replayable NPZ policies and JSON histories.
- `control_search.py`, `control_selftest.json`: unrestricted nonselective coordinate SDPs and short-horizon validation.
- `feedback_control.py`, `feedback_selftest.json`: finite classical-state instrument optimization and validation.
- `rep_control.py`: arbitrary physical SU(2) representation blocks, CPTP constraints, Kraus propagation, and scalar/multiplicity optimization.
- `spin_gauge_control.py`, `spin_gauge_selftest.json`: fixed-J tracial and asymmetric initialized gauges.
- `rotor_control.py`: coherent regular-frame control, including right multiplicities.
- `cascade_control.py`: independently pure matched-cascade starts with all stages optimized; propagation cross-checked against the independent channel constructor.
- `policy_ledger.py` and the `*_ledger.json` result files: balanced-Petz acquisition and irreversible-loss diagnostics.
- `covariant_control.py`, `covariant_selftest.json`: the first tensor-qubit Schur-block implementation. Its early exploratory searches are not used as the primary performance benchmarks when the later representation implementation supplies a stronger run.
- `build_numerical_summary.py`: regenerates this selected-run table from saved results.

Examples from the present directory:

```bash
python control_search.py --self-test
python control_search.py --m 4 --theta .7 --n 12 --sweeps 12 --init 'random:0.5' --solver SCS --tol .000001 --out results/replay_nonselective
python feedback_control.py --m 2 --C 2 --theta .3 --n 262 --sweeps 12 --init 'random:0.1' --out results/replay_feedback
python spin_gauge_control.py --j 2 --gauge-state north --theta .3 --n 262 --sweeps 12 --init 'random:0.1' --out results/replay_gauge
python rotor_control.py --cutoff 1 --theta .5 --n 37 --sweeps 6 --initial identity --seed-policy matched --solver SCS --tol .0000001 --out results/replay_rotor
python cascade_control.py --k 3 --theta .3 --n 262 --frame triad --sweeps 10 --out results/replay_cascade
```

The scripts use NumPy, SciPy and CVXPY with CLARABEL/SCS. They cap numerical-library threads at one so concurrent cases do not silently oversubscribe the host. Exact solver versions and hardware can change runtime and the local basin reached. The saved policies, rather than a claim of unique optimizer output, are the reproducible operation.


## Separate operational consequence of the exchanged three-site projection

`three_site_packing_extension.md` proves input-independent iid rank-label statistics and a grouped coherent codec for the algebra constructor's rank-2/rank-6 triple projection. Conditional on that constructor's exact b,h acquisition formula, it gives a valid overflow-abort diamond budget, packed data rate approaching .7295739585 qubits per original carrier, O(L) temporary quantum space, and O(NL) addressed arithmetic for groups of L triples. Routing and service queues are charged separately. This is a constant-factor storage improvement for targets above that projection's error floor, not a new theta exponent or an arbitrary-accuracy decoder. The projector/acquisition calculation belongs to the separate algebra construction; this file supplies its operational packing consequence.


Reproduction no longer depends on reconstructing an arbitrary SU(2) multiplicity basis: explicit base operators are saved in all thirteen selected representation-coordinate policies. The anchored-basis checks have zero state residual in the checked stages. `replay_checks.json` contains full replay comparisons for the unrestricted, feedback, tracial-gauge, asymmetric-gauge, regular-frame and cascade families. `runtime_versions.json` records the numerical software versions. All scripts are portable within this directory; source code contains no hard-coded workspace paths.

The six full replay comparisons have maximum final-state trace-norm discrepancy `1.093e-13`; their Bell fidelities agree to numerical roundoff. `cg_half.py` additionally gives an explicit real Clebsch–Gordan phase convention and payload/gauge fusion paths, with completeness and generator-intertwining checks. It is a deterministic helper, independent of the saved numerical multiplicity bases.

## Exact check of the central-limit / streaming-Schur continuation

`clt_block_analysis.md` completes a separate exact theorem for the standard real-path streaming Schur instrument. Even retaining all classical path labels and the final quantum spin, this instrument erases the ordered-area vector `Y=sum_(i<j) sigma_i cross sigma_j`. For a block of `b` carriers it loses at least `g_b q` of the source-traceless ledger, where `g_b=b(b-1) cos(theta)^(4b-4) sin(theta)^4 / 2`. The proof isolates a weight-two, reversal-odd component, proves orthogonality to every symmetric and different-weight contribution, and extends to an arbitrary old-memory coefficient Gram matrix. It uses no small-angle remainder.

Repeated independent blocks obey `a_infinity <= (1-r^b)/(1-r^b+g_b)`. Exact finite inequalities give the uniform joint asymptotic `2/(b+1) [1+O(b sin(theta)^2)]` when `b theta^2 -> 0`. Thus the logarithmic-memory weak-Schur primitive does not meet the required `o(b theta^4)` block-loss scale. This is a restricted obstruction, not a no-go for an instrument coherently retaining suitable multiplicity or ordered-area information. Kuperberg's tracial CLT and Cervero-Martín/Mančinska's weak-Schur algorithm are explicitly attributed and their original tasks kept distinct from recovery. `schur_block_obstruction.py` and `schur_block_checks.json` validate the physical channel, exact signal coefficient, and lower bound for twenty small-block cases.
