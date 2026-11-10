# Independent substantive theorem review

9 November 2026. Independent mathematical reconstruction of the stated theorem and complete proof. This reader edition preserves the mathematical analysis and verdict.

## Verdict

PASS at the precise stated scope. I found no mathematical defect in the upper-triangular pointwise support or its left-QR adapted-all-mean consequence. The complete original-density polynomial, the positive affine metric, every coefficient/Gram payment, the quantitative reserve, and the function-space argument are paid below.

The result concerns k=r=1 and perturbations phi=L_A grad psi, with L_A depending on the affine mean through a left target rotation. It does NOT prove quasiconvexity for arbitrary compatible vector gradients, the same fixed Hessian multiplier at every mean, or any other r. This report does not certify historical novelty.

Governing reviewed source SHA256: 70867bc2137841c0005f8876d073f1396149dbe09fc7ddd0a3619c143d86afaa. The standalone reader edition is THEOREM_AND_PROOF.md. It expands the inherited diagonal-block bounds without changing the theorem or any coefficient.

## 1. Independent original-density reconstruction

I reconstructed J_1 directly from

    u=a^2+c^2, v=b^2+d^2, j=ad-bc,
    J_1=(u-v+2j)^2/8+uv/2+j^2.

I then substituted A=[[alpha,beta],[0,delta]], X=[[x,2V],[-4V,y]], subtracted J_1(A), DJ_1(A):X, and the proposed multiplier

    (alpha^2-beta^2-delta^2+7alpha delta)(xy+8V^2)/2.

The resulting polynomial is exactly a^T Q a+c dot a+J_X, in a=(alpha,delta,beta), with every Q,c,J_X coefficient as printed in the candidate. The independent source does not import or execute the author's construction script.

The first two principal affine coordinates have

    Q11=(3x^2+4xy+7y^2)/4+5T>0

at every nonzero (x,y,T>=0), and

    det Q_first2=24T^2+(22x^2-7xy+28y^2)T/2+Pdet/16,
    Pdet=12(x^2-y^2-13xy/12)^2+(251/12)x^2y^2.

The quadratic coefficient is positive definite; Pdet vanishes only at x=y=0. Thus this principal block is positive definite. This was rederived directly, not taken on trust from the separate diagonal theorem.

The complete det Q and det M expansions in the candidate agree exactly with the independently reconstructed matrices. In particular the fourth row is c/2,J_X with no missing factor of two.

## 2. Positive affine metric

The T^2 coefficient in det Q is a positive definite quadratic. For its T coefficient,

    220|x^3y|<=100x^4+121x^2y^2,
    80|xy^3|<=40x^2y^2+40y^4

are exact weighted square inequalities. Subtraction gives the printed lower bound 28x^4+64x^2y^2+84y^4. The constant coefficient is (x^2+y^2)Pdet/64 and is positive when (x,y)!=0. At x=y=0, T>0, det Q=552T^3>0. Together with the leading principal block, this proves Q positive definite at every nonzero actual perturbation.

## 3. Every Schur coefficient payment

For P2 the positive diagonal coefficients and 4*4406*6516>3339^2 prove positivity.

For P4, the exact integer comparison is

    4*2000*3206-5064^2=3904>0.

The second stated Young inequality is immediate. The resulting coefficients 2176,5155,5498 are correct and strictly positive.

For P6,

    4*600*629-1228^2=1616>0.

The other two Young bounds are direct squares. The surviving coefficients 360,884,3297,424 are correct and positive. Signs of x,y are unrestricted because all odd terms were priced by absolute values.

For P8 I independently expanded the displayed rational Gram on (x^4,x^3y,x^2y^2,xy^3,y^4); it is exactly P8. Reorder the basis into its left pair, right pair, and central monomial. The two pair blocks are positive definite, with determinants 1392 and 5624. The exact central costs are respectively 3400/29 and 100920/703. The remaining scalar is

    570-3400/29-100920/703=6303710/20387>0.

Thus the whole Gram is positive definite. Its monomial vector is nonzero whenever (x,y)!=0, proving strict positivity of P8.

The constant coefficient P0 is reconstructed by the printed SOS. With D=x^2-y^2, K=xy, the last square forces K=0 at a zero; the first then forces D=0, hence x=y=0. The SOS therefore pays positivity without a root search or a discriminant assumption.

All coefficient forms in det M are positive for nonzero (x,y). Since T=V^2>=0, det M>0 whenever (x,y,V) is not zero. When x=y=0,V!=0, the leading term 14832T^5 is strictly positive. Q positive definite and det M>0 imply a strictly positive scalar Schur complement, so the complete 4x4 M is positive definite. In particular (alpha,delta,beta,1) M (alpha,delta,beta,1)^T is strictly positive for every nonzero H.

