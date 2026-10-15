# Independent audit: quadratic compatible-Hessian nulls and coefficient blow-up

Date: 2026-10-15. Worker: `smooth_null_classification`.

**Status:** internally derived analytic arguments and exact finite algebra checks. No external mathematical review, formal proof verification, historical novelty, PDE well-posedness, physical demonstration, or practical capability is certified.

The incoming planar two-output C² claims are valid under their stated global coefficient and all-background hypotheses. The classification extends to arbitrary output dimension and continuous coefficients, with closedness interpreted distributionally. The coefficient blow-up extends to arbitrary spatial/output dimensions, arbitrary constant output generators, and a second-order Peano coefficient expansion at the origin. Positive output diffusion alone does not imply dissipation of convex quartics. Higher spatial dimensions require representation gauges; the unique planar two-form statement cannot be copied unchanged.

## 1. Inputs and independence

Read the supplied `sources/astra_compatible_heat_result/RESEARCH_REPORT.md`, especially Propositions 2–3, and `verify_structure.py`. The proof below is reconstructed independently in column-major coordinates; `checks.py` neither imports nor executes the incoming verifier. The prior repository obstruction proof was not used as a premise. Repository HEAD was observed as `33c1ff7ebd9411e9b8b4b0f951f62e36e631cb5d`. No repository files were changed by this worker; outputs are confined to this worker directory.

The task contract is classification and internal audit of a local variational-certificate class. It is not a claim that all null corrections, all heat mechanisms, all quasiconvexity arguments, or all physical realizations have been classified.

## 2. Planar classification for every output dimension

Let the spatial variables be `(x,y)`, let `u:R²→R^m`, and use matrix coordinates

\[
 A=(p,q)=(u_x,u_y)\in V=\mathbb R^m\oplus\mathbb R^m.
\]

Write the compatible Hessian as `H=(X,Y,Z)=(u_xx,u_xy,u_yy)` and set

\[
 U(H)=(X,Y),\qquad V(H)=(Y,Z).
\]

The reuse of the letter `V` for the matrix space and the second tangent vector is avoided below by writing the latter as `V(H)`.

**Planar theorem.** Suppose `N(A,H)` has continuous coefficients in `A∈R^{2m}` and is homogeneous quadratic in `H`. Then

\[
 \int_{\mathbb R^2}N(B+Du,D^2u)=0
 \quad\text{for every }B\in\mathbb R^{m\times2},\ u\in C_c^\infty(\mathbb R^2;\mathbb R^m)
 \tag{2.1}
\]

if and only if there is a unique continuous two-form `ω` on `R^{2m}` satisfying

\[
 N(A,H)=\omega_A(U(H),V(H)),\qquad d\omega=0
 \tag{2.2}
\]

in the sense of distributions. If the coefficients are `C^r`, so are the form coefficients. For `C^1` coefficients the closedness condition is classical. The same statement holds on a ball about a matrix background for perturbations whose gradient images stay in that ball. On a general coefficient domain, necessity is local; sufficiency additionally needs an exact form or a null-homotopic gradient-image map. The global Euclidean and local-ball statements avoid this topological qualification.

### 2.1 Freezing and the constant-symbol kernel

Fix `A=B`, a target vector `a`, a spatial vector `ξ≠0`, and a cutoff `χ`. Put

\[
 u_k(x)=k^{-2}a\,\chi(x)\cos(k\xi\cdot x).
\]

Its gradient tends uniformly to zero, while

\[
 D^2u_k=-a\otimes\xi^{\otimes2}\,\chi\cos(k\xi\cdot x)+O(k^{-1}).
\]

Continuity of coefficients, quadraticity in `H`, and the oscillatory average of `cos²` in (2.1) give

\[
 N(B,a\otimes\xi^{\otimes2})=0.
 \tag{2.3}
\]

Thus every frozen coefficient quadratic lies in the kernel of

\[
 \operatorname{Sym}^2(\mathbb R^m\otimes\operatorname{Sym}^2\mathbb R^2)^*
 \longrightarrow
 \operatorname{Sym}^2(\mathbb R^m)^*\otimes\operatorname{Sym}^4(\mathbb R^2)^*.
\]

This map is surjective: for each output monomial `a_i a_j`, products of the three spatial monomials `ξ_x²,ξ_xξ_y,ξ_y²` span all five quartic spatial monomials. Therefore its kernel dimension is

\[
 \frac{3m(3m+1)}2-\frac{5m(m+1)}2
 =m(2m-1)=\binom{2m}{2}.
 \tag{2.4}
\]

