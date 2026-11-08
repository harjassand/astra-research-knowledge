Constructive research record · 9 November 2026 · Brisbane

A more tractable route to autonomous quantum memory

Use commuting quantum monitors and explicit local Pauli frames to turn quantum execution history into a classical streaming problem.

The full autonomous-memory theorem remains unresolved. This investigation produced component proofs, a stronger memory-specific representation, exact finite checks and explicit counterexamples to incomplete alternatives. The next decisive theorem concerns a noisy, asynchronous, reusable record interface and a decoder threshold for its actual observations.

Scope. Fixed local, time-independent driven/dissipative dynamics in two or three dimensions; finite site dimension, density, range and rates; nonzero local noise on data and controllers; unknown reference-entangled input retained for stretched-exponential time. Encoding, physical readout and entropy export require counted resources. This is the target, not an achieved device. [A]

The principal worked with the same two gpt-6.1-sol workers at maximum reasoning effort. We exchanged constructions and adversarial checks throughout. These are AI-generated, internally checked research arguments; no external review, proof-assistant certification or hardware validation is claimed. This record continues the broader repository/literature selection.

ResultsMemory representationRemaining theoremChecksDerivationsSources

The analytic bridge we can now state

Exact algebraBounded local signed perturbations
→

Physical costLocal normalization + added weak depolarization
→

Component proofRare CPTP errors + joint witness bound
→

UnprovedActual recurrent-device recursion

The strongest analytic result is an exact positive fault representation for the modified device. For local HP/trace-annihilating G with ‖G‖_{⋄}≤ε, let T(ρ)=Tr(ρ)I/d and γ=d²ε. Define Φ=T+G/γ. Its Choi matrix satisfies J(Φ)=I/d+J(G)/γ≥0; Φ preserves trace. Thus Φ is CPTP and

G + γ(T−Id) = γ(Φ−Id).

The paid depolarizer converts the residual exactly into rare state-independent Poisson error events with arbitrary local CPTP actions. The device need not know Φ. Local normalization gives γ_{X}=2d_{X}²ε_{X}. Assigned support budgets give a per-site rate bound 2d_{max}²ε; unknown support assignment costs its template-incidence factor. Added-emitter errors must fit the complete-hardware budget. This applies ordinary Choi-interior geometry to a changed architecture. [W]

Let μ bound integrated residual event intensity per fixed box, with one event touching at most K boxes. Positive Poisson counting bounds both the joint witness probability and its restricted channel’s diamond norm:

Pr(all marked witnesses bad), ‖E_{bad}(F)‖_{⋄} ≤ [q+(eKμ)^{1/K}]^{|F|},   eKμ≤1.

Here q controls ideal-clock witnesses. Signed generator terms themselves were never assigned probabilities. Correct behavior outside these witnesses is still a separate semantic obligation.

The general signed-norm interface

A difference between two physical generators need not itself generate physical evolution. Conditioning on ideal clocks while treating that signed difference as a physical background is invalid. Established conditional-Choi and isotropic-noise machinery gives a useful design repair. [W]

First normalize any bounded local decomposition of the globally Hermiticity-preserving, trace-annihilating perturbation into local terms with those properties. Support is unchanged; the norm budget increases by at most two. For a local term G on dimension d, with ‖G‖_{⋄} ≤ 2ε, add the actual depolarizing generator γD, where D(ρ)=Tr(ρ)I/d−ρ and γ=2d²ε. The residual R=G+γD is a genuine Lindblad generator, with

‖R‖_{⋄} ≤ 2(1+2d²)ε.

This modifies the architecture. The added noise, its emitter and its implementation errors are counted; it does not establish that adding noise improves storage. The completion mechanism is prior art. Our record supplies an explicit local budget, support-preserving normalization and use in the proposal-clock argument.

Fix r deterministic spacetime witness boxes. Let b bound the integrated residual norm touching any box, and K the maximum number of marked boxes touched by one elementary insertion. Suppose ideal proposal-clock bad events have joint probability at most q^{r}. A common expansion, with exterior choices resummed to physical channels, gives

‖E_{bad}(F)‖_{⋄} ≤ [q + e^{b}(eKb)^{1/K}]^{|F|},   eKb ≤ 1.

The proof uses physical hybrid propagators, inclusion–exclusion and an exact partition by the clock-bad subset. Signed quantum faults are never assigned probabilities. Shared insertions require the K-th-root loss. The continuous limit uses exact local channels. [K] [AGP]

The bound is uniform in exterior volume and clock-attempt count, and survives admissible finite-horizon causal testers at the specified physical ports. Its fixed witnesses still need a connection to actual repaired device failures. [STR] [SUPER]

The stronger representation for memory

Keep the data in fixed registers. Run commuting local stabilizer-monitoring instruments continuously. Place two physical Pauli-frame bits beside each data qubit; a classical decoder updates those bits instead of issuing physical correction gates. All of these registers remain noisy.

W = ⊗_{i} Σ_{x,z} |x,z⟩⟨x,z|_{Fᵢ} ⊗ Xᵢ^{x}Zᵢ^{z}.

At a check S_{a}, measure the raw sign σ and publish τ=χ_{a}(f)σ, where P_{f}^{†}S_{a}P_{f}=χ_{a}(f)S_{a}. Capture the local frame parity in the same event. Conjugating by W gives exactly the virtual stabilizer instrument publishing τ. Local classical frame updates become local virtual Pauli corrections.

This is an identity of Kraus operators on the full data/controller/record algebra, so it includes coherent frame faults and arbitrary reference entanglement. It also gives

E′_{X} = Ad_{W†} E_{X} Ad_{W},   ‖E′_{X}‖_{⋄} = ‖E_{X}‖_{⋄}.

Cell support is unchanged when frame and data share a cell; adjacent storage costs a fixed support enlargement. A global history-controlled frame would not have this locality guarantee. Bare frame errors are charged local quantum/controller faults.

The representation uses established Pauli covariance and controlled-unitary machinery. It removes noncommuting quantum execution-history reconstruction from the memory architecture. It does not provide reliable classical processing or authorize commuting measurements across arbitrary intervening faults. Actual record chronology remains part of the device. [PI] [DOA]

Other bridges: useful scope and sharp limits

Moving-code recovery. For any fixed physical-depth unitary window, attach gate flags and form the layered controlled circuit W. Conjugate a supplied idle-recovery generator and flag process by W. Arbitrary intended flag order and backwards repairs telescope to the correct window, while recovery follows the instantaneous code. This removes internal gate-predecessor tests inside that window. It assumes an already acquired recovery mechanism; growing logical depth cannot masquerade as fixed physical depth. [PI]

One-use causal rails. Vacuum-plus-payload ports let each CPTP gate consume its inputs and move data to fresh outputs. Legal states are circuit-DAG cuts, including reference entanglement. A finite-depth circuit completes with an exponential Poisson tail. Fresh ports consume space proportional to circuit volume; finite recycling still needs repair. Causal-box composition supplies a language for this interface, not a fault-tolerant implementation. [BOX]

 | Shortcut tested | Explicit obstruction | What a repair must prove

 | Flat frame cycles implement recurring gates | Transport V_{b}V_{a}^{†} telescopes to identity on a closed controller walk. | A real commit/holonomy, changed location or consumed resource.

 | Consume-once rails are sufficient | One phase swap leaves A₀B₁ occupied; neither forward nor reverse two-input gate can fire. | Bounded causal repair and progress after lost/misaligned tokens.

 | Frame repair protects waiting data | Decoded payload Pauli noise retains its original rate under a product Pauli-frame gauge. | Actual error correction or a proven damage witness for the delay.

 | Repair can recover an erased gate receipt | The same observed state can arise before U or after U on a different unknown input. | Contained faults, rather than exact history reconstruction from data.

 | Old records can use the current frame | A frame change between measurement and relabeling reverses the historical syndrome sign. | Atomic parity capture or a retained causal log.

The exact remaining theorem

Construct a finite-state, geometrically local, time-independent noisy transducer that accepts syndrome observations continuously at adequate per-check bandwidth; captures measurement-time frame labels; computes an actual decoder; and recycles finite buffers and epoch labels indefinitely. Prove bounded causal damage and joint sparse witnesses for capture, lost records, stale messages, repaired clocks, decoder commands and buffer reuse. Compose it with a quantum-memory threshold for the irregular or gapped observations that the real sampler actually delivers.

The quantum instrument and local-noise representation are now explicit; fresh classical input and its chronology are the unresolved interface. A raw pointer fault must not silently relabel an arbitrarily long history or authorize an unbounded wave of false correction commands.

The strongest concrete streaming baseline is Selub–Bhardwaj–Lake’s surface-code decoder, particularly its constant-resource-density hierarchy. Its reliable global clock and noiseless classical operations are assumptions to remove. Its asynchronous code-capacity statement does not already cover noisy streaming. [SBL]

Gács supplies powerful asynchronous repair, but Definition3.5/Theorem6.1’s imported computation contract has immutable input, pre-encoded initialization and a constant δ contribution to its error bound. It does not directly supply live syndrome intake, finite rolling reuse or exponentially small per-batch error. Clean offline desynchronization and the synchronous quantum automata are additional starting points with their stated boundaries. [G] [LAKE] [BDL] [DST]

Gács–Reif’s real-time reliable array is a useful throughput prior. Its journal theorem assumes synchronous steps and initially repeated inputs; “real-time” means no synchronous slowdown. It is not an asynchronous live-input theorem. [GR]

Resource trade. Deferring Pauli corrections permits polynomial decoder latency if observations are captured and protected meanwhile. A three-dimensional classical volume above a quantum plane may pay for history and routing. Polynomial geometric overhead can conditionally preserve stretched-exponential lifetime. Input bandwidth, buffer protection, reset heat and final pending-frame correction must be demonstrated for the actual layout.

Acceptance test. The same recurrent physical rule must establish a level-uniform joint fault recursion η_{j+1}≤Cη_{j}^{s}, s>1. One lower-level controller fault that erases an entire higher-level block gives a linear failure term and fails this test. Our norm estimate supplies an input to that induction; it does not replace gadget correctness or overlap/truncation analysis. [AGP]

Universal computation adds a further causal interface, particularly non-Clifford/adaptive dependencies. The commuting-monitor construction currently addresses memory. [MC]

A bounded next construction, now specified: one check producer, an atomic label latch, a finite ring buffer, neighboring-check handshakes and a decoder-window commit. Exhaustive lost-ACK, stale-epoch, pointer-flip, overwrite and restart injections should reject any recurrent class with permanent capture loss. An idempotent re-ACK repairs the simplest lost-ACK deadlock; a parameterized causal-damage and bandwidth proof is still required for an actual architecture.

Another concrete import: self-stabilizing data links

Bounded-capacity networking protocols already address stale packets, duplicates and acknowledgments after corrupted state. The Dolev–Dubois–Potop-Butucaru–Tixeuil link re-ACKs received packets and supplies a bounded initial-delivery exception. Its weak fairness and unbounded-delay model gives no wall-clock tail. We use version2’s corrected four-parameter specification. [SDL]

There is an elementary bridge to our clock witnesses: in a fixed finite deterministic proposal automaton, if every state can reach a forward-invariant target, concatenate shortest paths for surviving state images. One universal word of at most N² letters reaches the target from every state. Independent positive-rate clocks realize that prescribed word in fixed slots with probability

p = e^{−ΛΔM} ∏_{k=1…M}(λ_{wₖ}Δ) > 0.

Its absence in B disjoint blocks has probability (1−p)^{B}. This is an analysis event; no global clock is added to the device. Corrupt program counters, persistent request identity and all outside influences must be included in the premise. Progress alone does not certify correct contents, clear old packets or contain their delayed effects. Constants remain size-independent only for fixed finite modules, not an entire growing decoder.

A concrete base link was built and exhaustively checked. We implemented a capacity-one, binary-record realization with a constant-size receiver queue, an atomic receive/update/re-ACK action, and explicit sender count normalization. The clock word POLL · (SEND,RX,POLL)^{10} has 31 events. Every active typed state reaches sender completion by a prefix of this word.

