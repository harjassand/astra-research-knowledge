# Independent review: correlated-input accepted memory-filter theorem
2026-10-29 UTC. Reviewer: `review_current_channel_symmetry`.
Disposition: **accepted as a joint accepted-instrument statement**, not as scalar acceptance or normalized marginal preservation. All v1 physical boundaries, the finite cap, explicit Clifford/Pauli outer decoder, and permanent key retirement remain necessary. This receipt does not authorize a late-public-key or arbitrary-noisy-control version.

Governing `CORRELATED_INPUT_MEMORY_FILTER_v3.md` and check_memory_filter_v3.py/.json are hash-bound in RECEIPT_CORRELATED_v3.json. The author illustrative program reruns byte-identically. Independent actual finite-guard, tightness, steering and late-key challenge checks are in check_correlated_filter.py/.json.

## 1. Map types and factorization
Let U be the original logical payload, M the entire source-accessible initial memory, and R an arbitrary external reference not acted on by the protocol. The compared maps take U tensor M to U tensor M_out tensor T, where T contains allowed retained transcripts; the diamond norm extends them by id_R. The ideal is id_U tensor B_acc, with B_acc a trace-nonincreasing CP memory/transcript map M -> M_out tensor T. It is not generally p times a TP map for one input-independent scalar p.

The reviewed full joint service-twirl identity is valid on arbitrary U–M inputs. Actual independent fresh test preparation and local endpoint controls preserve a branch form Pauli-pattern-on-outer-data tensor memory-Kraus-map. Retired pad keys are averaged, never conditioned upon. The exact outer Clifford decoder maps every physical Pauli pattern—not merely correctable ones—to a deterministic syndrome and a logical Pauli. Its initialized ancillas, syndrome-only deterministic correction and fixed Pauli fallback introduce no payload-dependent record. Therefore every accepted refined branch is L_h tensor A_h. Correctable branches have L_h=I up to an irrelevant phase.

Virtual Kraus/Pauli flags may be used for the proof, then traced out. Actual retained records are only those allowed by the interface. If an additional physical output environment is to be assessed, it must be included in M_out when defining the source/instrument, rather than identifying an arbitrary Kraus label with a physical measured record.

## 2. Uniform bad effect and diamond bound
For any initial memory density sigma, applying the product-input theorem with an arbitrary fixed payload bounds Tr[B_bad(sigma)] by epsilon_NB. Since the branch maps themselves are fixed independently of that input, this holds for every sigma and implies

    E_bad=B_bad^dagger(I)<=epsilon_NB I_M.

One can equivalently track memory marginals in the branch tree: a unitary on U leaves the M marginal unchanged even on correlated inputs. This does not require the joint branch state to factorize. It supplies no scalar input-independent acceptance assertion.

The flagged bad memory map has effect E_bad. For a CP map its diamond norm equals the operator norm of its effect; tensoring with id_U leaves that value unchanged. After this flagged map, actual conditional-L_h application and ideal identity application are both CPTP postprocessings. Their difference has diamond norm at most two. Thus

    (1/2)||A_acc - id_U tensor B_acc||_diamond <= ||E_bad|| <= epsilon_NB.

This proof includes arbitrary U–M–R correlations. It uses the norm of the AGGREGATE effect, not a sum of individual branch norms. The latter can be arbitrarily looser: the independent check gives four orthogonal bad memory branches each of norm 0.03 but aggregate effect 0.03 I. The actual bad logical X distance attains 0.03, not 0.12. This also shows the aggregate bound is generally tight.

The real and ideal maps have exactly the same acceptance effect I_U tensor B_acc^dagger(I), because every L_h is unitary. Hence they have the same acceptance probability on each fixed joint input; that probability can vary with its memory marginal. If that probability is positive, normalizing a fixed input costs division by its own probability. There is no single universal normalized accepted channel on U when arbitrary initial correlations are allowed.