The pullback of a constant two-form vanishes on the symbol jets because `U` and `V(H)` are proportional there. The pullback map is injective: write a form in `pp,pq,qq` blocks. Its `pp` coefficients appear uniquely in `X_iY_j-X_jY_i`, its arbitrary `pq` matrix appears uniquely in `X_iZ_j`, and its `qq` coefficients appear uniquely in `Y_iZ_j-Y_jZ_i`. The source and kernel dimensions agree, so this identifies the full kernel and yields a unique form with the same coefficient regularity.

For `m=2`, reordering back to the incoming row-major Hessian coordinates gives exactly its six displayed minors, with possible basis signs. No additional constant-symbol directions exist.

### 2.2 Closedness from extreme third jets

First take smooth coefficients and put `T=dω`. Cartan's variation formula, followed by compact-support Stokes, gives

\[
 \delta I[u](\eta)
 =\int T_A(D\eta,U,V(H)).
\]

Let `e_{p_i},e_{q_i}` be the coordinate vectors. The Euler equation for `η_i` is

\[
 \partial_x\{T(e_{p_i},U,V(H))\}
 +\partial_y\{T(e_{q_i},U,V(H))\}=0.
 \tag{2.5}
\]

At an arbitrary fixed local jet, the coefficient of the independently prescribable third derivative `u^j_xxx` is

\[
 T(e_{p_i},e_{p_j},V(H)).
\]

Since `V(H)=(Y,Z)` can be any vector, every component of `T` containing two `p` coordinates vanishes. Similarly, the coefficient of `u^j_yyy` is

\[
 T(e_{q_i},U,e_{q_j}),
\]

so every component containing two `q` coordinates vanishes. Every triple of `p/q` coordinates contains two of one kind. Consequently `T=0`, for every `m`. Terms differentiating the coefficients of `T` contain only second jets and cannot cancel these third-jet coefficients. Arbitrary local jets can be embedded in compactly supported fields; reducing the support radius keeps the gradient within any prescribed neighborhood of its background.

This proves the result for smooth coefficients without the incoming four-selected-monomial calculation.

### 2.3 Removing differentiability by coefficient convolution

Convolve coefficients only in matrix space:

\[
 N_\varepsilon(A,H)=\int\rho_\varepsilon(h)N(A-h,H)\,dh.
\]

Every shifted background `B-h` is allowed in (2.1); Fubini therefore preserves the null identity for `N_ε`. It is smooth, and its associated form is `ω_ε=ρ_ε*ω`. The preceding proof gives `dω_ε=0`. Local uniform convergence gives `dω=0` distributionally. Conversely, a continuous distributionally closed form can be convolved, the smooth closed forms are exact on Euclidean space (or a ball), and their pullback integrals vanish. Local uniform convergence then gives (2.1).

Continuity is sufficient for the ordinary pointwise-coefficient formulation. Differentiating a merely continuous form directly in (2.5) would not be justified; convolution supplies the missing step.

## 3. Distribution coefficients: a legitimate weaker formulation

There is also a clean distribution version, but its null identity must be formulated in the affine background variable. Let the coefficients of `N` be distributions on matrix space. For fixed compactly supported `u`, define the background distribution

\[
 \mathcal I_u(B)=\int N(B+Du(x),D^2u(x))\,dx
\]

by translating each coefficient distribution and weighting it by the smooth compactly supported quadratic Hessian monomials. Explicitly, if `N=Σc_rs(A)H_rH_s`, its pairing with `ψ(B)` is

\[
 \langle\mathcal I_u,\psi\rangle
 =\sum_{r,s}\int H_r(x)H_s(x)
 \langle c_{rs},\psi(\cdot-Du(x))\rangle\,dx.
\]

Then `I_u=0` as a distribution for every `u` is equivalent to a unique distribution-coefficient two-form representation with `dω=0`. Proof: convolve, apply Section 2, and pass to the distribution limit in either direction. The algebraic inverse from null quadratics to form coefficients is fixed and linear, so it commutes with convolution and limits.

For `L¹_loc` coefficients, this is the averaged-in-background identity and gives a classification modulo almost-everywhere equality. It does not provide a canonical value on coefficient null sets or a pointwise positivity inequality. No positivity or physical-interpretation claim is attached to distribution coefficients.

## 4. Homogenization requires no two-form classification

Let now `n,m` be arbitrary, set

\[
 \mathcal A=\mathbb R^{m\times n},\qquad
 \mathcal J=\mathbb R^m\otimes\operatorname{Sym}^2\mathbb R^n,
\]

