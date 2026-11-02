# Skeptical self-audit of the physical phase join

2026-11-01, 22:56 UTC. This is a second self-check, NOT an independent-author audit. Reviewed ROOT_PHASE_CONSTRUCTION.md against LOCAL_CHANNEL.md, actual_decoder_binding.md, the Gram/sampler bridge, and the primary code geometry. No fatal counterexample was found under the stated geometry and inherited analytic inputs. The following details must remain explicit.

## 1. Source geometry is sufficient for memory, not arbitrary added bath

I reopened [Balasubramanian–Davydova–Lin2605.10943v1](https://arxiv.org/html/2605.10943v1): Theorem 1.2 explicitly includes bounded qubit density; Definition 3.1 and Theorem 3.16 retain level-independent square density and edge length. Covering a radius-r ball by O((1+r)^3) unit balls supplies the required physical growth. Check registers add bounded density because checks have bounded support/incidence. This does not cover an arbitrary polynomial-size bath; its bounded physical density remains a genuine additional scope restriction.

The source also explicitly distinguishes lambda (scaling per iteration) from ell (subdivision). Thus the trace exponent may be chosen

    p_tr = 1+2 log_2(lambda),

with constants and, if necessary, a larger exponent absorbing fixed local stages. Do not substitute ell without its relation to lambda. In the root's notation choose b>=max{p_tr,p_phi,p_decode}, where p_phi is the independently earned potential-envelope exponent and p_decode bounds full backward cones. All are fixed construction constants. Then q=max{7b+1,9} is a conservative causal-radius exponent.

## 2. Trace diameter: skeptical test passed with the isolated-replay qualification

An arbitrary sparse marked history need not have physical diameter polynomial in its marked cardinality: a high-level wire could span the sample. Here that counterexample is excluded only because every component is an individually VALID isolated replay, so halving occurs every two levels until the integer syndrome vanishes. Its deepest nonzero stage is O(log m). Every object of its complete stencil is at no more than an additional fixed number of stages. Forward displacement then bounds each host step by O(lambda^O(log m)); multiplying by at most m host steps is valid even when the trace folds or its top support is disconnected. Downward correction descendants obey the same forward carrier bound. No inverse-Lipschitz embedding is needed.

Do not weaken the premise to 'correction has polynomial cardinality'; that premise alone allows disconnected corrections arbitrarily far apart. The root correctly uses the stronger carrier argument.

## 3. Component recognition: one necessary procedural clarification

A radius-limited flood fill of top syndrome defects is NOT enough, nor is stopping after finding M inputs. Such a procedure can mistake the visible fragment of a large trace for a complete small component.

The correct procedure computes actual gate values from an unchanged copy of original syndrome bits through depth t_M=2 ceil(log_2 M)+C, including one extra layer to verify zero outgoing frontier. Every requested gate's entire backward dependency cone is included, whether or not that cone is active. Fixed local branching and t_M=O(log M) keep its size polynomial in M; the geometric carrier estimate keeps its radius polynomial in M. Explore the resulting marked full-stencil graph, stop at M+1 objects, and accept ONLY if all adjacent active-gate incidence and all outgoing frontier tests are exhausted/zero. Then an accepted component is genuinely complete in the original execution. Any undiscovered higher-level activity would require a nonzero path through the checked zero frontier. Every true <=M component passes by isolated replay. Large components may be left untouched on the exceptional event; a local fallback gives a CPTP map on all inputs.

The root's condensed sentence about closed components is sound only with this expanded algorithm. Correction additivity uses disjoint active-gate outputs plus the linear downward chain-map lift; Pauli phases cancel in conjugation. No global decoder oracle or global success bit is used.

## 4. Invalid control labels: no gap inference is needed

The direct-sum controlled parent can have invalid blocks with low eigenvalues, so applying a global gapped spectral-flow theorem verbatim would be unjustified. The root avoids this correctly. Define the filter integral globally with the fixed filter appropriate to the valid-sector gap; physical LR locality is independent of whether the complete direct sum is gapped. Control projectors commute with parent, derivative, and resulting generator. Restriction to a valid block is exactly its gapped spectral flow, hence transports that kernel. No invalid label is populated by the forward valid trace sampler. A purported proof requiring a spectral gap above the entire controlled band's zero space would be an overstatement; this proof does not.

## 5. Phase channel versus elementary runtime

The graphical-event bound is a real causal-cone argument: bounded root clock intensity, radius-r_u update dependencies, physical O(r_u^3) root choices per chronological step, and T^k/k! ordered-time volume. Finite time precision increases record bit lengths, not round count. Coloring plus dependency height gives the displayed polylog radius. The root appropriately does NOT turn continuous-time mixing alone into a local circuit.

Arbitrary CPTP block maps can contain polylog-volume truth tables and expensive quantum synthesis. The stated exp(log^{O(1)}(N/epsilon)) generic compilation is honest; simultaneous polynomial elementary cost/polylog depth is not earned. Precomputed coefficients may depend on the fixed Hamiltonian, but each online transition depends only on local records. If the previous global row reduction supplies a nonlocal stabilizer representation, select an envelope-supported representation by finite linear algebra in the certified envelope; brute-force block construction is already permitted by this cost statement.

## 6. Remaining claim boundaries

The specified-state result has O(epsilon+eta_n) error; O(epsilon+poly(N)eta_n) is a harmless looser root statement. Gram nearscalarity makes rank-two holonomy irrelevant only for maximally mixed logical sectors. Arbitrary unknown logical inputs require the separate parallel-transport argument and reference-safe error accounting, as the root says. Keep the inverse-polynomial asymptotic accuracy qualification and finite-bath geometry. No all-annulus stable-clustering theorem or high-temperature separation invariant has been proved by this channel construction alone.

Verdict: the narrowly stated ideal physical local-channel join survives this self-check, contingent on inherited code/Gram/gap results. The component-recognition algorithm and explicit exponent definitions above should be incorporated before treating the condensed root proof as complete.
