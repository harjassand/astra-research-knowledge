# General commuting repetition: heterogeneous concentration and the entropy frontier

Research dossier — 6 November 2026, Australia/Brisbane.

## 1. Strongest result and scientific disposition

This round obtains a **heterogeneous weighted-threshold theorem**, extending the pinned commuting reconstruction mechanism from identical repetitions to independent products of different games. The squared gaps of the individual games accumulate. The result permits a quantified amount of weighted failure, rather than requiring every test to succeed.

Let (G_1,ldots,G_N) be finite two-player games, let

\[
 \epsilon_i=1-\omega_{\rm co}(G_i),\qquad
 S=\sum_i\epsilon_i^2,\qquad
 Z=\sum_i\epsilon_i\mathbf1\{\text{loss in coordinate }i\}.
\]

For disjoint-block predicates, including ordinary one-way projection predicates, the extension gives, for every joint commuting strategy and (0<r\le1),

\[
 \boxed{\Pr\{Z\le(1-r)S\}\le
 \exp[-2^{-85}r^5S].} \tag{1}
\]

More generally the exponent is divided by (1+C_0) when the presentation charge defined below obeys (\kappa_i\le C_0\epsilon_i). A separate weighted greedy argument gives the stronger all-wins estimate

\[
 \boxed{\omega_{\rm co}(G_1\otimes\cdots\otimes G_N)
 \le\exp\!\left[-\frac{2^{-75}}{1+C_0}
                       \sum_i\epsilon_i^2\right].} \tag{2}
\]

**Dependency status:** these game statements are proved extensions **relative to the pinned exact finite-tracial resolvent, fine-measurement, local-history and operational sampler lemmas**. Their original mathematical status is preserved. The new finite-probability theorem, once its explicit scalar premise (9) is supplied, is unconditional and has a complete proof below. This round checked the load-bearing production interfaces and independently challenged the extensions; it did not replace the entire inherited sampler proof with an external certification. Lin's finite-table density is a primary mathematical import.

The strongest obstruction is also precise. No bounded universal constant can guarantee a low-mass, sufficiently accurate positive acceptance filter for **every** near-perfect tested instance. The failure persists at positive game gap and bounded tested-event probability. Classical common-information machinery supplies the decisive lower bound. This does **not** disprove general quadratic commuting repetition.

The obstruction has a constructive repair: independent question-free nuisance registers cancel exactly from the **entropy increments**, even when their optimal positive-factor masses grow exponentially. Direct increments therefore contain information discarded by endpoint mass bounds. The next substantial operation is an answer-free entropy allocation for genuinely question-correlated strategies, or an adaptive semantic reduction achieving its effect.

General quadratic repetition for arbitrary predicates, optimal threshold rates, an efficient finite-matrix implementation, and a new physical capability were **not** established. Historical priority of the broader commuting extensions is not settled by this search. Several important restrictions of the statements are already established machinery, as detailed in §8.

## 2. Sources, independence and exact inherited capital

The governing repository was checked at upstream revision
`d4718a92e3a0f5e1fa49cb09bb10d0acf68ae461`.
All fourteen selected governing proof files were verified identical to the local source cache, whose checkout is `377e86be0b69c91c611824f561ca96bdf3e34aad`.
The older weighted-mass proofs themselves pin `0451552424b4679fa9a73faf5849ea5a4af21cf6`; that historical dependency is retained.

The Astra connector was not exposed among this turn's available tools. Retrieval therefore used the local indexed repository, exact indexed proof passages and the corresponding current GitHub contents. Cards were navigation aids; the underlying proof passages were read. [Proof pins](commuting-repetition-record/source-pins/UPSTREAM_PROOF_PINS.json) record the current revision and hashes.

Exactly three GPT-6.1 Sol researchers at maximum reasoning worked initially independently, alongside the principal's independent investigation. Their frozen reports are [machinery](commuting-repetition-record/initial/machinery.md), [constructor](commuting-repetition-record/initial/constructor.md), [auditor](commuting-repetition-record/initial/auditor.md), and [principal](commuting-repetition-record/initial/principal.md). Later cross-challenges and corrections are retained separately. An initial proposal later disproved has not been rewritten to conceal that change.

The governing internal proof records are:

| Interface | Exact source and SHA256 | Role used here |
|---|---|---|
| R | `resolvent_production.txt`, `2acf3c9e5d067de16c873e16bf0fbe52e6becdd47c6db55a3fd526ac086e8627` | Operator Jensen gap, exact norm identities, finite scalar compression, fine POVM transport |
| H | `history_production.txt`, `0893936c7ab79d8a5b3fac87af28a90e4e7e9b45d52bd23b20d4b94629f02475` | Local posterior laws, question drift, finite shared history coupling |
| E | `near_perfect.txt`, `55c2956bb771d630307639a4fd5ff46ea772b484985499dcd765d34f9183cbce` | Same-protocol rare-losing-event estimate and ordered limits |
| S_actual | `sampler_original.txt`, `f37b03a0a84487328c4d1b96b30bbc03468e085bef5593a635126775310beb2b` | Actual all-input amplified left/right POVMs, synchronized-vector and bad-branch bounds |
| W | `N443_WEIGHTED_MASS.txt`, `9710eeb55748208212cc6e61317a16e0c667bae6162cdbd582597beb3fb43f94` | Positive-functional masses retained before log-sum |
| W+ | `ROOT_WEIGHTED_MASS_REFINEMENT.txt`, `10d17bb56009a173cb3b4807e5fca58fb9b3eb5728b3baeac3a10dbd4b453250` | Disjoint-block/projection scope and its limitations |

The original general rate remains exactly

\[
 \omega_{\rm co}(G^{\otimes n})
 \le\exp[-2^{-75}\epsilon^3n/(\epsilon+\log(|A||B|))]. \tag{3}
\]

