# Compatible certificates and a sharp rank-one exceptional subfamily

All statements use the checkpoint normalization

\[
 z=x+iy=(a+d)+i(c-b),\qquad w=u+iv=(a-d)+i(c+b),
 \quad r=|z|^2,\quad t=|w|^2,\quad F=t^2+2rt.
\]

The present polynomial is P=3p, where p is in the original task normalization. The checkpoint's unique translation reduction and its exact full ROC criterion are taken as earned facts. The constructions below concern the remaining cubic, and do not assume its quasiconvexity.

## 1. Results

Let

\[
 P=F+z_{\mathbb R}^{T}M\nu(w)+Q,\qquad
 \nu(w)=(u^2-v^2,2uv),
\]

with real (2\times2) matrix (M). Then the following are sufficient for quasiconvexity at **every** background matrix and for actual compatible gradient fields:

\[
 Q(a,b)\ \geq\ \frac{\|M\|_F^2}{4}
 \quad (|a|=|b|=1).                                      \tag{1}
\]

A useful improvement of (1) is given in Section 5. In particular, if (Q=\alpha r+\beta t), condition (1) is

\[
 \alpha+\beta\geq\frac{\sigma_1^2+\sigma_2^2}{4}.         \tag{2}
\]

Here (sigma_1\geq\sigma_2) are the singular values of (M). The supplied sharp ROC condition for this quadratic is

\[
 \alpha+\beta\geq\frac{2\sigma_1^2+\sigma_2^2}{8}.         \tag{3}
\]

Consequently **(3) is also the sharp QC threshold whenever (\operatorname{rank}M\leq1)**. This resolves an actual nontranslation exceptional subfamily at its complete isotropic lower-quadratic boundary. The coefficients (\alpha,\beta) themselves may have either sign; only their sum matters, because (r-t=4\det A) is a null Lagrangian.

For the conformal cubic (M=I), the stronger construction proves QC when

\[
 Q=\lambda(r+t),\qquad
 \lambda\geq\lambda_H:=\frac{3+\sqrt3}{24}
          =0.197168783648\ldots.                         \tag{4}
\]

The checkpoint's boundary is (\lambda=3/16=0.1875). The interval between these numbers remains unproved. No sharp QC threshold for full-rank (M) or general admitted (Q) is asserted.

## 2. Complex Hessian variables retain compatibility

For a real two-component potential (f=(f^1,f^2)), let

\[
 h=(f^1_{11},f^1_{12},f^1_{22},f^2_{11},f^2_{12},f^2_{22}).
\]

Define complex variables

\[
\begin{aligned}
 A&=h_0-h_2+2h_4+i(h_3-h_5-2h_1),\\
 B&=h_0+h_2+i(h_3+h_5),\\
 C&=h_0-h_2-2h_4+i(h_3-h_5+2h_1).
\end{aligned}                                           \tag{5}
\]

They are four times the three Wirtinger second derivatives of the complex potential. In real conformal coordinates the derivatives of the gradient are exactly

\[
 X=(h_0+h_4,h_3-h_1,h_0-h_4,h_3+h_1),
 \quad Y=(h_1+h_5,h_4-h_2,h_1-h_5,h_4+h_2).              \tag{6}
\]

In particular the argument never substitutes an arbitrary pair (X,Y) for an actual Hessian.

For a polynomial one-form (\eta) on matrix space, use the sign convention

\[
 \mathcal B_P=P''[X,X]+P''[Y,Y]
          +X^T(D\eta^T-D\eta)Y.                         \tag{7}
\]

The last term is the pullback of a closed exact two-form (up to the harmless fixed sign convention). Its integral over a periodic compatible field is zero.

## 3. A universal three-square identity

Set

\[
 C_+=x(u^2-v^2)+2yuv=\Re(\bar z w^2),\qquad
 C_-=x(u^2-v^2)-2yuv=\Re(z w^2).
\]

Let (a,b) be arbitrary real scalars, and put

\[
 P=F+aC_++bC_-+\frac{a^2+b^2}{4}(r+t),\quad
 \lambda=(a^2+b^2)/4.
\]

The following vectors are coefficients of real one-forms:

\[
 a_z=(-y,x,0,0),\quad a_w=(0,0,-v,u),
\]
\[
 \Pi_+=(0,0,xv-yu,xu+yv),\quad
 \Pi_-=(0,0,xv+yu,xu-yv).
\]

Choose

\[
 \eta=(2r+4t-2\lambda)a_z+(4r+2t-6\lambda)a_w
                    -4a\Pi_+-4b\Pi_-.                 \tag{8}
\]

Define the three complex linear-in-Hessian forms

\[
 S=zB+2wA,\qquad
 U=\bar zA+\bar wB+w\bar C,\qquad
 V=z\bar B+2\bar wB.
\]

Direct coefficient expansion gives the exact identity

\[
 \boxed{\quad \mathcal B_P
    =|S+b\bar C|^2+2|U|^2+|V+aC|^2.\quad}             \tag{9}
\]

This is the main construction. Its right side is nonnegative for every actual matrix and Hessian. `verify_certificate.py` independently builds (6), differentiates (P) and (8), and checks every coefficient of (9), with symbolic (a,b). It is not a finite sampling check.

To see why this proves QC, evolve an actual periodic test potential by the componentwise heat equation. Differentiating its integral energy and integrating by parts gives

\[
 \frac{d}{ds}\int P(A_0+D f_s)
       =-\int\sum_{i=1}^2 D^2P(A_0+Df_s)[\partial_iDf_s,\partial_iDf_s]
       =-\int\mathcal B_P\leq0.
\]

