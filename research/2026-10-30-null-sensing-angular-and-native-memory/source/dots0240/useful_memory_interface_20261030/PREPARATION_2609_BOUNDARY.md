# What the confinement-only single-shot preparation theorem does—and does not—supply
2026-10-30. Primary theorem/algorithm inspected, not an abstract-only comparison.

Primary: Zhao, Yuan, Han and Liu, arXiv:2609.39965v2, 1 October 2026, https://arxiv.org/html/2609.39965 . Exact locations: Sec. II.2–II.3; Theorem 1; Appendix B.2; conclusion.

## Source contract (concise)
The protocol prepares physical |+> qubits, measures Z checks once, repairs the noisy syndrome to a valid syndrome, then applies its chosen data correction. Noise is phenomenological: local-stochastic readout errors independent of ideal outcomes, followed by independent local-stochastic Pauli data errors. Theorem 1(1), assuming linear **soundness**, proves local-stochastic preparation residuals. Part (2), assuming only linear **confinement**, instead proves small logical failure after a formal perfect-syndrome recovery using its specially matched decoder. It does not prove local-stochastic residuals. Appendix B.2 defines that decoder through connected components of a low-closeness-syndrome graph, permits arbitrary base preimages in components not containing zero, and makes no efficiency claim. Its syndrome decoder minimizes a global closeness objective. The conclusion leaves efficient decoding open.

## Compatibility conclusion
Part (2) is not presently a direct initializer for the native GPT memory. The gap is not the existence of a logical state in some syndrome sector; that is supplied. The gap is membership, with a quantitative positive-event bound, in the native memory's common-correctable basin relative to its own decoder and controller initialization.

Specifically, the new preparation decoder's c(Sigma) may have large connected reduced-error support. Its logical convention is fixed by arbitrary choices in different low-syndrome components. The native GPT controller has neither been proved to preserve those conventions from arbitrary such components nor to move them into the component of the code vacuum. Appending the source's ideal recovery *before* memory would be an additional operation, not a proof that the already-physical prepared state is suitable.

This is why a claim such as 'linear confinement gives exp(-cN) preparation failure, so concatenate with exp(-cN) memory failure' is invalid without a channel/interface theorem. The formal recoveries need not match, and an ideal recovery is not performed at the concatenation boundary.

## Elementary noncomposition example
This logical issue exists even without noise details. Let P be a code-space projector and V its encoding. Let E map the code to an orthogonal syndrome sector, so an ideal decoder D satisfies D E V=id. A memory channel can preserve every encoded state perfectly while replacing all orthogonal-sector inputs by one fixed encoded state:

    M(rho)=P rho P + Tr[(I-P)rho] V|0><0|V^dagger.

For inputs supported separately in these sectors this is a CPTP measure-and-prepare extension. Thus D E V=id and D M V=id, but D M E V is constant. Good preparation after one formal decoder and good memory on exact code inputs do not imply good composition. This example is not a claim that the reviewed GPT controller behaves this way; it proves that the interface cannot be omitted.

## A genuine route that would compose
A preparation theorem supplying a small local-stochastic **physical residual** E_0, up to the stabilizers of the actual target state, can be inserted as a paid initial seed slab in the native backward-witness proof. This is the role of the stronger soundness branch or another factory with an LS repair theorem. INITIAL_SEED_SLAB.md states the required positive-record contract and derivation.

Three additional costs remain even then:
1. A physical one-shot syndrome/gate circuit must be compiled in the actual allowed noise model. The paper's independent Pauli/readout model is not automatically arbitrary joint retained-bath CPTP kicks.
2. The global classical correction must actually be obtained and its errors charged. A theorem with an inefficient or instantaneous classical decoder does not furnish a finite-rate controller.
3. During nonzero feedforward latency, an uncomputed high-weight Pauli byproduct cannot simply be treated as a zero-syndrome logical frame. The native zero-target memory need not protect that arbitrary syndrome sector. A protected latency bridge, explicit syndrome-frame-aware memory, or a factory whose output already meets the native initial-seed contract is required.

Therefore the confinement-only theorem sharply improves what is possible with a matching ideal recovery, but it does not presently erase the hardest autonomous loading boundary. No impossibility of such a bridge is inferred.
