# Adaptive prefix-cover acquisition: scoped cost theorem and review

28 October 2026. Ordinary proof only; no new Monte Carlo execution and no
change to the existing balanced-tape acquisition or its receipts.

**Conclusion.** The proposed zero-terminal algorithm and its
\(C_{\epsilon/2}\)-dependent cost bound are correct. The adaptive node
selection does not invalidate the confidence guarantee when each selected
word receives a fresh fixed batch. Minimality is particularly simple:
the minimum cover is the unique tree that stops at the first sufficiently
small-survival prefix.

Two optional refinements are substantive. Summable conditional confidence
spending also gives almost-sure termination and an unconditional expected
cost bound when the comparison cover is finite. If terminal predictions
may be nonzero interval midpoints, the same accuracy can instead be tied
to \(C_\epsilon\).

## 1. Definitions and statistical interface

Let \(\mathcal A\) be a finite alphabet of size \(q\ge1\). For a word \(w\),
let \(f(w)\in[0,1]\) be its survival probability from the fixed preparation,
with \(f(\varnothing)=1\). Irreversible absorption gives

\[
 f(wu)\le f(w)
\]

for every extension \(u\). This prefix monotonicity is the only structural
property needed for the cover and cost theorem. Selfadjointness and the
common order vector belong to the separate theorem that obtains a finite
switched tail from primitive repetitions.

A finite full \(q\)-ary prefix tree contains its root and every child of
each nonterminal node. It is an \(\eta\)-cover if every terminal word has
true survival at most \(\eta\). Let \(C_\eta\) be its minimum number of
nodes, or infinity if no finite cover exists. Root is included.

At each selected nonroot word, a trial starts from a genuine fresh
preparation and supplies a Bernoulli indicator with mean \(f(w)\).
Conditional on the history selecting that word, its batch consists of
independent such trials. The word and batch size are fixed before its
batch is inspected. Physical execution may stop after confirmed absorption:
the full-word indicator is then known to be zero.

This is a fresh-batch theorem. Applying its visit-index confidence budget
retroactively to prefixes selected after inspecting an existing shared
data set would require a different selection argument. The existing
balanced-tape acquisition uses its own preallocated potential-prefix
confidence accounting and is not being relabeled here.

## 2. The comparison tree is canonical

For \(0<\eta<1\), begin at the root. Stop a branch at the first node with
\(f(w)\le\eta\); otherwise include all \(q\) children.

Any valid \(\eta\)-cover must expand every encountered node with
\(f(w)>\eta\). It therefore contains this canonical tree. Conversely, if the
canonical tree is finite, it is a valid cover. Expanding one of its
terminal nodes cannot reduce node count.

Hence, whenever \(C_\eta<\infty\), the canonical tree is the unique minimum
cover. Denote it by \(T_\eta\), its maximum depth by \(H_\eta\), and its
number of internal nodes by \(I_\eta\). Then

\[
 C_\eta=1+qI_\eta.
\]

In particular, existence of some finite cover is enough; the learner
does not need \(C_\eta\), its depth, or the true canonical tree as inputs.

## 3. The proposed zero-terminal algorithm

Fix \(0<\epsilon<1\) and \(0<\delta<1\). Root survival is exactly known and
needs no trials. Index the other queried nodes by their order of visit,
\(j=1,2,\ldots\), and spend

\[
 \delta_j=\frac{\delta}{j(j+1)},\qquad
 r=\frac{\epsilon}{4},\qquad
 N_j=\left\lceil
       8\epsilon^{-2}
       \log\frac{2j(j+1)}{\delta}
      \right\rceil.
\]

For its fresh batch, let \(\widehat f_j\) be the empirical mean and use

\[
 L_j=\max(0,\widehat f_j-r),\qquad
 U_j=\min(1,\widehat f_j+r).
\]

If \(U_j\le\epsilon\), mark the node terminal. Otherwise record its interval
midpoint as the prediction at that exact word and include every child.
Process the resulting finite frontier fairly. On a terminal word and
every extension of it, predict zero. Predict one at the empty word.

