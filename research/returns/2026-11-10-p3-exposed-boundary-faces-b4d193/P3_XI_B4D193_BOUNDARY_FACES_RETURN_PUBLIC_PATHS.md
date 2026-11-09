# P3 complete Xi return

Source: https://chatgpt.com/c/6af11227-f57c-83ec-80e4-caf25a4bae01
Actual user turn: 753f43ef-a02a-41f2-9133-e68807ec4d13; response: b4d19317-f611-4972-a13f-b74d018e32a7.
Exact actual prompt reference: P3_FULL_MEAN_CALIBRATION_AFTER_80D545_XI_20261109.txt; SHA-256 742b1c7516d93c72a7e33ef4565abeb8805084cc972634536df41434e4f69a6a, with only terminal LF omitted in the posted body.
Model: GPT-6 standard, Extra High selected at send. No ZIP identified in the completed response.

## Available visible activity

Worked for 12m 53s. Developed structural bounds and boundary recursion controlling dual parameters and normal tilts; Extended face control, handled one-dimensional faces, bounded complexity, and established conditioning; Confirmed the reduction; Refining the proof; Searched 9 websites.

## Complete response (verbatim)

# P3 continuation — Logarithmic-accuracy extraction of equilibrium boundary faces

The accepted universal midpoint-balancing theorem changes what can be proved about boundary targets. I obtain a new uniform operation: **an entire equilibrium law conditioned on any exposed face containing the target can be approximated by ordinary positive rational activities with only logarithmic dependence on the requested accuracy.**

This removes the \(1/\epsilon\) dependence for suppressing a known face. It does not yet solve the global problem of selecting all the activity directions needed for an arbitrary target.

## 1\. The face-extraction theorem

Fix a weakly reversible structure \(R\), an actual class \(\Gamma\), and a feasible target \(m\)\.

Let

\[
\lambda_i^{(0)}=m_i+1,
\qquad
\pi_0(x)=\frac{W_0(x)}{Z_0},
\qquad
W_0(x)=\prod_i\frac{(\lambda_i^{(0)})^{x_i}}{x_i!}.
\]

The accepted universal local-witness theorem gives a computable constant \(H_R\) and an integer population \(y\in\Gamma\) such that

\[
\|y-m\|_\infty\le H_R.
\]

Its target-centred probability bound yields

\[
\boxed{\pi_0(y)\ge e^{-K_R},\qquad K_R=c_R(1+L),}
\tag{1}
\]

where \(c_R\) is computable and \(L\) is the complete binary input length.

Now let \(n\in\mathbb Z^d\setminus\{0\}\) and \(b\in\mathbb Z\) define a valid supporting inequality

\[
n\cdot x\ge b\quad(x\in\Gamma),
\qquad n\cdot m=b.
\tag{2}
\]

Define its exposed population set

\[
\Gamma_F=\{x\in\Gamma:n\cdot x=b\}.
\]

**Theorem.** If \(\|n\|_1\) is bounded by a fixed constant or by a polynomial in \(L\), there is a deterministic polynomial-bit construction of positive rational activities \(\lambda^{(T)}\) such that the full equilibrium law \(\pi_T\) satisfies

\[
\boxed{
\|\pi_T-\pi_0(\cdot\mid\Gamma_F)\|_{\rm TV}
\le\epsilon
}
\tag{3}
\]

and

\[
\boxed{
\max_i\left|
\mathbb E_{\pi_T}X_i-
\mathbb E_{\pi_0}[X_i\mid\Gamma_F]
\right|\le\epsilon.
}
\tag{4}
\]

The construction uses \(O_R(L+\log_2(1/\epsilon))\) bits per unit of \(\|n\|_1\), with no numerical-population loop, rare-event rejection, or conservation assumption.

### Proof

Let

\[
D(x)=n\cdot x-b.
\]

By (2),

\[
D(x)\in\mathbb Z_{\ge0}
\]

for all \(x\in\Gamma\)\.

The local mean witness for \(m\) is a convex combination of populations in \(\Gamma\)\. Taking the mean of \(D\) gives zero. Since \(D\ge0\), every population in that witness must satisfy \(D=0\)\.

In particular, \(y\in\Gamma_F\), so

\[
\boxed{
p_F:=\pi_0(\Gamma_F)\ge e^{-K_R}.
}
\tag{5}
\]

For an integer \(T\ge1\), put \(t=2^{-T}\) and choose

\[
\boxed{
\lambda_i^{(T)}=(m_i+1)t^{n_i}.
}
\tag{6}
\]

