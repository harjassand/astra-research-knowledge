# P3 Xi volume relaxation return

Source: https://chatgpt.com/c/6af11227-f57c-83ec-80e4-caf25a4bae01
Model: GPT-6 standard, Extra High. Turn e0c34814-8d24-4d6d-be62-c51cac331891; response 406ed247-956e-452c-9590-98d8938c20e1. UI showed a complete response and idle composer.
Capture: full native current-chat reader response below its 20,000-character cap; expanded user-visible activity transcribed from the chat, with one symbol not exposed in the accessible activity text. No producer ZIP visible.

## Actual prompt

Resolve this ONE FULL question: does every fixed conservative complex-balanced mass-action reaction network equilibrate in polynomial physical time as volume grows?

Input is any finite network y_r -> z_r on d species (arbitrary molecularities/linkage classes), positive binary-rational constants kappa_r and c_i, a supplied positive rational conservation vector w, and positive rational R. They satisfy w.(z_r-y_r)=0 and, at each complex y, sum_(r:y_r=y) kappa_r*c^y = sum_(r:z_r=y) kappa_r*c^(y_r). No deficiency-zero, detailed-balance, interior-start or lattice-fibre promise is added.

For every integer V>=1, use EXACT original physical rates lambda_r^V(x)=kappa_r*V^(1-|y_r|)*prod_i (x_i)_(y_ri), with falling factorial zero when disabled. For every x0 in Z_+^d with w.x0<=R*V, let Gamma be its ACTUAL reachable closed irreducible class. It is finite; do not replace it by a stoichiometric or saturated-lattice fibre. On Gamma, pi_V(x)=Z_Gamma^-1*prod_i (V*c_i)^x_i/x_i!. Define E_V(f,f)=1/2*sum_(x,r) pi_V(x)*lambda_r^V(x)*(f(x+z_r-y_r)-f(x))^2.

The FULL positive endpoint is ONE terminating deterministic construction from the fixed rational input of computable rational C>=1 and integer D>=0 such that Var_piV(f)<=C*(1+V)^D*E_V(f,f), for ALL V, ALL these actual classes and ALL real functions f. Singleton classes are vacuous. Give effective finite BIT costs for the construction and its bounds; dependence on the fixed network may be arbitrarily large but must be computable. No exponent uniform over different networks is required. This is polynomial in numeric V, not a demand for mixing or enumeration polynomial in log V. Preserve original continuous physical time, including near-boundary and small-total-population classes. A full negative can instead be a SINGLE fixed valid network/rational data and an explicit class/volume family with certified superpolynomial relaxation, or a genuine obstruction to the exact effective universal statement within this model. A failed proof route or a known infinite-state zero-gap example is not such a negative.

Every rate, reachability/path operation, stationary normalization/tail estimate, precision, randomness and computation used must be paid. Finite-state positivity or a separate computation at each V does not supply the uniform polynomial. No extra inflow/outflow, missing species, modified reactions, rescaled clocks, oracle or assumed fast sampler. There is no requested laboratory, practical-parameter or publication gate.

Available scoped capital: Anderson-Craciun-Kurtz, arXiv:0803.3042v4, Theorems4.1/4.3 and Section4.1 give exactly the product law and volume scaling above, NOT its mixing bound: https://arxiv.org/html/0803.3042v4 . Anderson-Cappelletti-Fan-Kim, arXiv:2309.06970v2, Theorem2.5/Corollary2.8 and Section3 supply sufficient path/congestion criteria; Theorem3.2 uses all-species inflow/outflow, while Example2.4 has an infinite-state detailed-balanced zero gap: https://arxiv.org/html/2309.06970v2 . Windisch, arXiv:1505.03018v3, Definition2.2/Theorem1.1 concerns simple fibre walks and failure of polynomial-in-log-cardinality mixing, not failure of polynomial-in-V relaxation for this weighted physical chain: https://arxiv.org/html/1505.03018v3 .

Accepted ROOT capital, not a free volume-uniform theorem: weak reversibility makes enabled population edges reversible by finite complex-cycle words; the ordinary ideal <u^y_r-u^z_r> decides actual class membership by monomial differences. Saturating can merge disabled boundary classes. An existing exact rank-one positive-gap compiler handles each fixed class, but its constants have not been bounded polynomially in V. These are available premises without a recurring reproof assignment.

