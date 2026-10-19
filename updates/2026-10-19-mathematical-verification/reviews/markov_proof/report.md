> Public selected edition of the 19 October audit. Original review SHA-256: `37e1e4613e36b7f1b549fa1a18b69b92e881adad986fb4d8e21392991e48383b`. Original scientific inputs are retained unchanged. Navigation and historical-receipt pointers are adapted to the selected public subset; mathematical statements, caveats and attribution are retained. Past private-audit statements describe that audit, before approved publication. Current reproduction and retained-file hashes are in the release README and FILES.json.

# Independent audit of the four-state Markov proof

**Verdict: the mathematical claims in the stated fixed-four-state setting are supported. I found no material gap in the sharp embedding criterion or the entropy minimization.** The value \(26.178911678346\ldots\) is the optimum for the particular rational observation matrix, over its time-homogeneous four-state generator embeddings. This audit does not establish a hidden-state entropy optimum, novelty, external peer review, formal verification, or a physical capability.

The source is `sources/pro/markov_family/reconstructed_markov_proof.md`, abbreviated **S** below. Its SHA-256 is `e6ce84755682685bad51c5f15399816a23a2174fe5834e5372ed57f5a2d7208f`. All line references refer to that snapshot. Sections 1–2 were read first. The spectral and rate reconstruction was completed before reading section 3; the independent entropy sum was recorded before reading section 4 in `derivation_before_entropy.md`. No original independent-check script/output or another review was read or executed. No source/snapshot/public files were changed.

The private implementation is `disposable/independent_check.py`; its independently generated evidence is `disposable/independent_certificate.json`. It imports no source audit code. Symbolic checks use SymPy 1.14.0. The numerical enclosure uses integer interval arithmetic with outward rounding at 90 decimal places, explicit series remainders, and integer square-root bounds. mpmath 1.3.0 proposes candidate bracket endpoints and supplies a secondary check; exact interval derivative signs certify the bracket without trusting that proposal.

**1. Real logarithms, nilpotents, and conventions.** S:15–41 and 56–72 are correct. With the orthogonal basis \(H=(\mathbf1/2,v,u,w)\), the three eigenspaces for \(b>2a\) have dimensions \(1,1,2\). Every logarithm commutes with its exponential, so it preserves those eigenspaces. Real scalar restrictions exponentiating to 1 and \(e^{-a}\) must be 0 and \(-a\). On the final block, a Jordan nilpotent cannot disappear: \(e^N-I=Nh(N)\) and \(h(N)\) is invertible because \(h(0)=1\). Thus the block is diagonalizable over the complex numbers. Its only possibilities are \(-bI\) or eigenvalues \(-b\pm2\pi ki\), \(k\ge1\). The latter are exactly

\[
 -bI+R,\qquad R=\begin{pmatrix}A&B\\C&-A\end{pmatrix},\quad
 BC=-(A^2+\omega^2),\quad\omega=2\pi k.
\]

Conversely \(R^2=-\omega^2I\) gives \(e^R=I\). This includes arbitrary nonnormal blocks, rather than only orthogonal rotations. It exhausts real logarithms in the stated regime.

Each block acts within the subspace orthogonal to \(\mathbf1\), so every such logarithm has **both** zero row sums and zero column sums. Row vectors are therefore consistent with \(Q\mathbf1=0\), and the stationary row distribution is \((1/4,1/4,1/4,1/4)\). Irreducibility of \(P\) follows from its positive cross entries. Every generator embedding is also irreducible: a reducible generator would have a zero reachability cut inherited by its exponential. Hence there is no alternative stationary distribution with which to evade the reversibility argument. Symmetry of a reversible generator follows from uniform stationarity, and the symmetric logarithm of this positive definite matrix is uniquely \(L\). This validates S:134 and the reversible criterion \(b\le2a\), including equality.

**The \(a=b\) degeneracy needs the explicit scope qualifier in S:56.** At \(a=b>0\), the nontrivial eigenspace is three-dimensional, and formula (1), with a distinguished fixed \(v\), does not exhaust all logarithms. In an arbitrary orthonormal basis \(U\) of \(\mathbf1^\perp\), all logarithms have the form

\[
 Q=-a(I-\Pi)+UTU^T,
\]

where \(T=0\), or \(T\) is real-similar to \(0\oplus\begin{pmatrix}0&\omega\\-\omega&0\end{pmatrix}\), \(\omega=2\pi k\), \(k\ge1\). Nilpotents remain excluded. This does not invalidate the source: section 2 assumes \(b>2a\), while \(a=b\) belongs to the reversible regime and \(L=-a(I-\Pi)\) already attains zero entropy. Any unqualified reuse of “all real logarithms” across the whole parameter family should retain this distinction.

**2. Sharp rate feasibility.** Direct multiplication of the outer products reproduces every entry in S:82–85. Write \(p=|B|\), \(q=|C|\), and \(r^2=A^2+\omega^2=pq\). Since \(B,C\) have opposite signs, feasibility is exactly

