**The strongest result from this investigation is a complete classification theorem for correlated products on finite commutative semigroups, with an explicit construction and sharp-order finite-size bounds. I have not established its historical originality or a landmark consequence sufficient to meet the historic objective.**

The central mechanism is concrete: **every output law satisfying a certain transport condition can be realized by replicas that are all identical except at one randomly chosen position**, while every individual replica retains exactly the prescribed input distribution.

There is also an important negative conclusion about significance: I derived a separate compact linear-programming formulation for the underlying feasibility problem. Consequently, replacing an exponentially large joint-distribution table is **not, by itself, a defensible claim of new computational power**.

correlated_product_research.zip[Complete research package](sandbox:/mnt/data/correlated_product_research.zip) · RESEARCH_NOTE.md[Research note and proofs](sandbox:/mnt/data/independent_math/RESEARCH_NOTE.md) · semigroup_replication.py[Exact-arithmetic constructor](sandbox:/mnt/data/independent_math/semigroup_replication.py)

## 1. The precise result

Let \(S\) be a finite commutative semigroup: a finite set with an associative, commutative multiplication. An identity is not required. Write \(m=|S|\).

Fix a probability distribution \(\mu\) with **full support**:
\[
\alpha:=\min_{x\in S}\mu(x)>0.
\]

We permit arbitrary dependence between random variables \(X_1,\ldots,X_n\), but require
\[
\mathcal L(X_i)=\mu
\qquad\text{for every }i.
\]

Define the attainable product laws
\[
\mathcal P_n(\mu)
=
\left\{
\mathcal L(X_1\cdots X_n):
\mathcal L(X_i)=\mu\ \text{for every }i
\right\}.
\]

The question is to characterize the entire set \(\mathcal P_n(\mu)\), rather than optimize one particular statistic of the product.

### The algebraic relation

For each \(x\in S\), let \(e_x\) denote its unique idempotent power. Thus some positive power of \(x\) equals \(e_x\), and
\[
e_x^2=e_x.
\]

Define
\[
xRz
\quad\Longleftrightarrow\quad
e_xz=z.
\]

This says that the eventual idempotent behavior of \(x\) preserves \(z\).

Now define a transport polytope:
\[
\mathcal T(\mu)
=
\left\{
\nu:
\begin{array}{l}
\exists\,\gamma(x,z)\ge0,\quad
\sum_z\gamma(x,z)=\mu(x),\\[2pt]
\sum_x\gamma(x,z)=\nu(z),\quad
\gamma(x,z)=0\text{ unless }xRz
\end{array}
\right\}.
\]

Membership in \(\mathcal T(\mu)\) is an ordinary bipartite transport-feasibility problem.

### Theorem: exact realization and asymptotic classification

Set
\[
n_0=\max\left\{3,\left\lceil\frac1\alpha\right\rceil\right\}.
\]

Then:

**Exact realization.** For every \(\nu\in\mathcal T(\mu)\) and every \(n\ge n_0\), there is an exchangeable coupling with individual marginal \(\mu\), product law \(\nu\), and the form
\[
(X_1,\ldots,X_n)
=
(B,\ldots,B,E,B,\ldots,B),
\]
where the exceptional position is uniform on \(\{1,\ldots,n\}\). At most \(m^2\) weighted choices of \((B,E,\text{product})\) are needed.

**Quantitative necessity.** For every \(n\ge1\),
\[
\sup_{\nu\in\mathcal P_n(\mu)}
\operatorname{dist}_{\mathrm{TV}}\!\left(\nu,\mathcal T(\mu)\right)
\le \frac{m-1}{n}.
\]

A sharper constant is available. Define
\[
t_x=\min\{r\ge1:e_xx^r=x^r\},
\qquad
c(S)=\min\left\{m-1,\sum_x(t_x-1)\right\}.
\]
Then the bound is \(c(S)/n\).

Consequently,
\[
\boxed{
\mathcal T(\mu)
=
\{\text{limits of attainable product laws as }n\to\infty\}.
}
\]

It is also exactly the set of fixed output laws attainable at arbitrarily large replica counts—and exactly the set attainable at every sufficiently large count.

