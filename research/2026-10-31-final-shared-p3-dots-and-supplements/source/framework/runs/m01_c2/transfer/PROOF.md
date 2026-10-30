# Positive rank-one Hessian quadrature for the exceptional quartic

This is a post-comparison source-transfer construction, separate from the frozen continuation. The unrestricted QC of P0 and of the full exceptional face remains open. The new result controls a genuinely different family of compatible fields, including overlapping resonances and arbitrarily many separated blocks, for **every globally ROC polynomial in the actual eight-cubic exceptional face**.

Write

\[
F=|w|^4+2|z|^2|w|^2=3F_{1/3},\qquad |A|^2=(|z|^2+|w|^2)/2.
\]

The supplied checkpoint proves that every globally ROC polynomial with leading F has cubic in

\[
\mathcal V=\operatorname{span}\{F_x,F_y,F_u,F_v,
 x(u^2-v^2),2xuv,y(u^2-v^2),2yuv\}. \tag{1}
\]

We use precisely this exceptional space, not the generic translation theorem or Ultra's different twelve-dimensional cubic space.

## 1. The transferred identity and the fixed-polynomial matching problem

The authorized Ultra proof supplies the following principle. For an actual compatible mean-zero gradient G, suppose positive weights wi and actual rank-one matrices Ri match its covariance, and actual matrices Ai satisfy

\[
\sum_iw_iDC(R_i)\cdot A_i=\langle C(G)\rangle.
\]

Then for p=F+C+Q+affine,

\[
\langle p(G)\rangle-p(0)=f-E+\frac12\sum_iw_i p''(A_i)[R_i,R_i],\quad
E=\frac12\sum_iw_iA_i^TF''(R_i)A_i. \tag{2}
\]

The source's F*, rays and numerical certificates are not used here. They would not establish (2)'s feasibility or budget for F.

### 1.1. Exactly five conditions suffice for the fixed P0 at every mean

Put C0=Re(conj(z)w²), gi=DC0(Ri), Hi=F''(Ri), and let the covariance-matching decomposition be fixed. For an actual G set

\[
H=\langle F''(G)\rangle,\quad v=\langle DF(G)\rangle,
w=\langle DC_0(G)\rangle,\quad c=\langle C_0(G)\rangle.
\]

Every mean M is handled if, in addition to the single cubic equality, one matches the four translation moments:

\[
\sum_iw_iH_iA_i=v,\qquad \sum_iw_ig_i\cdot A_i=c. \tag{3}
\]

No other lower cubic need be matched for this fixed-polynomial claim. Indeed expansion of p''(M+Ai) in (2), with (3), gives the exact all-mean identity

\[
\langle p(M+G)\rangle-p(M)=f-E+
\frac12\sum_iw_i p''(M+A_i)[R_i,R_i]. \tag{4}
\]

This uses the actual translated quadratic of p, not a replacement stabilization.

There is a finite explicit minimum-cost construction for (3). Admissibility gives gi in range Hi. Define

\[
\tau=\sum_iw_i g_i^TH_i^+g_i,\quad
K=\begin{pmatrix}H&w\\w^T&\tau\end{pmatrix},\quad b=(v,c).
\]

If b lies in range K, take (lambda,mu)=K⁺b and

\[
A_i=\lambda+\mu H_i^+g_i. \tag{5}
\]

These matrices satisfy (3), with the exact minimum

\[
E_{\min}=\tfrac12 b^TK^+b. \tag{6}
\]

The proof is ordinary weighted least squares in the Hi seminorms: the two sums in (3) are K(lambda,mu), while the cost is one half of (lambda,mu)ᵀK(lambda,mu). Orthogonality to the homogeneous constraint kernel proves minimality. Range failure or E_min>f obstructs that chosen decomposition, not QC itself. This is a finite quadrature construction; Ai are not asserted to form a gradient or to be a pointwise correction selector.

For the triad below, `construct.py` derives the actual five-condition optimum

\[
E_{\min}=\kappa^2\frac{2ABD(A+B+2D)}{2AB+D(A+B)}\le\kappa^2D(A+B). \tag{7}
\]

Thus fixed P0 is not obstructed by unnecessary matching of every other cubic. A simpler construction below happens to match all eight cubics at the same sufficient budget; it earns a stronger theorem.

## 2. Three original rays suffice for the actual exceptional face

Let

\[
\phi=a e_1\sin(x+\theta_0)+b e_2\sin(y+\theta_1)
+d(e_1+e_2)\sin(x+y+\theta_2),\quad G=D\phi.
\tag{8}
\]

Use the physical rank-one rays E11,E22 and the all-ones matrix. Their (x,y,u,v) vectors are

\[
R_0=(1,0,1,0),\ R_1=(1,0,-1,0),\ R_2=(2,0,0,2).
\]

Set A=a²,B=b²,D=d², S=A+B, kappa=cos(theta0+theta1-theta2). The covariance weights are A/2,B/2,D/2. Take the **literal constant matrices**

