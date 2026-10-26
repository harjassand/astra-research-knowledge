# Binary classical channel comparison is stable under arbitrary quantum conditioning

26 October 2026. Derived in Q28 stage 1. This is a self-contained candidate mathematical result. Priority is not established by the literature search. The ordinary scalar relative-entropy/Fisher-information comparison is antecedent; the step being constructed here is its extension to arbitrary noncommuting quantum reference states.

## 1. Claim and exact domain

Let `K=(k_yx)` and `L=(l_zx)` be any two finite-output classical stochastic channels with input alphabet `{0,1}`. Columns sum to one. Drop output rows that are identically zero. For `0<t<1`, write

\[
w_y(t)=k_{y1}+(k_{y0}-k_{y1})t,\qquad
G_K(t)=\sum_y\frac{(k_{y0}-k_{y1})^2}{w_y(t)}.
\]

Define `G_L` analogously. Suppose `L` has unequal columns, so `G_L(t)>0` in the open interval. Then the least constant `c` for which

\[
J_K(\rho,\sigma)\leq c J_L(\rho,\sigma) \tag{1}
\]

holds for **every finite-dimensional quantum reference R and every pair of classical-quantum states**

\[
\rho=|0\rangle\langle0|\otimes A_\rho+|1\rangle\langle1|\otimes B_\rho,
\quad \sigma=|0\rangle\langle0|\otimes A_\sigma+|1\rangle\langle1|\otimes B_\sigma
\]

is exactly

\[
\boxed{c=\sup_{0<t<1}G_K(t)/G_L(t).} \tag{2}
\]

Here

\[
J_K(\rho,\sigma)=D((K\otimes\mathrm{id})(\rho)\Vert(K\otimes\mathrm{id})(\sigma))
-D(\rho_R\Vert\sigma_R),
\]

using Umegaki relative entropy and initially finite divergences. Reference marginals need not agree. The theorem includes their equal-marginal restriction: with `L=id`, the optimal complete and conditional coefficients both equal the ordinary classical KL coefficient. It does **not** assert an equality for three or more input labels, coherent quantum input channels without a classical measurement boundary, arbitrary multi-matrix conditional expectations, or a fixed baseline state.

## 2. BKM representation from first principles

For a positive definite matrix `C`, define positive self-adjoint superoperators on the Hilbert-Schmidt space

\[
\mathcal L_C(H)=CH,\qquad \mathcal R_C(H)=HC,
\qquad T_u(C)=u\mathcal L_C+(1-u)\mathcal R_C.
\]

The Hessian of `Tr C log C` is

\[
g_C(H)=\int_0^1\langle H,T_u(C)^{-1}H\rangle_{HS}\,du. \tag{3}
\]

To verify (3), diagonalize C with eigenvalues `c_i`. The coefficient of `|H_ij|²` on the right is

\[
\int_0^1\frac{du}{u c_i+(1-u)c_j}
=\frac{\log c_i-\log c_j}{c_i-c_j},
\]

with continuous value `1/c_i` when the eigenvalues coincide. This is precisely the divided difference of the logarithm obtained by differentiating `Tr C log C` twice.

## 3. The binary operator identity

Fix positive definite input reference blocks A,B, and Hermitian tangents H_0,H_1. Put M=A+B and H=H_0+H_1. For each `u in [0,1]`, set

\[
X=T_u(A),\quad Y=T_u(B),\quad Z=X+Y=T_u(M),\quad
Q=Z^{-1/2}XZ^{-1/2}.
\]

Then `0<Q<I`, and `Z^{-1/2}YZ^{-1/2}=I-Q`. This automatic commutativity after congruence is the special binary step; no commutativity of A and B is assumed. View matrices H_i as Hilbert-Schmidt vectors and define

\[
v=Z^{-1/2}H,\quad a=Z^{-1/2}H_0,\quad r=a-Qv.
\]

For output y, let `delta_y=k_y0-k_y1` and

\[
W_y=k_{y1}I+\delta_y Q.
\]

Linearity gives

\[
T_u(k_{y0}A+k_{y1}B)=Z^{1/2}W_yZ^{1/2},
\quad Z^{-1/2}(k_{y0}H_0+k_{y1}H_1)=W_yv+\delta_y r.
\]

Because `sum_y W_y=I` and `sum_y delta_y=0`, direct expansion yields the exact identity

\[
\sum_y\langle W_yv+\delta_y r,W_y^{-1}(W_yv+\delta_y r)\rangle
-\langle v,v\rangle
=\langle r,G_K(Q)r\rangle. \tag{4}
\]

All inverses in (4) exist for nonzero output rows and positive definite A,B. The cross terms cancel because their coefficient sums to zero. The `v` quadratic terms sum to `||v||²`. The remaining terms are exactly `sum_y delta_y² W_y^{-1}`.

For L the same Q,v,r occur. By the definition of c in (2), scalar functional calculus gives `G_K(Q)<=c G_L(Q)`. Integrating (4) over u and applying (3) proves the Hessian inequality