These are strictly positive ordinary rationals, including when \(n_i<0\)\.

The associated full class-conditioned law is exactly

\[
\pi_T(x)=
\frac{\pi_0(x)t^{D(x)}}
{\mathbb E_{\pi_0}[t^{D(X)}]}.
\tag{7}
\]

The factor \(t^{-b}\) cancels from numerator and denominator.

For \(D(x)=0\), the multiplier equals one; for \(D(x)\ge1\), it is at most \(t\)\. Thus

\[
\sum_{x\notin\Gamma_F}\pi_0(x)t^{D(x)}\le t.
\]

Writing \(Z_T'=\mathbb E_{\pi_0}[t^{D(X)}]\), we have \(Z_T'\ge p_F\) and

\[
\Pr_{\pi_T}(X\notin\Gamma_F)\le\frac{t}{p_F}\le te^{K_R}.
\tag{8}
\]

The conditional law of \(\pi_T\) on \(\Gamma_F\) is exactly \(\pi_0(\cdot\mid\Gamma_F)\)\. Therefore the total variation distance in (3) is precisely the off-face probability.

For mean control, note that

\[
\mathbb E_{\pi_0}X_i
\le
\frac{\mathbb E[\operatorname{Pois}(m_i+1)]}
{\Pr_{\otimes\operatorname{Pois}(m+1)}(Y\in\Gamma)}
\le (m_i+1)e^{K_R}.
\tag{9}
\]

The same inequality and \(p_F\ge e^{-K_R}\) bound the conditional first moment on the face.

Using the decomposition of \(\pi_T\) into its face and off-face components,

\[
\begin{aligned}
\left|
\mathbb E_{\pi_T}X_i-
\mathbb E_{\pi_0}[X_i\mid\Gamma_F]
\right|
&\le \frac{t}{p_F}
\left(
\mathbb E_{\pi_0}X_i+
\mathbb E_{\pi_0}[X_i\mid\Gamma_F]
\right)\\
&\le 2t(m_i+1)e^{2K_R}.
\end{aligned}
\tag{10}
\]

Choose

\[
\boxed{
T=\left\lceil
\frac{2K_R+\log(4d(1+\|m\|_\infty)/\epsilon)}
{\log2}
\right\rceil+2.
}
\tag{11}
\]

Then (8)–(10) give both (3) and (4).

Because \(K_R=O_R(L)\) and the target is binary encoded, \(T=O_R(L)\) for a requested binary rational \(\epsilon\) already included in \(L\)\.

Finally, writing

\[
(m_i+1)2^{-Tn_i}
\]

as an ordinary numerator/denominator rational adds only \(O(T|n_i|)\) bits. All operations are integer arithmetic and bounded-precision rational calculations.

This proves the theorem.

## 2\. A paid log-partition evaluator for arbitrary exposed faces

The previous result also gives a new operation not already supplied by DDB1: **weighted inference on an exposed face that need not itself be a reaction communicating class.**

Define its unnormalized partition function

\[
Z_F(\lambda^{(0)})
=
\sum_{x\in\Gamma_F}
\prod_i\frac{(m_i+1)^{x_i}}{x_i!}.
\]

DDB1 directly evaluates partition functions of actual classes, not arbitrary intersections of classes with supporting hyperplanes.

Nevertheless, consider the activity vector (6). Its complete class partition function satisfies the exact identity

\[
Z_\Gamma(\lambda^{(T)})
=
t^b\left(Z_F(\lambda^{(0)})+E_T\right),
\]

where \(E_T\ge0\) is the contribution from outside the face after multiplying by \(t^{D(x)}\)\.

The relative error is bounded by

\[
\frac{E_T}{Z_F(\lambda^{(0)})}
\le\frac{t}{p_F}\le te^{K_R}.
\]

Consequently,

\[
\boxed{
0\le
\log Z_\Gamma(\lambda^{(T)})
-b\log t-\log Z_F(\lambda^{(0)})
\le te^{K_R}.
}
\tag{12}
\]

Given a binary rational \(0<\delta<1\), choose

\[
T\ge\left\lceil\frac{K_R+\log(4/\delta)}{\log2}\right\rceil.
\]

Run the paid DDB1 log-partition evaluator on \(\lambda^{(T)}\) to additive error \(\delta/4\), and compute the rational approximation to \(b\log t\) to error \(\delta/4\)\.

Equation (12) gives a rational output \(a_F\) satisfying