Optional intuition only: separable log-factorial weights and finite enabled-word algebra may control energy barriers; no uniform path/congestion or boundary-buffer theorem is assumed. You own all ideas, representations, methods, source order and framing, may discard this intuition, and may challenge the premise. Persist in pursuing the FULL statement rather than accepting a conditional wrapper or a restricted family as completion.

you may use all subagents avaible
Every helper inherits EVERY existing known/unknown source, access, transfer and resource hold. No retry, alternate/mirror/version recovery or identifying recovery of held sources. In particular Leroux-Sutre d-nb.info/990289982/34 Section5 remains unread/held after timeout; the earlier Wang publisher anti-bot original has unknown exact identity; NSF10314785/Cook-Gacs-Winfree overlap is unresolved; and ROOT's https://arxiv.org/html/1410.4820v3 returned404 and remains unread/held, with no alternate recovery. All older Dots/Golding-Henderson/Serre/CarloAlberto/OpenAI-tree/2410.23225v3/TR26-272/2610.00548v2/AB/ZIP and unidentified holds remain. Previously accepted scopes may be used without recovering originals. No extra principal chat/model/worker/resource/spending; Sol closed and Dots protected. Fresh context is not blind because shared retrieval/Personal Context may expose prior work.

## Available user-visible activity

Worked for 36m 11s.

I’ll test the full statement through the geometry of actual communicating classes, stationary weights, and physical-rate bottlenecks. The main issue is whether fixed reaction rules can create a superpolynomial bottleneck as [symbol not exposed in accessible activity text] grows. I’ll keep any result at its proved scope and won’t revisit the sources you’ve marked as held. Developed a connectivity proof and assessed bottlenecks Evaluated boundary behavior and tested geometric paths for conductance proof Proved bounded corridors using counterexamples, bounds, augmentation, and congruence moves Analyzed path geometry Developed a proof strategy for polynomial mixing via connectivity and spectral gaps Assessed structural connectivity Developed a structural approach Developed and verified an algebraic proof construction for connectivity bounds Consolidated and reviewed the proof Consolidated and finished the proof Audited and reviewed the proof structure

Searched 53 websites

## Complete response

## Resolution status: full theorem not yet established

The supplied hypotheses give substantial control over the finite-volume chains, but the decisive requirement is a **volume-uniform polynomial Poincaré inequality for every actual communicating class**, including classes confined to boundary regions.

Two useful facts hold uniformly over all \(V\) and all such classes.

### 1\. Every enabled nontrivial reaction has a polynomial lower rate bound

Write

\[
m_*=\max_r |y_r|,\qquad
\kappa_*=\min_r\kappa_r,\qquad
A=\left\lceil\frac{R}{\min_i w_i}\right\rceil.
\]

Conservation gives \(0\le x_i\le AV\)\. For every enabled reaction,

\[
\lambda_r^V(x)
=\kappa_r V^{1-|y_r|}(x)_{y_r}.
\]

Because the positive integer falling-factorial product is at least \(1\),

\[
\boxed{\lambda_r^V(x)\ge
\kappa_* V^{1-m_*}.}
\]

For a nontrivial conservative reaction, \(m_*\ge1\)\. Thus no individual enabled transition has an exponentially small physical rate. This uses exactly the original clock.

### 2\. A bounded-length reaction word has only polynomial local stationary-weight distortion

Put

\[
W_V(x)=\prod_i\frac{(Vc_i)^{x_i}}{x_i!}.
\]

For any two states \(x,z\) differing by a fixed bounded vector, their weight ratio is bounded above and below by fixed powers of \(1+V\), provided both are nonnegative. In particular, any reaction word of fixed length has at most polynomial stationary-weight distortion along its intermediate states.

These facts eliminate slow individual reactions and fixed-length activation sequences as possible sources of superpolynomial relaxation. They do **not** eliminate a bottleneck whose traversal requires visiting states with exponentially smaller stationary mass.

## 3\. A computable core-or-boundary dichotomy

A stronger structural fact follows from the finite reaction presentation. It is the key to addressing boundary classes without saturating their reaction ideal.

Consider a finite auxiliary state space of the form

\[
Q\times\mathbb Z_{\ge0}^{k},
\]

where \(Q\) records species whose counts have already been bounded, and the remaining \(k\) coordinates are unrestricted. Its transition templates have the form

