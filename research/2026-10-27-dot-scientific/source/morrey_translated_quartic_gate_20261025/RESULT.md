# All translations of the admitted quartic family are excluded as separators

25 October 2026. This is a completed, bounded discriminator for the ACTUAL contracted laws. It is not a full Morrey resolution or proof that those laws are laminates.

## Certified result

For every real 2-by-2 background A and every a in [-1,1], define

    W_a(X)=|X|_F^4+4a |X|_F^2 det X+(6a^2-2)(det X)^2.

For the actual full first root nu_1 of the correlated cosine law,

    integral W_a(A+B(z)) dnu_1(z)-W_a(A) > 1.

The SAME strict bound holds for the actual first randomized-and-ball-peeled law

    eta=omega delta_0+[f(z)-m0 1_(B_R)(z)] dz,
    R=sqrt(3)/2, m0=1/(10pi^2), omega=sqrt(3)/(20pi).

Its normalized continuous residual has gap greater than 1/(1-omega), hence also greater than 1. The statements include nonsymmetric backgrounds and parameter-endpoint sequences whose optimizing backgrounds diverge to infinity.

Thus no member of this entire translated, untransformed quartic family rejects either specified contraction branch. Arbitrary physical left/right anisotropic transforms are NOT covered. Nor is the later freshly renewed-and-repeeled descendant silently substituted for eta.

## 1. Global admission is independently proved

The family is globally rank-one convex for |a|<=1. For X=[[x,b],[c,y]], direct differentiation gives

    (1/2) D^2 W_a(X)[E11,E11]
      =6(x+a y)^2+2(b-a c)^2+2(1-a^2)c^2>=0.

Every rank-one direction can be brought to a multiple of E11 by left/right SO(2) rotations, which preserve |X|_F and det X. This proves global admission, including all translations, without relying on sampled Hessians or on the separate quasiconvexity theorem cited by the recovered source.

## 2. Only ten source moments are needed

Use the exact first-root map from the preceding positive-contraction packet. For its coefficient random vector (U,V,W), put

    tau=(U+V+2W)/2, y=((U-V)/2,W), H=|y|^2.

The needed moments are

    s=E shift^2,
    m1=E tau^3, m2=E tau H,
    m3=(E tau^2 y1,E tau^2 y2),
    m4=(E H y1,E H y2),
    A4=E tau^4, B4=E tau^2 H, C4=E H^2.

The second moments are not separately estimated: the exact covariance identity is

    Cov(nu_1)=I/2-s d d^T,  d=(-1,2,2), 0<s<1/18.

The certified integrator uses the unchanged source (cos x,cos y,cos(x+y)), not independent three cosines. It applies the exact weighted root formula on every Haar-phase box. The certificate first used N=1024, whose moment box was too broad for the final polynomial bound. One bounded refinement to N=2048 succeeded. No background or parameter grid was used in the proof.

All 4,194,304 boxes are enclosed, none omitted. The minimum certified denominator lower bound is 13.330973265275073. The rational-trigonometric/outward-rounded engine and each summand/summation bound are documented in nu1_moments_certificate.md. Exact hexadecimal moment endpoints are in nu1_moments_N2048.json. An independent rerun reproduced every endpoint exactly.

## 3. A stronger proxy covers both actual laws

Direct conditional Jensen on the actual original d-chords gives

    nu_1 <=rc nu_uniform.

The uniform coefficient ball sigma_R is a laminate by three coordinate conditional-Jensen contractions. Therefore its translated W_a gap G_ball(A) is nonnegative. Since omega<1/30,

    G_eta(A) >= G_nu1(A)-omega G_ball(A)
             >= G_nu1(A)-(1/30)G_ball(A).

The same right-hand side is also a lower bound for G_nu1. We certify this stronger common lower bound. It is only a signed-moment expression, NOT an asserted positive law.

Its coefficient covariance is

    C_proxy=(99/200)I-s d d^T.

Its third moments are unchanged. Its fourth conformal moments are

    A4_proxy=A4-81/22400,
    B4_proxy=B4-51/22400,
    C4_proxy=C4-57/22400.

These are exact uniform-ball fourth-moment subtractions. Thus no additional integration over the random contraction amount or over the peeled density is required.

