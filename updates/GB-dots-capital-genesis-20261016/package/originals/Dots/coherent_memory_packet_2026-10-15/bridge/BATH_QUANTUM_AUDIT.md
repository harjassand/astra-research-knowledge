# Independent quantum audit of the encoded-orbit bath extension

## Verdict

The quantum claims in REPORT.md Section 9 are correct under their explicit joint-channel, uniform-norm, local-detection, no-local-logical, and common-decoder hypotheses. Refinement is unnecessary for this encoded-orbit argument. This result does not imply a full-input independent rare-fault mixture. Its classical marked-clock certificate and probability bound remain separate premises, audited elsewhere.

## 1. Character cosets really preserve individual Pauli orbits

Let G detect exactly the global stabilizer syndrome of Paulis supported in A, and assume no logical Pauli is supported in A. Expand the joint finite-dimensional unitary U_AB in patch Paulis with bath-operator coefficients. If two supported Paulis P,Q have the same G character, P†Q centralizes every stabilizer and is supported in A. Hence P†Q is a stabilizer, up to phase. Choose one representative P_chi per nonempty character and absorb phases into bath coefficients. Then

U_chi=(P_chi tensor I_B) sum_M (M tensor B_(chi,M)),

where each M is a stabilizer supported in A. There is no assumption that its bath coefficients commute. For a Pauli error E and full-code encoding V, M E V=m_M(E) E V, with m_M(E) a scalar sign independent of the logical vector. Therefore

U_chi(EV tensor I_B)=P_chi E V tensor A_(chi,E),

where A_(chi,E)=sum_M m_M(E) B_(chi,M). This is an equality of linear maps and thus covers arbitrary initial logical-bath-reference entanglement. For the trivial character choose P_0=I. Its syndrome-dependent bath filter preserves the orbit, although it need not be memory identity on arbitrary superpositions of syndrome sectors.

The original completed correction Kraus Q_j Pi_j similarly either annihilates E V or maps it to Q_j E V. The aggregate inactive projector causes no problem: it is a stabilizer function and is scalar on every full-syndrome orbit. Consequently a fixed complete correction/character record follows one Pauli orbit. No additional stabilizer measurement is required for this conclusion.

## 2. Uniform bad-character effect bound

Assume ||U_AB-I_A tensor V_B||<=delta for a bath unitary V_B. Set D=U_AB-I_A tensor V_B. Conjugation averaging E_G gives the exact identity

sum_(chi != 0) U_chi† U_chi=E_G(D†D)-E_G(D)†E_G(D)<=delta² I_AB.

The negative term is positive semidefinite before subtraction. This bound holds on the full joint physical input space and does not use encoded states or refinement. Unitarity also gives sum_chi U_chi† U_chi=I_AB, so the character operators are a legitimate complete Kraus instrument.

After any trace-preserving correction, its adjoint preserves the same upper bound. Conditional on any feasible correction outcome or earlier instrument record, apply the bound to the normalized current joint state. Thus the probability of a nontrivial character is at most delta². Zero-probability histories require no conditional state.

This proves a bounded conditional instrument probability, not an independent physical Bernoulli decomposition. The latter generally fails because even the zero character can enact syndrome-dependent bath operations.

## 3. Adaptivity and discarded frames

Arbitrary causal dependence of U on genuine past classical records is allowed if the hypotheses, especially the same uniform norm bound and fresh-frame independence, hold for every admissible record. In a fixed Kraus record the selected unitary is definite, and its bath coefficient is multiplied in chronological order. Bath operators can be noncommuting and can retain all quantum correlations allowed by the finite bath model.

Mathematical character labels need not be actual observed records. A controller cannot be said to depend on those fictitious labels unless the corresponding instrument/record is actually implemented or its availability is explicitly added to the model. Existing physical classical records may instead be included in the record indexing, or represented by finite classical registers in the bath. Summing over records leaves a CP map, even with history-dependent choices.

Crucially the actual joint memory-bath map must equal the ideal frame twirl. The fresh frame must be sampled independently of the current joint state and the operation U, and its explicit classical register must be discarded/inaccessible to later operations. Retaining it and allowing subsequent feedback invalidates the use of the marginalized channel. Correlations transferred indirectly to the modeled bath through the stipulated joint U are already covered; an unmodeled frame leak is not. Noisy/frame-dependent physical implementations require another argument.

For a fixed finite-dimensional input/output bath, abstract classical histories can be summed and discarded without expanding the bath output dimension. If an unbounded classical record is retained as part of the output bath, that is an additional infinite-dimensional extension and is not covered by this audit.

## 4. Good subchannel and completion

Assume a measurable, input-independent rule selects complete Kraus records as good, and the deterministic support certificate guarantees that one fixed decoder maps every selected Pauli history E to a scalar multiple of logical identity. The selection may be a function of clock and instrument records; it cannot be chosen differently after inspecting the unknown input state.

For each good complete record alpha, including decoder label, the decoded Kraus operator is I_L tensor B_alpha. This follows from the map identities above before density matrices are formed. Averaging clocks and summing good records therefore gives G=Id_L tensor Lambda_g, where Lambda_g is CP and trace-nonincreasing. A good-record subset is not generally trace-preserving.

Let Gamma be the full decoded CPTP channel, and H=Gamma-G its bad CP subchannel. Then

H*(I)=I_L tensor D,  D=I_B-Lambda_g*(I),  0<=D<=I_B.

If bad probability is at most epsilon for every encoded joint logical-bath input, the effect inequality gives D<=epsilon I_B. In fact testing all bath states with any fixed logical state suffices. The claimed probability bound must be uniform over bath input states; one fixed prepared bath state would not establish the displayed joint-domain diamond bound.

Fix any output bath density matrix sigma and define Lambda_b(X)=Tr(DX) sigma. This map is CP, has adjoint effect D, and completes Lambda_g to a CPTP bath channel Lambda_g+Lambda_b. For any CP map Phi, ||Phi||_diamond=||Phi*(I)||. Hence

||H||_diamond=||D||,  ||Id_L tensor Lambda_b||_diamond=||D||,

and the triangle inequality gives

||Gamma-Id_L tensor (Lambda_g+Lambda_b)||_diamond<=2||D||<=2epsilon.

Tracing the output bath is contractive and yields the asserted recovered logical-reference estimate with arbitrary initial logical-bath-reference entanglement. The completion is mathematical; it is not a proposed physical intervention or a claim that actual bad dynamics is bath-only.

## 5. Boundaries retained

- No replacement by the fixed-U theorem's independent thinned streams.
- No assumption that a normalized good conditional channel is CPTP or input independent.
- No extension from memory-only twirling to the joint bath channel without an explicit premise.
- No claim about arbitrary continuous Hamiltonian interactions between proposal slots.
- No certification here of the marked-Poisson envelope, its monotonicity, or its failure probability.
- Finite-dimensional bath input/output and a common full-logical-space decoder are retained.

No quantum counterexample was found under these precise hypotheses. The uniform recordwise norm bound and inaccessible fresh frames are substantive assumptions rather than consequences of a small averaged error rate.