\[
X_0=(0,0,-1/4,0),\quad X_1=(0,0,1/4,0),\quad X_2=0. \tag{9}
\]

For every C in the actual space (1), exact differentiation gives

\[
\sum_{i=0}^2DC(R_i)\cdot X_i=\ell(C),\qquad
\langle C(G)\rangle=abd\kappa\ell(C). \tag{10}
\]

In the ordered basis (1), the complete row of values is

\[
\ell=(-4,0,0,0,-1,0,0,0). \tag{11}
\]

`receive.py` reconstructs each entry directly from F and the eight cubics. In particular no full-rank assumption about a feature map is imported from Ultra. Its original-three-ray obstruction was for a different twelve-cubic space; here (9) solves every required target exactly without a covariance exchange.

For nonzero amplitudes define

\[
A_i=abd\kappa X_i/w_i. \tag{12}
\]

These are three explicit actual matrices. They match (10), and hence apply to any actual cubic in the exceptional ROC face. Also

\[
X_0^TH_0X_0=X_1^TH_1X_1=1,\quad X_2^TH_2X_2=0,
\qquad E=\kappa^2D(A+B). \tag{13}
\]

The compatible quartic and radial moments are reconstructed exactly:

\[
f=\frac{9A^2+4AB+48AD+9B^2+48BD+144D^2}{8},
\]

\[
h=\langle|G|^4\rangle=
\frac{3A^2+4AB+24AD+3B^2+24BD+48D^2}{8}. \tag{14}
\]

The whole amplitude-and-phase budget has a short identity:

\[
f-E-2h=\frac{(S-8D)^2}{16}+2D^2+
\frac{5(A-B)^2}{16}+(1-\kappa^2)DS\ge0. \tag{15}
\]

Combining (2), ROC, and (15) proves

\[
\boxed{\langle p(M+D\phi)\rangle-p(M)\ge
2c\langle|D\phi|^4\rangle} \tag{16}
\]

for **every** globally ROC p with leading cF,c>0, its actual admissible cubic and actual quadratic, every mean M, every real a,b,d and every phase. Nonzero amplitudes were used only to display (12); zero amplitudes follow by continuity. Scaling p by 1/c gives the stated leading-coefficient factor. Argument translation keeps its cubic in (1), so all means follow from the same verified matching, not a presumed translation-only normal form.

Common proper output rotation is also allowed: F is left-rotation invariant, and p(OA) is again globally ROC with leading cF and cubic in (1). Apply (16) to that polynomial and mean OᵀM. Thus rotations need not preserve the particular P0 cubic.

This is not the frozen characteristic-polarized family. The three rays in (8) have nonzero sharp residual. For P0 and a=b=d=1, the actual Schur correlation is r=-4/7, verified exactly in `receive.py`; the theorem controls an active correlation.

## 3. A genuine overlapping four-wave block

Consider the actual map

\[
\psi=e_1\sin x+e_2\sin y+(e_1+e_2)\sin(x+y-\delta_1)
+(1/2,1/4)\sin(2x+y-\delta_1-\delta_2). \tag{17}
\]

Its fourth ray is R3=(5/4,0,3/4,1) in conformal coordinates. All four covariance weights are 1/2. There are two cubic resonances, 0+1=2 and 0+2=3, and two non-pairwise quartets, 2k0+k1=k3 and k1+k3=2k2. The quartets must be retained.

For y=0 fields, the last two cubics in (1) have zero moments and are matched by backgrounds with y=0. It suffices here to solve the four translation features and C1=x(u²-v²),C2=2xuv. This is used to prove a full-eight-cubic conclusion, rather than imposed on the earlier fixed-P0 problem.

Let gi be the 4-by-2 matrix with columns DC1(Ri),DC2(Ri), Hi=F''(Ri), and form the literal rational Gram matrix

\[
K=\sum_{i=0}^3\frac12
\begin{pmatrix}H_i&g_i\\g_i^T&g_i^TH_i^+g_i\end{pmatrix}.
\]

The two target columns, reconstructed by exact Fourier convolution, are

\[
T=\begin{pmatrix}-4&7\\0&0\\0&12\\0&12\\-1&-1/4\\0&3\end{pmatrix}.
\]

Set U=K⁻¹T and

\[
B_i=U_{1:4,:}+H_i^+g_iU_{5:6,:},\qquad
A_i=\cos\delta_1\,B_{i,1}+\cos\delta_2\,B_{i,2}. \tag{18}
\]

All matrices in (18) are finite literal rational matrices; `overlap.py` constructs and saves them in `overlap_exact.txt`. It verifies the two targets for **all eight cubics** and directly reconstructs their cost matrix, rather than assuming (18) works:

\[
E=(\cos\delta_1,\cos\delta_2)
\begin{pmatrix}21940/14549&-9477/14549\\
-9477/14549&249169/58196\end{pmatrix}
\binom{\cos\delta_1}{\cos\delta_2}. \tag{19}
\]

