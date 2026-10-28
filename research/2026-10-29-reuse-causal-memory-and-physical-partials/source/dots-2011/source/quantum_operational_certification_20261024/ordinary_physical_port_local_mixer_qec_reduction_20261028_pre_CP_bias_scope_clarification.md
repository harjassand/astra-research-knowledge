# Full physical-input access turns local mixer acquisition into a known-QEC module

28 October 2026. **New candidate interface reduction; independent receiving pending.** This is a stronger-access, potentially more scalable alternative to the injection-only coset lift. It does not make that extra port or local mixer structure free. It imports the received margin-free local acquisition and complete CP-domination results without changing their proofs.

## 1. Stronger physical access and restricted source structure

The device exposes n known physical input qubits BEFORE the unknown noise/mixer. It permits ordinary product-state preparation on ALL n input wires for calibration, and actual local physical Pauli gates on arbitrary encoded payloads at the same port for service frames. The latter is explicitly required; a state-preparation-only black box would not suffice. At the output all n known physical qubits support ordinary product-Pauli readout and the received local controlled-reflection interface.

The complete source at every exposed prior history has the form

    N=(Ad_V tensor id) o sum_alpha(Ad_Palpha tensor F_alpha),     (1)

where P_alpha ranges over n-qubit Paulis, F_alpha:M->M' are arbitrary CP retained-memory maps and T=sum_alpha F_alpha is TP. V is an unknown fixed n-qubit unitary. The instrument may vary arbitrarily with time/history; current preparation/readout/frame coins do not directly leak to its selected current map. There is no iid-across-use or memory-reset assumption. This is a physical Pauli-instrument source followed by a fixed mixer, NOT a general unknown quantum channel.

On a known physical output line, the TWO observables V X_i Vdagger and V Z_i Vdagger for each input i are jointly supported in some unknown interval of length at most a supplied w. Their logical algebras commute exactly for distinct i because all arise from the SAME V. Bounded-depth local circuits are possible instances, but circuit depth is not inferred from data and a generic dense V need not satisfy the promise.

During calibration require only the qualitative CP signed biases

    H_(i,j)=sum_alpha chi_(i,j)(alpha) F_alpha is CP,
    i=1,...,n, j=X,Z,                                           (2)

where chi is the Pauli commutation sign. No numerical positive bias or supplied support interval is required. The conditions are structural promises, not finite-data source-membership tests. For example a complete per-site nonidentity-error bound <=_CP p_max T with p_max<1/2 implies H_(i,j)>=_CP(1-2p_max)T. Such a stronger bound must itself be supplied/proved; mere observed small error frequencies do not establish CP order with memory.

This full physical port is stronger than only logical product preparation through a fixed code plus X-syndrome injection. The injection-only coset lift remains valid under that weaker interface. Neither construction discovers an arbitrary new code.

## 2. Automatic local excitation, with no dormant syndrome directions

Treat the n physical input qubits as q=n logical factors and the emitted gauge as TRIVIAL. Uniform ordinary product X/Z axes and signs average each input to I/2. For every incoming memory operator omega,

    N(I/2^n tensor omega)=I/2^n tensor T(omega).                 (3)

Thus any output interval J has unsigned marginal I_J/2^|J|, even jointly with outgoing retained memory. An individual readout can still update conditional memory; (3) is an averaged complete-map identity.

For an i,j signed input probe, write B_(i,j)=V sigma_(i,j)Vdagger. The full signed output/memory operator is

    B_(i,j)/2^n tensor H_(i,j)(omega).                           (4)

If J contains the true support, reduction gives

    Delta_(i,j,J)=B_(i,j,J) theta_(i,j)/2^|J|,
    theta_(i,j)=Tr H_(i,j)(omega) in [0,1].                      (5)

