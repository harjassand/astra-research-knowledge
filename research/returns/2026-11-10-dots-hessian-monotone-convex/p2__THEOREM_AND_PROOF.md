# Upper-triangular means and a valid all-mean adapted Hessian consequence

9 November 2026. A complete pointwise support theorem for the original anisotropic J_1 and an all-affine-mean consequence for adapted scalar-Hessian perturbations. This is not a theorem for arbitrary r or arbitrary compatible vector fields. No historical novelty claim is made.

Normalization: for F=[[a,b],[c,d]], put u=a^2+c^2, v=b^2+d^2 and j=ad-bc. Throughout this packet, k=r=1 and J_1(F)=(u-v+2j)^2/8+uv/2+j^2. Angle brackets denote normalized Lebesgue average on the chosen rectangular torus.

## 1. Pointwise theorem for every upper-triangular mean

Let L=diag(2,-4). For every real alpha,beta,delta, put

    A=[[alpha,beta],[0,delta]],
    lambda(A)=(alpha^2-beta^2-delta^2+7alpha delta)/2.

For EVERY real symmetric H,

    J_1(A+LH)>=J_1(A)+DJ_1(A):LH+lambda(A)det(LH). (1)

The inequality is strict for H!=0. No sign, invertibility, amplitude or frequency restriction is imposed. Consequently it proves the integrated Jensen inequality for every real periodic W^{2,4} scalar potential with perturbation LH=L D^2 psi, on any rectangular torus, and for compactly supported potentials by periodization.

## 2. Valid all-A adapted consequence: LEFT QR only

For any real 2x2 A, choose R in SO(2) so R^T A is upper triangular. If the first column is nonzero, take the first column of R to be A_1/|A_1| and its second column to be the counterclockwise perpendicular. If A_1=0, any such R is permissible.

The density is invariant under LEFT target rotations. Hence, with L_A=R L,

    J_1(A+L_A H)>=J_1(A)+DJ_1(A):L_A H
                      +lambda(A)det(L_A H),       (2)
    lambda(A)=(|A_1|^2-|A_2|^2+7det A)/2.

This proves the Jensen inequality at EVERY affine mean for the adapted scalar-potential class phi=L_A grad psi. It does not prove it for arbitrary phi or for the same fixed L at every A. Only output coordinates were rotated; the periodic lattice is unchanged. Arbitrary right/source rotations are invalid for J_1 and are not used.

## 3. Exact original-density affine matrix

Write H=[[U,V],[V,W]], x=2U, y=-4W, T=V^2. The perturbation is [[x,2V],[-4V,y]] and has determinant xy+8T. Its density is

    J_X=(x^4+y^4)/8+(7/4)x^2y^2+(x^3y-xy^3)/2
             +(9x^2+30xy+y^2)T+194T^2.

Subtracting the right side of (1) gives the EXACT polynomial

    a^T Q a+c dot a+J_X,   a=(alpha,delta,beta),

where

    Q11=5T+3x^2/4+xy+7y^2/4,
    Q22=5T+7x^2/4-xy+3y^2/4,
    Q12=T+3x^2/4+7xy/4-3y^2/4,
    Q13=V(3x+5y), Q23=V(5x-y),
    Q33=23T+(x^2+y^2)/4,

    c1=(x^3+3x^2y+7xy^2-y^3)/2+(18x+30y)T,
    c2=(x^3+7x^2y-3xy^2+y^3)/2+(30x+2y)T,
    c3=V(3x^2+10xy-y^2+124T).

Let M be the 4x4 symmetric matrix with upper-left Q, last column c/2, and last diagonal entry J_X. We prove M positive definite whenever (x,y,T)!=(0,0,0).

## 4. Positive quadratic mean metric

The first diagonal entry is (3x^2+4xy+7y^2)/4+5T, positive at every nonzero state with T>=0. The first 2x2 principal determinant is

    24T^2+(22x^2-7xy+28y^2)T/2+Pdet/16,

with Pdet as displayed below. Every coefficient is positive away from its zero set, proving this principal block positive definite. The full determinant is

    det Q=552T^3+(238x^2-273xy+376y^2)T^2/2
       +(128x^4-220x^3y+225x^2y^2+80xy^3+124y^4)T/16
       +(x^2+y^2)Pdet/64,

    Pdet=12(x^2-y^2-13xy/12)^2+(251/12)x^2y^2.

The degree-four coefficient is bounded below by

    28x^4+64x^2y^2+84y^4,

using 220|x^3y|<=100x^4+121x^2y^2 and 80|xy^3|<=40x^2y^2+40y^4. Every coefficient is a positive binary form. Therefore Q is positive definite away from the zero perturbation.