\[
\sum_y g_{k_{y0}A+k_{y1}B}(k_{y0}H_0+k_{y1}H_1)-g_M(H)
\le c\left[\sum_z g_{l_{z0}A+l_{z1}B}(l_{z0}H_0+l_{z1}H_1)-g_M(H)\right]. \tag{5}
\]

## 4. Integration to relative entropy

Let

\[
F_K(A,B)=\sum_y\operatorname{Tr}(k_{y0}A+k_{y1}B)\log(k_{y0}A+k_{y1}B)
-\operatorname{Tr}(A+B)\log(A+B).
\]

Its Bregman divergence is exactly `J_K`, since the output blocks sum to M and the linear trace terms cancel. Along the affine path from sigma to rho, Taylor's integral identity expresses `J_K` as the integral of its Hessian with nonnegative weight `1-s`, `0<=s<=1`. Integrating (5) proves (1) for faithful pairs.

For non-faithful pairs with finite relative entropies, replace both states by `(1-epsilon)` times themselves plus `epsilon` times the same faithful classical-quantum state. Apply (1) and let epsilon decrease to zero. Relative entropy converges to its finite value in this common regularization, so both conditional divergences converge as well. Cases with an infinite right-hand side are vacuous. No claim uses an undefined infinity-minus-infinity difference.

## 5. Sharpness and strongest ordinary comparator

Take R to be one-dimensional, input sigma `(t,1-t)` and rho `(t+h,1-t-h)`. Scalar Taylor expansion gives

\[
\lim_{h\to0}\frac{D(K\rho\Vert K\sigma)}{D(L\rho\Vert L\sigma)}=G_K(t)/G_L(t).
\]

Taking t toward a supremum proves necessity of c. Thus ordinary scalar distributions already attain every needed sharpness limit. Quantum reference engineering cannot improve this coefficient in the stated binary classical channel class.

For `L=id`, `G_L(t)=1/[t(1-t)]`, so

\[
\eta_D^\Delta(K)=\eta_D^c(K)=\eta_{KL}(K)
=\sup_{0<t<1}t(1-t)G_K(t). \tag{6}
\]

The same scalar witness has equal reference marginals automatically.

## 6. Conditional mutual information and arbitrarily large product registers

The same constant gives the sharp operational comparison

\[
I(U:Y\mid R)\leq c I(U:Z\mid R) \tag{7}
\]

for every finite-dimensional quantum U,R and every state with a classical binary X, with Y=K(X), Z=L(X). To see this directly, apply (1) with reference system UR to the compared states `rho_XUR` and `sigma_XUR=(I_U/d_U) tensor rho_XR`. Their output conditional divergence is

\[
D(\rho_{YUR}\Vert I_U/d_U\otimes\rho_{YR})
-D(\rho_{UR}\Vert I_U/d_U\otimes\rho_R)=I(U:Y\mid R).
\]

The L expression gives the right side. Ordinary classical auxiliary U already supplies sharpness: let a rare U=1 select one scalar hypothesis and U=0 select the other; as its probability goes to zero, the mutual-information ratio tends to their relative-entropy ratio. Therefore quantum U,R cannot improve the best binary classical comparison coefficient.

If `G_Ki(t)<=G_Li(t)` for every t and each i, then for **every finite n**, every arbitrarily correlated classical input string `X_1...X_n`, and every quantum R,

\[
J_{K_1\otimes\cdots\otimes K_n}(\rho,\sigma)
\le J_{L_1\otimes\cdots\otimes L_n}(\rho,\sigma). \tag{8}
\]

Replace the channels one at a time. At each replacement, all other outputs together with R form the reference system; the same reference-divergence term appears on the two sides and cancels. Summing the n inequalities proves (8). This is the usual complete less-noisy tensorization argument, now applicable from the scalar binary certificates. It is **not** the generally false assertion that an unrestricted product-channel contraction coefficient is the largest single-use coefficient.

These consequences extend the quantifier scope beyond a single favorable fixture. The general conditional-contraction/CMI framework and the tensorization technique are antecedents; the constructed step is the dimension-uniform binary lifting in Sections 2–5.

## 7. Binary-output closed form and biased-reset counterexample

For `K=[[a,b],[1-a,1-b]]`, `0<a,b<1`, algebraic maximization of (6) gives

\[
\eta_D^\Delta(K)=\left(\sqrt{a(1-b)}-\sqrt{b(1-a)}\right)^2. \tag{9}
\]

To verify the maximization without assuming it, set `x=t/(1-t)>0`. Then the quantity to maximize is

\[
\frac{(a-b)^2x}{(ax+b)((1-a)x+1-b)}.
\]

For `a!=b`, its derivative vanishes at

\[
x_*=\sqrt{\frac{b(1-b)}{a(1-a)}}.
\]

The derivative changes from positive to negative there. Substitution gives (9); the formula extends to endpoints by continuity. If `a=b`, the coefficient is zero.

For a biased binary reset with `p=(1/4,3/4)` and retention `lambda=1/2`, `a=5/8`, `b=1/8`, so the exact coefficient is

\[
\boxed{\eta=(19-\sqrt{105})/32\approx0.2735327885637626.} \tag{10}
\]

