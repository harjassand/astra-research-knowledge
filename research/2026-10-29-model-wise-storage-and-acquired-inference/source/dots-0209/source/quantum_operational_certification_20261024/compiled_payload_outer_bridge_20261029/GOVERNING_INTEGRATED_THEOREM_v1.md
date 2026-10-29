# Compiled unknown-algebra payload protection with an actual finite outer code
2026-10-29. New integrated theorem; frozen for substantive independent review after finite programs below. No historical novelty, hardware threshold, generic unknown-noise capacity, or free remote Bell-access claim.

## 1. Input contract and conclusion
Fix n and known1<=k0<=n, g=n-k0, m=2g. Every source call acts on n selected qubits and arbitrary retained source memory. At every actual history its JOINT source Kraus operators have Pauli support in the same unknown subspace S*⊆F_2^(2n), whose symplectic cost a*+b*<=g. The source may be coherent, time-varying and retain arbitrary memory. Trusted controller operations, fresh randomness, isolated quantum registers, and a joint Bell-probe interface are supplied. Source access to reference registers, future payloads, retired keys or other control side channels is excluded. Unknown noise during trusted controls is not silently included in the source-call model.

Under this contract the construction below transmits a fixed K-qubit payload through finitely many actual service calls, using an explicit Clifford inner compiler, actual private pads, a finite CSS/GRS outer encoder and a total polynomial-time syndrome decoder. For any payload including an arbitrary external reference, initially independent of source memory, its averaged reduced channel has half-diamond error at most

  epsilon_fault + delta_cap + eta_control.

Here epsilon_fault is an explicit negative-binomial tail, delta_cap is a charged finite call-budget failure, and eta_control is the sum of implementation error allowances. The source need not excite every hidden generator, and no environment/process tomography or iid reset is assumed. All statements concern the defined trusted controller/channel-query interface.

## 2. Grouping and fixed register typing
Choose B>=8, t with0<=4t<B, and set

  h=ceil(log2 B), u=max(1,ceil(h/k0)), s=floor(u*k0/h),
  J=uB, ell=B-4t, K=s*h*ell.

Group consecutive service slots in batches of u. Each group contains u*k0 logical physical slots. Pack s h-qubit symbols into the firsts*h slots and fill the fewer thanh leftover slots with known fresh filler qubits. Across the B groups, these form s stripes, each with B symbols over GF(2^h). A fixed reversible permutation performs packing/unpacking; it does not depend on unknown errors. During acquisition, probe calls do not advance the service-slot pointer; service calls advance it by exactlyk0 slots.

The payload consists ofs*ell symbols. For each stripe prepare2t zero ancilla symbols before and2t zero symbols after the ell payload symbols, then apply the direct encoder in Section3. Pack the encoded symbols into the J service slots. After all slots return, unpack and discard filler bits before outer decoding.

A nonidentity Pauli on one service slot can affect only its own group, possibly several stripes in that group. Therefore<=t bad service slots imply<=t bad groups and<=t erroneous symbols in EACH stripe, without any union factor in s or multiplicative factor u. No independence between stripes/groups is assumed.

For x=u*k0/h>=1, floor(x)>=x/2, so

  s*h/u >= k0/2.                                         (2.1)

This resolves the small-k0 field-size problem without an exponentially large field: 2^h is betweenB and2B and all field construction is polynomialB.

## 3. Actual direct CSS/GRS encoding and decoding
This section transfers the received explicit GRS construction to direct arbitrary-payload encoding; it is not merely an invocation of a hypothetical outer corrector.

Over GF(2^h), take B distinct elements a_i and multipliers v_i with

  v_i²=[product_{j≠i}(a_i-a_j)]^{-1}.

Let C=GRS_(B-2t)(a,v). The first2t weighted Vandermonde rows form H=C^perp, contained in C; the remaining B-4t rows form L. Extend with2t coordinate rows R so that the B×B matrix T=[H;L;R] is invertible and H R^T is invertible. These are explicit finite field operations. The received proof gives the CSS code [[B,B-4t,2t+1]]_(2^h).

For row-coordinate field strings, define Lin(T)|x>=|xT> and the trace Fourier F|x>=2^(-h/2)sum_y(-1)^Tr(xy)|y>. The actual encoder is

  U_enc=Lin(T)(F on first2t symbols),

on |0>^(2t) tensor arbitrary ell-symbol payload tensor |0>^(2t). Its inverse is the actual outer decoding unitary. Lin(T) compiles through field-coordinate Gaussian elimination into CNOT/SWAP gates; F compiles into h Hadamards followed by the inverse binary trace-Gram basis change. The field modulus is found by enumerating and testing at mostB candidate degree-h binary polynomials. No dense2^(Bh) matrix, free Fourier transform, nearest-codeword oracle or exponentially long syndrome table is assumed.

For a physical stripe error X(e)Z(f), direct inverse encoding gives

  e'=e T^(-1), f'=f T^T,