Conditional Hoeffding gives

\[
 \Pr\!\left(
  |\widehat f_j-f(w_j)|>r
  \mid\hbox{history before batch }j
 \right)
 \le 2e^{-2N_jr^2}
 \le\delta_j.
\]

The selected word is random but already fixed in this conditioning.
Independence between different batches is not needed beyond the stated
conditional sampling law. Define failures after termination to be empty
events. The countable union bound and
\(\sum_{j\ge1}1/[j(j+1)]=1\) give a simultaneous event \(\mathcal G\)
with probability at least \(1-\delta\).

On \(\mathcal G\),

\[
 f(w_j)\le U_j\le f(w_j)+2r
                 =f(w_j)+\epsilon/2.
\]

Thus every node with true survival at most \(\epsilon/2\) is necessarily
terminal. If \(C_{\epsilon/2}<\infty\), the acquired tree is a subtree of
\(T_{\epsilon/2}\); it can stop earlier but cannot expand one of that
tree's terminal nodes. It consequently visits at most
\(C_{\epsilon/2}\) nodes and has depth at most \(H_{\epsilon/2}\).

At a nonterminal word, the midpoint error is at most half the interval
width, hence at most \(\epsilon/4\). At a terminal word and all its
extensions, survival is between zero and \(U_j\le\epsilon\), so the
zero prediction has error at most \(\epsilon\). Full prefix coverage
exhausts all finite words. The all-word error is therefore at most
\(\epsilon\) on \(\mathcal G\).

No union bound over the infinite target language is needed: only the
finite acquired node intervals and deterministic prefix monotonicity are
used.

## 4. Complete costs on the simultaneous event

Write \(C=C_{\epsilon/2}\), \(H=H_{\epsilon/2}\), and

\[
 B_C=
 1+8\epsilon^{-2}\log\frac{2C(C+1)}{\delta}.
\]

There are at most \(C-1\) measured nodes; root is free. The complete
preparation count is

\[
 P=\sum_{\text{queried }j}N_j
 \le (C-1)B_C
 =O\!\left(C\epsilon^{-2}\log(C/\delta)\right).
\]

No preparation reuse is assumed merely because a previous trial remained
alive. Coarse survival does not identify that hidden state with the
preparation distribution.

Every trial at word \(w_j\) uses at most \(|w_j|\) primitive applications.
Consequently the total source work satisfies the sharper bound

\[
 S\le\sum_j|w_j|N_j
 \le B_C\sum_{w\in T_{\epsilon/2}\setminus\{\varnothing\}}|w|
 \le H(C-1)B_C.
\]

Thus

\[
 S=O\!\left(
  HC\epsilon^{-2}\log(C/\delta)
 \right).
\]

With one nonintrusive survival report per executed application, reports
have the same upper bound. The actual censored ledger may be smaller and
should be reported as executed rather than replaced by the worst-case
word lengths. Any separate physical price of a warranted preparation or
report must multiply these respective counts.

These are acquired, sampling-based confidence costs. A nominal count of
scalar measurements is not standing in for precision.

## 5. Summable spending also controls cost outside the good event

This optional strengthening avoids leaving the expectation undefined on
the confidence-failure event.

Let \(E_j\) be the confidence failure at queried node \(j\), and
\(B=\sum_j1_{E_j}\). Then

\[
 \mathbb EB\le\sum_j\delta_j=\delta,
\]

so \(B<\infty\) almost surely. Every expanded node that is not an internal
node of \(T_{\epsilon/2}\) lies at or below a canonical terminal node.
Prefix monotonicity gives its true survival at most \(\epsilon/2\);
expanding it therefore requires its own confidence failure. If the
algorithm's internal-node count is \(I\),

\[
 I\le I_{\epsilon/2}+B.
\]

