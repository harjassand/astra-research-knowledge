# Executable known-model local admission compiler

31 October 2026. This document receives the reviewed local-occupation theorem and physical-unit corollary into an exact classical acquisition program. It is not hardware calibration, a quantum gate backend, a new threshold theorem, or a claim to validate an arbitrary experimental source.

## 1. Delivered operation

`acquire_local_admission.py` reads a finite declared model, a complete finite gate/idle schedule and a supplied consumer amplitude budget. It derives the local parameters, checks structural premises and emits a rational sufficient amplitude certificate. `verify_certificate(external_spec, record)` recomputes against the CALLER'S external specification. `verify_admitted` additionally requires status PASS. A valid NOT_ADMITTED record is not a successful scientific admission.

The input format is `occupation-local-admission-v1`. All rationals are canonical integer pairs `[numerator, positive_denominator]`, with coprime entries. Booleans, floats, nonfinite JSON numbers, duplicate JSON keys, unknown fields and noncanonical rational encodings are rejected. Source and system indices are zero-based.

## 2. Exact input contract

The top-level fields are exactly:

- `format`;
- `task`: nonempty task ID, SHA-256 of the external consumer contract, and its requested amplitude budget strictly between zero and one;
- `source_model`;
- `system_qubits` and positive rational total `duration`;
- global always-on `couplings`;
- the full `locations` list.

### Source model

Two interfaces are deliberately distinguished.

**Explicit graph.** `mode="explicit"`, a nonempty source list with positive `loss_lower` and nonnegative `injection_upper` for every source, and an edge list. Each edge has unique `i<j`, rational `real`, and rational `imag`. The actual Hermitian hopping term is h_ij sigma_i^+ sigma_j^- plus its conjugate adjoint. The program reads every source and edge and computes

  lambda_min=min_i loss_lower_i,
  a=max_i injection_upper_i,
  beta=max_i sum_{j adjacent i} (|Re h_ij|+|Im h_ij|)/lambda_min,
  gamma=1-2 beta.

This uses a safe rational upper bound on |h_ij|, not a square-root oracle or an uncomputed exact spectral norm.

**Known finite program.** `mode="uniform_open_chain"`, positive integer n, common positive loss lower bound, common nonnegative injection upper bound, and common rational complex nearest-neighbor hopping. The graph is DEFINED by this finite program, not supplied as an unknown large table. Its maximum degree is exactly min(2,n-1), or zero if the hopping is zero. The certificate explicitly reports symbolic program acquisition and zero explicitly inspected graph vertices/edges. This does not claim to have checked a million independently supplied couplings.

Only the declared loss/injection/hopping grammar is accepted. Arbitrary generator additions are rejected rather than treated as harmless. The mathematics allows some additional commuting diagonal source Hamiltonians, but this executable interface does not accept an unchecked generic Hamiltonian field.

### Global unwanted coupling

Each term has a source index, `source_operator="occupation"`, a real rational coefficient, and a sparse nonidentity system Pauli word. The Pauli word is a sorted list of distinct `[qubit,"X"|"Y"|"Z"]` entries. The operator is the supplied coefficient times n_source tensor that Pauli word. Terms are constant and ON throughout the entire schedule. Identical terms are combined exactly before taking absolute values; exact cancellations are honored.

Source X/Y/raising/lowering terms, products of multiple source projectors, unspecified time dependence and generic norm promises are not accepted by this grammar. An identity-only system term is also outside this sparse input grammar; it is not silently confused with an arbitrary target operation.

### Full finite schedule and intended operation

Each location has a unique ID, positive-length rational interval in `[0,T]`, a nonempty sorted system patch, an actual intended target, and a control-error premise. Every system qubit must be covered from zero to T with no gap and no overlapping location. Thus omitted idle exposure is rejected.

An intended target is either `idle` or a constant local Hermitian Pauli Hamiltonian supplied as an exact rational term list. Its Pauli support must lie within the patch. The code records its Pauli-LCU action upper bound, not an executed implementation or a proof that it realizes a particular error-correcting gadget. Preparation, measurement and reset are deliberately not accepted as magic target names. A consumer requiring them must acquire a separately justified complete interface; this executable certificate alone is not a universal machine.

The control-error record supplies an `integrated_hamiltonian_bound` and the SHA-256 of its external evidence. This is the precise source-independent, patch-supported integrated Hamiltonian discrepancy in the theorem. The program checks type/sign and binds the evidence identifier. It DOES NOT read that evidence or prove a physical calibration. Average gate infidelity, a reduced-channel estimate, or an unverified norm guess is not automatically this parameter. Even a declared zero bound is a model premise, not evidence of perfect hardware.

