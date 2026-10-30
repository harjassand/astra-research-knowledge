# A baseline-free bilateral encoded-Bell buffer
2026-10-30. Constructive scheduled LOCC implementation; algebra and the retained-bath common-span step are independently proved in BILATERAL_BELL_ALGEBRA_AUDIT.md and BILATERAL_SCHEDULED_CPTP_ADDENDUM.md. This is a Bell-resource preparation-and-maintenance bridge, not arbitrary quantum-state loading, not a finished autonomous LOCC compiler, and not a new entanglement-purification principle.

## Useful result first
A shared encoded Bell resource does not require either party to know or erase its extensive initial syndrome. Prepare physical Bell pairs, measure identical local CSS checks, and continually correct the DIFFERENCE of the two parties' syndromes. The unknown common syndrome cancels. No immutable baseline register and no initial global syndrome-to-Pauli computation is needed.

A constant-iteration single-shot Tanner decoder gives a concrete noisy, constant-depth-per-round ordinary implementation. Its local classical circuitry may itself be faulty; finite-depth fault spread is charged. The necessary ongoing resource is two-sided syndrome extraction plus classical communication, not entangling gates between the separated parties. This is stronger operationally than silently assuming pre-encoded links, but its scheduled version is an ordinary entanglement-purification architecture, not an autonomous-memory priority claim.

## 1. Exact preparation instrument
Let C be a real CSS [[N,k,d]] code, r=N-k independent stabilizers, and Pi_s its syndrome-sector projector, with rank d_L=2^k. Let D=2^N and

    |Phi_D> = D^{-1/2} sum_x |x>_A |x>_B.

This is N physical Bell pairs, not an encoded Bell pair. In the noiseless protocol Alice measures the commuting stabilizers locally; Bob may measure the same stabilizers locally. The instrument obeys

    (Pi_s tensor Pi_t)|Phi_D> = 0 for s!=t,
    Pr(s=t)=2^{-r},
    |Phi_s> = sqrt(D/d_L)(Pi_s tensor I)|Phi_D>.

If V_s is any isometry onto the s-sector, then

    |Phi_s>=(V_s tensor V_s^*)|Phi_(d_L)>.

For any Pauli P_s taking C into the s-sector, choose V_s=P_s V. Thus

    |Phi_s>=(P_s tensor P_s^*)|Phi_C>.

Changing P_s by an encoded logical Pauli changes both halves conjugately and leaves the Bell state invariant. The state has the known +1 eigenvalues of every fixed paired logical operator barX_i^A barX_i^B and barZ_i^A barZ_i^B, despite its random individual syndrome. There is no exponentially unlikely postselection on s=0.

All stabilizer measurements have bounded weight and incidence. One ancilla per check and a fixed coloring of local extraction gates implement the complete commuting measurement instrument in constant graph-local quantum depth, with X/Z extraction blocks sequenced as necessary. Initial Bell-pair creation and transmission noise are charged as initial bounded-support faults. N noisy physical pairs are a genuine one-time entanglement input; they are not created by LOCC, and asynchronous acquisition of those N pairs is a separate source-buffering cost.

## 2. Relative error is the protected quantity
For physical Pauli errors E_A,E_B, using the transpose identity on |Phi_D>,

    (E_A tensor E_B)|Phi_s>
       = phase · (I tensor E_B E_A^T)|Phi_(s+sigma(E_A))>.

Let e be the binary Pauli label of E_B E_A^T. The unknown common syndrome may change arbitrarily under common Pauli errors, but the measured difference is exactly sigma(e). Common errors have e=0 and merely change the shared syndrome sector.

After ideal local measurements with outcomes s_A,s_B,

    s_A+s_B = sigma(e).

Applying a Pauli f on Bob's half changes e to e+f. The ordinary code decoder can therefore act on the relative syndrome without ever decoding s_A or s_B individually.

If e+f is an ordinary code stabilizer, then

    (I tensor P_(e+f))|Phi_s>=phase · |Phi_s>.