\[
(s,a+u)\longleftrightarrow(t,b+u),
\qquad u\in\mathbb Z_{\ge0}^{k},
\]

with finitely many fixed \(s,t,a,b\)\.

The reverse arrows here are graph edges, implemented by the original network's fixed complex-cycle words; they are not changes to the physical generator.

**Core-or-boundary lemma.** For every prescribed integer \(T\ge1\), one can compute \(K\ge1\), depending only on this finite transition system and \(T\), such that every connected class satisfies at least one of\:

1. The class contains a state with all \(k\) unrestricted coordinates at least \(T\)\.
2. Some unrestricted coordinate \(i\) is less than \(K\) at **every** state of that class.

The lemma permits the bounded coordinate to depend on the class, but \(K\) is uniform.

### Algebraic proof and terminating construction

Let

\[
S=\mathbb Q[X_1,\ldots,X_k],\qquad F=S^Q,
\]

and form the submodule

\[
N=\left\langle e_sX^a-e_tX^b:
(s,a)\leftrightarrow(t,b)\text{ is a transition template}\right\rangle_S.
\]

Monomial basis vectors represent population states. Two states are connected precisely when the difference of their monomial vectors belongs to \(N\)\.

Put \(p=X_1\cdots X_k\) and

\[
J=N+p^TF.
\]

In the finitely generated module \(M=F/J\), multiplication by \(p^T\) is zero.

By a finite primary decomposition of the zero submodule of \(M\), every associated prime contains some variable \(X_i\)\. Consequently there is a finite \(K\) for which

\[
\bigcap_{i=1}^{k}X_i^K M=\{0\}.
\]

In particular,

\[
\boxed{\bigcap_{i=1}^{k}(N+X_i^KF)
\subseteq N+p^TF.}
\tag{1}
\]

There is a deterministic way to find \(K\)\: enumerate \(K=1,2,\ldots\), calculate the submodule intersections using exact Gröbner-basis arithmetic, and stop when inclusion (1) holds. The primary-decomposition argument proves termination.

If a connected class contained a state with coordinate \(i\ge K\) for every \(i\), every representative monomial of that class would belong to the left side of (1). The right side says that the class contains a representative divisible by \(p^T\)—a state with every unrestricted coordinate at least \(T\)\.

This proves the dichotomy.

The important consequence is that a class which fails to reach a sufficiently thick core can be reduced to a system with **one fewer unrestricted coordinate and a finite additional control-state coordinate**\. Repeating this reduction takes at most \(d\) levels.

## 4\. Uniform paths through a thick core

The remaining ingredients can be constructed using finite graph operations, integer lattices and a backward reachability calculation.

### 4.1 Compute the finite-control lattice

At one node of the dimension-reduction construction, build the finite undirected graph \(H\) on the control states \(Q\)\. Each template

\[
(s,a)\leftrightarrow(t,b)
\]

has unrestricted-coordinate displacement \(g_e=b-a\)\.

For each connected component of \(H\), select a base control state \(s_*\) and a spanning tree. Let \(h_s\) be the displacement along its chosen tree path from \(s\) to \(s_*\)\.

Compute the integer lattice

\[
L=\operatorname{span}_{\mathbb Z}
\{g_e+h_t-h_s:e=(s,a;t,b)\}.
\]

Each generator is the displacement of a closed walk based at \(s_*\)\. Conversely, the displacement of every closed walk at \(s_*\) belongs to \(L\)\.

Compute the finite Graver basis \(\mathcal G(L)\)\: the nonzero elements of \(L\) that cannot be decomposed into two nonzero elements of \(L\) having the same coordinatewise signs.

This is effective using integer lattice normal forms and Hilbert-basis calculations in the finitely many orthants.

For each \(g\in\mathcal G(L)\), express it as an integer combination of the displayed lattice generators. Replacing those generators by their finite closed walks produces a **fixed reaction word implementing \(g\)**\.

Because the list is finite, an integer \(M\) can be computed so that every such word is enabled from the base control state whenever all unrestricted coordinates are at least \(M\)\.

The original directed complex-cycle words implement every abstract reverse edge. Thus all these words expand into genuine original physical reactions.

Choose \(T\ge M\) sufficiently large that every control-tree normalization from a state whose unrestricted coordinates are at least \(T\) ends at base control \(s_*\) with unrestricted coordinates at least \(M\)\.

### 4.2 Access to the core takes a uniformly bounded number of reactions