## 3. Steering is unavoidable, not a theorem defect
The ideal filter itself can steer the user marginal. For an initial Bell state of U and M and a memory acceptance Kraus diag(1,1/2), the ideal pass probability is 5/8 and the normalized user marginal changes from diag(1/2,1/2) to diag(4/5,1/5), despite identity acting on U. Our independent executable verifies this exact example. Consequently a statement that the accepted marginal equals the original user marginal would be false, even for the ideal comparator. The manuscript correctly rejects that interpretation.

## 4. Counterexample challenge: late disclosure of the pad key
Permanent key retirement is LOAD-BEARING for the full joint-output claim, even when disclosure occurs only after the last source call. Take a single qubit service U_theta=exp(i theta Z), with no source memory. Random logical Pauli conjugation and key retirement yield

    (1-sin^2(theta)) id + sin^2(theta) Ad_Z,

whose half-diamond error is epsilon=sin^2(theta). If the previously private conjugating key is then appended to the output, every key block instead contains the coherent rotation by +theta or -theta. On input |+>, distance from identity on the payload tensor an independent uniform key is |sin(theta)|=sqrt(epsilon). Revealing the key is not a permissible postprocessing of a state in which that key was already traced out.

At theta=0.07 the independent check gives reduced retired-key error 0.0048920019 versus joint disclosed-key distance 0.0699428473. The discrepancy does not require a hostile bath or later interaction. Therefore no earlier remote-interface permission to release pads after storage may be imported into this theorem. Its allowed memory/transcript output excludes retired key records. A separate late-key variant would require a weaker bound or a different protocol/proof.

## 5. Actual sequential correlated-input check
The new independent check uses the prior independent three-Kraus NONUNITAL n=4 physical source with three-dimensional retained memory, its actual weighted sign-test map, and its actual inner encoder/TP decoder Pauli instrument. For valid trivial outer code J=1,t=0, failure budget b=0 and cap8, it explicitly sums all accepted histories consisting of r passing tests followed by a service. Its accepted memory maps are

    B_P = s sum_{r=0}^{L-1} Phi_P composed with (a Psi_pass)^r.

This construction uses actual noncommuting memory updates rather than an iid count replacement. The bad effect norm is 0.1610040431, below the NB bound 0.4883720930. Across 100 arbitrary pure payload–memory–reference inputs, real-versus-ideal joint trace distances remain below the bad effect norm, with maximum 0.1104451607. This is a finite numerical stress test, not a numerical proof of the diamond theorem. Nontrivial outer-code correctness remains governed by the separate reviewed exact algebra and direct-circuit checks; this small correlated fixture does not pretend to implement a length5 GF(2) code.

## 6. Calibration extensions and exclusions
V1 route (a): if actual controls differ in total adaptive-instrument half diamond by Delta, the triangle inequality gives distance at most epsilon_NB+Delta from the IDEAL protocol's id_U tensor B_acc. Arbitrary coherent actual control faults can destroy exact branch factorization. One must not assert that the actual accepted map still defines the same or any memory-only filter, nor silently identify actual acceptance with the ideal filter's acceptance.

V1 route (b): if services retain exact Pauli instruments, tests are independent prepared probes with a uniform all-memory allowance, and endpoint outer processing remains the stated Clifford/Pauli circuit, the modified product-input hazard bound holds for every sigma. The aggregate effect argument therefore transfers with epsilon_NB replaced by epsilon_NB+sum_r s C eta_r (clipped at one if useful). Test memory updates need not match service updates. Finite favourable calibration samples alone do not establish the required all-memory inequality.

Role/edge/sign/key privacy through each call, same source map apart from declared quantum input, endpoint buffers, paid seed/routing/readout error, no uncontrolled access to R, finite cap and absence of guaranteed availability all remain as before. A payload-dependent replacement decoder or a late disclosed key requires new analysis. No generic composable-authentication novelty or superiority is accepted.
