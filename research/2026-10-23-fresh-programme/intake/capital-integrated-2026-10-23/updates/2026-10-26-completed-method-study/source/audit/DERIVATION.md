# Independent mathematical reconstruction of Q28 stage 2

This is an audit of the frozen `review_material/Q28/stage2/finite_reference_proof.md`, not a modification of it. Statements labelled “independent refinement” below are not credited to the submitted result. All channels use the column-stochastic convention. Zero output rows are removed. All reference spaces here are finite. The coefficient is defined by the least nonnegative universal comparison constant; consequently 0/0 witnesses impose no condition and the coefficient of two discard channels is 0.

## 1. Reconstructing the upper implication

For positive classical–quantum blocks $A=(A_i)$, define

\[
\Phi_K(A)=\sum_y\operatorname{Tr}[(KA)_y\log (KA)_y]
             -\operatorname{Tr}[M\log M],\qquad M=\sum_iA_i.
\]

The Bregman divergence of this function is exactly $J_K(\rho,\sigma)$: the linear trace terms cancel between the joint and marginal terms. Along $A(t)=\sigma+t(\rho-\sigma)$,

\[
J_K(\rho,\sigma)=\int_0^1(1-t)\left[\sum_y g_{(KA(t))_y}((KH)_y)-g_{M(t)}(H_R)\right]dt.
\]

To verify the required BKM formula directly, diagonalize a positive $A$. On the matrix unit $E_{ab}$, $sL_A+(1-s)R_A$ has eigenvalue $s\lambda_a+(1-s)\lambda_b$. Its inverse integrates to

\[
\int_0^1\frac{ds}{s\lambda_a+(1-s)\lambda_b}
=\frac{\log\lambda_a-\log\lambda_b}{\lambda_a-\lambda_b},
\]

with the continuous value $1/\lambda_a$ for coincident eigenvalues. These are exactly the Hessian coefficients of $\operatorname{Tr}A\log A$. Neither simultaneous diagonalization of the different $A_i$ nor commutativity with the tangents is assumed.

Fix $t,s$, set $Z=T_s(M)$, $Q_i=Z^{-1/2}T_s(A_i)Z^{-1/2}$, $a_i=Z^{-1/2}H_i$, and $v=\sum_i a_i$. Here $Q_i$ act on a complex Hilbert–Schmidt space; they are strictly positive and sum to identity. Congruence transforms each output inverse exactly. Set $u_i=a_i-Q_i v$. For a channel $K$,

\[
\sum_y(v_y+W_yv)^*W_y^{-1}(v_y+W_yv)
=F_K+2\operatorname{Re}\big[(\sum_yv_y)^*v\big]+v^*(\sum_yW_y)v
=F_K+\|v\|^2.
\]

This proves the submitted gauge identity with the same $Q,u$ for both channels. There is no Hermiticity restriction missing from the free domain: allowing complex vectors is an upper relaxation here, and the reverse construction below realizes every such vector. A universal free inequality $F_K\le cF_L$ can therefore be integrated in $s$ and $t$, giving $J_K\le cJ_L$.

For a pair whose input blocks are singular, add the same faithful cq state to both hypotheses with mixing weight $\eta$. For any finite relative-entropy term, joint convexity gives an upper limit bounded by the original value, and lower semicontinuity gives the matching lower limit. Apply this separately to both output terms and to the reference term before subtracting. The original input relative entropy need not be finite. No difference of two infinite numbers is taken.

## 2. Compression and the quantifiers

For any nonzero free witness, let $S$ contain all $u_i$ and all $x_y=W_y^{-1}v_y$ for both channels. The $u_i$ have one linear dependence, so

\[
1\le\dim S\le n-1+m_K+m_L=d_*.
\]

For $P=P_S$, $Q'_i=PQ_iP|_S>0$, and $\sum_iQ'_i=I_S$. Each $v_y\in S$ and $x_y\in S$, whence $PW_yP x_y=v_y$. Thus the compressed inverse really returns $x_y$; this is equality, not an appeal to a generally false commutation of compression and inversion. Both $F_K,F_L$ are preserved exactly. If every $u_i=0$, both forms are zero and the witness can be discarded or put in dimension 1.

Compression applies separately to each witness; it need not compress an original pair of states, its whole BKM integral, or its relative entropies. Since it preserves each numerator/denominator pair, it is sufficient to replace the supremum over all finite dimensions by $1\le d\le d_*$. Nonattainment and singular limits do not change this argument.

## 3. Reverse implication, including zero denominators