It concerns finite binary-predicate two-player games, arbitrary joint question distributions within a round, independent rounds, arbitrary commuting Hilbert-space strategies, and no matrix-dimension or efficiency assertion. The later mass refinement gives a source-dependent quadratic rate for disjoint-block masks. This round does not relabel either as a new discovery.

The inspected source chain treats a finite von Neumann algebra as potentially infinite dimensional. Its correlation sampler produces complete unconditional POVMs on an amplified resource; it is not a trace-preserving local channel preparing an arbitrary requested state on the original algebra. Its rare-event estimate is stronger than ordinary total variation. For a losing effect, squared good-vector error plus bad-branch probability (F) gives loss at most (\alpha+2\sqrt{\alpha F}+F). That estimate must hold for the same protocol used in the history construction.

## 3. A reusable coordinate-budget theorem

### 3.1 Models and predicate presentation charge

A finite game is (G=(X,Y,A,B,\mu,V)), with finite nonempty alphabets, a probability law (\mu) on (X\times Y), and (V\in\{0,1\}). A commuting strategy consists of a unit vector and two finite POVM families commuting between players for every pair of questions. Its value is the supremum payoff. No optimizer is assumed. The product game draws question pairs independently with law (\prod_i\mu_i), but each player's measurement may depend on its entire question string.

For every supported question pair of (G_i), choose an **exact fractional rectangle partition**

\[
 V_i(x,y,a,b)=\sum_k w_{i,xy,k}
              \mathbf1_{R_{i,xy,k}}(a)\mathbf1_{T_{i,xy,k}}(b),
 \qquad w_{i,xy,k}\ge0. \tag{4}
\]

Exact equality, including at losing cells, is required. This is a partition identity, not merely a cover. Let (A_i(x,y),B_i(x,y)\ge1) bound its maximum row and column loads:

\[
 \sum_{k:a\in R_k}w_k\le A_i(x,y),\qquad
 \sum_{k:b\in T_k}w_k\le B_i(x,y).
\]

Define

\[
 a_i=\mathbb E_{\mu_i}A_i,\quad b_i=\mathbb E_{\mu_i}B_i,
 \qquad \kappa_i=\tfrac12\log(a_ib_i). \tag{5}
\]

All logarithms in this dossier are natural. The charge is a property of the chosen predicate presentation and partition; it is **not invariant under strategically irrelevant answer padding**. It may be minimized over the finite family of supported rectangles. This entails no efficient algorithm claim.

A simpler symmetric parameter is the smallest maximum local load (\rho(V_{xy})\), with (\rho\ge1), giving (\kappa=\log\mathbb E_\mu\rho(V_{xy})). Asymmetric partitions can improve it. For the three-edge (2\times2) mask, a row-star partition has loads ((1,2)), whereas the minimum balanced load is (3/2).

Disjoint unions of vertex-disjoint complete bipartite blocks admit loads one. Every ordinary projection (V_{xy}(a,b)=\mathbf1\{\pi_{xy}(a)=b\}) qualifies: group the rows by their common projected answer. Injectivity is unnecessary. A mask with no winning cells uses the convention (A=B=1).

### 3.2 Production of individual charges

Fix a product strategy and a proper tested set (D\subsetneq[N]), with actual event (E_D) that all its coordinates win. Write (p=\Pr(E_D)>0), (L=\log(1/p)), and (J=[N]\setminus D).

In a finite-tracial realization, use the inherited fixed exposure

\[
 \Omega_j=(X_D,Y_D,X_{J,\le j},Y_{J,>j}).
\]

Conditionally on a flag under the **original** product referee law, the full Alice and Bob question strings are independent. Each live position uses its own kernel (\mu_i(x\mid y)) or (\mu_i(y\mid x)). The exposure identity does not require identical games or a product law within a question pair.

For each live (i), R gives unnormalized ideal/local vectors (v_i,u_i,z_i), the exact local fine POVMs, and coordinate errors (e_{u,i},e_{z,i}). The norm-marginal identities and each coordinate's total mass are exactly those in H, with total mass **(p)**. The normalized ideal law (Q_i) is the original event-conditioned coordinate/history/fine-answer law.

For positive contractions (F,H) put (\chi(F,H)=\tau(\sigma F\sigma H)). With (h=\chi(F,H)), (g=\chi(I,H)), scalar Jensen for the normalized positive functional gives

\[
 -\chi(F\log F,H)\le h\log(g/h).
\]

Zero masses are interpreted by continuity. Weighted log-sum then gives 

\[
 -\sum_k w_k\chi(F_k\log F_k,H_k)\le p\log(G_B/p),
 \quad G_B=\sum_k w_k\chi(I,H_k), \tag{6}
\]

and the transposed estimate uses (G_A). Products of (4) preserve the tested event, its mass and **every** live fine-answer measure. At a fixed tested-question string the local loads multiply. Averaging under its unconditioned law gives

\[
 G_A\le\prod_{j\in D}a_j,\qquad G_B\le\prod_{j\in D}b_j.
\]

The resolvent Jensen-gap telescope therefore supplies

\[
 \sum_{i\in J}e_{u,i}\le p\left[L+\sum_{j\in D}\log b_j\right],
 \quad
 \sum_{i\in J}e_{z,i}\le p\left[L+\sum_{j\in D}\log a_j\right].
\]

Either naming of the two orientations gives the same sum. The event-conditioned full question density is at most (1/p); relative entropy to a product dominates the sum of its coordinate marginal divergences. Consequently, for (d_i=D(Q_i^{X_iY_i}\Vert\mu_i)), (\sum_{i\in J}d_i\le L). Set

