# Independent review: actual top-down quantum output decoder
30 October 2026. Scoped PASS under the frozen scheduled-computation-code receiving contract. This is an additional physical decoding construction, not acceptance of an autonomous implementation.

Reviewed TOP_DOWN_QUANTUM_OUTPUT_DECODER.md SHA256 b778a2bef677a1e1e84d181afda32ca6c59c085bb9be4b3863432fc3b867efd3.
Received foundation: producer-workspace/INDEPENDENT_REVIEW.md and its frozen sources/STANDARD_FT_SUPEROPERATOR_RECEIVING.md SHA256 751b5452f3bea9bbe31a9d833b569a144b45977d8503931c7f6dcc3aa37da7fc.
Independent supporting notes: CODE_AND_INTERTWINER_NOTES.md in this directory, SHA256 14a64f7cbf58bb737236e9729b4ae59b050288218c0a3832cb55eed0e1a4e183.

## 1. Genuine quantum decoder and arbitrary bad children
The finite coherent syndrome-recovery circuit followed by a unitary inverse stabilizer encoder is the correct replacement for a classical readout procedure. A fixed recovery for the entire correctable family satisfies the cross-term Knill–Laflamme identities, so syndrome garbage is independent of the recovered unknown logical state. The finite classical syndrome lookup can be compiled into actual reversible gates; it is not free software at runtime. All lookup/preparation/routing resources belong in the constant B.

An input upper-level sparse module can have arbitrarily malformed exceptional children. Consequently the initial child totalizing corrections are necessary. A mere claim that the upper code corrects d_c erroneous logical symbols would otherwise identify malformed physical children with logical symbols without a map. The manuscript explicitly performs physical child correction/identity refreshes and receives the frozen arbitrary-input totalization property. Their fault-good range is the lower code/sparse module, even on exceptional children; their logical action on correctly received children is identity.

With the same completed child analysis decoder used on every sparse operator support, the effective upper-symbol error is supported on at most d_c children, retaining arbitrary bath/garbage correlations. The clean upper recovery corrects the entire family, including its two-sided cross terms. Every actual lower-level rectangle implementing that circuit is required good. Hence the retained output child lies in the corresponding lower sparse module. The induction ends in an ACTUAL fault-free physical recovery/inverse-encoder circuit, not an ideal decoder appended to the final output.

The accepted local-contraction completion/rank-one marginal argument extends the deterministic physical-history assertion to arbitrary operator histories with bath coefficients. The same recovery is essential throughout. Classical-basis correctness or a decoder chosen separately for each support would not earn equation(2).

This conclusion is conditional on the imported totalizing correction and common quantum-module statement, not merely on gate spread. A gadget family lacking that property is not certified by this receipt.

## 2. Mixed-level inclusive counting
The selected child rectangles lie in distinct stage intervals and distinct output modules. They form a prefix-free family of disjoint physical location sets. Recursive threshold sieving therefore yields the product of their individual x_j strengths jointly, including a shared bath. Exact OR sieving over stage failures gives product_j(1+x_j)^B-1 per output, and a product of this majorant for any selected output set.

For x_j<=x_* r^(s^j), s>=2, the inequality s^j>=j+1 gives sum_j x_j<=x_0/(1-r). The claimed O(x_0) bound is uniform in depth, with fixed subthreshold margin (for example r<=r_0<1). This is a physical terminal error floor: increasing depth at fixed noise does not deliver an arbitrarily accurate exposed physical qubit. The manuscript states that limit correctly.

The joint computation/decoder inclusion also follows from their disjoint physical locations and one full expansion. Thus subtracting computation-bad sectors costs the factor 1+epsilon_comp, not conditioning by a positive probability. The cardinality sieve produces the displayed binomial output-support bound. On a known fixed target, all good ket/bra histories occupy the common target-error span. A genuine projector onto its complement annihilates their map; its actual nonnegative population is at most b_total. The resulting 2sqrt(b_total) gentle source bound is justified. For a full logical-channel distance instead, the usual good-part trace-defect factor is still required; a bad-map norm is not automatically the whole channel distance.

## 3. Costs and remaining interfaces
Every stage needs its initial refresh, all actual recovery/inverse-encoder gates, finite reset locations and waiting idles. B is a fixed constant only for a fixed computation code and fixed routing contract. All outputs must be synchronized to a common observation time to avoid an uncharged unencoded wait. The manuscript includes padding and terminal fault charging.

The geometric sum of stage sizes is O(A^l), so the decoder keeps the scheduled construction's polylogarithmic-in-L/epsilon overhead. When epsilon_comp is exponentially small in target length q, that overhead is polynomial in q rather than polylogarithmic in q. This correction is explicitly present. No favorable constants or practical threshold follow.

This gives a route to ordinary scheduled target-state preparation with physical quantum outputs whose low-density failures are corrected by an outer code. It does not supply the native apparatus's actual warm-input interface, unknown-state ingress, autonomous schedule, physical terminal detector qualification, or prolonged storage of exposed outputs.

## 4. Separate qubit-code candidate check
The odd-r concatenated Steane stabilizer space is doubly even, selforthogonal and has dimension(7^r-1)/2. Adding all-ones with one parity coordinate gives a Type-II selfdual extension for odd r. The recursive quantum distance is 3^r, so r=5 has length16807, distance243 and quantum correction radius121. A conservative composed procedure spread16 leaves a strict k=1 margin if the imported spread4 contract includes the actual totalizing correction.

Do NOT call its punctured classical code distance243: inner weight4 stabilizers remain, and for r>=2 its classical distance is4. The syndrome decoder must be justified modulo stabilizers. The independent notes give the needed argument: two weight<=121 representatives of the same syndrome differ by a normalizer of weight<243, hence by a stabilizer. Further circuit spread/range claims are received from the fixed procedure contract, not from this algebra alone.

The independent script check_steane_typeii.py verifies generator rank, double-evenness and selforthogonality for r=1,2,3, and the odd/even extension distinction; its JSON passes. This finite check is not the proof of r=5 distance or fault tolerance. The recursive algebra in the notes supplies the former.

Primary attribution boundary: Aharonov–Ben-Or, https://arxiv.org/html/quant-ph/9906129, supplies the computation-code framework and its stated procedures. Section4.9 permits classical-output garbage and is not used as a quantum-output theorem. The present top-down coherent circuit and mixed-level receiving proof are the additional construction audited here.