The enumeration covers 4,078,368 configurations, including 2,718,912 active in-flight states and 113,288 freshly initialized calls. Every fresh call delivered its held bit exactly once and produced one completion acknowledgment. We inspected the transitions against the governing source and independently reran the enumeration.

The separation matters: 1,100,456 corrupted in-flight configurations completed without delivering their current payload. The construction proves recovery of progress, with fresh-call correctness under the witness. It does not recover a lost current record. Physical acceptance at the destination, stable held input, atomic receiver action and no new faults or outside arrivals during the witness are explicit premises. Occupied output buffers, live framing and the growing decoder remain outside this component.

The next representation: synchronization-indexed records

A single insertion or deletion can shift every later record’s interpretation. Synchronization strings supply established machinery for converting synchronization damage into symbol errors. Their local decoder has a stronger certificate: incorrect indexing requires high edit density in a suffix. The infinite version still assumes the correct received-symbol count and reliable endpoint computation. [SYNC] [LOCAL]

We proved a conditional scalar bridge for those certificates. On a fixed integer slot lattice, suppose error positions satisfy Pr(F⊆E)≤η^{|F|}. Mark t bad if some interval ending at t has error density at least α. Choosing the rightmost remaining marked endpoint gives disjoint witness intervals covering all marks. Counting them yields

Pr(all r marked positions bad) ≤ [8η^{α}/(1−4η^{α})]^{r},   4η^{α}<1.

This needs no independent errors. It is a probability argument, compatible in principle with the paid CP-event model. Applying it to the device still requires a bounded physical-fault-to-edit charge, a source-index-to-spacetime map, adequate service, and protected counters and buffers. The indexing theorem does not repair a corrupted counter or an unbounded stall.

What was checked

- 15 exact rational cases: common fault-path sums equal physical-hybrid inclusion–exclusion for every nonempty subset of four overlapping boxes. Scalar tail bounds pass. One shared fault explicitly defeats a false squared-independence bound.

- 16 exact-entry operator identities: QND/Pauli-frame Kraus and frame-update conjugacies, including the stale-parity counterexample. Operator equality extends to untouched references.

- 36 floating diagnostics: explicit Lindblad reconstruction in dimensions 2, 3, 4, using analytic norm upper bounds. Largest entry discrepancy: 2.05e-12. Conditional Choi/rate bounds and sampled semigroup CP checks pass to stated numerical tolerance.

- 36 additional complex-map diagnostics: the padded error channel is CP/trace preserving, its generator identity holds, and its Poisson mixture agrees with direct exponentiation. Maximum Poisson/exponential entry discrepancy: 1.84×10^{−15}.

- Finite counterexamples: the four-slot recurrent rail deadlock was enumerated. All 16 states of an ACK-progress toy expose two trap states without duplicate re-ACK; re-ACK admits a three-letter universal progress word.

- Exhaustive base-link check: 4,078,368 typed configurations, zero completion failures under the 31-event witness, zero incorrect fresh calls among 113,288. The current record can be lost after in-flight corruption; this negative result is retained separately.

These computations check finite identities and falsify shortcuts. They do not implement the streaming decoder, prove a global threshold, certify novelty or demonstrate a physical advantage. The ACK toy checks progress only; it is not a content-correct FIFO link.

Download proofs, scripts and check outputs · Read the evidence ledger

Complete component derivations

The following notes retain explicit premises, proofs and failed constructions. They are internally audited mathematical research notes. The analytic budget can be made nonzero at fixed design constants; practical parameter estimates and a recurrent device theorem remain absent.

Local support-preserving normalization and causal testers

Local normalization and operational extension

9 November 2026. Elementary root derivations; no novelty or full-threshold claim.

Local HP/trace normalization

Let a globally Hermiticity-preserving, trace-annihilating linear map E have a bounded-support decomposition E=sum_X E_X, with ||E_X||diamond<=epsilon_X. The individual summands need not have either property. Define E_X^#(rho)=E_X(rho†)† and F_X=(E_X+E_X^#)/2. Then F_X is HP, preserves support, ||F_X||diamond<=epsilon_X and sum_X F_X=E. Adjoining an arbitrary reference commutes with #, and taking an adjoint preserves trace norm, so # preserves diamond norm.

Put A_X=F_X^*(I_X), with * the Hilbert-Schmidt adjoint, and

G_X(rho)=F_X(rho)-{A_X,rho}/2.

A_X is Hermitian and ||A_X||op<=||F_X||diamond, by induced trace/operator norm duality. Thus G_X is HP and trace annihilating, retains support, and ||G_X||diamond<=2epsilon_X. Upon embedding in the full lattice, sum_X A_X=E^*(I)=0. Therefore sum_X G_X=E exactly. No global correction term has been added.

The paid local-completion lemma now applies with gamma_X=2d_X²epsilon_X to an arbitrary bounded local decomposition of a globally HP/TA generator difference. The residual R_X=G_X+gamma_X D_X is GKLS and ||R_X||diamond<=2(1+2d_X²)epsilon_X. For d_X<=D the per-site norm-density cost is at most 2(1+2D²). Adding the depolarizers is a real physical change; normalizing the decomposition itself is exact algebra.

The adversarial worker independently checked support, complete-norm invariance, the anticommutator bound and the cancellation of embedded A_X on 9 November 2026.

Finite-horizon adaptive testers

The fixed-box and mixed clock/noise bounds hold uniformly after inserting any admissible causal CPTP tester at the device's physical open ports. The tester may keep reference/work registers, feed inputs adaptively from previous outcomes, and output an unconditioned classical/quantum record. On a common refined time grid each tester operation is another norm-one exterior channel. The same hitting-path regrouping and norm inequalities apply on the enlarged space. Taking the supremum over such testers preserves the bound.

The tester must not change the predefined box geometry or the state-independent proposal law, or inject unbudgeted interactions into the device. Adaptation must be causal. Postselected records must retain their probability weight; conditioning and renormalizing a rare successful event does not inherit this bound. This proves an operational interactive extension, not equality of arbitrary timing transcripts with an externally clocked ideal process. The ideal comparison must expose the specified ports and retiming law.

Gutoski arXiv:1008.4636v2 supplies the established strategy-norm framework; Chiribella-D'Ariano-Perinotti arXiv:0804.0180v2 supplies the established physical-supermap framework. Here we only use contractivity of each physical tester channel; no equivalence of a terminal diamond bound and an adaptive causal simulation is assumed.

Exact rare CPTP-event representation after paid depolarization

Paid depolarization gives exact rare CP-event noise

9 November 2026. Stronger root completion argument, independently audited by the adversarial worker. Standard Choi positivity/interior geometry; no originality claim. It changes the device physically and does not uniformize an unmodified generic GKLS generator.

Local channel construction

Let G on M_d be Hermiticity preserving and trace annihilating, with ||G||diamond<=epsilon. Define T(rho)=Tr(rho)I/d, D=T−Id and gamma=d²epsilon. For epsilon>0 set

Phi=T+G/gamma.

In the unnormalized Choi convention J(T)=I_(d²)/d, and ||J(G)||op<=||J(G)||1<=d||G||diamond<=d epsilon. Hence

J(Phi)>= [1/d−d epsilon/gamma]I=0.

Trace annihilation of G and trace preservation of T give trace preservation of Phi. Thus Phi is CPTP and, exactly,

G+gamma D = gamma(Phi−Id).                              (P1)

If epsilon=0 the term vanishes. A fixed upper norm budget can replace the actual norm. Phi may be unknown: the proof re-represents the actual noisy device after known depolarization was added; the device computes neither G nor Phi.

Full Choi positivity gives an ordinary finite-rate CP-event representation of the completed residual. The conditional-Choi argument alone had obscured this stronger conclusion. Unpadded generic Hamiltonian/GKLS terms do not inherit it.

Local lattice budget

Normalize a globally HP/TA E=sum_X E_X locally as before. The resulting G_X retain supports and ||G_X||diamond<=2epsilon_X. Add gamma_X D_X with gamma_X=2d_X²epsilon_X. Then

L_modified=L0+sum_X gamma_X(Phi_X−Id),
Phi_X=T_X+G_X/gamma_X CPTP.

For d_X<=D and per-site perturbation density epsilon_local, residual proposal intensity per site is at most2D²epsilon_local. Its error locations are genuine independent state-independent Poisson clocks; their payload actions are arbitrary local CPTP maps. Dimension, support/template incidence, added-noise hardware, entropy export and its implementation imperfections remain paid. Those imperfections belong inside the epsilon budget. Rates are fixed independently of size and storage time.

Pointwise bounded time-dependent G_X(t) can use fixed dominating rates and time-dependent channels. The time-independent target has time-independent channels. Correlated non-Markovian noise is not supplied.

If only an aggregate site budget is known, rather than the individual epsilon_X budgets, pad every admissible support template and pay its finite incidence nu. The resulting conservative intensity is <=2D²nu epsilon_site. Unknown noise assignment is not free information.

The assumed norm bound must include the added emitter. If its additional contribution to ||G|| is bounded by eta gamma, while the remainder is epsilon_0, a sufficient self-consistent choice solves gamma>=d²(epsilon_0+eta gamma). This requires d²eta<1 and gamma>=d²epsilon_0/(1−d²eta). Here epsilon_0 and eta refer to the already HP/TA-normalized G budget. An absolute complete-hardware budget can instead be assumed directly. Neither model grants a perfect depolarizer.

Positive joint witness bound

Fix deterministic spacetime boxes. Suppose residual error-clock intensity integrated over events incident on any box is <=mu, and each event touches at most K marked boxes. For r fixed boxes their incident-event union has mean B<=r mu. To hit all boxes requires at least m=ceil(r/K) distinct events. Its event count is Poisson(B). For eKmu<=1, the Poisson Chernoff bound gives

Pr[all r boxes hit] <= exp(−B)(eB/m)^m
                   <= [(eKmu)^(1/K)]^r.                 (P2)

Zero budgets are trivial. This bound is uniform in exterior volume; unrelated clocks were never counted. With K=1 and truly disjoint incident-event regions, independence gives the sharper product of (1−exp(−mu_j)).

Let ideal proposal-clock events have joint bad bound q^r and be fixed independently of quantum state. The ideal and residual proposal processes are genuinely independent here. A positive union bound over which marks use ideal-clock rather than residual witnesses yields

Pr[all combined witnesses bad] <= [q+(eKmu)^(1/K)]^r.   (P3)

Conditional on each full clock history, all ideal and residual maps are CPTP. The quantum map restricted to a classical witness event is a positive mixture of norm-one channels. Its diamond norm is therefore at most the event probability in (P3), including arbitrary reference entanglement. This is a real fault-location probability argument for the MODIFIED architecture, rather than probabilities assigned to G itself or to a signed A/F expansion.

Here 'clock history' retains proposal labels/times but does not postselect quantum measurement outcomes. The witness event must be defined by those clocks, or a separate clock-defined envelope must dominate it uniformly over all quantum outcomes/inputs. An arbitrary outcome-selected subchannel does not inherit an input-independent event probability from this statement.

The previous signed-norm estimate remains useful without this representation. For the paid design, (P1)–(P3) provide a simpler stronger interface. They still do not prove that controller/record failures have local causal witnesses or implement a protected streaming decoder. Applying a scalar suffix-density lemma needs a proved bounded edit charge and a mapping from source slots to physical spacetime.

Paid completion, mixed norm proof and adversarial counterexamples

Constructive adversary: autonomous continuous-time quantum correction

9 November 2026. Work in progress. This file separates proved finite-dimensional lemmas, explicit architecture counterexamples, and the missing autonomous hierarchy. No full autonomous threshold or physical advantage is claimed.

1. A paid depolarizing completion removes signed-background obstruction

Lemma 1 (local depolarizing completion). Let E:M_d -> M_d be linear, Hermiticity preserving and trace annihilating, and suppose ||E||diamond <= epsilon. Define T_d(rho)=Tr(rho) I_d/d and D_d=T_d-Id. For any gamma >= d^2 epsilon, the map

R=E+gamma D_d

is a GKLS generator. In particular exp(tR) is CPTP for every t>=0. It obeys

||R||diamond <= epsilon+2gamma.

