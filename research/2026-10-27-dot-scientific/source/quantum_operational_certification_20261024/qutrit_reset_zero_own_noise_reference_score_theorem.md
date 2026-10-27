# The distinguished-zero-noise qutrit-reset reference score is nonnegative

26 October 2026. Exact analytical boundary receiving for the anchored reference-filter problem. This closes one of the two singular faces left by the coordinate-score spectral-floor reduction, not the global anchored comparison.

## 1. Actual source and coordinate score

Consider S=3d P_Phi+I3 tensor A with A=diag(0,b,c), d>0, b,c>=0. Let T_r=diag(sqrt(r),1,1) act on the reference and define

 Q0(S)=partial_r Delta[(I3 tensor T_r)S(I3 tensor T_r)] at r=1.

Then Q0(S)>=0, with strict inequality whenever b+c>0. For b=c=0 the score is zero. No generic reference-filter monotonicity is asserted away from this unfiltered source.

Homogeneity reduces to d=1 by replacing b,c by b/d,c/d and multiplying the final score by d.

## 2. Exact block-entropy formula

For d=1 define J_m to be the all-ones m by m matrix, and

 H=J3+diag(0,b,c), M(u)=J2+diag(0,u),
 g3(b,c)=(H logH)_00, g2(u)=(M(u)logM(u))_00.

The actual input's changing correlated block is H. The two WH output pairs involving reference label0 are M(2b)/2 and M(2c)/2, up to harmless signs. The reference entry at label0 equals1. Differentiating the homogeneous entropy expression, the affine trace terms cancel; the factors1/2 in the output produce2log2, and the normalization term produces-log3. Therefore

 Q0=kappa+g3(b,c)-g2(2b)-g2(2c), kappa=log(4/3).      (1)

This also follows from the previously acquired actual reference-score integral. Formula (1) receives all b,c>=0 by continuity of xlogx, including the pure endpoint; it avoids singular ambient logarithms.

## 3. A pointwise positive resolvent compensation

For s>0 put

 h_s(z)=z/[(s+1)(s+1+z)],
 v=s/(b+s), w=s/(c+s).

The integral representation of xlogx and Sherman-Morrison applied to diag(0,b,c)+J3 give

 g3(b,c)=integral_0^infinity h_s(v+w)ds,
 g2(2b)=integral_0^infinity h_s(v/(2-v))ds,
 g2(2c)=integral_0^infinity h_s(w/(2-w))ds.

For example the central resolvent is

 (H+sI)^(-1)_(00)=(s+v+w)/[s(s+1+v+w)],

and the constant central entry H00=1 makes its entropy integrand exactly h_s(v+w). Also

 kappa=integral[2h_s(1)-h_s(2)]ds=2log2-log3.

Thus the exact score is the integral of

 D_s(v,w)=h_s(v+w)-h_s(v/(2-v))-h_s(w/(2-w))
          +2h_s(1)-h_s(2).                              (2)

This expression is nonnegative POINTWISE for every s>0 and v,w in[0,1]. This is a special acquired compensation, not a generic sign assertion for the original score kernel.

There is a short analytical proof, making the polynomial below optional corroboration. For fixed s, h_s is increasing and concave. Its concavity gap J(x,y)=h_s(x)+h_s(y)-h_s(x+y) is increasing in each argument, since partial_x J=h_s'(x)-h_s'(x+y)>=0. Also v/(2-v)<=v and w/(2-w)<=w. Therefore D_s(v,w)>=J(1,1)-J(v,w)>=0. For finite actual b+c>0, at least one of the first two inequalities is strict at every s>0.


## 4. Exact positive polynomial certificate

Set v=1/(1+x), w=1/(1+y), x,y>=0. In the actual source x=b/s,y=c/s. The denominator of (2) is the positive polynomial

 (s+2)(s+3)(2sx+s+2x+2)(2sy+s+2y+2)
 *[sxy+sx+sy+s+xy+2x+2y+3].

Its numerator is N=s^3 N3+s^2 N2+s N1+N0, where

 N3=2x^2y+2xy^2+6xy+x+y,
 N2=8x^2y^2+24x^2y+4x^2+24xy^2+52xy+10x+4y^2+10y,
 N1=16x^2y^2+58x^2y+16x^2+58xy^2+128xy+30x+16y^2+30y,
 N0=8x^2y^2+36x^2y+16x^2+36xy^2+88xy+28x+16y^2+28y.

Every coefficient is positive. If x+y>0, N>0; if x=y=0 it vanishes. This proves the pointwise assertion, hence (1)'s strict score conclusion. The corners v=0 or w=0 follow by continuity if needed; finite actual b,c give v,w>0.

All individual entropy integrals converge and their combination is the actual derivative, so no conditional exchange or unreceived normalization is involved.

## Scope

Together with the separate coordinate-score floor reduction, this excludes a negative infinitesimal reference score on the face where its OWN reset eigenvalue vanishes. The companion-zero face remains a separate problem. Even positivity of all unfiltered coordinate scores would not by itself imply the finite anchored reference-filter inequality or any generic filtered-source score order.

## 5. Finite expansion of the reset-kernel reference direction

The same polynomial pays a finite anchored filter, not only the infinitesimal score. Let d=1 initially and

 psi_r=sqrt(r)|00>+|11>+|22>,
 S_r=|psi_r><psi_r|+I3 tensor diag(0,b,c), r>=1.

This is the actual reference-filtered seed with Z_r=diag(sqrt(r),1,1). Its reset term is unchanged because the expanded direction is in the reset kernel. Let P_r=|psi_r><psi_r| alone.

