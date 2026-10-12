# Exact affine-span sampling for compressed discrete noise

**Status:** proof candidate, 12 October 2026. No implementation, practical-speed, or novelty claim is made.

## 1. Input and output

An acyclic straight-line grammar specifies deterministic linear controls on F_2^D interleaved with independent discrete additive noise slots. Binary nested repetitions are compiled by repeated squaring, so their bit lengths, not their expanded lengths, are charged.

In the first theorem, a slot adds F(U), where U consists of fresh uniform bits and F is an explicit multilinear vector polynomial of degree at most d. All occurrences are independent. The output is one sample from the complete final state distribution.

There is an exact expected-polynomial sampler, with expected at most D 2^d structurally active slot visits, apart from polynomial grammar and linear-algebra factors. A fixed polynomial cap gives an epsilon-total-variation sampler. No laziness, continuous-time embedding, or mixing-time assumption is required.

The controls may be singular. For Clifford applications they are the supplied symplectic actions on Pauli frames. This concerns final joint error frames; it does not output an exponentially long measurement history or solve adaptive nonlinear feedback dynamics.

## 2. Centering and final-frame coordinates

For every noise leaf let c = F(0) and G = F + c. Thus G has zero constant coefficient. The deterministic contribution of all c values is compiled using affine-map composition, together with the supplied controls. Add this contribution only once to the final output.

The remaining random error is a sum of independent transported centered marks M_i G_i(U_i), where M_i is the deterministic linear suffix after occurrence i. There can be exponentially many occurrences, but they need not be listed.

For each grammar node A precompute its clean linear map C_A and its output-frame centered coefficient span S_A. For A followed by B,

    C_AB = C_B C_A,
    S_AB = C_B S_A + S_B.

Zero constant coefficients ensure that the image span of G is exactly its coefficient span. The inclusion of the image in the coefficient span is immediate. Conversely each coefficient is the XOR of suitable evaluations, by Boolean Mobius inversion.

## 3. Two independent marks give an affine random line

