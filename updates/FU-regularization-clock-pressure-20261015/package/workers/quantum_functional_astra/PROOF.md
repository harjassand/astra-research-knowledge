# A fixed positive-density test for Hermitian polynomial symbols

Date: 2026-10-15. Status: internally derived theorem and counterexamples, with classical dependencies identified. No historical-priority, formal-verification, decision-complexity, or physical-capability claim is made.

## 1. The mathematical opportunity

The polynomial consequence in PR94 can be strengthened: for finite matrix coefficients, the regularizer's shape need not be adapted to the polynomial's Laplace-positivity margin. One fixed radial formula works for every strictly positive Hermitian polynomial, after an instance-dependent broadening.

This strengthening also narrows the foundational claim. It follows from the classical strict Positivstellensatz plus a finite derivative calculation, without the full compact-distribution convolution theorem. The actual novelty status of the explicit fixed-template formulation has not been cleared. Its useful content is an exact analytic representation and sharp distinctions between finite matrices, infinite operator coefficients, and Gaussian smoothing.

Let

\[
 P(g)=\sum_{|\alpha|\le d}P_\alpha g^\alpha,
 \qquad P_\alpha=P_\alpha^*\in M_n(\mathbb C),
 \qquad g\in\mathbb R^m.
\]

All variables in this polynomial commute. The coefficient matrices need not commute. Put

\[
 \rho(z)=\sqrt{1+|z|^2},\quad
 f(z)=\rho(z)\log\rho(z),\quad
 V_L(x)=L f(x/L),\quad
 p_L(x)=Z_L^{-1}e^{-V_L(x)}.
 \tag{1}
\]

The same formula is used for every polynomial, degree, and finite matrix size. Only the normalizing constant depends on the ambient dimension, and only the eventually sufficient value of \(L\) depends on \(P\).

**Theorem 1.** Assume \(P(0)\succ0\). The following are equivalent.

1. \(P(g)\succ0\) for every \(g\in\mathbb R^m\).
2. For every \(\epsilon\in(0,1)\), some finite \(L_0\) makes, for every \(L\ge L_0\) and every \(x\),
   \[
   (1-\epsilon)p_L(x)P(\nabla V_L(x))
   \preceq P(-\partial)p_L(x)
   \preceq(1+\epsilon)p_L(x)P(\nabla V_L(x)).
   \tag{2}
   \]
3. For some \(L>0\), \(P(-\partial)p_L(x)\succeq0\) for every \(x\).

The densities \(p_L\) are smooth, strictly positive, radial, and strictly log-concave. Every derivative is integrable against every exponential weight. The positive output has total matrix mass \(P(0)\), and

\[
 \int e^{g\cdot x}P(-\partial)p_L(x)\,dx
 =P(g)\int e^{g\cdot x}p_L(x)\,dx.
 \tag{3}
\]

Thus, after normalization, strictly positive finite Hermitian polynomial symbols are exactly those represented by a ratio of the Laplace transform of a positive matrix density and that of a member of one fixed scalar family.

The theorem includes polynomials with infimum zero at infinity and singular leading homogeneous part. Neither a uniform positive lower bound nor ellipticity is assumed.

The singular-mass version is exact as well: for an arbitrary finite Hermitian matrix polynomial, some member of (1) has positive-semidefinite differential output if and only if \(P(g)\succeq0\) for every real \(g\) and \(\ker P(g)\) is independent of \(g\). Necessity follows by integrating each nonnegative quadratic form and then using (3); sufficiency follows by compression to the fixed kernel's orthogonal complement and Theorem 1. The zero polynomial is included. This uses the same kernel argument already present in PR94, now with the fixed scalar family.

## 2. Classical algebra supplies the missing lower margin

We first isolate the only algebraic input.

**Lemma 2.** If \(P(g)\succ0\) everywhere and has finite matrix size, then there are \(c>0\) and a finite nonnegative integer \(\kappa\) such that

\[
 \lambda_{\min}(P(g))\ge c(1+|g|)^{-\kappa}
 \quad\hbox{for all }g.
 \tag{4}
\]

**Proof.** The scalar polynomial \(h=\det P\) is real and strictly positive on \(\mathbb R^m\). The strict Krivine–Stengle Positivstellensatz gives sums-of-squares polynomials \(a,b\) with

\[
 a h=1+b.
 \tag{5}
\]

In particular \(a>0\) everywhere. If \(s=\deg a\), there is a finite \(C_a>0\) with \(a(g)\le C_a(1+|g|)^s\), whence

