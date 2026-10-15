# Toom cluster tail: finite-torus interface

**Strongest direct source.** Hartarsky–Toninelli, *Kinetically constrained models out of equilibrium*, arXiv:2212.08437v2, §9, Corollary 9.5: for an attractive eroder CA with iid death probability \(\delta\), the maximal \(k\)-connected **space-time zero component through a fixed point** in the process started from its **upper invariant measure** has
\[
\Pr(\operatorname{diam} A_{x,t}\geq\ell)\leq\delta^{c(\ell+1)}.
\]
This is a cluster theorem, stronger than density stability; it is infinite-lattice and stationary. On \(\mathbb Z^d\), cold-start fixed-time tails follow because the all-one start stochastically dominates the upper invariant law at every time. The zero-cluster event is decreasing, and any spatial-slice zero path is a space-time zero path.

For finite histories with local-stochastic faults, the contour mechanism behind this result is also suitable: every present contour requires its distinct sink set to be faulty, so \(\Pr(S\subset F)\leq\eta^{|S|}\) supplies the contour weight; disjoint contour supports have disjoint sinks and the corresponding joint bound. HT §9.1 Proposition 9.3 is the decorated-set estimate that converts these weights and exponential contour counts to cluster tails. Alternatively, finite-range-dependent fresh fault flags can be dominated by iid faults using LSS, if their dependence radius and marginal bound are uniform.

**Finite-torus stopped transfer (checked conditional argument).** A finite-torus *all-time* cluster tail is impossible for zero-preserving Toom maps: on an \(N\)-site torus, a complete death layer has probability \(\delta^N\) per round and creates the absorbing all-zero state. Thus
\[
\Pr(\text{all-zero reached by round }T)\geq 1-(1-\delta^N)^T\longrightarrow1.
\]
This does not block a finite-horizon estimate.

The source results can support a finite-horizon stopped estimate without copying a whole backward light cone, provided the actual coarse update has the following form: a monotone DNF/OR-of-AND map \(\phi(x)=\bigvee_i\bigwedge_{a\in A_i}x_{x+a}\); each faulted update is dominated, for the bad-state order, by forcing output 0; each fault flag depends only on fresh primitive noise in a fixed guard of radius \(R\); and the relevant fault field has the stated local-stochastic bound (or a uniform LSS iid domination). Take \(k\) large enough that every space-time parent offset \((a,-1)\) is \(k\)-adjacent.

Reveal zero nodes in time order and stop at the first insertion producing a complete \(k\)-connected **space-time** zero component of diameter at least \(\ell\). The new anchor joins only prior components of diameter below \(\ell\); hence the entire newly formed component lies in a deterministic patch of radius at most \(\ell+k\) (up to the chosen metric constants). Crucially, for every nonfault zero node \(z\), the DNF equation being zero implies that each one-set \(A_i\) has a zero parent. Those parents are \(k\)-adjacent to \(z\), so belong to the same complete zero component. Recursing backwards therefore keeps all required zero ancestry inside the stopped component and ends at a fault or the all-one initial boundary. Healthy parents outside the component are irrelevant: one zero in each \(A_i\) forces the DNF output to zero.

Consequently, if \(\ell+k+R\) is below the torus injectivity radius, that component and all fault guards needed to reproduce it lift injectively to an infinite-lattice patch. Define the local witness event as existence of such a closed zero set in the patch. The finite-torus first crossing implies this witness; replaying its fault guards in the infinite CA reproduces all its zero nodes by induction, so it implies an infinite-lattice space-time component of diameter at least \(\ell\). The local primitive law in the patch is identical after the injective lift. The infinite-lattice contour tail then gives a per-anchor bound \(C\delta^{c\ell}\) (or its local-stochastic analogue). A union bound over \(|V|(T+1)\) space-time anchors yields
\[
\Pr(\text{some spatial zero component reaches diameter }\ell\text{ by }T)
\leq C|V|(T+1)\delta^{c\ell},
\]
when \(\ell+k+R<\operatorname{injrad}(V)\). This is sufficient for an exponential-in-\(L\) horizon with \(\ell=\Theta(L)\), if constants leave room.

This argument avoids the winding-contour issue by lifting only the first-crossing component and its bounded local guards, not an arbitrary Toom contour or the entire backward light cone. It is a finite-horizon proof adapter, not a theorem stated in HT. The exact Q1 model still must verify the DNF/one-set representation, parent adjacency, fault-to-zero domination, fresh-primitive-only guard dependence, and the patch-radius inequality; if it is multiregister, the scalar binary Toom theorem needs a proved encoding or a componentwise reduction.

**Source gates.** Swart–Szabó–Toninelli, *Peierls bounds from Toom contours*, current arXiv v3, §2.3 Theorem 22 gives contour existence for a maximal trajectory on an arbitrary acyclic typed-dependence graph, hence applies to a finite time slab with an all-one initial layer. Quantitative estimates are separate: §5.3 Lemma 40 bounds edge counts by sink counts for a restricted Peierls contour family using a linear polar potential on \(\mathbb Z^d\). Neither that lemma nor HT Cor. 9.5 states a general periodic-boundary winding estimate. Do not cite it as a torus theorem; use the stopped-component localization above and check its local-update hypotheses. This is a gap in direct source transfer, not a counterexample to the autonomous-memory theorem. Both CA sources concern synchronous discrete-time updates; a Poisson-to-layer reduction is a separate interface.

Primary sources:
- Hartarsky–Toninelli, arXiv:2212.08437v2: https://arxiv.org/html/2212.08437v2 (§2.4; §9.1 Prop. 9.3; §9.2 Cor. 9.5; §9.3).
- Swart–Szabó–Toninelli, arXiv:2202.10999v3: https://arxiv.org/html/2202.10999v3 (§2.3 Thm. 22; §2.5 Thm. 26; §5.3 Lemma 40).
