# Independent audit of the anisotropic polynomial criterion

Date: 16 October 2026, Australia/Brisbane.

Task scope: independently attack or prove the proposed weighted criterion; do not rely on agreement with the construction worker. No other worker output was read and no contact with the construction worker was made.

Repository pin supplied and checked locally: `f80a8f15137575133ad2c9af975513b32e8fa93e` in `/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016`.

Analytic input inspected: `../../originals/conformal_packet/RESEARCH_REPORT.md`, Sections 2.1–2.2. The proof below uses its finite-exponent mixed-derivative lemma, with an independent check of how its exponent restrictions enter the argument.

**Audit outcome:** the proposed equivalence is correct for real homogeneous polynomials of integer degree (m\ge3), every finite (1<p,s<\infty), and (0<\alpha\le m), subject to

\[
\frac{\alpha}{p}+\frac{m-\alpha}{s}=1.
\tag{A}
\]

There is no additional restriction within that finite-exponent regime. The same algebraic condition characterizes the signed integral estimate and the absolute (L^1) estimate. Their best constants need not agree. Degree two has a genuine signed null Lagrangian exception, and multiplying a determinant by a nonconstant gradient polynomial does not preserve that exception.

This is an internally derived proof of finite boundedness and its exact algebraic condition. It supplies no sharp constant for the conformal quartic problem, no quasiconvexity proof, and no historical-priority clearance. Infinite or (L^1) endpoint exponents are not covered by this audit's theorem.

## Exact statement

Let

\[
D\phi=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
q=\sigma a+d,\qquad T_\sigma\phi=(q,c),\qquad\sigma>0,
\]

for smooth periodic maps on the square two-torus. Norms and averages may use normalized measure, as in the supplied packet. Given a homogeneous polynomial (P) of degree (m\ge3), express it in the invertible linear coordinates ((a,b,c,q)). Assign

\[
\operatorname{wt}(b)=0,\quad\operatorname{wt}(a)=1,
\quad\operatorname{wt}(c)=\operatorname{wt}(q)=2.
\]

The following are equivalent:

1. Every nonzero monomial of (P(a,b,c,q-\sigma a)) has weight at least (2\alpha).
2. There is a finite (K) such that
   \[
   \|P(D\phi)\|_1\le K\|T_\sigma\phi\|_p^\alpha
                       \|D\phi\|_s^{m-\alpha}.
   \tag{B}
   \]
