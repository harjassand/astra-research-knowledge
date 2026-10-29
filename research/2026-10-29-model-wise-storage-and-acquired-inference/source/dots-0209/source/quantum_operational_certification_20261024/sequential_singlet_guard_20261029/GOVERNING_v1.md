# Sequential local-symmetry guard for an accepted finite quantum operation
2026-10-29. Root-proposed composition, developed here. New theorem pending independent review. No priority, hardware-threshold or comparative advantage claim.

## 1. Objective, code and physical boundary
Fix even n, a frozen chosen local frame, full singlet dimension d0=Catalan(n/2), an inner logical dimension K=2^k≤d0 with K>d0/2, and its actual deterministic encoder E and TP logical-output decoder D (fixed-state replacement on leakage). The weighted local test of `../singlet_dirichlet_certificate_20261029/SINGLET_WEIGHTED_CERTIFICATE_v3.md` and branch preparations v4/v5 has, for EVERY CPTP n-qubit source channel N,
 e(N):=1−Fe(D N E) ≤ C q(N), C=(d0/K)(n−1)<2(n−1),
where q is its actual ideal local swap-sign failure probability. No collective-noise model is needed for this inequality.

The source is now an arbitrary causal CPTP process on each n-qubit carrier and ALL retained apparatus memory M. It need not reset, mix, be Markovian, be stationary, have a finite classical description, or satisfy a collective algebra promise. Calls may depend on past source-accessible records. One identified physical port and native call duration are used for both roles. Fresh current role/test-setting/sign/key information must not reach the source as extra classical/pulse/timing/routing side channels before it finishes acting. Quantum input states may differ between roles and may be distinguished by N; the theorem handles that through the inequality above, not a false identical-state claim.

The entire unknown user payload and its arbitrary reference initially factor from the source memory. Secure endpoint controls and buffer memories are outside M. This is a substantive interface: unprocessed outer-code symbols and received logical symbols must be held without uncontrolled source interaction, or their complete errors must be separately budgeted. The construction is not protection of all hardware from arbitrary all-encompassing noise.

Choose an explicit outer quantum code correcting up to t faulty inner-service symbols among J, with J>4t and J≤K. The characteristic-two CSS/GRS construction below encodes ell=J−4t K-dimensional payload symbols. Encode the arbitrary entangled payload BEFORE the guarded sequence and hold its J symbols securely.

## 2. Actual finite protocol
At each trial, independently choose SERVICE with probability s and TEST with probability a=1−s, where0<s<1. Settings are private until the current complete call ends. Pad role-dependent preparation/routing/timing so the source has the same control boundary; preparation may occur in an isolated trusted area.

SERVICE: take the next unused outer-code symbol, apply a fresh independent uniform logical k-qubit Pauli key (2k bits), inner-encode, invoke the source, inner-decode to exactly K logical dimensions, invert the same logical Pauli, and permanently retire the key from every later source/output interaction. Store the resulting symbol securely. Do not measure user data or adapt controls to its unknown logical contents.

TEST: prepare the weighted signed singlet ensemble using the explicit v4/v5 pair-singlet/four-qubit-seed method, invoke the SAME source port, and measure selected-pair Bell sign. Mark failure if output sign differs from the private input sign. Discard the test carrier. Past test records may be retained/disclosed after the completed call; their full bath updates need not match the service instrument.

Abort immediately on test failure number b+1. Accept after J services if no abort has occurred. Also abort if a fixed total-call cap L is reached without J services. On acceptance, execute the TOTAL outer decoder, including its fixed fallback beyond the guaranteed correction radius; do not postselect on syndrome-decoder success. On abort, no successful payload claim is made. The original unknown payload may have been consumed; this is not a retryable nondestructive test on it.

The endpoint outer encoder/decoder, storage of unprocessed/received symbols, isolated native routing, physical test preparation/readout, logical pads and private randomness are actual resources. A source call may itself be a chosen multi-step storage interval; tests pay its entire duration.

## 3. Full-memory Pauli instrument and the correct virtual history
For a SERVICE call include E,D and the complete source process in one joint map from logical L⊗M to L⊗M'. Write any Kraus operator as
 A_lambda=Σ_P P⊗B_lambda,P,
where P ranges over the K² normalized-unitary logical Paulis and B_lambda,P=(1/K)Tr_L[(P†⊗I)A_lambda]. Averaging the actual fresh conjugating key and retiring it removes all off-diagonal Pauli terms:
 T_service(ρ)=Σ_P (Ad_P⊗Phi_P)(ρ),
 Phi_P(σ)=Σ_lambda B_lambda,P σ B_lambda,P†.
These are genuine CP memory instruments. Their sum is trace preserving. A virtual label P is proof bookkeeping, not an observed microscopic error. The aggregate nonidentity probability for memory state σ is exactly e(N_sigma), the logical Bell loss for that pre-call bath state.