and let `N(A,H)` be continuous in `A` and quadratic in `H`, with local null identities for all affine backgrounds near zero. Suppose its coefficients have the second-order Peano expansion

\[
 N(A,H)=N_0(H)+N_1(A,H)+N_2(A,H)+o(|A|^2)|H|^2,
 \tag{4.1}
\]

where `N_j` is polynomial homogeneous of degree `j` in `A`. This requires a second-order coefficient jet at the origin; C² on a neighborhood is stronger than necessary.

Let `P(A,H)` be quadratic in `H` and satisfy

\[
 P(A,H)=P_2(A,H)+o(|A|^2)|H|^2,
 \tag{4.2}
\]

with `P_2` homogeneous quadratic in `A`. Assume

\[
 P(A,H)+N(A,H)\ge0
 \quad\text{for all }H\text{ and all }A\text{ near zero}.
 \tag{4.3}
\]

**Homogenization theorem.** Then `N_0=N_1=0`, `N_2` is a global quadratic-Hessian null Lagrangian, and

\[
 P_2(A,H)+N_2(A,H)\ge0
 \quad\text{for every }A,H.
 \tag{4.4}
\]

In the planar case `N_2` therefore has a unique homogeneous-quadratic closed two-form representation. For a fixed heat generator and homogeneous quartic `F`, `P=P_2` exactly. For a genuinely quasilinear principal coefficient continuous at zero, the theorem applies whenever the actual integrated dissipation has the expansion (4.2); freezing a coefficient in an incorrect dissipation expression is not covered.

### 4.1 The only algebra needed

The high-frequency argument of Section 2 works for all `n,m`, so each frozen `N(A,·)` vanishes on every pure Hessian symbol `a⊗ξ²`. These symbols span `J`: use each output basis vector and spatial vectors `e_i` and `e_i+e_j`; subtracting the two diagonal tensors isolates each symmetric off-diagonal basis tensor.

A positive semidefinite quadratic form vanishing on a spanning set is zero. At `A=0`, (4.2) and (4.3) therefore give `N_0=0`. Dividing (4.3) at `tA` by `t>0` and passing to zero makes `N_1(A,·)` positive semidefinite. It still vanishes on pure symbols, hence is zero. Dividing instead by `t²` gives (4.4), for arbitrary fixed `A,H`. The two-sided `±t` argument in the incoming proof is another valid way to eliminate `N_1`.

### 4.2 The quadratic coefficient is fully null

For arbitrary `B` and compactly supported `u`, the scaled background and field fit within the local coefficient ball for sufficiently small `t`. Their null identity is

\[
 0=\int N(t(B+Du),tD^2u).
\]

Using `N_0=N_1=0` and (4.1), divide by `t⁴` and pass to the limit on the compact support. This yields

\[
 \int N_2(B+Du,D^2u)=0.
\]

This proves full nullness, rather than only constant-symbol vanishing. In two dimensions, Section 2 forces closedness of its associated form. Equivalently, rescaled closed form coefficients converge locally uniformly to their quadratic Peano part, and distributional closedness passes to that limit.

The proof uses neither ellipticity, output symmetry, a Gram/SOS representation, nor a planar form classification. It needs the genuine quadratic principal scaling (4.2), an actual null correction, and positivity on all compatible Hessian jets.

## 5. What continuity and positivity do without a second jet

Let `L⊂Sym²(J*)` be the finite-dimensional space of symbol-null quadratics. The span argument gives

\[
 L\cap\mathrm{PSD}=\{0\}.
\]

Compactness of its unit sphere gives a constant `c>0` such that

\[
 \lambda_{\min}(M)\le-c\|M\|\quad(M\in L).
\]

If `P(A)+N(A)` is positive semidefinite, the eigenvalue bound implies

\[
 \|N(A)\|\le c^{-1}\|P(A)\|=O(|A|^2).
 \tag{5.1}
\]

Thus continuity plus positivity already suppresses coefficient orders below two. It does not create a polynomial second-order jet.

An exact boundary example is the scalar planar form

\[
 \omega=p\sqrt{p^2+q^2}\,dp\wedge dq.
 \tag{5.2}
\]

It is closed, since the coefficient space is two-dimensional. Its coefficients are C¹,¹: away from zero the coefficient Hessian entries are `3p/r-p³/r³`, `q³/r³`, and `p³/r³`, which are uniformly bounded, and its gradient extends continuously to zero. Yet no quadratic Peano polynomial exists: its values on opposite unit directions are opposite, while a quadratic polynomial has equal values there.

For `F(p,q)=(p²+q²)²` and ordinary heat, the heat density is

