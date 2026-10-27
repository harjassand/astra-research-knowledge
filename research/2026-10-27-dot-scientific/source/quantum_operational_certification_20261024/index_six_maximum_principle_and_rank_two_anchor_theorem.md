# Index-six maximum principle and all nonaligned Schmidt-rank-two anchors

2026-10-25. Exact dimension-free theorem. It closes the entire nonaligned Schmidt-rank-two top-vector interface, not only a scalar threshold or commuting subcase. The unrestricted Schmidt-rank-three target remains open.

## 1. Universal two-operator maximum principle

Let U,V be effects on any finite-dimensional space, and let psi be a unit vector with Upsi=psi. Define

B=(U+5V)/6,
C=(U+3B)/4=(3U+5V)/8,
y=<psi,Vpsi>.

Then

<psi,[logB-2logC]psi> >= c_6(1-y),                  (1)
c_6=5/12+(25/288)log(5/256)>5/72>0.

No tensor product, marginal relation or commutation is needed in this abstract theorem. Supported logarithms handle singular operators.

### The exact pencil and moment

Initially assume U,V faithful. Set

q(t)=<psi,1_(0,infinity)(tV-U)psi>,
h(s)=<psi,log(U+sV)psi>.

The balanced-binary positive-part identity, differentiated in U along P=|psi><psi|, gives

h(s)=integral_0^infinity s q(t)/[t(t+s)]dt,
integral_0^infinity q(t)/t^2dt=y.                  (2)

For an explicit renormalized derivation of the first identity, use the exact two-source formula

D(Z||V)=TrZ
 +integral_0^1 [Tr(Z-tV)_+-TrZ]/t dt
 +integral_1^infinity Tr(Z-tV)_+/t dt.

Differentiate in Z along P, first at Z=U+sV and then at Z=U, and subtract. The affine and small-t subtraction terms cancel. The result is

Tr P[log(U+sV)-logU]
 =integral_0^infinity Tr P[Pi_+(U-(t-s)V)-Pi_+(U-tV)]/t dt.

For t<s the first projector is identity; for t>s the complement relation converts the numerator to q(t)-q(t-s). Changing variables with a finite cutoff and then taking the limit yields integral s q(t)/[t(t+s)]dt. The cutoff boundary vanishes since q is bounded and equals1 for all sufficiently large t in the faithful case. Thus no divergent unrenormalized hinge functional is differentiated.

The first identity uses <psi,logU psi>=0. The second is the same exact sum rule already proved and audited in nonaligned_product_top_overlap_theorem.md: differentiate D(V||U), whose gradient compression is -<psi,Dlog_U(V)psi>=-y. Both identities use ONE and the same pencil tV-U.

The left side of (1) is

j=log(32/27)+h(5)-2h(5/3)
 =log(32/27)-integral_0^infinity w(t)q(t)dt,
w(t)=5(5-t)/[t(t+5)(3t+5)].                        (3)

Unlike the previous index-three kernel, w changes sign. That sign is retained exactly.

### A tail defect bound from the actual maximal vector

For t>1 put H_t=tV-U. Since Upsi=psi,

(H_t-(t-1)I)psi=t(V-I)psi.

On the nonpositive spectral subspace of H_t, the absolute value of H_t-(t-1)I is at least t-1. Therefore

1-q(t)<=t^2 <psi,(I-V)^2psi>/(t-1)^2
       <=t^2(1-y)/(t-1)^2.                         (4)

This is a spectral norm inequality, not an assumption that q is monotone. It remains valid even when its right side exceeds1.

### An exact calibrated multiplier

Let rho_0=5/12 and

k(t)=w(t)-rho_0/t^2
 =-25(t-1)(3t-5)/[12t^2(t+5)(3t+5)].

The sign is positive precisely on (1,5/3), negative on its complement. Compare q with q_0(t)=1_(t>1). Their moments are y and1, and direct integration gives

integral_1^infinity w(t)dt=log(32/27).

Hence

integral wq-log(32/27)
 =rho_0(y-1)+integral k(t)[q(t)-q_0(t)]dt.

The contributions from t<1 and 1<t<5/3 are nonpositive, using only 0<=q<=1. On t>5/3, apply (4) with the correct negative sign of k to get

integral wq-log(32/27)
 <=-(1-y)[rho_0+integral_(5/3)^infinity k(t)t^2/(t-1)^2dt].

The remaining integral is elementary:

k(t)t^2/(t-1)^2
 =-75/[32(3t+5)]+25/[36(t+5)]+25/[288(t-1)],

integral_(5/3)^infinity k(t)t^2/(t-1)^2dt
 =(25/288)log(5/256).

This proves (1). For an entirely rational positivity check, e^4 exceeds its degree-seven Taylor sum, and that rational sum exceeds256/5. Thus log(256/5)<4 and

c_6>5/12-100/288=5/72.

### Singular extension

Replace U,V by (1-e)U+eI,(1-e)V+eI. The top condition Upsi=psi survives. Both logarithmic arguments dominate fixed positive multiples of P, so their P-weighted logarithms converge on supported spaces. The overlap y also converges, and (1) follows for all effects.

## 2. Equivalent index-six source certificate

Suppose A,B are effects, Apsi=psi, and BOTH

