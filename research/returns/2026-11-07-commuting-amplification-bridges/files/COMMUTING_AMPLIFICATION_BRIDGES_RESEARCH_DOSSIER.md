# Commuting repetition: reconstruction, quadratic projection amplification, and noisy information flow

Research dossier — 7 November 2026, Australia/Brisbane.

## 1. Strongest results actually obtained

This round completes a new proof of the **charged coordinate reconstruction condition** that the existing paper left as Hypothesis \(\mathrm{FR}(K)\). It gives a substantive simplification: the old resolvent production and the separate posterior-history construction are unnecessary. The replacement uses conditional relative entropy, one common refined target, two separate one-sided comparison states, and explicit polar corrections in a common finite von Neumann algebra. It retains the standalone operational correlated sampler and Lin's finite-table closure.

The strongest amplification consequence is:

**Theorem A — quadratic commuting repetition for disjoint-block games.** Let \(G=(X,Y,A,B,\mu,V)\) be a finite two-player Boolean game. Suppose that, for each supported \((x,y)\), its winning answer graph is a union of vertex-disjoint complete bipartite blocks. Isolated vertices are permitted. Put \(\epsilon=1-\omega_{\mathrm{co}}(G)\). Then

\[
 \boxed{\omega_{\mathrm{co}}(G^{\otimes n})
       \le \exp[-2^{-75}\epsilon^2 n]\qquad(n\ge1).} \tag{A}
\]

This includes noninjective and partial projection predicates. Questions may have an arbitrary joint law within a round; rounds are independent. Strategies may be arbitrary joint commuting strategies on arbitrary Hilbert spaces. There is no dimension, resource-size, or efficiency bound.

There is a **separate tensor theorem with its own gap**
\(\epsilon_*=1-\omega_*(G)\): the same bound holds for \(\omega_*(G^{\otimes n})\) with \(\epsilon_*\). Its proof keeps every algebra finite dimensional, rather than substituting a tensor gap into a commuting theorem.

More generally, the completed reconstruction theorem proves the previous heterogeneous all-wins and weighted-threshold consequences at their displayed charge-to-gap assumptions. Those consequences no longer need an unproved reconstruction hypothesis. It does **not** prove quadratic repetition for arbitrary predicates.

The strongest operational bridge obtained is:

**Theorem B — amplification with interactive noisy quantum communication.** Let \(H\) be any finite Boolean game, including a threshold repetition game, and write \(q_0=\omega_{\mathrm{co}}(H)\). Ordinary finite-dimensional quantum players may share arbitrary prior entanglement independent of the referee questions and communicate through a prescribed finite sequence of fixed memoryless channels \(\mathcal N_1,\ldots,\mathcal N_m\), in either direction, with arbitrary local adaptation. Every cross-player signal is charged. For every \(\alpha>1\),

\[
 \boxed{p_{\mathrm{accept}}
 \le \exp\!\left\{\frac{\alpha-1}{\alpha}
       \left[\log q_0+\sum_j I_\alpha(\mathcal N_j)\right]\right\}.} \tag{B}
\]

Here logarithms and channel information are in nats, and \(I_\alpha\) is the reference-marginal-fixed sandwiched Rényi information defined in §8. The bound is capped at one and may be optimized over one common \(\alpha\). An initial finite-order source correlation cost can be included in the same telescope.

Thus a certified bound \(q_0\le e^{-gn}\) remains exponentially small when the aggregate entanglement-assisted communication-capacity rate is strictly below \(g\), under the precise finite-family memoryless assumptions in §8. Combining this with (A) improves the certified noise/communication budget for block and projection games from the inherited cubic scale to a quadratic scale.

**Scientific disposition.** These are complete mathematical derivations with the independent internal checks recorded below, at the exact named imports and scopes. Neither historical firstness nor a physical or computational advantage has been established. The strongest reusable new proof operation is the pair of one-sided positive comparison states for one common target. Channel Rényi amortization, the relevant trace inequalities, correlated sampling, coding exponents, and several restricted repetition theorems are established machinery and are credited as such.

The transformative endpoints remain unresolved: general quadratic repetition, a useful locality-preserving verifier/Hamiltonian compiler, polynomial-cost cryptographic compilation for growing games, and an implemented capability exceeding matched existing methods. An unrestricted compiler from arbitrary commuting games to explicitly finite Hamiltonian promise problems cannot be obtained merely by strengthening repetition; the computability obstruction in §11 applies.

## 2. Governing capital, independence, and source status

The supplied original result remains intact:

\[
 \omega_{\mathrm{co}}(G^{\otimes n})
 \le \exp\!\left[-2^{-75}
       \frac{\epsilon^3 n}{\epsilon+\log(|A||B|)}\right]. \tag{2.1}
\]

Its original threshold statement is

\[
 \Pr\{W\ge\lceil(1-\epsilon+\delta)n\rceil\}
 \le\exp\!\left[-2^{-78}
       \frac{\delta^5n}{\epsilon^2(\delta+\log(|A||B|))}\right],
 \quad0<\delta\le\epsilon. \tag{2.2}
\]

These are mathematical capital at their governing source scope; there is no matrix-density or efficient-implementation assertion. The original sampler's actual fine-output and rare-event statements were inspected, rather than inferred from a mean total-variation estimate.

The public paper's retained source module [games.tex](commuting-amplification-bridges-record/inherited-source/prior-published-games.tex) explicitly stated its newer charged applications under \(\mathrm{FR}(K)\). The preceding private dossier derived them relative to a longer source-production chain. This round supplies a different complete reconstruction proof, with new dependencies stated below. Earlier artifacts are retained unchanged; their historical conditional wording has not been silently edited.

Upstream main was refreshed to
\[
 \texttt{d4f37ab168f9312707b47709945cb0da5e896f33}.
\]
All fourteen selected governing proof bodies have unchanged hashes relative to the previous verified revision. The Astra connector was not available to the principal; exact indexed local passages and pinned GitHub files were used. The shared indexed checkout and unrelated work were left read-only.

Exactly three GPT-6.1 Sol researchers at maximum reasoning worked initially independently, alongside the principal. Frozen initial reports are [principal](commuting-amplification-bridges-record/initial/principal.md), [machinery](commuting-amplification-bridges-record/initial/machinery.md), [constructor](commuting-amplification-bridges-record/initial/constructor.md), and [auditor](commuting-amplification-bridges-record/initial/auditor.md). Their hashes were checked unchanged after cross-challenge. No additional researchers were spawned.

The [supporting record](commuting-amplification-bridges-record/INDEX.md) preserves candidate stages, exposed challenges, corrections, exact proof details, source pins, and diagnostics. An earlier file saying “candidate” is not retrospectively rewritten; its later disposition is explicit in that index.

## 3. Model and the reusable reconstruction theorem

A commuting strategy uses a unit vector \(\psi\), complete finite POVMs \(P_a^x,Q_b^y\), and
\([P_a^x,Q_b^y]=0\) for every input/output pair. Its payoff is
\(\sum\mu(x,y)V(x,y,a,b)\langle\psi,P_a^xQ_b^y\psi\rangle\).
No optimizer is assumed. In a repeated game each POVM can depend on the entire local question string.

First work in finite-tracial standard form:
\[
 (\mathcal M,\tau),\qquad
 \mathcal H=L^2(\mathcal M,\tau),\qquad
 \sigma\in\mathcal M_+,\quad\tau(\sigma^2)=1.
\]
Alice acts by \(L(a)\xi=a\xi\), Bob by \(R(b)\xi=\xi b\). The right representation is opposite, and commutes with the left representation on every input. The finite von Neumann algebra can be infinite dimensional. Boundedness of \(\sigma\) is part of this starting representation. Subsequent finite amplifications and finite tensor powers preserve that setting.

### 3.1 Conditional comparisons

