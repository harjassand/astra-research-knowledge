# Acquisition-only certification of an accepted quantum operation
2026-10-29. New protocol and all-input proof, awaiting independent review. No separate matching-validation role is used. This is NOT postselection of an older accepted-error guarantee.

## 0. Mission and actual boundary
Use the finite fixed-clock FTPL acquisition controller, its actual product-probe records, a service with the CP/memory interface below and a verified outer quantum code correcting arbitrary errors on at most t of J native logical service slots. At the fixed-four-spin port each service carries one bare logical qubit through the paid four-spin encoder, current frame, complete source call, inverse controls and total decoder. It may use physical-permutation orbit randomization, but the cheaper bare-logical-Pauli version proved in section6 is sufficient and is the preferred fixed-port interpretation.

The source is an arbitrary causal joint data-memory CPTP process at the declared port. No common algebra/frame, low occupation gap, IID/reset source, low defect, or favorable noise promise is used for soundness. Fresh current roles, perturbations, candidates and keys must remain private from the pre-call source map; quantum response through that fixed map is allowed. Source access to unprocessed/returned payload registers, references, retired keys or decoder trash is excluded. Controls, storage, fixed clock and SPAM remain trusted or separately quantitatively budgeted.

The conclusion concerns the ACCEPTED subnormalized quantum instrument. The source may always force rejection. No quantum-capacity or practical-cost advantage is claimed. The conventional adaptive full-path alternative remains a serious comparator.

## 1. Two-role finite operation, with actual data-only acceptance
Fix p+s=1 with p>0,s>0, finite call cap T, and target J services. Every active round runs the always-output fixed-budget candidate solver BEFORE the private role. It records its actual rational candidate gap e_it, using a sound lower bound never below the trivial coefficient-l1 bound. Neutral preflight caps are ordered as in the reviewed schedule; a preflight resource abort rejects.

- LEARN, probability p: use the genuine product-Pauli input/readout bank. Update each35-coefficient feedback vector g_it and the shared probe counter. The unknown payload is not used in this call.
- SERVICE, probability s: process the next native outer-code slot through the declared randomized service. No loss feedback update occurs. Retire its physical-permutation or logical-Pauli key.

There is NO matching-validation role or validation failure count. Stop source calls upon J completed services or the cap. A resource/code-generation failure rejects. If fewer than J services completed, reject. Otherwise compute a retrospective rational candidate tuple qhat from the actual final feedback bank using any paid finite classical method, including an always-certificate optimizer. A global empirical optimum is not assumed.

Evaluate the data-only bound below using ONLY actual probe records, certified solver gaps, declared public parameters and qhat. ACCEPT exactly when it is at most t; otherwise reject. On acceptance apply the specified TOTAL outer decoder. Outer decoder syndrome/ancilla/trash records are retired. The acceptance flag and specified coarse memory/history may be retained. The unknown payload may instead be supplied through the separately reviewed finite resource-first Bell wrapper, with its paid clean reference storage and teleportation requirements.

## 2. Required finer filtration — mathematical labels, not observed faults
For every service, after averaging/retiring its current physical-permutation key, the accepted orbit theorem gives

 S=id_slot tensor B_good+S_bad,
 S_bad*(I)=I_slot tensor H_bad,
 Tr_slot S_bad(rho)=B_bad(Tr_slot rho).

The good and bad terms are CP. Introduce their good/bad labels solely as a MATHEMATICAL refinement of the process; the actual controller never receives or uses those labels. Do NOT condition on the retired permutation key, which would undo the averaging behind this split.

Use a fine pre-call filtration containing actual earlier acquisition/controller history and these earlier virtual labels, plus neutral preflight count/success events before current accepted indices are revealed. It may condition the memory marginal differently from the coarse observed history. At each such fine history:

1. The next candidate perturbations/internal coins and role remain fresh and independent. The actual controller's weights are functions of a subset of this history and are therefore predictable.
2. A fresh sacrificial probe sees the current source with its FINE conditional memory marginal. Its bank remains unbiased for the corresponding conditional star losses. No source reset or replacement memory is introduced.
3. The actual service slot can be correlated with memory and the remaining outer block. The orbit bad-effect identity makes its bad probability depend ONLY on that same memory marginal, equal to the raw full-P Bell-loss effect.
4. The any-source Poincare transfer bounds that effect by alpha_n times the sum of current star losses, alpha_n=2^n/Catalan(n/2).

