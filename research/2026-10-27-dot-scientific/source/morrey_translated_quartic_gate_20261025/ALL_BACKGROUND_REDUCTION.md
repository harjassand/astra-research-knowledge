# Exact all-background reduction for the admitted planar quartics

25 October 2026. This is an algebraic reduction, not a sampled search. It applies to the actual first conditional-root law and, through the explicit inequality below, the actual randomized-and-ball-peeled law. Numerical moment certification is a separate obligation.

## 1. Coordinates and exact gap

Write every real 2 by 2 background, including nonsymmetric ones, uniquely as

A = [[t+p,h+r],[h-r,t-p]].

For the symmetric random increment X=B(u,v,w), put

τ=(u+v+2w)/2, y=((u-v)/2,w).

Let m=Eτ²=E|y|², c=E(τy), M=E(yyᵀ), and let

m1=Eτ³, m2=E(τ|y|²), m3=E(τ²y), m4=E(|y|²y).

The equality defining m is exactly E det X=0. Mean zero is also required. Set

α=2(a+1)(3a+1), β=12(1-a²), γ=2(a-1)(3a-1).

Then W_a=α(t²+r²)²+β(t²+r²)(p²+h²)+γ(p²+h²)². Its translated expectation gap is exactly

G_a(A)=k(a)+zᵀQ(a)z+ℓ(a)ᵀz+16m(a+1)r²,

where z=(t,p,h), k(a)=E W_a(X),

Qtt=24m(a+1)²,
Qt,y=24(1-a)(1+a)cᵀ,
Qy,y=8(1-a)[2m I-(3a-1)M],

ℓt=8(a+1)L,
ℓy=8(1-a)N,
L=(3a+1)m1+3(1-a)m2,
N=3(1+a)m3-(3a-1)m4.

All terms here follow by polynomial expansion; no convexity premise was used. The formula remains valid for a signed moment functional of total mass one, mean zero and determinant moment zero.

The skew coordinate has no linear or mixed term. For -1<a≤1 its unique minimizing value is r=0, provided m>0. At a=-1 it is flat. In particular, optimizing only symmetric backgrounds is justified only after this calculation, not as an assumption.

## 2. Stable elimination and parameter endpoints

For -1<a<1 set x=(1+a)t. Completing the square in x and then in b=(p,h) gives

D(a)=2m I-(3a-1)M-3(1-a)ccᵀ/m,
v(a)=N-Lc/m,

F(a)=inf_A G_a(A)
    =k(a)-(2/3)L²/m-2(1-a)vᵀD(a)^{-1}v,

provided D(a) is positive definite. The minimizing background is

b*=-(1/2)D(a)^{-1}v,
x*= -L/(6m)-(1-a)cᵀb*/m,
t*=x*/(1+a), r*=0.

The correct unrestricted quadratic criterion is Q positive semidefinite and ℓ in its range; otherwise the infimum is minus infinity. When it holds, the value is k-ℓᵀQ^+ℓ/4, and all optimizers are -Q^+ℓ/2+ker Q. The present D bounds below give the stronger positive-definite condition for every interior parameter.

At a=1 the exact endpoint is W_1=16(t²+r²)². The p,h directions are flat, and

inf_A G_1(A)=k(1)-(32/3)m1²/m,
t*=-m1/(3m), r*=0.

The continuous extension of F to a=1 equals this value.

At a=-1 the exact endpoint is W_-1=16(p²+h²)². The t,r directions are flat. Its actual minimum is

inf_A G_-1(A)=k(-1)-32m4ᵀ(m I+2M)^{-1}m4,
b*=-(m I+2M)^{-1}m4.

The interior F(-1+) need not equal this endpoint value: the change of variables x=(1+a)t ceases to be invertible at a=-1. A finite nonzero x can be approached by t diverging as 1/(a+1). Consequently the extension F(-1) obtained by allowing x free is a valid lower bound for the actual endpoint, not necessarily its value. Certifying the extended F on the closed interval is sufficient and also covers noncompact background limits. No continuity assertion for the exact minimized value at -1 is warranted.

## 3. Covariance, symmetry, and the exact first-root quadratic

For coefficient covariance C=h0 I-s ddᵀ with d=(-1,2,2), direct transformation gives

m=3h0/2-25s/4,
c=(15s/4,h0-5s),
M=[[h0/2-9s/4,3s],[3s,h0-4s]].

For the actual first-root law h0=1/2 and 0<s<1/18. Then

Qtt=6(a+1)²(3-25s),
Qtp=90s(1-a)(a+1),
Qth=12(1-a)(a+1)(1-10s),
Qpp=2(1-a)(27as-3a-59s+7),
Qph=-24s(1-a)(3a-1),
Qhh=4(1-a)(24as-3a-33s+4).

Q is affine in s. At s=1/18 its leading principal minors are

29(a+1)²/3,
4(1-a)(a+1)²(317-27a)/27,
232(1-a)²(a+1)²(29-27a)/27.

They are strictly positive for -1<a<1. The s=0 minors are likewise strictly positive, so convexity of the positive-definite cone proves the interior assertion for the entire stated s interval. At a=-1,

Q=diag(0, [[40-344s,192s],[192s,56-456s]]),

