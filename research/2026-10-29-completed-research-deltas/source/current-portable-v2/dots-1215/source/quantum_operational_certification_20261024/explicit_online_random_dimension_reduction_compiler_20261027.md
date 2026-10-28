# Polynomial online random dimension reduction: a phase-safe explicit compiler

27 October 2026. New theorem candidate; independent receiving required. The causal-existence receipt remains unchanged. This note gives a constructive sequential dilation with a fully paid normalization/which-path erasure circuit. It imports established efficient Schur/CG implementations; it claims no first CG transform or first compressed Haar oracle.

## Theorem and resources

Fix finite H and `1<=k<=s`. There is a known causal receiver circuit with H steps. Step n accepts one s-dimensional register, emits one k-dimensional register immediately, and retains quantum memory. For every fixed unknown isometry W:C^k->C^s and EVERY operator X on `(C^k)^tensor H`, the exact-reference channel obeys

`T_H(Ad_(W^tensor H) X)=integral Ad_(U^tensor H)(X) dU`.       (1)

The circuit is a CPTP causal channel on ALL input operators, including those not on a common k-support; its forbidden-sector completion is order-specific. It has a finite approximation with total interactive error nu, polynomial known gate/classical arithmetic count in `H,k,log s,log(1/nu)`, and polynomially many memory/workspace qubits in these parameters. All inverse circuits are KNOWN RECEIVER operations, not the unknown source or its environment. There is no pre-source coherent encoder reference.

A conservative useful description of its persistent memory on the valid branch is

`direct_sum_(lambda partitions n, rows(lambda)<=k) Q_lambda^s tensor bar Q_lambda^k`.       (2)

The bar denotes the complex-conjugate representation in the chosen known basis, not an antiunitary operation on an unknown state. Logical memory size can be bounded by `O(n(log s+log k))` qubits before allowing the chosen Schur encoding/workspace. The compiled representations may use more, still polynomially many, encoding qubits. A first invalid branch switches to a finite isometric fallback and retains enough memory to preserve earlier outputs. The horizon and memory lifetime are actual resources.

## 1. Phase-compatible ordinary CG convention

Use Schur transforms whose symmetric-group multiplicity space is the SAME fixed Young–Yamanouchi representation for each ambient dimension. Let

`C_(lambda,mu)^d : Q_mu^d -> Q_lambda^d tensor C^d`

be the ordinary CG EMBEDDING for `mu=lambda+one box`; its adjoint is the corresponding coupled transform branch. Write its coefficients as `C[a,i,b]`, with a in Q_lambda, i in the defining representation, b in Q_mu. Define the FORWARD coisometry `G=C*`, so `G[b;a,i]=conjugate(C[a,i,b])`. The full forward ordinary CG transform is unitary on the direct sum of its branches. All labels and paths are retained coherently until they are uncomputed as described below.

This convention can be enforced from a full Schur transform, avoiding an unproved high-dimensional per-step circuit assumption. On an input Q_lambda^s, append a known canonical multiplicity-path ket p_lambda, apply inverse full Schur_(n-1)^s to create n-1 RECEIVER-LOCAL tensor registers, append the newly arrived physical s-register, then apply full Schur_n^s. Prefix branching leaves the old canonical path unchanged and outputs its predecessor lambda plus new shape mu and Q_mu^s. Reversibly uncompute the known p_lambda, retaining the predecessor label needed below. This implements exactly the desired ordinary CG_s without touching any previously emitted output.