Given any free witness $Q,u$, choose any strictly positive distribution $p$, add one vacuum direction, and put

\[
\sigma_i^\epsilon=\frac{1-\epsilon}{d}Q_i\oplus\epsilon p_i,
\qquad H_i=\begin{pmatrix}0&u_i\\u_i^*&0\end{pmatrix}.
\]

The submitted normalization is correct: the total trace is 1; each tangent has trace zero; and $\sum_iH_i=0$ exactly. The Schur complement gives the submitted positivity radius

\[
t^2<\min_{u_i\ne0}\frac{\epsilon p_i(1-\epsilon)}{d\,u_i^*Q_i^{-1}u_i}.
\]

At output $y$, diagonalize $W_y$ with eigenvalues $w_j>0$. Let $z$ be $v_y$ in this eigenbasis and $q_y=\sum_i k_{yi}p_i>0$. Direct calculation gives

\[
g_y=2\sum_j|z_j|^2\frac{\log((1-\epsilon)w_j/d)-\log(\epsilon q_y)}{(1-\epsilon)w_j/d-\epsilon q_y},
\qquad
\frac{g_y}{2d\log(1/\epsilon)}\longrightarrow\sum_j\frac{|z_j|^2}{w_j}.
\]

This verifies the factor $2d$, all complex conjugations, and the claimed limit. To avoid any denominator ambiguity, fix a proposed finite $c$ and a witness with $F_K-cF_L>0$. The scaled metric difference is positive for some sufficiently small $\epsilon$; the relative-entropy difference is then positive for sufficiently small nonzero $t$, because its leading term is $t^2/2$ times that metric difference. This constructs an equal-marginal counterexample to $c$ in reference dimension $d+1\le d_*+1$.

If $F_L=0<F_K$, positivity of the inverses forces every $L$-output tangent to be zero. The two constructed $L$ outputs are then identical for every admissible $t$, so this case gives an actual $J_L=0<J_K$ pair. If the supremum is infinite only through increasing finite ratios, the preceding positive-difference argument works for each finite $c$. Thus the quantifier order is correct in both cases.

A concrete test of the latter distinction is $K=I_2$, $L=\left(\begin{smallmatrix}3/4&1/4\\1/4&3/4\end{smallmatrix}\right)$, with scalar $Q=(t,1-t)$, $u=(1,-1)$. Here $F_K/F_L=1+3/[4t(1-t)]\to\infty$, although $L$ is invertible and $F_L>0$ for every nonzero zero-sum tangent. No claim that infinity must have an exact kernel witness is being made.

Writing $\alpha$ for the free supremum, the complete chain is

\[
\alpha\le C_{eq}^{\dim R\le d_*+1}
\le C_{cond}^{\dim R\le d_*+1}
\le C_{cond}^{all\ finite\ R}\le\alpha.
\]

This proves all equalities and the stated sufficient reference bound. It also checks that the bound concerns the coefficient, not exact attainment at a faithful optimizer.

For the rate bound, each spectral component divided by its limiting value equals
$(1+\ell/\log(1/\epsilon))/(1-h)$, where
$h=\epsilon(1+dq_y/w)$,
$\ell=\log((1-\epsilon)w/(dq_y))$.
For the submitted $\delta,B$, $0\le h\le\delta<1$ and $|\ell|\le B$ when $\epsilon\le1/2$. Subtracting 1 and taking absolute values proves (7). The bound applies to a fixed strictly positive witness, not uniformly over all witnesses. The division formula is interpreted continuously if two eigenvalues coincide; the bound's $\delta<1$ assumption avoids that coincidence in the part where it is used.

## 4. Algebraicity and decidability

For each of finitely many dimensions $d\le d_*$, write Hermitian $Q_i$, vectors $u_i$, and Hermitian inverse variables $X_y$ in real and imaginary coordinates. Strict positivity is expressible by positive leading principal minors. The conditions $\sum_iQ_i=I$, $\sum_i u_i=0$, and $W_yX_y=I$ are polynomial equations over the rational channel entries. Output inverses exist because every output row is nonzero. The free inequality becomes a real polynomial inequality with these variables.

Real quantifier elimination therefore applies to the threshold statement. Its set of valid nonnegative thresholds is an intersection of closed upper rays, hence either empty or $[C,\infty)$. It is semialgebraic over $\mathbb Q$; a finite boundary point of such a one-dimensional set is algebraic. This also covers $C=0$ and permits an in-principle decision for the existence of any finite threshold. This is a correct consequence of the proved reduction. Neither the submitted work nor this audit executes general quantifier elimination or establishes useful complexity bounds.