The unknown syndrome changes only that harmless stabilizer phase. Thus ordinary stabilizer-reduced error control protects the logical Bell correlations. It does NOT protect an arbitrary joint logical state of A,B: common logical Paulis can act nontrivially on such a state. In particular there is no claim that the enlarged joint code has distance d; its low-weight common Pauli directions are gauge directions for this Bell-resource target.

## 3. Actual scheduled LOCC round
At each round:
1. Alice and Bob each run a local bounded-depth CSS syndrome extraction circuit, producing their local classical records.
2. Alice sends her O(N) syndrome bits to Bob over a declared classical channel. Bob forms their bitwise difference.
3. Bob runs a FIXED number of parallel single-shot Tanner decoder iterations, for both CSS sectors, on that difference.
4. Bob applies the resulting Pauli mask locally and resets round scratch space. No accumulated Pauli frame is needed for this correction policy.

Only local quantum operations and classical messages cross the Alice/Bob partition. No maintained inter-half Hamiltonian, quantum bus, entangled refresh ancilla, or new entanglement supply is used during storage. Allowing such resources would change the comparison and could trivialize maintaining Bell pairs.

The round duration tau includes extraction, classical propagation, local parallel decoding, and correction. Require tau bounded independently of N, or explicitly scale the fault budget with tau. An arbitrarily long physical link is not a free constant-time classical channel. O(N) check bits per round and corresponding bandwidth are real costs. Lost/corrupted bits and local classical gate faults are included in the round fault budget; nonlocal simultaneous bus failure is not a bounded-incidence local fault.

## 4. Deterministic contraction, including faulty local classical processing
The primary Tanner single-shot theorem supplies constants A,B,C,beta and a fixed iteration count with alpha<1 such that, whenever

    A |e|_R+B|D|<=C N,

its ideal local classical circuit returns f with

    |e+f|_R<=alpha |e|_R+beta |D|.

Its parallel implementation has constant depth for that fixed iteration count, bounded-degree local communication, and finite local lookup tables. Thus a fault in its classical circuit changes at most a constant number of final correction bits; fresh scratch is reset each round. There is no need to demand that every classical gate in the entire N-site decoder be correct.

Relocate quantum extraction/gate faults through the bounded-depth nominal Clifford circuit. They produce bounded-support data Pauli terms and bounded syndrome-record flips on a common actual fault-location support. The local classical circuit has bounded light cones even though it is nonlinear. All faults, including those while the classical message travels, can therefore be bounded by a per-round count K_j with fixed constants:

    |a_j|<=c_a K_j, |D_j|<=c_D K_j, |b_j|+|g_j|<=c_b K_j.

Here a_j is data noise before the ideal snapshot, b_j after it, and g_j the discrepancy from faulty decoder/correction outputs. The residual recurrence is

    r_(j+1)<=alpha(r_j+c_a K_j)+beta c_D K_j+c_b K_j
             =alpha r_j+C_K K_j.                    (1)

A minimum stabilizer representative can be used in this inequality since it gives the same syndrome and decoder output. This is not a minimum-*syndrome*-weight replacement that could erase an unknown logical error.

Choose a small constant f and suppose K_j<=fN each round. With r_0<=z0N, induction gives

    r_j<=zN,  z=max{z0,C_K f/(1-alpha)},

provided A(z+c_a f)+B c_D f<C. Pick z well below d/(2N) and all decoder radii. Initial transmission/preparation faults have the same small-total-support requirement. No temporal independence of the errors is needed for this deterministic argument.

A local-stochastic or bounded-rate exogenous Poisson fault-location model supplies Pr(K_j>fN)<=exp(-cN) for sufficiently small fixed physical noise and fixed tau. Union-bounding L rounds gives a failure envelope of the form

    delta<=eta_source+C(L+1)exp(-cN).                (2)

The old persistent calibration offset is absent. All syndrome registers are fresh round records stored only for tau, so an O(N)-bit unprotected baseline is not being assumed stable for exponential time.

