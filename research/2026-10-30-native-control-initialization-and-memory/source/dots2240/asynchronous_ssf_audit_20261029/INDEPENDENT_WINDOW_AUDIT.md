# Independent adversarial audit: asynchronous SSF window witness
2026-10-29. Audited ASYNCHRONOUS_WINDOW_WITNESS.md §§1–9 and DERIVATION.md.

## Result first
**I found no mathematical counterexample to the ideal atomic, independent-clock, Pauli comparator under the explicitly strengthened hypotheses below.** Its threshold closure can be made precise with a rooted-forest count and an unnormalized induction. This is not an audit endorsement of an autonomous finite-duration quantum memory: the physical scheduler/instrument interface and coherent-noise/readout interface remain unproved. No novelty or acceptance claim is justified by this audit.

The most useful correction is to replace the schematic counting/iteration in §9 by the explicit bounds below. Importantly, neither adaptively selected missed candidates nor minimum-syndrome representatives cause an apparent fatal selection bias: deterministic domination by fixed containing sets, followed by a union bound, removes it. The argument does **not** justify conditioning on a favorable clock record and declaring its DATA action clean.

## 1. Exact assumptions needed for the comparator
- A bounded-degree fixed graph contains every check support, every correction hub's full read footprint, and every elementary fault support as cliques. Let its maximum degree be D.
- Accepted corrections have integer syndrome decrease at least one, bounded support w, and obey the stated SSF inequality. Every atomic hub ring either chooses an accepted candidate or does nothing only if none exists. The candidate family must include the family used by FGL Proposition 14; an arbitrary strict subset is not enough.
- Hub clocks are mutually independent Poisson clocks with rate at least lambda. Their fresh increments are independent of the past and of the dominating fault clocks. Fault clocks have bounded support s and bounded per-site channel incidence z, with total touching intensity at most epsilon z per site. Thinning may depend causally on the history; no anticipatory dependence on future clock increments is permitted.
- The input error law is locally stochastic; after killing failed histories it is a subprobability law with the same support inequalities. For the quantum interpretation, Pauli trajectory weights must describe a legitimate random-Pauli/noise instrument that does not learn logical information. A general state-dependent quantum jump is not a Pauli jump merely because a Pauli label is attached to it.
- A deterministic tie-breaking convention selects a global minimum-Hamming-weight representative of each syndrome. This is an analysis/ideal-readout representative, not a claimed efficient physical operation.
- The code family has the expansion hypothesis and small-error constants required by FGL, constant rate, and distance at least d_0 sqrt(N).

## 2. Deterministic claims checked
### Packing and window contraction
The syndrome-disjoint, at-most-one-per-hub packing is valid with bounded candidate multiplicity. A correction can resolve at most |sigma(H)| packed candidates by syndrome intersection and at most one more through its own hub, hence at most 2 d(H)/beta. A bad event can resolve at most |sigma(Q)| candidates. Thus equation (2) follows without a sweep or a scheduler distribution.

### Future-support localization
For a fixed actual or virtual serial history, U_i = E_i union future masks = E_L union future masks is exact, and is decreasing. Each event mask is in a single component because it is a clique. Errors sharing a check cannot lie in distinct components. A beneficial candidate touches a currently erroneous site through its hub's read footprint; every actually chosen alternative at that hub lies in the same component. Candidates whose hypothetical masks extend outside U_i are harmless: no hypothetical correction is added to support.

For equation (4), explicitly note that at the next boundary, W_{j+1} and the pieces discarded from W_j belong to different U_{j+1} components. Their syndromes are disjoint. Therefore discarding pieces cannot increase the local syndrome weight. Nested supports alone would not imply this without check-support adjacency.

### Reduction and mergers
Let U contain the original initial error and all actual event masks, and K be a component of U union R_min. Check-clique adjacency implies that E_L intersect K and R_min intersect K have the same syndrome. Replacing the latter by the former is a legal same-syndrome competitor, so minimum weight gives |R_min intersect K| <= |E_L intersect K|. Restricting the actual history to K preserves correction decreases, giving

  |K| <= 2 (1+w Delta) [|E_0 intersect K|+Q_block(K)].

This estimate is unconditional: it does not require K to be below the cutoff. This avoids circularity in the bad-cluster union bound. On |K| < min(distance, FGL cutoff), the componentwise zero-syndrome difference has weight below distance and is a stabilizer. Global minimum-syndrome weight also implies stabilizer-reduced weight. The virtual suffix ends at R_min, stays inside U union R_min, and has the same syndrome at every instant. FGL is applied separately to its small components, not to their extensive union.

Enlarging W_0 to components of U union R_min meeting S is essential. Applying seed density directly to W_0 is unjustified, because representative reduction may remove connecting original seed sites. The manuscript already makes the required enlargement.

## 3. Explicit count for arbitrary target S (including disconnected S)
Fix nonempty S of size k and m >= k. Let A_m(S) contain all W of size m containing S such that every induced G_R component of W meets S. Then

  |A_m(S)| <= 2^(D m).

Proof: initialize a deterministic breadth-first traversal with all vertices of S as ordered roots. For each popped vertex, inspect its D ordered neighbor slots and flag the children that are first discovered in W. Every W vertex is discovered since every component meets S. The resulting forest is encoded by a bit string of length Dm; given S and the graph, the string reconstructs W. Fix a deterministic tie rule to obtain an injection. This bound does not assume independence among components or one distinguished root for all of W. For D=0 it remains valid.

The same bound with one root, followed by a union bound over N roots, bounds connected large components. An N-dependent factor is required for the cutoff probability but **not** for the fixed-S support tail.

