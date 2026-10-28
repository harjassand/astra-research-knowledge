# Scoped review: observable acquisition cost and a reachable norm-one source

28 October 2026. Independent review of sections 1–2 of
`ABSORBING_BOUNDARY_EXTENSIONS.md`, `core/absorbing_slow_family.py`, and its
seven saved exact receipts. The previously reviewed matrix/domain theorem,
main acquisition, energy theorem, and calibration lower bound are accepted
dependencies here. Sensor errors are outside this review.

**Conclusion:** the stated expected acquisition rates and the concrete
infinite-state family are sound at their stated scope. No unresolved
mathematical objection was found. The receipts verify exact source algebra;
they do not execute the proposed statistical acquisition.

## 1. The observable conditions give the claimed complete expected cost

Write the scalar boundary holding probability as $p=1-d$, with

\[
c g\le d\le Cg,\qquad a_H\ge c_a g,\qquad
u_H\le C_u g^2,\qquad \mathbb E L_H\le C_L.
\]

Here $u_H$ denotes the probability of a nontrivial return by the fixed
censor time or of still being alive outside at that time. It does not denote
only the pending probability. Every trial begins at the same exact boundary
state, using genuine preparation when exact boundary continuation is not
available. This is the common reversible, nonintrusive observation setting
of the main construction.

For $N=K g^{-3}\log(q/\delta)$ fixed trials per primitive, with a sufficiently
large class-dependent constant $K$, variance-aware Bernoulli bounds give,
simultaneously over primitives and their finitely many event counters,

\[
|\widehat p-p|
 =O\!\left(\sqrt{g\log(q/\delta)/N}
             +\log(q/\delta)/N\right)=O(g^2).
\]

The same bounds give an upper endpoint $u_U=O(g^2)$, and a lower absorption
endpoint $a_L=\Omega(g)$. The latter is compatible with $a_H\le d=O(g)$.
The accepted local source-form inequalities consequently yield

\[
M_b=O(g^{-1}),\qquad
Q_p\le u_U+\frac{u_U^2}{2a_L}
              +\frac{u_U^2}{2(2p_L+a_L)}=O(g^2).
\]

Transferring to the acquired scalar model costs

\[
\sqrt{Q_{\widehat p}}\le\sqrt{Q_p}
               +|\widehat p-p|\sqrt{M_b}
          =O(g)+O(g^{3/2}),
\]

so $Q_{\widehat p}=O(g^2)$. The computational dissipation is

\[
R=1-\widehat p^2=\Theta(g).
\]

Therefore the dynamic normalization is \(\theta^2=O(g)\). With exact scalar
Gram entry one, the weak-defect interval radius is $O(g^2)$, and its
dissipation normalization is \(\zeta=O(g)\). The accepted corrected all-word
theorem gives $O(g)$ error. This uses no strict global source norm cap and
does not introduce a hidden-dimension factor.

The expected total source work is at most $qNC_L$, hence

\[
O\!\left(qg^{-3}\log(q/\delta)\right).
\]

Observing the fixed labels once per source step has the same order. This
counts source operations and label reports separately from any physical
cost of realizing the warranted reset and observation interfaces.

A trial that finishes at the exact boundary can continue directly into the
next trial. The strong Markov property supplies the correct fresh trial law.
A new preparation is needed only after a departed trial finishes outside;
that event has probability at most $d=O(g)$. Thus expected preparations are
at most $q+O(qNg)$, or

\[
O\!\left(qg^{-2}\log(q/\delta)\right)+q.
\]

This is an upper bound on preparations, not a matching preparation lower
bound. Expected trial length alone also does not prove a deterministic or
high-probability total-work bound. The text correctly distinguishes those
claims. Adaptive choices of sample count or censor time would require their
own simultaneous/anytime confidence accounting; the result reviewed here
uses fixed choices.

The already reviewed one-live-state survival alternatives satisfy these
observable conditions: their departure and immediately visible absorption
are \(\Theta(g)\), the return-or-pending probability is zero, and every trial
costs one source step. The accepted, accuracy-constant-matched
\(\Omega(g^{-3})\) source-action lower bound therefore remains a lower bound
for this larger observable class. This matches the exponent, not its
dependence on $q$, all preparation tradeoffs, or a particular certificate's
numerical constant. Ordinary variance-aware survival calibration matches
the lower family. The new contribution is the acquired local source form
that extends a sound certificate to the larger class.

## 2. The infinite source is a genuine reachable norm-one example

Let $0<g\le1/4$, $S=g^3/16$, and use the stated symmetric star source:
boundary diagonal $p=1-g$; fast edge $g/2$, fast diagonal $1/4$; and
slow edges and exit rates

\[
w_n=S2^{-n-1},\qquad \eta_n=4S2^{-n},\qquad n\ge0.
\]

All row deficits are positive. They are $g/2-S$ at the boundary,

\[
\frac34-\frac g2
\]

at the fast state, and \(\eta_n-w_n=7\eta_n/8\) at slow state $n$.
The operator is entrywise nonnegative, symmetric, and substochastic, so the Schur
test bounds its \(\ell^2\) norm by one. Unit vectors supported at increasingly
slow states have Rayleigh quotients $1-\eta_n\to1$, so the norm equals one.
Every slow state has a positive edge from the boundary. This is not an
unreachable norm-one block attached to an otherwise gapped source.

