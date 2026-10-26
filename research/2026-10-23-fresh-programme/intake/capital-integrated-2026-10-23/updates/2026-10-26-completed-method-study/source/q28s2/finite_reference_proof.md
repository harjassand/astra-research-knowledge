# Finite reference reduction for every finite classical channel comparison

26 October 2026, Q28 stage 2. Stage 1 is unchanged. This is a candidate mathematical construction, not an established priority claim or an independent audit.

## 1. Result

Let K,L be classical stochastic matrices with the same n-element input alphabet, n>=2, and respectively m_K,m_L nonzero output rows. For a classical-quantum pair rho,sigma with arbitrary finite reference R, define

\[
J_K(\rho,\sigma)=D((K\otimes id_R)\rho\Vert(K\otimes id_R)\sigma)-D(\rho_R\Vert\sigma_R).
\]

Only finite differences are used; infinity minus infinity is not defined. Let C_cond(K,L) be the least nonnegative constant in `J_K<=C J_L` over all such pairs and references. Let C_eq(K,L) restrict the same comparison to equal reference marginals. If the comparison fails on a pair with J_L=0<J_K, the coefficient is infinite.

Put

\[
d_* = n-1+m_K+m_L.
\]

For positive definite operators Q_1,...,Q_n on C^d with `sum_i Q_i=I`, and vectors u_i in C^d with `sum_i u_i=0`, define

\[
W_y^K=\sum_i k_{yi}Q_i,\quad v_y^K=\sum_i k_{yi}u_i,\quad
F_K(Q,u)=\sum_y\langle v_y^K,(W_y^K)^{-1}v_y^K\rangle.
\]

The same definitions apply to L. Define the supremum with zero-denominator convention as above. Then

\[
\boxed{C_{cond}(K,L)=C_{eq}(K,L)=
\sup_{1\le d\le d_*}\ \sup_{Q_i>0,\ \sum Q_i=I,\ \sum u_i=0}
\frac{F_K(Q,u)}{F_L(Q,u)}.} \tag{1}
\]

Moreover the coefficients on the left are unchanged if references are restricted to

\[
\boxed{\dim R\le d_*+1=n+m_K+m_L.} \tag{2}
\]

The bound is sufficient, not minimal. Extremizers need not be attained and may require ill-conditioned faithful states. Neither polynomial running time nor uniformly favorable precision is asserted.

This extends the binary construction to all finite classical alphabets. It also proves that complete and conditional relative-entropy **comparison** coefficients coincide for classical channels, even though quantum conditioning can exceed the ordinary scalar coefficient when n>=3. It does not prove equality for arbitrary coherent quantum channels or fixed-baseline SDPI constants.

If a classical channel is represented as a quantum CPTP map that first dephases its input basis and then applies its stochastic matrix, arbitrary coherent input hypotheses have the same outputs and reference marginals as their dephased versions. Thus the same comparison theorem applies in that representation. Both compared channels must share this explicit classical input boundary.

## 2. Upper bound: the conditional BKM metric becomes a positive-operator quadratic form

At faithful input reference blocks A_i>0, with Hermitian tangents H_i, put M=sum_i A_i and H=sum_i H_i. For s in [0,1], let

\[
T_s(A)=s L_A+(1-s)R_A,\quad Z=T_s(M),\quad
Q_i=Z^{-1/2}T_s(A_i)Z^{-1/2},\quad a_i=Z^{-1/2}H_i,\quad v=\sum_i a_i.
\]

Operators act on the Hilbert-Schmidt space, while H_i and a_i are vectors in that space. Each Q_i is positive definite and sum_i Q_i=I. The input matrices A_i need not commute. The standard BKM representation, directly verified by logarithmic divided differences in stage 1, is

\[
g_A(H)=\int_0^1\langle H,T_s(A)^{-1}H\rangle\,ds.
\]

The integrand of the conditional output Hessian is therefore

\[
\mathcal F_K(Q,a)=\sum_y\left\langle\sum_i k_{yi}a_i,
(\sum_i k_{yi}Q_i)^{-1}\sum_i k_{yi}a_i\right\rangle-\langle v,v\rangle. \tag{3}
\]

There is an exact gauge identity. Set `u_i=a_i-Q_i v`; then sum_i u_i=0. For each output, `sum_i k_yi a_i=v_y^K+W_y^K v`. Expanding the squares, using sum_y W_y^K=I and sum_y v_y^K=sum_i u_i=0, gives

\[
\mathcal F_K(Q,a)=F_K(Q,u). \tag{4}
\]

