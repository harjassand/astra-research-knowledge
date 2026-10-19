> Public selected edition of the 19 October audit. Original review SHA-256: `b1c85c78913e236480b7d7d105ccf4b568971badc70aee5ba7c91ee438ea63d6`. Original scientific inputs are retained unchanged. Navigation and historical-receipt pointers are adapted to the selected public subset; mathematical statements, caveats and attribution are retained. Past private-audit statements describe that audit, before approved publication. Current reproduction and retained-file hashes are in the release README and FILES.json.

# General observed-state entropy theorem: mathematical check

**Verdict: the displayed bound is supported under its stated fixed-state assumptions. No mathematical counterexample or fatal proof gap was found.** This is a mathematical check with independently written computations, not a blind derivation, external peer review, originality certificate, or physical validation.

The supported statement is the following. Fix a finite row-stochastic matrix \(P\), a full-support probability vector \(p\) for which \(P\) is reversible, and an interval \(t>0\). Assume all eigenvalues of \(P\) are strictly positive. Set

\[
D=\operatorname{diag}(p),\quad R=D^{1/2}PD^{-1/2},\quad
H=t^{-1}\log R,\quad T=-t^{-1}\log\det P,
\]
\[
d^2=\sum_{i\ne j}[-H_{ij}]_+^2,\quad m=\min_i p_i,\quad
s=p_{(1)}+p_{(2)}.
\]

If \(d>0\) and at least one real row generator \(Q\) on these same states satisfies \(e^{tQ}=P\), then every such generator satisfies

\[
\boxed{\quad
\sigma_p(Q)\geq \frac{\max\{12m,2s\}}{T}
\left(d^2+\frac{8\pi^2}{t^2}\right),\qquad
\sigma_p(Q)=\sum_{i<j}(p_iq_{ij}-p_jq_{ji})
\log\frac{p_iq_{ij}}{p_jq_{ji}}.
\quad}
\]

The conventions are zero for a pair of zero fluxes and infinity for exactly one positive flux. Natural logarithms and ordinary time reversal with even states are essential to the interpretation. The theorem includes reducible \(P\) with the specified full-support \(p\). Its hypotheses actually force \(n\geq4\) and \(T>0\). The compatible-generator set is nonempty and compact, and this extended-valued entropy attains a strictly positive minimum, possibly infinity.

## Review provenance and sources

An initial command intended to read the statement displayed `proof_notes.md` lines 1–180. Thus the stationarity, compactness, branch identity, and elementary traffic proof were visible before the check. They were recalculated and challenged, but their reconstruction is **not blind**. The completion of the circulation proof was not read until after independently deriving the directed-cycle argument and the three-color inequality below. A later long excerpt also displayed the separate hidden-state discussion; that discussion was not analyzed or used as evidence for this result. No supplied verification/audit program or verification output was run, imported, or used as computational evidence.

All source files were treated as mathematical data. The only writes in this review were in `reviews/general_entropy`. No packages were installed, no source or public files were edited, and no private statement was uploaded or sent to an external research service.

Source identifiers:

- **PN:** [entropy_bound/proof_notes.md](../../sources/pro/entropy_bound/proof_notes.md).
- **GB:** [report/general_bound.tex](../../sources/pro/report/general_bound.tex).
- **MF:** [markov_family/reconstructed_markov_proof.md](../../sources/pro/markov_family/reconstructed_markov_proof.md).

the original private structured receipt (not part of this selected public subset) records full SHA-256 hashes of these three files.

## Derivation and challenge of the proof

### 1. Stationarity survives reducibility

Uniformization with \(c\geq\max_i(-q_{ii})\), \(c>0\), expresses

\[
e^{tQ}=e^{-ct}\sum_{r\geq0}\frac{(ct)^r}{r!}(I+Q/c)^r.
\]