\[
\boxed{
|a_F-\log Z_F(\lambda^{(0)})|<\delta.
}
\tag{13}
\]

The complexity is polynomial in

\[
L+\|n\|_1\bigl(L+\log(1/\delta)\bigr).
\]

Here every input activity is written explicitly in binary, and the potentially enormous normalizing probability is never formed directly.

### Multiple exposed constraints

The same argument works for any nonempty face specified by finitely many integral supporting equalities

\[
n_j\cdot x=b_j,\qquad j=1,\ldots,s,
\]

where \(n_j\cdot x\ge b_j\) on \(\Gamma\) and \(n_j\cdot m=b_j\)\.

Set

\[
D(x)=\sum_{j=1}^s(n_j\cdot x-b_j).
\]

Then \(D(x)\) is a nonnegative integer and its zero set is exactly the intersection of those exposed faces. Replace \(n\) by \(\sum_jn_j\) in the activity tilt.

All estimates continue to hold. Thus intersections of exceptional boundary faces are included, not just single facets.

## 3\. An unconditional sampler supported exactly on an exposed face

There is a useful sampling counterpart.

Suppose the goal is to sample

\[
\pi_F=\pi_0(\cdot\mid\Gamma_F)
\]

to total variation accuracy \(\delta\), with **every possible output belonging to \(\Gamma_F\)**\.

The construction is\:

1. Compute the local witness and select an integer point \(y\in\Gamma_F\)\.
2. Choose \(T\) so that the full tilted law \(\pi_T\) has off-face probability at most \(\delta/4\)\.
3. Invoke the accepted DDB1 sampler at activities \(\lambda^{(T)}\), with entire-law total variation error at most \(\delta/4\)\.
4. If its sample \(X\) lies on the face, output \(X\)\. Otherwise output the precomputed \(y\)\.

The last step is deterministic and ensures that every run returns a valid face population.

Changing the outside-face outcomes to \(y\) modifies the ideal tilted distribution by total variation at most \(\delta/4\)\. The sampler's original approximation error remains at most \(\delta/4\) under this deterministic mapping.

Therefore the returned unconditional law satisfies

\[
\boxed{
\|\mathcal L(X_{\rm output})-\pi_F\|_{\rm TV}
<\delta.
}
\tag{14}
\]

Everything is paid: the witness computation, original class sampler, normal comparison, replacement and binary output.

This gives an effective inference compiler for a class-conditioned law restricted to a known exposed face, even if that face is not closed under the original physical reaction dynamics.

## 4\. The remaining obstruction can be expressed as a weighted slice-growth bound

The face-extraction construction suggests a more precise route toward the unrestricted inverse-height theorem.

Suppose \(F\) is an exposed face with integral supporting inequality

\[
D(x)=n\cdot x-b\ge0.
\]

For any log-activity vector \(\theta\), define the weighted slices

\[
Z_k(\theta)=
\sum_{\substack{x\in\Gamma\\D(x)=k}}
\frac{e^{\theta\cdot x}}{x!},
\qquad k=0,1,\ldots,
\]

and their first-moment counterparts

\[
M_k(\theta)=
\sum_{\substack{x\in\Gamma\\D(x)=k}}
(1+\|x\|_1)\frac{e^{\theta\cdot x}}{x!}.
\]

The exact face-extraction theorem works because, at the target-centred baseline \(\theta_0=\log(m+1)\), the aggregate off-face mass can be compared with an explicitly non-negligible on-face anchor.

For a recursively calibrated activity on the face, the corresponding comparison is not automatic.

### A sufficient slice-growth statement

Suppose there is a computable fixed-\(R\) polynomial \(P_R\) such that, whenever \(\theta\) has numerical magnitude at most \(B\) and its face-conditioned equilibrium mean is sufficiently close to \(m\),

\[
\boxed{
M_k(\theta)\le
Z_0(\theta)\,
2^{P_R(L+B)(k+1)}
\qquad(k\ge1).
}
\tag{15}
\]

Then choose an integer

\[
T=3P_R(L+B)+
\left\lceil\log_2(16/\epsilon)\right\rceil+10
\]

and tilt along \(-Tn\log2\)\.

The weighted off-face first moment relative to the face partition becomes

\[
\begin{aligned}
\frac1{Z_0(\theta)}
\sum_{k\ge1}2^{-Tk}M_k(\theta)
&\le
2^{P_R(L+B)}
\sum_{k\ge1}2^{-k(T-P_R(L+B))}\\
&<\epsilon/8.
\end{aligned}
\tag{16}
\]