## 3. Acquired support and normalization, with outside interactions ON

For each global Pauli term, the program finds every location touching its system support. The entire support must lie in that location's patch; otherwise the always-on term straddles simultaneous locations and is rejected. This prevents a term from being omitted while another gate runs.

For a location l and source i, it sums the absolute coefficients of the merged assigned Pauli terms. This is an acquired upper bound c_li on the actual Hermitian operator norm, without diagonalizing a system-sized matrix. It then computes

  c=max_{l,i} c_li,
  g=max_l number of assigned sources,
  tau=max_l actual location duration,
  epsilon_ctl=max_l declared integrated control-error bound.

For each source, all location intervals to which it is assigned must be nonoverlapping. A source that controls two simultaneous patches is rejected, even if each individual term is small. Sequential reuse is allowed. Multiple Pauli terms from one source within a single joint gate patch are allowed and their coefficient sums are paid.

The complete declared graph remains present; unused and exterior source nodes are not removed in the certificate. The theorem's local product weight is what permits an n-independent admission parameter.

## 4. Receiving unequal loss bounds

The frozen proof writes a common loss lambda. For actual rates lambda_i>=lambda_min, its product-weight loss term has the additional contribution

  -sum_i (lambda_i-lambda_min) u_i n_i V/(1+u_i) <=0.

Thus using lambda_min in the backward influence equation and in the radius bound is conservative. Likewise replacing actual injection rates by their maximum upper bound only increases the scalar growth estimate. Physical hopping is normalized by lambda_min. No stationarity or equality of the losses is assumed by this executable receiving step.

The Markov loss/injection fields must still be initialized as required by the specified Lindblad model. Arbitrary initial finite source/system/reference correlations are permitted; arbitrary unknown correlated incoming fields are not.

## 5. Exact rational admission

For c>0 and gamma>0 define

  R0=gamma lambda_min/[8 c g(1+a tau)],
  R=R0 if epsilon_ctl=0,
  R=min(R0,1/(2 epsilon_ctl)) otherwise.

The program requires R>=2 for this sufficient interface. It uses the rigorous rational constants

  exp(1/4)<9/7,  exp(3/4)<17/8.

Consequently the emitted bound is

  eta_upper=(9/7)/(R-1)              if epsilon_ctl=0,
  eta_upper=(17/8)/(R-1)             otherwise.

It also emits the looser linear resource envelope

  max{16 E c g(1+a tau)/(gamma lambda_min), 4 E epsilon_ctl},

where E is the corresponding rational exponential upper bound. Since R>=2, the direct rational bound is no larger than this envelope. PASS means exactly that the direct bound does not exceed the externally supplied amplitude budget. The program does not choose a universal threshold.

The two exponential constants have finite rational proofs. For x=1/4 or 3/4,

  exp(x) <= sum_{j=0}^8 x^j/j! + [x^9/9!]/[1-x/10].

The displayed rational expression is strictly below 9/7 or 17/8 respectively, as checked with exact fractions in the tests. No floating logarithm or exponential comparison enters admission.

If c=0, exact cancellation or absence of all source couplings leaves the ordinary source-independent Hamiltonian control-error model. The standard first-insertion bound gives inclusive amplitude strength epsilon_ctl directly. Source transport need not meet the occupation criterion in this branch because it is decoupled from the system. The program labels this separate ordinary control-only branch explicitly.

A valid declared model with nonpositive gamma, R<2 or an excessive resulting eta receives NOT_ADMITTED, not a false theorem. Invalid syntax, unsupported operators, missing exposure and overlapping support receive REJECTED/InputError. Failure of this sufficient test is not proof that the physical device cannot operate reliably.

## 6. Verification and external task binding

The record contains hashes of the FULL external specification and the external task, the exact parameter derivation, the proof/corollary hashes, resource counts, the requested budget and the computed bound. Verification requires the external specification as a separate argument and deterministically recomputes all fields.

The comparison uses canonical JSON type/value encoding, not Python's permissive equality between True, 1 and 1.0. A certificate cannot substitute its own easier budget, different target Hamiltonian, new control-evidence hash or truncated schedule and still verify against the original external task. Extra fields and malformed records fail verification.