All terms are nonnegative. A positive rate gives a positive sampled entry through the one-jump term; more generally sampled reachability is precisely rate-graph reachability. Reversibility with \(p>0\) makes the support of \(P\) undirected, so its communicating components are closed irreducible blocks, with no transient blocks. A compatible \(Q\) cannot have an edge between these blocks and must be irreducible inside each block. Its stationary vector on a block is consequently the normalized restriction of \(p\). Therefore \(pQ=0\), including one-state blocks. It is not legitimate to infer this for arbitrary stochastic \(P\) just from \(pP=p\); the generator and full-support reversible support structure are doing work here.

This validates PN:55–65 and GB:85–103.

### 2. The branch contribution does not assume normality

Write

\[
A=D^{1/2}QD^{-1/2},\quad S=(A+A^T)/2,\quad K=(A-A^T)/2,
\quad U=S-H,\quad B=A-H=U+K.
\]

Since \(A\) is Metzler, \(S_{ij}\geq0\) off the diagonal. Hence \(\|U\|_F^2\geq d^2\); the definition of \(d\) counts both entries of each symmetric negative pair.

Every matrix commutes with its exponential, so \([A,R]=0\). Because \(R\) is symmetric positive definite, \(H\) is scalar on each real eigenspace of \(R\) and can also be interpolated as a real polynomial in \(R\). Thus \([A,H]=0\) and \(e^{tB}=I\). Eigenvalues of \(B\), counted with algebraic multiplicity, are \(2\pi i k_\ell/t\), \(k_\ell\in\mathbb Z\). They occur in conjugate pairs inside the same real observed eigenspace.

A Jordan block with nonzero nilpotent part cannot exponentiate to the identity: \(e^{tN}-I=N h(N)\), where \(h(0)=t\ne0\), so \(h(N)\) is invertible. Consequently \(B\) is diagonalizable over \(\mathbb C\), although generally not normal or orthogonally diagonalizable. This argument excludes the alleged all-zero-eigenvalue but nonzero-nilpotent loophole.

The valid identity is a trace identity:

\[
\operatorname{tr}B^2=-\frac{4\pi^2}{t^2}\sum_\ell k_\ell^2
=\|U\|_F^2-\|K\|_F^2.
\]

Here \(\operatorname{tr}(UK)=0\). No identification of Frobenius norm with a sum of squared eigenvalue moduli is made for a nonnormal matrix. If every \(k_\ell\) were zero, diagonalizability would give \(B=0\), contradicting the negative off-diagonal entry of \(H\). At least one conjugate pair is nonzero, so

\[
\|K\|_F^2=\|U\|_F^2+\frac{4\pi^2}{t^2}\sum_\ell k_\ell^2
\geq d^2+\frac{8\pi^2}{t^2}.
\]

Repeated eigenvalues create continuous logarithm families but do not evade this identity. A simple positive spectrum instead forces the unique real logarithm to be principal. Nonzero branches on eigenvalue one are excluded by the closed-block stationarity argument: the eigenvalue-one space is spanned by the stationary vectors of those blocks, and \(A\) vanishes there.

This validates PN:83–126 and GB:133–201.

### 3. Entropy normalization and the elementary constant

For one unordered edge let \(a=p_iq_{ij}\), \(b=p_jq_{ji}\), \(c=a+b\), \(j=a-b\). The scalar inequality is

\[
j\log(a/b)\geq 2j^2/c,
\qquad K_{ij}=\frac{j}{2\sqrt{p_ip_j}},\qquad
N:=\sum_{i<j}\frac{j_{ij}^2}{p_ip_j}=2\|K\|_F^2.
\]

Thus for \(\kappa=\max_{i<j}c_{ij}/(2p_ip_j)\),
\(\sigma\geq N/\kappa=2\|K\|_F^2/\kappa\).
The sum over unordered edges agrees with the conventional one-half of the ordered current/log-ratio sum; there is no missing factor of two.

