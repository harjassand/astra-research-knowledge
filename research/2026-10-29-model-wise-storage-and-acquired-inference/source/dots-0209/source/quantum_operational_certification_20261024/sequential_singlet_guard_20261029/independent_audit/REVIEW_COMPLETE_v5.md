# Independent review: complete grouped finite instance v5
2026-10-29 UTC. Reviewer: `review_current_channel_symmetry`.
Disposition: **accepted as a reproducible finite mathematical/source-generator fixture and valid grouping composition**, not as hardware evidence or an equal-resource advantage. The ideal guard theorem and operational/key/control boundaries remain governed by the preceding receipts.

Sources, dependencies and checks are hash-bound in RECEIPT_COMPLETE_v5.json. The complete author program reproduces its stored JSON byte for byte. New independent checks are in check_complete_instance.py/.json. They reuse the declared acquired frame/source generators and reviewed field decoder, but independently form the physical signed preparation maps, propagate a differently organized matrix-state DP, and construct grouped binary/field errors.

## 1. Alphabet mismatch is correctly resolved
The n=4 full singlet inner code carries one qubit, so it cannot itself be a GF(32) symbol or support a length31 code over GF(2). V5 does not claim that. It groups five consecutive serviced qubit coordinates into each GF(32) symbol. A nonidentity pattern on at most six inner coordinates touches at most six grouped symbols. The [[31,7,13]]_32 code therefore corrects it, regardless of entanglement and correlations between all 155 service positions. Independent logical-qubit pads suffice: their tensor Pauli group is the q-ary Pauli group after fixing the binary field/trace convention.

In polynomial coordinates, X labels are the corresponding field coefficients. Z labels must use the trace-dual basis; otherwise the stabilizer syndromes generally change. The implementation explicitly computes that dual basis. Our independent check exhausts all 5x32 trace-pairing identities. It then independently forms grouped errors and invokes the actual total decoder on 36 additional patterns: spread errors, random errors through six inner positions, and clustered errors on six outer symbols containing up to 30 inner faults. All decode correctly. The latter illustrate that the <=6-inner-fault event is sufficient but not necessary; the NB bad-count bound can be conservative.

The guard stopping count is 155 services, whereas the outer code length is31 and payload is7 field symbols=35 qubits. These are kept distinct throughout. The product/correlated-input arguments still apply after this grouping because every service label is a one-qubit Pauli and every grouped pattern is a q-ary Pauli. No reset, iid error distribution, or latent-label access is introduced.

## 2. Exact bound and domain
For the specified n=4 full singlet code the exact witness coefficient is3. Declaring the weaker C=6 is valid. With s=1/7, a=6/7, b=0,t=6, the declared hazard ratio is1 and the accepted-subnormalized bound is exactly 2^(-7)=1/128=0.0078125. The finite cap1400 only censors paths, so does not invalidate the bound. This controls accepted bad mass without dividing by acceptance probability.

As an optional mathematical observation, the unchanged ideal instance also permits C=3, giving ratio1/2 and bound3^(-7)=1/2187. The author reports the valid conservative bound instead. Extra coefficient slack is NOT by itself a proved physical-control error allowance: any real control error still needs the reviewed complete-instrument or uniform-effect accounting. No claim of optimal parameter choice is accepted.

## 3. Acquired frame and physical test inputs
The old seeded acquisition program's final finite-data bank—not its exact-operator diagnostic—selects VH and EH. Reading its dataflow confirms that exact transfer matrices/gaps are used for diagnostic reporting, not to replace the finite bank in the chosen frame. The final bank count81*100000=8,100,000 and all finite-bank count81*(1000+10000+100000)=8,991,000 are correct. This is replayed simulated acquisition under the earlier source family, not hardware calibration of a wholly unknown source. The guard's theorem does not assume that family; the fixture's high yield reflects a source sharing the planted local frame.

The author's source simulator writes its ideal test density using projected singlet-sector matrices. To ensure this is not an extra preparation oracle, our independent check explicitly prepares the n=4 minus product-singlet branch and plus four-qubit seed for every selected pair, applies the acquired frame, runs the actual declared source unitary, and performs final sign measurement with carrier discard. The four pass/fail memory superoperators for good/burst source match the author's projected formulas with norm residual below1.4e-16. Thus the previously reviewed physical branch construction realizes these simulator inputs.

The burst is appended physical lab Z on calls500..511 of the guarded sequence, independent of current role. The same declared joint source map is used in service and test calls at each index. It is a predeclared model violation, not a conditional swap to a more convenient source based on the hidden role. No bath reset is inserted between calls.

## 4. Independent DP and execution reproduction
The original DP correctly shifts good and bad service counts, saturates the bad-count bucket at7, accepts at155 services, immediately absorbs test failures (b=0), and adds surviving mass to cap abort. Expected call count sums active mass before each call. These are unnormalized 2x2 memory-state updates, not a stationary or iid replacement. Test and service memory maps need not commute.

The independent implementation reverses count-axis order, keeps explicit memory matrix indices, uses a separate terminal service bucket, and propagates all1400 calls. Results:

- Good source: acceptance0.9474587156989888; accepted >6-fault mass9.6887650e-17; cap abort0.00015494421246324032; expected calls1056.1399867441721.
- Predeclared burst: acceptance0.016720408680195673; accepted >6-fault mass1.243974380093553e-5; cap abort2.245697296529371e-6; expected calls505.89268538919134.

The largest difference from author outputs over these compared fields is4.55e-13. Those are floating-point reproductions, not interval-certified probabilities. The tiny good-source bad mass should not be marketed as experimental error suppression at that precision.

The author's 1000-trajectory samples and selected actual nonzero-ledger decoder calls also reproduce. They are a supplementary code-wiring/finite-sampling check, not evidence that unsampled bad events do not exist. The independent DP and exact theorem, rather than Monte Carlo absence, support the stated source-specific and universal bounds respectively.

## 5. Genuine controls and remaining scope
This is a source-generator simulation: the numerical evaluator knows the joint U and latent Pauli CP instruments, but the proposed physical protocol uses only private role/key/setting choices, prepared tests, observed sign failures and final code syndromes. No physical bath measurement, latent fault-label readout, or implemented bath tomography is supplied or needed by the proposed protocol. Full 32^31-dimensional outer amplitudes are not simulated; exact field/Clifford-label correction is the validated alternative.

The outer encoder is invoked once on35 input qubits with120 initialized ancillary qubits;155 encoded qubits are held/processed. Inner encoding/TP decoding is actually required for every serviced coordinate. Up to155 trusted logical buffer qubits must be protected over the capped operation. Outer Clifford gates and classical BW decoding, all native storage durations, four-qubit inner controls, signed seed preparation, routing/padding, readout, private randomness and permanent key retirement remain paid. Neither the simulation nor a good witness supplies a physical endpoint-memory threshold.

The burst strongly lowers availability: acceptance is only about1.67%. Its normalized universal accepted error cannot be declared0.0078125. The source-specific bad-mass/acceptance ratio is a generator-dependent illustrative upper bound; the theorem-level postselected bound requires division by the relevant success probability. Initial correlated memory requires the separately reviewed memory-filter ideal, not a scalar acceptance claim.

The8.991-million-call simulated learner dominates the1400-call guarded operation and has not been shown advantageous over strong conventional estimation/authentication/QEC alternatives. This fixture supplies a coherent finite end-to-end wiring and cost example, not a practical advantage, hardware breakthrough or generic unknown-noise solver.
