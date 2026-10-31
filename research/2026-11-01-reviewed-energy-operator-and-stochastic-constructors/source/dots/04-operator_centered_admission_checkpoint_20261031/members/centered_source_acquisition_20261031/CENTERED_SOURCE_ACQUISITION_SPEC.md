# Executable source-derived charges and centered-creation admission

31 October 2026. Candidate specification; independent review pending. The old guarded compiler and its files are unchanged. This is exact known-model analysis, not physical calibration, a gate backend, an optimal stability solver, or a new threshold.

## 1. Two separate earned operations

1. `acquire_centered_certificate.py` proposes charges from supplied SOURCE jumps, checks centered coupling compression, then finds and verifies a full source drift certificate.
2. `receive_centered_schedule.py` checks a complete external static gate/idle schedule and receives that certificate using `GENERAL_DRIFT_CLAMPED_RECEIVER.md`, including its acquired diagonal-to-gap parameter D.

A successful first operation alone is not small-error admission. The second may still return NOT_ADMITTED because the physical coupling, time, activation, D/kappa conditioning, residual controls or arithmetic budget are inadequate.

The components reuse the frozen rational matrix/LP functions in
`raw_local_operator_acquisition_20261031/acquire_operator_certificate.py`, SHA256
`35acdcdcc533f523cc78c558153f97fcb800711bbd4ff0f57b8a2ea50d60ee35`,
and the frozen schedule support checker
`local_energy_fault_admission_20261031/acquire_local_admission.py`, SHA256
`a7bc4e513cb4de03a3ef5c504bae75b7b464cb4985a9a683cd560f9d439136f8`.
Both bytes are hash-checked. Their prior proofs/reviews are dependencies, not replaced or upgraded here. Exact complex-rational normalization includes the earlier reviewed Schur/projector correction.

## 2. Input and actual charge proposal

A centered specification contains:

- format `source-derived-centered-certificate-v1`;
- `operator_model`, with the frozen raw finite-matrix schema: cell dimensions, all actual local Hamiltonians and positive-rate dissipators, actual Hermitian source coefficients times explicit system Pauli strings, requested gap/activation cap, task binding and matrix/LP budgets;
- `candidate_budget`: maximum subset size, subsets checked per cell, joint candidates and LP attempts.

Only actual POSITIVE-rate ONE-CELL jump matrices are used to propose that cell's P. Enumerate the empty subset, then subsets in increasing cardinality and input-index lexicographic order, up to the declared size/count limits. The empty subset proposes P=I; it passes centering only if all corresponding coupling coefficients vanish. For a subset of jumps L_j, stack their matrices, compute an exact rational complex nullspace basis X and form

 P=X(X^dagger X)^(-1)X^dagger, Q=I-P.

A zero kernel is discarded. Test the projector identities and L_j P=0 exactly. For EVERY actual coupling coefficient B on that cell, require P B P=0. Unlike the old guarded mode, B P need not vanish. Nonzero ground compression is REJECTED from this candidate catalog, not averaged away, subtracted as an unpaid mean or called small merely because loss is rapid.

Equivalent P matrices are deduplicated in their exact canonical rational representation. All subset trials count, including failed centering, zero kernels and duplicate projectors. Subset size is at most8; this implementation additionally limits the other candidate-budget numbers to10000. These are finite implementation limits, not a claim that a larger search is physically impossible. A local source Hamiltonian is not silently treated as a loss proposal. A multi-cell jump is not silently collapsed to a favorable one-cell jump. Such models may return UNKNOWN even if another acquisition method could succeed.

The catalog does not claim that the proposing jump subset alone is the source generator. Its only role is to propose P. Every term of the actual `operator_model` is subsequently included in the Bernstein drift check, including raising, recycling and coherent source-creating terms that were not selected for the proposal.

## 3. Bounded finder and optimizer-independent checker

For each joint tuple of retained local charges, in deterministic Cartesian order, call the frozen local polynomial/DD-cone LP construction with THESE Q_i, not the old coupling-kernel Q_i. The requested gap and activation cap are unchanged. The maximum number of tried tuples is the minimum of the joint-candidate and LP-attempt budgets. Every actual LP call also has its inherited variable/constraint and wall-clock budget. Preprocessing, catalog construction and exact verification are separate paid work, not hidden inside that timer.

