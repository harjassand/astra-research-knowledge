# A source-compatible two-plane orientation comparison and whole-value region

26 October 2026. New noncommuting filtered-seed receiving, submitted for independent audit. This is fixed-spectrum orientation, not Schmidt-Gram pinching or the anchored filter comparison.

## 1. Actual source and common spectral kernel

For qutrit matrices H,A>=0 let

 psi_H=(I3 tensor sqrt(H))Omega3,
 X(H,A)=P_(psi_H)+I3 tensor A,

where Omega3=sum_i |i,i>. The main reference Gram is H. The source need not be a normalized TP Choi state; all statements are homogeneous entropy-value statements.

For faithful A and t>0 put K(t)=sqrt(H)(A+tI)^(-1)sqrt(H). The acquired determinant entropy calculation gives

 Delta(X(H,A))=integral_0^infinity F(K(t))dt,

 F(K)=2logdet[I+(TrK I-K)/2]-3logdet(I+K/3)-log(1+TrK).

Indeed the input rank-one head is1+TrK; after the reference rescaling s=3t its head is det(I+K/3); the rank-three antisymmetric WH-output compression has the spectrum of (TrK I-K)/2. The affine cutoff terms cancel the homogeneous log3 term. At A=0 this integral correctly gives the pure-main deficit, not necessarily zero. PSD endpoints follow by continuity.

## 2. Hypothesis and orientation theorem

Suppose H and A share a reducing one-dimensional eigenspace with respective eigenvalues h3,a3 satisfying

 h3<=2a3.

Their two-dimensional complementary blocks H2,A2 may be arbitrary and noncommuting. Keep their spectra fixed and let H_al be obtained by aligning H2 with A2 so that the larger eigenvalue of H2 is paired with the larger eigenvalue of A2. Then

 Delta(X(H,A))>=Delta(X(H_al,A)).                     (1)

The right side is nonnegative by the independently received aligned filtered-seed theorem `aligned_filtered_seed_cq_dilation_value_theorem.md` / `aligned_filtered_seed_cq_dilation_independent_audit.md`. Thus this is a whole-value class with genuinely noncommuting two-dimensional main/reset blocks. It does not require the initial F kernel to be nonnegative. In fact, fix a noncommuting faithful active pair H2,A2 and scale H2 by M while keeping the allowed spectator fixed. At t=0 the two active kernel eigenvalues grow like M, so F(K(0))=-log M+O(1). Thus this whole-value class contains genuinely noncommuting sources with arbitrarily negative initial logarithmic kernel; it is not a restatement of the initial-positive cone.

## 3. Exact scalar geometry of the pair trace

At each t, the third eigenvalue is k=h3/(a3+t)<=2. The active pair has trace s and product p, with p<=s^2/4. Its product is orientation-independent:

 p=det(H2)/det(A2+tI).

At fixed p,k, differentiation of the spectral logarithmic kernel with respect to s gives

 g(s,p,k)=2/(s+2)+2(k+2)/[p+(k+2)(s+k+2)]
          -9/(p+3s+9)-1/(s+k+1).

Its positive denominator has numerator

 N=Acoef s^2+Bcoef s+Ccoef,
 Acoef=3(kp-k^2+4),
 Bcoef=p^2+(5k^2+15k-2)p-3k^3+24k+24,
 Ccoef=2kp^2+(2k^3+12k^2+20k-10)p+18k^2+36k.

For 0<=k<=2 this numerator is strictly positive on the nontrivial physical domain s>0,0<=p<=s^2/4:

- Acoef>=0.
- If k<=1, Bcoef>=(p-1)^2+20>0. If1<=k<=2, both24-3k^3 and the p coefficient in Bcoef are nonnegative, so Bcoef>=0.
- If k>=1/2, Ccoef>0.
- If k<=1/2, Acoef>=45/4 and Ccoef>=-10p, so Acoef s^2+Ccoef>=35p>=0; Bcoef s>0 completes strictness.

Therefore F is strictly increasing in the active pair trace throughout the required range.

## 4. One actual alignment minimizes the trace at every resolvent parameter

In an eigenbasis of A2, the active trace is

 s(t)=Tr[H2(A2+tI)^(-1)].

The ordinary two-dimensional trace rearrangement inequality minimizes this by pairing the larger H2 eigenvalue with the smaller inverse eigenvalue, namely the larger A2 eigenvalue. This SAME alignment minimizes s(t) for every t>0. The pair product and spectator k are unchanged. Section3 therefore gives a pointwise F comparison; integrating yields (1).

This is an actual fixed-spectrum source replacement. It does not replace a pointwise minimum by a different source at each t. If both complementary spectra are nondegenerate and the orientation is not a minimizing alignment, the trace and hence value comparison are strict.

## 5. Singular endpoints and scope

To receive PSD endpoints, replace H,A by H+epsilon I,A+epsilon I. The common reducing line and the condition h3<=2a3 are preserved, the minimizing complementary alignment is unchanged, and entropy continuity receives the limit. If the active pair is identically zero, the orientation statement is vacuous.

This theorem is stronger than a positive fixture: it receives all two-plane coherences under the single spectator ratio condition, with arbitrary active spectra. It does not prove a global commuting-orientation minimum when h3>2a3, nor when H,A have no common reducing line. It does not imply the anchored inequality Delta(filtered)>=lambda_min(Z*Z)Delta(seed).

## 6. Additional pointwise geometry beyond the paid region

For completeness, if Acoef>=0 with k>2, then p>=k-4/k. The coefficient Bcoef is increasing in p and at that lower endpoint equals

 2(k-1)^2(k+2)(k^2+8k+4)/k^2>=0,

while Ccoef>0. Hence N>0 there as well. If Acoef<0, necessarily k>2 and Ccoef>0, so N has exactly one positive root in s, crossed downward. Thus the pointwise pair-trace kernel has no interior minimum even outside the paid region. This last geometry alone does NOT receive the integrated orientation: different t can have different maximizing traces, and minima must not be exchanged with integration.

## 7. Optional exact determinant-compensated criterion

The same actual orientation conclusion holds under the more general condition

 k(t)p(t)-k(t)^2+4>=0 for every t>=0,

not only k<=2. For faithful A this is the nonnegativity on t>=0 of the explicit quartic

 P(t)=h3 det(H2)(a3+t)
      +[4(a3+t)^2-h3^2] det(A2+tI).

Section6 proves positivity of g whenever this coefficient condition holds. The condition is source-compatible, independent of the active orientation, and can be certified by an exact univariate polynomial test. No numerical sampling of t is a substitute for that certificate. The simple h3<=2a3 cone is an immediate sufficient case with no polynomial test required.

This is an optional determinant resource comparison within the SAME reducing-line geometry; it makes no assertion for fully irreducible H,A or for a quartic that fails the nonnegativity test.