\[
 A\ge b-2a>0,\qquad \sqrt2\max(p,q)\le b-A,\qquad
 \sqrt2(p+q)\le b+3A.
\]

The geometric-mean replacement \(p=q=r\) reduces both left sides and preserves the product, proving necessity and sufficiency of the balanced feasibility test. It is not an assumption that generators have a symmetry. The two remaining lower bounds on \(b\),

\[
 f_1(A)=A+\sqrt2\sqrt{A^2+\omega^2},\qquad
 f_2(A)=-3A+2\sqrt2\sqrt{A^2+\omega^2},
\]

increase and decrease, respectively, on \(A\ge0\). Their crossing is \(A=\omega/\sqrt7\), \(b=5\omega/\sqrt7\). Solving yields

\[
 A_-=-3b+\sqrt{8(b^2+\omega^2)},\qquad
 A_+=-b+\sqrt{2(b^2-\omega^2)},
\]

and the feasible set is \([\max\{b-2a,A_-\},A_+]\). Replacing \(k>1\) by \(k=1\) weakens both inequalities at the same \(A\). At \(k=1\), nonemptiness is precisely

\[
 b\ge10\pi/\sqrt7,\qquad a\ge b-\sqrt{(b^2-4\pi^2)/2}.
\]

Thus S:90–136 and Theorem 1 are supported. These inequalities imply stochasticity: the lower bound on \(a\) increases for \(b\ge10\pi/\sqrt7\) and is \(4\pi/\sqrt7>\log2\) at the threshold. In the reversible regime stochasticity follows from \(2e^{-b/2}\le1+e^{-b}\).

**3. Entropy normalization and global reductions.** The definition in S:7–13 is the standard unordered-pair stationary path entropy with natural logarithms, using the uniform factor \(1/4\). There is no missing factor of two. The pair \(12\) contributes zero even if its two rates simultaneously vanish.

After transposing if necessary, take \(B=p>0,C=-q<0\). Put \(c=(b-A)/4\), \(d=(b+3A)/4\), \(x=p/(2\sqrt2)\), \(y=q/(2\sqrt2)\), and \(t=x+y\). Direct summation of the four cross pairs and pair \(34\) gives

\[
 \sigma(Q)=\frac t2\left[
 \log\frac{c^2+xy+ct}{c^2+xy-ct}
 +\log\frac{d+t}{d-t}\right].
\]

At fixed \(A,\omega\), the product \(xy=(A^2+\omega^2)/8\) is fixed. Both logarithms are positive and strictly increase with \(t\) throughout the finite domain, so the whole expression strictly increases with \(t\). Its unique minimizing magnitudes have \(p=q=r\). This independently confirms S:140–155. It also excludes an asymmetric nonnormal logarithm with a smaller finite objective.

For balanced rates and \(s=\sqrt2\sqrt{A^2+\omega^2}\), the reduced function is exactly

\[
 F_{b,\omega}(A)=\frac{s}{2}\log\frac{b-A+s}{b-A-s}
 +\frac{s}{4}\log\frac{b+3A+2s}{b+3A-2s}.
\]

It strictly increases with \(s\) on its finite domain. A feasible higher-winding generator can first be balanced, then replaced at the same \(A\) by a strictly lower-entropy first-winding generator. The latter has strictly positive cross and \(34\) rates even if the former was at a one-way boundary. This validates the full winding reduction in S:157–166, rather than only a comparison within a guessed subfamily.

**4. Convexity, attainment, and infinite boundaries.** The perspective proof in S:170–182 is valid: for \(f(z)=z\log((1+z)/(1-z))\), \(f''(z)=4/(1-z^2)^2>0\) on \(0<z<1\), so \(h(c,j)=cf(j/c)\) is jointly convex. The function

\[
 G_b(A,s)=\tfrac12h(b-A,s)+\tfrac18h(b+3A,2s)
\]

is jointly convex and strictly increasing in \(s>0\). Since \(s''(A)=4\omega^2/s(A)^3>0\), composing gives strict convexity of \(F_b\). The relevant domain \(b-A>s\), \(b+3A>2s\) is the interval \((A_-,A_+)\); this remains true when \(A_-<0\). Its endpoints are genuine divergences because the numerator/current remains positive while one reverse rate vanishes. Thus a unique unconstrained minimizer \(A_*(b)\) exists when \(b>5\omega/\sqrt7\). If zero is inside the domain,

\[
 F_b'(0)=-\frac{s(0)^2(2b^2+s(0)^2)}{(b^2-s(0)^2)(b^2-4s(0)^2)}<0,
\]

so \(A_*>0\). Restricting to \(A\ge b-2a\) proves the clamping formula \(\widehat A=\max\{b-2a,A_*\}\). Balanced magnitudes and the strict reductions leave exactly the displayed optimizer and its transpose in the strict embedding interior, as claimed in S:184–205.

There is no escape through arbitrarily large rates or winding. For any generator embedding, \(\operatorname{tr}Q=\log\det P=-a-2b\); hence the sum of all nonnegative off-diagonal rates is \(a+2b\). The admissible generators lie in a compact rate simplex, and \(e^Q=P\) is a closed constraint. The extended pair entropy is lower semicontinuous: its value at two zero rates is zero, and at exactly one zero rate is infinity. This gives a separate attainment argument.