and at a=1, Q=diag(72-600s,0,0). The linear terms automatically vanish on these nullspaces.

The actual first-root law has coefficient symmetry v↔w, since the original cosine law and its exact d-root operation have that symmetry. This reduces the independent cubic moments to

c300=Eu³, c030=Ev³=Ew³,
c210=Eu²v=Eu²w, c120=Euv²=Euw²,
c021=Ev²w=Evw², c111=Euvw.

In these terms,

m1=(c300+9c030+9c210+15c120+18c021+12c111)/8,
m2=(c300+9c030+c210+3c120+6c021-4c111)/8,
m3_p=(c300-c030+5c210+3c120-8c021)/8,
m3_h=(c210+4c030+4c120+5c021+2c111)/4,
m4_p=(c300-c030-3c210+7c120-4c021)/8,
m4_h=(c210+4c030+c021-2c111)/4.

This symmetry does not discard a background coordinate. Its action on B is a nonorthogonal congruence, not a left/right orthogonal invariance of W_a. One must not set p,h, or t to zero from v↔w alone.

## 4. Actual peeled-law reduction without integrating its density

Let σ be uniform on the coefficient ball of radius sqrt(3)/2 and ω=sqrt(3)/(20π)<1/30. Conditional rank-one Jensen on the actual original chords gives ν1≤rcνuniform, directly. For every translated W_a,

G_peeled(A) ≥ G_ν1(A)-ωG_σ(A).

The coefficient ball is a laminate: successively collapse each coordinate by its centered conditional law; each coordinate direction is sent by B to a rank-one matrix. Hence G_σ(A)≥0. It follows that

G_peeled(A) ≥ G_ν1(A)-(1/30)G_σ(A).

The expression on the right is only a signed-moment proxy. It is not asserted to be the gap of a positive measure. Its moments fit the preceding algebra with

h0=1/2-(1/30)(3/20)=99/200,
s unchanged, all cubic moments unchanged,
k(a)=k_ν1(a)-(333+72a+81a²)/8400.

The ball quartic used here is (333+72a+81a²)/280, and its coefficient covariance is (3/20)I. This exact upper replacement of ω is legitimate because the entire translated ball gap, not only its origin value, is nonnegative.

For comparison, the actual uniform-partial law has covariance I/2-(2s/3)ddᵀ, and the actual peeled law has covariance (1/2-3ω/20)I-(2s/3)ddᵀ. Neither is substituted for the signed proxy.

## 5. Uniform denominator certificate for the proxy

For h0=99/200, 0≤s≤1/18 and -1≤a≤1,

m≥1423/3600>0, and D(a,s)>(1/50)I.

Indeed, D is affine in a. For fixed a≤1 it is matrix-concave in s: m,M,c are affine and ccᵀ/m is matrix-convex for m>0. Thus it suffices to check the four corners. They are

D(-1,0)=diag(99/40,297/200),
D(1,0)=diag(99/100,99/200),
D(1,1/18)=[[491/900,-1/3],[-1/3,49/200]],
D(-1,1/18)=[[318503/512280,-173/8538],[-173/8538,331681/284600]].

The corresponding determinants after subtracting I/50 are, in that order,

143863/40000, 1843/4000, 257/36000, 352876541/512280000.

Their leading entries are positive. The same lower bound applies to the unpeeled root covariance h0=1/2: increasing h0 adds a positive-semidefinite laminate second-moment Hessian; alternatively its corners can be checked directly. Only the proxy bound is needed to cover both laws, because its certified positive gap and G_ball≥0 also imply the root gap is positive.

## 6. One quartic polynomial certifies every parameter and background

Define H=mD and V=mN-Lc. All their entries, as well as L and N, are affine in a. Then

F(a)=P(a)/(3m det H),

P(a)=[3m k(a)-2L(a)²] det H(a)
     -6(1-a)V(a)ᵀ adj(H(a)) V(a).

P has degree at most four. The denominator is strictly positive by Section 5. To certify F≥δ replace k(a) with k(a)-δ in P. Given certified intervals for the third and fourth moments and s, interval polynomial arithmetic encloses its five power coefficients. Substitute a=2x-1 and convert to degree-four Bernstein coefficients

b_k = sum_{j=0}^k binom(k,j)/binom(4,j) p_j,

where p_j are the power coefficients of P(2x-1). Positive lower endpoints for all b_k certify P>0 on all x∈[0,1]. If necessary, exact rational de Casteljau subdivision yields a finite-domain certificate, not a sampling argument or an anisotropic/background sweep.

The square-completion certificate can be stated without any endpoint change of variables: with x=(1+a)t and b=(p,h),

G(a,A)-δ = 24m[x+L/(6m)+(1-a)cᵀb/m]²
          +8(1-a)[b+D⁻¹v/2]ᵀD[b+D⁻¹v/2]
          +16m(1+a)r²+Pδ(a)/(3m det H).

It is an exact identity on the closed parameter interval, including a=-1 and a=1. Therefore positive Bernstein coefficients prove positivity even at both degenerate endpoints without any continuity argument.

This reduction covers arbitrary full 2 by 2 translations for this untransformed admitted quartic family. It does not cover independent physical anisotropic pullbacks or other admitted nonquartic sources, and establishes no general laminate-completion theorem.