Define the core target

\[
\mathcal C_T=\{(s,x):s\in Q,\ x_i\ge T\text{ for every unrestricted }i\}.
\]

The set of states from which \(\mathcal C_T\) is reachable is upward-closed in the unrestricted coordinates.

Its finite minimal basis can be computed by backward saturation. For a template

\[
(s,a+u)\longrightarrow(t,b+u)
\]

and a target lower bound \(v\) at control \(t\), the corresponding minimal predecessor at control \(s\) is

\[
a+(v-b)_+,
\]

where the positive part is coordinatewise.

Starting from the finitely many core targets, repeatedly add these predecessors and discard elements dominated by another element at the same control state. Dickson's lemma proves termination.

Store a witness word with each surviving minimal predecessor. The resulting table has a fixed maximum expanded physical word length \(L_{\mathrm{cov}}\)\.

Therefore\:

\[
\boxed{\text{If a class meets }\mathcal C_T,\text{ every state in it can reach }\mathcal C_T
\text{ in at most }L_{\mathrm{cov}}\text{ physical reactions.}}
\tag{2}
\]

To see the uniformity, take a minimal predecessor \(a\le x\)\. The stored witness from \(a\) remains enabled after adding \(x-a\) to every unrestricted coordinate. Its length and coordinate excursions are unchanged.

This includes states arbitrarily close to boundary faces.

### 4.3 The entire buffered fibre is connected

Let \((s_*,z_0)\) be one normalized core state in an actual class \(\Gamma\)\.

Then every point in

\[
\mathcal F=
\{z\in(z_0+L)\cap\mathbb Z_{\ge0}^k:z_i\ge M\}
\tag{3}
\]

is connected to \((s_*,z_0)\)\.

Indeed, for any \(z,z'\in\mathcal F\), the lattice difference \(z'-z\) has a sign-compatible decomposition into elements of \(\mathcal G(L)\)\. Applying those moves in sequence keeps every coordinate between its two endpoint values, and hence at least \(M\)\. Every move is implemented by its previously compiled finite physical reaction word.

Conversely, the unrestricted-coordinate displacement between any two states in \(\Gamma\) at base control \(s_*\) belongs to \(L\), by the finite-control graph construction.

Thus (3) is exactly the base-control buffered portion of \(\Gamma\)\. No saturation of the original reachability ideal has been used.

## 5\. Log-factorial convexity produces a nondecreasing-weight route

At base control \(s_*\), define

\[
\Phi_V(z)=\sum_{i=1}^{k}
\left[\log(z_i!)-z_i\log(Vc_i)\right].
\]

The fixed small-species coordinates contribute only a constant to \(\Phi_V\)\. Each summand is a convex function on the nonnegative integers.

Choose a maximizer \(z_*\) of \(W_V(s_*,z)\) over the finite set \(\mathcal F\), breaking ties lexicographically. Equivalently, \(z_*\) minimizes \(\Phi_V\)\.

For any \(z\ne z_*\), write

\[
z_*-z=g_1+\cdots+g_h
\]

as a sign-compatible Graver decomposition.

Coordinatewise convexity gives

\[
\sum_{j=1}^{h}
\big[\Phi_V(z+g_j)-\Phi_V(z)\big]
\le
\Phi_V(z_*)-\Phi_V(z)
\le0.
\]

Consequently, some feasible \(g_j\) satisfies

\[
\Phi_V(z+g_j)\le\Phi_V(z).
\]

Select such a move deterministically. It does not decrease stationary weight, and it strictly reduces \(\|z-z_*\|_1\)\. Repetition reaches \(z_*\) in at most \(\|z-z_*\|_1=O(V)\) Graver moves.

Each Graver move is a fixed physical reaction word. Its intermediate populations differ from its starting population by fixed bounded amounts, so its intermediate stationary weights lose at most a polynomial factor in \(V\)\.

Combining this route with (2) and the control-tree normalization proves the following uniform path property\:

**For every actual class reaching the chosen core, there is a common root \(\rho\) and constants \(L_0,P_0\ge1\), \(b\ge0\), computed at this finite-control node, such that every \(x\in\Gamma\) has a path of original directed reactions to \(\rho\) satisfying**

\[
|\gamma_x|\le L_0(1+V),
\]

and, at every vertex \(v\) of that path,