Let h contain past roles, complete test outcomes and these virtual SERVICE Pauli labels, but NOT conditioned values of retired service keys. Starting from a payload/reference factorized from M, induction shows that conditional on h, the current bath state σ_h is independent of the complete user payload, which has only accumulated a tensor product of logical Paulis on the serviced outer positions. Tests are independent prepared probes and act only on bath/test carrier; therefore their outcome probabilities and bath updates also do not depend on user input. This remains true if all outer symbols are mutually entangled with a reference.

Thus a single current N_h is well-defined before the fresh role coin, and
 p_h(bad service)=s e_h ≤ s C q_h = R p_h(test failure),
 R=Cs/a.
No iid tests, stationary reduced channel, equality of TEST and SERVICE bath instruments, or exact quantum role indistinguishability is used. The premise is the same complete source map conditional on pre-call history, with no additional current-role controls.

Conditioning on a revealed retired key would undo the Pauli-instrument argument. Freshness and permanent key inaccessibility are essential. Initial arbitrary correlations between user payload and source memory are not covered by the input-independent acceptance theorem below.

## 4. Exact negative-binomial tail under adaptive memory
Let F count virtual nonidentity SERVICE labels and B count test failures. Before termination, their conditional one-step hazards obey f_h≤R g_h. All other outcomes leave both counts unchanged. Define
 p=1/(1+R), u=R/(1+R),
 epsilon_NB=Σ_{j=0}^b binom(t+j,j) u^(t+1) p^j.
This is the probability of obtaining t+1 bad-service marks before b+1 failure marks in the constant-bias comparison process, equivalently the negative-binomial upper tail.

Proof without iid assumptions: let H(i,j) be the comparison probability of hitting i=t+1 before j=b+1, starting at counts(i,j). It is increasing in i, decreasing in j, with boundaries1 and0, and satisfies u H(i+1,j)+p H(i,j+1)=H(i,j). For the actual process,
 E[H(next)−H(i,j)|h]
 =f_h[H(i+1,j)−H(i,j)]+g_h[H(i,j+1)−H(i,j)]≤0.
Therefore bounded optional stopping at the finite cap/hitting boundaries gives probability of hitting t+1 faults before abort≤H(0,0)=epsilon_NB. Stopping early at J services or the cap only censors this event. In particular
 Pr(ACCEPT and F>t)≤epsilon_NB.
For b=0, epsilon_NB=u^(t+1). No division by pass probability occurs in this soundness bound.

## 5. Accepted channel, quantum reference and abort scope
Every history/Pauli-pattern probability is independent of user input. Hence p_acc is input independent. Every accepted pattern with F≤t is corrected EXACTLY by the outer code, for arbitrary reference entanglement. All other accepted patterns undergo a total CPTP decoder. Writing the accepted, subnormalized user map A_acc,
 (1/2)||A_acc−p_acc id||diamond ≤ Pr(ACCEPT,F>t)≤epsilon_NB.
One can include final source memory and retained public test/syndrome transcripts: the ideal accepted map is identity on user payload tensored with the same input-independent accepted memory/transcript state; the same bound follows by summing good/bad CP branches. This uses permanently retired service keys and the secure-buffer boundary above.

The statement is unconditional/subnormalized. If p_acc>0, the normalized accepted-channel error is at most epsilon_NB/p_acc, not epsilon_NB. Without an independently justified positive acceptance rate this can be vacuous. There is no per-transcript posterior guarantee, no claimed availability against arbitrary noise, no infinite-stream extension, and no recovery of an aborted unknown input for free.

## 6. Actual correlated-error outer decoder, not an iid import
Use ONLY the algebraic correction/circuit part of the reviewed `../outer_grs_distillation_20261028/GOVERNING_WRAPPER_v1.md` and `grs_wrapper_v1.py`. Its independent-block distillation premise and binomial tail are NOT imported.

Let q=K=2^k and choose J distinct field elements a_i. For v_i²=[product_(j!=i)(a_i−a_j)]^(−1), the first2t rows H of the weighted Vandermonde matrix generate a self-orthogonal GRS code. Its dual C has dimension J−2t and distance2t+1. The CSS code has parameters [[J,J−4t,2t+1]]_q, correcting every Pauli error whose union of X/Z support has size≤t, regardless of correlations between positions.

An explicit encoder is U_enc=Lin(T)(F^tensor2t⊗I), with T rows[H;logical-complement;full-space-complement], the first and last2t registers initialized0, and the ell=J−4t payload registers in the middle. The known source constructs T and its inverse over exact GF(2^k), compiles O(J²k²) Clifford gates, and provides a total syndrome-only Berlekamp–Welch decoder with O(J³) field operations.