If
\[
e_xx=x\qquad\text{for every }x\in S,
\]
then the finite-size discrepancy disappears:
\[
\boxed{\mathcal P_n(\mu)=\mathcal T(\mu)\qquad(n\ge n_0).}
\]

The threshold \(n_0\) is a uniform sufficient bound, not a claim of the optimal threshold for every individual instance.

## 2. Proof of the realization theorem

The proof separates the algebraic correction from the probability-marginal correction.

### A. The relation \(R\) is transitive

The powers of an element of a finite semigroup eventually become periodic. A sufficiently large exponent divisible by that period produces its unique idempotent power. Choose one exponent \(L\) that works simultaneously for every element.

Commutativity gives
\[
e_{xy}=(xy)^L=x^Ly^L=e_xe_y.
\]

Suppose \(xRy\) and \(yRz\). From \(e_xy=y\), taking the \(L\)-th power gives
\[
e_xe_y=e_y.
\]
Therefore
\[
e_xz=e_xe_yz=e_yz=z.
\]
Hence \(xRz\).

Reflexivity is not assumed and can fail.

### B. A transport-subtraction lemma

Suppose \(\mu\) admits an \(R\)-supported transport to \(\nu\), and
\[
\rho=\frac{n\mu-\nu}{n-1}\ge0,
\qquad n>1.
\]

Then \(\rho\) also admits an \(R\)-supported transport to \(\nu\).

To prove this, write the original transport as a stochastic kernel \(K\), so that
\[
\mu K=\nu.
\]
Define
\[
K'=(n-1)K(nI-K)^{-1}.
\]

Equivalently,
\[
K'
=
\left(1-\frac1n\right)
\sum_{j\ge1}n^{-(j-1)}K^j.
\]

