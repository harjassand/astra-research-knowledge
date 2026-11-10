# P1 completed return — original quartic continuation

Chat: https://chatgpt.com/c/6af2bc39-2f58-83ec-b26b-3a99e1d2c0f2. Original question turn b52f414e-ac5d-429e-90de-491405e1be50; continuation turn 8f5285b0-f3b8-42e5-8a4b-3663f549ba2c; assistant final cfea80c7-fee8-50f5-9768-2212f9cdf6fa. UI displayed Pro and response complete.

Exact held question: work/astra-renewed-pro-programmes-20261103/P1_FULL_QUARTIC_SHARP_COMPATIBLE_LIFT_CONTINUATION_PRO_20261110.txt (SHA-256 ce797add36f6086f349b29b69a2c729e4df00070ce9a9a69cb8340b48496a44b).

Full available final below was copied via response Copy and TextEdit accessibility; its formatting is not asserted to equal native bytes. The native reader's first 20,000 characters are included below. Expanded current-turn activity is included as available; the browser accessibility history is virtualized and may omit some. Original producer ZIP copied unchanged and uninspected: P1_PRO_CFEA80_ORIGINAL_20261110.zip (SHA-256 e5757716b0f1da04796019c31a6fd6fc6213b038665cf3d68dce7ccaca07cf2e).

## Full response (UI copy)