The difference E need not itself be positive, completely positive, GKLS, or the difference of matched physical local terms. This is an application of the established conditional-complete-positivity characterization, with an explicit robust completion constant; no originality of the criterion is claimed.

Proof. Use the unnormalized maximally entangled vector Omega=sum_i |i,i>, normalized vector e=Omega/sqrt(d), projection P=I-|e><e|, and Choi convention

J(E)=sum_(a,b) |a><b| tensor E(|a><b|).

Hermiticity preservation makes J(E) Hermitian. Since J(E)=d (Id tensor E)(|e><e|),

||J(E)||op <= ||J(E)||1 <= d ||E||diamond <= d epsilon.

Also J(D_d)=I_(d^2)/d-|Omega><Omega|, hence P J(D_d) P=P/d. Therefore

P J(R) P >= (gamma/d-d epsilon) P >=0.

R is Hermiticity preserving and trace annihilating. The finite-dimensional GKLS conditional-Choi criterion now gives the result. Finally ||D_d||diamond<=2, proving the norm bound. This proves all claims. The constant d² is sufficient, not optimized.

Primary governing criterion and mechanism. Wolf, Eisert, Cubitt and Cirac, Assessing non-Markovian dynamics, arXiv:0711.3172v2, Eq(2) gives the conditional-Choi characterization. SectionIV explicitly adds isotropic generator noise to make a signed generator Lindblad and optimizes it by SDP; the root checked this mechanism-specific passage. Our assembly uses a conservative explicit local d²epsilon bound, support-preserving HP/trace normalization and a clock-conditioned fault interface. Isotropic completion is established prior, not a novelty claim. Primary source.

Constructive finite GKLS decomposition and rate bounds

Let C=P J(R) P>=0. Diagonalize C=sum_j lambda_j |v_j><v_j|. For at most d²-1 nonzero terms define V_j by |V_j>>=sqrt(lambda_j) v_j, with vectorization |A>>=sum_a |a> tensor A|a>. Let Phi(rho)=sum_j V_j rho V_j† and G=sum_j V_j† V_j.

Write v=P J(R)e and alpha=<e|J(R)|e> (real). Define A through

|A>>=v/sqrt(d)+alpha e/(2sqrt(d)).

Then J(R)-C=|A>><Omega|+|Omega><A|, so R(rho)=Phi(rho)+A rho+rho A†. Trace annihilation implies A+A†=-G. Setting H=(A†-A)/(2i) gives the explicit finite Lindblad form

R(rho)=-i[H,rho]+sum_j(V_j rho V_j† - {V_j†V_j,rho}/2).

The added depolarizer has no cross block P J(D_d)e. Thus v=P J(E)e, and the alpha contribution to A is a real scalar multiple of I. Consequently ||H||op <= ||v||/sqrt(d) <= sqrt(d) epsilon.

For gamma=d² epsilon, the total squared jump-operator norm has the conservative bound

sum_j ||V_j||op² <= sum_j ||V_j||HS² = Tr C <= d epsilon + gamma(d²-1)/d = d³ epsilon.

No finite-rate CP uniformization of a generic generator was used. The decomposition exists as ordinary Hamiltonian plus finitely many Lindblad operators. It need not be known to the device: the actual device already supplies its unknown perturbation, and the proof certifies that the residual after intentional depolarization is physical.

Local lattice corollary

Suppose E=sum_X E_X, where each E_X is supported on an admitted bounded support X, is Hermiticity preserving/trace annihilating, and has a known bound ||E_X||diamond<=epsilon_X. Add the physical engineered noise gamma_X D_X on each such support, with gamma_X=d_X² epsilon_X. Then

L_actual + sum_X gamma_X D_X = L_0 + sum_X R_X,

where every R_X is a local GKLS generator. If d_X<=D and sup_i sum_(X contains i) epsilon_X <= epsilon_local, then

sup_i sum_(X contains i) gamma_X <= D² epsilon_local,

sup_i sum_(X contains i) ||R_X||diamond <= (1+2D²) epsilon_local.

If only a uniform bound per possible support is available, one adds noise on all admissible translated support templates, paying their finite incidence factor. Bounded radius and onsite dimension imply finitely many templates. Onsite depolarization alone does not necessarily dominate negative entangling GKS directions on a larger support. An individually HP/trace-annihilating local decomposition is an explicit premise; a merely physical total generator does not by itself provide that decomposition with the claimed norm budget.

Physical boundary of this lemma

This changes the actual architecture by adding known noise; it is not an alternative decomposition of the unmodified apparatus. Pick a nonzero admissible error budget and fixed completion rates before scaling size/time. The added local rate, support, source randomness, hardware and entropy export are paid. Calibration/implementation error of the depolarizer belongs inside E and its bound; the emitter is not a noiseless external controller. With finite local dimensions the constants may be huge, but remain independent of lattice size and storage duration. This is an existence-level reduction, not a claim of practical parameters or watts.

Why this matters for the proposal-clock gap

If L_0=sum_a lambda_a(Phi_a-Id) is the explicit ideal CP-event controller, the completed generator is L_0+R with R genuinely GKLS. It has an exact representation as independent state-independent ideal proposal clocks interleaved with CPTP R evolution. Conditioning on those proposal clocks leaves a physical norm-one background. This avoids the invalid step of conditioning on ideal clocks while treating a signed E background as CPTP. It does not by itself prove the joint mixed clock/noise locality bound or correct quantum semantics; those are the next statements to establish.

2. Counterexample: safe Pauli-frame repair is not protected WAIT

Let F be a finite frame register, Q the payload, W=sum_f |f><f| tensor P_f, where P_f are Pauli frame operators. Let L_PI=Ad_W (L_F tensor Id_Q) Ad_W†, for an arbitrary GKLS frame generator. Define the physical decoder D(rho)=Tr_F(W† rho W).

The frame-gauge construction gives D L_PI=0. Now add physical payload noise L_P=kappa(Ad_(I tensor P)-Id) for a Pauli P. Since P_f† P P_f=chi_f P with phases chi_f, W†(I tensor P)W=Z_F tensor P for a diagonal unitary Z_F. Invariance of partial trace under conjugation on F implies

D L_P = kappa(Ad_P-Id) D.

Therefore for every initial joint state, including arbitrary reference entanglement, the decoded payload obeys exactly

d rho_Q/dt = kappa(P rho_Q P-rho_Q).

The error rate is unchanged by frame-controller speed or its path independence. A product Pauli-frame gauge permits harmless lifted frame motion; it does not correct payload errors. A physical frame flip alone also is not automatically a lifted gauge move. The same argument termwise gives unchanged local depolarizing error on Q. Thus PI frame repair cannot supply a noncircular protected WAIT without an independently proved encoded correction mechanism.

Relevant established PI algebra: Ma–Li–Jiang arXiv:2201.00360v2, Definition1 and Theorem1 require the Hamiltonian/jumps to lie in the same path-independent algebra. Their AppendixA identifies the controlled-unitary conjugation. Theorem1 and its scope were read directly. Primary source.

3. Mixed fixed-box clock/noise locality after completion

Lemma 2. On a finite lattice and deterministic horizon T let L=L_0+R, with L_0=sum_a lambda_a(Phi_a-Id), each Phi_a CPTP, and R=sum_X R_X a sum of local GKLS generators. Consider deterministic spacetime boxes. A residual factor touches at most K boxes and the integrated residual norm weight incident on any one box is at most b. Let fixed events B_v(omega) of the independent ideal proposal-clock history obey P(all B_v,v in C)<=a^|C| for every fixed C. For ProofS take a=beta_H^(1/chi).

Define a box bad in a joint formal path if B_v holds or a residual fault factor hits it. Let E(F) sum/integrate joint paths bad at every box of fixed F. If eKb<=1, then

||E(F)||diamond <= (a+zeta)^|F|,

zeta=exp(b)(eKb)^(1/K).

Residual fault maps are not assigned positive probabilities. No independence of actual data/controller states and those faults is assumed.

Proof. The exact Poisson/Dyson representation of exp(T(L_0+R)) has independent proposal clocks with R semigroups between proposal channels. Every clock-conditioned background is CPTP. This is where a signed non-GKLS residual would fail; paid Lemma1 makes it valid.

For fixed clock history split R evolution into exact local Trotter factors A_i=exp(dt_i R_X)=Id+F_i, with ||F_i||diamond<=dt_i||R_X||diamond. Proposal channels have norm one. For n required residual-hit boxes N, expand factors incident on their union and keep all other factors fully actual. This is a resummation of a common global expansion. Hitting all n boxes needs m=ceil(n/K) selected factors. Their total available weight B obeys B<=nb, so

||E_noise(N;omega)||diamond <= sum_(q>=m) B^q/q!

<= exp(B)(eB/m)^m <= [exp(b)(eKb)^(1/K)]^n.

The bound is uniform in proposal count/history. Fix box-edge conventions before the Trotter limit. The marked-hit limit exists by finite inclusion–exclusion of the physical hybrid evolutions obtained by removing R_X terms incident on selected boxes; all hybrids remain GKLS.

For each omega let C(omega)={v in F:B_v(omega)}. Partition by its exact value C. Only residual hits on F\C are then required. Thus

E(F)=sum_(C subset F) int_(C(omega)=C) E_noise(F\C;omega) dP(omega).

Each term's norm is at most zeta^(|F|-|C|) P(C(omega)=C), and the probability is at most a^|C|. Sum over C to obtain (a+zeta)^|F|. This exact classical partition avoids an invalid union bound for non-CP fault sums. QED.

Root and this worker independently arrived at the same mixed argument and exchanged the matching derivation. The mathematical result is a fixed-box interface. It does not show that service/repair failures are covered by these boxes or that good boxes implement the intended quantum causal cut. Adaptive box geometry, protected WAIT, recurrent rails and the uniform hierarchy remain additional obligations.

Choose fixed H first to suppress a, then a nonzero physical noise budget to suppress b, including completion and box-volume factors. H, dimensions, ranges and rates then stay fixed as system size/time grow. Current constants may be enormous; no practical regime follows.

4. A one-fault recurrent-rail deadlock

Consider four fixed packet slots A0,A1,B0,B1, each vacuum plus one payload. Ideal gate U consumes occupied A0,B0 and vacant A1,B1, applies its quantum channel, and relocates to A1,B1. Ideal gate V does the reverse. Each gate's guard also requires its two output slots vacant. Start with A0,B0 occupied. Without faults the two-gate cycle runs; consumed-input guards forbid immediate replay.

One bounded local fault swaps the B0/B1 slot contents. Now A0 and B1 are occupied. U lacks B0 and V lacks A1, so both guards are permanently false. Proposal clocks may run forever without changing the state. Consuming payloads has prevented replay but has not supplied liveness or a protected idle. If A carries half a Bell pair and undergoes local Z-jump noise at rate kappa during this stall, its entanglement fidelity is exactly (1+exp(-2 kappa t))/2.

The fault can be a local unitary transport within the B phase pair, without even damaging B's unknown internal state. The example is a counterexample to a bare recurrent-token compiler, not to every repaired token architecture or to the clean acyclic order-ideal lemma. A timeout/poisoning mechanism can address this particular configuration but must be specified and analyzed. It cannot be credited for free.

Why erasure timeout needs an explicit interface

A gate waiting for an absent input and the same gate waiting for a merely delayed input have identical local histories before that input arrives. Any rule that progresses in bounded time in the missing-input case must sometimes progress before the delayed input arrives, unless it has another certified completion/latency signal. This need not forbid fault tolerance: premature completion can be a charged local erasure with a proved stochastic tail. It forbids silently treating a timeout as both zero-error and wait-free.

Starting a deadline only after the first input does not solve a component in which every triggering packet was deleted. An always-running source can fix that but may generate phantom future work unless activation/epoch state is also certified. In a finite recurrent fabric, an old delayed packet can encounter a reused slot with the same finite epoch label (ABA). A guarded consume-once rule alone does not prove exclusion of that stale packet.

Fresh spacetime rails spend space

One-use acyclic rails genuinely remove replay by consuming old input slots forever. A computation of growing circuit volume then spends growing numbers of fresh gate/edge slots. A claimed fixed finite memory fabric must reuse them. At that point the clean DAG/order-ideal proof needs a physical epoch/recycling protocol and a fault bound for its repair, or an independently protected moving code. It is not a finite autonomous hierarchy merely because every gate footprint is constant.