\[
 \det P(g)\ge C_a^{-1}(1+|g|)^{-s}.
\]

Also \(\|P(g)\|\le A_P(1+|g|)^d\), where one may take
\(A_P=\sum_\alpha\|P_\alpha\|>0\). Since all eigenvalues are positive,

\[
 \lambda_{\min}(P(g))
 \ge\frac{\det P(g)}{\|P(g)\|^{n-1}}
 \ge\frac{(1+|g|)^{-[s+d(n-1)]}}{C_a A_P^{n-1}}.
\]

This proves (4). For complex Hermitian coefficients, the determinant still has real coefficients, since it is real on all real arguments. No matrix Positivstellensatz is needed. ∎

The identity (5) is established prior mathematics. A directly inspected primary research statement is Marshall–Netzer, *Positivstellensätze for real function algebras*, Theorem 1.4 and condition Q1, specialized to \(A=\mathbb R[g]\), \(X=\mathbb R^m\), \(Q=\sum A^2\): https://arxiv.org/html/1004.4521 . The original Stengle reference is https://doi.org/10.1007/BF01362149 . The latter's bibliographic record was inspected; its full original proof was not retrieved here.

This proof is an existence proof of \(c,\kappa\). It does not acquire a usable algebraic certificate, bound its degree, or establish an efficient way to choose \(L_0\).

## 3. The finite derivative estimate

Write \(z=x/L\), \(\rho=\rho(z)\), \(q=1+\log\rho\), and \(g=\nabla V_L(x)\). Direct differentiation gives

\[
 \nabla f=qz/\rho,
 \qquad D^2f=qD^2\rho+\rho^{-1}\nabla\rho\otimes\nabla\rho\succ0.
 \tag{6}
\]

For every \(j\ge1\), there is a scalar \(C_{m,j}\), independent of \(L,x,P,n\), such that

\[
 \|D^jf(z)\|\le C_{m,j}q\rho^{1-j},\qquad
 \|D^jV_L(x)\|\le C_{m,j}L^{1-j}q\rho^{1-j}.
 \tag{7}
\]