\[
 t_i=(e_{u,i}+e_{z,i})/p+d_i.
 \quad\text{Then}\quad
 \sum_{i\in J}t_i\le3L+2\sum_{j\in D}\kappa_j. \tag{7}
\]

Apply H with **one mode** for each fixed (i). Its local law discrepancy is at most ((1+1/\sqrt2)\sqrt{t_i}), the squared descriptor discrepancy at most (16t_i), and the ideal alignment error at most (4t_i). E and S_actual give a legal single-game strategy of loss at most

\[
 \alpha_i+K\big(\sqrt{\alpha_i}\,t_i^{1/4}+\sqrt{t_i}\big)+o(1),
 \quad K=65536,
 \quad\alpha_i=\Pr(\text{loss at }i\mid E_D). \tag{8}
\]

For each (i), its one resource is fixed over all its own input/history pairs, including mismatched histories. Different (i)'s may use different resources: these are separate existence statements, not a simultaneous physical preparation. The source compression preserves ideal masses and fine tables exactly; its positive error tends to zero at fixed finite family and (p>0). Coefficient mass can make the necessary accuracy severe. No uniform dimension or time bound follows.

### 3.3 Eliminate representation-dependent errors before Lin

Define the continuous function

\[
 \Phi_K(\epsilon,\alpha)=
 \left[\frac{\sqrt{\alpha+4(\epsilon-\alpha)_+/K}-\sqrt\alpha}{2}\right]^4.
\]

Writing (z=t^{1/4}) in (8), and using the base value as a lower bound on any legal strategy's loss, gives (z^2+\sqrt\alpha z\ge(\epsilon-\alpha)_+/K). Therefore (t\ge\Phi_K(\epsilon,\alpha)). Summing (7), after taking inner accuracies to zero, proves the finite-table statement

\[
 \boxed{\sum_{i\notin D}\Phi_K(\epsilon_i,\alpha_i(D))
 \le3\log(1/p_D)+2\sum_{j\in D}\kappa_j.} \tag{9}
\]

This is the reusable interface. Lin's Theorem 3.2 applies to the full finite product table. At the fixed event with (p_D>0), its probabilities and conditional losses converge; conditional error is at most a constant times table error divided by (p_D). Continuity of (\Phi_K) transfers (9) to arbitrary commuting strategies. **The raw (t_i), state vectors and algebras are not asserted to converge.** The tested set is chosen only after this uniform scalar result has been established.

For (D=[N]), assign its empty-live assertion the trivial value (0\le3\log(1/p_D)+2\sum_D\kappa_j) whenever (p_D>0). No extraction is needed. Zero-probability events will always receive zero weight below.

The exact R/H/S_actual input requirements are thus visible: positive exact tested-factor identities; original one-coordinate norm masses and fine-answer laws; a summed, unaveraged Jensen-gap budget; local fresh-question histories; and the actual rare-event comparison. A mean-TV-only sampler, approximate event mass, or matrix-density assertion would not supply (9).

## 4. Complete heterogeneous concentration proof

**Theorem (finite scalar form).** Let arbitrary correlated (W_i\in\{0,1\}), numbers (\epsilon_i\in[0,1]), (\kappa_i\ge0), and (K\ge1) obey (9) for every proper tested set of positive probability. Suppose (\kappa_i\le C_0\epsilon_i). Put (S=\sum_i\epsilon_i^2) and (Z=\sum_i\epsilon_i(1-W_i)). If (S>0), then for (0<r\le1),

\[
 \Pr\{Z\le(1-r)S\}\le
 \exp\!\left[-\frac{r^5S}{2^{21}K^4(1+C_0)}\right]. \tag{10}
\]

The assertion holds for every finite (N\ge1), without a limiting-length argument. When (S=0) the corresponding upper bound is one.

