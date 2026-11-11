# P3 completed return — 889e4d3e

Chat: https://chatgpt.com/c/6af3030c-e834-83ec-b294-ad6a7f60aa46; model shown: Pro. Prompt: P3_FULL_DETAILED_BALANCED_ALL_TIME_AFTER_ENTROPY_PRO_20261111.txt (source SHA-256 94361c70e719ffe22288c43a4f831833866e8fcb662432cd6fb13a70f366ffbf), user turn 563e6fe3-4a18-4122-bb61-15dd3b784849. Assistant final 889e4d3e-9968-5405-b22d-d5a89e7d595f. Captured using this answer's UI Copy and clipboard. Native first 20,000 characters match after normalizing whitespace and the UI-expanded citation representation; native final is truncated at that limit. Visible UI ending matches. Current activity and helper panels are not captured: the accessible tree exposes older history and an older helper panel. ZIP availability is unknown; no archive or individual files were collected.

## Complete UI-copied final

**I have not resolved the full statement for arbitrary \(d\).** I do have a construction that closes **the entire contract for one original species, with variable reaction order**, including nominal detailed balance, arbitrary predictable faults, complete timed marked-path accuracy, and all-time population and firing costs. It uses a reversible augmentation of the paired-prefix lift.

For that scalar theorem, explicit universal constants are
\[
\boxed{C=2^{4096},\qquad p=512.}
\]
These constants apply to the scalar construction below, **not to the unresolved arbitrary-dimensional question**.

There are also two useful findings for the general problem:

- The supplied \(X\rightleftarrows2X\) linear-weight argument cannot extend unchanged to the ordinary paired-prefix lift: \(2X\rightleftarrows3X\) already provides a counterexample to that proof strategy.
- If an admitted network has any strictly positive conservation vector, detailed balance and the upper-drift promise force every reaction to conserve the supplied \(\omega\), even when \(A>0\).

I give the scalar construction and its resource proof first, then explain precisely what remains missing in several dimensions. The finite-horizon averaging theorem used below is your accepted premise; the new part is the reversible augmentation and its fault-uniform all-time estimate.

## 1. A full scalar theorem

Let the sole original species be \(X\), and write the original labels as
\[
r:q_rX\longrightarrow p_rX.
\]

If every \(q_r=p_r\), decoded population is conserved, and the accepted paired-prefix construction already satisfies the all-time contract. Suppose otherwise. Reversibility supplies a decreasing label; choose one deterministically from the stoichiometric input:
\[
r_*:qX\longrightarrow pX,\qquad q>p,
\qquad d_*=q-p.
\]
This choice depends only on \(R\), as required.

The construction adds rare reversible reactions that produce a negative quadratic drift term at **every binary fine complex**. Their rates are small enough to preserve the required finite-horizon path law, but strictly positive. The all-time proof uses their actual finite rates at every population size.

### 1.1 Base species and additional cluster species

Start with the uniform paired-prefix lift in the question. Add species
\[
X_j,\qquad 2\le j\le D,
\]
with
\[
PX_j=j,\qquad X_1=X,
\]
and the hidden reversible chain
\[
2X\rightleftarrows X_2,\qquad
X_{j-1}+X\rightleftarrows X_j,\quad 3\le j\le D.
\]

Use activities
\[
\widetilde a_{X_j}=\theta U^{-j}a^j.
\]
The first binding/release coefficients are \(K\theta/U^2,K\); later binding/release coefficients are \(K/U,K\).

Define
\[
J=\sum_r q_r,\qquad
M=J+D-1,\qquad
s=M+1.
\]
Thus \(M\) is the auxiliary-species count and \(s\) the total species count. Every species \(S\) has a scalar payload
\[
p_S=PS\in\{1,\ldots,D\}.
\]

For analysis, use the positive linear function
\[
V(z)=\sum_S w_Sz_S,
\qquad w_S=1+p_S.
\]
Writing \(n=|z|_1\),
\[
2n\le V(z)\le(D+1)n. \tag{1}
\]

Every base or helper binding has two reactants, one product, and unchanged decoded payload. Consequently, every such binding decreases \(V\) by exactly one.

### 1.2 A finite forest on binary fine complexes

Let \(\mathcal B\) be the set of all unordered binary complexes of fine species, including \(2S\), and put
\[
b=|\mathcal B|=\frac{s(s+1)}2.
\]

For each \(\alpha\in\mathcal B\), its decoded payload is an integer
\[
t=P\alpha\in\{2,\ldots,2D\}.
\]
Give \(\alpha\) one parent \(\beta(\alpha)\).