Then

 partial_r Delta(S_r) >= partial_r Delta(P_r)
 =log[4r(r+2)/(3(r+1)^2)]>=0.                         (3)

To verify the full derivative, the correlated input block is

 H_r=diag(0,b,c)+[sqrt(r),1,1]^T[sqrt(r),1,1],

and the two changing output pairs are one half of

 M_r(2b)=[[r,sqrt(r)],[sqrt(r),1+2b]],
 M_r(2c)=[[r,sqrt(r)],[sqrt(r),1+2c]].

Reference differentiation gives r log r before division by r. Affine terms cancel as in §2, yielding

 partial_r Delta(S_r)
 =kappa+log r+(H_r logH_r)_00/r
   -(M_r(2b)logM_r(2b))_00/r
   -(M_r(2c)logM_r(2c))_00/r.

Put a=s+r and h_a(z)=z/[a(a+z)]. Sherman-Morrison gives each central entry divided by r as log r plus the corresponding integral of h_a. Consequently the difference between the derivative above and the pure derivative is EXACTLY

 integral [h_a(v+w)-h_a(v/(2-v))-h_a(w/(2-w))
            +2h_a(1)-h_a(2)]ds,

with the same v=s/(b+s),w=s/(c+s). For r>=1, a-1=s+r-1>=0. The polynomial certificate in §4 applies verbatim with its parameter s replaced by a-1; v,w remain arbitrary numbers in[0,1]. Thus the integral is nonnegative, and strictly positive when b+c>0. The last sign in (3) follows from

 4r(r+2)-3(r+1)^2=(r-1)(r+3)>=0.

Integrating (3) from1 to r gives the quantitative anchored inequality

 Delta(S_r)>=Delta(S_1)+Delta(P_r),                    (4)

since Delta(P_1)=0. General d>0 follows by scaling b,c by1/d and multiplying all deficits by d.

By matched physical/reference covariance, the statement applies to any qutrit reset A>=0 with a kernel vector u and filter Z*Z=I+(r-1)P_u, r>=1; an output unitary factor in Z is irrelevant. It is a genuine finite reference-filter comparison with its pure-Schmidt payment retained. At this stage alone it does not justify iteration after other unequal filter eigenvalues have already been introduced. The weighted extension in §6 DOES permit kernel-only iteration, as stated below; expansion of noisy reference directions and arbitrary invertible filters remain unreceived.


## 6. General compensated clean-Schmidt-direction monotonicity

The preceding scalar concavity-gap proof gives more than the unfiltered seed. Let

 psi_r=sqrt(r)|00>+sqrt(u)|11>+sqrt(v)|22>,
 S_r=P_(psi_r)+I3 tensor diag(0,b,c),

where r,u,v>0 and b,c>=0. With P_r=P_(psi_r), the exact claim is

 partial_r[Delta(S_r)-Delta(P_r)]>=0                 (5)

for EVERY r>0. It is strict when b+c>0. Noise and main remain diagonal in the same two-dimensional reference plane; no arbitrary noncommuting transverse extension is claimed.

For s>0 put a=s+r, x=u s/(b+s), y=v s/(c+s). The same actual block/resolvent calculation as §5 gives the derivative difference as the integral of

 D=h_a(x+y)-h_a(ux/(2u-x))-h_a(vy/(2v-y))
   +h_a(u)+h_a(v)-h_a(u+v),

where h_a(z)=z/[a(a+z)]. Since 0<x<=u, 0<y<=v and

 ux/(2u-x)<=x, vy/(2v-y)<=y,

monotonicity of h_a and of its concavity gap J_a give

 D>=J_a(u,v)-J_a(x,y)>=0.

This proof works for every a>0; no inverse floor or relation between r,u,v is needed for the COMPENSATED derivative. Integrating gives

 Delta(S_r1)-Delta(S_r0)>=Delta(P_r1)-Delta(P_r0)

whenever r1>=r0>0. If r>=max(u,v), the pure derivative is itself nonnegative:

 partial_r Delta(P_r)=log[4r(r+u+v)/(3(r+u)(r+v))]>=0,

because r^2+r(u+v)-3uv>=0. Thus increasing the largest clean Schmidt coefficient cannot lower the actual deficit in this aligned family. This maximum-direction conclusion is not an assertion that every reference score is positive, and the compensated inequality does not by itself supply a whole-value baseline for arbitrary unequal u,v.


## 7. Finite filters supported in the reset kernel

Let the unfiltered seed be S=3dP_Phi+I3 tensor A with A>=0 on C3. Let K>=I satisfy ran(K-I) subset kerA, and let Z*Z=K. Then

 Delta((I tensor Z)S(I tensor Z*))
 >=Delta(S)+Delta((I tensor Z)3dP_Phi(I tensor Z*)).    (6)

An output-unitary polar factor of Z is irrelevant. Since K-I is supported in kerA, K and A commute and the reset is unchanged. Choose their common eigenbasis. Increase the kernel-axis eigenvalues of K one at a time from1 to their targets. The weighted compensated derivative in §6 remains valid after earlier clean weights have changed. Telescoping those compensated inequalities gives (6), using Delta(3dP_Phi)=0. Intermediate pure derivatives need not be positive; their total pure-deficit contribution is retained exactly.

This is a legitimate kernel-only iteration, not a claim that arbitrary reference-filter scores are positive. No noisy axis is changed, and no noncommuting A,K case is inferred.