A<=6B,
I-A<=6(I-B).                                       (5)

Then V=(6B-A)/5 is an effect and the abstract theorem applies with U=A. Therefore

<psi,[logB-2log((A+3B)/4)]psi>
 >=(6c_6/5)(1-<psi,Bpsi>)
 >=(1/12)(1-<psi,Bpsi>)>=0.                         (6)

The two order inequalities are jointly necessary for this receiving use; no arbitrary index-nine relaxation is substituted.

## 3. Every physical two-plus-one source has index at most six

Let A=X direct-sum Y be an effect across C^3=C^2 direct-sum C, with R=Tr_2X and B=EA=I_3 tensor(R+Y)/3. The standard two-dimensional partial-trace index inequality gives

X<=2 I_2 tensor R<=2 I_2 tensor(R+Y),
Y<=R+Y<=2(R+Y).

Thus A<=6B. Apply the same argument to the effect I-A, which has the same physical block structure, to obtain I-A<=6(I-B). Hence (6) applies to EVERY unit top vector of A, even one entangled with a completely nonaligned reference.

The partial-trace inequality can be proved without a dimension assumption on reference: pinching X in the two physical basis blocks gives X<=2 diag(X_00,X_11)<=2 I_2 tensor(X_00+X_11).

## 4. Full actual-N anchor for every Schmidt-rank-at-most-two top vector

Let A be any physical qutrit effect and let psi be ANY unit top vector of Schmidt rank at most two. Choose its physical Schmidt support and twirl only the relative phase between that support and its physical complement. The twirl fixes P=|psi><psi| and B=EA, and produces a two-plus-one block Abar. WH covariance and convexity of -Tr NP log NA at fixed B give

g_N(A;P)>=g_N(Abar;P),
g_N(A;P)=Tr EP logB-2Tr NP log NA.

For the actual unital channel N, operator Jensen gives

N(log NAbar)<=log(N^2 Abar),
N^2 Abar=(Abar+3B)/4.

Consequently

g_N(A;P)>=<psi,[logB-2log((Abar+3B)/4)]psi>
 >=(1/12)(1-<psi,Bpsi>)>=0.                         (7)

No reference pinching, reference-dimensional truncation, assumption [rho,B]=0, or pointwise-value-to-gradient lift occurs. The actual source marginal is unchanged throughout. Singular outputs are handled by A_e=(1-e)A+eI, which preserves the maximal-vector condition, then supported limits.

In particular, the formerly open nonaligned Schmidt-two formula

log(4/3)+Tr rho[log(R+Y)-logR]
 -<psi,log(X+I_2 tensor Y)psi>

is nonnegative for ALL effects X,Y with Xpsi=psi, in every finite reference dimension.

## 5. Full-target stationary consequence and its boundary

At a negative fixed-reference global minimizer of Delta, the two-sided normalized curve (A+sP)/(TrA+s) for any rank-one top P has constant relevant supports and forces

g_N(A;P)=Delta(A)/TrA<0.

Equation(7) therefore shows that EVERY nonzero vector in such a minimizer's maximal eigenspace must have Schmidt rank THREE. This is an exact necessary condition, not a proof that no such minimizer exists.

For a three-dimensional reference, the top eigenvalue of a negative minimizer must in particular be simple. If a top eigenspace contained two independent full-Schmidt-rank vectors, identify them with invertible3-by-3 coefficient matrices M,N. The complex polynomial det(M+tN) has a root, giving a nonzero vector of Schmidt rank at most two in their span, a contradiction. References of dimension at most two are completely excluded, consistently with the earlier independent qubit-reference theorem.

The unrestricted full-target theorem remains open in the genuinely full-Schmidt-rank-three sector. The generic index-nine certificate is already known to fail, so the index-six proof is not extrapolated to that sector.

## 6. Full entropy theorem for Schmidt-rank-two spectral inputs

If A has an orthonormal eigenbasis in which every eigenvector has Schmidt rank at most two, then Delta(A)>=0. More generally it suffices that every cumulative spectral superlevel projection admit a positive decomposition into rank-one projectors onto Schmidt-rank-at-most-two vectors.

Proof: lower the entire maximal spectral level continuously to the next level, then repeat. On each open segment its derivative in the increasing top-level direction is the sum (or positive weighted sum) of the actual anchored gradients in Section4, after scaling that level to1. Each is nonnegative. The chosen eigenbasis is unchanged, or the cumulative projections remain in their assumed positive rank-two decomposition cone. Thus lowering cannot increase Delta. The finite sequence ends at a scalar multiple of identity or at zero, where Delta=0; singular endpoints follow by entropy continuity. This is the same precise spectral-lowering receiver used previously for product eigenbases.

This full-value class strictly extends the product-eigenbasis theorem and includes every physical two-plus-one block input, because its eigenvectors in the two-dimensional physical block have Schmidt rank at most two and those in the remaining physical line are product vectors. It also includes, for example, arbitrary spectral weights on the orthonormal qutrit-pair basis consisting of |ii> and (|ij>+/-|ji>)/sqrt2, i<j.

It is NOT asserted that every mixed state of Schmidt number at most two has such a spectral decomposition. An arbitrary low-Schmidt-rank convex decomposition need not be orthogonal or respect the spectral superlevel projections; no free mixture lift is used.