**When \(t\le D\):**
\[
\beta(\alpha)=X_t,
\]
and make the pair hidden.

**When \(t>D\):** put \(t'=t-d_*\), and define
\[
\beta(\alpha)=
\begin{cases}
X_{t'},&t'\le D,\\[2mm]
X_D+X_{t'-D},&t'>D.
\end{cases}
\]
Label \(\alpha\to\beta(\alpha)\) by \(r_*\), and its reverse by \(\bar r_*\).

These are valid elementary channels. In the observed case,
\[
t>D\ge q,
\]
so the original decreasing edge is enabled. At the reverse source,
\[
t'=t-q+p\ge p,
\]
so the reverse original edge is enabled too.

Set
\[
\Delta_\alpha=w\cdot\alpha-w\cdot\beta(\alpha).
\]
For hidden mergers, \(\Delta_\alpha=1\). For observed pairs,
\[
\Delta_\alpha=d_*+2-|\beta(\alpha)|_1.
\]
Therefore
\[
1\le\Delta_\alpha\le D+1. \tag{2}
\]

Whenever the parent is binary, its payload is strictly smaller. Thus the binary vertices form a finite forest ending at unary complexes. The forest introduces \(2b\) labelled channels and no further species.

### 1.3 Balanced coefficients with an exact quadratic drift identity

For each fine complex \(\alpha\), write
\[
A_\alpha=\widetilde a^\alpha.
\]
For a binary vertex, define recursively
\[
f_\alpha
=A_\alpha+
\sum_{\gamma:\,\beta(\gamma)=\alpha}f_\gamma. \tag{3}
\]
Equivalently, \(f_\alpha\) is the sum of \(A_\gamma\) over all binary descendants of \(\alpha\), including itself.

Give its reversible pair the unscaled coefficients
\[
\kappa_{\alpha\beta}
=\frac{f_\alpha}{A_\alpha\Delta_\alpha},
\qquad
\kappa_{\beta\alpha}
=\frac{f_\alpha}{A_\beta\Delta_\alpha}. \tag{4}
\]
Multiply both coefficients by a small rational \(\eta>0\), specified below.

Detailed balance holds exactly:
\[
\eta\kappa_{\alpha\beta}\widetilde a^\alpha
=
\eta\kappa_{\beta\alpha}\widetilde a^\beta. \tag{5}
\]

More importantly, the coefficient of the factorial monomial \((z)_\alpha\) in the forest contribution to the nominal generator applied to \(V\) is
\[
-\eta\frac{f_\alpha}{A_\alpha}
+\eta
\sum_{\gamma:\,\beta(\gamma)=\alpha}
\frac{f_\gamma}{A_\alpha}
=-\eta. \tag{6}
\]
This cancellation is the reason for using descendant sums in (3).

Let
\[
G=\max\left\{
1,\max_S\widetilde a_S,\max_S\widetilde a_S^{-1}
\right\}.
\]
Binary-complex activities lie in \([G^{-2},G^2]\), and
\[
f_\alpha\le bG^2.
\]
It follows that
\[
\max_e\kappa_e\le bG^4,
\qquad
\max_e\kappa_e^{-1}\le(D+1)G^4. \tag{7}
\]

At any binary vertex, the sum of the absolute weighted incident coefficients is at most
\[
2bG^4.
\]
Thus independent instantaneous rate errors preserve a coefficient at most \(-\eta/2\) whenever
\[
\delta\le\frac1{8bG^4}. \tag{8}
\]

This is a pointwise inequality for every fine state and every vector of multipliers in the allowed box. It consequently applies to history-dependent predictable faults.

## 2. Explicit parameters and the balance certificate

Write \(\Gamma=\Gamma_B\), and choose
\[
C_f=4(D+1)^2,
\]
\[
Q=
1+4096(m+2)UC_f
+128\epsilon^{-1}(M+1)\Gamma(1+\tau),
\qquad \theta=Q^{-1},
\]
\[
\Lambda=m+Q\Gamma U,
\]
\[
K=
1+Q\Gamma+
512\epsilon^{-1}BC_f\Lambda(1+\Lambda\tau),
\]
\[
H=1+K+Q\Gamma. \tag{9}
\]

The base and helper activities are now determined. Calculate \(G\) and set
\[
R_f=1+bG^4,
\qquad
\eta=\frac{\epsilon}
{512\,bR_fU^2(1+\tau)}. \tag{10}
\]
The full channel count is
\[
m_f=2M+m+2b.
\]
Choose
\[
\boxed{
\delta=
\min\left\{
\frac{\epsilon}{128m_fU^2(1+H\tau)},
\frac1{8bG^4}
\right\}.} \tag{11}
\]
In the nontrivial case this is positive and strictly less than \(1/2\).

Divide every raw coefficient by \(H\). The base coefficients are bounded by \(H\), and
\[
\eta\max_e\kappa_e<1,
\]
so all emitted coefficients belong to \((0,1]\).

The certificate covers every channel:

- Hidden source-prefix and helper bindings satisfy balance by their displayed activity ratios.
- Full-prefix/pending exchanges have equal activities and equal rates.
- A nonempty-source observed channel has equilibrium flux
  \[
  Qk_rU^{q_r}\,
  \bigl(Q^{-1}U^{-q_r}a^{q_r}\bigr)
  =k_ra^{q_r}.
  \]
  Its reverse flux is equal by the supplied original balance identity.
- Zero-source and null channels obey the same identity.
- Every new forest pair satisfies (5).

Common normalization by \(H\) preserves all these equalities.

### Graph, labels and initialization

Every new decoder column is a positive integer. All auxiliaries, including the helpers, start at zero.

Every auxiliary can be released through hidden reactions to its canonical original population. Every forest channel either preserves the decoder or executes an enabled \(r_*\) or \(\bar r_*\). Hence every fine path projects to an original path.

Conversely, for arbitrary fine states \(u,v\), release \(u\) to \(j(Pu)\), lift an original path from \(Pu\) to \(Pv\), and reverse the release path from \(v\) to \(j(Pv)\). Therefore
\[
u\leadsto v
\quad\Longleftrightarrow\quad
Pu\leadsto Pv. \tag{12}
\]
This proves the required all-state directed statement.

The new pairs have their actual reverse channels. Existing original null and parallel labels remain distinct in the base lift. Parallel hidden pairs created by the augmentation are also retained and counted separately.

## 3. The all-time fault-uniform estimate

This is the part absent from the unaugmented finite-horizon argument.

Let \(\mathscr L^{\rm raw}_{\xi}\) denote the instantaneous raw generator with any multipliers \(\xi_e\in[1-\delta,1+\delta]\).

The base bindings contribute nonpositive drift. Base releases contribute at most \((3/2)Kn\). Positive observed drift contributes at most a constant plus \((3/2)DQ\Gamma n\).

At a unary forest root, the total reverse weighted flux is at most \(\eta bG^3\) times its population. Thus one may take
\[
C_0=\frac32m(D+1),
\]
\[
C_1=\frac32\left(K+DQ\Gamma+\eta bG^3\right).
\]
Using (6)–(8),
\[
\mathscr L^{\rm raw}_{\xi}V
\le
C_0+C_1n
-\frac{\eta}{2}\sum_{\alpha\in\mathcal B}(z)_\alpha. \tag{13}
\]

For unordered binary complexes,
\[
\begin{aligned}
\sum_{\alpha\in\mathcal B}(z)_\alpha
&=\sum_Sz_S(z_S-1)+\sum_{S<T}z_Sz_T\\
&\ge\frac{n(n-1)}2.
\end{aligned}
\]
Consequently,
\[
\boxed{
\mathscr L^{\rm raw}_{\xi}V
\le C_0+C_1n-\frac\eta4n(n-1).
} \tag{14}
\]

Set
\[
B_*=
C_0+\frac{(C_1+3\eta/8)^2}{\eta},
\qquad
\gamma=\frac{\eta}{8(D+1)}.
\]
Because \(V\le(D+1)n\), completing the square gives
\[
\boxed{
\mathscr L^{\rm raw}_{\xi}V
\le B_*-\gamma V.
} \tag{15}
\]

The physical generator is the raw generator divided by \(H\). Localized Dynkin estimates therefore yield
\[
\sup_{t\ge0}\mathbb EV(Z_t)
\le V(j(x_0))+\frac{B_*}{\gamma}
=:M_* . \tag{16}
\]
No Markov assumption on the faulty marginal is used: (15) holds for every instantaneous multiplier vector.

### 3.1 Nonexplosion

An elementary reaction can increase physical molecule count only if its source has zero or one molecule. Since physical coefficients are at most one and multipliers are below \(3/2\), the total population-increasing intensity is at most
\[
\frac32m_f(1+n).
\]
Positive jumps have size at most two.

An affine-rate pure-birth comparison proves that population stays finite on finite time intervals. On a bounded population set, the total marked intensity is bounded, including null and parallel firings. Thus the complete marked process is nonexplosive. This preliminary comparison also justifies localization before applying (15).

### 3.2 Expected population supremum

Count positive population jumps. From (16),
\[
\mathbb E\sup_{s\le t}(1+n_s)
\le
1+n_0+3m_f\int_0^t(1+\mathbb En_s)\,ds
\le \operatorname{poly}(W)(1+t). \tag{17}
\]

This pays the actual supremum, including rare trajectories.

### 3.3 Every firing, including the added binary cycles

The new \(2\to2\) channels need a quadratic activity estimate; the old count identity alone would not pay them.

Integrating (14) gives
\[
\begin{aligned}
\mathbb E\int_0^t n_s^2\,ds
\le{}&
\frac{4H}{\eta}V(j(x_0))
+\frac{4C_0}{\eta}t\\
&+\frac{4(C_1+\eta/4)}{\eta}
\int_0^t\mathbb En_s\,ds.
\end{aligned} \tag{18}
\]
By (16), the right side is polynomial in \(W\), times \(1+t\).

The complete physical marked intensity satisfies
\[
a_{\rm all}(z)
\le\frac32m_f(1+n)^2.
\]
Therefore
\[
\boxed{
\mathbb EF_{\rm all}(t)
\le\operatorname{poly}(W)(1+t).
} \tag{19}
\]
This is stronger than the requested quadratic growth in time. It includes all releases, failed assemblies, forest cycles, original null events and parallel marks.

## 4. Complete timed-path accuracy

For the comparison proof, use the paired-prefix lift plus the helper chain as a reference, omitting the forest only from that reference. The emitted process always contains the forest.

### Hidden mixing and averaged rates

Below the analytical cutoff, the helper chain changes the auxiliary count from \(J\) to \(M\), and
\[
1\le q_\theta(x)\le e^{\theta M}.
\]

There are at most \(m+1\) chain-initiation types. Their total tag-immigration rate is at most \(K\theta(m+1)\), and each initial tag has release mean at most \(C_f/K\).

At
\[
h=\frac{16BC_f}{K},
\]
the probability that any initial tag survives is at most \(1/16\). The probability of a new tag immigration is at most
\[
16\theta(m+1)BC_f\le\frac1{256}.
\]
The hidden kernel therefore has a common canonical atom of mass at least \(1/2\), giving
\[
I\le2h.
\]

Your accepted complete marked-path averaging estimate then gives
\[
\Lambda I(1+\Lambda\tau)\le\frac{\epsilon}{16}. \tag{20}
\]
The averaged labelled intensities remain exactly
\[
\bar\lambda_r(x)
=k_r(x)_{q_r}
\frac{q_\theta(x-q_r)}{q_\theta(x)}.
\]
The partition-ratio error costs at most \(\epsilon/64\).

### Added forest and predictable faults

Before analytical exit, the total raw forest intensity is at most
\[
2b\eta R_fU^2.
\]
Coupling until the first forest firing costs at most
\[
2b\eta R_fU^2\tau\le\frac{\epsilon}{256}. \tag{21}
\]
Both hidden and observed forest firings are treated as mismatches in this comparison.

The complete-mark fault coupling costs at most
\[
\delta m_fU^2H\tau\le\frac{\epsilon}{128}. \tag{22}
\]
It includes hidden-history mismatches, so an adaptive fault cannot exploit a hidden mark that the coupling disregarded.

The original escape probability is at most \(\epsilon/32\). The sum of the comparison budgets is
\[
\frac{\epsilon}{16}
+\frac{\epsilon}{64}
+\frac{\epsilon}{256}
+\frac{\epsilon}{128}
+\frac{\epsilon}{32}
=\frac{31\epsilon}{256}.
\]
Even allowing a factor of two when passing from stopped comparisons to unrestricted path laws leaves the error below \(\epsilon\).

These are comparisons of complete marked paths with their exact event times. The physical clock is the single constant factor \(H\); no residence time is removed.

## 5. Universal scalar resource bounds

The potentially problematic variable-order factors are paid by \(\Gamma_B\) and \(\Xi\).

Let \(k_*=\min_r k_r\). Because reverse labels are supplied, an order-\(D\) complex occurs as a source in the nontrivial case. Hence
\[
U^D\le\frac{\Gamma_B}{k_*}. \tag{23}
\]
This gives
\[
G\le Q\Gamma_Bk_*^{-1}\Xi. \tag{24}
\]
No exponent depending on \(D\) remains in the final \(W\)-bounds.

The following loose estimates suffice:

| Quantity | Bound |
|---|---:|
| \(U\) | \(2^7W^3\) |
| \(M,s\) | \(2W^2\) |
| \(b\) | \(4W^4\) |
| \(m_f\) | \(16W^4\) |
| \(Q\) | \(2^{25}W^6\) |
| \(\Lambda\) | \(2^{33}W^{10}\) |
| \(K\) | \(2^{88}W^{27}\) |
| \(H\) | \(2^{89}W^{27}\) |
| \(G\) | \(2^{25}W^9\) |
| \(\eta^{-1}\) | \(2^{129}W^{52}\) |
| \(\delta^{-1}\) | \(2^{115}W^{40}\) |
| \(\max_e c_e^{-1}\) | \(2^{321}W^{116}\) |

Also,
\[
\max_S(\widetilde a_S+\widetilde a_S^{-1})
\le2^{26}W^9,
\qquad
\max_SP_S\le D.
\]

For completeness, the drift estimates above imply
\[
B_*\le2^{324}W^{116},
\qquad
\gamma^{-1}\le2^{133}W^{53},
\]
and consequently
\[
\sup_{t\ge0}\mathbb EV(Z_t)
\le2^{458}W^{169}.
\]
One obtains
\[
\mathbb E\sup_{s\le t}(1+|Z_s|_1)
\le2^{465}W^{173}(1+t), \tag{25}
\]
\[
\mathbb EF_{\rm all}(t)
\le2^{695}W^{257}(1+t), \tag{26}
\]
and
\[
\mathbb EF_{\rm all}(H\tau)
\le2^{785}W^{285}. \tag{27}
\]

There are \(O(L)\) species and \(O(L^2)\) forest channels. Descending-payload dynamic programming computes (3). All calculations use exact rational arithmetic. A generic implementation has intermediate bit lengths \(O(L^4)\), with the safe combined work, memory and output bound
\[
2^{1000}(1+L)^{24}. \tag{28}
\]
No population set, communicating class or normalizer is enumerated.

Thus
\[
C=2^{4096},\qquad p=512
\]
covers every scalar inequality in the question, including the sum of the numerical output costs.

## 6. Why the supplied linear-weight calculation does not extend directly

Consider the admitted original pair
\[
2X\rightleftarrows3X,
\qquad k_+=k_-=a=1,\qquad\omega=1.
\]
Its original drift is
\[
LN(n)=(n)_2-(n)_3=n(n-1)(3-n)\le2. \tag{29}
\]

Nevertheless, its **ordinary private paired-prefix lift** has no positive linear \(V=w\cdot z\) whose nominal generator is bounded above globally.

Let \(S\) be the full dimer prefix in the \(2X\)-source chain, and \(T\) the proper dimer prefix in the \(3X\)-source chain.

At states consisting solely of \(T\), its unary release is \(T\to2X\). Bounded upper drift forces
\[
w_T\ge2w_X. \tag{30}
\]

The finite unary service block starting at \(S\) can exit as either \(2X\) or \(T+X\), each with positive probability. Bounded drift on pure auxiliary rays makes the auxiliary weights superharmonic for this service block. Consequently,
\[
w_S\ge
\mathbb E_S[\text{terminal weight}]
>2w_X, \tag{31}
\]
because the second exit has weight at least \(3w_X\).

At a canonical state \(nX\), the two first bindings
\[
2X\to S,\qquad2X\to T
\]
then have nonnegative weight increments, one strictly positive. Their quadratic contribution makes
\[
LV(nX)\longrightarrow+\infty.
\]

This excludes the direct extension of the supplied linear-weight proof on that topology. It does not exclude other potentials or other designs; the scalar forest above explicitly repairs it.

## 7. Structural consequences in several dimensions

Two consequences of the admission promise help identify the remaining problem.

### 7.1 A support that permits growth also permits an inward reaction

Let \(Q\) be a set of species. If an original reaction with nonempty source supported in \(Q\) increases \(\omega\cdot x\), then some original reaction whose source is supported in \(Q\) decreases it.

Otherwise evaluate \(LN\) at
\[
x=n\,1_Q.
\]
All enabled nonempty-source summands would be nonnegative, with at least one growing without bound. Zero-source terms contribute only constants. This contradicts \(LN\le A\).

In particular, if a payload \(c\) supports such a growing reaction, at most \(D\) copies of \(c\) contain the source of a decreasing reaction.

The difficulty is what happens after that reaction: its residual and product payloads need not stay in a predetermined polynomial-size family.

### 7.2 Positive conservation forces conservation of the supplied \(\omega\)

Suppose \(\chi\ge0\) is a conservation vector:
\[
\chi\cdot(z_r-y_r)=0\quad\text{for all }r.
\]
Then every reaction in a complex-graph component with positive \(\chi\)-mass conserves \(\omega\).

Here is a direct proof.

Let
\[
F(x)=LN(x),\qquad G(x)=A-F(x)\ge0.
\]
For every \(t\ge1\), the activities
\[
a_i(t)=a_it^{\chi_i}
\]
remain detailed balanced. The associated independent Poisson law has the usual product form; the autonomous product-Poisson and reversibility statements are established in Anderson–Craciun–Kurtz, Theorem 4.1 and §4.2. [arxiv.org](https://arxiv.org/pdf/0803.3042?utm_source=chatgpt.com) Direct cancellation of paired equilibrium fluxes gives
\[
\mathbb EF(X)=0,\qquad \mathbb EG(X)=A. \tag{32}
\]

Put \(S=\{i:\chi_i>0\}\). Condition on any fixed integer values of the coordinates outside \(S\). Their Poisson probability is positive and independent of \(t\), so the conditional expectation of \(G\) remains bounded.

A nonconstant polynomial, nonnegative on the integer lattice, cannot have bounded expectations under independent Poisson variables whose means all tend to infinity. To see this, standardize the Poisson variables. A highest-degree coefficient grows as a product of square roots of their means. Normalize the polynomial by its largest coefficient and take a convergent coefficient subsequence. The standardized Poissons converge to independent Gaussians, with uniformly bounded fixed moments. The normalized absolute expectation therefore converges to the positive Gaussian \(L^1\) norm of a nonzero polynomial. Nonnegativity and bounded original expectation would instead force that limit to be zero.

It follows that \(F\) is independent of the coordinates in \(S\). Write
\[
F(x)=\sum_y b_y(x)_y,
\qquad
b_y=\sum_{r:y_r=y}k_r\,\omega\cdot(z_r-y).
\]
Uniqueness of the falling-factorial expansion gives \(b_y=0\) whenever \(y\) uses a species in \(S\).

Every vertex of a positive-\(\chi\)-mass complex component has that property. Therefore \(h(y)=\omega\cdot y\) is harmonic on its finite reversible complex graph:
\[
\sum_{r:y_r=y}k_r\bigl(h(z_r)-h(y)\bigr)=0.
\]
The finite maximum principle makes \(h\) constant on that component.

In particular,
\[
\boxed{
\chi>0\text{ conserved}
\quad\Longrightarrow\quad
\omega\cdot(z_r-y_r)=0\text{ for every }r.
} \tag{33}
\]
Thus all admitted inputs possessing a strictly positive conservation vector already fall into the solved conservative subcase, regardless of whether the supplied \(A\) is zero.

## 8. The remaining arbitrary-dimensional gap

The scalar forest works because every payload between \(1\) and \(2D\) has an encoding using at most two members of
\[
\{X_1,\ldots,X_D\}.
\]
A decreasing original move keeps the payload inside this finite ordered family.

For vector payloads, executing an inward reaction from two stored molecules gives
\[
P\alpha-y_r+z_r.
\]
That vector need not have a representation using two members of the existing auxiliary family. Adding a species for it creates more binary complexes, whose corresponding moves may require further payloads. Neither the support lemma nor the conservation lemma proves a polynomial bound on this closure.

Pure-species stabilization is also insufficient as a general premise. For example,
\[
A+B\rightleftarrows2A+B,
\qquad
0\rightleftarrows B,
\]
with unit rates and activities and \(\omega=(1,1)\), satisfies
\[
LN(A,B)=1-B(A-1)^2\le1.
\]
There is no \(A\)-removing reaction enabled on the pure \(A\)-axis. A general argument must accommodate mixed-support stabilization.

A fixed-\(R\) terminating closure search would not meet the present uniform contract without a polynomial bound on its output, arithmetic and physical margins. I have not supplied such a bound, nor an alternative controlled Lyapunov argument for arbitrary vector payloads.

**The proved result here is the full scalar compiler and the structural lemmas above. The existence or impossibility of the entire arbitrary-\(d\) compiler remains unresolved in this answer.**