Let \(x_i=-q_{ii}\). Stationarity gives total incoming and outgoing flux both equal to \(p_i x_i\), so \(c_{ij}\leq2p_i x_i\) and \(c_{ij}\leq2p_j x_j\). Since \(\sum_i x_i=T\),

\[
\kappa\leq\max_{i<j}\frac{T}{p_i+p_j}\leq T/s,
\qquad \sigma\geq\frac{2s}{T}\|K\|_F^2.
\]

The optional no-jump bound in PN:158–161 also has the stated sign: \(P_{ii}\geq e^{-tx_i}\) implies \(x_i\geq-t^{-1}\log P_{ii}\). This refinement is unnecessary for the claimed theorem.

This validates PN:130–163 and GB:205–228.

### 4. Independent reconstruction of the circulation constant 12

Orient each nonzero net current in its positive direction. Stationarity makes this a nonnegative divergence-free flow. Iteratively remove a directed simple cycle with amplitude equal to its smallest edge current. This terminates after finitely many edge removals and produces a sign-compatible decomposition
\(j=\sum_C\alpha_C\mathbf1_C\), \(\alpha_C>0\). Each cycle has at least three edges: the current graph has no self-loop and cannot contain both orientations of the same undirected pair.

Put

\[
h_{ij}=\frac{p_i+p_j}{2p_ip_j},\qquad
L=\sum_{i<j}|j_{ij}|\sqrt{h_{ij}}.
\]

The total exit rate is the **unweighted trace budget**, not the stationary average activity. Indeed,

\[
T=\sum_{i<j}\left(\frac a{p_i}+\frac b{p_j}\right)
=\sum_{i<j}h_{ij}c_{ij}
+\frac12\sum_{i<j}j_{ij}(p_i^{-1}-p_j^{-1})
=\sum_{i<j}h_{ij}c_{ij}.
\]

The last sum is a current paired with a gradient and vanishes by divergence zero. Cauchy–Schwarz therefore gives

\[
\sigma\geq2\sum j_{ij}^2/c_{ij}\geq2L^2/T.
\]

Here is a separate proof of the necessary cycle geometry, reconstructed before reading PN:182–231. For one simple cycle define
\(\ell_C=\sum_{ij\in C}\sqrt{h_{ij}}\),
\(n_C=\sum_{ij\in C}1/(p_ip_j)\), and \(x_i=\sqrt{m/p_i}\in(0,1]\). Then

\[
\ell_C=\frac1{\sqrt m}\sum_{ij\in C}\sqrt{\frac{x_i^2+x_j^2}{2}}
\geq\frac1{\sqrt m}\sum_{i\in C}x_i,
\qquad
n_C=\frac1{m^2}\sum_{ij\in C}x_i^2x_j^2
\leq\frac1{m^2}\sum_{ij\in C}x_ix_j.
\]

A simple cycle has a proper coloring with at most three colors. If \(z_1,z_2,z_3\) are the sums of the \(x_i\) in its color classes, then

\[
\sum_{ij\in C}x_ix_j
\leq z_1z_2+z_1z_3+z_2z_3
\leq(z_1+z_2+z_3)^2/3.
\]

It follows that \(\ell_C^2\geq3m n_C\). The weighted Euclidean triangle inequality now gives

\[
\sqrt N=\left\|\sum_C\alpha_C\frac{\mathbf1_C}{\sqrt{p_ip_j}}\right\|_2
\leq\sum_C\alpha_C\sqrt{n_C}
\leq\frac{\sum_C\alpha_C\ell_C}{\sqrt{3m}}
=\frac L{\sqrt{3m}}.
\]

Consequently

\[
\boxed{\sigma\geq2L^2/T\geq6mN/T
=12m\|K\|_F^2/T.}
\]

This independently verifies the coefficient and handles unequal stationary probabilities, not just uniform triangles. Afterward, PN:203–220 was checked separately: its alternative \(a_i=m/p_i\), \(\sqrt{x}\geq x\), and cycle clique bound are valid. The clique-bound mass-transfer argument terminates because each transfer removes a positive-support nonadjacent vertex; the three-color argument above also proves its asserted quadratic inequality directly.

