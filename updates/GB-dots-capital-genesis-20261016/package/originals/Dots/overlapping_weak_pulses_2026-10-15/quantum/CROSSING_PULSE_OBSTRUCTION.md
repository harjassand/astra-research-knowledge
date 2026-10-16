# Crossing finite pulses with a shared bath: failure of conditional character bounds

Date: 2026-10-15. Status: exact analytic and rational counterexample to the proposed chronological conditional-character interface. This is not a counterexample to every possible local-stochastic bound or to the completed-memory theorem under its existing atomic hypotheses.

## 1. Verdict

Uniform small integrated non-bath interaction norm for each pulse does NOT imply the needed conditional bound on each pulse's completion character when temporally overlapping, memory-disjoint pulses share a noncommuting persistent bath. Independent private stabilizer frames held across the respective pulses do not repair this.

Two crossing echo pulses suffice. Each isolated pulse is exactly identity. Both act nontrivially near their actual completion, so the example cannot be dismissed merely by shortening an artificial idle tail. Each has arbitrarily small total interaction action. Yet after observing the first pulse's rare nontrivial character, the second pulse's nontrivial character has probability approaching one as both actions approach zero.

Consequently the atomic post-error interface in

    ../../finite_duration_syndrome_addendum_2026-10-15/finite_duration/COMPOSED_POST_ERROR_INTERFACE.md

cannot be replaced by that integrated-norm condition alone. The original proof's causal conditional-effect premise and its sequential iid-mark coupling would be missing.

## 2. Three-qubit construction and physical frames

Use disjoint memory qubits A and C, and one shared bath qubit B. Stabilizers are Z_A and Z_C; append any untouched logical subsystem if desired. Initially encode A,C in |00>; the bath state can be arbitrary, including correlations with the untouched logical/reference system. Each one-qubit memory patch has no local logical operator and its Z check is detection-complete.

Define Hermitian involutions

    H_1=X_A tensor I_C tensor X_B,
    H_2=I_A tensor X_C tensor Z_B.

They anticommute. Let R_1=exp(-i a H_1), R_2=exp(-i b H_2).

Pulse A spans times 0 through 2: it applies R_1 early and R_1^dagger near completion. Pulse C spans times 1 through 3: it applies R_2 early and R_2^dagger near completion. The order of the four interaction lobes is

    R_1, R_2, R_1^dagger, R_2^dagger.

The lobes may be finite positive-width rectangular Hamiltonian intervals with empty gaps; their supports need not overlap at the instant of a lobe. The pulse reservation intervals cross, have equal duration, and both have a genuine last nonzero lobe. Integrated non-bath norms are exactly 2|a| and 2|b|. With the other pulse absent, either echo is identity.

Independently sample private frames F_A in {I,Z_A} and F_C in {I,Z_C}. Apply each at its pulse's start and undo it at that pulse's end. No frame information is supplied to the bath Hamiltonians or to another controller. The actual laboratory Hamiltonian lobes are fixed, not selected by the frame.

Let r,t be their conjugation signs. Direct rearrangement, using the disjoint memory supports, gives the actual full framed unitary

    U(r,t)=R_2(t)^dagger R_1(r)^dagger R_2(t) R_1(r),
    R_1(r)=exp(-i r a H_1), R_2(t)=exp(-i t b H_2).

The checker verifies equality with the raw physical start/undo ordering; this is not an assumed independent composition of atomic twirls. Average the two independent inaccessible frame registers only as stipulated by the physical protocol.

## 3. Exact Fourier character operators

Write c_b=cos b, s_b=sin b, C_a=cos(2a), S_a=sin(2a). The complete four-character Kraus family is

    K_00=(c_b^2+s_b^2 C_a) I,
    K_01=i c_b s_b(1-C_a) H_2,
    K_10=-i s_b^2 S_a H_1,
    K_11=c_b s_b S_a H_1 H_2.                 (1)

Here the first bit labels the A frame character and the second the C frame character. Each K^dagger K is a scalar multiple of identity, so all the following probabilities are uniform over bath inputs, not reduced-system approximations:

    p_10=s_b^4 S_a^2,
    p_11=c_b^2 s_b^2 S_a^2,
    p_01=c_b^2 s_b^2(1-C_a)^2,
    p_00=(c_b^2+s_b^2 C_a)^2.

They sum to one. For nonzero small a,b,

    Pr(C_bad | A_bad)=p_11/(p_10+p_11)=cos^2 b.             (2)

This approaches one, whereas the proposed per-pulse action bound (2b)^2 approaches zero. No universal constant multiplying that squared small action repairs this conditional claim.

Changing the order in which complete character labels are revealed does not help: the reverse conditional is

    Pr(A_bad | C_bad)=cos^2 a.

A's physical completion precedes C's, so (2) is exactly the problematic chronological direction.

## 4. Causal records, rather than only a final Fourier calculation

At A's completion, before the last C lobe, the toggling-frame propagator is

    W(r,t)=R_1(r)^dagger R_2(t) R_1(r)
          =c_b I-i t s_b C_a H_2+r t s_b S_a H_1 H_2.

Its nontrivial A Fourier component is t s_b S_a H_1H_2. Notice that it already contains X_C: integrating out one overlapping bath-coupled pulse does not yield a branch supported solely on its own memory qubit A. The shared bath has transmitted interference to the other open pulse.