Every conservative envelope is fully excited: its marginal floor is EXACTLY 2^-|J|, including padding outside the true support. No dormant syndrome/spectator occupation needs to be manufactured. The true signed gap is theta_(i,j)/2^|J|. Positivity alone does not force theta>0; the finite learner may still abstain when complementary information vanishes.

Equations (3)--(5) are an exact specialization of the received margin-free local-gap source to q=n, G trivial. Use its paired-axis support scores, permanent asynchronous support/reflection certificates, finite stage caps, rational sign fits and colored ONE coherent extraction circuit. This learns a physical implementation of Vdagger on all n qubits; it is not n independently fitted marginal channels. Unknown-payload inputs are introduced only after acceptance.

Let W=min(n,3w-2) and let A be the SAME overlap/cone factor defined by that received source. If a uniform declared reached-history signed bias theta_*>0 is available as an instance condition, the least fine gap is >=theta_*/2^W. To get a global complete-reference learned-inverse defect b<=1/4, run the received learner with epsilon_train=4b. Its fine source scale is

    O_tilde(A n 3^W/[ (theta_*/2^W)^2 b])
       =O_tilde(A n 12^W/(theta_*^2 b)),                         (6)

plus its coarse support acquisition. The actual algorithm does not receive theta_*. The funded cap, persistent/intermittent excitation and accepted-risk qualifications remain exactly those of the received theorem. At fixed w this is polynomial in n; it is NOT polynomial in arbitrary unknown mixer width. Every source block still prepares and reads n physical qubits, so physical traffic multiplies the block count by n.

## 3. Complete learned-inverse reduction before a KNOWN quantum code decoder

Fix b as an acceptance target/uniform upper bound on every good accepted record, rather than a random record-dependent number. On a good accepted record, the frozen physical inverse receiver Rhat has global n-input Bell error at most b relative to Vdagger. The gauge is trivial, so this is the uniform-all-gauge hypothesis of the received CP-domination theorem. In service apply a fresh uniform n-qubit Pauli Q AFTER any known code encoder but BEFORE (1), then Qdagger AFTER Rhat and BEFORE the known code decoder. Pay 2n fair bits and both sets of actual physical frame gates. Keys must be privately retired and never fed to later source/controllers.

With all original physical outputs and receiver records discarded, the DECLARED exact-control privately framed learned physical channel obeys

    N_hat >=_CP (1-b) sum_alpha(Ad_Palpha tensor F_alpha).       (7)

This exact-control complete-map inequality includes arbitrary physical-input/memory/reference correlations. A generic finite physical implementation error need not preserve exact CP order; the IMPLEMENTED module inherits the final process-distance statement with its whole-service norm debit, not automatically the same exact CP decomposition. It does not require positive biases at service time once V has been acquired. It does require the same fixed V, physical Pauli-instrument form and frame-privacy interface. Output frames cannot silently be replaced by only logical code frames: arbitrary physical Paulis generally change code syndromes.

Now supply ANY known quantum encoder Enc:L->P and known CPTP decoder Dec:P->L. Suppose a specified set Good of physical Paulis is exactly corrected:

    Dec Ad_Palpha Enc = id_L  for alpha in Good.                 (8)

This is a known-code operation contract, not something inferred by local mixer tomography. Enc/Dec may be stabilizer circuits, another explicitly implemented quantum code, or a small known repetition code. Their resources and accuracy are paid. Composition of (7) with Enc/Dec gives

    R_hat,code >=_CP (1-b) R_exact,code.                         (9)

Assume additionally a complete native bad-pattern bound

    T_bad:=sum_(alpha notin Good) F_alpha <=_CP r T              (10)

for a supplied/proved r in [0,1]. Then T_good>=_CP(1-r)T, and the known exactly corrected branches give

    R_exact,code >=_CP (1-r)(id_L tensor T),
    R_hat,code >=_CP (1-b)(1-r)(id_L tensor T).                  (11)