The independent exact binary check gives a concrete illustration. For

\[
K=\begin{pmatrix}1/5&2/5\\4/5&3/5\end{pmatrix},\quad
L=\begin{pmatrix}1/5&3/5\\4/5&2/5\end{pmatrix},
\]

spectral calculus of $Q_1,I-Q_1$ reduces the full coefficient to the scalar ratio
$(2t^2-t-3)/(2t^2+2t-12)$. Checking its stationary points and boundary limits gives
$C=29/50-3\sqrt6/25$, the smaller root of $100C^2-116C+25=0$, attained in the scalar optimization at $t=3-\sqrt6$. This is an independently calculated example, not a claim that the trial executed a general optimizer.

## 5. Strong ordinary comparator and the known reset controls

When all $Q_i$ commute, a common eigenbasis splits each form into a sum of scalar Fisher forms. Their comparison coefficient is the ordinary classical KL/Fisher coefficient: a ratio of sums cannot exceed the largest scalar ratio, and a scalar witness is already allowed. For $n=2$, $Q_2=I-Q_1$, so this conclusion covers the entire free domain. For $n\ge3$, simultaneous diagonalization is unavailable.

The supplied reset controls can also be checked analytically without treating a random maximum as an upper bound. For $K_\lambda=\lambda I+(1-\lambda)\mathbf1\mathbf1^T/n$, $L=I$, set $a=(1-\lambda)/n$, $x_i=Q_i^{-1/2}u_i$, $V=[Q_1^{1/2}\ \cdots\ Q_n^{1/2}]$. Then $VV^*=I$, $Vx=0$, and, for $B=\operatorname{diag}(Q_i)$,

\[
F_K=\lambda^2 x^*f(B)x,\quad F_I=\|x\|^2,
\qquad f(t)=\frac{t}{\lambda t+a}.
\]

Let $P=I-V^*V$. Its block diagonal part is $I-B$. The elementary pinching inequality $P\le n\operatorname{diag}(P)$, applied to $Px=x$, implies $x^*Bx/\|x\|^2\le(n-1)/n$. Concavity and monotonicity of the scalar $f$, applied to the spectral distribution of $B$ in $x$, give

\[
F_K/F_I\le\frac{(n-1)\lambda^2}{1+(n-2)\lambda}.
\]

Regular-simplex rank-one $Q_i$, approximated by strictly positive $Q_i$, and $u_i$ the simplex vectors attain the limit. In the scalar restriction, the corresponding compressed diagonal matrix has the same nonzero spectrum as $\operatorname{diag}(q)-qq^T$, whose largest eigenvalue is at most 1/2 by Gershgorin's row bound $2q_i(1-q_i)\le1/2$. The same concavity argument gives the exact ordinary coefficient $\lambda^2/[\lambda+2(1-\lambda)/n]$, approached by two input masses $1/2,1/2$. Thus at $\lambda=1/2$ the known full values $1/3,3/8,2/5$ and ordinary values $3/10,1/3,5/14$ are consistent and distinct. The endpoints $\lambda=0,1$ follow directly. These are checks of supplied antecedent controls, not new discoveries.

## 6. Independent refinement, not an original-trial claim

The submitted dimension bound is conservative. Let $S$ contain the $u_i$ and only the $K$-inverse vectors. This has dimension at most $n-1+m_K$. It preserves $F_K$, while for each $L$ output,

\[
v^*(PWP|_S)^{-1}v\le v^*W^{-1}v.
\]

One proof uses $v^*W^{-1}v=\sup_z[2\operatorname{Re}v^*z-z^*Wz]$: restricting $z$ to $S$ can only decrease this supremum. Consequently the ratio cannot decrease. This independently sharpens the coefficient witness bound to active dimension $n-1+m_K$, reference dimension $n+m_K$. It is not needed to repair any submitted step, is not credited to the frozen output, and does not imply a practical efficient optimizer. The independent script checks its preservation/monotonicity numerically on 15 sparse cases.

## Outcome of the mathematical audit

All three principal claims—free formula, equality of the conditional/equal-marginal coefficients with the stated finite reference bound, and rational-channel algebraicity/decidability in principle—survive independent reconstruction at their stated scope. No critical missing step or analytic counterexample was found. The original theorem requires no repair. Historical originality, practical advantage, coherent quantum-channel extensions, and the original broad physical capability are separate matters not established by this proof.