The fine conditional losses are proof quantities, not measured labels. Their numerical values need not equal coarse-history conditional losses. The high-probability proof must be rerun on this fine filtration; merely importing a coarse expectation bound would be insufficient. Fresh action/probe independence and all numerical bounds hold on the fine filtration with the SAME observed feedback/certificate counters.

## 3. Observable actual-loss upper bound on the fine filtration
Let m=n-1,d=35,L=720. Put B=(T-1)L/p+dR. Let Eobs=sum_(t,i)e_it and Vobs=sum_(t,i)||g_it||1², with0 values after stopping. Let ell_e,ell_m,ell_f be rational upper bounds on ln(1/delta_e),ln(1/delta_m),ln(1/delta_f), for declared failure allowances. Define

 Ubar_e=2Eobs+2mB ell_e,
 Hret=mdR/4+Vobs/(4R)
      +L sqrt[(mT/R)Ubar_e+m²dT²/M]
      +m(1+45/(2p))sqrt[2T ell_m].

The retrospective empirical score is

 Lemp(qhat)=3m N_probe/(4p)+(1/2)sum_i G_iT dot phi(qhat_i).

Every term is actual classical data or a declared parameter; rational upper square roots may be used. The accepted retrospective proof, applied afresh to the fine history of section2, gives with probability>=1-delta_e-delta_m

 sum_(t,i)delta_it^fine(C_it) <= Uret:=max(0,Lemp+Hret).  (1)

The pathwise step Phi(G_T)<=min_x G_T dot x<=G_T dot x(qhat) holds for every final data-selected candidate. No hindsight comparator is inserted into a martingale. The source promise is only the trusted/nonanticipating interface; it need not possess a good frame.

## 4. Virtual service-fault martingale and the acceptance threshold
Let V_t be the indicator of a SERVICE-bad virtual branch at call t,0 for other calls. Given the fine past and current candidate tuple, but before the independent role and retired permutation average,

 E[V_t|fine past,current candidates]
 <=s alpha_n sum_i delta_it^fine(C_it).

The binary martingale difference has conditional range1, so with probability>=1-delta_f,

 V:=sum_t V_t <=s alpha_n sum_(t,i)delta_it^fine(C_it)
                         +sqrt[(T/2)ell_f].             (2)

The protocol's NEW acceptance threshold is

             s alpha_n Uret +sqrt[(T/2)ell_f] <= t.      (ACQ-CERT)

On the simultaneous good events(1),(2), acceptance implies V<=t. Therefore, for EVERY initial joint payload-memory state and every permitted source process,

 Pr[ACCEPT and V>t] <=delta:=delta_e+delta_m+delta_f.     (3)

No service-shortage allowance is needed for this SOUNDNESS statement: incomplete blocks are rejected. Code-generation and neutral sampler failures likewise reject rather than create unchecked accepted branches. They matter for yield, not for increasing(3). Physical control errors require their own compositional budget.

## 5. From a uniform probability bound to an accepted quantum instrument
Fix the complete controller/source CPTP process and refine it by the virtual CP labels from section2. The event ACCEPT and V>t defines a CP trace-nonincreasing map A_bad. Equation(3) was proved for arbitrary initial joint payload-memory density operators with the same constants. Thus its effect obeys

 A_bad*(I)<=delta I,
 ||A_bad||diamond<=delta.

This is not an inference from one observed dataset or a single Choi fidelity. External references do not change the effect bound.

For each refined branch with V<=t, the combined joint Kraus operators act nontrivially on at most those t native service slots, tensored with memory operators. Interspersed probes act only on memory and fresh sacrificial registers. The verified outer corrector corrects the entire linear span of such errors, including coherent sums and input/source-memory correlations. Consequently the accepted good contribution factors as id_payload tensor B_good, at the actual coarse-memory/retired-trash boundary.