The same gauge, Q_i and u_i work simultaneously for K and L. Thus a universal free quadratic inequality `F_K<=c F_L` implies the conditional Hessian inequality at every faithful state and tangent. Integrate first in s, and then along the affine path from sigma to rho with nonnegative Taylor weight 1-t. Since the resulting Bregman divergence is J_K, this proves the relative-entropy inequality for every finite reference.

For non-faithful finite-divergence pairs, mix both hypotheses with the same faithful classical-quantum state and pass to the common-mixture limit. This is the same legitimate finite-dimensional support regularization as in stage 1. No infinite-minus-infinite expression enters.

## 3. Exact witness compression

Consider any finite dimension d, positive Q_i and zero-sum u_i. Let S be the span of

\[
\{u_i:1\le i\le n\}\ \cup
\{(W_y^K)^{-1}v_y^K:1\le y\le m_K\}\ \cup
\{(W_z^L)^{-1}v_z^L:1\le z\le m_L\}.
\]

The first collection spans at most n-1 dimensions because sum_i u_i=0. Hence dim S<=d_*. Let P be the projection onto S, and compress `Q_i` to `Q_i'=P Q_i P|_S`. They remain positive definite on S and sum to I_S. All u_i lie in S.

For any listed output, x=(W_y^K)^{-1}v_y^K lies in S by construction. Therefore

\[
(P W_y^K P)|_S x=P W_y^K x=v_y^K.
\]

By invertibility of the compressed positive operator, its inverse applied to v_y^K is exactly x. Thus each inverse quadratic term is preserved, for both K and L, not merely bounded. This proves

\[
F_K(Q',u)=F_K(Q,u),\qquad F_L(Q',u)=F_L(Q,u). \tag{5}
\]

Every possible quadratic witness therefore has one in dimension at most d_*. The reduction does not assume that a maximizer exists.

## 4. Lower bound: every free witness is realizable by faithful equal-marginal states

Fix a compressed witness on C^d, d<=d_*, and any strictly positive input probability vector p. Let the reference be `R=C^d direct_sum C|0>`. For epsilon in (0,1), define faithful reference blocks

\[
\sigma_i^{\epsilon}=\frac{1-\epsilon}{d}Q_i\ \oplus\ \epsilon p_i,
\quad H_i=\begin{pmatrix}0&u_i\\u_i^*&0\end{pmatrix}.
\]

Their total trace is one. Since sum_i u_i=0, sum_i H_i=0. For sufficiently small real t, rho_i=sigma_i^epsilon+t H_i remains positive definite, and the hypotheses have **exactly equal** reference marginals. This supplies the missing operation as an explicit state construction, rather than assuming a favorable input family.

There is an explicit admissible step, rather than an unknown positivity assumption. By the Schur complement, it suffices to choose

\[
|t|<\min_{i:u_i\ne0}\sqrt{\frac{\epsilon p_i(1-\epsilon)}{d\,\langle u_i,Q_i^{-1}u_i\rangle}}.
\]

Taking half that quantity is a concrete faithful construction.

At output y, the active block is `(1-epsilon)W_y^K/d`, the vacuum weight is `epsilon q_y` with q_y=sum_i k_yi p_i>0, and the off-diagonal tangent is v_y^K. The eigenvalue divided-difference formula gives

\[
\lim_{\epsilon\downarrow0}\frac{g_{\sigma_y^{\epsilon,K}}(H_y^K)}{2d\log(1/\epsilon)}
=\langle v_y^K,(W_y^K)^{-1}v_y^K\rangle. \tag{6}
\]

Indeed every active eigenvalue tends to a fixed positive number while the vacuum eigenvalue is epsilon q_y; divide its logarithmic divided difference by log(1/epsilon). This finite spectral calculation proves (6) without assuming an unknown convergence sign or favorable rate.

First let t go to zero, obtaining the local relative-entropy ratio. Then let epsilon decrease to zero. Equations (6) and its L analogue realize F_K/F_L. A positive numerator and exactly zero L tangent gives a genuine no-finite-coefficient witness. Thus the free supremum is bounded above by C_eq with reference dimension at most d_*+1.

The convergence is explicitly logarithmic and need not be practically favorable. For a fixed free witness, let w_min,w_max bound the eigenvalues of all W_y for one channel and let q_y=sum_i k_yi p_i>0. Define

\[
\delta=\max_y\epsilon(1+d q_y/w_{\min}),\qquad
B=\log 2+\max_{y,w\in\{w_{\min},w_{\max}\}}|\log(w/(d q_y))|.
\]

For epsilon<=1/2 and delta<1, direct substitution into the divided difference proves

\[
\left|\frac{\sum_y g_{\sigma_y^{\epsilon,K}}(H_y^K)}{2d\log(1/\epsilon)}-F_K\right|
\leq \frac{\delta+B/\log(1/\epsilon)}{1-\delta}\,F_K. \tag{7}
\]