At \(b=10\pi/\sqrt7\), feasibility forces \(A=2\pi/\sqrt7\) and balanced rates, with one-way edges. At equality in the second embedding inequality, \(A=A_+\) and the maximum/product constraints again force balancing; a cross reverse rate is zero. All feasible generators at either nonprincipal embedding boundary therefore have infinite entropy. A zero symmetric \(12\) pair is harmless; it is not one of these divergences. The “minimum is infinity” statement uses the extended-real convention and does not assert existence of a finite-entropy embedding at the boundary.

**5. Exact rational example and independent numerical certificate.** Exact algebra verifies the rational matrix in S:211–222, including

\[
 H^TPH=\operatorname{diag}(1,2^{-8},2^{-18},2^{-18}).
\]

For the displayed \(Q_0\), with \(t=2\pi/\sqrt7\), the independent symbolic calculation gives

\[
 H^TQ_0H=0\oplus(-a)\oplus
 \begin{pmatrix}-b+t&2\sqrt2t\\-2\sqrt2t&-b-t\end{pmatrix}.
\]

Subtracting \(-bI\) from that block yields \(R_0^2=-7t^2I=-4\pi^2I\). Consequently its exponential is \(e^{-b}I\), giving **exactly** \(e^{Q_0}=P\). This is a spectral algebra proof, not a floating `expm` assertion. Exact outward-rounded intervals also give \(b-5t>0.6025\) and \(t-2\log2>0.9885\), verifying every off-diagonal witness rate is strictly positive. “All-positive generator” in S:224 should be read as positive off-diagonal rates; generator diagonals are negative.

The independent interval certificate proves

\[
2.2905478380320088794502388023657123520794
<A_*<
2.2905478380320088794502388023657123520795,
\]

with the derivative negative at the lower endpoint and positive at the upper endpoint. Its entropy enclosure is contained in

\[
26.17891167834635390855790239853806327479
<\sigma_*<
26.17891167834635390855790239853806327480.
\]

The bound \(A_*>2\log2=b-2a\) is certified, so the constraint is inactive. Only the first winding can be feasible for this example. The finite-rate margins \(b-A_*-s>0.7282\) and \(b+3A_*-2s>0.4326\) are certified as well. These results imply the source enclosure \(26.178911678346<\sigma_*<26.178911678347\) in S:237–240. As a secondary normalization check, a direct six-pair evaluation and the scalar objective agree to about \(4\times10^{-90}\) at 90-digit mpmath precision.

Reproduce from this private directory with `python3 disposable/independent_check.py`. The symbolic identities are at script lines 128–170; interval arithmetic/series bounds at lines 18–125; derivative signs, feasibility margins, and entropy assertions at lines 172–202; and direct pairwise evaluation at lines 204–228. An initial optional SciPy availability probe failed because SciPy is absent from the system Python; nothing here depends on it and no package was installed.

**6. Claim boundaries and remaining obligations.** The proof already states the necessary boundary in S:271. The optimized class fixes the exact \(P(a,b)\), one observation interval, four states, a constant real Markov generator, and stationary path entropy. The rational example has an exact repeated eigenvalue; a noisy or statistically estimated matrix requires a separate analysis. With a physical interval \(\tau\), the corresponding entropy rate is divided by \(\tau\), while entropy per observation interval is the reported quantity.

The number \(26.1789\ldots\) is not a positive floor over the whole two-parameter family. To see this directly, fix \(A=\varepsilon>0\), put \(a=(b-\varepsilon)/2\), choose balanced first-winding rates, and let \(b\to\infty\). These are feasible for sufficiently large \(b\), satisfy \(b>2a\), and have \(F_{b,2\pi}(\varepsilon)=4(\varepsilon^2+4\pi^2)/b+O(b^{-2})\to0\). Nor does the four-state optimum give a hidden-state lower bound: if the enlarged realization class contains the four-state chains, class inclusion gives only \(\inf\sigma_{\rm enlarged}\le26.1789\ldots\). A hidden-state floor needs its own theorem and hypotheses, which this audit has not assessed.

The four-state minimality argument in S:273 is also valid for irreducible reversible **positive-spectrum** stochastic matrices: in dimension three, the only repeated case is \(1,\mu,\mu\), for which \(P=\Pi_\pi+\mu(I-\Pi_\pi)\) and \(\log P=(\log\mu)(I-\Pi_\pi)\) has nonnegative off-diagonal rates. Use “positive spectrum” explicitly if the word “positive” could be read as entrywise positivity alone.

No mathematical correction is required for the claims with their present regime and state-space qualifications. The \(a=b\) distinction, the extended-real boundary convention, and the fixed-matrix quantifier should travel with any shorter restatement. Prior-art strength and Theorem 3.16 comparison were deliberately left to the separate literature reviewer. This is an internal model audit with reproducible exact checks, not external mathematical certification or physical validation.
