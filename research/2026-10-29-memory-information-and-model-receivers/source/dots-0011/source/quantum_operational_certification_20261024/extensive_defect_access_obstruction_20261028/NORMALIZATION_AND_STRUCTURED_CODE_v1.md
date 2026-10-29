# The extensive-defect access cost: a normalization obstruction, not a general decoding lower bound

28 October 2026. New algebraic analysis; pending independent review. This separates two obstacles in extending the received fixed-defect Schur decoder. No oracle assumption is promoted to a lower bound on all structured decoders.

## 1. Exact lower bound for a code-oblivious row interface

Let F_1,...,F_N:C^d→C^D be a normalized-Hilbert–Schmidt orthonormal isotropic error frame:

    Tr(F_i†F_j)/d=delta_ij,
    sum_i F_i F_i†=(dN/D) I_D.

Define the unencoded row B|i,x>=F_i|x>. Then

    B B†=(dN/D)I_D,  ||B||=sqrt(dN/D).                  (1)

Every unitary projected-block realization B/alpha must therefore have alpha>=sqrt(dN/D). This is exact, independent of frame redundancy or which basis realizes the same projector. A redundant Parseval realization has the same BB† and hence cannot lower this norm.

After restricting to an actual rank-K code C, the desired row is W=B(I_N tensor C). Its squared Frobenius norm is KN, giving only

    ||W||>=sqrt(KN/D).                                 (2)

The code-oblivious normalization is larger than this trace lower bound by sqrt(d/K). At an approximately orthogonal packing W†W≈I, W itself has norm near one even if sqrt(dN/D) is exponential. Thus feeding an efficiently encoded full reference row into a code and then applying a generic normalized inverse/polar routine can retain an exponential scale that is not intrinsic to the encoded matrix.

This rules out the claim “remove explicit frame enumeration, therefore efficient recovery follows.” It does **not** rule out code-specific compilation, a different decoder, or efficient use of known structure. An oracle-query lower bound would additionally have to specify the exact supplied unitary, inverse access, projectors and any known description; equation (1) is not such a universal lower bound.

## 2. Explicit example where code-aware compilation removes the entire obstruction

Let d=D=NK, with input/output factorization C^N_flag tensor C^K_payload, and

    F_i=sqrt(N)|i><i| tensor I_K,
    C|x>=|+_N> tensor |x>,
    |+_N>=N^(−1/2)sum_i|i>.

These F_i are normalized-HS orthonormal and isotropic. The full row has norm sqrt(N), saturating (1). But

    F_i C|x>=|i> tensor |x>,

so the encoded row W is exactly a wire relabeling from error-label plus payload to flag plus payload. It has normalization one, for every N, and its polar inverse is a register permutation. For N a power of two this needs only O(log N+log K) wiring/basic operations, not sqrt(N) calls. Discarding the flag gives exact recovery for every physical positive error weight compatible with this frame (the output flag carries that weight, and the payload is unchanged).

The corresponding normalized channel with Kraus F_i/sqrt(N) is simply flag dephasing. This is a familiar noiseless-subsystem mechanism, not a new quantum code. It decisively demonstrates that exponentially large full-reference row norm can be an interface artifact even for a physically realizable channel and an exact code. A generic normalization lower bound alone cannot justify giving up on structured codes.

## 3. Why the naive Young-prefix noiseless subsystem does not transfer

Before orbit completion, H-invariant branching matrix units act as identity on a shared prefix V_alpha and arbitrarily on suffix multiplicities. Encoding into that prefix is a genuine ordinary noiseless-subsystem mechanism for the **unconjugated** H-commutant error algebra.

The universal reference requires conjugating these errors by all relevant permutations. A fixed prefix is not invariant under arbitrary conjugates of H. In particular, whenever the selected error span contains the represented transpositions p_lambda((ij)), their generated unital algebra on irreducible V_lambda is all End(V_lambda): transpositions generate S_k, and an irreducible finite-dimensional complex representation has scalar commutant, hence full matrix algebra by the finite-dimensional double-commutant theorem. There is then no nontrivial noiseless subsystem for that whole generated algebra.

This last statement rejects only the proposed literal common-prefix/noiseless-subsystem shortcut. It does not exclude quantum error correction of the **linear** single-error family: products generated to arbitrary length are not the same noise promise. A code may correct the specified family even when its generated algebra is full. Nor has this note proved that every chosen Schur selected set contains all transpositions; that must be checked for each set rather than silently assumed.

## Consequence for the next construction

A successful extensive-defect decoder must either compile the restricted W using code/reference structure (as the simple flag example does), exploit a different recovery operation that avoids the full-row scale, or establish a useful source-weighted interface with a paid acquisition/normalization bound. Merely replacing the exponentially enumerated frame by a coherent representation register leaves equation (1) untouched. The received fixed-defect algorithm solves its small-defect access problem; it does not yet supply one of these extensive-defect mechanisms.
