# Independent receiving review: disjoint scheduled fault tolerance
30 October 2026. Scope-frozen receipt by challenge_standard_ft_receiving.

## Verdict and frozen target

**PASS, with the common-decoder argument and resource qualifications below binding the scope.** No blocking counterexample was found. Reviewed source: `sources/STANDARD_FT_SUPEROPERATOR_RECEIVING.md`, SHA256 `751b5452f3bea9bbe31a9d833b569a144b45977d8503931c7f6dcc3aa37da7fc`.

This accepts the receiving of the separately accepted inclusive complete-norm law into the stated disjoint, fixed-schedule computation-code construction. It is not acceptance of an autonomous implementation, an arbitrary ingress/measurement interface, a numerical practical threshold, or historical novelty. The approximate-target/reset interface is accepted only through its own frozen receipt, SHA256 `42967299b02d9dee422b48d91b10afc8fbaf80790fd04f14907179e6cb9a775f`.

## Actual primary-source checks

Read the actual definitions and proofs in [Aharonov–Ben-Or, quant-ph/9906129](https://arxiv.org/html/quant-ph/9906129), not just its abstract or threshold headline. Definition 16 counts the spread of correction followed by the gate. Section 7.3 explicitly makes rectangles a nested partition. Definition 18 supplies the recursive sparse predicate. Lemma 8 uses **k ell <= d**, not a stronger missing inequality, and its proof includes correction of arbitrary incoming states into the code module. Section 7.2 requires redundant classical input and recursive-majority output. Lemma 9 requires 2d+1<=m. Section 8.3's particular signed-path reduction uses linear combinations of physical trace-preserving paths; that argument alone does not establish the new bath-coefficient claim. Section 9 requires an entropy-removal/preparation resource. No numerical threshold is imported.

The following is our additional receiving argument, not a quotation of a source theorem in a stronger norm.

## 1. One common decoder, including cross terms

There is a fixed recursive ideal recovery/decoder for the union of all admitted sparse operator supports, not a decoder selected after learning the fault path. At level one the entire weight-at-most-d error family satisfies the cross-term Knill–Laflamme condition. Recovery maps each error applied to the code into the unchanged logical system and an error-dependent syndrome vector. The decoder can be completed to a channel on the whole physical input space.

Inductively, take an error operator supported on an (r,d)-sparse set and expand it in a product operator basis across child blocks. In each product term all but at most d children have (r-1,d)-sparse support. Their fixed child decoders return the correct child logical systems and syndrome factors. The exceptional children induce arbitrary operators on at most d upper-level physical symbols and their garbage. Base-code recovery corrects these together, again retaining garbage. Linearity proves the assertion for arbitrary operators on the sparse set, including entangled operators and cross terms between different sparse sets. In particular, the decoder is common to the entire hierarchical sparse-error span; it need not determine the actual support.

Apply the deterministic sparse propagation invariant with this decoder at working-period boundaries, and before the physical classical de-encoding for the quantum-output version. A useful explicit extension from physical fault paths to unrestricted local operator histories is the following. Scale any local fault operator to a contraction and complete it to a trace-preserving channel with a complementary Kraus operator at the same location. For a prescribed sparse history, complete every local insertion this way. All resulting Kraus branches remain supported within that same sparse fault set. For each pure logical input the recovered logical output of the completed physical path is the ideal pure state. Every individual branch must therefore have that same logical factor, since a positive sum with rank-one marginal has no component outside that marginal's support. Linearity in the input makes the branch's syndrome/environment factor independent of the logical state. The same decoder works for every completed history.

Thus each history operator H obeys, on the input code, D H V = U tensor |s_H>, with all ideal discard/preparation channels dilated and garbage retained for this algebraic assertion. Consequently D H_a V (.) V* H_b* D* factors as U(.)U* tensor the corresponding syndrome cross term. Arbitrary bath operators and arbitrary signed linear coefficients can now be attached, and summed, without changing the logical factor. No norm estimate, positivity, trace preservation, or dimension bound is assigned to those coefficients. This establishes the source's equation (4), rather than assuming that general bath coefficients lie in a span of trace-preserving fault maps.

For a nonunitary logical computation, first keep its discarded work in a unitary/isometric dilation; only then trace the declared outputs. The analysis decoder and retained dilation environments are proof devices, not noiseless hardware supplied by this receipt.

## 2. Recursive norm counting

The nested partition eliminates overlapping-exRec issues. On every selected collection of parent rectangles, multiply the exact threshold-indicator sieve over their disjoint child sets. Each monomial is precisely an inclusive event on a union of distinct children. The previous-level joint inclusive bound applies; no independence, physicality of a grouped bad map, or bath reset is needed. The coefficient inequality is

 C(A,t) C(t-1,s-1) = (s/t) C(A,s) C(A-s,t-s).

It gives C(A,s)x^s(1+x)^(A-s) uniformly for gadgets of size at most A. The next-level inclusive statement therefore follows jointly, not merely for single gadgets. `SIEVE_CHECK.txt` records 9,425 exact integer evaluations of the indicator identity for 2<=s<=A<=30; the symbolic argument, not this test, proves arbitrary size.

The stated x-star choices imply (1+x)^(A-s)<=e and e C(A,s)x-star^(s-1)<=1. They yield x_j<=x-star (x_0/x-star)^(s^j), including A=s. We assume 2<=s<=A; the actual nontrivial gadget family has this property. The exact top-level union expansion gives (1+x_j)^L-1 and then L x_j exp(L x_j). There is no illicit union bound on signed probabilities.

## 3. Trace defect and the factor two

Enc and the completed analysis Dec are CPTP, so the decoded bad map has diamond norm at most b. Since the whole decoded channel is TP and its good part factors U tensor K, its trace defect is I tensor (K*(I)-I), with operator norm at most b. For any logical/bath/reference state, partial tracing the bath against this bounded effect changes the ideal logical/reference output by trace norm at most b (duality with a norm-one output observable proves the bound even with initial correlations). The reduced bad term contributes at most another b. Thus the complete logical error is <=2b, without normalizing a signed state. Hermiticity preservation follows from the physical cavity expansion; no positivity of K is needed. A deterministic wrong-answer projector annihilating all good outputs instead gives the direct bound b.

## 4. Hardware, input/output and cost boundaries

The hierarchy requires the chosen actual computation-code circuits, including coherent syndrome gates, entropy removal, identities and routing. Supplied connectivity must support that family with the declared finite A and depth constant; arbitrary routing must not silently change these to size-dependent constants. Synchronization/padding and idles during long resets are counted with actual durations. Error tolerance can be positive but arbitrarily small: first choose a finite reset duration making its residual less than x-star, then choose incident noise small enough for the resulting maximum duration. This is not circular and does not demand exact physical reset.

With fixed x_0<x-star, the displayed recursion gives O(log log(L/delta)) levels and L A^j locations, hence polylogarithmic overhead. Here L must count the complete ideal padded circuit and its required preparation/output modules, not just nonidentity logical gates. The quantum-channel assertion starts from a supplied encoded input and ends at the analysis decoder. The physical classical assertion uses the actual protected de-encoding and recursive-majority contract, with 2d+1<=m (satisfied by the selected error-correcting code family). An unknown raw symbol/state or a final exposed detector needs a separate reliability interface.

Initially dirty ancillary targets are received by the separately accepted approximate-target cavity theorem and the actually supplied reset primitive, not by pretending a finite reset is exact. The total bath may have memory and initial correlations within the bounded finite model; this does not manufacture an infinite-bath theorem or an autonomous clock/controller.

## Final scope

Accepted: scheduled reliable encoded computation / protected classical output for this concrete disjoint computation-code architecture, under the fixed resource/input contract and separately accepted cavity and approximate-gate hypotheses. No claim of practical advantage, autonomous universality, unknown-input capture, detector qualification, or novelty is accepted. This review made no external changes.