\[
 4|A|^2|H|_F^2+8|HA|^2.
\]

Since `|p sqrt(p²+q²)|≤|A|²` and `|det H|≤|H|_F²/2`, adding the correction in (5.2) leaves density at least

\[
 \frac72|A|^2|H|_F^2\ge0.
\]

This is a C¹,¹ closed admissible correction with no quadratic Taylor part. It shows why the coefficient-expansion hypothesis cannot simply be omitted from the Taylor-extraction statement. **It does not separate certificate cones:** the zero correction already works for this convex `F`. No claim that angular corrections enlarge the polynomial feasibility cone has been proved here.

## 6. Input anisotropy and output generators

For the constant system

\[
 u_t=\sum_{i,j}M_{ij}u_{ij},\qquad M_{ij}=M_{ji}\in\mathbb R^{m\times m},
\]

let `B_i=∂_i A`. One spatial integration by parts gives the actual fixed-coefficient heat density

\[
 Q_{M,F}(A,H)=
 \sum_{i,j}B_i^T D^2F(A)(M_{ij}\otimes I_n)B_j.
 \tag{6.1}
\]

For homogeneous quartic `F` it is quadratic in `A` and `H`, even if the output matrices are nonsymmetric. Consequently Section 4 applies unchanged. The spatial antisymmetric coefficient part has no effect on `u_ij`; an output skew part generally does affect (6.1), because it need not commute with `D²F`.

If `M_ij=D_ij I_m` with `D` symmetric positive semidefinite, every convex `F` gives a nonnegative density by the positive semidefinite tensor contraction. This includes all scalar-output anisotropic heat generators.

### 6.1 Exact counterexamples to unrestricted output extension

Take `n=m=2`, `u_t=MΔu`, the convex homogeneous quartic `F(A)=A_11⁴`, and a background with `A_11=1`. For the pure Hessian `H=a⊗e_1²`, the two tangent columns are `B_1=a⊗e_1`, `B_2=0`, and

\[
 Q_{M,F}=12(e_1\cdot a)(e_1\cdot Ma).
\]

The following exact choices both give `Q=-12`:

\[
 M=\begin{pmatrix}1&1/2\\1/2&1\end{pmatrix},\ a=(1,-4);
 \qquad
 M=\begin{pmatrix}1&-1\\1&1\end{pmatrix},\ a=(1,2).
\]

The first `M` is positive definite. The second has symmetric part `I`, so its constant system is strongly parabolic in the usual symmetric-part sense. Every quadratic-Hessian null correction vanishes on this pure symbol and cannot remove the negative value. Strong parabolicity does not imply dissipation of every convex quartic.

### 6.2 A sharp universal boundary

Require a constant generator to admit pointwise nonnegative corrected dissipation for **every convex homogeneous quartic**, allowing a separate quadratic-Hessian null correction for each quartic. Testing

\[
 F(A)=(v\cdot A\xi)^4
\]

at a background with `v·Aξ=1` and on `a⊗ξ²` forces

\[
 (v\cdot a)(v\cdot M(\xi)a)\ge0
 \quad\text{for every }v,a,
 \qquad M(\xi)=\sum_{i,j}\xi_i\xi_jM_{ij}.
 \tag{6.2}
\]

For fixed nonzero `v`, two linear functionals have product nonnegative everywhere only if they are nonnegative scalar multiples. Hence `M(ξ)^T v=λ_v v` for every `v`. Applying this to basis vectors and their sums gives `M(ξ)=λ(ξ)I` with `λ(ξ)≥0`. Comparing the quadratic polynomial coefficients in `ξ` gives `M_ij=D_ij I` with `D≥0`. The converse was proved above. Under strong parabolicity, `D` is positive definite.

Therefore universal convex-quartic preservation in this pointwise-certificate class is exactly scalar-output anisotropic heat. This is a statement about universal preservation; it does not forbid a non-scalar generator from dissipating a particular appropriately matched integrand.

## 7. The higher-spatial-dimension representation boundary

For `n>2`, a two-form pulls back to a spatial two-form rather than directly to an `n`-dimensional density. A natural quadratic-minor representation is

\[
 N(A,H)=\sum_{i<j}\omega_A^{ij}(\partial_i A,\partial_j A),
\]

but its coefficient forms need not be unique. For a scalar field in three dimensions, write `p=Du` and `H=D²u`. The nonzero constant pair forms

\[
 \omega^{12}=dp_1\wedge dp_3,
 \qquad \omega^{13}=-dp_1\wedge dp_2
\]

give identically zero density, because

