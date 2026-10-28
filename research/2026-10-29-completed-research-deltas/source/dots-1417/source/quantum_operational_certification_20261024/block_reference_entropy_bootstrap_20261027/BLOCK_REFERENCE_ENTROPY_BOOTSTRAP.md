# Conditional entropy-seed bootstrap with block-protected Gamma references

27 October 2026. Conditional composition; ordinary entropy-seed discovery is a separate receiving obligation. This replaces per-reference concatenated-code transport, not the coherent learner or its comparator. Direct payload coding remains the simpler communication baseline. No hardware fault tolerance, novelty or practical advantage is claimed.

## 1. Exact imported interface and scope

Use the stationary independently reset source, known calibrated quaternion encoder family E_x=N Ad(V_x), and supplied four-anchor Choi-rank bound R of `../coherent_encoder_bures_bridge_20261027/COHERENT_ENCODER_UNRESTRICTED_RECOVERY.md`. Put s=physical output dimension, K=min(s,8R), d=8K, r=min(4R,d), D=nextpow2(dr), L=log(2D)+1. All data and seed-carrier outputs have the same unknown common support of dimension at most K. Trusted controlled-anchor phases remain an assumption. No unknown source inverse or controlled unknown source is available.

Import the received causal persistent-frame compiler, initialized for the entire finite horizon below. Its exact arbitrary-operator comb law is equivalent to one latent U shared by warm calibration, all data/carrier outputs and final payloads. After warm conditioning the posterior of U need not be Haar. The argument is pointwise in U; U is neither implemented nor exposed. No frame reset is allowed.

**Conditional startup interface.** A separately proved ordinary discovery/qualification protocol uses at most N_warm(beta) calls and supplies either abort or a frozen seed x0,D0 and rational probability box C. There is a pre-payload, input-independent latent good event G with Pr(G^c)<=beta, including all aborts, such that on G the privately and independently Pauli-framed seed channel is an EXACT conditional iid Pauli channel q in C. The entropy certificate is valid with PUBLIC fixed eta>0,h_*<1,R_c>0,xi>0 satisfying R_c+h_*+xi<=1. The eta-expanded box C+ has maximum entropy <=h_*. The same frame and seed decoder persist. Confidence conditional on acceptance alone is insufficient: success/abort mass must satisfy this interface. No claimed autonomous startup follows until the separate discovery proof is received.

The entropy code source `../no_inner_random_coding_20261027/CERTIFIED_PAULI_ENTROPY_RANDOM_CODING.md`, SHA256 ef3088105699d61f6353ceaee0bfd5bc204ef947300433cce666777505e3220c, is independently received in its neighboring `ROOT_ENTROPY_RANDOM_CODING_RECEIPT.md`. Its fixed-code complete-error expectation, uniform in q in C, permits arbitrary entangled inputs and a visible classical code descriptor. We import that result, not a per-realized-code guarantee.

The coherent learner imports the direct bridge's expected finite-arithmetic Bures bound m<=40DL/n_Gamma+8a_eig^2 and the coherent bridge's exact positive-loss inequality

    E ell(x_hat,D_hat) <=(1+gamma)ell_*+128m/gamma+4eta_opt/gamma,
    ell_*=min_(x,D CPTP) [1-F_e(D E_x)].                 (1)

The optimizer is feasible on every input state, with the received global quaternion net and full CPTP decoder SDPs; known synthesis is separately paid. Final D_hat is retained and used in this same frame, not relearned.

## 2. Public budgets and finite deterministic horizon

For M>=1, 0<epsilon,gamma<=1, set

    e=epsilon/(8M), beta<=epsilon/8, delta_ref=epsilon/4,
    n_Gamma=ceil[20480 DL/(gamma e)],
    a_eig^2<=gamma e/4096, eta_opt<=gamma e/8.           (2)

Then m<=gamma e/256 and (1) is at most (1+gamma)ell_*+e. This is an expected-risk bound, not a new high-probability tomography assertion.

Let Q=3n_Gamma reference qubits. Choose n_c by doubling from max(2,ceil(6/R_c)) until outward interval certification establishes BOTH

    8 exp(-2n_c eta^2) <= delta_ref/[8(Q+1)],
    2(n_c+1)^4 2^(-n_c xi) <= delta_ref/[8(Q+1)].       (3)

These are public deterministic computations, independent of the warm outcomes. k_c=floor(R_c n_c)>=3 and >=R_c n_c/2. Put B=ceil(Q/k_c). The capped exact uniform symplectic sampler uses

    J=ceil(log_4(4n_c/delta_ref))

