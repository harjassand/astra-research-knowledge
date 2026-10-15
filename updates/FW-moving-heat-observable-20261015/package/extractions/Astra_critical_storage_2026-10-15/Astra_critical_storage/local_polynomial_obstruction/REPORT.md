# No nonzero constant-coefficient local quartic storage of derivative weight three

15 October 2026. An independently checked obstruction; no historical novelty claim is made.

## Precise theorem

Let X be the mean-zero real vector space W^{3/4,4}(R/(2πZ);R²), with its strong norm topology. For smooth U consider

F(U)=average_y p(U,U′,U″,U‴),

where p is a real constant-coefficient polynomial, homogeneous of polynomial degree four and homogeneous of derivative weight three (a factor U^{(j)} has weight j). Suppose F is invariant under constant target rotations SO(2). If F extends to a continuous real-valued function on X, then F is identically zero on smooth traces. For an SO(2)-invariant density, this also says its class modulo total derivatives is zero. If invariance is assumed only of the functional, this conclusion applies to its group-averaged density representative.

This is a theorem about the stated polynomial ansatz. It does not exclude nonlocal storage, nonpolynomial local expressions, additional state variables, or discontinuous functionals. Variable coefficients depending on y are not included. A nonzero density which is itself a total derivative defines the zero functional and is not excluded.

## 1. Complete classification modulo integration by parts

Write A=U, B=U′, C=U″, D=U‴, and let brackets denote normalized periodic integration. Define

Pdot=[(A·B)|B|²],
Pdet=[det(A,B)|B|²],
P2=[|A|² det(B,C)].

If only F, rather than p, is rotation invariant, average p over SO(2). This produces an invariant polynomial with the same functional, degree and derivative weight. Thus it suffices to classify invariant densities.

Every invariant four-linear tensor on copies of R² is spanned by pairings made from dot products and determinants. One direct proof uses complex coordinates: under a rotation z→exp(iθ)z, a degree-four invariant monomial has exactly two z factors and two conjugate factors. Pair z with a conjugate z; the real and imaginary parts of each such pair are dot products and determinants. Products of two determinants reduce to dot-product pairings by the two-dimensional determinant identity. This proof also covers repeated vector arguments by polarization.

The only derivative partitions are 0003, 0012 and 0111. Consequently the following lists span their invariant densities:

- 0003: |A|²(A·D), |A|²det(A,D).
- 0012, reflection-even: E1=|A|²(B·C), E2=(A·B)(A·C).
- 0012, reflection-odd: F1=|A|²det(B,C), F2=(A·B)det(A,C), F3=(A·C)det(A,B).
- 0111: (A·B)|B|², det(A,B)|B|².

The pointwise identity F1=F2−F3 and periodic integration of derivatives give

[E1]=[E2]=−Pdot,
[|A|²(A·D)]=3Pdot,
[F1]=P2,
[F2]=(P2−Pdet)/2,
[F3]=−(P2+Pdet)/2,
[|A|²det(A,D)]=Pdet−2P2.

For completeness, these follow by differentiating respectively |A|²|B|², (A·B)², |A|²(A·C), (A·B)det(A,B), and |A|²det(A,C). Each relation is an actual polynomial total-derivative identity, not merely an assertion about a selected family of traces.

Therefore F=aPdot+bPdet+cP2. The tests below also prove that these three functional classes are linearly independent on mean-zero smooth traces.

## 2. Exact Fourier tests

All formulas here hold for every integer n≥5 and every real h. Frequencies are integers and every displayed trace has zero mean.

### Circle plus high circle

U=(cos y,sin y)+h(cos ny,sin ny).

Pdot=0,
Pdet=1+2h²n+2h²n²+h⁴n³,
P2=1+h²+h²n+h²n²+h²n³+h⁴n³.

### Scalar resonance

U=(sin y+h cos ny+h cos((2n+1)y),0).

Pdot=(3/4)h³n(n+1)²,
Pdet=P2=0.

### Determinant resonance

U=(sin y+h cos ny,h cos((2n+1)y)).

Pdot=0,
Pdet=(1/4)h³n(n²+4n+1),
P2=−(1/4)h³(2n+1)(3n²+2n+1).

The accompanying checker uses exact Gaussian-rational Fourier coefficients and formal frequencies an+b. Every quartic term has |b|≤4. Hence for n≥5, an+b=0 implies a=b=0: there are no accidental constant-frequency collisions. Derivatives multiply a coefficient by i(an+b) and do not change this bound. The checker additionally collapses to ordinary integer frequencies for several n and verifies the same exact formulas independently of the formal-frequency extraction.

## 3. Strong convergence and coefficient elimination

Fix any ε with 0<ε<1/4 and set h=n^{−3/4−ε}. For 0<s<1 the elementary Slobodeckij estimate

||sin(ky)||_{W^{s,4}}+||cos(ky)||_{W^{s,4}} ≤ C_s(1+|k|^s)

follows by bounding a translation difference by C min(1,|k|t) and integrating its fourth power against t^{−1−4s}dt. Splitting at t=1/|k| proves the estimate directly. Thus all the high-frequency perturbations above have W^{3/4,4} norm O(n^{−ε}) and tend strongly to zero. This is a finite-sum estimate; no orthogonality in a fractional L4 norm is assumed.

Apply continuity to the first family at the fixed circle. The difference F(U)−F(circle) must tend to zero. Divide it by h²n³=n^{3/2−2ε}, which tends to infinity. The Pdet difference divided by h²n³ tends to zero, while the P2 difference divided by h²n³ tends to one. Therefore c=0. The term h⁴n³ causes no difficulty: after division it is h²→0 (and it itself tends to zero).

Apply continuity to the scalar family at (sin y,0). Since h³n³=n^{3/4−3ε}→infinity, its exact formula forces a=0.

Finally apply continuity to the determinant family at the same base. With c=a=0, its exact Pdet formula and h³n³→infinity force b=0. This proves the theorem. In particular, continuity fails at one of two fixed smooth mean-zero traces for every nonzero class; the assertion is stronger than failure of a uniform bound over a rough ball.

## 4. Consequence and limits for the storage problem

If the intended storage is known independently to be strongly continuous on this critical trace space, any representation by a density of exactly the stated local homogeneous kind must be zero. If the intended storage is nonzero, this excludes that representation.

The prerequisite report at ../critical_storage_construction/REPORT.md states that full required supply is finite and strongly continuous, and supplies a negative-action incoming path for a circular endpoint. Taking that report's underlying storage theorem and action certificate as prerequisites, full required supply is nonzero; the present obstruction therefore applies to it. The present argument does not independently re-prove those prerequisites or identify the required supply.

No claim is made that a scaling argument alone forces all possible local representations into this ansatz. In particular, lower/higher derivative weights, variable coefficients, nonsmooth or rational densities, or a cancellation involving other classes require separate analysis.

## Replay

Run `python check.py` in this directory. SymPy is the only dependency. It verifies the three exact Fourier identities, absence of relevant formal-frequency collisions for n≥5, ordinary-frequency cross-checks, and all listed integration-by-parts identities as exact polynomial equalities. No floating-point acceptance tests are used.