For \(j=1\), take the constant one. For higher \(j\), apply the chain rule to \(H\circ\rho\), where \(H(u)=u\log u\). The identities
\(H'=1+\log u\), \(H^{(j)}=(-1)^j(j-2)!u^{1-j}\) for \(j\ge2\), and \(D^j\rho=O_{m,j}(\rho^{1-j})\) prove (7) term by term.

For a derivative of total order \(r\), the exponential derivative formula expresses

\[
 \frac{(-\partial)^\alpha p_L}{p_L}
\]

as a finite sum indexed by partitions of \(r\) labelled derivative slots. A block of size \(j\) contributes a derivative \(D^jV_L\). The partition into singleton blocks is exactly \(g^\alpha\). Every other partition has \(b\le r-1\) blocks, and (7) bounds its magnitude by

\[
 C_{m,r} L^{b-r}q^b\rho^{b-r}
 \le \frac{C_{m,r}}L\frac{q^{r-1}}\rho,
 \qquad L\ge1.
 \tag{8}
\]

There is no remainder of infinite order: the polynomial has finite degree. Summing the finitely many coefficient-weighted formulas, and taking \(d\ge\max\{2,\deg P\}\), gives

\[
 \frac{P(-\partial)p_L(x)}{p_L(x)}=P(g)+E_L(x),
 \qquad
 \|E_L(x)\|\le \frac{C_{m,d}A_P}{L}\frac{q^{d-1}}\rho.
 \tag{9}
\]

The derivative constants can be bounded by explicit finite differentiation and partition enumeration. Their existence alone suffices for the theorem.

Combining (4), \(|g|\le q\), and \(1+q\le2q\),

\[
 \frac{\|E_L(x)\|}{\lambda_{\min}P(g)}
 \le\frac{C_{m,d}A_P2^\kappa}{cL}
 \frac{q^{d+\kappa-1}}\rho.
 \tag{10}
\]

For \(a=d+\kappa-1\ge1\), the last scalar factor has the exact supremum

\[
 B_a=\sup_{s\ge0}(1+s)^ae^{-s}=a^a e^{1-a}.
 \tag{11}
\]

Consequently

\[
 L_0=\max\left\{1,
 \frac{C_{m,d}A_P2^\kappa B_{d+\kappa-1}}{c\epsilon}\right\}
 \tag{12}
\]

is sufficient once the constants in (4) and (7) are supplied. The norm bound implies
\(-\epsilon P(g)\preceq E_L\preceq\epsilon P(g)\), proving (2).

Since \(V_L(x)/|x|\to\infty\) and all derivatives of \(p_L\) are bounded by \(p_L\) times powers of \(1+\log\rho\), all integrations by parts against exponentials are justified. They give (3), including total mass at \(g=0\).

Finally assume condition 3. For every nonzero vector \(v\), the nonnegative function
\(v^*P(-\partial)p_L(x)v\) has strictly positive integral \(v^*P(0)v\). Its integral against the strictly positive weight \(e^{g\cdot x}\) is therefore strictly positive. Equation (3), and the positive finite scalar Laplace transform of \(p_L\), imply \(v^*P(g)v>0\). This proves condition 1 and completes Theorem 1.

## 4. Faster tails when a polynomial margin is supplied

The same calculation gives a quantitative refinement. For \(\beta>0\), replace (1) by

\[
 f_\beta(z)=\frac{\rho(z)^{1+\beta}-1}{1+\beta},\qquad
 V_{L,\beta}(x)=Lf_\beta(x/L),\qquad
 p_{L,\beta}=Z_{L,\beta}^{-1}e^{-V_{L,\beta}}.
 \tag{13}
\]

Here \(|\nabla V_{L,\beta}|\le\rho^\beta\) and
\(D^jV_{L,\beta}=O_{m,j,\beta}(L^{1-j}\rho^{1+\beta-j})\).
For a partition with \(b\) blocks and \(r\) slots, the exponent of \(\rho\) is \(b(1+\beta)-r\). For a non-singleton partition this is at most \((r-1)\beta-1\). Therefore

\[
 \|E_{L,\beta}(x)\|
 \le\frac{C_{m,d,\beta}A_P}{L}
 \rho^{(d-1)\beta-1},
\]

and, under (4),

\[
 \frac{\|E_{L,\beta}(x)\|}{\lambda_{\min}P(\nabla V_{L,\beta}(x))}
 \le\frac{C_{m,d,\beta}A_P2^\kappa}{cL}
 \rho^{\beta(d+\kappa-1)-1}.
 \tag{14}
\]

**Corollary 3.** If

\[
 0<\beta\le\frac1{d+\kappa-1},
 \tag{15}
\]

then all sufficiently large \(L\) give the relative sandwich (2) with \(p_{L,\beta}\). The density has tails of the form
\(\exp[-\Theta(|x|^{1+\beta})]\).

This is a sufficient bound depending on a supplied algebraic margin. It is not claimed to be optimal for every individual polynomial. The next example shows that the endpoint can be sharp even for a scalar sum of two squares.

## 5. A strict sum of squares with a sharp 6/5 exponent

Consider

\[
 Q(s,t)=(st-1)^2+s^2
 =(1+t^2)\left(s-\frac{t}{1+t^2}\right)^2+\frac1{1+t^2}.
 \tag{16}
\]

Thus \(Q>0\), \(Q(0)=1\), and (4) holds with \(c=1\), \(\kappa=2\), \(d=4\). It has infimum zero, and Corollary 3 proves eventual positivity for (13) whenever \(0<\beta\le1/5\).

This endpoint is exact for this family. Fix \(L>0\). At a large physical radius \(r=|x|\), let \(q_r=|\nabla V_{L,\beta}(x)|\). Choose the angle of \(x\) so that

\[
 g=(g_1,g_2)=(t^{-1},t),\qquad
 t^2+t^{-2}=q_r^2,\qquad t\longrightarrow\infty.
 \tag{17}
\]

This is possible when \(q_r\ge\sqrt2\), since the radial gradient points in the direction of \(x\). One has
\(q_r\sim(r/L)^\beta\) and \(t\sim q_r\).

For a smooth potential \(V\), direct differentiation gives the exact identity

\[
\begin{aligned}
 \frac{Q(-\partial)e^{-V}}{e^{-V}}
 ={}&Q(g)-V_{11}(g_2^2+1)-V_{22}g_1^2
       +(2-4g_1g_2)V_{12}\\
 &+V_{11}V_{22}+2V_{12}^2
       +2g_2V_{112}+2g_1V_{122}-V_{1122}.
\end{aligned}
 \tag{18}
\]

On (17), radial differentiation yields

\[
 V_{11}\sim q_r/r\sim t/r,\quad
 V_{22}=O(t/r),\quad V_{12}=O((rt)^{-1}),
\]

and \(D^jV=O(t/r^{j-1})\) for \(j=3,4\). In particular, every error term in (18) other than \(-V_{11}t^2\) is \(o(t^3/r)\). For example, \(V_{11}V_{22}\) and \(tV_{112}\) are \(O(t^2/r^2)\), whose ratio to \(t^3/r\) tends to zero. Since \(Q(t^{-1},t)=t^{-2}\),

\[
 \frac{Q(-\partial)p_{L,\beta}}{p_{L,\beta}}
 =t^{-2}-\frac{t^3}{r}(1+o(1)).
 \tag{19}
\]

The ratio of the negative term to the positive term is

\[
 \frac{t^5}{r}\sim L^{-5\beta}r^{5\beta-1}.
 \tag{20}
\]

If \(\beta>1/5\), this tends to infinity, so the output is negative in the remote tails for every fixed \(L\). At \(\beta=1/5\), Corollary 3 supplies positivity for sufficiently large \(L\). Therefore, for (13) and this \(Q\), the largest possible tail exponent is exactly

\[
 1+\beta=6/5.
 \tag{21}
\]

This sharpness concerns the stated radial power-potential family; it is not a universal obstruction on every density with a comparable upper tail. No such larger statement is inferred.

There is also no fixed \(\beta>0\) that works for all strictly positive scalar polynomials after broadening. For
\(Q_k(s,t)=(st^k-1)^2+s^2\), evaluate on the spatial axis \(x_1=0,x_2=r\). Odd \(x_1\) derivatives vanish. With \(q_r=V'(r)\) and \(h_r=q_r/r\), one has \(\partial_1^2p=-h_rp\) on this axis. Repeated differentiation in \(r\), using \(q'_r/q_r^2=O((rq_r)^{-1})\), gives

\[
 \frac{Q_k(-\partial)p_{L,\beta}}{p_{L,\beta}}
 =1-\frac{q_r^{2k+1}}r(1+o(1)).
 \tag{22}
\]

It is negative eventually if \(\beta(2k+1)>1\). Every fixed positive \(\beta\) is defeated by some finite \(k\). Equation (22) is sufficient for this no-universal-power conclusion; no sharp exponent for every \(Q_k\) is claimed here.

## 6. Gaussian smoothing fails even for this sum of squares

For a nondegenerate Gaussian with precision matrix

\[
 H=\begin{pmatrix}a&b\\b&c\end{pmatrix}\succ0,
 \qquad V(x)=\tfrac12(x-\mu)^TH(x-\mu),
\]

the differential ratio is

\[
 \frac{Q(-\partial)p(x)}{p(x)}
 =\left[e^{-\frac12 H:\nabla_g^2}Q\right](g),
 \qquad g=H(x-\mu).
 \tag{23}
\]

The exponential terminates after its quadratic term. Its exact value is

\[
 Q(s,t)-a(t^2+1)-c s^2-4bst+2b+ac+2b^2.
 \tag{24}
\]

Along \(s=0\), the leading term is \(-at^2\). Since \(a>0\) and the Gaussian gradient covers all \(\mathbb R^2\), the output becomes negative. Neither covariance, rotation, nor mean can repair this example with a Gaussian.

Thus the fixed family in Theorem 1 is doing something a general Gaussian heat regularization cannot do. But the input polynomial is already an explicit sum of squares, so Gaussian failure is not evidence of overcoming the sum-of-squares obstruction.

## 7. A degree-two infinite-operator boundary

Finite coefficient dimension is essential for the automatic algebraic margin. On \(\ell^2(\mathbb N)\), define the bounded self-adjoint operator polynomial

\[
 P(g)=\operatorname{diag}_{n\ge1}
 \frac{(g-n)^2+e^{-2n^2}}{n^2+e^{-2n^2}}.
 \tag{25}
\]

Its degree is two and \(P(0)=I\). All three coefficient operators are bounded. For fixed \(g\), all sufficiently large \(n\) have \(|n-g|\ge n/2\), so the corresponding entries are at least \(1/8\). The finitely many remaining entries are strictly positive. Thus

\[
 P(g)\succeq\lambda_gI\quad\hbox{for some }\lambda_g>0
\]

at every finite real \(g\). Nevertheless

\[
 \lambda_{\min}P(n)\le\frac{e^{-2n^2}}{n^2+e^{-2n^2}},
 \tag{26}
\]

so no algebraic margin (4) exists.

Now use the one-dimensional canonical density (1), with any fixed \(L>0\). At the unique point \(x_n=Lz_n>0\) satisfying \(V_L'(x_n)=n\), its \(n\)-th output diagonal entry divided by \(p_L(x_n)\) is exactly

\[
 \frac{e^{-2n^2}-V_L''(x_n)}{n^2+e^{-2n^2}}.
 \tag{27}
\]

Here

\[
 f'(z)=\frac{z}{\rho}(1+\log\rho),\qquad
 f''(z)=\frac1\rho+\frac{\log\rho}{\rho^3},
\]

so \(z_n\sim e^{n-1}\) and \(V_L''(x_n)\sim e^{1-n}/L\). Equation (27) is negative for all sufficiently large \(n\). Hence **no member of the fixed family (1) regularizes (25)**, despite real-point coercivity at every finite tilt.

The general PR94 theorem, if taken as established, still supplies a margin-adapted regularizer for this polynomial distribution supported at zero. The example does not refute that theorem. It disproves the proposed dimension-independent extension of the fixed-template corollary and explains exactly where finite-dimensional real algebra enters.

## 8. Limits on the proposed noncommutative and PDE consequences

The commuting differential variables do not retain free commutators. For example, the Hermitian free polynomial

\[
 F(X,Y)=I+i(XY-YX)
\]

has commutative image \(1\), for which every scalar density is a positive differential certificate. But at \(X=\sigma_x,Y=\sigma_y\),

\[
 F(X,Y)=I-2\sigma_z
\]

has eigenvalue \(-1\). The construction therefore does not imply a free noncommutative positivity certificate. The all-matrix-size positivity-to-squares theorem is already due to Helton; current operator-coefficient versions have their own explicit all-size hypotheses. Sources inspected directly:

- Helton, *“Positive” noncommutative polynomials are sums of squares*, Annals of Mathematics 156 (2002), 675–694: https://annals.math.princeton.edu/2002/156-2/p09 .
- Jindal–Klep–McCullough, *Positive operator-valued noncommutative polynomials are squares*, Theorem 1.1, preprint v1 (2025): https://arxiv.org/html/2511.06487v1 . Its theorem requires positivity on every tuple of self-adjoint matrices of every size, and obtains operator-valued sums of squares. The one-square conclusion within the same coefficient algebra is additionally stated for infinite-dimensional coefficient Hilbert space; rectangular factorization expresses the general sum of squares as one square between different spaces.

Likewise, Theorem 1 chooses a positive source \(M=P(-\partial)p\). It does not solve the inverse PDE for a prescribed source, establish ellipticity, or make the inverse positivity-preserving. Already \(P(g)=1+g^2\) is strictly positive but \((1+\partial^2)E=\delta_0\) has no positive all-exponential probability-measure solution: its hypothetical Laplace transform would be \(1/(1+g^2)\), whose second derivative at zero is \(-2\), contradicting nonnegative second moment.

Finally, \(P(-\partial)p_L\succeq0\) is itself a global analytic condition. Without a supplied positivity margin or an acquired algebraic certificate, the formula is not a finite verified decision procedure. Finite sampling in \(x\) cannot certify the remote tails, as (19), (24), and (27) demonstrate.

## 9. What is established and what remains open

The exact finite-matrix equivalence, the uniform relative-error estimate, the margin-dependent power-tail refinement, the sharp \(6/5\) example, Gaussian failure, and the infinite-operator counterexample have complete arguments above. A small symbolic/numerical script checks the delicate finite identities; it does not certify the general theorem.

The proof uses the classical strict Positivstellensatz as a substantive premise. It does not establish a new solution to Hilbert's seventeenth problem, a new free positivity theorem, an efficient positivity test, or an exact positive Green operator. The strongest defensible opportunity is a fixed-form analytic representation theorem and a quantitative bridge from polynomial lower margins to permissible density tails.

Historical priority for this exact formulation remains unresolved. The narrow searches performed did not locate the fixed-template statement; failure to locate it is not evidence of novelty. The proposed polynomial application should be presented as a sharpened corollary of established algebra plus an explicit analytic argument, unless further priority work establishes otherwise.

## 10. Source pin and reproducibility

The PR94 cone proof was read at commit `df8e6dac844f1832e79cea6cd40d0915307b12bb`, path `updates/FT-foundational-capability-v2-20261015/package/workers/mathematical_invention/PROOF.md`, and copied without modification to `sources/PR94_CONE_PROOF.md` in this worker packet. `SOURCE_RECEIPTS.json` records the pin, hashes, supplied attachment, and acquired primary webpages.

Only this worker directory was written. No GitHub, shared-worktree, or other-worker content was modified. The artifact is independent of other workers' conclusions.
