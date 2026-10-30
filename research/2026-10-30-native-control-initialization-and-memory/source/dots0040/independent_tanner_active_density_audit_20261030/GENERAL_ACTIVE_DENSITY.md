# A quantitative active-hub theorem for the GPT potential decoder
2026-10-30. NEW CONSTRUCTION, awaiting independent hostile review. This supersedes the *open-step status* of PARTIAL_CONSTRUCTION.md, not any accepted memory theorem.

## Result
Fix the GPT quantum Tanner-code family with sufficiently large fixed local degree Delta and its robustness/expansion constants. Let e be stabilizer-reduced and satisfy the small-error bound used by GPT Theorem 10. A hub v in V0 union V1 is active when some subset of Q(v) strictly decreases the GPT integer potential U. Then

  g_active(e) >= kappa_GPT U(e),
  kappa_GPT = c_Y/[2 Delta^2(1+c_Y)],
  c_Y = alpha/(16 Delta K),
  alpha = delta^2/648,
  K = 1+3 Delta^2.

K may be replaced by any bound on a closed one-hop ball in the hub-overlap graph. The constants are conservative and independent of blocklength. Delta must be sufficiently large for GPT's estimates with this chosen alpha and beta_exc=772/alpha; this is permitted by the family construction. For U=0 the assertion is trivial.

The proof does NOT assume e is globally metastable or globally low-overlap. Its key new observation is that INACTIVITY OF ONE HUB gives precisely the local metastability and low-overlap facts needed near that hub. It therefore avoids a hypothetical global repair of the configuration.

## Primary inputs, with precise scope
Reference: Gu–Pattison–Tang, https://arxiv.org/html/2206.06557 . Use their Definitions 16,24,25,28,31 for c_v,R_v^+,R,Y,y, exceptional/normal vertices and dense edges; the graph mixing estimates used in Lemmas 29 and 33; dual-tensor robustness; and the algebraic local-view analysis of Section 4.2.2. The calculations below explain why its latter hypotheses hold on the selected patch without global metastability. FGL candidate mass is not used.

Each qubit is incident to exactly two V1 potential terms. Each Q(v) has Delta^2 qubits. The local base code has distance at least delta Delta. The needed error-size bound is

  |e| <= delta n/(6 Delta^(3/2-eps)),
  n=Delta^2 |V1|/2.

For a confinement/memory application one should use the SMALLER guaranteed correction radius from GPT Theorem 12/Corollary 14, not confuse it with this existence radius.

## 1. Local reversal lemma, without global metastability
Choose arbitrary nearest c_v and R_v^+=e_v+c_v. Suppose a qubit q belongs to two endpoint corrections. Flipping q lowers each of its two local potentials by exactly one, so it is an improving singleton.

Consequently, if a hub a is inactive, every q in Q(a) belongs to at most one endpoint correction. Let F be any subset of R intersect Q(a). Define candidate corrections after flipping F by

  R'_v = R_v^+ XOR (F intersect Q(v)).

They return the modified local error to the SAME c_v. Each flipped edge was in exactly one endpoint correction: its candidate correction weight falls by one there and rises by one at the other endpoint. Summing the candidate weights gives U(e), so U(e XOR F)<=U(e). Hub inactivity gives the reverse inequality. Equality forces every R'_v to be locally minimum. All nearest c_v can therefore be kept unchanged, and the union R stays unchanged: the unique correction incidence of each q in F reverses endpoints.

This proof requires disjoint correction incidence ONLY ON F. Any overlaps elsewhere are irrelevant. It is the local version of the R-flipping fact needed below.

## 2. An inactive V1 hub has low overlap
Let v in V1 be inactive. By the preceding lemma all correction incidences on Q(v) are disjoint. Suppose some local codeword c has |R_v intersect c|>|c|/2. Flip F=R_v^+ first. Inactivity and the local reversal lemma imply unchanged potential, unchanged nearest codewords and unchanged R, with the new outgoing correction at v empty.

Next flip F'=R_v intersect c. Every qubit of F' is now in the correction of its OTHER V1 endpoint, so those neighbors' total potential falls by |F'|. At v a valid correction is F' XOR c, of weight strictly less than |F'|. Thus U falls overall. The combined mask F XOR F' is still a subset of Q(v), contradicting inactivity.

Therefore every inactive V1 hub has the full local low-overlap property, regardless of what happens elsewhere in the system.

## 3. Bounds on Y which hold for arbitrary e
Let A be the set of all active hubs, g=|A|, and Y={v in V1:c_v!=0}. Since c_v is nearest and zero is an available codeword,

  |c_v|<=2|e_v|.

The local distance gives |e_v|>=delta Delta/2 for v in Y. Summing, with each error qubit counted twice,

  |Y|<=4|e|/(delta Delta)
      <=|V1|/(3 Delta^(1/2-eps)).                    (1)

This replaces GPT's use of global low-overlap to obtain its small-|Y| mixing regime.

Every y-edge has both endpoints in Y, directly from y=e minus R. Define Y_e by |y_v|>Delta^(3/2+eps)/2 as in GPT. Expander mixing between Y_e and Y, using (1), yields

  |Y_e|<=q_e |Y|,     q_e=576/Delta^(1+2eps).        (2)

Indeed the lower edge count is (1/2)Delta^(3/2+eps)|Y_e|, whereas the upper count is at most (1/3)Delta^(3/2+eps)|Y_e|+4Delta sqrt(|Y_e||Y|). Rearranging gives (2). Neither step needs metastability or low overlap.

