# Connected-source construction by extracting positive singleton noise

2026-11-02. This continues—not replaces—the protected normalized-column bound. It gives an exact linked-source expansion and a constructive forest route for **one marked source column per clock**. Applying it to arbitrary overlapping multi-clock operator insertions still requires the source-molecule dictionary specified at the end. The counterterm K^-2 candidate is not used.

## A. A real obstruction to the wrong normalization

Actual one-source weights can be exponentially small for purely phase reasons. For an ideal Poisson background of intensity lambda, let two sources each contribute -1 to every event. Then

`R(1)=R(2)=exp(-2lambda)`, `R(1,2)=1`,

so `kappa(1,2)/(R(1)R(2))=exp(4lambda)-1`.

This ideal gas satisfies background KP trivially. Thus a polynomial bridge bound relative to **actual singleton weights** is false. The correct weights are conservative scalar-pressure-normalized source envelopes. The example has |kappa(1,2)|<=1 and does not obstruct that envelope.

## B. Exact effective source representation

Fix a finite set S of distinct source clocks and their full pinned trajectories omega_i. Source-column amplitudes and direct source–source factors are kept outside the background gas. Let T denote a connected cluster in the ORIGINAL background rod expansion, with complex integrated weight w(T), including all its trajectory labels. Define

`B_i(T)=0` if any rod of T uses source clock i;

otherwise `B_i(T)=product_(r in T) h(omega_i,r)`.

Here h is the exact modulus-at-most-one trajectory pair factor; it includes all nonzero intervals on source i. Thus |B_i(T)|<=1. Removing source clocks and coupling their fixed histories to the remaining gas gives exactly

`log R(S) = integral w(T) [product_(i in S) B_i(T)-1]`.

This follows by modifying each background rod's activity by its source interaction factors and setting activities on source clocks to zero. The connected background graph coefficient itself is unchanged. Absolute convergence of the background cluster expansion justifies substitution and regrouping.

For |A|>=1, define the source hyperedge potential

`U_A = integral w(T) product_(i in A)[B_i(T)-1]`.

Möbius inversion gives `log R(S)=sum_(nonempty A subset S) U_A`. A cluster T can affect sources only in the closed clock neighborhood of its support, but that support is unbounded: bounded local degree does NOT bound hyperedge arity.

## C. Remove the ONLY large-intensity component before taking absolute values

Separate T into:

1. P: single ordinary NONWINDING rods. Their weights are nonnegative, independent of flux, and their total intensity on clock x is

   `lambda_x = beta integral_0^beta rho_nv(l) dl`.

2. E: everything else—single winding rods, wraps, and all clusters with >=2 rods. Their local absolute weighted intensity is O(beta*J0), not O(beta*M0), by the normalized-source p estimate and the existing weighted KP theorem.

The exponential of the P contribution is the generating functional of an independent positive Poisson process on each clock. This is an exact algebraic representation of that part of log Xi; it is not an assertion that physical rods are independent. Physical exclusion and signs reside in E.

For sources S, multiply by `exp(sum_(i in S) lambda_i)`. This cancels exactly the Poisson no-event factor on each deleted source clock. What remains is

`P(S)=exp{ integral_(single nonwinding rods on clocks outside S)
                     w(r)[product_(i in S) B_i(r)-1] }`.

Since |B_i|<=1 and w(r)>=0,

`|P(S)|<=1`.

Moreover, P(S) factorizes whenever the source-neighborhood intersection graph is disconnected. Each singleton rod lives on ONE clock and can see only sources in its closed clock neighborhood; deletion of that clock is another dependence on the same local neighborhood. Thus the graph G0 has edges between source clocks at clock-graph distance at most two. Direct source–source factors have the same finite-range property and modulus <=1, so including them preserves both facts:

- the base moments M_base(S) have modulus at most one;
- they factorize on disconnected induced subgraphs of G0.

The large Poisson intensity lambda~beta*J0*K disappears entirely from these two bounds. No estimate exp(lambda) is used.

The replacement of finite-beta lambda by beta*h_nv costs only the already-bounded nonwinding tail. Alternatively retain lambda exactly throughout; then the bare source measure gets `exp(-lambda)` instead of `exp(-beta*h_nv)`.

## D. Base connected cumulants: finite dependency graph, not a small interaction expansion

Define base cumulants algebraically by partition Möbius inversion. The usual dependency-graph cumulant proof uses only bounded moments and factorization across disconnected induced graphs; it does not require positivity of the moment functional. Applied to the preceding two properties, it bounds a cumulant on S by a universal constant to the power |S| times the sum of spanning trees of G0[S]. In a standard normalization one may use the familiar `2^(|S|-1)` tree factor; using a larger universal constant does not change any parameter conclusion here.

This is the needed saturation mechanism. Arbitrarily strong singleton-Poisson sign effects are treated as bounded finite-range dependence, not exponentiated weak bridges. For maximum clock degree D, G0 has degree at most O(D²), independent of K if D is fixed.

Primary reference for the dependency-graph / cumulant-tree framework: Valentin Feray, https://arxiv.org/abs/1605.03836 . The applicability to complex algebraic moment families should be justified by its combinatorial proof (factorization plus moment bounds), rather than claiming a positive probability measure exists for all source amplitudes.

## E. Residual hyperedges have ONLY O(beta J0) row intensity

Apply the formula for U_A only to residual clusters E. Let n(T) be the number of rods in T. There are at most D*n(T) possible distinct source-clock locations affected by T. Fix a root source clock i and a positive source-cardinality weight a. Since |B_j-1|<=2,