**Proof.** For a tested set (D) let (S_D=\sum_{i\notin D}\epsilon_i^2), (A_D=\sum_{i\notin D}\epsilon_i\alpha_i(D)), and (M_D) denote the right side of (9). Put (t_i=\Phi_K(\epsilon_i,\alpha_i)) and (\alpha'_i=\min(\alpha_i,\epsilon_i)). The quadratic root defining (\Phi_K) gives

\[
 \epsilon_i\le\alpha'_i+
 K(\sqrt{\alpha'_i}\,t_i^{1/4}+\sqrt{t_i}).
\]

Multiply by (\epsilon_i), sum, and use Hölder and Cauchy–Schwarz:

\[
 S_D-A_D\le
 K\left[S_D^{3/4}M_D^{1/4}+\sqrt{S_DM_D}\right]. \tag{11}
\]

The cap on (\alpha_i) is essential. Without it, the first Hölder estimate would be unjustified. For an empty live set both sides before the error term are zero.

For (u>0), independently include (i) in a random tested set with probability

\[
 q_i(u)=\frac{u\epsilon_i}{1+u\epsilon_i}.
\]

Let (\nu_u(D)) be its law, and define

\[
 F(u)=\sum_D\nu_u(D)p_D
     =\mathbb E\prod_i(1+u\epsilon_i)^{-(1-W_i)}>0,
 \qquad L(u)=-\log F(u). \tag{12}
\]

Condition the joint outcome/subset experiment on every selected test winning. Its subset law is (w_u(D)=\nu_u(D)p_D/F(u)); its outcome law is the original law tilted by the product in (12), denoted (T_u). Given the outcome, a loss is never selected, and a winning coordinate is selected with probability (q_i(u)). Thus

\[
 \mathbb E_{w_u}A_D=\mathbb E_{T_u}Z,\quad
 \mathbb E_{w_u}S_D\ge(1-u)S,\quad
 \mathbb E_{w_u}\sum_{j\in D}\kappa_j\le C_0uS. \tag{13}
\]

For the second inequality, the removed squared-gap mass is at most (\sum_iq_i\epsilon_i^2\le u\sum_i\epsilon_i^3\le uS). The third uses (q_i\le u\epsilon_i). The exact entropy identity

\[
 \mathbb E_{w_u}\log(1/p_D)
 =L(u)-D(w_u\Vert\nu_u)\le L(u)
\]

implies (\overline M(u)\le3L(u)+2C_0uS). Average (11), using (S_D\le S) and concavity of the roots, to obtain

\[
 \mathbb E_{T_u}Z\ge(1-u)S
 -K\left[S^{3/4}\overline M(u)^{1/4}
                       +\sqrt{S\overline M(u)}\right]. \tag{14}
\]

The finite generating function is differentiable, and

\[
 L'(u)=\mathbb E_{T_u}\sum_i
       \frac{\epsilon_i(1-W_i)}{1+u\epsilon_i}
       \ge\frac{\mathbb E_{T_u}Z}{1+u}. \tag{15}
\]

In particular (L) is nondecreasing and (L(0)=0). Fix (r) and put (\lambda=r^4/[2^{20}K^4(1+C_0)]). At every (0\le u\le\lambda) with (L(u)\le\lambda S),

\[
 \overline M(u)/S\le(3+2C_0)\lambda
                 \le3r^4/(2^{20}K^4).
\]

The normalized error in (14) is bounded by

\[
 (3^{1/4}/32)r+(\sqrt3/(1024K))r^2<r/16.
\]

Also (\lambda\le r/16). Hence (14)–(15) give (L'(u)\ge(1-r/4)S) on that region. If (L(\lambda)\ge\lambda S), then certainly (L(\lambda)\ge(1-r/4)\lambda S). Otherwise monotonicity keeps (L(u)<\lambda S) throughout the interval; integrating the derivative gives the same conclusion.

On (Z\le(1-r)S), (\log(1+\lambda\epsilon_i)\le\lambda\epsilon_i) implies that the product in (12) is at least (e^{-\lambda(1-r)S}). Therefore

\[
 \Pr\{Z\le(1-r)S\}
 \le e^{\lambda(1-r)S-L(\lambda)}
 \le e^{-3r\lambda S/4}\le e^{-r\lambda S/2},
\]

which is (10). No original-coordinate independence was used. Full tested sets contribute zero live mass; events of probability zero have zero posterior weight. ∎

Applying §3 with (K=2^{16}) proves (1) and its charged version. For identical block games and (\delta=r\epsilon), it yields

\[
 \Pr\{W\ge\lceil(1-\epsilon+\delta)N\rceil\}
 \le\exp[-2^{-85}\delta^5N/\epsilon^3]. \tag{16}
\]

An independently checked homogeneous factorial-moment argument improves the constant to (2^{-77}), without improving the exponents. That derivation is retained in the constructor's initial report; the heterogeneous mechanism is the substantive advance here. The old wrapper's singleton-answer branch cannot be repurposed simply by replacing its alphabet logarithm with zero.

### A sharper all-wins consequence

Let (t_0=1/(256K^4)=2^{-72}). If (\alpha\le\epsilon/2), then (\Phi_K(\epsilon,\alpha)\ge t_0\epsilon^2): substituting (t<t_0\epsilon^2) into (8) would give a loss-to-gap ratio at most (1/2+1/(4\sqrt2)+1/(16K)<1).

For a fixed product strategy of all-wins probability (\theta>0), start with (D=\varnothing) and add a positive-gap coordinate whenever its current conditional loss exceeds (\epsilon_i/2). If (L_\theta=\log(1/\theta)), each addition increases (\log(1/p_D)) by more than (\epsilon_i/2). Hence

\[
 \sum_{j\in D}\epsilon_j\le2L_\theta,\quad
 \sum_{j\in D}\epsilon_j^2\le2L_\theta,\quad
 \sum_{j\in D}\kappa_j\le2C_0L_\theta.
\]

If all positive-gap coordinates are exhausted, (S\le2L_\theta). Otherwise (9) at termination gives

\[
 t_0(S-2L_\theta)\le(3+4C_0)L_\theta.
\]

Thus (L_\theta\ge t_0S/(3+4C_0+2t_0)), which implies (2). Zero-gap components can be discarded for this upper bound by sampling their omitted question pairs as shared randomness. Taking the supremum requires no attained optimizer. This completes the product proof.

### Robust scope and semantic preprocessing

If non-block question pairs have probability at most (\eta_i), with balanced load at most (R_i), then

\[
 \kappa_i\le\log[1+\eta_i(R_i-1)].
\]

Therefore (\eta_i(R_i-1)\le C_0\epsilon_i) is sufficient. Compare this with the simpler operation of declaring exceptional predicates automatically winning: it gives a block-game gap at least (\epsilon_i-\eta_i). The load theorem adds scope when exceptional mass is comparable to or larger than the gap, while its charge-to-gap ratio remains bounded. It should not be presented as a new mechanism in the regime already covered by deletion.

Local answer reductions can be applied first. If local maps (\pi_x,\rho_y) send every G-winning pair to an H-winning pair, then (\omega_{\rm co}(\bigotimes G_i)\le\omega_{\rm co}(\bigotimes H_i)). If local lift maps send every H-winning pair back to a G-winning pair, all these values are equal. Both claims follow by deterministic coarse-graining/postprocessing of complete commuting POVMs. Thus nuisance padding can be removed before applying the charge theorem. These reductions are elementary, not an invented new theory of games.

## 5. Sharp obstruction to positive-mass reconstruction

### 5.1 What the positive-factor mechanism can guarantee

A finite Boolean mask has a mass-one exact positive factorization uniformly over all tested strategies **if and only if** its nonisolated bipartite components are complete bicliques with disjoint vertex sets. More strongly, outside that class even a uniform subexponential mass guarantee is impossible for global factorizations of tensor powers.

For necessity, a non-block mask contains the three-edge submatrix (T=\left(\begin{smallmatrix}1&1\\0&1\end{smallmatrix}\right)), obtained from a shortest path between a nonadjacent row and column in one connected component. For any exact bounded positive factorization (M=\sum_k\lambda_kf_kg_k^\top), with local marginals (P,Q), put (G_A=\sum_k\lambda_kP(f_k)), (G_B=\sum_k\lambda_kQ(g_k)). Standard nuclear-norm factorization gives

\[
 \|D_P^{1/2}MD_Q^{1/2}\|_*
 \le\sum_k\lambda_k\sqrt{P(f_k)Q(g_k)}
 \le\sqrt{G_AG_B}. \tag{17}
\]

The first bound uses (f_k^2\le f_k), (g_k^2\le g_k) and the rank-one nuclear norm. With uniform active marginals on the two rows/columns, (\|T/2\|_*=\sqrt5/2); nuclear norm tensorizes exactly. A classical strategy sharing a uniform equal bit string has those marginals, diagonal joint law and tested success (p=1). Restricting any full-mask factorization to the active answers proves

\[
 \max(G_A,G_B)\ge(\sqrt5/2)^t. \tag{18}
\]

Arbitrary joint factorizations across all (t) coordinates are covered. Sufficiency for block masks follows by grouping the disjoint blocks, giving sums of local effects at most identity. The balanced local partition parameter has a sharp gap: it is one for block masks and at least (3/2) otherwise; the three-edge mask attains (3/2). These are consequences of established positive-factor/nuclear machinery applied to this exact interface, not a claim to have invented that machinery.

For the principal's separate crown fixture, let (m\ge2) be even, (M(a,b)=\mathbf1\{a\ne b\}), with uniform marginals. Every exact bounded positive factorization of (M^{\otimes t}) satisfies

\[
 \inf\max(G_A,G_B)=[2(1-1/m)]^t. \tag{19}
\]

Indeed each supported rectangle has disjoint row/column projections at each coordinate, so its normalized support product is at most (4^{-t}). If (x=P(f)), (y=Q(g)), then (xy\le2^{-t-1}(x+y)). Integrating the exact mask identity, whose accepted mass is ((1-1/m)^t), proves the lower bound. Equality follows by uniformly averaging (S\times S^c) over all balanced subsets of ([m]), with total coefficient (4(m-1)/m), and tensoring that partition.

Large masses do **not** imply large actual entropy increments: a constant exposure can have zero increment. Nor do these fixtures give lower bounds against general quadratic repetition. Their strategic nuisance can be removed.

### 5.2 A robust common-information obstruction

Let (R_m) be uniform on unequal ordered pairs in ([m]^2), (m) even. Its Wyner common information is the known scatter/task-assignment formula

\[
 C_W(R_m)=\log[4(1-1/m)],
 \quad I(R_m)=\log[m/(m-1)]. \tag{20}
\]

The first is due to Cuff–Permuter–Cover, not a discovery of this round. A direct proof useful here is short. In any conditional product component avoiding equality, the two supports are disjoint, so their entropy sum is at most (2\log(m/2)). Subtract from the uniform joint entropy (\log[m(m-1)]). Balanced complementary supports attain equality. The same argument works for arbitrary global product decompositions of (R_m^{\otimes t}), giving (tC_W(R_m)).

The following quantitative, context-conditional bound is proved here for application to filters; its independent historical priority is unestablished. Suppose a target law is (Q_C\otimes R_m^{\otimes t}), and an actual law is within total variation (\beta\le1/m). If (U^t,V^t) are independent given (C,K), then, with binary entropy (h),

\[
 I(K;U^tV^t\mid C)\ge
 t\{\log[4(1-1/m)]-2h(\tfrac12\sqrt{m\beta})-2\beta\log m\}
 -h(\beta). \tag{21}
\]

**Proof.** Collision probability at any coordinate is at most (\beta). Given (C,K), let its two marginal vectors be (p,q). Their affinity is at most (\sqrt{m\sum_ap_aq_a}). A fair binary selector between (p) and (q) has discrimination error at most half that affinity. Binary Fano and (H((p+q)/2)\le\log m) give

\[
 H(p)+H(q)\le2\log m-2\log2+2h(e).
\]

Average over (C,K), use Cauchy–Schwarz and concavity to bound mean (e) by (\tfrac12\sqrt{m\beta}). Conditional independence and entropy subadditivity bound (H(U^tV^t\mid C,K)). Meanwhile classical conditional-entropy continuity yields

\[
 H(U^tV^t\mid C)\ge t\log[m(m-1)]-2t\beta\log m-h(\beta).
\]

This continuity bound is independent of the size of (C): use a maximal coupling of the two joint laws, split on its mismatch event of probability at most (\beta), and charge at most (log|mathcal U^t\times\mathcal V^t|) on the mismatch. Subtract the conditional entropies. ∎

For a prefilter law (\nu(c)P_c(a)Q_c(b)), consider any bounded positive filter with exact decomposition (\widetilde\theta_c=\sum_k\lambda_{c,k}f_{c,k}g_{c,k}\in[0,1]), mass (p'>0), and averaged one-sided masses (G_A,G_B). Set (x_{c,k}=P_c(f_{c,k})), (y_{c,k}=Q_c(g_{c,k})). Its product-component weights are (\nu(c)\lambda_{c,k}x_{c,k}y_{c,k}/p'). Component divergence to the prefilter local laws is at most (-\log x-\log y); the chain rule and Jensen give

\[
 I(K;AB\mid C)+\mathbb E_C D(R'_{AB\mid C}\Vert P_CQ_C)
 \le\log(G_AG_B/p'^2). \tag{22}
\]

For example (\mathbb E_w(1/y)\le G_A/p'); zero-mass terms can only weaken this bound. Hence a near-scatter target with (eta) of order (1/(8m)) forces (log\max(G_A,G_B)\ge\log p'+ct) for a positive constant (c). The limiting coefficient in braces in (21) is

\[
 \log4-2h(1/(4\sqrt2))=0.4533534\ldots>0.
\]

### 5.3 Positive-gap tested instances: a universal filter shortcut fails

Use the binary line game of length (L), whose commuting gap is (\epsilon=1/(2L-1)). Kempe–Regev's classical lower bound gives a strategy on (N=L^2) rounds with all-wins probability bounded below. Greedy testing supplies (D_0), (|D_0|=O(1/\epsilon)), tested probability bounded below, and remaining conditional loss at most (\epsilon/2).

Append (t=m=2L) independent dummy rounds, all tested, using the line game's optimal constant-answer base strategy. Their base success probability ((1-\epsilon)^t) stays bounded below. Add nuisance answers in ([m]) to the game and require inequality of the two nuisance answers. On the dummy rounds use independent uniform nuisance symbols; elsewhere use a deterministic distinct accepted pair. Forgetting the nuisance answers and appending a fixed accepted pair prove that the enlarged game has exactly the original commuting gap and all product values.

The resulting tested event has (p\ge c_*>0), (|D|=O(1/\epsilon)), and live conditional loss at most (\epsilon/2). Conditional on the original exposure context its dummy nuisance law is (R_m^{\otimes t}). Now demand a replacement filter with unnormalized error at most (\epsilon p/8) and masses at most (B). Normalization changes the conditional table by at most (\beta=\epsilon/8). Here (m\beta\to1/8), (p') remains bounded below, and (21)–(22) force

\[
 B\ge\exp[\Omega(1/\epsilon)]. \tag{23}
\]

It is therefore **false** that every such tested instance admits a relative-accurate positive filter with (B\le\exp(c\epsilon|D|)), for any fixed universal (c). The conclusion allows arbitrary global filter factorizations and changing posterior context marginals. It uses growing nuisance alphabets. Allowing (c) to grow with the game is not excluded.

This disproves the universal acquisition proposal in the constructor's frozen initial report. Its implication *if such filters exist, then quadratic repetition follows* remains valid. It does not rule out choosing another tested set, semantic retraction, a representation without classical separator labels, or direct entropy increments.

## 6. Constructive repair: independent nuisance entropy cancels

**Proposition.** Suppose the tested finite-tracial construction is a tensor product of a base strategy and an independent nuisance strategy whose state, tested mask and answer POVMs are independent of every referee question. Use product positive factorizations. If their tested masses are (p_b,p_\nu>0), then the exposure entropy potentials satisfy

\[
 U_j^{\rm aug}=p_\nu U_j^b+p_bU^\nu,
 \qquad Z_j^{\rm aug}=p_\nu Z_j^b+p_bZ^\nu, \tag{24}
\]

where (U^\nu,Z^\nu) are independent of the exposure stage. Thus every increment scales by (p_\nu), and division by (p_bp_\nu) gives the **base** normalized entropy budget.

**Proof.** Coarse factors have form (F_j\otimes F_\nu,H_j\otimes H_\nu). For (f(t)=t\log t), (f(0)=0), joint functional calculus gives

\[
 f(A\otimes B)=f(A)\otimes B+A\otimes f(B).
\]

The identity extends to kernels by continuity. The positive bilinear form factors, so insertion into the potential gives the first term (p_\nu U_j^b) and a second term equal to (U^\nu) times the **flag-averaged** base mass. R's exact mass identity makes that averaged mass (p_b) at every stage. No per-flag constancy is asserted. The transpose proves the (Z) identity. Taking differences proves the proposition. ∎

R bounds the actual resolvent squared errors by these increments. Its fine-POVM transport in the augmented algebra still preserves the complete live table; the transported POVMs need not factor. The question posterior also satisfies

\[
 P(\text{questions}\mid E_b\cap E_\nu)
 =P(\text{questions}\mid E_b).
\]

Hence its divergence cost is bounded by (\log(1/p_b)). Finite compression accuracy may worsen, but its error is sent to zero at fixed positive augmented mass. All independent padding obstructions above are repaired **without changing their actual event**. Their mass and common-information lower bounds remain true, showing why those bounds are not lower bounds on the relevant entropy increments.

The proposition requires literal independent tensor structure. It does not remove answer charges from a general strategy with question-correlated workspace. Proving an appropriate conditional or operator-valued replacement is the decisive missing step.

## 7. Best streamlined proof of the inherited theorem

The clean proof spine is unchanged in substance, but the present accounting removes unnecessary assumptions:

1. Work first in finite-tracial standard form. Use one fixed prefix/suffix exposure; random exposure and a falsely input-independent posterior history are unnecessary.
2. Use the resolvent feature (T(T+s)^{-1}), whose squared integral is (T). Its Jensen gap controls squared vector changes. Regularize zero spectrum; removing a kernel alone does not make an operator boundedly invertible.
3. Preserve exact masses and fine-answer laws in finite auxiliary compression. Bound the **sum** of the coordinate alignment costs. Retain the actual one-sided masses before weighted log-sum; use presentation loads only when necessary, and direct increments when they cancel.
4. Couple the input-dependent local histories under fresh questions. Apply the actual all-input sampler. Pay law drift and mismatch outside the rare-loss square-root term.
5. Remove representation-dependent errors into a continuous scalar table inequality, then apply Lin at fixed positive tested mass. Only afterward select tested coordinates.
6. Use greedy testing for all wins, or sparse successful-subset tilting for thresholds.

For a general mask, singleton accepted-pair factors recover the original answer charge and hence (3). Disjoint blocks remove it. The heterogeneous extension needs no new operator sampler; its new operations are individual charge retention, scalar elimination before closure, weighted greedy selection and sparse subset tilting.

An alternative proof architecture comes from Jain's conditional-relative-entropy/marginal-replacement method. Its finite-dimensional theorem is a serious comparator, but a general finite-von-Neumann transfer still needs its four-operator estimate, continuous-zero-spectrum inverse-power control, and compatible local standard-form purification corrections. Moreover its parent budget still contains the checked-answer charge: transferring it alone would give another cubic proof, not solve general quadratic repetition.

## 8. Verified machinery and novelty audit

The following entries state the imported part, hypotheses and actual applicability. Detailed source checks are in the machinery reports; no absence-of-search-hit is treated as priority clearance.

| Primary source | Exact usable result and applicability |
|---|---|
| Lin, *Tracially embeddable strategies*, arXiv:2304.01940v3, Definition 3.1, Theorem 3.2 | For finite input/output sets, tracial standard-form correlation tables have (\ell_1)-closure (C_{qc}). Applies to a fixed finite product table and then (9) by scalar continuity at (p>0). Supplies neither matrix density nor convergence of descriptors. [Source](https://arxiv.org/html/2304.01940v3#S3). |
| Kempe–Regev–Toner, *Unique Games with Entangled Provers are Easy*, arXiv:0710.0655v3, SDP 3, Lemma 5.7, Theorems 5.2 and 5.5 | Existing quadratic **unique-game** machinery already extends to commuting strategies and heterogeneous products, as proved just below. This restriction of (2) is not new. [Source](https://arxiv.org/html/0710.0655v3#S5). |
| Dinur–Steurer, *Analytical approach to parallel repetition*, author version 10 June 2014, Theorems 3.3, 4.1 and Claim 2.3 | Product collision norm and relaxed-value comparison already yield heterogeneous quadratic **classical projection** products. Version numbering differs from arXiv; do not use a search snippet's theorem number/formula. [Author paper](https://www.dsteurer.org/paper/productgames.pdf). |
| Dinur–Steurer–Vidick, arXiv:1310.4113v2, Theorem 1 and Lemmas 6–8 | Multiplicative relaxed tensor projection value and rounding yield mixed products with a universal gap power at most 12; expanding cases are stronger. A commuting finite-von-Neumann rounding transfer is an additional operation, not supplied by correlation closure. [Source](https://arxiv.org/html/1310.4113v2). |
| Lin, *MIPco=coRE*, arXiv:2510.07162v1, Definition 9.1, Theorem 9.3 / A.1 | The specific anchored transformation has bound (16\epsilon^{-1}\exp[-c\epsilon^{17}n/\log(|A|+1)]). It changes the game. It does not directly bound the original unanchored product. Theorem 1.1 already identifies (\mathsf{MIP}^{co}=\mathsf{coRE}); that classification is not a new consequence here. [Source](https://arxiv.org/html/2510.07162v1). |
| Song, ECCC TR26-199, Theorems 1.1 / 4.6, Lemma 4.1 | General cubic tensor repetition and smooth-label sampling precede this round. The tracial/opposite-algebra event protocol is the additional inherited step. [Primary paper](https://eccc.weizmann.ac.il/report/2026/199/download/). |
| Jain, arXiv:2610.21410v1, Theorem 1.1, Corollary 5.2, Lemmas 4.1–4.2 | Finite-dimensional tensor cubic repetition and (\delta^5/(\epsilon^2L)) thresholds via conditional relative entropy. Does not itself acquire a commuting standard-form theorem or remove the answer charge. [Source](https://arxiv.org/html/2610.21410v1). |
| Culf, arXiv:2603.14746v1, Theorem 6.1 | Near-perfect nondegenerate projection strategies, including commuting strategies, round to tracial ones with loss at most (148(L\epsilon)^{1/4}), (L) the inverse least supported conditional question probability. On a repeated game (L) can grow exponentially, so this is not the needed uniform product theorem. [Source](https://arxiv.org/html/2603.14746v1#S6). |
| Braverman–Minzer, arXiv:2610.30455v1, Theorem 1.3, Lemma 2.3 | Multiplayer classical XOR repetition and tensorized contradiction/gluing machinery give an independent comparison route. Their exact commuting-embedding condition and player-increasing transformation are not automatically a two-player quantitative commuting-gap compiler. [Source](https://arxiv.org/html/2610.30455v1). |
| Kempe–Regev, arXiv:0911.0201v1, Definition 3.1, Theorems 3.2 and 4.4 | Binary line-game classical and no-signaling base values coincide; commuting lies between them. Its classical repeated strategy supplies the quadratic-rate obstruction and the positive-gap filter fixture. [Source](https://arxiv.org/html/0911.0201v1). |
| Cuff–Permuter–Cover, *Coordination Capacity*, IEEE TIT 56(9), 4181–4206 (2010), Example 7 / Theorem 10; Cuff, *Distributed Channel Synthesis*, §II-H, (44) | The scatter common-information formula (20) is established. The finite-support product and entropy assumptions are exactly those used in §5. The operational channel-synthesis theorem is not imported as a nonlocal quantum protocol. [Original paper](https://isl.stanford.edu/~cover/papers/2010coordination.pdf), [scatter formula](https://arxiv.org/html/1208.4415#S2.SS8). |
| Fawzi–Parrilo, arXiv:1210.6970v2, §2.3 (7), Theorem 4; Watts, EJC 13 (2006), R74; Pinto, arXiv:1307.6363v2 | Nuclear factorization, fractional exact biclique partitions and local biclique load are established machinery. Our exact interface estimates are proved directly in §5, so no unverified specialized import is needed. [Fawzi–Parrilo](https://arxiv.org/html/1210.6970v2), [Watts](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v13i1r74), [Pinto](https://arxiv.org/html/1307.6363v2). |

**KRT applicability proof.** For commuting projective measurements on an arbitrary Hilbert space, the finite vectors (P_a^x\psi,Q_b^y\psi), realified, satisfy SDP 3 and reproduce the payoff. Finite POVMs can be projectivized in separate ancillas with operator coefficients from the respective commuting algebras. Thus (\omega_{co}(G)\le s(G)), the SDP value. Lemma 5.7 gives an actual finite tensor strategy of value at least (1-2\sqrt{2t}-4t) when (s(G)=1-t). For (\epsilon=1-\omega_{co}(G)), this forces (s(G)\le1-\epsilon^2/16). Indeed (t<\epsilon^2/16) would make (2\sqrt{2t}+4t<(1/\sqrt2+1/4)\epsilon<\epsilon).

The strictly feasible bipartite SDP product theorem and the product-game relaxation inclusion then imply

\[
 \omega_{co}(\bigotimes_iG_i)
 \le\prod_i s(G_i)\le\prod_i(1-\epsilon_i^2/16)
 \le e^{-\sum_i\epsilon_i^2/16}
\]

for unique games. No equality of tensor and commuting correlation sets is used. The genuinely broader target of this round is projection/disjoint-block and charged non-block products, with the inherited interfaces explicitly retained.

The common-information formula, basic nuclear norm, biclique LP, SDP products, greedy conditioning, and entropy inequalities are predecessors. The current contributions are the checked coordinate-budget extension and scalar-before-closure organization; the sparse-test heterogeneous weighted concentration deduction; the robust filter-interface obstruction; and exact independent-nuisance increment cancellation. Their historical novelty beyond the comparisons above remains unestablished. The initial individual reports document independent rediscovery of some established facts and the subsequent corrections.

## 9. Decisive remaining problems and constructive attacks

1. **General quadratic commuting repetition.** Prove an answer-free conditional information allocation for a suitably selected near-perfect event, or a comparably strong product relaxation. Exact positive-mask masses cannot be the universal invariant. Theorem (24) supplies a nontrivial case where direct increments succeed despite those obstructions.
2. **Semantic, conditional entropy subtraction.** Extend (24) from independent tensor nuisance to question-correlated redundant workspace. A candidate must identify a local sufficient object, preserve the full fine-answer laws and keep all inputs in one valid local algebra. Conditional relative entropy and standard-form recovery are promising machinery; the actual local correction remains to be proved.
3. **Adaptive relative reconstruction.** The all-tested-sets filter target is false. A theorem selecting a tested set jointly with a semantic quotient is still viable. It must be invariant under the line/crown padding counterexample and charge relative error at the rare-event scale, rather than only absolute TV.
4. **Fully heterogeneous intrinsic rate.** Without a bounded ratio (\kappa_i/\epsilon_i), (9) still holds, but this round does not prove (\exp[-c\sum_i\epsilon_i^3/(\epsilon_i+\kappa_i)]). Tested-coordinate information affects other coordinates; replacing the maximum ratio by an average, or multiplying upper bounds for separate groups, is unjustified. A new weighted or multiscale allocation is needed.
5. **Optimal thresholds.** For independent near-optimal coordinate play, the binomial KL scale is a necessary ceiling; the line family separately obstructs a universally better-than-quadratic all-wins gap rate. The fifth-power deviation in (10) is not shown optimal. Seek a stronger rare-event reconstruction, not an unsupported substitution in an old formula.
6. **Alternative cubic proof and effective resources.** A correct standard-form transfer of Jain's marginal-replacement method could simplify the inherited architecture. It does not alone improve its gap exponent. Separately, explicit finite compression/sampling costs and a named verifier application are required before claiming algorithmic or physical benefit.

There is no new quantum-PCP result, constant-locality Hamiltonian compiler, general multiplayer theorem, or new (\mathsf{MIP}^{co}) classification. Product sampling does not furnish a useful question-chain gap; product-algebra strategies form only a subclass of arbitrary joint repeated measurements.

## 10. Ledger, checks and retained record

| Statement | Final status |
|---|---|
| Original general cubic and later block quadratic commuting capital | Preserved at exact pinned scopes and original dependency status |
| Coordinate budget (9), with asymmetric averaged loads and heterogeneous games | Proved relative to the named R/H/S_actual production; Lin import checked |
| Weighted concentration (10) from (9), all finite lengths | Proved scalar theorem; game application retains those dependencies |
| Sum-of-squared-gaps all-wins theorem (2) | Proved with the same game dependencies |
| Unique-game quadratic and mixed-product restriction | Application of existing KRT machinery, not a new discovery |
| Uniform subexponential exact positive mass outside block masks | Disproved by (17)–(18) |
| Universal bounded-charge relative filters on all near-perfect instances | Disproved by (21)–(23), for bounded universal charge constant |
| Independent nuisance direct-increment cancellation | Proved under literal product state/POVM and question-free nuisance hypotheses |
| Correlated nuisance subtraction, general quadratic repetition, optimal thresholds | Open |
| Efficient finite matrices, physical advantage, historical priority | Not established |

The complete independent reports, exposed challenges and proof checks are in [the supporting record](commuting-repetition-record/INDEX.md). Exact-rational diagnostics check sparse-subset normalizers, posterior identities and derivatives on correlated four-coordinate laws, including zero/unit gaps; nuclear witnesses, small-mask classifications and rectangle support bounds were checked independently. These support orientation and arithmetic; the all-(N) and all-tensor-power conclusions follow from the proofs, not finite enumeration.

No public repository, manuscript, Zenodo record or website was changed in this research round.
