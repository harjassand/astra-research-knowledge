# Independent review: sequential singlet guard
2026-10-29 UTC. Reviewer: `review_current_channel_symmetry`.
Disposition: **accepted at the explicitly bounded, accepted-subnormalized operation scope**, with the inherited nontrivial inner-code domain even n>=4, K>=2, integers 0<=4t<J<=K. No initial payload–source-memory correlations, uncontrolled endpoint noise, availability against arbitrary sources, or generic security/novelty advantage is accepted.

Hash-bound sources and checks are listed in RECEIPT_v1.json. The author's check_memory_and_guard_v1.py reruns byte-identically. Independent checks were written for joint nonunital sources, exact adaptive scalar-policy optimization, and a direct single-sided outer code circuit on a reference-entangled payload.

## 1. Full-memory instrument: checked without assuming classical/iid memory
For each complete joint logical-memory Kraus A_lambda, the unitary Pauli expansion A_lambda=sum_P P tensor B_lambda,P is exact. Conjugating input/output by the same fresh uniform logical Pauli and discarding the key averages distinct character cross terms to zero. Hence the ACTUAL averaged joint map is sum_P Ad_P tensor Phi_P, with Phi_P(sigma)=sum_lambda B_lambda,P sigma B_lambda,P^dagger. Complete positivity is manifest. Taking the logical partial trace of the joint TP identity proves sum_P Phi_P is TP on memory; no assumption that each branch is TP is used.

For memory input sigma, the identity-Pauli branch probability equals the normalized logical Choi identity coefficient, hence Fe of the effective logical service. All nonidentity branches sum to e=1-Fe. This remains true with inner leakage followed by the specified TP replacement decoder. It would not hold for a trace-decreasing leakage-selected channel normalized after the fact.

The full map identity holds even on correlated logical-memory inputs. However the manuscript's input-independent acceptance induction starts with the stronger product assumption and does not extend its conclusion merely from that identity. Beginning with payload/reference independent of source memory, conditioning on past roles, full test outcomes and VIRTUAL Pauli labels leaves a tensor product of a Pauli-modified outer payload with a memory state. Tests are independent prepared carriers and alter only memory/test registers. Thus the complete current memory state, branch probabilities and source-accessible transcript distribution are independent of unknown user amplitudes. Entanglement among unprocessed/processed outer positions and reference is permitted.

The proof must average permanently retired keys rather than condition on them. Keys cannot be later exposed or coupled back into the assessed source/output. The boundary also excludes the source acting on stored outer symbols or retained decoded symbols outside their declared calls.

## 2. Same-map witness and hidden current settings
Conditional on the virtual history, both current roles invoke the SAME complete physical source map with a fixed pre-call memory state. Different quantum role inputs are allowed and are not claimed indistinguishable. This is exactly what the already-reviewed all-CPTP weighted witness handles:

    s e_h <= s C q_h = (Cs/a) p_h(test failure).

The test and service bath instruments need not agree, and the channel may change after every actual history. Current role, edge, sign, key, preparation seed and distinguishing external control/timing information must not reach the source as additional side channels before the call completes. An independent quantum input-state response is allowed. Trusted padding/routing and preparation-record isolation are therefore genuine assumptions, not consequences of the witness.

Equivalently, the all-memory inequality is an operator effect domination W_bad<=C F_testfail. Independent tests construct three-Kraus NONUNITAL joint sources with memory dimensions 2 and 3, explicitly derive service Pauli Kraus maps and actual weighted test effects, and verify this effect inequality, TP sum, and equality of the actual joint key-average to its Pauli instrument. These complement—not replace—the all-memory derivation.

## 3. Adaptive negative-binomial bound: accepted
Let R=Cs/a, u=R/(1+R), p=1/(1+R). Comparison hitting probability H(i,j) has boundaries H(t+1,j)=1 and H(i,b+1)=0 and recurrence H=u H(i+1,j)+p H(i,j+1). It is increasing with faults and decreasing with test failures. Since f_h<=R g_h, the one-step conditional drift of H under the actual process is nonpositive; zero-count-change outcomes make no contribution. The fixed finite call cap permits bounded stopping without limit/interchange assumptions.

Consequently the probability of t+1 faults before the abort boundary, and hence the smaller accepted-bad event, is bounded by

    epsilon_NB=sum_{j=0}^b binom(t+j,j) u^(t+1) p^j.

Stopping at J services or the call cap only censors paths. This is not an iid error-count assertion. The source can adapt its complete quantum memory and all branch probabilities after each history.

Independent check_guard.py uses exact Fraction arithmetic to optimize the final ACCEPT-and-bad probability over ALL adaptive scalar hazard policies obeying the stronger role constraints f<=s, g<=a, f<=R g. It maximizes the DP at every state over the feasible polygon vertices rather than sampling a stationary policy. Three finite instances lie below the claimed NB bound. This is a finite stress test, not the general proof. The author separately simulates actual quantum memory updates and history-dependent source variants; that output reproduces exactly.