trials per nonzero-vector stage, so beta_gen<=n_c 4^-J<=delta_ref/4. On sampler failure abort with a fixed replacement output. Conditional on successful generation the code is exactly uniform. Enumerate errors with empirical type in C+; use the first fixed representative for each syndrome, identity for absent syndromes, inverse encoder and ancilla trace. This is total CPTP, not postselection.

Writing F=8 exp(-2n_c eta^2)+2(n_c+1)^4 2^(-n_c xi), the received ensemble result gives

    2 beta_gen+2B F <=delta_ref.                         (4)

Indeed B<=Q+1 and each term in F is <=delta_ref/[8(Q+1)]. Code-generation failure is paid ONCE, not B times. The warm bad event is NOT included in (4).

The exact call cap is

    H=N_warm+n_Gamma+n_c ceil(3n_Gamma/k_c)+M
      <=N_warm+(1+6/R_c)n_Gamma+n_c+M.                  (5)

Early abort uses fewer calls; harmless dummy padding may realize a fixed cap. The frame is initialized for H and common support K. At fixed entropy/type margins n_c=O(log((n_Gamma+1)/epsilon)); the reference transport therefore costs O(n_Gamma+log(n_Gamma/epsilon)), not n_Gamma times a polylogarithmic per-reference factor.

## 3. Actual grouped data-first chronology

All calibration is completed before unknown final payload arrival. Sample and communicate one classical code descriptor after warmup; compile its encoder and syndrome decoder. Reuse this code for every reference block. The dictionary depends on C and the descriptor; keys used for private Pauli framing remain hidden.

Maintain a sender FIFO of unsent calibration references, in the fixed order I1,I2,A for each Gamma sample, and a receiver bank of reduced data outputs. Begin with an empty FIFO. While samples remain:

1. If r0<k_c references are queued, prepare g=min(number of remaining samples,ceil((k_c-r0)/3)) fresh Gamma preparations. For each, prepare control I in the known equal superposition and Bell A,L; apply the known controlled anchors and send ONLY its data through N once. Immediately enter the output into the next persistent-frame step and store its emitted K-register B_t. The three references stay at the sender, coherently entangled with B_t and its source environment, and join the FIFO.
2. If at least k_c references are queued, encode the first k_c into the [[n_c,k_c]] code and send its n_c carriers sequentially through the seed encoder, N, the next same-frame steps, D0 and independent private Pauli pairs. Decode at the receiver, place the recovered references into their labeled Gamma slots and discard syndrome ancillas. Never expose or reset frame memory.
3. Repeat. Once all data samples have been sent, transmit a final partially filled FIFO block with known |0> padding if necessary. Discard recovered padding. A triple may straddle two code blocks; its data output remains stored until all three references arrive.

There are exactly ceil(3n_Gamma/k_c) reference blocks. Before each full block the FIFO has at most k_c+2 references; after it, at most two remain. This avoids an otherwise hidden triple-alignment overhead. Every reference qubit is consumed in transmission through N; none is transported through a supplied bypass. Sender storage includes the untransmitted references and current codeword; receiver storage includes all data and recovered references. All waits and local memories are trusted paid resources.

## 4. Complete-bank comparison and visible code metadata

Work first in the EXACT common-U virtual experiment and fix U and the entire warm history. On G the seed is a fixed Pauli channel q in C, iid across carriers conditional on that history, independent of codeword input and error-correcting code randomness. Data calls and carrier calls can be entangled; the common-frame law is valid on arbitrary operators and the code comparison is a complete norm bound. Merely observing small single-use error would not establish this iid assertion.

For each successfully sampled fixed descriptor, compare its actual reference channels with identities on the same Q reference wires, retaining the descriptor and known classical compilation/dictionary metadata in both experiments. Average the fixed-code diamond bounds, and hybrid/union-bound the B blocks. Shared-code quality is correlated, but no independent-code assumption is used. The resulting cq complete discrepancy, including generation failure, is bounded by (4). This remains valid with all acquired data registers and untouched external systems as references, including when future controlled operations depend on descriptor metadata.

This identity transport is an ANALYSIS comparison in the whole causal comb. Do not physically delete carrier frame steps or start a fresh frame. The common-U representation already links all slots. In the ideal comparison the stored bank is exactly Gamma_U^tensor n_Gamma conditional on U and warm history, independent of the code descriptor (its classical metadata may depend on warm C). The specified Gamma estimator and optimizer act as their received algorithms; exposing metadata does not license replacing them with an arbitrary estimator lacking (1).

Define an ideal comparison that uses the same warm experiment but ignores abort/bad-seed outcomes and always supplies this exact Gamma bank and the specified learner. On histories where metadata is undefined choose a fixed dummy descriptor in both comparison bookkeeping. Its future learner bound is uniform in U and warm history. Bad histories cost at most 2Pr(G^c), not a success-conditioned normalization. Thus the complete-bank transfer, including subsequent learning and deployment, costs

    2 beta+delta_ref.                                  (6)