This binds the supplied specification; it is not authentication of an external document, a proof that a device follows the declared generator, or a verifier of experimental history. A valid record with NOT_ADMITTED returns true from `verify_certificate` but false from `verify_admitted`. Consumers must use the latter (or explicitly check status), not mistake record consistency for scientific admission. CLI verification exits nonzero for an invalid record; add `--require-admitted` to require PASS as well. Acquisition with that flag similarly exits nonzero on NOT_ADMITTED. Without that flag, successful generation of a truthful NOT_ADMITTED record is not treated as an execution failure.

## 7. Computation and precision costs

Let V,E denote explicitly supplied source vertices/edges, L the number of locations, Q the total patch entries, and P the number of Pauli terms. Explicit graph acquisition costs O(V+E) exact local arithmetic and storage. The known-chain interface instead checks its finite parameters and exact degree formula; its n dependence is integer encoding, not an n-entry scan.

The schedule is checked through per-qubit sorted interval lists, with sorting cost polynomial in Q and L. Coupling-to-location assignment is computed from the actual sparse supports and those lists; the straightforward implementation can cost the number of term/location incidences and in the worst case a polynomial cross product of the explicit term and schedule sizes. Source interval lists are also sorted. No exponential Hilbert-space table, matrix exponential, quantum oracle or free QRAM is used.

All normalization, radius, budget and certificate operations are rational. Fraction numerator/denominator lengths can grow with the total input bit length, and that ordinary big-integer cost is paid. The code does not claim constant-time rational arithmetic. It uses Python's standard library and has no gate synthesis backend.

The output additionally records actual maximum system-patch size, intended Pauli action, explicit graph inspection counts and assignment counts. These are not a complete physical execution cost. The loss, injection, hopping, gate generation, reset supply, routing, readout and consumer code costs are separate actual resources.

## 8. Reproducible checks and examples

Run:

```
python test_acquire_local_admission.py
python benchmark_local_admission.py
python acquire_local_admission.py explicit_fixture_input.json --verify explicit_fixture_certificate.json
python acquire_local_admission.py million_source_fixture_input.json --verify million_source_fixture_certificate.json
```

The author suite currently has 93 checks, including exact rational constants, cancellation, complex hopping, unequal loss minima, malformed types/indices/edges, source-creating rejection, missing idle exposure, cross-patch and same-source fanout rejection, sequential reuse, a joint gate, control caps, genuine NOT_ADMITTED records, strict certificate types and external task/target/evidence changes. Independent review is separate; a test count is not itself a proof.

The measured benchmark JSON records exact input/output sizes, integer bit lengths and platform-dependent wall times. The timer starts from an already-parsed Python specification; fixture construction, JSON parsing and file I/O are not included. Physical parameter acquisition is not timed or claimed. Canonical JSON byte counts are distinguished from pretty-printed file sizes. Its fixtures are:

- four explicitly inspected source qubits/three edges and two physical gate locations: eta=27/1749979, approximately 1.54e-5, against supplied budget1e-4;
- a KNOWN uniform open-chain program defining one million sources, one localized coupling and one finite gate: eta=9/262499993, approximately 3.43e-8, against supplied budget1e-6; no million-entry graph is claimed inspected;
- an explicitly materialized ten-thousand-source chain, with all10,000 vertices/9,999 edges actually inspected, giving the same local bound as the known program at the same physical parameters.

The raw integrated unwanted Hamiltonian bound is one in all three fixtures, and fails those supplied budgets. That is a comparison against one standard sufficient raw-norm test, not proof that the strongest conventional methods fail. The million-source example is a finite-program theorem instance, not a million-source experiment or quantum simulation. The large loss/coupling ratios are declared model parameters, not demonstrated achievable rates.

## 9. Strong ordinary comparator and present consequence

AGP/AKP and the accessible Astra N951/N1467/N1483 machinery already provide fault-path and robust-computation receivers with actual physical premises. They get identical graph, pulse, coupling and calibration information. Ng–Preskill's Gaussian correlation admission already bypasses some raw high-frequency operator-norm limitations; Gaussian/Wick and correlation-integral inputs are not supplied by this non-Gaussian qubit model, so this executable does not pretend to compute that comparator's bound. No absence-of-title or absent-numeric-output argument establishes superiority.

The useful operation delivered here is finite local input -> checked all-subset amplitude admission, without reconstructing the full source channel or assuming a tensor product of marginal faults. It is reusable across finite schedules/coupling lists, but each changed external task is rebound and recomputed. It is known-program reasoning, not learning an unknown source. It remains restricted to number-controlled, non-source-creating couplings with bounded activation. The deeper local operator-certificate acquisition problem is not solved by this code.
