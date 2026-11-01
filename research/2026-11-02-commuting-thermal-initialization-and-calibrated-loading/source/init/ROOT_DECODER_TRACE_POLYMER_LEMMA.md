# Root candidate: a zero-background decoder trace yields an exact positive polymer gas

1 November 2026. Abstract constructive lemma; actual RX/RZ hypotheses require a separate binding proof. This is not yet a physical loader.

## Required decoder representation
Consider a finite directed acyclic circuit with binary input x (the syndrome), finite-alphabet internal wires, and deterministic gates. Every gate sends all-zero input to all-zero output. Bound gate fan-in/out, alphabet, stencil size, and wire fanout by constants independent of n. Distinguish rejecting output flags: x is a valid syndrome iff all such flags vanish. Require the gate-level representation, not merely a global decoder oracle. Local reconstruction witnesses may establish the same validation contract.

An execution marks EVERY gate with at least one nonzero input, including gates whose outputs all cancel to zero. Also mark nonzero external input wires. Each marked object includes its complete input/output wire stencil. Connect marked objects whenever their stencils overlap. A polymer is one connected component of this marked execution, including all wire values on its stencil and the labels of its top-level syndrome inputs.

Required quantitative condition on every valid execution:
 total marked objects <= A |x|,
with A independent of n. A multiscale contraction sum_i |x_i|<=C|x| with a bounded-size local gadget circuit is one way to earn it. Do not assume this for an arbitrary polynomial-time decoder.

## Exact splitting and recombination
Take an accepting execution and a connected trace component gamma. Set all input bits outside its component to zero and replay the circuit. Induction over the circuit shows that each marked gate in gamma sees precisely its original input; each other gate sees zero or belongs to an original distinct component. If a gate had nonzero inputs from two purported components, that gate would itself be marked and join their stencils. Cancellation gates are why the full-input marking is necessary. Thus the replay exactly reproduces gamma and zero elsewhere. All rejecting flags remain zero, so the isolated component is valid.

Conversely, take any family of individually accepting connected traces whose stencils are pairwise disjoint. Their top-level inputs have disjoint supports. Replay their union. The same induction gives the union of their traces: no gate can become newly active from multiple components without already belonging to their marked fanout stencils. Therefore the union is valid and its unique trace decomposition is precisely the family. Determinism gives uniqueness; this is not a many-to-one witness cover.

Hence valid syndrome strings are in bijection with compatible collections of individually valid connected traces. For additive positive syndrome energy E(x)=sum_i J_i x_i, weights factor exactly as product_gamma exp(-beta E(x_gamma)). Any constant logical-sector degeneracy in a commuting stabilizer Gibbs state factors out separately.

## Counting, truncation and algorithmic promise
Suppose the marked-object incidence graph has maximum degree Delta, O(n) vertices, and at most M possible local trace labels. Connected labeled traces of size m containing a specified object admit an upper count (c Delta M)^m. Since m<=A|x_gamma| for isolated valid components, activity is <=exp[-beta J_min m/A]. At sufficiently low fixed temperature this supplies a convergent small-activity hard-core polymer model.

Enumerate connected labeled subsets of size <=L, replay/validate each candidate, and retain only exact connected traces. L=O(log(n/epsilon)) makes enumeration polynomial in n/epsilon for fixed constants, although the exponent can be enormous. A union bound over incompatible or compatible polymer gases bounds the omitted large-polymer probability by the sum of their activities: positivity and Z(excluding neighbors)<=Z give the elementary single-polymer inclusion bound Prob(gamma present)<=w_gamma.

This establishes an explicit finite polynomial candidate dictionary plus a controlled truncation error IF the premises hold. It does not yet prove a polynomial mixing sampler on that dictionary: a specific rapidly mixing hard-core update rule or exact sampling algorithm must still be supplied, with its implementation cost. Invoking Peierls counting alone is insufficient.

## Physical boundaries
Even a successful syndrome sampler only handles the COMMUTING known Hamiltonian. It still needs an actual encoded input and a physical procedure for applying reconstructed corrections. It does not prepare generic noncommuting memory-bath equilibrium, tolerate noisy routing, or erase the raw input error floor. Its relevance is removal of one essential ideal thermal-initialization obstruction, not an end-to-end memory claim.

## Explicit sampler closure under the rooted activity bound
The preceding algorithmic gap can be closed directly for the finite truncated dictionary. Use a continuous-time hard-core chain: remove each present polymer at rate 1; insert each absent compatible polymer gamma at rate w_gamma. Detailed balance holds for the exact truncated Gibbs distribution.

Let |gamma| count marked objects and assume
 sum_{eta incompatible with gamma} w_eta |eta| <= theta |gamma|, theta<1.
Here incompatibility includes overlapping dependency stencils. The bounded-degree rooted-animal estimate implies this for sufficiently large fixed beta: sum rooted m (c Delta M)^m exp(-beta J_min m/A) can be made arbitrarily small, and each gamma has O(|gamma|) possible touching roots.

Couple two adjacent configurations differing by gamma with identical birth and death clocks. Removal of gamma decreases their weighted symmetric-difference distance by |gamma| at rate 1. A birth admitted on only one side can increase distance by at most |eta| and must be incompatible with gamma. All other events preserve or decrease distance. Expected instantaneous drift is thus <=-(1-theta)|gamma|. The path metric is weighted symmetric difference: remove differing polymers, then insert the others, always through legal configurations. Path coupling gives Wasserstein contraction exp[-(1-theta)t]. Compatible trace components have total marked size at most N, the circuit's marked-object universe, so diameter <=2N. Total variation mixing error is <=2N exp[-(1-theta)t]. Thus t >= log(2N/epsilon)/(1-theta) suffices.

A direct implementable uniformization uses rate R=sum_{gamma in dictionary}(1+w_gamma): choose gamma with probability (1+w_gamma)/R, choose death with probability 1/(1+w_gamma) or birth otherwise, and do the corresponding legal update or a null event. Simulate a Poisson(Rt) number of steps. Dictionary size is polynomial after truncation, every acceptance test is polynomial, and R<=2 times dictionary size since w<=1. Approximate real probabilities and Poisson sampling to total variation epsilon/2 with a charged finite-bit implementation; weights may be supplied with polynomial-time computable precision. This is a conventional hard-core polymer sampler, now explicit, not a novel mixing theorem.

Together, the trace-bijection and activity premises give a polynomial ideal Gibbs syndrome sampler to any inverse-polynomial target error. For arbitrary epsilon the displayed enumeration is polynomial in n/epsilon, not necessarily in log(1/epsilon). The large fixed constants may make it impractical.