Only finitely many expansions can occur almost surely. Fair processing
and finite batches then give almost-sure termination, even though no
deterministic worst-case tree-size cap is imposed. For its completed
node count \(M=1+qI\),

\[
 \boxed{\quad \mathbb E M\le C+q\delta.\quad}
\]

More is available because the conditional failure bound holds at every
visit. For each \(\theta>0\), iterated conditioning gives

\[
 \mathbb E e^{\theta B}
 \le\prod_{j\ge1}\left[1+\delta_j(e^\theta-1)\right]
 \le\exp\!\left(\delta(e^\theta-1)\right).
\]

No independence assumption for the failure events is used. Also,

\[
 M\le C+qB,\qquad
 \text{maximum acquired depth}\le H+B.
\]

The latter holds because every expansion beyond the first canonical
terminal on a path is a counted failure. Since \(q\le C\), \(H\ge1\), and
\(\delta<1\), the exponential-moment bound controls all fixed moments of
\(B\). Applying it to the logarithmic batch-size formula gives

\[
 \mathbb E P
 =O\!\left(C\epsilon^{-2}\log(C/\delta)\right),\qquad
 \mathbb E S
 =O\!\left(HC\epsilon^{-2}\log(C/\delta)\right).
\]

For example, \(M\le C(1+B)\), so
\(\log(M+1)\le \log(C+1)+\log(1+B)\); the source-work bound adds at most
another factor \(1+B\). Their expectations are bounded by the displayed
exponential moment. The implicit constants here are absolute.

These expectations concern the same algorithm and finite-cover
population condition. They do not make an incorrect output on a
confidence-failure event correct.

## 6. A midpoint-terminal alternative changes the comparison threshold

If zero predictions after terminal nodes are not required, an
\(\epsilon\)-accurate scalar predictor can use a more favorable cover
threshold. For \(0<\epsilon<1/2\), take

\[
 r=\epsilon/2,\qquad
 N_j=\left\lceil
       2\epsilon^{-2}
       \log\frac{2j(j+1)}{\delta}
      \right\rceil
\]

and declare a node terminal when \(U_j\le2\epsilon\). For that word and
all its extensions, predict \(U_j/2\). Their true survivals lie in
\([0,U_j]\), so error is at most \(\epsilon\). Branch midpoint error is
at most \(\epsilon/2\).

On the simultaneous event \(U_j\le f(w_j)+\epsilon\), every node with
\(f(w_j)\le\epsilon\) is necessarily terminal. The acquired tree is
therefore a subtree of \(T_\epsilon\). All preceding cost and expected
overshoot arguments hold with \(C_\epsilon,H_\epsilon\), and the smaller
batch constant.

This is more than a constant improvement in sample size when the true
cover complexity changes sharply with its survival threshold. It changes
the terminal prediction convention; it is not an assertion that the
original zero-terminal rule already attains \(C_\epsilon\). For
\(\epsilon\ge1/2\), a constant \(1/2\) predictor already has the desired
absolute accuracy for probabilities.

## 7. Scope of the context-complexity resource

The condition \(C_{\epsilon/2}<\infty\) is sufficient, not necessary for
learnability or for this algorithm to stop. Its slack absorbs statistical
uncertainty. One cannot simply replace it by \(C_\epsilon\) in the
zero-terminal proof while keeping the same fixed radius and cutoff.

Cover size is also representation-specific, not an established
minimax sample-complexity lower bound. For the identity source,
\(C_\eta=\infty\) for every \(\eta<1\), although the constant-one response
has a trivial predictor. With one action, a single complete or censored
lifetime record supplies many prefix indicators, so fresh trials for each
prefix can cost more preparations than shared-trajectory estimation.
Additional structural models or carefully accounted prefix sharing can
likewise improve the present route.

The theorem exposes the number and depth of observable contexts as an
explicit sufficient resource, with paid estimation precision. It does not
remove possible exponential growth of \(C_\eta\), establish optimality
against every equally informed method, or introduce a new general
statistical principle.
