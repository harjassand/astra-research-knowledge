**I constructed a reusable joint-law representation and a fully acquired general Gaussian-mean channel, with explicit costs. The original polylogarithmic-dimension target remains open.** The strongest new result is a positive compiler that reuses previously computed noisy means without rerunning their predecessor trees, while tracking the exact precision consumed by that reuse. Its independent Gaussian reserve and center-shift operations are constructed from the finite program.

The work also produced two discriminating failures. They show why neither a more accurate bounded likelihood correction around the same averaged proposal, nor a cheap universal hidden-center Gaussian oracle, supplies the remaining bridge. Neither is a lower bound for the original target.

The complete proofs, ordinary code, execution data, unchanged frozen sources, and preserved first-round results are in:

- [Astra_Gaussian_Continuation_2026-10-27.zip](https://chatgpt.com/library?file_id=libfile_e6a415f789888191bc29f6d0a7db60e0&account_id=personal)
- :chatgpt-content-reference{index="5"}[CONTINUATION.txt](sandbox:/workspace/scratch/810b1ee40202/research/round2_main/CONTINUATION.txt)

## 1. A positive compiler for reusing actual noisy outputs

The relevant object is a **jointly controlled record** of noisy means. Suppose an acquired record \(R\in(\mathbb R^d)^k\) satisfies

\[
\operatorname{TV}\!\left(\mathcal L(R),
  N(m,C\otimes I_d)\right)\le \varepsilon_{\rm in},
\]

where \(m\) is unknown and \(C\) is known.

Each child is an actual finite program \(Q_i(c;\xi_i)\), with its complete source-query and arithmetic costs included. It has a known seed vector \(v_i\) and radius \(r_i\) satisfying the pathwise identity

\[
Q_i(c+r_i h;\xi_i+v_i\otimes h)=Q_i(c;\xi_i).
\tag{1}
\]

This identity must preserve every physical source-query point. It is stronger than an expectation identity, but it is available for explicit programs. For example,

\[
Q(c;\xi)
=\frac1n\sum_{j=1}^{n}g(c+r\xi_j)+s\xi_{n+1}
\]

has \(v=(-1,\ldots,-1,0)\). Its \(n\) values and its standalone Gaussian approximation error remain charged.

Suppose the intended new centers are

\[
c_i=b_i+\sum_j A_{ij}m_j.
\]

Define

\[
\Gamma_{ii}=\frac{\|v_i\|^2}{r_i^2}.
\]

Then the precision required to retain the old record while evaluating these children is

\[
\boxed{
C_{\rm new}^{-1}=C^{-1}-A^\top\Gamma A.
}
\tag{2}
\]

When this matrix is positive definite, there is an explicit positive construction that evaluates each child once and retains the old means at covariance \(C_{\rm new}\).

### The implemented transformation

Let \(H\) place \(v_i/r_i\) in child \(i\)’s seed block, so that \(H^\top H=\Gamma\). Choose known factors

\[
C=LL^\top,\qquad C_{\rm new}=TT^\top,
\]

and set

\[
B=
\begin{bmatrix}
-T^{-1}L\\
HAL
\end{bmatrix}.
\]

Equation (2) gives \(B^\top B=I\). Draw fresh standard Gaussian seed slots \(G\), and compute

\[
\xi=(I-BB^\top)G.
\]

Return

\[
R_{\rm new,old}=R+T\xi_0,
\qquad
R_{{\rm new},i}
=
Q_i\!\left(b_i+\sum_j A_{ij}R_j;\xi_i\right).
\tag{3}
\]

Every argument in (3) is available. The implementation does not evaluate \(m\), the intended centers, or the Gaussian error in the old record.

### Why this proves the whole joint law

For analysis only, write an ideal input as \(R=m+LZ\). Applying the child identities (1), the complete effective seed array becomes

\[
\eta=(I-BB^\top)G-BZ.
\]

It is jointly Gaussian and has covariance

\[
(I-BB^\top)^2+BB^\top=I.
\]

Thus its slots are independent standard Gaussians. The retained old record and every standalone child output consequently have the required product law. This remains an exact identity even when a standalone child output is nonlinear and non-Gaussian.

If child \(i\)’s standalone law has uniform error \(\varepsilon_i\) from its Gaussian target, data processing and the independent product comparison give

\[
\boxed{
\varepsilon_{\rm new}
\le \varepsilon_{\rm in}+\sum_i\varepsilon_i.
}
\tag{4}
\]

The old record’s error is charged once, regardless of how many children read it in this layer.

### A complete DAG has one precision test

For a fixed affine computation graph, let \(A\) be its strictly lower triangular matrix of dependencies and let

\[
D=\operatorname{diag}(S_i^2)
\]

contain the standalone child noise variances. Sequential application gives

\[
\boxed{
C_{\rm final}^{-1}=D^{-1}-A^\top\Gamma A.
}
\tag{5}
\]

Positive definiteness of this final matrix implies feasibility at every prefix. Each logical child executes once. Its ancestors are not independently regenerated merely to supply another center.

For final weights \(w\), the resulting noise variance is exactly

\[
w^\top C_{\rm final}w.
\]

Additional Gaussian noise can bring this to \(\sigma^2\) only when it is already at most \(\sigma^2\). That output-noise condition is part of the theorem.

This is a genuine alternative to independent tree expansion, but it is conditional on a feasible precision assignment. In the simplest repeated-read example,

\[
\tau_{\rm retained}^2
=
\frac{\tau^2}
 {1-Ma^2\tau^2\|v\|^2/r^2}.
\]

Reuse eventually exhausts precision. The theorem makes that cost explicit instead of treating reuse as free.

Output-only nodes are useful here: their columns in \(A\) vanish, so their large output noises consume no read precision. Internal centers and final outputs need not receive the same noise allocation.

Full proof: BLOCK_GAUSSIAN_ABSORPTION.md[BLOCK_GAUSSIAN_ABSORPTION.md](sandbox:/workspace/scratch/810b1ee40202/research/round2_reuse/BLOCK_GAUSSIAN_ABSORPTION.md).

## 2. The Gaussian reserve and recursive metadata are constructed

A joint Gaussian comparison alone does not provide a usable Gaussian reserve inside the actual program. I therefore constructed a stronger interface.

Suppose a known matrix \(W\) satisfies

\[
Q(z+Wu)=Q(z)+u
\]

while leaving all physical source queries unchanged. Gaussian orthogonal decomposition gives the exact identity

\[
Q(z)
=
Q\!\left(z-W(W^\top W)^{-1}W^\top z\right)
+
(W^\top W)^{-1}W^\top z.
\tag{6}
\]

The second term is an independent Gaussian reserve of covariance

\[
(W^\top W)^{-1}\otimes I_d.
\]

It is independent of every source query. This is derived from the finite seed program.

For the joint absorption construction, the new output-response matrix is explicit. If the incoming record and child programs certify reserve fraction \(\rho\), the constructed response satisfies

\[
W_{\rm new}^\top W_{\rm new}
\preceq
\rho^{-1}
\operatorname{blockdiag}
\bigl(C_{\rm new}^{-1},S_i^{-2}\bigr).
\tag{7}
\]

**The reserve fraction need not decay through internal DAG layers.**

An external-center gauge can also be constructed. Its norm increment is bounded by

\[
\sqrt{\kappa^\top\Gamma\kappa/\rho},
\]

where \(\kappa\) is the known response of the deterministic offsets to the external center.

### A real closure failure, followed by a repair

The newly constructed center gauge need not be orthogonal to the output-response matrix. The exact executed example produced

\[
V^\top W=(3/16,-27/16,0,0,0,0).
\]

Assuming orthogonality would therefore have broken recursive promotion of the program to a child.

There is a finite repair requiring no source calls. Append one unused Gaussian \(d\)-vector slot and define, for \(V\ne0\),

\[
V_{\rm aug}=
\begin{bmatrix}V\\ \|V\|\end{bmatrix},
\qquad
W_{\rm aug}=
\begin{bmatrix}
W\\ -V^\top W/\|V\|
\end{bmatrix}.
\]

The program ignores that slot, so its actual output and queries are unchanged. Nevertheless,

\[
V_{\rm aug}^\top W_{\rm aug}=0,
\]

and

\[
\|V_{\rm aug}\|^2=2\|V\|^2,
\qquad
W_{\rm aug}^\top W_{\rm aug}\preceq2W^\top W.
\tag{8}
\]

The price is one seed slot, a \(\sqrt2\) gauge factor, and at most a factor-two loss in the guaranteed reserve covariance per such promotion. Those factors remain in the cost recurrence. An explicitly untouched final reserve, as already present in S1, can avoid this particular loss.

### A code-derived normal form

For fixed affine value-query programs there is another constructive route. Write the physical queries as

\[
q_i=u_i+b_i x+\sum_{j<i}a_{ij}g(q_j)+\sum_k B_{ik}Z_k,
\]

and the output as

\[
Y=cx+v+\sum_j f_jg(q_j)+DZ.
\]

All displayed coefficients are known and independent of the source values. Put

\[
P=B^\dagger B,\qquad
U=bx+BZ,\qquad
a=c-DB^\dagger b.
\]

Induction over the queries shows that \(U\) determines every physical query and returned source value. Moreover,

\[
\boxed{
Y=ax+\Psi(U)+D(I-P)Z.
}
\tag{9}
\]

The last term is an exactly independent Gaussian reserve, with known covariance

\[
R=D(I-P)D^\top.
\]

The minimum-norm query-preserving center gauge is \(-B^\dagger b\). After tracking the known affine term \(ax\) separately, that gauge is orthogonal to the reserve.

This constructs the useful representation: **query-visible Gaussian inputs, the source evaluations they determine, a known affine response, and an independent Gaussian reserve.** It does not apply automatically to source-dependent rejection branches or arbitrary nonlinear coefficients.

The normal-form identities were checked with exact rational matrices and executed against an 11-dimensional nonseparable conservative source. No source mean was supplied.

Proof and checks: AFFINE_ORACLE_NORMAL_FORM.md[AFFINE_ORACLE_NORMAL_FORM.md](sandbox:/workspace/scratch/810b1ee40202/research/round2_main/AFFINE_ORACLE_NORMAL_FORM.md).

## 3. A complete general value-only Gaussian channel was executed

To establish a fully acquired comparator, I specialized the Gaussian-cloud fluctuation correction to the actual source contract and reconstructed explicit constants and deterministic caps. The underlying likelihood mechanism is existing primary research; it is not being claimed as a new general sampling method. The paper’s robust correction theorem and gradient-only implementation are directly relevant to this acquisition problem. [arxiv.org](https://arxiv.org/html/2609.38710v1?utm_source=chatgpt.com) [arxiv.org](https://arxiv.org/html/2609.38710v1?utm_source=chatgpt.com)

The resulting construction works for every source in the original class and every \(\sigma>0\). Its dimension cost is still roughly \(\sqrt d\).

### An acquired action with the required realized-map properties

For fixed \(c,a,r,\xi\), define

\[
\mathcal D(v)
=
\frac{\|v\|}{2r}
\left[
g\!\left(c+a\xi+r\frac v{\|v\|}\right)
-
g\!\left(c+a\xi-r\frac v{\|v\|}\right)
\right].
\tag{10}
\]

At \(v=0\), the convention returns zero while still making two repeated-center queries.

For each fixed seed, this entire realized map is:

- odd and positively homogeneous;
- bounded by \(\|\mathcal D(v)\|\le L\|v\|\);
- globally \(\sqrt2L\)-Lipschitz.

Its conditional mean satisfies the all-direction bound

\[
\left\|
\mathbb E\mathcal D(v)-D(P_ag)(c)v
\right\|
\le
\frac{Lr}{\sqrt{2\pi}\,a}\|v\|.
\tag{11}
\]

The action is not asserted to be a random linear matrix. The useful property is its joint behavior as a function of the direction, together with a uniformly linear relative error.

Two independent compositions acquire the squared heat-Hessian action in four values. Conservativity provides symmetry, so no transpose oracle is introduced.

For an average of \(M\) Gaussian source evaluations, selecting one Brownian block and one time acquires the corresponding covariance action in four values, independently of \(M\). Evaluating the **same realized action** at both likelihood-word vectors costs eight values; both internal smoothing seeds and the Brownian anchor are shared.

Every Brownian point is generated by a Gaussian bridge between already retained neighboring times. The paths are retained across all likelihood estimators in an attempt.

### Full-law guarantee and every-execution cost

Let

\[
\rho=L/\sigma,\qquad \alpha=2\rho^2/M,
\]

and, for even \(p\),

\[
e_p=5\alpha(\sqrt{dp}+p)+3\alpha^2d.
\]

The reconstructed full-law bound is

\[
\operatorname{TV}
\le
4d\alpha^{K+1}
+12\eta\alpha d
+6B(e_p/B)^p
+2\rho s\sqrt d,
\tag{12}
\]

before separately budgeted stopping caps. Here:

- \(K\) is the likelihood-word order;
- \(\eta\) is the uniform relative action bias;
- \(s\) is source smoothing;
- \(B=1/4\) is the clipping bound.

The proof compares full positive likelihoods and uses the Brownian exponential-martingale identity. It does not infer a Gaussian law from moments.

One explicit parameter assignment is

\[
p=2\left\lceil\frac{\log(128/\varepsilon)}{\log16}\right\rceil,
\qquad
M=\left\lceil256(1+\rho^2)(\sqrt{dp}+p)\right\rceil,
\]

\[
K=\max\!\left\{
1,\left\lceil
\frac{\log(64d/\varepsilon)}{\log(1/\alpha)}
\right\rceil
\right\},
\]

\[
A=\left\lceil\log_2(64/\varepsilon)\right\rceil,
\qquad
J=\left\lceil\log_2(64A/\varepsilon)\right\rceil.
\]

The proof specifies \(s\) and the secant radius so that the smoothing and action-bias terms are each at most \(\varepsilon/16\). All four terms in (12) together are below \(\varepsilon/4\), leaving room for the caps and scalar approximation.

The complete deterministic source-query bound is

\[
\boxed{Q_{\max}=1+A[M+8JK].}
\tag{13}
\]

It counts the offset-removing \(g(0)\) query, every proposal, every rejected proposal, and every action evaluation.

Poisson sampling is also acquired: a finite rational Taylor table and Gaussian-generated uniforms implement a capped Poisson law, with its approximation error included. There is no uncharged source fitting.

The additional arithmetic is

\[
O\!\left(
dA[M+JK]+A(JK)^2+AJK\log(M+1)
\right),
\]

plus polynomial rational-table work. Storage is \(O(d[M+JK])\).

The guarantee is uniform over supplied centers. Fresh calls at adaptively acquired centers therefore compose with the sum of their conditional TV budgets. This is actual output-law reuse. **It is not automatically the pathwise gauge contract required by the separate DAG compiler:** the rejection decisions would need an additional argument before those constructions could be combined recursively.

Complete algorithm, constants, and proof: ACQUIRED_CAPPED_GAUSSIAN_CHANNEL.md[ACQUIRED_CAPPED_GAUSSIAN_CHANNEL.md](sandbox:/workspace/scratch/810b1ee40202/research/round2_challenge/ACQUIRED_CAPPED_GAUSSIAN_CHANNEL.md).  
Executable: capped_gaussian_channel.py[capped_gaussian_channel.py](sandbox:/workspace/scratch/810b1ee40202/research/round2_challenge/capped_gaussian_channel.py).

## 4. Why this acquired channel cannot simply be tuned to polylogarithmic dimension

The \(\sqrt d\) cost is not merely an artifact of the upper-bound calculation for this particular proposal.

A single log tilt bounded in \([-B,B]\) can increase the probability of any proposal event by at most \(e^{2B}\).

Take the legal affine conservative source \(g(x)=\lambda x\). After normalization by \(\sigma\), its averaged proposal is

\[
Q=N(0,(1+\beta)I_d),
\qquad
\beta=\frac{\lambda^2}{M\sigma^2},
\]

whereas the target is \(P=N(0,I_d)\).

For the radius event

\[
E=\{\|y\|^2\le d(1+\beta/2)\},
\]

Gaussian tail bounds imply, for \(0<\beta\le1\),

\[
\boxed{
\operatorname{TV}(P,P_{\rm clip})
\ge
1-e^{-d\beta^2/24}
-e^{\,2B-d\beta^2/64}.
}
\tag{14}
\]

For the capped implementation, subtract its already budgeted coupling error.

Consequently, at fixed \(B\) and \(\lambda/\sigma\),

\[
M=o(\sqrt d)
\quad\Longrightarrow\quad
\operatorname{TV}(P,P_{\rm clip})\to1.
\]

Increasing the word order or shrinking the secant radius cannot repair this architectural failure.

The saved calculation at \(d=2^{30}\), \(M=900\), \(B=1/4\), and \(\lambda/\sigma=1\) gives the lower bound \(0.99999999833\).

This is deliberately scoped. The same affine source’s mean is obtained by one query at zero. Equation (14) rejects the averaged-proposal/bounded-global-tilt mechanism, not the target. A better construction needs a source-aware proposal or a transport capable of correcting many coordinates simultaneously.

## 5. A stronger obstruction to a cheap hidden-center oracle

I also tested the idea that a nonlinear mean operation could be recovered cheaply from Gaussian samples of an unknown center, paying only a local statistical precision cost.

That is too strong.

Consider this intermediate contract:

- \(g\) is fixed and may even be completely known;
- an unknown \(\theta\) enters only through at most \(n\) independent observations \(N(\theta,\tau^2)\);
- arbitrary computation, auxiliary randomness, and unlimited values of this fixed \(g\) are allowed;
- the required output is uniformly TV-close to
  \[
  N\!\left(\mathbb E g(\theta+rG),S^2\right).
  \]

For \(0<\kappa=Lr/S\le1\), I proved that some legal sources require

\[
\boxed{
n\ge
\frac{\tau^2}{2r^2\log(12/\kappa)}
\qquad
\text{when }\varepsilon\le\kappa/32.
}
\tag{15}
\]

### Proof of the discriminating bound

Choose

\[
g(x)=Lr\cos(x/r),
\qquad
F(x)=Lr^2\sin(x/r).
\]

This is a globally \(L\)-Lipschitz smooth conservative source, and

\[
m(\theta)=Lr e^{-1/2}\cos(\theta/r).
\]

The sample mean of the \(n\) center observations is sufficient and has law

\[
N(\theta,\tau^2/n).
\]

The residual observations are independent of both the mean and \(\theta\). A bounded adaptive observation rule can be padded to \(n\), so the whole algorithm is a positive kernel from this sufficient statistic.

Take the output characteristic function at argument \(1/S\), then its Fourier coefficient in \(\theta\) at frequency \(1/r\). Gaussian input convolution attenuates that coefficient by

\[
e^{-\tau^2/(2nr^2)}.
\]

The target coefficient has magnitude

\[
e^{-1/2}J_1(\kappa e^{-1/2}).
\]

The alternating Bessel series gives

\[
J_1(z)\ge \frac{7z}{16},\qquad 0\le z\le1,
\]

so the target coefficient exceeds \(7\kappa/48\). TV error at most \(\kappa/32\) changes the characteristic coefficient by at most \(\kappa/16\). Therefore

\[
e^{-\tau^2/(2nr^2)}\ge \kappa/12,
\]

which proves (15).

The proof does not assume a periodic kernel: long-interval Fourier averages have a translation boundary error tending to zero. It uses bounded tests, not output moments.

For \(L=S=\tau=1\), the certified integer consequences include:

| \(\kappa=r\) | Required TV accuracy | Required center observations |
|---:|---:|---:|
| \(1/16\) | \(1/512\) | At least \(25\) |
| \(1/256\) | \(1/8192\) | At least \(4{,}081\) |
| \(1/4096\) | \(1/131072\) | At least \(776{,}531\) |

These integer comparisons were certified with rational exponential enclosures.

The related exact rigidity statement is also useful: a fixed positive kernel mapping every \(N(\theta,I)\) to \(N(m(\theta),\Sigma)\), with fixed \(\Sigma\), forces \(m\) to be affine. Gaussian transition-operator characterization is established mathematical territory; the files give a self-contained proof and make no priority claim. [Theory of Probability &amp; Its Applications](https://epubs.siam.org/doi/10.1137/S0040585X97T988435?utm_source=chatgpt.com)

**The consequence for the research direction is specific:** a universal cheap nonlinear hidden-center Gaussian oracle cannot replace the retained source dependence. The original N687 algorithm is allowed information that this restricted oracle discards, including correlations between its intermediate centers and the original source-query history.

Proof and independent audit: CLOUD_ONLY_ACQUISITION_LOWER_BOUND.md[CLOUD_ONLY_ACQUISITION_LOWER_BOUND.md](sandbox:/workspace/scratch/810b1ee40202/research/round2_main/CLOUD_ONLY_ACQUISITION_LOWER_BOUND.md).

## 6. A high-dimensional positive benchmark at the cheaper precision scale

The affine case shows that the larger pathwise source-precision cost is not always intrinsic.

Let \(g(v)=Av+c\), with unknown symmetric \(A\), \(\|A\|_{\rm op}\le L\). Let the center itself be unavailable, supplied only as

\[
X=\theta+\tau Z.
\]

For \(S>\tau L\), define analytically

\[
B=(S^2I-\tau^2A^2)^{1/2}.
\]

Then

\[
Y=g(X)+BW,
\qquad
X_{\rm new}=X-\tau^2AB^{-1}W
\tag{16}
\]

are independent Gaussians, with

\[
Y\sim N(A\theta+c,S^2I),
\]

\[
X_{\rm new}\sim
N\!\left(\theta,
(\tau^{-2}I-S^{-2}A^2)^{-1}\right).
\]

The matrix operations are acquired from values: query \(g(0)\), then obtain \(Av=g(v)-g(0)\). Shared binomial polynomial expansions implement both actions using exactly \(2n+3\) source values, \(O(nd)\) arithmetic, and \(O(d)\) working storage.

Writing \(q=\tau L/S<1\), the full joint-law bound is

\[
\operatorname{TV}
\le
3\sqrt d\,\frac{q^{2n+2}}{1-q^2}.
\tag{17}
\]

At fixed \(q\), this gives \(O(\log d+\log(1/\varepsilon))\) queries.

This is an ordinary matrix-polynomial Gaussian simulation construction. An equally informed conventional method reproduces it. Its value here is as an acquired joint-reuse benchmark with unknown matrix and unknown center. Replacing \(A\) by a random unbiased secant does not preserve its Gaussian-law proof.

Proof and implementation: AFFINE_VALUE_ONLY_CLOUD_CHANNEL.md[AFFINE_VALUE_ONLY_CLOUD_CHANNEL.md](sandbox:/workspace/scratch/810b1ee40202/research/round2_positive/AFFINE_VALUE_ONLY_CLOUD_CHANNEL.md).

## 7. Evidence, comparison, and the exact remaining obligation

The executed work includes:

- **General acquired channel:** 96 parameter checks, 200 shared-action checks, null-event controls, and eight outputs from multidimensional sums of noncommuting rotated clipping gradients. Rejected proposals and retained Brownian bridges were exercised.
- **Joint reuse:** exact rational covariance, projector, positivity, and response-Gram identities; a demonstrated orthogonality failure and its exact repair; 17-dimensional nonlinear query replay.
- **Normal form:** exact rational projection and reserve identities, plus 11-dimensional nonlinear query and output-response replay.
- **Affine channel:** dimensions \(5,17,64,129\), three noise ratios, and a null-seed execution.
- **Obstructions:** bounded-test proofs and exact rational numerical certificates.

For the general channel, actual calls ranged from **3,489 to 10,177 per output**, within deterministic caps **32,257 and 52,641**. Those constants are conservative and do not establish a practical speedup.

This continuation executed **109,097 synthetic source calls**, including recorded development reruns. Floating runs test implementation identities; the full-law evidence is the mathematical proof. A finite-bit guarantee against a commonly rounded target remains a separate obligation.

The strongest comparisons remain:

| Construction | Established scope and cost | Remaining limitation |
|---|---|---|
| Independent averaging plus Gaussian noise | General Lipschitz source; \(O(\sqrt d/\varepsilon)\) values | Poor accuracy dependence |
| Acquired capped cloud channel here | Full conservative class; \(\sqrt d\) times logarithms; complete deterministic cap | Bounded global tilt cannot remove its dimension scale |
| Frozen S1 candidate | Arbitrarily small **fixed** positive dimension exponent | Candidate proof and order-dependent costs do not give a uniform polylog theorem |
| Joint DAG reuse compiler | Full joint-law reuse; one execution per logical child | Precision, gauge, reserve, and child-acquisition recurrences must close |
| Affine unknown-center channel | Polylogarithmic queries; acquired joint output | Affine subclass; ordinary matrix-polynomial comparator matches it |

The previous coercive inverse remains useful analytical machinery. Its coefficient acquisition, dimension-normalized control, and reusable nonlinear correction are still unresolved.

**The next scientific obligation is now narrower:** construct a positive nonlinear transport or correction acting on the retained query-visible Gaussian program, with a defect that improves superlinearly at a dimension-normalized scale, while closing

\[
D^{-1}-A^\top\Gamma A\succ0,
\]

the final \(\sigma^2\) budget, the reserve/gauge growth, and the complete original-value query recurrence.

A small global likelihood refinement of the same averaged proposal will not do this. Nor can an unrestricted cheap hidden-center Gaussian oracle be assumed in its place. The new reuse compiler and normal form preserve the source information and Gaussian noise needed for a more capable correction; the missing step is to exploit that structure with a proved nonlinear law improvement and a polylogarithmic total cost.