No exact-once recovery from an erased history log

Suppose a repair sees the same controller state and payload rho in two histories: in one, U was already executed on prior input U†rho U; in the other, U has not executed on prior input rho. Exactly-once semantics requires repair to act as identity in the first history and as U in the second. For a nontrivial U and arbitrary unknown inputs these requirements disagree on the same observed physical state. Thus a lost irreversible-action log cannot be reconstructed exactly from unknown data alone.

This is not a no-go for FT: a bounded ambiguity may be declared a bounded quantum fault or erased region. The substantive requirement is that repair uncertainty have a bounded causal footprint/overlap, not that history be magically recovered.

5. Safe fail-closed repair: precise candidate and circularity test

A candidate rule is: any repair that changes the causal interpretation of a payload port first erases/marks every potentially affected payload in a bounded causal footprint. It never resumes an unknown state under a rewritten program history. This trades impossible rollback for explicit quantum faults. To be usable, a classical damage theorem must bound the entire spacetime repair/poisoning footprint, including fresh data entering a repair wave, with witnesses that require enough lower-level faults.

Erasing a whole level-j encoded block after one level-(j-1) controller fault gives a level-j failure linear in the lower-level fault strength. It does not provide the needed superlinear recursion, even if the block is a fixed size in abstract level-j units. Likewise a moving-code/PI theorem assuming an already noise-robust autonomous recovery generator proves a safe representation change, but cannot establish that recovery generator without a recursive closure proof. Noncommuting code patches, syndrome extraction, fresh reset, stopping a partial correction cycle and changes in the active-data set all belong in that proof.

A local controller repair may instead be absorbed into a local burst quantum fault if all mismatched prefix operations lie in a bounded causal neighborhood. This is promising when classical damage shrinks rapidly and lower-level idles remain active. It fails if the prefix/repair wave reaches unboundedly many fresh blocks or if one lower-level fault erases an entire higher-level block. No complete construction satisfying these conditions has been proved in this file.

6. Root extension: local HP/trace normalization