For direct single-sided quantum transmission/storage, apply U_dec=U_enc† after all J serviced symbols return. Measure the first and last2t decoded registers in the computational basis. There is NO Alice/Bob difference in this direct use: the noiseless ancillas were initialized0, so the actual measurements themselves give d_first=H f and d_last=(eT^−1)_last for a physical Pauli X(e)Z(f). Recover sigma_e=(H R^T)d_last and sigma_f=d_first, run the exact finite decoder, and apply the inferred inverse Pauli on the middle ell registers. For every pattern of support≤t the correction is exact. Beyond radius t the fixed fallback still defines a CPTP output. For any Pauli pattern the ancilla outcomes depend on that pattern, not unknown logical amplitudes.

All J inner-service symbols are individually Pauli-twirled, creating the actual correlated Pauli ledger needed here. No Bell-pair source or joint Bell probe gate is used. Endpoint holding costs are O(Jk) logical qubits each, over the full capped sequence; they are not protected by source-port spot-checking itself. If k is too large for convenient field representation, the previously explicit small-field stripe variant can be adapted, but this v1 theorem takes J≤2^k and uses one q-ary symbol per inner service.

## 7. Yield and real control errors
For arbitrary noise only soundness is claimed. Under the additional good-operation promise q_h≤q0 at every visited history, a simple sufficient acceptance lower bound is
 p_acc≥1−Pr[Binomial(L,s)<J]−Pr[Binomial(L,a q0)>b],
using independent role coins and standard conditional-probability domination for test failures. This is a union bound, not an asserted independence of the two counts. At exact collective protection with exact frames, q0=0 and only the service-count cap limits acceptance. Model-free soundness is separate from any such yield promise.

Two distinct error-payment routes:
(a) If actual trusted instruments/pads/encoder/decoder/holding differ from the specified complete ideal instruments by half-diamond allowances whose sum is Delta over the fixed cap, adaptive channel telescoping adds at most Delta to accepted-map error against the ideal protocol. Exact input-independent acceptance and exact Pauli labels then belong to the ideal comparator; do not falsely assert them for arbitrary coherent control errors.
(b) If the SERVICE still has an exact genuine Pauli instrument but the actual TEST satisfies the uniform all-memory scalar/effect allowance e_h≤C(q_actual,h+eta_h), then the hazard has additive term sC eta_h. The same supermartingale proof adds at most Σ_{r≤L}sC eta_r to epsilon_NB, since each upward H increment is≤1. Test bath updates may be arbitrary; only the all-history effect allowance is used. Favorable finite SPAM data do not establish this uniform premise automatically.

The costs include L complete source calls, expected about Ls service pads, O(Ln) state-preparation volume before routing, all reset/discard/readout, source durations, role padding, and outer O(J²k²) Clifford gates/classical decoding. No physical fault-tolerance threshold or free trusted endpoint memory is delivered.

## 8. Strong conventional comparisons and actual contribution
Quantum authentication/purity-testing codes already give exponentially small accepted-state error against coherent attacks using private keys; trap schemes and quantum sampling/QKD provide sophisticated non-iid acceptance analyses. Pauli twirling, hidden roles, CP error instruments, stochastic domination and CSS/GRS correction are established machinery. No claim is made to invent authentication, arbitrary-noise accepted communication, or a better asymptotic resource rate.

Direct full logical 2-design survival tests are another strong comparator: their nonnegative failure has a constant-factor Bell-loss relation, better than C=O(n), but each test executes full randomized logical preparation and code encoder/decoder. Our specific construction uses the newly explicit weighted local-symmetry preparation/readout to guard a learned high-rate physical encoder without full code execution on test calls. The source can distinguish roles through their quantum inputs; the quantified witness handles it, unlike an unjustified role-secrecy assertion. Whether this tradeoff beats conventional authentication/traps under equal source, private-control and buffer resources is unresolved.

Primary comparisons: Barnum–Crépeau–Gottesman–Smith–Tapp, Authentication of Quantum Messages, https://arxiv.org/abs/quant-ph/0205128 ; Bouman–Fehr, Sampling in a Quantum Population, and Applications, https://arxiv.org/abs/0907.4246 ; Dulek–Speelman, Quantum Ciphertext Authentication and Key Recycling with the Trap Code, https://drops.dagstuhl.de/storage/00lipics/lipics-vol111-tqc2018/LIPIcs.TQC.2018.1/LIPIcs.TQC.2018.1.pdf . These are comparators, not unexamined theorem premises.

Astra first retrieval: current N1023 capsule (all pages) and governing full-memory Pauli/role-sealing source lines1–80 read at revision6aa6381fc04b2577852c341489a655a4d50bd1b8, input6c7f4e84e80695d6e7a5ec8aecc9bc374b5e51510ef0aac71c0621ef82462bae. Its exact positive use refinement and weaker uniform-effect pathway are relevant foundations, but its identical input-role ensembles are NOT claimed here. The new weighted witness supplies an all-current-channel scalar inequality for the distinct ensembles; the full-memory induction and NB composition are proved above. Reviewed GRS source/circuit and review files were read locally; only their algebraic implementation is reused.