\[
\boxed{\pi_V(v)\ge
\frac{\pi_V(x)}{P_0(1+V)^b}.}
\tag{4}
\]

The constants do not depend on \(V\), \(x_0\), or the communicating class.

## 6\. An explicit polynomial Poincaré constant

We now turn the path property into the required bound, without imposing reversibility on the Markov chain.

Retain the fixed-network quantities

\[
A=\left\lceil\frac{R}{\min_i w_i}\right\rceil,
\quad m_*=\max_r|y_r|,
\quad \kappa_*=\min_r\kappa_r,
\]

and define the computable positive rational

\[
H=\max\left\{1,\max_i c_i,\frac{A}{\min_i c_i}\right\}.
\]

For any two states \(u,v\) satisfying the conserved mass bound,

\[
\max\left\{
\frac{W_V(u)}{W_V(v)},
\frac{W_V(v)}{W_V(u)}
\right\}
\le [H(1+V)]^{\|u-v\|_1}.
\tag{5}
\]

This follows by changing coordinates one unit at a time and using the exact factorial ratios.

At a given finite-control node, compute three bounds from the finite physical words\:

- \(\ell_{\rm cov},\ell_{\rm tree},\ell_{\rm G}\)\: their maximum lengths for core access, control normalization and a Graver move.
- \(b_{\rm cov},b_{\rm tree},b_{\rm G}\)\: their maximum coordinatewise excursions relative to their respective starting populations.

All six values are nonnegative integers, obtained by inspecting finite words.

Set

\[
b_0=b_{\rm cov}+b_{\rm tree}+b_{\rm G},
\]

and

\[
L_0=1+\ell_{\rm cov}+\ell_{\rm tree}
       +dA\ell_{\rm G}.
\]

The construction in Sections 4–5 gives, for every state of every core-reaching class, a root path of length at most \(L_0(1+V)\), with

\[
\pi_V(v)\ge
H^{-db_0}(1+V)^{-db_0}\pi_V(x)
\]

at every path vertex \(v\)\.

Now let \(\gamma_x\) be the selected root path from \(x\), and let \(\rho\) be the root.

For every real \(f\),

\[
\begin{aligned}
\operatorname{Var}_{\pi_V}(f)
&\le\sum_{x\in\Gamma}\pi_V(x)(f(x)-f(\rho))^2\\
&\le L_0(1+V)
\sum_{x\in\Gamma}\pi_V(x)
\sum_{e\in\gamma_x}(\nabla_e f)^2.
\end{aligned}
\tag{6}
\]

Here every edge in \(\gamma_x\) is an actual original directed reaction, not an artificial macro transition.

For a particular physical reaction edge \(e\) beginning at \(u\), the weight comparison and maximum path length give

\[
\sum_{\substack{x,j\\\gamma_x(j)=e}}\pi_V(x)
\le
|\Gamma|L_0(1+V)
H^{db_0}(1+V)^{db_0}\pi_V(u).
\]

Since

\[
|\Gamma|\le(AV+1)^d
\le(A+1)^d(1+V)^d
\]

and every enabled edge rate is at least

\[
\kappa_*(1+V)^{-(m_*-1)},
\]

substitution into (6), with the factor \(1/2\) in the specified Dirichlet form, yields

\[
\boxed{
\operatorname{Var}_{\pi_V}(f)
\le C_{\rm node}(1+V)^{D_{\rm node}}
\mathcal E_V(f,f)
}
\tag{7}
\]

where the explicit valid choices are

\[
\boxed{
C_{\rm node}=
\max\left\{
1,\,
\frac{2(A+1)^d L_0^2H^{db_0}}{\kappa_*}
\right\},
\qquad
D_{\rm node}=d+m_*+1+db_0.
}
\]

Both are computable from the fixed-network input and the finite word certificates. In particular, \(C_{\rm node}\) is rational and \(D_{\rm node}\) is a nonnegative integer.

## 7\. The complete terminating compiler

The core case is handled by (7). The algebraic dichotomy in Section 3 handles every remaining class.

The deterministic compiler performs the following finite recursion.

