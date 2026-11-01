# Verified plans: exact native execution, conditional commit, and certificate/rearm obstruction

Developed after reading the parent's verified-plan proposal, 2026-11-01. The clock note remains frozen unchanged.

## 1. Exact physical remaining-mask operation

For a witness register w and physical mask register m, define
 D=product_i CNOT(m_i -> w_i),  W_virtual=D W D†.
The native two-qubit jump
 L_i=sqrt(kappa) X_(w_i) tensor |0><1|_(m_i)
executes one pending witness flip and clears its mask bit. Direct conjugation gives
 D† L_i D = sqrt(kappa) I_w tensor |0><1|_(m_i).
Consequently the dissipator satisfies D[L_i]^*(W_virtual)=0, and likewise D[L_i]^*(exp(a W_virtual))=0. This is exact for coherent, entangled masks, not only classical plans. In the decoded frame the jump simply damps a gauge ancilla. It cannot damage protected logical information.

An active flag a permits an inactive plan-loading phase:
 D_a=product_i C^{a m_i}X_(w_i).
For a=1, condition the same execution jump on a; it then has three-qubit support and the same decoded action. For a=0, writing mask bits does not affect the decoded witness. Each physical bit and flag must remain in the noise budget. One shared active flag spreads a fault across the entire bounded plan footprint in the decoded frame; that constant, and its incidence, must be charged.

## 2. Native commit is possible ONLY conditional on physical certificate soundness

Let q be a physical certificate qubit. The two-qubit commit jump
 L_commit=sqrt(kappa) |1><0|_a tensor |1><1|_q
activates the already stored mask. In the decoded frame it applies X^m to witnesses. If q=1 certifies that m is the selected strictly downhill update for the current local syndrome/witness pattern, this is precisely the desired abstract correction branch. Its decrease of W_virtual is at least1. It has the same protected-logical property as the original witness-update branch within the admitted safe component.

This is a genuine way to move the large conditional operation into PHYSICAL metadata and a controlled decoding frame. It is not a proof that q is reliable. A corrupted q or mask changes the decoded data by a bounded-support operation; that alone makes it admissible NOISE, but does not justify allowing the ideal controller to create false certificates at an unsuppressed rate.

Also, commit preserves m and old input records, so the quantum input need not be erased. No CP 'completion map has a good kernel' assumption is required: D_a is an explicit unitary, and protected logical observables are D_a(L_original tensor I_metadata)D_a†, augmented by the established witness frame. Auxiliary stabilizers and any certificate-validity constraints still require a separate ground-space specification.

## 3. What a classical verifier really provides

If the actual predicate inputs are available as native commuting physical bits, implement a finite bounded-fan-in Boolean circuit with physical gate-output bits. For gate j let E_j be the projector onto output_j != f_j(inputs_j). A native local jump repairs its output. With topologically ordered weights satisfying
 mu_j > sum_(k directly downstream of j) mu_k + B_j,
its repair decreases sum_j mu_j E_j, allowing for a bounded change B_j of the remaining potential. This is a useful finite noisy apparatus construction; weights may be enormous but do not scale with memory size. The constraints also certify that an output q is the correct function when all E_j=0.

However the quantum syndrome is NOT a primitive collection of native input bits. A source consistency term contains S_v Z_(s_v), where S_v is the real stabilizer. Repairing s_v conditional on it is exactly the high-body operation we set out to compile. Replacing it by a stored bit without charging staleness or extraction progress is circular. Overlapping X/Z-check partial extraction must be treated as quantum circuits with the appropriate frame and ownership; separately reading their single-qubit factors can reveal logical information or introduce unwanted disturbance.

## 4. A second, independent gap: perpetual verifier rearming

Even granting initial true inputs, disabling verifier penalties after commit does not automatically make a forever-running decoder. After executing the mask, the witness has changed. Turning the inactive verifier back on with its old records generally creates new consistency violations. Resetting all workspace to zero is not a consistency repair for an arbitrary new input.

A minimal example exposes the bookkeeping: W(w)=w for one classical witness, an input-copy wire v, and E=[v!=w_virtual]. A correct commit w_virtual:1->0 with v=1 changes W by-1 and E by+1. Keeping the same certificate penalty mu E gives total change -1+mu; suppressing an erroneous uphill commit of size1 by this single penalty would demand mu>1. One cannot simultaneously call both transitions strictly downhill using that same static bookkeeping. This example refutes that simple certificate-energy argument, not all plan architectures.

Phase-dependent freezing can avoid the increase at commit, but then reactivation must be accounted for; it cannot be hidden in a clean reset. Retaining old and new records and reversibly computing the next workspace is possible, but requires a real bounded-time progress/energy argument. It returns us to the clock/ownership theorem rather than eliminating it for free.

## 5. Earned capability and decisive next gate

Earned: exact two-/three-qubit execution of remaining masks, explicit protected unitary frame, and a two-qubit physical commit conditional on a genuinely sound local certificate. This is stronger and more specific than an abstract CP completion proposal.

Not earned: a perpetually reusable native certificate engine whose false-plan repair, extraction, commit and rearm jointly admit extensive positive drift under arbitrary local coherent noise. A single completion probability or a static classical Boolean verifier does not establish it. The important verification target is now one COMPLETE reusable plan transaction, including quantum-syndrome extraction and workspace rearm, with a positive potential on every physical metadata state. Neither reliable metadata nor uncharged fresh ancillas is allowed.

The ordinary active Tanner decoder gets the identical gates, masks, noisy ancillas and graph. The native plan execution is useful to that comparator as well. Any new capability must come from proving autonomous reusable transaction drift/containment, not merely the low-arity commit syntax.
