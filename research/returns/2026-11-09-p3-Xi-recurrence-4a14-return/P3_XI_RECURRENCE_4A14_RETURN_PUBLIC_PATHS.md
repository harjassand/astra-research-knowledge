# P3 Xi return

Chat: https://chatgpt.com/c/6af0a937-daa0-83ec-99c5-8df8b56023e0
Prompt source: P3_FULL_STOCHASTIC_RECURRENCE_AFTER_MARKED_COUNTEREXAMPLE_UNRELEASED_20261108.txt
Prompt turn: 4a14f540-2074-49b6-8862-ecb89033e3ec
Response: 6ad9fc71-07a7-4c2c-a72c-4835d352c289
Model selected at dispatch: GPT-6 standard, Extra High. Collected 9 November 2026 Brisbane.
No ZIP visible.

## Complete response

# Full weak-reversibility recurrence problem

## 1\. What is established

An unrestricted proof or counterexample is not yet established by the sources examined. The central difficulty is proving finite expected return times and nonexplosion for every weakly reversible network, with no restriction on linkage classes or molecularity.

There is, however, a rigorous universal result.

**Theorem — Closed communicating classes under weak reversibility.**

For every finite weakly reversible reaction network, every positive rate vector, every dimension \(d\), and every initial state \(x_0\),

\[
\boxed{\Gamma(x_0)\text{ is a closed, irreducible communicating class.}}
\]