The orbit memory-marginal closure holds on every good/bad branch. Probe instruments and the classical data-dependent controller/acceptance rule compose CP maps on that memory. After tracing the payload and retiring decoder trash, it therefore also gives

 Tr_payload A_bad=B_bad composed with Tr_payload,
 B_acc=B_good+B_bad,
 A_acc=id_payload tensor B_good+A_bad.

Here B_acc is the ACTUAL accepted coarse-memory instrument, not a simulator chosen after observing success. Norms of A_bad and B_bad are both at mostdelta. Hence

 (1/2)||A_acc-id_payload tensor B_acc||diamond<=delta.  (4)

This is a fresh all-input proof for the new acceptance rule. It does NOT condition an older accepted guarantee on a new diagnostic. A normalized accepted error needs a separately justified positive acceptance probability, and correlated payload-memory inputs retain the instrument/filter interpretation.

## 6. Strong fixed-port baseline: bare logical Pauli pads suffice
At n=4, the full singlet sector has dimension d=2, equal to the logical code dimension K=2. The same acquisition-only theorem therefore does NOT require physical permutation SWAPs.

Let E embed this full singlet code. The canonical total reset decoder has Kraus operators D0=E† and D_r=|0><v_r| for an orthonormal complement basis {v_r}. For joint source Kraus K_a, the completed logical-channel Kraus operators are A_ar=(D_r tensor I)K_a(E tensor I). Their logical identity coefficients are B_ar=Tr_logical(A_ar)/2. The r=0 coefficient is exactly the raw full-P coefficient B_a,raw. Consequently the completed logical identity CP map is

 B_completed_good=B_raw_good+sum_(a,r>0) Ad_(B_ar),

and its memory effect dominates the raw good effect. Equivalently,

 H_completed_bad<=H_raw_bad<=8 sum_i E_i(C_i).

Actually apply a fresh uniform logical Pauli BEFORE the four-spin encoding and its inverse AFTER the total decoder; retire its two-bit key. Pauli character averaging gives the exact joint instrument sum_P Ad_P tensor B_P. It supplies the same identity-good CP branch, input-independent bad effect and branchwise memory-marginal closure needed in sections2–5. The fine virtual label is now identity versus nonidentity Pauli (or its refinement), never the retired pad key. Thus the entire acquisition-only proof applies with no physical permutations at this fixed port.

This is an explicit equally informed conventional implementation, not a claimed orbit-specific advantage. Permutation orbits remain useful for proper subcodes where the raw full-P transfer would otherwise incur localization penalties; that issue does not occur for this d=K=2 port. Pauli pads and endpoint encoder/decoder/control errors remain real paid operations.

## 7. Finite resource interpretation and honest limitations
For the accepted fixed-four-spin concatenated code, J=N=16h2^h native slots, payload=N/32 and t>=N/256. One possible role choice is p=1/3,s=2/3,T=3J, whose hypothetical role sequence has at least2J expected services. The nominal cap payload/source-qubit exposure ratio is1/384, CONDITIONAL on acceptance. This arithmetic is not a demonstrated throughput improvement: the observable certificate may be extremely conservative or never pass, and source/test/control/classical costs differ from conventional alternatives. Expected useful yield multiplies by actual acceptance probability, which is not lower bounded here.

The protocol uses the same product-probe acquisition records to learn AND certify the delivered accepted operation, with no fresh matching holdout. Its legitimacy comes from adaptive martingales and a data-only all-input CP-effect certificate, not from treating training data as independent validation. Solver gaps are sound exact certificates but may be large. Fixed-clock hardware, endpoint synthesis/calibration, trusted storage, private sampling, code verification, final empirical-candidate computation and retirement mechanisms remain paid. No historical novelty, practical advantage or unrestricted quantum-capacity claim is established.

## Dependency status
Observable fixed-comparator v1 has its independent receipt. Retrospective empirical-frame v2 has independent receipt observable_fixed_clock_gap_audit_20261029/retrospective/REVIEW_RECEIPT.json. THIS acquisition-only transfer and its cheap fixed-port service implementation are new load-bearing additions requiring their own receiving review. No older accepted proof is overwritten or silently broadened. The prior full-memory orbit and outer arbitrary-error compiler are inherited at their actual accepted scope.
