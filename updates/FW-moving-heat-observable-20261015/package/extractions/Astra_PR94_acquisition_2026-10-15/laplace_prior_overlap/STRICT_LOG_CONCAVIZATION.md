# Scalar KV multiplier: strict log-concavization and Gaussian obstruction

Status: explicit internal analytic deductions, not externally reviewed theorems or novelty claims. No canonical edits. Based on the verified Katkova–Vishnyakova theorem, whose institutional primary text is https://ekhnuir.karazin.ua/bitstreams/41e252c6-eba5-435f-bbbb-66a8582ace7e/download .

## Main outcome

Within the scalar input class admitted by KV Theorem 1 or 2, the full combination of a smooth even strictly log-concave all-exponential-moment probability kernel and everywhere-strict positive output follows by postprocessing their multiplier. Thus strict log-concavity is also not a remaining separation within that class. This does not settle arbitrary signed compact distributions, multidimensional radiality, matrix/Banach-cone scope, or Diamond–Essén priority.

The tempting Gaussian postprocessing is insufficient: a nontrivial symmetric compound-Poisson lattice law convolved with any finite-variance Gaussian is not log-concave. Both claims are proved below.

## 1. Setup

Fix λ,h>0. Let ν be the law of hN with N Poisson(λ), and η=ν*ν̌, the law of Y=h(N_+−N_−) for independent Poisson(λ) variables. If KV supplies f*μ≥0, its normalized multiplier ν=e^{−λ}μ gives q=f*ν≥0 with total mass L_f(0)>0.

Choose a>0 so α=ah≤1/4. For R>0 define

V_R(x)=a[x asinh(x/R)−sqrt(R²+x²)+R],
κ_R(x)=Z_R^{-1} exp(−V_R(x)),
p_R=η*κ_R.

Then V_R is even, smooth, strictly convex, with

V_R'(x)=a asinh(x/R),
V_R''(x)=a/sqrt(R²+x²).

V_R(x)/|x|→∞. Consequently κ_R is a smooth strictly positive probability density with every absolute exponential moment. Every derivative has this property as well, since derivatives are κ_R times combinations of logarithmically growing V_R' and bounded higher derivatives. The same smoothness, positivity, moments, and weighted derivative integrability pass to p_R by convolution. Both η and κ_R are symmetric, so p_R is even (radial in one dimension).

## 2. Explicit sufficient scale

Set

B=2λ·2^α,
C2=h²(B²+B),
C4=h⁴(B⁴+6B³+7B²+B),
D0=√2 a C2/R+2a C4/R³,
P0=4C2/R².

Choose any R large enough that

D0+P0≤1/2,
16a C2/R+8a C4/R³≤1/6.

These explicit inequalities are satisfiable for all λ,h>0. Then, for every real x,

(log p_R)''(x)≤−a/[6(R+|x|)]<0.

## 3. Proof of the global curvature bound

Fix x, put c=R+|x|, t=c/R≥1, and s=V_R'(x). Let P_s be the exponential tilt of η by e^{sY}. Under P_s, N_+,N_− are independent Poisson variables of means λe^{hs}, λe^{−hs}. Their sum has Poisson mean

m=2λ cosh(hs)≤2λ exp(α asinh(|x|/R))≤B t^α.

Since |Y|≤h(N_++N_−), the exact second and fourth moments of a Poisson variable imply

E_s Y²≤C2 t^{2α},
E_s Y⁴≤C4 t^{4α}.

Define the nonnegative convexity remainder

D(Y)=V_R(x−Y)−V_R(x)+sY≥0.

The conditional law ρ_x of Y in the convolution p_R(x) has Radon–Nikodym density e^{−D}/Z_x relative to P_s, with Z_x=E_s e^{−D}≤1.

Let A={|Y|≤c/2}. On each line segment from x to x−Y with Y∈A,

R+|x−u|≥c−|u|≥c/2,
sqrt(R²+(x−u)²)≥(R+|x−u|)/√2≥c/(2√2).

Therefore

D(Y)≤√2 aY²/c on A,
|V_R'(x−Y)−s|≤2√2 a|Y|/c on A.

Globally, V_R''≤a/R, so D(Y)≤aY²/(2R) and |V_R'(x−Y)−s|≤a|Y|/R. Also

E_s[Y² 1_{A^c}]≤4 E_sY⁴/c²,
P_s(A^c)≤4 E_sY²/c².

Combining these estimates, and using α≤1/4 and t≥1, gives