followed by swapping X/Z labels on the first2t symbols due to F. Measuring the first and last2t decoded symbols in the computational basis yields d_first,d_last. Their ideal values were zero, so these **actual single-system measurements**, not Alice/Bob outcome differences, give

  sigma_f=d_first=Hf,
  sigma_e=(H R^T)d_last=He.

Use the received total Berlekamp-Welch syndrome decoder separately on these two syndromes. It returns correct e_hat,f_hat for all errors supported on at mostt sites; outside that radius it still returns a defined correction/failure flag with no postselection. Propagate the inferred error through U_enc† and undo its middle ell-symbol Pauli. For every weight<=t Pauli error, the middle logical operator is precisely cancelled. Ancilla measurements cannot reveal or alter the arbitrary logical payload: after Clifford conjugation, the error is a tensor product of ancilla Paulis and a logical Pauli. Thus this is an actual arbitrary-state quantum decoder, not solely an entanglement-fidelity test on one input.

Binary Z labels from k0-qubit service blocks are converted to field Z(f) by the nonsingular trace-Gram map: z_j=Tr(f alpha_j). This conversion is included in the finite tests; identifying binary Z bits directly with f coefficients without this map would in general be wrong.

Per stripe the encoder/decoder uses O(B²h²) elementary Clifford gates; finite field Gaussian/Berlekamp-Welch processing is polynomialB,h. There are s stripes. Outer storage is O(J*k0) qubits plus workspace. These are ideal operation counts; accurate physical control/storage must be supplied or separately fault-tolerantly implemented.

## 4. Actual inner service/probe process
Before each call compile the span S_t of actual earlier physical-frame Bell probe labels using the accepted binary symplectic algorithm. Cost monotonicity and S_t⊆S* ensure at leastk0 logical qubits; pad gauge to exactlyg. The gate list C_t is explicit. On a probe, prepare n fresh Bell pairs, apply C_t to source halves, make the source call, apply C_t* to retained reference halves, and Bell-measure to obtain the physical-frame label.

On a service, take the nextk0 logical slots of the already outer-encoded payload; prepare independent gauge I/2^g; choose a fresh private logical Pauli pad; apply pad then C_t, make the source call, apply C_t†, discard gauge, undo pad, retire the key, and isolate returned logical slots. The current service/probe role is a private Bernoulli coin with service probability q; it must be chosen before actual payload loading, with no side channel. The source-facing input is maximally mixed and decoupled from source memory in both roles. Gauge preparation records/purifications and logical pad keys remain unavailable to source throughout the execution.

The accepted private-pad lemma gives the EXACT joint logical-memory instrument

  rho_LM -> sum_(r,v) [P_l(v) tensor A_rv] rho_LM
                              [P_l(v)† tensor A_rv†].

It holds even for correlated inputs. For a complete fresh outer payload initially independent of source memory, conditioning latent Pauli/Kraus branches preserves a tensor product of a definite payload-Pauli history and a source-memory state. Consequently the full logical stream is an input-independent correlated Pauli channel. Future actual controls depend only on actual probe records, not latent service labels. This supplies a genuine operational error-pattern model, rather than a Pauli approximation to coherent memory.

The accepted two-stream coupling implies that the total numberF of faulty service blocks is stochastically dominated by NB(m,1-q), where m=2g and NB counts failures beforem probe successes. Hence

  Pr(F>t) <= beta(m,t,q)
   :=Pr[Binomial(m+t,1-q)<=m-1].                          (4.1)

For m=0 definebeta=0. The source label process need not be iid, stationary or bounded away from zero excitation. Only the private role coins are iid. The exact common-algebra promise and source blindness to current role are load-bearing.

## 5. Integrated error bound and finite stopping
Run until J=uB services or a fixed call cap L. On cap failure discard/replace the unprocessed output with a fixed correctly sized fallback and return an actual K-qubit output; no conditioning on success is allowed. Choose

  Lq >= max(2J,8 ln(1/delta_cap)).

The probability of fewer thanJ services by L is at mostdelta_cap by the standard binomial lower-tail bound. The uncapped mean number of calls is J/q; capping cannot increase it. Each service slot is processed exactly once on successful acquisition.

On every latent Pauli pattern with<=t bad service slots, the grouping rule and actual decoder of Sections2–3 return the exact entire K-qubit payload, including its external reference. All other patterns remain CPTP branches. Their weights are input-independent. Thus the reduced decoded channel is a mixture of identity and a CPTP bad branch with bad probability at mostbeta(m,t,q)+delta_cap. It follows directly that

  (1/2)||Decoded-Id_K||_diamond <= beta(m,t,q)+delta_cap.

No dimension factor and no fidelity-to-square-root conversion is used. Adding implementation half-diamond error allowances by telescoping gives eta_control. Retired randomization/outcome records and inaccessible source purification are not added to this linear-error target without separate analysis.

## 6. Explicit constant-rate finite parameters
Take q=1/2 and t=floor(B/8). It suffices that

  B >= max(24m+8,128 ln(1/epsilon_fault)+8).