`sum_(A contains i) exp(a|A|) |U_A|`

` <= 2 exp(a) integral_(T affects i) |w(T)| [1+2exp(a)]^(D*n(T))`.

This is a conservative trajectory-uniform bound, independent of source pin times. Pay the displayed factor using a stronger per-rod cardinality weight

`kappa >= D log[1+2exp(a)]`

in the background KP proof. This means choosing eta small enough for that strengthened `Dbar=D exp(kappa)`; it is a real resource/constant cost and must not be hidden. Add any desired spatial-decay weight separately.

The weighted residual root norm is bounded by the same calculation as before:

`L = O_D,kappa( beta*J0 + beta*p_weighted + weighted_wrap )`

`  = O_D,kappa(beta*J0)`

in the admitted cold regime, since p_weighted/J0=O(Dbar eta²). The winding singleton has total intensity <=beta*J0. Finite-beta tails may be retained explicitly. Crucially the positive nonwinding singleton intensity beta*M0 is NOT included in L.

Therefore residual singleton hyperedges U_{i} cost at most exp(L) per source. All remaining residual hyperedges have size >=2 and a weighted row norm at most L.

## F. Exact linked expansion and the forest operation

For fixed source paths, write

`M(S)=M_base(S) * exp[sum_(A subset S) U_A]`.

Expand the base moment by its cumulant partition formula,

`M_base(S)=sum_(partitions pi of S) product_(B in pi) kappa_base(B)`.

Expand each residual hyperedge factor as `exp(U_A)=1+f_A`. In the full source generating function, the exponential formula now selects exactly the configurations for which the union of:

- base cumulant blocks, and
- selected residual hyperedges

connects all source labels. This is an exact linked-source expansion, not an inference from a bound on untruncated moments.

For the absolute estimate, replace each base cumulant block by its finite-range spanning-tree majorant. Replace `|f_A|` by `exp(u_A)-1`, u_A=|U_A|. DO NOT then bound the remaining graph sum by exp(sum |f_A|); that would introduce an unnecessary second exponential.

Instead use

`1+|f_A| <= exp(u_A)`.

The positive hypergraph sum can be viewed as independent hyperedge selection with probability `p_A=1-exp(-u_A)`, multiplied by `exp(sum_A u_A)`. The latter is at most `exp(L|S|)`. Connectivity can then be bounded by extracting an exploration hyperforest. Each selected connecting hyperedge costs at most `p_A<=u_A`, not exp(u_A). Base finite-range tree edges contribute a fixed O(D²) branching factor. Extra subsets encountered in a hyperedge exploration are paid by the source-cardinality weight exp(a|A|), taking a comfortably larger than log 2.

This yields the standard rooted hyperforest recursion: after absorbing fixed finite-range edge stability and residual stability into the single-source envelope Q, convergence follows from a sufficient condition of the form

`Q * C [1+degree(G0)+L] < 1`,

where

`Q = q_bare * exp[C degree(G0)+C L]`.

Universal constants can be made explicit by selecting a fixed exploration ordering; no parameter-dependent exponential other than exp(O(L)) is required. The key combinatorial operations have been identified: base cumulant partitioning, hyperedge expansion, stability extraction, and connected exploration. A final theorem statement should give the chosen exploration/counting convention rather than quote the schematic sufficient constant C as optimized.

## G. Integrating the source paths and resource statement

The finite-beta scalar-normalized bare source-column trace is bounded by

`K exp[beta(J0+delta_beta)]`

per occupied clock, times source endpoint / local-operator decomposition factors. This is the UNTILTED source transfer bound; residual and Poisson interactions were handled above rather than charged again as e^(a_source). Consequently, the forest condition admits a scale

`q(v) = C_dictionary * K^(b_c) * exp[C_D beta J0 b_c] * beta*v`

with additional polynomial branching factors in D, beta*J0, and source support size. Here b_c is the number of affected/deleted clocks per microscopic source, and C_dictionary includes the actual l1 norm overhead of its Pauli/matrix-unit decomposition.

This is polynomial in K only with b_c, D, and the dictionary overhead appropriately controlled. A generic clock-local physical perturbation can become a hook touching O(K) clocks after dressing; then K^(b_c) is not polynomial in K. Nevertheless removing the unnecessary exp(beta*J0*K*b_c) self-pressure cost remains a material improvement.

## H. Remaining gate for the actual generic-V compiler

The column lemma assumes distinct marked clock columns. Generic perturbations can pin several clocks simultaneously, and several insertions can share a column. Before claiming the full compiler theorem:

1. Group source insertions into connected source molecules under shared clock supports, retaining their exact ordered-time simplex and matrix-unit sums.
2. Assign each occupied clock once, so its finite-beta nonwinding singleton pressure is canceled once, not once per insertion.
3. Include the physical V-support hyperedges in the base dependency structure; charge their size and dictionary l1 overhead explicitly.
4. Verify that the source dictionary leaves every unaffected clock's reference flux unchanged and introduces only the audited local modulus-at-most-one pair factors.
5. Supply the explicit rooted hyperforest counting lemma/constants for the chosen molecule measure, with spatial/filling weights needed by the downstream robustness theorem.

The exact linked-source representation and removal of the beta*M0 exponential are constructive progress. Until this molecule/exploration bookkeeping is written and checked, retain the full generic-perturbation admission as CONDITIONAL, not as a theorem inferred from the earlier fixed-support moment bound.
