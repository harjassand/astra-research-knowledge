# Independent review: actual private-pad payload instrument and adaptive composition
2026-10-29. Substantive mathematical review of `PRIVATE_PAD_PAYLOAD_INSTRUMENT_v1.md`; outer instantiated rate/circuit manuscript to be bound separately when received.

## Accepted mathematical mechanism
Let physical Hermitian Paulis have the fixed known frame, and let each joint source Kraus operator be `sum_v P_v tensor A_rv`. For an actual compiled Clifford C, decompose `C†P_v C = phase_v G_v tensor L_v`. Inserting independent maximally mixed gauge and averaging an actual fresh logical Pauli pad/inverse gives cross coefficients

    Tr(G_v G_w†)/d_g times average_K chi_K(L_v) conjugate(chi_K(L_w)).

The first factor vanishes for distinct gauge labels; character orthogonality kills distinct logical labels. The Clifford label map is bijective, so only v=w survives. Scalar Clifford signs cancel on each diagonal. Thus the exact reduced joint operation on arbitrary correlated logical-memory-reference input is

    sum_{r,v} (L_v tensor A_rv tensor I_R) rho (L_v tensor A_rv tensor I_R)†.

No diagonal-channel assumption, independent current logical/memory input, or virtual measurement of an unrandomized channel is used. The actual key average is load-bearing. Averaging the fresh pad before source access also gives physical source input `I_B/d_B tensor rho_M` (and decouples all untouched spectators), so service versus probe preparation is source-indistinguishable under the no-sidechannel interface.

For the full adaptive payload theorem, require the WHOLE original payload plus external reference to be initially independent of source memory. Condition mathematically on source Kraus indices and latent service labels as well as actual probe outcomes/roles. Every branch operator factors as a product of known-location logical Paulis on payload slots and a memory-only operator. The compiler depends only on actual probe records and pads to the same fixed g/k0 split. Therefore branch weights do not depend on the input payload or reference. This inductive factorization survives arbitrary retained memory, source measurements, coherent one-call Kraus combinations, cross-call payload entanglement, and adaptive compiled frames.

The actual probe branch has the same label-indexed memory instrument as the averaged keyed service. Conditional on the full latent prefix, private Bernoulli role choice therefore charges nonidentity service-Pauli events to actual innovative probes. A service fault implies v outside the learned span, while at most m*=dim(S*) innovations can occur. Predictable active indicators and nonnegative summation give expected total faulty service slots <=m*q/(1-q). The latent labels are never supplied to the controller; this is a dilation of a proved averaged channel, not extra acquisition.

The complete pre-outer-decoder payload map is consequently a correlated Pauli channel with input-independent weights. For a total outer decoder that corrects every pattern of <=t whole-block Pauli faults, Markov gives `p_bad<=m*q/((1-q)(t+1))`. Since all good-pattern channels equal identity including an arbitrary external reference, the decoded map is `(1-p_bad)Id+p_bad Bad`, where Bad is CPTP. This directly yields the same half-diamond bound. It is NOT an inference of diamond norm from entanglement fidelity. Finite-cap fallback is charged once by its input-independent abort probability.

## Key privacy clarification (load-bearing)
Keys must remain inaccessible to the source forever, not merely during their own call, and inverse-pad controls must not leak them. Actual retirement/discarding supplies that scope. Later key disclosure before future source actions can destroy the reduced averaged comb. For example, before a hidden gauge algebra is discovered, the source may SWAP an initially unprotected physical logical qubit into its memory. The memory then holds K|psi>; disclosure of K lets the source recover the input. Such a strategy fits a one-qubit Pauli-algebra support on that physical qubit but is not described by the key-retired input-independent memory evolution. Keeping a key record inaccessible forever is equivalent to tracing it for this reduced output, but using it to adapt the source is not.

If the initial payload is correlated with source memory, the single-call identity still holds; the full input-independent correlated-Pauli channel theorem does not automatically follow. No claim about full source/pad purification distance is made.

## Physical and runtime boundaries
Every service handles one fixed k0-qubit outer-code slot, prepared with mixed gauge and fresh pad, then isolates its output. Future unserviced and past serviced payload blocks must remain outside source access. Source-facing timing/routing/control sidechannels must not reveal the private current role. Keys require 2k0 fresh random bits per service and trusted delivery to the inverse-pad controller. Local storage, outer encoding/decoding, finite-field processing and actual Clifford controls remain paid capabilities.

The accepted GRS machinery can support a direct stabilizer code, but the direct-payload implementation must explicitly prepare its zero ancillas, apply U_enc before service, decode after all slots, measure the decoded check registers, and perform the total syndrome/Berlekamp-Welch correction. Merely invoking the bilateral resource-distillation circuit would not specify this operation. If small k0 slots are grouped into field symbols, union bounds charge bad groups by bad slots without an independence assumption; fixed slot grouping and stripe truncation must be stated.

Full Bell probes still require trusted joint reference/output access. This is not free remote LOCC; the previously preserved access boundary continues to apply. No claim of generic unknown noise, unknown frame, fault-tolerant implementation, historical novelty or advantage over trusted-storage bypass follows.

## Executable checks
Independently inspected and reran both frozen programs. Eight generic correlated L:M:R inputs agree with the actual-key/gauge circuit identity within1.09e-16 Frobenius norm; pre-source decoupling error is below2.58e-17. The adaptive two-payload fixture explicitly averages physical keys and gauge traces and compares against a separately stored memory/Pauli-history expansion. For a whole payload maximally entangled with a4D reference, completed Choi operators agree within1.90e-15 through cap24. Fault expectation .277878 is below innovation charge .470788 and rank bound .666667. These are finite floating consistency checks, not the proof or hardware evidence.