This argument uses an explicitly proved order between these particular intermediate laws. It does not infer that every downward contraction of a laminate remains a laminate.

## 4. Exact elimination of every full background

The full derivation and endpoint treatment are in ALL_BACKGROUND_REDUCTION.md. Briefly, write

    A=[[t+p,h+r],[h-r,t-p]],    b=(p,h),
    alpha=2(a+1)(3a+1), beta=12(1-a^2), gamma=2(a-1)(3a-1).

For the proxy set h0=99/200 and

    m=3h0/2-25s/4,
    c=(15s/4,h0-5s),
    M=[[h0/2-9s/4,3s],[3s,h0-4s]],
    k(a)=alpha A4_proxy+beta B4_proxy+gamma C4_proxy,
    L=(3a+1)m1+3(1-a)m2,
    N=3(1+a)m3-(3a-1)m4,
    D=2mI-(3a-1)M-3(1-a)cc^T/m.

The skew-background contribution is 16m(a+1)r^2>=0, with no mixed or linear term. Set x=(1+a)t and complete both remaining squares. A lower bound for every background is

    F(a)=k(a)-(2/3)L^2/m
         -2(1-a)(N-Lc/m)^T D^(-1)(N-Lc/m).

For -1<a<1 it is the exact minimized proxy gap. At a=-1 the rescaling allows an additional free x, giving a valid lower bound for the actual endpoint and correctly controlling backgrounds escaping to infinity as a tends to -1. Ignoring this endpoint phenomenon would be an invalid compact-background shortcut.

The underlying square identity is valid even at both endpoints, without dividing by 1+a or 1-a. With v0=N-Lc/m, it is

    G_proxy(A)-delta
      =24m[x+L/(6m)+(1-a)c^T b/m]^2
       +8(1-a)[b+(1/2)D^(-1)v0]^T D [b+(1/2)D^(-1)v0]
       +16m(1+a)r^2 + P_delta(a)/(3m det(mD)).

This also supplies a direct positivity proof without assuming that the exact minimized gap is continuous at the degenerate endpoint.

Uniform denominator positivity is analytic, not inferred from the quadrature:

    m>=1423/3600>0,   D(a,s)>(1/50)I

for all -1<=a<=1, 0<=s<=1/18. Matrix concavity in s and affinity in a reduce this to four exact 2-by-2 corner checks, recorded in the algebra receipt.

## 5. One quartic polynomial proves the whole interval

Put E=mD and v=mN-Lc. To prove F(a)>1, form

    P(a)=[3m(k(a)-1)-2L(a)^2] det E(a)
         -6(1-a) v(a)^T adj(E(a)) v(a).

This is a polynomial of degree at most four, and

    F(a)-1=P(a)/(3m det E(a)).

The denominator is positive. Exact rational interval arithmetic encloses the five degree-four Bernstein coefficients of P(2x-1), x in [0,1], directly from the certified moment intervals. The lower endpoints are approximately

    1.8866952118745164,
    1.6898266693751172,
    1.7889115025140410,
    1.2739923402645006,
    0.5921539941833247.

The stored proof uses their exact rational values, not these displayed decimals. Every coefficient exceeds 59/100. Since Bernstein basis functions are nonnegative and sum to one, P(a)>59/100 throughout [-1,1]. This proves the claimed strict gap greater than 1 for all parameters and all backgrounds at once.

The exact rational computation was independently reviewed and rerun. No parameter subdivision was needed; no optimizer, background sweep, anisotropic transform scan, or sampled negative was used to certify the result.

## 6. Reproduce and scope

    python check_all_background_reduction.py
    python certify_nu1_moments.py 2048 > nu1_moments_N2048.rerun.json
    python certify_background_bernstein.py nu1_moments_N2048.json 1 background_bernstein_N2048.json

These commands run from this packet directory. The standalone moment script includes the prior exact-rational trigonometric and outward interval routines; its source hash is included in SHA256SUMS. The original N1024 receipts and their failed interval-polynomial bounds remain preserved; their failure was an insufficient enclosure, not a negative Jensen gap.

This closes the requested translated-quartic discriminator. It does not prove a positive null stress from the origin to either residual, does not exclude other globally admitted integrands or anisotropic quartic pullbacks, and does not resolve full Morrey. The prior atom peel, exterior renewal, and their same-direction obstruction remain unchanged.