1. Verify the rational conservation and complex-balance identities. If every reaction has zero displacement, return \(C=1,D=0\)\.
2. For every reaction, compute a fixed directed complex-cycle return word. Replace each reaction by a two-sided graph template, retaining the original directed physical word for each orientation.
3. Begin with one control state and all \(d\) species unrestricted.
4. At each node, construct the finite control graph, its cycle lattice and Graver basis, the fixed implementing words, the thick-core threshold \(T\), and the backward-coverability witness table.
5. Compute the node's rational \(C_{\rm node}\) and integer \(D_{\rm node}\) using (7).
6. If unrestricted coordinates remain, find \(K\) by the terminating module-inclusion search (1). Create one child for each possible coordinate \(i\) that might be globally bounded, moving \(i\) into the finite control with allowed values \(0,\ldots,K-1\)\.
7. Stop at nodes with no unrestricted coordinates. Their finite-control classes are covered by the same root-path argument, with no Graver moves required.

There are at most \(d\) coordinate-reduction levels and finitely many children at each node. Every subroutine terminates, so the entire tree is finite.

Output

\[
\boxed{
C=\max_{\text{nodes}}C_{\rm node},
\qquad
D=\max_{\text{nodes}}D_{\rm node}.
}
\]

For any \(V\) and actual class \(\Gamma\), either that class reaches the thick core at the current node, where (7) applies, or the core-or-boundary lemma places it entirely within at least one child. Descending through the tree eventually reaches a node where (7) applies.

Every constructed path remains in the original actual communicating class. The finite-control restriction is used only when that class has already been proved to stay within the corresponding coordinate bounds.

Therefore the proposed construction gives the requested uniform inequality for every class.

## 8\. Computation and bit costs

The construction uses finite exact arithmetic throughout.

**Fixed-input compiler.** Control graphs and return words are finite graph computations. Integer-lattice normal forms use exact integer arithmetic. Graver bases are obtained from finitely many rational polyhedral cones and their Hilbert bases. Backward coverability is the explicit antichain saturation of Section 4.2. The search for \(K\) uses exact Gröbner-basis module intersections and membership tests. Every integer, rational coefficient, polynomial, word and intermediate expression is represented in binary; none is treated as an oracle.

These procedures have computable finite bit costs, potentially enormous in the complete input length \(B\)\. In particular, an a priori recursive worst-case cost function can be defined constructively by enumerating all valid binary inputs of length at most \(B\), executing this proved-terminating compiler on each, and taking the maximum number of elementary bit operations. This also bounds the output bit lengths. No elementary or polynomial dependence on \(B\) is asserted.

**Optional per-volume computation.** For a specified \(V,x_0\), a deterministic implementation can enumerate the actual class by breadth-first search. There are at most \((AV+1)^d\) states. Exact rational stationary weights have \(O_{\text{fixed}}(V\log(2+V))\) bits, so the finite base-fibre maximizer and selected paths can be computed using polynomially many bit operations in numeric \(V\)\. A deliberately loose bound is \(O_{\text{fixed}}((1+V)^{d+10})\) with schoolbook integer arithmetic.

Individual physical rates are exact rationals whose evaluation requires only a fixed number of falling-factorial factors and integer powers. All comparisons can be performed exactly. There is no floating-point precision requirement and no random-bit cost.

Stationary normalization is not required by the compiler or the path proof: every comparison uses \(W_V(u)/W_V(v)\), in which \(Z_\Gamma\) cancels. There is no infinite tail estimate because conservation makes every class finite. Exact normalization, if independently requested for a given \(V\), is also a finite sum over the enumerated class with polynomial-in-\(V\) bit cost.

## Conclusion

The construction above gives a positive answer to the stated polynomial physical-time Poincaré question, conditional on the standard exact algebraic and integer-lattice algorithms used in its finite subroutines.

The central mechanism is the combination of\:

- The core-or-bounded-coordinate dichotomy for finitely presented population graphs.
- Fixed-word realization of every Graver move after entering a sufficiently thick core.
- Monotone improvement of separable log-factorial stationary weights.
- Polynomial-weight rooted paths, followed by an explicit Dirichlet-form comparison.

This proof does not require deficiency zero, detailed balance, positive initial populations, identification of classes with saturated lattice fibres, or any modification of the physical rates.

The product-form stationary law is the established Anderson–Craciun–Kurtz ingredient. citeturn824951search2 The volume-uniform polynomial conclusion here comes from the additional construction and argument, not from that stationary-law theorem or from a previously verified published result.

This is a self-contained proposed mathematical proof, not an independently peer-verified theorem. In particular, the claimed full endpoint rests on the correctness of the finite-control lifting and the module-theoretic dichotomy as applied above.