Also every error qubit has an endpoint in Y OR is an improving singleton: if both endpoint nearest codewords were zero, it would belong to both endpoint corrections. Such a singleton lies in the local view of an active V1 hub. Therefore

  |e|<=Delta^2(|Y|+g),
  U(e)<=2|e|<=2Delta^2(|Y|+g).                      (3)

## 4. Dense-edge counting using only inactive normal vertices
If g>=|Y|/4, we already have a linear g-versus-|Y| bound stronger than the one claimed. Otherwise assume g<|Y|/4. Choose Delta large enough that q_e<=1/4 and define

  Y_* = Y minus (Y_e union (A intersect V1)).

Then |Y_*|>=|Y|/2. Every v in Y_* is inactive and normal, so Section 2 supplies low overlap locally. Consequently its nearest codeword has weight at most 2|y_v|<=Delta^(3/2+eps), and the local robustness conclusion gives at least one dense edge. All dense-edge facts below are used ONLY for these good originating vertices.

Let D_* be the dense edges originating in Y_*, and W their V0 endpoints. Each v in Y_* contributes at least one, and every w has total degree 2Delta. Thus

  |D_*|>=|Y|/2,       |W|>=|Y|/(4Delta).            (4)

For w in W choose its originating v in Y_*. Local low overlap at v and local robustness imply that w has at least delta Delta/2-Delta^(1/2+eps)/delta neighbors in Y. Applying the same mixing inequality as GPT Lemma 33, with (1), gives

  |W|<=81|Y|/(delta^2 Delta).                       (5)

It follows that the average D_*-degree of W is at least delta^2 Delta/162, which is at least 2alpha Delta for alpha=delta^2/648. Since the maximum degree is 2Delta, at least an alpha/2 fraction of W have at least alpha Delta D_*-edges.

Using (1),(2),(4) in the mixing estimate between W and Y_e gives, for sufficiently large Delta,

  |E(W,Y_e)|<=193 Delta^(1/2-eps)|W|.

Markov counting with beta_exc=772/alpha removes at most alpha|W|/4 vertices having more than beta_exc Delta^(1/2-eps) exceptional neighbors. Hence at least

  alpha |W|/4                                    (6)

vertices w have BOTH many dense edges from Y_* and few exceptional Y_e neighbors.

## 5. Localize the case-3 contradiction
Form the hub-overlap graph: v,w are adjacent when Q(v) intersects Q(w). A closed one-hop ball has at most K=1+3Delta^2 hubs, since each of the Delta^2 incident faces has only three other vertices. Let B=N[A] be the union of these closed balls. Then |B|<=Kg.

Suppose a special w from (6) lies outside B. Then w is inactive and every V1 neighbor of w is inactive. Thus:

(a) every correction incidence on Q(w) is disjoint, by singleton inactivity at w;
(b) every neighboring V1 view has low overlap, by Section 2;
(c) every normal neighboring V1 view has the required local robust-code decomposition;
(d) w has at least alpha Delta good dense edges and at most beta_exc Delta^(1/2-eps) exceptional neighbors;
(e) no subset of Q(w) decreases U, by inactivity.

These are exactly the LOCAL hypotheses needed in GPT Section 4.2.2. Its row/column split uses (a). Its change e->e minus (e intersect R_w) uses the LOCAL reversal lemma from Section 1; global disjointness outside Q(w) is never required. All ensuing potential differences are supported on Q(w) and involve only its neighboring V1 views. Their normal-view approximations use (b),(c); their exceptional corrections use (d). The no-improvement inequalities use (e), including after the zero-cost first flip because the combined mask remains in Q(w).

The resulting local estimates produce a stabilizer supported on Q(w) which strictly lowers |e|, contradicting that e is reduced. All degree requirements are the finite inequalities in that local argument with our fixed alpha,beta_exc, and can be enforced by taking fixed Delta sufficiently large.

Therefore EVERY special w in (6) belongs to B. Equations (4),(6) give

  Kg >= alpha |W|/4 >= alpha |Y|/(16Delta),
  g >= c_Y |Y|,   c_Y=alpha/(16Delta K).             (7)

The alternative g>=|Y|/4 also implies (7), since c_Y<=1/4. If Y is empty, (3) already gives the desired conclusion directly.

Finally combine (3),(7):

  U(e)<=2Delta^2(1+1/c_Y)g,

which proves the stated kappa_GPT.

## 6. What this does and does not establish
This supplies the active-hub multiplicity missing from a direct reading of GPT Theorem 10. It is a new robust/localized extraction from that proof, not a theorem quoted from GPT and not an independently accepted result yet.

With complete read-neighborhood separation, one may apply it to each small reduced component exactly as in the prior container construction. GPT's local energy is syndrome-computable; unary local-energy tokens can provide bounded bit changes and confinement at a linear-in-n cutoff. Those interface/lift steps are separate and should be audited before asserting exp(O(n)) coherent-memory lifetime.

The parallel mismatch decoders in arXiv:2208.05537 and arXiv:2306.12470 are alternative routes, but their state and potential were not silently substituted for this syndrome-only GPT algorithm.

## Audit targets
1. Local reversal lemma: only flipped qubits need unique endpoint correction incidence.
2. Local high-overlap contradiction at an inactive V1 hub.
3. Y-size bound from nearest-codeword minimality rather than low overlap.
4. Restrict dense-edge origins to Y_*, while keeping full Y and Y_e in mixing estimates.
5. Section 4.2.2 uses no global metastability beyond (a)-(e) on the chosen patch.
6. Choose Delta large enough for the modified fixed alpha,beta_exc; retain GPT's code-family/robustness assumptions.