## 5. The complete tenth-degree Schur determinant

Literal expansion gives

    det M=14832T^5+P2 T^4+(P4/8)T^3
                        +(P6/32)T^2+(P8/128)T
                        +(x^2+y^2)P0/512,

with

    P2=4406x^2-3339xy+6516y^2,

    P4=4176x^4-5064x^3y+8651x^2y^2-580xy^3+5788y^4,

    P6=960x^6-1228x^5y+1533x^4y^2+40x^3y^3
                              +3377x^2y^4+120xy^5+484y^6,

    P8=104x^8-88x^7y-23x^6y^2+100x^5y^3+570x^4y^4
                              +232x^3y^5+129x^2y^6-92xy^7+60y^8.

The constant coefficient P0 has the following explicit positive degree-eight sum of squares. With D=x^2-y^2 and K=xy,

    P0=4(D^2+KD/4-K^2)^2
          +(11/4)(KD+28K^2/11)^2+(112/11)K^4>0

for (x,y)!=(0,0).

All remaining coefficient forms are positive, as follows.

### 5.1 Quadratic and quartic coefficients

P2 is positive definite. For P4, use

    5064|x^3y|<=2000x^4+3206x^2y^2,
    580|xy^3|<=290x^2y^2+290y^4.

The first inequality holds because 4*2000*3206>5064^2. Thus

    P4>=2176x^4+5155x^2y^2+5498y^4>0.

### 5.2 Sextic coefficient

Use

    1228|x^5y|<=600x^6+629x^4y^2,
    40|x^3y^3|<=20x^4y^2+20x^2y^4,
    120|xy^5|<=60x^2y^4+60y^6.

Since 4*600*629>1228^2, these imply

    P6>=360x^6+884x^4y^2+3297x^2y^4+424y^6>0.

### 5.3 Octic coefficient: one explicit rational Gram

On the monomials (x^4,x^3y,x^2y^2,xy^3,y^4), P8 has the exact Gram

    [[104,-44,-55/2,0,0],
     [-44,32,50,0,0],
     [-55/2,50,570,116,0],
     [0,0,116,129,-46],
     [0,0,0,-46,60]].

Its left 2x2 block has determinant 1392>0; its right 2x2 block has determinant 5624>0. Eliminating those blocks leaves the scalar

    570-3400/29-100920/703=6303710/20387>0.

Thus the Gram is positive definite. All coefficient forms in det M are positive, so det M>0 for every nonzero perturbation. Schur complementation proves (1).

## 6. Uniform reserve and exact remaining scope

For a quantitative continuation one may retain the full Schur remainder. A deliberately coarse uniform bound is also available. Set S=x^2+y^2 and Z=S+T. Here P0>=S^4/6 follows directly from its displayed squares. Set A0=D^2+KD/4-K^2. Then S^2<=8|A0|/7+37K^2/7, so weighted Cauchy gives S^4<=(16851/5488)[4A0^2+(112/11)K^4]<6P0. Consequently det M>=S^5/3072+14832T^5>=Z^5/49152. For det Q, the T^2, T and constant coefficients are at most (887/2)S, (777/16)S^2 and (135/256)S^3 respectively, so det Q<=552Z^3. The constant part of J_X is at most (13/16)S^2 and its T coefficient at most 24S, so J_X<=194Z^2. Therefore

    J_X-c^T Q^(-1)c/4>=J_X/5263589376.

The original pointwise support has this reserve uniformly in every upper-triangular affine mean, and the rotated statement inherits it. This tiny floor is not intended to replace the actual matrix resource in the transverse proof.

The full compatible problem still requires paying the transverse component outside the adapted scalar-potential class. No right rotation, arbitrary-field density argument, or addition of separate restricted certificates is licensed by this theorem. Other r remain separate obligations.

## 7. Reproduction and independent review

The independent checker `check_exact.py` reconstructs the literal original J_1, extracts the full affine polynomial, and verifies the two Q determinants, the complete det M polynomial and its rational Gram. `CHECK_RESULT.json` records all 16 exact checks passing. Sections 4-6 supply the analytic inequalities and transformation argument that a finite symbolic check alone cannot prove. `INDEPENDENT_REVIEW.md` gives their separate full reconstruction.

The reviewed source SHA256 is 70867bc2137841c0005f8876d073f1396149dbe09fc7ddd0a3619c143d86afaa. This reader edition expands the original two references to a diagonal special case into the complete formulas and bounds above. It changes no theorem, normalization, matrix, coefficient, inequality or scope. `PROVENANCE.md` identifies the original review and preserves the receipt-only technical correction honestly.