To prove this, consider an enabled reaction \(y\to y'\) at population \(x\)\. Write \(x=\rho+y\), where \(\rho\geq0\)\. Weak reversibility supplies a directed path

\[
y'=z_0\to z_1\to\cdots\to z_m=y.
\]

After the original reaction, the population is \(\rho+z_0\)\. The path lifts directly to population states\:

\[
\rho+z_0\to\rho+z_1\to\cdots\to\rho+z_m=x.
\]

Every step is enabled because its source complex is present. Thus every allowed population transition can be reversed by a finite path. Reversing an arbitrary sequence establishes mutual reachability.

This proves class closure without requiring binary reactions, a single linkage class, complex balance, or any restriction on boundary states. It is the established lifted-path argument of Kriebel's Lemma 2.2, not a new result. citeturn596283view1turn248003view2

**What this does not prove\:** a closed communicating class can still fail to be positive recurrent, and the existence of finite return paths does not rule out explosion.

## 2\. A complete positive-recurrence result for rank-one networks

The full conclusion holds for **arbitrary molecularity and arbitrary numbers of linkage classes when the stoichiometric subspace has dimension at most one**\. This is an established result of Wiuf and Xu; the following gives a direct proof of the relevant case. citeturn605902search0turn605902academia20

Let

\[
S=\operatorname{span}_{\mathbb R}\{y'_r-y_r:r\in\mathcal R\}.
\]

If \(\dim S=0\), every population is absorbing. Suppose \(\dim S=1\), and choose a primitive integer vector \(v\) spanning \(S\)\.

If \(v\) has both positive and negative coordinates, the intersection

\[
(x_0+\mathbb Rv)\cap\mathbb N_0^d
\]

is bounded. The reachable class is consequently finite.

Otherwise orient \(v\) so that \(v\geq0\)\. States on the class can be written

\[
x=x_0+nv
\]

for integers \(n\) in a subset bounded below.

A reaction has displacement \(a_rv\) for some integer \(a_r\)\. All coordinates with \(v_i=0\) are invariant, and their source requirements are identical throughout each linkage class. Thus, a linkage class is either permanently disabled by those requirements or eventually has all its reactions enabled as \(n\to\infty\)\.

For an active complex \(y\), set

\[
h(y)=\sum_{i:v_i>0}y_i.
\]

Its propensity, as a function of \(n\), is a polynomial with strictly positive leading coefficient and degree \(h(y)\)\. Moreover,

\[
h(y'_r)-h(y_r)
=a_r\sum_i v_i.
\]

Let \(D\) be the largest degree attained among active nontrivial linkage classes. At degree \(D\), every reaction has \(a_r\leq0\), and at least one has \(a_r<0\)\. Indeed, strong connectivity forces a path from a maximal-degree complex to a lower-degree complex.

Therefore the leading coefficient of the drift of \(n\) is strictly negative\:

\[
\mathcal Ln=-c n^D+O(n^{D-1}),
\qquad c>0.
\]

Consequently, for sufficiently large reachable \(n\),

\[
\mathcal Ln\leq-1.
\]

After shifting \(n\) by a constant to make it a nonnegative proper function, this is a Foster–Lyapunov drift inequality. It proves nonexplosion, finite mean return times, and positive recurrence on every nonabsorbing class. Standard irreducible continuous-time Markov-chain theory then gives uniqueness of the stationary probability and total-variation convergence.

The important point is that this proof works because all unbounded population changes are ordered along a single stoichiometric direction. It does **not** establish an ordering among competing high-order reactions when \(\dim S\geq2\)\.

## 3\. A general structural drift bound

There is also a useful statement for networks with any number of species and linkage classes.

Let \(M(x)=\sum_i x_i\)\. Call a linkage class *mass-changing* if its complexes do not all have the same molecularity, and define

\[
D=\max\{|y|:y\text{ belongs to a mass-changing linkage class}\}.
\]

If there are no mass-changing linkage classes, \(M\) is conserved and every reachable class is finite.

Otherwise, weak reversibility implies\:

1. A mass-increasing reaction has source molecularity at most \(D-1\)\.
2. No reaction of source molecularity greater than \(D\) changes total mass.
3. At least one reaction of source molecularity exactly \(D\) strictly decreases total mass.

The third assertion follows because a linkage class attaining \(D\) must contain a directed path from a maximum-molecularity complex to a lower-molecularity complex.

Consequently,

\[
\mathcal LM(x)
\leq C(1+M(x))^{D-1}.
\]

More strongly, take a degree-\(D\) mass-decreasing reaction with source \(y_*\)\. In every cone satisfying

\[
x_i\geq\eta M(x)
\quad\text{for all }i\text{ with }(y_*)_i>0,
\]

where \(\eta>0\), its negative propensity is of order \(M(x)^D\), while every positive contribution to \(\mathcal LM\) is at most order \(M(x)^{D-1}\)\. Hence, for sufficiently large \(M(x)\) in that cone,

\[
\boxed{\mathcal LM(x)\leq-c_\eta M(x)^D.}
\]

This establishes strong radial dissipation in an interior region for arbitrary molecularity.

It also gives the following unconditional nonexplosion result: **if \(D\leq2\), the minimal CTMC is nonexplosive**, even if mass-preserving linkage classes have arbitrarily high molecularity. Indeed,

\[
\mathcal L(1+M)(x)\leq C(1+M(x)),
\]

and \(1+M\) has finite sublevel sets. The standard stopped-process Lyapunov argument rules out finite-time explosion.

This is not enough for full recurrence. Near a boundary face, the chosen degree-\(D\) restoring source can be disabled. The interior estimate supplies no negative drift there, and for \(D\geq3\) the global upper bound is not even linear. Both issues require additional arguments.

## 4\. An exact obstruction at higher molecularity

Consider the one-linkage, reversible network

\[
\boxed{
0\rightleftarrows B,\qquad
0\rightleftarrows A+2B,\qquad
0\rightleftarrows 2A+3B.
}
\]

Take all six rate constants equal to one.

This network has two species, one linkage class, and maximum molecularity five. Its reachable class from \((0,0)\) is all of \(\mathbb N_0^2\)\.

Indeed, \(0\to B\) increases \(B\) by one, while the enabled sequence

\[
0\to2A+3B,\quad
A+2B\to0,\quad
B\to0
\]

increases \(A\) by one without changing the final \(B\) count. Repeating these operations reaches every population.

### The network is demonstrably positive recurrent

For unit rates, its stationary distribution is

\[
\boxed{\pi(a,b)=\frac{e^{-2}}{a!\,b!}.}
\]

For each reversible pair \(0\rightleftarrows y\), detailed balance holds because

\[
\pi(x+y)(x+y)_y=\pi(x).
\]

The distribution has finite expected total reaction intensity, so the minimal process is nonexplosive. Its irreducibility and the displayed stationary probability establish positive recurrence.

### But the proposed terminal-rarity mechanism fails

Take the reachable marked states

\[
(x_n,t)=((n,0),0),\qquad \rho_n=(n,0).
\]

For every complex \(c\) in the reaction graph, and every source \(s\) enabled at \(\rho_n+c\), direct examination gives

\[
(\rho_n+c)_c\geq(\rho_n+c)_s.
\]

For example, at terminal \(c=A+2B\), its falling factorial is \(2(n+1)\), whereas those of the other enabled complexes are at most \(2\)\. At terminal \(c=2A+3B\), its falling factorial is \(6(n+2)(n+1)\), greater than that of every other enabled complex.

Therefore, Kriebel's exact marked-potential identity gives

\[
\delta(\rho_n+c,c)
=\sum_s p_{\rho_n+c}(s)
\log\frac{(\rho_n+c)_c}{(\rho_n+c)_s}
\geq0.
\]

Every designated target-following step has zero potential increment. Every intermediate and terminal phase has nonnegative expected increment. Thus **every fixed-residual target-following episode of this construction starting at the marked state \(((n,0),0)\) has nonnegative expected drift**\.

There is no divergent linear conservation law to eliminate these states: the reaction vectors \((0,1)\) and \((1,2)\) already span \(\mathbb R^2\)\.

This is an exact counterexample to extending the particular terminal-rarity argument directly to unrestricted molecularity. It is **not** a counterexample to positive recurrence. The same network was proved recurrent above.

The distinction is important: the full theorem requires a method that can account for competition between reactions following different complexes, rather than merely selecting one terminal complex whose source becomes rare. citeturn596283view2turn930542view2

## 5\. The unresolved part of the full conjecture

The strongest relevant established results have complementary scopes\:

| Network class | Established conclusion |
|--------|--------|
| All finite weakly reversible networks | Closed, irreducible reachable classes |
| Stoichiometric rank at most one | Full nonexplosion and positive recurrence citeturn605902search0 |
| One linkage class, molecularity at most two | Full positive recurrence in Kriebel v1.2.4, an unrefereed preprint citeturn637057view0 |
| Arbitrary bimolecular weakly reversible networks | Nonexplosion, established by Xu; unrestricted positive recurrence not established by that result citeturn330744academia42 |
| Two-species weakly reversible networks | A full positive-recurrence proof has been publicly announced by the ConStRAINeD collaboration; its publicly described scope is two species citeturn934759search1turn934759search6 |
| Arbitrary dimension, molecularity and linkage classes | Full positive-recurrence conjecture remains unresolved in the sources examined |

The transient and explosive examples in Anderson–Cappelletti–Kim–Nguyen, Examples 3.1–3.2, do not provide the requested negative answer: their reaction graphs are not weakly reversible. Their Theorem 7.2 requires additional dissipative reactions, and Theorem 7.3 is a conditional Foster–Lyapunov result, not a structural recurrence theorem for arbitrary weakly reversible networks. citeturn248003view3turn248003view5

For the unrestricted problem, the remaining task is to establish a class-wise finite-return-time argument that simultaneously handles arbitrary high-order boundary layers and interference between linkage classes. A negative resolution would instead require one explicit weakly reversible stochastic mass-action network, positive rates, and a proved explosive, null-recurrent or transient reachable class.

Neither the interior-drift bound nor the marked-potential calculations above provide that missing step.

## Final determination

**I cannot establish the requested full theorem or a valid counterexample.**

The analysis establishes the universal closed-class result, recovers the full rank-one recurrence theorem, derives a general radial-dissipation bound and an associated nonexplosion criterion, and demonstrates a precise obstruction to the higher-molecularity extension of the marked-target method.

Those conclusions are rigorous at their stated scope. They do not resolve the unrestricted Anderson–Kim positive-recurrence conjecture, and presenting them as a full resolution would be unjustified.

## Visible activity — Worked for 26m 20s

I’ll examine the specified results and their exact scope, then test whether a new Lyapunov or return-time argument can cover multiple linkage classes and arbitrary molecularity. I’ll also look for a counterexample in the stated mass-action model. I’ll keep a method obstruction separate from an actual failure of recurrence and avoid the held sources.
Evaluated the research task
Constructed counterexample and tested reaction cycle return paths
Assessed proof prospects, invariants, and candidate mechanisms
Developed entropy bounds and control strategies for thermodynamic recurrence dynamics
Searched 24 websites
The source review confirms a sharp distinction: Kriebel’s theorem covers one linkage class with molecularity at most two, while the published strongly-endotactic escape examples are not weakly reversible. The unrestricted case remains unresolved in the sources checked. I’m now testing a separate radial-drift argument; it gives a useful bound away from boundary faces, but that bound alone cannot establish recurrence.
Evaluated robustness
Explored recurrence, Lyapunov, entropy methods, and proof gaps
Assessed recurrence and stability arguments, conjecture, and proof gaps
Refined recurrence arguments and identified the obstruction
Searched 17 websites
A second test gives a sharper obstruction: a one-linkage, higher-molecularity network can have arbitrarily large reachable populations at which every fixed-residual target-following episode has nonnegative expected log-factorial drift. With unit rates, that same network has an explicit product-Poisson stationary law. This rules out a direct extension of the marked-path proof, not the recurrence conjecture.
Refined the obstruction