The good-operation acceptance lower bound is also valid as a separate conditional promise: independent role coins bound insufficient services, and a uniform visited-history q_h<=q0 gives test-failure binomial domination. The union bound does not require the counts to be mutually independent. It supplies no unconditional yield for arbitrary sources.

## 4. Direct outer code and complete output channel
Only the reviewed GRS algebra/circuit is imported, not its earlier independent-block noise model. The characteristic-two dual-containing CSS construction with 0<=4t<J<=K corrects every Pauli pattern with UNION X/Z support at most t; correlated occurrence of those patterns is irrelevant. The weighted Vandermonde identities and exact syndrome decoder remain applicable.

For direct quantum transmission/storage, U_enc starts with zero first/last ancillas. After a physical Pauli and U_enc^dagger, the measured ancilla values themselves are the X labels of decoded first/last registers; no bilateral outcome difference is needed. The formulas d_first=H f and d_last=(e T^-1)_last therefore give the exact classical syndromes. For any Pauli pattern, including outside the correction radius, these ancilla values are independent of payload amplitudes. The total decoder's deterministic fallback remains CPTP; no syndrome-success postselection is allowed.

Independent check_direct_outer.py physically propagates a q=8,J=5,t=1 encoded payload entangled with a two-dimensional reference through the single-sided circuit. It tests 35 one-site X/Z/combined patterns, deterministic ancilla readout and actual decoded correction; wrong-syndrome and corrected-infidelity residuals are below 1.4e-15. It reuses the previously reviewed exact field construction and classical decoder, but independently implements amplitude-level encoding/error/decoding and its indexing conventions. This is not a single end-to-end implementation of the n=4 inner fixture: that inner K=2 cannot support J=5. The author's fixture correctly labels these separate scopes. A combined nontrivial outer-code instance needs a larger inner K (e.g. n=8 gives K=8).

## 5. Accepted subnormalized diamond and transcript scope
Given initial product state and retired keys, accepted history probabilities and p_acc are independent of the unknown payload. Each accepted pattern with <=t faults implements identity on arbitrary user/reference state after correction. Its memory and transcript branch is also input independent. Bad accepted patterns define complete output maps, possibly logical-error maps, with their fixed branch memory/transcript. Replacing every bad branch by identity tensored with that same branch state changes the accepted subnormalized map by at most its probability in half diamond norm. Summing gives

    (1/2)||A_acc-p_acc id||_diamond <= Pr(ACCEPT,F>t) <= epsilon_NB,

and the analogous identity tensor accepted-memory/transcript comparison. Actual syndrome transcripts can be included because their values depend on Pauli patterns, not user amplitudes. The virtual labels need not be accessible or measured by the implementation.

Normalization after acceptance costs division by p_acc. There is no transcript-wise posterior bound, unconditional availability, infinite-stream conclusion, or nondestructive retry guarantee. An aborted unknown payload can be lost. Initial correlated payload/source memory is excluded here; a later proposed correlated-input theorem is NOT reviewed or imported by this receipt.

## 6. Calibration/control scope and finite resources
Route (a) is a comparison to the specified ideal protocol: adaptive instrument half-diamond errors summing to Delta add at most Delta by telescoping through the fixed cap and arbitrary causal source. The ideal comparator has exact input-independent acceptance. Arbitrary actual coherent endpoint/control errors do NOT preserve that assertion, so one must not silently substitute an actual input-dependent p_acc into the ideal formula.

Route (b) keeps a genuine exact service Pauli instrument and assumes a uniform all-memory TEST allowance e_h<=C(q_actual,h+eta_h). It gives drift error at most s C eta_h because each upward H increment is <=1. Summing over the cap yields the displayed additive allowance. Arbitrary test memory updates are permitted. A finite collection of favourable SPAM samples is not proof of this all-memory effect bound.

Real resources include J inner encoder/decoder executions on completed service paths (or the appropriate capped count on abort), private pads and key retirement, L whole source calls, test seed/matching preparation, all routing/role padding, endpoint holding, outer Clifford circuits and finite syndrome decoding. The old O(n) test-control volume and precision budgets remain applicable. The trusted buffers hold O(Jk) logical qubits over the FULL capped sequence, including unresolved reference-entangled outer symbols. The guard does not protect those buffers or guarantee a physical fault-tolerance threshold.

## Actual progress accepted
This composes the weighted local certificate with an explicit causal-memory Pauli instrument, an adaptive finite-call stopping theorem and a correcting outer code. It removes independent source-reset and exact collective-algebra assumptions for the stated accepted finite source-port operation, while retaining a strong trusted endpoint/interface boundary. The result is not a generic claim to have solved quantum authentication or arbitrary-device protection. Conventional authentication/traps and full encoded 2-design tests remain serious comparators; equal-resource advantage is unresolved.