## 5. Quantum scope and coherent errors
The deterministic bound holds for EVERY Pauli coefficient history on a common safe physical fault record under the explicit measured classical-gate/message implementation in BILATERAL_SCHEDULED_CPTP_ADDENDUM.md. That addendum proves the common support envelope from bounded-depth extraction and bounded-depth classical control: no Pauli branch probabilities are assigned. Relative Pauli errors differing by ordinary code stabilizers act identically on the target Bell resource up to syndrome-dependent phases, so a final relative recovery sends the entire safe span to the same pure logical Bell state, with all syndrome/controller/bath dependence outside that factor.

Consequently the correct quantum conclusion is a trace-norm/fidelity bound for the known Bell resource (or Bell-diagonal classically labelled resources), after the declared relative encoded decoder. It is NOT the arbitrary-input logical diamond-norm identity theorem of the original memory. The common-span proof must retain all measurement records and any common bath; no twirl is assumed.

The source single-shot theorem is stated for Pauli errors and ideal classical processing. Equation (1) supplies the finite-depth classical-fault extension at the support level. The frozen BILATERAL_SCHEDULED_CPTP_ADDENDUM.md pins the measured record/control channels and proves the common-record factorization, including coherent gauge inputs and a uniform positive bad-record tail. Equation (2) therefore defines a proved ordinary scheduled-circuit construction in that scope, not a reviewed native-controller theorem.

## 6. Retrieval and what is already operational
For a formal relative decoder, measure exact local syndromes, decode their difference, and correct Bob. The sectors then match. Both parties could use ANY common syndrome preimage and local code decoding to obtain k Bell pairs; no minimum-weight inference of the extensive common syndrome is needed. Such final decoding is an interface, not a noiseless bare-output guarantee.

A concrete classical endpoint needs less: to test/read paired logical X correlations, both measure physical X; XOR corresponding raw outcomes and run the noiseless relevant-sector classical decoder on the resulting difference string. The common syndrome cancels in the paired check parities. Z correlations work analogously. This uses only local destructive measurements and classical communication, with output noise added as relative data masks. It does not by itself furnish arbitrary encoded teleportation or a fault-tolerant bare Bell-pair output.

A previously proved zero-syndrome Bell switch cannot simply be attached without checking its signed-code input/readout conventions. The maintained output here is a shared-syndrome encoded Bell resource, not two individually vacuum-syndrome memory blocks. The direct full-physical-mask switch in SIGNED_SECTOR_BELL_SWITCH.md supplies that signed-code operation without conversion: send and apply all raw physical Bell byproduct bits inside a declared finite-latency terminal stage. Its autonomous live-controller seam is still a separate obligation.

## 7. Strong ordinary comparator and claimed contribution
The basic projection and syndrome-difference protocol is standard CSS entanglement purification, explicitly described by Shor–Preskill, arXiv:quant-ph/0003004, p.2: local check measurements project perfect physical pairs into a common syndrome-coded Bell state, and disagreements diagnose relative bit/phase errors. Bennett–DiVincenzo–Smolin–Wootters established the error-correction/purification correspondence earlier. None of this is claimed as new.

The useful application of the current analysis is to recognize that this resource-specific interface removes the previously assumed high-energy preparation-frame inference and stable-baseline record. Ordinary scheduled noisy single-shot Tanner correction already provides the strong constructive comparator. A new autonomous result would require an actual finite-rate LOCC transaction/message compiler with noisy local records, consistent snapshots, physical-time service bounds, and no entangling inter-party interaction. The existing coherent Tanner controller does not automatically supply that LOCC compiler.

Primary sources inspected: https://arxiv.org/pdf/quant-ph/0003004 (CSS purification instrument); https://arxiv.org/html/2306.12470 (Definitions 3.2–3.3, Theorem 3.5, Corollary 3.6, parallel decoder and Theorem 4.20). The recurrence and physical resource accounting above are the present derivation.
