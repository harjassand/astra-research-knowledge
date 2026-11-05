# Code Swendsen--Wang versus BDL thermal loading

Independent comparator audit, 5 November 2026.

## Verdict

Code Swendsen--Wang (CSW) is a serious possible route to the proposed BDL loading operation, not a comparator that can be dismissed because BDL metachecks are not LDPC. The latest version still has a structural mixing hypothesis; it does not prove polynomial mixing for every stabilizer Hamiltonian. I have not proved that the BDL matrices satisfy or fail that hypothesis. Thus the honest status is **applicability unresolved**, not an established separation from CSW.

A proof that both BDL CSS check matrices are Delta-(co)graphic with Delta=O(log N) would substantially close the ideal sampling/loading problem using existing CSW machinery. Such a reduction could itself be the constructive opening. Conversely, a claim that a new sampler is needed should first address that matroid test or a direct mixing proof for the actual BDL family.

## Exact versions checked

- Hangleiter, Ju, Vazirani, *Code Swendsen--Wang Dynamics*, arXiv:2510.08446 **v4**, 5 October 2026. The abstract page lists v1 (9 October 2025), v2 (20 April 2026), v3 (26 May 2026), v4 (5 October 2026).
  - https://arxiv.org/abs/2510.08446
  - https://arxiv.org/html/2510.08446v4
  - Retrieved refs: turn88view1, turn91view0, turn95view0.
- Balasubramanian, Davydova, Lin, *A passive self-correcting quantum memory in three dimensions*, arXiv:2605.10943 **v1**, 11 May 2026. The current abstract page has only v1.
  - https://arxiv.org/html/2605.10943v1
  - https://arxiv.org/pdf/2605.10943
  - Retrieved refs: turn88view0, turn91view1, turn101view0.

In CSW v4 the relevant precise statements are **Definition 10, Theorem 16, and Corollary 17**, rather than the earlier numbering Definition 8/Corollary 15.

## What CSW actually proves

For h in F_2^{c by n}, let the rows label the actual Hamiltonian checks, so that their dependencies are ker(h^T) and valid syndromes form col(h).

Definition 10: h is Delta-graphic when there is a graph incidence matrix g in F_2^{c by m}, m=O(n) (polynomial m also suffices), such that

    ker(h^T) subset ker(g^T),
    dim ker(g^T) - dim ker(h^T) <= Delta.

It is Delta-cographic when a column-generator matrix of col(h)^perp is Delta-graphic. Equivalently, there is a graph incidence matrix g with

    col(h) subset ker(g^T),
    dim ker(g^T) - rank(h) <= Delta.

The coordinates in both tests are the c Hamiltonian checks, which must be the graph's edges. An arbitrary change of the Hamiltonian check basis is not free: replacing checks by products normally changes the Hamiltonian and its Gibbs law. Column-basis changes that preserve the relevant code subspaces are different.

Theorem 16 constructs flow congestion O(c^2 2^{2Delta+5} n^4). Corollary 17 then gives polynomial mixing for Delta=O(log n), at every temperature. Its displayed bound contains

    c^2 2^{O(Delta)} n^4
    [2+n log 2+c max{2 beta, log(1/(1-exp(-2 beta)))}].

For the fixed positive low temperature needed by BDL, the temperature factor causes no asymptotic issue. The algorithm has global linear-algebra updates. Its correctness is general; rapid mixing is not.

The v4 proof also shows the chain can mix exponentially slowly for a 3-spin Curie--Weiss code Hamiltonian at a first-order transition. Thus a general-code correctness statement is not a general-code efficiency result.

## What the available BDL structure establishes, and does not establish

BDL starts from a finite CSS seed with one logical qubit and alternates R_X and R_Z replacements. Each iteration enlarges the code by a constant factor, giving N=exp(Theta(k)), and preserves H^1, hence the one logical qubit.

That one-logical-qubit fact does **not** bound the CSW Delta. The quantities differ:

    k_logical = N - rank(h_X) - rank(h_Z),

whereas CSW needs graph-cycle realizations of each individual row-dependency space or syndrome space. The metacheck spaces can grow extensively even with k_logical=1.

BDL Lemma 3.8 / equation (74) describes the R_X induced coarse complex as the old complex with doubled terminal Z-check coordinates, plus extra H^2(C_X) and H^2(C_Q) summands. Remark 3.9 says those summands capture relations among extra Z stabilizers. The dual Lemma 3.11 / equation (97) and Remark 3.12 introduce analogous H^0(C_Q), H^0(C_Z) relations for X stabilizers under R_Z.

These are useful inputs for an inductive matroid analysis. But a cohomology isomorphism or a direct-sum statement after local homological reduction is not automatically a graphic/cographic certificate for the *physical Hamiltonian's check coordinates*. The coordinate maps and all additional local relations must be retained.

The main replacement is not simply the informal full tensor-product thickening. The paper distinguishes its intuitive four-step variant from the main two-step perturbation/replacement construction. A matroid calculation on the intuitive variant, or on a small arbitrary parity-history toy, cannot establish CSW applicability or non-applicability for the main memory theorem.

The BDL outlook says its metacheck matrix is not LDPC, excluding the hypotheses of the earlier initialization result discussed there. This does **not** exclude CSW. A single global dependency can be arbitrarily high weight and still be represented by a graph cycle; CSW v4 explicitly treats the 2D toric code as 0-graphic. No inference from metacheck weight alone to large Delta is valid.