The exact-form term has zero integral by Stokes. At infinite time the mean-zero periodic perturbation tends smoothly to zero; hence the limiting energy is the energy of (A_0). This proves the required inequality for every (A_0). Compactly supported smooth tests embed in a periodic cell; approximation supplies the usual bounded-gradient test class. This uses precisely the compatible heat mechanism credited in the packet to Bruno--Pasqualotto, Appendix A, with the new lower-order primitive (8) and new square identity (9).

## 4. Arbitrary real M, and the exact rank-one consequence

Identify a real matrix (M=(m_{ij})) with the complex real-linear map

\[
 M\xi=\mu\xi+\nu\bar\xi,\quad
 \mu=\frac{m_{11}+m_{22}+i(m_{21}-m_{12})}{2},\quad
 \nu=\frac{m_{11}-m_{22}+i(m_{21}+m_{12})}{2}.
\]

Its cubic is

\[
 \Re\{\mu\bar z w^2+\bar\nu z w^2\}.
\]

Independent phase rotations of (z,w) arise from actual proper output and domain rotations of matrices. The two phase equations allow both coefficients to be made nonnegative real simultaneously. Thus (9) applies with

\[
 a=|\mu|,\quad b=|\nu|,\qquad a^2+b^2=\|M\|_F^2/2.
\]

QC is preserved by these actual rotations. Equation (9) therefore proves QC of

\[
 F+z_{\mathbb R}^TM\nu(w)+\frac{\|M\|_F^2}{8}(r+t).
\]

If (1) holds, the remaining quadratic (R=Q-\|M\|_F^2(r+t)/8) is rank-one convex. Every quadratic rank-one convex integrand is QC: expand a real periodic gradient in Fourier modes and apply (R(q\otimes k)\geq0) to each real sine and cosine amplitude. Adding this compatible inequality proves the stated general-Q sufficient region.

For rank-one (M), (a=b=\sigma_1/2). Formula (9) reaches (lambda=\sigma_1^2/8), or (alpha+\beta=\sigma_1^2/4), exactly (3). Necessity follows from QC implying ROC. Thus the isotropic-quadratic threshold in this rank-one subfamily is completely resolved, including equality, not just a large positive stabilization.

## 5. A tunable certificate and improved conformal bound

Write

\[
 T=(\bar zA+2\bar wB,\ z\bar B+2w\bar C,\ z\bar B+2\bar wB)^T.
\]

For (0<p<1), define

\[
 G_p=\begin{pmatrix}
 1+p&p&-p\\p&1/2&1/2-p\\-p&1/2-p&3/2
 \end{pmatrix},\qquad
 f(p)=\frac{2p+1}{1+4p-2p^2}.
\]

The leading principal minors are

\[
 1+p,\quad (1-p)(2p+1)/2,\quad
 (1-p)(1+4p-2p^2)/2,
\]

so (G_p\) is positive definite. Also (e_3^TG_p^{-1}e_3=f(p)). Replacing the leading part of (8) by

\[
 \eta_F=((1+p)r+(8p-4)t)a_z+(4r+2t)a_w
\]

gives the exact leading identity

\[
 \mathcal B_F=p|S|^2+T^*G_pT.
\]

The same cubic primitives give the cross score

\[
 2\Re\{aT_3\bar C+bSC\}.
\]

Keep the quadratic primitive (-2\lambda a_z-6\lambda a_w). Its corrected score is (4\lambda|C|^2). Completing both squares proves QC whenever

\[
 \boxed{\quad
 \lambda\geq\Lambda_p(a,b):=
 \frac14\left(a^2\frac{2p+1}{1+4p-2p^2}+\frac{b^2}{p}\right),
 \quad0<p<1.\quad}                                    \tag{10}
\]

The endpoint (p=1) is exactly (9), with threshold ((a^2+b^2)/4). Thus (10), or its minimum over one real parameter, gives a computable improved sufficient region for every (M), and for every (Q) with (Q(a_0,b_0)\geq2\Lambda_p(a,b)) on the two unit circles. No optimality among all QC certificates is claimed.

For (b=0,a=1), (f(p)) has its minimum at (p=(\sqrt3-1)/2). The value is ((3+\sqrt3)/6), giving (4). At this parameter an exact completion uses

\[
 G_p^{-1}e_3=(1/3,-(1+\sqrt3)/6,(3+\sqrt3)/6)^T.
\]

The radical certificate is checked independently by the receiver. The construction has not reached (3/16); its proven gap is ((2\sqrt3-3)/48\).

## 6. Remaining scope and unsuccessful attacks

The universal ROC-implies-QC question remains open. Even rank-one (M) with an arbitrary quadratic admitted by the checkpoint criterion is not classified by this proof. For full-rank (M=I), the original sharp-boundary (P_0) is still unproved QC.

A local Fourier search used actual two-component trigonometric potentials, analytically eliminated the background and scalar amplitude, and sought both an energy violation and a negative integrated heat derivative. Twenty thousand random fields followed by local optimization approached the rank-one threshold from below (best integrated-heat required coefficient about 0.18748165, with the comparison energy coefficient about 0.18747821). No violation was found. These finite diagnostics are not positive QC evidence beyond their individual fields. `fourier_search.py` and its small output archive preserve the failed attack.

A coarse finite supporting-minor search at the improved conformal coefficient found no non-polyconvexity witness. This is not a polyconvexity proof; no polyconvex status for the newly certified members is asserted. The checkpoint's non-PC boundary example is not silently promoted to a QC example.

The exact ROC classifier, exceptional cubic normal form, and polynomial-heat obstruction at (P_0) remain the checkpoint's results. Homogeneous QC and the heat/Stokes mechanism remain the packet's credited input. The square identities, sharp rank-one isotropic QC theorem, and sufficient bounds (1), (10) are the present construction, without an external historical-priority claim.