Thus the full law under the tilted activities has mean within \(\epsilon/8\) of the face-conditioned law.

The important feature is that the required normal tilt is polynomial in \(L+B\) and logarithmic in the accuracy, not proportional to \(\epsilon^{-1}\)\.

This would allow inverse parameters already constructed on one face to be lifted to the original class at controlled additional height.

### Why (15) is not already proved

The accepted local-witness and conformal-word theorems give strong geometric information: nearby legal reaction directions, bounded midpoint balancing and short binary-encoded reachability certificates.

However, (15) is a comparison of **entire weighted populations of different slices**\. It requires control of factorial carrier ratios and of the number of populations contributing to each slice, uniformly over possibly unbounded tangent directions.

The target-centred bound in Section 1 handles a special case because its reference Poisson means are explicitly \(m_i+1\)\. After a large tangential tilt, the full unconditioned product-Poisson law can have enormous means, even when the distribution conditioned on the face has the desired target mean.

Therefore the bound at the target-centred reference cannot simply be reused after tangential calibration.

Proving (15), or a weaker aggregate bound sufficient for (16), is a concrete remaining mathematical task. It is not an established consequence of the accepted midpoint-balancing theorem.

## 5\. Connection with finite-support maximum-entropy dual bounds

I also examined the proof mechanism of urlStraszak–Vishnoi, Maximum Entropy Distributions: Bit Complexity and Stability (2019)https://proceedings.mlr.press/v99/straszak19a/straszak19a.pdf\.

Their argument expresses a dual direction using supporting-facet normals and caps its nonnegative normal coefficients. Integer facet gaps then exponentially suppress off-face contributions. citeturn173181view0

The geometric mechanism resembles (15)–(16). The distinction is quantitative\:

| Ingredient | Finite-support theorem | Present reaction-class setting |
|--------|--------|--------|
| Supporting facets | Unary facet complexity | Must be controlled from fixed-\(R\) actual-class geometry |
| Weight ratios | Uniform finite prior-weight bound | Factorial weights on potentially unbounded populations |
| Suppression across facets | Integer gap of at least one | Integer gap of at least one |
| Off-face mass | Finite sum controlled by prior bounds and support size | Potentially infinite weighted slices |
| Target accuracy | Logarithmic dual dependence | Logarithmic dependence still sought |

A relevant independent geometric result is Eisenbrand and Rothvoss's urlA Parameterized Linear Formulation of the Integer Hull (SODA 2026)https://epubs.siam.org/doi/abs/10.1137/1.9781611978971.164, which establishes fixed possible integer-hull normal directions when a constraint matrix is fixed and its right-hand side varies. citeturn411263search4

That suggests a way of controlling normal directions for the fixed Presburger templates. It does not independently prove that their factorial-weighted slice partition functions satisfy (15).

## 6\. Updated status

| Result | Scope | Status |
|--------|--------|--------|
| Universal exact local mean witnesses | Every actual class of fixed weakly reversible \(R\) | Accepted ROOT |
| Full inverse calibration for rank \(\le1\), unimolecular, multipartite and fixed-degree creation structures | Their respective arbitrary-population classes | Accepted |
| Full calibration for inverse-polynomial accuracy | All \(R\), via accepted entropy radius and selector | Accepted |
| Logarithmic-accuracy exposed-face suppression | Every feasible target on a specified supporting face | **New, proved** |
| Paid exposed-face log-partition evaluation | Target-centred activities, finite or infinite class | **New, proved** |
| Unconditional sampling supported exactly on an exposed face | Target-centred face-conditioned law | **New, proved** |
| General weighted slice-growth inequality (15) | Arbitrary calibrated tangential activities | Not established |
| Full polynomial-binary inverse-height theorem | Every fixed weakly reversible \(R\) | **Open** |

The new construction is independent of whether the boundary face is itself an original reaction communicating class. It uses the accepted actual-class sampler and local witnesses rather than postulating additional reactions or a face-specific oracle.

**Final result\:** I have established logarithmic-accuracy extraction, normalization and sampling of arbitrary specified exposed boundary faces. This removes the inverse-\(\epsilon\) cost of suppressing an exposed face from target-centred activities and gives a concrete weighted-slice formulation for extending the result to calibrated tangential directions.

I have **not** established the unrestricted polynomial-in-\(L\) activity-height bound, an every-instance polynomial-bit calibration compiler, or a fixed-network negative counterexample.