On the encoded input |00>_AC, the character labels equal the actual Z_A/Z_C error syndromes. A genuine Z_A measurement at A completion and Z_C measurement at C completion give exactly the probabilities in (1), for every bath input. The first measurement is causal and commutes with all remaining C operations. On these encoded inputs, resolving that syndrome refines the dephasing already supplied by the private A frame; it does not require disclosing either frame or conditioning on a future outcome.

The exact checker verifies the two sequential measurement effects directly, without relying only on final Fourier labeling. This avoids an ambiguity in choosing phases for a Kraus family while another private frame is still open. The later bad label is the final C error syndrome relative to the state at C's start, not a newly sampled error label for its final lobe alone.

The last lobe by itself still has a small effect on every input. What fails is treating an overlapping multi-lobe pulse as a fresh local instrument at its completion, independently of the correlations accumulated during the pulse.

## 5. Exact rational certificate

Choose a=b in (0,pi/2) with cos a=99/101 and sin a=20/101. The exact verifier is

    ../checks/exact/check_crossing_echo.py

It checks physical frame placement, joint unitarity, all four Fourier Kraus matrices, their completeness, their scalar joint effects, and the real chronological syndrome-measurement probabilities using rational SymPy arithmetic.

It gives

    Pr(C_bad|A_bad)=9801/10201.

Since a<=tan a=20/99, the integrated action obeys

    2a<=40/99,       (2a)^2<=1600/9801.

The exact conditional gap against even this conservative squared-action upper bound is

    9801/10201-1600/9801=79738001/99980001>0.

Both interaction pulses can be made arbitrarily weak by taking smaller a,b; the obstruction is not specific to this rational angle.

## 6. What this counterexample does and does not rule out

It rules out deriving the uniform chronological conditional-character effect bound used for same-parent sequential Bernoulli coupling from integrated action alone under the stated overlap/shared-bath assumptions. It also rules out silently replacing each isolated echo by its identity channel inside the joint overlapping process.

It does not prove that a dominating iid field is impossible by some different argument. In this two-pulse example, the joint bad probability is order a^2 b^2 and is bounded by the product of the conservative action-square bounds. Thus a fault-path or joint-subset probability approach might remain viable. Such an approach would need a new probability/interface proof; the existing sequential conditional-bound proof cannot simply be cited.

There is a useful weaker marginal fact. Fix all other private frames and compare the full propagator with the i-th pulse's non-bath interaction removed, leaving the other dynamics in chronological order. Duhamel's bound is at most the i-th integrated interaction action, provided its frame commutes with other memory interactions and all removed-control dependence is accounted for. The comparison propagator is independent of that frame. Fourier Parseval then bounds the unconditioned nontrivial-i character effect by the squared action. Conditioning on outcomes of overlapping pulses can destroy this bound, as above. Marginal bounds alone do not supply the finite-dependence or domination premise used by the current coarse-tail theorem.

No conclusion about failure of the actual quantum memory follows from this algebraic obstruction. It identifies a proof/physical-interface boundary, not a device impossibility.

## 7. Sufficient extensions that genuinely remove atomicity

Two stronger hypotheses do recover an ordinary finite-duration post-error primitive.

### A. No temporal overlap with other noncommuting bath-coupled operations

During a pulse, permit arbitrary bath-only Hamiltonian H_B(t), and a patch-bath interaction h_i(t) with integral norm alpha_i. If no other memory-bath operation interleaves with this pulse, interaction-picture Duhamel gives

    ||U_i-I tensor V_B||<=alpha_i.

Fresh private memory frames conjugate this whole local joint unitary exactly, since bath-only evolution is frame-independent. Its completion therefore admits the original character-effect bound alpha_i^2 for every preceding state. Its actual finite duration must be included in the reservation/terminal/conflict bookkeeping.

The same conclusion holds if every intervening operation commutes with the clean pulse's relevant joint generators/propagators, allowing justified serialization. Disjoint memory support alone does not establish this commutation.

### B. Commuting interactions in a common bath interaction picture

Suppose all overlapping pulse interactions in the interaction picture of the common bath-only evolution satisfy

    [h_i(t),h_j(s)]=0 for distinct pulses i,j and all relevant t,s,

including their framed versions, and all other intervening bath-coupled operations satisfy the needed commutations. Then the time-ordered propagator factors into pulse propagators. They can be placed at their physical completions in any allowed order, with the bath-picture conversions kept exact. Each pulse remains patch-bath local and has distance at most alpha_i from bath-only evolution. The atomic character proof then applies to this derived finite-duration channel.

This covers, for example, suitably commuting shared classical bath variables, or genuinely separate bath factors with nonmixing bath evolution. It does not cover the anticommuting X_B/Z_B construction above.

Alternatively, declare every overlap of noncommuting bath-sharing resources a conflict. This is compatible with the existing geometric proof only when that enlarged conflict graph has bounded degree independent of L. One globally shared bath can make the degree grow with the entire system, invalidating the fixed local conflict budget. An unrestricted bath-global serialization rule cannot be advertised as a bounded-resource local solution.

## 8. Handoff

The finalized finite-duration composition theorem should retain its atomic post-error premise unless a physical implementation supplies a sufficient nonoverlap/commutation/factorization condition or a new joint fault-path theorem replaces sequential mark domination. No canonical theorem file was modified by this investigation.