This is an identity-logical/noisy-memory component, not merely a current-gauge oracle regret. With eta=b+r-br, it is a virtual convex decomposition R_hat,code=(1-eta)(id_L tensor T)+eta F for a complete CPTP residual F. There is no observable clean flag. Bad branches may contain arbitrary logical-memory correlations.

Under the same common causal controller and key/gauge-retirement rules, J finite encoded uses have process-distance allowance

    1-[(1-b)(1-r)]^J <= J(b+r-br).                              (12)

The reference process replaces only these encoded forward modules by id_L tensor T_h; other gates/storage remain as declared. The all-clean CP branch has the exact reference memory trajectory; no actual-occupation shortcut is used. This is not a full computational fault-tolerance threshold.

## 4. A physically meaningful native error-tail premise

Condition (10) is stronger than a scalar probability at one occupied memory state. It holds, for example, when a CP memory instrument selects conditionally independent per-site physical Pauli errors with total nonidentity rates <=p_max, and the known code corrects all patterns of weight <=t. At each instrument branch the probability of weight >t is bounded by the binomial tail

    r= sum_(s=t+1)^n binom(n,s) p_max^s(1-p_max)^(n-s),          (13)

using independent Bernoulli domination if the rates differ by site. For this example one must also require the EXACT scalar-mixture map F_alpha=sum_a w_alpha,a K_a: the retained output K_a has no additional sampled-error-pattern tag or pattern-dependent state update. Multiplying the scalar inequality by each SAME CP instrument branch K_a and summing then proves (10). If outgoing memory retains the actual error alpha, its bad branch can have support orthogonal to its good branch; a small bad-event probability then does NOT imply CP domination by r times the total map. Such a source is allowed in (1) and can still be calibrated, but it needs a different service comparison unless (10) is separately established. The branches may be arbitrarily correlated between different uses through retained memory. For t>=1 and fixed n, the native error is of order p_max^(t+1); a useful physical module additionally requires learned b and all encoding/decoding/control/storage errors at that scale.

This conditional independence/error-tail premise is not a consequence of calibrating V. General correlated Pauli instruments may violate (10) despite small one-site error rates. No local-stochastic threshold, optimal code selection or efficient fault-tolerant encoder/decoder is established.

## 5. Physical ledger and accepted-process scope

Calibration uses the full unencoded n-wire product-input port, all n output readouts, actual paired-axis random labels and the received finite matrix arithmetic. It neither prepares entangled calibration references nor uses the supplied code as an uncharged helper. It does require that the source remain the SAME fixed-V instrument family on both unencoded calibration and encoded payload inputs.

Service prepares n mixed extraction ancillas and uses the received 3n controlled-patch-reflection network with its actual coloring/routing and full-register error budget. These are width-W+1 controlled operations, not automatically elementary gates. It then pays the known quantum decoder on the extracted n-qubit register, along with the known encoder, Pauli frames, source traffic, resets, holding and disposal. The arbitrary code decoder may itself be expensive or noisy; learning a local mixer does not fix that. There are N calibration blocks plus J encoded blocks, each using n physical source wires, for n(N+J) physical passages.

The two compared processes share the ACTUAL calibration record, memory, acceptance and abort branch. With nominal bad-certificate mass beta, full retained-record discrepancy nu_cal and whole-J-service implementation discrepancy nu_J, add beta+nu_cal+nu_J ONCE to (12), capped at one. The unknown payload is requested only after acceptance. Conditional-on-acceptance claims pay their probability denominator; no public-record posterior guarantee is asserted. The initial payload/reference is conditionally product with source for a payload-only induced channel, or the complete comparison is understood on the enlarged joint input.

The strongest equally informed conventional learner gets the SAME full physical port, locality, Pauli-instrument promises, known code and controls, and can implement this route. Its advantage over dense injection-only learning is an interface/structure advantage, not a computational separation. General unknown-noise code discovery, model-membership certification and practical hardware performance remain open.
