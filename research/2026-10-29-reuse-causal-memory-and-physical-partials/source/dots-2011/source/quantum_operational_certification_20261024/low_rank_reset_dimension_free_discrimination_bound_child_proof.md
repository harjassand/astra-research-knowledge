# Dimension-free overlap stability for rank-at-most-two reset

27 October 2026. Local post-cutoff analytic construction; independent receiving requested.

## Scope and statement

Let V:C^3 tensor C^r -> R be any isometry into a finite reference space,
C>=0, and Y>=0 on R with rank Y<=2. Use the UNNORMALIZED
Omega=sum_{i=1}^3 |ii>, so ||Omega||^2=3. Let

 X=(I tensor V)(P_Omega tensor C)(I tensor V*)+I_3 tensor Y,
 A=V(I_3 tensor C)V*, T=Tr A+Tr Y,
 e=(Tr A+Tr Y-||A-Y||_1)/2.

With the original homogeneous entropy deficit Delta(X) of the received
dynamic theorem,

                 e^2 <= 1944 (Tr Y) Delta(X) <= 1944 T Delta(X).

The numerical constant is intentionally crude. No least eigenvalue, main
rank, ambient dimension, or support alignment enters it. Zero T is trivial.
This proves a quantitative overlap implication, not a complete equality
classification. The sole imported entropy dependency is the received dynamic
reduction-clock payment and its original-source determinant identity in
`low_rank_reset_dynamic_duality_independent_audit.md` and
`monotone_reduction_clock_value_root.md`.

## 1. Quantitative payment in the actual positive clock direction

Write Y=sum_{j=1}^k y_j |v_j><v_j|, k<=2, y_j>0, with orthonormal v_j.
Put C0=I_3 tensor C and

 B_s=s C0^(1/2)V*(s+Y)^(-1)V C0^(1/2), R_s=Tr_code B_s.

For J_s=V*Y(s+Y)^(-1)V, positivity of partial trace gives

 Tr_code J_s <= Tr J_s I <= [sum_j y_j/(s+y_j)] I.

Consequently B_s<=C0 and R_s>=q_s C, where

 q_s=3-sum_j y_j/(s+y_j),  1<=q_s<=3.

For every j, q_s-1>=s/(s+y_j); for k=1 the unused rank budget contributes
an additional positive 1. The clock derivative is

 B'_s=sum_j y_j/(s+y_j)^2 C0^(1/2)V*P_vj V C0^(1/2).

The received dynamic identity pays Delta(X) by the integral of
Tr G_s B'_s, plus other nonnegative terms, where

 G_s=k'_s(B_s)-I_3 tensor k'_s(R_s),
 k'_s(x)=integral_s^(3s) (x+t)^(-1)dt-log 3.

Because k'_s is operator antitone, the preceding two source bounds give

 G_s >= k'_s(C0)-k'_s(q_s C0).

This last difference is a functional calculus expression. For c>=0,

 k'_s(c)-k'_s(q c)
 =integral_s^(3s) (q-1)c/[(t+c)(t+qc)]dt
 >=(2/9)(q-1) s c/(s+c)^2,      1<=q<=3.

Thus, summing the actual derivative residues separately,

 Delta(X)>=(2/9) sum_j integral_0^infinity
   [s^2 y_j/(s+y_j)^3] <v_j|A^2(s+A)^(-2)|v_j> ds.

All integrations have nonnegative integrands, so Tonelli/spectral calculus
applies without a nonsingularity assumption. For c,y>0,

 integral_0^infinity s^2 y c^2/[(s+y)^3(s+c)^2]ds
 >= y c^2 integral_0^infinity s^2/(s+c+y)^5 ds
 = y c^2/[12(c+y)^2].

At c=0 both sides vanish. Hence the exact quantitative payment is

 Delta(X)>=S/54,
 S=sum_j y_j ||A(A+y_j I)^(-1)v_j||^2.                 (1)

The derivation can first be performed from a positive cutoff and then sent
to zero using the received source entropy continuity/payment. It retains
the FULL reference-space inverse and arbitrary reset spectators.

## 2. A dimension-free two-vector discrimination test

Set delta_j=||A(A+y_j)^(-1)v_j||. Each delta_j is in [0,1]. Keep indices
with delta_j<=1/(2 sqrt(2)); discard the others. For each retained index set

 w_j=y_j(A+y_j)^(-1)v_j,

and form W with these columns. Its corresponding original column matrix
V_keep is an isometry, and

 ||W-V_keep|| <= ||W-V_keep||_HS
               =(sum_keep delta_j^2)^(1/2)<=1/2.

Therefore W has smallest singular value at least 1/2. The orthogonal
projector Q onto ran W satisfies Q=W(W*W)^(-1)W*<=4WW*.
If there are no retained indices take Q=0. Interpret Q as the decision Y.
Its binary discrimination cost bounds the optimal Helstrom cost e:

 e <= Tr A Q+Tr Y(I-Q).

Since ||w_j||<=1 and A w_j=y_j(v_j-w_j),

 Tr A Q <=4 sum_keep <w_j,A w_j>
         <=4 sum_keep y_j delta_j
         <=4 sqrt((Tr Y) S).

For retained v_j, w_j belongs to ran Q and ||v_j-w_j||=delta_j, so
< v_j,(I-Q)v_j > <=delta_j^2. For discarded indices delta_j^2>1/8,
so their total reset mass is at most 8S. Consequently

 Tr Y(I-Q)<=S_keep+8S_discard<=8S.

Write t=Tr Y. In addition to e<=4 sqrt(tS)+8S we have the
trivial decision-always-A bound e<=t. If S>=t/16, then
 e<=t<=4 sqrt(tS).
If S<t/16, then 8S<=2 sqrt(tS), hence
 e<=6 sqrt(tS).
Therefore in all cases

 e^2<=36 (Tr Y) S<=36 T S.                            (2)

Combining (1) and (2) proves the stated constant 1944.

## 3. Rank-one improvement

When Y=y|v><v|, set q=<v|(A+y)^(-1)|v>,
r=<v|(A+y)^(-2)|v>, m=1-yq=<v|A(A+y)^(-1)|v>.
If q<1/(2y), the trivial decision always-A gives e<=y<=2ym.
Otherwise use the rank-one decision-Y projector onto
w=(A+y)^(-1)v/sqrt(r). Its exact cost is

 <w|A|w>+y(1-|<v,w>|^2)=q(1-yq)/r.

The scalar Cauchy inequality r>=q^2 yields cost<=m/q<=2ym.
Therefore in all cases e<=2ym. Another Cauchy inequality gives
m^2<=||A(A+y)^(-1)v||^2. Thus

 e^2<=4y S<=216 (Tr Y) Delta(X)<=216 T Delta(X).

Zero reset is trivial. This improvement is stated separately and is not
used for the two-vector theorem.

## Guards

This is not obtained from unsupported overlap subadditivity, pinching,
or replacing the actual reset inverse by a compressed inverse. The
measurement construction directly treats both reset eigenvectors. Rank
at most two is used twice: to keep q_s>=1 and in the retained-column
singular-value estimate. No assertion for arbitrary higher-rank reset
or nonreversible main is made.