The root supplied the following exact extension, checked by this worker. Given E=sum_X E_X, with only total E HP/trace annihilating, set F_X=(E_X+E_X#)/2, where E_X#(rho)=E_X(rho†)†. Dagger conjugation preserves diamond norm, so F_X is HP, has norm at most ||E_X||diamond, unchanged support and sum E.

Set A_X=F_X*(I_X) (Hermitian) and G_X(rho)=F_X(rho)-{A_X,rho}/2. Then G_X is HP/trace annihilating, has norm at most 2||E_X||diamond, and unchanged support. Since the embedded sum of A_X is E*(I_total)=0, the anticommutators sum to zero: sum_X G_X=E exactly. Thus completion rates gamma_X=2d_X²epsilon_X and residual local norm budget 2(1+2D²)epsilon_local suffice. No extra global remainder is introduced. A missing bounded local decomposition is still not supplied by this normalization.

Remaining live interface

Target a finite reusable, noisy, asynchronous classical record transducer for the actual Selub–Bhardwaj–Lake streaming decoder, arXiv2609.11457v1. Its bounded-speed constant-density hierarchy assumes noiseless classical processors (intro/Fig1 and stability footnote). Its algorithm is a useful destination, not proof of robust implementation.

A sufficient new theorem needs this contract under fixed local time-independent dynamics, fixed site dimension/range/rates and the completed local GKLS noise model:

- Live intake: latch monitor outcomes and contemporaneous frame parity at a per-check physical bandwidth bounded below independently of code distance. A small local capture-error floor is allowed; noiseless pre-encoded fresh inputs are not supplied.

- Causal labeling: records correspond exactly once to source and virtual order, up to declared monotone bounded-displacement retimings with bounded gaps/neighbor skew. A bounded phase offset may be legitimate. Unbounded age/backpressure or stale records relabeled arbitrarily fresh are not.

- Finite reuse: retain a polynomial rolling window, pipeline and committed frame. Epoch/lease/ACK rules handle wraparound, delayed packets, duplicate publication, overwrite and restart. An unprotected shared pointer may not discard uncommitted records. Old-window commit needs the decoder's actual consistency criterion.

- Reliable processing: implement the streaming algorithm on changing inputs, uniformly over histories. Either prove adequately small global processing failure over the memory horizon, or prove remaining errors become sparse local faults to which the destination decoder is robust. Selub's noiseless-processor theorem cannot silently tolerate arbitrary constant-rate virtual processor faults.

- Joint causal-damage witnesses: r fixed bad virtual intake/record/commit locations require a bounded-overlap family of physical fault/slow-clock witnesses with cardinality at least r/c, or the precise sufficient alternative cluster exponent. Witness multiplicity must grow at most exponentially in witness size, uniformly in size/time. This is what allows the fixed-box norm theorem to transfer; mean throughput and marginal failures do not suffice.

State the result as a full-record channel/causal-process bound with arbitrary references. Exact onsite-frame conjugation supplies the quantum representation identity, not the classical transducer. No claim is made that all such classical results are absent; the exact required import/proof remains unestablished here.

One-ACK pipeline counterexample

Consider a stop-and-wait sender retaining a record until ACK. Receiver accepts once and sends its ACK once; duplicates are ignored without re-ACK. One transient fault erases that ACK. Sender retransmits the old record forever; receiver ignores duplicates; no ACK transition is enabled. New syndrome records fill any finite queue and are then lost without bound. Retry clocks can continue firing, so bounded heartbeat/dwell does not establish intake progress.

This refutes that concrete naive protocol. Idempotent re-ACK, timeout/erasure and a proved reuse rule can repair it; they are feasible classical mechanisms, not impossibility claims. The exact requirement is that one physical fault cannot cause an unbounded strip of fresh record losses while charged only once.

Bounded decisive gate

Implement one check producer, latch, finite ring, two neighboring-check epoch handshakes and decoder-window commit. Exhaustively inject lost ACK, stale epoch, pointer flip, overwrite, duplicate publication and restart. Every reachable recurrent class must resume correctly ordered capture or have a proved finite-time/sparse bad-record witness. A hidden permanent wait rejects the design. Then prove the parameterized witness lemma and bandwidth/window/latency inequality. Finite enumeration can falsify the protocol, not establish the complete theorem.

Concrete finite base link

Explicit capacity-one realization and 31-event word

Use binary payload alphabet {0,1} plus reserved SYNCHRO; packet keys are (payload-or-SYNCHRO,bit), six possibilities. Each directed mailbox is empty or holds one packet. On overflow choose overwrite-old, one of the capacity model's allowed rules. Sender has phase SYNCHRO/DATA/DONE, counter0,…,5 and program counter SEND/POLL. A fresh call begins in SYNCHRO, count0, SEND after its first bit flip; the payload is held until the call completes.

Each SEND proposal writes the current packet and changes the local program counter to POLL. POLL removes the reverse packet, increments its ACK count only on a match and returns to SEND. At count5 it advances the phase, clearing the counter and flipping the bit at SYNCHRO→DATA; DATA→DONE emits the application completion ACK. For arbitrary typed count5 states, the SEND/POLL entry includes this same local normalization. This normalization is an explicit implementation choice covering unused-but-physically-representable counter states.

The RX proposal is one finite local CPTP classical transition: consume the forward packet; update the receiver's at-most-two-entry queue and last bit; perform the guarded delivery/drop/reset; write its ACK into the reverse mailbox. This atomic RX+queue+ACK handler touches the receiver state and the two adjacent mailboxes. It has bounded support/dimension, which must be paid. A hardware model restricting primitive interactions further needs a compiled split-handler protocol and another proof; the 31-event claim does not silently provide that compiler.

Assume that DeliverMessage is accepted immediately by the application at the delivery event, exactly as in the source abstraction. The word

POLL · (SEND, RX, POLL)^10

has31 proposal letters. The initial POLL either does nothing or puts the sender at SEND (possibly completing a phase). Each subsequent triple overwrites any stale forward packet, receives that precise packet, overwrites any stale reverse packet with its matching ACK, and increments the current phase's counter. At most five successful increments per phase and two phases remain. Therefore every active typed state reaches DONE within this word. If the call was freshly initialized, the five SYNCHRO receipts align the receiver's bit even from an arbitrary queue/last-bit state; the DATA phase has the opposite bit and delivers the held payload exactly once before completion. No quantum payload is moved by this link; its inputs are classical check records.

Destination readiness is a premise. An occupied finite destination port requires a separately paid acceptance/drain handshake, or backpressure with its own service guarantee. It is invalid to replace DeliverMessage by an unbounded queue. Similarly, source arrivals are held/excluded during the word; capture throughput and the fate of fresh syndrome samples while the link is busy remain part of the live-transducer contract.

Exhaustive finite check, separated from the proof

check_finite_link_word.py compiles and runs check_finite_link_word.cpp; finite_link_word_exact.json records the result. The C++ implementation independently constructs every valid typed receiver queue and its RX transition table, then executes the word on the full Cartesian state space:

- 289 unique-key queues of length0,1,2, counts0,1,2;

- 2 receiver last-bit values;

- 7 possible contents for each directed mailbox;

- 2 payload values,2 sender alternating bits,3 phases,6 ACK-counter values and2 sender program-counter values.

This is 4,078,368 typed configurations, of which 2,718,912 are active in-flight and 1,359,456 already terminal. Every active state reaches DONE within31 events. All 113,288 fresh-call configurations deliver the held payload exactly once with one completion ACK. Conversely, 1,100,456 active in-flight states terminate without delivering their current payload. That last number is a direct counterexample to equating repaired progress with preservation of the current record. No active configuration delivered the current payload more than once along this particular word; arbitrary fair histories retain the source's one-extra-prefix allowance. The check covers typed finite states, not arbitrary malformed linked-list memory; implement the finite queue as its declared alphabet or normalize unused bit encodings.

Hashes at this run: C++ e5da195d2c6f21bee6529747e0c2bf6fc501eb002ca7d3d9ea351f7d2a7f42a5; Python driver d8b87709f119937beea5ed8fe1ec3028b6bd30ebfba6fb45cfd08e720b97ec26. This is exact integer finite enumeration, not a noisy-device simulation, complete streaming implementation or threshold proof.

Quantitative physical-clock lemma

Implement these three guarded CP proposal maps with independent exogenous Poisson rates, each at least lambda_min>0, and total relevant proposal rate at most Lambda. Disabled guarded proposals act as identity. Hold input and readiness through the window; exclude other touching transitions or include them in Lambda and require their absence in the clean word. Non-touching distant proposals need not be suppressed.

For M=31 and B=M/Lambda, the probability of exactly M relevant proposals in time B with the prescribed labels is at least

p = exp(-M) M^M/M! · (lambda_min/Lambda)^M > 0.

This bound is uniform over all typed starting states and input values. Consequently, an outstanding call with the stated service premises has hitting-time tail

Pr[T_done > nB] <= (1-p)^n.

For a freshly initialized call the same event witnesses correct delivery/completion. This is the strong Markov/independent-clock argument on a specified finite physical realization, not a deduction of a deadline from weak fairness. For three equal proposal rates and no extra touching actions, the crude bound is p≈1.157e-16, B=31/(3lambda); these constants are deliberately conservative and establish no practical service rate. Better finite-chain estimates are possible but were not run. Taking H consecutive windows gives slow-clock probability at most (1-p)^H; fixed-box clock witnesses can then be colored by bounded overlap. Noise insertions are handled by the separate root norm expansion, not interpreted as independent classical failure probabilities.

Resources and remaining obstruction

The binary link's typed state product has4,078,368 states. Separate encodings cost at least8 sender bits,10 receiver bits and3 bits per mailbox, i.e.24 bits before source/destination handshake buffers, captured-frame labels, physical locality implementation, redundancy and decoder processing. This is an information count, not a protected hardware realization. The RX macro support is large but constant; its support dimension and rates enter the depolarizing-completion/noise constants. Larger record alphabets/epoch fields must be counted afresh.

Thus known prior machinery plus this explicit local realization closes a base record-link liveness/reuse gap and disproves any claim that ACK-safe finite reuse was unavailable. It does not yet close the autonomous memory theorem. Missing interfaces are bounded destination readiness and sufficient aggregate bandwidth; causal framing across many links and repeated faults; robust fresh capture; noisy realization of the actual streaming decoder; rolling-window retirement and Pauli-frame commit. Even an O(1) sequence-edit allowance per transient is not, by itself, a uniform geometric damage-cover theorem for a decoder: persistent index/epoch corruption and accumulated insertion offsets still require a proved labeling/resynchronization representation. Those requirements should now be attacked above this concrete finite link rather than by reopening the lost-ACK deadlock.

Final implementation and checker boundaries

Each declared classical transition has a finite local measure/prepare CPTP realization, with Kraus operators K_s=|f(s)><s| on its finite classical neighborhood (and identity on the reference/outside). Unchanged guarded configurations may instead be grouped into an idle-projector Kraus block. The proposal term lambda(Phi-Id) is therefore legitimate GKLS. The state-path argument is on classical configurations; arbitrary coherent local perturbations are handled by the separate norm framework, not by treating them as classical transition probabilities. Input records are the classical outputs of the QND instrument. Direct finite alphabets or an explicitly clamped spare-state encoding implement the typed state space; an unchecked pointer representation is not covered.

The checker stops at the first DONE. It verifies a prefix hitting-time bound, not purification of all registers after exactly31 proposals. For a fresh call the forward mailbox is empty at DONE, so later RX proposals produce no extra delivery when no new call begins. Arbitrary in-flight configurations can leave terminal stale state, and their subsequent output safety must use the source's bounded-prefix theorem with the pending-call caveat. No clean global boundary or erased history follows merely from reaching DONE.

11. Stronger paid-padding representation: exact rare CP clocks

The root identified a stronger consequence of the same paid depolarizing padding. This worker audited it and found no algebraic flaw. It supersedes the need for signed residual-fault expansions for the modified padded device at this model scope; the earlier norm lemmas remain useful for unpadded or differently modeled devices.

Full-Choi proof

Let G be a local linear HP/trace-annihilating map on a d-dimensional subsystem, ||G||diamond<=epsilon. Let T(rho)=Tr(rho)I/d, gamma>=d²epsilon>0, and define

Phi = T + G/gamma.

Use the input-first unnormalized Choi convention, J(G)=(Id tensor G)(|Omega><Omega|), |Omega>=sum_i |ii>. The input operator has trace norm d, hence the definition of diamond norm gives

||J(G)||op <= ||J(G)||1 <= d ||G||diamond <= d epsilon.

HP makes J(G) Hermitian, including for genuinely complex maps. Also J(T)=I_(d²)/d, so

J(Phi) = I_(d²)/d + J(G)/gamma >= (1/d-d epsilon/gamma) I >= 0.

Trace annihilation gives Tr_out J(G)=0; therefore Tr_out J(Phi)=I and Phi is CPTP. The exact generator identity is

G + gamma(T-Id) = gamma(Phi-Id).

Consequently

exp[t(G+gamma(T-Id))] = exp(-gamma t) sum_(n>=0) (gamma t)^n/n! Phi^n.

This is a genuine state-independent Poisson proposal representation with rate gamma and CPTP event Phi. The local dimension is d_X of the support X, not the global system/reference dimension; tensoring identity outside X preserves locality and complete positivity. If epsilon=0 and G=0 the term can be omitted. A positive conservative bound can instead be used to choose gamma, paying unnecessary but legitimate additional noise.

For the root's HP/TA normalization ||G_X||diamond<=2epsilon_X, the already chosen padding gamma_X=2d_X²epsilon_X suffices. On a finite system the independently clocked local CP events, interleaved with the ideal evolution, have average generator

L_modified = L0 + sum_X gamma_X(Phi_X-Id).

This equality holds for full system/reference channels. Phi_X may be unknown; it is an analytical decomposition of the actual padded dynamics, not a demand that the controller identify or implement the unknown noise map. If known upper bounds satisfy sum_(X contains v) epsilon_X<=epsilon_site and d_X<=D, the per-site error-clock intensity is at most 2D²epsilon_site. If instead only an aggregate site bound is supplied and every admissible support template is padded at its individual worst-case bound, charge the template-incidence factor explicitly. No hidden tailoring of physical padding to unknown E_X is allowed.

Why the generic uniformization counterexample is untouched

For unpadded amplitude damping G=kappa D_(|0><1|), Id+G/gamma has a Choi principal2×2 block with determinant -(kappa/gamma)²/4<0 for every finite gamma. Thus arbitrary GKLS generators are not being asserted to have exact positive Euler-event uniformization. Here the full-rank Choi floor comes from physically adding gamma(T-Id); Phi is centered at T, not Id. Apply this construction only to the small residual perturbation, leaving strong ideal Hamiltonian/control dynamics in L0. Padding a strong ideal term would pay a correspondingly strong error rate.

Wolf–Eisert–Cubitt–Cirac arXiv0711.3172v2, §IV, directly establishes the prior mechanism of adding isotropic generator noise to restore Lindblad form. The full-Choi bound above is an elementary stronger sufficient representation for this assembly; no historical novelty is claimed for depolarizing completion or Poisson channel generators.

Physical and model boundaries

The device is changed. Full-support depolarization is a real added error process, with support/rate/implementation costs. Onsite noise alone does not provide the needed full-rank Choi floor for a larger entangling support X. All allowed local support templates must be covered at their known bounds. The analytic event clocks introduce no additional physical detector or history tape, but their existence does not remove the actual reservoir/reset requirements of the added depolarization.

Padding calibration faults belong in the total G budget. If padding error is known only through ||G_cal||diamond<=eta gamma and pre-padding residual norm is at most epsilon0, a conservative self-consistent sufficient condition is

gamma >= d²(epsilon0+eta gamma).

This requires d²eta<1 and then gamma>=d²epsilon0/(1-d²eta). A strict known noise margin or a fixed absolute total-error promise avoids circular calibration accounting. The HP/TA normalization factor and any new implementation support must be included when translating these symbols back to the original hardware model. Markovian, local, bounded-dimensional premises remain; arbitrary nonlocal or non-Markovian faults are not covered.

After this change, error locations really can be sampled by independent rare clocks and event values are arbitrary local CPTP channels. They are not necessarily Pauli/classical errors. This substantially simplifies joint clock/noise witness accounting. A local error can still corrupt an epoch/pointer and cause persistent semantic damage; positivity does not prove scheduler/decoder strong simulation, live capture, destination service or rolling-window commit.

Finite complex diagnostics

check_padded_cp_clock.py / padded_cp_clock_check.json test36 complex signed HP/TA perturbations in dimensions2,3,4 with analytic diamond-norm upper bounds. All Phi Choi matrices were positive and TP. Minimum tested Phi Choi eigenvalue:0.22299116156670787. Maximum TP error:2.22e-16; generator-identity entry error:4.55e-13. Direct numerical semigroup versus Poisson-series comparison at gamma t=0.3,3 differed by at most1.84e-15. These floating checks supplement the exact Choi proof; they are not norm certificates, threshold tests or physical demonstrations.

Fixed-box theorem and continuous hybrid limit

Joint fixed-box estimate: finite product

9 November 2026. Component theorem only; no novelty or autonomous-threshold claim.

Let C_N ... C_1 be CPTP channels. Choose ideal CPTP A_i and define F_i=C_i-A_i, f_i=||F_i||diamond. Fix r marked index sets G_j, with sum{i in G_j}f_i<=b and each index in at most K groups. In ONE common global A/F expansion let E(S) sum terms whose F-index set hits every G_j; all other faults are unrestricted. With U=union G_j, B=sum_{i in U}f_i<=rb and m=ceil(r/K),

||E(S)||diamond <= sum{q>=m}B^q/q! <= exp(B)B^m/m!.

If eKb<=1, then

||E(S)||_diamond <= [exp(b)(eKb)^(1/K)]^r.                 (1)

Proof: outside U sum A/F choices exactly to actual C_i, each of norm1. This merely regroups the common expansion. Each hitting subset Q inside U has at least m insertions and norm at most product_{i in Q}f_i. Its degree-q scalar sum is bounded by B^q/q!, since B^q contains each distinct-index product q! times plus nonnegative repeated-index terms. The factorial inequality (m+s)!>=m!s! gives the exponential-tail bound. For B>0, m!>=(m/e)^m and B/m<=Kb give exp(B)B^m/m!<=exp(rb)(eKb)^m. Since eKb<=1 and m>=r/K, this implies (1). B=0 is trivial. QED.

For disjoint groups the sharper bound product_j[exp(B_j)-1], B_j=sum_{i in G_j}f_i, follows by factoring the positive scalar subset sum.

No positivity is attributed to F_i. No exponential in exterior system volume appears: exterior choices were resummed to physical channels. The K-th-root loss is necessary in general, since one insertion can hit K marked groups.

Continuous-time theorem and canonical limit

On a finite lattice let K_x(t), L_x(t) be bounded piecewise-continuous local GKLS generators on the SAME assigned support X_x. Put epsilon_x(t)=||K_x(t)-L_x(t)||_diamond. The difference need not itself be GKLS.

Fix deterministic half-open spacetime boxes with an endpoint convention. Let G_j contain local-term/time pairs (x,t) whose assigned support at t touches box j. Assume every pair belongs to at most K groups uniformly in size/mesh, and each integral sum_{x:(x,t) in G_j}epsilon_x(t)dt<=b.

For Tsubset of marked boxes, form the hybrid generator H^(Tsubset) by replacing the ENTIRE K_x by L_x whenever (x,t) belongs to a group selected by Tsubset; otherwise retain K_x. Each hybrid is physical GKLS. Let U^(Tsubset) denote its propagator. Define

E(S)=sum_{Tsubset subset S}(-1)^|Tsubset| U^(Tsubset).    (2)

Then (1) holds for (2). To prove this, use a common refined Lie-Trotter grid respecting coefficient/box boundaries. Exact local actual/ideal propagators are CPTP, and Duhamel with complete trace-norm contractivity gives ||C_i-A_i||_diamond<=integral_over_factor epsilon_x(t)dt. At finite mesh inclusion-exclusion equates (2)'s hybrid product sum with the hitting sum: paths missing a marked group cancel, all-group hitters survive. All 2^r physical hybrid products converge by the finite-dimensional GKLS product formula; the uniform bound passes to their diamond-norm limit. No Euler CP approximation is used. QED.

Prior machinery: Kliesch–Barthel–Gogolin–Kastoryano–Eisert, arXiv1105.3986v2 Theorem1/AppendicesA–B for GKLS product formulas and propagator estimates; complete trace-norm contraction follows by adjoining arbitrary untouched references. No quantitative simulation-runtime bound is needed here. Destination joint-fault interfaces: AGP quant-ph/0504218v3 Section11; DST2601.20818v3 Definition3.

Exact open interfaces

This covers matched physical local GKLS terms, including additive GKLS/Hamiltonian noise via ideal-zero terms. It does not show that arbitrary signed local E with only TOTAL L+E physical admits close positive local matching. A separate depolarizing-completion construction may repair that input restriction, with paid added physical noise.

No actual autonomous macro-locations, controller-damage witnesses, protected WAIT, repaired frontier or gadget correctness are supplied. Such semantic statements and a compatible contracting recursion remain needed.

Conditioning on ideal Poisson clocks with arbitrary signed engineered E is NOT free: between proposals E may not generate CP evolution, invalidating norm-1 exterior resummation. Additive local GKLS noise does have a physical conditional background. The joint fixed-box clock/noise witness argument is supplied in mixed_clock_noise.md; local_gauge_and_testers.md removes the individual HP/TA decomposition premise before paid completion.

Equation(2) defines an analytic fault decomposition, not an efficient computation: explicit evaluation may require 2^r hybrid evolutions.

Joint classical-clock and signed quantum-fault estimate

Joint clock and residual-noise estimate

Let L0=sum kappa_alpha(Phi_alpha-Id), with local CPTP ideal proposal channels, and R=sum R_x with local GKLS residual terms. Sample exogenous ideal Poisson attempts. Conditional on their full history omega, the system undergoes CPTP Phi events interleaved with physical R propagators.

Apply fixed_box_lemma.md to residual factors expanded about identity. If each deterministic marked box has integrated residual norm <=b and each elementary factor touches <=K boxes, the conditional hitting sum D_Sn(omega) has diamond norm <=eta_n^|Sn| uniformly in omega, eta_n=exp(b)(eKb)^(1/K), eKb<=1. The budget depends on support-time, not number of proposals.

Suppose fixed proposal-clock events E_j satisfy P(all j in Sc bad)<=q^|Sc|. Then

||integral 1_{all Sc bad} D_Sn(omega)dP(omega)||diamond <= q^|Sc| eta_n^|Sn|.

This is triangle inequality plus the uniform conditional bound, not an independence claim about quantum faults.

For combined badness (clock event E_j OR residual subset hits box j), partition omega by its EXACT clock-bad subset T within S. The remaining S minus T must be residual-hit. Summing the restricted fault sums gives

||E_bad(S)||diamond <= sum_{T subset S} q^|T| eta_n^(|S|-|T|) = (q+eta_n)^|S|.

Exact-T partition is essential: a probability union bound alone cannot be applied to non-CP fault sums. Finite inclusion-exclusion of hybrid residual generators deleting selected R_x defines the continuous hitting sums; each conditional hybrid remains CPTP.

This does not yet connect actual repaired macro-location failures to these fixed witnesses, protect WAIT, implement recurring commits or close the hierarchy.

Local frames, finite windows, causal rails, QND memory and finite progress

Constructive causal representation bridge

9 November 2026. Two bounded representation lemmas below have complete algebraic proofs. Neither supplies a continuous-time autonomous threshold. The recursive closure question is recorded separately.

G. Exact local covariant frame repair

Let F_i be a finite frame register, Q_i a finite payload register, and P_{i,f} specified payload unitaries. Define W_i=sum_f |f><f| tensor P_{i,f}, W=tensor_i W_i, and D(rho)=Tr_F(W†rho W).

A stochastic frame transition T(f'|f) has covariant CPTP Kraus operators

K_f'f = sqrt(T(f'|f)) |f'><f| tensor P_f' P_f†.