Taking the larger of this inequality and the elementary \(2s/T\) inequality, and then applying the branch floor, proves the displayed theorem.

This validates PN:167–231. The generic uniform entropy-to-skew coefficient 12 is optimal as a limiting conversion coefficient for \(n\geq3\): for a uniform stationary three-state cycle with rates \(r+\varepsilon,r-\varepsilon\), \(\sigma T/(12m\|K\|_F^2)=(r/\varepsilon)\operatorname{atanh}(\varepsilon/r)\to1\). Extra states may be isolated with full-support uniform \(p\), or weakly reversibly coupled if irreducibility is required.

### 5. Compactness and lower semicontinuity

\(\det e^{tQ}=e^{t\operatorname{tr}Q}\) and the reality of \(\operatorname{tr}Q\) give \(\operatorname{tr}Q=t^{-1}\log\det P=-T\), with no branch ambiguity. Nonnegative off-diagonal rates and zero row sums imply every exit and every individual rate is at most \(T\). The matrix-exponential constraint is closed, so the feasible set is closed and bounded in a fixed finite-dimensional space.

At \((a,b)=(0,0)\), lower semicontinuity of the edge entropy follows from nonnegativity, not from a claim of continuity. At \((a,0)\) with \(a>0\), the limit diverges to infinity. In the interior it is continuous. A finite sum is therefore lower semicontinuous, and it attains its extended-valued minimum on the nonempty compact feasible set. If all values are infinity, this still means the extended minimum is attained. This validates PN:67–79 and GB:105–129.

## Edge cases and required scope

- **No zero denominator:** \(T=0\) forces every generator rate to vanish, hence \(P=I\) and \(d=0\). Equivalently, a positive-spectrum stochastic \(P\) has eigenvalues in \((0,1]\); determinant one forces the symmetric representative to be \(I\).
- **No binary counterexample:** a two-state irreducible positive-spectrum observation has distinct eigenvalues \(1,\lambda\), so a compatible real logarithm is principal. Reducible two-state observations are \(I\). Neither permits \(d>0\) with a compatible generator.
- **In fact four states are necessary:** on a three-state irreducible component, distinct positive eigenvalues again force the principal logarithm. With repeated nontrivial eigenvalue \(\lambda\), \(H=t^{-1}\log\lambda(I-vv^T)\), \(v=\sqrt p\), whose off-diagonal entries are nonnegative. Reducible cases reduce to blocks of size at most three. Thus the hypotheses imply \(n\geq4\), making the two-smallest-probabilities definition legitimate. GB explicitly assumes \(n\geq3\); PN could add an explicit dimension convention, although no valid case is lost.
- **Do not drop \(d>0\):** an equilibrium generator with \(d=0\) has \(\sigma=0\); adding the universal positive branch term to its entropy would be false. The branch floor applies to each nonprincipal embedding, while \(d>0\) forces every compatible embedding to be nonprincipal.
- **Fixed reducible mixture:** the theorem specifies \(p\). When \(P\) is reducible, the masses assigned to its closed classes are not uniquely determined by \(P\). PN:44's phrase “from \(P\) and \(t\) alone” should be read as “from \(P,t\), and the specified stationary class mixture \(p\)” in that case. This is a wording clarification, not a failure of the displayed inequality.
- **Units:** \(H,K,d,T\) have units of inverse time (with \(d^2\) inverse time squared). The right side and \(\sigma\) are nats per time. Rescaling \(t\) and all compatible rates gives the correct reciprocal-time scaling. \(T\) must not be replaced by \(\sum_i p_i(-q_{ii})\).
- **Finite-state and homogeneous:** enlarging the state space, varying the generator in time, approximate/noisy equality \(e^{tQ}\approx P\), or a time reversal involving odd variables requires a different theorem.

