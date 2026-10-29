# Correlated block certification with an explicit fixed distillation code

28 October 2026. **New scoped derivation/instantiation, not an invention of entanglement distillation, QKD, or adversarial sampling. Independent review pending.** This is a stronger conventional alternative to private-terminal decoder learning. No simulated or laboratory acquisition is claimed in this note; the program evaluates exact finite combinatorics and code algebra.

## Operational question and supplied interfaces

Can an arbitrary block of outputs from actual noisy encoder/storage/recovery arms be turned into a certified resource for a later unknown input, without predicting the environment or reconstructing a channel? Yes, conditionally, by paying for stored bipartite qubits and fixed local distillation. This differs from sending a fresh unknown input through an acquired receiver. It never promises nonzero yield for every source.

Let A and B hold N labelled qubit pairs in an arbitrary joint state rho_(A^N B^N E), possibly produced by an adaptive retained-memory source, correlated across every pair and with E. Candidate pair preparation, transmission and all earlier noisy controls can be arbitrary: perfect Bell preparation is NOT a premise of soundness. Both endpoints must possess the advertised qubit registers and calibrated local axes. All N pairs are isolated from E before the following private random test selection. Subsequent storage/control/test faults must have one declared whole-protocol operational discrepancy nu from the ideal protocol below; arbitrary further interaction of E with the pairs is not allowed for free. No source reset, iid source, microscopic bath model, or source memory dimension is required.

For every pair perform a fresh bilateral Pauli twirl, P* on A and P on B, uniformly over I,X,Y,Z. Retire the keys from the output/evaluator interface. Independent twirling gives exactly

    rho' = sum_e |Phi_e><Phi_e| tensor tau_e,

where e is a length-N Pauli string, tau_e>=0, and sum_e Tr tau_e=1. This is Bell-basis dephasing: the bilateral Pauli characters are distinct for distinct Bell labels. The environment can keep all classical/quantum correlations in tau_e. The twirl is an actual physical randomization, not an assertion that unknown errors were Pauli. A retained-key version is a different interface and does not inherit the diagonalization argument.

Select a uniform subset of m pairs, AFTER isolation; retain n=N-m pairs. On each sacrificed pair independently select X,Y,Z uniformly. Locally measure that axis on both halves and compare parity with the corresponding ideal Phi+ parity (+1,-1,+1 respectively). A nonidentity Bell label fails exactly two axes, so failure probability is 2/3; an identity label never fails. Keep all outcomes, including mismatches. Accept iff total failures F<=c. This costs 2m local one-qubit measurements, m axis choices, classical communication and pair storage until subset selection. A finite bounded sampler may use rejection with a separately charged exhaustion probability; exact combinatorics below is for ideal uniform choices.

## Exact worst-case bad acceptance bound

A fixed Bell string has weight w. Its sample error count H has probability

    Pr(H=h)=C(m,h) C(n,w-h)/C(N,w).

Given H=h, independent uniform axes give F~Binomial(h,2/3). Hence, if a code corrects every Pauli error of weight at most t on the n retained pairs,

    beta(n,m,t,c) = max_(w=t+1,...,N)
       sum_(h=max(0,w-n))^min(m,w-t-1)
       C(m,h) C(n,w-h)/C(N,w)
       sum_(j=0)^min(c,h) C(h,j) 2^j/3^h.             (1)

For EVERY initial rho, the probability of accepting while the retained Bell label has weight greater than t is at most beta. Conditioning on an arbitrary retained environment is unnecessary: (1) holds for each e and mixtures preserve it. This bound is exact for the classical event because a fixed-weight Bell string attaining the maximum is admissible. It is not necessarily a sharp bound on actual decoding error: some weight>t errors are harmless.

All terms are rational. `exact_block_test_v1.py` computes them with integer binomial coefficients and Fraction arithmetic, not floating tail approximations.

## Explicit standard code rather than a capacity-existence oracle

Use the twice-concatenated standard five-qubit code, [[25,1,9]], so n=25 and t=4. The base generators are XZZXI, IXZZX, XIXZZ, ZXIXZ, with logical X=XXXXX and Z=ZZZZZ. The 25-qubit generators are the twenty inner generators plus the four outer generators with X/Z replaced by inner logical X/Z. The program verifies commutation and rank24. Exhaustive enumeration of all1024 base Paulis verifies base distance3.

Distance9 follows directly: a concatenated normalizer commutes with each inner stabilizer. Each block therefore acts as an inner stabilizer or a logical Pauli; each nontrivial logical block has weight at least3. For an overall nontrivial logical operator, the induced outer logical Pauli lies in the outer normalizer outside its stabilizer and has at least3 nontrivial blocks. Total weight is at least9. Equality is attained by lifting a weight3 outer logical through weight3 inner logicals.

An EXPLICIT finite decoder enumerates all1,089,526 Pauli candidates of weight0 through4 in a fixed order, computes each24-bit syndrome, and returns the first matching correction. If no candidate matches, it returns identity, so the decoder is total and does not discard unfavorable records. Two candidates sharing syndrome differ by a weight<=8 normalizer, which by distance9 is a stabilizer; thus any candidate is correct on the promised set. This may be computationally expensive, but no unknown channel or recovery oracle is assumed. A recursive minimum-weight-at-each-level decoder is NOT substituted: it need not correct every weight4 error.

Standard bilateral stabilizer distillation supplies the physical operation: each side measures the24 code checks, compares the syndrome records, applies the explicit correction on B, and decodes the remaining logical subsystem. A's random code syndrome is mapped to the standard sector on both sides before decoding. For all weight<=4 labels this outputs Phi+ exactly, regardless of the environment state. An implementation can synthesize a Clifford encoder/decoder by symplectic elimination; this note has NOT supplied a gate-level verified noisy25-qubit implementation. The check list alone requires160 controlled-Pauli interactions per side (twenty weight4 plus four weight20 checks),24 local check preparations/measurements per side, plus sector correction, decoding and routing. The numerical sample certificate does not make those controls ideal.