Let \(\mu\) be a probability law on finite \(X\times Y\), and let \(q\) be supported on its support. Consider bounded unit vectors \(\psi_{xy}\in L^2(\mathcal N)\) in a finite tracial algebra. They determine a copied-input pure family
\[
 \sum_{x,y}\sqrt{q(x,y)}
 |x\rangle_{\widehat X}|x\rangle_X
 |y\rangle_{\widehat Y}|y\rangle_Y\psi_{xy}. \tag{3.1}
\]
Its Alice marginal is classical in \(\widehat Y\); in each \(y\) block its coherent \(x,x'\) entries are
\[
 \sqrt{q(x,y)q(x',y)}\,\psi_{xy}\psi_{x'y}^*.
\]
Matching \(\widehat X=X\) copies are understood.

For any positive normalized seed \(T=[T_{xx'}]\) over \(\mathcal N\), an **Alice conditional comparison** has entries
\[
 (\nu_A)_{y;xx'}
 =\sqrt{\mu(y|x)\mu(y|x')}\,T_{xx'}. \tag{3.2}
\]
The seed's local \(X\) law is arbitrary on the supported symbols. It need not equal \(q_X\). Bob's comparison is defined by reversing the roles and working over the opposite algebra. These are two separately chosen comparisons for the **same target**; they need not be margins of a common reference state.

Let \(K_A=XA\), \(K_B=YB\), including all designated residual workspaces. With finite full divergences, define
\[
 b_A=D(\rho_A\Vert\nu_A)
       -D(\rho_A^{K_A}\Vert\nu_A^{K_A}),\quad
 b_B=D(\rho_B\Vert\nu_B)
       -D(\rho_B^{K_B}\Vert\nu_B^{K_B}). \tag{3.3}
\]
All quantities are relative-entropy differences of finite displayed values. Infinite individual entropies are not subtracted.

### 3.2 Operational reconstruction

**Theorem C — finite-tracial conditional-comparison reconstruction.**
Under the preceding finite-input, bounded-vector, support, comparison-form, and finite-divergence assumptions, fix finite local/opposite fine POVMs and a Boolean losing predicate. Let \(\alpha\) be its mean loss on the target under \(q\). Put
\[
 t=b_A+b_B+D(q\Vert\mu).
\]
For every \(\zeta>0\), there is one shared resource fixed before the inputs arrive and complete commuting POVMs on **every** local input pair, with loss under \(\mu\) at most
\[
 \boxed{\alpha+K\big(\sqrt\alpha\,t^{1/4}+\sqrt t\big)+\zeta,
 \qquad K=65536.} \tag{3.4}
\]
The resource is a finite amplification and finite tensor power of the original finite algebra. It need not be finite dimensional. The construction preserves the declared fine measurement interface, not an output channel onto the original algebra. Its resource parameters can depend on the entire finite family, spectra, and accuracy; there is no uniform size bound.

This is the genuinely reusable statement. Neither a game mask nor a repeated-game structure is needed for it. Its proof follows in §4.

## 4. Proof of Theorem C

### 4.1 Exact marginal replacement at positive faithful slack

Write \(r=\rho_K,n=\nu_K\). For Alice, the supported full algebra is \(\bigoplus_{y:\mu_Y(y)>0}M_{X_y}(\mathcal N)\), \(X_y=\{x:\mu(x,y)>0\}\), with the matching fresh-question copies understood; the retained marginal is block diagonal in \(X\). Bob uses the reversed supported corner. Start with boundedly invertible densities there. Set
\[
 L_s=r^{(1+is)/2}n^{-(1+is)/2},\qquad
 \widetilde\nu=\int_{\mathbb R}\beta_0(s)L_s\nu L_s^*\,ds,
\quad
 \beta_0(s)=\frac{\pi}{2(\cosh(\pi s)+1)}. \tag{4.1}
\]
The integral is normal and all inverse powers are bounded. Its retained marginal is exactly \(r\), since \(L_snL_s^*=r\) pointwise. Because \(K\) is classical in the local question control \(X\), \(L_s\) is \(X\)-block diagonal and commutes with the scalar conditional-amplitude factors in (3.2). Thus \(\widetilde\nu\) remains a conditional comparison. If \(\nu\ge c_\nu I\), \(r\ge c_rI\), and \(n\le M_nI\), then \(\|L_s^{-1}\|\le\sqrt{M_n/c_r}\) uniformly in \(s\), and \(\widetilde\nu\ge(c_\nu c_r/M_n)I\). The following faithful-density arguments therefore apply also to the replacement.

The finite-tracial specialization of Junge–LaRacuente's Theorem 1.2 gives, for positive invertible \(W\),
\[
 \tau e^{\log W+\log r-\log n+\log\nu}
 \le\int\beta_0(s)\tau(WL_s\nu L_s^*)\,ds. \tag{4.2}
\]
The operator order in this formula is essential. Apply their \(p=2\) inequality to half-logarithms and then scalar Jensen; cyclicity removes the endpoint imaginary powers. This is a primary-source trace-inequality import over general von Neumann algebras, not a matrix-approximation argument.

The Gibbs variational formula and (4.2) imply
\[
 b=D(\rho\Vert\nu)-D(r\Vert n)
 \ge \tau(\rho\log W)+1-\tau(\widetilde\nu W).
\]
Taking the supremum is the measured-relative-entropy variational formula, hence
\[
 D_{\mathrm{meas}}(\rho\Vert\widetilde\nu)\le b,\qquad
 F(\rho,\widetilde\nu)^2\ge e^{-b}. \tag{4.3}
\]
Here \(F(a,b)=\|\sqrt a\sqrt b\|_1\) is root fidelity.

The second inequality is valid in finite trace without a dimension assumption. For faithful bounded densities, the positive operator
\[
 H=\rho^{-1/2}(\rho^{1/2}\widetilde\nu\rho^{1/2})^{1/2}\rho^{-1/2}
\]
satisfies \(H\rho H=\widetilde\nu\). Finite spectral partitions of \(H\) have classical fidelities tending to \(\tau(\rho H)=F\); scalar Jensen gives \(D(p\Vert q)\ge-2\log\sum\sqrt{pq}\). This proves the needed fidelity bound. The measured variational formula follows from operator concavity of \(\log\) in one direction and finite spectral step approximations in the other.

Continuous spectrum at zero requires care. Choose a faithful bounded conditional comparison \(\nu_0\) bounded below on the supported corner, and replace
\[
 \rho_\eta=(1-\eta)\rho+\eta\nu_0,\quad
 \nu_\eta=(1-\eta)\nu+\eta\nu_0,\qquad\eta>0. \tag{4.4}
\]
Every positive \(\eta\) permits (4.1)–(4.3). The full and retained divergences converge separately to their finite original values. One direct verification uses uniform continuity of \(u\log u\) on a bounded interval, the bound
\(\log\nu_\eta\ge\log\nu+\log(1-\eta)\), and a fixed regularizer \(\log(\nu_\eta+\delta I)\) for the reverse limiting inequality. The additional \(\eta\nu_0\log\nu_\eta\) contribution is \(O(\eta|\log\eta|)\). Therefore their difference converges too.

Since \(\rho_\eta\to\rho\) in norm, its square roots converge in \(L^2\), uniformly for comparison with any normalized state. Consequently each positive slack admits an actual normal comparison with
\[
 F(\rho,\widetilde\nu_\eta)^2\ge e^{-b}-o_\eta(1). \tag{4.5}
\]
There is no claim that inverse powers converge, that removing a kernel creates a spectral gap, or that the comparison states have a normal limiting point. The positive-slack construction suffices.

### 4.2 One common amplification and genuinely local corrections

Let the Alice replacement seed be \(T\in M_k(\mathcal N)\), \(k=|X|\), and write \(C=\sqrt T\), \(r_x=\tau(T_{xx})\). Use unnormalized matrix trace temporarily. In \(\mathcal P=M_k(\mathcal N)\), define
\[
 \chi_x=r_x^{-1/2}\sum_z e_{1z}\otimes C_{xz},\qquad
 \psi_{xy}^{\rm emb}=e_{11}\otimes\psi_{xy}. \tag{4.6}
\]
The \(\chi_x\) are unit vectors and
\(\chi_x\chi_{x'}^*=e_{11}\otimes T_{xx'}/\sqrt{r_xr_{x'}}\). The column index is the finite purifier.

For fixed \(y\), form
\[
 A_y=\sum_x e_{x1}\otimes\sqrt{q(x,y)}\psi_{xy},\quad
 B_y=\sum_{xz}e_{xz}\otimes\sqrt{\mu(y|x)}C_{xz}. \tag{4.7}
\]
Their left densities are the target and comparison \(y\) blocks. Their fidelity is \(\|A_y^*B_y\|_1\). Polar decomposition supplies \(U_y\) such that
\[
 \operatorname{Re}\tau(B_y^*A_yU_y)=\|A_y^*B_y\|_1.
\]
It acts by **right multiplication on purifier columns**, independently of the external coherent \(x\) row. Expanding this trace and applying Cauchy–Schwarz with the normalized comparison law \(r_x\mu(y|x)\) yields
\[
 e_A:=\mathbb E_q[1-|\langle\chi_x,\psi_{xy}^{\rm emb}U_y\rangle|^2]
 \le b_A+o(1). \tag{4.8}
\]
No equality of the target and comparison \(X\) marginals is used.

The separate Bob comparison bounds the **same target's** variation:
\[
 e_B:=\mathbb E_q P^2(d_{xy},d_y)\le b_B,
\quad d_{xy}=\psi_{xy}^*\psi_{xy},\quad
 d_y=\mathbb E_{x|y}d_{xy}. \tag{4.9}
\]
To see the information step, discard the protected copied question in the full divergence, use the conditional comparison form, and subtract the retained divergence. The remaining expression contains \(I(X:B|Y)\) plus a nonnegative question-law divergence. Then use \(P^2\le D\) in natural units. These finite-classical-record identities do not involve infinite entropies.

Write \(\chi_x=J_xu_x\), \(u_x=|\chi_x|\), and set
\[
 v_y=[U_y^*(e_{11}\otimes d_y)U_y]^{1/2}.
\]
For normalized densities \(a,b\), Hölder with exponents \(4,2,4\) gives
\[
 F(a,b)\le[\tau(\sqrt a\sqrt b)]^{1/2},\quad
 \|\sqrt a-\sqrt b\|_2^2\le2P(a,b)^2.
\]
Contract (4.8) to the right marginals and use (4.9) and the squared triangle inequality:
\[
 \mathbb E_q\|u_x-v_y\|_2^2\le4(b_A+b_B)+o(1). \tag{4.10}
\]

All finite families fit in one finite amplification. Partial polar factors have unitary completions after finite padding; an explicit completion for a partial isometry \(v\) is
\[
 \begin{pmatrix}v&I-vv^*\\I-v^*v&-v^*\end{pmatrix}.
\]
Left and right completions can use separate finite factors. The corrected fine effects are
\[
 A'_x=J_x^*(I\otimes A_x)J_x,\qquad
 B'_y=U_y^*(I\otimes B_y)U_y. \tag{4.11}
\]
They are complete POVMs; support-only versions put the complement into a default output. Trace cyclicity checks the Bob orientation. Every left effect commutes with every right effect on all input pairs. Normalizing the matrix trace rescales all vectors by the same square-root factor, leaving probabilities and estimates unchanged.

### 4.3 Actual sampling, rare loss, and the fresh law

Apply the inspected standalone standard-form sampler to the finite families \(u_x,v_y\) and the transported fine POVMs. Its contract gives actual unconditional POVMs and, for the **same protocol**, a losing-event bound
\[
 \beta_q\le\alpha'+2\sqrt{\alpha'F_0}+F_0.
\]
Its Section 8 gives \(F_0\le896(h^2+\overline D/h^2)+o(1)\), with \(\overline D\le2D_{\rm desc}+o(1)\). For small positive descriptor discrepancy choose \(h=D_{\rm desc}^{1/4}\); at zero discrepancy take positive \(h\downarrow0\), with inner accuracies chosen first at each \(h\). Equations (4.8)–(4.10) then give, with \(s=b_A+b_B\),
\[
 \sqrt{\beta_q}\le\sqrt\alpha+75s^{1/4}+o(1). \tag{4.12}
\]
This uses the sampler's actual good-vector and bad-branch estimates. A mean-TV sampler alone would not justify it.

For its all-input losing function \(f(x,y)\in[0,1]\),
\[
 |\sqrt{\mathbb E_qf}-\sqrt{\mathbb E_\mu f}|
 \le\|\sqrt q-\sqrt\mu\|_2\le\sqrt{D(q\Vert\mu)}. \tag{4.13}
\]
For \(t\le1\), (4.12)–(4.13) imply
\[
 \beta_\mu\le\alpha+152\sqrt\alpha\,t^{1/4}
                         +5776\sqrt t+o(1).
\]
The remaining regimes use the trivial upper bound one. Both coefficients are below \(65536\). Inner accuracies are taken to zero at a fixed finite family and fixed positive event probability. Every requested positive slack has actual complete POVMs and a fixed resource. This proves Theorem C.

The proof replaces the resolvent and separate-history production. It still uses the standalone sampler, whose source hash is
\(\texttt{f37b03a0a84487328c4d1b96b30bbc03468e085bef5593a635126775310beb2b}\).

## 5. The new central construction: one target, two one-sided parents

### 5.1 Exact presentation and charge

For every supported question pair of coordinate \(i\), choose an exact positive fractional rectangle partition
\[
 V_i(x,y,a,b)=\sum_lw_{i,xy,l}
                 {\bf1}_{R_{i,xy,l}}(a){\bf1}_{T_{i,xy,l}}(b),
 \quad w_{i,xy,l}\ge0. \tag{5.1}
\]
Equality includes losing cells. Let \(A_i(x,y),B_i(x,y)\ge1\) bound its maximum row and column loads, and put
\[
 a_i=\mathbb E_{\mu_i}A_i,\quad b_i=\mathbb E_{\mu_i}B_i,\quad
 \kappa_i=\tfrac12\log(a_ib_i). \tag{5.2}
\]
The parameter depends on the chosen presentation. Every finite Boolean mask has such a partition, for example singleton winning cells. Disjoint-block masks have unit loads and zero charge. A projection mask is disjoint-block by grouping rows with the same projected output; injectivity is unnecessary.

Consider an arbitrary finite-tracial joint strategy for an independent product of possibly different games. For a proper tested set \(D\), let \(p=\Pr(E_D)>0\), \(L=\log(1/p)\), and
\[
 \alpha_i(D)=\Pr\{\text{loss at }i\mid E_D\}.
 \tag{5.3}
\]
Fix tested questions \(c=(x_D,y_D)\). Product partitions give one exact mask with weights \(w_{c,l}\) and local load bounds \(A_c=\prod_D A_j(c_j)\), \(B_c=\prod_D B_j(c_j)\).

### 5.2 One pure target with the original complete measured table

Coherently dilate the original full local measurements and retain every fine output on its own side. For live strings \(x,y\) and full fine outputs \(a,b\), write their residual standard-form vector as
\(\sqrt{P_a^{c_A,x}}\sigma\sqrt{Q_b^{c_B,y}}\).
Append three copies of a common label \(l\) on each target side and use amplitudes
\[
 \sqrt{\frac{\mu_J(x,y)w_{c,l}}{p_c}}\,
 {\bf1}_{R_{c,l}}(a_D){\bf1}_{T_{c,l}}(b_D)
 \sqrt{P_a^{c_A,x}}\sigma\sqrt{Q_b^{c_B,y}}. \tag{5.4}
\]
Here \(p_c=\Pr(E_D\mid c)>0\). Orthogonality of all fine-output and label registers plus (5.1) gives norm one and **exactly** the original conditional fine table.

This is a specified mathematical pure target. It is not claimed to arise from a new physically local filter on the original resource. Coherences outside the declared measured table can change. The same target must be used for both comparisons.

One own-label copy stays private in each residual workspace. External copies form the duplicated shared histories, with all such external copies omitted from each comparison parent. Fixing a label leaves a pure target; retaining a cross-created external copy in a reference would invalidate locality and is not done.

### 5.3 Separate one-sided parents and positive operator-matrix domination

Alice's one-sided successful coefficients are
\[
 \sqrt{w_{c,l}/A_c}\,
 {\bf1}_{R_{c,l}}(a_D)\sqrt{P_a^{c_A,x}}.
\]
Their adjoint-products sum to at most identity. Adding the local coefficient
\[
 \left[I-\frac1{A_c}\sum_a
       \Big(\sum_lw_{c,l}{\bf1}_{R_{c,l}}(a_D)\Big)P_a^{c_A,x}\right]^{1/2}
\]
with a distinct failure sentinel completes a local isometry. Copying the sentinel into the external as well as private label records dephases success/failure when the external records are discarded. Bob has a **different** completion using \(B_c\) and \(T_{c,l}\). The two completions are not simultaneously applied. This prevents the erroneous coefficient \(w_l^2\).

There is a simpler normalization. Use each uncompleted positive one-sided seed and divide by its actual trace \(G_{A,c}\) or \(G_{B,c}\). Any normalized positive local seed is allowed by (3.2); its question marginal can differ from the target's. Thus no physical reference-preparation claim is required.

For the exact type-II check, at fixed \(y,l\) set
\[
 Z_{x,a}=\sqrt{\mu_J(x,y)w_{c,l}}\,
          {\bf1}_{R_{c,l}}(a_D)\sqrt{P_a^{c_A,x}}\sigma .
\]
The raw Alice parent is \(S_l=[Z_{x,a}Z_{x',a'}^*]\). The selected target parent is
\[
 T_l=[Z_{x,a}Q_{y,T_l}Z_{x',a'}^*],
 \quad Q_{y,T_l}=\sum_{b:b_D\in T_{c,l}}Q_b^{c_B,y}\le I.
\]
Therefore \(S_l-T_l\ge0\) by an operator-matrix congruence. No undefined partial trace over an infinite commutant or exchange of same-algebra factors occurs. Bob's calculation is in the opposite algebra.

These comparisons have the original conditional-question form: replace \(\sqrt{\mu_J(x,y)}\) in the Alice seed by \(\sqrt{\mu_{X,J}(x)}\), then attach the scalar conditional factors \(\sqrt{\mu_J(y|x)\mu_J(y|x')}\). Consequently
\[
 p_c\rho_{A,c}\le G_{A,c}\nu_{A,c},\qquad
 p_c\rho_{B,c}\le G_{B,c}\nu_{B,c}, \tag{5.5}
\]
with \(p_c\le G_{A,c}\le A_c\), \(p_c\le G_{B,c}\le B_c\).

The local-description proof in §4 needs one target and two conditional comparisons. It uses Alice's comparison for coherent alignment and Bob's for the same target's marginal variation. It never requires a common reference purification. This is why the separate-parent operation is valid.

### 5.4 Exact entropy cancellation, tilted averaging, and allocation

For an ensemble \(\rho=\sum_lq_l\rho_l\), Donald's identity on both marginals gives
\[
 \begin{split}
 \sum_lq_l[D(\rho_l\Vert\nu)-D(\rho_l^K\Vert\nu^K)]
 &=D(\rho\Vert\nu)-D(\rho^K\Vert\nu^K)
       +I(l:R|K).
 \end{split} \tag{5.6}
\]
The private orthogonal label in \(K\) determines \(l\), so the last term is zero, including for question-correlated labels. Order domination in (5.5) then bounds the parent deficit by
\(\log(G_{A,c}/p_c)\) or \(\log(G_{B,c}/p_c)\).

Let \(Q_C(c)=\mu_D(c)p_c/p\), \(G_A=\mathbb E_{\mu_D}G_{A,c}\), and similarly \(G_B\). The exact change-of-measure identity is
\[
 \mathbb E_{Q_C}\log(G_{A,c}/p_c)
 =L+\log G_A
       -D\!\left(Q_C\middle\Vert
                  \frac{\mu_D(c)G_{A,c}}{G_A}\right)
 \le L+\log G_A. \tag{5.7}
\]
Zero-\(p_c\) branches have zero target weight. This is not an exchange of prior and posterior expectations. Product load bounds give
\[
 G_A\le\prod_{j\in D}a_j,\qquad
 G_B\le\prod_{j\in D}b_j. \tag{5.8}
\]

For completeness the ordered allocation is the copied-register chain rule. Write \(R_i=\widehat X_i\widehat Y_i\). On Alice's side trace \(R_{>i}\), condition only on the classical exposed records \((\widehat Y_{<i},X_{>i})\), and retain the fixed records. Direct-sum relative entropy makes the expected coordinate deficit
\[
 D(\rho^{R_{\le i}K}\Vert\nu^{R_{\le i}K})
 -D(\rho^{R_{<i}K}\Vert\nu^{R_{<i}K}).
\]
Summing telescopes to the parent deficit. The restriction commutes with attaching the fresh \(i\)-th conditional-question amplitudes, so its comparison form is preserved. Bob uses the reverse order. Both target families are partitions of (5.4): their external histories carry the same \(c,l,Y_{<i},X_{>i}\), their residual spaces carry the complementary coherent questions and the original fine records.

Crucially the local-preparation theorem is applied to the **whole** \(x_i,y_i\)-indexed target with histories inside its output workspace. The history is not sampled independently beforehand.

The unconditional fresh question marginals \(q_i^{X_iY_i}\) satisfy
\[
 \sum_{i\notin D}d_i
 :=\sum_{i\notin D}D(q_i^{X_iY_i}\Vert\mu_i)\le L. \tag{5.9}
\]
Indeed event conditioning has density at most \(1/p\) relative to the full product referee law; classical relative entropy to a product dominates the sum of its coordinate marginal divergences.

Set \(t_i=b_{A,i}+b_{B,i}+d_i\). Equations (5.6)–(5.9) and Theorem C prove
\[
 \boxed{\sum_{i\notin D}t_i
 \le3L+\log(G_AG_B)
 \le3L+2\sum_{j\in D}\kappa_j,} \tag{5.10}
\]
with, for every positive accuracy, legal single-game witnesses of loss
\[
 \alpha_i(D)+K\big(\sqrt{\alpha_i(D)}\,t_i^{1/4}+\sqrt{t_i}\big)
       +\text{accuracy}. \tag{5.11}
\]
This proves the full charged finite-tracial \(\mathrm{FR}(65536)\) condition at the stated exact fractional-partition scope.

### 5.5 The parity challenge and why the question quantifier matters

Let \(X_i=Y_i\) be iid uniform bits and a sure common checked label be the parity of all live bits. The history \((l,Y_{<i},X_{>i})\) fixes the fresh bit, so
\(\sum_i\mathbb E_{\rm history}D(q_i^{XY|\rm history}\Vert\mu_i)=m\log2\)
despite \(p=1\). Charging this conditional divergence by \(L=0\) would be false.

Our \(d_i\) is unconditional and equals zero. Histories stay in the full target; both local kernels can generate the same parity from the equal fresh bit and pre-shared outside bits. Equivalently,
\[
 D(Q_i^{RXY}\Vert\mu_i Q_i^{R|X})
 =d_i+I(Y:R|X)\le d_i+b_{A,i},
\]
and symmetrically for Bob. No conditional-history law is silently replaced by \(\mu_i\). The standalone whole-workspace preparation makes a separate history race unnecessary.

## 6. Scalar closure and amplification consequences

### 6.1 Eliminate the representation before Lin

For \(K\ge1\), define
\[
 \Phi_K(e,a)=
 \left[\frac{\sqrt{a+4(e-a)_+/K}-\sqrt a}{2}\right]^4. \tag{6.1}
\]
Every legal extracted base strategy has loss at least
\(\epsilon_i=1-\omega_{\mathrm{co}}(G_i)\). Let the positive accuracy in (5.11) decrease to zero and solve the quadratic in \(t_i^{1/4}\). Equations (5.10)–(5.11) imply
\[
 \sum_{i\notin D}\Phi_K(\epsilon_i,\alpha_i(D))
 \le3\log(1/p_D)+\log(G_A(P,D)G_B(P,D)). \tag{6.2}
\]

The actual masses are finite positive linear table functionals. Explicitly,
\[
 G_{A,c}(P)=\sum_lw_{c,l}
 \sum_{x_J}\mu_{X,J}(x_J)
 \sum_{a:a_D\in R_{c,l}}P_A(a\mid c_A,x_J), \tag{6.3}
\]
and Bob is symmetric. These functionals are independent of the chosen finite-tracial representation. For each tested question \(c\), \(G_{A,c},G_{B,c}\ge p_c\); their prior-averaged masses \(G_A,G_B\) satisfy \(G_A,G_B\ge p_D>0\). It is these averaged masses that occur in (6.2).

Lin's Definition 3.1/Theorem 3.2 gives full finite-table closure of finite-tracial strategies in \(C_{qc}\). At a fixed \(D\) with target \(p_D>0\), the probabilities, conditional losses, and masses in (6.2) converge. The arguments of the logarithms stay bounded away from zero and \(\Phi_K\) is continuous. Thus (6.2) passes to arbitrary commuting strategies. No raw costs, vectors, algebras, or POVMs are asserted to converge. Finite tracial does not mean finite matrix.

Using (5.8) gives the published scalar budget with \(3L+2\sum_D\kappa_j\). This closure is independent of the old resolvent/history proof. It still depends on the exact standalone sampler and Lin's theorem.

### 6.2 Quadratic blocks, charged games, and the original theorem

For an identical block game, (5.10) has zero presentation charge. Here is a complete all-finite-length proof of (A). First suppose a finite-tracial repeated strategy has all-wins probability
\(\theta>\exp(-\gamma\epsilon^2n)\), \(\gamma=2^{-75}\), and put \(L_\theta=\log(1/\theta)\).
Greedily test a coordinate whose conditional loss exceeds \(\epsilon/2\) while the remaining mean loss does so. Each addition raises log inverse event probability by more than \(\epsilon/2\), while every tested event contains all wins. Fewer than \(2L_\theta/\epsilon<n/2\) coordinates can be tested. At stopping, \(m\ge n/2\), \(p_D\ge\theta\), and mean remaining loss \(\alpha\le\epsilon/2\).

Mix the single-coordinate witnesses with a pre-shared uniform index. Cauchy–Schwarz and Jensen bound its loss by
\(\alpha+K[\sqrt\alpha(\mathbb Et_i)^{1/4}+\sqrt{\mathbb Et_i}]\)
at arbitrary positive slack. Now \(\mathbb Et_i\le3L_\theta/m<6\gamma\epsilon^2\). Its limiting loss divided by \(\epsilon\) is at most
\[
 \frac12+\frac K{\sqrt2}(6\gamma)^{1/4}
                 +K\sqrt{6\gamma}<0.665<1.
\]
A sufficiently small finite slack contradicts the base commuting gap. Zero gap or zero all-wins probability is trivial. We have therefore proved a uniform scalar all-wins bound for every finite-tracial table. Applying Lin's finite-table closure to that bound, and only then taking the arbitrary-commuting supremum, proves (A). No operational witnesses or raw \(t_i\) are passed through that limit.

For a common charge \(\kappa\), set \(t_0=1/(256K^4)=2^{-72}\). A live coordinate with conditional loss at most \(\epsilon/2\) has inverse deficit at least \(t_0\epsilon^2\). For this argument, test any live coordinate with conditional loss greater than \(\epsilon/2\) until none remains; do not stop merely when the mean is small. If \(L_\theta=\log(1/\theta)\), the tested set has size at most \(2L_\theta/\epsilon\) and total charge at most \(2\kappa L_\theta/\epsilon\). If the process stops with live coordinates, the scalar budget implies
\[
 t_0\epsilon^2(n-2L_\theta/\epsilon)
       \le(3+4\kappa/\epsilon)L_\theta,
\]
and hence
\[
 L_\theta\ge
 \frac{t_0\epsilon^2n}{3+4\kappa/\epsilon+2t_0\epsilon}
 \ge\frac{2^{-75}\epsilon^3n}{\epsilon+\kappa}.
\]
If all coordinates are exhausted, their tested losses already give \(L_\theta\ge n\epsilon/2\), which is stronger. Thus
\[
 \boxed{\omega_{\mathrm{co}}(G^{\otimes n})
 \le\exp[-2^{-75}\epsilon^3n/(\epsilon+\kappa)].} \tag{6.4}
\]
For zero gap the exponent is interpreted as zero, including when \(\kappa=0\).
For general masks singleton factors recover (2.1), conservatively. A row-star partition has one unit load and the other at most \(|A|\); a column-star partition reverses the roles. Hence one may always take
\[
 \kappa\le\tfrac12\log\min\{|A|,|B|\}. \tag{6.5}
\]
This is a presentation refinement, with no priority claim. The important mechanism is the proved reconstruction, rather than the improvement of a logarithmic factor.

**The gap power is optimal within the full block class.** The original binary line game \(L_m\) of Kempe–Regev has only equality masks and endpoint singleton masks, all of which are disjoint-block. Their Definition 3.1 and Theorem 3.2 give matching classical and no-signalling values, so
\[
 1-\omega_{\mathrm{co}}(L_m)=\epsilon_m=\frac1{2m-1}.
\]
Their Theorem 4.4 gives a classical repeated lower bound \((1-O(m^{-2}))^n\) for \(n\ge m^2\). Thus an absolute constant \(C\) satisfies
\[
 \omega_{\mathrm{co}}(L_m^{\otimes n})
 \ge\omega(L_m^{\otimes n})
 \ge \exp[-C\epsilon_m^2n]\qquad(n\ge m^2)
\]
for all sufficiently large \(m\). A universal exponent \(f(\epsilon)\) with \(f(\epsilon_m)/\epsilon_m^2\to\infty\) would contradict this lower bound. The power two in (A) is therefore optimal for its full disjoint-block class, up to constants. This does not optimize \(2^{-75}\), establish priority, or show optimality for the narrower class of total projections: the endpoint predicates in this fixture are partial.

For the tensor statement, start with a finite tensor strategy and use a full matrix standard form. Every step above, including all sampler copies, stays a full finite matrix algebra; its left/right action is a genuine finite tensor resource. The greedy contradiction therefore uses \(\epsilon_*\), uniformly before the supremum. This does not assert equality of tensor and commuting values.

### 6.3 Heterogeneous games and weighted thresholds

Let \(\epsilon_i=1-\omega_{\mathrm{co}}(G_i)\), assume
\(\kappa_i\le C_0\epsilon_i\), and put
\[
 S=\sum_i\epsilon_i^2,\qquad
 Z=\sum_i\epsilon_i{\bf1}\{\text{loss at }i\}.
\]
The earlier complete finite-probability theorem now has its game premise proved:
\[
 \boxed{\omega_{\mathrm{co}}(\bigotimes_iG_i)
 \le\exp[-2^{-75}S/(1+C_0)],} \tag{6.6}
\]
\[
 \boxed{\Pr\{Z\le(1-r)S\}
 \le\exp[-2^{-85}r^5 S/(1+C_0)],
 \quad0<r\le1.} \tag{6.7}
\]
For blocks \(C_0=0\). The zero-\(S\) interpretation is the trivial upper bound one.

For clarity, the scalar deduction of (6.7) is included. Set \(M_D=3\log(1/p_D)+2\sum_D\kappa_i\). Apply the inverse deficit (6.1), cap the conditional loss by \(\alpha_i'=\min(\alpha_i,\epsilon_i)\), and use Hölder to obtain
\[
 S_D-A_D\le K[S_D^{3/4}M_D^{1/4}+\sqrt{S_DM_D}],
\quad S_D=\sum_{i\notin D}\epsilon_i^2,\ 
 A_D=\sum_{i\notin D}\epsilon_i\alpha_i(D).
\]
The cap is necessary for the Hölder step.

Independently include \(i\) in a random tested set with probability
\(u\epsilon_i/(1+u\epsilon_i)\), and condition its selected tests to succeed. Its normalization is
\[
 F(u)=\mathbb E\prod_i(1+u\epsilon_i)^{-{\bf1}\{\text{loss at }i\}},
\quad L(u)=-\log F(u).
\]
The posterior entropy identity gives \(\mathbb E\log(1/p_D)\le L(u)\), while
\(\mathbb ES_D\ge(1-u)S\) and
\(\mathbb E\sum_D\kappa_i\le C_0uS\).
Under the tilted outcome law \(T_u\),
\[
 \mathbb E_{T_u}Z\ge(1-u)S
 -K[S^{3/4}\overline M^{1/4}+\sqrt{S\overline M}],
\quad\overline M\le3L(u)+2C_0uS,
\]
\[
 L'(u)\ge\mathbb E_{T_u}Z/(1+u).
\]
Take \(\lambda=r^4/[2^{20}K^4(1+C_0)]\). Wherever \(0\le u\le\lambda\) and \(L(u)\le\lambda S\), the error is below \(rS/16\); thus
\(L'(u)\ge(1-r/4)S\). By monotonicity, either \(L(\lambda)\ge\lambda S\) or this derivative bound integrates throughout the interval. In both cases
\(L(\lambda)\ge(1-r/4)\lambda S\).
On \(Z\le(1-r)S\) the product defining \(F(\lambda)\) is at least \(e^{-\lambda(1-r)S}\). Therefore the event probability is at most \(e^{-r\lambda S/2}\), which is (6.7) for \(K=2^{16}\). Full tested sets contribute zero live mass; zero-probability tested events have zero posterior weight.

For (6.6), test a positive-gap coordinate whenever its conditional loss exceeds \(\epsilon_i/2\). Then \(\sum_D\epsilon_i\le2L_\theta\), \(\sum_D\epsilon_i^2\le2L_\theta\), and \(\sum_D\kappa_i\le2C_0L_\theta\). With \(t_0=1/(256K^4)=2^{-72}\), a conditional loss at most \(\epsilon_i/2\) forces \(\Phi_K\ge t_0\epsilon_i^2\). Hence
\(t_0(S-2L_\theta)\le(3+4C_0)L_\theta\), which implies (6.6). Exhausting every positive-gap coordinate gives the bound directly.

The more ambitious intrinsic rate
\(\exp[-c\sum_i\epsilon_i^3/(\epsilon_i+\kappa_i)]\)
without a bounded ratio is still open. One must not multiply bounds for separate groups.

## 7. Further proved transfers and what was inherited

**Heterogeneity directly from the original iid theorem.** Independently of the new reconstruction, for any probability vector \(r_i\), put
\(r_*=\max r_i\), \(e_r=\sum r_i\epsilon_i\), and
\(\ell_J=\log(\max_J|A_i|\max_J|B_i|)\), \(J=\{i:r_i>0\}\). Then
\[
 \omega_{\mathrm{co}}(\bigotimes_iG_i)
 \le\exp[-2^{-75}e_r^3/(r_*(e_r+\ell_J))]. \tag{7.1}
\]
Construct a labelled mixture revealing the type \(i\) to both players; its value is exactly \(1-e_r\). On \(T\) copies of a product strategy of score \(\theta\), assign
\(\lfloor(1-\eta)T/r_*\rfloor\) mixture questions to their type cells whenever every type count is at most \(T\), and fill other cells with pre-shared independent dummy question pairs. The good-count probability tends to one. This gives mixture score at least \(\Pr(\text{good})\theta^T\). Apply (2.1), divide logarithms by \(T\), let \(T\to\infty\), then \(\eta\downarrow0\). The construction is all-input commuting and uses no pair-specific resource. This is an elementary transfer, not a new repetition mechanism.

**Correlated-resource nuisance cancellation.** For fixed nuisance effects \(R,S\), an arbitrary correlated bounded \(\sigma\) is allowed:
\[
 f(F\otimes R)=f(F)\otimes R+F\otimes f(R),\quad f(u)=u\log u.
\]
Consequently the nuisance-log term cancels exactly in any Jensen increment
\(\sum_xq_xf(F_x\otimes R)-f((\sum_xq_xF_x)\otimes R)\).
No product-state assumption is used. A fixed positive accepting contraction commuting with the retained local observable algebra can also be absorbed into one input-independent shared vector. Fresh-question-dependent nuisance effects are not covered. This repairs a state-independence restriction from the earlier round without claiming general semantic subtraction.

## 8. Interactive noisy-channel verification: proof and exact scope

For finite density matrices, use the sandwiched divergence
\[
 D_\alpha(\rho\Vert\sigma)
 =\frac1{\alpha-1}\log\operatorname{Tr}
 [(\sigma^{(1-\alpha)/(2\alpha)}\rho
                 \sigma^{(1-\alpha)/(2\alpha)})^\alpha].
\]
Inverse powers are restricted to the comparison support; the divergence is \(+\infty\) when \(\operatorname{supp}\rho\not\subseteq\operatorname{supp}\sigma\). Trace distance below means \(\tfrac12\|\rho-\sigma\|_1\).
Define
\[
 I_\alpha(\mathcal N)
 =\sup_{\psi_{RQ}\ {\rm pure}}\inf_{\zeta_B}
 D_\alpha(({\rm id}_R\otimes\mathcal N)(\psi)
                         \Vert\psi_R\otimes\zeta_B). \tag{8.1}
\]
The unchanged-reference marginal is fixed. Some simulation papers reverse this orientation; that alternative is not substituted.

### 8.1 Complete proof of Theorem B

The initial shared state is independent of the full referee question record and the laboratories initially receive only their respective local questions. Section 8.2 handles correlated initial resources with an additional source cost.

Gupta–Wilde Lemma 5 gives
\[
 I_\alpha(\mathcal N)=\inf_\zeta
 D_\alpha(\mathcal N\Vert\mathcal R_\zeta),\quad
 \mathcal R_\zeta(Z)=\operatorname{Tr}(Z)\zeta.
\]
Wilde–Berta–Hirche–Kaur Proposition 41 gives, for arbitrary different input states and arbitrary reference memories,
\[
 D_\alpha(\mathcal N(\rho_{RQ})\Vert\sigma_R\otimes\zeta)
 \le D_\alpha(\rho_{RQ}\Vert\sigma_{RQ})
                  +D_\alpha(\mathcal N\Vert\mathcal R_\zeta).
 \tag{8.2}
\]
This amortization collapse is for a channel versus a replacer, not for two arbitrary channels.

Choose almost-minimizing replacers separately for each prescribed slot and fixed \(\alpha\). Compare the real interactive protocol with the same local protocol in which every cross-player channel is replaced by its fixed local discard-and-prepare map. Include all referee questions, outputs, memories, and both laboratories in the reference for (8.2). Initially the states agree. Between slots, the same local maps cannot increase divergence. At slot \(j\), (8.2) adds at most \(I_\alpha(\mathcal N_j)\) plus arbitrarily small slack. The final divergence is at most their sum, regardless of local feedback or transmission direction.

The all-replacer experiment is a legal zero-communication quantum strategy with acceptance \(q\le q_0\). Apply the same binary acceptance measurement to both final states. Binary data processing gives
\[
 D_\alpha(\operatorname{Ber}(p)\Vert\operatorname{Ber}(q))
 \ge\frac{\alpha}{\alpha-1}\log p-\log q.
\]
This proves (B), after removing finite slack. If \(q_0=0\), finite channel costs force \(p=0\); if \(q_0=1\), cap at one. The argument supplies no unrestricted infinite-algebra Rényi statement about communicating arbitrary-co resources.

### 8.2 Source correlations, smoothing, and transcript errors

Let the actual normalized cq initial state be \(\rho_{UAB}\), where \(U\) is the full referee question record and \(A,B\) are the device resources before ordinary local question copies are delivered. For one question-independent resource \(\sigma_{AB}\), suppose
\[
 J_\alpha\ge D_\alpha(\rho_{UAB}\Vert
        \sum_u\mu_H(u)|u\rangle\langle u|\otimes\sigma_{AB}).
\]
The same telescope yields
\[
 p\le\inf_{\alpha>1}\exp\!\left\{
 \frac{\alpha-1}{\alpha}
 [\log q_0+J_\alpha+\sum_jI_\alpha(\mathcal N_j)]\right\}. \tag{8.3}
\]
Every term must use the **same** order. A normalized cq state within trace distance \(\eta\) of a state satisfying the displayed Rényi bound adds \(\eta\) once, after the whole protocol.

There is a different algebraic source interface. If the complete controlled acceptance effects obey
\[
 P_{\rm actual}\le e^hP_{\rm independent}+\eta
\]
by a certified hockey-stick/order defect, then the valid finite-order consequence is
\[
 p\le\eta+e^h
 \inf_{\alpha>1}
 e^{\frac{\alpha-1}{\alpha}(\log q_0+\sum_jI_\alpha(\mathcal N_j))}. \tag{8.4}
\]
This interface yields (8.4); moving \(h\) inside the Rényi factor is not justified by the normalized-smoothing argument. For example \(\rho=|0\rangle\langle0|\), \(\sigma=|+\rangle\langle+|\), multiplier two, has hockey-stick defect \((\sqrt5-1)/2\), but its nearest normalized state dominated by \(2\sigma\) is at trace distance \(1/\sqrt2\). These two smoothing notions are not equivalent. This example distinguishes the interfaces; it does not rule out every stronger inequality under additional assumptions.

If the referee tolerates a nonnegative integer \(r\) failed coordinates and an adversary can edit a nonnegative integer \(t\) coordinate answer records after the interaction and after seeing the transcript, while the referee retains its original questions, acceptance implies at most \(r+t\) original failures. Apply (B) or (8.3) to that original threshold event. For the inherited general bound use
\(\delta=\epsilon-(r+t)/n>0\) in (2.2). For identical blocks use (6.7), with \(r_{\rm rel}=\delta/\epsilon\), giving the available rate \(2^{-85}\delta^5/\epsilon^3\). An actual perfect honest strategy remains accepted under \(t\) edits when the tolerance is at least \(t\); supremum-one completeness is preserved as a supremum. No noisy honest implementation is assumed.

### 8.3 Capacity-rate consequence and exact channel assumptions

Suppose \(\omega_{\mathrm{co}}(H_n)\le e^{-gn}\). Channels come from a fixed finite family \(\mathcal M_l\), with prescribed slot counts \(m_l(n)/n\to\beta_l<\infty\), in any prescribed order/directions. Their environments are independent and inaccessible; no timing, routing, identity-selection, or classical control signal is free.

Finite-dimensional continuity \(I_\alpha\to C_E\) at order one implies exponential soundness if
\[
 \sum_l\beta_lC_E(\mathcal M_l)<g. \tag{8.5}
\]
Choose one fixed order sufficiently close to one with a strict margin and apply (B). For arbitrary \(n\)-dependent correlated sources, a bound on \(J_1/n\) alone is insufficient; require a fixed-order margin in (8.3), or a justified uniform/iid Rényi-regularity condition.

Noiseless classical \(c\)-bit and quantum \(q\)-qubit channels have costs \(c\log2\) and \(2q\log2\) at every order. Letting \(\alpha\to\infty\) recovers the factors \(2^c,4^q\). Independently, transcript guessing and teleportation prove the same maximum-order transfer for the explicitly admissible commuting-start instrument model, with local Kraus/isometry coefficients in the respective commuting algebras. Arbitrary abstract CP maps without a locality implementation are not included by terminology alone.

For arbitrary finite channels this broader maximum-order version uses
\[
 M(\mathcal N)=\min\{\operatorname{Tr}S:
              S\ge0,\ I_Q\otimes S\ge J_{\mathcal N}\}.
\]
CP order gives \(p\le q_0\prod_jM(\mathcal N_j)\), reference-uniformly. This is the known channel max-information/simulation quantity, not a new invariant.

## 9. Concrete strict gain and matched coding comparator

For a \(d\)-dimensional erasure channel with survival \(s\),
\[
 \mathcal E_{s,d}(\rho)=s\rho\oplus(1-s)\operatorname{Tr}(\rho)|e\rangle\langle e|,
\]
the exact costs are, with \(u=(\alpha-1)/\alpha\),
\[
 I_\alpha(\mathcal E_{s,d})
 =u^{-1}\log[1-s+s d^{2u}],\quad
 C_E=2s\log d,\quad I_\infty=\log(1-s+sd^2). \tag{9.1}
\]
To verify the formula, compare to \(zI_d/d\oplus(1-z)|e\rangle\langle e|\). A pure input's successful-block power is bounded using its at most \(d\) Schmidt coefficients, with equality for a maximally entangled input. Twirling that input shows arbitrary replacers cannot improve it. Minimizing
\(a^\alpha z^{1-\alpha}+b^\alpha(1-z)^{1-\alpha}\),
\(a=sd^{2u},b=1-s\), gives \((a+b)^\alpha\). Thus both sides match. The explicit CP primal/dual witnesses are in the supporting derivation.

There is a strict transfer for every certified exponent \(0<g\le1/4\). Allow one qubit-erasure slot per game coordinate with
\(s=3g/(8\log2)\). Order \(\alpha=4/3\) gives
\[
 p_n\le e^{-gn/64}, \tag{9.2}
\]
while both raw qubit counting and the optimum per-slot maximum-order cost are vacuous. Indeed \(I_{4/3}<15g/16\), whereas
\(\log(1+3s)>g\). This includes the conservative exponents of the present repetition results. For tiny \(g\) the required erasure rate is correspondingly extreme; no practical efficiency follows.

A completely solvable comparator makes the gain concrete. Let Alice receive a uniform \(n\)-bit string, Bob receive one fixed question, and require Bob to output that string. Its commuting zero-communication value is exactly \(2^{-n}\). Allow \(4n\) forward qubit-erasure slots with survival \(1/10\). Counting charges \(4\log4>\log2\); exact maximum-order domination charges \(4\log(13/10)>\log2\). Both fail. The finite-order bound gives
\[
 p_n\le e^{-E_*n},\qquad
 E_*=4D_{\rm bin}(1/8\Vert1/10)
      =0.01297370627\ldots>1/100. \tag{9.3}
\]
The maximizing \(u\) satisfies \(4^u=9/7\).

For even \(n\), an explicit randomized linear protocol achieves
\[
 \frac9{32(4n+1)}e^{-E_*n}
 \le p_{\rm construction}\le p_{\rm optimal}\le e^{-E_*n}. \tag{9.4}
\]
Pre-share \(4n\) EPR pairs and a uniform binary \(8n\times n\) matrix \(B\). Alice dense-codes consecutive pairs of \(BX\) into the EPR halves and sends them through the slots. Bob reads surviving pairs and samples uniformly from the affine solution space. With \(K=n/2\) surviving slots, the resulting square random binary matrix is invertible with probability at least \(9/32\). The binomial type probability is at least
\((4n+1)^{-1}e^{-4nD_{\rm bin}(1/8\Vert1/10)}\).
Multiplication proves (9.4).

Costs: \(4n\) transmitted qubits, \(4n\) EPR pairs, \(8n^2\) pre-shared random bits, \(O(n^2)\) encoding work and \(O(n^3)\) binary elimination work. There is no exponential codebook or unreported deterministic-code acquisition. The executable artifact simulates the logical channel induced by ideal dense coding; it is not a quantum experiment.

The exact channel-coding exponent is **established** Li–Yao machinery. This construction is a matched demonstration of the theorem's strength, not a new coding theorem. A noisy-source example further shows that a finite \(J_\alpha\), rather than a maximum-order source charge, can be necessary for this method; its full derivation and source-decoding costs are retained in the record.

## 10. Strongest counterexamples and surviving barriers

### 10.1 A current recovery shortcut fails in operator norm

Bhattacharya's 2026 Theorem 1 asserts operator-norm convergence of iterated Petz recovery under its “strict CPTP” hypotheses. Those hypotheses define strictness as preserving positive invertible elements; unital channels qualify.

Take
\[
 \mathcal M=\ell_\infty(\mathbb N\times\{+,-\}),\quad
 \tau(f)=\sum_{j\ge1}2^{-j}[f(j,+)+f(j,-)]/2,\quad B=1.
\]
Let \(\phi\) independently mix each pair with swap probability
\(a_j=1/(j+2)\). It is normal, unital, trace preserving, CP and self-adjoint in \(L^2(\tau)\). Its Petz map is \(\phi\). On the normalized sign vector of pair \(j\), \(\phi^2\) has eigenvalue \((1-2a_j)^2<1\), approaching one. If \(P\) averages each pair, then
\[
 \|(\mathcal R\phi)^n-P\|_{2\to2}
 =\sup_j(1-2a_j)^{2n}=1,\qquad n\ge1. \tag{10.1}
\]
Powers converge strongly, not in operator norm. The erroneous inference is that a nonzero fixed subspace isolates the spectral point one. An actual spectral gap repairs the norm statement with rate \((1-\gamma)^n\). Such a gap was not acquired for the game problem. This disproved shortcut is not used by our proof.

### 10.2 Rare complete revelation defeats average leakage

In the bit-guessing fixture, reveal all \(n\) bits with independent probability \(1/n\), otherwise reveal nothing. Expected communication is one bit and \(I(X^n:L)=\log2\), yet all-wins probability is at least \(1/n\). Thus expected communication, bounded Shannon information, or merely vanishing trace-distance leakage does not preserve an exponential guarantee. The finite-order/source-tail conditions in §8 are essential.

### 10.3 Unchanged referee laws do not legalize postselection

Start with independent uniform \(X,Y,A,B\), and condition on \(A\oplus B=XY\). Event probability is \(1/2\) at every input, so the referee law is unchanged, but the conditional box wins CHSH perfectly. The commuting bound is at most \((2+\sqrt2)/4\), by Cauchy–Schwarz applied to the CHSH operator. Therefore zero question-law drift is not a reconstruction theorem. Our construction also pays preparation deficits and reconstructs one legal all-input resource.

### 10.4 Approximate commutation and a global AND are not a locality compiler

Clock/shift unitaries, converted into real/imaginary binary effects, have cross commutators tending to zero but no uniformly close exactly cross-commuting effects in operator norm. The retained proof uses the integer winding index and gives a fixed \(1/32\) obstruction; it also supplies a tracial two-norm approximation, showing the importance of topology. This is established Voiculescu/Exel–Loring machinery and is not an objection to our exact opposite-algebra construction.

An elementary ancilla-free normalization bound is equally decisive. Let
\(Q=I-|0^n\rangle\langle0^n|\) and \(H=\sum_\beta h_\beta\), with positive \(k\)-local terms, \(\sum_\beta\|h_\beta\|\le T\), and \(H|0^n\rangle=0\). If \(H\ge\lambda Q\), then
\[
 \lambda\le kT/n. \tag{10.2}
\]
Each term annihilates the vacuum; on the one-excitation states it contributes only at sites in its support, so \(n\lambda\le\sum_i\langle e_i,H e_i\rangle\le kT\). Encodings, ancillas, extra consistency tests or changed normalization are outside this obstruction and require their own proof.

### 10.5 The older positive-filter barrier remains

The prior crown/scatter constructions rule out a universal bounded-charge positive filter on every near-perfect tested instance. Their exact common-information predecessor is Cuff–Permuter–Cover's coordination-capacity example. Our new one-sided proof controls actual masses and cancels retained-label information; it does not show those masses are small for every strategy or remove every question-correlated label. The barrier therefore survives without contradicting (A).

## 11. Decisive remaining problems and constructive attacks

**1. General quadratic repetition.** The remaining operation is a semantic, state-sensitive information allocation that replaces a positive presentation charge by something of order the game gap on suitably chosen tested sets. Universal low-mass exact filtering is already false. Promising attacks are a quotient by locally sufficient retained algebras, quantum rather than classical separator records, or a direct conditional-entropy increment estimate. A valid candidate must survive rare-event accuracy and the parity/PR fixtures, preserve the complete measured fine table, and produce one all-input local resource.

**2. A constructive locality bridge on a restricted family.** Repetition produces an acceptance operator with growing global dependence. To obtain a useful many-body or PCP capability, specify an encoding, bounded local tests, normalization, an efficient honest implementation, and a reconstruction map sound against arbitrary joint strategies. Improved repetition alone supplies none of these.

There is an additional absolute scope limit. A computable transformation from **every** promised constant-gap commuting game to an explicitly finite computable Hamiltonian, preserving a known separated energy promise, would decide an undecidable commuting-game promise problem by finite spectral computation. Lin's \(\mathsf{MIP}^{co}=\mathsf{coRE}\) supplies the relevant undecidability. Hence the unrestricted bridge is impossible at that scope, even without a polynomial-time requirement. The intended physical bridge must impose substantive restrictions such as a finite, acquired encoding/witness interface. Natarajan–Nirkhe's analysis already explains the analogous games/Hamiltonians distinction for tensor provers; this is a boundary to respect, not a new complexity classification.

**3. Scalable cryptographic compilation.** The all-compiled-games theorems take fixed games or fixed certificates before the security limit. To combine growing repetition with a single computationally bounded device, prove a uniform certificate-relative replacement theorem with controlled degree, coefficient norm, description size and cryptographic reduction cost. Full-cone channel Rényi costs do not follow from computational indistinguishability. General nice-SOS convergence is not a polynomial resource theorem. A finite-dimensional optimizer does not imply finite-level hierarchy convergence or flat optimality.

**4. Intrinsic heterogeneous rates and optimal thresholds.** Remove the maximum charge-to-gap restriction without illicit multiplication of subgroup bounds. For thresholds, improve the rare-event reconstruction or its scalar allocation; do not simply replace the fifth-power deviation by a binomial rate. The binomial KL ceiling and line-game quadratic obstruction remain controls.

**5. Quantitative finite resources.** The new proof avoids an entire resolvent/history architecture, but still has spectrum- and accuracy-dependent sampling resources and potentially infinite-dimensional finite algebras. Obtain meaningful costs on a physically implementable subclass before claiming a protocol improvement. A result in \(C_{qc}\) does not furnish finite matrices, device preparation, or practical advantage.

These are the strongest constructive openings left by this round. No general quantum-PCP theorem, efficient Hamiltonian compiler, generic DIQKD security theorem, or extraordinary physical capability is claimed.

## 12. Primary-source import and novelty audit

The table states the imported result and its actual applicability. The displayed proofs above establish the new bridges; the sources are not treated as success labels.

| Primary source | Exact result and use |
|---|---|
| [Jain, arXiv:2610.21410v1](https://arxiv.org/html/2610.21410v1), 15 October 2026 | Definitions 2.6/2.8, Lemmas 2.24–2.25 and 4.1–4.2: copied-input comparisons, ordered allocation, local descriptions and exact-marginal replacement for finite tensors. We reconstructed the relevant identities and extended the operation over finite trace using explicit matrices/polar corrections. General cubic and fifth-power threshold forms are predecessors. |
| [Junge–LaRacuente, arXiv:2009.11866v2](https://arxiv.org/html/2009.11866v2), JMP 63, 122204 (2022), DOI [10.1063/5.0066653](https://doi.org/10.1063/5.0066653) | ArXiv Theorem 1.2, published Theorem I.2, for bounded Hermitian operators in a von Neumann algebra with faithful reference; its finite-tracial \(p=2\) specialization gives (4.2) after positive slack. Published Lemma VI.2, arXiv Lemma 6.2, is the measured-entropy variational comparator. |
| [Lin, arXiv:2304.01940v3](https://arxiv.org/html/2304.01940v3) | Definition 3.1/Theorem 3.2: finite-table closure of finite-tracial standard-form correlations equals \(C_{qc}\). Applied only after scalar elimination at fixed \(p_D>0\), including the continuous actual masses. It supplies no matrix density. |
| [Song, ECCC TR26-199](https://eccc.weizmann.ac.il/report/2026/199/download/) | Lemma 4.1 and Theorems 1.1/4.6: smooth correlated sampling and general cubic tensor repetition. The standalone finite-tracial sampler is the inherited additional construction; its actual Section 8 is explicitly pinned. Cubic gap dependence and smooth labels are not new here. |
| [Kempe–Regev–Toner, arXiv:0710.0655v3](https://arxiv.org/html/0710.0655v3) | SDP 3, Lemma 5.7 and Theorems 5.2/5.5 already imply stronger quadratic unique-game bounds. Commuting vectors satisfy their finite SDP; rounding is a finite tensor strategy; the SDP product argument applies. The unique-game restriction is not a new theorem. |
| [Dinur–Steurer–Vidick, arXiv:1310.4113v2](https://arxiv.org/html/1310.4113v2), Theorem 1 | Projection tensor repetition with general gap power at most 12; expanding games have the stronger linear-gap conclusion in this version. The current projection comparison uses the separate \(\epsilon_*\) proof, not a claim that commuting and tensor values agree. |
| [Dinur–Steurer, author paper](https://www.dsteurer.org/paper/productgames.pdf) | Classical projection collision/relaxed-value product machinery already gives quadratic classical projection repetition. It is a predecessor and comparator, not itself a commuting import. |
| [Lin, arXiv:2510.07162v1](https://arxiv.org/html/2510.07162v1) | Theorem 9.3/A.1 is anchored commuting repetition, with its changed game and much higher gap power. Theorem 1.1 already proves \(\mathsf{MIP}^{co}=\mathsf{coRE}\). Question/answer reduction and gap compression also predate this round. |
| [Kempe–Regev, arXiv:0911.0201v1](https://arxiv.org/abs/0911.0201) | Definition 3.1/Theorems 3.2 and 4.4 provide the line-game obstruction to a stronger-than-quadratic gap rate within the full disjoint-block class itself. Exact commuting gaps follow by sandwiching between matching classical and no-signalling values. The binary endpoint masks are partial; no total-projection optimality claim follows from this fixture. |
| [Gupta–Wilde, arXiv:1310.7028v3](https://arxiv.org/html/1310.7028v3), CMP 334, 867–887 (2015) | Lemma 5, (5.16), with minimax exchange (5.19)–(5.20), gives the replacer radius for the exact orientation (8.1), for every \(\alpha>1\). Lemma 6 gives channel additivity; the interactive proof only needs the minimax identity and continuity at one. |
| [Wilde–Berta–Hirche–Kaur, arXiv:1808.01498v2](https://arxiv.org/html/1808.01498v2), Proposition 41/(283) | Sandwiched-Rényi amortization collapse for an arbitrary finite channel versus a replacer, allowing different input states and arbitrary reference memories. These are exactly the states encountered after feedback in §8. |
| [Jain–Kundu, arXiv:2106.04299v3](https://arxiv.org/abs/2106.04299v3), Lemma 8 | Established teleportation/transcript-guessing communication mechanism. The independent constructor supplied its full fine-output identity and exact commuting-start local-instrument check. This is a scope transfer, not an invention of the mechanism. |
| [Li–Yao, arXiv:2209.00555v3](https://arxiv.org/html/2209.00555v3), Theorem 6 | Exact entanglement-assisted channel-coding strong-converse exponent, including the feedback comparator. Our erasure guessing construction matches this established mechanism; no new capacity theorem is asserted. |
| [Li–Yao, arXiv:2112.04475v5](https://arxiv.org/html/2112.04475v5), Theorems 9/11 | Exponentially accurate entanglement-assisted channel simulation was the principal's first route. The direct amortization proof supersedes the fixed-parallel-block simulation restriction and its polynomial prefactor. The known simulation theorem remains a comparator. |
| [Fang–Wang–Tomamichel–Berta, arXiv:1807.05354](https://arxiv.org/abs/1807.05354), IEEE TIT 66 (2020) | Channel max-information and simulation SDP precede the CP-order formulation in §8. The needed order comparison was proved directly here. No nonsignalling-assisted simulator is substituted for a quantum local protocol. |
| [Kulpe et al., arXiv:2408.06711v3](https://arxiv.org/html/2408.06711v3), Theorem 6.1 and Corollary 6.2 | Fixed-game asymptotic compiled-game commuting soundness. It does not justify interchanging growing game size and cryptographic security limits. |
| [Cui–Falor–Natarajan–Zhang, arXiv:2507.17581v1](https://arxiv.org/html/2507.17581v1), Theorem 3.5 | Nice-SOS certificate bounds for compilation; one-sided hierarchy convergence. Negligible terms depend on the certificate. Polynomial-cost repeated-game certificates are an additional missing operation. |
| [Klep et al., arXiv:2507.17006v3](https://arxiv.org/html/2507.17006v3), Theorem 2.7/Corollary 2.8/Theorem 3.4 | Fixed-level sequential-NPA bound, negligible commuting excess under finite convergence, and tensor identification under flat optimality. The 16 October 2026 revision corrects stronger readings of older abstract snippets. |
| [Natarajan–Nirkhe, arXiv:2403.13084v1](https://arxiv.org/html/2403.13084v1), §§2 and 4 | Distinguishes prover-efficient games PCP from unrestricted games and explains the failed energy-amplification bridge. Its restrictions remain relevant after improving repetition. |
| [Bhattacharya, arXiv:2605.08829v1](https://arxiv.org/html/2605.08829v1), Theorem 1 | Not imported: (10.1) contradicts the asserted uniform operator-norm conclusion under the source's stated strictness definition. Strong convergence/spectral-gap repairs are distinguished. |

Several other relevant 2026 sources were inspected as comparisons: Culf's projection-to-tracial rounding has a least-supported-question-probability cost that can grow exponentially under repetition; composable simultaneous purification and information-restricted prepare-and-measure work already connect communication restrictions with spatial correlations. Neither supplies the full new charged reconstruction by itself.

The distinctive proof contribution is the **one exact refined target with two independently normalized one-sided conditional comparisons**, together with its operational finite-tracial reconstruction and continuous actual-mass scalar closure. The quadratic projection/disjoint-block result and its mixed-game consequences follow from that mechanism. The interactive noisy-channel theorem is a new synthesis/application at the stated game interface; its strong-converse tools and solved coding restrictions are established.

### Recent audits and priority limits

Zenodo [22061117](https://zenodo.org/records/22061117) was retrieved through its public API and its six-page audit read. Its comparison of a polynomial upper bound with a stronger exponential upper bound does not constitute a contradiction; it supplies no explicit counterexample resolving the present operational construction. That is a scoped evaluation of its arguments, not certification of the original theorem.

Record [22060622](https://zenodo.org/records/22060622) returned HTTP 410 and remains unread and uncleared. A separate arXiv audit's earlier greedy-polarity objection was withdrawn in its current version after a missing overbar in text extraction was identified; it is not listed as a surviving defect. Current versions, not snippets of superseded versions, govern those comparisons.

The previous October Git preservation supports source chronology but does not independently prove a public-disclosure date. No first-priority claim is awarded. The current primary-source search found no exact prior statement of the full new projection/block conclusion, but absence of an accessible hit is not exhaustive novelty clearance.

## 13. Final theorem/status and dependency ledger

| Claim | Status and exact dependency |
|---|---|
| Original general cubic and threshold theorem | Preserved as supplied capital at exact source scope. |
| Finite-tracial conditional-comparison local reconstruction, Theorem C | Proved here using multivariate GT, explicit finite-algebra polar construction, and the standalone actual sampler. |
| One common weighted target with two separate one-sided parents | Proved; independently challenged on non-block, overlapping/fractional, noncommuting-POVM and zero-weight fixtures. |
| Full charged finite-tracial \(\mathrm{FR}(65536)\) | Proved at every finite exact positive fractional rectangle partition, with arbitrary joint local repeated measurements. |
| Actual-mass scalar budget for arbitrary commuting tables | Proved; masses are finite linear table functionals; scalar closure uses Lin. |
| Quadratic commuting disjoint-block/projection repetition | Proved as (A); no general-predicate quadratic claim. |
| Tensor quadratic disjoint-block/projection repetition with \(\epsilon_*\) | Proved by a separate finite-matrix argument. |
| Optimality of the quadratic gap power within the full disjoint-block class | Proved by applying the established binary line-game lower bound; no optimal constant, total-projection optimality or priority claim. |
| Earlier heterogeneous controlled-charge all-wins/weighted thresholds | Now proved without an unproved FR premise; previous scalar proofs and their exact assumptions retained. |
| Independent labelled-mixture heterogeneous theorem | Proved from original iid capital alone; elementary transfer, priority unclaimed. |
| Interactive finite-order channel/source theorem | Proved for ordinary finite-dimensional protocols with fixed memoryless channel slots and full signal accounting, using checked strong-converse imports. |
| Arbitrary-commuting-start maximum-order communication/CP theorem | Proved at the explicit local-instrument model; not promoted to a finite-order von Neumann Rényi theorem. |
| Explicit erasure strict improvement and matching randomized code | Proved mathematically with complete resource costs; existing coding predecessors credited. |
| Uniform iterated-Petz operator-norm convergence under the inspected 2026 hypotheses | Disproved by the infinite pair-mixing channel; a spectral gap repairs the norm conclusion. |
| Average information/expected communication preserving exponential security | Disproved by rare complete revelation. |
| General quadratic repetition, optimal threshold rate, unrestricted intrinsic heterogeneous sum | Open. |
| Efficient growing-game cryptographic compilation, restricted useful local Hamiltonian compiler | Open; unrestricted arbitrary-game finite Hamiltonian compiler has the computability obstruction stated above. |
| Historical firstness, efficient finite matrices for arbitrary co tables, implemented practical advantage | Not established. |

The principal checked the load-bearing operator order, common-amplification orientation, faithful-slack argument, scalar constants and continuous table passage. Independent review accepted the same operations at the recorded scopes. Finite diagnostics support orientation and arithmetic; the general theorems follow from the proofs.

The supporting record retains 224 noncommuting fractional-rectangle contexts, 192 tilted-average controls, common-label negative controls, finite Rényi/amortization cases with different noncommuting states, exact rational exponent certificates, coding/affine-decoder checks, and the frozen initial hashes. Its manifest distinguishes these from proof certification.

No manuscript, Zenodo record, website deployment, or unrelated research artifact was modified or published in this research round.