Exact Fourier convolution gives

\[
f=132473/2048-(11/8)\cos(\delta_1+\delta_2)
+(7/2)\cos(\delta_1-\delta_2),
\]

\[
h=\langle|D\psi|^4\rangle=51155/2048+(1/8)\cos(\delta_1+\delta_2)
+(11/4)\cos(\delta_1-\delta_2). \tag{20}
\]

Thus, uniformly over both phases,

\[
f-E\ge1570767021/29796352,\quad h\le57043/2048,
\quad\frac{1570767021}{29796352}>\frac32\frac{57043}{2048}.
\]

The same quadrature identity proves

\[
\boxed{\langle p(M+\rho D\psi)\rangle-p(M)\ge
\tfrac32c\langle|\rho D\psi|^4\rangle} \tag{21}
\]

for both phases, every mean, every real overall amplitude, every common proper output rotation, and every globally ROC p with leading cF. The four relative amplitudes in (17) are fixed. Scaling uses weights rho²/2 and backgrounds rho Ai. The other two wave phases are removed by domain translation. No arbitrary-amplitude four-wave claim is made.

## 4. An unbounded number of blocks, with a uniform constant

The new F has an especially strong cross inequality. Normalize rank-one R=(a,b) and S=(d,e) so each conformal component has unit norm. Put s=a·d,t=b·e. Both physical matrix norms equal one, and

\[
F''(R)[S,S]=12+8t^2+16st,\qquad
(|\cdot|^4)''(R)[S,S]=4+2(s+t)^2.
\]

Their difference is

\[
6(s+t)^2+8(1-s^2)\ge0. \tag{22}
\]

By scaling, **the F cross-Hessian dominates the radial quartic cross-Hessian on every pair of actual rank-one matrices**. This is derived for F; Ultra's numerical cross constants are not imported.

Take any finite collection of blocks of types (8) and (17), with independent parameters allowed by their theorems and independent proper output rotations. Put them at scales L_j=9^j, dividing each potential amplitude by L_j, so their gradient amplitudes stay fixed. Every base frequency has integer components of size at most two. A nonzero sum of frequencies from the largest block has a component of size at least L_j, while four lower frequencies have components at most 8L_{j-1}<L_j. Hence mixed relations of length at most four reduce to one opposite pair in each of two blocks. A largest-block internal three-term resonance cannot leave a nonzero single lower frequency to cancel.

Quadratic and cubic moments therefore add blockwise. The only mixed quartic term between blocks i,j is

\[
\tfrac12\operatorname{Tr}(\langle F''(G_i)\rangle\langle G_jG_j^T\rangle).
\]

Each covariance is a positive sum of actual rank-one Fourier outer products. Inequality (22) therefore says that this mixed F term dominates the corresponding mixed radial quartic term. Each individual block already has budget at least c times its radial moment, by (16) or (21). Adding the blocks gives

\[
\boxed{\langle p(M+G)\rangle-p(M)\ge c\langle|G|^4\rangle}, \tag{23}
\]

independently of the finite number of blocks. The mixed cancellation argument applies also after translating p by M; no lower-degree cross term is lost. For original task normalization, the leading part is F/3, so c=1/3 in (16),(21),(23).

## 5. Verification and remaining scope

Run with bytecode writes disabled:

```
PYTHONDONTWRITEBYTECODE=1 python3 receive.py
PYTHONDONTWRITEBYTECODE=1 python3 overlap.py
PYTHONDONTWRITEBYTECODE=1 python3 verify_identity.py
```

The first receiver verifies the actual eight-mode matching, both quartic moments, the exact sum-of-squares budget, cross domination, and r=-4/7 for P0. The second reconstructs every phase coefficient, both cubic targets, literal backgrounds, their directly evaluated cost, and the uniform overlap budget. The third reconstructs the actual rational-phase periodic energy of P0 at a nonzero rational mean and checks its exact equality to the budget plus three positive rank-one Hessian scores. `construct.py` and `full_face.py` retain the five-condition and six-feature minimum-cost calculations as additional artifacts.

This extends the frozen characteristic-triad result to a different all-amplitude family, all eight admissible cubics and every actual ROC quadratic, a genuine two-resonance overlap, and unbounded separated copies. The general QC of P0 remains unproved. Arbitrary field geometry, arbitrary relative amplitudes of the four-wave block, and unrestricted overlapping resonance networks are not covered or asserted dense. No compatible negative-energy field was obtained. A finite test list is not being promoted to global QC.

The abstract positive Hessian quadrature, overlap pattern and separated-block method are credited to the two authorized Ultra source proofs. The exact F0 rays, simple three-ray matching, budgets, fixed-polynomial reduction, overlap coefficients and cross domination above were derived and verified here. Ultra's F*, twelve modes and certificates were not transferred as facts about F0. Homogeneous QC, normal form and P0 ROC admission retain their frozen packet/checkpoint credits. No outside sources, sibling post-comparison work, services or memory were consulted.