There is no nonzero fixed live vector: the killed-chain Dirichlet identity

\[
\langle x,(I-A)x\rangle
=\frac12\sum_{i,j}A_{ij}|x_i-x_j|^2
 +\sum_i\left(1-\sum_jA_{ij}\right)|x_i|^2
\]

has nonnegative terms and strictly positive killing coefficient at every
state. A fixed vector makes every term zero, hence every coordinate zero.
This ordinary infinite-dimensional argument is essential; a finite
truncation receipt alone would not establish norm one or the kernel claim.

The eventual excursion return probability is

\[
r_\infty
=\frac{(g/2)^2}{1-1/4}+\sum_{n\ge0}\frac{w_n^2}{\eta_n}
=\frac{g^2}{3}+\frac S8.
\]

Let $h=H-1$ be the least nonnegative integer with $4^{-h}\le g/8$.
Fast pending mass is \((g/2)4^{-h}\le g^2/16\), while all slow pending mass
is at most $S$. Thus the actual return-or-pending probability $u_H$ is
at most

\[
U=\frac{g^2}{3}+\frac S8+\frac g2\,4^{-h}+S
\le\left(\frac{19}{48}+\frac9{512}\right)g^2
=\frac{635}{1536}g^2<\frac{g^2}{2}.
\]

This upper bound is conservative because it counts some eventual returns
that would arise from pending paths. It does not mistake the two events for
disjoint events. The actual absorption probability is $a_H=g-u_H$, hence

\[
a_H\ge g-U\ge\frac{7g}{8}.
\]

Consequently the negative-sector margin is at least $55/32$, and the
stated simple constants follow:

\[
M_b\le\frac4{7g}+\frac{16}{55}
       \le\frac{248}{385g},
\qquad
Q_{\rm upper}\le\frac{g^2}{2}+M_b\frac{g^4}{4}
       \le\frac{208}{385}g^2.
\]

Since $1-p^2=2g-g^2\ge7g/4$, the weighted dynamic bound is at most

\[
\frac{2Q_{\rm upper}}{1-p^2}
\le\frac{1664}{2695}g<g.
\]

By contrast, the exact unweighted bound supplied with the exact same model
and exact residual is

\[
\frac{\|D\|^2}{(1-p)^2}
=\frac{(g/2)^2+S^2/3}{g^2}
=\frac14+\frac{g^4}{768}\ge\frac14.
\]

The comparison is correctly restricted to those certificates; it is not a
lower bound against an equally informed method using the new local form.

## 3. Censoring is essential to the cost claim

The censored trial obeys

\[
\mathbb E L_H
\le1+\frac{g/2}{1-1/4}+S(H-1)
=1+\frac{2g}{3}+\frac{g^3h}{16}<2.
\]

The coarse inequality $h\le8/g$ already proves this; the actual growth is
only logarithmic. Across $N$ trials of one primitive, if $D_N$ is the
number of first-step departures, total length is at most $N+hD_N$.
Here $D_N$ is binomial with mean $gN$, so its ordinary fixed-budget
Chernoff bound gives $D_N=O(gN)$ with the required high probability.
Because $gh\le8$, the high-probability source work is $O(N)$. A union
bound supplies the corresponding $q$-primitive statement.

There is a useful limitation in this very example. The *uncensored* mean
excursion length is infinite:

\[
\sum_{n\ge0}\frac{w_n}{\eta_n}
=\sum_{n\ge0}\frac18=\infty.
\]

Each individual slow state exits almost surely, yet the reachable mixture
has infinite mean waiting time. Small local return forms therefore do not
justify unlimited waiting or bounded acquisition work by themselves. The
finite censor, its small unresolved mass, and the explicit expected-length
condition are substantive parts of the result. The construction keeps the
slow mass small enough to certify it without resolving all slow modes.

## 4. Replayed evidence and frozen inputs

`review_absorbing_slow_cost.py` independently reconstructs the seven saved
receipts using closed scalar expressions, checks horizon minimality and the
all-scale rational constants, and verifies exact equality to every reported
fraction. It does not import or call the source implementation, generate
new stochastic data, or approximate the infinite source by a finite matrix.
Its output is `ABSORBING_SLOW_COST_REVIEW_CHECKS.json`.

Reviewed input SHA-256 values:

- `ABSORBING_BOUNDARY_EXTENSIONS.md`, the exact UTF-8 prefix before
  the first literal `## 3.`:
  `413060e0c8bbc6bc3ae0136bd95e0533481afbe8a05f3ec8fea1233f8a476833`.
  This binds sections 1–2 independently of concurrent edits to excluded
  section 3.
- `core/absorbing_slow_family.py`:
  `4120b60bd145299ded3bc58e7b89c4c5598daee4568555a5b099a238d00666e2`.
- `results/ABSORBING_SLOW_FAMILY.json`:
  `c86306f6e647f7cbdd3d91c51da5d4c11fe968b8dd9cbb8f0305d8e5c35e9e00`.
- Accepted lower-bound dependency,
  `branches/scalar/CALIBRATION_COST_THEOREM_REVIEW.md`:
  `a8b07e62ddbefb5c81e3a970d7599a47ca19ba28949d4513c69991183f9cf1f0`.