## Actual delivered guarantee and heralding

Let p_acc be acceptance probability and omega_acc the subnormalized accepted output Bell pair. Let tau_acc be the corresponding subnormalized retained environment state, including public records but excluding retired twirl keys. On the good accepted labels distillation is exact and decouples the logical Bell pair. The bad accepted mass is at most beta. Therefore

    (1/2)||omega_acc - Phi+ tensor tau_acc||_1 <= beta. (2)

With whole-process implementation discrepancy nu, one can compare the actual accepted instrument to the ideal accepted Bell/reject instrument within beta+nu, using its matching ideal success probability/reference state. Care is needed if replacing that reference by actual acceptance probabilities; that replacement can incur another nu. Do not silently divide by an assumed success probability.

Under ideal local operations and conditioned on success, (2) gives error at most beta/p_acc. It is NOT a conditional beta guarantee. An unknown input supplied only after acceptance can be teleported through the distilled pair, using one actual Bell measurement, two classical bits and physical Pauli correction. Contractivity gives the same success-weighted reference-complete error beta. No long prior storage of that unknown input is needed. Its final Bell measurement/correction errors must be paid in nu. Repeating until success requires a separate availability/yield bound and has no guaranteed finite cap under arbitrary source memory; a fixed cap can abort and keeps its actual abort probability.

## Exact concrete instance and yield diagnostic

For n25,m100,t4,c0, (1) gives beta=97106/217474455 = .0004465168104456222, attained by total Bell weight7. Thus125 arbitrary correlated pairs can yield one certified accepted Bell pair at this success-weighted level, under the explicit trusted local-processing contract. No channel tomography is performed.

For an iid Pauli-error source of rate.01 ONLY AS A YIELD DIAGNOSTIC, acceptance is (1-2*.01/3)^100 = .51227237. The retained weight>4 probability is4.49596e-6. These are not assumptions of soundness or evidence for the actual Astra noisy-arm source. Initial125 pair creation and all stored halves must be charged; this is a very low rate and a larger quantum-memory/control bill than a single-carrier receiver.

Increasing sacrificed pairs to200 gives beta529/21489156≈2.46171e-5;500 gives≈3.65794e-7. At fixed physical error rate acceptance then falls, so tighter soundness is not automatically a practical advantage.

## Relation to Astra and conventional work

Astra N1161/62/63 use private roles and actual probe occupations for online recovery; their comparators are not another controller's counterfactual memory trajectory. This construction instead certifies a finite already-held block and uses an explicit fixed correction code. No online comparator or unknown memory reconstruction is involved. It does NOT instantiate their claims or remove their own storage/privacy premises.

Bennett, DiVincenzo, Smolin and Wootters, *Mixed State Entanglement and Quantum Error Correction*, quant-ph/9604024v2, establishes distillation/QECC connections, bilateral operations and finite-block codes. Primary full text inspected: https://arxiv.org/html/quant-ph/9604024v2 . This construction uses established operations, not a new general distillation principle.

Pfister et al., *Capacity estimation and verification of quantum channels with arbitrarily correlated errors*, Nature Communications9,27(2018), https://pmc.ncbi.nlm.nih.gov/articles/PMC5750239/ , explicitly supplies no-iid capacity estimation/verification from limited measurements. Its capacity lower bound concerns the best possible code; it is not a supplied learned executable decoder. No theorem or typicality parameter from that paper is imported here; (1) is independently derived for the fixed executable-code interface.

The strongest equally informed conventional alternative is this very sampling-plus-distillation pipeline (or more efficient modern distillation/code designs), not full environment tomography. Thus 'unknown noise without environment reconstruction' alone is not an Astra novelty claim. The genuinely unfinished bridge is a noisy, timed, resource-complete local distillation/teleportation operation with useful yield and quality using the actually available controller. Current five-qubit-arm simulations can generate candidate pairs, but their controls do not automatically certify the much larger two-sided distillation circuit. Readout/timing/storage and retained-key scope remain load-bearing.

## Candidate learned frames and control validation

Previously acquired local frame inverses or noisy code arms may be used to generate the125 candidate pairs. Their correctness is not assumed by (1): all their errors belong to the arbitrary pre-test rho. Thus this finite-block interface does not need to extrapolate a calibration estimate to a later bath state. A malicious source can still force rejection. Selecting the test subset only after isolation also avoids revealing TEST versus retained roles during source interactions. This is a resource substitution, not a free removal of privacy costs: the pairs must remain accessible and isolated, and the later controlled tests/distillation must be trusted to the stated nu.

`operation_checks_v1.py` independently implements the bilateral stabilizer maps for the base five-qubit code on all16 correctable Bell labels and all16 Alice syndrome sectors. It checks256 branches and obtains the correct Bell output to1.2e-16 entry/trace tolerance. It also checks bilateral twirling on a generic joint pair/environment state. These are ordinary floating matrix sanity checks, not an interval-certified25-qubit controller or sampled acquisition.

The soundness/yield tradeoff cannot be hidden. At fixed nonzero iid error rate, zero-failure acceptance decays exponentially with the number of sacrificed pairs. Arbitrarily small beta obtained by simply increasing m does not imply useful throughput. Allowing more failures can raise yield, but a fixed finite25-qubit code retains a real probability of an uncorrectable output pattern. Scaling the code, its decoder and noisy local circuit is the hard practical obligation.