This is a stochastic kernel. Transitivity ensures that every \(K^j\), and therefore \(K'\), remains supported on \(R\). Finally,
\[
\begin{aligned}
\rho K'
&=(n\mu-\nu)K(nI-K)^{-1}\\
&=(n\nu-\nu K)(nI-K)^{-1}\\
&=\nu.
\end{aligned}
\]

This proves the lemma.

For the theorem’s replica counts, \(\rho\ge0\) follows from
\[
n\mu(x)\ge1\ge\nu(x).
\]

### C. Correcting the product with one exceptional entry

If \(xRz\), then
\[
x^Lz=e_xz=z.
\]
Thus multiplication by \(x\) acts periodically on the orbit starting at \(z\), with a period \(\ell(x,z)\le m\).

Choose
\[
r\equiv-(n-1)\pmod{\ell(x,z)},
\qquad 0\le r<\ell(x,z),
\]
and set
\[
\phi_n(x,z)=x^rz.
\]
For \(r=0\), this means simply \(z\), without requiring an identity.

By construction,
\[
\boxed{x^{n-1}\phi_n(x,z)=z.}
\]

The correction also preserves the target’s idempotent label:
\[
\boxed{e_{\phi_n(x,z)}=e_z.}
\]

Indeed, \(e_xz=z\) implies \(e_xe_z=e_z\), and
\[
e_{x^rz}=e_xe_z=e_z
\]
when \(r>0\); the case \(r=0\) is immediate.

The remaining difficulty is probabilistic: choosing this exceptional value changes the individual marginal. The next step corrects that change exactly.

### D. Balancing the individual marginal

Partition \(S\) into fibres
\[
F_e=\{x:e_x=e\}.
\]

Let
\[
r_e=\rho(F_e).
\]
Aggregate an \(R\)-supported transport from \(\rho\) to \(\nu\) over its source fibres. This gives \(\Gamma(e,z)\) satisfying
\[
\sum_z\Gamma(e,z)=r_e,
\qquad
\sum_e\Gamma(e,z)=\nu(z),
\]
with \(\Gamma(e,z)=0\) unless \(ez=z\).

For \(r_{e_x}>0\), define
\[
L(x,y)
=
\sum_z
\frac{\Gamma(e_x,z)}{r_{e_x}}
\mathbf1\{\phi_n(x,z)=y\}.
\]
Zero-mass fibres may have arbitrary stochastic rows.

Consider the simplex slice
\[
D=\{q\ge0:q(F_e)=r_e\text{ for every }e\}.
\]

For every \(q\in D\), preservation of the idempotent label gives
\[
(qL)(F_e)=\nu(F_e).
\]

Define the affine map
\[
F(q)=\frac{n\mu-qL}{n-1}.
\]

This maps \(D\) into itself. Each coordinate is nonnegative because \(qL\) is a probability law and \(n\mu(y)\ge1\). Its fibre masses are
\[
\frac{n\mu(F_e)-\nu(F_e)}{n-1}=r_e.
\]

Moreover, stochastic kernels contract the \(\ell^1\) norm:
\[
\|F(q)-F(q')\|_1
\le\frac1{n-1}\|q-q'\|_1.
\]

Since \(n\ge3\), this is a contraction. Its fixed point satisfies
\[
(n-1)q+qL=n\mu,
\]
and is explicitly
\[
\boxed{
q=n\mu\big((n-1)I+L\big)^{-1}.
}
\]

The inverse exists because every eigenvalue of \(L\) has absolute value at most one.

Crucially, **nonnegativity of \(q\) follows from the invariant simplex and contraction argument**, not from an unjustified assertion that the inverse matrix is entrywise positive.

### E. Assemble the coupling

Choose \((B,Z)\) according to
\[
\Pr(B=x,Z=z)
=
q(x)\frac{\Gamma(e_x,z)}{r_{e_x}},
\]
omitting zero-mass fibres.

Set
\[
E=\phi_n(B,Z),
\]
and place \(E\) at an independent uniform position among \(n-1\) copies of \(B\).

The target variable \(Z\) has law \(\nu\). The exceptional entry has law \(qL\). Every coordinate therefore has law
\[
\frac{(n-1)q+qL}{n}=\mu.
\]

The product is exactly \(Z\), because
\[
B^{n-1}E=Z.
\]

Uniform placement makes the coupling exchangeable. The pair \((B,Z)\) has at most \(m^2\) possibilities. This completes the construction.

## 3. Proof of necessity and the finite-size bound

For a word with product \(z\), call an occurrence of \(x\) *forbidden* when
\[
e_xz\ne z.
\]

If \(x\) occurs at least \(t_x\) times, it cannot be forbidden: factor out \(x^{t_x}\) and use
\[
e_xx^{t_x}=x^{t_x}.
\]
Hence the number of forbidden occurrences is at most
\[
\sum_x(t_x-1).
\]

There is also a universal bound of \(m-1\).

Reorder the forbidden letters to the front, writing them as
\[
b_1,\ldots,b_k,
\]
and define prefixes
\[
p_i=b_1\cdots b_i.
\]

These prefixes must be distinct. Otherwise \(p_i=p_j\), with \(i<j\), gives
\[
p_i(b_{i+1}\cdots b_j)=p_i.
\]
Taking an idempotent power of the parenthesized product shows that the idempotent of each letter in that block fixes \(p_i\), and therefore fixes the final product \(z\). That contradicts forbiddenness.

Now put
\[
e=e_{b_1}\cdots e_{b_k}.
\]
The element \(p_ke\) differs from every \(p_i\). Equality with one prefix would make every \(e_{b_j}\) fix that prefix, and hence fix \(z\), again a contradiction.

Thus there are at least \(k+1\) distinct elements of \(S\), so
\[
k\le m-1.
\]

For an arbitrary coupling, define
\[
\gamma(x,z)
=
\mathbb E\left[
\frac1n\#\{i:X_i=x\}\,
\mathbf1\{X_1\cdots X_n=z\}
\right].
\]

Its source marginal is \(\mu\), its target marginal is the product law \(\nu\), and its mass outside \(R\) is at most \(c(S)/n\).

Let \(b\) be the product of all idempotents in \(S\). Then
\[
e_xb=b
\qquad\text{for every }x.
\]
Reroute every forbidden transport entry \((x,z)\) to \((x,b)\).

The source marginal remains \(\mu\). The new target law \(\eta\) belongs to \(\mathcal T(\mu)\), and at most \(c(S)/n\) probability mass has moved:
\[
\|\nu-\eta\|_{\mathrm{TV}}\le\frac{c(S)}n.
\]

If \(e_xx=x\) for every \(x\), every factor is already related to the product. No rerouting is necessary, giving exact necessity for every \(n\).

Compactness of \(\mathcal T(\mu)\), together with exact realization for sufficiently large \(n\), now proves the claimed limiting and eventual-attainability characterizations.

## 4. Consequences and sharpness

### All asymptotic output-cost optimization becomes explicit

For any function \(f:S\to\mathbb R\), define
\[
A_f
=
\sum_x\mu(x)\max_{z:e_xz=z}f(z).
\]

This is exactly the maximum of \(\mathbb E_\nu f\) over \(\mathcal T(\mu)\): choose a maximizing allowed target separately for each source \(x\).

Therefore, for \(n\ge n_0\),
\[
\boxed{
A_f
\le
\sup_{\nu\in\mathcal P_n(\mu)}\mathbb E_\nu f
\le
A_f+\frac{c(S)}n\big(\max f-\min f\big).
}
\]

When \(e_xx=x\) for every \(x\), equality holds for every \(n\ge n_0\).

This is an operational consequence, not just a characterization: every asymptotic linear output objective reduces to pointwise maximization over the sets
\[
\{z:e_xz=z\}.
\]

### Groups and joins

For a finite abelian group, every \(e_x\) is the identity. Thus \(R\) is universal and \(\mathcal T(\mu)\) is the entire probability simplex. **Every prescribed output distribution can be imposed exactly**, for sufficiently many dependent copies of any full-support input law.

For a finite join-semilattice, multiplication is \(x\vee y\), and
\[
e_x=x,\qquad xRz\iff x\le z.
\]
Thus the attainable join laws, for sufficiently large \(n\), are exactly the laws stochastically dominating \(\mu\).

These are statements about dependent copies. In particular, they are different from the independent two-option product model studied under the title *Mixability of finite groups*. [arXiv](https://arxiv.org/abs/2501.17806)

### A concrete four-replica example

Take
\[
S=\{1,a,0\},
\qquad a^2=0,
\]
with identity \(1\) and absorbing zero \(0\). Let
\[
\mu=(1/2,1/4,1/4),
\qquad
\nu=(0,1/2,1/2).
\]

Choose a row of this table, then place its exceptional entry uniformly among four positions:

| Probability | Repeated entry | Exceptional entry | Product |
|---|---|---|---|
| \(1/2\) | \(1\) | \(a\) | \(a\) |
| \(1/6\) | \(1\) | \(0\) | \(0\) |
| \(1/6\) | \(a\) | \(0\) | \(0\) |
| \(1/6\) | \(0\) | \(0\) | \(0\) |

Every coordinate has distribution \(\mu\), while the product has distribution \(\nu\).

### The resource dependence and error order are necessary

The dependence on \(1/\alpha\) cannot be removed uniformly. In \(\mathbb Z/2\mathbb Z\), take \(\mu(1)=\alpha\) and require the product—equivalently, the sum modulo two—to equal \(1\). Every realization contains at least one \(1\), so
\[
1
\le
\mathbb E\sum_i\mathbf1\{X_i=1\}
=n\alpha.
\]

The \(1/n\) error order is also necessary.

Use the three-element semigroup above and the same \(\mu\). For \(n\ge3\), set
\[
b_n=\frac{n}{2(n-1)}.
\]
With probability \(b_n\), use one \(a\) and \(n-1\) copies of \(1\), placing \(a\) uniformly. Otherwise use entries in \(\{a,0\}\), independently equal to \(a\) with probability
\[
r_n=\frac{n-3}{2(n-2)}.
\]

Every marginal is \(\mu\). The first event has product \(a\); the second always has product \(0\). Hence
\[
\nu_n(a)=b_n.
\]

Only source \(1\) is \(R\)-related to target \(a\), so every \(\eta\in\mathcal T(\mu)\) has \(\eta(a)\le1/2\). Since \((0,1/2,1/2)\in\mathcal T(\mu)\),
\[
\boxed{
\operatorname{dist}_{\mathrm{TV}}
\bigl(\nu_n,\mathcal T(\mu)\bigr)
=
\frac1{2(n-1)}.
}
\]

A universal \(o(1/n)\) replacement is therefore impossible.

## 5. Computation—and the failed computational-breakthrough claim

For exact rational input, the single-exception constructor needs only an explicit multiplication table, rational transport, action periods, and an \(m\times m\) rational linear system.

The preprocessing and compressed description have size polynomial in
\[
m,\quad \text{input bit length},\quad \log n.
\]

There is no need to enumerate the \(m^n\) possible tuples. A compressed sample can be generated in expected polynomial time; physically writing all \(n\) coordinates still costs at least \(n\) symbol writes.

But the exponential-table comparison would overstate the advance.

### A separate compact formulation already solves finite-\(n\) feasibility

Build a balanced binary product tree, recursively splitting size \(s\) into
\[
\lfloor s/2\rfloor,\qquad \lceil s/2\rceil.
\]
There are only \(O(\log n)\) distinct subtree-size types.

For each type, introduce variables for the expected counts of parent values and child-value pairs. Impose:

- consistency between parent values and child products;
- consistency between the expected parent and child counts;
- root distribution \(\nu\) and expected leaf counts \(n\mu\).

This gives a rational linear program with \(O(m^2\log n)\) variables. Conversely, a feasible flow generates a random product tree; randomly permuting its leaves makes every leaf marginal equal to \(\mu\), while commutativity preserves the product.

The complete equations and both directions of this argument are in Section 10 of the research note. Unlike the single-exception classification, this formulation also allows zero entries in \(\mu\).

Thus **polynomial-time feasibility alone is not the new contribution here**. Structured multi-marginal transport already has an extensive algorithmic theory, including exact sparse solutions in suitable graphical settings. [arXiv](https://arxiv.org/abs/2008.03006)

The candidate contribution is narrower: the explicit limiting transport condition, exact eventual realization, and single-exception normal form.

The implementation passed 361 exact-rational construction checks. A separate enumeration checked the forbidden-occurrence bound on 69,558 words across all labelled commutative semigroups of sizes one through three. A compressed \(10^{100}\)-replica example also passed its symbolic checks; its coordinates were not materialized. These are finite diagnostics, not substitutes for the general proof.

## 6. What failed, what is already known, and what remains unresolved

**Full support cannot simply be dropped.** In \(\mathbb Z/2\mathbb Z\), if \(\mu=\delta_0\), every product is \(0\), although \(R\) is universal. The transport criterion alone would permit other targets.

**Commutativity cannot simply be dropped.** In a right-zero semigroup,
\[
xy=y.
\]
Every element is idempotent and \(e_xz=z\) always, so the proposed relation is universal. Nevertheless,
\[
X_1\cdots X_n=X_n,
\qquad
\mathcal P_n(\mu)=\{\mu\}.
\]
This directly refutes the naive noncommutative extension.

**The original entropy-amplification route did not resolve the union-closed obstruction.** Uniform input on a finite union-closed family already has the largest possible entropy of any output supported on that family. Increasing the entropy of a coupled union cannot exceed it. The uniform-input obstruction is also explicitly recorded in recent literature, so that observation is not an originality claim. [arXiv](https://arxiv.org/html/2609.08291v1)

**The underlying research vocabulary is established.** Semigroup-valued complete and joint mixability were already defined in Wang’s 2015 survey, which also explicitly identified the influence of semigroup algebra as a research direction. Neither the terminology nor that broad direction is new. [arXiv](https://arxiv.org/html/1411.6190v3)

Astra was consulted after the construction, at revision `128aa73eec77425898430e68285158e5f1d81408`. The inspected quantum-semigroup dossiers were not used as proof dependencies; their own records retain source-derived, unreviewed status.  

I did not identify the exact theorem above in the sources reviewed. That does **not** establish historical priority.

The remaining gap is substantive: no argument here resolves a landmark conjecture, supplies an unrestricted global-constraint solver, or establishes general-purpose computational power beyond an explicitly represented finite algebra. The construction also permits very strong dependence and assumes the desired output law is supplied.

**Established in this investigation:** the stated classification, construction, quantitative bounds, sharpness examples, and explicit computational contracts.

**Not established:** historical originality, external validation, or the historic mathematical breakthrough sought by the mission.