For any distribution of a vector J, let J and J' be independent samples. If B is an independent fair bit, then

    J + B(J+J')

has the same marginal law as J: it is J when B=0 and J' when B=1.

Suppose the current accumulated error has conditional law Uniform(C+W), where W is a subspace. Exposing J,J' while leaving B unexposed changes the conditional law to

    Uniform(C+J + span(W,J+J')).

This identity is exact. In particular, even when J+J' lies in W and no rank grows, the offset C must still be updated by J. Omitting that offset would be incorrect.

For a polynomial slot in final-frame context M, use J=M G(U), J'=M G(V) for two fresh independent latent inputs. Maintain

    C <- C + M G(U),
    W <- span(W, M(G(U)+G(V))).

At the end, sample a uniform vector in C+W and add the separately compiled deterministic drift.

## 4. Every structurally active polynomial slot has a rank chance

A slot is structurally inactive when M S is a subspace of W. Then every centered mark lies in W, so the slot is exactly the identity on Uniform(C+W), and it may be skipped.

Otherwise some linear functional ell vanishing on W has a nonzero scalar polynomial P(U)=ell(M G(U)). Its constant coefficient is zero, so P is nonconstant. If its degree is at most d, both P and 1+P are nonzero degree-at-most-d polynomials. Therefore

    2^{-d} <= p = Pr(P(U)=1) <= 1-2^{-d}.

For independent U,V,

    Pr(P(U) != P(V)) = 2p(1-p) >= 2^{-d}

for d>=1. This event forces M(G(U)+G(V)) outside W and hence increases rank. Degree-zero leaves have no centered noise and are skipped.

There are at most D rank increases. Conditional on every history, each visited active slot has success probability at least 2^{-d}. Thus the number of active visits is dominated by the waiting time for D successes with probability 2^{-d}, stopped earlier if the program ends. Its expectation is at most D 2^d. A standard binomial tail gives a cap O(2^d(D+log(1/epsilon))) with failure at most epsilon.

## 5. Exact compressed traversal

Work in final-frame coordinates, so W only grows and the marks may be processed in any deterministic order. At a node in suffix context M, skip the entire occurrence if M S_A is contained in W. Otherwise descend to a structurally active leaf. For a concatenation A followed by B, the left context is M C_B and the right context is M.

A depth-first traversal stack stores only polynomially many matrices and node references. After consuming a leaf, continue at the next unresolved occurrence. Previously skipped occurrences remain safe because their centered marks lay in an earlier subspace contained in the current W. Between consecutive active leaves, the compressed traversal crosses only O(H) stack edges and fully skipped sibling subtrees, where H is the compiled grammar depth. No expanded prefix is scanned leaf by leaf.

Equivalently, persistently delete each consumed noise occurrence by copying its root-to-leaf path and setting only that occurrence's noise span to zero. This uses O(H) new nodes per consumed occurrence and preserves all deterministic controls. Searching for any remaining active occurrence then costs polynomial work per visit. It is useful when processing leaves out of order.

All randomness here consists of finite uniform latent bits and the final uniform span coefficients. Hence the expected-polynomial algorithm is exact in the ordinary bit model; there is no ideal real-clock operation. A capped version has polynomial worst-case work and a directly charged total-variation error.

## 6. Extension: arbitrary explicit categorical slots

The same affine-pair operation, combined with a rank-budget Poissonization lemma and the companion compound-Poisson compiler, gives an approximate sampler for explicit finite categorical distributions with arbitrary rational weights. This extension does not infer a lower bound from a large total noise probability.

Assume each leaf distribution has at most s explicitly listed atoms. Choose one maximum-mass atom b, whose probability is at least 1/s. Subtract b as a deterministic shift and compile all these shifts globally. Call an atom heavy if its probability is at least tau, and center every atom v to v+b.

Search the remaining compressed program for an occurrence with a transported heavy centered atom outside W. This is acquired by the exact span summaries of the heavy centered atoms, under suffix contexts. If such an occurrence exists, consume its **whole original categorical slot** using two independent exact samples J,J' from its centered law and the affine-pair update above. Persistently delete only that noise occurrence, retaining the controls.

If v is a witnessed heavy atom outside W, the two pair outcomes (v,b) and (b,v) occur with total probability at least 2 tau/s, and their centered difference is the witnessed outside vector. Therefore each consumed slot grows rank with probability at least 2 tau/s. The expected number consumed is at most D s/(2 tau), with a polynomial high-probability cap.

When the search terminates, every heavy centered mark of every remaining occurrence lies in the current W. Replace these marks by zero: they are exactly identities on the present conditional affine-uniform law, and they remain so as W grows. Each residual slot now has total nonzero probability at most s tau. It is crucial that the positive grammar represents the remaining occurrences; no subtractive intensity estimates are used.

### Rank-budget Poissonization lemma

On subspaces, let K_j add the span of one random proposed mark, and let

    P_j = I + p_j(K_j-I),    E_j = exp[p_j(K_j-I)],

with 0 <= p_j <= 1. Let a_j(W) be the probability that the proposal lies outside W. In total-variation norm on signed rows,

    ||delta_W(K_j-I)|| = a_j(W),    ||K_j-I|| <= 2.

The integral Taylor remainder gives

    TV(delta_W P_j, delta_W E_j) <= p_j^2 a_j(W).

Telescope the product comparison using original P-prefixes and approximate E-suffixes. Its total error is at most

    sum_j p_j^2 E[a_j(W_before_j)]
    <= p_max sum_j p_j E[a_j(W_before_j)]
    <= D p_max.

The final sum is the expected number of original rank increases, bounded by D, not the number of slots. The bound holds for arbitrary varying mark laws and numbers of slots.

A residual physical XOR slot with nonzero probabilities mu_j(v) and total mass q_j <= s tau has the exact random-line representation with trigger p_j=2q_j and conditional proposal distribution mu_j(v)/q_j, provided q_j<=1/2. Its Poissonized span kernel corresponds to physical compound-Poisson marks of intensity mu_j(v). Thus all residual slots can be replaced jointly by compound-Poisson noise at total error at most 2D s tau.

Choose tau = epsilon/(8 D s), for example. The remaining positive grammar has grown by only polynomially many path copies. Apply the companion compressed compound-Poisson compiler to its light atoms, starting from the acquired affine state C+Uniform(W), and allocate the remaining error budget to that compiler and the high-stage cap. The final result has epsilon total variation and polynomial cost in the grammar, D, s, rational bit lengths and epsilon^{-1}.

No assumption mu(0)>=1/2 is required in this explicit-alphabet extension. The selected modal atom supplies a probability at least 1/s for the heavy-stage pair witness; the residual becomes lazy only after all heavy directions have been absorbed. Uniform-latent polynomial slots use the simpler exact theorem in Sections 1-5 instead.

## 7. Scientific contract

These results supply final joint samples for compressed deterministic linear/Clifford control with structured independent discrete faults, including repeated and nested schedules. Full endpoint correlations are retained. A polynomial-time final syndrome map or supplied decoder can be evaluated on each sample, with additive statistical accuracy.

They do not supply physical noise calibration, coherent-error simulation, generic quantum dynamics, nonlinear online decoding, or exponentially long output records. Exact algebraic noise descriptions and the actual deterministic compressed schedule are required inputs. Large polynomial costs and finite-sample rare-event limitations remain.