The complete order index of the reset expectation on the weighted commutative algebra is `C=1/min(p_i)=4`: for positive reference blocks Z_i, the density expectation domination reduces to `Z_i<=C p_i sum_j Z_j`; necessity is obtained by supporting all mass on the rare label. Here the Heisenberg expectation preserves the weighted trace with weights p, and its preadjoint is the stochastic state reset to p. The transplanted full-matrix formula would give `(C-1)lambda²/[1+(C-2)lambda]=3/8`. Equations (9) and (10) prove that transplant false. This is **outside** N967's stated full-matrix domain and does not refute N967.

## 8. A proved boundary check at three input labels

For the n-symbol uniform classical reset `K=lambda id+b 11^T`, `b=(1-lambda)/n`, the ordinary scalar coefficient is

\[
c_{\rm scalar}=\frac{\lambda^2}{\lambda+2b}. \tag{11}
\]

Here is an elementary check of the scalar upper bound, so the negative control does not rely on a guessed incumbent. At input probability p and a zero-sum tangent x, the desired Fisher inequality reduces to

\[
\sum_i\frac{2p_i-1}{p_i(\lambda p_i+b)}x_i^2\leq0.
\]

If all p_i are at most 1/2 this is immediate. Otherwise only p_1 exceeds 1/2. Put `s=1-p_1<1/2` and `f(t)=t(lambda t+b)/(1-2t)` on `[0,1/2)`. Since `f(t)/t` is increasing, `sum_{i>1}f(p_i)<=f(s)<=p_1(lambda p_1+b)/(2p_1-1)`. Weighted Cauchy-Schwarz applied to `sum_{i>1}x_i=-x_1` then proves the displayed inequality. Boundary probabilities follow by limits. Equality is approached at p=(1/2,1/2,0,...), with tangent on the first two symbols. Affine-path integration gives the global KL coefficient (11).

At n=3, lambda=1/2, (11) is 3/10. The **pre-existing** N967 regular-simplex construction on a three-dimensional reference has the exact BKM quotient

\[
\frac13\frac{\log(1+3(1-\epsilon)(3/4)/\epsilon)}{\log(1+3(1-\epsilon)/\epsilon)}.
\]

At epsilon=1/100 this is `(1/3)log(895/4)/log(298)>3/10`, since the exact integer inequality `895^10>4^10 298^9` holds. Its value is about 0.31656665. Nearby faithful hypotheses with equal reference marginals realize this local ratio in the relative-entropy limit. Thus the analogue of our binary equality is actually false for a three-label classical channel with quantum conditioning. The code reproduces both the matrix metric ratio and a finite nearby-hypothesis ratio. The witness and its asymptotic value are credited to N967; the calculation is a scope check, not an invented improvement.

## 9. Consequence and limits

Every finite-output binary classical channel comparison in relative entropy can be certified against arbitrary quantum conditioning using a one-variable rational inequality. This includes asymmetric reset and readout channels, and all comparisons among BSC/BEC/asymmetric finite-output mechanisms. It supplies a bridge from established scalar comparison to a noncommuting-reference guarantee; it does not improve the ordinary scalar optimum.

For an ordinary binary projective measurement followed by K, data processing through the measurement gives the same upper coefficient on arbitrary coherent input states. If both measurement outcomes have nonzero subspaces, mixtures of one vector in each subspace supply the scalar lower witness, so the coefficient is again exact. This uses the measurement boundary explicitly; it is not a theorem for arbitrary coherent quantum memories.

This is a complete mathematical construction with a general quantifier scope. Historical priority and independent audit remain unresolved. It is not evidence of a civilisation-changing physical or computational capability, a working hardware operation, or a resource advantage over the strongest ordinary method.

## Primary antecedents

- Hirche, George, Nuradha and Wilde, *Conditional contraction coefficients and their applications to quantum networks*, arXiv:2608.27171v1 (2026): https://arxiv.org/html/2608.27171v1 . Conditional contraction/CMI framework is pre-existing.
- Makur and Polyanskiy, *Comparison of Channels: Criteria for Domination by a Symmetric Channel*, IEEE TIT 64 (2018), 5704–5725: https://arxiv.org/abs/1609.06877 ; https://doi.org/10.1109/TIT.2018.2839743 . Scalar KL/chi-square channel ordering is pre-existing.
- Hirche, Rouze and Stilck Franca, *On contraction coefficients, partial orders and approximation of capacities for quantum channels*: https://arxiv.org/html/2011.05949v3 . Quantum metric/relative-entropy comparison and channel orders are pre-existing.
- Public N967 proof at frozen knowledge commit 0aecbbdb1fa289741c1f1ed96366610d13d37486, saved locally in `sources/N967_governing.md`: https://raw.githubusercontent.com/harjassand/astra-research-knowledge/0aecbbdb1fa289741c1f1ed96366610d13d37486/research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-25-dots-ultra-selected-sources/source/dots/general_inclusion_sharpness.md . Full-matrix sharp reset law and the reference-simplex construction are pre-existing.