## Independent computation and evidence limits

The new [check_general_entropy.py](check_general_entropy.py) was executed successfully under Python 3.14.3 and NumPy 2.5.3. It does not import or execute any supplied verifier. Results are in [checks.json](checks.json).

- Exact integer/rational enumeration checked **97,625** positive rational vertex-weight assignments on simple cycles of lengths 3–7 for \((\sum_i a_i)^2\geq3\sum_{ij\in C}a_i a_j\). No violation occurred; the minimum ratio was exactly 3 on equal-weight triangles.
- From 600 randomly generated rational stationary-flow cases on 3–8 states, **596** had nonzero net current. Exact arithmetic checked divergence zero, \(T=\sum hc\), and \(\kappa\leq T/s\). Floating evaluations checked the cycle and entropy inequalities. The smallest observed ratios to their respective lower bounds were 1.03048 for cycle geometry, 1.09339 for the circulation entropy bound, and 3.10693 for the elementary entropy bound. These minima describe only this finite sample.
- **29 compatible nonnormal matrix cases** used the supplied four-state witness formula, implemented afresh, with windings 1–3, different imbalance parameters, time intervals 0.25, 1, and 2.5, and reducible five/six-state extensions with full-support \(p\). A newly written Taylor scaling-and-squaring exponential gave maximum absolute exponential error \(7.05\times10^{-15}\); the largest absolute branch-trace residual was \(3.64\times10^{-12}\). All claimed inequalities passed. The analytic repeated-eigenvalue construction was used to avoid trusting numerical logarithms of nearly degenerate matrices.
- The uniform-triangle near-equilibrium conversion ratio was 1.0000000000003335 at \(\varepsilon/r=10^{-6}\), consistent with the independently derived sharp limiting coefficient.

These are finite checks and floating-point consistency tests. They are not certified interval enclosures, proof of an unbounded search, proof of novelty, or experimental evidence. The proof above supplies the general result.

## What is sharpened, and what is not established

The logarithm/Jordan machinery, determinant trace identity, scalar entropy inequality, and stationary cycle decomposition are standard mathematical ingredients. PN:235–264 attributes relevant embedding and entropy-to-skew ingredients to existing literature; those bibliographic/priority claims were not independently checked against external primary sources in this review.

The supported sharpened consequence is the explicit observation-based combination: a negative principal-log off-diagonal defect forces a nonzero conjugate branch pair; the exact trace identity controls its skew norm even for nonnormal logarithms; the trace-budget and current-cycle inequalities turn that skew floor into the stated entropy certificate. The circulation coefficient improves the elementary uniform coefficient by exactly three. This mathematical consequence is verified here; bibliographic first discovery remains **unestablished**.

The coefficient 12 being optimal for a generic entropy-to-skew conversion does **not** make the final observation bound an exact entropy optimum. In fact, whenever the entropy is finite under \(d>0\), some current is nonzero, and the scalar inequality \(j\log(a/b)\geq2j^2/c\) is strict on that edge. Thus each finite compatible generator, and also the attained finite minimum, lies strictly above the final displayed lower bound.

MF:190–243 makes a separate exact four-state optimization claim, with a scalar minimizer and an interval near 26.178911678346–26.178911678347 for its rational example. That exact optimization and its interval certification were **not independently audited here**. For the same example this general theorem gives approximately **7.790264194785**; direct evaluation of the supplied all-positive witness gives **26.417969060876**. These are three distinct quantities: a universal lower certificate, the separately claimed exact family optimum, and one witness's entropy.

Nothing in this observed-state theorem is a positive numerical entropy floor over arbitrary larger hidden-state models. The separate two-lag hidden-equilibrium incompatibility question was outside this review. Thermodynamic meaning also needs a specified physical time-reversal and local-detailed-balance model; the proved quantity here is the stated statistical Markov entropy-production rate.