Only this ONE warm debit occurs. Actual decoded references may have correlated errors within and between blocks and the actual bank may be full rank. No iid noisy-Gamma model or low-rank theorem is applied to the actual bank. Run the same globally CPTP learner on both banks; contractivity transfers (6). Code metadata may be retained during this comparison, but private Pauli keys, code syndrome environments and frame quantum memory are not exported as additional tested outputs.

## 5. One-use-family optimization guarantee

Deploy each final payload once through its independent private Pauli frame, learned x_hat, N, the next continuing frame step, learned D_hat and unframe. No final payload code is used. Define the exact omniscient fixed-family-encoder comparator, allowing arbitrary collective physical decoders but not cross-use payload encoding or extra payload-dependent calls,

    delta^*_(family,M)=2[1-(1-ell_*)^M].

The received collective-decoder tensorization and private-frame expected-regret transfer yield for the ideal Gamma learner

    ||Lambda_ideal-id||diamond <=(1+gamma)delta^*_(family,M)+2M e.

This statement concerns final logical outputs with calibration records discarded; the code descriptor may be used internally as above. An exposed-learning-record benchmark would require its own ideal record specification. Add (6) and a uniform finite whole-process discrepancy nu<=epsilon/4. Equations (2)-(4) give

    ||Lambda_actual-id||diamond
      <= min{2,(1+gamma)delta^*_(family,M)+epsilon},      (7)

because 2Me+2beta+delta_ref+nu<=epsilon. There is no second recovery-optimization multiplicative factor. For M=1 this also supplies the coherent bridge's unframed Bell-risk family optimization interpretation; it does not establish generic unframed diamond-optimality.

## 6. Gate, arithmetic, storage and fault ledger

Type/syndrome enumeration costs 2^{O(n_c)} classical time/storage, polynomial in n_Gamma/epsilon ONLY at fixed eta,xi,R_c, with potentially enormous exponent. No useful practical decoder claim follows. Dense known stabilizer encoding and syndrome extraction use polynomial-in-n_c gates (generic O(n_c^2) Clifford circuit size with polynomial synthesis); total carrier controls scale with B and their actual supplied costs. Exact capped code sampling uses polynomial random bits/linear algebra. Rational membership and certified entropy/log arithmetic follow the received entropy note. The Gamma learner retains its polynomial purification, finite Clifford estimation, feasible SDPs and global quaternion net; source calls do not multiply by the classical net size.

The causal frame costs polynomial gates/arithmeticproducer-workspace/workspace in H,K,log s and log precision, with persistent quantum memory allowed to grow with H. The Gamma bank needs n_Gamma(log_2 K+3) reduced qubits plus learner workspace. Sender reference/codeword storage is O(k_c+n_c), receiver needs O(n_c) transient carrier/decoder workspace in addition to its bank. Warm banks and frame memory are charged separately. Each actual carrier and final payload uses two private random bits, totaling 2(B n_c+M) beyond warm randomness. Code descriptors/dictionaries may be huge; their construction, memory and communication are not free. Storage duration includes classical code search and optimization latency.

Specify a deterministic operation cap including source-independent compilation and all storage intervals. Allocate nu across all warm controls, frame steps, coherent data preparation (especially relative phases), seed encoders/decoders, code gates, syndrome measurements, memories, finite random generation not already paid in beta_gen, Gamma learner quantum circuits, and final deployment. Arithmetic allowances in (2) are not charged twice. Any arbitrary local fault contributes its actual worst-case complete interactive discrepancy; an unknown correlated local error cannot be folded into the iid Pauli q and suppressed by this theorem. Unbounded drift or unknown-memory faults block implementation claims.

## 7. Meaning and evidence

This is a conditional constant-rate reference-transport composition, not evidence that every unknown positive-capacity source can be autonomously discovered. The sufficient entropy promise, trusted controls and separately received startup interface remain substantive. For communication alone the already received direct entropy-code payload protocol avoids the Gamma learner entirely and is the simpler baseline. This branch matters when learning a near-optimal fixed one-use family encoder/decoder is itself the objective.

An equally informed conventional learner with the same coherent controls, persistent quantum memory, source calls and code resources can use the same construction. The gain here is removal of the earlier per-reference transport polylogarithmic SOURCE factor; it is not a separation from conventional learning, a generic quantum-capacity theorem or a practical wall-clock advantage.

`block_reference_checks.py/.json` verifies exact budgets, FIFO chronology, ceiling/padding inequalities, and finite block choices. It does not execute a high-dimensional frame, huge type dictionary or laboratory circuit. This composition requires independent receiving; imported entropy coding is already received, ordinary entropy startup remains separately conditional.