The LP finds local M^e and activation allocations. The independent checker reconstructs

 F_e=sum_i(M^e u)_i Q_i product_(j!=i)(I+u_jQ_j)
       +sum_i a_i^e u_i V_e-G_e^dagger(V_e)

from ALL supplied local matrices. It verifies every degree2 tensor-Bernstein coefficient by exact singular-safe rational PSD elimination, and verifies global Metzler signs, both row and column margins and activation caps. It does not trust a numerical optimizer status or merely favorable subset dynamics. Valid supplied PSD allocations outside the DD search cone may be checked.

The record binds the external centered specification, task, exact proposing jump references, selected catalog indices, projectors, coupling norm bounds and allocations. Catalog summaries and the candidate's Cartesian position are recomputed. Position must lie within the declared attempt limits. These fields describe a reproducible finite search envelope/proposal position, not a cryptographic attestation of elapsed execution history or proof that every earlier candidate failed. The verifier never needs to trust such a history to validate the accepted local inequalities.

CERTIFIED means these exact properties passed. UNKNOWN means no certificate was found within the stated sound-incomplete search. It includes no centered candidate, sufficient-cone failure and search exhaustion. UNKNOWN is not a general instability/impossibility statement. Malformed input is REJECTED separately. The verifier accepts successful exact certificates only, not an UNKNOWN record as physical admission.

## 4. Cost and precision of acquisition

For cell i with N_i positive-rate one-cell jumps, the untruncated subset catalog has

 sum_(r=0)^min(N_i,s) binom(N_i,r)

proposals. The actual number tested is capped before enumeration exceeds the declared budget. Each trial is an exact local nullspace/Gram/projector computation at the supplied bounded cell dimension; coefficient bit lengths and rational growth are real costs. If C_i candidates survive, at most min(product_i C_i, joint budget, attempt budget) joint tuples are tried. No product of source Hilbert dimensions is enumerated.

Each tuple incurs the local Bernstein/LP construction and exact postcheck already described in the raw frontend. Its matrix count is sum_e3^|e| with actual local matrix sizes. SymPy1.14.0 exact simplex is an ordinary component, NOT asserted polynomial-time in the worst case. The checker costs exact local linear algebra plus global matrix/row/column assembly; the current code uses a dense matrix on CELL INDICES for M, not a dense Hilbert-space matrix, so its cell-count memory is quadratic and is charged. Explicit graph/operator inspection is not free.

The implementation does not acquire unknown spectator operator bounds. Its matrices are fully supplied finite operators. The separate shared-spectator theorem requires an explicit bounded expansion/norm certificate; there is no omitted E dimension masquerading as an executable guarantee here.

## 5. Complete external schedule and aggregate coupling norm

The receiver input contains a centered specification and valid certificate, a separately supplied schedule/task/amplitude budget, and arithmetic budgets. Task IDs and contract hashes must agree. It recomputes

 kappa=min(negative row sums,negative column sums),
 D=max_i(-M_ii), a=max_i sum_e a_i^e.

For each actual Hermitian source coefficient B, a rational row-sum norm upper is already acquired. At each active(cell,location), the receiver SUMS these norm bounds over ALL its declared Pauli terms. The resulting c bounds the TOTAL unwanted operator, not each summand with an uncharged multiplicity. Complete system patch supports, every idle, simultaneous-source incidence and actual static intended gate/control-error inputs are checked.

To reuse these schedule checks, a scalar loss=kappa, zero-transport, injection=a envelope is constructed internally. This is SUPPORT/NORM BOOKKEEPING ONLY. It is NOT a physical source replacement and its annihilating-guard error bound is never used for centered X-type couplings. The new clamped formula is evaluated separately. The output names actual source cell dimensions rather than labeling arbitrary cells as physical qubits.

Only when exact B P=0 holds for every coefficient on the selected charges does the output also expose a separately labeled `guarded_alternative`. The old general product-weight guarded receiver then genuinely applies to the same verified charges/drift. This can be far cheaper. It does not change the centered status, and is not asserted applicable merely because P B P=0. The original guarded compiler remains unchanged and available.

This executable schedule interface supports the frozen component's explicit static Pauli-Hamiltonian gates/idles. It does not implement arbitrary adaptive instruments, prepare physical sources, verify experimental control evidence from its SHA or establish a consumer threshold. The broader mathematical receiver's controlled-branch premises remain separate from this finite executable schema.