The required full Schur and inverse circuits use `poly(n,log s,log(1/delta))` gates in the conventional bases, by [Burchardt et al., *High-dimensional quantum Schur transforms*, Theorem 1 and Sections 8–8.1](https://arxiv.org/html/2509.22640); the same contract is stated as Lowe–Tan Theorem 5.1. Canonical-path construction and GT/shape checks are finite reversible classical computations. Alternatively, [Grinko–Yoshida, Appendix D, equations (115)–(124)](https://arxiv.org/html/2509.26623v2) gives a DIRECT streaming compressed-GT/alphabet update on receipt of a new symbol. Either route supplies the physical CG compiler, rather than inferring it from mere consistency on promised inputs.

For the canonical phase-compatible implementation, choose the SAME Grinko–Yoshida ordinary-CG family at d=s and d=k. On the coordinate alphabet [k], its sparse-alphabet/core update is literally the same; this fixes the cross-dimension edge phases rather than importing unrelated black-box CG conventions. The full-Schur sandwich is an alternative only with the same verified Young-path branching convention.

For the k-dimensional ordinary CG used below, the standard polynomial-in-k construction suffices. Complex conjugating its KNOWN gate sequence implements the conjugated unitary linearly; no unknown-state complex conjugation is attempted.

## 2. The required co-CG isometry

For fixed valid mu, define on each valid predecessor lambda=mu−one box

`F_(lambda,mu): bar Q_lambda^k -> C^k tensor bar Q_mu^k`,

`F_(lambda,mu)[i,b;a] = sqrt(d_lambda/d_mu) conjugate(G_(lambda,mu)^k[b;a,i])
                      = sqrt(d_lambda/d_mu) C_(lambda,mu)^k[a,i,b]`,              (3)

where d_lambda=dim Q_lambda^k. Define the JOINT map with predecessor label as its INPUT direct sum,

`F_mu : direct_sum_(lambda predecessor mu) bar Q_lambda^k -> C^k tensor bar Q_mu^k`.        (4)

There is NO surviving copy of lambda at the output of F_mu.

Schur's lemma gives `Tr_(C^k)(C C*)=(d_mu/d_lambda) I_(Q_lambda)`, since the partial trace intertwines the irreducible Q_lambda representation and has trace d_mu. Thus every F_(lambda,mu) is an isometry. Its range carries the conjugate irrep bar Q_lambda inside `C^k tensor bar Q_mu`. Distinct predecessors give inequivalent U(k) irreps, so their ranges are orthogonal. Consequently

`F_mu* F_mu = I` on the ENTIRE predecessor direct sum.                                    (5)

This is the precise coherent erasure of the old shape label. Merely applying controlled F_(lambda,mu) while retaining a classical/quantum which-lambda label would destroy later multiplicity-path interference and is NOT sufficient.

## 3. A known block circuit that erases the predecessor label

A direct mixed/dual-CG compiler can implement (4) after matching dual-basis and relative-phase conventions. [Nguyen, Section 4.4 and Corollary 4.11](https://arxiv.org/html/2310.01613) supplies polynomial-k dual-CG circuits with coherently computed reduced-Wigner coefficients and uncomputed workspace. To avoid assuming a reciprocity-phase match, this proof instead builds (3) literally from the SAME ordinary CG coefficients used above.

Fix target mu coherently; it also controls the spectator physical Q_mu^s register. Let `m=2^ceil(log2 k)` (m=1 when k=1). Each mu has at most k valid predecessors. A known reversible relabelling maps the ordinary CG predecessor label lambda to a removable-box index j in an m-dimensional register, conditional on the output shape. It does not copy lambda.

Construct a known unitary U_block on padded registers with these operations:

1. Initially the co-CG input is `|mu>|lambda>|bar a>`, with all new work/flag registers zero. Compute a known attenuation r_(lambda,mu) specified in Section 4, rotate a flag so its designated zero amplitude is r, and uncompute ALL arithmetic workspace while lambda is still present.
2. Prepare a normalized maximally entangled k-pair `k^(-1/2) sum_i |i>_out |bar i>_aux`.
3. Apply the complex-conjugate ordinary k-CG to `|lambda>|bar a>|bar i>_aux`. Its coupled output consists of shape mu', irrep bar Q_mu', and the predecessor label. Replace the latter reversibly by its removable-box index j; no extra lambda record is kept.
4. XOR mu' with target mu. Apply the m-dimensional Hadamard transform to j. Designate success as: attenuation flag zero, XOR-shape register zero, and Hadamard-transformed j zero. Workspaces must also be returned to zero. The k-dimensional output half of the entangled pair is NOT projected.

Any temporary reconstructed copy of lambda is uncomputed BEFORE the predecessor projection; otherwise which-path information remains and (6) is false. These are coherent unitary operations. The stated success projection defines a matrix BLOCK only; the procedure will NOT postselect/retry the unknown input. Section 4 removes its failure amplitude coherently with a deterministic gate cap.

Before attenuation, the success block on predecessor lambda is exactly

`alpha_(lambda,mu) F_(lambda,mu)`,

`alpha_(lambda,mu)=sqrt(d_mu/(k m d_lambda))`.                (6)

The factor k comes from the Bell pair, and m pays the actual which-predecessor erasure. Omitting m would leave a hidden path record. All these amplitudes have the phase of the literal conjugated CG tensor, so (6) introduces no untracked predecessor-dependent phase.

## 4. Uniform attenuation and EXACT oblivious amplification

For a legal box addition in row j, the Weyl dimension ratio obeys

`d_mu/d_lambda >= 1/j >=1/k`.                               (7)

Indeed, the factors involving earlier rows are

`product_(i<j) [lambda_i-lambda_j+j-i-1]/[lambda_i-lambda_j+j-i]`.

Legality gives lambda_i−lambda_j>=1 there, hence each factor is at least `(j-i)/(j-i+1)` and their product is at least 1/j. Factors involving later rows are at least one. It follows that

`alpha_(lambda,mu)>=1/(k sqrt(m))>=1/(sqrt(2) k^(3/2))`.       (8)

All dimensions/ratios are known positive integers or rational products of O(k^2) factors; their bit lengths are polynomial in k and log(H+k).

Choose the EXACT integer

`J=8 k ceil(sqrt(k))`, `theta=pi/(4J+2)`, `c=sin(theta)`.

Then `c<=pi/(32 k^(3/2))`, while J=O(k^(3/2)). Set

`r_(lambda,mu)=c/alpha_(lambda,mu)`.

This is bounded above by `pi sqrt(2)/32<1/sqrt(2)`, so the known rotation is well away from the r=1 endpoint. It is efficiently computable to any prescribed finite accuracy. With exact-reference rotations, the full success block is

`Pi_out U_block Pi_in = c F`,                               (9)

where F is the direct sum of F_mu over target mu, including identity on the spectator physical irrep, and Pi_in projects onto valid input predecessor/GT labels with fresh flags zero. Pi_out checks the prescribed success flags. Both reflections are known reversible shape/GT/zero tests of polynomial size. No source-support oracle is involved: these are basis labels of known representation registers.

Let `S_in=I-2Pi_in`, `S_out=I-2Pi_out`, and

`Q= - U_block S_in U_block* S_out`.

For any input vector v in Pi_in, write

`U_block v = sin(theta) Fv + cos(theta) Gv`.

Equation (9) and unitarity imply that G is an isometry into the failure space and its range is orthogonal to F. All input directions therefore carry the SAME two-dimensional rotation, even when entangled with the physical-irrep spectator or an external reference. Direct multiplication gives

`Q^j U_block v = sin((2j+1)theta) Fv + cos((2j+1)theta) Gv`.

Because `(2J+1)theta=pi/2`,

`Q^J U_block Pi_in = F`.                                   (10)

This is an exact FULL-ISOMETRY statement, not only a high acceptance probability or an averaged accepted branch. It uses 2J+1 calls to U_block or its inverse, plus known reflections. No trial is thrown away; there is no retry or conditional output normalization. The construction is the usual known-isometry amplitude-amplification rotation, here with a directly chosen exact angle, so no phase-synthesis theorem beyond known rotations is needed.

Finite approximations of the known Schur/CG circuits, arithmetic rotations, comparisons and uniform-state preparation are allocated across the deterministic O(k^(3/2)) call cap. A hybrid operator-norm bound on the whole isometry gives a uniform reference-preserving diamond bound (at most twice the isometry operator error). Choose component accuracies accordingly. There is no square-root failure-probability ambiguity because the ideal amplified isometry is exactly F. Private flags/workspace can then be discarded; actual finite circuits remain CPTP.

## 5. One sequential step and its full-input completion

Initialize with the empty irrep, dimensions one. At step n on the VALID flag:

1. Apply the phase-compatible physical CG_s to memory Q_lambda^s and the arriving s-register, leaving the dual Q_lambda^k memory untouched.
2. This produces a coherent sum of target shapes mu, physical irrep Q_mu^s and predecessor lambda. If rows(mu)<=k, apply the amplified F_mu to `(lambda,bar Q_lambda^k)`. Emit its C^k output and retain `(mu,Q_mu^s,bar Q_mu^k)`.
3. If mu is invalid, switch coherently to a distinct FALLEN memory flag. Preserve all remaining physical/dual registers isometrically, emit half of a fresh k-dimensional maximally entangled pair, and retain its other half. All later FALLEN steps store the arriving physical register and emit another independent maximally mixed k-output through a retained purification.

The physical CG_s is unitary and each valid F_mu is an isometry. Different target mu and VALID/FALLEN flags are orthogonal in memory. Distinct old lambda at the same valid mu have orthogonal F ranges by (5). Thus this is an isometry on the entire reachable memory/input space. Its polynomial completion on unused/invalid encodings is the one supplied by the actual padded known gate circuits, not an arbitrarily specified dense isometry. If explicit invalid-encoding semantics are needed, a reversible representation-validity flag routes them to the same store-and-EPR FALLEN path; the known validity checks and controlled padding are charged. No physical source input is rejected. On a promised common k-support, an invalid Young diagram never occurs; the fallback is needed to make the receiver globally physical and causal, not to define a conditional-success theorem.

The first step simply stores the physical input and emits half of a maximally entangled k-pair while retaining the other half. It need not know W or the input state.

## 6. Telescoping identity and common frame

Expand the n sequential isometries along a multiplicity path

`empty=lambda_0 ->lambda_1 ->...->lambda_n=mu`.

The physical CG tensors multiply to the physical Schur transform. The conjugated FORWARD k-CG coefficients, with input/output legs bent as in (3), multiply to the inverse k-Schur transform, with the SAME path because old labels were erased coherently, not measured. The dimension factors telescope:

`product_(j=1)^n sqrt(d_(lambda_(j-1))/d_(lambda_j))=1/sqrt(d_mu)`.

Consequently the valid-branch final isometry, in physical Schur coordinates, is

`|mu,p,a>_physical -> (1/sqrt(d_mu)) sum_b
     (Schur_k)^dagger |mu,p,b>_emitted_outputs tensor |mu,a,bar b>_memory`,          (11)

with the conjugation/orientation chosen consistently with (3). Equation (11) states the standard Schur-replacement dilation: tracing memory preserves the path/multiplicity operator, traces the physical irrep, and replaces the k-irrep by its maximally mixed state. It therefore equals the standard exact reduction on the allowed sector, including off-diagonal path operators.

An arbitrary W^tensor n input is supported there, and Schur naturality gives (1). The full sequential construction is causal by construction, including references and arbitrary unpromised physical inputs. Equality on the whole supported operator space then gives equality of the restricted causal combs, so all ordinary adaptive preparations, training measurements and later decoder choices can be linked into the process. The same latent U is a mathematical decomposition for the whole horizon; it is not an exposed variable of the actual circuit.

## 7. Complexity and finite-error contract

The physical CG_s may be compiled with two known full-Schur circuits of size `poly(n,log s,log(1/delta))` plus polynomial reversible bookkeeping, or the direct streaming Appendix-D circuit. The co-CG uses O(k^(3/2)) ordinary k-CG calls/reflections and polynomial-k/log-H arithmetic. Thus EACH step has polynomial cost in n,k,log s and precision, and summing n<=H preserves polynomial total cost. The fallback stores at most H physical registers and H k-dimensional halves plus existing valid memory, also polynomially many qubits.

For total interactive error nu, request per-step channel discrepancies summing to at most nu (e.g. nu/H), and subdivide within every step's deterministic known gate cap. Telescoping in an arbitrary external causal tester proves total error <=nu; no parallel-channel norm is silently used in place of this interactive bound. Precision increases logarithmically in H/nu and in the known call cap. Input physical memory, output register size, all ancillas, coherent arithmetic, flags, finite-basis conventions, and finite horizon are charged.

The actual isometry matrices depend only on s,k,H, not W or the unknown source. Persistent frame memory cannot be measured/reset without changing the process. It can be retained through future payloads, which is a different resource interface from the old simultaneous-bank reduction. It is not a reusable classical alignment and not a noiseless logical/control bypass around the source.

## 8. Existing results, checks and boundary

[Grinko–Yoshida](https://arxiv.org/html/2509.26623v2) already constructs compressed Haar oracles from paired CG transforms, including efficient high-dimensional updates. The k=s special case is therefore established background, not a new random-oracle claim. This note uses a rectangular common-support dimension-reduction identity, a valid forbidden-sector causal completion, and a phase-safe polynomial co-CG compiler to bind that mechanism to ordinary unknown-source recovery.

`explicit_online_random_dimension_reduction_compiler_check.py/.json` checks phase-correct complex co-CG tensors, the full Grover-exact block-dilation isometry including input superpositions, and the sequential U(2) channel on every matrix unit through four steps. The separate `co_cg_dimension_ratio_fallback_check.py/.json` verifies Weyl-ratio bounds in 18,176 exact cases. The independent receiving check additionally constructs the complete Bell/CG/predecessor-erasure preparatory unitary; the author block-dilation check alone does not establish that gate layout. It is not a gate-level execution or a fault-tolerance claim. General correctness is the representation/isometry argument above. The received causal-existence proof independently checks a full-input extension; this circuit may choose a different harmless forbidden-sector completion.

The separate `streaming_bures_recovery_persistent_frame_20261027.md` gives the resulting calibrated streaming recovery theorem. Global ordinary encoder discovery still lacks the requested R^2 active-acquisition proof; its received scalar-action route pays R^4 and an exponential decoder-net classical search. Efficient online alignment alone must not be advertised as closing that separate statistical optimization gap.