3. There is a finite (K') such that
   \[
   |\langle P(D\phi)\rangle|\le K'\|T_\sigma\phi\|_p^\alpha
                       \|D\phi\|_s^{m-\alpha}.
   \tag{C}
   \]

Constants may depend on (P,m,\sigma,p,s,\alpha), and are uniform over the map. For the zero polynomial all statements are immediate. For a nonzero polynomial, let (w_*(P)) be its smallest monomial weight. The largest admissible defect exponent, within the balanced finite-exponent regime, is exactly (w_*(P)/2).

For (0<\alpha<m), (A) already implies (p>\alpha) and (s>m-\alpha). Equivalently,

\[
s=\frac{p(m-\alpha)}{p-\alpha},\qquad p>\max\{1,\alpha\},
\]

with no upper restriction on (p) when (\alpha\le m-1), and with

\[
p<\frac{\alpha}{\alpha-m+1}
\]

when (m-1<\alpha<m). These are consequences of (1<p,s<\infty) and (A), not extra analytic hypotheses. When (\alpha=m), (A) gives (p=m), the right side has no full-gradient factor, and the criterion says that (P) is a homogeneous polynomial in (q,c) alone. Any finite (s>1) is then immaterial.

The particularly simple choice (p=s=m) is admissible for every (0<\alpha\le m). It gives the entire criterion in one Sobolev scale:

\[
\|P(D\phi)\|_1\le K\|T_\sigma\phi\|_m^\alpha
                       \|D\phi\|_m^{m-\alpha}
\quad\Longleftrightarrow\quad w_*(P)\ge2\alpha.
\]

## Sufficiency without hidden exponent assumptions

Put (A=\|T_\sigma\phi\|_p), (B=\|D\phi\|_s), and

\[
\frac1t=\frac12\left(\frac1p+\frac1s\right).
\]

The supplied mixed-derivative lemma and periodic Hodge decomposition give

\[
\|a\|_t^2\le C_{\sigma,p,s}AB.
\tag{D}
\]

Here is the exact argument. After subtracting irrelevant means, write

\[
(\sigma f,g)=\nabla\chi+(\psi_y,-\psi_x),\qquad\Delta\chi=q.
\]

Then

\[
\sigma a=\chi_{xx}+\psi_{xy},\quad
\sigma b=\chi_{xy}+\psi_{yy},\quad
c=\chi_{xy}-\psi_{xx}.
\]

Second-order Riesz bounds on finite (L^p,L^s) imply

\[
\|\psi_{xx}\|_p\le CA,\quad\|\psi_{yy}\|_s\le C_\sigma B,
\quad\|\chi_{xx}\|_p\le CA,\quad\|\chi_{xx}\|_s\le C_\sigma B.
\]

In particular, the (L^s) bound uses (\|q\|_s\le C_\sigma B), and does not require (p\le s). Apply the mixed-derivative lemma to (psi) and ordinary interpolation to (chi_{xx}). This proves (D). The source lemma's complex-interpolation proof applies to arbitrary finite (p,s>1): the intermediate exponent (t) is also strictly greater than one. It does not require an ordering of (p,s).

Each (a) factor can therefore carry any defect exponent (\beta\in[0,1/2]), while each (c) or (q) factor can carry any (\beta\in[0,1]). More explicitly, with

\[
\frac1{r_\beta}=\frac\beta p+\frac{1-\beta}s,
\]

interpolation gives

\[
\|a\|_{r_\beta}\le C A^\beta B^{1-\beta}\quad(0\le\beta\le1/2),
\]

and

\[
\|c\|_{r_\beta}+\|q\|_{r_\beta}
\le C_\sigma A^\beta B^{1-\beta}\quad(0\le\beta\le1).
\]

A (b) factor carries exponent zero and uses (L^s). A monomial (a^j b^k c^\ell q^n), of degree (m), has total available defect exponent

\[
\frac j2+\ell+n=\frac{\operatorname{wt}(a^j b^k c^\ell q^n)}2.
\]

If this is at least (\alpha), distribute (\alpha) among its factors within the displayed intervals. The sum of their reciprocal Lebesgue exponents is exactly (A), so Hölder gives (B) for the monomial. Every factor exponent is strictly greater than one since (p,s>1). Sum over the finitely many monomials. This proves (B), hence (C). If (A=0), (D) gives (a=0), while (c=q=d=0); the weighted condition makes (P) vanish on the remaining pure shear, so the zero-defect case is also included.

## Necessity from genuine periodic compatible fields

The following two-scale test permits an independent leading (q), which is necessary to test all weighted monomials rather than only the plane (q=0).

Fix arbitrary smooth periodic (psi,u,v). For an integer (N\ge1), set (\varepsilon=1/N) and

\[
\phi_N(x,y)=\left(
\varepsilon\psi_y(x,Ny)+\varepsilon^2u(x,Ny),
-\sigma\varepsilon^2\psi_x(x,Ny)+\varepsilon^3v(x,Ny)
\right).
\tag{E}
\]

Writing (Q=\sigma u_x+v_y), its actual derivatives are

\[
\begin{aligned}
a_N&=\varepsilon\psi_{xy}+\varepsilon^2u_x,&
b_N&=\psi_{yy}+\varepsilon u_y,\\
c_N&=-\sigma\varepsilon^2\psi_{xx}+\varepsilon^3v_x,&
d_N&=-\sigma\varepsilon\psi_{xy}+\varepsilon^2v_y,\\
q_N&=\varepsilon^2Q.
\end{aligned}
\tag{F}
\]

All functions on the right are evaluated at ((x,Ny)). Every smooth periodic mean-zero (Q) is available: solve (\Delta h=Q), and choose (u=h_x/\sigma), (v=h_y). Thus (Q) is independent of the Hessian of (psi).

The torus map ((x,y)\mapsto(x,Ny)) preserves normalized averages and all finite Lebesgue norms. Consequently

\[
\|T_\sigma\phi_N\|_p=O(\varepsilon^2),\qquad
\|D\phi_N\|_s=O(1).
\tag{G}
\]

Let (P_w\ne0) be the lowest weighted component of (P). Polynomial expansion of (F), uniformly on the torus, gives

\[
P(D\phi_N)=\varepsilon^w
 P_w(\psi_{xy},\psi_{yy},-\sigma\psi_{xx},Q)
 +O(\varepsilon^{w+1}).
\tag{H}
\]

If (w<2\alpha), the absolute estimate would force

\[
\|P_w(\psi_{xy},\psi_{yy},-\sigma\psi_{xx},Q)\|_1=0
\]

for every (psi,Q). Arbitrary Hessian and (Q) values can be prescribed on a small open patch using a quadratic polynomial times a cutoff and a separate correction to the mean of (Q). Since the coordinate substitution is invertible, a nonzero (P_w) is nonzero on one such patch. This contradicts the displayed conclusion and proves absolute necessity.

For the signed estimate, (G)–(H) instead force

\[
\langle H(\psi_{xx},\psi_{xy},\psi_{yy},Q)\rangle=0
\quad\text{for every smooth periodic (psi) and mean-zero (Q)},
\tag{I}
\]

where (H(U,V,Z,Q)=P_w(V,Z,-\sigma U,Q)) is a nonzero homogeneous polynomial of ordinary degree (m). The following elementary null-polynomial argument rules this out for (m\ge3).

First vary (Q) by an arbitrary smooth mean-zero function. Equation (I) implies that (H_Q(D^2\psi,Q)) is spatially constant. Arbitrary values of (D^2\psi,Q) can be realized in two disjoint patches of the same map, with a third patch correcting the mean of (Q). Hence (H_Q) is a constant polynomial in all four variables. Its homogeneous degree is (m-1\ge1), so that constant is zero. Therefore (H) is independent of (Q).

Now vary (psi) and integrate by parts twice. The Euler–Lagrange identity is

\[
\partial_{xx}H_U+\partial_{xy}H_V+\partial_{yy}H_Z=0.
\]

At a point, prescribe an arbitrary Hessian, zero third derivatives, and arbitrary fourth derivatives. Their independent coefficients give

\[
H_{UU}=H_{UV}=H_{VZ}=H_{ZZ}=0,\qquad H_{VV}+2H_{UZ}=0.
\tag{J}
\]

Solving these polynomial equations yields exactly

\[
H(U,V,Z)=\lambda(UZ-V^2)+\beta U+\gamma V+\delta Z+\eta.
\tag{K}
\]

For completeness, (H_{UU}=H_{UV}=0) gives (H=U A(Z)+B(V,Z)); (H_{ZZ}=H_{VZ}=0) gives (A(Z)=\lambda Z+\beta) and (B=C(V)+\delta Z); the last equation in (J) gives (C(V)=-\lambda V^2+\gamma V+\eta). A homogeneous polynomial of degree (m\ge3) in (K) must be zero. This contradicts the nonzero (P_w), and proves signed necessity.

This proof constructs compatible periodic gradients throughout. It does not substitute a freely prescribed matrix-valued field for a gradient.

## Degree two and the failure of determinant multiplication

The exact signed exception at degree two is the determinant:

\[
\det D\phi=a q-\sigma a^2-bc,\qquad
\langle\det D\phi\rangle=0.
\]

Its lowest weight is two, but its signed integral is zero for every map, including when (2\alpha>2). More generally, the degree-two signed criterion is the weighted criterion **modulo a scalar multiple of the determinant**: there must exist (lambda) such that (P-\lambda\det) has only weights at least (2\alpha). The same leading-component proof establishes this, since the only nonzero homogeneous degree-two polynomial in (K) is the Hessian determinant. Subtracting the corresponding full gradient determinant removes that leading component, after which the proof continues. The absolute criterion has no such quotient.

There can be a signed gain even for a density that is not itself null. For example,

\[
P=-\sigma a^2-bc=\det D\phi-aq
\]

has weight two, while its signed integral is (-\langle aq\rangle). At (p=s=2), (D) gives a signed estimate with (\alpha=3/2). Its absolute estimate with that exponent fails.

The degree-two exception does not extend by polynomial multiplication. For the explicit periodic potential

\[
\psi=-\cos(x+y)-\cos y-\tfrac12\cos(x+2y),
\]

exact Fourier algebra gives

\[
\langle\psi_{yy}\det D^2\psi\rangle=\frac34.
\]

Taking (u=v=0) in (E), one obtains

\[
\langle b_N\det D\phi_N\rangle=\frac{3\sigma}{4N^2},
\qquad\|T_\sigma\phi_N\|_p=O(N^{-2}),\quad
\|D\phi_N\|_s=O(1).
\]

Thus the cubic (b\det D\phi) fails every proposed estimate with (\alpha>1), including the balanced basic choice (p=s=3), (\alpha=3/2). Its determinant factor does not make its integral null. The general argument (I)–(K) excludes every higher-degree null exception, not merely this example.

## Reproduction and limits

Run:

```sh
python3 verify_weighted_audit.py
```

The standard-library script passed **265 exact checks** and wrote `VERIFICATION_RECEIPT.json`. It checks the homogeneous systems (J), with (H_Q=0), in degrees two through eight using rational row reduction: degree two has the one-dimensional determinant kernel; degrees three through eight have zero kernel. It also checks exact compatible Fourier fields with an independently chosen (Q), determinant means, the packet's (ab^2) witness, a nonzero (a^3) witness, the cubic determinant-product obstruction, and representative rational exponent allocations.

The finite ranks corroborate the general proof (J)–(K); they do not replace it. The script does not machine-formalize Hodge theory, the mixed-derivative interpolation lemma, arbitrary smooth jets, or the variational argument.

The proof first concerns smooth maps. For the natural mixed space (D\phi\in L^s), (T_\sigma\phi\in L^p), strong periodic convolution approximation and (D) give convergence in all factor spaces used above, hence (L^1) convergence of the selected monomials. This extends the absolute and signed estimates to that space. When (p=s=m), this is the ordinary periodic (W^{1,m}) class.

No endpoint (p=1,s=1,p=\infty,s=\infty) claim is made here. The supplied complex-interpolation and Riesz argument uses finite exponents strictly greater than one. Some individual endpoint cases can have separate proofs; their omission is a precise scope boundary, not a claim of endpoint failure.

For (m=3,\alpha=1), the weighted condition removes exactly (b^3) and (ab^2), recovering the supplied 18-dimensional cubic space and its finite ((p,s)=(2,4)) estimate. The audit therefore confirms a strict generalization in degree and defect exponent while leaving the sharp positive-core inequality unresolved.