Then t>=3m and m+t>=16 ln(1/epsilon_fault). The binomial mean in(4.1) is(m+t)/2, at least2m and8 ln(1/epsilon_fault), so beta<=epsilon_fault. Also ell/B>=1/2. Combining with(2.1),

  K/[n*(J/q)]
    = q*(s*h/(u*n))*(1-4t/B) >= k0/(8n).                (6.1)

This is the normalized rate with respect to the **expected source-call upper bound J/q**, countingn physical input qubits per source call, including probes. The deterministic worst-case cap rate is K/(nL), which is generally smaller and is reported separately in the budget program. This distinction must not be dropped. For each prescribed finite error target all calls, registers and outputs are finitely typed, and all compilation/decoding costs are polynomial in their sizes. The theorem is conditional on the stated controller interface, not a hardware throughput assertion.

## 7. Paid remote Bell acquisition: a separate resource-mode corollary
For spatially separated sender/receiver, joint probe Bell measurement is not free LOCC. Use the separately accepted unkeyed-resource service and deferred final-Bell-statistics NB theorem, rather than importing the direct-payload secret-key interface without payment. Supply a trusted preshared entanglement seed. Each probe consumesn seed ebits to teleport the retained reference to the receiver after the source call; local Bell measurement then obtains the label, which is fed back classically. Actual service references stay at the sender. Apply the received twirl-free outer GRS distillation to the grouped/striped J services, producingK output ebits with error beta plus budget failure. The corrected-span effect E>=P_good handles coherent resource states; they are not asserted Pauli-diagonal.

Let r=1-q<=1/4. Stop at J services or P probes, with

  P>=max(4rJ,6 ln(1/delta_seed)).

Supply exactlynP seed ebits. There are at mostJ+P source calls. A binomial coupling bounds the abort probability by exp(-P/6)<=delta_seed. Net entanglement output is conservatively K-nP; unused seed is not counted in this lower bound. Negative values are not hidden.

For a sequence with t/B->0, r->0 and packing efficiency(s*h)/(u*k0)->1, the capped normalized net rate

  (K-nP)/(n(J+P))

approachesk0/n (for fixedn,k0). For example choose r on order sqrt((m+log(1/epsilon_fault))/B), choose t from the exact NB quantile, and letB grow. With fixedk0, h grows and u=ceil(h/k0), so packing efficiency tends1. Rate-approach formulas in terms of total service count J must retain the grouping factor u; writing a universal sqrt(1/J) approach while silently settingB=J would be incorrect for smallk0. This is explicitly seeded, feedback-assisted entanglement generation, NOT an unassisted channel-capacity theorem. No bootstrap from noisy uncertified service resources is justified. Direct remote payload mode additionally needs protected key delivery or separately justified end-of-execution key revelation after source retirement.

## 8. Evidence, dependencies and nonclaims
- `direct_outer_checks_v1.py/.json`: emits actual Hadamard/CNOT/SWAP encoder and inverse-decoder lists, checks exact binary Clifford vs finite-field Pauli formulas, actual computational ancilla syndromes, and arbitrary logical-Pauli preservation. Cases coverk0 below/aboveh, grouping, multiple stripes and discarded padding. There are1000 correlated stripe-error/direct-logical checks. These are exact Boolean/finite-field calculations, not noisy hardware or an exponential density-matrix simulation.
- `integrated_budget_v1.py/.json`: uses exact integer NB-tail comparisons, finite cap budgets, grouping and rate checks. A conservative integer upper bound on ln is used for executable sufficient sizes. Large budget cases do NOT construct the corresponding large circuit matrices.
- Inner compiler and instrument dependencies: learned_pauli_algebra_compiler_20261029/{compiled_frame_api_v2.py,PRIVATE_PAD_PAYLOAD_INSTRUMENT_v1.md,NEGATIVE_BINOMIAL_FAULT_TAIL_v1.md,OPPORTUNITY_STREAM_COUPLING_v1.md} and their independent operational receipts.
- Actual outer algebra, field compiler and total decoder: outer_grs_distillation_20261028/{GOVERNING_WRAPPER_v1.md,grs_wrapper_v1.py,check_field_and_gates_v1.py}, with received independent receipts. The direct-payload wiring above is new checking; received sources remain unmodified.
- Resource corollary additionally uses MIXED_ROLE_SERVICE_THEOREM_v1.md, DEFERRED_RESOURCE_FAULT_TAIL_v1.md and their separate receipts.

This closes the actual outer encoder/decoder and finite grouping obligation; it does not make the exact hidden-algebra promise empirically certifiable from finitely many nonexciting samples. Ordinary full-support weak bit-flip noise can leave no subsystem under this algebra criterion even while conventional QEC has positive rate. Unknown non-Clifford frames, out-of-algebra noise, faulty probes, continuously acting uncontrolled baths, and long-term physical storage are not solved. The LPN-scoped robust-selection obstruction and the closest conventional partial-noise/code-discovery literature remain governing comparison boundaries. Historical novelty of the complete combination has not been cleared.