I found no BDL citation or explicit classification in CSW v4, and no CSW reference in BDL v1. That absence is not evidence that their conditions fail or that a new result has priority.

## Why a full Gibbs sampler suffices for unknown-qubit loading

The actual quantum CSW chain randomizes logical degrees of freedom, so running it directly on the unknown logical input is unsuitable. This does not invalidate it as a comparator for loading:

1. Run the full Gibbs sampler on an auxiliary register (or use its classical stabilizer simulation).
2. Read or compute its syndrome, obtaining the required Gibbs syndrome law.
3. Encode the unknown qubit coherently into the zero-syndrome code space.
4. Apply the inverse of the specified decoder's syndrome representative, to place that unknown qubit in the corresponding thermal syndrome sector with the intended logical frame.

No unknown input is measured in this reduction. The classical syndrome law is the resource supplied by the sampler. A generic linear-algebra Pauli representative must be aligned with the BDL decoder's logical frame; an arbitrary representative can differ by a logical Pauli.

This costs the full sampling runtime, classical linear algebra, a physical encoding circuit, syndrome-dependent Pauli application, geometry/routing, and whatever error-protection assumptions are permitted during writing. Global CSW updates are not a passive cooling protocol, but the proposed loading task also permits paid control. Nonlocality alone is therefore not a fair reason to discard the comparator if polynomial routing overhead is allowed.

## The concrete algebraic gate for the selection

For the specified BDL construction, one must do at least one of the following:

- Construct graph couplings g_{X,k}, g_{Z,k} satisfying Definition 10 with Delta=O(k)=O(log N), tracking how every physical check coordinate changes under R_X and R_Z; then use CSW.
- Prove a lower bound on the required Delta that excludes the stated corollary, while remembering that this would not prove CSW itself mixes slowly.
- Establish a direct mixing theorem for CSW on these matrices without the graphic/cographic criterion.
- Build another sampler and state honestly that CSW applicability remains an unresolved alternative, rather than claiming an established advantage.

The first is a real possible shortcut, not merely a literature formality. The current evidence does not decide which branch holds.

## Stronger comparator: regular-matroid approximate counting already gives sampling

Goldberg and Jerrum, *A polynomial-time algorithm for estimating the partition function of the ferromagnetic Ising model on a regular matroid*, SICOMP 42 (2013), 1132–1157, arXiv:1010.6231v2, Theorem 1, give an FPRAS for

    Z_tilde(M; 2, gamma) = sum_{S subset E} gamma_S 2^{-rank_M(S)}

when a binary matrix representing the regular matroid M is supplied, with arbitrary nonnegative rational element weights gamma_e. Primary full text: https://arxiv.org/html/1010.6231v2 ; DOI https://doi.org/10.1137/110851213 . CSW v4 expressly points to this result while conjecturing rapid CSW mixing for regular matroids; the conjecture concerns that particular dynamics, not existence of any efficient sampler.

For a classical code Hamiltonian H(x)=-sum_e J_e(-1)^{h_e x} with J_e>=0, put gamma_e=exp(2 beta J_e)-1 and let M be the column matroid of h^T. Expanding each local factor gives

    Z_H = exp(-beta sum_e J_e) 2^n Z_tilde(M;2,gamma).

The joint Edwards–Sokal law can be sampled by first drawing S with probability proportional to gamma_S 2^{-rank_M(S)}, then drawing x uniformly from ker(h_S). This second step is ordinary GF(2) elimination.

Here is the explicit counting-to-sampling reduction. After some inclusion/exclusion decisions, the conditional random-cluster law is that of a deletion/contraction minor M'. For the next element e, its two unnormalized branch weights are

    a = gamma_e 2^{-rank_{M'}({e})} Z_tilde(M'/e;2,gamma),
    b = Z_tilde(M'\\e;2,gamma).

The inclusion probability is a/(a+b); rank({e}) is 0 for a loop and 1 otherwise. Regularity is closed under both minor operations. Use the FPRAS for the two weights with relative log-error O(epsilon/|E|), and amplify its failure probability to O(epsilon/|E|). Sequential coupling bounds total variation error by O(epsilon). The total runtime is polynomial in matrix size, epsilon^{-1}, and the bit lengths of the rational weights. Fixed low beta has no growing weight-bit cost; rational approximations to exp(2 beta J_e)-1 can be chosen so that accumulated Gibbs-law error is O(epsilon).

Consequently, proving that both physical BDL check matroids are **regular** would already give polynomial approximate full Gibbs sampling, followed by the unknown-input thermal-loading reduction above. One does not also need to prove CSW rapid mixing or Delta=O(log N). The route is an inference from the cited FPRAS plus the displayed self-reduction, not a theorem stated about BDL in either paper.

This strengthens the unresolved algebraic gate: the audit should test regularity (or proximity to regularity) as well as approximate graphicness. No proof of BDL regularity or nonregularity has been obtained here. A new polymer compiler cannot be advertised as beating the strongest existing general method before this route has been handled.

Accuracy convention matters. This direct FPRAS reduction costs polynomial in epsilon^{-1}; the CSW mixing bound has logarithmic dependence on its final total-variation error. The regular-matroid route therefore closes fixed-error or inverse-polynomial-error ideal loading if regularity holds. It need not close polynomial-time loading with exponentially small error. Such a stronger accuracy demand needs its own operational justification: an initial trace-distance error remains at most that error under every subsequent CPTP storage channel, so a long storage lifetime at fixed target error does not require exponentially accurate initial loading.