E_sD≤√2 a C2/R·t^{2α−1}+2a C4/R³·t^{4α−2}≤D0,
P_s(A^c)≤4C2/R²·t^{2α−2}≤P0.

Hence Z_x≥1−D0≥1/2 and

E_s[e^{−D}1_A]≥1−E_sD−P_s(A^c)≥1/2.

On A, sqrt(R²+(x−Y)²)≤R+|x−Y|≤3c/2; consequently

E_{ρ_x} V_R''(x−Y)≥(2a/(3c)) E_s[e^{−D}1_A]/Z_x≥a/(3c).

The variance is bounded using the fixed center s:

Var_{ρ_x}(V_R'(x−Y))
≤E_{ρ_x}(V_R'(x−Y)−s)²
≤Z_x^{-1}[8a² C2/R²·t^{2α−2}+4a² C4/R⁴·t^{4α−2}]
≤(a/c)[16a C2/R·t^{2α−1}+8a C4/R³·t^{4α−1}]
≤a/(6c).

Differentiating the convolution under its integral gives the exact identity

(log p_R)''=−E_{ρ_x}V_R''(x−Y)+Var_{ρ_x}(V_R'(x−Y)).

All differentiations are justified by the smooth superlinear-tail kernel and finite exponential moments of η. Substitution proves the claimed strictly negative bound.

## 4. Consequence for KV inputs

For any input f admitted by KV, use its λ,h and the construction above. Then

f*p_R=(f*ν)*ν̌*κ_R=q*ν̌*κ_R>0

at every real x, since q*ν̌ is a nonzero finite positive measure and κ_R is positive everywhere. Thus p_R has all the requested one-dimensional scalar kernel properties, including strict log-concavity. This uses KV only for q≥0; Sections 1–3 are an elementary additional argument. Its mathematical correctness remains subject to independent checking.

## 5. Gaussian postprocessing fails at every finite variance

Let η have mass w_k at hk, k∈Z. Its explicit series is

w_k=e^{−2λ} λ^{|k|}/|k|! ·r_{|k|},
r_m=Σ_{l≥0} λ^{2l}m!/[l!(m+l)!].

For m≥0, 1≤r_m≤exp(λ²/(m+1)), so r_m→1. Fix σ>0 and let g=η*γ_σ. For n≥1 and real r define

x_n=hn+(σ²/h)log(n/λ)+r.

Relative to the term k=n in g(x_n), the term k=n+j has weight

A_{n,j} exp(hrj/σ²−h²j²/(2σ²)),
A_{n,j}=(w_{n+j}/w_n)(n/λ)^j.

For every fixed integer j, A_{n,j}→1. There is also a bound uniform in n,j: A_{n,j}≤exp(2λ²). To see this, for n+j≥0, the factorial product inequality n!/(n+j)!≤n^{−j} gives A_{n,j}≤exp(λ²). For n+j=−m<0,

A_{n,j}≤exp(λ²) λ^{2m}n!/[m! n^{n+m}]
≤exp(λ²) (λ²/n)^m/m!≤exp(2λ²).

Gaussian domination now gives convergence of the posterior law of j and its first two moments to weights proportional to

exp(hrj/σ²−h²j²/(2σ²)).

The convolution derivative identity implies

(log g)''(x_n)→−1/σ²+(h²/σ⁴) Var_r(j)=(log H)''(r),

where H(r)=Σ_{j∈Z}exp(−(r−hj)²/(2σ²)). H is a positive smooth h-periodic nonconstant function. Nonconstancy follows, for example, because its first Fourier coefficient is proportional to exp(−2π²σ²/h²)>0 (obtained by integrating the Gaussian over the tiled real line). A nonconstant smooth periodic log H cannot have second derivative everywhere nonpositive: its second derivative integrates to zero over a period, and a continuously concave periodic function is constant. Thus (log H)''(r)>0 somewhere. At that r, (log g)''(x_n)>0 for all sufficiently large n. Hence g is not log-concave for any finite σ.

This argument applies to λ,h>0; the degenerate λ=0 case is simply Gaussian and is excluded.

## 6. Limits and literature search

A targeted search surfaced general reviews and work on convolution partners preserving log-concavity, but no verified prior theorem establishing the precise all-exponential-moment strict-log-concavization statement here. No such theorem is being attributed to those search results. The broader question for every arbitrary all-exponential-moment probability measure is NOT settled by this note: the proof crucially uses polynomial growth in t of tilted Skellam moments. It does settle the bounded KV multiplier question without reconstructing the general N853 distribution/cone theorem.
