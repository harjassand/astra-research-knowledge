# Public-current-frame response-family extension

Additive author construction, not part of frozen v1 acceptance. Jointly developed with the acquisition-certificate author. This changes the completeness promise and comparator, not merely the proof wording.

## Stronger uniform response promise
At each actual conditional past h, independently draw the m candidate arms with implemented probabilities q_i. Publish the full current frame tuple A if desired. Permit the source to choose a joint carrier/memory interaction N_(h,A) after seeing that tuple. Require ONE fixed hidden frame C* such that EVERY possible response N_(h,A), at every actual past, has its operators in the same hidden collective algebra. The source still cannot condition its map on the current private role, selected witness edge, random Bell eigenstate or readout randomness. Quantum input dependence through this fixed current map is allowed as usual.

This uniform response-family assumption is stronger than checking that only realized maps happen to share an algebra. It is a pointwise promise over possible current classical frame announcements. It does not cover quantum-controlled superpositions of hidden frames, arbitrary public preparation keys, or adversaries allowed to violate the family on unobserved responses.

## Predictable response loss vector
For edge i and arm j, define
 ell_(t,i)(j)= E_(A_-i drawn from current product q_-i)[delta_i(N_(h,(j,A_-i)), C_ij)/2].
Although the source is reactive to the published arm tuple, this response loss vector is well-defined before the tuple draw, conditional on the actual past and the source's response policy. It can depend on the current learner distributions; that is predictable and allowed in the v1 conditional calculation.

Because candidates are drawn independently and the witness role/edge is chosen independently, the same importance update Y/(rho q_i(j)) has conditional expectation ell_(t,i)(j). Expected selected loss sum_j q_i(j) ell_(t,i)(j) equals the actual expected edge loss under the reactive source. Thus the finite barrier proof, sampler domination and first-order stability apply without alteration to these response vectors.

The fixed net arm nearest C_i* has loss<= (9/4)epsilon^2 for EVERY response by the pointwise commutator bound; averaging other arms preserves this bound. Consequently the v1 exact-common-frame acquisition rate remains valid even when the current candidate tuple is public. Actual subsequent source memory is retained in the next history h; this proof makes no counterfactual future-history or policy-regret comparison.

## What changes and what does not
The comparator is now a RESPONSE-vector comparator at actual pasts, not the v1 fixed-frame defect evaluated on the single realized current map. The v1 approximate-Gamma corollary must NOT be imported unchanged. A separate uniform response-defect budget could support an approximate extension, but none is claimed here.

This distinction can remove candidate-frame secrecy as a requirement for structured completeness under this stronger promise. It does NOT remove role/key secrecy, the cost of preparing/reading candidate-relative Bell probes, finite sampler scheduling, trusted calibration, or the need for an independently checked service/outer-code acceptance proof. Any source-visible timing or metadata is covered only insofar as it can be included in a response family obeying the same uniform algebra promise and does not disclose protected current role/probe choices.

An equally informed ordinary adaptive bandit controller receives the same response-family benefit. No unique quantum computational advantage, historical novelty or laboratory demonstration is inferred.