**I continued, but I have not resolved the full universal inequality.** I have neither a proof for every compatible \(D\phi\) nor an admissible field with a negative original-energy gap.
This continuation completed an exact classification of a proposed convex generator, extended the outer-affine mean reduction to variable Jacobians, and produced small exact certificates excluding two specific lifting/certificate constructions. It also made the obstruction in the pressure approach more concrete and strengthened the earlier radial argument.
The complete proofs, constructions, exact certificates, and computation records are in the <u>[updated research packet](chatgpt.com/library?file_id=libfile_6d1aa4e4e9f08191bc79875c2b2752c0&account_id=personal)</u>. The NONLINEAR_AND_GLOBAL_MEAN_CONTINUATION.txt distinguishes these results from the earlier accepted capital.
**1. Exact convexity classification for a proposed nonlinear generator**
Consider the additional quartic
\[ W_k(F)=(u+v-2j)(k^2u+v+2kj) \]
and the proposed generator
\[ V_{k,s}=J_k+sW_k. \]
I obtained the complete answer to its **ordinary matrix convexity** question:
\[ \boxed{ \exists s\in\mathbb R\text{ such that }V_{k,s}\text{ is convex} \quad\Longleftrightarrow\quad k(3k+5)^2\ge32. } \]
Let \(k_*\) be the unique positive root of
\[ 9k^3+30k^2+25k-32=0. \]
Then
\[ k_*\approx0.657961495631632. \]
For every \(k\ge k_*\), an explicit working coefficient is
\[ \boxed{ s_*(k)=\frac{9k^2+25k-2}{8(k+1)^3}. } \]
For \(1/3<k<k_*\), no real \(s\), positive or negative, works. The corresponding statement for \(tJ_k+sW_k\), \(t>0\), follows by replacing \(s\) with \(s/t\).
This classifies the particular generator family \(J_k+sW_k\). Energy dissipation for \(J_k\) would require a further argument even where the generator is convex.
**Proof of the classification**
Represent the two columns of \(F\) by complex numbers
\[ p+q,\qquad i(p-q), \]
and introduce
\[ w=np+(k-1)q,\qquad w=2\sqrt{k}\,X,\qquad q=Y. \]
These are invertible real linear changes of the four matrix entries. Define
\[ H_1=|X|^2-|Y|^2,\qquad H_2=2X\cdot Y,\qquad H_3=2\det(X,Y). \]
Direct expansion of the **original** density gives
\[ \frac{n^3}{2k^2(3k+5)}V_{k,s}=H^TMH, \]
where
\[ M= \begin{pmatrix} 1&g&0\\ g&\tau+\delta&0\\ 0&0&\tau \end{pmatrix}, \]\[ g=\frac{2}{\sqrt{k}(3k+5)},\qquad \delta=\frac{1-k}{k(3k+5)},\qquad \tau=\frac{n(\ell+4sn^2)}{2k(3k+5)}. \]
The useful algebraic lemma is
\[ \boxed{ H^TMH\text{ is convex on }\mathbb R^4 \quad\Longleftrightarrow\quad \lambda_{\max}(M)\le2\lambda_{\min}(M). } \]
For necessity, orthogonal transformations of \((X,Y)\) induce all rotations of \(H\), so \(M\) can be diagonalized. At \(X=e_1,Y=0\), an appropriate variation has second derivative
\[ 4(2\lambda_j-\lambda_i). \]
All these derivatives must be nonnegative.
For sufficiency, normalize the ordered eigenvalues to \(1\le b\le a\le2\) and use
\[ \operatorname{diag}(a,b,1) =(2-a)\operatorname{diag}(1,1,1) +(a-b)\operatorname{diag}(2,1,1) +(b-1)\operatorname{diag}(2,2,1). \]
The three corresponding quartics are
\[ (|X|^2+|Y|^2)^2,\qquad 2(|X|^4+|Y|^4),\qquad 2\operatorname{tr}\bigl((Z^TZ)^2\bigr),\quad Z=[X\ Y], \]
and each is convex.
Now put \(h=\tau+\delta\). The eigenvalue-ratio condition for the first \(2\times2\) block requires
\[ 2h^2-5h+2+9g^2\le0. \]
Its minimum over every possible \(h\) occurs at \(h=5/4\), giving
\[ g^2\le\frac18 \quad\Longleftrightarrow\quad k(3k+5)^2\ge32. \]
The displayed \(s_*(k)\) makes \(h=5/4\). Under this threshold condition, all three eigenvalues of \(M\) lie in \([3/4,3/2]\), which proves sufficiency.
At \(k=1\), the full convex coefficient interval is
\[ \boxed{ \frac{8-3\sqrt2}{16}\le s\le \frac{8+3\sqrt2}{16}. } \]
These coordinate changes establish ordinary convexity only; their effect on compatibility is addressed separately below. The CONVEX_GENERATOR_CLASSIFICATION.md contain the complete argument.
**2. The exact outer-affine criterion now includes variable Jacobians**
The construction work originally considered determinant-one maps. The same reduction extends to **every** fixed compatible field
\[ B=I+D\psi\in L^4(\mathbb T^2;\mathbb R^{2\times2}). \]
For each constant matrix \(A\),
\[ AB=A+D(A\psi) \]
is an actual compatible field with affine mean \(A\).
Set
\[ C=A^TA,\qquad d=\det A,\qquad z=(C_{11},C_{12},C_{22})^T. \]
For the columns of \(B\), define
\[ p=(B_{11}^2,\,2B_{11}B_{21},\,B_{21}^2)^T, \qquad q=(B_{12}^2,\,2B_{12}B_{22},\,B_{22}^2)^T. \]
Then
\[ u(AB)=p\cdot z,\qquad v(AB)=q\cdot z,\qquad j(AB)=d\,\det B. \]
Write \(h=\det B\), \(e=(1,0,0)^T\), \(f=(0,0,1)^T\), and define
\[ U=\int pp^T-ee^T,\qquad V=\int qq^T-ff^T, \]\[ W=\frac12\int(pq^T+qp^T)-\frac12(ef^T+fe^T), \]\[ R_k=k^2U+2W+V, \]\[ l_k=\int h(kp-q)-(ke-f),\qquad \eta=\int h^2-1. \]
Compatibility gives \(\int h=1\), so \(\eta\ge0\).
The original polynomial expands as
\[ 8nJ_k(F) =\ell\bigl[k^2u^2+2uv+v^2+4j(ku-v)\bigr] +4(5k+1)j^2. \]
Consequently,
\[ \boxed{ 8n\left[\int J_k(AB)-J_k(A)\right] = \ell\left[z^TR_kz+4d\,l_k^Tz\right] +4(5k+1)\eta d^2. } \]
The determinant weights in \(l_k\) remain present. The last term accounts explicitly for determinant variance.
**Reduction to one scalar support parameter**
By homogeneity, normalize \(\operatorname{tr}C=2\) when \(A\ne0\), and write
\[ C= \begin{pmatrix} 1+x&y\\ y&1-x \end{pmatrix}. \]
Then
\[ x^2+y^2+d^2=1. \]
Conversely, every point of this sphere is realized by a real \(A\), including singular matrices and both determinant orientations.
Thus, for this fixed \(B\), the complete all-\(A\) problem is positivity of a quadratic polynomial
\[ P_k(v)=v^TM_kv+2a_k^Tv+c_k,\qquad |v|=1. \]
It has the exact criterion
\[ \boxed{ P_k\ge0\text{ on }S^2 \quad\Longleftrightarrow\quad \exists\tau\in\mathbb R: \begin{pmatrix} M_k-\tau I&a_k\\ a_k^T&c_k+\tau \end{pmatrix}\succeq0. } \]
Sufficiency follows by subtracting \(\tau(|v|^2-1)\). For necessity, the sphere-constrained quadratic minimization has a minimizer satisfying
\[ (M_k-\tau I)v_*=-a_k,\qquad M_k-\tau I\succeq0. \]
Below the least eigenvalue, \(\tau\) is found through the scalar secular equation. In the hard case, \(\tau\) equals the least eigenvalue and the missing norm is supplied within its eigenspace. The minimum is
\[ c_k+\tau-a_k^T(M_k-\tau I)^\dagger a_k, \]
and the Schur-complement condition gives the displayed matrix criterion. No completeness assertion about sums of squares is needed.
For rational moments, a strict negative sphere value admits a rational mean. For a rational point \((x,y,d)\in S^2\), \(x\ne-1\), the matrix
\[ \widetilde A= \begin{pmatrix} 1+x&y\\ 0&d \end{pmatrix} \]
realizes the same sign, with a positive scaling factor.
This criterion, quantified over **every** compatible mean-\(I\) field \(B\), is equivalent to the original full question. For invertible \(A\), use
\[ B=I+D(A^{-1}\phi). \]
Singular means follow by continuity. The unrestricted quantifier over \(B\) is still the unsolved part. See the VARIABLE_JACOBIAN_OUTER_AFFINE_CRITERION.md.
**Two fixed fields now have all-mean, all-parameter certificates**
The criterion was applied to two actual rational generating-function fields, each with 2,048 polygons:
**Field
Minimum twist
Exact lower-parameter certificate**
Earlier generating-function field
\(117/256\)
Three positive Bernstein control matrices on \([1/3,1]\)
New field from the outer-affine exploration
\(109/2048\)
Six positive control matrices on \([1/3,2/3]\) and \([2/3,1]\)
Every retained rational LDL pivot is positive. I independently reconstructed all nine matrices from the saved moments and checked every pivot. The accepted constant-determinant theorem supplies \(k\ge1\).
These are certificates for two fixed compatible fields. They are separate from the already exhausted 128-triangle field, and neither produces a negative original gap. Their constructions and certificates are in the OUTER_AFFINE_CRITERION.md.
**3. Two proposed algebraic constructions now have small exact exclusions
A Riesz-multiplier correction cannot satisfy the lifting identity**
I tested corrections whose four components are linear combinations of second-order Riesz multipliers applied to
\[ u,\quad v,\quad G_{\cdot1}\cdot G_{\cdot2},\quad \det G, \]
with each multiplier having symbol
\[ \frac{a\xi_1^2+b\xi_1\xi_2+c\xi_2^2}{|\xi|^2}. \]
At \(k=1\), this gives 48 unknown coefficients. Enforcing the correction identity on all resonant triads and clearing denominators produces 1,392 polynomial coefficient equations. Their coefficient and augmented ranks are 48 and 49.
The exclusion now has a much smaller certificate: **eight integer-weighted equations annihilate all 48 unknown columns while their right-hand sides sum to \(12\)**. Thus the proposed identity would imply
\[ \boxed{0=12.} \]
The selected coefficients require at most six bits, and the weights at most three bits. I replayed the integer certificate independently.
This excludes the specified output-frequency Riesz multipliers of local quadratic products. General bilinear symbols depending on both input frequencies, and nonlinear compatible lifts, remain outside the exclusion. The coupled_triad_assessment.md contains the equations and the eight-row certificate.
**The tested DSOS entropy class is exactly infeasible**
At \(k=1\), consider
\[ V=J+\sigma W,\qquad W=(u+v)^2-4j^2. \]
The finite certificate search sought
\[ \operatorname{div}DJ(F)\cdot\operatorname{div}DV(F) +\omega_F(B_1,B_2)\ge0, \]
using a closed degree-four two-form and a diagonally dominant sum-of-squares Gram matrix in the specified monomial basis.
The failure has a short exact explanation. Restrict to
\[ F=\operatorname{diag}(a,d),\qquad \phi_{1,22}=1, \]
with all other second derivatives zero. Then \(B_1=0\), so every two-form pullback vanishes. The entropy becomes
\[ P(a,d) =(a-d)^2 \left[\left(\frac14+2\sigma\right)(a^2+d^2)-\frac12ad\right]. \]
Its coefficients satisfy
\[ [a^4]P+\frac12[a^3d]P=-\frac14. \]
Every allowed DSOS generator has nonnegative value under this coefficient functional. Hence no certificate in that class exists, independently of \(\sigma\).
The scope is particularly clear because the same polynomial has the ordinary SOS representation
\[ \boxed{ P(a,d)=\sigma(a^2-d^2)^2+ \left(\frac14+\sigma\right)(a-d)^4. } \]
Thus the tested basis restriction fails even on this nonnegative entropy restriction. General SOS certificates and the nonlinear flow itself have not been excluded.
The full LP has an exact two-row integer dual, which I also replayed. The EXACT_DSOS_OBSTRUCTION.md records it.
**4. Pressure pays the instantaneous energy work, but affine convergence remains unproved**
The pressure construction gives an actual dissipation identity. For smooth compatible \(F=A+D\phi\), put
\[ L_Fv=\operatorname{cof}F:Dv,\qquad L_F^*p=-\operatorname{cof}F\,Dp,\qquad w=\operatorname{div}T(F). \]
For \(\eta>0\), choose \(p\) through
\[ (L_FL_F^*+\eta\ell I)p=L_Fw+\eta\lambda, \]
and set
\[ v=w-L_F^*p,\qquad r=\lambda-\ell p. \]
Then
\[ L_Fv=-\eta r \]
and
\[ \boxed{ DE_J(F)[Dv]=-\ell\|v\|_2^2-\eta\|r\|_2^2. } \]
Eliminating pressure gives
\[ (\ell I+\eta^{-1}L_F^*L_F)v=\operatorname{div}DJ(F). \]
Its stationary equation is therefore still \(\operatorname{div}DJ(F)=0\). The strict monotonicity of \(T\) does not by itself prove that these stationary fields are affine.
**Ordinary distance to the affine map can increase**
This limitation is visible on an explicit compatible wave. Set
\[ k=1,\quad A=I,\quad \eta=2\pi^2, \]\[ \phi_\varepsilon(x) =\frac{\varepsilon}{2\pi}(2,-5) \sin\bigl(2\pi(x_1+2x_2)\bigr). \]
For this field, the full pressure operator has constant coefficients on its one-phase subspace. Exact calculation gives
\[ \frac{d}{dt}\frac12\|\phi_\varepsilon\|_2^2 =\frac{\varepsilon^2}{6} -\frac{39875}{32}\varepsilon^4. \]
At \(\varepsilon=1/1000\),
\[ \boxed{ \frac{d}{dt}\frac12\|\phi_\varepsilon\|_2^2 =\frac{127043}{768000000000}>0. } \]
The Jacobian remains positive, and the original energy decreases by the pressure identity. This rules out the proposed ordinary-distance monotonicity argument.
**The stronger Jacobian distance leaves signed work**
The natural stronger quantity
\[ \mathcal D(\phi) =\frac{\ell}{2}\|\phi\|_2^2+ \frac1{2\eta}\|\det F-\det A\|_2^2 \]
satisfies
\[ \boxed{ \mathcal D' =-\int DJ(F):G+\int r\,\det G. } \]
The last term takes both signs on an actual compatible Hessian triad. With
\[ \psi= \frac{\cos(2\pi x_1)+\cos(2\pi x_2) +\cos(2\pi(x_1+x_2))}{(2\pi)^2}, \qquad \phi_\varepsilon=\varepsilon D\psi, \]
the first-order pressure residual satisfies
\[ \int r_1\det D^2\psi=-\frac{35}{12}. \]
An explicit resolvent estimate gives
\[ \|r(\varepsilon)-\varepsilon r_1\|_2 \le\frac{11541}{8}\varepsilon^2 \qquad (|\varepsilon|\le1/8). \]
At \(\varepsilon=\pm1/7914\), the two curvature-work integrals therefore have opposite signs, each with guaranteed magnitude exceeding
\[ \frac{35}{11895956830656}. \]
The proof uses a Fourier–Neumann contraction ratio below \(1/900\), with the remainder paid explicitly.
**That work is not an exact endpoint differential**
Define the one-form on compatible potentials
\[ \beta_\phi(v) =\int\det G\,\operatorname{cof}(A+G):Dv. \]
Its exterior derivative is
\[ (d\beta)_\phi(v,w) = \int\left[ (\operatorname{cof}G:Dv)(\operatorname{cof}A:Dw) - (\operatorname{cof}G:Dw)(\operatorname{cof}A:Dv) \right]. \]
At \(A=I\), take
\[ \phi=\left(\frac{\sin(2\pi x_1)}{4\pi},0\right),\qquad v=\left(0,\frac{\sin(2\pi x_2)}{2\pi}\right), \]\[ w=\left(\frac{\sin(2\pi(x_1+x_2))}{2\pi},0\right). \]
The background is uniformly invertible, and
\[ \boxed{(d\beta)_\phi(v,w)=\frac18.} \]
Thus \(\beta\) itself cannot be replaced by the differential of an endpoint functional. Another functional, integrating factor, or estimate along a specially chosen path would need its own proof.
The pressure_curvature_details.md gives the finite-amplitude calculations and remainder bounds. These are limitations of the convergence argument, not negative quasiconvexity gaps.
**5. The earlier radial argument now has a quantitative reserve and a complete \(W^{1,4}\) center passage**
The qualitative smooth radial telescoping argument was already in the earlier notes. The additions here are the reserve and its extension through a possibly singular center.
Let
\[ f(x)=C(r)x,\qquad r=|x|,\qquad C(R)=A, \]
where \(C\) is a locally absolutely continuous matrix path and \(f\in W^{1,4}(B_R;\mathbb R^2)\). Set
\[ e=x/r,\qquad E=r(C'(r)e)\otimes e. \]
Then
\[ Df=C(r)+E, \]
and \(E\) has rank at most one. The accepted quartic increment estimate yields
\[ J_k(Df)\ge J_k(C)+DJ_k(C):E+\frac13J_k(E). \]
Angular averaging gives
\[ \fint_{S^1}DJ_k(C):E =\frac r2\frac{d}{dr}J_k(C). \]
After multiplication by \(2\pi r\), the first two terms telescope. The result is
\[ \boxed{ \int_{B_R}J_k(Df)-\pi R^2J_k(A) \ge \frac13\int_{B_R} J_k\!\left(r(C'(r)e)\otimes e\right). } \]
The center is accounted for without a boundedness assumption. Tangential differentiation gives
\[ (Df)e_\perp=C(r)e_\perp, \]
and
\[ \fint_{S^1}|Ce|^4 =\frac{|C|^4+2\operatorname{tr}((C^TC)^2)}8 \ge\frac{|C|^4}{4}. \]
Hence
\[ \int_0^R r|C(r)|^4\,dr<\infty. \]
There is a sequence \(\rho_i\downarrow0\) with
\[ \rho_i^2|C(\rho_i)|^4\longrightarrow0. \]
Replacing the profile by the constant \(C(\rho_i)\) inside \(\rho_i\) produces compatible constant-core maps whose core fourth-power gradient cost is
\[ \pi\rho_i^2|C(\rho_i)|^4\longrightarrow0. \]
They converge strongly in \(W^{1,4}\), so the original quartic energy and the reserve pass to the limit.
For the spiral profile
\[ C(r)=A(r/R)^{\alpha-1}R_{\beta\log(r/R)}, \qquad \alpha>\frac12, \]
put
\[ \eta_0=(\alpha-1)^2+\beta^2,\qquad \nu_k=\frac{\ell\min(k^2,1)}{8n}. \]
The explicit bound is
\[ \boxed{ \int_{B_R}J_k(Df)-\pi R^2J_k(A) \ge \frac{\nu_k\pi R^2\eta_0^2}{3(2\alpha-1)} \frac{|A|^4+2\operatorname{tr}((A^TA)^2)}8. } \]
It is strictly positive for \(A\ne0\) and a nonidentity spiral.
The perturbation \(f-Ax\) has zero trace and extends by zero into the unit torus. Strong compact-support approximation is justified by quartic growth. Arbitrary angular dependence remains outside this class. The RADIAL_MATRIX_PATH_RESERVE.md contains these details.
**6. The balanced coordinates have an exact compatible Beurling formulation**
The coordinate change used in the convexity classification also gives a useful exact reformulation, provided compatibility is retained.
For the complex potential, let
\[ p=\partial_z\phi,\qquad q=\partial_{\bar z}\phi. \]
On the original torus,
\[ p=\mathcal Bq, \qquad \widehat{\mathcal Bq}(\xi) =\frac{\xi_1-i\xi_2}{\xi_1+i\xi_2}\widehat q(\xi), \quad \xi\ne0. \]
Conversely, every mean-zero \(q\in L^4(\mathbb T^2;\mathbb C)\) reconstructs a periodic \(W^{1,4}\) potential. For finite Fourier data,
\[ \widehat\phi(\xi) =\frac{\widehat q(\xi)} {\pi i(\xi_1+i\xi_2)}, \]
and Fejér approximation supplies the general case.
Thus the balanced variables obey
\[ X=X_0+T_kh,\qquad Y=Y_0+h, \]
where
\[ T_k= \frac{k+1}{2\sqrt{k}}\mathcal B+ \frac{k-1}{2\sqrt{k}}I. \]
Both directions of this correspondence use the original torus and preserve the full compatibility requirement.
At \(k=1\), the original density becomes
\[ J_1=2Q, \]\[ Q(X,Y) = |X|^4+|Y|^4-|X|^2|Y|^2 +(|X|^2-|Y|^2)\operatorname{Re}(X\overline Y). \]
The full question at this parameter is exactly
\[ \int Q(X_0+\mathcal Bh,Y_0+h) \ge Q(X_0,Y_0) \]
for every pair of constants and every mean-zero complex \(h\in L^4\).
No sharp estimate for this phase-sensitive polynomial was obtained. In particular, convexity of \(J_k+sW_k\) gives only
\[ \int J_k(A+D\phi)-J_k(A) \ge -s\left[\int W_k(A+D\phi)-W_k(A)\right], \]
and the \(W_k\) gap remains to be controlled. The BEURLING_GRAPH_EQUIVALENCE.md proves the compatibility and approximation statements.
**7. Finite computation and remaining endpoint**
The consequential computations were bounded, and strict sign claims use exact certificates:
**Calculation
Finite scope and outcome**
Convex-generator classification
Two exact polynomial identities; 45 rational bisections for the displayed threshold; \(0.617\) seconds
Outer-affine exploration
Four deterministic seeds; 377 iterations, 434 objective evaluations, 3,733 bounded trust-region candidates; \(7.40\) seconds; no negative found
Exact polygon certificates
Extraction/certification in \(1.41\) and \(4.13\) seconds; nine rational positive-definiteness checks
Independent support verification
Every saved LDL pivot reconstructed; \(1.009\) seconds; largest pivot integers had 24,335 bits
Riesz exclusion
48 unknowns, 1,392 coefficient equations; eight-row integer contradiction; reconstruction and extraction in \(7.444\) seconds
Entropy DSOS search
One LP: 735 equations, 3,600 nonnegative square weights, 140 closed-form coefficients, one bounded \(\sigma\); exact two-row infeasibility certificate
Pressure calculations
Exact verifier in \(2.317\) seconds; explicit finite-amplitude signs and resolvent remainder
Radial extension
Analytic proof and explicit integration; no numerical search
The floating calculations selected candidates. They were not used to infer universal positivity. The exact Riesz and DSOS exclusions were replayed without optimization.
The unrestricted requirement remains
\[ \boxed{ b_G^TH_G^\dagger b_G\le2c_G \qquad\text{for every compatible }G=D\phi. } \]
The new reductions and certificates do not establish that sharp estimate. No compatible field violating it—and therefore no negative original quasiconvexity gap—is contained in this continuation.


## Native prefix (reader truncated at 20,000 characters)

**I continued, but I have not resolved the full universal inequality.** I have neither a proof for every compatible \(D\phi\) nor an admissible field with a negative original-energy gap.

This continuation completed an exact classification of a proposed convex generator, extended the outer-affine mean reduction to variable Jacobians, and produced small exact certificates excluding two specific lifting/certificate constructions. It also made the obstruction in the pressure approach more concrete and strengthened the earlier radial argument.

The complete proofs, constructions, exact certificates, and computation records are in the [updated research packet](https://chatgpt.com/library?file_id=libfile_6d1aa4e4e9f08191bc79875c2b2752c0&account_id=personal). The :chatgpt-content-reference{index="0"}[continuation record](sandbox:/workspace/scratch/21b466b728a1/quartic_research_packet/NONLINEAR_AND_GLOBAL_MEAN_CONTINUATION.txt) distinguishes these results from the earlier accepted capital.

## 1. Exact convexity classification for a proposed nonlinear generator

Consider the additional quartic
\[
W_k(F)=(u+v-2j)(k^2u+v+2kj)
\]
and the proposed generator
\[
V_{k,s}=J_k+sW_k.
\]

I obtained the complete answer to its **ordinary matrix convexity** question:
\[
\boxed{
\exists s\in\mathbb R\text{ such that }V_{k,s}\text{ is convex}
\quad\Longleftrightarrow\quad
k(3k+5)^2\ge32.
}
\]

Let \(k_*\) be the unique positive root of
\[
9k^3+30k^2+25k-32=0.
\]
Then
\[
k_*\approx0.657961495631632.
\]
For every \(k\ge k_*\), an explicit working coefficient is
\[
\boxed{
s_*(k)=\frac{9k^2+25k-2}{8(k+1)^3}.
}
\]
For \(1/3<k<k_*\), no real \(s\), positive or negative, works. The corresponding statement for \(tJ_k+sW_k\), \(t>0\), follows by replacing \(s\) with \(s/t\).

This classifies the particular generator family \(J_k+sW_k\). Energy dissipation for \(J_k\) would require a further argument even where the generator is convex.

### Proof of the classification

Represent the two columns of \(F\) by complex numbers
\[
p+q,\qquad i(p-q),
\]
and introduce
\[
w=np+(k-1)q,\qquad w=2\sqrt{k}\,X,\qquad q=Y.
\]
These are invertible real linear changes of the four matrix entries. Define
\[
H_1=|X|^2-|Y|^2,\qquad
H_2=2X\cdot Y,\qquad
H_3=2\det(X,Y).
\]
Direct expansion of the **original** density gives
\[
\frac{n^3}{2k^2(3k+5)}V_{k,s}=H^TMH,
\]
where
\[
M=
\begin{pmatrix}
1&g&0\\
g&\tau+\delta&0\\
0&0&\tau
\end{pmatrix},
\]
\[
g=\frac{2}{\sqrt{k}(3k+5)},\qquad
\delta=\frac{1-k}{k(3k+5)},\qquad
\tau=\frac{n(\ell+4sn^2)}{2k(3k+5)}.
\]

The useful algebraic lemma is
\[
\boxed{
H^TMH\text{ is convex on }\mathbb R^4
\quad\Longleftrightarrow\quad
\lambda_{\max}(M)\le2\lambda_{\min}(M).
}
\]

For necessity, orthogonal transformations of \((X,Y)\) induce all rotations of \(H\), so \(M\) can be diagonalized. At \(X=e_1,Y=0\), an appropriate variation has second derivative
\[
4(2\lambda_j-\lambda_i).
\]
All these derivatives must be nonnegative.

For sufficiency, normalize the ordered eigenvalues to \(1\le b\le a\le2\) and use
\[
\operatorname{diag}(a,b,1)
=(2-a)\operatorname{diag}(1,1,1)
+(a-b)\operatorname{diag}(2,1,1)
+(b-1)\operatorname{diag}(2,2,1).
\]
The three corresponding quartics are
\[
(|X|^2+|Y|^2)^2,\qquad
2(|X|^4+|Y|^4),\qquad
2\operatorname{tr}\bigl((Z^TZ)^2\bigr),\quad Z=[X\ Y],
\]
and each is convex.

Now put \(h=\tau+\delta\). The eigenvalue-ratio condition for the first \(2\times2\) block requires
\[
2h^2-5h+2+9g^2\le0.
\]
Its minimum over every possible \(h\) occurs at \(h=5/4\), giving
\[
g^2\le\frac18
\quad\Longleftrightarrow\quad
k(3k+5)^2\ge32.
\]
The displayed \(s_*(k)\) makes \(h=5/4\). Under this threshold condition, all three eigenvalues of \(M\) lie in \([3/4,3/2]\), which proves sufficiency.

At \(k=1\), the full convex coefficient interval is
\[
\boxed{
\frac{8-3\sqrt2}{16}\le s\le
\frac{8+3\sqrt2}{16}.
}
\]

These coordinate changes establish ordinary convexity only; their effect on compatibility is addressed separately below. The :chatgpt-content-reference{index="1"}[classification proof and exact verification](sandbox:/workspace/scratch/21b466b728a1/construction_global_continuation/convex_generator/CONVEX_GENERATOR_CLASSIFICATION.md) contain the complete argument.

## 2. The exact outer-affine criterion now includes variable Jacobians

The construction work originally considered determinant-one maps. The same reduction extends to **every** fixed compatible field
\[
B=I+D\psi\in L^4(\mathbb T^2;\mathbb R^{2\times2}).
\]
For each constant matrix \(A\),
\[
AB=A+D(A\psi)
\]
is an actual compatible field with affine mean \(A\).

Set
\[
C=A^TA,\qquad d=\det A,\qquad
z=(C_{11},C_{12},C_{22})^T.
\]
For the columns of \(B\), define
\[
p=(B_{11}^2,\,2B_{11}B_{21},\,B_{21}^2)^T,
\qquad
q=(B_{12}^2,\,2B_{12}B_{22},\,B_{22}^2)^T.
\]
Then
\[
u(AB)=p\cdot z,\qquad
v(AB)=q\cdot z,\qquad
j(AB)=d\,\det B.
\]

Write \(h=\det B\), \(e=(1,0,0)^T\), \(f=(0,0,1)^T\), and define
\[
U=\int pp^T-ee^T,\qquad
V=\int qq^T-ff^T,
\]
\[
W=\frac12\int(pq^T+qp^T)-\frac12(ef^T+fe^T),
\]
\[
R_k=k^2U+2W+V,
\]
\[
l_k=\int h(kp-q)-(ke-f),\qquad
\eta=\int h^2-1.
\]
Compatibility gives \(\int h=1\), so \(\eta\ge0\).

The original polynomial expands as
\[
8nJ_k(F)
=\ell\bigl[k^2u^2+2uv+v^2+4j(ku-v)\bigr]
+4(5k+1)j^2.
\]
Consequently,
\[
\boxed{
8n\left[\int J_k(AB)-J_k(A)\right]
=
\ell\left[z^TR_kz+4d\,l_k^Tz\right]
+4(5k+1)\eta d^2.
}
\]

The determinant weights in \(l_k\) remain present. The last term accounts explicitly for determinant variance.

### Reduction to one scalar support parameter

By homogeneity, normalize \(\operatorname{tr}C=2\) when \(A\ne0\), and write
\[
C=
\begin{pmatrix}
1+x&y\\
y&1-x
\end{pmatrix}.
\]
Then
\[
x^2+y^2+d^2=1.
\]
Conversely, every point of this sphere is realized by a real \(A\), including singular matrices and both determinant orientations.

Thus, for this fixed \(B\), the complete all-\(A\) problem is positivity of a quadratic polynomial
\[
P_k(v)=v^TM_kv+2a_k^Tv+c_k,\qquad |v|=1.
\]
It has the exact criterion
\[
\boxed{
P_k\ge0\text{ on }S^2
\quad\Longleftrightarrow\quad
\exists\tau\in\mathbb R:
\begin{pmatrix}
M_k-\tau I&a_k\\
a_k^T&c_k+\tau
\end{pmatrix}\succeq0.
}
\]

Sufficiency follows by subtracting \(\tau(|v|^2-1)\). For necessity, the sphere-constrained quadratic minimization has a minimizer satisfying
\[
(M_k-\tau I)v_*=-a_k,\qquad M_k-\tau I\succeq0.
\]
Below the least eigenvalue, \(\tau\) is found through the scalar secular equation. In the hard case, \(\tau\) equals the least eigenvalue and the missing norm is supplied within its eigenspace. The minimum is
\[
c_k+\tau-a_k^T(M_k-\tau I)^\dagger a_k,
\]
and the Schur-complement condition gives the displayed matrix criterion. No completeness assertion about sums of squares is needed.

For rational moments, a strict negative sphere value admits a rational mean. For a rational point \((x,y,d)\in S^2\), \(x\ne-1\), the matrix
\[
\widetilde A=
\begin{pmatrix}
1+x&y\\
0&d
\end{pmatrix}
\]
realizes the same sign, with a positive scaling factor.

This criterion, quantified over **every** compatible mean-\(I\) field \(B\), is equivalent to the original full question. For invertible \(A\), use
\[
B=I+D(A^{-1}\phi).
\]
Singular means follow by continuity. The unrestricted quantifier over \(B\) is still the unsolved part. See the :chatgpt-content-reference{index="2"}[variable-Jacobian criterion](sandbox:/workspace/scratch/21b466b728a1/construction_global_continuation/VARIABLE_JACOBIAN_OUTER_AFFINE_CRITERION.md).

### Two fixed fields now have all-mean, all-parameter certificates

The criterion was applied to two actual rational generating-function fields, each with 2,048 polygons:

| Field | Minimum twist | Exact lower-parameter certificate |
|---|---:|---|
| Earlier generating-function field | \(117/256\) | Three positive Bernstein control matrices on \([1/3,1]\) |
| New field from the outer-affine exploration | \(109/2048\) | Six positive control matrices on \([1/3,2/3]\) and \([2/3,1]\) |

Every retained rational LDL pivot is positive. I independently reconstructed all nine matrices from the saved moments and checked every pivot. The accepted constant-determinant theorem supplies \(k\ge1\).

These are certificates for two fixed compatible fields. They are separate from the already exhausted 128-triangle field, and neither produces a negative original gap. Their constructions and certificates are in the :chatgpt-content-reference{index="3"}[outer-affine proof record](sandbox:/workspace/scratch/21b466b728a1/construction_global_continuation/OUTER_AFFINE_CRITERION.md).

## 3. Two proposed algebraic constructions now have small exact exclusions

### A Riesz-multiplier correction cannot satisfy the lifting identity

I tested corrections whose four components are linear combinations of second-order Riesz multipliers applied to
\[
u,\quad v,\quad G_{\cdot1}\cdot G_{\cdot2},\quad \det G,
\]
with each multiplier having symbol
\[
\frac{a\xi_1^2+b\xi_1\xi_2+c\xi_2^2}{|\xi|^2}.
\]

At \(k=1\), this gives 48 unknown coefficients. Enforcing the correction identity on all resonant triads and clearing denominators produces 1,392 polynomial coefficient equations. Their coefficient and augmented ranks are 48 and 49.

The exclusion now has a much smaller certificate: **eight integer-weighted equations annihilate all 48 unknown columns while their right-hand sides sum to \(12\)**. Thus the proposed identity would imply
\[
\boxed{0=12.}
\]
The selected coefficients require at most six bits, and the weights at most three bits. I replayed the integer certificate independently.

This excludes the specified output-frequency Riesz multipliers of local quadratic products. General bilinear symbols depending on both input frequencies, and nonlinear compatible lifts, remain outside the exclusion. The :chatgpt-content-reference{index="4"}[triad assessment](sandbox:/workspace/scratch/21b466b728a1/moment_coupled_lift/coupled_triad_assessment.md) contains the equations and the eight-row certificate.

### The tested DSOS entropy class is exactly infeasible

At \(k=1\), consider
\[
V=J+\sigma W,\qquad W=(u+v)^2-4j^2.
\]
The finite certificate search sought
\[
\operatorname{div}DJ(F)\cdot\operatorname{div}DV(F)
+\omega_F(B_1,B_2)\ge0,
\]
using a closed degree-four two-form and a diagonally dominant sum-of-squares Gram matrix in the specified monomial basis.

The failure has a short exact explanation. Restrict to
\[
F=\operatorname{diag}(a,d),\qquad \phi_{1,22}=1,
\]
with all other second derivatives zero. Then \(B_1=0\), so every two-form pullback vanishes. The entropy becomes
\[
P(a,d)
=(a-d)^2
\left[\left(\frac14+2\sigma\right)(a^2+d^2)-\frac12ad\right].
\]
Its coefficients satisfy
\[
[a^4]P+\frac12[a^3d]P=-\frac14.
\]
Every allowed DSOS generator has nonnegative value under this coefficient functional. Hence no certificate in that class exists, independently of \(\sigma\).

The scope is particularly clear because the same polynomial has the ordinary SOS representation
\[
\boxed{
P(a,d)=\sigma(a^2-d^2)^2+
\left(\frac14+\sigma\right)(a-d)^4.
}
\]
Thus the tested basis restriction fails even on this nonnegative entropy restriction. General SOS certificates and the nonlinear flow itself have not been excluded.

The full LP has an exact two-row integer dual, which I also replayed. The :chatgpt-content-reference{index="5"}[DSOS obstruction note](sandbox:/workspace/scratch/21b466b728a1/moment_convexflow_dsos/EXACT_DSOS_OBSTRUCTION.md) records it.

## 4. Pressure pays the instantaneous energy work, but affine convergence remains unproved

The pressure construction gives an actual dissipation identity. For smooth compatible \(F=A+D\phi\), put
\[
L_Fv=\operatorname{cof}F:Dv,\qquad
L_F^*p=-\operatorname{cof}F\,Dp,\qquad
w=\operatorname{div}T(F).
\]
For \(\eta>0\), choose \(p\) through
\[
(L_FL_F^*+\eta\ell I)p=L_Fw+\eta\lambda,
\]
and set
\[
v=w-L_F^*p,\qquad r=\lambda-\ell p.
\]
Then
\[
L_Fv=-\eta r
\]
and
\[
\boxed{
DE_J(F)[Dv]=-\ell\|v\|_2^2-\eta\|r\|_2^2.
}
\]

Eliminating pressure gives
\[
(\ell I+\eta^{-1}L_F^*L_F)v=\operatorname{div}DJ(F).
\]
Its stationary equation is therefore still \(\operatorname{div}DJ(F)=0\). The strict monotonicity of \(T\) does not by itself prove that these stationary fields are affine.

### Ordinary distance to the affine map can increase

This limitation is visible on an explicit compatible wave. Set
\[
k=1,\quad A=I,\quad \eta=2\pi^2,
\]
\[
\phi_\varepsilon(x)
=\frac{\varepsilon}{2\pi}(2,-5)
\sin\bigl(2\pi(x_1+2x_2)\bigr).
\]
For this field, the full pressure operator has constant coefficients on its one-phase subspace. Exact calculation gives
\[
\frac{d}{dt}\frac12\|\phi_\varepsilon\|_2^2
=\frac{\varepsilon^2}{6}
-\frac{39875}{32}\varepsilon^4.
\]
At \(\varepsilon=1/1000\),
\[
\boxed{
\frac{d}{dt}\frac12\|\phi_\varepsilon\|_2^2
=\frac{127043}{768000000000}>0.
}
\]
The Jacobian remains positive, and the original energy decreases by the pressure identity. This rules out the proposed ordinary-distance monotonicity argument.

### The stronger Jacobian distance leaves signed work

The natural stronger quantity
\[
\mathcal D(\phi)
=\frac{\ell}{2}\|\phi\|_2^2+
\frac1{2\eta}\|\det F-\det A\|_2^2
\]
satisfies
\[
\boxed{
\mathcal D'
=-\int DJ(F):G+\int r\,\det G.
}
\]

The last term takes both signs on an actual compatible Hessian triad. With
\[
\psi=
\frac{\cos(2\pi x_1)+\cos(2\pi x_2)
+\cos(2\pi(x_1+x_2))}{(2\pi)^2},
\qquad \phi_\varepsilon=\varepsilon D\psi,
\]
the first-order pressure residual satisfies
\[
\int r_1\det D^2\psi=-\frac{35}{12}.
\]
An explicit resolvent estimate gives
\[
\|r(\varepsilon)-\varepsilon r_1\|_2
\le\frac{11541}{8}\varepsilon^2
\qquad (|\varepsilon|\le1/8).
\]
At \(\varepsilon=\pm1/7914\), the two curvature-work integrals therefore have opposite signs, each with guaranteed magnitude exceeding
\[
\frac{35}{11895956830656}.
\]
The proof uses a Fourier–Neumann contraction ratio below \(1/900\), with the remainder paid explicitly.

### That work is not an exact endpoint differential

Define the one-form on compatible potentials
\[
\beta_\phi(v)
=\int\det G\,\operatorname{cof}(A+G):Dv.
\]
Its exterior derivative is
\[
(d\beta)_\phi(v,w)
=
\int\left[
(\operatorname{cof}G:Dv)(\operatorname{cof}A:Dw)
-
(\operatorname{cof}G:Dw)(\operatorname{cof}A:Dv)
\right].
\]
At \(A=I\), take
\[
\phi=\left(\frac{\sin(2\pi x_1)}{4\pi},0\right),\qquad
v=\left(0,\frac{\sin(2\pi x_2)}{2\pi}\right),
\]
\[
w=\left(\frac{\sin(2\pi(x_1+x_2))}{2\pi},0\right).
\]
The background is uniformly invertible, and
\[
\boxed{(d\beta)_\phi(v,w)=\frac18.}
\]
Thus \(\beta\) itself cannot be replaced by the differential of an endpoint functional. Another functional, integrating factor, or estimate along a specially chosen path would need its own proof.

The :chatgpt-content-reference{index="6"}[pressure and curvature note](sandbox:/workspace/scratch/21b466b728a1/projection_global_continuation/pressure_curvature_details.md) gives the finite-amplitude calculations and remainder bounds. These are limitations of the convergence argument, not negative quasiconvexity gaps.

## 5. The earlier radial argument now has a quantitative reserve and a complete \(W^{1,4}\) center passage

The qualitative smooth radial telescoping argument was already in the earlier notes. The additions here are the reserve and its extension through a possibly singular center.

Let
\[
f(x)=C(r)x,\qquad r=|x|,\qquad C(R)=A,
\]
where \(C\) is a locally absolutely continuous matrix path and \(f\in W^{1,4}(B_R;\mathbb R^2)\). Set
\[
e=x/r,\qquad E=r(C'(r)e)\otimes e.
\]
Then
\[
Df=C(r)+E,
\]
and \(E\) has rank at most one. The accepted quartic increment estimate yields
\[
J_k(Df)\ge J_k(C)+DJ_k(C):E+\frac13J_k(E).
\]
Angular averaging gives
\[
\fint_{S^1}DJ_k(C):E
=\frac r2\frac{d}{dr}J_k(C).
\]
After multiplication by \(2\pi r\), the first two terms telescope. The result is
\[
\boxed{
\int_{B_R}J_k(Df)-\pi R^2J_k(A)
\ge
\frac13\int_{B_R}
J_k\!\left(r(C'(r)e)\otimes e\right).
}
\]

The center is accounted for without a boundedness assumption. Tangential differentiation gives
\[
(Df)e_\perp=C(r)e_\perp,
\]
and
\[
\fint_{S^1}|Ce|^4
=\frac{|C|^4+2\operatorname{tr}((C^TC)^2)}8
\ge\frac{|C|^4}{4}.
\]
Hence
\[
\int_0^R r|C(r)|^4\,dr<\infty.
\]
There is a sequence \(\rho_i\downarrow0\) with
\[
\rho_i^2|C(\rho_i)|^4\longrightarrow0.
\]
Replacing the profile by the constant \(C(\rho_i)\) inside \(\rho_i\) produces compatible constant-core maps whose core fourth-power gradient cost is
\[
\pi\rho_i^2|C(\rho_i)|^4\longrightarrow0.
\]
They converge strongly in \(W^{1,4}\), so the original quartic energy and the reserve pass to the limit.

For the spiral profile
\[
C(r)=A(r/R)^{\alpha-1}R_{\beta\log(r/R)},
\qquad \alpha>\frac12,
\]
put
\[
\eta_0=(\alpha-1)^2+\beta^2,\qquad
\nu_k=\frac{\ell\min(k^2,1)}{8n}.
\]
The explicit bound is
\[
\boxed{
\int_{B_R}J_k(Df)-\pi R^2J_k(A)
\ge
\frac{\nu_k\pi R^2\eta_0^2}{3(2\alpha-1)}
\frac{|A|^4+2\operatorname{tr}((A^TA)^2)}8.
}
\]
It is strictly positive for \(A\ne0\) and a nonidentity spiral.

The perturbation \(f-Ax\) has zero trace and extends by zero into the unit torus. Strong compact-support approximation is justified by quartic growth. Arbitrary angular dependence remains outside this class. The :chatgpt-content-reference{index="7"}[radial reserve proof](sandbox:/workspace/scratch/21b466b728a1/construction_global_continuation/RADIAL_MATRIX_PATH_RESERVE.md) contains these details.

## 6. The balanced coordinates have an exact compatible Beurling formulation

The coordinate change used in the convexity classification also gives a useful exact reformulation, provided compatibility is retained.

For the complex potential, let
\[
p=\partial_z\phi,\qquad q=\partial_{\bar z}\phi.
\]
On the original torus,
\[
p=\mathcal Bq,
\qquad
\widehat{\mathcal Bq}(\xi)
=\frac{\xi_1-i\xi_2}{\xi_1+i\xi_2}\widehat q(\xi),
\quad \xi\ne0.
\]
Conversely, every mean-zero \(q\in L^4(\mathbb T^2;\mathbb C)\) reconstructs a periodic \(W^{1,4}\) potential. For finite Fourier data,
\[
\widehat\phi(\xi)
=\frac{\widehat q(\xi)}
{\pi i(\xi_1+i\xi_2)},
\]
and Fejér approximation supplies the general case.

Thus the balanced variables obey
\[
X=X_0+T_kh,\qquad Y=Y_0+h,
\]
where
\[
T_k=
\frac{k+1}{2\sqrt{k}}\mathcal B+
\frac{k-1}{2\sqrt{k}}I.
\]
Both directions of this correspondence use the original torus and preserve the full compatibility requirement.

At \(k=1\), the original density becomes
\[
J_1=2Q,
\]
\[
Q(X,Y)
=
|X|^4+|Y|^4-|X|^2|Y|^2
+(|X|^2-|Y|^2)\operatorname{Re}(X\overline Y).
\]
The full question at this parameter is exactly
\[
\int Q(X_0+\mathcal Bh,Y_0+h)
\ge Q(X_0,Y_0)
\]
for every pair of constants and every mean-zero complex \(h\in L^4\).

No sharp estimate for this phase-sensitive polynomial was obtained. In particular, convexity of \(J_k+sW_k\) gives only
\[
\int J_k(A+D\phi)-J_k(A)
\ge
-s\left[\int W_k(A+D\phi)-W_k(A)\right],
\]
and the \(W_k\) gap remains to be controlled. The :chatgpt-content-reference{index="8"}[Beurling equivalence note](sandbox:/workspace/scratch/21b466b728a1/construction_global_continuation/BEURLING_GRAPH_EQUIVALENCE.md) proves the compatibility and approximation statements.

## 7. Finite computation and remaining endpoint

The consequential computations were bounded, and strict sign claims use exact certificates:

| Calculation | Finite scope and outcome |
|---|---|
| Convex-generator classification | Two exact polynomial identities; 45 rational bisections for the displayed threshold; \(0.617\) seconds |
| Outer-affine exploration | Four deterministic seeds; 377 iterations, 434 objective evaluations, 3,733 bounded trust-region candidates; \(7.40\) seconds; no negative found |
| Exact polygon certificates | Extraction/certification in \(1.41\) and \(4.13\) seconds; nine rational positive-definiteness checks |
| Independent support verification | Every saved LDL pivot reconstructed; \(1.009\) seconds; largest pivot integers had 24,335 bits |
| Riesz exclusion | 48 unknowns, 1,392 coefficient equations; eight-r

## Visible current-turn activity (accessibility; virtualized)

3518 button (expanded) Worked for 71m 51s, Secondary Actions: Collapse
										3519 text Worked for 71m 51s
										3520 image
									4106 text I’ll continue from the small-Jacobian theorem. I’ll focus on determinant fluctuations outside that region and look for an argument that can handle the sharp lifting cross term or an actual compatible field with a negative gap. Expanded the scalar restriction Tested parameter k equivalence and checked the global minimum Optimized over area-preserving matrices
									4107 container Subagent activity
										4108 container
											4109 button Principal construction
											4110 text , 
											4111 button Principal moment
											4112 text  and 
											4113 button Principal projection
											4114 text  updated
									4115 text Analyzed inverse-gradient convexity and checked Schur-complement positivity Explored monotone operator rigidity Analyzed quartic quasiconvexity and area structure
									4116 container
										4117 button (collapsed) Ran a command, searched the web, Secondary Actions: Expand
										4118 text Ran a command, searched the web
									4119 text Expanded the moment polynomial and checked the left-SO average
									4120 text Rechecked J1’s rotated form
									4121 text Checked cofactor compatibility and tested nonlocal output mixing
									4122 text Derived Beurling product identities
									4123 text Analyzed finite Fourier triads and assessed moment-matrix norms
									4124 text Tested gradient constraints and reviewed quartic convexity theorems
									4125 text Refined the diffusion analysis
									4126 text Tested amplitude interpolation and checked transport convexity
									4127 text Checked stationarity in A
									4128 text Checked weak lower semicontinuity and derived stress-energy identity
									4129 text Checked radial monotonicity and constructed the global root
									4130 text Checked the k<1 case and endpoint rank-one convexity
									4131 text The area-preserving construction has a useful unexplored degree of freedom: its affine mean. Writing the gradient as 
									4132 container
										4133 text 𝐴 𝐵 ( 𝑥 )
									4134 text , with 
									4135 container
										4136 text det ⁡ 𝐵 = 1
									4137 text  and 
									4138 container
										4139 text ∫ 𝐵 = 𝐼
									4140 text , keeps compatibility and constant determinant exact while allowing 
									4141 text 𝐴
									4142 text  to vary. I’m reducing that problem algebraically alongside the sharp Fourier-lifting and nonlinear-flow approaches. Checked Hessian-measure certificates and rank-one convexity Derived scalar quadratic Jensen and analyzed J’s quadratic form Checked quartic-form convexity Estimated P’s L4 and sharp norms Checked acoustic symmetrization and scalar stiffness Analyzed the k-quadratic and derived the cone criterion Tested τ=0 nonnegativity and derived the determinant-induced gap
									4143 container Subagent activity
										4144 container
											4145 button Principal projection
											4146 text  and 
											4147 button Principal construction
											4148 text  updated
									4149 text Explored determinant constraints and tested gradient truncation Tested quartic energy coercivity and shifted energy sign Checked P's quadratic term Checked nonlinear Korn control and S(I,G) kernel Derived sharp cubic bounds Checked critical support coverage and rank-one ratios Tested strict quality control and pointwise support Checked projection confirmation
									4150 container Subagent activity
										4151 container
											4152 button Principal moment
											4153 text  finished
									4154 text Computed local nonlinear response and analyzed soft kernel Derived S-eigenvector alignment Enumerated invariant quartic terms Computed acoustic Hessian and checked J-basis coupling
									4155 container Subagent activity
										4156 container
											4157 button Principal projection
											4158 text  updated
									4159 text Simplified K coefficients
									4160 text Ran command
									4161 container Subagent activity
										4162 container
											4163 button Principal projection
											4164 text  updated
									4165 text Compared Hessian coefficients
									4166 container
										4167 button (collapsed) Ran a command, Secondary Actions: Expand
										4168 text Ran a command
									4169 text Checked quartic convexity Generated closed 2-form basis and derived analytic Fourier jets Checked convex companion family and derived commute constraint
									4170 container
										4171 button (collapsed) Ran a command, Secondary Actions: Expand
										4172 text Ran a command
									4173 text Checked W0 factorization Tested V convexity and verified V symmetry Derived V’s convexity conditions
									4174 container Subagent activity
										4175 container
											4176 button Principal projection
											4177 text  and 
											4178 button Principal construction
											4179 text  updated
									4180 text Derived transformed-coordinate action The convex companion’s gradient flow fails a necessary single-wave test, even though it passes the test at the most degenerate directions. I’ve found a different one-parameter correction that makes the relevant matrices commute at both critical backgrounds. I’m checking whether that corrected density is globally convex and whether its flow decreases the original energy. Diagonalized the Hopf form and checked Hessian convexity Derived the Hessian criterion and tested quartic convexity Derived convexity conditions Derived convexity conditions Checked convexity conditions Examined Hessian SOS structure and binary-quartic cones Tested binary quartic equivalence and checked polarization positivity Checked binary quartic convexity and canonical determinant coefficient Checked canonical convexity Derived Hessian bounds Tested convexity decomposition and checked k=1 convexity Checked convexity at k=1/3 Tested j²+σW convexity Tested J+σW convexity Tested pressure correction
							