Completeness follows by summing T(f'|f) over f'. Direct multiplication gives D Lift(T)=D on arbitrary operators, including arbitrary external references. Replacing the transport by P_f' A_a P_f† for Kraus A_a of payload channel C gives D Lift_T(C)=C D. Frame dephasing is intentional; D itself ignores off-diagonal frame coherences, so this identity is not restricted to classical product inputs.

For arbitrary finite frame GKLS generator L_F and payload GKLS generator R, put

L_cov = Ad_W (L_F tensor Id + Id tensor R) Ad_W†.

Unitary conjugation preserves GKLS. The two terms commute before conjugation, so

exp(t L_cov)=Ad_W (exp(t L_F) tensor exp(t R)) Ad_W†,
D exp(t L_cov)=exp(t R) D.                                (G1)

Tensoring with Id_reference proves the full-reference claim. No postselection or terminal ancilla measurement is needed.

For any local linear perturbation E_X, including a non-CP generator difference, E'_X=Ad_W† E_X Ad_W has the same diamond norm. Onsite product W preserves support exactly; a fixed-depth bounded-range W enlarges support only by its fixed light cone, paying its bounded overlap in per-site norm density. This is an exact coordinate change, not positive-probability noise uniformization.

A bare frame bit flip without the compensating transport is NOT harmless: decoded data undergo P_f'†P_f. It is a local quantum fault. Every intended covariant repair costs real quantum gates and noise on the entire transport footprint. An operation counter cannot be called gauge unless that transport is actually implemented locally.

For one exclusively owned bounded gate U, choose P_0=I,P_1=U. Intended done-flag changes 0→1 apply U; 1→0 apply U†. All intended repair/retry paths telescope. Export at flag1 gives U independent of the internal path. This can remove historical truthfulness of one done flag; it does not repair ambiguous ownership or NEXTOP. Irreversible resets cannot be inverted without retained, charged Stinespring workspace.

T. Moving-code idle protection for partial transversal progress

Suppose R is an already specified local idle-recovery generator. Let U_i act on disjoint bounded footprints (e.g. physical pairs of one transversal gate), with binary progress frames s_i. Define P_s=product_i U_i^(s_i) and W=product_i controlled-U_i. This W has fixed local depth. For a local frame generator L_s, use

L_mov=Ad_W (L_s tensor Id + Id tensor R) Ad_W†.             (T1)

Starting with all progress frames zero, exact evolution is

rho(t)=W[sigma_s(t) tensor exp(t R)(rho_in)]W†,
sigma_s(t)=exp(t L_s)(|0...0><0...0|).                     (T2)

If the frames are classical, branch s has payload P_s exp(tR)(rho_in)P_s†. Thus the instantaneous code is P_s C and recovery is P_s R P_s†. Idle recovery is never disabled during asynchronous partial progress or intended frame repair. Full-reference equality follows from (G1). Transformed recovery terms involving paired blocks and nearby flags must really be engineered; their support, rates and noise are paid.

This removes a frozen-data WAIT assumption ONLY for this restricted device, conditional on the acquired protection of R under the relevant noise. It does not derive that protection. At all s_i=1 the physical output is P_all applied to the idle-evolved input. A fixed logical endpoint decoder still needs the ordinary code/gadget intertwining condition, or paid trailing EC with a bounded-spread condition. No gate-dependent free decoder is supplied.

No local ALL-DONE collector, safe recurring progress-frame reset, or recursive compiler for the transformed recovery is supplied yet. In particular a logical extended unitary may not be silently treated as a bounded-range physical interaction. General nonunitary gadgets require a charged workspace lifecycle before this representation can apply.

C. Why a flat finite gauge does not close recurrence

Closed-cycle obstruction. Let a finite controller graph have unitary edge transports U_ba=V_b V_a†. For any closed walk a_0,a_1,...,a_k=a_0, the physical payload transport is

U_a0,a(k-1) ... U_a2,a1 U_a1,a0 = V_a0 V_a0† = I.

Therefore a recurring controller which returns to the same physical frame/workspace state cannot execute a nontrivial logical gate solely through flat PI transport. This remains true for noncommuting V_a because adjacent factors cancel in their actual order. A real computation needs a non-gauge COMMIT/holonomy, a physically changed payload location, or a consumed/retained resource. That event is where one-time causal advancement must be proved.

For Lemma T, after all flags reach1 the gauge-covariant reset back to0 applies P_all† and undoes the intended gate. Resetting flags without that inverse is a non-gauge commit. Calling that reset a free gauge fixing hides the missing one-shot-history obligation.

Accumulated-prefix locality obstruction. Let V_m=CNOT_(m,m+1)...CNOT_(1,2) on a chain. Then V_m X_1 V_m†=X_1...X_(m+1). If a mutable one-bit receipt represents whether an early X_1 happened before this prefix, changing that receipt at the current cut requires the displayed extensive transport to preserve decoded state. No channel on a fixed-radius neighborhood can implement this unitary on all reference-entangled inputs: a distant endpoint observable Z_(m+1) changes sign under the string but is unchanged by a channel supported elsewhere. Hence accumulated global program history is not an onsite frame with uniform locality.

Fault-tolerant circuit windows can limit such propagation through paid EC; that is a possible route, not a theorem that all histories have a constant-depth gauge. A successful recurring construction must specify canonicalization at each paid EC boundary, preserve the one-shot commit through reconstruction, and run lower-level maintenance while that commit is pending. The present two lemmas do not eliminate those obligations.

R. Exact clean one-shot CPTP rails

Let a finite circuit DAG have one quantum port per wire segment, no branching that copies a quantum wire, and bounded gate arity. Each wire port has H_tilde=C|vac> direct-sum H_payload. Require every gate to have at least one consumed input port; a preparation-only gate can use a one-dimensional activation-token input. This activation token is paid and prevents source gates from firing repeatedly.

For gate v with CPTP Kraus A_va:H_in→H_out, let J_in embed occupied inputs and vacant outputs in its local footprint, and J_out embed vacant inputs and occupied outputs. Set

B_va=J_out A_va J_in†,   P_v=J_in J_in†,   Q_v=I-P_v,
Phi_v(rho)=sum_a B_va rho B_va† + Q_v rho Q_v.              (R1)

Since sum_a B_va†B_va=P_v, (R1) is CPTP. lambda_v(Phi_v-Id) is an exactly legitimate CP-event GKLS term; no generic-GKLS uniformization is claimed.

A legal configuration is indexed by an order ideal I of completed gates. Ports crossing from the completed past to uncompleted future are occupied; all other ports are vacant. On that sector, Phi_v either acts as identity (v not enabled) or executes exactly C_v and transfers the payload to the new cut I union{v}. Completed gates cannot fire again because their consumed input ports stay vacant. Incomparable enabled gates have disjoint ports and commute, including their arbitrary CPTP Kraus effects.

Thus for any input rho entangled with any reference, the exact continuous-time state is

sum_I p_t(I) J_I [(C_I tensor Id_ref)(rho)] J_I†.           (R2)

C_I is independent of the topological ordering: any two linear extensions differ by swaps of incomparable disjoint operations. p_t is a purely classical order-ideal birth process, with rate lambda_v for each enabled gate, independent of the quantum input. This proves the full-reference causal-cut statement, not only equality of terminal completion bits. Instrument outcomes/adaptive classical data can be included as ordinary retained payload ports; their causal inputs must still be respected.

For lambda_v≥lambda>0, successful completion times satisfy T_v=max_(u predecessor v) T_u+E_v, with independent E_v~Exp(lambda_v), by the memoryless property of independent proposal clocks. If G gates have depth≤D and indegree≤b (use b≥1), the number of directed source-to-vertex paths of length≤D is at most G times (b+1)^D. Chernoff with theta=lambda/2 bounds each path sum by exp(-lambda t/2)2^D. A conservative consequence is

P(T_all > (2/lambda)[D log(2(b+1))+log(G/delta)]) ≤ delta. (R3)

The spatial wire count is O(G), with one-use activation tokens and any Stinespring/instrument workspace counted. Bounded arity does not guarantee a fixed-dimensional geometric embedding; layout/wire length must be paid separately. In particular O(G) space does not meet an indefinitely recurring memory contract.

Deleting a live token can permanently block a downstream gate and all descendants. A forged occupancy can execute a gate using a replacement payload and destroy the order-ideal invariant. On a reused cyclic rail, an old token can be mistaken for a new epoch (ABA). These faults are not handled by (R2)-(R3). Timeouts, erasure replacement and fail-closed repair require their own deterministic causal-damage and recurrence proofs; clean service tails do not provide them.

F. General finite-depth windows: remove internal causal eligibility

Lemma T extends beyond disjoint transversal gates. Take any fixed-depth D, bounded-range unitary circuit window, with disjoint gates within each layer. Attach one binary flag s_g to each gate and form W by replacing every U_g in the original layer order with controlled-U_g. W has depth D and fixed interaction radius. For each complete flag configuration s, its payload action P_s is the original ordered circuit with the unselected gates replaced by identity.

Use the same conjugation as (T1), now with this W and an arbitrary local flag process. An intended flag update at g is physically lifted by W (flag update) W†. Its support is the depth-D light cone of g, uniformly bounded when D is fixed. Different flag updates can occur in any temporal order, including backwards repairs. Their payload transports telescope, so a branch from all0 to all1 implements the intended entire noncommuting window. No internal gate-predecessor eligibility test is needed. Covariantly transformed idle recovery remains active throughout. This is an exact channel construction; compensated operations when flags change are charged physical operations, not a classical relabeling.

This finite-window result is stronger than the clean rail's ordering invariant: it tolerates arbitrary intended internal schedule reorderings by real compensating transport. It still does not tolerate arbitrary unaccompanied record faults for free; those are bounded-light-cone data faults in decoded coordinates.

Its limitation is exact: D must be bounded in physical depth, not merely number of logical gadget layers. If D grows with hierarchy level, locality may grow too. Conjugating a lower-level recovery by a putative constant-depth logical circuit is not a physical construction until all logical interactions/routing have been compiled with size-uniform support. No such recursive closure is proved here.

For memory-only EC cycles the net logical action is identity, which may ease the closed-cycle obstruction. But the physical syndrome/workspace channel is nonunitary, and its reset can still erase needed history. A unitary dilation is legitimate only with its ancillas retained until a specified safe commit and reset. That lifecycle is the next constructive obligation.

P. Onsite frames combined with clean rails

Give every rail port an onsite finite Pauli frame and extend its P_f by identity on vacuum. Conjugate the entire rail generator and an independent local frame process by the product W over ports. Each physical gate becomes the local P_out C_v P_in† transport on its own ports. The clean physical-cut invariant survives in decoded coordinates; all intended frame repair is local and covariant. Final frame correction is onsite Pauli and paid. It is not a free arbitrary-prefix final decoder. Deleted/forged tokens and cyclic reuse remain unresolved.

Q. Memory-only alternative: commuting QND and virtual Pauli feedback

Quantum data stay in fixed registers and undergo commuting stabilizer measurements. A classical streaming decoder updates explicit nearby Pauli-frame bits; it applies no physical Pauli correction. The following reduction is exact; live intake, reliable streaming and rolling buffers are not supplied by it.

Let S_a be commuting local Pauli checks, M_a,sigma=(I+sigma S_a)/2. Next to each data qubit place two explicit frame bits F_i=(x_i,z_i), P_f=product_i X_i^(x_i)Z_i^(z_i), and

W=tensor_i sum_(x,z) |x,z><x,z|_F_i tensor X_i^x Z_i^z.

W is NOT controlled by the global syndrome history or decoder output. Define chi_a(f) by P_f†S_aP_f=chi_a(f)S_a. It reads only frame bits adjacent to supp(S_a).

Q1. Full-reference monitoring instrument

At an ideal physical check, read/dephase the nearby frame bits f, measure S_a with raw outcome sigma, and publish tau=chi_a(f)sigma. The parity must be captured AT measurement time. This is a bounded-support CP event; a decomposed implementation must charge its real gates/noise. Its Kraus operators, including a fresh classical record R, are

K_phys(f,sigma)=|f><f| tensor M_a,sigma tensor |chi_a(f)sigma>_R.

Conjugation gives

W† K_phys(f,sigma) W
   =|f><f| tensor M_a,chi_a(f)sigma tensor |chi_a(f)sigma>_R.

Rename tau=chi_a(f)sigma. This is the standard virtual stabilizer instrument publishing its measured outcome tau, plus dephasing of explicitly classical frame bits. A classical buffer guard can control the CP event, making it identity when disabled. The equation holds on arbitrary operators, including coherent frame faults and arbitrary external-reference entanglement, and retains the measurement record.

Q2. Frame updates are virtual active corrections

A local physical classical transition changing (c,f) to (c',f') and leaving data untouched has Kraus alpha |c',f'><c,f| tensor I. Its virtual Kraus operator is exactly

alpha |c',f'><c,f| tensor P_f'† P_f.                      (Q1)

If the command changes frame bits only in B, this Pauli is supported in B. Therefore physical QND monitoring with a classical frame decoder is exactly conjugate to active QEC with the SAME causal decoder and local virtual Pauli feedback. A classical malfunction may issue many commands and still needs its own damage/failure theorem. A bare frame-cache error becomes a local quantum/controller fault; it is not harmless.

Q3. Arbitrary local coherent/GKLS faults

For the FULL joint physical generator, including data, records, caches and internal decoder registers, set

L_virt=Ad_W† L_phys Ad_W.

It is time independent whenever L_phys is, and GKLS whenever L_phys is. Every local linear perturbation E_X becomes E'_X=Ad_W†E_XAd_W with the same cell support and diamond norm. This covers coherent/non-Pauli faults on data AND controllers, and non-CP differences of physical generators. If frame bits and data are neighboring separate sites, pay the fixed support enlargement.

The conjugacy is applied before conditioning on any record. It neither assumes outcomes independent of input nor turns signed faults into probabilities. Tensoring with Id_reference proves full-reference equality. It holds term by term after inserting arbitrary local linear fault maps in the actual chronological composition. Ideal frame timing can be retained as an output instrument; do not normalize a successful branch of the perturbed process and keep its unconditional error bound.

Q4. What commutation removes

The ideal stabilizer projectors commute and same-check projectors are idempotent. Duplicate or retimed ideal checks thus do not require quantum gate-order reconstruction. They must NOT be commuted past arbitrary noise insertions for free. The actual record chronology is retained.

An unrecorded intended check preserves every encoded input and its reference exactly; off the code it dephases syndrome sectors. An overflow therefore loses a classical syndrome observation rather than resetting an unknown logical payload. Missing, overwritten, delayed or mislabeled records still need a local phenomenological-fault/witness theorem. Using a later frame value for the measurement-time relabel without a causal log gives a false virtual instrument; Q1 explicitly captures the local label.

The remaining implication is active-QEC-with-unreliable-local-classical-processing to a correct finite-resource streaming memory. No noiseless external decoder, perfect source timestamps, infinite record tape or live-input theorem from a preloaded-computation theorem is assumed. Non-Clifford/universal computing requires an additional interface; the QND argument is currently memory-only.

Q5. Precise finite-memory interface and remaining theorem

Record ports. The fresh output register in Q1 is an instrument notation, not a free infinite tape. A physical implementation may use a fixed local alphabet {empty,+,-} and enable a check only at an empty port. On that sector use |chi(f)sigma><empty| together with the displayed frame/projector Kraus operators; on the occupied sector use the complementary identity Kraus operator. Their adjoint products sum to identity, and conjugacy by W is unchanged. An explicit local reset can clear an occupied port (losing that observation) and is itself a paid noisy CP event. With unrestricted overwrite one instead sums Kraus operators |chi(f)sigma><r| over all old port symbols r; that also is CPTP, but loses the previous report. Neither choice proves delivery. Every parity latch, queue, reset and transfer register belongs to the finite device and the perturbation budget.

Required theorem, stated separately from the acquired algebra. Fix a concrete local streaming stabilizer decoder A_L with a proved memory threshold for its actual observation model. Construct a finite, time-independent, bounded-range, bounded-rate classical controller in three dimensions that continuously accepts the O(L^2) distributed raw check ports of a two-dimensional quantum code. Local state alphabets and physical rate/noise constants must be independent of L and storage time T. Total volume, latency and retained history may be polynomial in L and must be counted; the live input must not be replaced by a pre-encoded immutable tape.

Its correctness statement must hold uniformly for arbitrary input-record histories and adaptive quantum/reference contexts: until a rare declared controller failure, its local frame-command instrument agrees with A_L on the actual causal observations, allowing only a specified bounded-latency/erasure transformation. The extra erasures, mislabels and wrong commands caused by intake, framing and reusable buffers must have a joint local fault-cover bound tending to zero with physical noise. Alternatively, a hierarchical cover is acceptable if every scale's spatial and temporal dilation and probability/norm cost is stated. The rare global controller failure must be bounded by poly(L) T exp[-c L^a] for constants c,a>0. This is a destination theorem, not an imported result.

In particular, one corrupted pointer/epoch cannot silently shift an unlimited temporal strip of reports; a lost report cannot leave the source permanently blocked; and stale data cannot become a current report after a finite buffer wraps. A construction must prove eventual resynchronization with a charged fault cover rather than assume trustworthy timestamps, reset flags or globally coordinated rounds. Report-to-check association and the parity captured at measurement time must survive the same audit.

The quantum threshold to compose with that theorem must itself allow the resulting bounded-delay irregular QND monitoring, the accounted local data/controller norm faults, and the specified input-erasure model. Commutativity alone does not prove a threshold under arbitrary gaps. Polynomial decoding latency is not automatically harmless: errors accumulated during that latency must remain represented in retained syndrome history and pending frame state. A final all-reference decoded-channel bound and readout operation must include the residual pending history/frame correction.

If quantum code distance is L and the complete three-dimensional implementation has linear size O(L^b), a lifetime exp(c L^a) is still exp(c' L_total^(a/b)); polynomial controller overhead therefore fits a stretched-exponential version of the dossier's geometric target. It does not fit an uncharged two-dimensional boundary export: the O(L^2) distributed intake needs sufficient bulk bandwidth. Exact exponents remain construction-dependent.

Verdict. Q1–Q3 are proved representation identities, and Q4 eliminates noncommuting quantum schedule reconstruction for this memory-only architecture. Q5 is genuinely unproved here. Neither a static-input Gacs computation theorem nor a noiseless-classical streaming decoder closes it. Universal computation/non-Clifford feedforward is a further problem. Thus this is a concrete reduction and a sharper candidate construction, not a solution of the full continuous-time autonomous FT target.

U. Audited finite progress-to-Poisson-word lemma

Let S be a finite classical state set, B a forward-invariant target set, and {f_a:S→S} a finite alphabet of deterministic total transition maps. Suppose every s outside B admits a word taking s into B. If n=|S\B|, there is one word w, independent of the initial state, of length at most n^2 taking every state into B.

Proof: quotient B to a single absorbing sink. Track the set I of non-sink images of all initial states under the word constructed so far. Pick s in I. A shortest path from s to the sink has no repeated non-sink vertex, hence length at most n. Append its labels. At least s disappears from I, and no sink image can return; thus |I| decreases by at least one. At most n iterations suffice. This proves reachability to an absorbing set, not synchronization of the final underlying non-target registers. For a one-time progress event, append a bookkeeping bit which stays set forever after the event; that flag is a proof variable, not a reliable physical memory supplied for free.

If independent exogenous proposal clocks have rates lambda_a>0, let Lambda=sum_a lambda_a include every clock whose action could affect this closed state machine. Divide time into |w| slots of length delta. Requiring exactly one proposal of the requested label and zero other relevant proposals in each slot implements w exactly, with probability

p = exp[-Lambda delta |w|] product_(j=1)^|w| (lambda_(w_j) delta) > 0.

Choose delta=1/Lambda to get p≥(lambda_min/(e Lambda))^|w|. From every initial state the target is therefore hit by time tau=|w|/Lambda with probability at least p. Fresh disjoint blocks yield a conditional tail ≤(1-p)^k after k blocks. The same conclusion holds from an adaptive start for these independent clocks, provided the finite closed-state and deterministic-map hypotheses still hold. Constants can be catastrophically small: n itself may grow exponentially in all link registers. This is useful for fixed-size links; it gives no efficient uniform controller rate when applied wholesale to a growing decoder.

Necessary audit conditions: all invalid PC/counter/packet encodings must be included and have a target-reaching path for the same persistent request; every needed channel-delivery/loss choice must be represented by a positive-rate proposal map; outside actions during the word must be suppressed by a finite guard region or proved irrelevant; and quantum outcomes/live changing inputs cannot silently be treated as deterministic letters. A universal word for possible nondeterministic choices is insufficient against adversarial choices. The word proves occurrence, not correct exactly-once delivery or bounded ghost/duplicate damage; those require the link specification separately.

Weak fairness by itself does not yield the positive probability or latency bound. Even a two-state system may remain outside the target for any prescribed finite number of steps while still eventually taking its fair progress transition. Likewise, if the target is not absorbing, individual reachability does not imply one word ending all states there (a two-state permutation is a counterexample); the event flag matters.

Primary scope check (corrected final source): Dolev–Dubois–Potop-Butucaru–Tixeuil, arXiv:1011.3632v2 (7 February 2011), Sections2–4, Theorem4: bounded non-FIFO unreliable channels and arbitrary initial state; (0,1,1,1) link specification including reordering. Section2.2 states the corrected trace property R(E)=S(E) or R(E)=m.S(E), with at most one extra initial delivery m. The channel model permits unbounded delivery latency and requires weak fairness, so the paper alone does not provide the exponential service tail. Its serialized application Send calls and finite known channel capacity must be matched by any physical compiler. This source-scope correction leaves the universal-word proof above unchanged. https://arxiv.org/html/1011.3632v2

S. Synchronization strings: matched framing machinery

S1. Primary imports checked

Haeupler–Shahrasbi–Vitercik, arXiv:1707.04233v2 (20 March 2018), Sections2–3, Algorithm1, Theorem3.3: for n one-way uses, edit fraction delta<1/7, and an epsilon-synchronization string, the simulation gives n(1-delta) corruption-channel symbols with at most 2n delta[2+1/(1-epsilon)] corruptions, subject to the product-alphabet condition. Algorithm1 initializes sender index i and receiver index I_B, assuming reliable local computation. Its interactive message-driven model restricts errors to deletion-followed-by-insertion edits to avoid hangs; the one-way model permits ordinary insertions/deletions. This is not a timeout theorem. https://arxiv.org/html/1707.04233v2

Haeupler–Shahrasbi, arXiv:1710.09795v2 (10 November 2017), Theorems5.2,7.1,7.2 and proofs: Theorem5.2 correctly indexes from the last O(log n) received symbols in O(log^3 n) work if relative suffix edit density is below 1-epsilon/2. The infinite Theorem7.1 uses the last O(log i) symbols AND the number received; its proof uses that number to locate a geometric-scale block. Theorem7.2 uses O(log n) state and near-linear total work. Channel edits are the modeled faults, with reliable endpoints/computation. Infinite strings remove foreknowledge of termination, not growing counter/history storage. https://arxiv.org/html/1710.09795v2

Source-index convention: edits are counted between transmitted source positions, not fixed physical-time boxes. The original paper's published Error Count and Relative Suffix Error Density definitions are Definitions5.12–5.13 (2021 JACM version), visible in the primary NSF full-text search index. Direct full-text fetch timed out; no additional theorem is imported from that failed fetch. https://par.nsf.gov/servlets/purl/10314785

S2. Audited one-sided scalar witness lemma

Root proposed this conditional combinatorial lift, checked here. Let E be a random subset of a FIXED integer slot lattice with P(F subset E)≤eta^|F| for every finite F. Call t bad if some interval [t-ell+1,t] contains at least alpha ell errors, 0<alpha≤1. For r fixed marked positions, put q=4 eta^alpha<1. Then

P(all r marked positions bad)
   ≤ 2^r sum_(L≥r) q^L
   ≤ [8 eta^alpha/(1-4 eta^alpha)]^r.                   (S1)

Proof: take the rightmost remaining marked position t and any dense suffix witness I=[a,t]; remove all marked positions in I. Every remaining marker is strictly left of a, and every later suffix ending at one of them lies strictly left of I. The selected witnesses are therefore pairwise disjoint and cover all r markers; their total integer length L≥r. No dilation or factor-three loss is needed.

Their right endpoints form a subset of the r fixed markers (at most2^r choices). For that ordered subset, positive lengths totaling L have at most2^L compositions. Within the disjoint intervals, selecting sufficient error sites costs at most2^L choices; their total cardinality is at least alpha L, so each is bounded by eta^(alpha L). Summation proves the first inequality. The second uses q^r/(1-q)≤[q/(1-q)]^r for r≥1. The earlier general-interval 3-cover bound is correct but weaker; suffix orientation gives this improvement. No independent errors are required.

Thus pointwise suffix-density correctness offers useful interval certificates beyond a global edit-fraction guarantee. This is probability-only and assumes correct execution of the indexing algorithm; no signed fault-norm lift is asserted.

S3. Exact destination and remaining interfaces

The next matched representation is an indexed classical syndrome stream with dense suffix-interval certificates. To compose it with fixed-box norm analysis, first prove an edit-to-physical-box map: bound edits produced by each damaged region, insertion multiplicity, and source-index interval dilation into physical spacetime using paid service. If one bad source slot can generate at most b edits, the analogous binary fault-site witness uses effective density alpha/b. A symbol corruption can be charged as deletion plus insertion. An unbounded stall has no finite edit count and is not fixed merely by indexing.

Locality in received symbols is not spatial locality or constant physical processing time. Internal counter upset lies outside the channel-error model: the theorem may cease applying even if no channel edit occurred. Sender index, receive count, rolling window, decoder workspace and publication queue need the same noisy autonomous implementation and repair audit. A global trace/fraction bound does not prove S1's fixed-lattice hypothesis.

For a chosen horizon T_L=exp(poly(L)), O(log T_L) counter/window storage and polylogarithmic work per report are polynomial in L and may be paid in finite three-dimensional hardware. This avoids treating infinite strings as intrinsically disqualified. It still requires a counted parallel/pipelined implementation sustaining the quantum plane's arrival rate, protected counters through the chosen horizon, and safe finite-capacity endpoint behavior. Indefinite recurrence with fixed resources requires reusable framing/resynchronization; the imported theorems provide no wraparound/reset guarantee.

Verdict: synchronization strings supply a sharply matched representation and pointwise certificates for a conditional joint-witness lift. They do not by themselves close physical framing, live intake, reliable classical processing, finite recurrence, or the quantum threshold. DDPT's bounded extra-prefix trace and paid finite-link service constrain some interfaces; composition still needs an explicit physical state machine and fault-cover proof.

S4. Paid CP-clock completion removes the signed-subset obstacle for this design

Audited root's work/ctqec/poisson_completion.md. For local HP trace-annihilating G with diamond norm≤epsilon, use the unnormalized Choi convention. J(T)=I/d for the full replacement channel T, and ||J(G)||op≤||J(G)||1≤d epsilon. Hence gamma=d^2 epsilon makes Phi=T+G/gamma CPTP, and exactly

G+gamma(T-Id)=gamma(Phi-Id).

Zero epsilon is trivial. After the stated local HP/TA normalization, gamma_X=2d_X^2 epsilon_X is sufficient. This changes the physical device by adding paid full-support depolarization; it does not represent an unmodified arbitrary GKLS generator by CP clocks. Phi need not be computed or engineered: it is the proof representation of the modified noisy device. Added hardware imperfections and support-template incidence remain inside its self-consistent noise/rate budget.

The completed residual has genuine state-independent independent Poisson proposal clocks and arbitrary local CPTP actions. With integrated incident intensity≤mu per fixed box and each event hitting at most K marked boxes, the audited clock-counting bound is eta_res=(e K mu)^(1/K), for e K mu≤1. Adding independent ideal-clock bad witnesses q gives eta=q+eta_res. Restricting the full quantum process to a CLOCK-DEFINED witness event gives a positive mixture of CPTP maps, with diamond norm at most that event probability for arbitrary references. If a witness depends on quantum outcomes, a separate uniform envelope is required.

Consequently S1 can be used directly as a probability argument for this modified architecture ONCE the physical box-to-source-slot and bounded edit-charge maps are proved. No lift through signed fault subsets is then needed. Arbitrary CPTP error events still need not be bounded classical edits automatically: they may corrupt counters, create coherent controller states or trigger long error cascades. Captures, endpoint reliability, insertion multiplicity, decoder damage and recurring buffers remain unbuilt interfaces.

Positive analytic witness budget and exact recursive gap

What the analytic interface buys, and what it does not

Fix a physical local CP-event proposal rule L0=sum_a kappa_a(Phi_a-Id). Suppose the globally HP/TA perturbation E has a bounded local decomposition with per-site norm density epsilon. Normalize it locally as in local_gauge_and_testers.md and add the counted depolarizers. With maximum local support dimension D, the additive physical residual has per-site density at most C_D epsilon, C_D=2(1+2D²).

Choose deterministic witness boxes of fixed duration/volume; let V_H bound the integrated incident norm budget for unit per-site density. Then b<=C_D epsilon V_H. If a local insertion touches at most K marked boxes and fixed clock events obey the joint bound q_H^r, the joint bad-witness norm is at most

[q_H + exp(b)(eKb)^(1/K)]^r,  eKb<=1.

If q_H→0 as a finite design parameter H grows, any target witness strength 0<eta_<1 can be reached in the order: first choose fixed H with q_H<=eta_/2; then fix a positive epsilon satisfying

C_D epsilon V_H <= (eta_*/(2e))^K/(eK).

The last inequality implies b<=1 and exp(b)(eKb)^(1/K)<=eta_*/2. D, V_H and K are evaluated for that chosen design and then kept fixed as size/time scale. They may depend badly on H. This is an existence statement for the analytic witness budget; it supplies neither a device threshold nor useful rates/energies. The service q_H=beta_H^(1/chi) is available only under Proof S's clean, continuously eligible request premise.

If a separate actual-gadget theorem establishes eta_(j+1)<=C eta_j^s with fixed s>1, its algebraic solution is

eta_j <= C^(-1/(s-1)) [C^(1/(s-1)) eta_0]^(s^j).

For eta_0<C^(-1/(s-1)) this contracts rapidly. Deriving that gadget theorem for the real recurrent device, including records, repair, waiting and truncation/overlap bookkeeping, is precisely unfinished. An arbitrary subset of a signed fault sum is not bounded by the norm of its unrestricted parent sum. One must use the actual norm fault-path/gadget lemma, not a probability union bound in its place.

For the QND/frame memory route, the service module may no longer be the right sampler. Its sampling, buffer, classical damage and decoder witnesses must instead be built and checked. The displayed budget can consume those witnesses once supplied; it cannot invent them.

Governing primary sources

- [A] Astra governing dossier
Target and complete Proof S; service starts only after clean causal eligibility.

- [W] Wolf–Eisert–Cubitt–Cirac
Equation2, SectionIV isotropic-noise completion and Appendix. Completion is established prior machinery.

- [K] Kliesch et al.
Theorem1 and AppendicesA–B: physical local GKLS product formulas and propagator estimates.

- [AGP] Aliferis–Gottesman–Preskill
Section11, Eq59 and Lemmas8–9: operator-norm fault paths and contracting recursive gadgets, subject to their actual hypotheses.

- [PI] Ma–Li–Jiang
Definition1, Theorem1, AppendixA Eq14–15: path-independent algebra and controlled-unitary representation.

- [G] Gács, corrected v2
Strong classical simulation; Definition3.5 and Theorem6.1 constrain the imported input/output theorem to preloaded input.

- [GR] Gács–Reif (1988)
Journal version, Section2 Eq2.0/Theorem2.1 and Section3: synchronous real-time simulation with initially repeated inputs. Duke preprint publication-year imprint is inconsistent.

- [SBL] Selub–Bhardwaj–Lake
Sections1.1–1.3,2 and7: concrete streaming/constant-density decoder; noiseless classical operations and reliable clock assumed.

- [LAKE] Lake, offline decoder
Section6, Lemma6.2 and Corollary6.3: faithful clean desynchronization; not noisy online intake.

- [BDL] Balasubramanian–Davydova–Lake
Sections1.3 and6: synchronous local automaton and 3D layering; continuous Poisson extension explicitly not established.

- [DST] Dünnweber–Styliaris–Trivedi
Definition3, continuous-time discussion and SuppVII: synchronous noisy-control incumbent; formal continuous threshold deferred.

- [DOA] Drechsler–Oreg–Aharonov
Syndrome/Pauli continuous correspondence and Floquet lift; general time-independent lift remains open.

- [STR] Gutoski
Operational strategy norm for interactive adaptive contexts; terminal channel closeness alone is insufficient.

- [SUPER] Chiribella–D’Ariano–Perinotti
Physical-supermap realization: a composable open process needs its causal port interface.

- [BOX] Portmann et al.
Causal boxes: Definitions4.3/4.5 and Theorems6.7/6.11; representation/composition, not noisy hardware.

- [MC] Danos–Kashefi–Panangaden
Measurement-calculus dependencies/standardization; Pauli frames do not remove non-Clifford causal dependencies.

- [SDL] Dolev–Dubois–Potop-Butucaru–Tixeuil
Version2, Sections2–4, Theorem4: bounded-capacity self-stabilizing data link, bounded initial irregularity, weak fairness with unbounded latency.

- [SYNC] Haeupler–Shahrasbi–Vitercik
Algorithm1/Theorem3.3: message-driven insdel-to-corruption simulation; reliable initialized endpoints assumed.

- [LOCAL] Haeupler–Shahrasbi
Theorems5.2/7.1/7.2: local suffix-density correctness/infinite indexing; correct receive count and growing memory/work required.

Research record · Astra pin 3522a0e866bde8005e16aee40b9383da6515dfb4 · Full autonomous threshold unresolved