## 4. Explicit moment and union bounds
Write C_g=2^D, C_work=1+w Delta, alpha=1/(2 C_work), u=max(p,epsilon z RT), v=max(exp(-lambda T),epsilon z RT), and assume 0<u,v<1. Let

  r_seed(u) = C_g exp(2 sqrt(u)) u^[1/(4s C_work)],
  r_bad(v)  = C_g exp((h0+1) sqrt(v)) v^[1/(2s C_bad)].

These follow directly by setting t=u^(-1/(2s)) or v^(-1/(2s)). The seed moment is at most exp(2 sqrt(u)m), since the two contributions are bounded by u t and u t^s. The obstruction moment is at most exp((h0+1)sqrt(v)m). No unspecified parameter-dependent constant is needed.

For a fixed W, the count of missed packed candidates is bounded pathwise by the number of hubs in the fixed containing set H(W) with zero rings in the specified window. This is true even when the selected W and packing depend on the complete future history: apply the fixed-W probability bound first and union-bound over W afterward. Do not condition on the adaptive selection. Dominate suffix faults by full-block fault counts, which only weakens the estimate.

Let c_R=(h/Delta) theta^(-R), and choose R with c_R>=1. The witness dichotomy and the forest count give, for k=|S|,

 P[Good and S subset R_min]
 <= r_seed(u)^[ceil(c_R k)]/(1-r_seed(u))
    + R r_bad(v)^k/(1-r_bad(v)).

This makes the target-size dependence and the R-window union explicit. If both bases are at most 1/2, the residual is subnormalized locally stochastic with parameter

  p_out = 2 r_seed(u)^c_R + 2R r_bad(v).

Indeed 2a^k+2R b^k <= (2a+2R b)^k for integer k>=1. There is no problematic constant independent of k left outside the support-tail parameter.

Let L_N be an integer cutoff no larger than both the FGL cutoff and the code distance, and define Good by every enlarged component having size <L_N. Then

 P[not Good] <= N r_seed(u)^L_N/(1-r_seed(u)).

The density estimate for K is unconditional, so this uses no stopped-process bootstrap. Strict inequality in Good is necessary for the distance argument when L_N equals the distance.

## 5. Noncircular fixed-parameter selection
Put eta=1/(4s C_work). Choose constant R with c_R>=1 and eta c_R>1. Choose p_* so small that r_seed(p_*)<=1/2 and

  2 r_seed(p_*)^c_R <= p_*/2.

Next choose v_*>0 small enough that r_bad(v_*)<=1/2 and 2R r_bad(v_*)<=p_*/2. Choose constant T with exp(-lambda T)<=v_*. Finally choose

  epsilon z RT <= min(p_*,v_*).

Then every input parameter p<=p_* yields p_out<=p_*. All choices are independent of N. Increasing T makes the fault budget harder, but the final epsilon choice explicitly pays for it. This establishes existence, not a useful numerical threshold or efficient finite-size performance.

## 6. Subnormalized induction and quantum meaning
Let H_b mean all previous blocks were Good and define the input measure mu_b(A)=P[H_b and E_b in A]. Maintain mu_b[S subset E_b]<=p_*^|S| and mu_b(total)<=1. For this measure,

  integral t^|E intersect W| dmu_b
  = sum_{A subset W}(t-1)^|A| mu_b[A subset E]
  <= (1+p_*(t-1))^|W|.

The empty-set term is bounded by one, not divided by mu_b(total). Fresh independent clock increments give the same block proof on mu_b. Kill the new bad histories and select the equivalent R_min on the survivors. This yields the same inequalities for mu_{b+1}. No conditional input distribution is asserted to be locally stochastic. The failure mass accumulated in B blocks is at most B N r_seed(p_*)^L_N/(1-r_seed(p_*)).

For two CSS sectors, independence between the sectors is unnecessary: retain a common survivor event, use each marginal support inequality and a union bound. Ideal X and Z corrections preserve the other syndrome. For arbitrary encoded state entangled with a reference, each surviving Pauli trajectory differs from the appropriate decoded state only by stabilizers and an irrelevant phase. This is an ideal decoded-logical channel statement; it is not pristine physical output and does not implement a bounded-latency physical decoder.

## 7. Remaining limits: do not promote this into the desired memory claim
1. Finite-duration transactions need an exact clean DATA instrument after workspace initialization, read locking, conflicts, aborts, repairs, and reset. A successful control/CLOCK path probability alone supplies neither that instrument nor independence.
2. Real missed opportunities need product-type domination uniformly under competing histories. Independent no-ring indicators are available only in this atomic comparator.
3. General local coherent perturbations require an amplitude/norm fault expansion or a separately justified Pauli reduction. Support-probability counting alone does not control coherent interference.
4. Output during unfinished transactions requires a physical readout/drain/dressed-data theorem. Analysis-time minimum-syndrome representatives are not that theorem.
5. Graph-local constant overhead is not fixed-dimensional geometrically local constant overhead. Wires, bandwidth, routing and reset/pumping resources remain charged.
6. 'Unknown noise' here can mean unknown causal thinning of specified bounded-rate local Pauli clocks. It cannot mean unrestricted noise, correlated fault fields without product tails, or arbitrary state-dependent non-Pauli Lindblad terms.

## Primary-reference check
Directly inspected Fawzi–Grospellier–Leverrier, arXiv:1808.03821, Proposition 14 and Lemmas 15 and 17: https://arxiv.org/html/1808.03821 . The cited small-error candidate-mass, reduced-error confinement, and subset-reduction properties match their use here. The new asynchronous counting and induction above are audited derivations, not claims that the reference proves an online asynchronous compiler threshold.

## Access/action record
Read the two specified local files and the public arXiv primary source. Wrote only this audit file under the requested shared audit directory. No denied read, escalation, external mutation, or pending tool action occurred. No simulation of an HGP decoder was performed.