## 6. Exact rational clamped bound

For c>0 set

 kappa'=3kappa/4, F=D-kappa/4,
 a_eff=a+4c^2/kappa,
 C0=g(1+F/kappa')+a_eff g(1/kappa'+F tau/kappa').

Search by doubling from R=2, using only rational comparisons:

 16cR<=kappa, 72R^2c^2g tau<=kappa,
 2R epsilon_ctl<=1 when epsilon_ctl>0.

If R=2 fails, this sufficient route is NOT_ADMITTED. If the explicit doubling budget is exhausted, it likewise refuses rather than inventing a radius. When search completes, R is the largest admitted power of two. Its bit size, every multiplication/comparison and the number of doublings are paid; no online square-root or logarithm oracle is used.

Compute the actual rational exponent

 x=C0/2+18R^2c^2g tau/kappa+R epsilon_ctl.

With m=ceil(8x), use E=(8/7)^m >=e^x and eta_upper=E/(R-1). An explicit maximum exponent limits the size of these rational integers. Exceeding it gives NOT_ADMITTED with an arithmetic-budget reason; it does not assert the apparatus is impossible. For an admitted exponent m the numerator/denominator output sizes grow linearly with m, in addition to input rational sizes. The c=0 case uses the ordinary control-only residual bound.

The receiver compares eta_upper to the supplied external amplitude budget exactly. `verify_certificate` recomputes the whole output against that external input and may validate a truthful NOT_ADMITTED record; `verify_admitted` additionally requires PASS. The CLI's verification requires actual PASS. Rational/boolean/float aliases and undeclared fields are rejected.

## 7. Actual recovered and failed cases

The test fixtures are exact known-model calculations, not achievable-hardware claims.

- **X-coupled lossy qubit:** actual lowering jump with loss10^12, actual B=X, requested source gap10^12 and zero admitted source activation. The source jump kernel gives P=|0><0|, PXP=0 but XP!=0. A complete duration1 system gate with c=1 and supplied zero control residual gets eta_upper about5.08e-5, below the externally requested1e-4. No guard-kernel bound is substituted.
- **Two-jump qutrit intersection:** one loss from each excited level to0; neither individual jump kernel is centered for the actual B, but their intersection is. Subset-size1 or a trial budget stopping before that pair yields UNKNOWN; size2 with sufficient count discovers the centered charge and verifies all generator terms.
- **Omitted-source-term trap:** add a strong raising jump that is not needed to propose the ground. The full drift check fails under the small activation cap. It succeeds only after the cap is increased, and the accepted record contains the corresponding nonzero activation. The favorable subset never authorizes dropping that term.
- **Nonzero ground compression:** adding a PP component to the coupling causes refusal. No hidden mean subtraction occurs.
- **Complex rotated loss/coupling:** exact rational complex source coordinates are recognized using the repaired canonical matrix arithmetic.
- **Guarded comparison:** replacing B=X by B=Q gives the same conservative centered bound, but the separately valid guarded alternative is about1.03e-11 at the same supplied parameters. The older method wins this case and is retained.
- **Fixed diffusion:** tests with c proportional to sqrt(loss) retain a nonvanishing bound. Raising loss does not erase the leading disturbance.

Additional tests bind all external task/model changes, zero-rate proposals, unavailable local proposals, integer-type aliases, invalid certificates, missing idles, source fanout/support conditions, control costs and arithmetic refusal. Test count and frozen hashes are recorded separately after review; tests do not claim raw operator calibration or gate execution.

## 8. Ordinary methods and scientific scope

Source-jump nullspaces, rational projectors, Bernstein positivity, matrix-Lyapunov/LP/SDP search, Schur bounds and Cauchy fault-amplitude receiving are ordinary tools. The strongest equally informed solver can use all the same raw matrices and may find better certificates than this deliberately incomplete cone/search. Earlier primary comparisons with Gaussian noise, local non-Markovian thresholds and actual leakage-removal methods remain applicable; neither a new threshold nor historical priority is inferred.

The concrete acquisition-to-reuse capability is narrower and explicit: actual source operators propose a charge even when the coupling has no annihilating kernel; all omitted-from-proposal generator terms are still verified; then a complete finite schedule receives a bound at the actual creation/diffusion scale. Physical loss/activation/interaction structure, consumer gadgets and real controls still require acquisition. A successful declared-model proof is not a hardware demonstration.