## 4. Quantitative reserve, independently paid

The candidate's coarse denominator is correct. Here is a direct bound that does not rely on the signed-coefficient parts of the earlier diagonal proof.

Set S=x^2+y^2 and Z=S+T. Let A0=D^2+KD/4-K^2. Then

    S^2<=8|A0|/7+37K^2/7.

Indeed |KD|/4<=(D^2+K^2)/8, and S^2=D^2+4K^2. Weighted Cauchy applied to the first and last P0 squares gives

    S^4 <=(16851/5488)[4A0^2+(112/11)K^4] <6P0.

Therefore det M>=S^5/3072+14832T^5>=(S+T)^5/49152, using (S+T)^5<=16(S^5+T^5).

For the upper bound on det Q, its T^2 coefficient is at most (887/2)S, its T coefficient is at most (777/16)S^2, and its constant coefficient is at most (135/256)S^3. The last bound follows from Pdet=12D^2-26DK+35K^2 and |D|<=S, |K|<=S/2. Each is safely below the corresponding coefficient of 552(S+T)^3. Hence det Q<=552Z^3.

Also the constant-in-T part of J_X is at most (13/16)S^2, and its T coefficient is at most 24S. Thus J_X<=194Z^2. The exact Schur remainder is det M/det Q, giving

    J_X-c^T Q^{-1}c/4 >=Z^2/(49152*552)
                          >=J_X/5263589376.

No part of this coarse floor is added to a separate reserve. The full exact Schur complement remains the more useful continuation quantity.

## 5. Left QR and the actual all-mean quantifier

For A_1!=0, take R with first column A_1/|A_1| and second column its counterclockwise perpendicular. Then R is in SO(2), and R^T A is upper triangular. If A_1=0, every R in SO(2) leaves the first column zero, so the construction remains valid. No determinant, sign or invertibility assumption on A is needed.

Left target rotations preserve u,v and j, hence the ORIGINAL anisotropic J_1. The chain rule gives DJ_1(R^T A):LH=DJ_1(A):RLH. Also det(RLH)=det(LH). For R^T A=[[alpha,beta],[0,delta]],

    alpha^2-beta^2-delta^2=|A_1|^2-|A_2|^2,
    alpha delta=det A.

The multiplier is therefore exactly (|A_1|^2-|A_2|^2+7det A)/2, as claimed.

Only the target/output is rotated. The source lattice and Hessian derivatives are not rotated. This distinction is essential: the proof does not use an invalid right/source-rotation invariance of J_1. At each A the admitted class is phi=R diag(2,-4) grad psi. It is a scalar-potential subclass of compatible vector fields, not all such fields.

## 6. Function spaces and equality

For smooth periodic psi, every Hessian entry has zero mean and the determinant integral is zero by integration by parts. For example <psi_xx psi_yy>=<psi_xy^2>. These facts hold on any rectangular torus. The multiplier is constant in space, so its determinant term integrates to zero.

Approximate a periodic W^{2,4} scalar in that norm by smooth periodic scalars. Hessians converge in L4, all original quartic energies converge in L1, the linear term converges, and the quadratic determinant term converges in L2. Thus the same inequality holds in the stated space. Compactly supported W^{2,4} scalar potentials on R2 can be embedded and periodized in a larger rectangle without a boundary jump; smooth approximation gives the same conclusion.

The quantitative pointwise reserve, or strict M positivity, shows that equality requires Hess psi=0 almost everywhere. On a periodic torus this means psi is constant up to its irrelevant additive constant. The proof does not establish an extension to arbitrary W^{1,4} vector fields by density: that larger class is not dense in the adapted scalar-potential class.

## 7. Reproduction and correction history

The independent checker reconstructs the original density rather than importing the construction program. Its first execution reached receipt serialization but JSON could not encode a SymPy BooleanTrue. This was a reporting error, not a failed polynomial identity, and no successful receipt was claimed from that run. A separate correction converts the check values to Python bool without changing any candidate, identity or acceptance condition. The corrected source passed all 16 exact checks in 1.092180251 seconds on Python 3.12.14 with SymPy 1.14.0.

The delivered `check_exact.py` is byte-identical to the corrected reviewed checker, SHA256 8af615d47b1b29c20375f2e3652c4efb80e0d277215e018ddb5b680208d607b1. `CHECK_RESULT.json` is its original successful receipt. The complete technical history is retained separately; the first reporting error is not concealed or treated as a scientific negative result.

No optimizer, field sample, parameter scan or physical experiment is evidence for the theorem. No historical novelty or unrestricted J_r conclusion is asserted.
