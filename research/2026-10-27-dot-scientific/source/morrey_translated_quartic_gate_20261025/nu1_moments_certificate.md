# Certified moments of the actual contracted cosine law

This is a bounded, deterministic interval proof for the actual law ν₁ = R#ν, where ν is the Haar cosine law. It computes no randomized-peel moments, no optimization, and no trajectory.

## Formula and scope

Let x,y be independent uniform phases in [0,2π]. Set u=cos x, v=cos y, w=cos(x+y), B=−9+8u−4v−4w, C=2u+4u(v+w)−2vw−4(v+w), D=B²+32C, and m=2C/(3√D−B). Then (U,V,W)=(u−m,v+2m,w+2m). The moments use τ=(U+V+2W)/2, y₁=(U−V)/2, y₂=W, and H=y₁²+y₂².

The covariance identity Cov(ν₁)=I/2−sddᵀ, d=(−1,2,2), is a separate exact structural identity supplied by the surrounding argument; this computation certifies s=E[m²] and the requested third/fourth moments. It does not independently prove that covariance identity or any variational conclusion.

## N=1024 endpoints (preserved initial certificate)

| Moment | Lower (outward decimal) | Upper (outward decimal) |
|---|---:|---:|
| s | 0.028079101800725 | 0.036760449643482 |
| m1 | 0.324053194976786 | 0.406767181400578 |
| m2 | -0.117228774408320 | -0.052759232401960 |
| m3_1 | -0.036727676474264 | 0.000486313595061 |
| m3_2 | 0.102645862146987 | 0.156545274037951 |
| m4_1 | -0.067424609795408 | -0.028986384368599 |
| m4_2 | -0.105437357539757 | -0.055755452741006 |
| A4 | 0.858770687170966 | 0.972902676852105 |
| B4 | 0.370400846065272 | 0.440517464588316 |
| C4 | 0.468645263854041 | 0.544378277955197 |

These decimal numbers are rigorously outward-rounded, not nearest rounded. The JSON receipt also gives exact hexadecimal binary64 endpoints and accumulated sum endpoints.

## Verification argument

1. The N² phase boxes have equal normalized Haar mass 1/N². All 1,048,576 boxes were processed, with no exclusions. The cosine endpoint engine is copied unchanged from the earlier cubic certificate: exact rational Machin-formula π bounds, exact rational alternating Taylor cosine bounds, verified outward conversion to binary64, and exact quadrant symmetries. The x+y interval includes two consecutive phase intervals.
2. Every subsequent interval arithmetic operation is enlarged by one binary64 nextafter in the corresponding direction. Multiplication examines all four endpoint products; squares handle intervals crossing zero. Correctly rounded IEEE-754 elementary arithmetic and square root with gradual underflow are assumed. No floating-point trigonometric library is used.
3. The restriction D≥0 is exact on the cosine torus. The Gram matrix A=[[1,u,v],[u,1,w],[v,w,1]] is positive semidefinite, det(A)=0. With L=[[0,−1,2],[−1,0,2],[2,2,0]], det(A+tL)=t(C+Bt−8t²). The nonzero determinant roots are real because L⁻¹A has the same characteristic polynomial as the real symmetric matrix A^(1/2)L⁻¹A^(1/2); hence the quadratic discriminant D is nonnegative. Intersecting its interval with [0,∞) is therefore valid.
4. The denominator interval lower endpoint is positive in every box, with certified minimum 13.041530726661733. Thus every division is valid. Every coordinate endpoint of R is checked within [−2,2]. H is intersected with [0,∞) using its exact sum-of-squares definition.
5. The interval monomials enclose the true summands. Every finite lower and upper endpoint is explicitly checked in [−M,M] using the following fixed power-of-two caps: s:1; m1:64; m2:32; m3_1:32; m3_2:32; m4_1:16; m4_2:16; A4:256; B4:128; C4:64. The JSON records the actual minimum and maximum interval endpoints as well as these caps. No cancellation or sign assumption is used in these caps.
6. Each strip has n=32N summands: 32768 at N=1024 and 65536 at N=2048. For each strip and moment, a bound M n² ε/(1−n ε), ε=2⁻⁵², is rounded upward and subtracted/added to the numerical lower/upper sum. This exceeds the standard γₙ Σ|xᵢ| summation-error bound for any reduction using at most n additions, even using twice the usual unit roundoff. At both permitted resolutions all operations in this error expression before its division are exact powers of two or exact binary differences. The bound also greatly exceeds any possible subnormal absolute summation error.
7. Strip-error subtraction/addition, strip accumulation, and the final normalization by N² are all stepped outward. Averages of interval lower and upper summands therefore certify the expectation bounds. The receipt includes exact hexadecimal accumulated sums for reproducibility.

## Reproduction

Run `python certify_nu1_moments.py 1024` from this directory. The only implemented resolutions are 1024 and 2048; no automatic refinement or iteration occurs. Both N=1024 and the single requested N=2048 refinement have separately saved receipts. The enclosing script is standalone, not an import from another mutable file.

Recorded runtime: 1.4848 seconds. Python 3.12.14, NumPy 2.3.5. No assertion failed.

## Single requested N=2048 refinement

The parent requested this one refinement after the downstream exact interval-Bernstein attempt with N=1024 reported four positive coefficients but a first coefficient approximately −0.176 even for zero target gap. This is failure of that interval lower bound, not a negative true polynomial. The initial N=1024 receipt is retained unchanged. The downstream failed-bound evidence is maintained by the parent, not recomputed here.

| Moment | Lower (outward decimal) | Upper (outward decimal) |
|---|---:|---:|
| s | 0.029597702709571 | 0.034120184620198 |
| m1 | 0.347587901210022 | 0.388807524937471 |
| m2 | -0.098122491480810 | -0.065486171651929 |
| m3_1 | -0.030104635620703 | -0.011226635825176 |
| m3_2 | 0.118518585374826 | 0.145625502812799 |
| m4_1 | -0.060671283448878 | -0.040839816386600 |
| m4_2 | -0.090587663196669 | -0.065171009952065 |
| A4 | 0.882091355215203 | 0.938446396322935 |
| B4 | 0.381996235075972 | 0.417094070011831 |
| C4 | 0.480600824593016 | 0.519452004970475 |

All 4,194,304 phase boxes were covered, with no omitted boxes. Minimum denominator lower endpoint: 13.330973265275073. Runtime: 4.1811 seconds. All interval summand assertions passed. The identical standalone script and proof apply with N=2048; no additional moment or randomized law was integrated.

No further refinement was performed or scheduled.