\[
 (H_{11}H_{23}-H_{13}H_{12})
 -(H_{11}H_{23}-H_{12}H_{13})=0.
\]

Even closedness of an arbitrarily chosen representative is not necessary. The density

\[
 N=p_3(H_{11}H_{22}-H_{12}^2)
\]

has the nonclosed single representative `ω^{12}=p_3 dp_1∧dp_2`, but the same density is represented by the closed pair

\[
 \widetilde\omega^{12}=dp_1\wedge d(p_2p_3),
 \qquad
 \widetilde\omega^{13}=-p_2dp_1\wedge dp_2.
\]

Both are exact; integrating their spatial pullback components gives zero for compact perturbations. Thus the density is indeed null. This refutes a higher-dimensional statement demanding each chosen pair form be closed, while leaving open the correct existence classification modulo the representation kernel.

The general constant-symbol kernel dimension, obtained by the same surjective symbol map, is

\[
 \binom{d+1}{2}-\binom{m+1}{2}\binom{n+3}{4},
 \qquad d=m\binom{n+1}{2}.
\]

For `n=3,m=1` it is six, whereas the pair-form coefficient count is nine. The planar unique-two-form argument is therefore special. The general homogenization theorem in Section 4 survives these gauges because it operates directly on densities.

## 8. Primary-source comparison and priority scope

Ball, Currie, and Olver, *Null Lagrangians, Weak Continuity, and Variational Problems of Arbitrary Order*, JFA 41 (1981), 135–174: Theorem 3.4 gives equivalent nullness conditions for continuous derivative-only integrands; Theorem 4.1 identifies them as affine combinations of higher-order Jacobians. Example 4.10(d), printed page 155, explicitly lists the same six independent quadratic planar two-output Hessian minors. Thus the six-dimensional constant-coefficient classification is already in the primary literature. The theorem itself concerns dependence solely on the highest derivative and cannot be quoted alone as the proof of the coefficient-dependent constrained-gradient closedness step. [Author-hosted full text](https://www-users.cse.umn.edu/~olver/e_/bco.pdf).

Olver and Sivaloganathan, *The structure of null Lagrangians*, Nonlinearity 1 (1988), 389–398: Proposition 2, Lemma 5, and Theorems 7–8 relate variable-coefficient minor expansions, closed differential forms, divergences, and potentials for first-order null Lagrangians. The introduction explicitly discusses higher-order generalization. Their first-order map is unrestricted; simply substituting `A=Du` does not establish the converse needed here. Section 2 supplies that constrained converse directly. This is a specialized reconstruction within an established framework, with no priority claim. [Author-hosted full text](https://www-users.cse.umn.edu/~olver/e_/null.pdf).

Olver, *Conservation laws and null divergences*, Math. Proc. Camb. Phil. Soc. 94 (1983), 529–540: Theorems 2.4, 3.1 and the coefficient-freezing discussion in Section 4 provide broader divergence and Jacobian context. [Author-hosted full text](https://www-users.cse.umn.edu/~olver/e_/clnd.pdf). Olver's sequel, *II. Non-negative divergences*, 97 (1985), 511–514, Theorem 1 shows that an everywhere nonnegative smooth divergence reduces to a function of the independent variables; its null-Lagrangian discussion is consistent with the elementary `L∩PSD={0}` argument used here. [Author-hosted full text](https://www-users.cse.umn.edu/~olver/e_/clnd2.pdf).

All four primary texts were inspected through their author-hosted PDFs. The proofs above stand separately. Inspection does not establish that the extensions are historically new or that the cited papers fail to contain a theorem implying them.

## 9. Exact checks and unresolved boundaries

Run `python3 checks.py` in this directory. The script checks, over exact rationals, the symbol-map ranks, injective pullback ranks, and extreme-third-jet closedness ranks for `m=1,…,6`; pure-symbol spanning in several spatial/output dimensions; both output-generator witnesses; the three-dimensional representation gauge and closed replacement; and algebra in the C¹,¹ boundary example. `CHECKS.json` records the results and script hash. The dimension-uniform arguments are the proofs in this note, not an extrapolation from six finite cases.

Unresolved here: whether continuous/angular non-Peano corrections can strictly enlarge the polynomial certificate cone for a nonconvex quartic; the full variable-coefficient null representation modulo gauges in general spatial dimension; singular/nonlocal/higher-jet corrections; positivity only along a restricted orbit; and any global dynamical or variational completeness claim. The output-generator examples establish failure for those explicit generator/integrand pairs, not failure of quasiconvexity of their convex integrands.