Indeed each eigencomponent is its limiting weight times `(1+ell/log(1/epsilon))/(1-h)`, where `h=epsilon(1+d q_y/w)` and `ell=log((1-epsilon)w/(d q_y))`; `|ell|<=B` and `h<=delta`. Apply the same bound to L to obtain an explicit ratio bound whenever its relative error bound is less than one. This controls a **fixed supplied witness**. It does not supply a uniformly well-conditioned optimizer or a cheap way to acquire one.

Together with `C_eq<=C_cond` and the upper bound, this proves (1) and (2). It also identifies why arbitrary changes in the reference marginal provide no extra comparison power for classical channels: the gauge in (4) converts them to a zero-sum off-diagonal witness.

## 5. Strongest conventional comparator and the binary check

The governing BKM/relative-entropy optimization, conditional-contraction/CMI framework, complete channel ordering, operator inverse quadratic forms, and linear-algebra compression are established tools. This work does not invent them. The construction combines them to obtain the explicit classical-channel free formula and finite reference bound.

For n=2, u_1=-u_2 and Q_2=I-Q_1. Then F_K is the quadratic form of G_K(Q_1), with the same scalar G_K as stage 1. Spectral calculus reduces (1) exactly to `sup_t G_K(t)/G_L(t)`. Thus the stage 1 theorem survives the strongest full-reference stress as a corollary, without relying on its favorable finite examples.

For n>=3 the Q_i can fail to commute. The scalar conventional comparator restricts Q_i to commuting operators (and thus decomposes into scalar ordinary channel comparisons). The new representation retains their noncommutativity explicitly; it does not assert that ordinary scalar optimization has failed when no global scalar bound is available.

For rational channels and rational candidate c, the finite-dimensional inequality can, in principle, be expressed with finitely many real polynomial equations and inequalities: introduce inverse variables for each W, impose W X=I and positive principal minors, and quantify over Q_i,u_i. Real quantifier elimination is an existing decision method. Consequently the all-reference comparison in this classical subclass admits a finite exact decision formulation. This is a computability consequence, **not** a practical polynomial-time algorithm or an executed global optimization of the resulting high-dimensional problem.

There is a further precise consequence: when K,L have rational entries, their finite coefficient in (1) is a real algebraic number. To prove this, split complex entries into real and imaginary parts and introduce inverse variables as above. The set of admissible thresholds

\[
\{c\ge0:\ \forall Q,u\ \ F_K(Q,u)\le cF_L(Q,u)\}
\]

is semialgebraic over the rationals by real quantifier elimination. It is either empty (no finite coefficient) or the ray `[C,infinity)`. A finite boundary point of a semialgebraic set defined over the rationals is real algebraic. Existing quantifier-elimination and real-root isolation methods therefore give an exact computability statement for this coefficient, including a decision for any rational threshold. This proof does not supply an efficient complexity bound. Collins' established decision method is being used, not invented here.

## 6. Sources, novelty and scope

- Hirche, George, Nuradha and Wilde, arXiv:2608.27171v1, https://arxiv.org/html/2608.27171v1 , gives the conditional-contraction framework, CMI equivalence and existing complete-order machinery. Its discussion identifies potentially unbounded references as a difficulty; it asks about complete-versus-conditional separation for faithful divergences in general. The present theorem concerns classical channels only and does not settle that general quantum question.
- Hirche, Rouze and Stilck Franca, arXiv:2011.05949v3, https://arxiv.org/html/2011.05949v3 , gives prior quantum metric/relative-entropy comparison and channel-order tools.
- Makur and Polyanskiy, arXiv:1609.06877v3, https://arxiv.org/html/1609.06877v3 , supplies the strong ordinary classical KL/chi-square comparison antecedent.
- Collins, *Quantifier elimination for real closed fields by cylindrical algebraic decomposition* (1975), https://doi.org/10.1007/3-540-07407-4_17 ; publisher primary text https://link.springer.com/content/pdf/10.1007/3-540-07407-4_17.pdf , supplies the pre-existing real-algebraic decision method used in the computability corollary.
- Public N967 at frozen commit 0aecbbdb1fa289741c1f1ed96366610d13d37486, source saved unchanged in stage1/sources/N967_governing.md, supplies the uniform-reset simplex witness and full-matrix index law used as a known control, not a new invention.

No priority conclusion follows from not finding this exact statement in a targeted search. The proof is a completed self-contained candidate unit, not independently audited. It supplies no physical measurements, better memory recovery cycle, general coherent-channel theorem, or demonstrated practical advantage. The original civilisation-changing capability mission remains NOT_ACHIEVED.
